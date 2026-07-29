---
category: harness
date: 2026-07-29
topic: A guard pointed at the wrong subject is indistinguishable from no guard — six instances in one session where the mechanism ran, went green, produced output, and measured something other than the thing it existed to protect
source: issues #863 / #844 / #860, PRs #857 / #858 / #865, ga#605 spike, jules-auto-delegate audit
---

# The guard was running. It was looking somewhere else.

## The prior lesson, and why it wasn't enough

Demerzel already knows **green ≠ alive**: a scheduled workflow that reports
`success` while emitting nothing is dead, and the exit code will never tell you.
That lesson produced freshness guards, the anti-swallow sweep, and the
born-dead-tripwire discipline.

This session found the next failure one level in. Six mechanisms were **alive,
running, green, and producing real output** — and each was measuring something
other than the thing it existed to protect. Liveness checks cannot catch this.
The guard is not dead. It is looking in the wrong direction, confidently.

## The six

**1. The budget gate evaluated the right policy against the wrong provider.**
`run_afk_cycle.py --backend local` runs `claudeCode("claude-opus-4-8")` and
forwards `ANTHROPIC_API_KEY` into the sandbox — metered API spend. But
`BACKEND_PROVIDER` maps `local` → `codex-cli`, which the policy classifies
`tier: local-seat`, `requires_manual_approval: false`. The AIW budget gate exists
precisely to stop unapproved metered spend. It ran, it passed, and it was correct
about `codex-cli` — a provider that was not being used. (#863)

**2. The agent's oracle checked schemas, not the suite.**
`prompts/afk-implement.prompt.md` required `validate_governance.py` and nothing
else. A dispatched agent changed a function signature, watched its own gate go
green, and opened a PR with 299 tests red. The oracle worked perfectly on
schemas and the manifest, which were fine. (#858)

**3. The retired-model guard enumerated retirements, so it was blind to a model
that never existed.** `test_no_retired_models.py` matched a hand-maintained list
of retired ids. `demerzel-ideation` pinned `claude-sonnet-4-6-20250514` — not
retired, simply never a model. The guard passed. It also exempted any line
containing the word "retired", so `# retired id kept on purpose` sailed through.
(#860, fixed in #865)

**4. The freshness guard could not see event-triggered loops.**
`ecosystem-freshness` watches scheduled workflows. `cross-model-review` is
PR-triggered, so a week of fabricated placeholder reviews was invisible to the
mechanism built to notice exactly that. (#844)

**5. Jules delegation reported success for a month of nothing.**
`jules-auto-delegate` runs every 30 minutes and skips issues carrying
`<!-- jules-delegated -->`. Five issues were marked delegated on 2026-06-29/30
and produced **zero PRs**. Every run since reported `success` — truthfully. It
had found nothing to do. "Nothing to do" and "delivered nothing in a month" are
the same green.

**6. GA spends 20% of its similarity weight on a constant.**
Not ours, but the same shape. `EmbeddingSchema.cs:122` declares partition
`CONTEXT` at similarity weight `0.20`, documented as *"temporal motion and
harmonic function"*. Measured across all 313,047 voicings: 11 of 12 dims are
identically zero and the survivor is a constant. The weighting mechanism works.
It weights nothing.

## The shape

Every one has the same structure:

> A mechanism M exists to protect property P.
> M is alive, runs on schedule, and returns a true answer —
> about subject S′, which is not the subject P is a property of.

The failure is never in M's logic. Auditing M's implementation finds nothing,
because the implementation is correct. The defect lives in the **binding** between
M and its subject: a lookup table, a path filter, an enumerated list, a marker, a
partition index. Bindings are boring, get written once, and are never revisited —
while the thing they point at moves.

And the tell is inverted from the liveness case. A dead loop is *cheap*. Three
loops fixed this session were free precisely because they were broken: ideation's
invalid id 400'd instantly, capability-expansion errored before billing. **Fixing
them made costs go up.** If you are watching spend as a health signal, a
correctly-working guard on a correctly-working loop looks worse than the broken
pair.

## What to do about it

**Ask what the guard is bound to, not whether it runs.** "Is the freshness check
green?" is the wrong question. "What set does it enumerate, and what is outside
that set?" is the right one. For every guard, name the subject explicitly and ask
what could change about the world without changing the binding.

**Prefer structural rules to enumerated ones.** #865's fix is the model: instead
of listing retired ids, reject *any* dated `claude-*-YYYYMMDD` literal in live
config. An enumerated list is a binding that rots silently; a structural rule
catches the case nobody thought to enumerate — including the one that was never
a model at all.

**Mutation-test the binding, not just the logic.** The born-dead discipline says
prove the guard fires. Extend it: prove it fires *on the subject you care about*.
The comment-keyword bypass survived a guard whose logic was correct, and only
appeared when someone mutated the input rather than reading the code.

**Treat a cost drop as a symptom.** When a metered thing gets cheaper without a
deliberate change, ask what stopped happening. Cheap is what dead looks like on
the invoice.

## What it cost to learn

The budget gate instance was found by accident, after it had already let real
Opus spend through — surfaced only because the owner asked *"who pumps on my
Anthropic key?"* and the answer required reading `BACKEND_PROVIDER` next to
`main.mts` rather than either alone. Nothing flagged it. The mechanism designed to
flag it was, itself, the sixth instance of the pattern.

Related: [`2026-07-28-a-constraint-is-worth-its-enforcement-path.md`](2026-07-28-a-constraint-is-worth-its-enforcement-path.md)
(a constraint is worth its enforcement path) and
[`2026-07-25-partial-sweep-of-a-shared-seam-recurs.md`](2026-07-25-partial-sweep-of-a-shared-seam-recurs.md)
(fix by where the value lives). This is the third in the sequence: *and check what
the enforcer is pointed at.*
