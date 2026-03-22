# Weakness Prober — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** Demerzel (policy, schema, driver integration, behavioral tests)
**Issue:** #97

## Overview

The weakness prober is a RECON extension that ranks system weaknesses by severity and feeds them into the Driver PLAN phase. While the completeness instinct (System 4) scans for what's *missing*, the weakness prober (System 3*) audits what *exists but is weak* — test gaps, stale artifacts, low-confidence beliefs, uncited policies, error-prone areas.

This is Stafford Beer's System 3* function: sporadic auditing that goes beyond routine management to probe for hidden weaknesses.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Position in cycle | RECON Stage 3c (after meta-recognition 3b) | Needs enriched data from Stages 1-2 and meta-proposals from 3b |
| Output | Ranked weakness list with severity scores | Directly consumable by PLAN phase priority scoring |
| Probe independence | Each probe runs independently | Parallelizable, testable in isolation, new probes addable |
| Scoring | Normalized 0.0-1.0 weakness score per finding | Comparable across probe types |
| Remediation | Proposals, not actions | System 3* recommends; System 3 (driver) decides |

## The Five Probes

### Probe 1: Repo Health Weakness

**What it measures:** Which repo is the weakest link across CI, tests, governance, dependencies.

**Data sources:**
- `state/driver/health-scores.json` — composite health per repo
- GitHub API — CI runs, test results, Dependabot alerts
- Governance artifact coverage analysis

**Weakness indicators:**
- CI failure rate > 20% in last 7 days
- Test pass rate < 90%
- Governance coverage < 80%
- Critical Dependabot alerts > 0
- Submodule drift > 5 commits

**Scoring:**
```
repo_weakness = 1.0 - health_score
severity = critical if repo_weakness > 0.5
           high     if repo_weakness > 0.3
           medium   if repo_weakness > 0.15
           low      otherwise
```

### Probe 2: Belief Weakness

**What it measures:** Beliefs that are stale, low-confidence, or contradictory while still being cited in decisions.

**Data sources:**
- `state/beliefs/*.belief.json` — all beliefs
- Cycle manifests — which beliefs were cited in recent decisions
- Evolution logs — belief change history

**Weakness indicators:**
- Stale belief in use: cited in last 7 days but not updated in 14 days
- Unresolved contradiction: value = C for more than 7 days
- Decaying confidence: confidence trending downward over 3+ cycles
- Orphan belief: not cited in any recent decision (potential dead state)

**Scoring:**
```
belief_weakness = base_score + staleness_bonus + citation_bonus
  base: 0.3 (any weakness detected)
  staleness_bonus: +0.1 per 7 days stale (cap 0.3)
  citation_bonus: +0.2 if belief was cited in a decision
  contradiction_bonus: +0.2 if value == C
severity: critical if stale AND cited AND confidence < 0.5
          high     if stale AND cited
          medium   if stale OR contradictory
          low      if orphan only
```

### Probe 3: Governance Coverage Weakness

**What it measures:** Governance artifacts that exist but lack enforcement, testing, or cross-reference integrity.

**Data sources:**
- `policies/*.yaml` — all policies
- `personas/*.persona.yaml` — all personas
- `tests/behavioral/*-cases.md` — all behavioral tests
- `grammars/*.ebnf` — all grammars
- `schemas/*.schema.json` — all schemas

**Weakness indicators:**
- Policy without behavioral test
- Persona without behavioral test
- Policy without enforcement trigger (no `triggers:` field or empty)
- Grammar with zero research cycles (never used)
- Schema unreferenced by any JSON file
- Department without courses
- Asimov article without behavioral test coverage

**Scoring:**
```
governance_weakness = base_score + constitutional_bonus
  base: 0.4 (untested artifact)
  constitutional_bonus: +0.3 if artifact is constitutional or implements Asimov article
  enforcement_bonus: +0.2 if policy has no trigger mechanism
severity: critical if constitutional artifact untested
          high     if policy untested or unenforced
          medium   if persona untested or grammar unused
          low      if schema orphaned or department empty
```

