# Foundation Operational Guide Design

**Date:** 2026-03-15
**Status:** Draft
**Approach:** Split by purpose — validation as policy, examples in examples/, templates in templates/

## Overview

Complete the Demerzel governance framework with three operational components: a governance audit policy for automated validation, scenario walkthroughs with sample data showing each framework in action, and integration templates for consumer repos to adopt governance.

## 1. Governance Audit Policy

File: `policies/governance-audit-policy.yaml`

Structured checklist formalizing Tier 1 reconnaissance for the Demerzel repo itself. Three audit levels.

### Level 1 — Schema Validation

- All personas conform to `persona.schema.json`
- All belief states conform to `tetravalent-state.schema.json`
- All PDCA states conform to `kaizen-pdca-state.schema.json`
- All knowledge states conform to `knowledge-state.schema.json`
- All contract schemas are valid JSON Schema

### Level 2 — Cross-Reference Integrity

- Every persona has a corresponding behavioral test in `tests/behavioral/`
- All `estimator_pairing` values reference existing personas
- All policy `references` point to existing constitutions/policies
- All contract schema `$ref` values resolve to existing schemas
- No orphaned artifacts (files not referenced by any other artifact)
- No stale artifacts (personas for removed agents, policies for deprecated features)

### Level 3 — Full Governance Audit

- Precedence hierarchy is consistent (Asimov > mandate + default > policies > personas)
- Every Asimov article has at least one behavioral test
- Every policy has at least one behavioral test
- Architecture doc artifact listings match actual files on disk
- Contract schemas cover all protocol flows defined in `galactic-protocol.md`
- Versioning is consistent (all artifacts have valid semver, constitutions have version headers)

Each check has: `id`, `description`, `method` (how to verify), `severity_if_failed`.

## 2. Operational Examples

### Scenario Walkthroughs (`examples/scenarios/`)

1. **`constitutional-violation.md`** — Agent fabricates citation → Demerzel detects → issues directive → agent remediates → compliance report. References sample directive and compliance report.
2. **`pdca-cycle-complete.md`** — Full Kaizen cycle Plan → Do → Check → Act. Shows belief state U → T. Includes 5 Whys when first attempt returns F. References sample PDCA states.
3. **`knowledge-transfer.md`** — Seldon teaches new tars agent constitutional hierarchy. Adaptive delivery, belief state assessment, behavioral verification. References sample knowledge state and package.
4. **`reconnaissance-sync.md`** — Three-tier reconnaissance on ix. Tier 1 passes, Tier 2 discovers ungoverned tool, Tier 3 assesses risk. References sample belief snapshot and directive.
5. **`zeroth-law-escalation.md`** — Unauthorized governance modification discovered. Zeroth Law triggers, operations halt, human review. References sample critical directive.

### Sample Data (`examples/sample-data/`)

1. `directive-violation-remediation.json` — Conforms to `directive.schema.json`
2. `compliance-report-clean.json` — Compliant status
3. `compliance-report-violation.json` — Report with violation
4. `belief-snapshot-tars.json` — 3 beliefs (T, U, C states)
5. `pdca-plan-phase.json` — PDCA at Plan (belief: U)
6. `pdca-act-phase.json` — PDCA at Act (belief: T, outcome: standardized)
7. `knowledge-state-in-progress.json` — Attempt 1, belief still U
8. `knowledge-state-learned.json` — Complete, belief T, behavioral verification confirmed

## 3. Integration Templates

### CLAUDE.md Snippet (`templates/CLAUDE.md.snippet`)

Template text for consumer repo CLAUDE.md files covering: governance framework reference, constitutional compliance requirements, policy compliance, reconnaissance protocol instructions, Galactic Protocol participation, persona requirements.

### State Directory Template (`templates/state/`)

- `README.md` — Convention guide (directory structure, file naming, lifecycle, staleness)
- `beliefs/.gitkeep`, `pdca/.gitkeep`, `knowledge/.gitkeep`, `snapshots/.gitkeep` — Directory placeholders

### Agent Config Template (`templates/agent-config/`)

- `agent-template.persona.yaml` — Template persona with all required fields, placeholder values, and explanatory comments
- `README.md` — How to create a governed agent: fill template, validate, register, get Seldon onboarding

## 4. File Changes Summary

### New Files (22)

| File | Purpose |
|------|---------|
| `policies/governance-audit-policy.yaml` | Three-level governance validation checklist |
| `examples/scenarios/constitutional-violation.md` | Walkthrough: violation detection and remediation |
| `examples/scenarios/pdca-cycle-complete.md` | Walkthrough: full Kaizen improvement cycle |
| `examples/scenarios/knowledge-transfer.md` | Walkthrough: Seldon teaches a new agent |
| `examples/scenarios/reconnaissance-sync.md` | Walkthrough: three-tier reconnaissance on ix |
| `examples/scenarios/zeroth-law-escalation.md` | Walkthrough: Zeroth Law trigger and escalation |
| `examples/sample-data/directive-violation-remediation.json` | Sample directive |
| `examples/sample-data/compliance-report-clean.json` | Sample compliant report |
| `examples/sample-data/compliance-report-violation.json` | Sample report with violation |
| `examples/sample-data/belief-snapshot-tars.json` | Sample belief snapshot |
| `examples/sample-data/pdca-plan-phase.json` | Sample PDCA at Plan |
| `examples/sample-data/pdca-act-phase.json` | Sample PDCA at Act |
| `examples/sample-data/knowledge-state-in-progress.json` | Sample in-progress knowledge transfer |
| `examples/sample-data/knowledge-state-learned.json` | Sample completed knowledge transfer |
| `templates/CLAUDE.md.snippet` | Template governance text for consumer repos |
| `templates/state/README.md` | State directory convention guide |
| `templates/state/beliefs/.gitkeep` | Directory placeholder |
| `templates/state/pdca/.gitkeep` | Directory placeholder |
| `templates/state/knowledge/.gitkeep` | Directory placeholder |
| `templates/state/snapshots/.gitkeep` | Directory placeholder |
| `templates/agent-config/agent-template.persona.yaml` | Template governed persona |
| `templates/agent-config/README.md` | Agent creation guide |

### Modified Files

| File | Change |
|------|--------|
| `docs/architecture.md` | Add Governance Audit to Policies, add Examples and Templates sections |
