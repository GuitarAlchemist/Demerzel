# PM-003 learner task — answer-free handout

Give this sheet to a learner before they see PM-003 or its answer blocks. The source inventory is a dated Demerzel snapshot at commit [`0220ca8`](https://github.com/GuitarAlchemist/Demerzel/tree/0220ca84a25f59973bd6b9236cc00b7f68631a50): 81 English course files, 16 modules with all six active-language files, zero approved production reviews, and one `review_pending` production record. These are **snapshot counts**, not a timed review ledger.

The event ledger below is **synthetic teaching data**. Its interval is `[2026-10-05 00:00 UTC, 2026-10-12 00:00 UTC)`. At the start, modules A and B are in review work in progress (WIP). A returned draft stays in WIP until an approved review or explicit withdrawal.

| Time (UTC) | Module | Event |
|---|---|---|
| Oct 6, 09:00 | C | Ready for review; enters queue |
| Oct 7, 16:00 | A | Required reviews approved; exits |
| Oct 8, 11:00 | D | English draft authored; no review entry |
| Oct 9, 14:00 | B | Returned for correction; stays assigned |
| Oct 10, 12:00 | E | Ready for review; enters queue |
| Oct 11, 18:00 | C | Explicitly withdrawn; exits |

## Tasks

1. A card says “78 English modules became 81, so three reviews shipped.” Rewrite that claim using the correct unit. Say which event evidence is missing for a review-throughput rate.
2. Which of the four pinned snapshot counts establishes review WIP for this seven-day window? Which establishes completed-review throughput for this window? Explain.
3. Calculate closing review WIP from the synthetic ledger and list the module IDs still in it. Explain why B's return for correction does or does not remove unfinished review work.
4. Report approved-review completions, withdrawals, and authored drafts separately for the synthetic window. What error results if every queue exit is called a completed review?
5. Write a two-sentence dashboard caption that keeps the real pinned snapshot separate from the synthetic ledger and names the next measurement action needed for real Streeling flow.

## Response and observation

- Unedited learner response, without the lesson answers: _attach or paste here_.
- Actual time to complete: _record it_.
- Ambiguous words or counts in the learner's own terms: _record them_.
- Other sources consulted: _list them_.

Use `pm-003-learner-scorecard.md` only after the response is complete. This handout is preparation, not a learner result.
