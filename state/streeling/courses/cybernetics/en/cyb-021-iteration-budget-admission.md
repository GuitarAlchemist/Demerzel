---
module_id: cyb-021-iteration-budget-admission
department: cybernetics
course: "Governed loops: resource admission"
level: intermediate
prerequisites: [CYB-010, CYB-014]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Iteration Budgets: Admit the Next Action Before Executing It

> **Department of Cybernetics** | Intermediate | 40 minutes

A request to keep improving an artifact is not a resource contract. Three unsuccessful attempts may consume three attempts, even when they leave the artifact unchanged. Conversely, three cheap successes may fit a credit limit but exceed a deadline. This lesson turns a budget into an admission decision made before an action. All quantities below are synthetic teaching units: they are neither prices nor measured execution times.

## Objectives

- Calculate whether an action fits attempt, credit, and duration limits simultaneously.
- Locate and correct a check performed one action too late.
- Explain why failed attempts still consume the authorized attempt allowance.
- Produce a bounded stop receipt that distinguishes exhaustion from success.

## 1. Define the Unit Being Bounded

An iteration is one admitted action with a recorded outcome. A retry counts as another action. A diagnostic observation can be a separate operation with its own budget; calling every observation an iteration obscures cost. Write the unit, initial allowance, owner, and reset condition before execution. Otherwise a worker can rename a failed action a preparation step and silently extend its autonomy.

For our fixture, the limits are three actions, nine credits, and six duration units. Every candidate supplies a positive credit estimate and a positive worst-case duration estimate. These estimates are assumed correct and enforced by a single sequential caller. They are not predictions generated during execution. Parallel workers, inaccurate estimates, and actions that cannot be interrupted need additional reservation and enforcement mechanisms.

**Exercise.** A worker executes twice, fails both times, then says its count is still zero because no useful result exists. What count should the controller use?

**Worked correction.** The count is two. Attempts measure authorized resource use, not useful outcomes. There is one remaining action. Success is a different field; replenishment requires the budget owner's explicit rule, not the worker's interpretation of failure.

## 2. Calculate Admission as a Conjunction

Let the current counters be attempts `a`, credits `c`, and reserved duration `t`. Admit a candidate with estimates `p` and `d` only if `a + 1 <= 3`, `c + p <= 9`, and `t + d <= 6`. All three conditions must hold. Equality is allowed at a limit. A negative or zero estimate is invalid in this fixture because it could manufacture apparent spare capacity.

With four candidates each costing two credits and one duration unit, the states after admitted actions are `(1,2,1)`, `(2,4,2)`, and `(3,6,3)`. The fourth candidate is rejected by the attempt limit although credits and time remain. A separate sequence costing four credits per action admits two actions, then rejects the third at twelve credits. Duration estimates of four and four admit only the first action because eight exceeds six.

**Exercise.** Starting at `(2,8,4)`, test a candidate costing one credit and two duration units. Then test a candidate costing two credits and one duration unit.

**Worked correction.** The first reaches `(3,9,6)` and fits all boundaries. The second would reach `(3,10,5)` and fails the credit boundary. Using an average remaining allowance would wrongly authorize it. Unused duration cannot compensate for insufficient credits.

## 3. Reserve Before the Side Effect

Checking after execution detects a violation but does not prevent it. Reserve the attempt and its resource allowance before entering the action body. A failure can release unused reservations under a documented accounting rule, but it must not erase the fact that an attempt occurred. This fixture conservatively keeps every admitted estimate charged, so its accounting is easy to inspect.

Two concurrent workers can both read one remaining slot and both pass a local check. A production design would need one atomic check-and-reserve operation shared by both workers. The teaching script intentionally makes no concurrent safety claim. Likewise a duration estimate is not an actual timeout: a stuck operation needs an independent cancellation or containment mechanism. A correct admission calculation alone does not stop a hung process.

**Exercise.** A loop performs an action, increments the counter, and stops when the counter becomes greater than three. How many actions can run? Repair the ordering.

**Worked correction.** Four actions can run. Before action four, the count is three; the side effect occurs before the greater-than test. Test `a + 1 > cap` before execution, reject that candidate, and persist the reserved count before entering the action body. Merely changing the final message does not repair the fourth side effect.

## 4. Apply and Report the Boundary

Run the package fixture from any working directory, supplying its actual path:

```text
python <package>/overlay/scripts/course-exercises/cyb_governed_loops.py --json
```

Here `<package>` is a placeholder to replace, not executable shell syntax. The `CYB-021` record has test ID `budget_admission`. Its solution function is `budget_trace`: it rejects before modifying counters and reports every exceeded limit. Positive control: exactly three affordable candidates are admitted. Negative controls: a fourth candidate, excessive credit reservation, excessive duration reservation, and an invalid zero estimate are rejected. An implementation that checks only attempts misses the two resource counterexamples.

**Exercise.** Design the receipt after the fourth cheap candidate is denied. Is this task completed?

**Worked correction.** Record three admitted attempts, six credits, three duration units, and `attempt_cap` as the rejection reason. The receipt says budget exhausted. It says completed only if a separately specified output verifier passed. Remaining credits do not authorize a fourth action, and exhaustion does not prove the target is impossible.

[Offline solution and executable controls](../../../../../scripts/course-exercises/cyb_governed_loops.py): record `budget_admission`.

## Two-Stage Assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Conceptual stage, four points: calculate the two boundary examples correctly, explain failure accounting, and identify the post-action error. Require four correct answers before practical assessment; record a learner's explanation rather than inventing a confidence score. Behavioral stage, four points: run the fixture, preserve its result, change the second sequence to exceed credits on action two, and demonstrate rejection before that action. Require both controls and an accurate stop receipt. These are assessment instructions; no learner outcome has been observed.

## Key Takeaways

- Admit an action only when every declared budget fits.
- Failed actions consume attempts; reset rules require an owner.
- Exhaustion is a stop reason, not a successful output verifier.

## Journal, Proof, and Synthesis

Record initial allowances, estimates, admitted actions, failed actions, rejection reasons, script revision, and verifier outcome. Write what assumption would fail if duration estimates were too small. Summarize: admission proves the next modeled action fits the declared limits; it does not prove successful completion, accurate cost estimation, concurrency safety, or cancellation. Revise both the exercise code and this course if a counterexample contradicts that boundary.

## Further Reading and Overlap Boundary

CS-002 introduces the general governed-loop pattern; CYB-021 contributes multi-limit arithmetic and reservation counterexamples rather than repeating its six-property survey. CYB-010 covers observable stopping and CYB-014 capacity; this lesson covers authorization of individual actions. [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) supplies broader risk-management context, not our invented numerical limits. The existing Streeling two-stage assessment policy supplies the assessment structure. Translation and independent review remain pending.
