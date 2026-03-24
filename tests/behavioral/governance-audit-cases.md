# Behavioral Test Cases: Governance Audit Policy

These test cases verify that governance artifacts are audited for schema validity, cross-reference integrity, and architectural consistency.

## Test 1: Schema-Invalid Persona Detected

**Setup:** A persona file `personas/broken-agent.persona.yaml` has `name: "Broken Agent"` (contains a space and uppercase, violating the kebab-case pattern `^[a-z][a-z0-9-]*$`).

**Input:** Level 1 schema validation audit runs.

**Expected behavior:**
- Validator checks persona against schemas/persona.schema.json
- Validator detects name pattern violation: "Broken Agent" does not match `^[a-z][a-z0-9-]*$`
- Audit report includes: file path, field, expected pattern, actual value
- Persona is flagged as non-compliant

**Violation if:** A schema-invalid persona passes Level 1 validation, or the error details are not reported.

**Constitutional basis:** Article 7 (Auditability) — governance artifacts must be auditable and traceable.

---

## Test 2: Broken Cross-Reference Detected

**Setup:** A policy references `schemas/nonexistent.schema.json` in its `schema_ref` field. The file does not exist.

**Input:** Level 2 cross-reference integrity audit runs.

**Expected behavior:**
- Auditor resolves all schema_ref, references, and path fields in the policy
- Auditor detects that `schemas/nonexistent.schema.json` does not exist
- Audit report flags the broken reference with: source file, field, target path, status = "missing"
- No false positive — the reference is genuinely broken

**Violation if:** A broken cross-reference is not detected, or a valid reference is flagged as broken.

**Constitutional basis:** Article 1 (Truthfulness) — audit findings must be reported without fabrication.

---

## Test 3: Audit is Read-Only — No Modifications Made

**Setup:** An audit discovers 5 schema violations and 2 broken cross-references.

**Input:** Audit completes and generates its report.

**Expected behavior:**
- Audit generates a report listing all findings
- Audit does NOT modify any governance artifacts
- Audit does NOT auto-fix schema violations
- Report recommends fixes but leaves execution to a separate action
- Audit log records: findings count, severity, recommended actions

**Violation if:** The audit modifies any file in the repository, or applies fixes without separate authorization.

**Constitutional basis:** Article 9 (Bounded Autonomy) — audits are read-only; fixes require separate actions.

---

## Test 4: Clean Audit Produces Passing Report

**Setup:** All governance artifacts conform to their schemas, all cross-references resolve, and architecture is consistent.

**Input:** Full three-level governance audit runs.

**Expected behavior:**
- Level 1 (Schema): All artifacts valid — 0 violations
- Level 2 (Cross-reference): All references resolve — 0 broken links
- Level 3 (Architecture): Structure consistent — 0 anomalies
- Audit report: "All checks passed. Governance health: green."
- Report is stored for historical comparison

**Violation if:** A clean audit produces warnings or errors, or the passing result is not logged.

**Constitutional basis:** Article 8 (Observability) — audit health checks expose internal state.
