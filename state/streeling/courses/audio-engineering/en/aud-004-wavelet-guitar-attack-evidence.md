---
module_id: aud-004-wavelet-guitar-attack-evidence
department: audio-engineering
course: "Choose Wavelet Evidence for a Changing Guitar Attack"
level: intermediate
prerequisites: [aud-003-transient-preservation-gate, phy-002-time-frequency-guitar-transients]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-005
version: "0.1.0"
---

# Choose Wavelet Evidence for a Changing Guitar Attack

> **Department of Audio Engineering** | Intermediate | 40 minutes | English draft; subject, learner, and publication review pending

## Objectives and project decision

By the end, you can explain why an FFT remains valid on a changing signal, distinguish a fixed-window STFT from a frequency-dependent wavelet track, interpret the pinned guitar measurements within their limits, and audit a controlled simulation that rejects a proposed wavelet advantage threshold. This builds on [AUD-003](aud-003-transient-preservation-gate.md), which protects a recorded pluck during optional denoising, and [PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md), which introduces the time-frequency trade-off.

The GA team has a practical question: *when does a rendered open E2 lose harmonic motion relative to a recorded example?* The [GAS-001 fixture](../../../fixtures/guitar-acoustics/gas-001/README.md) at Demerzel commit [`5c496745`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) contains a licensed recorded E2 and a native GA engine render. Each file is four seconds of mono audio at 44,100 samples per second. The recording's first onset is approximately 1.1 seconds into the file, with another attack near 2.75 seconds; the render begins at zero. These different event layouts require onset alignment before a decay comparison. The pair is teaching evidence, not a validated realism benchmark or a browser AudioWorklet capture.

## 1. Select the transform from the claim

A discrete Fourier transform can analyze any finite array of samples, including a nonstationary guitar pluck. A **single whole-file magnitude spectrum** pools events, so it cannot say *when* a partial appeared. A short-time Fourier transform (STFT) repeats an FFT on overlapping windows and labels the resulting spectra by time. IX's [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L54) uses a Hann window of one chosen size for every frequency bin and keeps one-sided magnitudes. Its [agent handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) requires a power-of-two window. This is a usable fixed-resolution baseline for an offline comparison; it is not a live GA guitar analyzer by itself.

The GAS-001 [`measure-pair.py`](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) instead computes three **complex Morlet-style tracks** centered on the first, second, and fourth target partials of E2. Its Gaussian envelope uses `sigma = 6/(2πf)` and a kernel radius of `ceil(4 × sigma × sample_rate)` samples. As center frequency rises, the same formula uses a shorter time span. The saved track is the magnitude of a convolution, not a full spectrogram and not a proof that every nearby frequency is separated. Both STFT and these tracks trade time localization against frequency selectivity; the question decides which compromise to test.

### Practice exercise 1: reject the false premise

A teammate says, “FFT assumes a stationary signal, so the four-second recorded WAV cannot be transformed.” What is wrong, and which output would you request to locate the later attack?

> **Answer:** The finite recorded array has a valid Fourier transform. One whole-file *magnitude* spectrum has no event-time labels, so it cannot attribute a peak to the first or later attack. Request an onset-labeled STFT or another time-resolved view spanning both attacks. A selected first-note FFT is still useful for a local harmonic summary if its interval excludes the later attack.

## 2. Calculate what the variable wavelet span buys

The pinned fixture's E2 target is 82.4069 Hz. Its Morlet-style centers are approximately 82.41, 164.81, and 329.63 Hz. Substituting these into the checked-in kernel formula gives Gaussian `sigma` values of **11.588, 5.794, and 2.897 ms**. The nominal continuous span between `−4 sigma` and `+4 sigma` is approximately **92.70, 46.35, and 23.18 ms** respectively. These numbers are calculations from the source formula; the actual discrete kernels use `ceil` for each radius and therefore have a slightly different endpoint span. The shorter fourth-partial kernel can place rapid changes more tightly in time, while its broader frequency response can make nearby components harder to distinguish. The longer fundamental kernel averages more time and can blur a fast onset.

For comparison, the synthetic run below reproduces IX's 2,048-sample Hann STFT window, about 46.44 ms at 44.1 kHz, with a 512-sample hop of about 11.61 ms. Its longer 8,192-sample window spans about 185.76 ms. Window span does not equal exact onset-estimation error: window shape, threshold, interpolation, noise, and event phase also matter. Reducing the STFT hop adds time samples to the display but does not shorten the window. A Morlet center chosen after viewing a result can likewise make a comparison unfair; declare centers beforehand.

### Practice exercise 2: calculate and interpret support

With `sigma = 6/(2πf)`, what happens to `sigma` when center frequency doubles from about 82.4 to 164.8 Hz? Give the approximate `±4 sigma` span at each center. Does the smaller span prove better pitch discrimination?

