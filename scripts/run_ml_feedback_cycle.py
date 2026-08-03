#!/usr/bin/env python3
"""
Demerzel run_ml_feedback_cycle — the orchestrator that turns the four hand-run
ML-feedback legs into ONE unattended, bounded self-improvement cycle.

It runs, in dependency order, a single pass of pipelines/ml-feedback-loop.ixql
(standing in for the absent IxQL executor):

  0. HALT check       — honor the cross-repo HALT-ALL kill switch (~/.demerzel/
                        HALT-ALL); abort the whole cycle if halted (per the
                        overseer-halt-marker contract). This is the real bound.
  1. Harvest          — compliance_report.py for each consumer repo (feeds §3c)
  2. Analyze (ix)     — the four producers emit recommendations into the inbox:
                        confidence_calibrator (§3a), staleness_predictor (§3b),
                        violation_pattern_detector (§3c), remediation_optimizer (§3d)
  3. Govern           — apply_ml_feedback.py gates each recommendation (Article 9):
                        bounded auto-apply or escalate to human review
  4. Summarize        — write one cycle summary to state/oversight/

One invocation = one cycle. Cadence comes from whatever schedules this (cron /
Task Scheduler), NOT from a cycle-count gate here — the ml-feedback policy defines
no per-day cap, and WAKE-time count gates have wedged loops before. The only
loop-level bound is the HALT switch; per-decision bounds live in the governor.

Producers that find nothing to do exit 4 (no-op) and are reported as such, not as
errors. A producer/harvest error is logged but does not abort the cycle (the
governor simply processes whatever reached the inbox); only HALT aborts.

Usage:
  python scripts/run_ml_feedback_cycle.py                 # run one cycle
  python scripts/run_ml_feedback_cycle.py --dry-run       # plan only, no writes
  python scripts/run_ml_feedback_cycle.py --repos ix tars # limit consumer harvest
  python scripts/run_ml_feedback_cycle.py --producer-source worktree  # use ix working tree
  python scripts/run_ml_feedback_cycle.py --dry-run --strict  # CI smoke: errored steps are fatal

Producers default to ix origin/main (branch-independent), materialized into
state/.cache/ix-producers/, so a scheduled cycle is unaffected by which branch
ix's working tree is on. Use --producer-source worktree to run local edits.

Exit codes:
  0  cycle ran (any mix of applied/escalated/no-op)
  1  usage / environment error (e.g. ix producers not found), or --strict
     and one or more steps errored (e.g. an unresolved producer)
  3  aborted: HALT-ALL marker in effect
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import demerzel_kit as kit


def _halt_active(path: Path | None = None, now: datetime | None = None) -> tuple[bool, str]:
    """Translate the shared HALT-ALL facts into this cycle's stop decision."""
    state = kit.halt_state(
        path or Path.home() / ".demerzel" / "HALT-ALL",
        now or datetime.now(timezone.utc),
    )
    if not state["active"]:
        return False, ""
    if not state["valid"]:
        return True, (f"HALT-ALL {state['reason']} — treating as halted (fail-safe): "
                      f"{state['errors']}")
    return True, f"HALT-ALL in effect (reason: {state['reason']})"


def _run(label: str, cmd: list[str], dry: bool) -> dict:
    """Run a step; capture exit code + last stderr line. exit 4 == benign no-op."""
    if dry:
        return {"step": label, "status": "planned", "cmd": " ".join(cmd)}
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"step": label, "status": "error", "note": str(exc)}
    tail = (p.stderr.strip().splitlines() or [""])[-1][:160]
    status = {0: "ok", 4: "no-op"}.get(p.returncode, "error")
    out = {"step": label, "status": status, "returncode": p.returncode, "note": tail}
    if p.stdout.strip():
        out["stdout_tail"] = p.stdout.strip().splitlines()[-1][:200]
    return out


PRODUCERS = ["confidence_calibrator", "staleness_predictor",
             "violation_pattern_detector", "remediation_optimizer"]


