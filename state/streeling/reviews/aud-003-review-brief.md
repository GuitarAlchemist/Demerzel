# AUD-003 bounded human review brief

Status: **open**. The existing AI subject and translation preflights and IX probe are supporting material, not human approval or a learner result.

## Frozen target

Review the AUD-003 course sources as they stood at Demerzel commit [`b8ed1f190d348869165353387f37e03c81e73b1e`](https://github.com/GuitarAlchemist/Demerzel/tree/b8ed1f190d348869165353387f37e03c81e73b1e/state/streeling/courses/audio-engineering). Each verdict must name the relevant Git blob. A later edit does not inherit the verdict automatically.

| Locale | Git blob | Human gate |
|---|---|---|
| English | `43c64022065899770fcafc66872c3789df5aa1a1` | Audio/DSP subject and answer review |
| French | `657e8c87dc0fe3352d02b517a9b6a1fcde55c8f2` | Fluent technical-language review |
| Spanish | `be1635b6d8f14cb0a24a58bd92fd805c9ec0b16d` | Fluent technical-language review |
| Portuguese | `bafe8e014fd5e7e02a309fc08c2565782e475d68` | Fluent technical-language review |
| Italian | `8ffce4ed57587d4a65e699046bff453c09389583` | Fluent technical-language review |
| German | `8ca2ab001f4db56dee730b8635bce05c1d550442` | Fluent technical-language review |

The [English course](https://github.com/GuitarAlchemist/Demerzel/blob/b8ed1f190d348869165353387f37e03c81e73b1e/state/streeling/courses/audio-engineering/en/aud-003-transient-preservation-gate.md) links IX source at `bd1336b7c4045e427dcdbe80b102790e45da5ce1` and the GAS-001 fixture at `5c4967454ddc740ed937c87719ca4d71a3522e4b`. The recorded E2 file SHA-256 is `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. The separate [IX probe record](aud-003-ix-probe-2026-10-11.md) explains the live endpoint run and its limits.

## Subject review and engineering checks

1. Recompute the proposed 2,048/512 STFT window and hop durations at 44.1 kHz, frequency spacing, and 1,025 one-sided bins. Verify the handler's power-of-two guard and distinguish the source code from an executed WAV spectrogram.
2. Recompute the 64-sample Hann boundary-impulse case and the eight-sample one-level Haar threshold-one reconstruction. Check all five course exercises and answers without using the answer blocks first.
3. Inspect the empirical IX Haar probe: 8,192 recorded-WAV samples, three thresholds, provisional 35 ms pre-onset interval, and no threshold reaching the proposed 3 dB noise target. Recheck that the course never upgrades this result into a full-file, listener, or GA-realism claim. The running endpoint binary was not independently attested to the pinned IX source commit.
4. Challenge the proposed 3 dB noise / 10% attack-peak / 1 ms timing gate. Is the onset proxy justified for the recorded file? What would fail under marker shifts, another pluck, or a full-file run? Record whether the illustrative gate is useful for teaching without presenting it as an accepted GA standard.
5. Check how the English empirical addendum appears in each translated source, including numbers, negations, and limitations. A shared number string is a parity signal, not a fluent-language verdict. A subject reviewer need not be fluent in all five languages; assign language gates separately.

## Answer-free learner trial

Give [`aud-003-learner-task.md`](aud-003-learner-task.md) without this brief or the course answer blocks. Record the learner's prior audio/DSP experience, elapsed time, unedited response, uncertainty, and any course revision followed by retest.

Score five criteria from 0 to 2, for 10 possible points: (1) correct time/frequency arithmetic for the transfer STFT setting; (2) correct explanation of the boundary-onset risk; (3) correct calculation and decision on the synthetic preservation gate; (4) correct separation of measured probe data from source-derived and hypothetical results; (5) an explicit follow-up experiment and honest limits. A proposed pilot pass is at least 8/10 with no false claim that the measured probe passed the 3 dB gate. This threshold itself should be evaluated during the learner trial. No learner result is recorded.

## Verdict and publication boundary

For each actual review, record reviewer identity or pseudonym, UTC time, reviewed commit and blob, kind (`subject`, one named `language`, or `learner`), evidence, findings, corrections, and `approved`, `changes_requested`, or `not_assessed`. A language verdict also binds the English source blob. The draft receipt contract is in Demerzel PR #1211 and requires its own human schema review. Do not create an approval from the prior AI preflights or this brief.

Keep `review.completed` and `publish.completed` false until real decisions are recorded and defects are corrected. After accepted source integration, generate Learn pages, build, deploy, and verify anonymous public course text and source provenance. Portuguese, Italian, and German source files require an actual site-rendering path before claiming public pages in those languages.
