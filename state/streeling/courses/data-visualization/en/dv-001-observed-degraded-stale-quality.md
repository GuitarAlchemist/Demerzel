---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Observed, Degraded, and Stale Quality Runs
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Observed, Degraded, and Stale Quality Runs

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 35 minutes | Status: review pending

## Objectives

After this lesson, you will be able to:

- Distinguish a measured pass rate from an unavailable run and a carried-forward historical value.
- Draw a quality timeline that does not turn missing observations into failures or silently bridge an outage.
- Identify the denominator, freshness, and environment checks required before comparing two measurements.
- Give a text and tabular alternative to a status chart.

## The project question

GA records chatbot QA snapshots under `state/quality/chatbot-qa/`. A dashboard reader asks, "Did the chatbot get worse?" The display must answer only as far as the records allow. This lesson uses four **historical fixtures**, pinned to GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). They are an exercise dataset, not a claim about today's chatbot.

| Snapshot date | `total_prompts` | `pass_pct` | `degraded` | What the record supports |
|---|---:|---:|---|---|
| [2026-06-08](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | The backend was unavailable; no pass rate was reported. |
| [2026-06-15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75.00 | `false` | A pass rate was reported for this run. |
| [2026-06-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7.69 | `false` | A low pass rate was reported; the snapshot alone does not explain why. |
| [2026-07-19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98.08 | `false` | A higher pass rate was reported for this later run. |

### Practice exercise

Classify each row as an observed pass rate or an unavailable run. Which row can be placed on a pass-rate axis at 0%?

> **Answer:** June 15, June 19, and July 19 have reported pass rates. June 8 is an unavailable run. None of these rows reports a 0% pass rate; placing June 8 at zero would invent a measurement.

## 1. Three different data states

An **observation** is a value actually reported by a run. An **unavailable run** says the measurement could not be made or trusted under its stated conditions. A **carried-forward value** is a previous observation shown for context; it is not a new measurement on the date it is displayed.

The June 8 file has `pass_pct: null`, `degraded: true`, and `degraded_reason: "backend_unavailable"`. It also contains `last_known_good_pass_pct: 94.0` with an earlier date and `last_known_good_source: "carryforward"`. The 94.0 value belongs to the earlier observation. Plotting it as a June 8 point would make an outage look like steady performance. Plotting `null` as zero would make it look like a chatbot failure. Both transformations change the claim.

Keep two fields in the display model: `quality_value` for measured pass rate, and `run_status` for observed, degraded, or unknown. Preserve the source timestamp of any historical reference separately from the display date. Do not infer a quality value from `total_prompts`: the June 8 note reports backend errors rather than scored chatbot answers.

### Practice exercise

A dashboard card for June 8 reads "94% pass rate" because the file contains `last_known_good_pass_pct: 94.0`. Rewrite the card in one sentence.

> **Answer:** "June 8 QA unavailable: backend unavailable; last known good value was 94% on May 16." The card must make the historical date visible and leave the June 8 pass rate unknown.

## 2. Draw quality and availability separately

Use a pass-rate axis only for measured values. Put a gap where `pass_pct` is `null`, rather than connecting two points across it. A second, aligned availability lane can mark the June 8 run as degraded with an icon and text label. That gives the reader two separate answers: what was measured, and whether a measurement was available.

For the four-row fixture, a textual sketch is sufficient:

```text
Date          Quality lane          Availability lane
2026-06-08    no point              DEGRADED: backend unavailable
2026-06-15    75.00%                observed
2026-06-19     7.69%                observed; investigate
2026-07-19    98.08%                observed
```

These are sparse dates, not four consecutive daily readings. A drawn line between June 19 and July 19 would suggest that the unshown days were measured and followed a smooth path. If the full series has gaps, segment the line at them. Show the actual dates, not equally spaced category slots that erase elapsed time. The GA [quality trend report at the pinned commit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) also marks stale feeds; a displayed "latest" value needs its observation date.

### Practice exercise

Sketch a two-lane view of June 8 and June 15. Include the date and a text status. Should the 94% carried-forward value join a line to June 15's 75%?

> **Answer:** June 8 gets no quality point and a "backend unavailable" availability marker. June 15 gets a 75% point and "observed" marker. The 94% reference is annotated with its original May 16 date and is not a June 8 point or a line segment to June 15.

## 3. A low number is a question, not a diagnosis

June 19 reports 7.69% and `degraded: false`. The chart should display the number, but it cannot conclude from this file alone whether GA code regressed, the model changed, the corpus changed, or another dependency behaved differently. `degraded: false` only records the producer's classification for that run; it is not a complete health certificate. Investigate the run configuration, prompt identities, backend logs, scoring rules, and adjacent runs before attributing cause.

The three observed rows each list 52 prompts. That is useful context, but equal counts do not prove identical questions or scoring. A comparison should pin the corpus revision and evaluator version as well as the count. If those fields are missing, annotate the comparison as provisional. A percentage axis without a denominator and source can conceal how fragile a small sample is.

### Practice exercise

Assess the statement "GA recovered from a confirmed software regression between June 19 and July 19." Which part is observed, and which part needs more evidence?

> **Answer:** The files report 7.69% on June 19 and 98.08% on July 19. "Recovered" and "software regression" attribute a cause and continuity that the four snapshots do not establish. Compare the same prompt corpus, evaluator, and environment and inspect the failures before making that claim.

## 4. Make the chart readable without color

Color can help, but an outage marker must also have a label or shape. The [W3C guidance on use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) requires another visual cue when color carries information. The [W3C guidance on non-text content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) explains that a chart needs a text alternative that conveys its purpose; a data table can carry the exact values.

For this fixture, a useful short description is: "Historical GA chatbot QA: June 8 unavailable; reported pass rates were 75% on June 15, 7.69% on June 19, and 98.08% on July 19. Cause of the low June 19 result is not established here." Keep the table above next to the chart. A screen reader user should be able to reach the dates, values, and statuses without interpreting color or a tooltip.

### Practice exercise

Review an icon-only red dot on June 8. What information must be added?

> **Answer:** Add visible text such as "backend unavailable" and a programmatically available label. Keep June 8's pass rate absent. Supply a table or equivalent description with the date and status.

## Key takeaways

- Missing quality data is neither a zero score nor a successful score.
- A carried-forward reference keeps its original observation date.
- A chart should display measurement availability alongside measured quality.
- A low observed percentage can trigger investigation without proving a cause.
- Dates, denominators, source revisions, and accessible text are part of the claim.

## Further reading and project evidence

- GA [historical chatbot QA snapshots](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) and [quality trend report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). The latter is a dated report, not live status.
- W3C, [Understanding Success Criterion 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C, [Understanding Success Criterion 1.1.1: Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Research: `data-visualization-2026-10-04-001`. Subject review and localization are pending; do not present this draft as a verified course.*
