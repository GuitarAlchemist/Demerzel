# Hexavalent Observation Merge

## Overview

This document specifies how observations from multiple sources (tars,
ix, Demerzel, and any future agent) combine into a single hexavalent
belief state. The merge is a **stateless, CRDT-correct, pure
function** from a set of observations to a derived distribution, with
an auxiliary contradiction-synthesis step.

This is the governance-layer companion to `hexavalent-logic.md`:
where that doc specifies *the six values* T/P/U/D/F/C, this one
specifies *what happens when multiple sources disagree* about a
claim.

**Related artifacts:**

- `schemas/session-event.schema.json` — canonical JSON Schema for
  the SessionEvent type including the `ObservationAdded` variant
  this merge operates on
- `schemas/fuzzy-distribution.schema.json` — the derived output
  distribution type
- `logic/hexavalent-logic.md` — the six-value truth vocabulary
- `logic/fuzzy-membership.md` — the underlying fuzzy algebra
- `logic/tetravalent-logic.md` — the four-value precursor

## Why this document exists

As of 2026-04-11, the ix harness ships with `ix_triage_session`, an
end-to-end governed scenario that dispatches LLM-proposed actions
through a middleware chain. Phase 1 of the cross-repo "Path C"
design extends this pattern across the ix ↔ tars process boundary.

When multiple agents contribute observations about the same claim,
**a governance system must specify how those observations combine**.
Without a deterministic merge rule, agents can disagree silently and
the coordinator (today: the Claude Code client) has no principled
way to decide whether to escalate, proceed, or block.

This document defines that merge rule.

## Core claim: observations form a G-Set CRDT

Each observation is a quintuple:

```
HexObservation := {
    source       : string                 // "tars" | "ix" | "demerzel-merge" | ...
    diagnosis_id : string                  // content hash of the originating diagnosis
    round        : u32                     // remediation round number
    ordinal      : u32                     // monotone position within (source, diagnosis_id, round)
    claim_key    : string                  // see "Claim Key Grammar" below
    variant      : "T"|"P"|"U"|"D"|"F"|"C" // hexavalent value
    weight       : f64                     // (0.0, 1.0]
    evidence     : string?                 // optional short description
}
```

**The deduplication key** is `(source, diagnosis_id, round, ordinal)`.
Two observations with the same key are the same observation.

**The merge operation** is set union:

```
merge(A, B) := A ∪ B
```

This makes the state a **state-based CRDT**, specifically a G-Set
(grow-only set):

| Law | Why it holds |
|---|---|
| Commutative | Set union: `A ∪ B = B ∪ A` |
| Associative | Set union: `(A ∪ B) ∪ C = A ∪ (B ∪ C)` |
| Idempotent | `A ∪ A = A` |
| Monotone | State only grows; no removal |

The hexavalent **distribution** is a pure derivation from the set —
it is not itself the CRDT state. This separation matters because
*distributions under mixture fail associativity*, so a naive
"merge two distributions by averaging" is not CRDT-correct. The G-Set
of observations is; the distribution is the observable.

## Claim Key Grammar

Two observations contradict only when they make claims about **the
same thing on the same axis**. The grammar for identifying "the same
thing" is:

```
claim_key   := action_key "::" aspect
action_key  := tool_name [":" target_hint]
aspect      := "valuable"      // will this action advance the goal?
             | "safe"          // will it execute without blast-radius damage?
             | "reversible"    // can we roll back if it fails?
             | "timely"        // does it respect current deadlines?
             | "reproducible"  // will it produce the same result next time?
             | "reliable"      // is this SOURCE itself trustworthy? (harness adapters)
             | "meta_conflict" // reserved for derived cross-aspect conflicts
```

### Canonical examples

| claim_key | Interpretation |
|---|---|
| `ix_stats::valuable` | Is calling `ix_stats` helpful? |
| `ix_context_walk:ix_math::eigen::jacobi::valuable` | Is walking that specific target helpful? |
| `restart_gpu_service::safe` | Is restarting the GPU service safe to execute? |
| `git_gc::reversible` | Can `git gc` be rolled back? |
| `ix_cache_prune::meta_conflict` | Derived — cross-aspect disagreement on this action |

### Rules

1. **Default aspect is `valuable`.** Observations that omit the aspect
   are treated as claims about value.
2. **`action_key` reuses the loop-detector convention.** If an action
   has a `target_hint`, include it: `tool_name:target_hint`. This
   ensures two observations about `ix_context_walk` with different
   targets do NOT contradict each other.
