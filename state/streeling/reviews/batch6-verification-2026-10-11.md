# Streeling batch 6 verification — 2026-10-11

## Scope

This batch adds English drafts FUT-002, GTR-004, and WML-002, each with a research-cycle record, an in-progress production record, five answered exercises, pinned GA evidence, and a bounded AI subject review. The reviews are `fut-002-subject-review-2026-10-11.md`, `gtr-004-subject-review-2026-10-11.md`, and `wml-002-subject-review-2026-10-11.md`. They do not represent human approval or publication.

## Local checks

- Draft 7 schema validation passed for all six new JSON records against `schemas/research-cycle.schema.json` and `schemas/course-production.schema.json`.
- `python -m unittest scripts.test_streeling_course_progress` passed all three tests.
- The three authors checked lesson word counts, five answer pairs per lesson, and local/pinned source links; independent reviewers recomputed FUT-002's numbers and GTR-004's fret/MIDI predictions. A separate parent review checked WML-002 against the pinned tuning table.
- `python scripts/streeling_course_progress.py` reports 96 English source modules across 21 course directories, 429 short of the provisional 525 target, 16 with all six active-language source files, and zero approved pipeline reviews. The registry still has 23 department records; issue #1209 tracks the denominator decision.
- The complete local `scripts/verify.ps1` was not rerun for this documentation-only batch after a prior run stalled in an unrelated temporary-Git unit test. GitHub Governance Validate on the previous content commit `264b1845d21550023bdfc144b006ba30c77b731d` passed all seven jobs. The new commit still requires its own CI result.

Human subject/cultural review, musician or learner trials, fluent localization, Learn deployment, and anonymous public readback remain open. The English file count is an authoring measure, not a reviewed or published course count.