### Probe 4: Cycle Effectiveness Weakness

**What it measures:** Whether the governance system is actually improving or stagnating.

**Data sources:**
- `state/manifests/*.manifest.json` — cycle history
- `state/evolution/*.evolution.json` — evolution trajectory
- `LOG.md` — cycle summaries

**Weakness indicators:**
- Recurring task failures: same task type fails 2+ times across cycles
- High revert ratio: > 30% of tasks reverted in a cycle
- Sub-linear compounding: D_c < 1.0 (fractal compounding dimension)
- Stalled PDCA: cycles stuck in Plan phase > 14 days
- Diminishing task completion: fewer tasks completed per cycle (3-cycle trend)

**Scoring:**
```
cycle_weakness = max(individual_scores)
  recurring_failure: 0.6 + 0.1 per recurrence (cap 0.9)
  high_revert: revert_ratio (direct mapping)
  sub_linear: 1.0 - D_c (inverted — D_c=0.5 yields weakness 0.5)
  stalled_pdca: 0.4 + 0.05 per day stalled (cap 0.8)
severity: critical if recurring_failure AND high_revert
          high     if any score > 0.6
          medium   if any score > 0.3
          low      otherwise
```

### Probe 5: Conscience Weakness

**What it measures:** Ethical signals that are unresolved, aging, or being ignored.

**Data sources:**
- `state/conscience/signals/*.signal.json`
- `state/conscience/patterns/*.pattern.json`
- `state/conscience/regrets/*.regret.json`

**Weakness indicators:**
- Stale conscience signal: active > 3 days (per staleness-detection-policy)
- Unresolved pattern: active > 14 days with no linked resolution
- Unaddressed regret: active > 7 days
- Rising discomfort trend: pattern discomfort increasing over 3+ signals

**Scoring:**
```
conscience_weakness = max(individual_scores)
  stale_signal: 0.7 + 0.1 per day over threshold (cap 0.95)
  unresolved_pattern: 0.5 + 0.03 per day over threshold (cap 0.8)
  unaddressed_regret: 0.4 + 0.05 per day over threshold (cap 0.8)
severity: critical if ANY stale signal (ethics cannot wait)
          high     if unresolved pattern
          medium   if unaddressed regret
          low      if rising trend only
```

## Weakness Report Schema

Output conforms to `schemas/weakness-report.schema.json`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/weakness-report",
  "title": "Weakness Report",
  "description": "Ranked system weaknesses with severity scores and remediation proposals",
  "type": "object",
  "required": ["report_id", "timestamp", "weaknesses", "summary"],
  "properties": {
    "report_id": {
      "type": "string",
      "pattern": "^wr-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$"
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "cycle_id": { "type": "string" },
    "weaknesses": {
      "type": "array",
      "items": { "$ref": "#/$defs/weakness" }
    },
    "summary": { "$ref": "#/$defs/summary" }
  },
  "$defs": {
    "weakness": {
      "type": "object",
      "required": ["id", "probe", "target", "severity", "score", "evidence", "remediation"],
      "properties": {
        "id": { "type": "string", "pattern": "^w-[0-9]{3}$" },
        "probe": {
          "type": "string",
          "enum": ["repo_health", "belief", "governance_coverage", "cycle_effectiveness", "conscience"]
        },
        "target": { "type": "string", "description": "What is weak" },
        "severity": {
          "type": "string",
          "enum": ["critical", "high", "medium", "low"]
        },
        "score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "indicator": { "type": "string" },
              "value": {},
              "threshold": {},
              "source": { "type": "string" }
            }
          },
          "minItems": 1
        },
        "remediation": {
          "type": "object",
          "properties": {
            "proposed_action": { "type": "string" },
            "skill": { "type": "string", "description": "Which skill to invoke" },
            "risk_level": { "type": "string", "enum": ["low", "medium", "high"] },
            "reversible": { "type": "boolean" }
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_weaknesses": { "type": "integer" },
        "critical_count": { "type": "integer" },
        "high_count": { "type": "integer" },
        "medium_count": { "type": "integer" },
        "low_count": { "type": "integer" },
        "weakest_link": { "type": "string", "description": "Single highest-scored weakness" },
        "overall_resilience": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "1.0 - max(weakness_scores). System resilience metric."
        }
      }
    }
  }
}
```

## Driver Integration

### RECON Phase

The weakness prober runs as **Stage 3c** after meta-recognition:

```
RECON
  Stage 1: Gather
  Stage 2: Enrich
  Stage 3: Analyze (governance drift, anomalies)
  Stage 3b: Meta-Recognize (meta-opportunities)
  Stage 3c: Weakness Probe (THIS — weakest-link detection)
  Stage 4: Surface (situation report now includes weakness report)
