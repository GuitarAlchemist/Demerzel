#!/usr/bin/env python3
"""
Demerzel run_afk_cycle — the AFK implement-lane governor.

Reads the `agent-implement` GitHub issue queue, honors HALT, classifies risk per
policies/autonomous-loop-policy.yaml, and for each eligible (non-critical) issue
invokes the agent-agnostic sandcastle harness (../afk-harness) which runs headless
Claude Code in a Podman sandbox to produce a branch + commits. The governor then
pushes the branch, opens a PR linked to the issue, and records loop-state + audit.
Critical issues (constitution/policy) are skipped with a "needs human pre-approval"
comment. Merge is left to existing review gates (self-merge automation deferred).

Parallelism (--max-parallel, default 3): issues are processed concurrently, each
in its OWN ephemeral clone of the repo so there are no git races on the shared
.git (worktree/index/ref contention). Each agent's branch pushes to the shared
origin; PRs are independent. The whole queue is always processed — concurrency is
a throughput cap, not a truncation (waves of --max-parallel at a time).

Backends (--backend):
  local        — per-agent ephemeral clone + Podman sandbox (default; runs on this box)
  claude-code  — per-agent ephemeral clone + headless `claude -p` (no container;
                 bills the interactive subscription, not the spend-capped API key)
  remote       — Vercel isolated sandboxes (NOT yet implemented; seam reserved)

Usage:
  python scripts/run_afk_cycle.py --dry-run            # classify + plan, no side effects
  python scripts/run_afk_cycle.py                      # run one cycle, up to 3 in parallel
  python scripts/run_afk_cycle.py --max-parallel 1     # force sequential
  python scripts/run_afk_cycle.py --max-parallel 5     # heavier local fan-out

Exit codes:
  0  cycle ran (any mix of implemented/skipped/stalled/no-op)
  1  usage / environment error (e.g. Podman unavailable, bad --max-parallel)
  3  aborted: HALT-ALL marker in effect
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aiw_budget_gate as budget  # noqa: E402  (fail-closed AIW budget preflight)
import council_emit  # noqa: E402  (sibling module in scripts/; self-merge gate)
import demerzel_kit as kit  # noqa: E402  (shared gh / write-artifact seam)

ROOT = Path(__file__).resolve().parents[1]            # repos/Demerzel
HARNESS_DIR = ROOT.parent / "afk-harness"             # sibling, outside Demerzel
PROMPT_FILE = ROOT / "prompts" / "afk-implement.prompt.md"
LABEL = "agent-implement"
REPO_SLUG = "GuitarAlchemist/Demerzel"

CRITICAL_PATHS = ("constitution", "policies/", "policy")
HIGH_KEYWORDS = ("schema migration", "migrate schema", "cross-repo", "infrastructure")
MEDIUM_KEYWORDS = ("persona", "refactor", "schema")
LOW_KEYWORDS = ("doc", "documentation", "typo", "comment", "test", "config")

# Self-merge gate constants (policies/autonomous-loop-policy.yaml §Self-Merge Authority)
CONSCIENCE_SIGNALS_DIR = ROOT / "state" / "conscience" / "signals"
CONSCIENCE_BLOCK_WEIGHT = 0.8         # an active signal at/above this blocks self-merge
SELF_MERGE_MIN_CONFIDENCE = 0.7       # minimum post_council_confidence

# ── AIW budget enforcement (#471) ──────────────────────────────────────────
# Every worker invocation goes through the fail-closed budget gate first: no
# granted reservation, no invocation. Each backend maps to an allowlisted
# provider so the gate applies its per-job / per-cycle caps and local-first rule.
BACKEND_PROVIDER = {
    "local": "codex-cli",             # ../afk-harness sandcastle runs Codex CLI
    "claude-code": "claude-code-cli",  # headless `claude -p` on the subscription
}
# Recognized budget numbers an issue may carry to tighten the policy defaults.
_BUDGET_KEYS = (
    "estimated_cost_usd", "estimated_total_tokens", "estimated_model_calls",
    "estimated_retries", "estimated_runner_minutes",
    "max_cost_usd", "max_total_tokens", "max_model_calls", "max_retries",
    "max_runner_minutes", "approval_required_above_usd",
)


def _parse_budget_block(body: str) -> dict:
    """Harvest recognized budget numbers from an issue body (string-based, no
    regex). Any ``key: number`` line whose key is a known budget field is picked
    up; unknown keys and non-numeric values are ignored. Missing fields fall back
    to the gate's policy defaults."""
    out: dict[str, float] = {}
    for raw in (body or "").splitlines():
        line = raw.strip().lstrip("-").strip()
        key, sep, val = line.partition(":")
        if not sep or key.strip() not in _BUDGET_KEYS:
            continue
        try:
            num = float(val.strip().rstrip(","))
        except ValueError:
            continue
        if num >= 0:
            out[key.strip()] = num
    return out


