---
module_id: gas-003-decay-calibration-open-e
department: guitar-acoustics
course: "Calibrate an Open-E Decay Test for GA's Guitar Engine"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-12-003
version: "0.1.0"
---

# Calibrate an Open-E Decay Test for GA's Guitar Engine

> **Department of Guitar Acoustics & Sound Synthesis** | Intermediate | 40 minutes | English draft; review pending

## Objectives

You will distinguish an observed decay *measurement* from a Rust decay *parameter*, calculate the measured gap for the pinned open-E pair, trace the engine's actual feedback coefficient, and define a one-parameter native-render experiment with a falsifier and safety guards. [GAS-001](gas-001-open-string-audio-evidence.md) establishes the recorded/rendered pair. [GAS-002](gas-002-brightness-control-and-evaluation-gate.md) tests a brightness hypothesis for a local harmonic ratio. This lesson asks a different question: **can a controlled change to GA's decay setting move its open-E level decline toward the recorded fixture without damaging the attack, pitch, or other notes?** No decay candidate has yet been rendered for this lesson.

## 1. Start with the measured envelope, not the knob

The pinned [GAS-001 fixture](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) contains two four-second mono 44,100 Hz WAVs: a separately attributed acoustic recording labeled open E2 by its dataset, and a **native** render from GA's Rust guitar engine at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. The render uses default guitar profile 0 and `engine_note_on(82.4069 Hz, velocity 0.1)`. It is not a capture of the browser AudioWorklet. The [fixture README](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md) gives the WAV hashes, acquisition boundaries, source credit, and CC BY-SA 4.0 attribution for the recorded file.

The saved [measurement JSON](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) gives a late-minus-early RMS level change of **−3.9 dB** for the recording and **−1.1 dB** for the render. The [measurement script](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py) takes early RMS at 0.2–0.4 seconds and late RMS at 1.0–1.2 seconds **after each first onset**. The recorded first onset is approximately 1.1 seconds into its file, with another attack near 2.75 seconds; the render begins at zero. Thus the selected recording windows are approximately file times **1.3–1.5** and **2.1–2.3 seconds**, before the second attack. They are not whole-file decay constants.

The render's selected decline is **2.8 dB less negative**: `−1.1 − (−3.9) = +2.8 dB`. Equivalently, its absolute error against this recording's late-minus-early change is `|−1.1 − (−3.9)| = 2.8 dB`. Both values are already rounded to a tenth of a decibel. The WAVs differ in initial level, instrument, microphone, room, and plucking conditions, so comparing within-file level *changes* is more useful here than comparing their absolute RMS dBFS values. Even this difference does not show which engine parameter caused it or which sample listeners prefer.

### Exercise 1 — Read the gap

Using the saved values, calculate the signed render-minus-recorded late-minus-early difference and the absolute error. Does a 2.8 dB error mean the render's whole file is 2.8 dB louder?

> **Answer:** `−1.1 − (−3.9) = +2.8 dB`, and the absolute error is `2.8 dB`. The render's level falls less between the two selected onset-relative RMS windows. This is not a whole-file loudness comparison and does not establish a listener preference.

### Exercise 2 — Keep the second attack out

Where do the recording's two RMS windows fall in file time if its first onset is approximately 1.1 seconds? Why is a late window beginning at 2.8 seconds unsuitable for this first-note question?

> **Answer:** Early is approximately `1.1 + [0.2, 0.4] = 1.3–1.5 s`; late is `1.1 + [1.0, 1.2] = 2.1–2.3 s`. A window beginning at 2.8 s is after the additional recorded attack near 2.75 s. It would mix another event into a supposed decay measurement. The onset itself is approximate, so repeat the analysis with a small onset perturbation before making a strong claim.

## 2. Trace the Rust parameter and its effective coefficient

In the pinned [GA Rust engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), `Engine::new` starts with `decay = 0.9968` but then selects default guitar profile 0, which sets **base decay to 0.9978**. The exported `engine_set_decay` clamps a requested base value to `[0.95, 0.9999]`. Select the profile **before** applying a candidate setter value: choosing a profile afterwards rewrites decay along with other profile controls. The checked-in [fixture renderer](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py) calls `engine_init` and `engine_note_on`, but does not call `engine_set_decay`; a candidate run therefore needs a documented extension or separate harness. No such candidate run is reported here.

Inside the render loop, the relevant source expressions are:

```text
f_norm = clamp((voice_frequency_hz - 82) / (330 - 82), 0, 1)
voice.sustain = min(0.995 + 0.006 * (1 - f_norm), 0.9998)  # assigned at note excitation
feedback_decay = (base_decay + 0.0025 * (1 - f_norm)) * voice.sustain
```

For the fixture's nominal `82.4069 Hz`, `f_norm ≈ 0.00164073`. The uncapped sustain expression is about `1.00099016`, so `voice.sustain = 0.9998`. With profile-0 base decay `0.9978`, the source expression gives `(0.9978 + 0.0025 × (1 − 0.00164073)) × 0.9998 ≈ 1.00009584`. A proposed base value of **0.9976** gives approximately **0.99989588**. Both requested base values lie inside the setter's clamp.

These are **feedback coefficients calculated from source**, not measured envelope decay rates. The loop also combines the current and next delay samples, all-pass dispersion, a stateful low-pass path blended by brightness, attack noise, body resonators, and reverb. A coefficient slightly above one in one expression does **not**, by itself, prove an unstable output or an audible defect. Nor does a lower coefficient prove a particular `−dB` change in the resulting WAV. Measure the output under a fixed method.

The engine's separate `attack_decay` controls attack-noise evolution; `reverb_mix` affects the tail; brightness changes the feedback blend. Do not move these at the same time as the decay candidate, or the cause of any observed change becomes ambiguous. GAS-002 already addresses brightness. This experiment holds it fixed.

