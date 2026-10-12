# COG-001 bounded review brief

Status: **open**. This packet requests human cognitive-science and project-domain review, fluent-language review, and an answer-free learner trial. It records no reviewer approval or learner outcome.

## Candidate source identity

At Demerzel commit `34a70d5c70a057d99cabe235f732f7d444a3ea6f`, the following course blobs were verified with `git ls-tree`. If a blob changes, review its diff before issuing a revision-bound human review receipt. Pinned project-source links inside the course use the earlier Demerzel commit `af4e9a3a6f242745730f2d0d28e2535fe7477666`.

| Locale | Course Git blob |
|---|---|
| EN | `0062f261f6d4e590c0fd50df40f3cb1db2f27af1` |
| FR | `e181e610dfa3abc4d2d04b29b7657224ec7e9d9e` |
| ES | `f8a52262c0b9dafcef9a1ed465cea96317547f94` |
| PT | `e44d5ce892870c70af6b5b2f1dd23d497a461e2e` |
| IT | `e5a9d1cecb194635983cf2b36b79aec0ffad4da9` |
| DE | `0dadf8c870371bc63323dbcdd44c4761bfe89101` |

The synthetic fixture blob is `4d030de462703f4d4c0ecb46e20d64c960bd6bc8`. The production record is `state/streeling/course-productions/cp-cognitive-science-2026-10-12-001.json`; review and publish flags are false. Existing baseline prose predates this bounded exercise; review the whole lesson before approving it.

## Subject and source review

1. Inspect [`scripts/streeling_course_preflight.py`](../../../scripts/streeling_course_preflight.py), [`scripts/streeling_review_candidates.py`](../../../scripts/streeling_review_candidates.py), and [`CONTEXT.md`](../../../CONTEXT.md) at the pinned project-source commit `af4e9a3a6f242745730f2d0d28e2535fe7477666`. Confirm that source checks and triage are not human subject review or public deployment and that T/P/U/D/F/C is canonical while T/F/U/C is only a subset.
2. Check that each case number is explicitly synthetic: twelve planned courses, four checked local preview passes, eight unchecked local previews, one checked public 404, eleven unobserved public results, proposed 80%, eight elapsed months, and 2/5 forecast weekly hours. Reject any wording that turns them into GA/Learn measurements.
3. Recompute 4/12 = 1/3 = 33.3% preview coverage and 2 − 5 = −3 forecast hours per week. Check the inference boundary: zero **confirmed** public successes is not proof that all twelve pages fail; only the observed URL failed at its stated time.
4. Review all five answers for specificity to confirmation, survivorship, anchoring, availability, and sunk cost. Check that a 404 leads to a bounded publication gate and follow-up measurements, not a blanket permanent stop.
5. Review the older overview separately for overgeneralized bias definitions or unqualified Demerzel claims. In particular, assess whether the Dunning–Kruger explanation and causal wording about governance countermeasures need qualification. The new exercise does not certify that earlier prose.

## Language and learner review

Fluent FR/ES/PT/IT/DE reviewers should compare all five localized questions and answers with EN. Check the distinctions between **local preview**, **human review**, and **public readback**, the known 404 versus eleven unknown public results, the 4/12 denominator, and the forecast label on −3 hours. A mechanical five-pair count is only parity triage.

Give [`cog-001-learner-task.md`](cog-001-learner-task.md) without the course answers or this brief. Record the learner's background, elapsed time, unedited response, confusion, and any retest. For the task's **different synthetic case**, score five criteria 0–2: (1) evidence categories and missing gates; (2) correct denominator; (3) careful public-result inference; (4) proportionate investigation after 404; (5) prospective-cost arithmetic without sunk-cost reasoning. Provisional pass: 8/10, to revise after a real trial. No learner result is recorded.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC time, reviewed commit and exact locale blob, review kind (`subject`, `language`, or `learner`), observed evidence, actionable findings, and verdict (`approved`, `changes_requested`, or `not_assessed`) under the separately gated receipt contract. This packet alone issues no receipt. Keep review and publish false until the required human verdicts and learner evidence exist. After accepted source integration, synchronize Learn and anonymously read back intended pages and revision.
