---
module_id: cyb-014-saturation-queue-conservation
department: cybernetics
course: "Saturation, Queues and Conservation of Work"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Saturation, Queues and Conservation of Work

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration ID; translations and review pending

## Objectives

- Calculate queue growth under a stated arrival and service ordering.
- Account for every incoming item as completed, queued or explicitly rejected.
- Separate capacity protection from throughput and learner value.
- Reject a silently dropping queue with a conservation counterexample.

CYB-002 introduces rate limiting. This module studies where accepted work waits, what happens at capacity, and how queue accounting detects hidden loss. MAT-024 treats dynamical stability and actuator saturation mathematically; we focus on a finite operational queue rather than re-derive its control theory.

## 1. Define the boundary before counting

A queue holds work awaiting service. **Saturation** means a resource has reached a declared limit; it does not mean all useful work has finished. Let `q` be waiting items at the beginning of a tick, `a` incoming items, `c` queue capacity, and `s` service capacity. Our ordering admits first, then serves:

```text
accepted = min(a, c - q)
rejected = a - accepted
served = min(q + accepted, s)
next_q = q + accepted - served
```

This is runnable logic in `queue_trace`; the displayed equations describe its inputs. Every item has identical service cost, service finishes within the tick, and no item retries, expires or fails. These are strong synthetic assumptions. A real course review might take minutes or days and require multiple rounds. Calling a drafted title a completed course would move the accounting boundary incorrectly.

Python's bounded `Queue` blocks insertion when full; nonblocking insertion raises `Full`. Its size checks are approximate under concurrency and do not reserve capacity. [Python queue documentation](https://docs.python.org/3/library/queue.html). Our sequential arithmetic fixture uses explicit rejection instead of blocking and does not instantiate a threaded queue.

### Practice Exercise 1

With `q=2`, `a=3`, `c=4`, `s=2`, calculate acceptance and the next queue. What changes if service happens before admission?

**Worked correction:** Admission accepts two, rejects one, and service drains two, leaving two waiting. Serving first would drain the initial queue, accept all three, and leave three waiting. Both can be defined policies, but they produce different traces. State ordering in the receipt rather than diagnosing the difference as random noise.

## 2. Trace overload and recovery

Feed arrivals `[3,3,3,0,0]` to service capacity two and queue capacity four. The post-service queue is `[1,2,2,0,0]`. Nine items arrived, eight completed and one was explicitly rejected. The third tick begins with two waiting; accepting all three would exceed capacity, so only two enter. During the next quiet tick the remaining two finish. The last tick performs no work.

| Tick | Incoming | Accepted | Queue before service | Served | Waiting after |
|---|---|---|---|---|---|
| 0 | 3 | 3 | 3 | 2 | 1 |
| 1 | 3 | 3 | 4 | 2 | 2 |
| 2 | 3 | 2 | 4 | 2 | 2 |
| 3 | 0 | 0 | 2 | 2 | 0 |
| 4 | 0 | 0 | 0 | 0 | 0 |

Without a bound, the pre-service peak becomes five and all nine eventually finish. The bounded queue protects a capacity of four by rejecting one item; it does not increase service speed. For indefinitely repeated arrivals of three and service of two, an unbounded deterministic queue gains one item each tick. A finite five-tick drain does not establish long-run stability for an arbitrary workload.

### Practice Exercise 2

An operator celebrates that the bounded queue is empty after tick 3 and says all nine requests were delivered. What evidence contradicts the claim?

**Worked correction:** The receipt records eight completions and one rejection. Empty means no waiting items at that moment. The rejected item is outside the queue, still requiring a user-visible disposition. Never silently classify rejection as completion.

## 3. Use conservation to expose missing work

At every tick, cumulative incoming equals completed plus waiting plus rejected. That equality is an **accounting invariant** under this model's assumptions. The defective control clips arrivals to capacity but never records the dropped item. It reports eight items accounted for after nine arrived. A graph showing a comfortable queue length would conceal the defect; the conservation equation exposes it immediately.

If a real workflow has running, failed, cancelled or expired items, add distinct states and terminal outcomes. Do not count the same task in both queued and running. Retry attempts should be counted separately from logical tasks; otherwise a timeout can inflate throughput. CYB-015 supplies a complementary recovery model for that boundary.

### Practice Exercise 3

A review queue reports 12 arrivals, three waiting, seven accepted reviews and one cancellation. What may you conclude? May you label the missing item failed?

**Worked correction:** Only eleven logical items are accounted for. One is unknown under the reported categories. Inspect task identifiers and transitions before assigning failure. The accounting gap might be a lost entry, a duplicate arrival counter or an omitted running item. Conservation detects inconsistency without diagnosing its cause.

## 4. Apply admission control without masking the bottleneck

Run the supplied fixture:

```powershell
python overlay/scripts/course-exercises/cyb_resilience.py --json
```

Record `CYB-014`, test `queue_conservation_and_admission`, includes all five ticks, the bounded totals, an unbounded counterexample and a balanced-arrival positive control. With two arrivals and two service slots for five ticks, ten items finish with no rejection or waiting. This confirms that the controller permits feasible work; a controller rejecting everything would protect capacity but fail the positive control.

Apply the lesson to drafting and review with separate queues. If drafting produces three pages per interval but review approves two, increasing drafting parallelism increases pending work. Reduce admission, improve review capacity, or negotiate scope with evidence. A queue cap is a transparent limit, not a substitute for identifying why review is slow. Measure reviewed course quality and waiting time as well as counts; the fixture has no quality model.

### Practice Exercise 4

Propose capacity six instead of four. Predict whether this changes eventual completions for the supplied burst, and explain what it cannot fix.

**Worked correction:** All nine items can be accepted; the queue peaks at five before service and drains within the quiet ticks. Service still finishes at most two per tick. A larger queue cannot make permanent arrivals of three sustainable, nor prove that reviewed pages are useful. Add the changed-capacity trace before presenting the change as an improvement.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** compute the ordering example (1), explain rejection versus completion (1), derive conservation (1), and distinguish finite drainage from permanent overload (1). Require four points and a reasoned revised belief before application; this score is not a confidence probability.

**Behavioral, 4 points:** predict a new burst (1), run an isolated changed-capacity case (1), pass balanced arrivals (1), and detect a silent-drop mutant (1). Observe the learner's next relevant receipt before marking knowledge transfer. After three unsuccessful teaching attempts, escalate the unresolved understanding under Streeling policy. No learner has been assessed by the author run.

## Journal, proof and synthesis

Journal the arrival sequence, unit costs, event ordering, capacity, every terminal disposition, expected/actual trace and script hash. Synthesize whether a change improved service, reduced admission or merely hid pending work. Revise code and wording when the invariant reveals a missing category.

This experiment establishes exact accounting for one sequential synthetic model. It does not measure operational queue latency, fairness, cancellation races, distributed capacity, human review quality or published course availability. Those need their own observations and boundaries.

## Further Reading

- CYB-002, existing dampening survey: admission rate is one part of coordination.
- MAT-024, existing `mat-024-dynamical-systems-stability-feedback.md`: stability and saturated control, a different mathematical scope.
- [Python queue API](https://docs.python.org/3/library/queue.html), verified 2026-10-07: bounded insertion and concurrency limits.

*Local English draft; no publication or learner outcome is claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_resilience.py).
