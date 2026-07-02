# [Example] Add `pr_fact` JSON schema for intelligence tracking

**Labels:** `ready-for-agent`, `worker:claude`, `routing:architecture`

## Goal
Create a Draft 2020-12 JSON schema for the `pr_fact` event to support Seldon intelligence tracking in the GitHub pipeline.

## Context
Seldon requires deterministic fact definitions derived from immutable Streeling event streams. We are adding the PR metrics fact to the schema registry.
- Related issue: #512 (Epic: Intelligence tracking)
- Reference spec: `docs/intelligence/kpi-catalog.md`

## Allowed Paths
- `schemas/seldon/pr-fact.schema.json`

## Non-goals
- Do not modify existing schemas.
- Do not write implementation code in `ga` or `ix`.
- Do not alter the overarching Seldon intelligence policy.

## Expected Output Artifacts
1. A new file `schemas/seldon/pr-fact.schema.json` containing the valid Draft 2020-12 schema.

## Test/Validation Plan
Run the schema validation script:
```bash
python scripts/validate_seldon_schemas.py
```
It must exit with code 0 and show `pr-fact.schema.json` as valid.

## Stop Conditions
- Halt if the validation script throws errors you cannot resolve within 3 retries.
- Halt if existing Seldon KPI catalogs contradict the schema requirements.

## Risk Tier
Low (Schema addition only).

## Dependency Links
- Blocks: #520 (PR KPI dashboard)

## Suggested Worker
`worker:claude` (Builder capability for JSON schema authoring).

## Acceptance Criteria
- `pr-fact.schema.json` is created.
- Schema defines fields: `pr_id`, `repo`, `author`, `lines_added`, `lines_removed`, `time_to_merge_seconds`.
- `validate_seldon_schemas.py` passes successfully.

## Reviewer Expectations
Skeptical Auditor (AI) will review the schema structure against Draft 2020-12 rules. Demerzel (Human) will review for alignment with the KPI catalog.
