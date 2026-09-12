#!/usr/bin/env python3
"""
Demerzel run_ml_feedback_cycle — the orchestrator that turns the four hand-run
ML-feedback legs into ONE unattended, bounded self-improvement cycle.

Execution policy: externally-scheduled.
An operator-managed cron or Task Scheduler owns the mutating cycle's cadence.
GitHub Actions `ml-governance-schedule.yml` is a read-only freshness tripwire and
strict dry-run smoke; it never runs the mutating cycle.

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

One invocation = one cycle. Cadence belongs to the external operator scheduler,
NOT to a cycle-count gate here — the ml-feedback policy defines no per-day cap,
and WAKE-time count gates have wedged loops before. The only loop-level bound is
the HALT switch; per-decision bounds live in the governor.

Producers that find nothing to do exit 4 (no-op) and are reported as such, not as
errors. A producer/harvest error is logged but does not abort the cycle (the
governor simply processes whatever reached the inbox); only HALT aborts.

Usage:
  python scripts/run_ml_feedback_cycle.py                 # run one cycle
  python scripts/run_ml_feedback_cycle.py --dry-run       # plan only, no writes
  python scripts/run_ml_feedback_cycle.py --repos ix tars # limit consumer harvest
  python scripts/run_ml_feedback_cycle.py --producer-source worktree  # use ix working tree
  python scripts/run_ml_feedback_cycle.py --dry-run --strict  # CI smoke: errored steps are fatal
  python scripts/run_ml_feedback_cycle.py --commit         # land the belief refresh on master

Producers default to ix origin/main (branch-independent), materialized into
state/.cache/ix-producers/, so a scheduled cycle is unaffected by which branch
ix's working tree is on. Use --producer-source worktree to run local edits.

--commit closes the loop's LANDING leg, which was a human. The committed evidence
trail is state/beliefs/*.belief.json (the cycle summaries under state/oversight/
are gitignored runtime I/O), and ml-governance-schedule.yml's freshness leg goes
RED when that trail goes stale. Until now the refresh reached the repo only if an
operator noticed and committed it: it went 43 days uncommitted (2026-07-30 ->
2026-09-12) while the Task Scheduler entry succeeded daily, and the previous
landing was also a hand-patch (2875014, "uncommitted in the working tree ...
preserved rather than discarded"). A loop whose output depends on someone
remembering is a loop that dies while its producer stays green.

The output is made branch-independent to match the input: --commit refuses to run
from a checkout that does not push to master, because the stale refresh had been
written onto a feature branch 110 commits behind it, where no amount of
committing would have satisfied the guard. It fast-forwards BEFORE the cycle runs
(master takes bot commits daily from demerzel-quality-trend.yml, so a cycle that
wrote first would be unpushable), stages only state/beliefs/ so unrelated edits
never ride along, and treats a rejected push as a re-sync-and-retry rather than a
dead loop.

Exit codes:
  0  cycle ran (any mix of applied/escalated/no-op)
  1  usage / environment error (e.g. ix producers not found), or --strict
     and one or more steps errored (e.g. an unresolved producer)
  3  aborted: HALT-ALL marker in effect
  5  --commit could not guarantee a landing (checkout does not push to master, or
     it has diverged from origin/master) — refused BEFORE running the cycle, so a
     refresh is never produced where it cannot land
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import demerzel_halt as halt
import demerzel_kit as kit


def _halt_active(path: Path | None = None, now: datetime | None = None) -> tuple[bool, str]:
    """Thin decider over the shared HALT-ALL reader (demerzel_halt.is_active owns
    the marker path, schema, expiry, and fail-safe semantics)."""
    return halt.is_active(path.parent if path else None, now=now)


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


BELIEF_PATH = "state/beliefs"


def _git(root: Path, *args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run one git command in root. Never raises on a non-zero exit: callers
    decide, because 'nothing to commit' and 'cannot push' are different answers."""
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, timeout=timeout)


def _sync_master(root: Path, dry: bool) -> dict:
    """Guarantee the cycle's output can land, BEFORE producing any of it.

    Fail-closed on three distinct ways a landing is impossible, each reported by
    name rather than as a generic git error:
      - wrong line      -> the checkout does not push to master, so the refresh
                           would land where the freshness guard never looks (how
                           it went 43 days stale on a feature branch)
      - cannot ff       -> the checkout carries commits origin/master lacks;
                           ff-only refuses rather than merging or discarding them
      - no remote       -> offline; the commit would be unpushable

    The test is "does this checkout push to master", not "is it named master".
    Requiring the name would force the scheduled worktree to hold master itself,
    and git allows one checkout per branch - that would block a `git checkout
    master` in the operator's main tree for as long as the loop exists. A branch
    whose upstream is origin/master lands in exactly the same place.
    """
    label = "sync:master"
    if dry:
        return {"step": label, "status": "planned",
                "cmd": f"git -C {root} fetch origin master && git merge --ff-only origin/master"}

    head = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    branch = head.stdout.strip()
    upstream = _git(root, "rev-parse", "--abbrev-ref", "@{upstream}").stdout.strip()
    if head.returncode != 0 or (branch != "master" and upstream != "origin/master"):
        return {"step": label, "status": "error",
                "note": f"refusing to commit from '{branch or '?'}' "
                        f"(upstream '{upstream or 'none'}') - it does not push to "
                        f"master, where the belief trail is read"}

    fetch = _git(root, "fetch", "origin", "master")
    if fetch.returncode != 0:
        return {"step": label, "status": "error",
                "note": f"fetch failed: {(fetch.stderr.strip().splitlines() or [''])[-1][:160]}"}

    ff = _git(root, "merge", "--ff-only", "origin/master")
    if ff.returncode != 0:
        return {"step": label, "status": "error",
                "note": f"'{branch}' is not fast-forwardable to origin/master "
                        f"(local divergence or unpushed commits): "
                        f"{(ff.stderr.strip().splitlines() or [''])[-1][:160]}"}
    return {"step": label, "status": "ok", "note": ff.stdout.strip().splitlines()[-1][:160]
            if ff.stdout.strip() else "already up to date"}


