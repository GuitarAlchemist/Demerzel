---
module_id: gas-002-brightness-control-and-evaluation-gate
department: guitar-acoustics
course: "Guitar Acoustics: Test a Brightness Control in GA WASM"
level: intermediate
alchemical_stage: albedo
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-11-002
version: "0.1.0"
---

# Test a Brightness Control in GA's Guitar Engine

> **Department of Guitar Acoustics & Sound Synthesis** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to locate the GA guitar engine's brightness control, calculate its effective value for two notes, and design a one-parameter test with explicit acceptance and failure conditions. You will distinguish a changed coefficient from a measured spectral change, a native engine fixture from browser AudioWorklet output, and an existing offline critic from a proposed ComfyUI candidate.

## Project question and sources

[GAS-001](gas-001-open-string-audio-evidence.md) established a recorded open E2 and a GA-rendered E2 as a narrow teaching pair. The [pinned GAS-001 fixture](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) has a [measurement record](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/measurements.json) and [provenance notes](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). The GA WAV is a **native render** from the pinned Rust source, using default profile 0 and `engine_note_on(82.4069, 0.1)` at 44,100 Hz. It is not a recording of the browser AudioWorklet. The external file is a separately attributed recording labeled open E2 by its dataset; its recording conditions were not independently observed.

The measurement record reports the second partial relative to the first as **+7.0 dB** for the recording and **−16.9 dB** for the GA render in a one-second, onset-relative spectral window. This is a 23.9 dB difference in that *within-file partial ratio*. It is not a 23.9 dB difference in overall loudness, and the recorded instrument, microphone, room, and playing force are not controlled against the synthetic source. **Would changing the engine's brightness control narrow this particular measured gap without harming pitch, level, decay, or other notes?** The answer requires a new controlled render. This lesson derives a test from pinned code; it has not run the candidate.

### Exercise 1 — Read the gap correctly

Subtract the GA render's second-to-first partial ratio from the recorded file's ratio. State the sign and what the result measures. May it be called a listener preference?

> **Answer:** `+7.0 − (−16.9) = +23.9 dB`: the recorded second partial is 23.9 dB higher *relative to its own first partial* than the render's second partial is relative to the render's first. It is a selected-window spectral comparison, not a whole-file loudness difference or a measured listener preference.

## 1. Trace the parameter before changing it