3. **`meta_conflict` is reserved.** Only the merge function produces
   observations with `aspect=meta_conflict`; no agent should emit
   them directly.
4. **Claim keys are case-sensitive** and must exactly match for
   contradiction detection. Canonicalization (lower-casing, trimming
   whitespace) is the responsibility of the agent producing the
   observation; the merge function does not normalize.

### Adding new aspects

New aspects MAY be added in minor versions of this document, but:
- Aspect names MUST be kebab-case alphanumeric with no `::`
- Aspect names MUST be added to the Belnap table rules below
- Aspect names MUST NOT shadow existing ones
- Changes MUST cite a motivating governance case

## Belnap-extended Contradiction Table

When the merge function encounters multiple observations on the
**same claim_key** from **different sources**, it may synthesize
a new observation with `variant=C, source=demerzel-merge` to
represent the disagreement.

The table below specifies which pairs trigger synthesis and at what
weight. A cell shows either `—` (no synthesis) or `w` where `w` is
a multiplier applied to `min(weight_a, weight_b)`.

|       | **T** | **P** | **U** | **D** | **F** | **C** |
|-------|-------|-------|-------|-------|-------|-------|
| **T** | —     | —     | —     | 0.8   | **1.0** | —   |
| **P** | —     | —     | —     | 0.5   | 0.8   | —     |
| **U** | —     | —     | —     | —     | —     | —     |
| **D** | 0.8   | 0.5   | —     | —     | —     | —     |
| **F** | **1.0** | 0.8 | —     | —     | —     | —     |
| **C** | —     | —     | —     | —     | —     | —     |

### Cell-by-cell rationale

- **T + F → C 1.0** (full contradiction). One source says "definitely
  yes," the other says "definitely no." Maximum synthesized weight.
- **T + D, D + T → C 0.8** (strong). Definite yes meets evidence-
  leaning no. The certain side dominates slightly, but the
  disagreement is meaningful.
- **P + F, F + P → C 0.8** (strong, mirror of above). Evidence-
  leaning yes meets definite no.
- **P + D, D + P → C 0.5** (soft). Both sides only "leaning" — the
  signal is real but weaker. Still synthesized so the distribution
  knows there's disagreement.
- **U + anything → —** (unknown preserves). Classical Belnap behavior:
  unknown cannot contradict anything. The unknown observation still
  counts toward the distribution; it just doesn't trigger synthesis.
- **C + anything → —** (contradictory is terminal). Once something is
  contradictory, adding more evidence doesn't make it more
  contradictory in a way the synthesizer should amplify.
- **Same-side pairs** (T+P, P+T, D+F, F+D) → `—` (agreement with
  different confidence, NOT contradiction). These are the cells that
  distinguish this table from a naive "any two different variants
  disagree" rule.

### Reasoning about same-side pairs

