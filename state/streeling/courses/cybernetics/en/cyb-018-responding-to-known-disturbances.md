---
module_id: cyb-018-responding-to-known-disturbances
department: cybernetics
course: "Anticipate a Known Disturbance Without Hiding Model Error"
level: intermediate
prerequisites: [cyb-017-local-versus-global-stability]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# CYB-018: Responding to Known Disturbances

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration candidate; English draft, review and translations pending

## Objectives

- Distinguish a measured disturbance, its forecast and the resulting controller action.
- Calculate backlog for reactive and anticipatory policies using the same arrival trace.
- Detect forecast error and actuator saturation with separate negative controls.
- Produce a receipt that states the information and capacity required by an observed improvement.

## 1. A known event is useful only at the right time

Suppose a synthetic build service normally receives four jobs per tick. A scheduled release will generate eight jobs in each of two ticks. The disturbance is the extra arrival load. Its forecast is a statement available before selecting capacity. Feedback measures the queue after previous arrivals; feedforward uses a prediction of the coming arrivals. Neither term grants extra resources or makes the forecast true.

Let q be the nonnegative number of waiting jobs at the end of a tick. Assume jobs have equal unit cost, arrival and service batches occur within that tick, no jobs disappear, and service capacity is selected before arrivals are observed. Our map is q_next=max(0,q+arrival−service). It treats sufficient same-tick service as immediate completion; it does not model individual waiting times or partly completed jobs. These simplifications make the numerical comparison understandable and limit what it proves.

### Practice exercise and correction

At q=3, arrival=8 and service=6, find the next backlog. **Correction:** max(0,3+8−6)=5. Knowing the release schedule changes the information available to the controller, but backlog still follows actual arrivals and actual service, not the forecast alone.

## 2. Compare policies on one fixed trace

Use arrivals [4,4,8,8,4,4], initial q=0 and maximum service 8. The reactive policy selects 4 when the previous backlog is zero and 8 otherwise. Its end-of-tick backlogs are [0,0,4,4,0,0]. At tick 2 it still selects 4, because the previous backlog was zero. At tick 3 it selects 8, which matches arrivals but does not remove the four queued jobs. Tick 4 finally clears them.

The anticipatory policy selects the forecast arrival count, clipped to the capacity cap. With the exact schedule and cap 8, capacities are [4,4,8,8,4,4] and every backlog is zero. Each policy uses 32 units of selected capacity over the six ticks. The advantage comes from allocation timing under these assumptions, not from a larger total budget. Unused selected capacity cannot be carried into another tick in this model.

### Practice exercise and correction

Does the zero-backlog trace show that anticipation always costs less? **Correction:** no. Both policies selected 32 units here. A different cost model could charge reservation fees, startup delays or wasted capacity. Report this example's timing and peak backlog, not an economic conclusion it did not measure.

## 3. Forecast error and capacity limits are different failures

Now forecast four jobs every tick despite the scheduled burst. The anticipatory rule selects four throughout. Its queues become [0,0,4,8,8,8]. An unchanged forecast prevents recovery even after arrivals return to normal: capacity only matches fresh work. This is not evidence that anticipation is intrinsically bad. It demonstrates a failed forecast plus absence of a feedback correction for accumulated work.

Keep the correct forecast but reduce the physical cap to six. Queues become [0,0,2,4,4,4]. The forecast remains accurate, yet the policy cannot supply the requested capacity and later does not request extra service to drain backlog. A robust design would combine forecast information, measured backlog and bounded available capacity. That design must be evaluated in its own experiment; this lesson does not silently replace the policy mid-comparison.

Google's practitioner account emphasizes measuring relevant resources and negotiating capacity with dependent customers. Our equal-cost queue is a deliberately narrower model; actual requests can have different resource costs. See [Handling Overload](https://sre.google/sre-book/handling-overload/).

### Practice exercise and correction

Which diagnosis fits accurate forecast, requested service 8, actual service 6? **Correction:** capacity saturation. Fixing the forecast will not restore the missing two units. Record requested and actual actions separately, then consider admission reduction or a verified backlog-draining policy within the permitted resource budget.

## 4. Apply the comparison without rewriting history

Run from the package overlay root:

```powershell
python scripts/course-exercises/cyb_systems.py --json
```

The exact experiment `known_disturbance_forecast` calls the solution function `backlog` with a fixed trace. Output preserves each tick's arrival, selected service and queue. Its positive control requires planned peak 0 and reactive peak 4. Two negative controls require peak 8 with the wrong forecast and peak 4 with cap 6. An implementation that returns zeros for every queue cannot pass these checks.

In an assessment copy, add a policy requesting forecast plus current backlog, clipped to the cap. With correct forecast and cap 6, capacities after the burst can drain the four waiting jobs at two per tick. Check the actual trace instead of assuming success. Preserve the original receipt and label the added policy as a new experiment, not a correction to what the original run measured.

### Practice exercise and correction

Why is supplying the full arrival array not production forecasting? **Correction:** the fixture has perfect future information by construction. A real forecast must have a creation timestamp, source and accuracy record showing it existed before the action. Looking at future arrivals after a run creates an oracle comparison, not evidence that a deployed controller could have known them.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** correctly calculate a queue step, explain the reactive delay, distinguish forecast error from saturation, and state the perfect-information assumption. Require all four. Capture pre/post beliefs and remaining uncertainty without inventing confidence from a quiz score.

**Behavioral, 4 points:** preserve all policy inputs, reproduce the four traces, reject the two bad cases, and attach an action/forecast timing statement to the conclusion. Require all four plus observed execution before marking application verified. This authoring run tests software; it has not taught or assessed a learner. Use at most three assessment attempts before policy escalation.

## Journal, proof and synthesis

Record forecast creation time, arrival observation time, cap, chosen service, maximum backlog, residual backlog and costs excluded by the model. Preserve a wrong-forecast run rather than only the successful oracle. Synthesize: exact advance information and sufficient instantaneous capacity eliminate backlog in this fixture. Their absence produces two identifiable failure modes. There is no fleet throughput measurement, capacity purchase or production forecast here. CYB-006 studies feedback delay; CYB-014 studies saturation and queues. This module adds anticipatory disturbance treatment and explicit comparison under matched total selected capacity. CYB-017 constrains the stability claim; CYB-019 extends the disturbance across dependencies.

## Further reading

- [Google SRE, Handling Overload](https://sre.google/sre-book/handling-overload/), written by Alejandro Forero Cuervo; inspected 2026-10-07.
- Existing CYB-002 for coordination dampening and CYB-003 for disturbance variety; their aggregate variety estimates are not queue forecasts.

*Locally authored under streeling-cyb-20261007; no Seldon research cycle, publication or learning outcome claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_systems.py).
