# Governance Meta-Compounding Design

**Date:** 2026-03-15
**Status:** Draft
**Approach:** Level 3 upgrade — five integrated improvements

## Overview

Elevate Demerzel's governance to Level 3 meta-compounding — the framework recursively improves itself. Inspired by the "Compound the Compounding" notebook's promotion staircase, the Semantic Event Routing notebook's bounded fuzziness and confidence protocols, and the Probabilistic Grammars notebook's constrained reasoning.

Five components:
1. **Governance Promotion Protocol** — formalize how patterns become policies become constitutional articles
2. **Confidence Calibration Protocol** — ensure agents' confidence scores are honest and evidence-grounded
3. **Crisp/Fuzzy Channel Separation** — distinguish actionable data from explanatory content in Galactic Protocol
4. **Semantic Routing by Affordances** — match directives to agents by capability, not hardcoded names
5. **Governance Evolution Log** — track artifact effectiveness and drive promotion/demotion decisions

## 1. Governance Promotion Protocol

Formalizes how governance patterns get elevated through the precedence hierarchy.

### Promotion Staircase

```
Operational pattern → Policy → Constitutional article
(observed)           (codified)   (foundational)
```

### Stage 1: Pattern → Policy (evidence-based)

- **Trigger:** A governance pattern appears in 3+ PDCA cycles, reconnaissance findings, or compliance decisions
- **Evidence required:** Usage frequency, measurable impact, consistency across repos
- **Process:** Demerzel proposes the promotion. Skeptical-auditor reviews the evidence. If approved, a new policy is drafted following existing YAML conventions.
- **Kaizen model:** Proactive Kaizen — improving something that works informally by making it formal

### Stage 2: Policy → Constitutional (human judgment)

- **Trigger:** A policy has been in effect for a sustained period and has proven inviolable in practice — agents always comply, violations always cause harm
- **Evidence required:** Everything from Stage 1, plus: no exceptions in the governance evolution log, strong consensus that violation constitutes fundamental harm
- **Process:** Demerzel proposes with full evidence package. Human reviews. Constitutional amendment process applies (written proposal, stakeholder review, explicit approval, version increment).
- **Kaizen model:** Innovative Kaizen — structural change requiring human authorization

### Demotion Path

If a governance artifact proves unused (waste category: ceremony_without_value) or counterproductive, it can be demoted or deprecated. Same evidence requirements, same approval levels.

## 2. Confidence Calibration Protocol

Addresses the "confidence inflation" problem — ensuring agents' confidence scores are honest. Added to scientific objectivity policy.

### Calibration Requirements

Confidence must be grounded in evidence density, not subjective assessment:

- `>= 0.9` — Requires 3+ independent empirical evidence sources
- `>= 0.7` — Requires 2+ evidence sources, at least 1 empirical
- `>= 0.5` — Requires 1+ evidence source of any type
- `< 0.5` — Acceptable with inferential or subjective evidence only, but must be flagged as low-confidence

### Calibration Checks (skeptical-auditor performs)

- Does the evidence density justify the confidence score?
- Are there contradicting sources the agent didn't account for? (would shift to C state)
- Has the agent historically over-estimated confidence? (track calibration accuracy over time)

### Inflation Detection Signals

- Agent claims 0.9 confidence with only 1 evidence source
- Agent's confidence doesn't decrease when contradicting evidence arrives
- Pattern of high-confidence claims that later prove wrong (tracked in governance evolution log)

### Tetravalent Integration