### Exercise 3 — Calculate, then limit the inference

For `82.4069 Hz`, what sustain cap applies, and what are the approximate effective feedback-decay coefficients for base `0.9978` and `0.9976`? Does the first value above one prove that the recorded GA WAV grows louder over time?

> **Answer:** `f_norm ≈ 0.00164073`; the uncapped sustain exceeds `0.9998`, so the cap is `0.9998`. The source expression yields approximately `1.00009584` for base `0.9978` and `0.99989588` for base `0.9976`. No. This is one coefficient inside a filtered, stateful, resonant, reverberant system. The saved WAV's selected RMS change is actually `−1.1 dB`; the coefficient alone cannot predict its envelope.

## 3. Predeclare a one-parameter experiment

A controlled native trial would build the **same pinned Rust revision** and initialize a fresh engine for each arm at 44,100 Hz. Keep profile 0, E2 frequency `82.4069 Hz`, velocity `0.1`, four-second duration, compiler/toolchain, WAV encoding, and all other settings fixed. The baseline arm uses profile 0's base decay `0.9978`. In the candidate arm, call `engine_set_decay(0.9976)` **after** initialization/profile selection and before `engine_note_on`. Log the order and requested value; persist both WAV hashes and the measured onset choice. The source fixes a noise seed at engine creation, but fresh engines and an identical build are still needed to avoid state carry-over. The current fixture renderer has no decay option, so adapt or replace it and review the resulting script before making any empirical claim. A native comparison will not certify the browser AudioWorklet; test that path separately if it is the shipping target.

Run the same measurement procedure on baseline and candidate. A narrow **proposed classroom gate** is an absolute late-minus-early error at least **1.0 dB smaller** than the saved rounded baseline error of `2.8 dB`: target `≤ 1.8 dB` from the recorded `−3.9 dB`. On rounded values, this corresponds to a candidate decline between **−5.7 and −2.1 dB**. For an actual acceptance decision, compute from the unrounded WAV measurements and record a tolerance, rather than deciding at a tenth-decibel boundary using rounded JSON. This gate is a teaching threshold chosen in advance, **not** a GA product standard or a prediction that `0.9976` will pass.

Guard the comparison: no clipping or near-clipping (proposed peak absolute amplitude below **0.95**), preserve the E2 fundamental near its baseline under the same one-second peak search, and examine the initial attack and the second/fourth partial tracks so a better aggregate RMS number cannot hide a damaged transient or spectral tail. Repeat on other strings, notes, and velocities before generalizing. Inspect level-matched, blinded listening judgments; a numerical match to one external guitar cannot establish perceived realism. If the candidate fails the `≤1.8 dB` gate or violates a guard, reject this **candidate setting for this test** and report the measured result. A failed test does not prove that no decay change could ever help.

### Exercise 4 — Apply the proposed gate

Using the saved rounded baseline values, what is the maximum allowed absolute error for a 1.0 dB improvement? What candidate decline interval does that imply around `−3.9 dB`? Would a candidate in the interval but with a peak of `0.98` pass all the proposed guards?

> **Answer:** The threshold is `2.8 − 1.0 = 1.8 dB`; `|candidate − (−3.9)| ≤ 1.8` gives `−5.7 ≤ candidate ≤ −2.1 dB`. A peak of `0.98` fails the proposed `<0.95` peak guard even if the decay number passes. This is arithmetic on a proposed gate, not a measured candidate result.

### Exercise 5 — State a falsifier

An agent claims “lowering base decay to `0.9976` improves GA's E2 damping.” Name the minimum controlled artifacts and one result that would falsify that claim under this lesson's gate. What would still be unknown after a passing single-E2 run?

> **Answer:** Save the exact engine revision/build and parameter-call order; baseline and candidate native WAVs and hashes from fresh engines; the same onset-aligned measurement output and peak/partial/attack checks. If the candidate's unrounded absolute error does not shrink by at least the declared 1.0 dB, or a guard fails, this candidate fails the gate. Even a passing E2 result leaves browser output, other notes/velocities, recording-condition mismatch, and listener preference unverified.

## 4. Separate improvement from calibration

The recorded reference is a **calibration probe**, not an exact physical target for every guitar. The source dataset labels it open E2, but its microphone, room, player, and instrument differ from the render. A global `decay` change can affect many notes; the frequency-dependent source formula makes extrapolation from E2 especially unsafe. If the candidate moves the measured envelope toward this one reference, say only that it moved the **specified late-minus-early measure** for the tested render. If it does not, save the failed artifact so the next hypothesis can address attack noise, reverb, frequency-dependent feedback, or measurement-window sensitivity without rewriting history.

GA's existing [offline iteration loop](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) and spectral critic can support repeated experiments, but neither provides an automatic listener verdict. A ComfyUI-processed candidate, if introduced later, is a **separate offline arm**, not evidence that the Rust setter succeeded. Keep agent proposals, engine renders, recorded references, hashes, measurements, review, and public publication status distinct.

## Sources and limits

- [GAS-001 provenance](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md), [saved measurements](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json), [measurement method](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measure-pair.py), and [native renderer](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/render-ga-e2.py), all at Demerzel `5c4967454ddc740ed937c87719ca4d71a3522e4b`.
- [GA Rust engine source](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) and [offline iteration script](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), both at GA `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Only the saved GAS-001 pair was measured before this lesson. The coefficient values and acceptance interval are derived calculations; the `0.9976` candidate, native harness extension, browser capture, multi-note checks, and listening panel have not been run. Five AI-drafted localizations and a bounded independent AI subject preflight exist. Human subject, learner, and fluent-language reviews, Learn deployment, and public readback remain pending.
