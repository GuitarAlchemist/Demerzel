# [Example] Add `pr_fact` JSON schema

**Fixes #518** (Add `pr_fact` JSON schema for intelligence tracking)

## Summary
Adds the new Draft 2020-12 JSON schema for `pr_fact` to the `schemas/seldon/` directory. This aligns with the requirements specified in the KPI catalog for intelligence tracking.

## Validation Evidence
Ran the required validation scripts locally.

```bash
$ python scripts/validate_seldon_schemas.py
=== Seldon Schema Validation ===
OK schemas/seldon/pr-fact.schema.json
Result: 1 valid, 0 invalid
PASSED
```

## Risk Notes
**Path:** `schemas/seldon/pr-fact.schema.json`
**Risk:** Low. This is a purely additive schema file. It does not modify existing validation rules for other events and does not change any runtime code in `ix` or `ga`.

## Follow-up Issues
None. The scope of this PR exactly matches the vertical slice defined in #518.

## Review Notes
- **Skeptical Auditor:** Please confirm the schema structure correctly utilizes the Draft 2020-12 specification, particularly the types for `time_to_merge_seconds`.
- **Demerzel:** Awaiting human approval before merge. No auto-merge expected.
