---
module_id: psy-003-review-throughput-and-compounding
department: psychohistory
course: Measure Recursive Improvement Across Review and Publication
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: psychohistory-2026-10-12-003
version: "0.1.0"
---

# Measure Recursive Improvement Across Review and Publication

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will distinguish measured work from a throughput hypothesis, calculate two queues through four weekly cycles, and define a falsifier for a proposed recursive improvement. **Project question:** if Streeling agents draft courses faster, will the project actually reach 25 useful, reviewed, public courses in each of 21 departments faster? The answer depends on every stage of the path, including human verdicts and public readback. More drafts alone cannot establish it.

[PSY-001](psy-001-intro-fractal-compounding.md) introduces a “fractal compounding” analogy. [PSY-002](psy-002-governance-phase-transitions.md) reads governance change as a phase transition, but calls its regime boundaries chosen rather than measured and warns that a variety ratio crossing 1.0 is not by itself a phase transition. Here we make the same discipline operational: a repeated improvement loop is a *candidate explanation* for rising throughput, not proof of exponential progress. Neither a power-law label nor an analogy to a physical conservation theorem establishes a measured delivery rate.

## 1. Start from an observed boundary

The pinned [review-candidate snapshot](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) reports **21** course directories, a provisional **525** core-course target, **113** distinct core codes, **114** authored English modules because one optional course lies beyond a department's first 25 codes, **nine** sources with all six active languages and at least five detectable exercise/answer pairs, and **four** committed review briefs. The progress reporter at this source revision recorded **zero approved production-review flags**. These are source and triage observations, not a count of human learning or published pages. The [generator](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_review_candidates.py) pins each listed source file to a Git blob and says explicitly that a file, answer signal, or brief is not an authenticated review.

