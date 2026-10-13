# COG-003 bounded review brief

Status: **open**. This packet requests human cognitive-science/guitar subject review, fluent-language checks, and a learner trial. It is not evidence that GA users have entered confidence values or improved recall.

## Frozen source set

At Demerzel commit `f339e8b551414de8750945a55c15181096c6abf7`, [`cog-003-calibrating-fretboard-confidence.md`](https://github.com/GuitarAlchemist/Demerzel/blob/f339e8b551414de8750945a55c15181096c6abf7/state/streeling/courses/cognitive-science/en/cog-003-calibrating-fretboard-confidence.md) and its localizations have these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `26432356b48ed737ef5c6722117fe83dab05a93d` |
| ES | `2d5a6fa952c84461d339113747d99c6dd304f686` |
| PT | `1d55a48b4d58a2d091876b33b88f8f7c54e9bba3` |
| FR | `9b913066bdc423dbf5cf85ea2ba5965f64b7102e` |
| IT | `962d9625be592e45c7fc7b50bf3d7285cd5da274` |
| DE | `2c34b18f954ef001164d4a7f000542a8b4a377b7` |

The production record is `state/streeling/course-productions/cp-cognitive-science-2026-10-12-003.json`; review and publish flags are false. The [independent AI subject and translation preflight](cog-003-subject-preflight-2026-10-12.md) checks static source and arithmetic only. A later course edit changes the blob and requires explicit diff review.

## Subject and method review

1. Inspect pinned GA `GuitarFretboardTest.tsx` and `GuitarFretboard.tsx` at `dc2e74cbd992a298f67efb928b5b3754615e1924`. Check string order (index 0 high E, index 5 low E), default tuning, and the six demo positions. The displayed `C` at low E string 5 fret 3 conflicts with the independently calculated G. Confirm the course never uses the mistaken display label as its verified key.
2. Check the prediction event: after choosing a note, the learner states the probability that **their own answer** is correct, before seeing feedback. The pinned click handler records only string/fret, and the demo exposes labels. A real calibration study would need a new label-free question and confidence input; the six course probabilities are invented.
3. Recompute the six synthetic squared losses `0.01,0.04,0.49,0.16,0.01,0.81`, accuracy `4/6`, total `1.52`, and Brier mean `0.2533`. If the wrong displayed C contaminates the sixth key, the loss becomes `0.01` and the mean `0.12` without any learner improvement. Recompute the expected-loss identity `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)` and the `q=0.7` example.
4. Challenge the proposed intervention: compare held-out next-day Brier loss with answer-only feedback while guarding note accuracy, item-set comparability, consent, and pre-feedback logging. A lower Brier score alone need not mean more notes are known. Inspect the stated falsifier and any potential answer leakage.
5. Attempt all **six** course exercises before reading the answer blocks. Record any ambiguous key, probability event, or claim of real learner benefit with the precise course section.

## Language and learner review

Ask fluent reviewers to compare each localized answer and caution with the pinned EN source, especially corrected key `E,C,G,E,C,G`, the synthetic six-row probabilities, `0.2533` versus contaminated `0.12`, and the proposed next-day study. AI parity triage is not fluent approval.

Give [`cog-003-learner-task.md`](cog-003-learner-task.md) without this brief or course answers. Record prior fretboard/probability knowledge, elapsed time, unedited response, confusion, and any revision/retest. The new **synthetic** four-trial table has verified outcomes `[1,0,0,1]`, losses `[0.04,0.36,0.81,0.09]`, accuracy `2/4`, and Brier `(1.30)/4 = 0.325`. Using the demo's incorrect C at string 5 fret 3 would change trial 3 to correct, yielding total loss `0.50` and mean `0.125`; that is key contamination, not learning. Score five criteria 0–2: (1) corrected fretboard key; (2) outcome/loss arithmetic; (3) contamination explanation; (4) proper pre-feedback probability event; (5) a falsifiable real-learner comparison with accuracy guardrail. Provisional pass: at least 8/10, to revise after an actual learner trial. No learner result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact locale blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 has a separate human schema gate. This packet cannot issue a receipt.

Keep review and publish false until real verdicts and learner evidence exist. After accepted source integration, import Learn and anonymously read back the intended pages and source revision. A generated local page is not publication.