```

### PLAN Phase

Weakness findings feed into PLAN priority scoring:

```
task_priority = base_priority
  + weakness_severity_bonus
  + weakness_score * 0.3

severity_bonus:
  critical: +0.4
  high:     +0.2
  medium:   +0.1
  low:      +0.0
```

Critical weaknesses become mandatory tasks (cannot be deprioritized by adaptive strategy).

### COMPOUND Phase

After the cycle, update weakness tracking:
- Did remediation reduce the weakness score?
- Has the weakness persisted across cycles? (escalate)
- New weakness patterns → feed to meta-recognition repetition detector

## Remediation Mapping

| Weakness Type | Primary Skill | Fallback |
|--------------|---------------|----------|
| CI failure rate | `/demerzel metafix` | Create GitHub issue |
| Stale belief | `/demerzel metasync` | `/seldon research` |
| Untested policy | `/demerzel metabuild --test` | Create GitHub issue |
| Untested persona | `/demerzel metabuild --test` | Create GitHub issue |
| Unused grammar | `/seldon research-cycle` | Archive candidate |
| Recurring failure | `/demerzel metafix` | Escalate to human |
| Stale conscience | `/demerzel conscience-cycle` | Hard escalate |
| Sub-linear D_c | `/demerzel compound` | Governance review |

## VSM Mapping

| VSM Component | Weakness Prober Role |
|--------------|---------------------|
| System 3* | The prober IS System 3* — sporadic audit function |
| System 3 | Driver receives probe results and acts (control) |
| System 4 | Completeness instinct scans for missing; prober scans for weak |
| System 5 | Constitution defines what "weak" means (thresholds, priorities) |

System 3* (prober) complements System 3 (routine management). The driver's regular RECON handles known metrics. The weakness prober goes deeper — it asks "what could fail that we're not watching?"

## Observability

| Metric | Formula | Target | Alert |
|--------|---------|--------|-------|
| overall_resilience | 1.0 - max(weakness_scores) | > 0.7 | < 0.5 |
| critical_weakness_count | count(severity == critical) | 0 | > 0 |
| weakness_closure_rate | closed_per_cycle / opened_per_cycle | > 1.0 | < 0.5 |
| probe_coverage | probes_run / total_probes | 1.0 | < 0.8 |
| mean_weakness_age | avg(days since first detected) | < 14 | > 30 |

## Constitutional Basis

- **Article 3 (Reversibility)** — remediations must be reversible
- **Article 4 (Proportionality)** — severity determines response scope
- **Article 6 (Escalation)** — critical weaknesses escalate to human
- **Article 7 (Auditability)** — all findings logged with evidence
- **Article 8 (Observability)** — resilience score is a governance metric
- **Article 9 (Bounded Autonomy)** — prober recommends, driver decides

## Behavioral Tests

See `tests/behavioral/weakness-prober-cases.md`.

## IxQL Pipeline

See `pipelines/weakness-probe.ixql` for the executable pipeline.
