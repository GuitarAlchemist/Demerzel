# PHY-004 learner transfer task

Give this sheet without PHY-004's answer blocks or reviewer brief. It uses a new **selected-source-formula thought experiment**, not an audio measurement.

An engineer holds sample rate at `44,100 Hz` and note frequency at `82.4069 Hz` in the pinned GA Rust guitar engine. The active integer delay-buffer length is `535` samples for both cases. They send note-on velocities `0.30` and `0.70`. The inspected source computes `pick_ratio = 0.18 + 0.60(1 - velocity)`, rounds `535 × pick_ratio` to an integer offset, and computes `pluck_mix = 0.15 + 0.35 velocity` for these in-range values. The source also multiplies the initial filtered-noise excitation by velocity.

Answer in your own words:

1. Calculate `pick_ratio` and integer `pick_offset` for both velocities. Show the arithmetic and state which direction the offset moves.
2. Calculate `pluck_mix` for both velocities. Is “velocity controls only gain” an accurate source-level description? Explain without claiming a particular audible result.
3. An ideal triangular pluck at one-quarter of a string predicts a zero initial coefficient for every fourth harmonic. Does the engine's buffer offset alone guarantee a fourth-harmonic null in a rendered or recorded note? Name one missing assumption.
4. Design one controlled render comparison to test whether the offset shift is the dominant cause of a measured brightness difference. Name conditions to fix, an intervention, a metric or observation window, and a result that would weaken the claim.
5. Separate your conclusions into facts from the pinned source, arithmetic predictions from the formulas, and observations that would require a new render or listener trial.

The reviewer will keep your unedited response and use the five criteria in the separate review brief. No learner result has been recorded.
