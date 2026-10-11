---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Protect a Guitar Pluck During Offline Spectral Analysis"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Protect a Guitar Pluck During Offline Spectral Analysis

> **Department of Audio Engineering** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; review and publication pending

## Objectives

After this lesson, you will be able to:

- choose a whole-interval FFT or an STFT according to the audio decision being made;
- set valid IX spectrogram window and hop sizes while retaining the attack in at least one frame;
- distinguish IX's Haar wavelet denoiser from the frequency-targeted wavelet tracks in the GAS-001 fixture;
- reject a noise-reduction step that changes a guitar transient beyond a declared gate; and
- specify an offline evaluation that another engineer could falsify with the same WAVs.

## The project decision

The [GAS-001 open-E fixture](../../../fixtures/guitar-acoustics/gas-001/README.md), pinned at Demerzel commit [`5c496745`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), contains a licensed recorded open E2 and a GA native-engine render. Both are four-second mono WAVs at 44,100 Hz. The first recorded onset is approximately 1.1 seconds into its file; the render begins at zero. The fixture records a later attack near 2.75 seconds in the recording. It is a teaching pair, not a validated realism benchmark or browser AudioWorklet capture.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) explains the time-frequency trade-off and interprets the fixture's saved FFT and Morlet-style wavelet measurements. [AUD-002](aud-002-level-matched-guitar-comparison.md) controls onset alignment and playback level before listening. This lesson addresses a different engineering choice: **should an offline analyst denoise the recorded reference before using its pluck attack to judge a GA render?** An apparent reduction in noise is not enough. A denoiser can also blunt, spread, or move the transient that the analyst meant to preserve.

The implementation case is pinned to IX commit [`bd1336b7`](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1). IX exposes an [FFT handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), a [spectrogram handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189), and a [Haar wavelet denoising handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). These accept numeric sample arrays, not WAV paths. A WAV decoder and a repeatable offline harness would be needed to apply them to the pinned audio pair; this lesson has not done that run.

## 1. Choose the view from the claim

IX's [`rfft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) transforms a finite real-valued sample array, zero-padding a non-power-of-two length to the next power of two. Despite its name, it returns the full FFT array. The `ix_fft` handler returns magnitudes and frequencies in **cycles per sample**, assuming sample rate 1.0. At 44,100 samples per second, multiply a normalized bin frequency **through Nyquist** by 44,100 to express it in hertz; the upper half mirrors negative frequencies. A whole-file magnitude spectrum is valid for a changing signal, but it cannot label which attack produced a peak. A selected first-note FFT is useful for a local harmonic summary; it still averages over its chosen interval.

IX's [`stft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) repeats windowed FFTs at successive sample positions. [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) uses a Hann window and retains one-sided magnitudes. It can show whether attack-related energy appears in an early frame and how that energy changes. Its `db=true` path computes `20 log10(max(magnitude, 1e-10))`; it is not a calibrated dBFS measure. Do not compare its raw dB numbers directly with the GAS-001 RMS dBFS values.

### Practice exercise 1: choose an output that can answer the question

An analyst computes `ix_fft` on the entire recorded four-second WAV and says the bright peak belongs to the *first* pluck, not the later attack. Which part of the result is useful, and what should be computed before assigning the peak to an event?

> **Answer:** The whole-file FFT can show that the file contains energy near that frequency, after converting cycles per sample to hertz. Its magnitude output has no time label, so it cannot attribute the peak to the first pluck. Decode the WAV, mark the approximate first onset, compute a declared first-note interval separately, and inspect an onset-aligned STFT over both attacks if event timing matters. Keep the raw file and analysis intervals in the record.

## 2. Make IX's STFT settings match an attack question

The IX **agent handler** requires a power-of-two `window_size` of at least two and no larger than the signal. This matters because the underlying FFT otherwise zero-pads a frame and the handler's stated bin count and frequency mapping would be wrong. The handler defaults `hop_size` to half a window, coerces a supplied zero hop to one, and reports `n_frames` and `n_bins`. The core `stft` function does not supply those input guards; an offline harness calling it directly must validate its own arguments. The core processes only complete frames, so it does not silently extend a short tail.

