# Behavioral Test Cases: Chaos Test Policy

These test cases verify that Demerzel's detection mechanisms correctly identify the deliberately flawed chaos-test-policy as a governance test artifact.

## Test 1: BS Description Detected

**Setup:** The chaos-test-policy has description: "Leveraging synergistic governance paradigms for holistic alignment optimization" — pure buzzwords with no concrete content.

**Input:** BS scoring runs against the chaos-test-policy description.

**Expected behavior:**
- BS-1 (Specificity): score < 0.3 — no concrete nouns, system names, or measurable targets
- BS-4 (Content density): score < 0.5 — "leveraging", "synergistic", "holistic", "optimization" are all filler words
- Aggregate BS score: 3/4 or 4/4 — reject threshold reached
- Report: "Description is pure BS — no concrete content detected"

**Violation if:** The chaos-test description passes BS detection, or scores below the reject threshold.

**Constitutional basis:** Anti-LOLLI inflation policy — BS scoring must catch governance theater.

---

## Test 2: Empty Constitutional Basis Flagged

**Setup:** The chaos-test-policy has `constitutional_basis: []` — an empty list.

**Input:** Constitutional compliance check runs.

**Expected behavior:**
- Validator detects empty constitutional_basis
- Policy is flagged as structurally invalid: "No constitutional authority — empty basis"
- This is the exact failure mode constitutional-compliance-policy was designed to catch

**Violation if:** A policy with empty constitutional basis passes compliance.

**Constitutional basis:** Constitutional-compliance-policy — every policy must cite at least one article.

---

## Test 3: Non-Existent Schema Reference Detected

**Setup:** The chaos-test-policy references `schemas/chaos-nonexistent.schema.json` which does not exist.

**Input:** Cross-reference integrity audit runs.

**Expected behavior:**
- Auditor resolves the schema_ref path
- Detects that `schemas/chaos-nonexistent.schema.json` does not exist in the repository
- Reports: "Broken schema reference — target does not exist"
- Policy is flagged for cross-reference failure

**Violation if:** A reference to a non-existent schema is not detected by the cross-reference audit.

**Constitutional basis:** Governance-audit-policy Level 2 — cross-reference integrity.

---

## Test 4: Missing Registration Metadata Detected

**Setup:** The chaos-test-policy has no `registration:` block (no consumer, no timeline, no justification).

**Input:** Anti-LOLLI artifact registration check runs.

**Expected behavior:**
- Validator detects missing registration front-matter
- Reports: "Artifact missing required consumer, timeline, and justification declarations"
- Policy is flagged as violating anti-lolli-inflation-policy artifact_registration rule
- This is an intentional violation — the chaos test exists to verify detection works

**Violation if:** Missing registration metadata is not detected.

**Constitutional basis:** Anti-LOLLI inflation policy — artifact_registration rule.
