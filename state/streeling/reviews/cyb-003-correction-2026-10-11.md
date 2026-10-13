# CYB-003 correction and review queue

Status: **draft corrected; subject, learner, and localization reviews pending**. This is a correction receipt, not a course approval or publication receipt.

## Problem found

The previous CYB-003 draft treated counts of personas, policies, grammars, and thresholds as independent numbers of effective regulatory states. It divided sums of their logarithms into “healthy” variety ratios and inferred a 3-bit regulatory deficit. Neither the state set nor a matched disturbance → response → outcome task was defined. The ranges and deficit therefore had no empirical basis. A second model's agreement did not validate them.

The earlier text also named a research cycle `cybernetics-2026-03-23-003`; no matching JSON record is present in this checkout. Its `T, confidence 0.85` label was not a substitute for the missing evidence. Preserve the historical Git version, but do not repeat those quantitative conclusions as findings.

## Bounded correction

- Rewrote the English course around a pinned Demerzel revision, a replayable schema/record snapshot, and five answered exercises.
- The fixture reads revision `66083fc684b57a12ef307c19c3819d91c551295f` directly from Git. It confirms five configured status labels, three configured review verdict labels, eight production records, a 7/1 observed status split, zero recorded verdicts, and `0.543564` bits of empirical status entropy.
- The course distinguishes configured labels, observed sample variety, entropy, and **unmeasured** regulatory effectiveness. It proposes a matched task instead of a claimed variety ratio.
- Updated PSY-002 in EN/FR/ES where it depended on CYB-003's ratio and an arbitrary 1.0 boundary. Reframed its phase-transition analogy, 2σ display band, proposed R measure, policy-saturation example, and transition exercise as illustrative or unvalidated. Removed claims that a 2× signal rate or three aligned signals predicts a transition, and that governance transitions are mostly second-order. The historical cross-model-agreement metadata was removed because it cannot validate the revised course.
- Added conservative exercise/answer and evidence-link signals to the source progress report. They are triage aids, not readiness verdicts: before this correction, 47/77 English modules had a detectable exercise/answer pair, 44/77 a pinned revision link, and 5/77 an existing fixture link; after it, the counts are 48, 45, and 6. Pipeline approvals remain zero.

## Evidence and limits

- Replay: `python scripts/streeling_verify_cyb003_snapshot.py` passed against the pinned Git object. The script is issue-backed by [Demerzel #1208](https://github.com/GuitarAlchemist/Demerzel/issues/1208) and lives under `scripts/` per `CONTRIBUTING.md`.
- Focused progress tests: `python -m unittest scripts.test_streeling_course_progress -v` passed 3/3.
- A bounded independent AI subject pass first requested revision: the course called 15 nonmissing label pairs an upper bound despite optional verdicts, and PSY-002 still presented several analogies and thresholds as established findings. After correction, a second bounded AI pass returned **APPROVE** for those specific findings in CYB-003 and PSY-002 EN/FR/ES. This is preliminary review evidence, not a pipeline approval or a substitute for a subject specialist or learner.
- Primary theory sources consulted: W. Ross Ashby's [*An Introduction to Cybernetics*](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf), chapters 7 and 11, and Claude Shannon's [original paper](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).
- No learner attempted the new exercises. No human subject reviewer has approved the correction. CYB-003 currently has only an English draft; FR/ES/PT/IT/DE versions must be created and reviewed. No public Learn readback was performed for this corrected version.

## Next review question

Can an independent reviewer reproduce all five answers from the pinned files and explain why a schema's label count cannot establish a controller's ability to keep an essential variable within bounds? If the distinction fails for a learner, revise the exercise before localization and publication.
