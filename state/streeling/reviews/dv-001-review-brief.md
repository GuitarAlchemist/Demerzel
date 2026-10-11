# DV-001 review brief

Status: **open**. A bounded AI subject check passed on 2026-10-11; fluent language review and a learner test remain open. This brief is not a publication receipt.

## Material to review

- Source lesson: `state/streeling/courses/data-visualization/en/dv-001-observed-degraded-stale-quality.md`
- Localizations with the same stem: `fr`, `es`, `pt`, `it`, `de`
- Historical GA source revision: `dc2e74cbd992a298f67efb928b5b3754615e1924`
- Four source snapshots: `state/quality/chatbot-qa/2026-06-08.json`, `2026-06-15.json`, `2026-06-19.json`, `2026-07-19.json`
- Research cycle: `state/streeling/research-cycles/data-visualization-2026-10-04-001.json`
- Production record: `state/streeling/course-productions/cp-data-visualization-2026-10-04-001.json`

## Subject review

1. Verify every value and date in the four-row table against the pinned JSON. In particular, June 8 has `pass_pct: null`, `degraded: true`, a backend-unavailable reason, and a 94% carried-forward reference dated May 16.
2. Attempt all five exercises using only the lesson table and linked records. Record where the answer requires information the learner does not have.
3. Check the two-lane proposal: it must not turn `null` into zero, place the historical 94% at June 8, or imply measurements on unshown days.
4. Check that the June 19 and July 19 comparison does not assert a software cause, identical prompts, or an identical evaluator without evidence.
5. Review the accessibility claim and the proposed text/table alternative against the linked W3C guidance.

An independent AI subject check is recorded in `dv-001-subject-review-2026-10-11.md`. It checked the pinned GA values and exercise answers and returned `approved` within that scope. It did not assess fluent translations or observe a learner. A human subject reviewer should repeat the checks above before the production record is approved.

## Localization review

For each language, a fluent reviewer should confirm that the technical meaning of `null`, `degraded`, and `carryforward` survives; all five exercise answers remain correct; dates and decimal separators are clear; and the prose reads naturally. Record a separate verdict and reviewer for each language. Structural parity alone is insufficient.

| Language | Structural draft | Fluent review | Verdict |
|---|---|---|---|
| EN | present | pending | pending |
| FR | present | pending | pending |
| ES | present | pending | pending |
| PT (Brazil) | present | pending | pending |
| IT | present | pending | pending |
| DE | present | pending | pending |

## Learner test and publication gate

Ask a learner to classify the four runs and sketch a two-lane chart without seeing the answers first. Record task success, confusion, and corrections. Keep the production record at `review_pending` until the subject, language, and learner findings have been addressed. Only then consider Learn synchronization and anonymous EN/FR/ES readback. The current Learn synchronizer does not render PT/IT/DE pages.
