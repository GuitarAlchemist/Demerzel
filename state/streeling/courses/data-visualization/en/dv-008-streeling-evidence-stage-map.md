---
module_id: dv-008-streeling-evidence-stage-map
department: data-visualization
course: Visualize Streeling Source, Review, and Public Readback
level: intermediate
prerequisites: [dv-001-observed-degraded-stale-quality, dv-002-denominators-and-test-populations]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-21-008
version: "0.1.0"
---

# Visualize Streeling Source, Review, and Public Readback

> **Department of Data Visualization** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; human and learner review pending

## Objectives

After this lesson, you will be able to:

- Draw separate evidence lanes for an authored course, an approved review, and an anonymous public readback.
- State the denominator and source revision of each count without turning an unmeasured public stage into zero.
- Show when a public page and a review exist but do not refer to the same source revision.
- Reproduce a small synthetic evidence matrix and challenge a misleading completion chart.

## The project question

The Streeling goal is 25 project-useful, reviewed, publicly readable courses in each of 21 course-bearing departments: **525 distinct core course codes**. A coordinator asks, “How many courses are done?” A single progress bar would conceal three different observations. Demerzel holds the authored Markdown and production records; a human review must approve the relevant content; Learn must serve the exact source anonymously. These are separate claims with separate evidence.

