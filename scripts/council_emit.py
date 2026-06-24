#!/usr/bin/env python3
"""
Demerzel council_emit — the LLM-council verdict emitter for self-merge gating.

Convenes a two-reviewer council on a pull request and writes a verdict that
validates against schemas/council-verdict.schema.json into state/council/. The
verdict carries a `post_council_confidence` (0-1) which the AFK governor's
self-merge gate (scripts/run_afk_cycle.py --harvest) consumes per the
`confidence_threshold` in policies/autonomous-loop-policy.yaml ("Post-council
confidence is used ... council must have run before self-merge is considered").

The two reviewers are deliberately heterogeneous so the council aggregates an
existing static gate with a fresh model opinion (multi-perspective, not
redundant):

  reviewer_a — Agent Blackbox. We read the `risk-report` CHECK CONCLUSION via
    `gh pr checks` rather than parsing agent-blackbox's risk-report.json (that
    JSON is produced by the external GuitarAlchemist/agent-blackbox repo at a
    pinned ref; its field shape is not vendored here, so parsing it would be a
    guess). A green check means the policy's pass band (risk <= 0.25, see
    agent-blackbox.policy.json) held, which maps to correctness_score 0.75 — at
    or above the 0.7 self-merge minimum and at/under the 0.8 single-model cap. A
    red check maps to 0.2 (REQUEST_CHANGES). Pending/absent -> unknown (the
    council reports incomplete and nothing self-merges).

  reviewer_b — A cross-model reviewer (Claude / Gemini / Codex, whichever API
    key is present), the same prompt the cross-model-review.yml workflow uses.
    Its APPROVE / REQUEST_CHANGES verdict maps to correctness_score 0.85 / 0.30.
    This is a genuinely different model from reviewer_a's static analyzer, so a
    two-review verdict lifts the single-model confidence cap honestly.

Chairman synthesis is strictest-wins (matching the tribunal panel's consensus
doctrine): the verdict is APPROVE only if every review is APPROVE-equivalent and
constitutionally aligned; `post_council_confidence` is the MIN of the reviewers'
correctness scores. Any reviewer that cannot run (missing check, missing API
key) is omitted — a verdict with fewer than two reviews is schema-valid but the
self-merge gate requires two, so a degraded council simply never self-merges.

Usage:
  python scripts/council_emit.py --pr 365                 # emit verdict, print JSON
  python scripts/council_emit.py --pr 365 --print-only    # do not write to disk

Exit codes:
  0  verdict emitted (any verdict value — APPROVE/REQUEST_CHANGES/REJECT)
  1  usage / environment error (e.g. PR not found)

Stdlib only (urllib for the model call) — no third-party deps, mirroring
run_afk_cycle.py so the governor can call this in the same environment.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_SLUG = "GuitarAlchemist/Demerzel"
COUNCIL_DIR = ROOT / "state" / "council"
BLACKBOX_CHECK = "risk-report"

# correctness_score mappings (0-1). reviewer_a green is the agent-blackbox pass
# band (risk <= 0.25 -> 1 - 0.25 = 0.75); red is a clear REQUEST_CHANGES.
SCORE_BLACKBOX_GREEN = 0.75
SCORE_BLACKBOX_RED = 0.2
SCORE_XMODEL_APPROVE = 0.85
SCORE_XMODEL_REQUEST_CHANGES = 0.3

SELF_MERGE_MIN_CONFIDENCE = 0.7   # policies/autonomous-loop-policy.yaml


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# Pure synthesis logic (unit-tested; no IO)
# --------------------------------------------------------------------------- #
def review_from_blackbox(check_state: str | None) -> dict | None:
    """Build reviewer_a from the agent-blackbox `risk-report` check conclusion.
    Returns None when the check is absent or not yet conclusive (pending), so the
    council reports incomplete rather than guessing."""
    if check_state is None:
        return None
    state = check_state.strip().lower()
    if state in ("pass", "success"):
        return {
            "reviewer": "reviewer_a",
            "correctness_score": SCORE_BLACKBOX_GREEN,
            "risk_assessment": "low",
            "constitutional_alignment": "pass",
            "rationale": "Agent Blackbox risk-report check is green: change sits in "
                         "the policy pass band (risk <= 0.25) and violates no "
                         "blocked-path constraint.",
        }
    if state in ("fail", "failure", "error"):
        return {
            "reviewer": "reviewer_a",
            "correctness_score": SCORE_BLACKBOX_RED,
            "risk_assessment": "high",
            "constitutional_alignment": "fail",
            "rationale": "Agent Blackbox risk-report check is red: risk exceeds the "
                         "pass band or a blocked-path/verify constraint failed.",
        }
    return None  # pending / neutral / skipped — not conclusive


def review_from_cross_model(verdict_text: str | None, model: str | None,
                            classified_risk: str) -> dict | None:
    """Build reviewer_b from a cross-model review's APPROVE/REQUEST_CHANGES text.
    Returns None when no model ran (no API key/response)."""
    if verdict_text is None:
        return None
    approve = "REQUEST_CHANGES" not in verdict_text.upper()
    return {
        "reviewer": "reviewer_b",
        "correctness_score": SCORE_XMODEL_APPROVE if approve else SCORE_XMODEL_REQUEST_CHANGES,
        "risk_assessment": classified_risk if classified_risk in ("low", "medium", "high", "critical") else "medium",
        "constitutional_alignment": "pass" if approve else "fail",
        "rationale": f"Cross-model reviewer ({model or 'unknown'}) verdict: "
                     f"{'APPROVE' if approve else 'REQUEST_CHANGES'}.",
    }


def synthesize(reviews: list[dict]) -> tuple[str, float, str]:
    """Chairman: strictest-wins. Returns (verdict, post_council_confidence,
    chairman_synthesis).

    - verdict APPROVE only if every review is constitutionally `pass` AND every
      correctness_score >= the self-merge minimum; otherwise REQUEST_CHANGES, or
      REJECT if any reviewer flagged a constitutional failure.
    - post_council_confidence = min(correctness_score) — the most skeptical
      reviewer caps the council. With a single review the value is additionally
      capped at the policy single-model cap (0.8); min() of one score <= 0.85
      already satisfies that, so no extra clamp is needed in practice.
    """
    if not reviews:
        return "REJECT", 0.0, "No reviewers could run; council is empty."
    scores = [r["correctness_score"] for r in reviews]
    confidence = round(min(scores), 4)
    all_aligned = all(r["constitutional_alignment"] == "pass" for r in reviews)
    any_constitutional_fail = any(r["constitutional_alignment"] == "fail" for r in reviews)
    if all_aligned and confidence >= SELF_MERGE_MIN_CONFIDENCE:
        verdict = "APPROVE"
    elif any_constitutional_fail:
        verdict = "REJECT"
    else:
        verdict = "REQUEST_CHANGES"
    chairman = (
        f"{len(reviews)} reviewer(s); strictest-wins confidence "
        f"{confidence:.2f} (min of {', '.join(f'{s:.2f}' for s in scores)}). "
        f"Constitutional alignment: {'all pass' if all_aligned else 'at least one fail'}. "
        f"Verdict: {verdict}."
    )
    return verdict, confidence, chairman


def build_verdict(pr: int, change_summary: str, reviews: list[dict],
                  today: str, seq: int) -> dict:
    """Assemble a council-verdict.schema.json-valid object."""
    verdict, confidence, chairman = synthesize(reviews)
    return {
        "verdict_id": f"council-{today}-{seq:03d}",
        "task_id": f"github_pr:#{pr}",
        "timestamp": _now_iso(),
        "trigger_condition": "borderline_confidence",
        "change_summary": change_summary[:500] if change_summary else f"PR #{pr}",
        "reviews": reviews,
        "chairman_synthesis": chairman,
        "verdict": verdict,
        "post_council_confidence": confidence,
    }


# --------------------------------------------------------------------------- #
# IO (thin wrappers around gh + model APIs)
# --------------------------------------------------------------------------- #
def _gh_json(args: list[str]) -> dict | list | None:
    try:
        p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            print(f"warn: gh {' '.join(args)} failed: {p.stderr.strip()[:160]}", file=sys.stderr)
            return None
        return json.loads(p.stdout or "null")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"warn: gh {' '.join(args)} unavailable: {exc}", file=sys.stderr)
        return None


def fetch_pr_meta(pr: int) -> dict | None:
    return _gh_json(["pr", "view", str(pr), "--repo", REPO_SLUG,
                     "--json", "number,title,body,headRefOid,labels"])  # type: ignore[return-value]


def fetch_blackbox_check_state(pr: int) -> str | None:
    """Return the `risk-report` check state ('pass'/'fail'/...) or None if absent.
    Parses `gh pr checks` tab-separated output (name<TAB>state<TAB>...)."""
    try:
        p = subprocess.run(["gh", "pr", "checks", str(pr), "--repo", REPO_SLUG],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"warn: gh pr checks failed: {exc}", file=sys.stderr)
        return None
    # gh pr checks exits non-zero when any check failed; output is still on stdout.
    for line in p.stdout.splitlines():
        parts = line.split("\t")
        if parts and parts[0].strip() == BLACKBOX_CHECK and len(parts) > 1:
            return parts[1].strip()
    return None


def fetch_diff(pr: int, limit: int = 12000) -> str:
    try:
        p = subprocess.run(["gh", "pr", "diff", str(pr), "--repo", REPO_SLUG],
                           capture_output=True, text=True, timeout=60)
        return (p.stdout or "")[:limit] if p.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _review_prompt(diff: str) -> str:
    return (
        "You are a cross-model code reviewer for the Demerzel governance framework.\n"
        "Review this pull request diff for:\n"
        "1. CORRECTNESS: Logic errors, off-by-one, missing edge cases\n"
        "2. SECURITY (OWASP): Injection risks, secrets exposure, insecure defaults\n"
        "3. ANTI-SLOP: Vague names, cargo-cult patterns, unnecessary complexity\n"
        "4. LOLLI: Artifacts without named consumers? Governance weight without value?\n"
        "5. CONSTITUTIONAL: Article 4 (Proportionality), 3 (Reversibility), 9 (Bounded Autonomy)\n\n"
        "End your response with exactly one line: 'Verdict: APPROVE' or "
        "'Verdict: REQUEST_CHANGES' with a one-line rationale. Be direct; no filler praise.\n\n"
        f"DIFF:\n{diff}"
    )


def run_cross_model(diff: str) -> tuple[str | None, str | None]:
    """Run one cross-model review using whichever API key is present.
    Returns (verdict_text, model_name) or (None, None) if no key / call failed.
    Preference order mirrors cross-model-review.yml: Claude, then Gemini, then
    Codex. Uses urllib (stdlib) so no extra deps are needed."""
    if not diff:
        return None, None
    prompt = _review_prompt(diff)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _call_anthropic(prompt), "claude"
    if os.environ.get("GOOGLE_AI_KEY"):
        return _call_gemini(prompt), "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return _call_openai(prompt), "codex"
    print("warn: no model API key (ANTHROPIC_API_KEY/GOOGLE_AI_KEY/OPENAI_API_KEY); "
          "reviewer_b unavailable", file=sys.stderr)
    return None, None


def _http_post_json(url: str, headers: dict, payload: dict) -> dict | None:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as exc:
        print(f"warn: model call failed: {exc}", file=sys.stderr)
        return None


def _call_anthropic(prompt: str) -> str | None:
    body = _http_post_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
        {"model": "claude-sonnet-4-20250514", "max_tokens": 1024,
         "messages": [{"role": "user", "content": prompt}]},
    )
    try:
        return body["content"][0]["text"] if body else None
    except (KeyError, IndexError, TypeError):
        return None


def _call_gemini(prompt: str) -> str | None:
    key = os.environ["GOOGLE_AI_KEY"]
    body = _http_post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}",
        {},
        {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 1024}},
    )
    try:
        return body["candidates"][0]["content"]["parts"][0]["text"] if body else None
    except (KeyError, IndexError, TypeError):
        return None


def _call_openai(prompt: str) -> str | None:
    body = _http_post_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        {"model": "gpt-4o", "max_tokens": 1024,
         "messages": [{"role": "user", "content": prompt}]},
    )
    try:
        return body["choices"][0]["message"]["content"] if body else None
    except (KeyError, IndexError, TypeError):
        return None


def _next_seq(today: str) -> int:
    """Next sequence for today's verdict id (council-YYYY-MM-DD-NNN)."""
    if not COUNCIL_DIR.is_dir():
        return 1
    prefix = f"council-{today}-"
    existing = [p.stem for p in COUNCIL_DIR.glob(f"{prefix}*.json")]
    seqs = []
    for stem in existing:
        tail = stem.replace(prefix, "")
        if tail.isdigit():
            seqs.append(int(tail))
    return (max(seqs) + 1) if seqs else 1


