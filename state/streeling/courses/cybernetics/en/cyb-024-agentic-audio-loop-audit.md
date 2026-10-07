---
module_id: cyb-024-agentic-audio-loop-audit
department: cybernetics
course: "Governed loops: evidence in audio iteration"
level: intermediate
prerequisites: [CYB-021, CYB-022, CYB-023]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Auditing an Agentic Audio Loop Without Inventing Listening Evidence

> **Department of Cybernetics** | Intermediate | 45 minutes

An automated audio iteration may generate a file, report a numerical improvement, and still sound worse. This lesson concerns the control of claims across that loop: what was transformed, which measurements belong to it, and what remains untested. It teaches no compressor recipe and requires no recording device, model download, GPU, or paid service. The only signal is four invented normalized samples.

## Objectives

- Bind an audio measurement to input, transformation configuration, and output.
- Calculate sample peak and root-mean-square magnitude for a synthetic gain step.
- Reject a configuration mismatch and a signal exceeding the declared peak limit.
- Report mechanical acceptance separately from unobserved perceptual quality.

## 1. Specify the Experiment Before Iterating

Our synthetic signal is `[-0.6, 0.2, 0.6, -0.2]`. Its values are dimensionless normalized sample amplitudes. The transform multiplies each sample by gain `0.5`. The acceptance rule is a finite nonempty signal, consistent provenance, and sample peak no greater than one. The rule checks numerical integrity, not artistic success. No loudness standard, true-peak estimate, spectral balance, or room response is represented by four numbers.

Before an actual listening experiment, a team would also define the musical question, comparison conditions, listener procedure, equipment, allowable iteration budget, and stopping criterion. Those decisions belong in a separately authorized experiment. This course neither launches such a test nor assumes one happened. A missing observation should remain a named unknown rather than become an imagined favorable review.

**Exercise.** A worker says its output is musically better because every sample lies within `[-1,1]`. Which inference is invalid?

**Worked correction.** Staying within the declared sample range supports the mechanical peak condition only. It does not establish timbre, loudness balance, intelligibility, preference, or musical quality. Record mechanical evidence and mark perceptual assessment `not_tested`. The transform could simply make an unusably quiet signal.

## 2. Calculate the Trace and Its Limits

Applying gain `0.5` produces `[-0.3, 0.1, 0.3, -0.1]`. Sample peak is the greatest absolute sample, so it is `0.3`. Root-mean-square magnitude is the square root of the average squared samples. The squares are `0.09`, `0.01`, `0.09`, and `0.01`; their average is `0.05`, so RMS is approximately `0.223607`.

Applying gain two instead gives `[-1.2, 0.4, 1.2, -0.4]` and peak `1.2`. The fixture rejects this range violation. It does not silently clamp the values; clamping would be another transform requiring its own configuration and evidence. In a real sampled signal, sample peak alone may miss extrema between samples, as explained in [ITU-R BS.1770-5](https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en). This course makes no true-peak compliance claim.

**Exercise.** Apply gain one to the input. Calculate peak and RMS squared, then compare with gain `0.5`. What useful conclusion follows?

**Worked correction.** Peak is `0.6`; mean square is `(0.36+0.04+0.36+0.04)/4 = 0.2`. Halving gain halves peak and quarters mean square to `0.05`. Both meet the fixture's peak boundary. This demonstrates numerical scaling, not that quieter output is perceptually preferable.

## 3. Bind Measurements to the Actual Transform

The receipt contains three content identities: a digest of input samples, a digest of `{"gain":0.5}`, and a digest of output samples. The audit recomputes all three. If a receipt belongs to gain one but the current output claims gain `0.5`, the numbers might remain plausible while the provenance fails. An attractive metric from a different candidate is not feedback for this iteration.

This repeats CYB-023's content-binding principle in an audio-specific setting. It also exposes two distinct control loops. The mechanical loop checks bounded numerical conditions. A perceptual loop would gather listening evidence under a defined comparison protocol. Conflating them allows a worker to stop on a convenient proxy. More iterations cannot fix an absent observation channel; first identify the missing measurement.

**Exercise.** Candidate A has peak `0.3`; candidate B has peak `0.6`. The worker copies A's measurement into B's completion receipt. How should the audit respond?

**Worked correction.** Reject the receipt if its input, configuration, or output identity differs from recomputation for B. Even if both candidates individually pass the peak limit, A's measurement cannot verify B. Preserve the mismatch as a failed control, then measure B directly under the declared procedure.

## 4. Apply the Audit and Preserve Unknowns

Run `cyb_governed_loops.py --json` by the fixture's actual package path. Record `CYB-024`, test ID `audio_audit`, uses `audio_receipt` and `audit_audio`. Positive control accepts gain `0.5` with its matching receipt. Negative controls reject gain two because peak exceeds one, reject a receipt from gain one, and reject a nonfinite sample. The accepted record still says `perceptual: not_tested`; that field is a substantive result, not a placeholder to delete.

The implementation computes the transformed sequence rather than trusting supplied peak values. It refuses nonfinite numbers before hashing, so a not-a-number value cannot flow through arithmetic as apparently valid evidence. It uses only Python's standard library and synthetic arrays. No real audio was generated, decoded, heard, or scored. Passing tests therefore supports the audit logic under modeled conditions, not a claim about actual music.

**Exercise.** Modify the fixture to return `perceptual: accepted` whenever peak is below one. Predict which documented claim becomes false.

**Worked correction.** The implementation would infer listening quality without listening evidence. The existing negative control checks that the mechanical positive case does not yield perceptual acceptance. Restore the separation, and add a real perceptual stage only after a defined, authorized experiment produces observations tied to the same output identity.

[Offline solution and executable controls](../../../../../scripts/course-exercises/cyb_governed_loops.py): record `audio_audit`.

## Two-Stage Assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Conceptual stage, four points: compute peak, compute RMS squared, explain provenance mismatch, and distinguish range acceptance from listening judgment. Require all four with calculations. Behavioral stage, four points: preserve the positive record, provoke excessive peak, provoke configuration mismatch, and retain `not_tested` for perception. Require all cases. No learner performance or confidence score has been observed; the package supplies questions and a grading contract.

## Key Takeaways

- Numerical range checks are not evidence of listening quality.
- A measurement belongs to one input, transform, and output identity.
- Preserve missing perceptual evidence as not tested.

## Journal, Proof, and Synthesis

Record signal definition, gain, input/configuration/output identities, metric formula, boundary, expected result, observed result, and untested perception. Separate assumptions from observations. Synthesize that a particular synthetic transformation passed numerical integrity checks; it does not establish audio usefulness, real-time behavior, psychoacoustic quality, or listener preference. If a future real experiment contradicts the proxy, revise both the stopping rule and the course rather than polishing the claim.

## Further Reading and Overlap Boundary

AUD-001 covers EQ/compression order; CYB-024 covers measurement provenance and termination claims, not signal-chain design. CS-004's composable audio-loop topic overlaps the application context. CYB-024 centers the distinction between numerical acceptance and unobserved perception; independent semantic review against the complete CS-004 source remains required. [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html) documents the digest API. [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) provides broader evaluation context; the synthetic acceptance rule is ours. Translation and independent review remain pending.
