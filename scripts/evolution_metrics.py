#!/usr/bin/env python3
"""Deterministic citation metrics for state/evolution/*.evolution.json.

Until 2026-09 every evolution metric was typed by hand when a session wrote
an entry, and nothing updated it afterwards: scripts/quality_trend.py read
the same numbers for 46 nights (last change 2026-07-29) and emitted zero
deltas. The hand counts were also not measurements — alignment-policy said 3
citations while 42 tracked files name it.

This producer computes the two metrics that git can answer without judgment:

  citation_count  tracked files that mention any of the artifact's citation
                  paths (`git grep -lF`), excluding the artifact's own files,
                  archived/, state/evolution/, state/quality-trend/ and the
                  generated governance-manifest.json.
  last_cited      commit time of the newest commit that added or removed such
                  a mention (`git log -1 -S<path>`), over the same pathspec;
                  null when no commit ever did.

Citation paths are the entry's `citation_paths` list when present, else its
`artifact` when that is a tracked path. An explicit empty list marks an
artifact that lives outside this repository (unmeasurable here). Anything
else is reported as unmeasurable and left untouched.

violation_count, compliance_rate and assessment are judgments; this script
never touches them. It stamps metrics.citation_source so quality_trend.py
can mark the first computed value as a rebaseline instead of a real jump.

A file is rewritten only when a computed value changes. Run with --check to
report differences without writing (exit 1 if any).
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import demerzel_kit

CITATION_SOURCE = "git-grep-v1"
EXCLUDED = (":!state/evolution", ":!state/quality-trend", ":!**/archived/**", ":!governance-manifest.json")


def git(root, *args):
    out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8")
    if out.returncode not in (0, 1):  # git grep exits 1 on no match
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def is_tracked(root, path):
    return bool(git(root, "ls-files", "--", path.rstrip("/")).strip())


def owned_by(ref, paths):
    return any(ref == p.rstrip("/") or ref.startswith(p.rstrip("/") + "/") for p in paths)


def citation_paths(root, entry):
    """Return (paths, reason). paths is None when the entry cannot be measured."""
    if "citation_paths" in entry:
        paths = entry["citation_paths"]
        if not paths:
            return None, "citation_paths is empty (artifact lives outside this repository)"
        missing = [p for p in paths if not is_tracked(root, p)]
        if missing:
            return None, f"citation_paths not tracked: {', '.join(missing)}"
        return paths, None
    if is_tracked(root, entry["artifact"]):
        return [entry["artifact"]], None
    return None, "artifact is not a tracked path and no citation_paths given"


def measure(root, paths):
    refs = set()
    last = None
    for p in paths:
        for ref in git(root, "grep", "-lF", "-e", p, "--", ".", *EXCLUDED).splitlines():
            if ref and not owned_by(ref, paths):
                refs.add(ref)
        ts = git(root, "log", "-1", f"-S{p}", "--format=%cI", "--", ".", *EXCLUDED).strip()
        if ts and (last is None or ts > last):
            last = ts
    return len(refs), last


def to_utc_z(iso):
    """git %cI carries the committer's offset; store UTC with Z like the rest of the log."""
    return datetime.fromisoformat(iso).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


CHANGED, UNCHANGED, UNMEASURABLE = "changed", "unchanged", "unmeasurable"


def update_entry(root, entry):
    """Return (status, note). Mutates entry in place when measurable."""
    paths, reason = citation_paths(root, entry)
    if paths is None:
        return UNMEASURABLE, reason
    count, last = measure(root, paths)
    metrics = entry.setdefault("metrics", {})
    new = {"citation_count": count, "citation_source": CITATION_SOURCE,
           "last_cited": to_utc_z(last) if last else None}
    changed = {k: v for k, v in new.items() if metrics.get(k) != v}
    metrics.update(new)
    if not changed:
        return UNCHANGED, ""
    return CHANGED, ", ".join(f"{k}={v}" for k, v in changed.items())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(demerzel_kit.ROOT))
    ap.add_argument("--evolution-dir", default="state/evolution")
    ap.add_argument("--check", action="store_true", help="report changes without writing; exit 1 if any")
    args = ap.parse_args(argv)
    root = Path(args.root)

    files = sorted((root / args.evolution_dir).glob("*.evolution.json"))
    if not files:
        print(f"::error::no evolution files under {args.evolution_dir}")
        return 2
    changed = unmeasurable = 0
    for path in files:
        entry = json.loads(path.read_text(encoding="utf-8"))
        status, note = update_entry(root, entry)
        name = path.relative_to(root).as_posix()
        if status == UNMEASURABLE:
            unmeasurable += 1
            print(f"::notice file={name}::unmeasurable: {note}")
        elif status == CHANGED:
            changed += 1
            print(f"{'would update' if args.check else 'updated'} {name}: {note}")
            if not args.check:
                path.write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"evolution_metrics: {len(files)} entries, {changed} changed, {unmeasurable} unmeasurable")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
