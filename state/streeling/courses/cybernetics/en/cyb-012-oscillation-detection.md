---
module_id: cyb-012-oscillation-detection
department: cybernetics
course: "Operational feedback: measured reversal patterns"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation, cyb-005-measured-signal-and-setpoint]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Detecting Oscillation Without Calling Every Reversal Unstable

> **Cybernetics** | Intermediate | 45 minutes | Provisional CYB-012

## Objectives

- Compute sign reversals, span and endpoint contraction from measured error.
- Separate persistent alternating error from damped convergence, noise and drift.
- Reject an unevenly sampled trace under a declared sampling contract.
- Explain why a detection flag neither proves instability nor chooses a remedy.

CYB-002 describes cross-repository oscillation and mechanisms for dampening it. This course supplies a falsifiable detection exercise. MAT-024 already covers multipliers, Lyapunov exponents and stability proofs; we do not rederive those results. A finite operational trace lacks the full model required by such proofs. Our detector is a deliberately narrow teaching rule, with explicit thresholds and known blind spots, rather than a universal oscillation test.

## 1. Observe signed error, not busy activity

Define error as measured value minus target, in common units. Positive error is above target; negative error below. A sequence of commands is not interchangeable with error: commands can alternate while the measured process remains steady. Sampling times must be recorded. A missing measurement is unknown, not zero, and an empty trace cannot justify a stable-state claim.

Use six samples at seconds 0 through 5. For errors [4,-4,4,-4,4,-4], adjacent signs reverse five times and span, maximum minus minimum, is eight. The endpoint magnitude ratio is |last|/|first| = one. These are descriptive statistics of this window; they are not probabilities, causal findings or claims about unseen time.

### Practice exercise and worked correction

For [1,2,3,4,5,6], calculate sign reversals, span and ratio. Is increasing error harmless because reversals are absent?

**Correction:** Zero reversals, span five, ratio six. The detector will not call this alternating oscillation, but the error is moving away from target. “No oscillation flag” says nothing about drift safety. A separate progress or bound check is needed; this course does not replace it with another invented score.

## 2. Deadband and contraction reject misleading patterns

Declare an in-band tolerance of 0.5 error units. Values with magnitude at or below it break a candidate segment. We do not remove them and join distant observations: that would erase elapsed settling time. Choose the longest contiguous segment outside the band, taking the first if tied. Count sign reversals within that segment.

Our rule flags a window only if the segment has at least six samples, at least four reversals, the full-window span is at least four and endpoint contraction is greater than 0.5. These numbers are exercise parameters, not calibrated operational thresholds. If the first error is zero, the ratio is undefined and no persistent flag is returned by this model.

### Practice exercise and worked correction

Compare [8,-4,2,-1,0.5,-0.25] with [0.1,-0.1,0.1,-0.1,0.1,-0.1]. Explain both rejections.

**Correction:** The first has contraction 0.25/8 = 0.03125 and a longest outside-band segment of four; it is consistent with shrinking alternating error. The second has no outside-band segment and span 0.2. A sign-only rule would call both oscillation. The declared detector calls neither persistent, while preserving their actual measurements for inspection.

## 3. Sampling and window choice limit conclusions

The fixture requires equally spaced finite timestamps, positive interval, and at least six finite values. Times [0,1,2,4,5,6] fail because one measurement is missing. Rejection is preferable to silently treating that gap as a regular sample. The interval also matters: sampling a fast cycle too slowly can hide it or suggest a different pattern. Without additional measurements, the correct result is uncertainty, not a reconstructed cycle.

Endpoint contraction is intentionally simple and can miss renewed growth inside a longer window. A quiet plateau can also split a genuine intermittent oscillation into short segments. Before operational use, test windows and thresholds against held-out disturbances and define whether intermittent behavior matters. These limitations prevent the exercise rule from masquerading as a stability theorem. For model-based alternatives, consult the preserved MAT-024 lesson rather than duplicating its mathematical content here.

### Practice exercise and worked correction

The observed errors alternate, but timestamps are uneven. A reviewer interpolates missing values until the detector passes. What is the evidentiary problem?

**Correction:** The new values are assumptions, not observations. Preserve the original trace, state the interpolation method separately and test sensitivity if interpolation is justified for the application. Our solution rejects the original timestamps and supplies no interpolation. An inferred flag must not be recorded as directly measured behavior.

## 4. Apply a detector and challenge its meaning

Run the self-contained solution with the package path substituted:

```text
python <package>/scripts/course-exercises/cyb_operations.py --json
```

Test ID `windowed_error_reversals` reports metrics for persistent alternation, damped convergence, tiny noise, monotonic drift and a positive sawtooth [1,5,1,5,1,5]. Only persistent alternation is flagged. The sawtooth is an intentional blind spot: changes alternate, but error never crosses target. This rule detects repeated target crossings; it does not detect every periodic waveform.

The negative mutant counts sign crossings only and incorrectly flags tiny noise. An additional malformed-time test is rejected before metrics are trusted. None of the experiments uses fleet traces or changes a controller. Detection should lead to scoped investigation; automatic gain reduction or shutdown would require a separately justified policy and authorization.

### Practice exercise and worked correction

The positive control is flagged. Can you conclude that stronger backoff will solve it? Design one next experiment.

**Correction:** No. The trace does not identify the cause. In a bounded synthetic model, vary one suspected delay or gain while keeping input disturbance and sampling fixed. Compare error magnitude, reversal pattern and progress with baseline. Preserve a case where the change does not help. A flag alone is not a causal diagnosis and a quieter controller may simply stop useful progress.

## Assessment, journal and synthesis

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Stage one: calculate the persistent trace's five reversals, span eight and ratio one; explain noise rejection and the positive sawtooth blind spot. Award two points per task and require five of six with the blind spot identified. Stage two: predict a changed synthetic trace, run the code, preserve the sign-only mutant rejection and explain the timestamp failure. Require all four artifacts before recording demonstrated application; no learner was tested by this authoring run.

Journal units, target, sample times, tolerance, window choice, script hash, expected result and observed result. Synthesize the positive and negative controls together: the code implements the declared target-crossing rule and resists the noise counterexample. It cannot establish global stability, causality, optimum thresholds or completeness for periodic behavior. CYB-002 retains regulation mechanisms, MAT-024 retains formal dynamics, and CYB-017 will examine local versus global stability. This provisional draft still requires independent review and translations before integration approval.

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_operations.py).
