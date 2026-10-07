---
module_id: cyb-008-deadband
department: cybernetics
course: "Feedback foundations"
level: beginner
prerequisites: ["CYB-005", "CYB-007"]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Deadband: Spend Corrections Outside a Defined Tolerance

> **Department of Cybernetics** | Beginner | 40 minutes

## Objectives

- Define a deadband using the signal's units and an explicit boundary rule.
- Compute all actions for a bounded noise-and-fault trace.
- Detect both needless correction and an over-wide band that hides a fault.
- Preserve an emergency bypass and distinguish deadband gating from hysteresis and a continuous dead-zone transfer.

## 1. A tolerance is a decision contract

A **deadband** is an interval in which the controller deliberately takes no ordinary corrective action. Here error `e` is a signed synthetic timing residual measured in milliseconds; positive means the observed value is below the target under `e=target-measured`. Width `w=2 ms` defines the inclusive interval `[-2,2]`. Inside it, output is zero; outside it, the teaching gate returns the full error. No previous alert state is stored.

This gate is deliberately simpler than a physical actuator. MathWorks' Dead Zone block also defines a zero-output interval, but subtracts the corresponding boundary outside it. [Primary reference: Dead Zone](https://www.mathworks.com/help/simulink/slref/deadzone.html). For error 3 and width 2, our gate returns 3 while that symmetric dead-zone transfer returns 1. Both definitions are coherent; substituting one for the other changes the response and must change expected results.

Zero action does not mean zero error. It means the error is tolerated for this ordinary correction channel. The measured residual should still be retained for audit and other requirements. An observer cannot infer exact target achievement from a quiet actuator.

### Practice exercise and worked correction

For errors -2, 2, 3, and -3, compute the teaching gate's outputs. Then compute the symmetric boundary-subtracting dead-zone outputs.

**Correction:** The gate gives `0,0,3,-3`. The boundary-subtracting transfer gives `0,0,1,-1`. Both give zero at the inclusive boundaries. These are different functions, not rounding differences; name which function the application requires.

## 2. Noise rejection needs a fault control

The fixture uses residuals `[-2,2,-1,1,0,3,-3,6]` and width 2. Expected actions are `[0,0,0,0,0,3,-3,6]`. The first five samples are a constructed noise trace whose absolute values never exceed 2. Exactly three ordinary actions remain. An allowed-residual budget of 5 ms is separately specified, so the last residual 6 is outside that budget and must remain visible.

Now remove the band by setting width zero. On the five noise samples, four outputs are nonzero: `[-2,2,-1,1,0]`. The controller spends corrections on every nonzero sample, although this scenario intended to tolerate those values. That is one negative control. A second sets width 10; error 6 then produces zero action, hiding an out-of-budget fault from ordinary correction. Quietness alone is therefore a poor acceptance metric.

These values model bounded noise for teaching, not an empirical noise distribution. No false-alarm probability, production latency, or long-run convergence rate is measured. A real threshold needs observed noise, decision cost, and fault sensitivity; a convenient number from this fixture cannot supply those.

### Practice exercise and worked correction

How many ordinary actions occur in the eight-sample width-2 trace? If width becomes 5, which samples still trigger? Does that prove width 5 is preferable?

**Correction:** Width 2 triggers three times. Width 5 triggers only the final 6. Fewer actions does not by itself imply a better design: tolerating residuals 3 and -3 changes the contract. Compare the permitted residual and correction cost before choosing a width, and retain the raw residuals even when no action occurs.

## 3. Preserve an independent emergency decision

The solution function receives a separate `emergency` Boolean. When true, it returns `"escalate"` before checking the ordinary numeric band. At error 1 with width 2, ordinary action would be zero, but the emergency result is escalation. This explicit precedence makes the teaching policy testable.

