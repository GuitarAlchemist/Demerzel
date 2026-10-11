# DV-001 bounded subject review — 2026-10-11

## Scope and provenance

- Reviewer: independent Codex AI subagent `dv001_subject_review`, read-only.
- Material: the English DV-001 lesson and GA historical fixtures pinned to commit `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Verdict: **approved for subject accuracy within this scope**. This is not a fluent-language review, a learner test, or approval to publish.

## Findings

1. The four lesson-table values and their observed/degraded statuses match the pinned GA snapshots for June 8, June 15, June 19, and July 19, 2026.
2. All five exercise answers preserve the distinction between measured values, unavailable runs, and carried-forward references. No concrete factual or answer error was found.
3. The pinned GA quality trend report supports warning readers about stale feeds.
4. The June 8 snapshot reports `pass_pct: null`, while carrying a prior `last_known_good_pass_pct: 94.0`. The pinned `baseline.json` attributes 94% to a post-#224 local snapshot of 47/50 active prompts established on May 16. The May 16 daily snapshot separately has `pass_pct: null`; neither file makes 94% a June 8 observation.

## Remaining gates

- Human subject review of the English lesson and its source interpretation.
- Fluent review of EN, FR, ES, PT, IT, and DE prose and exercise answers.
- A learner attempt at the classification and two-lane chart before seeing the answers.
- Publication synchronization and anonymous readback of each supported language page.

Keep the production record at `review_pending` until these gates have evidence.
