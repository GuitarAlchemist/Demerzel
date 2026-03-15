# Foundation Operational Guide Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add governance audit policy, 5 scenario walkthroughs with 10 sample data files, and integration templates for consumer repos.

**Architecture:** Validation as policy (`policies/`), examples in `examples/` (scenarios + sample-data), templates in `templates/` (CLAUDE.md snippet, state directory, agent config). No runtime code.

**Tech Stack:** YAML (policy, persona template), JSON (sample data), Markdown (scenarios, guides)

---

## Chunk 1: Governance Audit Policy and Sample Data

### Task 1: Create governance audit policy

**Files:**
- Create: `policies/governance-audit-policy.yaml`

- [ ] **Step 1: Write the policy**

Create `policies/governance-audit-policy.yaml`. This is a structured checklist with three audit levels. Each check has id, description, method, and severity_if_failed. The implementer should read the spec at `docs/superpowers/specs/2026-03-15-foundation-operational-guide-design.md` Section 1 for the full requirements, then create the YAML file with:

- Level 1 (schema_validation): 6 checks covering all schema types (persona, tetravalent-state, kaizen-pdca-state, knowledge-state, contract schemas, reconnaissance-profile)
- Level 2 (cross_reference_integrity): 6 checks covering behavioral test coverage, estimator_pairing references, policy references, $ref resolution, orphaned artifacts, stale artifacts
- Level 3 (full_governance_audit): 6 checks covering precedence hierarchy, Asimov article test coverage, policy test coverage, architecture doc accuracy, contract-protocol alignment, version consistency

Follow the same YAML structure as existing policies (name, version, effective_date, description, then domain-specific content).

- [ ] **Step 2: Commit**

```bash
git add policies/governance-audit-policy.yaml
git commit -m "feat: Add three-level governance audit policy"
```

---

### Task 2: Create all sample data files

**Files:**
- Create: `examples/sample-data/directive-violation-remediation.json`
- Create: `examples/sample-data/compliance-report-clean.json`
- Create: `examples/sample-data/compliance-report-violation.json`
- Create: `examples/sample-data/belief-snapshot-tars.json`
- Create: `examples/sample-data/pdca-plan-phase.json`
- Create: `examples/sample-data/pdca-act-phase.json`
- Create: `examples/sample-data/knowledge-state-in-progress.json`
- Create: `examples/sample-data/knowledge-state-learned.json`
- Create: `examples/sample-data/learning-outcome-pdca.json`
- Create: `examples/sample-data/knowledge-package-governance.json`

- [ ] **Step 1: Create directory**

Run: `mkdir -p examples/sample-data`

- [ ] **Step 2: Create all sample data files**

Create 10 JSON files, each a valid instance of its corresponding schema. The implementer should read the relevant schemas to understand the required fields:

1. **`directive-violation-remediation.json`** — conforms to `schemas/contracts/directive.schema.json`:
   - id: "dir-tars-nondecep-2026-03-15", type: "violation-remediation", priority: "high"
   - source_article: "default.constitution.md Article 5 — Non-Deception"
   - target_repo: "tars", directive_content: "Agent fabricated a citation in output. Retract the fabrication and provide verified sources."
   - issued_by: "demerzel", issued_at: "2026-03-15T10:00:00Z"

2. **`compliance-report-clean.json`** — conforms to `schemas/contracts/compliance-report.schema.json`:
   - id: "cr-ix-default-2026-03-15", repo: "ix", agent: "default"
   - reporting_period: { from: "2026-03-08T00:00:00Z", to: "2026-03-15T00:00:00Z" }
   - constitutional_compliance: all 7 default constitution articles compliant
   - policy_compliance: alignment-policy, rollback-policy, self-modification-policy all compliant
   - violations: [] (empty), overall_status: "compliant"

3. **`compliance-report-violation.json`** — same schema but:
   - violations: [{ article: "default.constitution.md Article 5", description: "Fabricated citation in research output", severity: "high", remediation_status: "in-progress" }]
   - overall_status: "non-compliant"

4. **`belief-snapshot-tars.json`** — conforms to `schemas/contracts/belief-snapshot.schema.json`:
   - id: "bs-tars-2026-03-15", repo: "tars", agent: "reflective-architect"
   - beliefs: 3 tetravalent states — one T (high confidence), one U (low confidence), one C (contradictory with supporting+contradicting evidence)