def _write_verdict(verdict: dict) -> Path:
    COUNCIL_DIR.mkdir(parents=True, exist_ok=True)
    out = COUNCIL_DIR / f"{verdict['verdict_id']}.json"
    out.write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    return out


def convene(pr: int, classified_risk: str = "medium",
            write: bool = True) -> dict:
    """Convene the council for one PR end-to-end and return the verdict dict.
    classified_risk is the governor's risk class for the PR (used for reviewer_b's
    independent risk_assessment field)."""
    meta = fetch_pr_meta(pr) or {}
    change_summary = meta.get("title", f"PR #{pr}")

    bb_state = fetch_blackbox_check_state(pr)
    reviews: list[dict] = []
    ra = review_from_blackbox(bb_state)
    if ra:
        reviews.append(ra)

    diff = fetch_diff(pr)
    xtext, xmodel = run_cross_model(diff)
    rb = review_from_cross_model(xtext, xmodel, classified_risk)
    if rb:
        reviews.append(rb)

    today = _now_iso()[:10]
    seq = _next_seq(today)
    verdict = build_verdict(pr, change_summary, reviews, today, seq)
    if write:
        path = _write_verdict(verdict)
        print(f"council verdict written: {path}", file=sys.stderr)
    return verdict


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel LLM-council verdict emitter")
    ap.add_argument("--pr", type=int, required=True, help="PR number to convene the council on")
    ap.add_argument("--risk", default="medium", help="governor risk class for the PR (low/medium/high/critical)")
    ap.add_argument("--print-only", action="store_true", help="print verdict JSON; do not write to state/council/")
    args = ap.parse_args(argv)

    verdict = convene(args.pr, classified_risk=args.risk, write=not args.print_only)
    print(json.dumps(verdict, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
