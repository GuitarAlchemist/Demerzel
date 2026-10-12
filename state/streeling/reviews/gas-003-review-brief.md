# GAS-003 bounded review brief

Status: **open**. This packet requests human guitar-audio subject review, fluent-language checks, and a learner trial. It is not an approval receipt or a candidate render result.

## Frozen source and measurement boundary

At Demerzel commit `e2fcb42759e7b724ce4bd27e249c3604bf88fda6`, [`gas-003-decay-calibration-open-e.md`](https://github.com/GuitarAlchemist/Demerzel/blob/e2fcb42759e7b724ce4bd27e249c3604bf88fda6/state/streeling/courses/guitar-acoustics/en/gas-003-decay-calibration-open-e.md) and its localizations have these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `ee5b6f9204a0c39cf65248b12761a0924703d4b2` |
| ES | `407ff6a2f986b282e9a610dac5f397018db8a328` |
| PT | `e141f868b6fb38ccc9d632599ed9cf26ab8c4677` |
| FR | `c026330435301076620d8cc825aa7bfa9f056d29` |
| IT | `8ff74f64ea0e2d90409875bc8c19694cc227381a` |
| DE | `978769917a4a82248112ad6e0d7fb71814be6047` |

The production record is `state/streeling/course-productions/cp-guitar-acoustics-2026-10-12-003.json`, with review and publish false. The [independent AI source and translation preflight](gas-003-subject-preflight-2026-10-12.md) found no actionable static issue in its bounded scope. It did not run a decay candidate, authenticate a human verdict, or assess fluent meaning. A changed source blob needs explicit diff review.

## Subject and method review

1. Verify the pinned [GAS-001 fixture](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001) provenance: two four-second 44.1 kHz mono WAVs, an attributed recorded open E2 and a **native** GA Rust render. Check the measurement script's onset-relative early/late windows and the recording's second attack. The saved `-3.9` and `-1.1 dB` changes concern those windows, not whole-file loudness or preference.
2. Recompute render-minus-recorded `+2.8 dB` and absolute error `2.8 dB`. Inspect pinned GA Rust engine `dc2e74cbd992a298f67efb928b5b3754615e1924`: profile 0 sets base decay `0.9978`, and the setter must follow profile selection. Verify the source-derived feedback coefficients around `1.00009584` and `0.99989588` for base `0.9978` and `0.9976`; challenge any inference of audible growth or a measured improvement from one coefficient.
3. Test the proposed one-parameter protocol. Does it keep note, velocity, profile, build, duration, brightness, attack, reverb, noise state, and capture path controlled? Does it save both native WAV hashes, onset choices, unrounded measurements, peak checks, and spectral/attack guards? Is the classroom `>=1.0 dB` error reduction and `<0.95` peak guard clearly a **proposal**, not a product standard? The candidate renderer has not been built or run.
4. Attempt the five exercises before reading the answer blocks. Verify `2.8-1.0=1.8 dB`, candidate decline interval `[-5.7,-2.1] dB` around `-3.9`, and that a peak `0.98` fails the declared guard. Check the difference between an E2 calibration probe and a general guitar realism claim.

## Language and learner review

Ask fluent reviewers to compare each locale with the pinned English blob. Pay particular attention to signed dB values, onset-relative windows, profile/setter order, calculated versus measured coefficients, proposed gate and guards, and the absence of a candidate runtime result. AI semantic parity does not grant fluent approval.

Give [`gas-003-learner-task.md`](gas-003-learner-task.md) without this brief or course answer blocks. Record background in audio analysis, elapsed time, unedited response, confusion, and revision/retest. The **synthetic** transfer values yield baseline absolute error `|-1.6 - (-4.2)| = 2.6 dB`; candidate `|-3.0 - (-4.2)| = 1.2 dB`, an improvement of `1.4 dB`. That passes a proposed 1.0 dB numeric gate, but its `0.97` peak fails `<0.95`. With first onset `0.9 s`, early window is `1.1-1.3 s` and late window `1.9-2.1 s`, before the separate `2.4 s` attack. Score five criteria 0–2: (1) signed and absolute error arithmetic; (2) gate and guard decision; (3) onset-relative windows; (4) setter/profile control; (5) remaining browser, multi-note, and listening uncertainty. Provisional pass: at least 8/10, to be revisited after a real trial. No learner result exists.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact locale Git blob, kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 has its own human schema gate. This brief cannot issue a review receipt.

Keep review and publish flags false until real verdicts and learner evidence exist. After accepted source integration, import into Learn, deploy, and anonymously read back the intended page and source revision. A local page preview is not publication.
