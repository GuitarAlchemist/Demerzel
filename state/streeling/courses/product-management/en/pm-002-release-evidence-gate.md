---
module_id: pm-002-release-evidence-gate
department: product-management
course: "A Release Evidence Gate for Streeling Courses"
level: beginner
prerequisites: [pm-001-shipping-vs-talking]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: product-management-2026-10-11-002
version: "0.1.0"
---

# A Release Evidence Gate for Streeling Courses

> **Department of Product and Project Management** | Level: Beginner | Estimated duration: 30 minutes | Status: English source draft; review and publication pending

## Objectives

After this lesson, you will be able to:

- Classify a Streeling module as authored, recorded, reviewed, locally built, or publicly readable using the artifact that proves each state.
- Name the missing evidence before making a release claim.
- Write a release note that gives a reader a reproducible path to the source and the deployed page.

## The project question

An agent writes a useful Streeling lesson in Demerzel. Another agent creates a JSON production record. Learn generates a page in a local build. May the team announce the course as reviewed and published? **No.** Those actions answer different questions. A source file proves that text was authored; a schema-valid record proves that required fields and types fit a schema; a local page proves that one generator/build run produced an output. None records a learner attempt or proves that an anonymous reader can fetch the deployed lesson.

This lesson uses the dated **DV-001 pilot** as a fixed case. The receipts are pinned to Demerzel pilot commit `6bc584d7ca1cd9eb1b1481e1100eeeb74e983863`, except the Learn generator, read at Learn commit `fe8e38444d882c28691dce9f12c21ac2ad404ec0`. They describe work observed on October 11, 2026, not the current public site. [PM-001](pm-001-shipping-vs-talking.md) asks whether a product claim is specific and falsifiable. Here the falsifier is a missing or failed release receipt.

### Practice exercise 1: classify the source

DV-001 has an English Markdown lesson and five answered exercises. The [production record](../../../course-productions/cp-data-visualization-2026-10-04-001.json) says `review.completed: false` and `publish.completed: false`. What can a release note safely say?

> **Answer:** “An English DV-001 source draft with five answered exercises exists in Demerzel.” It cannot say “reviewed” or “published.” Inspecting the source is necessary to judge its substance; the two false phase flags explicitly withhold those later claims.

## 1. One claim, one evidence owner

Use a gate card with the **claim**, **artifact**, **revision or date**, **result**, and **next owner**. The five rows below are separate decisions, not synonyms for “done.”

| Claim | Minimum evidence for this pilot | What the evidence does not establish |
|---|---|---|
| Authored source | Demerzel lesson path, module ID, source revision, answered exercise | Accuracy or learner usefulness |
| Production record conforms | JSON file validated against Demerzel's [`course-production` schema](../../../../../schemas/course-production.schema.json), with source/research IDs and honest phase flags | Whether the statements in the record happened |
| Reviewed | Recorded human subject verdict, fluent-language verdicts for required locales, and a learner attempt with corrections addressed | A deployed, reachable page |
| Learn integration | Sync output tied to a Demerzel source commit, `streeling.lock.json`, and successful site build with checked generated routes | Deployment or anonymous access |
| Public readback | After deployment, anonymous GET of the intended EN/FR/ES lesson and index routes, correct content and provenance | That the content was approved if review receipts are absent |

The [DV-001 review brief](../../../reviews/dv-001-review-brief.md) records an independent AI subject check and AI multilingual comparison but leaves human subject, fluent-language, and learner review open. The production record's `review.completed: false` matches that boundary. An AI check can narrow the queue without silently becoming the human review result. The [course curriculum rule](../../../../../docs/specs/streeling-project-curriculum-2026-10-04.md) also keeps ready, reviewed, and published counts separate.

### Practice exercise 2: read a valid record

Suppose a JSON validator accepts DV-001's production record. A teammate says, “The course passed production, so review is complete.” Which fields and missing receipt refute that conclusion?

> **Answer:** Schema acceptance covers the record's shape. The record says `status: review_pending`, `review.completed: false`, and `publish.completed: false`. The review brief has no completed human subject, fluent-language, or learner verdict. Validation cannot turn those false values into completed work.

## 2. Make review observable

Review requires a person and a result, not a checklist title. For subject accuracy, ask a reviewer to reproduce the dated claims and all exercise answers from the named source files. For localization, ask a fluent reviewer to check technical meaning and natural prose in each required language. For the learner gate, give a learner an answer-free task, capture their response, score it afterward, and record confusion and revisions. The [DV-001 review brief](../../../reviews/dv-001-review-brief.md) describes these tests; the brief itself is not a completed test. Its AI subject receipt approves only the bounded English fact check.

