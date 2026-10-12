# PSY-003 bounded review brief

Status: **open**. This is a human-review and learner-trial packet, not an approval receipt or evidence of an operational throughput improvement.

## Frozen target and inputs

- English course: [`psy-003-review-throughput-and-compounding.md`](https://github.com/GuitarAlchemist/Demerzel/blob/996086c8904479f97dcbe28b55f30171255e7295/state/streeling/courses/psychohistory/en/psy-003-review-throughput-and-compounding.md), Demerzel commit `996086c8904479f97dcbe28b55f30171255e7295`, Git blob `0b2a03ddb02fe62bee699e04ecfecc0195e1c839`.
- Synthetic simulator: Git blob `e9af269254d5276aeed3210f783c44a6c844805c`; result JSON: Git blob `bbe5709da4105d61004502bf1a0885a230035169` at that commit.
- Observed course inventory: `state/streeling/reviews/review-candidates-793e92b.json`, source commit `793e92bd5a8a97552ed3fee68a3956929c7d0c54`. It is a triage snapshot, not a human verdict.
- Production record: `state/streeling/course-productions/cp-psychohistory-2026-10-12-003.json`; review and publication flags are false.

A later course edit changes its blob. Review that diff explicitly before extending a verdict to the new source.

## Subject and method review

1. Recompute `21 × 25 = 525` and `525 − 113 = 412` from the pinned inventory. Check that the extra authored English module lies outside the first 25 core codes, and that 23 department records versus 21 directories remains an explicit scope question rather than a silently resolved fact.
2. Re-run the synthetic simulator and check both conservation identities. The flat scenario ends with 16 accepted, 16 published, 32 waiting review; the growing-review scenario ends with 48 accepted, 16 published, 32 waiting publication. Check the realized fourth-week count of 20 rather than the configured capacity of 32.
3. Read the course for any sentence that upgrades these synthetic counts into a measured four-week intervention, a guaranteed exponential trajectory, or approval by an automated reviewer. The model assumes every review approves and every approved item can be published; these assumptions are intentionally optimistic.
4. Inspect the proposed pilot measurements and falsifier. Are exact source identity, authenticated human verdicts, correction rate, learner outcome, deployment, and anonymous public readback distinguished? What data would be required to compare cohorts of different difficulty or language scope?
5. Attempt the five exercises before reading their answer blocks. Record ambiguity, missing inputs, or arithmetic errors with section references. The prior PSY-001 fractal/Noether analogy must remain an analogy, not a physical law asserted for this software workflow.

## Answer-free learner trial

Give [`psy-003-learner-task.md`](psy-003-learner-task.md) without this brief or the course answer blocks. Record prior experience with queues and software delivery, elapsed time, the unedited response, confusion, and any lesson revision followed by retest.

The transfer fixture in that task has three weeks with six new ready items each week, accepted-review capacities `3, 6, 9`, and publication capacity two per week. Expected weekly `(accepted, published, waiting_review, waiting_publication)` rows are `(3,2,3,1)`, `(6,2,3,5)`, `(9,2,0,12)`. Final accepted is 18 and published is six. Score five criteria 0–2: (1) correct arithmetic and queues; (2) both conservation checks; (3) identification of the actual downstream bottleneck; (4) a verifiable human/public outcome and falsifier; (5) separation of synthetic results from live Streeling evidence. A proposed pilot pass is at least 8/10 without calling a draft or synthetic publication a real one; evaluate this threshold after an actual learner trial. No result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, course blob, kind (`subject` or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. There is no translation of PSY-003 to approve. The draft exact-source receipt contract in Demerzel PR #1211 still requires human schema review; do not invent an approval receipt from this packet.

Keep review and publish flags false until actual verdicts and learner evidence are recorded. After accepted source integration, generate Learn, deploy, and anonymously read back the PSY-003 page with its source SHA. The isolated local Learn import is not public readback.