At pinned Demerzel revision [`8a37e1d`](https://github.com/GuitarAlchemist/Demerzel/tree/8a37e1d9a728a15ed384cbb912e3c8c518083d12/state/streeling), [`streeling_course_progress.py`](https://github.com/GuitarAlchemist/Demerzel/blob/8a37e1d9a728a15ed384cbb912e3c8c518083d12/scripts/streeling_course_progress.py) reports **120 core course codes**, **121 English source files**, and **zero production records marked review approved**. The extra English file is optional CYB-026, outside the first 25 core numbers. The script scans repository state; it does **not** query the public Learn site or establish subject quality. Those counts describe that revision, not today's catalog.

The separate [`streeling_public_readback.py`](https://github.com/GuitarAlchemist/Demerzel/blob/8a37e1d9a728a15ed384cbb912e3c8c518083d12/scripts/streeling_public_readback.py) accepts a full Demerzel SHA and module IDs. It fetches the Streeling index and module pages anonymously, then checks HTTP 200, an exact source link, and the rendered heading. Its result covers only the requested pages and revision; it does not certify human review or learning. Because the pinned progress report contains no exhaustive public readback, the **public count is unknown** at this evidence boundary. Do not draw it as zero.

### Practice exercise 1: label the baseline

At the pinned revision, should the chart headline read “121 of 525 complete,” “120 of 525 authored,” or “zero courses published”? Give the most defensible headline and one subtitle.

> **Answer:** “120 of 525 core course codes have English source drafts at Demerzel revision `8a37e1d`.” The 121st English file is optional CYB-026. A subtitle should say “0 approved in the production records scanned at that revision; exact public count not measured by this report.” Neither an English file nor an absent public measurement proves completion.

## 1. Make the evidence lanes explicit

Use one row per course code and three aligned columns. **Source** means an English file with a distinct core code; **review** means an applicable human verdict on that exact course version; **public** means a successful anonymous readback against the same source SHA. A production-record boolean is a useful inventory signal, but the reviewer, verdict, and content blob must also be inspected before claiming a valid human review. An HTTP 200 alone says only that some page responded.

The local [synthetic cards](../../../fixtures/data-visualization/dv-008/evidence-cards.json) and [evaluator](../../../../../scripts/streeling_fixtures/data-visualization/dv-008/evaluate_cards.py) let you rehearse this layout. Run from the Demerzel repository root:

```text
python scripts/streeling_fixtures/data-visualization/dv-008/evaluate_cards.py
```

The six cards are invented classroom states, **not observed Streeling modules**. All have authored source. Cards A and B have review approval. A and F have an exact public readback. Only A satisfies all three gates. F deliberately has exact public provenance but no approved review; B has approval but a public 404. C has a public 200 with a matching heading but stale index and module source links. E has a matching module source and heading while the index still cites another revision. These exceptions show why the columns must remain visible. A funnel alone would suggest every later stage is a subset of every earlier one; that is not guaranteed by the evidence.

| Card | Authored | Review approved | Exact public | All three |
|---|---|---|---|---|
| A | Yes | Yes | Yes | Yes |
| B | Yes | Yes | No: 404 | No |
| C | Yes | No | No: stale links | No |
| D | Yes | No | No: 404 | No |
| E | Yes | No | No: stale index | No |
| F | Yes | No | Yes | No |

### Practice exercise 2: count the classroom cards

Run the evaluator. Give the four counts: authored, review approved, exact public, and all three. Which card disproves the claim that public provenance implies approved review?

> **Answer:** The synthetic counts are **6, 2, 2, and 1**. F has an exact public readback but no approved review. B shows the converse: approval does not imply a public page. The counts are properties of the invented cards, not six real Streeling courses.

## 2. Draw unknown and stale states honestly

For a fixed source revision, a useful status grid uses **yes**, **no**, and **not measured** with words or symbols in every cell. The public lane needs a fourth explanation when a page exists but links to an older source. A 200 response with the right title is not an exact-source readback; a generated preview in a local `dist/` directory is also not anonymous deployment evidence. Label the timestamp of a public probe, because a passing readback can become stale after the next deployment. This follows [DV-001](dv-001-observed-degraded-stale-quality.md): missing observations and historical observations are not current zeroes.

For the pinned progress snapshot, a compact display could read:

```text
Core source drafts     120 / 525   observed at Demerzel 8a37e1d
Approved review         0 / 120   production-record signal at that revision
Exact public readback   ? / 120   not exhaustively measured by this report
All gates               ? / 525   cannot be certified from these inputs
```

This is **not** a single conversion funnel. A reviewed count may use all authored modules as its denominator for review throughput, while final completion uses 525 core targets. An exhaustive public sweep, exact-source comparison, and receipt validation could later establish the remaining numbers. Until then, preserve question marks. In a dashboard, show the relevant source SHA, readback timestamp, the course code, and direct links to evidence in an accessible table; do not encode state by color alone.

### Practice exercise 3: repair the chart

A release dashboard displays three equal-width bars labeled “Drafts 120; Reviewed 0; Published 0” and calls this “120 completed courses.” Identify two evidence errors and replace its public label.

> **Answer:** The 120 are authored core drafts, not completed reviewed and public courses. The pinned progress script did not measure all public pages, so “Published 0” invents a result; use “Exact public readback: not measured for the whole set.” A further issue is that equal bar widths would hide the different counts and denominators. State the pinned revision and show 0 as the production-record review signal, pending receipt validation.

## 3. Test the exact-source join

The public script requires the index to link to `tree/<sha>/state/streeling/courses` and each module page to link to `blob/<sha>/<course path>`, plus a heading match and HTTP 200. Its checks are deliberately narrow: they establish anonymous page provenance and a rendered title for the requested SHA. They do not compare every paragraph or exercise to the source, and they do not inspect review. A human review tied to a different course blob must be revisited after edits. This is a join on exact version, not a count of favorable labels.

The classroom evaluator models the readback's four booleans but performs no HTTP request. It uses a small matrix so the reasoning is reproducible without network access. For a live module, run the real public script **after** the source SHA is committed, reachable and deployed. Read its JSON result and independently check the review receipt's source identity. Do not copy a synthetic “A passed” result into a production record.

### Practice exercise 4: diagnose a partial match

Card E returns HTTP 200, the module source link and heading match the target, but the index source link does not. Should the card be counted in exact public readback? Name the next check for a real Streeling deployment.

> **Answer:** No. The pinned readback contract requires both index and module provenance. In a real deployment, inspect the index's source link and deployed generator revision, sync the intended Demerzel SHA into Learn, deploy, then repeat anonymous readback. Do not infer that the entire site is at the target revision from one matching module page.

## 4. Make the next action visible

The grid should lead to work, not just decorate a report. For a draft without review, give the subject reviewer an answer-free learner task and source-bound review brief. For a reviewed course without exact public readback, check the Learn sync and deployment. For an exact public page without review, finish the review before claiming completion. If a source file changes after approval, compare its new blob to the reviewed blob and seek a new verdict when the change affects reviewed content. These actions arise from each row's missing evidence, not from a generic “percentage complete.”

Do not turn `pipeline_review_approved` into a human verdict without inspecting its underlying receipt. Do not equate a local Learn preview with a public page. Finally, remember the goal's “project-useful” and “verifiable exercises” terms: the three-stage map is necessary for publishing discipline but does not itself prove the lesson is accurate, useful to a GA/IX/Demerzel/Learn user, or successful for a learner.

### Practice exercise 5: decide what to report

Suppose a newly written DV-008 draft passes local preflight and Learn can render it locally, but no human has reviewed it and no anonymous URL has been probed. Write a one-sentence status and two next evidence-producing actions.

> **Answer:** “DV-008 is an English source draft with local consistency and preview evidence; human review and exact public readback are pending.” Give a reviewer the answer-free task and exact source blob for a recorded verdict, then sync and deploy that reviewed SHA through Learn and run anonymous readback against the module and index. A local preview is neither a human review nor a public observation.

## Key takeaways

- A source draft, approved review, and exact public page answer different questions.
- Public provenance and human approval can occur in either order; count their intersection for completion.
- Zero is an observed count; unknown means the relevant measurement was not made.
- Pin source SHA, course blob, review receipt, and readback time before combining evidence.
- A status chart remains a navigation aid; learner success and project usefulness need separate tests.

## Project evidence and limits

- Pinned Demerzel [`streeling_course_progress.py`](https://github.com/GuitarAlchemist/Demerzel/blob/8a37e1d9a728a15ed384cbb912e3c8c518083d12/scripts/streeling_course_progress.py) and [`streeling_public_readback.py`](https://github.com/GuitarAlchemist/Demerzel/blob/8a37e1d9a728a15ed384cbb912e3c8c518083d12/scripts/streeling_public_readback.py) define the two measured scopes. The progress count was reproduced at that revision; a complete public sweep was not.
- The [six-card fixture](../../../fixtures/data-visualization/dv-008/evidence-cards.json) is synthetic. Its 6/2/2/1 results do not estimate real publication rates.
- The course is an English draft only. No human subject verdict, learner attempt, localization review, Learn deployment, or anonymous DV-008 readback is claimed.

*Research: `data-visualization-2026-10-21-008`. Review and publication pending.*