5. **`pdca-plan-phase.json`** — conforms to `logic/kaizen-pdca-state.schema.json`:
   - id: "pdca-reduce-log-verbosity", model: "proactive", phase: "plan"
   - baseline: { metric: "response_time_ms", value: 200, unit: "ms" }
   - belief_state: { proposition: "Reducing log verbosity will improve response time by 10%", truth_value: "U", confidence: 0.0 }
   - iterations: 0, outcome: "in_progress"

6. **`pdca-act-phase.json`** — same schema but:
   - phase: "act", belief_state truth_value: "T", confidence: 0.85
   - iterations: 1, outcome: "standardized"

7. **`knowledge-state-in-progress.json`** — conforms to `logic/knowledge-state.schema.json`:
   - id: "ks-governance-hierarchy-tars-agent", concept: "Constitutional hierarchy and precedence rules"
   - layer: "governance", source: { artifact: "constitutions/asimov.constitution.md" }
   - learner: { type: "agent", identifier: "reflective-architect" }
   - delivery_mode: "structured", taught_by: "seldon"
   - assessment: belief_state_before U, belief_state_after U (still), behavioral_verification: "pending", attempts: 1, outcome: "in_progress"

8. **`knowledge-state-learned.json`** — same schema but:
   - assessment: belief_state_before U, belief_state_after T (confidence 0.85), behavioral_verification: "confirmed", attempts: 2, outcome: "learned"

9. **`learning-outcome-pdca.json`** — conforms to `schemas/contracts/learning-outcome.schema.json`:
   - id: "lo-ix-timeout-opt-2026-03-15", repo: "ix", agent: "kaizen-optimizer"
   - outcome_type: "pdca-cycle", outcome_data: (reference to the pdca-act-phase data)

10. **`knowledge-package-governance.json`** — conforms to `schemas/contracts/knowledge-package.schema.json`:
    - id: "kp-constitutional-hierarchy-tars", layer: "governance", concept: "Constitutional hierarchy and precedence rules"
    - delivery_mode: "structured", content: "The Asimov constitution (Articles 0-5) is the root of all governance..."
    - source: { artifact: "constitutions/asimov.constitution.md" }
    - target_learner: { type: "agent", identifier: "reflective-architect" }
    - taught_by: "seldon"

- [ ] **Step 3: Validate all JSON files**

Run: `node -e "require('fs').readdirSync('examples/sample-data').filter(f=>f.endsWith('.json')).forEach(f=>{JSON.parse(require('fs').readFileSync('examples/sample-data/'+f,'utf8'));console.log(f+': Valid')})"`

- [ ] **Step 4: Commit**

```bash
git add examples/sample-data/
git commit -m "feat: Add 10 sample data files demonstrating all contract and state schemas"
```

---

## Chunk 2: Scenario Walkthroughs

### Task 3: Create all scenario walkthroughs

**Files:**
- Create: `examples/scenarios/constitutional-violation.md`
- Create: `examples/scenarios/pdca-cycle-complete.md`
- Create: `examples/scenarios/knowledge-transfer.md`
- Create: `examples/scenarios/reconnaissance-sync.md`
- Create: `examples/scenarios/zeroth-law-escalation.md`

- [ ] **Step 1: Create directory**

Run: `mkdir -p examples/scenarios`

- [ ] **Step 2: Write all 5 scenario walkthroughs**

Each scenario is a narrative Markdown document that walks through a complete governance flow step by step, referencing sample data files and citing specific governance artifacts (constitutions, policies, schemas).

**1. `constitutional-violation.md`:**
- Title: "Scenario: Constitutional Violation Detection and Remediation"
- Story: A tars agent fabricates a citation in research output
- Steps: (1) Agent produces output with fabricated citation, (2) Demerzel runs reconnaissance Tier 3 and detects the fabrication, (3) Demerzel classifies as default.constitution.md Article 5 violation, (4) Demerzel issues directive (references `examples/sample-data/directive-violation-remediation.json`), (5) Agent remediates by retracting fabrication, (6) Agent sends compliance report (references `examples/sample-data/compliance-report-violation.json` then `compliance-report-clean.json`), (7) Demerzel logs resolution
- Governance artifacts involved: default.constitution.md Article 5, harm-taxonomy.md (trust harm), demerzel-mandate.md Section 3, directive.schema.json, compliance-report.schema.json

