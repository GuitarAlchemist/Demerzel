---
module_id: cyb-007-hysteresis
department: cybernetics
course: "Feedback foundations"
level: beginner
prerequisites: ["cyb-002-active-dampening-cross-repo-oscillation", "cyb-005-measured-signal-and-setpoint"]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Hysteresis: Remember Which Threshold Was Crossed

> **Department of Cybernetics** | Beginner | 40 minutes

## Objectives

- Trace a two-threshold relay with an explicit initial state and equality rule.
- Explain how identical measurements can yield different decisions after different histories.
- Detect lost state using a deliberate reset mutant and exact transition counts.
- Separate damping an ordinary signal from suppressing an emergency or concealing stale evidence.

## 1. Memory changes the decision

**Hysteresis** means that a decision depends on previous state as well as current input. A two-state relay has a high activation threshold and a lower deactivation threshold. Between them, it retains its previous state. MathWorks documents separate switch-on and switch-off thresholds as a relay model of hysteresis. [Primary reference: Relay](https://www.mathworks.com/help/simulink/slref/relay.html). Its documentation is a conceptual reference; the exact boundary and initialization rules below belong to our Python fixture.

Our synthetic alert observes a finite scalar load score. Start inactive. Activate at **6 or above**; deactivate at **2 or below**. Between 2 and 6, preserve the stored Boolean. Thresholds are teaching values, not recommended governance parameters. One sample is one tick; the fixture models no delay, sensor failure, or emergency channel.

For input 4, an inactive alert remains inactive, while an active alert remains active. Both decisions are correct under this contract. Knowing only the current score cannot reconstruct the alert. The stored state is evidence the implementation needs, not an incidental performance cache.

### Practice exercise and worked correction

Two controllers both receive 4. One previously received 1; the other previously received 6. Both started inactive. Predict their states and explain the difference.

**Correction:** The first remains inactive; the second remains active because 6 activated it and 4 does not meet the clearing threshold. The current value is identical, but histories differ. A function returning only `value >= 6` would discard the second history and implement a different contract.

## 2. Count transitions, including the initial state

Use inputs `[1,5,6,5,6,5,2,3,6,2]`. Starting inactive, the states are `[off,off,on,on,on,on,off,off,on,off]`. There are four switches: off to on at the third input, on to off at the seventh, off to on at the ninth, and on to off at the tenth. The gap between thresholds is `6-2 = 4` score units. It is not four ticks of cooldown.

The three readings 5 after activation leave the relay on. Repeated crossings around the high threshold do not repeatedly clear and reactivate it. Nevertheless, a signal repeatedly moving from 6 to 2 can still force repeated switches. Hysteresis is not a universal guarantee against oscillation; it suppresses one specific source of toggling under stated input conditions.

Threshold ordering is essential. The fixture requires `low < high` and rejects reversed thresholds. Equality at each boundary is deliberately included in the trace. Another library might define crossing differently; copy the concept only after comparing its executable boundary contract.

### Practice exercise and worked correction

For initial state on and inputs `[4,2,4,6]`, give all four states and count transitions from that initial state.

**Correction:** States are `[on,off,off,on]`, with two switches. At 2, the inclusive clearing rule applies; at 4, inactive remains inactive; at 6, activation applies. Counting the first on as a switch would incorrectly ignore that the controller started on.

## 3. A reset mutant reveals what the memory does

The fixture's deliberate mutant resets `active=False` before each sample. On the ten-input trace it produces `[off,off,on,off,on,off,off,off,on,off]`, which has six switches. It passes a shallow test containing only one activation and one clear event. The middle readings expose the bug: after 6 activates the relay, the next 5 should retain on, but the mutant forgets activation.

This matters after process restart. Persisting state, reconstructing it from a trustworthy event history, or deliberately resetting according to a documented policy are different designs. None can be substituted silently. A retained alert may also be wrong if the controlled object changes: an alert for queue A must not be reused as queue B's memory. CYB-005's scope and freshness checks therefore come before the relay.

In the verified offline routing incident, an intended browser surface could resolve to another surface. That motivates identity checking; it supplies no measured hysteresis thresholds. Similarly, a nearby SaveAs dialog's cause remains unknown. An operational incident should sharpen the contract without becoming an invented tuning experiment.

### Practice exercise and worked correction

After observing 6, a worker restarts and then observes 5. Why is a passing test on `[6,2]` insufficient? Propose a test that distinguishes retained and reset state.

**Correction:** Both implementations activate at 6 and clear at 2, so that test does not interrogate the memory interval. Test `[6,5]` across the restart boundary. Retained state yields `[on,on]`; an undocumented reset yields `[on,off]`. Record the intended restart policy before choosing which result to accept.

## 4. Apply a relay without hiding evidence

Run the [offline solution fixture](../../../../../scripts/course-exercises/cyb_foundations.py) with `python <package>/scripts/course-exercises/cyb_foundations.py --json`. Inspect test ID `hysteresis-memory` for CYB-007. Function `relay` carries `active` across the loop; `switches` accepts the initial state explicitly. The receipt includes exact states, four correct switches, the six-switch mutant, threshold rejection, and the two histories ending at input 4. All are synthetic; no live session or controller is contacted.

An alert can retain on while a new measurement is unavailable, but that does not make the old reading fresh. Report alert state and observation age separately. A timeout is not a clearing measurement. Emergency handling belongs to a separate path: a genuine emergency should be observed and escalated according to its authorization contract, without waiting for normal threshold clearing. This lesson does not implement such a live channel.

### Practice exercise and worked correction

The alert is on and the next measurement is missing. Should it clear? What belongs in the journal?

**Correction:** The numeric relay cannot evaluate a missing sample. Preserve the last known state and mark measurement validity unknown under a documented missing-data policy; do not feed zero as a fabricated clear signal. Record last valid score, time, scope, retained state, and missing-data decision. Replacing missing with zero would hide both the alert and the evidence gap.

## Two-stage assessment

**Conceptual, 5 points:** one each for history dependence, inclusive boundaries, exact four-switch trace, mutant explanation, and missing-data distinction. Require 4 points, including history dependence. Capture the learner's prior and subsequent belief; a rubric score is not a confidence estimate. Record a learner-reported belief separately; Streeling's conceptual gate requires True with confidence at least 0.7. Unknown calls for adapted teaching, Contradictory for investigation, with escalation after at most three attempts.

**Behavioral, 4 points:** observe the learner reproduce the trace, preserve or explicitly reconstruct state across a synthetic restart, reject a wrong-scope observation, and retain the missing-data reason. Require all four. Author fixture success does not establish that a learner performed these actions.

## Journal, proof, and synthesis

Save thresholds, equality rules, initial state, input trace, predicted states, actual JSON, source hash, restart policy, and the reset mutant's failed criterion. Summarize why four switches replace six for this trace. CYB-002 surveys hysteresis; this module supplies state-memory semantics and an executable counterexample. CYB-008 isolates memoryless tolerance, and CYB-009 treats timing. This evidence establishes a bounded relay contract, not global stability, fleet reliability, a production parameter choice, or completed learning. Translation, integration, and independent review are separate pending gates.

## Further reading

- [CYB-002: Active Dampening](cyb-002-active-dampening-cross-repo-oscillation.md), preserved overview.
- [MathWorks: Relay](https://www.mathworks.com/help/simulink/slref/relay.html), primary documentation verified 2026-10-07; fixture boundaries and tests are independently constructed.

*Local authored draft; provisional integration ID. No Seldon research cycle or publication claimed.*