def _budget_request(issue: dict, backend: str) -> dict:
    """Build an AIW budget request for one issue+backend. Raises for a backend
    with no budgeted provider mapping (fail closed — an unmapped worker is never
    reserved)."""
    provider = BACKEND_PROVIDER.get(backend)
    if provider is None:
        raise ValueError(f"backend {backend!r} has no budgeted provider mapping")
    req = {"job_id": f"aiw-{issue.get('number')}", "provider": provider}
    req.update(_parse_budget_block(issue.get("body") or ""))
    return req


def _budget_reserve(issue: dict, backend: str) -> tuple[bool, dict]:
    """Fail-closed budget preflight before any worker invocation. Returns
    ``(allowed, result)``; ANY error is a block, never an invocation."""
    try:
        policy = budget.load_policy(budget.POLICY_PATH)
        result = budget.reserve(policy, _budget_request(issue, backend),
                                budget.CYCLE_LEDGER_PATH)
    except Exception as exc:  # a broken/absent policy must fail closed
        return False, {"decision": "block", "reasons": ["budget_preflight_error"],
                       "error": str(exc)[:200]}
    return result.get("decision") == "allow", result


def _budget_release(issue: dict, actual_cost_usd: float = 0.0) -> None:
    """Best-effort reservation release after an episode; a reconciliation hiccup
    must never break the loop. Local-seat backends carry no marginal spend."""
    try:
        budget.release(budget.CYCLE_LEDGER_PATH, f"aiw-{issue.get('number')}",
                       actual_cost_usd, policy=budget.load_policy(budget.POLICY_PATH))
    except Exception as exc:
        print(f"budget release skipped for #{issue.get('number')}: {exc}",
              file=sys.stderr)


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
        "started_at": kit.now_iso(),
        "max_iterations": 10,
    }


def _github_origin_url() -> str:
    """The GitHub URL of ROOT's origin, so per-agent clones push to the real remote."""
    p = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"],
                       capture_output=True, text=True, timeout=30)
    return p.stdout.strip() if p.returncode == 0 else ""


def _prepare_clone(issue: dict) -> str:
    """Make an isolated ephemeral clone of ROOT so a parallel agent never contends
    on the shared .git. Returns the clone path (caller deletes it). origin is
    repointed at GitHub so the agent's branch pushes to the shared remote, not the
    local source clone. --no-hardlinks keeps the clone fully independent."""
    clone = tempfile.mkdtemp(prefix=f"afk-{issue.get('number')}-")
    subprocess.run(["git", "clone", "--no-hardlinks", str(ROOT), clone],
                   capture_output=True, text=True, timeout=300, check=True)
    url = _github_origin_url()
    if url:
        subprocess.run(["git", "-C", clone, "remote", "set-url", "origin", url],
                       capture_output=True, text=True, timeout=30, check=True)
    return clone


def _invoke_harness(issue: dict, repo_path: str) -> dict:
    """Run the sandcastle harness for one issue against repo_path. Returns
    {branch,commits,blocked}.

    Invokes node with the tsx loader directly rather than `npx tsx`: on Windows
    `npx` is `npx.cmd` (no .exe) and Python's subprocess cannot CreateProcess it
    without a shell — and a shell would expose the issue body to command
    injection. `node` is a real executable and args pass straight through as argv.
    """
    cmd = ["node", "--import", "tsx", str(HARNESS_DIR / ".sandcastle" / "main.mts"),
           "--repo", str(repo_path), "--issue", str(issue.get("number")),
           "--title", issue.get("title", ""), "--body", issue.get("body", "")]
    p = subprocess.run(cmd, cwd=str(HARNESS_DIR), capture_output=True, text=True, timeout=1800)
    if p.returncode != 0:
        return {"branch": None, "commits": [], "blocked": f"harness exit {p.returncode}: {p.stderr.strip()[:200]}"}
    last = [l for l in p.stdout.strip().splitlines() if l.strip().startswith("{")]
    if not last:
        return {"branch": None, "commits": [], "blocked": "harness produced no JSON result"}
    return json.loads(last[-1])


