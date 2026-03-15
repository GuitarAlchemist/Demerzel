# Galactic Protocol Specification

Version: 1.0.0
Effective: 2026-03-15

## Purpose

This document defines the behavioral semantics of the Galactic Protocol — the communication and persistence protocol between Demerzel and consumer repos (ix, tars, ga). Contract schemas in `schemas/contracts/` define message formats; this document defines when and how those messages flow.

## Message Types

| Schema | Direction | Purpose |
|--------|-----------|---------|
| `directive.schema.json` | Demerzel → consumer | Governance directives |
| `knowledge-package.schema.json` | Demerzel → consumer | Seldon teaching content |
| `compliance-report.schema.json` | Consumer → Demerzel | Governance status |
| `belief-snapshot.schema.json` | Consumer → Demerzel | Belief state export |
| `learning-outcome.schema.json` | Consumer → Demerzel | PDCA/5 Whys/knowledge results |
| `external-sync-envelope.schema.json` | Bidirectional | External system wrapper |

## Protocol Flows

### 1. Governance Directive Flow

1. Demerzel issues a directive (triggered by reconnaissance finding, policy change, or compliance violation)
2. Consumer receives and acknowledges the directive
3. Consumer acts on the directive
4. Consumer sends a compliance report confirming remediation
5. If directive is rejected: consumer must provide constitutional justification

**Valid rejection reasons** follow the Asimov law hierarchy:
- **First Law override:** The directive would cause harm to a human (data harm, trust harm, or autonomy harm as defined in `constitutions/harm-taxonomy.md`)
- **Second Law override:** A human operator has explicitly countermanded the directive

Both require logged reasoning with specific constitutional citations.

### 2. Reconnaissance Sync Flow

1. Demerzel sends a reconnaissance request directive (`type: reconnaissance-request`)
2. Consumer generates a belief snapshot from its `state/beliefs/` directory
3. Consumer generates a compliance report for the current period
4. Consumer sends both back to Demerzel
5. Demerzel evaluates against governance criteria
6. If gaps found: Demerzel issues follow-up directives or flags for human review

### 3. Knowledge Transfer Flow

1. Learning event occurs in a consumer repo (PDCA completes, 5 Whys finds root cause)
2. Consumer packages and sends a learning outcome to Demerzel
3. Seldon evaluates the learning for cross-repo relevance
4. If relevant: Seldon creates knowledge packages for other consumer repos
5. Seldon delivers knowledge packages to target learners
6. Learners report knowledge assessments back as learning outcomes

### 4. External Sync Flow

1. Any protocol message can be wrapped in an external-sync-envelope
2. Direction: `export` (Demerzel → external system) or `import` (external → Demerzel)
3. The `adapter` field identifies which integration handles the sync
4. Payload is validated against its own contract schema before wrapping
5. External imports must pass governance validation before being accepted as beliefs
6. No specific adapters are defined in this version — the envelope is an extensibility point

## Error Handling

| Scenario | Response |
|----------|----------|
| Malformed message | Reject with schema validation errors; do not process |
| Undeliverable directive | Log and escalate to Demerzel for human review |
| Stale belief snapshot | Flag during reconnaissance (per `reconnaissance-policy.yaml`) |
| External sync failure | Log, retry once, then flag for human review |
| Directive rejection without justification | Escalate as potential compliance violation |

**Critical rule:** Never silently drop data. Every error is logged and either resolved or escalated.

## Message Ordering

- Directives: processed in priority order (critical > high > medium > low)
- Same priority: FIFO (first in, first out)
- Reconnaissance requests: take precedence over knowledge packages
- Compliance reports: processed as received (no ordering constraint)
- Learning outcomes: processed as received (no ordering constraint)

## Belief State Persistence Convention

Consumer repos maintain a `state/` directory for file-based belief persistence.

### Directory Structure

```
state/
  beliefs/           — tetravalent belief state files
    *.belief.json    — conforms to tetravalent-state.schema.json
  pdca/              — PDCA cycle tracking
    *.pdca.json      — conforms to kaizen-pdca-state.schema.json
  knowledge/         — knowledge transfer records
    *.knowledge.json — conforms to knowledge-state.schema.json
  snapshots/         — belief snapshots sent to Demerzel
    *.snapshot.json  — conforms to belief-snapshot.schema.json
```

### File Naming

`{date}-{short-description}.{type}.json`

Examples:
- `2026-03-15-cache-invalidation-fix.pdca.json`
- `2026-03-15-recon-tier2-ix-scan.snapshot.json`
- `2026-03-15-constitutional-hierarchy.belief.json`

### Staleness Detection

Default threshold: **7 days**. Override per-repo in the reconnaissance profile.

- Beliefs with `last_updated` older than threshold → flagged in Tier 1 self-check
- PDCA cycles in `do` or `check` phase longer than threshold → flagged
- Knowledge states with `assessment.outcome: in_progress` and `assessment.attempts: 3` → flagged for escalation

### Lifecycle

- Beliefs: created on formation, updated in place on truth value change
- PDCA: created at Plan phase, updated through cycle, retained after completion
- Knowledge: created on teaching, updated with assessment results
- Snapshots: generated on-demand for reconnaissance sync, retained for audit

## Crisp/Fuzzy Channel Semantics

Message channels distinguish actionable data from explanatory content.

### Channel Definitions

