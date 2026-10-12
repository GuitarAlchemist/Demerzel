---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Sampling and Aliasing at the GA Guitar Engine Boundary
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Sampling and Aliasing at the GA Guitar Engine Boundary

> **Department of Physics** | Intermediate | 35 minutes | English source draft; review and publication pending

## Objectives

You will calculate a Nyquist limit and an alias frequency, identify which sample rate the GA Rust engine actually receives, and design an offline test that could reveal aliasing without mistaking a computed risk for a measured defect. [PHY-001](phy-001-science-of-guitar-sound.md) introduces guitar harmonics. [PHY-002](phy-002-time-frequency-guitar-transients.md) chooses analysis windows for changing notes. Here the question is earlier in the signal chain: **which continuous frequencies can a sampled guitar signal represent, and what must happen before capture, synthesis, or rate conversion?**

## 1. Tie the rate to the artifact, not the note name

The pinned [GAS-001 fixture](../../../fixtures/guitar-acoustics/gas-001/README.md) contains a four-second recorded open E2 and a four-second native render of the GA Rust engine. Both files are mono at **44,100 samples per second**. The render calls `engine_note_on(82.4069 Hz, 0.1)`; the recorded file's E2 identity is a dataset label, not a frequency measurement. The render was produced by a native build, **not** by recording the browser AudioWorklet. Those distinctions matter when investigating an audio artifact.

At GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), the browser [audio bridge](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) sends `audioContext.sampleRate` to the [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). The worklet calls `engine_init(srToUse)` and renders mono float samples into the browser's output channels. The [Rust engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) stores that rate and uses it for resonator coefficients and delay length. Therefore the pinned 44.1 kHz WAV does **not** establish that every browser run uses 44.1 kHz. Log the actual context rate and capture path before comparing a browser recording to GAS-001.

For a duration `T`, sample count is `N = f_s T`. Four seconds at 44,100 Hz gives **176,400 samples** per mono channel. At 48,000 Hz it would give **192,000**. Neither count tells you whether the analog input was filtered correctly or whether the synthesizer avoided aliases.

### Practice exercise 1

A reviewer sees the GAS-001 44.1 kHz render and writes, “GA's browser engine always runs at 44.1 kHz.” What can the sources actually support, and what should a browser test record?

> **Answer:** GAS-001 fixes **its native rendered WAV** at 44,100 Hz. The inspected browser bridge passes `audioContext.sampleRate` into the worklet and Rust engine; its actual value must be observed in that browser session. Record the context rate, output or recording rate and codec, engine revision, and capture path. A native WAV is not a browser capture.

## 2. Calculate the representable band before discussing harmonics

For a uniformly sampled real signal at rate `f_s`, the Nyquist frequency is `f_N = f_s/2`: **22,050 Hz** at 44,100 Hz and **24,000 Hz** at 48,000 Hz. An ideal, band-limited continuous input with content strictly below `f_N` can be reconstructed in principle from its samples. Real capture needs an anti-alias filter before sampling, with a transition band below Nyquist. The number `f_N` is a mathematical boundary, not a promise that a microphone, converter, engine, or export chain has a brick-wall filter.

The open E2 target is `f_0 = 82.4069 Hz`. Its ideal integer partial `k` would be at `k f_0`, but a physical or synthesized guitar does not necessarily have every partial or keep them at exact integer multiples. At 44.1 kHz, `267 f_0 = 22,002.6423 Hz` is below Nyquist, while `268 f_0 = 22,085.0492 Hz` is above it. At 48 kHz, the corresponding boundary is between partial **291** (`23,980.4079 Hz`) and **292** (`24,062.8148 Hz`). These are *theoretical index limits* for this chosen fundamental, not a count of audible or measured partials. A useful production margin is lower than the exact boundary because filters need a transition region and implementation behavior matters.

### Practice exercise 2

For the same ideal E2 target, compute the highest integer harmonic strictly below Nyquist at 44.1 kHz and 48 kHz. Does that prove the fixture contains those harmonics?

> **Answer:** `floor(22,050 / 82.4069) = 267` and `floor(24,000 / 82.4069) = 291`. The adjacent 268th and 292nd partials lie above their respective Nyquist limits. This arithmetic does not prove either waveform contains a detectable 267th or 291st partial; measuring levels requires the WAVs, an appropriate window and noise floor, and explicit analysis limits.

## 3. Work an alias by hand

Sampling a continuous sine at `f` Hz gives values `sin(2π f n / f_s)` at integer `n`. Adding or subtracting an integer multiple of `f_s` gives the same samples up to phase or sign. A convenient magnitude-frequency rule is to fold `f` by multiples of `f_s` into `[0, f_s/2]`; equivalently, choose an integer `m` for which `|f - m f_s|` falls in that interval. This is a **synthetic single-tone calculation**, not an observation about GAS-001.

