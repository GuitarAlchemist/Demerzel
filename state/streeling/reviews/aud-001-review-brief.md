# AUD-001 review brief

Status: **open**. The English subject and five-localization AI preflights are recorded in `aud-001-subject-preflight-2026-10-12.md`. They are static checks, not human approval or a learner result.

## Review material

- Source course: `state/streeling/courses/audio-engineering/en/aud-001-eq-compression-order.md`; localizations with the same stem in `fr`, `es`, `pt`, `it`, and `de`.
- Fixture and provenance: `state/streeling/fixtures/guitar-acoustics/gas-001/README.md`; recorded E2 SHA-256 `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`.
- Pinned GA audio engine/worklet: commit `dc2e74cbd992a298f67efb928b5b3754615e1924`; pinned IX FIR source: `bd1336b7c4045e427dcdbe80b102790e45da5ce1`.
- Research cycle: `state/streeling/research-cycles/audio-engineering-2026-10-12-004.json`; production record: `state/streeling/course-productions/cp-audio-engineering-2026-10-12-004.json`.

## Subject and engineering review

1. Recompute both synthetic chains for `x=[0,2,0,0]`, `h=[0.5,0.5]`, threshold 1, and ratio 2:1. Verify that the result proves only noncommutativity of these declared operators, not a guitar listening preference.
2. Check that the recorded WAV is mono float32 and that its approximate first onset and second attack are handled correctly. Distinguish the recorded file from the native GA render and the browser AudioWorklet path.
3. Check pinned GA and IX source claims. Look for any sentence that implies an existing compressor, executed A/B run, measured order effect, or validated realism benchmark; none is established by this lesson.
4. Assess the proposed A/B contract: one unchanged source WAV, equal EQ/compressor parameters, independent state reset, explicit boundary/latency treatment, raw and level-matched outputs, gain-reduction trace, clipping guard, and a declared falsifier. Record missing conditions that would make an order comparison uninterpretable.
5. Attempt all five exercises without the answer blocks. Record ambiguity or required knowledge that is absent from the lesson.

## Localization and learner review

Ask a fluent reviewer for each language to check technical meaning, arithmetic, the difference between a synthetic result and an executed experiment, and idiomatic prose. Record a named or anonymized reviewer, date, verdict, and corrections for each language. The AI parity check narrows this work but does not approve a translation.

Give a learner `aud-001-learner-task.md` without the answer key, then score the unedited response using `aud-001-learner-scorecard.md`. Record prior audio/DSP experience, time, confusion, and any lesson change followed by a retest. No learner result is recorded yet.

Keep `review.completed` and `publish.completed` false until findings are addressed. The isolated Learn EN/FR/ES build passed, but the public AUD-001 route still serves the historical vocal lesson. After approval, deploy the revised source through Learn and verify anonymous public content and source provenance; PT/IT/DE require a separate site-rendering path.
