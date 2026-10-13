# CS-004 independent review and follow-up

After the first denied wmux attempt, the user authorized one narrow retry. On 2026-10-04 the coordinator started a new bounded Claude Code lane in a pre-created pane with `dontAsk`, the subscription binary, `Read,Write`, four exact file-read rules, and one exact receipt-write rule. The pane showed four `Read` calls and one `Write` call; the declared review file existed and ended with `STREELING_AGENTIC_REVIEW_V2_DONE`. The wrapper reported provider exit 0 and verified the marker. The coordinator stopped and reaped only this temporary lane; the existing Wayfinder session remained.

The 800-word-limit review was advisory. It identified two testable gaps in CS-004: a baseline-equals-candidate control cannot show that the comparator responds to a known perturbation, and the blind-listening gate lacks a predeclared protocol. It also noted that prompt-ID recovery is described but not implemented by the local GA bridge. The review's proposed three-guitarist panel, level matching, and comparison against a simpler manual workflow are hypotheses to test, not adopted product requirements. Its full local receipt is `ga/state/handoffs/streeling-agentic-dogfood-review-20261004-v2.md` and is not part of this Demerzel commit.

The coordinator reran the comparator with two deliberate FFmpeg transformations of the GAS-001 GA-rendered E2. [`positive-control-evidence.json`](positive-control-evidence.json) records commands, hashes, selected metrics, and limits. The half-amplitude control changed the 250 ms RMS error from `0.1241587463` to `0.0550300994`; the equalizer control changed spectral centroid from `85.7895` to `89.9233` Hz while its RMS error increased to `0.1367309830`. This demonstrates sensitivity to these particular perturbations. It does not show that either output sounds more realistic, that the reference is a valid optimization target, or that ComfyUI improves the engine.

Reproduce from a checkout with the GAS-001 fixtures and the local GA comparator (currently unmerged):

```powershell
$fixture = '<Demerzel-checkout>\state\streeling\fixtures\guitar-acoustics\gas-001'
$out = '<scratch-directory>'
ffmpeg -hide_banner -loglevel error -y -i "$fixture\ga-engine-e2-open-4s.wav" -af 'volume=0.5' -c:a pcm_s16le "$out\gain-half.wav"
ffmpeg -hide_banner -loglevel error -y -i "$fixture\ga-engine-e2-open-4s.wav" -af 'equalizer=f=164.8:t=q:w=1:g=6' -c:a pcm_s16le "$out\second-partial-plus6.wav"
node scripts/compare-audio.js --baseline "$fixture\ga-engine-e2-open-4s.wav" --candidate "$out\gain-half.wav" --reference "$fixture\deb-low-e-open.wav" --reference-offset 1.1 --seconds 1.5 --output "$out\gain-half.json"
node scripts/compare-audio.js --baseline "$fixture\ga-engine-e2-open-4s.wav" --candidate "$out\second-partial-plus6.wav" --reference "$fixture\deb-low-e-open.wav" --reference-offset 1.1 --seconds 1.5 --output "$out\second-partial-plus6.json"
```

Run the comparator commands from `Rust/guitar-web-wasm-demo` in the GA worktree containing commit `95b67785150961e7fb3b67978856ecb206e70a65`. The candidate WAVs and raw JSON were kept in a local scratch directory, outside the course fixture. Reproduction hashes may vary by FFmpeg build; the filter settings and directional checks are the teaching contract.