The [GA Rust engine at `dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) initializes an engine and calls `set_guitar_profile(0)`. That profile sets base `brightness = 0.80`, alongside decay, dispersion, attack decay, and reverb values. The exported `engine_set_brightness` clamps a supplied base value to `[0, 1]`. A proposed experiment can compare that profile's `0.80` with `0.90`, applying the setter **after** selecting the profile. Selecting a profile later writes a profile brightness again and can replace the test value. This order is an implementation detail worth including in a run log.

The browser [audio bridge](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) posts `set_brightness` with the number supplied by its caller. The [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) forwards that message to the Rust setter only while `ready` is true. Its asynchronous `init` handler sets `ready` only after creating the WASM engine and posts an initialization status. The bridge's `initAudioEngine` returns a node after posting `init`; that return alone is not proof the worklet has reached `ready`. For a browser trial, observe its initialized status, select the profile, set brightness, then trigger the note. Otherwise an early brightness message may be ignored or a later profile selection may replace it. The GAS-001 WAV did not exercise this browser message path.

This parameter is a base value, not the final coefficient for every note. A working test records the order of profile selection, setter call, and note event, plus the exact source revision. Logging only “brightness 0.90” would be ambiguous if another call reset it.

### Exercise 2 — Protect the intended setting

In a proposed browser run, an experimenter calls `setEngineBrightness(node, 0.90)` immediately after `initAudioEngine` returns, then selects guitar profile 0. Give two reasons the intended `0.90` may not control the note. What order should the experiment record?

> **Answer:** The worklet may not yet be `ready`, so it will not forward the brightness message; then selecting profile 0 sets base brightness to `0.80` again. Record successful worklet initialization, profile 0 selection, a brightness setter call with `0.90`, and the later note event in that order. The setter clamps values to `[0, 1]`; none of these source lines proves that this trial was executed.

## 2. Calculate what the DSP loop actually uses

In `excite`, the engine clamps velocity to `[0, 1]` and sets `pluck_mix = clamp(0.15 + 0.35 × velocity, 0.05, 0.7)`. During rendering it computes `f_norm = clamp((frequency − 82) / (330 − 82), 0, 1)`, then uses

`effective_brightness = clamp(base_brightness + 0.45 × f_norm + 0.30 × pluck_mix, 0, 1)`.

That coefficient blends a brighter feedback path with a low-pass state. It is not a direct setting of the second partial's amplitude. The engine also shapes excitation, attack noise, dispersion, decay, body resonance, and reverb. Increasing the coefficient is therefore a plausible **hypothesis** for an E2 spectral change, not a computed 23.9 dB correction. The measurement must decide whether the particular ratio moves, and other checks must decide whether the sound remains usable.

For the fixture's nominal E2 `82.4069 Hz` and velocity `0.1`, `pluck_mix = 0.185` and `f_norm = 0.4069 / 248 ≈ 0.001641`. The default profile's effective coefficient is `0.80 + 0.45(0.001641) + 0.30(0.185) ≈ 0.85624`; the proposed `0.90` base gives `≈ 0.95624`. This is source-derived arithmetic on a code path, not a new audio measurement. At `330 Hz` with the same velocity, `f_norm = 1` and both sums exceed 1, so both effective coefficients clamp to `1`. A change that matters to this coefficient at E2 need not matter at that higher note. It still could affect other paths or conditions; only a render can establish the audio result.

### Exercise 3 — Calculate the clamp

For velocity `0.1`, compute `pluck_mix` and effective brightness at `82.4069 Hz` for base values `0.80` and `0.90`. What are the two effective values at `330 Hz`, and what does this imply about extrapolating an E2 test?

> **Answer:** `pluck_mix = 0.15 + 0.35(0.1) = 0.185`; `f_norm ≈ 0.001641`. Effective E2 brightness is approximately `0.85624` at base `0.80` and `0.95624` at base `0.90`. At 330 Hz, `f_norm = 1`, giving sums `1.3055` and `1.4055`; both clamp to `1`. The code's brightness coefficient cannot demonstrate that an E2 spectral change generalizes to 330 Hz, or that either render sounds better.

## 3. Define an acceptance gate before hearing a candidate

Use the existing native E2 fixture as baseline, not as a browser measurement. A future one-knob native test would initialize the same pinned engine at 44,100 Hz, keep profile 0, E2 frequency `82.4069 Hz`, velocity `0.1`, render duration, analysis windows, and other settings fixed, and change only the base brightness from `0.80` to `0.90` after profile selection. Use a fresh engine per arm so initialization state and the source's fixed noise seed are comparable. Keep the baseline and candidate WAVs with hashes and the parameter/order log. If browser delivery is the question, repeat the test separately through AudioWorklet and capture that output; a native result cannot certify the browser path.

One **proposed classroom gate** is to shrink the absolute second-partial ratio error against the recorded +7.0 dB reference by at least 3.0 dB from the baseline 23.9 dB. The candidate error must therefore be at most **20.9 dB** under the same onset-relative measurement method. This is a predeclared test threshold, not an empirical GA standard. Guard against clipping with a recorded peak below 0.95 normalized amplitude; retain the E2 fundamental check, decay comparison, and other-note/velocity renders. Review the candidate's late partial behavior, because one good local FFT ratio could mask an unnatural attack or decay. A failed guard means do not accept the one-knob change merely because the second partial moved in the desired direction.

The gate does not settle perceived realism. Compare level-matched, onset-aligned listening copies under a blind protocol after the measurements, and preserve individual judgments. A fixed E2 reference from one recorded instrument is a useful probe, not a universal target for all guitars. A candidate that passes this numerical classroom gate can still fail the listening or multi-note check.

### Exercise 4 — Compute the proposed threshold

What maximum absolute error would satisfy the proposed 3.0 dB improvement rule from the 23.9 dB baseline gap? If a future candidate met that single spectral threshold but clipped, would the proposal accept it? Has such a candidate been measured here?

> **Answer:** `23.9 − 3.0 = 20.9 dB` maximum absolute error from the recorded +7.0 dB ratio, using the same method. No: clipping violates a separate guard, so movement in one partial ratio is insufficient. No brightness candidate was rendered or measured for this lesson.

## 4. Keep an offline candidate in its own lane

GA's pinned [offline loop](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) records an iteration, optionally applies DDSP coloration when `GA_USE_DDSP=1`, and invokes local and spectral critics. Those are existing inspected steps; they do not constitute a ComfyUI handoff. A **proposed** ComfyUI-generated or processed E2 belongs in a separate offline candidate arm, alongside the original recorded reference and the unchanged GA baseline. It would need its source WAV hash, workflow JSON, model/version, seed, settings, output hash, format, and rights for a reproducible comparison. Verify that it still represents an isolated E2 event before measuring it against the same reference.

The ComfyUI output is neither a change to the Rust/WASM renderer nor a substitute for a controlled engine render. It might suggest a target timbre or expose a question about excitation, but the engine parameter must be evaluated on an actual engine output. The existing spectral critic suggests possible adjustments from summary features; its score does not validate guitar realism or identify a unique causal knob. Acceptance still depends on the pinned measurement procedure, safety guards, more than one note, and listening evidence.

### Exercise 5 — Classify the third arm

An agent proposes a bright ComfyUI WAV with no workflow, model version, seed, or source hash. Can it count as evidence that base brightness `0.90` improved GA's WASM engine? Name the missing provenance and the required engine comparison.

> **Answer:** No. The WAV is an untraceable offline candidate, not an engine output. Preserve the source and output hashes, workflow, model/version, seed, settings, format, and rights; verify an isolated E2. Then render the pinned GA engine with only the brightness value changed, compare it with its own baseline by the same method and guards, and separately collect level-matched listening judgments. No ComfyUI run or such comparison was performed here.

## Limits and next check

The 23.9 dB gap is a saved measurement for one recorded and one native-rendered open E2, under stated onset-relative windows. The effective-brightness numbers are calculations from pinned source, not recorded changes in harmonic energy. The proposed `0.90` candidate, acceptance threshold, browser message sequence, multi-note sweep, ComfyUI arm, and listening test remain unrun. Before changing GA, capture a controlled candidate and verify its parameter order, WAV identity, pitch, partial ratios, attack/decay, peaks, browser behavior where relevant, and musician judgments. Human subject review, learner testing, localization, Learn sync/build, anonymous readback, and publication remain pending.