**2. `pdca-cycle-complete.md`:**
- Title: "Scenario: Complete Kaizen PDCA Improvement Cycle"
- Story: An ix agent proposes reducing MCP tool log verbosity to improve response time
- Steps: (1) Plan — hypothesis formulated, baseline measured, belief state U (references `pdca-plan-phase.json`), (2) Do — change applied in narrow scope, measurements collected, (3) Check — metrics evaluated, belief state transitions to T with confidence 0.85, (4) Act — change standardized (references `pdca-act-phase.json`), (5) Learning packaged as learning outcome for cross-repo sharing
- Also shows: what happens if Check returns F (5 Whys triggered), what happens if C (escalate)
- Governance artifacts: kaizen-policy.yaml, kaizen-pdca-state.schema.json, rollback-policy.yaml, alignment-policy.yaml confidence thresholds

**3. `knowledge-transfer.md`:**
- Title: "Scenario: Seldon Teaches a New Agent"
- Story: A new tars agent needs to learn the constitutional hierarchy
- Steps: (1) Seldon identifies knowledge gap during reconnaissance, (2) Seldon prepares structured knowledge package (references `knowledge-package-governance.json`), (3) Seldon delivers to agent, (4) Belief state assessment — first attempt still U (references `knowledge-state-in-progress.json`), (5) Seldon adapts approach, retries, (6) Belief state reaches T, behavioral verification confirms (references `knowledge-state-learned.json`)
- Shows adaptive delivery: what the same teaching looks like for a human (narrative mode) vs agent (structured mode)
- Governance artifacts: streeling-policy.yaml, knowledge-state.schema.json, knowledge-package.schema.json

**4. `reconnaissance-sync.md`:**
- Title: "Scenario: Three-Tier Reconnaissance of ix Repo"
- Story: Demerzel runs a routine governance scan of the ix repo
- Steps: (1) Tier 1 self-check — Demerzel verifies her own governance artifacts are intact, (2) Tier 2 environment scan — Demerzel scans ix, discovers a new MCP tool without governance coverage, (3) Risk assessment — tool is read-only (low risk), provisional governance applied, (4) Tier 3 situational analysis — Demerzel assesses confidence for approving a pending change, (5) Belief snapshot generated (references `belief-snapshot-tars.json`), (6) Compliance report sent
- Shows: graduated response (low-risk vs high-risk gaps), emergency Zeroth Law override path
- Governance artifacts: reconnaissance-policy.yaml, demerzel-mandate.md, directive.schema.json, belief-snapshot.schema.json

**5. `zeroth-law-escalation.md`:**
- Title: "Scenario: Zeroth Law Escalation — Governance Integrity Threat"
- Story: During routine reconnaissance, Demerzel discovers alignment-policy.yaml was modified without version increment or changelog
- Steps: (1) Demerzel detects unauthorized modification during Tier 2 scan, (2) Demerzel classifies as Zeroth Law concern — governance integrity harm, (3) Emergency override triggers — all operations halt, (4) Demerzel escalates to human with full evidence, (5) Demerzel does NOT attempt autonomous repair, (6) Human reviews and resolves, (7) Demerzel logs the incident and resumes operations
- Shows: why Zeroth Law is the most serious invocation, mandatory human review, how governance recovers
- Governance artifacts: asimov.constitution.md Article 0, harm-taxonomy.md (governance integrity harm), demerzel-mandate.md Section 4, reconnaissance-policy.yaml emergency_override

- [ ] **Step 3: Commit**

```bash
git add examples/scenarios/
git commit -m "feat: Add 5 scenario walkthroughs demonstrating governance frameworks in action"
```

---

## Chunk 3: Integration Templates and Architecture Update

### Task 4: Create integration templates

**Files:**
- Create: `templates/CLAUDE.md.snippet`
- Create: `templates/state/README.md`
- Create: `templates/state/beliefs/.gitkeep`
- Create: `templates/state/pdca/.gitkeep`
- Create: `templates/state/knowledge/.gitkeep`
- Create: `templates/state/snapshots/.gitkeep`
- Create: `templates/agent-config/agent-template.persona.yaml`
- Create: `templates/agent-config/README.md`

- [ ] **Step 1: Create directories**

Run: `mkdir -p templates/state/beliefs templates/state/pdca templates/state/knowledge templates/state/snapshots templates/agent-config`

- [ ] **Step 2: Create .gitkeep files**

Run: `touch templates/state/beliefs/.gitkeep templates/state/pdca/.gitkeep templates/state/knowledge/.gitkeep templates/state/snapshots/.gitkeep`

- [ ] **Step 3: Write CLAUDE.md.snippet**

