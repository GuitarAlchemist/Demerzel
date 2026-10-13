---
module_id: dv-005-baselines-alerts-and-targets
department: data-visualization
course: Baselines, Alert Thresholds, and Historical Targets
level: beginner
prerequisites: [dv-001-observed-degraded-stale-quality, dv-004-uncertainty-in-small-qa-suites]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-005
version: "0.1.0"
---

# Baselines, Alert Thresholds, and Historical Targets

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 30 minutes | Status: English draft; subject, learner, and localization review pending

## Objectives

After this lesson, you will be able to:

- Identify a reference measurement, an alert threshold, and an acceptance target without treating them as the same decision.
- Read GA's historical quality report without turning a missing regression alert into a claim of improvement.
- Explain why a drift flag and a current regression flag may disagree.
- Write a chart caption that preserves date, comparison, data availability, and limits.

## The project question

A GA dashboard needs a single sentence about chatbot QA. Its [historical quality trend report at GA revision `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) says the latest pass rate is **98.08%**, its seven-day average is **98.08%**, **no regression is flagged**, and a **drift** was detected around June 15, 2026. Which of these supports a claim that the chatbot is currently meeting a product target?

None does by itself. The report is a historical artifact generated on July 23, 2026; its latest chatbot QA measurement comes from the July 19 snapshot. It does not state a product acceptance target, and its own detail row contains degraded observations. Start with [DV-001](dv-001-observed-degraded-stale-quality.md) for distinguishing real observations from degraded or stale feeds, and [DV-004](dv-004-uncertainty-in-small-qa-suites.md) for the resolution of the 52-prompt QA suite. Do not use this report as today's service status.

### Practice exercise 1: name the three roles

For each item, write *reference*, *alert rule*, or *acceptance target*: (a) the report's seven-day average, (b) the report generator's default 5.0% regression threshold, (c) “At least 95% of a named, stable prompt suite must pass before release,” a hypothetical team rule. Which item is absent from the historical report?

> **Answer:** (a) is a moving reference, (b) is an alert rule comparing measurements, and (c) is a hypothetical acceptance target. The report contains (a) and (b), but no stated product target like (c). A team would have to approve and record such a rule separately, including its suite and evaluation method.

## 1. A reference is a comparison, not a promise

GA's pinned [`state/quality/README.md`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/README.md) describes the trend generator's `--baseline YYYY-MM-DD` option as an **informational marker**. The rendered report also has rolling seven-day and 30-day averages. These are different uses of “baseline”: a named historical date and a calculated moving reference. Neither is a minimum acceptable result.

The report's chatbot headline has latest 98.08% and seven-day average 98.08%. Their displayed difference is zero. That arithmetic explains why an alert based on a bad-direction change from the displayed average need not fire. It does not prove that the prompt set, evaluator, or backend stayed fixed, and it does not establish that 98.08% is good enough for users. The [June 15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) files both report 52 prompts, but they do not provide stable prompt IDs or an evaluator revision. Equal denominators are insufficient to establish a matched population; see [DV-002](dv-002-denominators-and-test-populations.md).

### Practice exercise 2: read the no-alert line

The report says “None. All tracked metrics are within threshold vs their 7-day average” under regressions, while the chatbot headline reads 98.08% for both latest and seven-day average. Write the strongest supported chatbot statement and one unsupported conclusion.

> **Answer:** “In the report generated July 23, the latest chatbot QA measurement is from July 19; its displayed pass rate equals the displayed seven-day average at 98.08%, and no regression is flagged.” “The chatbot now satisfies a 98% product target” is unsupported: the report has no such target, the observation is historical, and the QA snapshots do not establish current user outcomes.

## 2. An alert rule asks a narrower question

The pinned archive instructions state that `ix-quality-trend` defaults to a regression threshold of 5.0% versus a seven-day average. The report describes bad-direction changes and treats higher pass rates as better. The alert rule asks whether a measured change crosses its configured comparator and threshold. It does not decide whether the whole service is healthy, whether a release should ship, or why a metric changed. In a new report, preserve the threshold's exact unit and the generator revision before calculating a borderline case; “5% relative change” and “five percentage points” differ.

The same report lists a chatbot drift flag “since 2026-06-15” while its current regression list is empty. Its methodology names Page–Hinkley drift detection over direction-adjusted metric levels. Drift detection asks about a pattern or change point in a series; the regression rule asks about a latest comparison against a recent average. These are distinct tests with distinct windows. A historical drift flag does not prove a current regression, and an empty current regression list does not erase an earlier change in the recorded series.

### Practice exercise 3: reconcile two indicators

A colleague says, “The report is contradictory: it flags chatbot drift but says no regression.” Repair the statement without inventing a cause for the drift.

> **Answer:** “The two indicators answer different questions. The current regression rule found no bad-direction change beyond its threshold against the seven-day reference; the drift detector marked a series change around June 15. Inspect the underlying dated observations, degraded records, and generator version before explaining that change.” The report alone does not identify a causal change in prompts, model, or code.

## 3. Availability and coverage limit both comparisons

The historical report lists 35 chatbot QA snapshot files loaded. Its chatbot overall pass-rate detail row shows `n = 26` and `n_degraded = 23`. These numbers have different scopes: “files loaded” covers the snapshot category, while `n` and `n_degraded` describe this plotted metric series. Twenty-three of 26 points in that row carry a degraded marker. Do not silently read the sparkline as 26 independent, healthy chatbot assessments.

The report separately marks several embedding and topology feeds stale, with their last real observation on June 25, 28 days before the report. An old “latest” value can still have a perfectly formatted average and threshold comparison. Mark freshness at the metric level. A missing or degraded observation is a gap in evidence, not a failure score and not a pass. A product target also needs an agreed test population, stable scoring, a run-quality rule, and a date range; otherwise a threshold check can look decisive while answering the wrong question.

### Practice exercise 4: preserve the denominator

What can you calculate from `n = 26` and `n_degraded = 23` in the chatbot row, and what can you **not** infer from that calculation? Why should a caption not say “23 of 35 chatbot QA files were degraded”?

> **Answer:** The row has `26 - 23 = 3` points without a degraded marker, and 23/26 row points are marked degraded. The report does not establish that the three points cover all user needs or that the 35 loaded files all contributed to this one metric. “23 of 35 files” mixes the category file count with a metric-series count.

## 4. Write the decision boundary into the chart

For a quality dashboard, put the observation date and measured population next to the number, and identify the report-generation date separately. Label the moving reference as a comparison. Label a threshold as an alert configuration and an acceptance target only when a separate decision record actually defines one. Show drift as a different marker with its own explanation. Link a dated source and expose degraded or stale status close to the plotted data. If the exact prompt corpus or evaluator revision is missing, say so in the decision text rather than hiding it in a tooltip.

### Practice exercise 5: caption the historical report

Write a two-sentence caption that a release reviewer could use for the pinned chatbot QA row. Include both the July 23 report date and July 19 observation date, the rate, comparator, no-alert result, drift, and the strongest limitation. Do not recommend release from this artifact alone.

> **Answer:** “GA's report generated July 23, 2026 shows the July 19 chatbot QA measurement at 98.08%, equal to the displayed seven-day average; no latest-versus-average regression is flagged, while drift is marked around June 15. The row includes 23 degraded points among 26 metric-series points, and the underlying snapshots do not identify matched prompts or evaluator versions, so this report alone cannot establish a current product target or release decision.”

## Key takeaways

- A historical marker, a moving average, an alert threshold, and a release target serve different decisions.
- “No regression flagged” means a particular alert rule did not fire; it is not a general quality verdict.
- Drift and latest-versus-average regression can legitimately disagree.
- Keep metric-series counts, category file counts, freshness, and degraded status visible.
- A product target needs its own agreed population, scoring rule, date window, and decision owner.

## Project evidence

- Pinned GA [quality report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md), [archive instructions](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/README.md), and [June 15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) / [July 19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) snapshots.
- The 5.0% threshold is a generator alert setting described by the pinned archive instructions, not a documented GA release target. The report does not pin the exact IX generator revision; verify it before explaining a borderline alert calculation.

*Research: `data-visualization-2026-10-11-005`. Human subject review, learner attempt, localization, and public Learn readback are pending.*
