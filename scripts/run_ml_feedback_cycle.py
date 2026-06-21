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

Exit codes:
  0  cycle ran (any mix of applied/escalated/no-op)
  1  usage / environment error (e.g. ix producers not found)
  3  aborted: HALT-ALL marker in effect
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _halt_active() -> tuple[bool, str]:
    """Mirror demerzel_halt.py: ~/.demerzel/HALT-ALL present and not expired."""
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
                return False, ""  # expired -> consumers treat as absent
        except ValueError:
            pass
    return True, f"HALT-ALL in effect (reason: {data.get('reason', 'n/a')})"


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


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel ML-feedback cycle orchestrator")
    root = Path(__file__).resolve().parents[1]          # repos/Demerzel
    ap.add_argument("--repos", nargs="+", default=["ix", "tars", "ga"],
                    choices=["ix", "tars", "ga"], help="consumer repos to harvest")
    ap.add_argument("--repos-root", type=Path, default=root.parent)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    py = sys.executable
    ix_scripts = (args.repos_root / "ix" / "scripts").resolve()
    if not args.dry_run and not (ix_scripts / "confidence_calibrator.py").is_file():
        print(f"error: ix producers not found at {ix_scripts}", file=sys.stderr)
        return 1

    # 0. HALT kill switch
    halted, why = _halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    steps = []
    # 1. Harvest — compliance reports per consumer (feeds §3c)
    for repo in args.repos:
        steps.append(_run(f"harvest:{repo}",
                          [py, str(root / "scripts" / "compliance_report.py"), "--repo", repo]
                          + (["--dry-run"] if args.dry_run else []), args.dry_run))
    # 2. Analyze — the four ix producers
    for prod in ["confidence_calibrator", "staleness_predictor",
                 "violation_pattern_detector", "remediation_optimizer"]:
        steps.append(_run(f"produce:{prod}",
                          [py, str(ix_scripts / f"{prod}.py"), "--demerzel-root", str(root)]
                          + (["--dry-run"] if args.dry_run else []), args.dry_run))
    # 3. Govern
    gov = _run("govern", [py, str(root / "scripts" / "apply_ml_feedback.py")]
               + (["--dry-run"] if args.dry_run else []), args.dry_run)
    steps.append(gov)

    summary = {
        "cycle_at": _now_iso(),
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
        out = root / "state" / "oversight" / f"ml-feedback-cycle-{_now_iso()[:10]}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        import os
        os.replace(tmp, out)

    print(json.dumps(summary, indent=2))
    for s in steps:
        print(f"  {s['status']:8} {s['step']}  {s.get('note','')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
