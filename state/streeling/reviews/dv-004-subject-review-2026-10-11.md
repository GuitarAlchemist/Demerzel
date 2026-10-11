# DV-004 bounded subject review — 2026-10-11

## Scope and provenance

- Reviewer: independent Codex AI subagent `dv001_subject_review`, read-only.
- Material: English DV-004 lesson and GA June 15 and July 19, 2026 QA snapshots at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Final verdict: **approved for numeric and exercise-answer accuracy within this scope**. Human subject review, learner testing, fluent localization, and publication remain pending.

## Review loop

1. Initial verdict: **revise**. An exercise stem called all 52 June prompts “reconstructed failures.” The snapshot's 75% of 52 reconstructs 39 passes and 13 failures. Its answer already calculated `(39 + 1) / 52 ≈ 76.92%` correctly.
2. Correction: the stem now says “one of June's 13 reconstructed failures” in a hypothetical fixed suite of 52 prompts. The production record's word count was updated.
3. Focused recheck: **approved**. The reviewer re-read the corrected stem and answer, confirmed the 13/52 distinction and the +1.92 percentage-point calculation, and confirmed that the hypothetical is not presented as a GA observation.

The first pass found no other numeric or answer-key issues. It also confirmed that inferred counts are labeled as reconstructed and that a one-verdict rate step is not called a confidence interval. The focused recheck covered only the corrected stem and answer; it was not a new full review.

Keep `review.completed: false` until the remaining gates have evidence.
