---
module_id: phy-002-time-frequency-guitar-transients
department: physics
course: Choose a Time-Frequency View for a Guitar Transient
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-11-002
version: "0.1.0"
---

# Choose a Time-Frequency View for a Guitar Transient

> **Department of Physics** | Intermediate | 35 minutes | English draft; subject and learner review pending

## Objectives

You will answer a precise signal-analysis question: **can an FFT analyze a guitar note whose spectrum changes over time, and when should a GA analyst use an STFT or wavelet track instead?** You will separate a transform's valid computation from the claim its display supports, calculate a window trade-off, and interpret the pinned open-E measurements within their selected time intervals. [PHY-001](phy-001-science-of-guitar-sound.md) introduces harmonics; [GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) discusses the fixture's guitar-engine and listening questions. This lesson stays with the time-frequency method.

## 1. A global FFT is valid, but its spectrum has no event labels

Use the pinned [GAS-001 fixture and provenance](../../../fixtures/guitar-acoustics/gas-001/README.md) at Demerzel commit [`5c49674`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001). Both WAVs are four-second, mono, 44,100 Hz files. The recording's first onset is approximately **1.1 seconds** into the file, and another attack occurs near **2.75 seconds**. The GA-rendered note begins at file time zero. These are different event layouts even though both files are labeled open E2.

A discrete Fourier transform can be computed on **any finite sampled signal**, including a nonstationary one. It does not require the guitar to hold one constant spectrum. The problem is interpretation: one magnitude spectrum over all four seconds pools the quiet lead-in, attacks, and decays. A strong 165 Hz bin would not say which attack contributed that energy. The full complex transform retains phase and can be inverted; it is the **single, global magnitude view** that lacks a time axis for the event question. A four-second sample gives a nominal frequency-bin spacing of `1/4 = 0.25 Hz` before any padding, but fine bin spacing cannot restore the missing event labels.

### Practice exercise 1

An analyst says, “The recorded E2 changes over time, so applying an FFT is mathematically invalid.” Correct the statement and name the actual limitation of one whole-file magnitude spectrum here.

> **Answer:** The FFT is valid on the sampled recording. Its whole-file magnitude spectrum combines the quiet lead-in, first note, and later attack without saying when a component occurred. It cannot answer whether a partial belongs to the first attack or the later one. Use a selected time window or a time-resolved transform for that question.

## 2. Window the question, not just the data

The pinned [measurement script](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) chooses an approximate onset for each file and takes a **Hann-windowed one-second FFT from 0.2 to 1.2 seconds after that onset**. Thus the recording's FFT analyzes approximately file time **1.3–2.3 seconds**, while the render uses **0.2–1.2 seconds**. The recorded second attack near 2.75 seconds is outside the chosen spectral interval. At 44,100 Hz, the one-second window contains 44,100 samples and its unpadded FFT bins are spaced **1 Hz**. A Hann window reduces edge leakage but broadens spectral peaks; bin spacing alone is not a guarantee of resolving two nearby tones.

The rerun of `measure-pair.py` reproduced the saved [measurements](../../../fixtures/guitar-acoustics/gas-001/measurements.json): the local first-partial peak was **83 Hz** for the recording and **82 Hz** for the render. Those are picked bins within the script's ±8 Hz search around the E2 target of 82.4069 Hz. The numbers describe this window and peak-picking rule. They do not establish that the two sources have a one-hertz pitch difference. Changing the onset marker or window can change a nonstationary note's local spectrum.

### Practice exercise 2

What interval of the recorded file does the saved one-second FFT use, and why would file time 0.2–1.2 seconds answer a different question? Calculate its nominal unpadded bin spacing.

> **Answer:** It uses approximately 1.3–2.3 seconds of file time: onset 1.1 plus 0.2–1.2 seconds. File time 0.2–1.2 includes mostly lead-in and only the start of the first note. A one-second, 44,100-sample FFT has bins `44,100 / 44,100 = 1 Hz` apart. That grid spacing does not by itself certify one-hertz resolving power.

## 3. STFT trades spectral detail for event timing

