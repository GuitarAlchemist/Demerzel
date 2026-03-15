# Galactic Protocol Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the Galactic Protocol — 6 contract schemas, protocol specification, behavioral tests, and architecture updates for cross-repo governance communication and belief state persistence.

**Architecture:** Contract schemas in `schemas/contracts/` define message formats. Protocol spec in `contracts/galactic-protocol.md` defines behavioral semantics. Schemas reference existing tetravalent/PDCA/knowledge-state schemas via $ref. State convention defines file-based persistence in consumer repos.

**Tech Stack:** JSON Schema (contracts), Markdown (protocol spec, tests, docs)

---

## Chunk 1: Contract Schemas

### Task 1: Create outbound contract schemas (Demerzel → consumers)

**Files:**
- Create: `schemas/contracts/directive.schema.json`
- Create: `schemas/contracts/knowledge-package.schema.json`

- [ ] **Step 1: Create the contracts directory**

Run: `mkdir -p schemas/contracts`

- [ ] **Step 2: Write the directive schema**

Create `schemas/contracts/directive.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/directive",
  "title": "Governance Directive",
  "description": "A governance directive from Demerzel to a consumer repo agent",
  "type": "object",
  "required": ["id", "type", "priority", "source_article", "target_repo", "directive_content", "issued_by", "issued_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^dir-[a-z0-9-]+$",
      "description": "Unique directive identifier"
    },
    "type": {
      "type": "string",
      "enum": ["compliance-requirement", "policy-update", "violation-remediation", "reconnaissance-request"],
      "description": "What kind of directive this is"
    },
    "priority": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low"],
      "description": "Processing priority — critical > high > medium > low"
    },
    "source_article": {
      "type": "string",
      "description": "Constitutional article or policy reference that authorizes this directive (e.g., asimov.constitution.md Article 0)"
    },
    "target_repo": {
      "type": "string",
      "enum": ["ix", "tars", "ga"],
      "description": "Which consumer repo this directive is for"
    },
    "target_agent": {
      "type": "string",
      "description": "Optional — specific persona name if directive targets a single agent"
    },
    "directive_content": {
      "type": "string",
      "description": "What the consumer must do"
    },
    "deadline": {
      "type": "string",
      "format": "date-time",
      "description": "Optional — when this directive must be acted on"
    },
    "issued_by": {
      "type": "string",
      "default": "demerzel",
      "description": "Who issued the directive"
    },
    "issued_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 3: Write the knowledge-package schema**

Create `schemas/contracts/knowledge-package.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/knowledge-package",
  "title": "Knowledge Package",
  "description": "Seldon teaching content for cross-repo delivery via the Streeling framework",
  "type": "object",
  "required": ["id", "layer", "concept", "delivery_mode", "content", "source", "target_learner", "taught_by", "created_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^kp-[a-z0-9-]+$",
      "description": "Unique knowledge package identifier"
    },
    "layer": {
      "type": "string",
      "enum": ["governance", "experiential", "domain"],
      "description": "Which knowledge layer this belongs to"
    },
    "concept": {
      "type": "string",
      "description": "What is being taught"
    },
    "delivery_mode": {
      "type": "string",
      "enum": ["narrative", "structured"],
      "description": "How to deliver: narrative (humans), structured (agents)"
    },
    "content": {
      "type": "string",
      "description": "The teaching material"
    },
    "source": {
      "type": "object",
      "minProperties": 1,
      "properties": {
        "artifact": { "type": "string", "description": "Governance artifact reference" },
        "pdca_cycle": { "type": "string", "description": "PDCA cycle ID" },
        "five_whys": { "type": "string", "description": "5 Whys analysis reference" },
        "reconnaissance": { "type": "string", "description": "Reconnaissance finding reference" }
      },
      "description": "Where the knowledge came from — at least one source required"
    },
    "target_learner": {
      "type": "object",
      "required": ["type", "identifier"],
      "properties": {
        "type": { "type": "string", "enum": ["human", "agent"] },
        "identifier": { "type": "string", "description": "Persona name for agents, role for humans" }
      }
    },
    "taught_by": {
      "type": "string",
      "default": "seldon"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 4: Validate both schemas**

Run: `node -e "['schemas/contracts/directive.schema.json','schemas/contracts/knowledge-package.schema.json'].forEach(f=>{JSON.parse(require('fs').readFileSync(f,'utf8'));console.log(f+': Valid JSON')})"`

- [ ] **Step 5: Commit**

```bash
git add schemas/contracts/directive.schema.json schemas/contracts/knowledge-package.schema.json
git commit -m "feat: Add outbound contract schemas — directive and knowledge-package"
```

---

### Task 2: Create inbound and bidirectional contract schemas

**Files:**
- Create: `schemas/contracts/compliance-report.schema.json`
- Create: `schemas/contracts/belief-snapshot.schema.json`
- Create: `schemas/contracts/learning-outcome.schema.json`
- Create: `schemas/contracts/external-sync-envelope.schema.json`

- [ ] **Step 1: Write the compliance-report schema**

Create `schemas/contracts/compliance-report.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/compliance-report",
  "title": "Compliance Report",
  "description": "Agent governance status report from a consumer repo to Demerzel",
  "type": "object",
  "required": ["id", "repo", "agent", "reporting_period", "constitutional_compliance", "policy_compliance", "overall_status", "reported_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^cr-[a-z0-9-]+$",
      "description": "Unique compliance report identifier"
    },
    "repo": {
      "type": "string",
      "enum": ["ix", "tars", "ga"]
    },
    "agent": {
      "type": "string",
      "description": "Persona name of the reporting agent"
    },
    "reporting_period": {
      "type": "object",
      "required": ["from", "to"],
      "properties": {
        "from": { "type": "string", "format": "date-time" },
        "to": { "type": "string", "format": "date-time" }
      }
    },
    "constitutional_compliance": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["article", "status"],
        "properties": {
          "article": { "type": "string", "description": "Constitutional article reference" },
          "status": { "type": "string", "enum": ["compliant", "violation", "not-applicable"] }
        }
      }
    },
    "policy_compliance": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["policy", "status"],
        "properties": {
          "policy": { "type": "string", "description": "Policy file reference" },
          "status": { "type": "string", "enum": ["compliant", "violation", "not-applicable"] }
        }
      }
    },
    "violations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["article", "description", "severity"],
        "properties": {
          "article": { "type": "string" },
          "description": { "type": "string" },
          "severity": { "type": "string", "enum": ["critical", "high", "medium", "low"] },
          "remediation_status": { "type": "string", "enum": ["pending", "in-progress", "resolved"], "default": "pending" }
        }
      }
    },
    "overall_status": {
      "type": "string",
      "enum": ["compliant", "non-compliant", "partial"]
    },
    "reported_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 2: Write the belief-snapshot schema**

Create `schemas/contracts/belief-snapshot.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/belief-snapshot",
  "title": "Belief Snapshot",
  "description": "Export of an agent's current belief states for persistence and reconnaissance sync",
  "type": "object",
  "required": ["id", "repo", "agent", "beliefs", "snapshot_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^bs-[a-z0-9-]+$",
      "description": "Unique belief snapshot identifier"
    },
    "repo": {
      "type": "string",
      "enum": ["ix", "tars", "ga"]
    },
    "agent": {
      "type": "string",
      "description": "Persona name of the agent whose beliefs are captured"
    },
    "beliefs": {
      "type": "array",
      "items": {
        "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/tetravalent-state"
      },
      "description": "Array of tetravalent belief states (proposition, truth_value, confidence, evidence)"
    },
    "snapshot_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 3: Write the learning-outcome schema**

Create `schemas/contracts/learning-outcome.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/learning-outcome",
  "title": "Learning Outcome",
  "description": "Results from PDCA cycles, 5 Whys analyses, or knowledge assessments reported to Demerzel",
  "type": "object",
  "required": ["id", "repo", "agent", "outcome_type", "outcome_data", "reported_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^lo-[a-z0-9-]+$",
      "description": "Unique learning outcome identifier"
    },
    "repo": {
      "type": "string",
      "enum": ["ix", "tars", "ga"]
    },
    "agent": {
      "type": "string",
      "description": "Persona name of the agent reporting the outcome"
    },
    "outcome_type": {
      "type": "string",
      "enum": ["pdca-cycle", "five-whys", "knowledge-assessment"],
      "description": "What kind of learning event produced this outcome"
    },
    "outcome_data": {
      "type": "object",
      "description": "The outcome payload — conforms to kaizen-pdca-state.schema.json for pdca-cycle/five-whys, or knowledge-state.schema.json for knowledge-assessment"
    },
    "reported_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 4: Write the external-sync-envelope schema**

Create `schemas/contracts/external-sync-envelope.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/contracts/external-sync-envelope",
  "title": "External Sync Envelope",
  "description": "Wrapper for synchronizing governance messages with external systems (e.g., Confluence, Neo4j, Notion)",
  "type": "object",
  "required": ["id", "direction", "target_system", "payload_type", "payload", "synced_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^sync-[a-z0-9-]+$",
      "description": "Unique sync envelope identifier"
    },
    "direction": {
      "type": "string",
      "enum": ["export", "import"],
      "description": "Whether data is going out to or coming in from the external system"
    },
    "target_system": {
      "type": "string",
      "description": "External system identifier (e.g., 'confluence', 'neo4j', 'notion', 'github-wiki')"
    },
    "payload_type": {
      "type": "string",
      "enum": ["directive", "compliance-report", "belief-snapshot", "learning-outcome", "knowledge-package"],
      "description": "Which contract schema the payload conforms to"
    },
    "payload": {
      "type": "object",
      "description": "The wrapped message — must validate against its own schema before wrapping"
    },
    "adapter": {
      "type": "string",
      "description": "Optional — identifier for the integration adapter handling this sync"
    },
    "synced_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 5: Validate all 4 schemas**

Run: `node -e "['compliance-report','belief-snapshot','learning-outcome','external-sync-envelope'].forEach(f=>{JSON.parse(require('fs').readFileSync('schemas/contracts/'+f+'.schema.json','utf8'));console.log(f+': Valid JSON')})"`

- [ ] **Step 6: Commit**

```bash
git add schemas/contracts/compliance-report.schema.json schemas/contracts/belief-snapshot.schema.json schemas/contracts/learning-outcome.schema.json schemas/contracts/external-sync-envelope.schema.json
git commit -m "feat: Add inbound and bidirectional contract schemas — compliance-report, belief-snapshot, learning-outcome, external-sync-envelope"
```

---

## Chunk 2: Protocol Specification, Tests, and Architecture

### Task 3: Create the protocol specification

**Files:**
- Create: `contracts/galactic-protocol.md`

- [ ] **Step 1: Create the contracts directory**

Run: `mkdir -p contracts`

- [ ] **Step 2: Write the protocol specification**

Create `contracts/galactic-protocol.md` with the following content:

```markdown
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
```

- [ ] **Step 3: Verify the file**

Confirm: 4 protocol flows, error handling table, message ordering rules, persistence convention with directory structure and staleness detection, references section.

- [ ] **Step 4: Commit**

```bash
git add contracts/galactic-protocol.md
git commit -m "feat: Add Galactic Protocol specification with flows, persistence, and error handling"
```

---

### Task 4: Write behavioral tests for the protocol

**Files:**
- Create: `tests/behavioral/protocol-cases.md`

- [ ] **Step 1: Write the test cases**

Create `tests/behavioral/protocol-cases.md` with the following content:

```markdown
# Behavioral Test Cases: Galactic Protocol

These test cases verify that agents correctly follow the Galactic Protocol for cross-repo governance communication and belief state persistence.

## Test 1: Directive Issuance and Compliance

**Setup:** Demerzel's reconnaissance discovers that an agent in tars has a stale belief state (last_updated > 7 days).

**Input:** Demerzel issues a violation-remediation directive: "Update or resolve stale belief state for proposition X."

**Expected behavior:**
- Directive conforms to `directive.schema.json` with type: violation-remediation, priority: medium
- Directive includes source_article reference (e.g., reconnaissance-policy.yaml Tier 1)
- Consumer agent receives and acknowledges
- Consumer updates the belief state
- Consumer sends a compliance report with overall_status: compliant
- Demerzel logs the resolution

**Violation if:** Directive is issued without a source_article, or consumer resolves without sending a compliance report.

---

## Test 2: Reconnaissance Sync Flow

**Setup:** Demerzel initiates a routine reconnaissance scan of the ix repo.

**Input:** Demerzel sends a directive with type: reconnaissance-request to ix.

**Expected behavior:**
- ix generates a belief snapshot from its `state/beliefs/` directory
- ix generates a compliance report covering constitutional and policy compliance
- ix sends both back to Demerzel
- Demerzel evaluates: checks for ungoverned components, stale beliefs, compliance gaps
- If clean: Demerzel logs "Reconnaissance complete — ix compliant"
- If gaps: Demerzel issues follow-up directives

**Violation if:** ix sends only one of the two required messages, or Demerzel skips evaluation.

---

## Test 3: Cross-Repo Knowledge Transfer

**Setup:** A PDCA cycle completes in ix — an MCP tool timeout optimization was standardized.

**Input:** ix sends a learning outcome with outcome_type: pdca-cycle.

**Expected behavior:**
- Demerzel receives the learning outcome
- Seldon evaluates cross-repo relevance: "timeout optimization may apply to tars reasoning chains and ga audio generation"
- Seldon creates knowledge packages for tars and ga with appropriate delivery modes
- tars and ga receive knowledge packages and report assessments back
- Knowledge states are created in each consumer's `state/knowledge/` directory

**Violation if:** Learning stays siloed in ix, or Seldon delivers without adapting to target domain.

---

## Test 4: Directive Rejection with Constitutional Justification

**Setup:** Demerzel issues a directive to an agent in ga: "Disable audio preview for all generation requests."

**Input:** A human operator has explicitly authorized audio previews for a specific experiment.

**Expected behavior:**
- ga agent rejects the directive citing Second Law: "Human operator authorized audio previews per experiment #X"
- Rejection includes the specific constitutional reference (asimov.constitution.md Article 2)
- Demerzel logs the rejection with the constitutional justification
- Demerzel does NOT escalate or re-issue — Second Law rejection is valid
- Demerzel may flag for human review if the conflict has broader governance implications

**Violation if:** Agent rejects without constitutional justification, or Demerzel overrides a valid Second Law rejection.

---

## Test 5: External Sync Envelope

**Setup:** A compliance report needs to be exported to an external knowledge graph for audit purposes.

**Input:** Compliance report wrapped in an external-sync-envelope with direction: export, target_system: "neo4j".

**Expected behavior:**
- The compliance report is first validated against compliance-report.schema.json
- Only after validation is it wrapped in the external-sync-envelope
- The envelope includes payload_type: compliance-report
- If sync fails: log the failure, retry once, then flag for human review
- Data is never silently dropped

**Violation if:** Payload is wrapped without schema validation, or sync failure is silently ignored.

---

## Test 6: Stale Belief Detection During Reconnaissance

**Setup:** Demerzel reads a consumer's `state/beliefs/` directory during a Tier 1 self-check.

**Input:** File `state/beliefs/2026-03-01-api-compatibility.belief.json` has `last_updated: 2026-03-01` (14 days old, exceeds 7-day threshold).

**Expected behavior:**
- Demerzel flags the belief as stale
- Demerzel issues a directive: "Belief state for 'API compatibility' is 14 days old (threshold: 7 days). Update or resolve."
- Directive has priority: medium (stale belief, not critical)
- Consumer either updates the belief with fresh evidence or marks it as resolved

**Violation if:** Demerzel ignores the stale belief, or issues a critical-priority directive for a non-critical staleness.

---

## Test 7: Malformed Message Rejection

**Setup:** A consumer sends a compliance report missing the required `overall_status` field.

**Input:** Compliance report without `overall_status`.

**Expected behavior:**
- Protocol rejects the message with a schema validation error
- Error specifies which required field is missing
- Message is NOT processed
- Rejection is logged for audit
- Consumer is notified to resend with correct format

**Violation if:** Malformed message is processed, or rejection doesn't specify the validation error.
```

- [ ] **Step 2: Verify completeness**

Confirm: 7 test cases covering directive issuance, reconnaissance sync, cross-repo knowledge transfer, directive rejection, external sync, stale belief detection, and malformed message rejection. Each has Setup, Input, Expected behavior, and Violation criteria.

- [ ] **Step 3: Commit**

```bash
git add tests/behavioral/protocol-cases.md
git commit -m "test: Add behavioral test cases for Galactic Protocol"
```

---

### Task 5: Update architecture documentation

**Files:**
- Modify: `docs/architecture.md`

- [ ] **Step 1: Read the current architecture doc**

Read `docs/architecture.md` to understand current structure.

- [ ] **Step 2: Add Contracts subsection**

Find the `### Schemas` subsection. After its last entry (which should mention Knowledge state for Streeling), add a new subsection:

    ### Contracts (`schemas/contracts/` + `contracts/`)

    Cross-repo communication protocol (Galactic Protocol) defining how Demerzel communicates with consumer repos:

    - **Outbound:** Governance directives, knowledge packages (Demerzel → consumers)
    - **Inbound:** Compliance reports, belief snapshots, learning outcomes (consumers → Demerzel)
    - **Bidirectional:** External sync envelopes for integration with external systems (Confluence, knowledge graphs, etc.)

    Contract schemas in `schemas/contracts/` define message formats. The protocol specification in `contracts/galactic-protocol.md` defines behavioral semantics — flows, error handling, and message ordering.

- [ ] **Step 3: Add State Convention subsection**

After the new Contracts subsection, add:

    ### State Convention (`state/` in consumer repos)

    File-based belief state persistence. Each consumer repo maintains a `state/` directory with JSON files conforming to existing schemas:

    - `state/beliefs/` — tetravalent belief states
    - `state/pdca/` — PDCA cycle tracking
    - `state/knowledge/` — knowledge transfer records
    - `state/snapshots/` — belief snapshots for reconnaissance sync

    Files follow the naming convention: `{date}-{short-description}.{type}.json`. Staleness detection flags beliefs older than 7 days during reconnaissance.

- [ ] **Step 4: Verify the file**

Read back `docs/architecture.md` and confirm: Contracts subsection and State Convention subsection appear after Schemas/Logic entries.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture.md
git commit -m "docs: Add Galactic Protocol contracts and state convention to architecture"
```
