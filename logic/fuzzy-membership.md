# Fuzzy Membership for Hexavalent Logic

## Overview

Fuzzy membership extends Demerzel's hexavalent logic (T/P/U/D/F/C) with continuous membership degrees. Inspired by Jean-Pierre Petit's Logotron — not all truths are equally accessible. Membership captures how much evidential weight supports each truth value.

## Fuzzy Distribution

- A fuzzy distribution is an object `{T, P, U, D, F, C}` where each value is in [0, 1]
- P (Probable) and D (Doubtful) are optional, defaulting to 0 for backward compatibility
- Sum constraint: T + P + U + D + F + C = 1.0 (+-0.01 tolerance for floating point)
- Argmax rule: `truth_value` must equal the key with highest membership
- Tiebreak order: C > U > D > P > T > F (conservative — contradictions and unknowns surface first, doubt before hope)
- Schema: `schemas/fuzzy-distribution.schema.json`

## Confidence vs. Membership

- **membership**: Distribution of belief across T/F/U/C. Expresses *what* you believe.
- **confidence**: Meta-confidence in the membership distribution itself. Expresses *how much you trust your own assessment*.
- Example: confidence 0.9 with membership {T:0.5, U:0.5} = "I'm quite sure it's genuinely ambiguous"
- Example: confidence 0.3 with membership {T:0.8, F:0.2} = "I think it's true but I don't trust my assessment"
- When membership is absent (legacy beliefs), confidence retains its original meaning from tetravalent-state.schema.json

## Fuzzy Operations

### AND

```
result.T = min(a.T, b.T)
result.P = min(a.P, b.P)
result.F = max(a.F, b.F)
result.D = max(a.D, b.D)
result.U = max(a.U, b.U)
result.C = max(a.C, b.C)
Normalize: divide each by sum to restore sum=1.0
```

### OR

```
result.T = max(a.T, b.T)
result.P = max(a.P, b.P)
result.F = min(a.F, b.F)
result.D = min(a.D, b.D)
result.U = max(a.U, b.U)
result.C = max(a.C, b.C)
Normalize: divide each by sum to restore sum=1.0
```

### NOT

```
result.T = a.F
result.P = a.D
result.U = a.U
result.D = a.P
result.F = a.T
result.C = a.C
No normalization needed (swap preserves sum=1.0 invariant)
```

## Resolution Rules

- **Escalation**: When result.C > 0.3, trigger escalation to human (contradictory evidence exceeds tolerance)
- **Sharpening**: When argmax membership > 0.8, collapse fuzzy to discrete truth value with confidence = argmax membership
- Escalation fires *after* operations complete — compute first, then check

## Edge Cases

1. **Tied argmax** (e.g., {T:0.17, P:0.17, U:0.17, D:0.17, F:0.16, C:0.16}): Use tiebreak order C > U > D > P > T > F. Result: truth_value = U (highest tied), triggering investigation.
2. **NOT on pure-U** ({T:0, P:0, U:1.0, D:0, F:0, C:0}): NOT swaps T<->F and P<->D (all 0), preserves U and C. Result is identical to input — negating pure uncertainty yields uncertainty.
3. **Legacy 4-value input** ({T:0.5, F:0.1, U:0.3, C:0.1}): P and D default to 0.0. Sum still equals 1.0. Fully backward compatible.
3. **AND/OR with C > 0.3**: Escalation fires after the operation completes. Compute result first, then check C threshold.
4. **All-zero membership**: Invalid — memberships must sum to 1.0.

## Semantic Predicates

Natural-language guards in state machine transitions that return fuzzy distributions. Written as `?"predicate description"` in the grammar. Evaluated by the reasoning engine (tars), not mechanically by Demerzel. Bridges formal logic with contextual judgment — the Logotron's "metalanguage" level.

## Generalized Fuzzy Types: FuzzyEnum and FuzzyDU

### FuzzyEnum<'T>

Generalizes the tetravalent fuzzy distribution to any enum type. A `FuzzyEnum<'T>` is a probability distribution over variants of type `'T`. The tetravalent distribution `{T, F, U, C}` is `FuzzyEnum<TruthValue>`.

