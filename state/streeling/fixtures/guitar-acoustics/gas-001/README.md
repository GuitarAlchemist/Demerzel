# GAS-001: recorded and GA-rendered open E2

This fixture supports the draft course `gas-001-open-string-audio-evidence`. Both WAV files are 4 seconds, mono, 44,100 Hz. They are an exercise pair, not a validated realism benchmark.

## Provenance

| File | Source | SHA-256 |
|---|---|---|
| `deb-low-e-open.wav` | Unmodified WAV returned for `source=deb`, `string_name=low_E`, `fret=0`, `note_name=E2`, `test` row 39 in [`collegefishiesd/guitar-fretboard-notes` at revision `a33a26243e88e7ccd4893bee30eac3219ec8bef8`](https://huggingface.co/datasets/collegefishiesd/guitar-fretboard-notes/tree/a33a26243e88e7ccd4893bee30eac3219ec8bef8) | `03a1965f275f0858BE70476DAB2BF55D2CBF2272EF7A50C61453D45E7F38B248` |
| `ga-engine-e2-open-4s.wav` | Rendered from the GA [`guitar_engine` Rust source at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) with `render-ga-e2.py`: native release build, default guitar profile 0, one `engine_note_on(82.4069 Hz, velocity 0.1)`, 44,100 Hz, 4 seconds, mono PCM16 | `A78A70243A81AA79D806D9EF3DB7BAA1385C479505F7D5E97B8BF0C7866C3F98` |

The recorded sample is by **collegefishiesd**, distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) as stated on the [dataset card](https://huggingface.co/datasets/collegefishiesd/guitar-fretboard-notes). Attribution and that license apply to the recorded WAV. It is a separate audio file; the lesson's prose is not presented as a derivative of the recording. The dataset describes it as an acoustic guitar captured by player 1. We did not independently verify the instrument or string by watching the recording session.

The GA waveform was rendered through a native build of the same Rust engine source used by the WASM demo. It is not a browser AudioWorklet capture; packaging, sample format, and runtime can differ. The source engine fixes its random seed in `Engine::new`, but a different compiler or platform may produce small byte-level differences. Record the toolchain when regenerating.

## Regenerate and measure

Build the pinned GA `Rust/guitar-web-wasm-demo/rust-engine` source with `cargo build --release`. On Windows, the resulting library is `target/release/guitar_engine.dll`. From this directory:

```powershell
python render-ga-e2.py --library <path-to-guitar_engine.dll> --output ga-engine-e2-open-4s.wav
python measure-pair.py --output measurements.json
```

`measure-pair.py` needs NumPy and SciPy. It uses a Hann-windowed 1-second FFT from 0.2 to 1.2 seconds after each first onset, searches within ±8 Hz of the first six integer multiples of 82.4069 Hz, and reports each peak relative to the first. It also compares RMS in the 0.2–0.4 and 1.0–1.2 second windows after the first onset. A six-cycle complex Morlet-style wavelet tracks the first, second, and fourth target partials through time and reports their late-to-early level changes. The first recorded onset is **approximately 1.1 seconds**; the file has a quiet lead-in and another attack near 2.75 seconds. The generated note starts at time zero. These manually chosen onset markers and short windows are part of the method, not exact ground truth.

## Measured example

| Measurement | Recorded E2 | GA-rendered E2 |
|---|---:|---:|
| Peak near fundamental, 1-second FFT | 83 Hz | 82 Hz |
| Second partial relative to first | +7.0 dB | −16.9 dB |
| Fourth partial relative to first | −5.3 dB | −39.8 dB |
| RMS change, late minus early | −3.9 dB | −1.1 dB |
| Wavelet second-partial change, late minus early | −4.5 dB | −12.9 dB |

The complete output is in `measurements.json`. These values establish differences in the selected windows and analysis method. They do **not** rank perceived realism. A 1-second FFT is only a local summary; the wavelet track adds a time-resolved view whose result depends on its center frequency and six-cycle width. Absolute RMS levels are not comparable without playback-level calibration, and the recorded file's second attack must not be folded into a single-note decay estimate. The GA demo's existing [`compute-spectral-profile.js`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/scripts/compute-spectral-profile.js) reports approximate features and should not be treated as a pitch or perceptual oracle.

## AUD-004 synthetic time-frequency comparison

`compare-time-frequency.py` generates declared 40 ms Hann-gated bursts at E2 harmonics 1, 2, and 4, then compares a Python reproduction of the pinned IX Hann-window/rFFT spectrogram arithmetic at 2,048 and 8,192 samples with this fixture's Morlet-style kernel. It runs clean and fixed-noise arms and writes `synthetic-time-frequency.json`. Regenerate from this directory with NumPy and SciPy installed:

```powershell
python compare-time-frequency.py --output synthetic-time-frequency.json
```

All four fourth-partial bursts were detected per method. The saved medians are 2.313 ms absolute timing error for each fixed-window STFT and 0.034 ms for Morlet. The 2.279 ms difference against the longer STFT falls short of the lesson's declared 5 ms teaching threshold, despite 51.021 dB minimum wrong-center separation for Morlet. The threshold claim therefore fails in this **synthetic** run. The receipt records the script hash, library versions, selected bins, calibration gains, and all event scores. It does not run an IX binary, process either guitar WAV, measure listening quality, or establish a WASM engine benefit.