`525 − 113 = 412` core codes remain on the provisional 21-directory basis. That arithmetic does not mean 113 courses are ready to teach: content accuracy, verifiable exercise quality, translation meaning, real learner outcome, integration, deployment, and anonymous readback are separate gates. It also does not resolve why the repository has 23 department records; [issue #1209](https://github.com/GuitarAlchemist/Demerzel/issues/1209) tracks the directory-versus-record scope. Use the denominator declared for an evaluation, and revisit it if the institution changes its department definition.

### Practice Exercise 1

Calculate the remaining core codes from the pinned source counts. Why can the inventory truthfully show 114 English modules but only 113 core codes? Why does zero approved production-review flags not mean zero authored content?

> **Answer:** `21 × 25 = 525`; `525 − 113 = 412` core codes remain. The authored count includes one optional course with a code outside its department's 001–025 sequence, so it does not increase the core target count. Review flags track a later pipeline stage; 114 English source files can exist while none has a recorded approved production-review flag. Even a positive flag would need human receipt verification before making a public quality claim.

## 2. Model the queues before promising a rate

The [scenario input](../../../fixtures/psychohistory/psy-003/scenarios.json), [simulator](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py), and [saved result](../../../fixtures/psychohistory/psy-003/results.json) form a **synthetic four-week teaching fixture**. Run `python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check` at the Demerzel root to reproduce it; the [fixture README](../../../fixtures/psychohistory/psy-003/README.md) lists its self-checks. It assumes **12 new review-ready items per week**, starting with empty review and publication queues. That assumption is deliberately separate from the nine *triage candidates* observed above: being a candidate does not make a course review-ready.

For each week, add new ready items to the review queue; accept no more than review capacity and available items; move accepted items to the publication queue; publish no more than publication capacity and available accepted items. The model assumes every completed review returns `approved` and every approved course is deployable. In reality a reviewer may request changes, a language review may remain pending, a build may fail, and a public readback may disagree. Thus model “accepted” and “published” are **optimistic upper bounds**, not current Streeling measurements.

```text
reviewed_t  = min(waiting_review_t + new_ready_t, review_capacity_t)
waiting_review_(t+1) = waiting_review_t + new_ready_t - reviewed_t
published_t = min(waiting_publication_t + reviewed_t, publication_capacity_t)
waiting_publication_(t+1) = waiting_publication_t + reviewed_t - published_t
```

The conservation checks are useful: over the four weeks, total new-ready items equal accepted items plus the final review queue; total accepted items equal published items plus the final publication queue. If a dashboard violates either identity without an explicit rejection or withdrawal count, the stage accounting is wrong. The model does **not** encode changes requested, rework, or distinct kinds of review. Those would need their own states before the tool could estimate real throughput.

### Practice Exercise 2

In the `flat` scenario, weekly accepted-review and publication capacities are both four. With 12 new ready items each week and empty initial queues, compute the review queue after each of four weeks, total accepted, total published, and the final publication queue.

> **Answer:** The review queue grows by eight per week: `8, 16, 24, 32`. Four items are optimistically accepted and four published each week, giving 16 accepted and 16 published in total. The final publication queue is zero. This is not observed performance; the synthetic arrival rate exceeds the fixed review capacity.

## 3. A faster middle stage can move the bottleneck

The second scenario sets accepted-review capacities to `4, 8, 16, 32` while publication capacity stays at four per week. That doubling is an **assumption about available human and operational capacity**, not a free benefit from adding agents. The realized accepted counts are `4, 8, 16, 20`: in week four only 20 items are available, the new arrivals included, so a capacity of 32 is partly idle. After four weeks, all 48 hypothetical new-ready items are accepted and the review queue is empty. Only 16 are published; **32 wait for publication**. If the real publication stage requires deployment approval, site build, and readback, more review automation alone cannot remove that queue.

This is the point of recursive improvement rather than a promise about its shape. A better term checker or review packet might reduce reviewer time. One must measure whether it increases accepted verdicts of equal quality, whether it shifts delay to language review or deployment, and whether published pages are actually correct. A tool that makes the middle stage appear fast while increasing downstream corrections has not compounded useful output. The [review-receipt draft](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json) would distinguish subject, language, and learner verdicts by exact source blob, but it remains in a draft PR awaiting human schema review.

### Practice Exercise 3

Use the `growing_review_fixed_publication` scenario. Give the realized accepted counts by week, the final accepted and published totals, and both final queues. Why is the fourth week's capacity of 32 not fully used?

> **Answer:** The realized accepted counts are `4, 8, 16, 20`. Totals are 48 accepted and 16 published. The review queue is zero and the publication queue holds 32. In week four, eight items were waiting and 12 new items arrived, so only 20 could be accepted; the remaining capacity of 12 had no input. The scenario does not prove that real people could or would approve at these rates.

## 4. Test a recursive improvement on the whole path

To test a real change, record a baseline window and intervention: which tool or practice changed, who used it, which courses and exact source blobs entered each queue, when they entered and left, and why items were rejected or returned. Track at least four distinct weekly outputs: new drafts with five answered exercises, completed **human** subject/language verdicts, accepted merges/deployments, and anonymously read-back public pages at the intended source revision. Also track rework rate and reviewer time. Keep the denominator fixed or report a scope change. Compare cohorts with similar course complexity and language requirements; otherwise an easy cohort can create a false improvement.

A proposed **semantic backpressure** rule can route scarce agent effort toward repairing evidence when a downstream stage is overloaded. For example, a large review queue may justify improving reviewer packets, translation parity, or answer clarity. A large publication queue may justify checking deployment, source lock, and readback. This is an allocation hypothesis, not an implemented Streeling scheduler or a reason to abandon the 412 remaining core courses. If the rule increases waiting time without increasing accepted, public, learner-usable courses, reject or revise it. A human gate cannot be self-approved by a faster model.

Define a falsifier *before* the intervention. One reasonable pilot could require a sustained rise in weekly courses with authenticated human verdicts **and** public readback, with no increase in correction rate or unresolved learner failures. If only authored drafts rise, or only a model's confidence rises, the intervention has not demonstrated end-to-end progress. If published pages rise while evidence or quality falls, the apparent gain is not the goal. Four weeks of the synthetic table cannot substitute for such a pilot.

### Practice Exercise 4

A team reports that its new agent workflow raised drafts from 12 to 24 per week, while verified human approvals remain four and public readbacks remain four. Name one leading metric that improved, one outcome metric that did not, and a falsifier for the claim that the workflow accelerated delivery.

> **Answer:** Draft creation improved from 12 to 24 per week. Verified public readbacks, an outcome closer to the requested goal, stayed at four; human approvals also stayed at four. A predeclared falsifier is that comparable cohorts show no sustained rise in authenticated approvals and correct public readbacks after the change, or that rework/learner failures increase. A larger draft queue alone does not demonstrate delivery acceleration.

### Practice Exercise 5

The synthetic growing-review scenario ends with 32 items waiting for publication. An agent proposes doubling course drafting again and calling the result “exponential Streeling progress.” What work should the team inspect first, what source identity must be preserved, and what would count as a real improvement?

> **Answer:** Inspect why accepted items are waiting: site-generation input, build and release gates, deployment capacity, and anonymous readback. Preserve each accepted course's exact Git source commit and blob through the generated page and public verification; do not let a later edit inherit an old verdict. A real improvement would raise the rate of correctly reviewed and publicly read-back courses without hiding quality or rework problems. Continuing independent course drafting can still be useful, but doubling drafts is not a fix for this publication queue.

## Sources, limits, and next check

The observed baseline is the [commit-bound review-candidate snapshot](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) and the [source progress reporter](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_course_progress.py). The numerical four-week outcomes are computed by the [fixture script](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py), not measured from an intervention. The model assumes immediate, successful reviews and publication and omits rework and variable course difficulty. No four-week operational experiment, human review of this lesson or of its French and Spanish translations, learner attempt, or public readback was performed. The next check is a bounded real pilot with exact-source receipts, comparable course cohorts, and an explicit public readback count.
