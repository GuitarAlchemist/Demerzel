# AUD-003 learner task — no answer key

You have read **Protect a Guitar Pluck During Offline Spectral Analysis**. Work from the pinned course and source files, but do not open the course answer blocks while completing this task. Show your arithmetic and distinguish source declarations, synthetic examples, and observed audio measurements.

1. At 44,100 samples/s, propose a `window_size` of 4,096 and `hop_size` of 1,024 for an IX spectrogram. Calculate the window duration, hop duration, nominal frequency-bin spacing, and one-sided bin count. State whether the handler's power-of-two condition is met.
2. Explain how a pluck impulse can disappear from one Hann-windowed frame yet appear with a smaller hop in another frame. Specify one diagnostic you would use around a real onset.
3. A **hypothetical** denoised candidate shows 3.2 dB lower pre-onset RMS, an attack absolute peak 0.89 times the raw peak, and a peak-time shift of 0.8 ms. Apply the lesson's proposed 3 dB / 10% / 1 ms gate. Show the peak-loss calculation and decision.
4. Summarize what the recorded-WAV IX Haar probe actually measured. State the tested thresholds, whether any met the 3 dB target, and one reason its result cannot establish perceptual equivalence or GA render realism.
5. Propose one next experiment that could change the decision about denoising the recorded reference. Include the input identity, one controlled variable, a saved output or trace, and a falsifier. Say which result would cause you to keep the raw recording as the primary reference.

Return commands, calculations, and evidence references. Write “not assessed” where evidence is absent. The reviewer scores the unedited response separately; no result is supplied here.