def _invoke_harness_remote(issue: dict) -> dict:
    """Backend seam for Vercel isolated sandboxes (Approach C). Not yet
    implemented — returns a clean blocked result so --backend remote is a no-op
    rather than a crash until the remote provider lands."""
    return {"branch": None, "commits": [],
            "blocked": "remote backend (Vercel isolated sandboxes) not implemented yet — use --backend local"}


CLAUDE_CODE_TIMEOUT = 1800  # seconds for one headless `claude -p` agent run


def _claude_code_prompt(issue: dict) -> str:
    """The instruction handed to the headless Claude Code agent. The issue body
    already carries the full implementation spec (pattern + success criteria), so
    this only frames the autonomy contract: implement, test, commit — no push/PR
    (the governor owns those)."""
    num = issue.get("number")
    return (
        "You are an autonomous AFK engineer working in a fresh clone of the "
        "Demerzel governance repo, on a dedicated branch. Implement the issue "
        "below end-to-end, then COMMIT your work on the current branch with a "
        "conventional-commit message (feat/refactor/test). Be surgical — change "
        "only what the issue requires. After editing, run "
        "`python -m unittest discover -s scripts -p \"test_*.py\"` and make sure it "
        "passes before committing. Do NOT push and do NOT open a pull request; "
        "just commit locally.\n\n"
        f"=== ISSUE #{num}: {issue.get('title', '')} ===\n\n"
        f"{issue.get('body', '')}"
    )