- Confidence calibration applies to all belief states, not just T
- Unknown (U) with high confidence is a red flag — you can't be confident you don't know something
- Contradictory (C) states must have confidence = 0.0 until resolution (you can't be confident about a contradiction)

## 3. Crisp/Fuzzy Channel Separation

Adds channel typing to Galactic Protocol messages.

### Channel Types

- **Crisp** — Machine-actionable, validated against schema, deterministic
- **Fuzzy** — Explanatory, for human understanding, may contain ambiguity

### Channel Assignments

| Message Type | Channel |
|-------------|---------|
| Directives | Always crisp |
| Compliance reports | Always crisp |
| Belief snapshots | Always crisp |
| Learning outcomes | Always crisp |
| Knowledge packages (agents) | Crisp |
| Knowledge packages (humans) | Fuzzy |
| Governance notes in loops | Fuzzy |
| Escalation messages | Crisp directive + fuzzy explanation |

### Rules

- Crisp messages must pass schema validation before sending — reject if invalid
- Fuzzy messages are not schema-validated but must be tagged so downstream systems don't treat them as authoritative
- A message can include both channels: crisp payload for execution + fuzzy annotation for context
- Confidence inflation is a crisp/fuzzy boundary violation — subjective assessment (fuzzy) treated as calibrated confidence (crisp)

### Implementation

Add `channel` as an optional field (default: `crisp`) to all contract schemas. Backward-compatible — messages without explicit channel are treated as crisp.

## 4. Semantic Routing by Affordances

Makes directive targeting adaptive — match tasks to agents by capability instead of hardcoding names.

### Enhancement

`target_agent` in directive schema becomes optional. When omitted, Demerzel performs affordance matching:

1. Extract required capabilities from the directive content
2. Compare against all personas' `affordances` arrays in the target repo
3. Rank personas by match quality (coverage of required capabilities)
4. Select the best-fit persona, or escalate if no persona covers the requirements

### Matching Rules

- Exact match preferred
- Partial match acceptable if coverage > 70% of required capabilities
- No match (< 50% coverage) → escalate to Demerzel for human review, may indicate governance gap
- Multiple equal matches → prefer the persona with narrower affordances (specialist over generalist)

### Fallback

If `target_agent` is explicitly specified, skip affordance matching and route directly. Backward-compatible.

### Governance Integration

- Matching results logged in governance evolution log
- "No match" patterns indicate missing personas — feeds promotion protocol
- "Always same agent" patterns may indicate redundancy — feeds waste detection

## 5. Governance Evolution Log

The meta-compounding engine — tracks governance artifact effectiveness over time.

### Schema: `logic/governance-evolution.schema.json`

**Fields:**
- `id` — unique entry identifier
- `artifact` — governance artifact file path
- `artifact_type` — `constitution`, `policy`, `persona`, `schema`, `contract`
- `metrics`:
  - `citation_count` — times cited in governance decisions, directives, conflict resolutions
  - `violation_count` — times agents violated this artifact
  - `compliance_rate` — violations / total assessments
  - `last_cited` — timestamp of most recent citation
  - `last_violated` — timestamp of most recent violation
  - `promotion_candidate` — boolean, flagged if usage exceeds promotion threshold
  - `deprecation_candidate` — boolean, flagged if unused for extended period
- `events` — array of governance events:
  - `type` — `cited`, `violated`, `amended`, `promoted`, `demoted`, `created`
  - `context` — what happened
  - `timestamp`
- `assessment`:
  - `effectiveness` — tetravalent belief state (T/F/U/C)
  - `recommendation` — `maintain`, `promote`, `demote`, `deprecate`, `investigate`

### Integration Points

- **Governance audit Level 3** → reads evolution log to assess artifact effectiveness
- **Kaizen waste detection** → unused artifacts flagged as ceremony_without_value or stale_artifacts
- **Promotion protocol** → evolution log provides evidence for promotion/demotion decisions
- **Confidence calibration** → tracks historical calibration accuracy per agent
- **Streeling** → evolution insights become experiential knowledge for Seldon

### Population

Populated by governance activities — each directive citation, compliance report, conflict resolution. Institutional memory of governance effectiveness.

## 6. Behavioral Tests

Key scenarios for `tests/behavioral/meta-compounding-cases.md`:

1. **Promotion: pattern → policy** — Governance pattern appears in 4 PDCA cycles. Demerzel proposes promotion. Skeptical-auditor reviews evidence and approves.
2. **Promotion: policy → constitutional (requires human)** — Policy inviolable for 6 months. Demerzel proposes constitutional elevation with evidence. Human must approve.
3. **Demotion: unused policy deprecated** — Evolution log shows policy uncited for 90 days. Flagged as deprecation candidate.
4. **Confidence inflation detected** — Agent claims 0.92 confidence with 1 evidence source. Skeptical-auditor challenges.
5. **Crisp/fuzzy boundary violation** — Fuzzy annotation treated as actionable data. Protocol rejects.
6. **Affordance matching routes to best-fit agent** — Directive omits target_agent. Demerzel matches capabilities to affordances.
7. **Affordance matching finds no match** — No persona covers requirements. Escalated as governance gap.
8. **Evolution log drives Kaizen** — Constitutional article never cited. Flagged as potential waste. Investigation required before deprecation.

## 7. File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `logic/governance-evolution.schema.json` | Schema for tracking governance artifact effectiveness |
| `tests/behavioral/meta-compounding-cases.md` | Behavioral tests for all 5 meta-compounding improvements |

### Modified Files

| File | Change |
|------|--------|
| `policies/scientific-objectivity-policy.yaml` | Add confidence calibration section |
| `schemas/contracts/directive.schema.json` | Make `target_agent` optional, add `channel` field |
| `schemas/contracts/compliance-report.schema.json` | Add `channel` field |
| `schemas/contracts/belief-snapshot.schema.json` | Add `channel` field |
| `schemas/contracts/learning-outcome.schema.json` | Add `channel` field |
| `schemas/contracts/knowledge-package.schema.json` | Add `channel` field |
| `schemas/contracts/external-sync-envelope.schema.json` | Add `channel` field |
| `contracts/galactic-protocol.md` | Add promotion protocol section, crisp/fuzzy channel semantics, affordance matching semantics |
| `docs/architecture.md` | Add governance evolution to Logic, update Protocol spec description |

### Unchanged

- Constitutions (evolution log tracks them, doesn't modify them)
- Personas (affordance matching reads them, doesn't modify them)
- Existing policies other than scientific-objectivity
