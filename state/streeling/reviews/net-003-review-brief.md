# NET-003 bounded review brief

Status: **open**. This packet requests human subject and fluent-language review plus a learner trial. It is not an approval receipt or a live wmux staffing report.

## Frozen source set and replay

At Demerzel commit `de87345aed25b83a97da853fdee86caf43d26ebe`, [`net-003-worker-lane-coverage-and-fragility.md`](https://github.com/GuitarAlchemist/Demerzel/blob/de87345aed25b83a97da853fdee86caf43d26ebe/state/streeling/courses/network-science/en/net-003-worker-lane-coverage-and-fragility.md) and its five localizations have these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `8b01f7efa6b19fe54b72f83c770294bc2fff4c9a` |
| ES | `fa6fa3df9e8f8af1b0bf815eaec6c54ea29e7364` |
| PT | `73e1d92572763edfbb1e7d65b0cf4968af8fabad` |
| FR | `35b383ba4b6f381c5f054e952d4eab260b477437` |
| IT | `ed6c94329b35c71344731b5c881fc90c34f6a804` |
| DE | `c5d910e3843a984a4485b3a3ae8d77b3bd13e619` |

The production record is `state/streeling/course-productions/cp-network-science-2026-10-11-003.json`, with review and publish flags false. The [independent AI subject and translation preflight](net-003-subject-preflight-2026-10-11.md) is static triage, not human approval. The [offline selector replay receipt](net-003-selector-replay-2026-10-12.json) pins Demerzel policy/selector commit `ecdc6c27559bb1a11343cfad33687465893e9891` and their Git blobs; it is not evidence of live agent work. Re-review a changed course or policy blob rather than inheriting the old conclusion.

## Subject and method review

1. Inspect the pinned `state/driver/aiw-worker-lanes.json` and `scripts/aiw_lane_selector.py`. Re-run `python scripts/streeling_net003_replay.py` and compare its decision payload, source blobs, and counts with the receipt. Expected unblocked assigned-role paths across NORMAL/CONSTRAINED/DRAINING/HALTED are `22/21/21/8`; worker-class edges are `9/8/8/3`; unblocked primary paths are `5/4/4/1`.
2. Verify the graph construction: only primary and secondary assignments become worker-to-role paths; forbidden roles never become routes. Deduplicate multiple roles in one class before counting worker-class edges. Keep the five assigned classes as the declared coverage denominator when a mode blocks one of them.
3. Challenge the worker-removal example. In DRAINING, deleting `augment` loses the sole `navigate` edge and lowers coverage from `4/5` to `3/5`; deleting `codex` alone loses no whole class. Check that the course does not equate class redundancy with exact-role substitutability, current presence, permissions, or completion.
4. Inspect selector order and three controls. Expected forbidden role `block`, unknown role `warn`, unknown mode `escalate`. An exit code 0 means the request was evaluated; use the JSON decision, not process success, as the local oracle. `allow` and `recommend` remain advisory payloads.
5. Attempt the five answers before reading the course key. Look for any sentence that turns a dry-run policy or replay result into a claim that wmux agents are running, available, or authorized to merge.

## Language and learner review

Ask fluent reviewers to compare each localization with the pinned EN source, especially `22/21/21/8`, `9/8/8/3`, `5/4/4/1`, the NORMAL matrix, `augment` deletion, and `block`/`recommend`/`warn`/`escalate`. The existing AI parity preflight cannot approve meaning or teaching quality.

Give [`net-003-learner-task.md`](net-003-learner-task.md) without this brief or the course answers. Record the learner's experience with graphs and agent routing, elapsed time, unedited response, confusion, and any revision/retest. The transfer task's DRAINING matrix has eight worker-class edges and four covered classes out of the five-class denominator. Removing both `claude` and `codex` leaves four edges and `groom`, `navigate`, `review` covered, or `3/5`; it does not prove any surviving worker is online. Score five criteria 0–2: (1) projected edge and coverage arithmetic; (2) two-worker cut; (3) forbidden-role decision and selector-vs-graph distinction; (4) exit-code/decision interpretation; (5) live-evidence boundary. A provisional pass is at least 8/10; revisit after an actual learner trial. No learner result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact course blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 requires separate human schema review. This packet does not issue a receipt.

Keep review and publish flags false until real verdicts and learner evidence exist. After accepted source integration, import Learn and anonymously read back the intended pages at the source revision. Local generation is not public publication.
