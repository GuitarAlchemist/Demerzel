---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Test EQ and compression order on a guitar signal"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# Test EQ and compression order on a guitar signal

> **Department of Audio Engineering** | Intermediate | 35 minutes | Revised English draft; subject, learner, localization, and publication review pending

## Objectives and project question

You will distinguish a filter from a level-dependent processor, demonstrate their order dependence with a small calculation, and design an offline comparison that a future compressor implementation could actually falsify. **Project question:** if GA evaluates processing a recorded open E2 or its guitar-engine render, does placing a chosen EQ before compression change the attack and level behavior compared with placing that *same* EQ afterward? A processing decision needs measured outputs from the same input, not a generic rule about which order sounds more natural.

The [GAS-001 fixture](../../../fixtures/guitar-acoustics/gas-001/README.md) gives us a concrete guitar pair: a four-second, mono, 44,100 Hz recorded open E2 WAV and a four-second, mono GA native-rendered E2 WAV. The recorded attack begins **approximately 1.1 s** into the file, with another attack near **2.75 s**; the render begins at file time zero. The [fixture measurements](../../../fixtures/guitar-acoustics/gas-001/measurements.json) report different partial balances and decay in selected windows, but they do not rank realism or establish that either file needs compression. Keep both original WAVs untouched. For this lesson, use the *recorded* file as the proposed first input and the render only as a later, separately labeled replication. Do not compare processed audio against an unprocessed file as though order alone caused the difference.

