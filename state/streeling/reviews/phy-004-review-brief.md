# PHY-004 bounded review brief

Status: **open**. This is a packet for human physics/audio subject review and a learner transfer trial, not an approval receipt.

## Exact source set

The [English course](https://github.com/GuitarAlchemist/Demerzel/blob/eb2350d6d450a2e63a776b7a4a9d77a9416be939/state/streeling/courses/physics/en/phy-004-velocity-pick-position-guitar-engine.md) is at Demerzel commit `eb2350d6d450a2e63a776b7a4a9d77a9416be939`, Git blob `60ee03be07ede322d98b233c2118f2599757b9af`. Its deterministic fixture is `state/streeling/fixtures/physics/phy-004/` at commit `c781729a2bcbffed1bd8567ca94aae695960ea7e`; the production record is `state/streeling/course-productions/cp-physics-2026-10-12-004.json`. A later edit changes the review target and requires a new exact-source comparison.

The project source is GA commit [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), `Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs` Git blob `c5b5050061e680dbd01b6ff8fb5bee2e5adbe41b`. The source record and course must remain on these identities for this review. No translation source is declared beyond EN; fluent-language review is needed if translations are added later.

## Subject checks

1. Re-read `Engine::excite` and `Engine::render` in the pinned GA blob. Verify that velocity affects filtered-noise amplitude, `pick_ratio`, `pluck_mix`, and attack; `pluck_mix` enters brightness. Check that the course does not call the buffer index a measured physical distance or present the fixture as an audio render.
2. Recompute `floor(44100 / 82.4069) = 535`, `pick_ratio` values `0.63/0.48/0.33`, offsets `337/257/177`, `pluck_mix` values `0.2375/0.325/0.4125`, and the fractional remainder near `0.14936`. Confirm the script's positive-value rounding matches Rust's relevant cases.
3. Check the ideal fixed-end triangular-displacement result `A_n ∝ sin(nπp)/[n² p(1-p)]` under fixed apex height and the `p=1/4` and `p=1/2` null examples. Challenge any accidental transfer of those nulls to GA's filtered-noise excitation or a real recorded guitar.
4. Execute all five course exercises before reading the answer blocks. Check whether a learner can distinguish a source-level parameter coupling from a measured spectral or perceptual effect.
5. Challenge the proposed controlled experiment: would fixing pick offset while retaining other velocity mappings isolate its **contribution** sufficiently? Are source/build identity, rate, deterministic seed when possible, repeat renders, level matching, onset windows, and predeclared metric and tolerance adequate? State what additional intervention would be needed to separate `pluck_mix` and attack.

## Learner trial

Give [`phy-004-learner-task.md`](phy-004-learner-task.md) without this brief or answer blocks. Preserve the unedited response, prior guitar/DSP knowledge, time taken, confusion, and any retest. The new velocities are `0.30` and `0.70`. With `N=535`, the expected ratios are `0.60` and `0.36`, offsets `321` and `193`, and `pluck_mix` values `0.255` and `0.395`. The offset moves **128 samples** in this selected arithmetic. These are not acoustic measurements.

Score each criterion 0–2, with a proposed pass of at least 8/10: (1) computes the ratios and offsets; (2) identifies another coupled control and keeps gain distinct; (3) explains why ideal pluck modal zeros do not prove GA output; (4) designs a controlled, falsifiable render comparison; (5) labels every output as formula prediction, source fact, or actual measurement. Reconsider the rubric after the first real trial; no learner result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC time, exact reviewed locale blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed` through the accepted review receipt process. The fixture pass and this packet do not grant human approval. Keep review and publish flags false until real verdicts and learner evidence are recorded. After accepted source integration, import into Learn, deploy, and anonymously read back the public page and source revision. A generated local page is not public publication.
