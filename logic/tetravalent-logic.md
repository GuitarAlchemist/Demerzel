# Tetravalent Logic

## Overview

Standard boolean logic (True/False) is insufficient for agent reasoning where uncertainty and contradiction are normal operating conditions. Tetravalent logic extends the truth domain to four values:

| Value | Symbol | Meaning |
|-------|--------|---------|
| **True** | T | Verified with sufficient evidence |
| **False** | F | Refuted with sufficient evidence |
| **Unknown** | U | Insufficient evidence to determine |
| **Contradictory** | C | Evidence supports both True and False |

## Why Four Values?

### The Problem with Binary Logic in Agent Systems

- An agent asked "Is the API stable?" may have conflicting evidence (docs say yes, recent errors say no)
- Binary logic forces a choice: pick True or False, losing information
- "Unknown" captures genuine ignorance (haven't checked yet)
- "Contradictory" captures genuine conflict (checked, found disagreement)

### Operational Value

- **Unknown** triggers information-gathering actions
- **Contradictory** triggers escalation or deeper investigation
- Neither is equivalent to False — they demand different responses

## Truth Tables

### NOT (negation)

| x | NOT x |
|---|-------|
| T | F |
| F | T |
| U | U |
| C | C |

### AND (conjunction)

| AND | T | F | U | C |
|-----|---|---|---|---|
| T | T | F | U | C |
| F | F | F | F | F |
| U | U | F | U | C |
| C | C | F | C | C |

### OR (disjunction)

| OR | T | F | U | C |
|----|---|---|---|---|
| T | T | T | T | T |
| F | T | F | U | C |
| U | T | U | U | C |
| C | T | C | C | C |

## Belief State Management

Agent beliefs are tuples: `(proposition, truth_value, confidence, evidence_sources)`

Example:
```yaml
belief:
  proposition: "API v2 is backward compatible"
  truth_value: C  # Contradictory
  confidence: 0.6
  evidence:
    supporting:
      - source: "API changelog v2.0"
        claim: "All v1 endpoints preserved"
    contradicting:
      - source: "integration test results"
        claim: "3 endpoints return different response shapes"
```

## Resolution Rules

When an agent must act on a Contradictory or Unknown belief:

1. **Unknown → gather evidence**: Query additional sources, run tests, ask human
2. **Contradictory → escalate or resolve**: Compare evidence quality, recency, authority
3. **If action is reversible**: Proceed with noted uncertainty, verify after
4. **If action is irreversible**: Escalate to human

## Implementation

See `tetravalent-state.schema.json` for the JSON Schema defining belief state objects.

Agents implementing tetravalent logic should:
- Store beliefs with all four possible truth values
- Never silently collapse Unknown or Contradictory to False
- Log truth value transitions with evidence that triggered the change
