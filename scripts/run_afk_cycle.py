#!/usr/bin/env python3
"""
Demerzel run_afk_cycle — the AFK implement-lane governor.

Reads the `agent-implement` GitHub issue queue, honors HALT, classifies risk per
policies/autonomous-loop-policy.yaml, and for each eligible (non-critical) issue
invokes the agent-agnostic sandcastle harness (../afk-harness) which runs headless
Claude Code in a Docker sandbox to produce a branch + commits. The governor then
pushes the branch, opens a PR linked to the issue, and records loop-state + audit.
Critical issues (constitution/policy) are skipped with a "needs human pre-approval"
comment. Merge is left to existing review gates (self-merge automation deferred).

Usage:
  python scripts/run_afk_cycle.py --dry-run     # classify + plan, no sandbox/push/PR
  python scripts/run_afk_cycle.py               # run one cycle (live)

Exit codes:
  0  cycle ran (any mix of implemented/skipped/no-op)
  1  usage / environment error
  3  aborted: HALT-ALL marker in effect
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]            # repos/Demerzel
HARNESS_DIR = ROOT.parent / "afk-harness"             # sibling, outside Demerzel
PROMPT_FILE = ROOT / "prompts" / "afk-implement.prompt.md"
LABEL = "agent-implement"
REPO_SLUG = "GuitarAlchemist/Demerzel"

CRITICAL_PATHS = ("constitution", "policies/", "policy")
HIGH_KEYWORDS = ("schema migration", "migrate schema", "cross-repo", "infrastructure")
MEDIUM_KEYWORDS = ("persona", "refactor", "schema")
LOW_KEYWORDS = ("doc", "documentation", "typo", "comment", "test", "config")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def halt_active() -> tuple[bool, str]:
    """Mirror run_ml_feedback_cycle: ~/.demerzel/HALT-ALL present and not expired."""
    marker = Path.home() / ".demerzel" / "HALT-ALL"
    if not marker.is_file():
        return False, ""
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return True, "HALT-ALL present but unreadable — treating as halted (fail-safe)"
    exp = data.get("expires_at")
    if exp:
        try:
            if datetime.fromisoformat(exp.replace("Z", "+00:00")) < datetime.now(timezone.utc):
                return False, ""
        except ValueError:
            pass
    return True, f"HALT-ALL in effect (reason: {data.get('reason', 'n/a')})"


def _haystack(issue: dict) -> str:
    labels = " ".join(l.get("name", "") for l in issue.get("labels", []))
    return f"{issue.get('title', '')} {issue.get('body', '')} {labels}".lower()


def classify_risk(issue: dict) -> tuple[str, str]:
    """Return (risk, governance_mode). Conservative: any constitution/policy hint
    is critical; schema-migration/cross-repo is high; persona/refactor is medium;
    docs/tests/config is low; unknown defaults to medium (standard governance)."""
    h = _haystack(issue)
    if any(k in h for k in CRITICAL_PATHS):
        return "critical", "per-iteration"
    if any(k in h for k in HIGH_KEYWORDS):
        return "high", "per-iteration"
    if any(k in h for k in LOW_KEYWORDS) and not any(k in h for k in MEDIUM_KEYWORDS):
        return "low", "boundary-only"
    if any(k in h for k in MEDIUM_KEYWORDS):
        return "medium", "boundary-only"
    return "medium", "boundary-only"


def is_eligible(issue: dict) -> bool:
    """Eligible for AFK implementation unless critical (constitution/policy)."""
    return classify_risk(issue)[0] != "critical"


def build_loop_state(issue: dict, seq: int, risk: str, mode: str, today: str) -> dict:
    """A dict valid against schemas/loop-state.schema.json."""
    return {
        "loop_id": f"loop-{today}-{seq:03d}",
        "goal": f"AFK-implement issue #{issue.get('number')}: {issue.get('title', '')}",
        "repo": "demerzel",
        "risk": risk,
        "governance_mode": mode,
        "status": "running",
        "iterations": [],
        "stall_count": 0,
        "authorization_artifact": f"github_issue:#{issue.get('number')}",
        "started_at": _now_iso(),
        "max_iterations": 10,
    }


def _invoke_harness(issue: dict) -> dict:
    """Run the sandcastle harness for one issue. Returns {branch,commits,blocked}."""
    cmd = ["npx", "tsx", str(HARNESS_DIR / ".sandcastle" / "main.mts"),
           "--repo", str(ROOT), "--issue", str(issue.get("number")),
           "--title", issue.get("title", ""), "--body", issue.get("body", "")]
    p = subprocess.run(cmd, cwd=str(HARNESS_DIR), capture_output=True, text=True, timeout=1800)
    if p.returncode != 0:
        return {"branch": None, "commits": [], "blocked": f"harness exit {p.returncode}: {p.stderr.strip()[:200]}"}
    last = [l for l in p.stdout.strip().splitlines() if l.strip().startswith("{")]
    if not last:
        return {"branch": None, "commits": [], "blocked": "harness produced no JSON result"}
    return json.loads(last[-1])


def _ensure_podman() -> tuple[bool, str]:
    """Restart-robustness: make sure the Podman machine is up before sandboxing.
    Idempotent — 'already running' is success. Returns (ok, note)."""
    try:
        chk = subprocess.run(["podman", "machine", "list", "--format", "{{.Running}}"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"podman not available: {exc}"
    if chk.returncode == 0 and "true" in chk.stdout.lower():
        return True, "podman machine already running"
    start = subprocess.run(["podman", "machine", "start"],
                           capture_output=True, text=True, timeout=180)
    if start.returncode == 0 or "already running" in (start.stderr + start.stdout).lower():
        return True, "podman machine started"
    return False, f"podman machine start failed: {start.stderr.strip()[:160]}"


def _open_pr(issue: dict, branch: str) -> str:
    """Push the branch and open a PR linked to the issue. Returns the PR URL."""
    num = issue.get("number")
    subprocess.run(["git", "-C", str(ROOT), "push", "-u", "origin", branch],
                   capture_output=True, text=True, timeout=120, check=True)
    p = subprocess.run(
        ["gh", "pr", "create", "--repo", REPO_SLUG, "--head", branch,
         "--title", f"AFK: {issue.get('title', '')} (#{num})",
         "--body", f"Implements #{num} via the AFK agent.\n\nReview gates: agent-blackbox + cross-model-review.\nCloses #{num}"],
        capture_output=True, text=True, timeout=120)
    return p.stdout.strip() if p.returncode == 0 else f"pr-create-failed: {p.stderr.strip()[:160]}"


def _comment_needs_preapproval(issue: dict) -> None:
    subprocess.run(
        ["gh", "issue", "comment", str(issue.get("number")), "--repo", REPO_SLUG,
         "--body", "🤖 AFK agent: this issue classifies as **critical** "
                   "(touches constitutions/policies) and will not be auto-implemented. "
                   "It needs human pre-approval per autonomous-loop-policy."],
        capture_output=True, text=True, timeout=60)


def _gh_queue(dry: bool) -> list[dict]:
    """Fetch open agent-implement issues via gh. Returns [] on any failure."""
    try:
        p = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO_SLUG, "--label", LABEL,
             "--state", "open", "--json", "number,title,body,labels", "--limit", "20"],
            capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            print(f"warn: gh issue list failed: {p.stderr.strip()[:160]}", file=sys.stderr)
            return []
        return json.loads(p.stdout or "[]")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"warn: gh queue unavailable: {exc}", file=sys.stderr)
        return []


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel AFK implement-lane governor")
    ap.add_argument("--dry-run", action="store_true",
                    help="classify + plan + write loop-state, but do not invoke the "
                         "sandbox, push, or open PRs")
    args = ap.parse_args(argv)

    halted, why = halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    today = _now_iso()[:10]
    issues = _gh_queue(args.dry_run)
    decisions = []
    for seq, issue in enumerate(issues, start=1):
        risk, mode = classify_risk(issue)
        eligible = is_eligible(issue)
        state = build_loop_state(issue, seq, risk, mode, today)
        decision = {"issue": issue.get("number"), "title": issue.get("title"),
                    "risk": risk, "mode": mode, "eligible": eligible,
                    "action": "implement" if eligible else "skip:needs-human-preapproval"}
        if not args.dry_run:
            loops_dir = ROOT / "state" / "loops"
            loops_dir.mkdir(parents=True, exist_ok=True)
            if eligible:
                ok, pnote = _ensure_podman()   # restart-robustness preflight (idempotent)
                if not ok:
                    decision["action"] = f"blocked:{pnote}"
                    state["status"] = "halted"
                    state["halt_reason"] = pnote
                    (loops_dir / f"{state['loop_id']}.loop.json").write_text(
                        json.dumps(state, indent=2) + "\n", encoding="utf-8")
                    decisions.append(decision)
                    continue
                hr = _invoke_harness(issue)
                if hr.get("blocked"):
                    decision["action"] = f"blocked:{hr['blocked']}"
                    state["status"] = "halted"
                    state["halt_reason"] = str(hr["blocked"])
                elif hr.get("branch"):
                    decision["pr"] = _open_pr(issue, hr["branch"])
                    decision["branch"] = hr["branch"]
                    state["iterations"].append({
                        "iteration": 1, "timestamp": _now_iso(),
                        "action": f"opened PR for #{issue.get('number')}",
                        "outcome": "progress", "governance_decision": None})
                    state["status"] = "completed"
            else:
                _comment_needs_preapproval(issue)
                state["status"] = "halted"
                state["halt_reason"] = "critical: needs human pre-approval"
            (loops_dir / f"{state['loop_id']}.loop.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8")
        decisions.append(decision)

    summary = {"cycle_at": _now_iso(), "dry_run": args.dry_run, "halted": False,
               "queue_size": len(issues), "decisions": decisions,
               "tally": {"implement": sum(1 for d in decisions if d["action"] == "implement"),
                         "skipped": sum(1 for d in decisions if d["action"].startswith("skip"))}}
    if not args.dry_run:
        out = ROOT / "state" / "oversight" / f"afk-cycle-{today}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, out)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
