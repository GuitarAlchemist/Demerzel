# PHY-003 bounded review brief

Status: **open**. This is a packet for a human audio subject review, fluent-language checks, and a learner trial; it is not an approval receipt.

## Frozen source set

At Demerzel commit `8d57c2a680fab0d7c38ac78178c9baa9b5b0c637`, the course [`phy-003-sampling-aliasing-guitar-engine.md`](https://github.com/GuitarAlchemist/Demerzel/blob/8d57c2a680fab0d7c38ac78178c9baa9b5b0c637/state/streeling/courses/physics/en/phy-003-sampling-aliasing-guitar-engine.md) has these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `6e06cfdd2684496acda909ebc5cbb7049700e843` |
| ES | `37d2037c8bbf8b634504422dc9457652cb995518` |
| PT | `7039b53151f3b35a16ec00719a146b3a2ff3f2f8` |
| FR | `a7c7482201aeaae0fd54e83fbbd60fde5320efa2` |
| IT | `88d203cfa37dfcee068ac092ef6ca0b5f1ea2b0c` |
| DE | `8fe704550aed02311537086a2bd0740213285d29` |

The production record is `state/streeling/course-productions/cp-physics-2026-10-12-003.json`; review and publish flags are false. A later edit to any locale changes its target blob and needs an explicit diff review. The [independent AI subject and semantic preflight](phy-003-subject-preflight-2026-10-12.md) reports no remaining actionable static issue within its scope, but grants no human verdict.

## Subject review

1. Follow the source trail: pinned [GAS-001 fixture](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) is a 44.1 kHz recorded file plus a **native** engine render. At pinned [GA commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo), inspect `audioEngine.js`, `guitar-worklet.js`, and `rust-engine/src/lib.rs` for the browser's context-rate path. Check whether the course ever treats a native WAV as a browser capture.
2. Recompute the mathematical examples: 44.1/48 kHz Nyquist limits `22,050/24,000 Hz`; four-second mono counts `176,400/192,000`; E2 ideal partial thresholds `267/268` and `291/292` at `82.4069 Hz`; a 23 kHz sine folding to `21.1 kHz` at 44.1 kHz but staying in band at 48 kHz; and 30 kHz folding to `14.1/18 kHz`. Check that ideal sampling arithmetic is not presented as a measured engine defect or audible artifact.
3. Challenge the proposed experiment. Does it specify a deliberately unfiltered synthetic reference, a controlled rate change, native-versus-browser path consistency, source/build identity, onset-aligned windows, level control, and an observation that would weaken the alias hypothesis? Would any simpler controlled test be more decisive?
4. Attempt all five course exercises before reading the answer blocks. Look for ambiguities about analog anti-alias filtering versus digital synthesis and about resampling a tone that already folded.

## Language and learner review

Ask fluent reviewers to compare each localized answer and caution against the pinned EN blob. Especially check rate units, partial indices, the `23 kHz -> 21.1 kHz` example, native/browser distinction, and the absence of a measured alias claim. AI semantic parity is only a preflight.

Give [`phy-003-learner-task.md`](phy-003-learner-task.md) without this brief or answer blocks. Record prior sampling knowledge, elapsed time, unedited response, confusion, and revision/retest if needed. The transfer task expects `f_N = 16 kHz` at 32 kHz, `128,000` samples in four seconds, and a deliberately unfiltered 19 kHz sine folding to `13 kHz`. A proposed pass is at least 8/10 across five 0–2 criteria: (1) Nyquist and sample count; (2) alias arithmetic; (3) native/browser evidence boundary; (4) falsifiable controlled experiment; (5) distinction between prediction and observed GA behavior. Revisit the threshold after a real learner trial; no result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC time, reviewed locale blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. Do not infer a human verdict from the AI preflight or the course production flag. The draft exact-source receipt contract in Demerzel PR #1211 has a separate human schema gate.

Keep course review and publish flags false until real verdicts and learner evidence are recorded. After accepted source integration, import into Learn, deploy, and anonymously read back the intended public pages and exact source revision. A local generated page is not public publication.
