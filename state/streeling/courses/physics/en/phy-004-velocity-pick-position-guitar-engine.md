---
module_id: phy-004-velocity-pick-position-guitar-engine
department: physics
course: When Velocity Moves the Pick Position in GA's Guitar Engine
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound", "phy-003-sampling-aliasing-guitar-engine"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-004
version: "0.1.0"
---

# When Velocity Moves the Pick Position in GA's Guitar Engine

> **Department of Physics** | Intermediate | 40 minutes | English source draft; review and publication pending

## Objectives

You will distinguish a physical pluck location from the GA engine's excitation heuristic, calculate how an input velocity changes more than output gain, and design a comparison that can isolate the cause of a timbre change. This is useful when tuning the guitar WASM engine: a musician may request a louder note while expecting the same picking gesture, but the current control path changes several parameters at once. [PHY-001](phy-001-science-of-guitar-sound.md) describes standing waves; [PHY-003](phy-003-sampling-aliasing-guitar-engine.md) establishes why the engine rate must be recorded. Neither lesson resolves this control-coupling question.

The evidence boundary is important. The executable [PHY-004 fixture](../../../fixtures/physics/phy-004/README.md) reproduces **selected arithmetic from pinned source**. It does not synthesize audio, measure a spectrum, or establish what a listener hears. The point of the lesson is to make the competing explanations and a decisive experiment explicit before changing engine code.

## 1. What a physical pluck position predicts

For an ideal flexible string fixed at both ends, write a location as `p = x/L`, where `L` is string length and `0 < p < 1`. A simple model pulls the string to a triangular displacement with its apex at `pL`, then releases it. Resolving that initial shape into standing-wave modes gives a modal displacement coefficient proportional to `sin(nπp) / [n² p(1-p)]` for harmonic index `n`, when the apex height is held fixed. This follows by integrating the two straight pieces of the triangle against the string's sine modes. It is an **ideal initial-displacement model**, not a complete guitar recording model.

The sine term predicts position-dependent zeros: at `p = 1/2`, every even `n` has `sin(nπ/2) = 0`; at `p = 1/4`, every fourth harmonic has `sin(nπ/4) = 0`. A real pick has width, force history, and contact time. String stiffness, termination, pickup location, body coupling, damping, and microphone placement can all alter an observed spectrum. Thus a theoretical mode zero is a good experimental prediction under stated assumptions, not a promise of an exact null in a WAV.

The meaning of **velocity** depends on the interface. MIDI note velocity is a control value in `[0,1]` here, not a measurement of the pick's physical speed or the string's initial displacement. We cannot infer the real pick position from it without a calibrated mapping. A software instrument is free to use one input to control many hidden parameters, but that choice must be visible when evaluating cause and effect.

### Practice exercise 1

For the ideal triangular-displacement model, which harmonic indices have a zero initial coefficient at `p = 1/4`? Would a missing fourth harmonic in a captured guitar note prove that the player plucked at one-quarter of the string?

> **Answer:** The sine factor is zero when `n` is a positive multiple of four: `n = 4, 8, 12, ...`. A missing or low fourth harmonic alone does not prove a quarter-string pluck. Pickup or microphone placement, excitation width, string and body response, processing, noise, and the selected analysis window are alternative explanations. The formula describes one ideal initial displacement under fixed assumptions.

## 2. Follow the actual GA control path

At pinned [GA commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), `engine_note_on(engine, freq, velocity)` calls `Engine::excite`. The function clamps `velocity` into `[0,1]` and sets the active Karplus–Strong buffer length to `max(2, floor(sample_rate / max(freq,20)))`. The fractional remainder is stored separately. For a **controlled arithmetic example**, use `44,100 Hz` and `82.4069 Hz` E2, giving `floor(44,100 / 82.4069) = 535` active buffer samples and a fractional remainder of approximately `0.14936`. As in PHY-003, this rate belongs to the chosen example; it is not a universal browser rate.

The source then computes `pick_ratio = clamp(0.18 + 0.60(1 - velocity), 0.1, 0.85)`. It rounds `535 × pick_ratio` to the nearest positive integer and clamps the offset into the active buffer. Increasing velocity from `0.25` through `0.50` to `0.75` changes the chosen offsets from **337** through **257** to **177** samples, corresponding to normalized positions about **0.630**, **0.480**, and **0.331**. This is an **engine buffer index**, not a measured position in centimetres along a physical guitar string. The code comment calls it a pick-position heuristic; the implementation is the evidence for what it does.

The same velocity also multiplies the filtered-noise excitation, sets `pluck_mix = clamp(0.15 + 0.35 velocity, 0.05, 0.7)`, and helps set the attack level. During rendering, `pluck_mix` enters a brightness expression; the signal then passes through feedback, damping, body resonators, and reverb. Therefore comparing two exported notes at different velocity cannot attribute a spectral difference to gain alone or to pick position alone. The control is **coupled** in the pinned implementation.

### Practice exercise 2

At the fixture's rate and E2 target, calculate the pick ratio and sample offset for velocity `0.50`. What remains fixed when only velocity changes among the three fixture cases?

> **Answer:** `0.18 + 0.60(1 - 0.50) = 0.48`; `round(535 × 0.48) = round(256.8) = 257`. The input sample rate and note frequency are fixed, so the 535-sample integer buffer length and its approximately `0.14936` fractional remainder remain fixed. Velocity changes the ratio, offset, excitation multiplier, `pluck_mix`, and attack level. The calculated offset is not a microphone measurement.

## 3. Reproduce the arithmetic, and stop at its boundary

