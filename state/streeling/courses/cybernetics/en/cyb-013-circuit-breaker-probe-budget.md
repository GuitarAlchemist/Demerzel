---
module_id: cyb-013-circuit-breaker-probe-budget
department: cybernetics
course: "Circuit Breakers and a Bounded Recovery Probe"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Circuit Breakers and a Bounded Recovery Probe

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration ID; translations and review pending

## Objectives

After this lesson, you can:

- Trace closed, open and half-open states under an explicit failure policy.
- Distinguish a suppressed call from a failed call and from a successful probe.
- Enforce a one-probe recovery budget and reject a timer-only reopening.
- Test recovery, renewed failure and counter-reset behavior independently.

CYB-002 explains why coordination needs dampening. Here we implement one narrowly specified admission controller. We do not repeat its VSM survey, prove general stability as in MAT-024, or choose a universal operational threshold.

## 1. Specify what the breaker controls

A circuit breaker decides whether an operation may be attempted. It does not repair a dependency or establish that an attempted operation completed. Microsoft describes closed, open and half-open states, with limited recovery requests rather than unrestricted traffic. [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker).

Our synthetic policy opens after **two consecutive failures**, waits three logical ticks, and admits one probe. These numbers are teaching assumptions. They were not estimated from operational logs. The consecutive counter differs from a rolling-window failure-rate policy; changing between them changes which traces trigger the breaker.

Scope the controller to one dependency and operation class. An unavailable artifact decoder should not suppress unrelated source inspection. A circuit-wide refusal must have an explicit result such as `suppressed_by_breaker`; pretending it succeeded with an empty artifact makes downstream assessment dishonest. Similarly, transport acceptance cannot serve as the success signal for an operation whose contract requires a durable validated result.

### Practice Exercise 1

An operation fails at tick 0, succeeds at 1, and fails at 2. Does our breaker open? Would a policy counting two failures in three ticks behave identically?

**Worked correction:** The consecutive counts are 1, 0, 1, so our breaker remains closed. A three-tick window contains two failures and could open. Neither implementation is interchangeable without changing the contract and expected trace. Record the denominator and treatment of suppressed attempts before comparing failure rates.

## 2. Trace cooldown and renewed failure

Closed allows ordinary calls. At tick 0 a failure produces count 1; at tick 1 another failure produces count 2 and opens the circuit until tick 4. Requests at 2 and 3 are suppressed. They do not contact the dependency and cannot report its recovery. At 4, expiry permits a probe; it does not itself prove health. In our trace the probe fails, extending the open interval until 7. At 5 a request is again suppressed. At 7 a successful probe closes the circuit and clears the counter; the request at 8 proceeds normally.

| Tick | Attempt admitted? | Recorded outcome | State after decision |
|---|---|---|---|
| 0 | yes | failure | closed |
| 1 | yes | failure | open |
| 2, 3 | no | none | open |
| 4 | yes | failed probe | open |
| 5 | no | none | open |
| 7 | yes | successful probe | closed |
| 8 | yes | success | closed |

The boundary convention is `tick >= until`. Test tick 3 and tick 4 separately; an off-by-one error changes a stated three-tick wait. Production time should use a suitable monotonic clock and define restart behavior. The fixture uses integer ticks and has no clock dependency.

### Practice Exercise 2

Someone reports two successful responses at ticks 2 and 3 because their cached fallback returned a document. May those responses close this breaker?

**Worked correction:** No. They were suppressed dependency calls. A fallback can be useful, but its success is a different observation. Store the fallback origin and leave dependency health unknown until the authorized probe obtains the required evidence.

## 3. Keep half-open admission bounded

When five callers notice cooldown expiry together, a controller that immediately switches to closed admits all five. Our half-open state instead reserves one probe slot. A second admission request at tick 4 returns false until the first result is recorded. A failed probe opens again; a successful probe closes. That admission reservation must be synchronized if callers are concurrent.

The bundled `Breaker` models serialized method calls. It contains a `probe_inflight` flag, and `record` rejects a half-open result when no probe was admitted. It is **not a thread-safe production implementation**. Adding a Boolean without a lock or atomic transaction would leave the check-then-set race unresolved. Parallelism requires another test with a controlled interleaving and an implementation-level synchronization contract.

### Practice Exercise 3

The first caller reserves a probe but never produces a result. What does this model do, and what must an operational design add?

**Worked correction:** The probe remains in flight and later admissions stay blocked. Define a bounded probe deadline, how an unknown timed-out effect is reconciled, and who may reset the circuit. Do not simply mark the probe successful. CYB-015 treats unknown outcomes and replay separately.

## 4. Apply the policy and challenge the controls

Run the existing stdlib fixture from the package root:

```powershell
python scripts/course-exercises/cyb_resilience.py --json
```

Inspect record `CYB-013`, test ID `breaker_probe_budget`. The solution compares the whole eight-event trace, tests that success clears the consecutive counter, and requests the half-open slot twice. The negative control is an explicitly defective timer-only design admitting five calls at tick 4; the one-probe rule rejects it. This tests the intended admission budget rather than merely asserting that a state string exists.

Application to a course-production worker is straightforward: place admission before a dependency call, retain the original logical task identifier, and report suppression to the scheduler. Keep failure classification outside the breaker so an invalid user input does not look like a dependency outage. A breaker around writing does not make writes idempotent, and an open breaker must not hide already running work.

### Practice Exercise 4

Change the threshold to three. State the revised expectation before running code. Is the original negative control sufficient to validate the new policy?

**Worked correction:** Two initial failures should leave the circuit closed, so the original expected trace must change. Keep the probe-budget mutant, but also add three consecutive failures and an intervening success. Otherwise the changed threshold could be ignored and the test would fail to exercise it.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual assessment, 4 points:** explain the three states (1), compute the opening and probe boundaries (1), distinguish fallback success (1), and identify the serialized-concurrency limit (1). Require all four before application. Capture the learner's initial and revised belief with reasons; points are not calibrated confidence probabilities.

**Behavioral application, 4 points:** implement a changed threshold in an isolated copy (1), predict the new trace (1), pass a reset positive control (1), and reject an unrestricted reopening mutant (1). Observe the learner's actual receipt. An author test run does not establish learning. Retry teaching at most three times before escalating the unresolved gap under Streeling policy.

## Journal, proof and synthesis

Record inputs, policy, expected trace, actual trace, fixture hash, runtime, rejected mutant and one unresolved assumption. Synthesize the difference between admission and completion, then state which code or lesson wording changed after the failure case.

The synthetic evidence can establish that this serialized model follows this trace and probe budget. It cannot establish a fleet-safe threshold, real dependency recovery, concurrent correctness or operational improvement. Preserve those limits when proposing integration.

## Further Reading

- Existing CYB-002, `cyb-002-active-dampening-cross-repo-oscillation.md`: coordination survey, retained as prerequisite.
- [Microsoft circuit breaker documentation](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker), verified 2026-10-07: state vocabulary and bounded probe principle.

*Locally authored using the Seldon course format; no Seldon research cycle, publication, or learner outcome is claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_resilience.py).
