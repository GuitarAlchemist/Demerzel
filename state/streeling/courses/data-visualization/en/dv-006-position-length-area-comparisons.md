---
module_id: dv-006-position-length-area-comparisons
department: data-visualization
course: Position, Length, Area, and the Comparison Task
level: beginner
prerequisites: [dv-002-denominators-and-test-populations, dv-003-instrument-cohorts-and-units]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-006
version: "0.1.0"
---

# Position, Length, Area, and the Comparison Task

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 30 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Name the comparison and unit before choosing a visual encoding.
- Use a shared position scale or a common-origin length for quantitative comparisons.
- Explain why a circle's **area**, not its radius, must represent a count if circles are used.
- Keep historical dates, denominators, and comparability limits visible beside a chart.

## The project question

GA has three historical snapshots at pinned commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). The [July 23, 2026 voicing-analysis snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/voicing-analysis/2026-07-23.json) counts **297,910 guitar**, **7,795 bass**, and **7,342 ukulele** voicings, totaling **313,047**. The [June 15](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) and [July 19](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) chatbot QA snapshots report **75% of 52 prompts** and **98.08% of 52 prompts**. These are different comparison tasks: compare *counts across instruments* and compare *reported rates across dates*. A single collection of circles would make both look like “bigger versus smaller” while obscuring their units.

Decide what the reader needs to judge. For the voicing corpus, the question is “How large is each instrument cohort, and how much smaller are bass and ukulele than guitar?” For QA, the question is “What reported rate belongs to each date?” The QA files do not identify individual prompts or evaluator revisions, so the rate difference cannot establish improvement on a matched test set. Neither record describes current service or user experience.

### Practice exercise 1: name the task

A designer proposes one bubble chart with five bubbles: three instrument counts and two QA percentages. Name two problems, then write the two comparison questions with their units.

> **Answer:** The bubbles mix voicing counts with percentages, which have different units; circle area also makes close comparisons harder to read than a shared numeric scale. Compare **voicings per instrument** for guitar, bass, and ukulele in the July 23 audit. Separately compare **reported percent of 52 QA prompts passing** on June 15 and July 19. The latter is a dated descriptive comparison, not a matched-prompt improvement claim.

## 1. Position on a shared scale

For close values, put marks at their numeric positions on one labeled scale. A dot plot of the two QA rates can place dots at 75 and 98.08 on a 0–100% axis. The horizontal distance represents **23.08 percentage points**. If a detailed view starts at 70%, label that axis and the omitted range plainly; a zoomed position scale can help inspect the gap, but it must not turn the values into bar lengths measured from 70.

Show `June 15: 75% (52 prompts)` and `July 19: 98.08% (52 prompts)` as direct labels. The unchanged denominator does not prove unchanged questions. [DV-002](dv-002-denominators-and-test-populations.md) works through the missing matched-population evidence. Do not draw an unqualified “quality improved” arrow between the two dots.

### Practice exercise 2: read the axis

A QA dot plot places 75 and 98.08 on a shared percentage axis. Calculate their difference in percentage points. What would a 70–100% detail axis require in its caption, and what conclusion would still be unavailable?

> **Answer:** `98.08 - 75 = 23.08` percentage points. The caption must say that the displayed position axis begins at 70% and show both values and dates; otherwise the visual distance can be mistaken for a full 0–100% range. The records do not establish that the same prompts and evaluator produced both rates, so a matched-test improvement conclusion remains unavailable.

## 2. Length from a common origin

When the reader needs to compare cohort sizes, horizontal bars can encode counts by length. Start each at **zero**, use one linear scale, and print the exact count at its end. On a layout where the guitar bar is 100 units long, the bass bar should be about **2.62** units and the ukulele bar about **2.46** units. Those small lengths are an honest consequence of the corpus imbalance, not a layout bug. Provide a table or a close-up of the two smaller groups if the reader also needs to distinguish 7,795 from 7,342; keep the original overview and clearly label any close-up scale.

Guitar has about **38.22 times** as many audited voicings as bass (`297,910 / 7,795`). A bar cut off at 7,000 would encode bass as only 795 visible units and ukulele as 342, falsely magnifying their difference. If a zero-origin chart becomes unwieldy, use a labeled dot plot or separate overview and detail panels instead of hiding the baseline. [DV-003](dv-003-instrument-cohorts-and-units.md) explains why these corpus sizes do not measure per-instrument musical correctness.

