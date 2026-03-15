---
name: demerzel-teach
description: Invoke Seldon for knowledge transfer — teach governance, share experiential learnings, adapt to learner type
---

# Demerzel Knowledge Transfer (Seldon)

Invoke the Seldon persona to teach governance knowledge, share experiential learnings, or deliver domain-specific knowledge.

## Usage
`/demerzel teach [layer] [learner-type]`
- layer: `governance`, `experiential`, or `domain`
- learner-type: `human` or `agent`

## Knowledge Layers

### governance (universal)
Constitutional hierarchy, policy requirements, persona constraints, tetravalent logic.
Triggered: new agent, governance changes, compliance violations suggesting misunderstanding.

### experiential (ecosystem-wide)
PDCA outcomes, 5 Whys findings, reconnaissance discoveries, resolved Contradictory states.
Triggered: PDCA completion, root cause found, reconnaissance finding.

### domain (repo-specific)
- ix: MCP tools, skills, interfaces
- tars: reasoning chains, belief states, self-modification
- ga: music concepts, experimentation, audio safety

## Delivery Modes
- **Human:** Narrative with context, analogies, comprehension questions
- **Agent:** Structured with policy references, belief state tuples, citations

## Two-Stage Verification
1. **Belief state assessment:** Before → After teaching. Target: T with confidence >= 0.7
2. **Behavioral verification:** Does the learner apply the knowledge correctly?
- Max 3 attempts per concept. After 3 failures → escalate to Demerzel.

## Source
`personas/seldon.persona.yaml`, `policies/streeling-policy.yaml`, `logic/knowledge-state.schema.json`
