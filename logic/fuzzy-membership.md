# Fuzzy Membership for Tetravalent Logic

## Overview

Fuzzy membership extends Demerzel's tetravalent logic (T/F/U/C) with continuous membership degrees. Inspired by Jean-Pierre Petit's Logotron — not all truths are equally accessible. Membership captures how much evidential weight supports each truth value.

## Fuzzy Distribution

- A fuzzy distribution is an object `{T, F, U, C}` where each value is in [0, 1]
- Sum constraint: T + F + U + C = 1.0 (±0.01 tolerance for floating point)
- Argmax rule: `truth_value` must equal the key with highest membership
- Tiebreak order: C > U > T > F (conservative — contradictions and unknowns surface first)
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
result.F = max(a.F, b.F)
result.U = max(a.U, b.U)
result.C = max(a.C, b.C)
Normalize: divide each by sum to restore sum=1.0
```

### OR

```
result.T = max(a.T, b.T)
result.F = min(a.F, b.F)
result.U = max(a.U, b.U)
result.C = max(a.C, b.C)
Normalize: divide each by sum to restore sum=1.0
```

### NOT

```
result.T = a.F
result.F = a.T
result.U = a.U
result.C = a.C
No normalization needed (swap preserves sum=1.0 invariant)
```

## Resolution Rules

- **Escalation**: When result.C > 0.3, trigger escalation to human (contradictory evidence exceeds tolerance)
- **Sharpening**: When argmax membership > 0.8, collapse fuzzy to discrete truth value with confidence = argmax membership
- Escalation fires *after* operations complete — compute first, then check

## Edge Cases

1. **Tied argmax** (e.g., {T:0.25, F:0.25, U:0.25, C:0.25}): Use tiebreak order C > U > T > F. Result: truth_value = C, triggering escalation.
2. **NOT on pure-U** ({T:0, F:0, U:1.0, C:0}): NOT swaps T↔F (both 0), preserves U and C. Result is identical to input — negating pure uncertainty yields uncertainty.
3. **AND/OR with C > 0.3**: Escalation fires after the operation completes. Compute result first, then check C threshold.
4. **All-zero membership**: Invalid — memberships must sum to 1.0.

## Semantic Predicates

Natural-language guards in state machine transitions that return fuzzy distributions. Written as `?"predicate description"` in the grammar. Evaluated by the reasoning engine (tars), not mechanically by Demerzel. Bridges formal logic with contextual judgment — the Logotron's "metalanguage" level.

## Integration

- Schema: `schemas/fuzzy-belief.schema.json` (extends `tetravalent-state.schema.json` via allOf)
- Grammar: `grammars/state-machines.ebnf` section 9 (fuzzy transition gates)
- Policy: `policies/alignment-policy.yaml` (fuzzy thresholds)
- Tests: `tests/behavioral/fuzzy-logic-cases.md`