def _invoke_harness_claude_code(issue: dict, repo_path: str) -> dict:
    """Backend: delegate one issue to a headless Claude Code agent (`claude -p`)
    in repo_path instead of the Podman sandbox. Returns {branch,commits,blocked} —
    the same contract as the other backends, so the governor's push/PR/council
    wrappers are unchanged.

    Three deliberate choices:
      * ANTHROPIC_API_KEY is stripped from the child env so `claude` bills the
        interactive subscription, not the spend-capped API key — the reason this
        backend exists (the Podman backend's claude-code hits that cap).
      * The agent runs under a SCOPED tool allowlist (not skip-permissions): it may
        edit/read files and run only `python`/`git` — enough to migrate, test, and
        commit, but not arbitrary commands. A non-listed tool is denied rather than
        prompting (headless), so the blast radius is the allowlist, not the host.
      * Isolation is also the ephemeral clone (a git boundary). Even so this is a
        weaker boundary than the container backend; use for trusted, mechanical
        issues — the risk classifier keeps critical/high out of the auto lane.
    """
    num = issue.get("number")
    branch = f"agent/issue-{num}"
    try:
        subprocess.run(["git", "-C", repo_path, "checkout", "-b", branch],
                       capture_output=True, text=True, timeout=30, check=True)
        base = subprocess.run(["git", "-C", repo_path, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=30).stdout.strip()
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        cmd = ["claude", "-p", _claude_code_prompt(issue),
               "--output-format", "json",
               "--allowedTools", "Edit", "Write", "Read", "Grep", "Glob",
               "Bash(python *)", "Bash(python3 *)", "Bash(git *)"]
        p = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True,
                           timeout=CLAUDE_CODE_TIMEOUT, env=env)
    except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
        return {"branch": None, "commits": [], "blocked": f"claude-code invoke failed: {exc}"}

    # The agent is told to commit; if it left changes uncommitted, capture them so a
    # real implementation isn't lost to a missing commit step.
    dirty = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"],
                           capture_output=True, text=True, timeout=30).stdout.strip()
    if dirty:
        subprocess.run(["git", "-C", repo_path, "add", "-A"],
                       capture_output=True, text=True, timeout=60)
        subprocess.run(["git", "-C", repo_path, "commit", "-m",
                        f"feat: implement #{num} via AFK claude-code backend"],
                       capture_output=True, text=True, timeout=60)
    commits = subprocess.run(["git", "-C", repo_path, "log", "--format=%s", f"{base}..HEAD"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
    if not commits:
        tail = (p.stderr or p.stdout or "").strip()[-200:]
        return {"branch": None, "commits": [],
                "blocked": f"claude-code made no commits (exit {p.returncode}): {tail}"}
    return {"branch": branch, "commits": commits.splitlines(), "blocked": None}


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


def _open_pr(issue: dict, branch: str, repo_path: str) -> str:
    """Push the branch from repo_path and open a PR linked to the issue. Returns
    the PR URL (or a 'pr-create-failed: ...' sentinel)."""
    num = issue.get("number")
    subprocess.run(["git", "-C", str(repo_path), "push", "origin", branch],
                   capture_output=True, text=True, timeout=120, check=True)
    p = subprocess.run(
        ["gh", "pr", "create", "--repo", REPO_SLUG, "--head", branch,
         # The PR carries the agent-implement label so the --harvest self-merge
         # pass (which filters PRs on that label) can find it. Without this the
         # implement and harvest lanes are disconnected.
         "--label", LABEL,
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
    out = kit.gh_json(
        ["issue", "list", "--repo", REPO_SLUG, "--label", LABEL,
         "--state", "open", "--json", "number,title,body,labels", "--limit", "20"])
    return out if isinstance(out, list) else []


def _write_loop_state(state: dict) -> None:
    """Persist one loop-state file (schema-validated). Distinct filename per issue
    → thread-safe."""
    out = ROOT / "state" / "loops" / f"{state['loop_id']}.loop.json"
    kit.write_artifact(out, state, schema="loop-state")


def _write_audit(summary: dict, today: str) -> None:
    """Persist the combined cycle audit atomically to state/oversight/."""
    out = ROOT / "state" / "oversight" / f"afk-cycle-{today}.json"
    kit.write_artifact(out, summary)


# --------------------------------------------------------------------------- #
# Graduated self-merge (the --harvest pass)
#
# A SEPARATE pass from the implement queue: agent-blackbox runs asynchronously in
# CI, so a PR's gates are not settled when _process_issue opens it. Harvest
# re-examines already-open agent-implement PRs whose checks have settled and
# self-merges only those that clear the council + policy gate. This NEVER applies
# the `agent-blackbox-reviewed` override — it merges only PRs that already PASS
# their gates. Critical/high never self-merge.
# --------------------------------------------------------------------------- #
def parse_authorization_trace(pr_body: str) -> str | None:
    """Extract the authorization artifact a PR traces to. AFK PRs carry
    'Closes #N' / 'Implements #N' / 'Fixes #N'. Returns 'github_issue:#N' or None.
    String-based (no regex) per repo convention."""
    if not pr_body:
        return None
    for kw in ("closes #", "implements #", "fixes #", "resolves #"):
        idx = pr_body.lower().find(kw)
        if idx == -1:
            continue
        tail = pr_body[idx + len(kw):]
        num = ""
        for ch in tail:
            if ch.isdigit():
                num += ch
            else:
                break
        if num:
            return f"github_issue:#{num}"
    return None


def active_conscience_max_weight() -> float:
    """Max `weight` among ACTIVE conscience signals (state/conscience/signals/).
    A signal is active unless resolved (resolved_at present, or outcome begins
    'RESOLVED') or marked false_positive. Returns 0.0 when none or dir absent.
    Note: the policy prose says 'severity'; the schema field is `weight`."""
    if not CONSCIENCE_SIGNALS_DIR.is_dir():
        return 0.0
    mx = 0.0
    for p in CONSCIENCE_SIGNALS_DIR.glob("*.signal.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if d.get("false_positive") is True or d.get("resolved_at"):
            continue
        outcome = d.get("outcome") or ""
        if isinstance(outcome, str) and outcome.strip().upper().startswith("RESOLVED"):
            continue
        w = d.get("weight")
        if isinstance(w, (int, float)):
            mx = max(mx, float(w))
    return mx


def self_merge_decision(risk: str, checks_green: bool, authz_trace: str | None,
                        conscience_max_weight: float,
                        council_verdict: dict | None) -> tuple[bool, str]:
    """Pure gate predicate for graduated self-merge. Returns (merge?, reason).
    Mirrors policies/autonomous-loop-policy.yaml §Self-Merge Authority:
    CI pass · confidence >= 0.7 · no conscience >= 0.8 · authorization trace ·
    critical/high never · genuine multi-model council (>= 2 reviews)."""
    if risk not in ("low", "medium"):
        return False, f"risk={risk}: only low/medium self-merge (critical/high never)"
    if not checks_green:
        return False, "CI not all green"
    if not authz_trace:
        return False, "no authorization trace (PR not linked to an issue)"
    if conscience_max_weight >= CONSCIENCE_BLOCK_WEIGHT:
        return False, (f"active conscience signal weight {conscience_max_weight:.2f} "
                       f">= {CONSCIENCE_BLOCK_WEIGHT}")
    if not council_verdict:
        return False, "no council verdict"
    reviews = council_verdict.get("reviews", [])
    if len(reviews) < 2:
        return False, f"council incomplete: {len(reviews)} reviewer(s), need 2 (multi-model)"
    if council_verdict.get("verdict") != "APPROVE":
        return False, f"council verdict {council_verdict.get('verdict')}"
    conf = council_verdict.get("post_council_confidence", 0.0)
    if conf < SELF_MERGE_MIN_CONFIDENCE:
        return False, f"post_council_confidence {conf:.2f} < {SELF_MERGE_MIN_CONFIDENCE}"
    if any(r.get("constitutional_alignment") != "pass" for r in reviews):
        return False, "constitutional alignment not all pass"
    return True, f"self-merge OK (post_council_confidence={conf:.2f}, {len(reviews)} reviewers)"


def _checks_all_green(pr: int) -> bool:
    """True iff `gh pr checks` shows at least one check and none are failing or
    pending. pass/success/skipping/neutral count as OK; fail/pending block.
    `gh pr checks` exits non-zero when any check failed but the table is still
    valid output, so the read uses ok_nonzero=True."""
    out = kit.gh_text(["pr", "checks", str(pr), "--repo", REPO_SLUG], ok_nonzero=True)
    if out is None:
        return False
    saw_any = False
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        saw_any = True
        state = parts[1].strip().lower()
        if state not in ("pass", "success", "skipping", "neutral"):
            return False
    return saw_any


def _gh_open_afk_prs() -> list[dict]:
    """Open agent-implement PRs as dicts with number/title/body/labels."""
    out = kit.gh_json(
        ["pr", "list", "--repo", REPO_SLUG, "--label", LABEL,
         "--state", "open", "--json", "number,title,body,labels", "--limit", "20"])
    return out if isinstance(out, list) else []


def _merge_pr(pr: int) -> str:
    """Squash-merge a gate-cleared PR. Returns 'merged' or a failure sentinel."""
    p = subprocess.run(["gh", "pr", "merge", str(pr), "--repo", REPO_SLUG, "--squash"],
                       capture_output=True, text=True, timeout=120)
    return "merged" if p.returncode == 0 else f"merge-failed: {p.stderr.strip()[:160]}"


def _harvest_pr(pr: dict, conscience_w: float) -> dict:
    """Gate ONE open AFK PR through cheap pre-checks, then the council, then the
    self-merge predicate. The council call (a model request) is spent only on
    PRs that already pass the cheap gates."""
    num = pr.get("number")
    risk, _mode = classify_risk(pr)          # classify_risk reads title/body/labels — works on a PR dict
    authz = parse_authorization_trace(pr.get("body", ""))
    decision = {"pr": num, "title": pr.get("title"), "risk": risk,
                "authorization_trace": authz}

    if risk not in ("low", "medium"):
        decision["action"] = f"skip:risk-{risk}"
        return decision
    if not authz:
        decision["action"] = "skip:no-authorization-trace"
        return decision
    if not _checks_all_green(num):
        decision["action"] = "hold:ci-not-green"
        return decision

    verdict = council_emit.convene(num, classified_risk=risk, write=True)
    decision["council_verdict"] = verdict.get("verdict")
    decision["post_council_confidence"] = verdict.get("post_council_confidence")
    decision["reviewers"] = len(verdict.get("reviews", []))

    merge, reason = self_merge_decision(risk, True, authz, conscience_w, verdict)
    decision["gate"] = reason
    if not merge:
        decision["action"] = "hold:gate-not-met"
        return decision
    decision["action"] = "self-merge"
    decision["merge_result"] = _merge_pr(num)
    return decision


def _run_harvest(dry: bool, today: str) -> int:
    """The self-merge pass over open AFK PRs."""
    prs = _gh_open_afk_prs()
    conscience_w = active_conscience_max_weight()
    if prs:
        print(f"AFK harvest: {len(prs)} open agent-implement PR(s); "
              f"active conscience weight {conscience_w:.2f}", file=sys.stderr)

    decisions: list[dict] = []
    for pr in prs:
        if dry:
            risk, _ = classify_risk(pr)
            authz = parse_authorization_trace(pr.get("body", ""))
            decisions.append({
                "pr": pr.get("number"), "title": pr.get("title"), "risk": risk,
                "authorization_trace": authz,
                "action": "plan:would-gate" if risk in ("low", "medium") else f"skip:risk-{risk}"})
        else:
            decisions.append(_harvest_pr(pr, conscience_w))

    def _tally(prefix: str) -> int:
        return sum(1 for d in decisions if str(d.get("action", "")).startswith(prefix))
    summary = {
        "harvest_at": kit.now_iso(), "dry_run": dry, "halted": False,
        "conscience_max_weight": conscience_w, "queue_size": len(prs),
        "decisions": decisions,
        "tally": {"self_merge": _tally("self-merge"), "held": _tally("hold"),
                  "skipped": _tally("skip")},
    }
    if not dry:
        out = ROOT / "state" / "oversight" / f"afk-harvest-{today}.json"
        kit.write_artifact(out, summary)
    print(json.dumps(summary, indent=2))
    return 0


def _process_issue(issue: dict, seq: int, today: str, backend: str) -> tuple[dict, dict]:
    """Live processing of ONE issue end-to-end (runs inside the thread pool).
    Each call is independent: its own clone, its own branch, its own PR, its own
    loop-state file. Returns (decision, state)."""
    risk, mode = classify_risk(issue)
    eligible = is_eligible(issue)
    state = build_loop_state(issue, seq, risk, mode, today)
    decision = {"issue": issue.get("number"), "title": issue.get("title"),
                "risk": risk, "mode": mode, "eligible": eligible,
                "action": "implement" if eligible else "skip:needs-human-preapproval"}

    if not eligible:
        _comment_needs_preapproval(issue)
        state["status"] = "halted"
        state["halt_reason"] = "critical: needs human pre-approval"
        _write_loop_state(state)
        return decision, state

    # Budget preflight (#471): a worker is NEVER invoked without a granted
    # reservation. A blocked/errored preflight fails closed — no clone, no spend.
    allowed, budget_result = _budget_reserve(issue, backend)
    if not allowed:
        reasons = budget_result.get("reasons") or ["denied"]
        decision["action"] = f"blocked:budget:{','.join(reasons)}"
        state["status"] = "halted"
        state["halt_reason"] = f"budget: {', '.join(reasons)}"
        _write_loop_state(state)
        return decision, state

    clone = None
    try:
        if backend == "remote":
            hr = _invoke_harness_remote(issue)
            repo_for_push = None
        elif backend == "claude-code":
            clone = _prepare_clone(issue)
            hr = _invoke_harness_claude_code(issue, clone)
            repo_for_push = clone
        else:
            clone = _prepare_clone(issue)
            hr = _invoke_harness(issue, clone)
            repo_for_push = clone

        if hr.get("blocked"):
            decision["action"] = f"blocked:{hr['blocked']}"
            state["status"] = "halted"
            state["halt_reason"] = str(hr["blocked"])
        elif hr.get("branch"):
            pr = _open_pr(issue, hr["branch"], repo_for_push)
            decision["pr"] = pr
            decision["branch"] = hr["branch"]
            if pr.startswith("pr-create-failed"):
                # A failed PR must NOT be reported as completed.
                decision["action"] = "stalled:pr-create-failed"
                state["status"] = "stalled"
                state["halt_reason"] = pr
            else:
                state["iterations"].append({
                    "iteration": 1, "timestamp": kit.now_iso(),
                    "action": f"opened PR for #{issue.get('number')}",
                    "outcome": "progress", "governance_decision": None})
                state["status"] = "completed"
        else:
            # Harness returned neither a branch nor a blocked reason (e.g. agent
            # made no commits). Do not leave status pinned at 'running'.
            decision["action"] = "stalled:no-branch-no-blocked"
            state["status"] = "stalled"
            state["halt_reason"] = "harness returned neither branch nor blocked"
    except Exception as exc:  # one bad issue must not abort the rest of the cycle
        decision["action"] = f"error:{type(exc).__name__}"
        state["status"] = "stalled"
        state["halt_reason"] = str(exc)[:200]
    finally:
        if clone:
            shutil.rmtree(clone, ignore_errors=True)
        # Reconcile the reservation: local-seat backends carry no marginal spend.
        _budget_release(issue, actual_cost_usd=0.0)

    _write_loop_state(state)
    return decision, state


def _print_summary(decisions: list[dict], queue_size: int, dry_run: bool,
                   workers: int, backend: str, today: str) -> dict:
    def _tally(prefix: str) -> int:
        return sum(1 for d in decisions if str(d.get("action", "")).startswith(prefix))
    summary = {
        "cycle_at": kit.now_iso(), "dry_run": dry_run, "halted": False,
        "backend": backend, "max_parallel": workers, "queue_size": queue_size,
        "decisions": decisions,
        "tally": {
            "implement": _tally("implement"),
            "skipped": _tally("skip"),
            "stalled": _tally("stalled"),
            "blocked": _tally("blocked"),
            "error": _tally("error"),
        },
    }
    if not dry_run:
        _write_audit(summary, today)
    print(json.dumps(summary, indent=2))
    return summary


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel AFK implement-lane governor")
    ap.add_argument("--dry-run", action="store_true",
                    help="classify + plan only; no clone, sandbox, push, PR, or file writes")
    ap.add_argument("--max-parallel", type=int, default=3,
                    help="max concurrent AFK agents (default 3); the whole queue is "
                         "still processed in waves of this size")
    ap.add_argument("--backend", choices=["local", "remote", "claude-code"], default="local",
                    help="local = per-agent clone + Podman (default); "
                         "claude-code = per-agent clone + headless `claude -p` (no container, "
                         "bills the subscription not the spend-capped API key); "
                         "remote = Vercel isolated sandboxes (not yet implemented)")
    ap.add_argument("--harvest", action="store_true",
                    help="self-merge pass: gate already-open AFK PRs through the "
                         "council + policy thresholds and merge qualifiers, instead "
                         "of processing the issue queue")
    args = ap.parse_args(argv)

    if args.max_parallel < 1:
        print("error: --max-parallel must be >= 1", file=sys.stderr)
        return 1

    halted, why = halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    today = kit.now_iso()[:10]

    # Self-merge harvest is a distinct pass (CI gates settle asynchronously after
    # the implement pass opens a PR), so it has its own queue and audit.
    if args.harvest:
        return _run_harvest(args.dry_run, today)

    issues = _gh_queue(args.dry_run)

    # Dry-run: plan only, strictly no side effects (no clone/podman/files).
    if args.dry_run:
        decisions = []
        for seq, issue in enumerate(issues, start=1):
            risk, mode = classify_risk(issue)
            eligible = is_eligible(issue)
            decisions.append({"issue": issue.get("number"), "title": issue.get("title"),
                              "risk": risk, "mode": mode, "eligible": eligible,
                              "action": "implement" if eligible else "skip:needs-human-preapproval"})
        _print_summary(decisions, len(issues), True, args.max_parallel, args.backend, today)
        return 0

    # Live: ensure the sandbox backend is ready once, up front.
    if args.backend == "local" and issues:
        ok, pnote = _ensure_podman()
        if not ok:
            print(f"ABORT: {pnote}", file=sys.stderr)
            return 1

    workers = max(1, min(args.max_parallel, len(issues))) if issues else 1
    if issues:
        print(f"AFK: processing {len(issues)} issue(s), up to {workers} concurrent "
              f"({args.backend} backend)", file=sys.stderr)

    decisions_by_seq: dict[int, dict] = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_process_issue, issue, seq, today, args.backend): seq
                for seq, issue in enumerate(issues, start=1)}
        for fut in as_completed(futs):
            seq = futs[fut]
            try:
                decision, _state = fut.result()
            except Exception as exc:  # backstop; _process_issue catches its own
                decision = {"issue": None, "action": f"error:{type(exc).__name__}",
                            "detail": str(exc)[:160]}
            decisions_by_seq[seq] = decision

    decisions = [decisions_by_seq[s] for s in sorted(decisions_by_seq)]
    _print_summary(decisions, len(issues), False, workers, args.backend, today)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
