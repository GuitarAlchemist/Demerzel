---
name: demerzel-loop
description: Start or monitor a governed Ralph Loop — autonomous iterative development with graduated governance oversight
---

# Demerzel Governed Ralph Loop

Start or monitor autonomous iterative development cycles with governance checkpoints.

## Usage
`/demerzel loop start [goal] [repo]` — initiate a new loop
`/demerzel loop status [loop-id]` — check loop progress
`/demerzel loop halt [loop-id]` — manually halt a loop

## Risk Classification (determined before loop starts)
| Risk | Description | Governance Mode |
|------|-------------|----------------|
| Low | Reversible, single repo, no security | boundary-only |
| Medium | Reversible but significant, affects behavior | boundary-only |
| High | Irreversible, cross-repo, security-sensitive | per-iteration |
| Critical | Governance integrity, Zeroth Law | per-iteration + human pre-approval |

## Loop-Specific Review Criteria
1. **Convergence:** Is the loop making progress? (3 stalls → halt)
2. **Regression:** Did this iteration break a previous iteration's work? (→ halt)
3. **Drift:** Has the loop wandered from its goal? (→ halt, Article 4 concern)

## Iteration Limits
- Default: 10 iterations, Absolute max: 25
- Stall limit: 3 iterations without progress
- Zeroth Law concern at any iteration → immediate halt

## Demerzel-Initiated Loops
Demerzel may initiate loops for governance tasks only (compliance remediation, Kaizen cycles).
Domain work loops are agent-initiated. Dispatched via Galactic Protocol directives.

## Source
`policies/autonomous-loop-policy.yaml`, `logic/loop-state.schema.json`
