---
name: demerzel-evolve
description: Show governance evolution insights — track artifact effectiveness, identify promotion/deprecation candidates, detect waste
---

# Demerzel Governance Evolution

Inspect the governance evolution log to understand which artifacts are effective and which need attention.

## Usage
`/demerzel evolve [view]` — view is `summary`, `promotions`, `waste`, or `full`

## Views

### summary (default)
Show top-level metrics for all governance artifacts:
- Citation count, violation count, compliance rate
- Last cited/violated timestamps
- Promotion or deprecation candidate flags

### promotions
Show artifacts that meet promotion criteria:
- Patterns appearing in 3+ PDCA cycles (ready for policy promotion)
- Policies with 100% compliance and high citation count (ready for constitutional consideration)

### waste
Show potential governance waste:
- Artifacts with zero citations (ceremony_without_value)
- Stale artifacts (not cited in 90+ days)
- Redundant governance (overlapping coverage)

### full
Complete evolution log with all events and assessments.

## Integration
- Feeds into `/demerzel promote` for promotion decisions
- Feeds into `/demerzel audit` Level 3 for effectiveness assessment
- Feeds into Kaizen waste detection (Muda categories)
- Seldon uses evolution insights as experiential knowledge

## Source
`logic/governance-evolution.schema.json`, `docs/superpowers/specs/2026-03-15-governance-meta-compounding-design.md` Section 5
