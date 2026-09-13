#!/usr/bin/env python3
"""Mechanical scan for staleness-detection-policy.yaml (lifecycle_scope, 1.3.0).

The policy has declared thresholds per artifact category since 2026-03 and, in
1.3.0 (2026-09-13, Demerzel #1067), a lifecycle scope: terminal records are
finished and never stale; open work and live state are measured against the
category threshold, aged by git commit time. Until this script nothing ran
that rule — a policy with no mechanism is a claim, not a check.

For every file matching an `artifact_categories[].path` glob:

  terminal    skipped: a signal or PDCA carrying an outcome, a regret with
              status resolved. (archived/ is never reached: the globs are
              non-recursive.)
  open_work   a signal or PDCA without an outcome, an unresolved regret, a
              candidate intuition.
  live_state  everything else a category names (beliefs, evolution metrics,
              digests, health scores, weights, patterns, the source queue).

Age is the last commit touching the file (`git log -1 --format=%cI`), falling
back to the file's own `last_updated`, never filesystem mtime. A shallow
clone would make every file look as young as the checkout commit, so the
scan refuses to run on one (exit 2) rather than report a false all-clear.

Priority follows the policy's classify step: critical when older than twice
its threshold or when it is a conscience signal, otherwise the category's
declared priority.

Warn-only by default (exit 0). --strict exits 1 on any stale artifact.
"""

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

TERMINAL, OPEN_WORK, LIVE_STATE = "terminal", "open_work", "live_state"
PRIORITY_ORDER = ["critical", "high", "medium", "low"]


def parse_ts(s):
    if not s:
        return None
    try:
        ts = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)


def load_json(path):
    if path.suffix != ".json":
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def lifecycle(category, data):
    """Classify one artifact per lifecycle_scope."""
    if category in ("conscience_signals", "pdca_cycles"):
        return TERMINAL if data.get("outcome") else OPEN_WORK
    if category == "conscience_regrets":
        return TERMINAL if data.get("status") == "resolved" else OPEN_WORK
    if category == "intuition_signals" and data.get("status") == "candidate":
        return OPEN_WORK
    return LIVE_STATE


def git_is_shallow(root):
    out = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=root, capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"not a git repository: {root}")
    return out.stdout.strip() == "true"


def git_commit_time(root, rel):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", rel],
        cwd=root, capture_output=True, text=True,
    )
    return parse_ts(out.stdout.strip()) if out.returncode == 0 else None


def scan(root, categories, now, commit_time=git_commit_time):
    """Return (findings, counts). Findings cover every non-terminal file; stale ones have stale=True."""
    findings = []
    counts = {TERMINAL: 0, OPEN_WORK: 0, LIVE_STATE: 0}
    seen = set()
    for cat in categories:
        for path in sorted(root.glob(cat["path"])):
            rel = path.relative_to(root).as_posix()
            if rel in seen or not path.is_file():
                continue  # department_weights and grammar_weights share a glob
            seen.add(rel)
            data = load_json(path)
            life = lifecycle(cat["category"], data)
            counts[life] += 1
            if life == TERMINAL:
                continue
            aged_at, source = commit_time(root, rel), "last commit"
            if aged_at is None:
                aged_at, source = parse_ts(data.get("last_updated")), "last_updated"
            limit = cat["max_staleness_days"]
            f = {
                "file": rel, "category": cat["category"], "lifecycle": life,
                "max_allowed": limit, "refresh_action": cat.get("refresh_action", ""),
            }
            if aged_at is None:
                f.update(days=None, stale=True, source="none", priority=cat.get("priority", "low"))
            else:
                days = (now - aged_at).days
                critical = days > 2 * limit or cat["category"] == "conscience_signals"
                f.update(days=days, stale=days > limit, source=source,
                         priority="critical" if critical else cat.get("priority", "low"))
            findings.append(f)
    return findings, counts


def category_newest(findings):
    """Age in days of the youngest measured file per category (files of unknown age ignored)."""
    newest = {}
    for f in findings:
        if f["days"] is not None:
            newest[f["category"]] = min(f["days"], newest.get(f["category"], f["days"]))
    return newest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--policy", default="policies/staleness-detection-policy.yaml")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is stale")
    args = ap.parse_args(argv)

    root = Path(args.root)
    policy = yaml.safe_load((root / args.policy).read_text(encoding="utf-8"))
    categories = policy.get("artifact_categories") or []
    if not categories:
        print(f"::error::no artifact_categories in {args.policy}")
        return 2
    try:
        if git_is_shallow(root):
            print("::error::shallow clone: every commit age would read as the checkout commit. "
                  "Check out with fetch-depth: 0.")
            return 2
    except RuntimeError as e:
        print(f"::error::{e}")
        return 2

    findings, counts = scan(root, categories, datetime.now(timezone.utc))
    stale = [f for f in findings if f["stale"]]
    for f in sorted(stale, key=lambda f: (PRIORITY_ORDER.index(f["priority"]), f["file"])):
        if f["days"] is None:
            age = "age unknown (no commit, no last_updated)"
        else:
            age = f"{f['days']}d since {f['source']}"
        print(f"::warning file={f['file']}::stale {f['lifecycle']} ({f['category']}): {age}, "
              f"max {f['max_allowed']}d, priority {f['priority']} — {f['refresh_action']}")

    print("Staleness Report:")
    for p in PRIORITY_ORDER:
        group = [f for f in stale if f["priority"] == p]
        oldest = max((f["days"] or 0 for f in group), default=0)
        print(f"- {p.capitalize()}: {len(group)} items" + (f" (oldest: {oldest} days)" if group else ""))
    newest = category_newest(findings)
    if newest:
        fresh = min(newest, key=newest.get)
        stalest = max(newest, key=newest.get)
        print(f"- Freshest: {fresh} ({newest[fresh]} days)")
        print(f"- Stalest: {stalest} ({newest[stalest]} days)")
        # A category whose NEWEST file is past its threshold was not refreshed at all:
        # for a produced series (digests, weights, evolution) that is a dead producer.
        # One line per category instead of one per stale file.
        for cat, days in sorted(newest.items(), key=lambda kv: -kv[1]):
            n = sum(1 for f in stale if f["category"] == cat)
            limit = next(f["max_allowed"] for f in findings if f["category"] == cat)
            if days > limit:
                print(f"  {cat}: newest file {days}d old (max {limit}d), {n} stale — nothing in this category refreshed within threshold")
    print(f"staleness_scan: {sum(counts.values())} files — {counts[TERMINAL]} terminal (exempt), "
          f"{counts[OPEN_WORK]} open work, {counts[LIVE_STATE]} live state; {len(stale)} stale")
    return 1 if (args.strict and stale) else 0


if __name__ == "__main__":
    raise SystemExit(main())