The [GA browser audio engine at pinned commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) loads a WASM engine into an [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), connects it to speakers, and offers a MediaRecorder path. The GAS-001 render came from a **native build of the same Rust source**, not a capture from that worklet. The inspected source is provenance for the guitar signal path, not evidence of an EQ/compressor chain in the demo. At [IX commit `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), `FirFilter` supplies low-pass and high-pass design and a sample-domain `apply` method. That is a possible offline filter building block. No compressor implementation is established by these pinned artifacts; one must be specified and reviewed before a real A/B run.

## 1. State the two operations precisely

An FIR filter is linear: with coefficients `h`, its output is `E(x)[n] = Σ_k h[k] x[n-k]`, with an explicit boundary rule. IX's `FirFilter::apply` starts with zero-filled output and only includes terms whose input index is nonnegative. A low-pass or high-pass filter can alter the level entering a later detector. The exact response depends on its coefficients, and a filter can also shift or smear an attack. Calling every filter setting “corrective EQ” does not show that it improves a guitar signal.

A compressor is **level dependent**. Its gain depends on the input and, in a conventional design, on a detector envelope with attack and release state. The waveform may change according to threshold, ratio, detector type, time constants, channel linking, makeup gain, and initialization. Those details must be recorded. A compressor is not automatically frequency selective: a full-band detector responds to the level of its input waveform, which can be affected by multiple partials. “The compressor hears 200 Hz” is an informal description, not a guarantee about which component triggered gain reduction. Sidechain filtering, multiband compression, and dynamic EQ would be different experiments.

Let `E` be the chosen EQ and `C` the compressor. The two proposed chains are `A = E(C(x))` (**Comp→EQ**) and `B = C(E(x))` (**EQ→Comp**). The same `x`, EQ coefficients, compressor parameters, sample rate, and channel format must be used in both. `C` sees raw `x` in A and filtered `E(x)` in B. The final EQ in A cannot undo a detector decision that the compressor already made. Conversely, the compressor in B can act on peaks created or removed by EQ. Neither order is a universal default; the intended sound and measured tradeoffs determine the choice.

### Practice exercise 1: identify the detector input

For A and B above, what exactly enters `C`? If the EQ increases a selected guitar partial, which chain *might* change compressor gain reduction because of that increase?

> **Answer:** In A, `C` receives the unfiltered `x`; in B, it receives `E(x)`. The selected partial increase can affect the full-band detector directly in B. In A, EQ occurs after the compressor and cannot change its earlier gain decision. This is a causal path statement, not a prediction of audibility or the amount of gain reduction.

## 2. Prove order dependence with a synthetic fixture

Use a deliberately simple **synthetic** four-sample signal `x=[0,2,0,0]` with zero prehistory. Define the FIR `E` by `h=[0.5,0.5]`, so `E(x)[n]=0.5x[n]+0.5x[n-1]` for available samples. This two-tap average is a mathematical low-pass example, **not** a recommended guitar EQ setting or the coefficients returned by IX's `lowpass` designer. Define a memoryless teaching compressor with threshold `T=1`, ratio `R=2:1`, no makeup gain, and no attack/release: `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. It maps a positive sample of `2` to `1.5`. A real envelope compressor would require additional state and could yield different numbers.

Compute A: `C(x)=[0,1.5,0,0]`, then `E(C(x))=[0,0.75,0.75,0]`. Compute B: `E(x)=[0,1,1,0]`, then `C(E(x))=[0,1,1,0]`, because neither nonzero filtered sample exceeds the threshold. The output arrays differ at samples 1 and 2 by `0.25`. This is an exact counterexample to `E∘C = C∘E` for these declared operators. It does **not** measure the GAS-001 recording, predict the output of an unspecified plugin, or prove that B sounds better.

The different peak values, `0.75` for A and `1` for B, also warn against judging order by uncontrolled loudness. A listening comparison needs a declared playback level match applied **after** each full chain, with the matching gains logged. Do not alter thresholds separately to force similar gain reduction; that would change the experimental question. If both chains stay below threshold on some real passage, they can become identical or nearly so despite the synthetic counterexample.

### Practice exercise 2: calculate both chains

Using the declared `x`, `h`, and `C`, write A and B. What is `B[1]-A[1]`, and what conclusion does this calculation justify?

> **Answer:** `A=[0,0.75,0.75,0]`; `B=[0,1,1,0]`; `B[1]-A[1]=0.25`. The specified operators do not commute on this synthetic input. The calculation alone gives no listening verdict and no result for a real envelope compressor or guitar WAV.

### Practice exercise 3: handle the boundary

With zero prehistory and `h=[0.5,0.5]`, what are `E([2,0])[0]` and `E([2,0])[1]`? Why must an offline harness record its boundary and latency treatment?

> **Answer:** They are `1` and `1`. At index 0 the missing previous sample contributes zero; at index 1 the previous input sample is `2`. A different padding or warm-up rule changes the onset samples. Longer practical FIRs can add group delay, so onset comparisons need aligned outputs and a logged boundary rule before interpreting a peak-time difference.

## 3. Design a falsifiable guitar A/B harness

The following is a **proposed offline experiment, not an executed run**. Start from the recorded `deb-low-e-open.wav` in the [fixture directory](../../../fixtures/guitar-acoustics/gas-001/README.md), whose SHA-256 is `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. Decode its mono float32 WAV samples once and retain the original bytes. Record the decoder, sample rate, input hash, and approximate first onset; inspect the waveform before fixing a comparison interval that excludes the second attack. A second run may use `ga-engine-e2-open-4s.wav`, but report it separately because its source is a native render with different onset and provenance.

Before implementing the future compressor, write a parameter contract: threshold in dBFS, ratio, attack and release units, peak or RMS detector, lookahead, knee, makeup gain, state reset, and behavior at the first sample. Pin its code revision and tests. Use one deterministic EQ: either publish literal FIR coefficients or pin the [IX filter source](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) and log cutoff, order, coefficients, and boundary handling. Use the *same* compressor and EQ settings in both orders; reset compressor state independently before each render. Export lossless A and B WAVs at the same sample rate, and save the compressor gain-reduction trace, sample count, and processing manifest. Do not claim that GA or IX already provides this combined chain.

Choose the first-pluck window relative to the **approximately 1.1 s** recorded onset, with the chosen sample index written in the manifest. Report peak sample and time, short-window RMS or envelope near attack, later RMS, and the gain-reduction trace for each chain. Use a matched output level when listening, and report the applied match so the raw and matched measurements are not confused. Avoid clipping after makeup or level matching. If FIR latency differs from any bypass path, align using a documented delay or cross-correlation rule before comparing peak time. A listener trial, if later approved, should blind labels, randomize order, and allow “no discernible difference”; it is separate from numerical verification.

The **falsifier** for the narrow hypothesis “EQ placement changes this guitar passage under these pinned settings” is that A and B remain sample-identical within a predeclared numerical tolerance, or that any apparent difference vanishes after correcting an alignment, reset, or level-handling mistake. If they differ, inspect detector input and gain-reduction traces to attribute the mechanism. A difference is not proof that either order is more natural. If the chosen EQ is neutral or the compressor never crosses its threshold, a null result is plausible and useful. A claim that one order better preserves the guitar attack would require a declared attack metric, a direction, an acceptable tolerance, and a listener check where perception is part of the claim.

### Practice exercise 4: keep the fixture valid

A proposed harness processes the recorded WAV from file time `0.0–1.0 s`, compares it with the render over the same file-time interval, and concludes that EQ→Comp preserved the guitar attack better. Name two independent problems with this conclusion.

> **Answer:** The recorded first attack is only near `1.1 s`, so its `0.0–1.0 s` window is mainly lead-in, while the render starts at zero. The windows are not onset aligned. Also, a comparison across two different source files does not isolate processing order; the order comparison must use the **same source WAV** in A and B. Neither fixture is a validated realism benchmark.

### Practice exercise 5: choose the next check

A future run finds A and B differ by `0.2 dB` in the first-pluck RMS window, but the outputs have not been aligned and the compressor settings manifest is missing. Does that support a preferred order? What evidence should be requested?

> **Answer:** No. First preserve the input hash and window, publish the compressor version and settings, verify independent state resets, align latency and onset, confirm equal EQ coefficients and absence of clipping, then rerun and compare raw measurements and gain-reduction traces. Match playback level after processing for a separate blinded listening check if the claim concerns sound quality. The reported `0.2 dB` alone cannot identify which stage caused the difference or establish a preference.

## Evidence and limits

- The [GAS-001 fixture README](../../../fixtures/guitar-acoustics/gas-001/README.md) documents the recorded and native-rendered E2 files, hashes, attribution, approximate onsets, and measurement limits. The [GAS-001 lesson](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) and its saved measurements concern the *raw* comparison, not an EQ/compression trial.
- Pinned [GA browser routing](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) and [worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) establish the guitar demo path, while pinned [IX FIR code](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) establishes an available filter operation. They do not establish an implemented compressor, an EQ/compressor order test, or a processed-WAV outcome.
- The four-sample calculation is synthetic. The offline A/B harness, thresholds and metrics are proposed. No compressor was built or run for this lesson; no processed guitar WAV, blind listener verdict, or production routing decision exists here. Subject, learner, and fluent-language reviews, Learn deployment, and anonymous public readback remain pending. The 2026-03-23 research record remains a historical vocal-oriented artifact; this revision uses the new research cycle below.
