# INF-004 bounded review brief

Status: **open**. This packet requests human subject and learner review; it is not a verdict. At Demerzel commit `eb449fe83164bda739e2bec70ea7a926e3cb3d42`, the [English course](https://github.com/GuitarAlchemist/Demerzel/blob/eb449fe83164bda739e2bec70ea7a926e3cb3d42/state/streeling/courses/information-theory/en/inf-004-information-loss-in-agent-handoffs.md) has Git blob `e5e3706b012321aa6197ed50899aaa87664374d6`. The fixture JSON blob is `ce52b080e4c9d1fb735f8ce529fae2add57aa7a7` and evaluator blob is `778a02c4530f0f20ae070b401b152eb9e28a06e4`. A changed blob needs a new diff review.

## Source and arithmetic checks

1. Read GA `Scripts/antigravity-bridge.ps1` at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`, blob `cb4c999ebb615af327006045edb012c427c8858e`. Confirm the note's guaranteed fields and that tests, review, and single-writer status are not validated by the script. Challenge any implication that local branch/head and dirty-line count prove remote or current delivery state.
2. Run `python state/streeling/fixtures/information-theory/inf-004/evaluate_handoffs.py` from Demerzel's root. Inspect `handoff-cases.json`; all four headlines collide, only A passes the three toy gates, and the invented mean costs are `7.5`, `0.25`, and `0`. Try a missing gate and a non-boolean gate; validation should reject them. These are synthetic calculations, not live agent rates.
3. Solve the five course exercises before reading answers. Challenge the proposed richer handoff: are all fields needed for the named integration decision, which should be checked independently, and could a simpler link to an existing immutable receipt suffice? Do not interpret the toy zero cost as proof of real merge safety.

## Learner and verdict gates

Give [`inf-004-learner-task.md`](inf-004-learner-task.md) without the course answers. The transfer table has E and G ineligible, F eligible. With false-accept cost 6 and false-reject cost 2, accept-all mean cost is `(2 × 6)/3 = 4`; reject-all mean cost is `2/3`. The common headline cannot separate the cases. Score five criteria from 0 to 2: eligibility and collision, arithmetic, checkable receipt versus free-form claim, source/review exactness, and a falsifiable counterexample. A provisional pass is 8/10; revisit after a real learner attempt. No learner result exists.

Record reviewer identity or pseudonym, UTC date, exact course blob and GA source revision, independent checks, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft receipt contract in Demerzel PR #1211 has a separate human schema gate. Keep production review and publish flags false until an actual subject verdict, learner attempt, language review, Learn sync, deployment, and anonymous public readback. English is the only current source language.
