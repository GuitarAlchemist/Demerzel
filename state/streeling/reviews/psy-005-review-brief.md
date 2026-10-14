# PSY-005 bounded review brief

Status: **open**. This is a human-review and learner-trial packet, not an approval receipt and not evidence that any forecasting model was evaluated.

## Frozen target and inputs

- English course: `state/streeling/courses/psychohistory/en/psy-005-persistence-baseline.md`, Git blob `f4e0789bce43d6945e3311229b0a8522f63404f0` (the blob identifies the exact text; `git log --diff-filter=A --format=%H -- state/streeling/courses/psychohistory/en/psy-005-persistence-baseline.md` names the commit that added the file).
- Fixture folder `state/streeling/fixtures/psychohistory/psy-005/`:
  - `extract.py`: Git blob `db36bacecf19001cc979f83384caddbdd9fc3068`
  - `observed-input.json`: Git blob `36ac390c0e3b5b08b10fc4938ebc7990324e871a`
  - `scenarios.json`: Git blob `5e2bbf06b5ca249d1e8494d55b926c22cc9043a0`
  - `analyze.py`: Git blob `1002d21d3b3e031fbd73e87e12eb5e4c656f0c29`
  - `results.json`: Git blob `059ffcd8cf00ab46f568d7c58a818ba5d63543ad`
  - `README.md`: Git blob `39395fe6751f82a0e6a15e51428215862d50734c`
- Observed source: `state/quality-trend/2026-05.jsonl`, `2026-07.jsonl`, `2026-08.jsonl`, `2026-09.jsonl`, `2026-10.jsonl` and `state/evolution/2026-03-20-autonomous-driver.evolution.json` at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`. Their Git blob ids are recorded in `observed-input.json` under `source` and checked by `extract.py`. These files are project records, not a human verdict on the course.
- Production record: `state/streeling/course-productions/cp-psychohistory-2026-10-13-005.json`; review and publication flags are false.

A later course edit changes its blob. Review that diff explicitly before extending a verdict to the new source.

## Subject and method review

1. Rerun the fixture from the repository root: `python -I state/streeling/fixtures/psychohistory/psy-005/extract.py`, then `analyze.py`, then `analyze.py --check`. On a checkout where the daily job has appended rows since the pin, `extract.py` must refuse to run (blob mismatch); check out the pinned commit, or review the saved `observed-input.json`. Recount independently of the scripts: 1,548 lines in the five JSONL files, 88 distinct timestamps on 83 UTC dates, 18 distinct artifacts, 11 rows with `"baseline": true`.
2. Check the unit of a forecast. Recompute `1,548 − 18 = 1,530` row pairs and `1,530 − 1 = 1,529` usable pairs, and the cross-check `1,540 − 11 = 1,529`. Read line 104 of `scripts/quality_trend.py` at the pin and confirm that `effectiveness_from` is the previous row's `effectiveness_to`. Challenge the choice of consecutive rows over in-row pairs: does the lesson justify it, and would scoring per run (86 of 87, 98.85%) change its conclusion?
3. Recompute the persistence table: 1,528/1,529 = 0.999346; 10/11 for the pairs that start at a seed row (78.5 days); 72, 1,433 and 13 pairs between feeder runs, with no change. The 0.5-day and 1.5-day bounds are an analysis choice stored in `scenarios.json`: confirm that no other choice moves the changed pair, which starts at a seed row. Recompute "always T" as 775/1,529 = 0.506867 and note that T was chosen with hindsight.
4. Recompute the skills of the four imaginary forecasters (0, −1, 1, −2) and the tie at a cost ratio of 3 for `cautious_alarm`. Read the lesson for any sentence that presents these forecasters as existing models or as a measurement of the project. Challenge the sentence "a reported accuracy near 99.9% carries no information about whether it can anticipate a change": is it narrow enough, given that persistence itself is informative about the next label?
5. Check the sources. Finley's table (28, 72, 23, 2,680; 2,803 forecasts) against the cited JWGFVR page and Murphy (1996); the four method references as cited; and the claim about `contracts/galactic-protocol.md`, which rests on one file read at commit `d9ddbaf9203a12b14c31b580070599efb8498031` outside the fixture.
6. Weigh the objection the lesson raises against itself. Is a `demoted` event dated 2026-07-18 enough to call the single change a recorded retirement and not a drift? Should the headline be 99.93% (all pairs) or 100% (pairs between feeder runs)? Is "this sample cannot distinguish a stable system from an unrevised record" supported, given that the edit history of the evolution records was not read?
7. Attempt the five exercises before reading their answer blocks. Record ambiguity, missing inputs or arithmetic errors with section references.

## Answer-free learner trial

Give [`psy-005-learner-task.md`](psy-005-learner-task.md) without this brief or the course answer blocks. Record prior experience with forecasting and classification metrics, elapsed time, the unedited response, confusion, and any lesson revision followed by retest.

Expected answers, copied from `results.json` under `transfer_task` (a hypothetical registry, computed from `scenarios.json`):

- Question 1: 25 runbooks, `20 × 26 + 4 × 21 + 1 × 23 = 627` rows, `627 − 25 = 602` row pairs, and 600 usable pairs because the unlabelled row in mid-history removes the pair that ends at it and the pair that starts at it. 12 changed, 588 unchanged: persistence accuracy 588/600 = 0.98 (98.00%), base rate of change 12/600 = 0.02 (2.00%).
- Question 2: Mirror 12 errors (12 misses), accuracy 588/600 = 0.98. Sentinel 3 misses and 21 false alarms, 24 errors, accuracy 576/600 = 0.96. Scout 6 misses and 4 false alarms, 10 errors, accuracy 590/600 = 0.983333 (98.33%).
- Question 3: skill against persistence is 0 for Mirror, −1 for Sentinel and 1/6 = 0.166667 for Scout. Mirror's 98% carries no information beyond the baseline: it makes exactly the errors of persistence.
- Question 4: share of changes announced 9/12 = 75% for Sentinel and 6/12 = 50% for Scout; share of alarms that were false 21/30 = 70% and 4/10 = 40%. With a miss costing ten false alarms, the weighted costs are 120 for persistence and for Mirror, 51 for Sentinel and 64 for Scout. Ranking by cost: Sentinel, Scout, Mirror. Ranking by accuracy: Scout, Mirror, Sentinel.
- Question 5 has no single answer. A sufficient plan fixes the unit (consecutive labelled rows), the baseline (persistence on the same pairs), the window and the score before the data arrive, states a falsifier (for example, Scout's errors on the new window are not below those of persistence, or its weighted cost at the agreed ratio is not lower), and says that a window with few changes cannot settle the claim.

Score five criteria 0–2: (1) the count of forecasts, including the two pairs lost to the unlabelled row; (2) persistence accuracy and base rate of change; (3) errors, accuracy and skill for the three models, with Mirror identified as no better than persistence; (4) misses against false alarms and the cost-weighted decision; (5) a test plan fixed in advance with a falsifier, and the hypothetical registry kept apart from Streeling evidence. A proposed pilot pass is at least 8/10 without presenting the registry or the imaginary forecasters as measurements; evaluate this threshold after an actual learner trial. No result exists yet.

## Verdict and publication boundary

No verdict exists. When one is given, record reviewer identifier or pseudonym, UTC date, course blob, kind (`subject` or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. There is no translation of PSY-005 to approve, and no learner has attempted the task.

Keep the review and publish flags false until actual verdicts and learner evidence are recorded. After accepted source integration, the page still has to be generated, deployed and read back anonymously with its source SHA before anyone calls PSY-005 published.