def _resolve_producers(ix_root: Path, cache_dir: Path, source: str) -> dict:
    """Resolve each producer to a runnable path. Default source 'main' materializes
    the canonical ix origin/main version into cache_dir, so a scheduled cycle is
    independent of whatever branch ix's working tree happens to be on (it must not
    break when ix is mid-feature, nor pick up uncommitted producer edits). Falls
    back to the working tree only if git / origin-main is unavailable (offline)."""
    paths, notes = {}, {}
    if source == "main":
        try:  # best-effort refresh; stale-but-present origin/main still works offline
            subprocess.run(["git", "-C", str(ix_root), "fetch", "origin", "main"],
                           capture_output=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired):
            pass
    for name in PRODUCERS:
        path = None
        if source == "main":
            try:
                p = subprocess.run(
                    ["git", "-C", str(ix_root), "show", f"origin/main:scripts/{name}.py"],
                    capture_output=True, text=True, timeout=30)
                if p.returncode == 0 and p.stdout:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    dest = cache_dir / f"{name}.py"
                    dest.write_text(p.stdout, encoding="utf-8")
                    path, notes[name] = dest, "origin/main"
            except (OSError, subprocess.TimeoutExpired):
                pass
        if path is None:  # fallback: ix working tree
            wt = ix_root / "scripts" / f"{name}.py"
            if wt.is_file():
                path, notes[name] = wt, "working-tree fallback"
        paths[name] = path
    return {"paths": paths, "notes": notes}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel ML-feedback cycle orchestrator")
    root = Path(__file__).resolve().parents[1]          # repos/Demerzel
    ap.add_argument("--repos", nargs="+", default=["ix", "tars", "ga"],
                    choices=["ix", "tars", "ga"], help="consumer repos to harvest")
    ap.add_argument("--repos-root", type=Path, default=root.parent)
    ap.add_argument("--producer-source", choices=["main", "worktree"], default="main",
                    help="source ix producers from origin/main (default, branch-independent) "
                         "or the ix working tree")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any step errors; without it a dry-run always "
                         "exits 0, so a smoke check could pass on an incoherent plan")
    args = ap.parse_args(argv)

    # 0. HALT kill switch
    halted, why = _halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    py = sys.executable
    ix_root = (args.repos_root / "ix").resolve()
    cache_dir = root / "state" / ".cache" / "ix-producers"
    resolved = _resolve_producers(ix_root, cache_dir, args.producer_source)
    if not any(resolved["paths"].values()) and not args.dry_run:
        print(f"error: could not resolve any ix producers (source={args.producer_source}, "
              f"ix={ix_root})", file=sys.stderr)
        return 1

    steps = []
    # 1. Harvest — compliance reports per consumer (feeds §3c)
    for repo in args.repos:
        steps.append(_run(f"harvest:{repo}",
                          [py, str(root / "scripts" / "compliance_report.py"), "--repo", repo]
                          + (["--dry-run"] if args.dry_run else []), args.dry_run))
    # 2. Analyze — the four ix producers (sourced per --producer-source)
    for prod in PRODUCERS:
        ppath = resolved["paths"].get(prod)
        if ppath is None:
            steps.append({"step": f"produce:{prod}", "status": "error",
                          "note": f"unresolved (source={args.producer_source})"})
            continue
        step = _run(f"produce:{prod}",
                    [py, str(ppath), "--demerzel-root", str(root)]
                    + (["--dry-run"] if args.dry_run else []), args.dry_run)
        step["source"] = resolved["notes"].get(prod, "?")
        steps.append(step)
    # 3. Govern
    gov = _run("govern", [py, str(root / "scripts" / "apply_ml_feedback.py")]
               + (["--dry-run"] if args.dry_run else []), args.dry_run)
    steps.append(gov)

    summary = {
        "cycle_at": kit.now_iso(),
        "dry_run": args.dry_run,
        "halted": False,
        "steps": steps,
        "tally": {
            "harvested": sum(1 for s in steps if s["step"].startswith("harvest") and s["status"] == "ok"),
            "produced": sum(1 for s in steps if s["step"].startswith("produce") and s["status"] == "ok"),
            "no_op": sum(1 for s in steps if s["status"] == "no-op"),
            "errors": sum(1 for s in steps if s["status"] == "error"),
        },
        "governor": gov.get("stdout_tail", gov.get("note", "")),
    }
    if not args.dry_run:
        out = root / "state" / "oversight" / f"ml-feedback-cycle-{kit.now_iso()[:10]}.json"
        kit.write_artifact(out, summary)

    print(json.dumps(summary, indent=2))
    for s in steps:
        print(f"  {s['status']:8} {s['step']}  {s.get('note','')}", file=sys.stderr)
    if args.strict and summary["tally"]["errors"]:
        print(f"strict: {summary['tally']['errors']} step(s) errored", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
