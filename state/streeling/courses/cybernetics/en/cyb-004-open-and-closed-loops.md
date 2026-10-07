---
module_id: cyb-004-open-and-closed-loops
department: cybernetics
course: "Feedback foundations"
level: beginner
prerequisites: ["CYB-002"]
estimated_duration: "35 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Open and Closed Loops: Find the Return Path

> **Department of Cybernetics** | Beginner | 35 minutes

## Objectives

- Draw the causal return path that distinguishes an open loop from a closed loop.
- Calculate a ten-step response with and without a disturbance.
- Reject a completion claim supported only by delivery or acceptance evidence.
- Detect a reversed correction sign with a deliberate failing control.

## 1. A loop is a causal structure

A **plant** is the process being influenced; a **controller** chooses an action; a **sensor** reports an outcome. An open-loop controller chooses actions without using the resulting plant output to revise them. A closed-loop controller uses a measured output to choose a later action. Logging output is insufficient if the next action never depends on that log. NI's controller documentation describes measurement, comparison with a setpoint, and actuator adjustment as the closed-loop path. [Primary reference: NI](https://www.ni.com/en/shop/labview/pid-theory-explained.html).

Consider a coordinator submitting one bounded task to a worker. Submission changes the worker's input. An acceptance receipt indicates that input reached a processing stage. A durable result plus an independent check measures a different outcome. A verified 2026-10-06 continuation produced acceptance first and completion later. This supports separating those observations; it does not establish a universal worker latency or reliability rate.

The loop closes only when the coordinator's later decision depends on the relevant outcome: stop after verified completion, investigate an explicit blocker, or continue observing while work genuinely progresses. Repeatedly sending the same instruction is not itself feedback control. It may simply add input while the plant is already responding.

### Practice exercise and worked correction

Draw arrows for these steps: coordinator sends task, worker accepts, worker writes result, checker verifies result, coordinator decides whether another task is needed. Remove the last arrow from the checker to the coordinator. What changed?

**Correction:** The operational path still executes, but the completion decision no longer receives output evidence. The resulting decision process is open loop with respect to completion. Keeping an acceptance arrow does not repair it: acceptance measures a different stage. A complete answer names both the missing causal arrow and the outcome it should carry.

## 2. A numerical plant exposes the distinction

Use a synthetic discrete plant with state `x`, target 10 units, and one-unit actuator gain. At tick `k`, `x[k+1] = x[k] + u[k] + d[k]`. Start at zero. A proportional controller chooses `u[k] = 0.5 * (10 - x[k])`. Measurements are exact and immediate; there is no saturation, queue, rounding, or action cost. These assumptions are teaching conveniences.

The first states are 0, 5, 7.5, 8.75, and 9.375. Now apply disturbance `d[4] = -4`. The next state is `9.375 + 0.3125 - 4 = 5.6875`. A closed loop sees that drop and chooses `u[5] = 2.15625`, bringing the next state to 7.84375. An open-loop schedule computed from the undisturbed model instead sends 0.15625, reaching only 5.84375.

At ten ticks, the closed-loop state is 9.865234375; the open-loop state is 5.990234375. The nominal undisturbed schedule ends at 9.990234375. Open loop performs well when its model matches; the disturbance reveals why that success was conditional.

### Practice exercise and worked correction

Compute the two controls immediately after the disturbance and their errors at tick ten. Which trace better rejects this particular disturbance?

**Correction:** Controls are 2.15625 and 0.15625. Final errors `10-x` are 0.134765625 and 4.009765625. Closed loop has smaller error in this experiment. This comparison does not prove every closed-loop design is stable or that the chosen gain is suitable for a delayed worker.

## 3. Closing a loop can also amplify error

With no disturbance, substituting the control equation gives `e[k+1] = (1-K)e[k]`, where `e = target-x`. For this exact scalar plant, errors shrink when `abs(1-K) < 1`, hence `0 < K < 2`. At `K=0.5`, each undisturbed error halves. This is a derivation for one equation, not a tuning recommendation for organizational coordination.

Reverse the sign: choose `K=-0.5`. A positive error now causes negative movement, enlarging the error. In the disturbed ten-tick fixture, the final state is -597.025390625. This deliberately bad controller has a sensor and a return path, yet fails badly. Feedback topology and stable behavior are separate claims.

Measurement can also refer to the wrong plant. An offline browser-routing incident showed that an ordinary caller intended for surface B could resolve to A, while an explicit engine selection resolved to B. A reading from A cannot validate work on B. Terminal routing was separately inspected; the browser result must not be generalized to every interface. The cause of a nearby SaveAs dialog remained unknown.

### Practice exercise and worked correction

An operator sees a falling error on surface A after commanding B. Is the loop closed and verified for B? Suggest one observation that could falsify the operator's conclusion.

**Correction:** There may be a return path, but its scope does not match the controlled plant. A scoped read of B showing unchanged state falsifies the claim. Preserve both identities and timestamps rather than treating a visually convincing dashboard as proof.

## 4. Apply the model in code

Run `python <overlay>/scripts/course-exercises/cyb_foundations.py --json` from any working directory. Record `loop-disturbance`, the test ID for this module. The solution function `scalar_loop` maintains both actual state and nominal planned state. Its `open_loop` branch uses the plan as the controller input while both branches experience the same disturbance. That isolates the causal difference rather than comparing unrelated schedules.

The positive control checks exact final values. The negative control checks that the reversed-sign controller's final error exceeds the initial error. No network, session, or production actuator is contacted. Passing verifies the fixture's bounded predictions; it does not teach a learner or validate a fleet.

### Practice exercise and worked correction

Modify the disturbance from -4 to -2, keeping its tick unchanged. Predict the final difference between the disturbed and nominal closed-loop state before running.

**Correction:** The drop at tick five is 2. Five remaining corrections halve it, leaving `2/32 = 0.0625`. The final state should be 9.927734375. The corresponding open-loop offset stays 2 because its future controls ignore the output. An answer without the five remaining steps misses the timing assumption.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** causal return path, correct output stage, numerical errors, and sign counterexample each earn one point. Require at least 3 points and no acceptance-as-completion claim. Record the learner's prior and subsequent belief in their own words; do not infer a confidence number from this score.

**Behavioral, 4 points:** on a synthetic task, identify the plant, inspect a scoped result, run the independent criterion, and stop further input when it passes. Require all four observed actions. If conceptual understanding passes but behavior does not, record that gap; no learner is certified by this page's existence.

## Journal, proof, and synthesis

Save target, scope, tick definitions, predicted traces, actual JSON, script hash, and one failed-control explanation. State what decision changed because of output evidence. The lesson extends CYB-002's mechanism survey with a causal test and derivation; CYB-005 checks measurement contracts and CYB-006 tests delay. The evidence supports this scalar comparison and the acceptance/completion distinction. It does not establish general stability, live routing correctness, or production throughput. Translation and independent review are pending.

## Further reading

- [CYB-002: Active Dampening](cyb-002-active-dampening-cross-repo-oscillation.md), the existing overview preserved unchanged.
- [NI: controller and closed-loop terminology](https://www.ni.com/en/shop/labview/pid-theory-explained.html), verified 2026-10-07; numerical experiments here are independently constructed.

*Local authored draft; provisional integration ID. No Seldon research cycle or publication claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_foundations.py).