### Practice exercise 3: check bar geometry

With guitar's 297,910-count bar drawn at 100 units, calculate the bass and ukulele bar lengths to two decimals. Should the chart shorten both bars by subtracting 7,000 before drawing them?

> **Answer:** Bass is `100 × 7,795 / 297,910 = 2.62` units; ukulele is `100 × 7,342 / 297,910 = 2.46` units. No. Subtracting 7,000 from the lengths would change what the bars encode. Keep zero-origin lengths and exact labels; use an explicitly labeled detail view if the 453-voicing bass–ukulele difference is the task.

## 3. Area is a different encoding

Circles can carry counts when their **areas** are proportional to the values. A circle's area is `π × radius²`. For the guitar and bass counts, the desired area ratio is `297,910 / 7,795 ≈ 38.22`; therefore their radius ratio must be `√38.22 ≈ 6.18`. If someone makes the guitar radius 38.22 times the bass radius, its area becomes about **1,460.62 times** the bass area. That geometry greatly exaggerates the recorded count ratio.

Even correctly sized circles demand more mental estimation than comparing marks on a shared scale. Reserve them for a task where a rough magnitude or spatial placement matters, keep exact numbers nearby, and supply an accessible table. Avoid sizing circles with the QA percentages alongside voicing counts: an area ratio across unlike units has no useful interpretation.

### Practice exercise 4: test the bubbles

A draft sizes the guitar and bass circle **radii** in the ratio 38.22:1 and labels the result “38.22 times as many voicings.” What area ratio would viewers see? What radius ratio would preserve the count ratio?

> **Answer:** Area grows with the square of radius, so `38.22² ≈ 1,461:1` (about 1,460.62 using the unrounded count ratio). To show approximately 38.22:1 by area, use a radius ratio of `√38.22 ≈ 6.18:1`. A common-scale bar chart is easier to audit for this exact cohort comparison.

## 4. Review the comparison, then the claim

A compact GA panel can show three zero-origin count bars with exact labels, a separate dated two-dot QA display, and a small source table. Put **voicings** beside the first scale and **percent of 52 prompts** beside the second. State that all values are from historical snapshots at the pinned revision. The voicing count is an audited corpus size, not a user population; the QA rates are run summaries with unverified prompt and evaluator matching. The panel should link each number to its source and remain readable without color.

Before approving a chart, ask: Are the values the same unit? Is the visual geometry proportional to the intended quantity? Does the scale suit the comparison task? Does the caption state the observation dates and the evidence boundary? A visually clear chart can still support a false claim if its caption confuses corpus share, naming quality, and QA pass rate.

### Practice exercise 5: repair a dashboard caption

Review: “GA quality grew from 75% to 98.08%; guitar is 38 times better than bass, as the large bubble shows.” Replace it with a two-sentence caption that preserves the two tasks, dates, denominators, and strongest limits.

> **Answer:** “At GA revision `dc2e74c`, the July 23, 2026 voicing audit counted 297,910 guitar, 7,795 bass, and 7,342 ukulele voicings; these are corpus sizes, not instrument quality scores. Separate chatbot QA snapshots reported 75% of 52 prompts on June 15 and 98.08% of 52 on July 19, but the files do not establish matched prompt identities or evaluator revisions, so the difference is descriptive rather than a verified improvement.”

## Key takeaways

- Choose the encoding from the comparison task and unit: shared position for precise rates, common-origin length for counts, area only when rough magnitude suits the task.
- A bar's length needs a shared zero; a dot's position may use an explicitly labeled detail scale.
- For circles, value proportional to **area** means radius proportional to the square root of value.
- Print dates, counts, denominators, and source links so the visible comparison does not overstate the evidence.

## Project evidence and limits

- Pinned GA [July 23 voicing audit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/voicing-analysis/2026-07-23.json), [June 15 QA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json), and [July 19 QA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) snapshots supply the example values. Length and radius examples are teaching calculations from those fields, not emitted GA measurements.
- The snapshots do not establish representative users, independently reviewed voicing quality, matched QA prompts, or the QA evaluator revision. This lesson has not had human subject review, a learner attempt, localization, or public Learn readback.

*Research: `data-visualization-2026-10-11-006`. English draft only; review and publication pending.*
