---
module_id: dv-004-uncertainty-in-small-qa-suites
department: data-visualization
course: Uncertainty in Small QA Suites
level: beginner
prerequisites: [dv-002-denominators-and-test-populations]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-004
version: "0.1.0"
---

# Uncertainty in Small QA Suites

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 30 minutes | Status: review and localization pending

## Objectives

After this lesson, you will be able to:

- Calculate the percentage-point effect of one changed result in a suite or category.
- Show exact counts beside rounded percentages without claiming access to raw prompt results.
- Distinguish the resolution of a finite test suite from a statistical confidence interval.
- Specify evidence that would make a GA quality comparison repeatable.

## The project question

A GA dashboard displays a historical chatbot QA rate of 98.08%. How precise is that headline when the run contains 52 prompts, and what remains unknown even if its arithmetic is correct? Use the [June 15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) snapshots at pinned GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). These are historical teaching records, not today's service status.

Both files report `total_prompts: 52` and `degraded: false`. June reports `pass_pct: 75.0`; July reports `pass_pct: 98.08`. The overall pass counts are **reconstructed** as 39/52 and 51/52 from rounded percentages. The snapshots do not supply prompt identities, raw per-prompt verdicts, or an evaluator revision. [DV-002](dv-002-denominators-and-test-populations.md) explains why matching totals do not prove a matching test population.

### Practice exercise

Write a chart label for July that gives the number and its evidence limit in one line.

> **Answer:** “Historical GA chatbot QA, July 19: reported 98.08% of 52 prompts (about 51 passes reconstructed); prompt-level verdicts and evaluator revision are not in this snapshot.”

## 1. Show the step size behind the decimals

With 52 binary results, one changed result moves the overall rate by `100 / 52 ≈ 1.92` percentage points. A displayed rate with two decimal places can therefore look much smoother than the underlying steps. For July, `51 / 52 × 100 ≈ 98.08%`; one fewer pass would be `50 / 52 × 100 ≈ 96.15%`. Neither calculation predicts the next run. It only shows how a single verdict affects this fixed denominator.

The June and July reported rates differ by 23.08 percentage points, equivalent to twelve reconstructed passes if the denominator is held at 52. That is an arithmetic comparison, not proof that twelve particular prompts changed verdict. The snapshots lack prompt identities and scoring provenance.

### Practice exercise

If exactly one of June's 13 reconstructed failures became a pass **in a hypothetical fixed suite of 52 prompts**, what rate would the calculation produce? May it be plotted as a new GA run?

> **Answer:** `(39 + 1) / 52 × 100 ≈ 76.92%`, a rise of about 1.92 percentage points. This is a hypothetical sensitivity calculation; no new GA run was observed.

## 2. Small categories have larger steps

The July `operations` category reports 85.71% over seven prompts, consistent with six reconstructed passes. One changed verdict in that category moves its rate by `100 / 7 ≈ 14.29` percentage points. The `getting-started` category reports 100% over **one** prompt. A 100% badge over one prompt and a 100% badge over thirteen prompts (`modes`) have very different coverage, even though both bars end at the same place.

For a category chart, put the reconstructed fraction beside the percentage and sort or group by the actual comparison question. A useful label is “Operations: 6/7 reconstructed, 85.71% reported.” Do not call the category's seven prompts a random sample unless the test design establishes random sampling. A conventional confidence interval would answer a statistical sampling question whose assumptions these files do not document.

### Practice exercise

Compare one changed verdict in the overall suite, `operations`, and `getting-started`. Which headline is most sensitive to one verdict?

> **Answer:** The steps are about 1.92 percentage points for 52 prompts, 14.29 for seven, and 100 for one. The one-prompt `getting-started` category is most sensitive. These are exact denominator effects, not confidence intervals.

## 3. Separate three limits in the display

First, **rounding**: 98.08% is a rounded report; 51/52 is an inferred integer count rather than a stored overall pass count. Second, **coverage**: 52 prompts may omit other user needs, languages, or failure modes. Third, **comparability**: the two files give equal totals but not stable prompt IDs, expected answers, evaluator versions, or backend configuration. None of these limitations is fixed by adding decimal places or an unqualified error bar.

Use a main chart for the reported rate and a nearby table with date, denominator, category sizes, run status, and a “comparison basis unknown” note. Link the exact historical JSON. If the run is degraded or `pass_pct` is `null`, [DV-001](dv-001-observed-degraded-stale-quality.md) requires a gap, not a zero. If later evidence establishes matched prompts and repeated runs, then a separate analysis can quantify run-to-run variability; keep that measurement distinct from the one-verdict step size.

### Practice exercise

A dashboard says “98.08% ± 1.92% confidence” because one prompt is 1/52. Repair the claim.

> **Answer:** Show “98.08% of 52 prompts reported; about 51 passes reconstructed; one verdict changes this suite's rate by about 1.92 percentage points.” Do not label 1/52 as confidence: no sampling model or repeated-run variability was supplied.

## 4. Make the next comparison reproducible

A useful future QA record would retain a revision for the prompt corpus and evaluator, each prompt ID, its expected criterion, the verdict, backend/model configuration, and the timestamp. A comparison could then align the same IDs, list added and removed prompts separately, and show changed verdicts. Repeating an unchanged suite under recorded conditions would also reveal variability that a single snapshot cannot measure.

For the present historical pair, the strongest supported sentence is: “The reported rate rose from 75% of 52 on June 15 to 98.08% of 52 on July 19; prompt and evaluator equivalence are unverified.” That is useful evidence without inventing a causal explanation or a probability that the next run will pass.

### Practice exercise

Name two fields to add to a future GA record so “twelve prompts improved” can be tested. What must the comparison do with prompts present in only one run?

> **Answer:** Add a stable `prompt_id` and per-prompt `pass` verdict, plus a pinned evaluator revision to interpret the verdict. Compare matched IDs; report added or removed prompts as a separate cohort rather than counting them as changed answers.

## Key takeaways

- One verdict is about 1.92 percentage points in a 52-prompt suite, but 100 points in a one-prompt category.
- Exact denominators and reconstructed counts make the resolution of a rate visible.
- A one-verdict step is not a confidence interval.
- Equal prompt totals do not establish matched prompts, coverage, or scoring rules.
- A future matched comparison needs prompt IDs, verdicts, and evaluator provenance.

## Further reading and project evidence

- GA [historical June 15 snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19 snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json).
- [DV-002](dv-002-denominators-and-test-populations.md) for reconstructing counts and checking changing test populations.
- [DV-001](dv-001-observed-degraded-stale-quality.md) for unavailable observations.

*Research: `data-visualization-2026-10-11-004`. Subject review, learner exercise, localization, and public verification are pending.*
