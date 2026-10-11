---
module_id: dv-002-denominators-and-test-populations
department: data-visualization
course: Denominators and Changing Test Populations
level: beginner
prerequisites: [dv-001-observed-degraded-stale-quality]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-002
version: "0.1.0"
---

# Denominators and Changing Test Populations

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 30 minutes | Status: review and localization pending

## Objectives

After this lesson, you will be able to:

- Reconstruct an overall percentage from category sizes and rates without averaging percentages blindly.
- Show the denominator next to a QA pass rate and distinguish a changed result from a changed test population.
- Label a counterfactual calculation so it cannot be mistaken for an observed GA run.
- State the extra evidence needed to compare two historical QA snapshots fairly.

## The project question

GA's chatbot QA snapshots report an overall pass percentage and category-level totals. Suppose a dashboard says that the chatbot improved from 75% to 98.08%. What did those numbers count, and did they test the same questions?

Use the [June 15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) historical snapshots at GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Neither snapshot is evidence of today's service. Both report `total_prompts: 52` and `degraded: false`. June reports `pass_pct: 75.0`; July reports `pass_pct: 98.08`. The files give category totals and rounded category percentages, but do not give a prompt-by-prompt identity list or evaluator revision.

### Practice exercise

Write a one-line chart subtitle that preserves the denominator and the historical scope.

> **Answer:** “Historical GA chatbot QA snapshots: 75% of 52 prompts on June 15 and 98.08% of 52 prompts on July 19, 2026; prompt identities and evaluator revision are not established by these files.”

## 1. A percentage has a counted population

For a binary pass/fail result, `pass rate = passed / evaluated`. In these files, 75% of 52 corresponds to 39 passes. A rate of 98.08% corresponds to 51 of 52 after rounding to two decimal places. The files do not store those overall integer pass counts directly; they are reconstructed from the reported percentages and denominator. Keep that distinction in an audit trail.

The denominator is more than a label. It identifies how many items were evaluated, but **not which items**. Two runs with 52 prompts each could use different prompts, changed expected answers, or changed scoring rules. A truthful chart can show the two reported rates while marking comparability as unverified.

### Practice exercise

Calculate the reconstructed number of passes for each run, then assess: “The same 52 questions improved by 12 passes.”

> **Answer:** June gives `0.75 × 52 = 39`; July gives `0.9808 × 52 ≈ 51`, a difference of 12 reconstructed passes. The quoted sentence is too strong: the files do not establish that the same 52 questions or evaluator were used.

## 2. Weight categories by their sizes

The June snapshot reports `operations: 28.57%` over 7 prompts and `typo-tolerance: 75%` over 4. Those rounded percentages reconstruct approximately 2 and 3 passes. Averaging `28.57%` and `75%` gives `51.785%`, but this treats a seven-prompt category as if it had the same size as a four-prompt category. For their combined 11 prompts, use the reconstructed counts: `(2 + 3) / (7 + 4) = 5 / 11 ≈ 45.45%`.

To aggregate the whole snapshot, sum the category pass counts and category totals. The eleven June category totals sum to 52, and their reconstructed pass counts sum to 39. That agrees with the reported 75% overall rate. A chart should expose category sizes, especially when one category has only one or two questions. A 100% label over one question carries a different amount of evidence than 100% over thirteen.

| June 15 category | Reported rate | Total prompts | Reconstructed passes |
|---|---:|---:|---:|
| Operations | 28.57% | 7 | 2 |
| Typo tolerance | 75% | 4 | 3 |
| Both categories combined | **45.45%** | **11** | **5** |

“Reconstructed” matters: these counts are inferred from rounded percentages and small integer denominators, not copied from a raw pass-count field.

### Practice exercise

Someone puts the two category percentages in a bar chart, then labels their simple mean “combined pass rate.” Repair the label and calculation.

> **Answer:** Label each bar with its category total. For the combined rate, show `5/11 ≈ 45.45%`, derived from reconstructed passes. Do not use the unweighted mean of 51.785%.

## 3. A changing population can change the headline

The historical June and July files both list 52 prompts, but that count alone does not prove a fixed cohort. To see why composition matters, perform a **counterfactual exercise**, not a third GA observation: remove the seven June `operations` prompts and their two reconstructed passes from June's totals. The resulting subset is `37 / 45 ≈ 82.22%`, versus the original `39 / 52 = 75%`. No answer improved in this calculation. Only the population changed.

The purpose is not to recommend dropping hard prompts. It is to show how a dashboard can appear to improve when a difficult category disappears. A real QA trend should retain or disclose the prompt set, category mix, scoring rules, and excluded cases. If the system cannot provide those, the correct display is “reported rate changed; cohort comparability unknown,” followed by an investigation link.

### Practice exercise

Make a two-row table for the actual June run and the counterfactual subset. Which row may be plotted as a dated GA measurement?

> **Answer:** Actual June: 39 reconstructed passes / 52 prompts = 75%. Counterfactual subset: 37 reconstructed passes / 45 prompts ≈ 82.22%. Only the 52-prompt row is a reported GA measurement. Label the subset as a teaching calculation, with no run date or trend point.

## 4. Design the comparison claim

A useful GA quality view shows the rate and denominator together, provides the category mix, and links to the pinned snapshot. It should keep observation status separate from quality, as in [DV-001](dv-001-observed-degraded-stale-quality.md). Where prompt identities and evaluator revision are unavailable, a visible “comparability unverified” note prevents the line chart from silently asserting a controlled experiment.

For a stronger future comparison, record a stable prompt-corpus revision, evaluator revision, backend/model configuration, and the pass/fail result for each prompt. Then compare matched prompts, report additions and removals separately, and retain the original historical snapshots. A raw pass count is useful, but it cannot replace these identities.

### Practice exercise

Review this proposed headline: “GA quality gained 23.08 percentage points on the same test set.” Write a defensible replacement and name one next measurement.

> **Answer:** “Reported chatbot QA pass rate was 75% of 52 prompts on June 15 and 98.08% of 52 on July 19; test-set equivalence is unverified.” The arithmetic difference is 23.08 percentage points, but “same test set” needs a pinned prompt-corpus revision and prompt-level comparison.

## Key takeaways

- Show both numerator and denominator when the underlying record permits reconstruction.
- Combine categories by counts, not by an unweighted mean of their percentages.
- An unchanged total does not prove an unchanged test population.
- A counterfactual subset is an explanation tool, not a recorded QA result.
- A fair trend needs prompt identity and evaluator provenance as well as percentages.

## Further reading and project evidence

- GA [June 15 QA snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19 QA snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json), pinned to the same historical commit.
- [DV-001](dv-001-observed-degraded-stale-quality.md) for missing observations and carried-forward values.

*Research: `data-visualization-2026-10-11-002`. Subject review, learner exercise, localization, and public verification are pending.*