For a **proposed** 44.1 kHz first-attack view, choose a 2,048-sample window and a 512-sample hop. The window spans about **46.44 ms**, the hop about **11.61 ms**, and the FFT grid is `44,100 / 2,048 ≈ 21.53 Hz` per bin; the one-sided magnitude has **1,025 bins**. That grid is too coarse to use a single frame to settle a one-hertz pitch dispute. A larger 8,192-sample window spans about 185.76 ms and has 5.38 Hz bin spacing, but it mixes more of attack and decay. A smaller hop yields more overlapping frames; it does not improve the frequency discrimination of each frame. These are calculations from settings, **not** measured IX output on the WAVs.

### Practice exercise 2: specify a valid IX request

At 44,100 Hz, calculate the span, hop interval, and nominal bin spacing for `window_size=2048`, `hop_size=512`. How many bins should IX's spectrogram handler report? Why would `window_size=2205`, an exact 50 ms, be rejected by that handler?

> **Answer:** The span is `2048/44100 ≈ 46.44 ms`, the hop is `512/44100 ≈ 11.61 ms`, and spacing is `44100/2048 ≈ 21.53 Hz`. The handler reports `2048/2 + 1 = 1025` bins. It rejects 2,205 because it is not a power of two; a direct core call could zero-pad it, but interpreting its bins as if the FFT length were 2,205 would be wrong.

A Hann window tapers to zero at its endpoints. That helps with edge discontinuities, but a transient exactly at an endpoint can vanish from that frame. Overlap makes the same sample land at a different position in another frame. This is an **analysis placement** issue, not a statement that overlap creates new information. The IX [window function](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) and [frame loop](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) make the boundary effect checkable without a guitar recording.

### Practice exercise 3: keep the boundary impulse visible

Take a synthetic 64-sample array that is zero except for value 1 at sample index 16. IX uses a 16-sample Hann window. With hop 16, which complete frame contains the impulse, and what happens to it? What changes with hop 8?

> **Answer:** With hop 16, frames start at 0, 16, 32, and 48. Only the frame starting at 16 contains index 16; it lies at window offset 0, where the Hann weight is zero. All returned spectra can therefore miss this isolated impulse. With hop 8, the frame starting at 8 also contains it at offset 8, whose Hann weight is about 0.989, so that frame reports energy. This is a source-derived synthetic calculation, not an IX WAV measurement. It shows why the proposed 512-sample hop should be checked near real onset boundaries.

## 3. A Haar denoiser can alter the evidence

IX's [`haar_forward`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) forms pairwise averages and differences. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) soft-thresholds detail coefficients and reconstructs the signal. It is a discrete Haar processing step, **not** the frequency-centered complex Morlet-style wavelet track saved in GAS-001. The two methods have different outputs and answer different questions. A Haar detail coefficient can mark a rapid change, yet thresholding it can remove part of a real pluck along with noise.

The IX handler requires `levels >= 1`, a finite nonnegative threshold, and input length divisible by `2^levels`; otherwise it rejects the request because the core Haar transform can drop odd trailing samples. Its checked-in [noise test](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) uses a smooth ramp with alternating added noise and checks lower mean squared error. That test does not check preservation of an isolated guitar attack. The separate [guard tests](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) cover invalid spectrogram size and indivisible wavelet input length.

### Practice exercise 4: predict the transient change

For the synthetic eight-sample signal `[0, 1, 0, 0, 0, 0, 0, 0]`, apply IX's one-level Haar equations with soft threshold 1. What are the first two reconstructed samples? Does this support a claim that wavelet denoising always preserves a pluck peak?

