# PSY-003 bounded review brief

Status: **open**. This is a human-review and learner-trial packet, not an approval receipt or evidence of an operational throughput improvement.

## Frozen target and inputs

- English course: [`psy-003-review-throughput-and-compounding.md`](https://github.com/GuitarAlchemist/Demerzel/blob/3e2ac3f1ec322af684733ed1f01df5b775600546/state/streeling/courses/psychohistory/en/psy-003-review-throughput-and-compounding.md), merged from Demerzel `master` commit `3e2ac3f1ec322af684733ed1f01df5b775600546`, Git blob `7436b383a7446d58c253a9f53a12b0772422e568`. French blob: `397ea4b4afd5eb63f477e445ea96c7a186fbc9f2`; Spanish blob: `c1ad218149317f7c3ffc5172abc6336911e74e12`. Check these blobs again at the final integration commit.
- Synthetic simulator under `scripts/streeling_fixtures/psychohistory/psy-003/analyze.py`: Git blob `e728327e04388bd06ecde1ed3d908a803de9e0a5`; scenario JSON blob `58d842f2bea173421b65b9c676266638350b2f98`; result JSON blob `2aef2ab3fc7527b85fddd356688f5ff6361d6f5f` at the same master commit. The original pilot fixture remains in Git history but is not the current lesson's command.
- Observed course inventory: `state/streeling/reviews/review-candidates-793e92b.json`, source commit `793e92bd5a8a97552ed3fee68a3956929c7d0c54`. It is a triage snapshot, not a human verdict.
- Production record: `state/streeling/course-productions/cp-psychohistory-2026-10-12-003.json`; review and publication flags are false. English, French, and Spanish source files exist; fluent review remains pending.

A later course edit changes its blob. Review that diff explicitly before extending a verdict to the new source.

## Subject and method review

1. Recompute `21 × 25 = 525` and `525 − 113 = 412` from the pinned inventory. Check that the extra authored English module lies outside the first 25 core codes, and that 23 department records versus 21 directories remains an explicit scope question rather than a silently resolved fact.
2. Re-run `python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check` and check both conservation identities and its negative control. The flat scenario ends with 16 accepted, 16 published, 32 waiting review; the growing-review scenario ends with 48 accepted, 16 published, 32 waiting publication. Check the realized fourth-week count of 20 rather than the configured capacity of 32.
3. Read the course for any sentence that upgrades these synthetic counts into a measured four-week intervention, a guaranteed exponential trajectory, or approval by an automated reviewer. The model assumes every review approves and every approved item can be published; these assumptions are intentionally optimistic.
4. Inspect the proposed pilot measurements and falsifier. Are exact source identity, authenticated human verdicts, correction rate, learner outcome, deployment, and anonymous public readback distinguished? What data would be required to compare cohorts of different difficulty or language scope?
5. Attempt the five exercises before reading their answer blocks. Record ambiguity, missing inputs, or arithmetic errors with section references. The prior PSY-001 fractal/Noether analogy must remain an analogy, not a physical law asserted for this software workflow.

## Answer-free learner trial

Give [`psy-003-learner-task.md`](psy-003-learner-task.md) without this brief or the course answer blocks. Record prior experience with queues and software delivery, elapsed time, the unedited response, confusion, and any lesson revision followed by retest.

The transfer fixture in that task has three weeks with six new ready items each week, accepted-review capacities `3, 6, 9`, and publication capacity two per week. Expected weekly `(accepted, published, waiting_review, waiting_publication)` rows are `(3,2,3,1)`, `(6,2,3,5)`, `(9,2,0,12)`. Final accepted is 18 and published is six. Score five criteria 0–2: (1) correct arithmetic and queues; (2) both conservation checks; (3) identification of the actual downstream bottleneck; (4) a verifiable human/public outcome and falsifier; (5) separation of synthetic results from live Streeling evidence. A proposed pilot pass is at least 8/10 without calling a draft or synthetic publication a real one; evaluate this threshold after an actual learner trial. No result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact locale blob, kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. Fluent French and Spanish reviewers must check the 12/4/8/16/32 fixture values, the distinction between simulated acceptance and actual human approval, and the publication boundary against the English source. The draft exact-source receipt contract in Demerzel PR #1211 still requires human schema review; do not invent an approval receipt from this packet.

Keep review and publish flags false until actual verdicts and learner evidence are recorded. After accepted source integration, generate Learn, deploy, and anonymously read back the PSY-003 page with its source SHA. The isolated local Learn import is not public readback.
