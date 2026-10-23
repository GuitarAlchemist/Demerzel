---
module_id: psy-018-backtesting-without-leakage
department: psychohistory
course: "Backtesting Without Leakage"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-018
version: "0.1.0"
---

# Backtesting Without Leakage

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

A *backtest* scores a forecasting method on data that already exist, as if each value had not arrived yet. You will decide what one forecast is in an uneven record, roll the origin through it, score three simple methods, and recognise three ways a later value enters an earlier forecast. **Project question:** how do we test a forecast of an artifact's citation count without letting the future leak into the test?

[PSY-005](psy-005-persistence-baseline.md) scored "nothing changes" on labels. A numeric series adds errors with a size, and statistics to fit, where leaks enter. [PSY-011](psy-011-measurement-change-or-system-change.md) studies the change of instrument set aside here; [PSY-004](psy-004-how-large-is-large.md) explains why observations that share a cause count for fewer.

## 1. What there is to forecast

**Observed.** At each *run*, the *feeder* [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py) appends one row per governance *artifact* (a policy, a skill) to [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend). `citation_count` is meant to be [the number of tracked files that mention the artifact](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15); lessons count, hence the spaced slashes below. `delta_citations` is, by [line 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), the count minus the previous row's count, or 0 on a row flagged `rebaseline`.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/extract.py) snapshots these files at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-018/observed-input.json): **1,548** rows, **88** runs, **18** artifacts. The 11 rows of the first run are seed rows without a count, leaving 1,537 counted rows and 1,537 − 18 = 1,519 *pairs of consecutive rows* of one artifact.

The count differs in **20** pairs: 16 end on 2026-09-13 and 4 on 2026-10-03. Until the first date the counts were [typed by hand and never updated](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8); in the run of 2026-09-13T17:52:14Z a `git grep` count replaced them for 16 artifacts (`policies / alignment-policy.yaml` went from 3 to 42) and the feeder flagged those rows `rebaseline: true`. The *instrument*, the procedure that produces the number, had changed. This module restarts each series at a rebaseline row: a *series* is one artifact under one instrument. That gives **34** series (16 before a rebaseline row, 16 from one, 2 artifacts never re-measured) and 1,519 − 16 = 1,503 pairs inside a series.

Inside the series, **4** pairs change, in 4 artifacts: all in the run of 2026-10-03T15:31:16Z, all by +2 (42 to 44, 43 to 45, and 27 to 29 twice). The other 30 series never vary.

- **Two sets of twenty.** 20 rows carry a non-zero `delta_citations` and 20 rows differ from the previous row's count, yet only 4 rows are in both sets: sixteen non-zero deltas sit on an artifact's first counted row, where the feeder subtracts 0, and the 16 rebaseline rows changed while their delta was written as 0. This module counts changes of value.
- **A run is not a day.** Consecutive feeder runs lie 0.001 to 6.453 days apart: "one step ahead" means one run ahead.

### Practice Exercise 1

A forecast needs two earlier rows of its series. Starting from 1,548 rows, derive the number of forecasts the 34 series offer. Which rows have a non-zero delta although their count did not change?

> **Answer:** `1,548 − 11 = 1,537` counted rows; `1,537 − 18 = 1,519` pairs; `1,519 − 16 = 1,503` pairs inside a series; the first pair of each series has only one earlier row, so `1,503 − 34 = 1,469` forecasts. The `20 − 4 = 16` rows are first counted rows, 12 on 2026-07-18 and 4 on 2026-07-29: their delta is the count itself.

## 2. Roll the origin

