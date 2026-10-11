# DV-001 learner task — answer-free handout

Use this sheet before opening the DV-001 lesson or its answer blocks. The four records below are historical GA chatbot QA snapshots at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. They do not describe today's service.

In this task, the status lane reports what each **QA snapshot** says about its run. A reported pass rate or `degraded: false` is not a complete health check of the chatbot service.

| Date | Total prompts | Reported `pass_pct` | `degraded` | Other source detail |
|---|---:|---:|---|---|
| 2026-06-08 | 52 | `null` | `true` | Backend unavailable; `last_known_good_pass_pct: 94.0`, source `carryforward`, dated May 16. |
| 2026-06-15 | 52 | 75.00 | `false` | No degraded reason reported. |
| 2026-06-19 | 52 | 7.69 | `false` | No degraded reason reported. |
| 2026-07-19 | 52 | 98.08 | `false` | No degraded reason reported. |

## Tasks

1. For each date, write whether a pass rate was reported and what the QA snapshot says about degradation. If you would put any date at 0% on a pass-rate chart, identify it and explain why.
2. Sketch a two-lane display: one lane for reported pass rates and one for reported QA run status. Put dates on the display. Show how you would handle June 8 and the unshown days between the recorded dates.
3. Write a one-sentence dashboard caption for June 8 that mentions the 94% reference without making it a June 8 measurement.
4. A teammate writes, “GA recovered from a software regression by July 19.” State what the four records actually establish and name two further pieces of evidence needed to test the teammate's claim.
5. Write a short text alternative for your sketch that a reader could use without seeing its colors or shapes.

## Response and observation

- Learner response, written or sketched without the lesson answers: _attach or paste here_.
- Time to complete: _record actual duration_.
- Words or symbols that were unclear: _record the learner's words_.
- Source records consulted beyond this sheet: _list them, if any_.

The facilitator should score the response using `dv-001-learner-scorecard.md` only **after** the learner finishes. Do not fill in a successful result without an actual learner attempt.
