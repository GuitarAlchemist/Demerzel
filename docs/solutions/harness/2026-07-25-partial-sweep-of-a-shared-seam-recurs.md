---
category: harness
date: 2026-07-25
topic: Fixing a shared-seam config value at one call site and not the others guarantees recurrence — sweep, then guard the sweep
source: Issue #703 (capability-expansion dead 4 weeks), PR #833, prior partial fix recorded in state/digests/pr-unknown-fix-afk-live-proof-bugs-pr-labeling-seam.md
---

# The fix that was correct, local, and insufficient

## Symptom

`demerzel-capability-expansion` failed every scheduled run from 2026-06-22 to
2026-07-13, then "succeeded" on 07-20 having produced nothing at all. Four weeks
of a governance loop being dead, three of them loudly and one of them silently.

The cause named itself in the run log:

```
##[warning]Capability analysis call failed:
llm_call: API error: model: claude-sonnet-4-20250514
```

That model id passed its retirement date on 2026-06-15. The first failing run was
2026-06-22 — the following Monday.

## The part worth compounding

**This exact id had already been diagnosed and fixed in this repo.** A prior
session found `council_emit`'s reviewer_b 404ing on `claude-sonnet-4-20250514`,
correctly identified it as a retired snapshot, and updated that call site to a
current model. The digest records it cleanly.

That fix was correct. It was also local. The same id remained in **five** other
places, including `.github/scripts/llm_call.sh` — the *shared* LLM seam whose
default every workflow inherits unless it overrides. So the bug was not fixed; it
was relocated out of view of the person who had just looked at it.

The recurrence is not bad luck. It is the predictable consequence of treating a
symptom site as the fault site. A config value in a shared seam has a blast
radius equal to its caller count, and the caller you happened to be debugging is
not privileged.

## Root cause, stated generally

**A shared-seam constant fixed at one call site will recur, because the fix's
scope was set by where the failure was observed rather than by where the value
lives.**

The failure surfaced at `council_emit` because that is where someone was looking.
It lived in `llm_call.sh`. Nothing about the debugging path leads from the former
to the latter unless you deliberately ask "where else does this value appear?"

Two properties made it worse here:

- **Dated snapshots are time bombs with a known fuse.** `claude-sonnet-4-20250514`
  worked perfectly until a date printed in public documentation, then began
  404ing everywhere simultaneously. The failure was scheduled, not random.
- **The loop swallowed it.** The analyze step collapsed every failure into
  `ANALYSIS_READY=false` and exited 0, so the producing steps skipped behind a
  green check. Green ≠ alive, again.

## Fix

1. Migrated the seam default to an undated id (`claude-sonnet-5`), and **swept all
   four live sites** — `llm_call.sh`, `demerzel-discussion-responder.yml`,
   `ga-chatbot-discussions.yml`, `templates/cross-model-review.yml`.
2. Added `scripts/test_no_retired_models.py`: a repo-wide sweep for retired model
   ids across live config (`.github`, `scripts`, `templates`, `pipelines`,
   `tools`), run by the existing `unittest discover` CI job. `docs/` and `state/`
   are deliberately out of scope — they record retired ids as incident history,
   and rewriting history to satisfy a linter is worse than the bug.
3. Made the loop fail visibly (`::error::` + `exit 1`) instead of skipping behind
   a green check.

Point 2 is the actual fix. Points 1 and 3 repair this instance; only the guard
converts "remember to sweep" from a habit into a property of the repo.

## Generalization

When a fix changes a **value** rather than **logic**, the sweep is part of the
fix, not follow-up work:

- Before editing, ask **where else does this literal appear in live config?** —
  not "where did the error come from". `grep` the value across the repo, and
  classify each hit as live vs. historical before touching any of them.
- If the value has an expiry (model snapshots, certs, API versions, pinned
  digests, deprecation-dated endpoints), a one-time sweep is insufficient — the
  next one expires later. Encode the retired set as a test so the *next*
  reintroduction fails in CI rather than in production four weeks later.
- Prefer undated/alias forms in shared seams. A dated pin belongs where the
  pinning is the point, not where it is incidental.

## Corollary: fixing the top failure exposes the next

Three further defects sat behind this one, each invisible until the one above it
was fixed — a 404 error body interpolated into JSON, `|| echo` fallbacks that
could never fire because a pipeline's exit status is its *last* command's, and a
label that had never existed with its error hidden by `2>/dev/null`. Three canary
runs were needed: failed → failed differently → green.

**A loop dead for four weeks has more than one thing wrong with it.** Budget for
iteration, and do not treat the first green step as a fixed loop — the loop is
fixed when it emits its artifact. Here that was issue #830, produced by canary
run 30139021949. Verifying the run went green would have been insufficient; the
07-20 run was green and produced nothing.

## Related

- `docs/solutions/harness/2026-07-24-tripwire-must-read-committed-evidence.md` —
  same family: a check that cannot observe what it asserts on.
- Issue #703, PR #833.
