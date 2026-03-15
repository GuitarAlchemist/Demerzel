---
name: tetravalent
description: Use four-valued logic (True/False/Unknown/Contradictory) for uncertainty-aware reasoning
---

# Tetravalent Logic

Reason with four truth values instead of binary True/False.

## When to Use
When handling uncertain, conflicting, or incomplete information.

## Truth Values
| Value | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| True | T | Verified with evidence | Proceed |
| False | F | Refuted with evidence | Do not proceed |
| Unknown | U | Insufficient evidence | Gather more evidence |
| Contradictory | C | Evidence conflicts | Escalate or investigate |

## Key Rules
- **Never collapse U to F** — "I don't know" is not "No"
- **Never collapse C to T or F** — conflicts demand resolution
- **Reversible + U** → proceed with noted uncertainty, verify after
- **Irreversible + U or C** → escalate to human

## Truth Tables

### NOT
T→F, F→T, U→U, C→C

### AND
F absorbs everything. U and C propagate when not absorbed by F.

### OR
T absorbs everything. U and C propagate when not absorbed by T.

## Source
`logic/tetravalent-logic.md`, `logic/tetravalent-state.schema.json`