Consider a **23,000 Hz** continuous sine. At 44.1 kHz it is 950 Hz above Nyquist and folds to `|23,000 - 44,100| = 21,100 Hz`. The sampled sequence is equivalent to a 21,100 Hz sine with a sign or phase change. At 48 kHz, 23,000 Hz is below the 24,000 Hz limit, so it does not fold. Once a 44.1 kHz capture has folded that tone to 21,100 Hz, merely resampling the captured data to 48 kHz does not recover the original 23,000 Hz input: those sampled values cannot distinguish the two continuous origins.

In a guitar engine, broadband pluck excitation, nonlinear processing, and bright upper partials are reasons to *check* this boundary. The pinned [Rust excitation](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) uses filtered noise in a delay line and applies sample-domain processing. This inspection alone does not prove an audible or measurable alias in its output. Increasing the rate can move an alias boundary, but it also changes buffer sizes and compute cost; it is not a substitute for controlled band limiting and measurements.

### Practice exercise 3

A proposed excitation has a 30,000 Hz continuous component. Where would an ideal sampler place its single-tone alias at 44.1 kHz and at 48 kHz?

> **Answer:** At 44.1 kHz, `|30,000 - 44,100| = 14,100 Hz`. At 48 kHz, `|30,000 - 48,000| = 18,000 Hz`. These are ideal sampled-sine folds, not predicted spectral peaks of the GA engine. An upstream anti-alias filter may attenuate the component before capture; a digital generator must avoid creating out-of-band content or control its folding.

### Practice exercise 4

An engineer resamples a 44.1 kHz recording containing a 21.1 kHz peak to 48 kHz and says, “Now that the Nyquist limit is 24 kHz, the original 23 kHz tone is restored.” Explain the error.

> **Answer:** The 44.1 kHz sample sequence is compatible with both a 21.1 kHz tone and a 23 kHz tone with a phase or sign difference. Rate conversion can interpolate or filter the available data but cannot infer which continuous source was present. Prevent the fold before original sampling with analog anti-alias filtering, or generate band-limited digital content at the target rate.

## 4. Turn the risk into a falsifiable GA test

The [GAS-001 measurements](../../../fixtures/guitar-acoustics/gas-001/measurements.json) report near-E2 peaks and several low partials, not a high-frequency alias survey. A plot of the two 44.1 kHz WAVs alone cannot identify an alias's original frequency: a peak below Nyquist can have several causes. The recording also has an approximate first attack at 1.1 seconds and a second attack near 2.75 seconds, whereas the render begins at zero. Preserve onset-aligned intervals before comparing spectra; [PHY-002](phy-002-time-frequency-guitar-transients.md) explains that time-selection problem.

An offline experiment should first use a **known synthetic reference**: generate a 23 kHz sine at a higher reference rate, sample it at 44.1 and 48 kHz with the filtering choice recorded, and check for the predicted 21.1 kHz fold only in the deliberately unfiltered 44.1 kHz arm. Then render the same pinned GA engine source, note, velocity, profile, and duration at both rates through **native** calls, or capture both through the **browser** with its rate logged; do not silently mix paths. Save input settings, exact build, WAV hashes, rate, peak level, and spectral windows. Compare against a rate-matched, controlled baseline across multiple notes and velocities. If an unexpected tone moves according to an alias-fold prediction as the render rate changes, investigate its generating stage; if it persists at the same physical frequency, the simple alias hypothesis weakens. Confirm with a code-level change that targets the suspected stage and repeat listening at matched level. This protocol is proposed; these additional renders, captures, and listening checks have **not** been run for this lesson.

For future rate conversion, document the source and target rates, filter passband and stopband, delay, clipping checks, and whether the reference was captured before or after lossy encoding. The browser bridge has an optional [MediaRecorder path](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js); its blob should not be assumed to be a raw 44.1 kHz WAV. Keep that path separate from the fixture's native render.

### Practice exercise 5

A 21.1 kHz peak appears in one 44.1 kHz engine render. Is that sufficient to claim a 23 kHz synthesis alias? Specify a decisive next comparison and one control.

> **Answer:** No. The 21.1 kHz peak might be an in-band component, an alias from another out-of-band component, or a capture artifact. Render the same pinned engine configuration at 48 kHz and compare onset-aligned high-frequency spectra: a source near 23 kHz would be expected near 23 kHz there while its 44.1 kHz alias would be near 21.1 kHz. Control the engine revision, note, velocity, profile, and capture path; inspect the signal stage or add a targeted band-limiting change before attributing cause. The predicted movement is a test, not an observed result.

## Sources and current limits

- [Pinned GAS-001 fixture, provenance, and rates](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), with the local [README](../../../fixtures/guitar-acoustics/gas-001/README.md). The recorded source is credited to **collegefishiesd** under CC BY-SA 4.0 there; this lesson does not reproduce its audio.
- GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo): [browser bridge](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), and [Rust engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- The sample counts, harmonic-index thresholds, and single-sine fold examples above are direct calculations from stated rates and frequencies. No new GAS-001 high-frequency measurement, browser capture, human subject review, learner test, fluent-language review, or public readback has been completed for PHY-003. Five AI-drafted localizations and a bounded independent AI subject preflight exist; neither establishes those remaining gates.
