---
module_id: gas-001-open-string-audio-evidence
department: guitar-acoustics
course: What an Open-String Recording Can Teach a Guitar WASM Engine
level: beginner
prerequisites: []
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-04-001
version: "0.1.0"
---

# What an Open-String Recording Can Teach a Guitar WASM Engine

> **Department of Guitar Acoustics & Sound Synthesis** | Level: Beginner | Estimated duration: 40 minutes | Status: review pending

## Objectives

After this lesson, you will be able to:

- build a comparable pair from a recorded open string and a note rendered by GA's existing Rust/WASM guitar engine;
- locate the note onset before measuring pitch, partials, or decay;
- use a windowed FFT for local harmonic peaks and wavelets for the changing attack and partial envelopes;
- separate a measurable audio difference from a judgment of perceived realism;
- place an experimental ComfyUI audio candidate in an offline evaluation loop before changing the real-time WASM engine.

## The project question and fixture

GA already has a [Rust guitar engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) loaded by a browser [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js). It uses plucked-string feedback, body resonators, attack noise, and reverb. GA also has an [offline record-and-critic loop](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1) with optional DDSP coloration. There is **no ComfyUI audio handoff in the inspected GA source**. The intended path for this project is an offline ComfyUI experiment followed by controlled measurements, listening, and only then a change to the existing WASM engine. It does not require running a generative model inside the AudioWorklet.

This lesson uses the fixed pair in `state/streeling/fixtures/guitar-acoustics/gas-001/`:

