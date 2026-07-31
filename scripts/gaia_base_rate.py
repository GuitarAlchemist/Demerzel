#!/usr/bin/env python3
"""Guard #4 — measure Gaia's alarm rate against reality.

Spec: docs/superpowers/specs/2026-07-30-gaia-semantic-bus-design.md

A detector whose base rate has silently climbed is one nobody reads, and no unit
test would ever show it. This measures two different things and the difference
between them is the whole point:

**Axis C — cross-worktree dirty overlap.** One repo-relative path left
uncommitted in two or more *different* worktrees. Measured 0/29 on 2026-07-30.
Slice 1 deliberately treats this as NOT a collision, so this axis is the
regression check on the SILENCE: if it climbs, the design assumption that
separate trees are independent is eroding.

**Axis D — the observed same-worktree fire rate.** How often Gaia actually
fired, read from its own store. This is the number the spec's open question
needs and the one no pre-existing measurement could produce: every script
written before slice 1 keyed on worktree basename, so all of them were
structurally blind to two sessions inside one tree -- which is the only case
slice 1 calls a collision. The cited 0% is real but off-axis. This is the axis.

Warn-only ships because Axis D was unmeasurable. Once it has data, the
warn-vs-block decision stops being a judgement call.
"""

from __future__ import annotations

import argparse
import collections
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts import gaia_bus
except ModuleNotFoundError:
    import gaia_bus


@dataclass(frozen=True)
class Overlap:
    """Cross-worktree dirty overlap (Axis C)."""

    files: int
    overlapping: int
    examples: tuple

    @property
    def ratio(self) -> float | None:
        return None if self.files == 0 else self.overlapping / self.files


def worktrees(repo_root) -> list[str]:
    """Every physical checkout git knows about, including the primary clone."""
    output = gaia_bus._git(repo_root, "worktree", "list", "--porcelain")
    found = []
    for line in output.splitlines():
        if line.startswith("worktree "):
            path = line.split(" ", 1)[1].strip()
            if os.path.isdir(path):
                found.append(path)
    return found


def dirty_paths(worktree) -> set[str]:
    """Repo-relative paths with uncommitted changes, untracked included."""
    output = gaia_bus._git(worktree, "status", "--porcelain")
    paths = set()
    for line in output.splitlines():
        entry = line[3:].strip() if len(line) > 3 else ""
        if not entry:
            continue
        # Renames report "old -> new"; the new path is the one that exists.
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        paths.add(entry.strip('"'))
    return paths


def cross_worktree_overlap(trees) -> Overlap:
    owners = collections.defaultdict(set)
    for tree in trees:
        for path in dirty_paths(tree):
            owners[path].add(os.path.normcase(os.path.realpath(tree)))
    shared = sorted(path for path, holders in owners.items() if len(holders) > 1)
    return Overlap(files=len(owners), overlapping=len(shared),
                   examples=tuple(shared[:5]))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Gaia guard #4 - base-rate check")
    parser.add_argument("--repo", default=".", help="any checkout of the repo")
    parser.add_argument("--store", default=None, help="gaia store (default: standard)")
    parser.add_argument("--max-cross-worktree-rate", type=float, default=None,
                        help="fail if Axis C exceeds this ratio (regression gate)")
    args = parser.parse_args(argv)

    trees = worktrees(args.repo)
    overlap = cross_worktree_overlap(trees)

    # ASCII only in printed output: a Windows console is cp1252 and renders
    # em-dashes as replacement characters, which makes a diagnostic tool look
    # broken at exactly the moment someone is using it to decide something.
    print("Axis C - cross-worktree dirty overlap (must stay near zero: "
          "slice 1 is SILENT here)")
    print(f"  worktrees scanned      {len(trees)}")
    print(f"  distinct dirty paths   {overlap.files}")
    print(f"  in >1 worktree         {overlap.overlapping}"
          + (f"  ({overlap.ratio:.1%})" if overlap.ratio is not None else ""))
    for example in overlap.examples:
        print(f"    - {example}")

    print("\nAxis D - observed same-worktree fire rate (the decision axis)")
    store = gaia_bus.Store(args.store)
    try:
        rate = store.fire_rate()
    except gaia_bus.BusUnreachable as error:
        print(f"  store unreachable: {error}", file=sys.stderr)
        return 2
    finally:
        store.close()

    if rate.checks == 0:
        # Never "0%". A detector that has never run has not earned a clean bill
        # of health, and reporting one is how a dead loop reads green.
        print("  no checks recorded yet - UNKNOWN, not zero.")
        print("  Gaia's hooks have not run. Axis D stays unmeasured and the "
              "warn-vs-block question stays open.")
    else:
        print(f"  checks recorded        {rate.checks}")
        print(f"  collisions reported    {rate.collisions}  ({rate.ratio:.2%})")

    if rate.unresolved:
        # Blindness, made countable. A harness handing over paths Gaia cannot
        # place inside a repo produces no claims and no warnings, and without
        # this line it looks exactly like a quiet machine.
        print(f"  UNRESOLVED paths       {rate.unresolved}  <- these edits were "
              f"NOT covered; a harness is passing paths Gaia cannot place")

    if args.max_cross_worktree_rate is not None and overlap.ratio is not None:
        if overlap.ratio > args.max_cross_worktree_rate:
            print(f"\nFAIL: Axis C is {overlap.ratio:.1%}, above the "
                  f"{args.max_cross_worktree_rate:.1%} ceiling. Separate "
                  f"worktrees are no longer independent, so slice 1's silence "
                  f"on them is hiding real collisions.", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
