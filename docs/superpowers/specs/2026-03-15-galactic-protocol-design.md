# Galactic Protocol — Cross-Repo Contracts and Belief State Persistence Design

**Date:** 2026-03-15
**Status:** Draft
**Approach:** Protocol Specification (Approach 2)

## Overview

Define the communication and persistence protocol between Demerzel and her consumer repos (ix, tars, ga). Named "Galactic Protocol" in the Foundation naming tradition. Includes contract schemas for all message types, a protocol specification for behavioral semantics, and a file-based belief state persistence convention.

Scope: contracts + persistence (the protocol). Consumer repo integration (wiring) is a separate sub-project.

## 1. Contract Schemas

Directory: `schemas/contracts/`

Six message type schemas covering bidirectional governance communication and external system integration.

### Outbound (Demerzel → consumers)

**`directive.schema.json`** — Governance directive
- `id`, `type` (compliance-requirement, policy-update, violation-remediation, reconnaissance-request), `priority` (critical/high/medium/low), `source_article` (constitutional/policy reference), `target_repo` (ix/tars/ga), `target_agent` (optional persona name), `directive_content` (what to do), `deadline` (optional), `issued_by` (demerzel), `issued_at`

**`knowledge-package.schema.json`** — Seldon teaching content for cross-repo delivery
- `id`, `layer` (governance/experiential/domain), `concept`, `delivery_mode` (narrative/structured), `content` (the teaching material), `source` (artifact/pdca/5whys/reconnaissance reference), `target_learner` (type + identifier), `taught_by` (seldon), `created_at`

### Inbound (consumers → Demerzel)

**`compliance-report.schema.json`** — Agent governance status
- `id`, `repo` (ix/tars/ga), `agent` (persona name), `reporting_period`, `constitutional_compliance` (array of article statuses), `policy_compliance` (array of policy statuses), `violations` (array, each with article/description/severity/remediation_status), `overall_status` (compliant/non-compliant/partial), `reported_at`

**`belief-snapshot.schema.json`** — Current belief state export
- `id`, `repo`, `agent`, `beliefs` (array of tetravalent state tuples — reuses existing schema via $ref), `snapshot_at`
- This is what gets persisted to `state/` directories as JSON files

**`learning-outcome.schema.json`** — PDCA/5 Whys/knowledge results
- `id`, `repo`, `agent`, `outcome_type` (pdca-cycle/five-whys/knowledge-assessment), `outcome_data` (reuses PDCA state schema or knowledge state schema via $ref), `reported_at`

### Bidirectional

**`external-sync-envelope.schema.json`** — Wrapper for external system integration
- `id`, `direction` (export/import), `target_system` (free string — e.g., "confluence", "neo4j", "notion"), `payload_type` (directive/compliance-report/belief-snapshot/learning-outcome/knowledge-package), `payload` (the wrapped message), `adapter` (optional adapter identifier), `synced_at`
- This is the extensibility point — the envelope wraps any other message type for external delivery/ingestion

## 2. Protocol Specification

File: `contracts/galactic-protocol.md`

Markdown document defining behavioral semantics — when messages are sent, how they flow, error handling, and ordering.

### Protocol Flows

**1. Governance Directive Flow:**
- Demerzel issues a directive (triggered by reconnaissance finding, policy change, or compliance violation)
- Consumer receives and acknowledges
- Consumer acts on the directive
- Consumer sends a compliance report confirming remediation
- If directive is rejected: consumer must provide constitutional justification (Second Law — human authority override is the only valid reason)

**2. Reconnaissance Sync Flow:**
- Demerzel sends a reconnaissance request to a consumer repo
- Consumer generates a belief snapshot + compliance report
- Consumer sends both back to Demerzel
- Demerzel evaluates against governance criteria
- If gaps found: Demerzel issues directives or flags for human review

**3. Knowledge Transfer Flow:**
- Learning event occurs in a consumer repo (PDCA completes, 5 Whys finds root cause)
- Consumer sends a learning outcome to Demerzel
- Seldon packages it as cross-repo knowledge
- Seldon sends knowledge packages to relevant consumers
- Consumers report knowledge assessments back

