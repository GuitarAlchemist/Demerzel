# DV-008 source-bound review brief

Status: **open**. This is a request for a human subject review and an independent learner attempt, not a verdict. Review Demerzel commit `2641071b23b85cbef2e74bf69c8ec52de25f173d`: course blob `d307a8324de9313ad6d79d6eab541f232914dddc`, fixture JSON blob `93c560dcc19f02737403ac977215a1e1996c453c`, and evaluator blob `c898c183d057f1e52286870578be1795dc1e6aec`. Record the UTC review date and reviewer identity or pseudonym. Any later content edit needs a new diff review.

## Pinned evidence to challenge

1. At Demerzel commit `8a37e1d9a728a15ed384cbb912e3c8c518083d12`, inspect `scripts/streeling_course_progress.py` (blob `d467443a57c298abdb54d2a0b188eec849150713`). Reproduce its 21 course directories, 120 core codes, 121 English sources, zero recorded review approvals, and CYB-026 outside the 001–025 target. Check that the report does not claim an exhaustive public count.
2. At the same commit, inspect `scripts/streeling_public_readback.py` (blob `f72650b7b35ba079606fb2987cde4aa1d2bff00b`). Challenge the course's explanation of the anonymous HTTP, index link, module link, and heading checks. Confirm the script only checks the selected modules and does not prove pedagogical quality or human review.
3. Run `python scripts/streeling_fixtures/data-visualization/dv-008/evaluate_cards.py`. Inspect all six explicitly synthetic cards and derive the four counts independently. Check the exception cards B and F, and challenge the notion that the three stages form a guaranteed nested funnel. Try changing one JSON boolean to a string and confirm that the evaluator rejects it.
4. Solve the five course exercises before seeing their answers. Inspect the fixture links, version boundary, unknown-versus-zero treatment, accessibility of the proposed matrix, and whether the lesson makes any unsupported current-publication claim.

## Learner and decision gates

Give [`dv-008-learner-task.md`](dv-008-learner-task.md) without the lesson's answer blocks. Preserve the unedited response, relevant experience, duration, cited sources, confusion, proposed corrections, and any retest. Score five observable dimensions from 0 to 2: stage classification, arithmetic and denominator, unknown-versus-zero caption, source-bound next action, and a falsifiable real-world limit. A provisional pass threshold is 8/10; adjust the lesson if the actual response reveals a problem. A prepared task is not a learner attempt.

Record reviewer, exact course blob, independently checked claims, findings, and one of `approved`, `changes_requested`, or `not_assessed`. Keep production review and publish flags false until a real subject verdict, learner result, language review, Learn sync, deployment, and anonymous public readback exist. The English draft and synthetic fixture alone do not clear those gates.