def _commit_beliefs(root: Path, dry: bool) -> dict:
    """Land the belief refresh. A cycle that changed no belief is a no-op, not a
    failure - the governor legitimately applies a zero delta - but it is reported,
    because 'nothing changed' and 'nothing landed' must stay distinguishable in
    the evidence trail."""
    label = "commit:beliefs"
    if dry:
        return {"step": label, "status": "planned",
                "cmd": f"git -C {root} add -- {BELIEF_PATH} && git commit && "
                       f"git push origin HEAD:master"}

    add = _git(root, "add", "--", BELIEF_PATH)
    if add.returncode != 0:
        return {"step": label, "status": "error",
                "note": f"add failed: {(add.stderr.strip().splitlines() or [''])[-1][:160]}"}

    # Staged-vs-HEAD, scoped to the belief trail: the only diff that matters here.
    if _git(root, "diff", "--cached", "--quiet", "--", BELIEF_PATH).returncode == 0:
        return {"step": label, "status": "no-op", "note": "no belief changed this cycle"}

    msg = (f"state(ml-feedback): belief refresh {kit.now_iso()[:10]}\n\n"
           f"Committed by the cycle's own landing leg (run_ml_feedback_cycle.py "
           f"--commit), not by hand. The belief trail is what "
           f"ml-governance-schedule.yml reads to decide the loop is alive.")
    commit = _git(root, "commit", "-m", msg)
    if commit.returncode != 0:
        return {"step": label, "status": "error",
                "note": f"commit failed: {(commit.stderr.strip().splitlines() or [''])[-1][:160]}"}

    # HEAD:master, not the current branch's own name: the checkout may be a
    # dedicated landing branch tracking origin/master (see _sync_master).
    push = _git(root, "push", "origin", "HEAD:master")
    if push.returncode != 0:
        # The pre-cycle fetch cannot rule out a race: master takes bot commits
        # daily (demerzel-quality-trend.yml) and a cycle runs for minutes. This
        # was not theoretical - the first real landing was rejected exactly here,
        # by a nightly-deltas commit that arrived mid-cycle. One bounded re-sync;
        # a conflict aborts rather than guessing at someone else's belief edit.
        _git(root, "fetch", "origin", "master")
        rebase = _git(root, "rebase", "origin/master")
        if rebase.returncode != 0:
            _git(root, "rebase", "--abort")
            return {"step": label, "status": "error",
                    "note": "push rejected and rebase onto origin/master conflicted - "
                            "belief trail has NOT landed; resolve by hand"}
        push = _git(root, "push", "origin", "HEAD:master")

    if push.returncode != 0:
        # The commit exists locally; say so, because the guard reads the remote and
        # a silent local-only commit is the failure mode this leg exists to end.
        return {"step": label, "status": "error",
                "note": f"committed locally but push failed - belief trail has NOT landed: "
                        f"{(push.stderr.strip().splitlines() or [''])[-1][:160]}"}
    sha = _git(root, "rev-parse", "--short", "HEAD").stdout.strip()
    return {"step": label, "status": "ok", "note": f"pushed {sha} to origin/master"}


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
    ap.add_argument("--commit", action="store_true",
                    help="fast-forward master, then commit and push the belief refresh "
                         "(state/beliefs/) - the loop's landing leg. Refuses off master.")
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

    # 0b. Landing guarantee - before producing anything. A refresh written where
    # it cannot land is worse than no refresh: the producer stays green and the
    # freshness guard goes stale, which is the failure this leg ends.
    if args.commit:
        sync = _sync_master(root, args.dry_run)
        steps.append(sync)
        if sync["status"] == "error":
            print(f"ABORT: {sync['note']}", file=sys.stderr)
            return 5

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

    # 4. Land - the belief trail is the loop's only committed evidence.
    landing = _commit_beliefs(root, args.dry_run) if args.commit else None
    if landing:
        steps.append(landing)

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
    # A failed landing is loud with or without --strict. The cycle's whole value is
    # its committed trail; exiting 0 here would recreate the silent death exactly -
    # scheduler reports success, guard goes stale, nobody is told.
    if landing and landing["status"] == "error":
        print(f"landing failed: {landing['note']}", file=sys.stderr)
        return 1
    if args.strict and summary["tally"]["errors"]:
        print(f"strict: {summary['tally']['errors']} step(s) errored", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
