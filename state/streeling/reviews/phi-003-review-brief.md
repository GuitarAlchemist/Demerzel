# PHI-003 bounded review brief

Status: **open**. This packet invites a human music-theory/semantics review and a learner trial; it is not an approval receipt.

## Frozen target and inputs

- English course: [`phi-003-what-does-the-same-chord-mean.md`](https://github.com/GuitarAlchemist/Demerzel/blob/0455c23100c5757223da6f659cc61e06d5faea12/state/streeling/courses/philosophy/en/phi-003-what-does-the-same-chord-mean.md), Demerzel commit `0455c23100c5757223da6f659cc61e06d5faea12`, Git blob `7e2b48aff874fc29716dcd62b426cbdef7187294`.
- Teaching input, evaluator, and result: `state/streeling/fixtures/philosophy/phi-003/` at Demerzel commit `50c0d2f5eb6684499c3bcf95d77f0481af2cc136`.
- Production record: `state/streeling/course-productions/cp-philosophy-2026-10-12-003.json`; review and publish flags are false. No translations are declared.

A later source edit changes its blob. Review that diff explicitly before extending a verdict.

## Subject and answer-key review

1. Inspect the pinned GA `EmbeddingSchema.cs` and `TheoryVectorService.cs` at `dc2e74cbd992a298f67efb928b5b3754615e1924`. Verify OPTIC-K v1.8 and the distinction between literal chroma, ICV/cardinality, and ROOT. Challenge any phrase that calls the whole `STRUCTURE` partition transposition-invariant or treats the fixture's chroma-only cosine as a GA score.
2. Re-run `python state/streeling/fixtures/philosophy/phi-003/compare_voicings.py` and compare with `comparison-results.json`. Verify the four pair outcomes: octave revoicing same PC set; C-to-D major exact transposition and same ICV; C major/minor same ICV and supplied root but different PC sets; C diminished different ICV. Note that a zero-offset transposition is allowed for identical sets.
3. Challenge the operational meaning of “same”: MIDI-note multiset, pitch-class set, explicit T/I relation, ICV equality, and thresholded similarity. Check the course's nontransitivity example (`0.8`, `0.8`, `0.5` at threshold `0.75`) and its caution that ICV equality does not uniquely name a chord.
4. Inspect GA's pinned `IcvNeighborsSkill` and `Tools/GaStructureInvariance/Program.cs` only within their stated scope. The former is an ICV-distance path and the latter exports actual vectors; this lesson did not execute either to benchmark live retrieval. Ask whether a user-facing explanation should expose the relation or whether one simpler label works better.
5. Attempt all five exercises before reading their answers. Record any misleading guitar-fingering, inversion, root, cosine, or equivalence-language claim with the exact course section.

## Answer-free learner trial

Give [`phi-003-learner-task.md`](phi-003-learner-task.md) without this brief or course answer blocks. Record the learner's guitar and set-theory background, elapsed time, unedited answers, confusion, and revision/retest if needed.

The transfer example uses G major low/high, A major, and G minor. Expected pitch-class sets are `{2,7,11}`, `{2,7,11}`, `{1,4,9}`, and `{2,7,10}`. All three named triads have ICV `[0,0,1,1,1,0]`; G-to-A major is a `+2` transposition, while G major and G minor share ICV and a declared G root but have different PC sets. Score five criteria 0–2: (1) correct PC conversion; (2) correct transposition/ICV reasoning; (3) distinction between root label and PC identity; (4) no inference from toy cosine to full GA ranking; (5) a usable product claim with a falsifiable learner or query test. A provisional pass is at least 8/10; revise the threshold after a real trial. No learner result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact course blob, kind (`subject` or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 still needs human schema review; do not fabricate a receipt from this packet.

Keep review and publish flags false until real verdicts and learner evidence are recorded. After accepted source integration, generate Learn and anonymously read back the public page at its intended source SHA. The local import does not count as publication.
