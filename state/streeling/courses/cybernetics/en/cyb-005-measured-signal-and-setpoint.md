---
module_id: cyb-005-measured-signal-and-setpoint
department: cybernetics
course: "Feedback foundations"
level: beginner
prerequisites: ["CYB-004"]
estimated_duration: "35 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Measured Signal and Setpoint: Make Error Meaningful

> **Department of Cybernetics** | Beginner | 35 minutes

## Objectives

- Specify a measurement's quantity, scope, unit, phase, and observation time.
- Compute an error only after checking its compatibility with the setpoint.
- Reject wrong-scope, stale, future, and nonfinite observations.
- Separate proposed, authored, validated, indexed, and visible course counts.

## 1. Choose the quantity before choosing its target

A **setpoint** is a desired value for a defined quantity. A **measured signal** is an observation of that quantity. Their difference can guide action only when both mean the same thing. NI defines the process variable and setpoint in its controller documentation. [Primary reference: NI](https://www.ni.com/en/shop/labview/pid-theory-explained.html).

A goal of 25 courses per department looks simple until “course” is defined. A catalogue position describes an intention. A source page shows that material exists. An exercise receipt establishes a particular local check. An indexed page can be counted by a site, while a deployed visible page requires separate access evidence. These are related stages with different predicates. None is automatically equivalent to independently reviewed, teachable material.

Choose a predicate before arithmetic: “one distinct English module in this department with substantive sections, corrected exercises, and a passing local exercise receipt.” This is a local batch acceptance rule, not a replacement for Streeling's publication policy. Translations and independent review remain separate gates. Counting translated copies as new modules would change the unit halfway through the calculation.

### Practice exercise and worked correction

A department has three English source modules, twelve language files, 25 catalogue positions, and two visible website cards. Compute the deficit to 25 for source modules and for visible cards. Can you calculate the validated-course deficit?

**Correction:** Source deficit is 22; visible-card deficit is 23. The validated deficit is unknown until the acceptance predicate is applied. Twelve files do not establish twelve distinct courses. The difference between three sources and two cards motivates an indexing investigation before assuming the third source must be rewritten.

## 2. Define a measurement contract

Use five fields: `scope`, `phase`, `unit`, `value`, and `observed_at`. Scope identifies the department or controlled object. Phase states what predicate was evaluated. Unit prevents subtracting courses from milliseconds. Observation time identifies when the underlying fact was measured, not merely when a report was downloaded. A target carries the same scope, phase, and unit, plus its desired value.

For the synthetic fixture, target scope is `cybernetics`, phase is `authored_validated`, unit is `courses`, and value is 25. The matching observation is 3 at time 98; the decision occurs at time 100. Times are arbitrary monotonic seconds from a shared origin. Maximum permissible age is five seconds. The sample's age is two, so it can be used and error is `25-3 = 22`.

The phase label is synthetic. It does not certify that the three canonical source modules passed a new validation. A tutorial can test measurement logic without manufacturing evidence about the repository.

### Practice exercise and worked correction

Replace the observation's phase with `catalog_positions` and value with 575. A naive subtraction returns -550. What should the controller return instead?

**Correction:** Reject the incompatible phase before subtraction. An error of -550 would falsely suggest an excess of delivered courses. A large number and a valid integer type do not establish semantic compatibility. Preserve the rejected sample with its reason so the defect is diagnosable rather than silently replacing it with zero.

## 3. Freshness and validity are part of the signal

At decision time 100, an observation from 90 is ten seconds old and fails the fixture's age bound. A timestamp of 101 is in the future relative to the shared clock and also fails. Clock mismatch is a plausible explanation, but the sample cannot be treated as fresh merely because that explanation is convenient. If clocks differ, use a documented conversion or a same-clock elapsed-time measurement.

Reject `NaN`, a floating-point value that does not denote a finite number. Otherwise comparisons and arithmetic can propagate invalid results. A zero course count is valid when actually measured; absent evidence is not zero. This distinction changes action: zero may justify drafting all 25, while unknown calls for bounded inspection.

Freshness thresholds depend on the decision. Course sources usually change more slowly than active session state. Five seconds is intentionally a small teaching bound. Reusing it across every domain would be arbitrary. State the acceptable uncertainty and cost of acting on a stale value before selecting a threshold.

### Practice exercise and worked correction

Classify six changes to the fixture: different department, different phase, milliseconds instead of courses, time 90, time 101, and `NaN`. Which fail arithmetic and which fail the contract?

**Correction:** All six fail the contract. Wrong scope, phase, and unit are semantically incompatible; past and future times fail freshness; `NaN` fails numeric validity. Most would still permit syntactic subtraction in a loosely typed program. The key lesson is that mathematical executability is weaker than evidential validity.

## 4. Connect the signal to a bounded code decision

Run `python <overlay>/scripts/course-exercises/cyb_foundations.py --json`; inspect `signal-contract`. Function `contract_error` validates matching fields, checks `0 <= now-observed_at <= max_age`, checks a finite observation, and only then subtracts. Six deliberate invalid samples must raise `ValueError`. The positive control must return 22. The fixture also records the naive catalogue calculation as a rejected interpretation.

An application can use a valid positive deficit to propose a bounded drafting batch. It still needs scope authorization and a resource budget. A valid negative error does not authorize deleting courses: it means the chosen quantity exceeds its setpoint. Counting should inform decisions rather than silently becoming a destructive command.

In the verified offline routing incident, caller B could receive a browser route to A. The measurement contract explains the risk: a plausible value from the wrong scope cannot close B's loop. That incident is evidence for identity checks, not proof that every measurement channel is defective.

### Practice exercise and worked correction

Add a source revision field. A target expects revision `r2`, but an observation describes `r1`. Decide whether to convert, reject, or subtract directly, and explain your test.

**Correction:** For a revision-specific criterion, reject by default. A documented migration may permit conversion, but test that mapping explicitly. Add one matching-revision positive control and one old-revision negative control. Direct subtraction hides a semantic change even if the numerical values happen to agree.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 5 points:** one each for defining the quantity, separating stages, correct deficit arithmetic, freshness reasoning, and unknown-versus-zero distinction. Require 4 points and no catalogue-as-delivery claim. Capture a learner's prior belief, then ask them to explain the changed belief; a score is not an invented confidence value.

**Behavioral, 4 points:** on synthetic records, the learner builds a compatible pair, rejects wrong scope, rejects stale data, and retains an actionable rejection reason. Require all four observed behaviors. Fixture success alone is author evidence, not learner assessment.

## Journal, proof, and synthesis

Record the quantity predicate, scope, unit, source revision, observation time, decision time, error or rejection, and resulting bounded action. Link the JSON test receipt and script hash. Summarize which counts can legitimately be compared and which require new evidence. CYB-002 introduces target and measured state; this lesson operationalizes their compatibility. CYB-003 concerns distinguishable states and variety rather than count provenance. The fixture verifies contract cases under a shared-clock assumption; it does not validate deployed counters or certify existing course quality. Independent review and translations remain pending.

## Further reading

- [CYB-002: Active Dampening](cyb-002-active-dampening-cross-repo-oscillation.md), preserved survey of measured state and correction.
- [NI: process variable and setpoint](https://www.ni.com/en/shop/labview/pid-theory-explained.html), verified 2026-10-07. The provenance contract and counts here are local teaching constructions.

*Local authored draft; provisional integration ID. No Seldon research cycle or publication claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_foundations.py).
