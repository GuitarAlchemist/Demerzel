---
name: demerzel-patterns
description: Consult the agentic patterns catalog — governance rules for Reflection, Tool Use, ReAct, Planning, Multi-Agent, HITL, and Ralph Loops
---

# Demerzel Agentic Patterns Catalog

Governance reference mapping 7 agentic AI patterns to Demerzel's constitutional framework.

## Usage
`/demerzel patterns [pattern]` — pattern name or number (1-7)

## Patterns

### 1. Reflection (Self-Correction)
- **Governance:** Skeptical-auditor as estimator, scientific objectivity policy
- **Rules:** Self-reflection always permitted. Must not rationalize (Consequence Invariance). Contradictory quality → escalate.

### 2. Tool Use
- **Governance:** Affordances list defines permitted tools, Asimov Article 4
- **Rules:** Only within affordances. New tool acquisition requires authorization. Tag results with evidence type.

### 3. ReAct (Reason + Act)
- **Governance:** Tetravalent logic (Thought→Action→Observation), alignment policy
- **Rules:** Update belief states at each Observation. Max 5 cycles without resolution → escalate. Contradictions must be surfaced.

### 4. Planning
- **Governance:** Kaizen PDCA Plan phase, reconnaissance Tier 3
- **Rules:** Define success criteria and rollback paths. Multi-repo plans require Demerzel coordination. Plan drift must be logged.

### 5. Multi-Agent Collaboration
- **Governance:** Personas with affordances, Galactic Protocol, Demerzel mandate
- **Rules:** Each agent within affordances only. Conflicts escalate to Demerzel then human. No persona overrides.

### 6. Human-in-the-Loop (HITL)
- **Governance:** Alignment policy confidence thresholds, Asimov Article 2
- **Rules:** <0.5 → confirm, <0.3 → escalate. Irreversible → human confirm. Zeroth Law → always human review.

### 7. Autonomous Loops (Ralph)
- **Governance:** See `/demerzel loop`
- **Rules:** Risk classification → governance mode. Convergence/regression/drift checks. Max 25 iterations.

## Source
`policies/autonomous-loop-policy.yaml` (agentic_patterns section)
