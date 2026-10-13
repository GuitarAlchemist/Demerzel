# PHY-004 velocity and pick-position arithmetic

This dependency-free fixture reproduces **selected formulas**, not the output waveform, from GA commit `dc2e74cbd992a298f67efb928b5b3754615e1924`, `Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs`, `Engine::excite` lines 281–365. Run `python evaluate_pick.py` here or at its repository path. The script checks the expected delay-buffer length, pick offsets, `pluck_mix`, and ordering across three declared velocity inputs.

The E2 frequency `82.4069 Hz` and 44.1 kHz rate are controlled synthetic inputs. The 535-sample buffer is `floor(44100/82.4069)`. The fixture deliberately avoids the pseudo-random excitation, attack smoothing, feedback filter, body resonators, reverb, browser host, WAV generation, and listening. Thus its numbers establish a parameter coupling in the pinned source, **not** the spectrum or perceived timbre of a real render. In the source, `pluck_mix` also enters the brightness expression in `render`; this fixture only calculates its initial value.

To challenge the lesson, compare a pinned GA build with a controlled alternative that holds pick position and brightness inputs fixed while velocity alone varies, saving source/build identity, engine rate, output WAV hashes, levels, and onset-aligned spectra. No such comparison is included here.