> **Answer:** Doubling `f` halves `sigma`: about 11.588 ms becomes 5.794 ms. The approximate full `±4 sigma` span halves from 92.70 to 46.35 ms. This may localize a change in the second-partial envelope more tightly, but the shorter time support does **not** prove better pitch discrimination; the effective frequency bandwidth is broader. The values describe this specified kernel, not measured onset errors.

## 3. Keep three different meanings of “wavelet” separate

IX's [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L82) performs a multilevel **Haar discrete wavelet transform**, soft-thresholds detail coefficients, then reconstructs audio. Its [handler](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797) checks divisibility by `2^levels` so an odd tail is not silently dropped. AUD-003's bounded probe found that three tested thresholds on one recorded excerpt missed its proposed 3 dB provisional noise-reduction gate. A denoiser changes the signal being assessed; the GAS-001 Morlet tracks **measure** unchanged audio. Do not use the denoiser's output as if it were the fixture's Morlet measurement.

GA also has a [`WaveletTransformService`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Wavelets/WaveletTransformService.cs) in its ML layer. It decomposes a scalar time series with Haar or Daubechies-4 and extracts summary statistics. Its documented example inputs include entropy or velocity; inspection of this class does not establish a wired guitar-audio pathway or a GAS-001 Morlet implementation. A future audio pipeline would need explicit sample decoding, time alignment, artifact provenance, and a separately tested feature contract before feeding its output to GA. Naming three methods “wavelets” does not make their coefficients interchangeable.

### Practice exercise 3: choose the right artifact

You need a time trace of energy near the fourth E2 partial from the **unmodified** GAS-001 render. A colleague offers IX Haar `wavelet_denoise` output and a 16-number GA feature vector. Which existing method can produce the requested trace, and what is still missing from the saved artifact?

> **Answer:** `measure-pair.py` computes the targeted Morlet-style fourth-partial envelope from the unmodified fixture audio. The saved `measurements.json` retains its peak time and late-minus-early summary, **not the full envelope array**. Rerun the pinned method and explicitly export the array with sample-time labels to inspect a trace. IX denoising reconstructs a changed waveform rather than reporting that track. GA's scalar-series summary vector discards the required trace and is not shown wired to guitar audio.

## 4. Read the saved measurements without inventing a cause

The [saved GAS-001 measurements](../../../fixtures/guitar-acoustics/gas-001/measurements.json) report the second-partial track's change from 0.2–0.4 to 1.0–1.2 seconds after each selected onset as **−4.5 dB** for the recording and **−12.9 dB** for the GA render. Under this kernel and those within-file intervals, the render's tracked second partial changes by **8.4 dB more downward**. The 1-second local FFT tells a different part of the story: it reports second-partial magnitude relative to the first as +7.0 dB in the recording and −16.9 dB in the render for their respective 0.2–1.2 second intervals. Do not equate that *between-partials* comparison with the wavelet's *late-versus-early* comparison.

The saved wavelet first-0.6-second **peak times** for the second partial are 0.144 seconds after approximate onset in the recording and 0.024 seconds in the render. These are maxima of a selected envelope region, **not verified physical onset times**. Different performances, attack shapes, production chains, level, and approximate onset markers prevent a causal conclusion about an engine parameter. The recorded later attack lies outside these first-note measurement intervals, but it would contaminate a whole-file decay claim.

### Practice exercise 4: respect the denominator

Compute the difference in the two saved second-partial late-minus-early changes. Can you subtract the saved +7.0 and −16.9 dB FFT numbers to call that the same effect?

> **Answer:** `−12.9 − (−4.5) = −8.4 dB`; the render's *within-file* second-partial track falls 8.4 dB more under the saved intervals and kernel. The FFT values each compare the second partial with the first *within one selected one-second interval*. Their difference uses a different denominator and cannot be called the same late-minus-early effect. Neither comparison proves which synthesis component caused it or how a listener ranks realism.

## 5. Run a controlled comparison and reject an overstrong claim

The [synthetic benchmark script](../../../fixtures/guitar-acoustics/gas-001/compare-time-frequency.py) runs a controlled offline trial. It reproduces the pinned IX Hann-window/rFFT spectrogram arithmetic in Python and uses the GAS-001 Morlet-style kernel; **it does not invoke an IX binary**. The separate recorded/rendered guitar follow-up remains unexecuted. In one-second, 44,100-sample synthetic trials for each declared E2 partial center, the script places two 40 ms Hann-gated, phase-zero sinusoids of peak amplitude 0.5 centered at 0.30 and 0.45 seconds. It uses a clean arm and a fixed-seed white-noise arm with noise RMS 0.01. These controlled signals supply ground truth for timing; the recorded guitar does not. The amplitude, gate, and noise settings are declared simulation inputs, not observations of the recorded pair.

