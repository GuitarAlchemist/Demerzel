---
name: demerzel-metasync
description: Detect and fix drift between documentation and reality — README counts, CLAUDE.md descriptions, cross-repo references, and grammar section counts.
---

# Demerzel MetaSync — Documentation Reality Alignment

Detect drift between what Demerzel's documentation *claims* and what actually *exists* on disk. Auto-fix trivial drift (counts). Flag structural drift for review.

## Usage

`/demerzel metasync` — full sync scan and auto-fix
`/demerzel metasync --scan` — scan only, report drift without fixing
`/demerzel metasync --fix counts` — fix only artifact counts in README and CLAUDE.md
`/demerzel metasync --fix cross-repo` — check cross-repo references are valid
`/demerzel metasync --fix grammars` — verify grammar section counts in README

## What MetaSync Checks

### 1. README Artifact Counts

The README.md contains a `## Artifact Counts` table. MetaSync verifies each row against disk:

| Row | Source glob | How to count |
|-----|-------------|--------------|
| Constitutions | `constitutions/*.md` | count .md files |
| Personas | `personas/*.persona.yaml` | count .persona.yaml files |
| Policies | `policies/*.yaml` | count .yaml files |
| Grammars | `grammars/*.ebnf` | count .ebnf files |
| Schemas | `schemas/*.json` | count .json files |
| Behavioral tests | `tests/behavioral/*.md` | count .md files |
| Skills | `.claude/skills/*/` | count directories |
| Departments | `state/streeling/departments/*.department.json` | count .department.json files |
| Courses | `state/streeling/courses/**/en/` | count `en/` directories |

### 2. CLAUDE.md Description Counts

CLAUDE.md (the context file) embeds counts in prose descriptions. MetaSync verifies:

- `policies/` line: count listed policy names against `policies/*.yaml`
- `tests/behavioral/` line: count stated test suites against actual files
- `personas/` line: stated persona count against `personas/*.persona.yaml`

### 3. Cross-Repo References

Check that named files referenced in README ecosystem table exist:
- `grammars/sci-ml-pipelines.ebnf` referenced in IxQL section
- `docs/ixql-guide.md` referenced in README
- `policies/alignment-policy.yaml` referenced in HITL pattern note

### 4. Grammar Section Count

README states IxQL grammar has "11 sections" — verify against actual `grammars/sci-ml-pipelines.ebnf` section headers.

### 5. Streeling University Description

README body text says "16-department knowledge framework" — verify against actual department count in `state/streeling/departments/`.

## Process

### Step 1: SCAN

For each check above:
1. Count actual files on disk
2. Extract documented count from README/CLAUDE.md
3. Record as MATCH, TRIVIAL_DRIFT (count-only), or STRUCTURAL_DRIFT

```
TRIVIAL_DRIFT:  documented count ≠ actual count (auto-fixable)
STRUCTURAL_DRIFT: referenced file missing, broken link, wrong description
```

### Step 2: REPORT

Print drift summary:

```
MetaSync Scan Results — {date}
==============================
MATCHES (no action needed):
  ✓ Personas: 14
  ✓ Schemas: 23
  ✓ Skills: 37
  ✓ Courses: 14

TRIVIAL DRIFT (auto-fixable counts):
  ✗ Policies: README says 24, actual: 25
  ✗ Grammars: README says 21, actual: 26
  ✗ Behavioral tests: README says 44, actual: 52
  ✗ Departments: README says 16, actual: 21
  ✗ CLAUDE.md policies count: says 24, actual: 25
  ✗ CLAUDE.md tests count: says 41, actual: 52

STRUCTURAL DRIFT (requires review):
  ! docs/ixql-guide.md — referenced in README, check existence
  ! CLAUDE.md Streeling description says "16-department", actual: 21

Total: {N} trivial drifts, {M} structural flags
```

### Step 3: AUTO-FIX (trivial drift)

For each TRIVIAL_DRIFT:
1. Update the count in README.md artifact table
2. Update the count in CLAUDE.md prose where present
3. Commit with `fix: MetaSync — update artifact counts`

For STRUCTURAL_DRIFT: report only, do not auto-fix. Flag for human review.

### Step 4: LOG

After fixing, update `state/evolution/metasync-log.json`:

```json
{
  "timestamp": "2026-03-22T00:00:00Z",
  "scan_date": "2026-03-22",
  "trivial_drifts_fixed": 6,
  "structural_flags": 2,
  "artifacts_checked": 9,
  "fixes": [
    {"artifact": "Policies", "was": 24, "now": 25, "file": "README.md"},
    {"artifact": "Grammars", "was": 21, "now": 26, "file": "README.md"},
    {"artifact": "Behavioral tests", "was": 44, "now": 52, "file": "README.md"},
    {"artifact": "Departments", "was": 16, "now": 21, "file": "README.md"}
  ]
}
```

## Drift Classification

| Drift type | Description | Action |
|------------|-------------|--------|
| Count mismatch | README says N, disk has M | Auto-fix: update count |
| Missing reference | README links to file that doesn't exist | Flag for review |
| Stale description | Prose description inconsistent with reality | Flag for review |
| Schema count wrong | CLAUDE.md says "6 contract schemas", verify | Auto-fix if count-only |

## Scheduling

MetaSync should run:
- After every `/demerzel metabuild` (new artifacts created)
- As part of the driver RECON phase
- On demand via `/demerzel metasync`

## Governance

- Article 1 (Truthfulness) — documentation must not claim false counts
- Article 7 (Auditability) — every sync run is logged
- Article 8 (Observability) — drift metrics are governance health signals
- README sync policy — this skill implements the readme-sync-policy.yaml
- Staleness detection — drift counts older than 7 days trigger escalation

## Integration with MetaFix

When MetaSync finds STRUCTURAL_DRIFT:
- Log as anti-pattern in `state/patterns/`
- Feed to `/demerzel metafix` for Level 2+ analysis
- MetaFix determines root cause and prevents recurrence
