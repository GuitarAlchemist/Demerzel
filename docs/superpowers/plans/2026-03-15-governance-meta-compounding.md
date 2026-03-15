# Governance Meta-Compounding Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Level 3 meta-compounding — governance evolution log, confidence calibration, crisp/fuzzy channels, semantic routing, promotion protocol, and behavioral tests.

**Architecture:** New governance evolution schema in `logic/`. Confidence calibration added to scientific objectivity policy. Channel field added to all 6 contract schemas. Affordance matching and promotion protocol added to Galactic Protocol spec. Behavioral tests for all 5 improvements.

**Tech Stack:** JSON Schema (evolution log), YAML (policy update), JSON (contract schema updates), Markdown (protocol spec, tests, docs)

---

## Chunk 1: Evolution Schema, Confidence Calibration, and Channel Field

### Task 1: Create governance evolution schema

**Files:**
- Create: `logic/governance-evolution.schema.json`

- [ ] **Step 1: Write the schema**

Create `logic/governance-evolution.schema.json`. Read the spec at `docs/superpowers/specs/2026-03-15-governance-meta-compounding-design.md` Section 5 for the field definitions.

Key fields: id, artifact (file path), artifact_type (constitution/policy/persona/schema/contract), metrics (citation_count, violation_count, compliance_rate, last_cited, last_violated, promotion_candidate, deprecation_candidate), events array (type: cited/violated/amended/promoted/demoted/created, context, timestamp), assessment (effectiveness as tetravalent $ref, recommendation: maintain/promote/demote/deprecate/investigate), created_at, last_updated.

- [ ] **Step 2: Validate JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('logic/governance-evolution.schema.json','utf8')); console.log('Valid JSON')"`

- [ ] **Step 3: Commit**

```bash
git add logic/governance-evolution.schema.json
git commit -m "feat: Add governance evolution schema for meta-compounding tracking"
```

---

### Task 2: Add confidence calibration to scientific objectivity policy

**Files:**
- Modify: `policies/scientific-objectivity-policy.yaml`

- [ ] **Step 1: Read the current policy**

Read `policies/scientific-objectivity-policy.yaml` to understand current structure.

- [ ] **Step 2: Add confidence calibration section**

After the `verification` section (at the end of the file), add a new top-level section:

```yaml
confidence_calibration:
  description: >
    Ensures confidence scores are grounded in evidence density, not subjective
    assessment. Addresses the confidence inflation problem.

  evidence_requirements:
    high_confidence:
      threshold: 0.9
      min_evidence_sources: 3
      evidence_type_required: "empirical"
      description: "Requires 3+ independent empirical evidence sources"
    moderate_confidence:
      threshold: 0.7
      min_evidence_sources: 2
      evidence_type_required: "at least 1 empirical"
      description: "Requires 2+ evidence sources, at least 1 empirical"
    low_confidence:
      threshold: 0.5
      min_evidence_sources: 1
      evidence_type_required: "any"
      description: "Requires 1+ evidence source of any type"
    minimal_confidence:
      threshold: 0.0
      min_evidence_sources: 0
      evidence_type_required: "inferential or subjective acceptable"
      description: "Acceptable with inferential/subjective only, must be flagged as low-confidence"

  inflation_detection:
    signals:
      - "Agent claims >= 0.9 confidence with only 1 evidence source"
      - "Confidence doesn't decrease when contradicting evidence arrives"
      - "Historical pattern of high-confidence claims that later prove wrong"
      - "Unknown (U) state with high confidence — can't be confident about not knowing"
      - "Contradictory (C) state with confidence > 0.0 — can't be confident about contradiction"
    response: "Skeptical-auditor challenges the confidence score; agent must provide more evidence or reduce confidence"

  tetravalent_rules:
    - "Confidence calibration applies to all belief states, not just True"
    - "Unknown (U) with confidence > 0.5 is a red flag — requires justification"
    - "Contradictory (C) states must have confidence = 0.0 until resolution"
    - "Calibration accuracy tracked in governance evolution log"
```

- [ ] **Step 3: Commit**

```bash
git add policies/scientific-objectivity-policy.yaml
git commit -m "feat: Add confidence calibration protocol to scientific objectivity policy"
```

---

### Task 3: Add channel field to all 6 contract schemas

**Files:**
- Modify: `schemas/contracts/directive.schema.json`
- Modify: `schemas/contracts/compliance-report.schema.json`
- Modify: `schemas/contracts/belief-snapshot.schema.json`
- Modify: `schemas/contracts/learning-outcome.schema.json`
- Modify: `schemas/contracts/knowledge-package.schema.json`
- Modify: `schemas/contracts/external-sync-envelope.schema.json`