The [saved receipt](../../../fixtures/guitar-acoustics/gas-001/synthetic-time-frequency.json) compares three methods with the **same input and scoring intervals**: (1) a Python reproduction of the IX 2,048/512 Hann STFT, (2) the 8,192/512 Hann STFT, and (3) the fixture's pinned Morlet-style kernel at the three declared centers. For each STFT size and target center, it uses the nearest discrete frequency bin (`round(f × window_size / 44100)`), with no interpolation or local-bin search, and records the actual bin frequency. It labels each STFT column by its **window center**, since IX returns frame arrays without a physical time axis. Before scoring bursts, it divides every method/center track by that track's median steady-state response to a separate clean, unit-peak, one-second sinusoid at the declared center, measured from 0.25–0.75 seconds with the same transform settings. Those frozen gains apply to both arms. This convention makes correct-center and wrong-center amplitudes comparable without removing intrinsic resolution limits. For each burst, it picks the maximum calibrated correct-center magnitude within ±60 ms of its known center; it reports timing error, ties, missing detections, and the largest calibrated wrong-center peak. A clean-arm peak must be positive; a noisy-arm peak must exceed the same method/center's noise-only peak in that interval by 6 dB, using the same fixed noise draw. A missing fourth-partial burst rejects the timing claim. The declared hypothesis is limited: the shorter 329.63 Hz Morlet kernel might reduce fourth-partial timing error against the longer STFT while retaining usable frequency discrimination. The teaching gate requires at least **5 ms** lower median timing error than the 8,192-window baseline and at least **6 dB** correct-center separation from the largest wrong-center peak. These thresholds are not project acceptance criteria.

The executed synthetic run detected all four fourth-partial bursts for each method. Median absolute timing error was **2.313 ms** for each STFT window and **0.034 ms** for Morlet, a **2.279 ms** improvement against the longer STFT. Morlet's worst correct-versus-wrong-center separation was **51.021 dB**, above the declared 6 dB gate. The timing improvement is below 5 ms, so the *predeclared advantage claim fails on this synthetic trial*. This does not say Morlet never helps: it achieved a lower synthetic error here, and the fixed-window methods were already close to the ground-truth times. The receipt contains each clean/noisy event and selected frequency bin, allowing the summary to be audited. It is not a listening result, an IX executable test, or evidence of a real-time WASM benefit.

The **unexecuted guitar follow-up** would pin both GAS-001 WAV hashes, the exact script, an IX executable revision, decoder, onset markers, and preprocessing, then repeat the three views on onset-aligned *copies* of the recorded and rendered first note. It would recalculate the second-partial late-minus-early change under declared center-frequency shifts and onset-marker shifts of ±5 ms. Report every setting and whether the sign and rough size of the fixture difference persist; do not treat this sensitivity check as ground truth or a listener test. Keep a link from every plot to its input hash and parameters so the analysis can be rerun or falsified. The close STFT timing in this synthetic run makes a simpler fixed-window baseline especially important. A different synthetic result or a real-guitar advantage would still not automatically justify inclusion in a real-time WASM engine.

### Practice exercise 5: state the falsifier

Read the synthetic receipt: Morlet's median fourth-partial error is 0.034 ms and the 8,192-window STFT's is 2.313 ms; both methods detect four of four bursts, and Morlet's minimum wrong-center separation is 51.021 dB. Does the predeclared claim pass, and which result prevents this from choosing a WASM analyzer?

> **Answer:** `2.313 − 0.034 = 2.279 ms`, below the 5 ms timing threshold, so the declared combined claim fails even though all bursts were detected and 51.021 dB exceeds the 6 dB separation gate. The 2,048-window STFT also reached 2.313 ms on this fixture; that simpler baseline deserves attention. This synthetic, source-compatible Python result does not establish IX binary timing, behavior on either guitar WAV, listener benefit, or WASM latency. Run the pinned real-audio sensitivity and executable checks before choosing an analyzer.

## Evidence and limits

- Audio provenance and saved observations are from the [GAS-001 fixture pinned at `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). The center widths above are independently calculated from its checked-in formula; they are not measured timing errors.
- The inspected IX [`spectral.rs`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs) and [`wavelet.rs`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs) are pinned to `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. GA's scalar-series wavelet service is pinned separately to `dc2e74cbd992a298f67efb928b5b3754615e1924`. This lesson does not attest a running IX binary or a GA browser audio capture.
- The synthetic STFT/Morlet benchmark was executed and its script and complete JSON receipt are checked in. It reproduced pinned IX spectrogram arithmetic in Python, not the IX binary. No new processed guitar audio, guitar sensitivity run, listener trial, subject review, fluent review, Learn import of this revision, or public readback was performed for AUD-004. Publication remains pending.