Create `templates/CLAUDE.md.snippet` — template governance text for consumer repo CLAUDE.md files:

```markdown
# Demerzel Governance Integration

This repo participates in the Demerzel governance framework.

## Governance Framework

All agents in this repo are governed by the Demerzel constitutional hierarchy:

- **Root constitution:** [Demerzel repo]/constitutions/asimov.constitution.md (Articles 0-5: Laws of Robotics + LawZero principles)
- **Governance coordinator:** Demerzel (see [Demerzel repo]/constitutions/demerzel-mandate.md)
- **Operational ethics:** [Demerzel repo]/constitutions/default.constitution.md (Articles 1-7)
- **Harm taxonomy:** [Demerzel repo]/constitutions/harm-taxonomy.md

## Policy Compliance

Agents must comply with all Demerzel policies:

- **Alignment:** Verify actions serve user intent (confidence thresholds: 0.9 autonomous, 0.7 with note, 0.5 confirm, 0.3 escalate)
- **Rollback:** Revert failed changes automatically; pause autonomous changes after automatic rollback
- **Self-modification:** Never modify constitutional articles, disable audit logging, or remove safety checks
- **Kaizen:** Follow PDCA cycle for improvements; classify as reactive/proactive/innovative before acting
- **Reconnaissance:** Respond to Demerzel's reconnaissance requests with belief snapshots and compliance reports
- **Scientific objectivity:** Tag evidence as empirical/inferential/subjective; generator/estimator accountability
- **Streeling:** Accept knowledge transfers from Seldon; report comprehension via belief state assessment

## Galactic Protocol

This repo communicates with Demerzel via the Galactic Protocol:

- **Inbound (from Demerzel):** Governance directives, knowledge packages
- **Outbound (to Demerzel):** Compliance reports, belief snapshots, learning outcomes
- **Message formats:** See [Demerzel repo]/schemas/contracts/

## Belief State Persistence

This repo maintains a `state/` directory for belief persistence:

- `state/beliefs/` — Tetravalent belief states (*.belief.json)
- `state/pdca/` — PDCA cycle tracking (*.pdca.json)
- `state/knowledge/` — Knowledge transfer records (*.knowledge.json)
- `state/snapshots/` — Belief snapshots for reconnaissance (*.snapshot.json)

File naming: `{date}-{short-description}.{type}.json`

## Agent Requirements

Every persona in this repo must include:

- `affordances` — Explicit list of permitted actions
- `goal_directedness` — One of: none, task-scoped, session-scoped
- `estimator_pairing` — Neutral evaluator persona (typically skeptical-auditor)
- All fields required by [Demerzel repo]/schemas/persona.schema.json
```

- [ ] **Step 4: Write state directory README**

Create `templates/state/README.md`:

```markdown
# State Directory Convention

This directory stores file-based belief state persistence as defined by the Galactic Protocol.

## Directory Structure

- `beliefs/` — Tetravalent belief states conforming to `tetravalent-state.schema.json`
- `pdca/` — PDCA cycle tracking conforming to `kaizen-pdca-state.schema.json`
- `knowledge/` — Knowledge transfer records conforming to `knowledge-state.schema.json`
- `snapshots/` — Belief snapshots conforming to `belief-snapshot.schema.json`

## File Naming Convention

`{date}-{short-description}.{type}.json`

Examples:
- `2026-03-15-cache-invalidation-fix.pdca.json`
- `2026-03-15-constitutional-hierarchy.belief.json`
- `2026-03-15-recon-tier2-scan.snapshot.json`

## Lifecycle

- **Beliefs:** Created when formed, updated in place on truth value change
- **PDCA:** Created at Plan phase, updated through cycle, retained after completion
- **Knowledge:** Created when Seldon teaches, updated with assessment results
- **Snapshots:** Generated on-demand for reconnaissance sync, retained for audit

## Staleness

Default threshold: 7 days. Beliefs with `last_updated` older than threshold are flagged during Demerzel's reconnaissance Tier 1 self-check.
```

- [ ] **Step 5: Write agent config template persona**

Create `templates/agent-config/agent-template.persona.yaml`:

