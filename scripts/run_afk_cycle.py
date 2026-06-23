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
  local   — per-agent ephemeral clone + Podman sandbox (default; runs on this box)
  remote  — Vercel isolated sandboxes (NOT yet implemented; seam reserved)

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


def _write_loop_state(state: dict) -> None:
    """Persist one loop-state file. Distinct filename per issue → thread-safe."""
    loops_dir = ROOT / "state" / "loops"
    loops_dir.mkdir(parents=True, exist_ok=True)
    (loops_dir / f"{state['loop_id']}.loop.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _write_audit(summary: dict, today: str) -> None:
    """Persist the combined cycle audit atomically to state/oversight/."""
    out = ROOT / "state" / "oversight" / f"afk-cycle-{today}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, out)


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

    clone = None
    try:
        if backend == "remote":
            hr = _invoke_harness_remote(issue)
            repo_for_push = None
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
                    "iteration": 1, "timestamp": _now_iso(),
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

    _write_loop_state(state)
    return decision, state


def _print_summary(decisions: list[dict], queue_size: int, dry_run: bool,
                   workers: int, backend: str, today: str) -> dict:
    def _tally(prefix: str) -> int:
        return sum(1 for d in decisions if str(d.get("action", "")).startswith(prefix))
    summary = {
        "cycle_at": _now_iso(), "dry_run": dry_run, "halted": False,
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
    ap.add_argument("--backend", choices=["local", "remote"], default="local",
                    help="local = per-agent clone + Podman (default); "
                         "remote = Vercel isolated sandboxes (not yet implemented)")
    args = ap.parse_args(argv)

    if args.max_parallel < 1:
        print("error: --max-parallel must be >= 1", file=sys.stderr)
        return 1

    halted, why = halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    today = _now_iso()[:10]
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