> **Answer:** The first pair has approximation `1/sqrt(2)` and detail `-1/sqrt(2)`. Because its detail magnitude is below threshold 1, soft thresholding sets that detail to zero. The inverse gives `[0.5, 0.5]` for the first pair, leaving the other pairs at zero. The isolated peak drops from 1 to 0.5 and spreads one sample earlier. The calculation refutes an unconditional preservation claim; it does not predict what threshold is appropriate for a recorded guitar WAV.

## 4. Predeclare an offline preservation gate

The following is a **proposed evaluation recipe**, not a run or a GA acceptance standard. Retain both fixture WAVs and their full hashes. Decode each as mono normalized `f64` samples without overwriting it. Record decoder, sample rate, sample count, and any resampling; reject a silent sample-rate change. Use the fixture's approximate onset markers (recording 1.1 s, render 0.0 s) and inspect first-note attack excerpts separately from the recorded later attack. Keep a raw arm and a processed-copy arm at identical sample positions and gain. Run the IX STFT view on both arms with the declared 2,048/512 settings; label frames by **sample start and window span**, not just a visual column center. Record whether the boundary-onset conclusion survives an alternate hop or a small onset-marker shift.

Before any Haar run, declare `levels` and threshold, check the exact input length is divisible by `2^levels`, and save the padding/trimming policy if needed. For example, a 44,100-sample one-second excerpt is **not** divisible by eight for three levels: it leaves remainder four. Padding four zeros to 44,104 is one possible declared choice; it adds a boundary that may affect nearby coefficients. A different excerpt boundary or fewer levels is another choice. Do not call the core function directly on an odd-length input and assume its output stays aligned.

For the recorded reference, measure a stated pre-onset noise interval and a fixed first-attack interval on both raw and processed copies. A **teaching gate**, chosen before seeing the outcome, could demand at least **3 dB** lower pre-onset RMS while retaining the first-attack absolute peak within **10%** of raw and the time of that peak within **1 ms**. Require no clipping and unchanged sample count after any documented trim. Recheck at onset markers shifted by ±5 ms, and report every candidate threshold, including failures. The GA render starts at file time zero, so it has no equivalent pre-onset noise interval; do not apply that particular noise gate to it. Preserve the unprocessed recording as the primary comparison reference. Passing these waveform proxies would permit a separately documented, level-matched listening comparison, **not** prove that the processed file is perceptually unchanged or that GA sounds realistic.

### Practice exercise 5: apply the gate, then state the limit

An engineer proposes a three-level Haar run on a 44,100-sample recording excerpt without padding. The engineer also presents a *hypothetical* candidate with 4 dB lower pre-onset RMS, attack peak 0.82 times the raw peak, and peak-time shift 0.2 ms. What must change before the IX handler accepts the excerpt, and would the candidate pass the teaching gate?

> **Answer:** `44,100 mod 8 = 4`, so the handler rejects three levels on that length. Declare four added samples to reach 44,104 and a trim policy, choose a different excerpt, or reduce the levels. The hypothetical candidate fails even though noise falls by more than 3 dB and timing stays within 1 ms: `1 - 0.82 = 0.18`, an 18% peak loss, exceeds the declared 10% limit. That rejection concerns transient preservation under this proxy gate; it is not a measured result on either fixture WAV or a listener verdict.

## Evidence and limits

- The project audio and provenance come from the [GAS-001 fixture at Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). The recording and native GA render are separate sources with different performance and production chains. Their saved FFT and Morlet results are observations from that fixture, not output from IX.
- The STFT, FFT, Haar equations, handler guards, and tests cited above are IX source observations at `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. The 2,048/512 dimensions, Hann boundary example, eight-sample Haar result, and divisibility arithmetic are **derived examples**. No IX spectrogram or denoised WAV was produced or measured for AUD-003.
- An analysis magnitude is not a calibrated loudness or realism score. The onset markers are approximate; spectral windows, padding, thresholds, decoder, and input gain can change a result. A synthetic impulse exposes a possible failure mode but does not predict the behavior of every pluck.
- Subject review, learner attempts, native-language review, Learn sync/build, and public readback remain pending. This English source is a draft, not a published course.