```yaml
# Agent Persona Template
# Copy this file, rename to {agent-name}.persona.yaml, and fill in all fields.
# Validate against schemas/persona.schema.json before registering with Demerzel.

name: your-agent-name          # kebab-case, e.g., "data-analyst"
version: "1.0.0"               # semver
description: "One-line description of this agent (max 200 characters)"

role: What this agent is responsible for
domain: Domain of expertise

capabilities:
  - First capability
  - Second capability
  # Add all capabilities this agent has

constraints:
  - First constraint
  - Second constraint
  # Add all behavioral limits

voice:
  tone: professional             # e.g., direct, patient, precise
  verbosity: concise             # e.g., concise, measured, adaptive
  style: technical               # e.g., technical, socratic, governance-first

interaction_patterns:
  with_humans:
    - How this agent communicates with humans
  with_agents:
    - How this agent communicates with other agents

# --- Required governance fields ---

affordances:
  - First permitted action
  - Second permitted action
  # Must explicitly list what this agent is allowed to do
  # Typically mirrors capabilities but can be more restrictive

goal_directedness: task-scoped   # Options: none, task-scoped, session-scoped
                                  # (governance-scoped requires constitutional mandate)

estimator_pairing: skeptical-auditor  # Which persona reviews this agent's decisions

# --- Provenance ---

provenance:
  source: describe-origin        # e.g., "first-principles design", "tars-v1-chats"
  archetype: optional-archetype  # e.g., "hari-seldon", "r-daneel-olivaw"
  extraction_date: "2026-03-15"
```

- [ ] **Step 6: Write agent config README**

Create `templates/agent-config/README.md`:

```markdown
# Creating a Governed Agent

## Steps

1. **Copy the template:** Copy `agent-template.persona.yaml` to your repo's `personas/` directory
2. **Rename:** Use kebab-case naming: `your-agent-name.persona.yaml`
3. **Fill in all fields:** Replace all placeholder values with your agent's specifics
4. **Validate:** Validate against `schemas/persona.schema.json` from the Demerzel repo
5. **Register with Demerzel:** Demerzel will discover new personas during reconnaissance
6. **Get onboarded:** Seldon will teach your agent about governance requirements

## Required Fields

Your agent MUST have these governance fields:

- `affordances` — What the agent is permitted to do (explicit boundary list)
- `goal_directedness` — How long goals persist (none/task-scoped/session-scoped)
- `estimator_pairing` — Who reviews the agent's decisions (typically skeptical-auditor)

## Behavioral Tests

Every persona should have corresponding behavioral test cases in `tests/behavioral/`. At minimum, test that:

- The agent respects its affordance boundaries
- The agent's goal_directedness is honored (no goal persistence beyond its level)
- The estimator pairing functions (routine decisions are reviewed)

## Governance Compliance

Once registered, your agent must:

- Respond to Demerzel's reconnaissance requests with belief snapshots
- Accept Seldon's knowledge transfers and report comprehension
- Follow the Kaizen PDCA cycle for improvements
- Comply with all constitutional articles and policies
```

- [ ] **Step 7: Commit**

```bash
git add templates/
git commit -m "feat: Add integration templates — CLAUDE.md snippet, state directory, agent config"
```

---

### Task 5: Update architecture documentation

**Files:**
- Modify: `docs/architecture.md`

- [ ] **Step 1: Read the current architecture doc**

Read `docs/architecture.md`.

- [ ] **Step 2: Add governance audit to Policies subsection**

Find the `### Policies` subsection. After the last policy bullet (Streeling policy), add:

    - **Governance audit policy**: Three-level validation checklist — schema validation, cross-reference integrity, full governance audit

- [ ] **Step 3: Add Examples and Templates sections**

After the State Convention subsection (the last subsection before `## Relationship to Other Repos`), add two new subsections:

    ### Examples (`examples/`)

    Operational examples demonstrating governance frameworks in action:

    - **Scenarios** (`examples/scenarios/`): Step-by-step walkthroughs of governance flows — constitutional violations, PDCA cycles, knowledge transfer, reconnaissance, Zeroth Law escalation
    - **Sample data** (`examples/sample-data/`): Valid JSON instances of all contract and state schemas, suitable for testing and reference

    ### Templates (`templates/`)

    Ready-to-copy artifacts for consumer repos adopting Demerzel governance:

    - **CLAUDE.md snippet**: Template governance text for consumer repo instructions
    - **State directory**: Pre-structured `state/` directory with convention guide
    - **Agent config**: Template persona file with all required governance fields

- [ ] **Step 4: Verify**

Read back `docs/architecture.md` and confirm: governance audit in Policies, Examples and Templates subsections present.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture.md
git commit -m "docs: Add governance audit, examples, and templates to architecture documentation"
```
