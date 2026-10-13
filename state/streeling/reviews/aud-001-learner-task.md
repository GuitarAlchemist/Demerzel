# AUD-001 learner task — answer-free copy

Give this page to a learner after the AUD-001 lesson. Do not provide `aud-001-learner-scorecard.md` until the response is complete. The exercise concerns a synthetic signal and a proposed experiment; no audio plugin or guitar processing result is supplied.

Record the learner's relevant audio/DSP experience and start time. Ask for an unedited written response to these five tasks:

1. Let `A=E(C(x))` and `B=C(E(x))`, where `E` is an EQ and `C` is a full-band compressor. What signal enters `C` in each chain? Can an EQ boost after `C` change the gain-reduction decision already made by `C`?
2. For zero-prehistory `x=[0,2,0,0]`, FIR `h=[0.5,0.5]`, and memoryless `C(v)=sign(v)×(|v| if |v|≤1 else 1+(|v|−1)/2)`, calculate `A`, `B`, and `B[1]−A[1]`. State exactly what the calculation proves and one thing it does not prove.
3. The recorded GAS-001 open-E2 WAV begins its first attack approximately 1.1 seconds into the file, while the GA native render begins at file time zero. Explain two flaws in comparing the recorded file's `0.0–1.0 s` window with the render's `0.0–1.0 s` window to judge EQ/compression order.
4. Specify the minimum manifest and output artifacts needed to compare both orders on one recorded WAV. Include compressor state, filter coefficients, latency, playback-level matching, and a way to check whether the compressor actually acted.
5. Suppose an unaligned trial reports a `0.2 dB` short-window RMS difference without a compressor settings manifest. Decide whether it supports choosing either order. State one plausible null result and one result that would cause you to reject an apparent difference as an artifact.

End time and unedited response location: _to be recorded by facilitator_. Do not infer success from a blank task sheet.
