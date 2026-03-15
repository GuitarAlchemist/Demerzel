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

## References

- `constitutions/asimov.constitution.md` — Law hierarchy for directive rejection
- `constitutions/harm-taxonomy.md` — Harm definitions for First Law override
- `constitutions/demerzel-mandate.md` — Demerzel's governance authority
- `policies/reconnaissance-policy.yaml` — Reconnaissance sync integration
- `policies/kaizen-policy.yaml` — PDCA cycle outcomes as learning events
- `policies/streeling-policy.yaml` — Knowledge transfer integration
- `schemas/contracts/*.schema.json` — Message format definitions
