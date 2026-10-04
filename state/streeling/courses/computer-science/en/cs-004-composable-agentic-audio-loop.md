---
module_id: cs-004-composable-agentic-audio-loop
department: computer-science
course: Compose and Dogfood an Agentic Audio Improvement Loop
level: intermediate
prerequisites: ["cs-002-governing-agentic-loops", "gas-001-open-string-audio-evidence"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-004
version: "0.1.0"
---

# Compose and Dogfood an Agentic Audio Improvement Loop

> **Department of Computer Science** | Intermediate | 45 minutes | Draft: subject and translation review pending

## Objectives

You will be able to split GA's audio experiment into functions that transform evidence and operations that change the world; run a no-improvement control; explain what a retry can and cannot assume after a timeout; and reject an agent's success claim when independent evidence does not support it.

## 1. Start with a real user problem and a control

A guitarist wants GA's real-time WASM instrument to sound more convincing. GA has a Rust guitar engine, browser AudioWorklet, and an offline capture loop. The local, unmerged GA tracer at commit `6fac5735f7ffbb4116ebee05cfc9d7911bb12ce9` adds `Rust/guitar-web-wasm-demo/scripts/run-comfy-audio.js` and `compare-audio.js`. The first submits a WAV to a loopback ComfyUI API workflow and records provenance. The second compares a baseline, candidate, and reference using FFT summaries and time-resolved 250 ms RMS/Haar details. Its supplied workflow only loads and saves audio: it **does not improve sound**. No live ComfyUI candidate or blinded listening has been verified.

Use the [GAS-001 fixture](../../../fixtures/guitar-acoustics/gas-001/README.md): an attributed recorded open E2 and a native render of GA's Rust engine. The native render shares engine source with the WASM demo but is not an AudioWorklet capture. The recorded onset is approximately 1.1 seconds, followed by another attack near 2.75 seconds. An experiment must select comparable note windows before interpreting a distance.

First set **candidate = baseline**. With both pointing to `ga-engine-e2-open-4s.wav`, reference `deb-low-e-open.wav`, `--reference-offset 1.1`, and `--seconds 1.5`, the actual comparator produced identical baseline and candidate errors: 250 ms RMS mean absolute error `0.124158746` for each; every reported FFT and Haar error also matched. This is a useful negative control. A pipeline that calls this an improvement has a broken decision rule, even though it ran successfully.

### Practice exercise 1

What should the acceptance decision be when the candidate and baseline SHA-256 values are both `a78a70243a81aa79d806d9ef3db7baa1385c479505f7d5e97b8bf0c7866c3f98`?

> **Answer:** Reject any improvement claim. The files are byte-identical, so neither metrics nor listening can attribute a change to ComfyUI. Keep the run as a control and check whether the workflow produced an effect.

## 2. Compose transformations; isolate effects

Treat each arrow as a typed contract. A pure function returns the same output for the same input and does not read a clock, call a service, or write a file. Keep those operations at the edges:

```text
captureWasm(note, profile)             EFFECT -> baseline WAV
loadAndValidate(files, note, onsets)  EFFECT + PURE validation -> fixed manifest
submitComfy(workflow, baseline)        EFFECT -> prompt ID or explicit failure
retrieveCandidate(prompt ID)          EFFECT -> candidate WAV + hashes
decodeAlignedAudio(manifest)          EFFECT -> fixed sample arrays
features(samples)                     PURE -> FFT, RMS, Haar evidence
compare(features, reference)          PURE -> differences + guardrail flags
proposeDecision(evidence, policy)      PURE -> accept/reject/needs-listening
blindListen(A, B, question)           HUMAN OBSERVATION -> listening record
recordDecision(all evidence)          EFFECT -> immutable receipt
```

This layout lets tests feed known arrays to `features` and fixed records to `proposeDecision` without launching ComfyUI or relying on an agent's prose. The real bridge already separates some calculations (`timeFeatures`, `compareFeatures`) from its network and file I/O. That is a starting seam, not proof that every operation is pure. In particular, decoding with FFmpeg and reading a WAV remain effects. Prefer a result such as `Ok(candidate)` or `Err(kind, prompt_id, evidence)` at each boundary; never silently replace an unavailable candidate with the baseline.

The policy is deliberately narrow: byte-identical candidate means **reject improvement**; missing file, mismatched note, or unaligned onset means **needs repair**; plausible spectral change means **needs blinded listening**, not accept. A loss number does not speak for the guitarist. The evaluator must preserve the fixed reference and report both improvement and regressions in attack, pitch, decay, noise, and artifacts.

### Practice exercise 2

Classify `timeFeatures(samples)`, `fetch('/prompt')`, `hash(bytes)`, `ffmpeg decode`, and `write receipt` as pure transformations or effects. Where should an agent propose a new seed?

> **Answer:** `timeFeatures` and `hash` can be pure when their complete inputs are supplied. Fetching, FFmpeg execution, and writing are effects. The agent may propose a seed before `submitComfy`; the submitted seed and workflow hash must be recorded so the evaluator can reproduce the candidate.

### Practice exercise 3

A candidate lowers the spectral centroid error, but its attack sounds smeared in a level-matched blind A/B. Does the lower number authorize an engine change?

> **Answer:** No. The metric is diagnostic and only one part of the acceptance policy. Record the objective change and the guitarist's listening observation, reject or revise the candidate, and keep the baseline. No automatic Rust/WASM parameter write follows.

## 3. Make retries honest

Suppose ComfyUI accepts `/prompt` and the client times out before reading `/history/{prompt_id}`. The server may still be running. That is an **unknown outcome**, not proof of failure. If the prompt ID is known, query history before another submission. If it was lost, record uncertainty and do not count the retry as an independent experiment. Key the logical experiment by baseline hash, workflow hash, model fields, and seed; keep each submission's prompt ID and attempt separately. A fixed upload filename based on the input hash helps identify the same baseline, but it does not make model execution idempotent.

The first tracer does not yet persist a prompt ID before the candidate is retrieved, so restart recovery remains an implementation gap. Its later provenance correction does distinguish `comparison_pending`, `completed`, and `comparison_failed`: a failed comparison must never leave a successful quality verdict. Build recovery only after the failure case is reproduced with a mock and its receipt can be inspected.

### Practice exercise 4

The client has a candidate WAV, but reference decoding fails. What status should be written, and what may be retried?

> **Answer:** Preserve the candidate and its hashes, mark the comparison `comparison_failed`, and report the decode error. Fix the reference or decoder and retry the comparison on the same candidate. Do not rerun ComfyUI merely because the evaluator failed.

## 4. Dogfood the full loop

Run this from a checkout containing both GA and the Streeling fixtures, adjusting paths. The bridge is currently a **local GA commit**, so this command is an exercise for a reviewer with that worktree; it is not a public installation instruction:

```powershell
$fixture = '<path-to-Demerzel-checkout>\state\streeling\fixtures\guitar-acoustics\gas-001'
node scripts/compare-audio.js `
  --baseline "$fixture\ga-engine-e2-open-4s.wav" `
  --candidate "$fixture\ga-engine-e2-open-4s.wav" `
  --reference "$fixture\deb-low-e-open.wav" `
  --reference-offset 1.1 --seconds 1.5 --output control-comparison.json
```

Open the JSON and verify equal baseline/candidate hashes and errors. Then use a local ComfyUI workflow only when an audio model and its license are known. Keep the same baseline and reference, change one workflow parameter, record model/seed/hash, measure again, and have a guitarist listen blind at matched level. Write one receipt with the user's observation, the automated measurements, a rejected or accepted decision, and the next experiment. This is dogfooding: the team uses its own engine and tooling to discover friction in the entire experience, including setup, errors, recovery, and review. If the agent cannot access a fixture or write a receipt, record that failure as a product observation rather than treating a submitted prompt as progress.

### Practice exercise 5

Name a success condition and a falsifier for the next iteration. Who decides whether the real-time engine changes?

> **Answer:** One possible condition is a reproducible candidate with a fixed baseline/reference, no attack or pitch regression, and a blind listener preference recorded for the same note. A byte-identical output, missing provenance, or consistent listener rejection falsifies improvement. The agent proposes; an independent evaluator and authorized project reviewer decide whether a specific Rust/WASM change is worth testing. The offline candidate alone cannot become the real-time engine.

## Sources and limits

The concrete GA bridge is the local `6fac5735` commit; targeted mock tests passed, while ComfyUI at `127.0.0.1:8188` did not respond and browser WASM capture was not rerun. The control comparison above was rerun independently against the pinned [GAS-001 WAVs](../../../fixtures/guitar-acoustics/gas-001/README.md). [CS-002](cs-002-governing-agentic-loops.md) explains externally bounded agent loops; this course focuses on composing one observable experiment. GA's `docs/methodology/agentic-engineering.md` supplies the queue and harness context. ComfyUI's [core audio nodes](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py) and [server routes](https://github.com/Comfy-Org/ComfyUI/blob/master/server.py) describe the API boundary. FFT and Haar distances cannot establish perceived realism, and the recorded clip's metadata has not been independently verified at the capture session.
