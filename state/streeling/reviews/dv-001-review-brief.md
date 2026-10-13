# DV-001 review brief

Status: **open**. Bounded AI subject and multilingual semantic checks passed on 2026-10-11; human subject, fluent language, and learner reviews remain open. This brief is not a publication receipt.

## Frozen course sources

At Demerzel commit `be3e3fc73fb447d28a7e1ad85e311f327f804964`, the DV-001 course has these exact Git blobs. A later edit to any locale needs an explicit diff review before a verdict can cover the new file. This course-source revision is distinct from the historical GA snapshot used for the quality data below.

| Locale | Git blob |
|---|---|
| EN | `37047b77f21f91afeec137378f5cd398d3cc1520` |
| ES | `d75e33c3fef9f2b0f882a96f7cdf818b0f67ddef` |
| PT | `60bedcb591a421244b45abea6e6bd199b112339a` |
| FR | `b293b732747650a0b701371a0ed5f7f40edc715d` |
| IT | `2d06e75496b66cc902f52f4910441282891e1114` |
| DE | `b71bf6a78b74232a06b96f8ee7e0f7d83b068d16` |

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

For each language, a fluent reviewer should confirm that the technical meaning of `null`, `degraded`, and `carryforward` survives; all five exercise answers remain correct; dates and decimal separators are clear; and the prose reads naturally. A bounded AI comparison is recorded in `dv-001-ai-multilingual-check-2026-10-11.md`; it narrows the human review queue but does not replace it. Record a separate human verdict and reviewer for each language. Structural parity alone is insufficient.

| Language | Structural draft | AI semantic check | Fluent review | Final verdict |
|---|---|---|---|---|
| EN | present | subject check passed | pending | pending |
| FR | present | passed | pending | pending |
| ES | present | passed | pending | pending |
| PT (Brazil) | present | passed | pending | pending |
| IT | present | passed | pending | pending |
| DE | present | passed | pending | pending |

## Learner test and publication gate

Give a learner `dv-001-learner-task.md` without the lesson answers, then use the separate `dv-001-learner-scorecard.md` after the response. Record task success, confusion, and corrections. Neither document is a completed learner attempt. Keep the production record at `review_pending` until the subject, language, and learner findings have been addressed. Only then consider Learn synchronization and anonymous EN/FR/ES readback. The current Learn synchronizer does not render PT/IT/DE pages.
