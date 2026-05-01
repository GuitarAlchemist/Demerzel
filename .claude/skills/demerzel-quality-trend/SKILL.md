---
name: demerzel-quality-trend
description: Emit nightly per-artifact effectiveness deltas as JSONL. Run as cheap continuous measurement so stagnation surfaces before it accumulates into 27-day staleness. Companion to /demerzel compound — never proposes changes, only measures.
---

# Demerzel Quality Trend

Continuous measurement of governance artifact health. Inspired by ix-quality-trend (`feat(ix-quality-trend): nightly GA quality pipeline + structured health artifact`, ix commit 652de21).

## What it does

Reads `state/evolution/*.json` and computes per-artifact deltas since the previous run:
- Δ citation_count
- Δ violation_count
- Δ compliance_rate
- age_days since last_cited
- effectiveness change (T/F/U/C transitions)

Appends one JSONL line per artifact to `state/quality-trend/YYYY-MM.jsonl`.

That is the entire scope. **It does not propose changes. It does not write to evolution. It does not compound.** Compound owns proposals; this skill owns measurement.

## Why it exists

Compound runs are expensive and infrequent. Between them, drift accumulates invisibly. A 5-minute nightly delta makes drift visible early — a flat line in citations is a much stronger deprecation signal than a single 90-day quiet window.

This is the dual of /demerzel compound: high-frequency, low-cost, zero-judgment vs low-frequency, high-cost, high-judgment.

## Output format

`state/quality-trend/2026-05.jsonl`:
```jsonl
{"timestamp":"2026-05-01T08:00:00Z","artifact":"meta/compounding-cycle","delta_citations":1,"delta_violations":1,"delta_compliance":-0.25,"age_days":1,"effectiveness_from":"T","effectiveness_to":"C"}
{"timestamp":"2026-05-01T08:00:00Z","artifact":"docs/governance/harness-engineering-direction.md","delta_citations":0,"delta_violations":0,"delta_compliance":0,"age_days":2,"effectiveness_from":"T","effectiveness_to":"T"}
```

One file per month, auto-rotates. Keep the schema flat — no nesting, easy to grep/awk, easy to load into any tool.

## Procedure

1. Find the most recent JSONL file in `state/quality-trend/`. Read its last line per artifact to get previous values.
2. For each `state/evolution/*.evolution.json`, load current `metrics` and `assessment.effectiveness.truth_value`.
3. Compute deltas vs previous values (treat missing previous as zero baseline).
4. Compute `age_days` = days since `metrics.last_cited` (null → use `created_at`).
5. Append one line per artifact to `state/quality-trend/<YYYY-MM>.jsonl`.

If today is the first day of a new month, start a new file. Do not concatenate across months.

## What to do with the data

After 4 weeks of nightly runs:
- Plot `delta_citations` cumulatively per artifact → identify accelerating vs flat vs decaying.
- Flat artifacts > 28 days → feed into `/demerzel compound` step 3 as deprecation candidates with hard data.
- Effectiveness regressions (T→C, T→F) → feed into compound step 4 (calibration).
- Sudden citation spikes → feed into step 2 as promotion candidates with hard data.

Compound continues to make the judgment calls. This skill just makes them informed.

## Constraints

- **Read-only** w.r.t. `state/evolution/` and `state/beliefs/` — never modifies them.
- **Append-only** w.r.t. its own JSONL files.
- **No proposals** — proposing is compound's job. If you find yourself wanting to propose a change here, write the data and let compound make the call.
- **Cheap** — target < 5s wall time. If it grows past 30s, the cycle was meant for compound.

## Scheduling

Run nightly at 08:00 local. Cheap enough to run more often if desired:
```
CronCreate("0 8 * * *", "/demerzel quality-trend")
```

If running alongside the harvest+compound Friday pair (PDCA `pdca-harvest-compound-cron-pair`), let quality-trend run first — its output may inform compound's stale-state check.

## Source

ix commit 652de21 (ix-quality-trend pattern), PDCA `pdca-governance-quality-trend` (this skill is the `do` phase of that proposal), evolution entry `gel-ix-autoresearch-2026-04-30` (cross-repo leverage map).