**4. External Sync Flow:**
- Any message can be wrapped in an external-sync-envelope
- Direction: export (Demerzel → external system) or import (external → Demerzel)
- The adapter field identifies which integration handles the sync
- Payload is validated against its own schema before wrapping
- External imports must pass governance validation before being accepted as beliefs

### Error Handling

- Malformed messages: reject with schema validation errors, do not process
- Undeliverable directives: log and escalate to Demerzel for human review
- Stale belief snapshots: flag during reconnaissance (per existing policy)
- External sync failures: log, retry once, then flag for human review. Never silently drop data.

### Message Ordering

- Directives are processed in priority order (critical > high > medium > low)
- Within same priority, FIFO
- Reconnaissance requests take precedence over knowledge packages
- Compliance reports are processed as received (no ordering constraint)

## 3. Belief State Persistence Convention

Each consumer repo maintains a `state/` directory with JSON files conforming to existing schemas. Demerzel reads these during reconnaissance.

### Directory Structure (in each consumer repo)

```
state/
  beliefs/          — tetravalent belief state files
    *.belief.json   — each conforms to tetravalent-state.schema.json
  pdca/             — active and completed PDCA cycles
    *.pdca.json     — each conforms to kaizen-pdca-state.schema.json
  knowledge/        — knowledge transfer records
    *.knowledge.json — each conforms to knowledge-state.schema.json
  snapshots/        — belief snapshots sent to Demerzel
    *.snapshot.json  — each conforms to belief-snapshot.schema.json
```

### File Naming Convention

`{date}-{short-description}.{type}.json`
Example: `2026-03-15-cache-invalidation-fix.pdca.json`

### Lifecycle Rules

- Beliefs are created when an agent forms a new belief state (per tetravalent logic)
- Beliefs are updated in place when truth values change (transitions logged via `last_updated`)
- PDCA files are created at Plan phase, updated through the cycle, and retained after completion for experiential knowledge
- Knowledge files are created when Seldon teaches, updated with assessment results
- Snapshots are generated on-demand during reconnaissance sync and retained for audit trail

### Staleness Detection

- Beliefs with `last_updated` older than a configurable threshold are flagged during reconnaissance Tier 1
- PDCA cycles in `do` or `check` phase for longer than the threshold are flagged
- Knowledge states with `outcome: in_progress` and `attempts: 3` that haven't been escalated are flagged

### Future Extension: Demerzel's Own State

If Demerzel later needs governance-level belief persistence, she creates her own `state/` directory within the Demerzel repo. The protocol supports this without changes — same schemas, same conventions.

## 4. File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `schemas/contracts/directive.schema.json` | Governance directive message format |
| `schemas/contracts/knowledge-package.schema.json` | Cross-repo teaching content format |
| `schemas/contracts/compliance-report.schema.json` | Agent governance status report format |
| `schemas/contracts/belief-snapshot.schema.json` | Belief state export format |
| `schemas/contracts/learning-outcome.schema.json` | PDCA/5 Whys/knowledge results format |
| `schemas/contracts/external-sync-envelope.schema.json` | Wrapper for external system integration |
| `contracts/galactic-protocol.md` | Protocol specification — flows, semantics, error handling |
| `tests/behavioral/protocol-cases.md` | Behavioral tests for protocol compliance |

### Modified Files

| File | Change |
|------|--------|
| `docs/architecture.md` | Add contracts section, state convention, external sync extensibility |

### Unchanged

- Existing schemas (tetravalent-state, PDCA state, knowledge state) — contracts reference them via $ref
- Existing policies — protocol operates alongside them
- Personas — protocol defines communication format, not who communicates

### Integration Points

- **Reconnaissance → Protocol:** Tier 2 environment scan uses belief snapshots and compliance reports
- **Kaizen → Protocol:** PDCA outcomes flow as learning outcomes
- **Streeling → Protocol:** Knowledge packages carry Seldon's teaching content
- **Demerzel mandate → Protocol:** Directives carry Demerzel's governance authority
