---
name: demerzel-audit
description: Run Demerzel governance audit — three levels of validation from schema checks to full governance integrity assessment
---

# Demerzel Governance Audit

Run a governance audit at one of three levels. Each level includes all checks from lower levels.

## Usage
`/demerzel audit [level]` — level is 1, 2, or 3 (default: 1)

## Level 1 — Schema Validation
Verify all governance artifacts conform to their schemas.

- [ ] All personas conform to `schemas/persona.schema.json`
- [ ] All contract schemas are valid JSON Schema
- [ ] Reconnaissance profiles conform to `schemas/reconnaissance-profile.schema.json`
- [ ] PDCA states conform to `logic/kaizen-pdca-state.schema.json`
- [ ] Knowledge states conform to `logic/knowledge-state.schema.json`
- [ ] Loop states conform to `logic/loop-state.schema.json`

## Level 2 — Cross-Reference Integrity
Verify artifacts reference each other correctly.

- [ ] Every persona has a behavioral test in `tests/behavioral/`
- [ ] All `estimator_pairing` values reference existing personas
- [ ] All policy `references` point to existing constitutions/policies
- [ ] All contract schema `$ref` values resolve
- [ ] No orphaned artifacts (unreferenced files)
- [ ] No stale artifacts (referencing deprecated capabilities)

## Level 3 — Full Governance Audit
Verify the governance framework is internally consistent.

- [ ] Precedence hierarchy consistent across architecture doc, Asimov constitution, and Demerzel mandate
- [ ] Every Asimov article (0-5) has at least one behavioral test
- [ ] Every policy has at least one behavioral test
- [ ] Architecture doc artifact listings match actual files on disk
- [ ] Contract schemas cover all protocol flows in `galactic-protocol.md`
- [ ] All artifacts have valid semver versions

## How to Run
Read `policies/governance-audit-policy.yaml` for the full checklist with methods and severity levels. Execute each check and report results.

## State Maintenance (MANDATORY)

Audits MUST read and write Demerzel's persistent state:

### Before Auditing
1. Read existing beliefs from `state/beliefs/` for baseline
2. Read evolution logs from `state/evolution/` for artifact history

### After Auditing
1. **Update beliefs** in `state/beliefs/` for audit findings:
   - Schema validation passed → belief about framework integrity (T/F)
   - Cross-reference gaps found → belief about specific gap (F with evidence)
   - Audit clean → update confidence upward on integrity beliefs
2. **Update evolution logs** in `state/evolution/` — add audit events to assessed artifacts
3. **Write audit snapshot** to `state/snapshots/{date}-audit-level{N}.snapshot.json`

### Schema Compliance
- Beliefs: `logic/tetravalent-state.schema.json`
- Evolution: `logic/governance-evolution.schema.json`

## Source
`policies/governance-audit-policy.yaml`
