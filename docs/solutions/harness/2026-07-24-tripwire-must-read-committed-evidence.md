---
category: harness
date: 2026-07-24
topic: A CI freshness tripwire that globs gitignored runtime state is born dead — it must read committed evidence
source: PR #808 (ml-governance-schedule.yml), cross-model review findings SOL-808-P1/P2a, fix 958b4ea
---

# The death tripwire that was born dead

## Symptom

`ml-governance-schedule.yml` shipped as the "death detector" for the ML-feedback
loop: a daily freshness leg asserting `state/oversight/ml-feedback-cycle-*.json`
was fresher than 3 days. It would have gone red on day one and stayed red
forever — those files are gitignored runtime I/O and never exist in a CI
checkout. The companion smoke leg (`run_ml_feedback_cycle.py --dry-run`) exited
0 unconditionally, so it passed even with all four producers unresolved. Caught
by cross-model review before the first scheduled run, not by us.

## Root cause

Two instances of the same category error: **the check ran in an environment
that cannot see the evidence it asserts on.** CI checkouts contain only tracked
files; a tripwire that globs gitignored paths tests the .gitignore, not the
loop. And a dry-run whose exit code ignores step errors proves the entrypoint
parses, not that the plan is coherent.

## Fix

- Freshness leg now reads the **committed** evidence trail: max `last_updated`
  across `state/beliefs/*.belief.json`, which the governor bumps every cycle
  and the operator commits. Threshold widened 3d→7d because landings are
  commit-bound (observed belief-commit gaps reach 5 days).
- Bonus property: the guard now also trips when the loop *runs* but its output
  stops being committed — death by another name that the original design
  couldn't see at all.
- Smoke leg: `--strict` flag added (any errored plan step → exit 1) and the
  workflow checks out public `GuitarAlchemist/ix` so producers resolve from a
  real `origin/main`, making the smoke test the actual producer contract.

## Rule

Before shipping any CI guard, ask: **does every file this check reads exist in
a fresh `actions/checkout`?** If the evidence is runtime state, either find its
committed shadow (belief files, badges, snapshots) or have the guard's own run
produce the evidence. Extends the silent-loop-death doctrine: green ≠ alive,
and red-by-construction ≠ a guard.