| Fixture | Identity and source | Boundary |
|---|---|---|
| `deb-low-e-open.wav` | A 4-second mono acoustic guitar recording, labeled `source=deb`, `low_E`, `fret=0`, `E2` in the [`collegefishiesd` dataset at revision `a33a262`](https://huggingface.co/datasets/collegefishiesd/guitar-fretboard-notes/tree/a33a26243e88e7ccd4893bee30eac3219ec8bef8). The file is [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) and is attributed in the [fixture README](../../../fixtures/guitar-acoustics/gas-001/README.md). | The label is supplied by the dataset; the recording session was not independently observed. |
| `ga-engine-e2-open-4s.wav` | A 4-second mono render of the pinned GA engine at 44,100 Hz, default profile 0, `engine_note_on(82.4069, 0.1)`, made by the [fixture renderer](../../../fixtures/guitar-acoustics/gas-001/render-ga-e2.py). | A native build of the same Rust source produced it; it is not a capture of the browser AudioWorklet. |

The two WAVs and a [measurement script](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) are reviewable in the source repository. Publication must copy these assets or provide stable links. Their exact SHA-256 values, method, and attribution are in the [fixture README](../../../fixtures/guitar-acoustics/gas-001/README.md). A nominal E2 frequency of 82.4069 Hz defines the target note; a measured spectral peak need not land at that exact number.

### Practice exercise

GA also has a long `by-the-lake.wav` reference used by its spectral critic. Why is the labeled `low_E`, `fret=0` clip the appropriate fixture for this question?

> **Answer:** The dataset identifies one open E2 note and its source. `by-the-lake.wav` is a longer recorded reference with no verified isolated open-string identity; treating its first four seconds as one E2 note would make the comparison invalid.

## 1. Find the event before analyzing the sound

The recorded fixture has a quiet lead-in. Its first attack is approximately **1.1 seconds** into the file, and another attack appears near **2.75 seconds**. The GA render starts at zero. A global FFT over each whole four-second file would mix silence, attacks, and decays; even a local FFT from 0.2 to 1.2 seconds of each *file* would analyze mostly pre-attack material in the recording. Align analysis windows to the first onset and stop before the second recorded attack.

For this fixture, the [measurement script](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) takes a Hann-windowed one-second spectrum from **0.2 to 1.2 seconds after each first onset**. It compares RMS over 0.2–0.4 and 1.0–1.2 seconds after onset. The onset markers are approximate, chosen from short-window levels; another analyst should inspect the waveform and repeat the result after moving the marker slightly. [Audacity's spectrum guide](https://manual.audacityteam.org/man/plot_spectrum.html) explains why frequency resolution and the selected time window are linked.

### Practice exercise

A script reads both WAVs from file time 0.2 to 1.2 seconds and reports that the recording has no E2 partials. What must be corrected before making a claim about the guitar?

> **Answer:** Locate the recording's first attack and shift its window relative to that onset. The chosen file-time window mostly precedes the recorded note. Keep the second attack out of the decay window and report the approximate onset choice.

## 2. Use FFT peaks and wavelet tracks for different questions

A **windowed FFT** answers what frequencies were strong within one selected interval. This is useful for checking a local E2 peak and the relative size of nearby harmonics. It does not tell when each partial appeared or how it evolved. A **short-time Fourier transform (STFT)** slides that window over time and can analyze nonstationary audio, but its time and frequency resolution are fixed by the chosen window. [SciPy documents this time-resolved STFT use](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html).

A **complex wavelet track** uses a frequency-dependent time scale. In our script, six-cycle Morlet-style wavelets track target frequencies near 82, 165, and 330 Hz. They add a view of each partial's attack and later level. Their center frequencies, cycle count, and onset choice affect the answer; they are not a perceptual score. [Published guitar-timbre research](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218) also uses continuous wavelet analysis to study changing partial energy.

The fixture gives these results under its stated windows:

| Measurement | Recorded E2 | GA-rendered E2 |
|---|---:|---:|
| Peak near E2, local FFT | 83 Hz | 82 Hz |
| Second partial relative to first, local FFT | +7.0 dB | −16.9 dB |
| RMS level change, late minus early | −3.9 dB | −1.1 dB |
| Wavelet second-partial change, late minus early | −4.5 dB | −12.9 dB |

The reference and render have very different absolute recording levels, so compare *within-file ratios* before discussing their spectral shape or decay. The second-partial comparison shows a difference of 23.9 dB in this local spectral measure; it does not say that one audio file is 23.9 dB louder overall or more realistic. The wavelet result suggests the second partial falls faster in the render under this method. Inspect the waveform and listen before attributing that difference to one engine parameter.

### Practice exercise

Which tool would you choose to locate a fast pluck attack, and which measurement would you use to compare the exact local harmonic peaks? What does neither measurement prove?

> **Answer:** Use a time-resolved view such as the wavelet tracks or STFT for attack timing, then a stated-window FFT for local peak frequencies and relative levels. Neither proves perceived realism, especially from a single note and one recorded instrument.

## 3. Convert differences into a controlled WASM experiment

The [GA Rust engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) exposes decay, brightness, dispersion, attack decay, reverb mix, and guitar profile controls. A weak upper partial in this one comparison is a reason to **test** a brightness or excitation change, not a reason to declare it correct. Change one parameter or a small, recorded set; render the same E2 fixture again; preserve the before/after WAVs and code revision. Check peak safety, pitch, partial tracks, attack, and output latency across more than one string and velocity. Then conduct a level-matched listening comparison with guitarists. [Karplus and Strong's original plucked-string paper](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf) describes time-varying harmonic decay, which a single spectral snapshot cannot capture.

ComfyUI can supply an **offline candidate** for this loop. Its current core includes [audio load, preview, and save nodes](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py), and official workflows include [audio generation](https://github.com/Comfy-Org/ComfyUI/blob/master/blueprints/Audio%20Generation%20%28Stable%20Audio%203%20Medium%20Base%29.json). A processed or generated E2 candidate must carry its input hash, workflow JSON, model/version, seed, prompt, settings, output hash, format, and license. Verify that it is still a single E2 event before adding it as a **third arm** next to the recorded reference and GA baseline. If the output is FLAC or MP3, use a lossless export or a documented conversion for measurement; lossy compression can change the spectrum. GA's current offline loop uses DDSP or spectral coloration, not ComfyUI, so connecting these artifacts is future integration work.

This can become an **agentic dogfooding loop**: record GA's own baseline, let an agent propose one testable sound change, use ComfyUI to explore an offline candidate when useful, render the changed WASM engine, and compare every artifact against the same external recording. Log the parameter diff, hashes, measurements, listening result, and accept/reject decision. The proposing agent's own heuristic score is a diagnostic, not the only judge of its output; a fixed measurement procedure and a separate listening check keep the loop from rewarding its own preference. A rejected attempt still teaches the next cycle which change failed.

### Practice exercise

A ComfyUI output sounds brighter than the GA baseline. Its prompt, seed, source file, and model version are missing. Can it be used as an engineering target for the WASM engine? Name two controls for a valid next run.

> **Answer:** Not yet. Record the exact workflow/model/seed and source and output hashes, and confirm the output remains an isolated E2 note. Compare it at matched playback level with the same recorded and GA baseline, then change a documented engine parameter and remeasure. Have a separate listener or evaluator check the result; the agent that proposed the change cannot validate it solely with its own score. A bright sound alone does not identify a safe change.

## 4. State what remains unknown

This pair supports a narrow observation: both files contain energy near E2, but their selected partial ratios and time courses differ. It does not establish which is more convincing to listeners. The recorded guitar, microphone, room, playing force, and dataset processing differ from GA's native render. One pitch cannot establish behavior across the fretboard, chords, or playing dynamics. Wavelets reveal timing information but do not replace listening or solve all source mismatch.

Two audible properties the local FFT cannot settle are the **shape and feel of the initial pluck** and **how the instrument responds to different playing strengths**. A single E2 pair cannot establish either across use cases. A listening test should include blinded, level-matched examples, multiple strings and velocities, and a record of participant judgments. The GA [spectral critic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/scripts/run-spectral-critic.js) offers advisory feature comparisons, not a validated realism verdict.

### Practice exercise

Write the strongest claim supported by the table, then name two observations needed before saying "the new WASM engine sounds more like a guitar."

> **Answer:** The measured E2 pair differs in second-partial level and its time course under the stated method. A stronger realism claim needs level-matched listening judgments and repeat measurements across other notes or velocities, with source and recording conditions documented.

## Key takeaways

- Align onsets before comparing a recorded note with a synthetic note.
- A local FFT measures peaks in a chosen window; STFT and wavelets reveal changes over time.
- A numerical mismatch is a useful hypothesis for an engine experiment, not a perceptual verdict.
- ComfyUI belongs in the offline candidate and evaluation loop; the existing GA Rust/WASM engine remains the real-time renderer.
- Dogfooding gives the agent a GA output to improve; fixed evidence and an independent listening check decide whether the iteration helped.
- Keep the recorded reference, generated candidate, code revision, method, and listening results separate.

## Sources and limitations

- [Fixture provenance, hashes, scripts, measurements, and audio-license attribution](../../../fixtures/guitar-acoustics/gas-001/README.md).
- GA [Rust engine](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), [AudioWorklet bridge](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [offline loop](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), pinned to `dc2e74c`.
- [Karplus and Strong, *Digital Synthesis of Plucked-String and Drum Timbres*](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf); [Audacity Plot Spectrum](https://manual.audacityteam.org/man/plot_spectrum.html); [SciPy ShortTimeFFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html); [guitar wavelet analysis](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218).

*Research: `guitar-acoustics-2026-10-04-001`. The method and translations still need subject and native-language review. No browser AudioWorklet capture, ComfyUI handoff, or listening-panel verdict has been completed for this fixture.*