The example does not establish who can declare an emergency or authorize a real escalation. That decision requires an independent provenance and permission contract. CYB-002 already states that ordinary dampening must preserve the algedonic bypass; this exercise makes the precedence visible without sending a live governance message. A false emergency label could itself be harmful, so preserving the bypass is distinct from trusting every label.

A measurement also needs CYB-005's scope and freshness checks. A plausible small residual from the wrong surface cannot justify quieting the intended surface. The verified offline routing incident supports this identity check, while the cause of the related SaveAs dialog remains unknown. No threshold choice here diagnoses that incident.

### Practice exercise and worked correction

An emergency flag accompanies residual 1. A programmer checks `abs(e)<=2` first and returns zero, then checks the flag. What observable test catches the ordering defect?

**Correction:** Call the function with `e=1`, `width=2`, and `emergency=True`; require `"escalate"`. The incorrectly ordered implementation returns zero and fails. A test with error 6 would miss the defect if escalation is checked only after passing the band, so the inside-band emergency is the distinguishing case.

## 4. Apply and audit the exact function

Run the [offline solution fixture](../../../../../scripts/course-exercises/cyb_foundations.py) with `python <overlay>/scripts/course-exercises/cyb_foundations.py --json`. Inspect CYB-008 test ID `deadband-budget`. Function `deadband_action` rejects negative widths, preserves emergency precedence, returns zero within the inclusive band, and returns full error outside. Its receipt records the eight expected actions, emergency bypass, zero-width noise actions, and width-10 hidden fault. The functions assume finite numeric input; broader type and nonfinite validation belong to the measurement boundary, not an untested promise about this helper.

Hysteresis and deadband can coexist, but they solve different problems. At error 1, this deadband outputs zero regardless of history. CYB-007's relay can remain active at an intermediate score after earlier activation. If the application needs both, specify their order and whether silence affects stored state. Do not assemble them merely because both are called damping.

### Practice exercise and worked correction

A reviewer claims zero output proves the timing residual meets every requirement. Rewrite the claim and identify one independent observation needed for acceptance.

**Correction:** Zero output proves only that this gate suppressed ordinary correction under its current inputs, or received exact zero. Retain the raw residual and compare it independently with the allowed-residual budget. An over-wide band can output zero for a violation, as width 10 and error 6 demonstrate.

## Two-stage assessment

**Conceptual, 5 points:** exact boundary outputs, gate-versus-transfer distinction, both bad-width controls, emergency precedence, and silence-versus-success each earn one point. Require 4 points including emergency precedence. Capture the learner's belief separately from this score: Streeling's conceptual gate requires True with confidence at least 0.7. Adapt teaching for Unknown, investigate Contradictory, and escalate after at most three attempts; no author invents confidence on a learner's behalf.

**Behavioral, 4 points:** observe a learner reproduce the trace, compare raw residuals with the independent budget, reject the inside-band emergency mutant, and justify width with the stated noise assumptions. Require all four observed actions. Passing the author's fixture is not confirmation of knowledge transfer.

## Journal, proof, and synthesis

Save units, width, boundary rule, raw trace, action trace, residual budget, emergency precedence, predicted results, JSON receipt, and script hash. Explain why both no-band and over-wide-band controls are necessary. CYB-002 introduces deadbands; this module supplies executable tolerance and failure budgets. CYB-007 covers memory, CYB-009 cadence, and MAT-024 mathematical stability. Evidence supports this bounded gate and its controls, not a physical actuator model, universal stability, learner completion, or production fault coverage. Translation, integration, and independent review remain separate gates.

## Further reading

- [CYB-002: Active Dampening](cyb-002-active-dampening-cross-repo-oscillation.md), preserved survey and bypass motivation.
- [MathWorks: Dead Zone](https://www.mathworks.com/help/simulink/slref/deadzone.html), primary documentation verified 2026-10-07. The gate's full-error output is an explicit local variant.

*Local authored draft; provisional integration ID. No Seldon research cycle or publication claimed.*