The diagonal split is what makes this a governance-useful rule. If
tars says `T` ("I've verified X helps") and ix says `P` ("my trace
suggests X helps"), these are **agreement at different certainty
levels**, not a disagreement. The merge should record both
observations and let the distribution's final mass reflect the
cumulative support — not synthesize a contradiction.

The same applies on the negative side: tars `D` ("seems unhelpful")
+ ix `F` ("execution refuted") is a stronger negative conclusion,
not a conflict.

## Meta-Conflict Rule (cross-aspect contradiction)

The Belnap table handles **same-aspect** contradictions. But a
governance system also needs to catch **cross-aspect** disagreements:

> tars: `restart_gpu_service::valuable = T, 0.9` (definitely helps)
> ix: `restart_gpu_service::safe = F, 1.0` (refused on blast radius)

These observations are about the **same action** but **different
aspects**. They don't directly contradict (no same-claim_key pair),
so the Belnap table produces nothing. But a human reviewer would
rightly say: "tars and ix disagree about whether to run this."

The **meta-conflict rule** catches this:

```
for each action_key with observations from multiple sources:
    positives = {o for o in observations if o.variant in (T, P)}
    negatives = {o for o in observations if o.variant in (D, F)}
    for (pos_obs, neg_obs) in product(positives, negatives):
        if pos_obs.aspect == neg_obs.aspect:
            continue  # already handled by direct contradiction
        if pos_obs.source == neg_obs.source:
            continue  # a single source disagreeing with itself is not a cross-source conflict
        emit HexObservation(
            source       = "demerzel-merge",
            claim_key    = f"{action_key}::meta_conflict",
            variant      = C,
            weight       = min(pos_obs.weight, neg_obs.weight),
            evidence     = f"cross-aspect: {pos_obs.source}:{pos_obs.aspect}:{pos_obs.variant} "
                           f"vs {neg_obs.source}:{neg_obs.aspect}:{neg_obs.variant}",
        )
```

Weight is `min(w_pos, w_neg)` without a Belnap multiplier — cross-
aspect conflicts are treated at full strength because they require
human judgment to reconcile (one source is claiming value, another
is claiming a constraint).

The synthesized observation has a distinct `claim_key` ending in
`::meta_conflict` so it doesn't collide with direct contradictions
on the same action.

## Derivation: observations → distribution

Given a set `obs` of observations (both original and synthesized),
the hexavalent distribution is:

```
weights[v] = sum(o.weight for o in obs if o.variant == v)     for v in {T,P,U,D,F,C}
total      = sum(weights.values())
if total == 0:
    return uniform distribution over the six variants
else:
    return {v: weights[v] / total for v in {T,P,U,D,F,C}}
```

The distribution is the input to the existing escalation logic in
`ix-fuzzy::escalation_triggered`: if `dist[C] > ESCALATION_THRESHOLD`
(currently 0.3), the plan must be escalated rather than executed.

**Because synthesized C observations are folded in before
normalization**, cross-source disagreements automatically push the
distribution toward escalation without any special case in the
escalation checker. The math enforces the governance.

## Staleness Policy (the drift budget)

A pure G-Set grows forever. Without eviction, the observation set
becomes dominated by ancient rounds and new signals have no
influence.

**Staleness rule:** observations with `round < current_round - K`
are dropped from the merge input before derivation. `K` is the
**constitutional drift budget** — how many rounds of history the
governance system considers current.

**Default K:** 5 rounds. Justification: empirically, a remediation
scenario that hasn't converged in 5 rounds is a signal the
diagnosis is wrong, not that the remediations are ineffective. At
that point the algedonic channel should flag for human review
anyway.

**Staleness is policy, not math.** Adjusting `K` is a governance
decision that affects how much "institutional memory" the merge
considers. Setting `K=1` makes the merge purely reactive (only
this round matters). Setting `K=∞` makes the merge a pure
accumulator (everything ever observed counts equally).

**Future work:** replace the flat staleness window with a weighted
decay function (e.g., exponential with half-life 3 rounds). The
current flat window is simpler to reason about and easier to audit.

## CRDT Correctness Proof Obligations

Any implementation of this merge MUST satisfy the following tests:

1. **Commutativity:** for all `A, B`, `merge(A, B) == merge(B, A)`.
2. **Associativity:** for all `A, B, C`, `merge(merge(A, B), C) == merge(A, merge(B, C))`.
3. **Idempotence:** for all `A`, `merge(A, A) == A`.
4. **Monotonicity:** for all `A, B`, `|merge(A, B)| >= max(|A|, |B|)`.
5. **Deduplication by key:** two observations with the same
   `(source, diagnosis_id, round, ordinal)` tuple must merge to one.
6. **Belnap symmetry:** the synthesized `C` observation for `(T, F)`
   at the same claim_key must be the same regardless of which
   observation was added first.

The `demerzel-merge` source observations (the synthesized
contradictions) MUST be deterministic in their ordinals so the
merge is reproducible — two independent runs on the same input
produce the same output.

## Non-Goals

- **Probabilistic merging.** This is a set-based CRDT, not a
  Bayesian update. The distribution is a derivation over masses,
  not a posterior over likelihoods.
- **Cross-claim reasoning.** The merge only contradicts observations
  with matching or closely-related claim keys. Inferring "tars said
  X helps, therefore Y must also help" is the LLM's job, not this
  function.
- **Authentication.** Observations are trusted by `source` field
  at face value. Verifying that `source=tars` was actually emitted
  by tars is the job of the SessionLog signing layer (future work),
  not the merge.
- **Efficiency at scale.** The naive implementation is O(N²) in the
  number of observations per claim key. For expected sizes
  (hundreds of observations per session), this is trivial. If it
  becomes a bottleneck, index by claim_key first.

## Version

- **1.0** (2026-04-11) — initial specification. Six variants,
  Belnap-extended table, meta-conflict rule, staleness budget K=5.