Run `python state/streeling/fixtures/physics/phy-004/evaluate_pick.py` from the Demerzel root. The dependency-free script reads three declared cases and asserts the pinned formula's buffer length, offsets, and `pluck_mix` values. It checks that the offsets decrease and `pluck_mix` increases as velocity rises. It also evaluates the pre-noise shape at the chosen offset. The model's shape is `clamp(1 - 2.5 |i/N - offset/N|, 0, 1)` for active index `i`, so its peak there equals one by construction. The full Rust excitation multiplies this shape by low-pass-filtered pseudo-random noise and velocity; the fixture intentionally omits that stateful path.

This check rejects the **specific shortcut** “velocity is just a scalar gain control in this source path.” It does **not** reject the possibility that, in a particular rendered note and measurement band, changing gain dominates any timbre change. Formula inspection and a parameter trace establish coupling; an audio comparison is needed to establish perceptual size. The fixed JSON expected values make the teaching example reproducible and make accidental formula drift visible. If GA source changes, the pinned comparison remains a historical statement and needs a new source review.

An easy diagnostic mistake is to translate the normalized offset directly into a real pluck coordinate, then apply the ideal triangular-string zeros from section 1 to GA output. The engine uses filtered noise and a broad clamped shape, not the ideal triangular initial displacement. Its buffer is updated by a feedback loop with interpolation, dispersion, low-pass damping, and resonators. Any modal notch predicted from the ideal formula is therefore a **hypothesis to test** for GA, not a result of this fixture.

### Practice exercise 3

The fixture reports offsets `337`, `257`, and `177` at increasing velocities, while its shape peak is `1` in all three cases. A teammate concludes, “The three rendered WAVs must have identical brightness after level matching.” Identify two reasons the conclusion does not follow.

> **Answer:** First, the shape moves in the buffer; equal peak values do not make the complete shapes identical. Second, velocity also changes `pluck_mix`, which enters the render brightness expression, as well as the filtered-noise amplitude and attack. Stateful noise, filtering, feedback, resonators, and reverb are absent from the fixture. A matched-level render and time-local spectrum or listening trial would be needed to compare actual brightness.

## 4. Design a comparison that isolates the question

Suppose the user reports that a louder E2 in the WASM demo sounds brighter. Begin with the narrow statement the sources support: the pinned Rust code maps velocity into **at least** excitation scale, pick offset, pluck mix, and attack. The browser AudioWorklet may use a context rate different from the example. Log the actual rate, engine build or commit, note and velocity, recording path, duration, output format, and hashes. Compare onset-aligned windows and level-match before judging spectral balance; whole-file spectra can hide attack differences, as PHY-002 explains.

A decisive local experiment would add an **instrumented branch or test-only parameter injection** to hold pick offset fixed while varying velocity, then separately hold `pluck_mix` and attack settings fixed, using the same rate and deterministic noise seed where possible. Run repeated renders and save both parameter traces and outputs. Compare these interventions with the unmodified engine. If fixing pick offset leaves essentially the same measured brightness change, the simple “pick-position shift is the dominant cause” hypothesis weakens. If it removes most of the difference while other controls remain constant, it gains support. Either way, use an explicitly chosen metric, frequency band, onset window, and tolerance before looking at results.

A simpler alternative may suffice for the product: keep the current coupled velocity mapping and describe it honestly, rather than adding a new independent “physical pick position” control. An independent control is useful only if a musician or downstream ComfyUI audio workflow can demonstrate a meaningful task it enables, and if the extra state stays composable with the engine's existing controls. The lesson's experiment should guide that choice. No new engine build, browser capture, WAV pair, perceptual test, or UI change was executed for PHY-004.

### Practice exercise 4

Write one controlled comparison for the claim “the pick-offset change dominates the brightness change.” What should be held constant, what intervention should be made, and what result would weaken the claim?

> **Answer:** Pin the engine revision, note, sample rate, profile, output path, duration, and preferably noise seed; record the actual parameter trace. Render two velocities first with the current mapping, then render with pick offset held at one declared index while keeping the other velocity mappings unchanged. Level-match and compare a declared onset window and brightness metric over repeated trials. If holding the offset fixed barely changes the velocity-dependent brightness difference within a predeclared tolerance, the dominance claim weakens. This does not by itself identify which remaining parameter caused the difference.

### Practice exercise 5

A developer proposes exposing `pick_position = 0.25` as a new WASM API parameter because the ideal model predicts zero fourth harmonic. What evidence is missing before treating that API value as a calibrated physical coordinate and promising that acoustic result?

> **Answer:** The current API accepts frequency and velocity; the internal offset is a heuristic. We would need a defined mapping from normalized API value to excitation construction, source tests showing it is independent of velocity or documenting coupling, controlled rendered spectra and listening tests across notes and rates, and a physical or perceptual calibration if calling it a real string coordinate. The current broad filtered-noise excitation is not the ideal triangular release, so the fourth-harmonic null cannot be promised. A new public API is a one-way compatibility decision and should follow task evidence and review.

## Sources and limits

- [Pinned GA guitar engine source](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs): `Engine::excite` defines the delay length, velocity clamps, offset and excitation shape; `Engine::render` combines the brightness path and feedback; `engine_note_on` is the exposed call. The calculations in this lesson apply to that source revision.
- [PHY-004 executable fixture](../../../fixtures/physics/phy-004/README.md): a synthetic, deterministic mirror of selected source formulas. It does not run Rust, synthesize audio, or test a listener.
- The ideal triangular displacement formula follows the fixed-end string sine-series model stated in section 1. It is deliberately separate from GA's filtered-noise excitation. No engine spectral comparison, physical pick-position calibration, human subject review, learner trial, localization, or public readback has been completed for PHY-004.
