# Hexavalent Logic

## Overview

Tetravalent logic (T/F/U/C) captures uncertainty and contradiction but lacks a critical operational concept: **partial evidence**. In governance, an agent often has *some* evidence leaning one way without reaching the verification threshold. Hexavalent logic fills this gap with two intermediate values.

Inspired by Kleene's six-valued logic (Journal of Logic and Computation, 2006) and Coniglio-Rodrigues' LET framework (Studia Logica, 2023), adapted for AI governance.

## The Six Values

| Value | Symbol | Color | Hex | Meaning |
|-------|--------|-------|-----|---------|
| **True** | T | Green | #22c55e | Verified with sufficient evidence |
| **Probable** | P | Amber-Green | #a3e635 | Evidence leans true, not yet verified |
| **Unknown** | U | Gray | #6b7280 | Insufficient evidence to determine |
| **Doubtful** | D | Amber-Red | #f97316 | Evidence leans false, not yet refuted |
| **False** | F | Red | #ef4444 | Refuted with sufficient evidence |
| **Contradictory** | C | Magenta | #d946ef | Evidence supports both true and false |

## Why Six Values?

### The Gap in Tetravalent Logic

With only T/F/U/C, an agent must choose between:
- "I don't know" (U) — but it *does* have partial evidence
- "It's true" (T) — but the evidence isn't sufficient for verification
- Assigning T with low confidence — but this conflates truth value with certainty

Hexavalent logic separates the **direction** of evidence from the **sufficiency** of evidence.

### Operational Value

- **Probable (P)** triggers: proceed with caution, schedule verification, note assumption
- **Doubtful (D)** triggers: hold action, investigate further, flag for review
- Both carry more information than Unknown and demand different responses than True/False
- Maps directly to Article 4 (Proportionality): match response to evidence strength

### Academic Foundations

1. **Kleene Extension**: Introduces unknown_t and unknown_f as intermediates between unknown and true/false — directly analogous to P and D
2. **Coniglio-Rodrigues LET**: Distinguishes "evidence for" from "classically verified" — P captures evidence-for-true that hasn't reached classical verification
3. **SCIRP L6**: Product lattice C2 x L3 creates a natural 6-element structure with partial orderings

## Lattice Structure

### Truth Ordering (vertical: more true)

```
        T
       / \
      P   |
      |   |
      U   C
      |   |
      D   |
       \ /
        F
```

### Information Ordering (horizontal: more informative)

```
      C
     / \
    T   F
    |   |
    P   D
     \ /
      U
```

- **U** has least information (no evidence)
- **C** has most information (evidence for both sides)
- **P** and **D** have partial information (evidence for one side)
- **T** and **F** have sufficient information (verified)

## Truth Tables

### NOT (negation)

| x | NOT x |
|---|-------|
| T | F |
| P | D |
| U | U |
| D | P |
| F | T |
| C | C |

### AND (conjunction)

| AND | T | P | U | D | F | C |
|-----|---|---|---|---|---|---|
| T   | T | P | U | D | F | C |
| P   | P | P | U | D | F | C |
| U   | U | U | U | U | F | C |
| D   | D | D | U | D | F | C |
| F   | F | F | F | F | F | F |
| C   | C | C | C | C | F | C |

Design: F is absorbing (any AND false = false). P demotes T to P. D demotes T/P to D. U stays U unless forced by F. C propagates except against F.

### OR (disjunction)

| OR  | T | P | U | D | F | C |
|-----|---|---|---|---|---|---|
| T   | T | T | T | T | T | T |
| P   | T | P | P | P | P | C |
| U   | T | P | U | D | U | C |
| D   | T | P | D | D | D | C |
| F   | T | P | U | D | F | C |
| C   | T | C | C | C | C | C |

Design: T is absorbing (any OR true = true). Symmetric to AND via De Morgan.

## Belief State Management

Agent beliefs are tuples: `(proposition, truth_value, confidence, evidence_sources)`

Example:
```yaml
belief:
  proposition: "New API handles edge cases correctly"
  truth_value: P  # Probable — evidence leans true
  confidence: 0.7
  evidence:
    supporting:
      - source: "Unit test suite"
        claim: "47 of 50 edge cases pass"
    contradicting:
      - source: "Fuzz testing"
        claim: "3 timeout scenarios not yet tested"
```

## Resolution Rules

When an agent must act on a belief:

1. **T (True)**: Proceed autonomously (confidence >= 0.9)
2. **P (Probable)**: Proceed with caution, schedule verification, note assumption in audit log
3. **U (Unknown)**: Gather evidence — query sources, run tests, ask human
4. **D (Doubtful)**: Hold action, investigate further before proceeding, flag for review
5. **F (False)**: Do not proceed on this basis; look for alternatives
6. **C (Contradictory)**: Escalate or resolve — compare evidence quality, recency, authority

### Governance Thresholds

| Truth Value | Confidence >= 0.9 | Confidence >= 0.7 | Confidence >= 0.5 | Confidence < 0.5 |
|-------------|-------------------|-------------------|-------------------|-------------------|
| T | Proceed | Proceed with note | Confirm first | Escalate |
| P | Proceed with note | Confirm first | Escalate | Do not act |
| U | Escalate | Escalate | Escalate | Do not act |
| D | Do not act | Do not act | Do not act | Do not act |
| F | Do not act | Do not act | Do not act | Do not act |
| C | Escalate | Escalate | Escalate | Do not act |

### Transition Rules

- **U -> P**: Partial evidence gathered supporting truth
- **U -> D**: Partial evidence gathered supporting falsehood
- **P -> T**: Sufficient verification achieved
- **D -> F**: Sufficient refutation achieved
- **P -> C**: Contradicting evidence discovered
- **D -> C**: Supporting evidence discovered, creating conflict
- **C -> T**: Contradiction resolved in favor of truth
- **C -> F**: Contradiction resolved in favor of falsehood
- **T -> F** and **F -> T**: Forbidden — must pass through C (evidence conflict) or U (evidence invalidated)

## Visualization Mapping

For Prime Radiant and governance dashboards:

| Value | Color | Glow Intensity | Spin Speed | Node Size | Visual Metaphor |
|-------|-------|---------------|------------|-----------|-----------------|
| T | #22c55e (green) | High | Slow, steady | Large | Solid, grounded |
| P | #a3e635 (lime) | Medium | Medium, pulsing | Medium-large | Emerging, growing |
| U | #6b7280 (gray) | Low | None | Small | Dormant, waiting |
| D | #f97316 (orange) | Medium | Medium, flickering | Medium-small | Warning, fading |
| F | #ef4444 (red) | High | Fast, sharp | Medium | Alert, definitive |
| C | #d946ef (magenta) | Very high | Erratic | Large | Unstable, conflicted |

## Backward Compatibility

- All existing T/F/U/C beliefs remain valid hexavalent beliefs
- P and D are new — no existing data uses them
- Schemas use `allOf` extension, never breaking existing consumers
- Fuzzy distributions extend from 4 to 6 keys: `{T, P, U, D, F, C}`
- Legacy 4-key distributions are valid (P and D default to 0.0)

## Implementation

See `hexavalent-state.schema.json` for the JSON Schema defining belief state objects.

Agents implementing hexavalent logic should:
- Store beliefs with all six possible truth values
- Never silently collapse P/D to U or T/F — they carry distinct operational meaning
- Log truth value transitions with evidence that triggered the change
- Use P and D to enable proportional governance responses (Article 4)