A short-time Fourier transform (STFT) repeats a windowed FFT at successive times. [SciPy's `ShortTimeFFT` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html) describes the window and hop: the window sets the span of samples contributing to each spectrum; the hop sets how often the spectra are reported. The output has both time and frequency axes. A smaller hop produces more overlapping columns, **not** a narrower analysis window or independent extra frequency resolution.

Consider a **proposed** 50 ms Hann window for inspecting the attacks in the GAS-001 files. At 44,100 Hz that is 2,205 samples, with an unpadded bin grid of `1/0.05 = 20 Hz`. It localizes changes much more tightly than the saved one-second FFT, but it gives a much coarser frequency grid and wider spectral peaks. A one-second moving window retains the finer grid but smears a short attack across about a second of context. This is a time-frequency trade-off, not a ranking of tools. The actual fixture did **not** save an STFT; the 50 ms settings and comparison are a design exercise, not measured output.

For a useful follow-up, inspect the waveform for the two onsets, compute an STFT with a declared window and hop, and compare its time labels to the selected one-second FFT. Keep the same WAV hashes and onset convention. If the second attack appears in the windowed display but not in a first-note-only interval, the views are answering different questions as intended.

### Practice exercise 3

At 44,100 Hz, how many samples and what nominal bin spacing does a 50 ms, unpadded STFT window have? Would changing only the hop from 25 ms to 5 ms make two close partials easier to resolve in each column?

> **Answer:** `0.05 × 44,100 = 2,205` samples and `1/0.05 = 20 Hz` nominal bin spacing. A 5 ms hop creates more overlapping time columns; it does not change the 50 ms samples inside each column or their intrinsic frequency discrimination. Use a longer window to improve separation of close frequencies, accepting poorer timing localization.

## 4. A wavelet track changes its time span with frequency

The fixture script also computes **complex Morlet-style wavelet tracks** at selected centers near **82.41, 164.81, and 329.63 Hz**. It chooses a width from `sigma = 6/(2π × center_hz)`, so a lower-frequency track spans more time than a higher-frequency one. This is the source of its frequency-dependent time scale. [PyWavelets' continuous-wavelet guide](https://pywavelets.readthedocs.io/en/latest/ref/cwt.html) explains the general scale-to-frequency relationship; GAS-001 uses its own explicit convolution kernel, not `pywt.cwt`.

The saved artifact reports the second partial's level change from **0.2–0.4** to **1.0–1.2 seconds after the selected onset** as **−4.5 dB** for the recording and **−12.9 dB** for the render. Under this kernel and these intervals, the render's second-partial track has an **8.4 dB more negative** late-minus-early change. A local one-second FFT can report a second-partial level averaged over its interval, but it cannot alone report this change between two subintervals. The wavelet numbers are within-file ratios; they are not an absolute loudness or sound-quality comparison.

Wavelets do not escape the time-frequency trade-off. A broader low-frequency wavelet can blur a fast onset; a higher-frequency wavelet with shorter time support has broader absolute frequency bandwidth. Center choice, width, boundaries, and approximate onset all matter. This three-frequency track also cannot describe every spectral component. A targeted STFT or another wavelet setting may be preferable for a different question.

### Practice exercise 4

Compute the difference between the two saved second-partial late-minus-early changes. What can that difference establish, and what cannot it establish?

> **Answer:** `−12.9 − (−4.5) = −8.4 dB`: the render's tracked second partial fell 8.4 dB more under the saved method. This establishes a difference in these chosen within-file wavelet envelopes and intervals. It does not establish a pitch error, overall volume difference, causal engine parameter, or perceived realism.

## 5. Match a method to a falsifiable claim

For this fixture, use the local FFT for the question “Which peaks are strong during the selected first-note interval?” Use STFT when the question is “When does spectral energy change across the two attacks?” Use the saved wavelet tracks when the question is “How do these three chosen partial envelopes change after the aligned onset?” Keep the window, hop or wavelet width, onset marker, sample rate, and file hashes with every result. Change one analysis choice at a time and show whether the conclusion persists.

A falsifiable exercise for a later run is: with the recorded onset set near 1.1 seconds, a time-resolved display should distinguish the later attack near 2.75 seconds from the first-note interval. If a claimed first-note-only measure includes the later attack, inspect its time bounds and reject that claim. This is a check on analysis scope, not a listening or engine verdict.

### Practice exercise 5

A teammate shows the saved 83 Hz and 82 Hz peaks and claims, “The recording and render differ by exactly 1 Hz throughout both four-second clips.” What is the strongest supported statement, and which time-resolved check would test the broader claim?

> **Answer:** Under the saved onset-aligned, Hann-windowed one-second peak search, the selected bins were 83 Hz and 82 Hz. The analysis did not estimate pitch through both complete clips. Compute repeated time-local estimates with declared resolution adequate to test a 1 Hz gap, label each time span, and inspect the first note separately from the later recorded attack. A sufficiently resolved estimate showing a different gap would falsify the “throughout” claim; an unresolved gap in a coarse window would leave it unverified.

## Sources and limits

The WAVs, script, and JSON are pinned to Demerzel commit `5c4967454ddc740ed937c87719ca4d71a3522e4b`; the GA render's Rust source is pinned separately to GA commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs). I reran the checked-in Python measurement script against the checked-in WAVs and matched its saved values and file hashes. The onset markers are approximate, the recording's source label comes from dataset metadata, and the render is a native build rather than a browser capture. No STFT output was measured for this lesson. SciPy and PyWavelets documentation support the method descriptions, while the numeric comparisons come only from the pinned fixture. Subject review, learner testing, translation, and publication remain pending.
