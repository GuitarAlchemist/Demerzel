---
category: harness
date: 2026-07-28
topic: A constraint is worth exactly its enforcement path — trace who validates before defending strictness, and when two copies of a contract exist only the enforced one is real
source: PR #839 REQUEST_CHANGES adjudication, issues #834 / #852, adversarial Fable 5 review
---

# The strict schema that guarded nothing

## What happened

An automated cross-model reviewer issued REQUEST_CHANGES on a PR that relaxed
`logic/loop-state.schema.json`, moving six fields — `worker`, `reviewer`,
`convergence`, `outcome`, `current_iteration`, and a per-iteration
`governance_check` — out of `required`. The objection read well:

> ...suggests potential lack of full auditability fields, indicating a partial
> change that should be completed for full system alignment.

It is the right instinct. Making a check pass by weakening the check is a real
anti-pattern, and this repo already has an open proposal about it (#641). The
reviewer was defending auditability against erosion.

It was defending nothing.

## What the investigation found

Four facts, each independently sufficient:

1. **No instance ever carried the fields.** Two loop instances exist in the
   entire repo history. Both were born in the minimal shape at their first
   commit. Not one ever had `worker`, `reviewer`, `convergence`, or `outcome`.
2. **No code reads them.** `grep -rln "convergence\|current_iteration" scripts/`
   returns empty.
3. **Nothing validated against that file.** `demerzel_kit.py` sets
   `SCHEMA_DIR = ROOT / "schemas"`. Write-time validation resolves to
   `schemas/loop-state.schema.json` — a *different file*. The strict copy in
   `logic/` was referenced by one line of policy prose and checked by nothing
   in CI. Its first-ever validation was a hand-run audit skill, sixteen months
   after it was written.
4. **It was unsatisfiable.** Its `target_repo` enum was `["ix", "tars", "ga"]`.
   Every real instance is `repo: "demerzel"`. No emitter, however enriched,
   could ever have passed it.

The schema described a system that was never built, was never checked against
the system that was, and could not have been satisfied by it.

## Root cause, stated generally

**A constraint is worth exactly its enforcement path, not its text.**

Strictness in an unenforced artifact is decorative. It reads like a guarantee,
survives review like a guarantee, and gets defended like a guarantee — while
guaranteeing nothing. Worse, it actively misleads: the false belief it propped
up ("all artifacts schema-validated", T/0.98) was itself a governance artifact
that had to be downgraded.

Before defending a constraint, trace three questions to a specific file and line:

- **Who validates against this?** Name the caller. If you cannot, stop.
- **When does that run?** Write time, CI, or a skill someone remembers to invoke?
- **What happens on failure?** If the answer is "a red run nobody watches," you
  have a decoration, not a gate.

The same three questions dispose of "keep it failing as a tripwire." A failing
validation is a signal only if something reads it. This one sat failing from
2026-06-23 to 2026-07-25 undetected.

## The second finding: duplicate contracts

Two files described one artifact class, with different `$id`s and divergent
required sets, both cited by the same policy at different line numbers.

The enforced one stayed correct — the emitter validated against it at every
write, and a regression test pinned it. The unenforced one drifted freely for
sixteen months until it became unsatisfiable, and nobody noticed because
nothing ever asked it a question.

**When two copies of a contract exist, the enforced one is the real one.** The
other is documentation that lies with increasing confidence over time.

Aligning them is a snapshot. Deduplication is the fix — and a snapshot taken
without a CI check binding the copies together will be stale by the next edit.
Tracked here as #852.

Note the knock-on this exposed: the follow-up issue meant to restore the
"lost" fields (#834) named the *unenforced* file. Enriching it would have
changed nothing about what the emitter may produce. A follow-up aimed at the
decorative copy is itself decorative.

## The third finding: what adversarial review is actually for

The objection was adjudicated by a subagent instructed to default to refusal
and to attack the arguments for merging. It did not simply overturn the
reviewer — it found a **better objection than the reviewer had made**.

The reviewer said: *you weakened a guarantee.* False; there was no guarantee.

The adversary said: *you weakened it further than your own stated criterion.*
The PR claimed to relax to "the minimal core shape currently emitted by
`run_afk_cycle.py`" — but the emitter unconditionally writes `risk` and
`governance_mode`, both instances carry them, and the enforced sibling schema
had required them since 2026-03-20. The diff undershot its own justification,
and stripped three enums while documenting `status` with example values that
were not operational states at all.

That is an internal inconsistency, not a matter of taste, and it was invisible
to the surface objection. The fix was six lines and cost no calendar time —
the PR was already waiting on a human attestation, so the amendment rode the
same touch.

**Adversarial review earns its cost when it produces a sharper objection than
the one it was asked to evaluate — not when it ratifies or overturns.** A
reviewer that only ever agrees or disagrees with the framing it was handed is
a slower version of the framing.

## Generalization

- Trace the enforcement path before defending, reverting, or restoring any
  constraint. Name the validating caller or concede there is none.
- Treat "a follow-up ticket will restore this" as suspect twice over: the
  follow-up may die silently, *and* it may target the wrong artifact. Check
  which file the follow-up actually names against which file is enforced.
- When you find two definitions of one contract, do not align them and move on.
  Alignment without a binding check is a snapshot with a decay date.
- Give adversarial reviewers a default-refuse posture and the primary sources,
  then let them reframe the question. Constraining them to your options wastes
  the reason you called them.

## Related

- `docs/solutions/harness/2026-07-25-partial-sweep-of-a-shared-seam-recurs.md` —
  same family: a fix whose scope was set by where the failure was observed.
- `docs/solutions/harness/2026-07-24-tripwire-must-read-committed-evidence.md` —
  a guard that cannot observe what it asserts on. This is its mirror: a
  constraint that nothing observes at all.
- #839, #834, #852, #641.