### Practice exercise 3: separate reviewers

DV-001 has six language drafts and an AI semantic comparison. A teammate proposes checking the “reviewed” box. Give the missing minimum receipts.

> **Answer:** Record human subject review of the English claims and answers, fluent review and verdict for each required locale, and an observed learner attempt using the answer-free task with corrections addressed. The existing drafts and AI checks do not supply those results; leave `review.completed` false until they exist.

## 3. Local Learn output is a preflight

At pinned Learn commit `fe8e384`, [`scripts/sync-streeling.mjs`](https://github.com/spareilleux/learn/blob/fe8e38444d882c28691dce9f12c21ac2ad404ec0/scripts/sync-streeling.mjs) reads Demerzel course files and writes generated EN/FR/ES pages and `streeling.lock.json`; it preserves journals. The [DV-001 preflight receipt](../../../reviews/dv-001-learn-preflight-2026-10-11.md) reports a successful sync and Astro build in an isolated Learn worktree, including generated DV-001 HTML in all three locales. It also reports missing journal entries and outstanding review. The lock pins the Demerzel input for that run, not a public deployment. A later source edit needs a new sync and build receipt.

### Practice exercise 4: evaluate the build

A release dashboard shows “Astro build: passed; DV-001 EN/FR/ES files exist under `dist/`.” Is “DV-001 is live” supported? Name the next verifiable check.

> **Answer:** No. These are local preflight outputs. After approved source is synchronized and deployed, request each intended lesson and index URL without credentials, check the returned content and source provenance, and record the result and time. A successful local build alone cannot establish public reachability.

## 4. Close the public loop without inflating the claim

The [October 11 public baseline](../../../reviews/public-baseline-2026-10-11.md) recorded 404 for the DV-001 EN, FR, and ES lesson routes while the local preflight produced their HTML files. The two observations are compatible: the preflight tested local output; the baseline tested the then-public site. The baseline also reports that the public index warned its AI-generated modules had not been reviewed or tested by the site author. Public presence would still not be a review verdict.

A practical release gate has a stop rule: if any required receipt is missing, write the strongest narrower claim and assign the missing gate to an owner. After deployment, repeat anonymous readback against the new public source commit; an October 11 result cannot certify a later deployment. Keep the review and public-readback dates beside the verdict so a future editor can see which version was checked.

### Practice exercise 5: write the release note

Write two sentences for the DV-001 pilot using only these receipts: six source-language drafts; bounded AI checks; no completed human or learner reviews; local EN/FR/ES build passed; October 11 public EN/FR/ES routes returned 404.

> **Answer:** “DV-001 has six language drafts and bounded AI checks; a local Learn sync and build generated its EN/FR/ES pages from pinned Demerzel source. Human subject, fluent-language, and learner reviews remain open, and anonymous requests to those three public routes returned 404 on October 11, 2026, so these receipts do not establish a reviewed or published course.”

## Key takeaways

- A release claim needs a receipt for its specific boundary; JSON conformance, review, build, and public access are different boundaries.
- State the source revision and observation date. A dated preflight is not a promise about today's site.
- When a gate is missing, publish the narrower truthful status and the next check, not a completed verdict.

## Project evidence and limits

- Demerzel pilot commit `6bc584d7ca1cd9eb1b1481e1100eeeb74e983863`: [DV-001 production record](../../../course-productions/cp-data-visualization-2026-10-04-001.json), [review brief](../../../reviews/dv-001-review-brief.md), [subject check](../../../reviews/dv-001-subject-review-2026-10-11.md), [local Learn preflight](../../../reviews/dv-001-learn-preflight-2026-10-11.md), and [public baseline](../../../reviews/public-baseline-2026-10-11.md). These are dated pilot receipts, not PM-002 review receipts.
- Learn commit `fe8e38444d882c28691dce9f12c21ac2ad404ec0`: [sync script](https://github.com/spareilleux/learn/blob/fe8e38444d882c28691dce9f12c21ac2ad404ec0/scripts/sync-streeling.mjs). The DV-001 preflight additionally used a local generator fix; its passing build does not certify this PM-002 draft.
- This lesson's five answers follow the pinned receipts. No PM-002 subject, fluent-language, or learner review, Learn sync/build, deployment, or anonymous public readback has been performed.