**Properties:**
- `Memberships: Map<'T, float>` — variant to membership degree
- `ArgMax()` — variant with highest membership
- `IsSharp(threshold)` — true if argmax > threshold
- `Pure(variant)` — sharp (discrete) value: one variant = 1.0, rest = 0.0
- `Uniform(variants)` — equal distribution: each variant = 1/N

**Schema:** `schemas/fuzzy-enum.schema.json`

### FuzzyDU<'T, 'Payload>

Like FuzzyEnum but each variant carries an optional typed payload. Used when fuzzy classification needs associated data (e.g., BS detector with per-test evidence).

**Schema:** `schemas/fuzzy-du.schema.json`

### Generalized Operations

AND, OR, NOT, renormalize, and sharpen generalize from tetravalent to any FuzzyEnum:

- **AND:** min per variant, renormalize
- **OR:** max per variant, renormalize
- **NOT (generic):** invert (1.0 - v) per variant, renormalize
- **NOT (hexavalent):** swap T<->F and P<->D, preserve U/C (backward compatible with tetravalent when P=D=0)
- **Renormalize:** divide each by sum (idempotent)
- **Sharpen:** if argmax > threshold, collapse to discrete

### Computation Expression (FuzzyBuilder)

The `fuzzy { }` CE propagates membership through chained operations. Four strategies:

| Strategy | Combiner | Use Case |
|----------|----------|----------|
| Multiplicative | `a * b` | Default, good for independent evidence |
| Zadeh | `min(a, b)` | Classical fuzzy logic, conservative |
| Bayesian | `a*b / (a*b + (1-a)*(1-b))` | Posterior update, treats as evidence |
| Custom | user-defined | Domain-specific |

**FuzzyResult<'T>** carries `Outcomes: Map<'T, float>` and `Trace: FuzzyTrace list` for full auditability (Article 7).

### Unified Systems

Seven existing ad-hoc fuzzy systems unify under FuzzyEnum:

| System | Before | After |
|--------|--------|-------|
| Beliefs | `HexavalentTruthValue` | `FuzzyEnum<TruthValue>` |
| Grammar weights | `Map<string,float>` | `FuzzyEnum<HypothesisMethod>` |
| Risk gates | hardcoded string | `FuzzyEnum<RiskLevel>` |
| Persona routing | if/else chain | `FuzzyEnum<Persona>` |
| BS score | 4-test checklist | `FuzzyEnum<BsLevel>` |
| Governance decisions | Approve/Reject/Defer | `FuzzyEnum<Decision>` |
| Task priority | P0/P1/P2/P3 | `FuzzyEnum<Priority>` |

### Backward Compatibility

- Discrete `TruthValue.T` = `FuzzyEnum.Pure(T, [T;P;U;D;F;C])` = `{T:1.0, P:0.0, U:0.0, D:0.0, F:0.0, C:0.0}`
- Legacy 4-value distributions `{T, F, U, C}` remain valid — P and D default to 0.0
- Existing `BeliefState` gains optional `membership: FuzzyEnum<TruthValue>` field
- When membership is absent, `truth_value` and `confidence` retain original meaning
- All JSON schemas use `allOf` to extend, never breaking existing consumers

### Design Spec

Full specification: `docs/superpowers/specs/2026-03-22-fuzzy-enum-du-design.md`

## Integration

- Schema: `schemas/fuzzy-belief.schema.json` (extends `tetravalent-state.schema.json` via allOf)
- Schema: `schemas/fuzzy-enum.schema.json` (generalized fuzzy enum)
- Schema: `schemas/fuzzy-du.schema.json` (fuzzy discriminated union)
- Schema: `schemas/fuzzy-distribution.schema.json` (tetravalent-specific distribution)
- Grammar: `grammars/state-machines.ebnf` section 9 (fuzzy transition gates)
- Grammar: `grammars/gov-bs-generators.ebnf` (BS decoder productions)
- Policy: `policies/alignment-policy.yaml` (fuzzy thresholds)
- Tests: `tests/behavioral/fuzzy-logic-cases.md`
- Tests: `tests/behavioral/fuzzy-du-cases.md`
- Tests: `tests/behavioral/bs-decoder-cases.md`
- Skill: `.claude/skills/demerzel-bs-decode/SKILL.md`
- Directive: `contracts/directives/fuzzy-du-implementation.directive.md` (to tars)
