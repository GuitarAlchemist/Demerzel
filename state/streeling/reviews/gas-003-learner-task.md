# GAS-003 learner transfer task

Give this sheet without GAS-003's answer blocks or reviewer brief. All numbers here are a **hypothetical new dataset**, not a GA render, a listener study, or a measured change to the Rust engine.

Suppose an onset-aligned open-string reference has a late-minus-early RMS change of `-4.2 dB`. An unchanged native engine has `-1.6 dB` and a proposed candidate has `-3.0 dB`. The class proposes a gate of at least `1.0 dB` smaller absolute error against the reference, plus a peak absolute amplitude strictly below `0.95`. The candidate's peak is `0.97`.

The recording's first onset is approximately `0.9 s`, with another attack near `2.4 s`. Early and late RMS windows are `0.2-0.4 s` and `1.0-1.2 s` after the first onset. A developer also says they set a candidate decay value before selecting guitar profile 0.

Answer in your own words:

1. Compute the signed candidate-minus-reference change, and both baseline and candidate **absolute** errors against the reference.
2. How much did absolute error shrink? Does the candidate pass the numeric gate and the peak guard? Give an overall decision under the proposed classroom rules.
3. Convert both onset-relative RMS windows to approximate recording-file time. Would the second attack enter either window?
4. Why does the order of profile selection and decay setter call matter for a fair candidate render?
5. If a controlled native E2 run passed every classroom guard, what would still be unknown about the browser AudioWorklet, other notes/velocities, and what guitarists hear?

The reviewer will keep your unedited response and score it against the five criteria in the review brief. There is no recorded learner result.