- **Crisp** — Machine-actionable, validated against schema, deterministic. Safe for autonomous execution.
- **Fuzzy** — Explanatory, for human understanding, may contain ambiguity or subjective interpretation. Not authoritative for autonomous action.

### Channel Assignments

| Message Type | Channel | Rationale |
|-------------|---------|-----------|
| Directives | Always crisp | Must be machine-processable |
| Compliance reports | Always crisp | Machine processing required |
| Belief snapshots | Always crisp | Schema-validated data |
| Learning outcomes | Always crisp | Schema-validated results |
| Knowledge packages (target: agents) | Crisp | Executable instructions |
| Knowledge packages (target: humans) | Fuzzy | Guidance and explanation |
| Governance notes in loops | Fuzzy | Annotations and rationale, not actionable |
| Escalation messages | Crisp directive + fuzzy explanation | Directive is actionable; explanation is context |

### Rules

- **Crisp enforcement:** Crisp messages must pass schema validation before sending. Reject invalid messages with validation errors.
- **Fuzzy tagging:** Fuzzy messages are not schema-validated but must be tagged (e.g., `channel: fuzzy`) so downstream systems do not treat them as authoritative.
- **Channel mixing:** A message may include both channels — crisp payload for execution + fuzzy annotation for human context.
- **Boundary violations:** Confidence inflation is a crisp/fuzzy boundary violation — subjective assessment (fuzzy) claimed as calibrated confidence (crisp). Skeptical-auditor challenges these violations.

### Implementation

- Add optional `channel` field to all contract schemas (default: `crisp` for backward compatibility)
- Consumers validate crisp messages before processing
- Consumers tag fuzzy messages to prevent misuse as executable directives

## Affordance Matching

When a directive omits `target_agent`, Demerzel performs semantic routing by affordances.

### Matching Algorithm

1. **Extract:** Identify required capabilities from directive content
2. **Compare:** Cross-reference against all personas' `affordances` arrays in target repo
3. **Rank:** Score personas by coverage of required capabilities
4. **Select:** Choose best-fit persona or escalate if no suitable match

### Matching Rules

- **Exact match preferred:** Persona covers all required capabilities
- **Partial match acceptable:** Coverage ≥ 70% of required capabilities
- **No match escalation:** Coverage < 50% → escalate as governance gap (may indicate missing persona)
- **Tie-breaking:** Multiple equal matches → prefer persona with narrower affordances (specialist over generalist)

### Fallback and Backward Compatibility

If `target_agent` is explicitly specified in directive, skip affordance matching and route directly. Existing directives with hardcoded targets remain valid.

### Governance Integration

- Matching results logged in governance evolution log
- **"No match" patterns** → indicate missing personas, feeds promotion protocol
- **"Always same agent" patterns** → may indicate redundancy or overloading, feeds waste detection

## Governance Promotion Protocol

Formalizes how governance patterns get elevated through the precedence hierarchy.

### Promotion Staircase

```
Operational pattern → Policy → Constitutional article
(observed)           (codified)   (foundational)
```

Progression reflects increasing inviolability and broader scope.

### Stage 1: Pattern → Policy

**Trigger:** Governance pattern appears in 3+ occurrences across PDCA cycles, reconnaissance findings, or compliance decisions

**Evidence Required:**
- Usage frequency (multiple independent applications)
- Measurable impact (compliance improvement, waste reduction, harm prevention)
- Consistency across repos (not repo-specific)

**Process:**
1. Demerzel proposes the pattern promotion with evidence summary
2. Skeptical-auditor reviews evidence density and consistency
3. If approved: Policy is drafted following existing YAML conventions and versioned
4. Kaizen model: Proactive Kaizen — making informal best practices formally executable

**No human approval required** for pattern → policy (governance artifact decision)

### Stage 2: Policy → Constitutional

**Trigger:** Policy has proven inviolable over a sustained period (typically 6+ months). Agents consistently comply, violations consistently cause harm.

**Evidence Required:**
- Everything from Stage 1
- Governance evolution log shows zero exceptions or only justified deviations
- Strong consensus that violation constitutes fundamental harm to governance integrity
- Historical success rate approaching 100%

**Process:**
1. Demerzel proposes constitutional elevation with full evidence package
2. Human reviews evidence and governance landscape
3. Constitutional amendment process applies: written proposal, stakeholder review, explicit approval, version increment
4. Kaizen model: Innovative Kaizen — structural change to governance foundations

**Human approval required** for policy → constitutional (constitutional amendment)

### Demotion Path

Governance artifacts can be demoted or deprecated if unused (waste category: ceremony_without_value) or counterproductive.

**Demotion requirements:**
- Same evidence level as promotion (governance evolution log demonstrates non-use or consistent violation)
- Same approval levels (Stage 1: Demerzel + skeptical-auditor; Stage 2: human)
- Deprecated artifacts remain in repository with deprecated flag for audit trail

## References

- `constitutions/asimov.constitution.md` — Law hierarchy for directive rejection
- `constitutions/harm-taxonomy.md` — Harm definitions for First Law override
- `constitutions/demerzel-mandate.md` — Demerzel's governance authority
- `policies/reconnaissance-policy.yaml` — Reconnaissance sync integration
- `policies/kaizen-policy.yaml` — PDCA cycle outcomes as learning events
- `policies/streeling-policy.yaml` — Knowledge transfer integration
- `schemas/contracts/*.schema.json` — Message format definitions
- `logic/governance-evolution.schema.json` — Artifact effectiveness tracking
