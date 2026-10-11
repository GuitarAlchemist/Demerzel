---
module_id: cyb-003-measuring-variety-ratio-quantitatively
department: cybernetics
course: Measuring Requisite Variety Without Inventing Capacity
level: intermediate
prerequisites: [cyb-001-vsm-ai-governance-mapping, cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: cybernetics-2026-03-23-002
version: "0.2.0"
---

# Measuring Requisite Variety Without Inventing Capacity

> **Department of Cybernetics** | Level: Intermediate | Duration: 35 minutes | Status: subject and localization review pending

## Objectives

After this lesson, you can:

- distinguish a schema's possible labels from states observed in a sample and from effective regulatory responses;
- calculate a finite alphabet's maximum variety and a sample's empirical entropy without treating either as governance quality;
- explain why counts of policies, personas, and grammar productions cannot be divided into a meaningful “variety ratio”;
- design a matched disturbance → response → outcome experiment for Demerzel.

## The project question

The first CYB-003 draft reported “healthy” behavioral and regulatory ratios and a “3-bit regulatory gap” by adding logarithms of file counts, thresholds, and presumed policy interactions. Those numbers did not count distinguishable disturbances and effective responses under a defined task. Its healthy ranges had no measured outcome basis. **Withdraw those conclusions.** The calculations below use real project records but stop before claiming operational capacity.

The pinned example is Demerzel revision [`66083fc`](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f). Read the [course-production schema](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) and the [eight production records](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions). The [replay script](../../../fixtures/cybernetics/cyb-003/README.md) checks the counts in a checkout containing those records. This historical snapshot is not today's pipeline status.

## 1. Specify the set before counting

Ashby's variety concerns distinguishable states of a **specified set**. If all `N` states are possible, its maximum variety is `log2(N)` bits. The choice of set and the distinctions the observer can actually make matter. A schema lists *allowed symbols*; it does not show how often each symbol occurs, whether every combination can occur, or whether a controller can handle a disturbance. Ashby's [original text](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf) separates possible states, observed states, and regulation.

At the pinned revision, the schema permits five `status` labels: `in_progress`, `review_pending`, `published`, `rejected`, and `failed`. It also permits three `review.verdict` labels: `approved`, `revise`, and `reject`. A verdict is optional in the schema and absent from all eight sampled records. Seven records have status `in_progress`; one has `review_pending`.

| Question | Answer from the pinned source | What it does **not** establish |
|---|---:|---|
| How many status labels are configured? | 5 | Five exercised behaviors |
| How many status labels occur in these records? | 2 | The full operating range |
| How many records were sampled? | 8 | A representative time series |
| How many sampled records have a review verdict? | 0 | Reviewer capacity or quality |

### Practice exercise 1

Calculate the maximum variety for the configured status alphabet and for the two status labels seen in this sample. Can either number be called Demerzel's regulatory capacity?

> **Answer:** `log2(5) ≈ 2.322` bits for the configured alphabet; `log2(2) = 1` bit for the two observed labels. Neither measures regulatory capacity. They count labels, not distinct, effective responses to specified disturbances.

## 2. A sample distribution answers a different question

Shannon's entropy of a sampled symbol distribution is `H = -Σ p(x) log2 p(x)`. For the eight pinned records, status frequencies are `7/8` and `1/8`, so `H ≈ 0.544` bits per sampled status. This is a descriptive statistic of this small, selected set of course-production records, not an estimate of future agent behavior. The formula comes from Shannon's [original paper](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).

The configured status alphabet, observed alphabet, and empirical entropy are different measurements. Do not sum the variety of “five statuses” with “three verdicts”: the verdict can be missing, the phases constrain which combinations make sense, and no independence has been demonstrated. The arithmetic `log2(5 × 3) ≈ 3.907` is a **hypothetical Cartesian-product upper bound**, not 15 reachable pipeline states.

### Practice exercise 2

Recompute the empirical entropy from the table, then explain why `log2(8) = 3` bits is the wrong answer.

> **Answer:** `-(7/8)log2(7/8) -(1/8)log2(1/8) ≈ 0.544` bits. Eight is the number of records, not the number of distinct status outcomes. `log2(8)` measures the capacity to identify one of eight records if record identity is the defined variable; that is a different question.

### Practice exercise 3

A dashboard multiplies five statuses by three review verdicts, labels the result “15 regulator responses,” and marks 3.907 bits as proof of adequate governance. Identify two unsupported steps.

> **Answer:** It assumes all status/verdict combinations are valid and reachable, even though verdict is optional and phase constraints matter. It also substitutes schema symbols for tested responses to disturbances; no disturbance, chosen action, or outcome was measured.

## 3. Measure an actual regulation task

For a useful requisite-variety test, define the **disturbance** (what went wrong), the **response** (what the controller did), and an **essential outcome** (what must stay within bounds). For course production, a proposed test could present three distinct failures: an absent fixture, an unreadable evidence source, and an exercise whose answer is inconsistent with its fixture. The system could repair the fixture, request access, or revise the answer, then emit a receipt. These are **proposed test cases**, not observations of current Demerzel behavior.

Before running the test, record the input fixture, expected distinction, permitted action, time limit, and pass rule. Run each case and preserve the resulting decision and outcome. A generic “retry” response to all three cases exposes a missing distinction, even if the controller has many policy files. Conversely, three different labels do not help if they all produce the same broken artifact. Count *effective distinctions under the task*, not nouns in the repository.

| Proposed disturbance | Distinguishing evidence | Candidate response | Checkable outcome |
|---|---|---|---|
| Fixture absent | Declared file path does not exist | Repair or block with exact missing path | Receipt identifies missing fixture; no invented result |
| Source unreadable | Read attempt fails | Request access or use an explicitly allowed source | Receipt names the failed read and scope |
| Answer inconsistent | Recomputed result differs | Revise answer, then replay exercise | New answer matches the fixed fixture |

The table is an experiment design. It cannot establish a `response/disturbance` ratio until there are matched runs with outcomes. Even then, a ratio of entropy values alone would ignore which response works for which disturbance. Report the confusion matrix and task success alongside any information measure.

### Practice exercise 4

An agent sees an unreadable source but writes “review approved” after silently skipping it. Which fields must a replay receipt expose, and is this a successful regulation?

> **Answer:** Record the declared source and revision, attempted read, error, fallback if authorized, chosen action, and final outcome. Without the evidence, approval is unsupported; the safe outcome is blocked or review pending, not success.

### Practice exercise 5

Design a falsifier for the claim “adding a fourth governance policy improved course-review regulation.”

> **Answer:** Hold the disturbance fixtures and pass rule fixed, then compare review decisions and independently checked outcomes before and after the policy. If the new policy does not reduce unsupported approvals or unresolved cases, or increases them, this test does not support the improvement claim. Record preparation and review time too: extra policy text can add cost without improving decisions.

## 4. What to report next

A useful dashboard would show the configured state alphabet, observed state frequencies, missing verdicts, and matched disturbance outcomes **separately**. It would show the repository revision and sample selection. It would not assert “healthy” ranges for a ratio that has not been validated against user or governance outcomes. To test recurring improvement, repeat the same disturbance suite across revisions and track independently checked success, unresolved cases, and end-to-end effort. A shorter loop is only better if it reaches more correct decisions without shifting work into an invisible review queue.

This also connects to [CS-004's controlled agentic audio loop](../../../fixtures/computer-science/cs-004/recursive-improvement-evidence.json): failed source reads and an insensitive comparator became explicit harness and evaluation changes. Those few observed cycles support local learning, not an exponential-progress claim.

## Sources and limits

- [Demerzel course-production schema](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) and [pinned records](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions); counts checked by the [local replay fixture](../../../fixtures/cybernetics/cyb-003/README.md).
- W. Ross Ashby, [*An Introduction to Cybernetics*](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf), chapters 7 and 11; C. E. Shannon, [*A Mathematical Theory of Communication*](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).
- The eight records are a historical, selected sample. No disturbance/response/outcome log or human learner result was available for this lesson. Subject and localization review remain open.
