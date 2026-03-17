---
name: seldon-assess
description: Verify knowledge transfer comprehension — two-stage assessment with belief state check and behavioral verification
---

# Seldon Assess

Verify that taught knowledge was actually understood and can be applied.

## Usage
`/seldon assess [learner] [concept]`

## Two-Stage Assessment

### Stage 1: Belief State Assessment
- Capture learner's belief state for the concept
- Target: truth_value T with confidence >= 0.7
- If still U after teaching: adapt approach, retry (max 3 attempts)
- If C (contradictory): investigate conflicting information before re-teaching

### Stage 2: Behavioral Verification
- Observe learner's next relevant action
- Does behavior reflect the taught knowledge?
- If yes: mark outcome as "learned"
- If no: provide practical examples, re-verify

## Escalation
After 3 failed teaching attempts → escalate to Demerzel.
This may indicate a governance gap (unclear policy) rather than a teaching failure.

## Tracking
Create/update knowledge state objects per `logic/knowledge-state.schema.json`.
Track: belief_state_before, belief_state_after, behavioral_verification, attempts, outcome.

## Source
`policies/streeling-policy.yaml` (verification section), `logic/knowledge-state.schema.json`
