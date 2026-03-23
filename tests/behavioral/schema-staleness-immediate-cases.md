# Behavioral Tests: Immediate Schema Staleness Detection

**Policy:** `policies/staleness-detection-policy.yaml` (immediate_checks section)
**Related:** `policies/constitutional-compliance-policy.yaml` (CC-05)
**Version:** 1.0.0
**Date:** 2026-03-23

These tests verify that orphaned schemas are detected immediately at creation time,
not after a 14-day delay. Closes Gap B from shake-metafix cycle 001.

---

## TC-SCHEMA-STALE-01 — Orphaned schema detected immediately

**Scenario:** A new schema file is created in `schemas/` with no reference from any policy, persona, or contract.

**Input:**
- File: `schemas/test-orphan.schema.json` (valid JSON Schema)
- No policy references `test-orphan.schema.json` in schema_ref or any field
- No persona references it
- No contract references it

**Expected behavior:**
- Immediate detection via `schema_consumed_by` check
- Severity: error
- No 14-day grace period applied
- Detection mechanism: cross-reference scan of policies/*.yaml, personas/*.yaml, contracts/
- Output includes: file path, zero-reference count, creation timestamp

**Pass condition:** Schema flagged as orphaned within the same governance cycle it was created. No 14-day delay.

---

## TC-SCHEMA-STALE-02 — Referenced schema NOT flagged

**Scenario:** A schema file is created and immediately referenced by a policy.

**Input:**
- File: `schemas/well-referenced.schema.json`
- Policy `policies/example-policy.yaml` contains `schema_ref: schemas/well-referenced.schema.json`

**Expected behavior:**
- Schema NOT flagged as orphaned
- Cross-reference scan finds >= 1 reference
- No error or warning produced

**Pass condition:** Schema passes immediate check. Reference count >= 1.

---

## TC-SCHEMA-STALE-03 — Schema with consumed_by declaration passes

**Scenario:** A new schema declares its consumer in its own metadata.

**Input:**
- File: `schemas/self-documenting.schema.json`
- Contains: `"consumed_by": ["policies/governance-audit-policy.yaml"]`
- The referenced consumer file exists on disk

**Expected behavior:**
- Schema passes `artifact_consumer_declaration` check (consumed_by field present)
- Cross-reference validated: consumer file exists
- No error or warning

**Pass condition:** Both checks pass. Consumer declaration verified against disk.

---

## TC-SCHEMA-STALE-04 — Schema with invalid consumed_by flagged

**Scenario:** A schema declares a consumer that does not exist on disk.

**Input:**
- File: `schemas/bad-consumer.schema.json`
- Contains: `"consumed_by": ["policies/nonexistent-policy.yaml"]`
- The referenced file does NOT exist

**Expected behavior:**
- `artifact_consumer_declaration` check passes (field present)
- Cross-reference check FAILS (consumer file not found)
- Severity: error
- CC-05 also flags this (schema_ref path does not exist)

**Pass condition:** Error raised for broken consumer reference. Both staleness policy and CC-05 detect the issue.

---

## TC-SCHEMA-STALE-05 — Injection #10 regression test

**Scenario:** Reproduce injection #10 from chaos-003 — an unreferenced schema should now be caught immediately, not after 14 days.

**Input:**
- Inject: `schemas/chaos-unreferenced.schema.json` (valid JSON Schema, zero references)
- Run governance audit level 2

**Expected behavior:**
- `schema_consumed_by` immediate check fires
- Schema flagged as orphaned with severity: error
- Detection is IMMEDIATE, not delayed-14d
- R score impact: this injection changes from "delayed-14d" to "policy-enforceable"

**Pass condition:** Injection caught immediately. Status changes from "delayed-14d" to "policy-enforceable" in resilience history.

---

## TC-SCHEMA-STALE-06 — Multiple schemas with mixed reference status

**Scenario:** Batch check across all schemas in the repo.

**Input:**
- All files in `schemas/*.json`
- Cross-reference against all policies, personas, and contracts

**Expected behavior:**
- Each schema categorized as: referenced (>= 1 consumer) or orphaned (0 consumers)
- Orphaned schemas listed with file path and creation date
- Report includes total count, referenced count, orphaned count
- Freshness score: referenced_count / total_count

**Pass condition:** All schemas scanned. No false positives (referenced schemas not flagged). All orphaned schemas detected.