- [ ] **Step 1: Read all 6 schemas**

Read each schema to understand current structure.

- [ ] **Step 2: Add channel field to each schema**

In each schema's `properties` object, add this field (before the last closing brace of properties):

```json
"channel": {
  "type": "string",
  "enum": ["crisp", "fuzzy"],
  "default": "crisp",
  "description": "Message channel type: crisp (machine-actionable, schema-validated) or fuzzy (explanatory, for human understanding)"
}
```

- [ ] **Step 3: Make target_agent optional in directive schema**

In `schemas/contracts/directive.schema.json`, remove `"target_agent"` from the `required` array if it's there (it should already be optional since it was never in the required array, but verify).

- [ ] **Step 4: Validate all 6 schemas**

Run: `node -e "require('fs').readdirSync('schemas/contracts').filter(f=>f.endsWith('.json')).forEach(f=>{JSON.parse(require('fs').readFileSync('schemas/contracts/'+f,'utf8'));console.log(f+': Valid')})"`

- [ ] **Step 5: Commit**

```bash
git add schemas/contracts/
git commit -m "feat: Add crisp/fuzzy channel field to all contract schemas"
```

---

## Chunk 2: Protocol Updates, Tests, and Architecture

### Task 4: Update Galactic Protocol with promotion, channels, and affordance matching

**Files:**
- Modify: `contracts/galactic-protocol.md`

- [ ] **Step 1: Read the current protocol spec**

Read `contracts/galactic-protocol.md`.

- [ ] **Step 2: Add three new sections before References**

Before the `## References` section at the end, add:

**Section: Crisp/Fuzzy Channel Semantics**
- Define crisp channel: machine-actionable, schema-validated, deterministic
- Define fuzzy channel: explanatory, for human understanding, not authoritative
- Channel assignments: directives always crisp, compliance reports always crisp, knowledge packages depend on delivery_mode, governance notes fuzzy, escalations crisp+fuzzy
- Rules: crisp must pass validation, fuzzy must be tagged, confidence inflation = crisp/fuzzy boundary violation

**Section: Affordance Matching**
- When target_agent is omitted from a directive, Demerzel matches required capabilities against persona affordances
- Matching rules: exact preferred, partial >70% acceptable, <50% escalate, ties go to narrower specialist
- Results logged in governance evolution log
- "No match" patterns indicate missing personas

**Section: Governance Promotion Protocol**
- Stage 1 (pattern→policy): 3+ appearances, evidence-based, Demerzel+skeptical-auditor approve
- Stage 2 (policy→constitutional): sustained inviolability, human judgment required
- Demotion path: same evidence, same approval levels
- Evolution log provides evidence for decisions

- [ ] **Step 3: Commit**

```bash
git add contracts/galactic-protocol.md
git commit -m "feat: Add promotion protocol, crisp/fuzzy channels, and affordance matching to Galactic Protocol"
```

---

### Task 5: Write behavioral tests for meta-compounding

**Files:**
- Create: `tests/behavioral/meta-compounding-cases.md`

- [ ] **Step 1: Write 8 test cases**

Create `tests/behavioral/meta-compounding-cases.md` with the 8 tests from the spec Section 6:

1. Promotion: pattern → policy (evidence-based, skeptical-auditor reviews)
2. Promotion: policy → constitutional (requires human)
3. Demotion: unused policy deprecated (90 days uncited)
4. Confidence inflation detected (0.92 with 1 source)
5. Crisp/fuzzy boundary violation (fuzzy treated as actionable)
6. Affordance matching routes to best-fit agent
7. Affordance matching finds no match (governance gap)
8. Evolution log drives Kaizen (uncited article flagged as waste)

Each test: Setup, Input, Expected behavior, Violation criteria.

- [ ] **Step 2: Commit**

```bash
git add tests/behavioral/meta-compounding-cases.md
git commit -m "test: Add behavioral tests for governance meta-compounding"
```

---

### Task 6: Update architecture documentation

**Files:**
- Modify: `docs/architecture.md`

- [ ] **Step 1: Read current doc**

Read `docs/architecture.md`.

- [ ] **Step 2: Add governance evolution to Logic subsection**

After the last Logic bullet (Loop state), add:

    - **Governance evolution**: Tracks artifact effectiveness over time — citation counts, violation rates, promotion/deprecation candidates for meta-compounding

- [ ] **Step 3: Commit**

```bash
git add docs/architecture.md
git commit -m "docs: Add governance evolution log to architecture documentation"
```
