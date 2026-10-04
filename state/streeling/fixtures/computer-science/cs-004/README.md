# CS-004 control: candidate equals baseline

This is a negative control for the draft course `cs-004-composable-agentic-audio-loop`. It reuses the two [GAS-001 WAVs](../../guitar-acoustics/gas-001/README.md); no audio is duplicated here. The recorded file remains attributed to collegefishiesd under CC BY-SA 4.0.

The comparator came from local, unmerged GA commit `6fac5735f7ffbb4116ebee05cfc9d7911bb12ce9` at `Rust/guitar-web-wasm-demo/scripts/compare-audio.js`. On 2026-10-04, the same GA native-rendered E2 WAV was supplied as both baseline and candidate. The recorded E2 was the reference. The comparison used a 1.1-second reference offset and a 1.5-second analysis window to stop before the recorded clip's later attack. `control-evidence.json` stores selected values from that run with portable relative paths; the full raw comparator output was local and contained machine-specific paths.

From the GA demo directory in a checkout containing the comparator, set `$fixture` to the GAS-001 fixture directory and run:

```powershell
node scripts/compare-audio.js `
  --baseline "$fixture\ga-engine-e2-open-4s.wav" `
  --candidate "$fixture\ga-engine-e2-open-4s.wav" `
  --reference "$fixture\deb-low-e-open.wav" `
  --reference-offset 1.1 --seconds 1.5 --output control-comparison.json
```

The baseline and candidate hashes and every baseline/candidate error should match. The observed 250 ms RMS mean absolute error against the reference was `0.12415874627653194` for each. This establishes only that the control cannot show improvement. It does not validate the comparator as a perceptual metric, a ComfyUI model, or the browser WASM path. The input onset is approximate, and levels have not been calibrated for listening.