A forecast has an *origin*, the last row it may use, and a *target*, the row it predicts. A *split in time* puts every training row before every test row. A *rolling origin* repeats the split: each row in turn is the target, forecast from the rows before it only ([Hyndman and Athanasopoulos, section 5.10](https://otexts.com/fpp3/toolbox.html#sec-tscv); Tashman 2000). Three methods, for a series y_1 … y_t known at origin t:

```text
persistence (naive)   forecast = y_t
mean so far           forecast = (y_1 + ... + y_t) / t
drift                 forecast = y_t + (y_t - y_1) / (t - 1)

error = actual - forecast          MAE = mean of |error|
relative MAE = MAE / MAE of persistence, on the same forecasts
```

**Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/analyze.py) into [`results.json`](../../../fixtures/psychohistory/psy-018/results.json), rounded to 6 decimals:

| Method | Total absolute error (1,469 forecasts) | MAE, one varying series (30 forecasts) | Relative MAE |
|---|---|---|---|
| persistence | 8 | 0.066667 | 1 |
| drift | 11.177980 | 0.093150 | 1.397247 |
| mean so far | 72.156930 | 0.601308 | 9.019616 |

Persistence errs by 2 at each of the four steps. The other two make the same errors and keep paying: the mean lags behind the new level for ten more rows, and drift extrapolates a rise that happened once. All these errors lie among the 480 forecasts on `git grep` counts; the 819 on hand-typed counts and the 170 on the two artifacts never re-measured re-read a number nobody updated. There every method is exact, and the relative MAE of the 30 flat series is 0/0.

A *scaled error* (Hyndman and Koehler 2006) divides each error by the naive forecast's MAE inside the training rows:

```text
scale at origin t = (|y_2 - y_1| + ... + |y_t - y_(t-1)|) / (t - 1)
scaled error      = |error| / scale
```

Here the scale stays at 0 until a series has changed: only 40 of the 1,469 forecasts have a positive scale, none in a flat series, and persistence's four errors fall on origins where it is still 0. Over the 40, persistence scores 0 and drift 1: once each series restarts at its rebaseline row, the score exists only where nothing is left to measure.

### Practice Exercise 2

`policies / alignment-policy.yaml` reads 42 for 21 rows, then 44 for 11 rows. Compute the three forecasts of row 23 (origin: row 22) and their errors, then the MAE of persistence over this series' 30 forecasts.

> **Answer:** Persistence: 44, error 0. Mean so far: `(21 × 42 + 44) / 22 = 42.090909`, error 1.909091. Drift: `44 + (44 − 42) / 21 = 44.095238`, error −0.095238. Persistence errs once, by 2, at row 22: MAE `2 / 30 = 0.066667`.

### Practice Exercise 3

Same series. Give the scale at origins 21 and 22, then each method's scaled error for row 23. What is the scaled error of the forecasts of row 22?

> **Answer:** At origin 21 every row reads 42: scale 0. At origin 22, one change of 2 in 21 pairs: `2 / 21 = 0.095238`. Row 23: persistence 0, mean so far `(42 / 22) / (2 / 21) = 20.045455`, drift `(2 / 21) / (2 / 21) = 1`. At row 22, the step, every method errs by 2 over a scale of 0: undefined.

## 3. Three ways the future gets in

A backtest **leaks** when a forecast uses an input not yet recorded at its origin: the target, a later row, or a number derived from them (a mean, a scale, a fitted parameter), later rows put among the training rows by a random split included (after Kaufman et al. 2012). One question tests any number in a pipeline: *could it have been written down at the origin?* A related error changes no forecast yet biases the score: choosing targets with later information, a *selection with hindsight*. Choosing a method on the test rows is the test-set reuse of [PSY-013](psy-013-four-scores-and-a-trend.md).

Persistence fits nothing, so two of the three leaks cannot reach it; they reach any method that fits a statistic. The simplest is a *level*: the mean of the training rows, forecast for every test row. **Computed:** take one varying series (32 rows; the four give identical numbers) and test on its last quarter, a choice stored in [`scenarios.json`](../../../fixtures/psychohistory/psy-018/scenarios.json).

| Test of the fitted level | MAE on the 8 test rows | Change |
|---|---|---|
| Split in time: level from rows 1 to 24 | 1.75 | reference |
| Leak 1: level computed on all 32 rows, test rows included | 1.3125 | −25% |
| Leak 3: 8 test rows drawn at random, level from the other 24, later rows among them | 0.931452 | −46.77% |

The third figure is the exact average over the 10,518,300 ways to draw the test rows; only 165 report an error as large as the split in time.

**Leak 2** is a feature that encodes the target: forecast "previous count + `delta_citations` of the target row". Under the rolling origin it makes no error in 1,469 forecasts, where persistence errs four times: −100%.

Leaks 1 and 3 do not always flatter. Across the 30 cuts that leave at least two training rows, leak 1 lowers the error at 21 (by up to 34.38%), ties at 1 and raises it at 8 (by up to 25%); leak 3 lowers it at 23 and raises it at 7. Under the rolling origin, the mean of the whole series scores 0.916667 against 0.601308 for the mean so far, 52.45% worse, because the honest mean is exact while the series is flat. A leak makes the score wrong, in a direction that depends on where the change falls among the test rows.

### Practice Exercise 4

With "could it have been written down at the origin?", classify as a leak, a selection with hindsight or neither: (a) a scale computed on the whole series; (b) a test on "the artifacts that vary" only; (c) `delta_citations` of the origin row. Then compute the leak-2 forecast for `constitutions / asimov.constitution.md` at its rebaseline row: previous count 5, `delta_citations` 0, actual 65.

> **Answer:** (a) Leak: the scale contains later rows; it would make every scaled error of a varying series defined (persistence 1.033333). (b) Selection with hindsight: no forecast changes, but which artifacts vary is known only at the end of the record; the pooled 1,469 forecasts avoid that choice. (c) Neither: that delta was recorded at the origin. Forecast `5 + 0 = 5`, error 60. The leaked feature fails where the feeder wrote 0: over all 1,519 pairs it misses the 16 rebaseline rows, a total absolute error of 306.

## 4. What this backtest can show

**Four series, one event.** The four changes share a run and a size; the four series share one error profile, so section 2's ratios repeat by construction. Of 85 target runs, one holds every error of persistence. Read outside the fixture, the history is consistent with one cause: between the two runs, commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642) added 26 translated lessons, six of which spell these artifacts' paths, two per artifact. To forecast this count is to forecast what gets written in the repository, lessons included. "Persistence beat drift on 4 of 4 series" sounds like four coin tosses (an analogy), a chance of 1/16; with one event it is one toss, 1/2.

**The strongest objection to this lesson** is that its own test depends on a later value. The `rebaseline` flag sits in the target row: at the origin of 2026-09-13T15:24:53Z nobody could know that the next run, 0.102 days later, would change the instrument. Restarting the series there is a selection with hindsight: it removes 16 targets using later information. Without the restart, persistence's total absolute error is 314 in place of 8, and 306 of it (97.45%) lies on the rebaseline rows. The two figures answer different questions, "what will the file say?" and "what will this instrument read?"; a report must say which it gives.

**This sample cannot distinguish** a step process from a slow trend, nor rank the methods beyond one step: under a fixed instrument it holds one event in 31 run-to-run steps. It shows something narrower: the bookkeeping of a test moved a reported error, by −100% to +52.45% through the three leaks and from 8 to 314 through the choice of targets. Only a longer record would settle more.

### Practice Exercise 5

(a) Why is 1/16 the wrong chance for "4 of 4"? (b) Assume, only for scale, that runs with a change keep arriving once per 31 run-to-run steps. How many runs until 10 such runs are expected, against the 32 recorded since the rebaseline?

> **Answer:** (a) `(1/2)^4 = 1/16` needs four independent comparisons; the four steps share one run and one size: one event, chance `1/2`. (b) `10 × 31 = 310` steps, so 311 runs, about ten times the 32 recorded. The rate rests on one change run: an order of magnitude, not a schedule.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the five JSONL files of `state/quality-trend/` and the two scripts linked above.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-018/extract.py`, then `analyze.py`, then `analyze.py --check`; the [README](../../../fixtures/psychohistory/psy-018/README.md) lists the 35 self-checks, the closed forms and the negative controls.

**Method references.** Hyndman, R. J., and Koehler, A. B. (2006), "Another look at measures of forecast accuracy", *International Journal of Forecasting* 22(4), 679–688. Tashman, L. J. (2000), "Out-of-sample tests of forecasting accuracy: an analysis and review", *International Journal of Forecasting* 16(4), 437–450. Kaufman, S., Rosset, S., Perlich, C., and Stitelman, O. (2012), "Leakage in data mining: Formulation, detection, and avoidance", *ACM Transactions on Knowledge Discovery from Data* 6(4), 1–21. Hyndman, R. J., and Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, 3rd edition, OTexts, sections 5.2, [5.8](https://otexts.com/fpp3/toolbox.html#sec-accuracy), 5.10.

**Not done.** No model beyond the three benchmarks was fitted. The uneven time between an origin and its target (0.001 to 6.453 days) was not modelled. The history was read by hand, outside the fixture. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Rerun the fixture once the record holds several change runs with separate causes under one instrument: a method that then beats persistence would turn "cannot rank" into a ranking with a stated uncertainty.
