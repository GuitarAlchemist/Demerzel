---
module_id: psy-005-persistence-baseline
department: psychohistory
course: "Persistence First: The Baseline a Governance Forecast Must Beat"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-005
version: "0.1.0"
---

# Persistence First: The Baseline a Governance Forecast Must Beat

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will decide what counts as one forecast in a log, score the forecast "nothing changes", express any other forecast as a skill score against it, and say when that score cannot be computed. **Project question:** if a model predicts tomorrow's effectiveness label for each governance artifact, what accuracy does "nothing changes" already reach on the recorded quality trend?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) treats a fast change in the balance of truth-value labels as a sign of a coming regime shift. Any model that forecasts such labels must first be compared with the cheapest forecast available; this module builds that comparison for categorical labels. PSY-016 scores probability forecasts on the same pairs, PSY-006 turns them into a transition matrix, and PSY-018 backtests numeric series.

## 1. Decide what one forecast is

**Observed.** A [daily scheduled job](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) runs [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), which the repository calls the *feeder*. It reads one evolution record (a JSON file in `state/evolution/`) per governance *artifact* (a policy, a constitution, a schema, a skill) and appends one row per artifact to `state/quality-trend/`. All rows of one execution share a `timestamp`; call that a *run*. A row's `effectiveness_to` is the truth value the record currently gives to a written proposition about the artifact: T (true), P (probable), U (unknown), D (doubtful), F (false) or C (contradictory). Its `effectiveness_from` is [copied from the artifact's previous row](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L104).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/extract.py) snapshots these files at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-005/observed-input.json): **1,548** rows, **88** runs on **83** UTC dates, **18** artifacts. The first run differs in kind. Its 11 rows, stamped 2026-05-01, are flagged `baseline: true`: *seed rows* that record a starting state. The other 87 are *feeder runs*, from 2026-07-18 to 2026-10-13.

Both labels are present in 1,540 rows. Seven rows lack `effectiveness_from` because there was no earlier label to copy. One row, the first for `contracts/galactic-protocol.md`, lacks both: the feeder writes a null `effectiveness_to` when a record's assessment is free text, which is what [that record held at the time](https://github.com/GuitarAlchemist/Demerzel/blob/d9ddbaf9203a12b14c31b580070599efb8498031/state/evolution/2026-07-23-galactic-v1.3-ratification.evolution.json) (read once at commit `d9ddbaf`, outside the fixture).

A forecast needs a time of issue and a later time of verification. The data offer two readings:

- **In-row:** `effectiveness_from` against `effectiveness_to` inside one row, 1,540 pairs.
- **Consecutive rows:** an artifact's `effectiveness_to` in one row against its next row. There are 1,548 − 18 = 1,530 row pairs; 1 starts at the unlabelled row, which leaves **1,529**.

This lesson uses consecutive rows: each pair joins two labels recorded at two different times. The in-row count also contains the 11 seed rows, whose two fields were written together with no earlier row behind them: there was no earlier moment at which a forecast could have been made, and all 11 agree by construction. **Computed cross-check:** outside the seed rows the two readings give the same 1,529 pairs, and no row's `effectiveness_from` differs from the previous row's `effectiveness_to` (0 mismatches; `negative_controls` in [`results.json`](../../../fixtures/psychohistory/psy-005/results.json) shows that a planted mismatch is counted).

### Practice Exercise 1

Starting from 1,548 rows and 18 artifacts, derive the number of forecasts. Then derive it again from the 1,540 rows that carry both labels, and say why 1,540 itself is the wrong count.

> **Answer:** Each artifact's first row has no predecessor: `1,548 − 18 = 1,530` row pairs. One starts at the row without a label: `1,530 − 1 = 1,529` forecasts. From the other side, `1,540 − 11 = 1,529` once the seed rows are removed. Counting 1,540 would add 11 pairs with no earlier run behind them, each "correct" only because its two fields were written together.

## 2. Score the forecast that predicts nothing new

The *persistence forecast* says that the next label equals the current one; it needs no model and no training data. *Accuracy* is the share of forecasts that match the outcome. The *base rate of change* is the share of pairs whose label changed.

```text
accuracy             = correct forecasts / forecasts
base rate of change  = changed pairs / pairs
persistence accuracy = 1 - base rate of change
```

**Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/analyze.py) from the snapshot (percentages rounded to two decimals):

| Pairs | Count | Changed | Persistence accuracy |
|---|---|---|---|
| All usable pairs | 1,529 | 1 | 1,528/1,529 = 99.93% |
| From a seed row to the first feeder run, 78.5 days | 11 | 1 | 10/11 = 90.91% |
| Between feeder runs under half a day apart | 72 | 0 | 100% |
| Between feeder runs 0.565 to 1.372 days apart | 1,433 | 0 | 100% |
| Between feeder runs 6.453 days apart | 13 | 0 | 100% |

The answer to the project question is 99.93% over everything recorded, and 100% over the 1,433 pairs whose two rows are about one day apart. The base rate of change is 1/1,529 = 0.000654. The single change is U to F for `skills/demerzel-drive + policies/autonomous-loop-policy v1.1.0`; the labels of the other seventeen artifacts never changed in the record.

The unit and the reference both matter. Scored per run ("no label changes in this run"), persistence is right for 86 of 87 target runs, 98.85%. Another cheap forecast, "always T" (the most frequent outcome, chosen with hindsight), is right for 775 of 1,529 pairs, 50.69%. A model has to beat the best cheap forecast, not zero and not the weakest one.

### Practice Exercise 2

From the table and the paragraph above, compute the persistence accuracy and the base rate of change (a) over all usable pairs and (b) over all pairs between feeder runs. Then compute the accuracy of "always T".

> **Answer:** (a) `1,528 / 1,529 = 0.999346`, or 99.93%; base rate `1 / 1,529 = 0.000654`. (b) `72 + 1,433 + 13 = 1,518` pairs and no change: accuracy 100%, base rate 0. "Always T": `775 / 1,529 = 0.506867`, or 50.69%. These are counts on the pinned snapshot, not forecasts of future runs.

## 3. Measure skill from the baseline

A *skill score* places an accuracy A on a scale where a reference forecast scores 0 and a forecast without error scores 1:

```text
skill = (A - A_ref) / (1 - A_ref) = 1 - E / E_ref
```

E and E_ref count the errors of the forecast and of the reference on the same pairs. A negative skill means the forecast did worse than the reference.

Here the reference is persistence, with E_ref = 1. The scale therefore moves in whole steps of 1: no error gives 1, one error gives 0, two errors give −1. No value between 0 and 1 can occur.

**Synthetic.** The models below do not exist. [`scenarios.json`](../../../fixtures/psychohistory/psy-005/scenarios.json) defines each by how it would have behaved on the observed pairs:

| Imaginary model | Behaviour | Accuracy | Skill |
|---|---|---|---|
| `echo` | outputs the previous label, whatever its internals | 99.93% | 0 |
| `one_false_alarm` | as `echo`, plus one announced change that did not happen | 99.87% | −1 |
| `one_right_call` | announces the one change and nothing else | 100% | 1 |
| `cautious_alarm` | announces the one change and three that did not happen | 99.80% | −2 |

The first row is the point of this module. A model reaches 99.93% by learning nothing beyond "copy the last label", so a reported accuracy near 99.9% carries no information about whether it can anticipate a change. Only the comparison with persistence does, and here that comparison rests on one pair: `one_right_call` earns the top score with a single call, which this sample cannot distinguish from a lucky guess.

### Practice Exercise 3

A vendor reports that its model was right on 1,527 of the 1,529 pairs. Give its accuracy and its skill against persistence. What does the report still not tell you?

> **Answer:** Accuracy `1,527 / 1,529 = 0.998692`, or 99.87%. It made 2 errors where persistence made 1: skill `= 1 − 2/1 = −1`, worse than copying the last label. The report does not say which errors they were: the missed change plus one false alarm, the change announced correctly plus two false alarms, or the change announced with the wrong new label plus one false alarm.

## 4. Misses, false alarms, and the strongest objection

Accuracy, and a skill score built on it, count every error alike. For rare changes there are two kinds: a *miss* (a change nobody announced) and a *false alarm* (an announced change that did not happen). A change announced with the wrong new label is an error too. Persistence never raises a false alarm and misses every change. If a miss costs c times a false alarm, compare `c × misses + false alarms`.

**Analogy (cited data, not project data).** In 1884, J. P. Finley's tornado forecasts were correct 96.61% of the time over 2,803 forecasts. Never forecasting a tornado would have scored 98.18%, yet Finley announced 28 of the 51 tornadoes, with 72% of his alarms false ([JWGFVR table](https://jwgfvr.github.io/forecastverification/); Murphy 1996). Which forecast was better depends on what a missed tornado costs.

### Practice Exercise 4

Synthetic. `cautious_alarm` announces the one change and raises three false alarms; persistence misses the change. For which cost ratio c is `cautious_alarm` the cheaper forecast, and what do both cost at c = 10?

> **Answer:** Persistence costs `c × 1 + 0 = c`; `cautious_alarm` costs `c × 0 + 3 = 3`. They tie at `c = 3`; above 3 the alarm is cheaper, below 3 persistence is. At `c = 10` the costs are 10 and 3. The alarm has the lower accuracy (99.80% against 99.93%) and a skill of −2, so the criterion is the cost of each kind of error, not accuracy. The model is imaginary: this says nothing about a real forecaster.

**The strongest objection to this lesson's reading** is that its one change is not a day-ahead event. It lies on the 78.5-day step from a seed row to the first feeder run, and the artifact's [evolution record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-03-20-autonomous-driver.evolution.json) dates a `demoted` event to 2026-07-18, the day of that run. That is a retirement someone decided and wrote down, not a drift that label history could reveal. Between feeder runs nothing changed in 1,518 pairs, so there persistence makes no error and skill is undefined (a division by zero): a model can equal persistence's zero errors or make more, never fewer. The labels are also written assessments that the feeder re-reads; an unchanged label may mean "nobody reassessed" as much as "still effective". **This sample cannot distinguish a stable system from an unrevised record, nor a skilled model from persistence.** Two things would settle it: the edit history of the evolution records (how often a truth value is re-examined, and how often it then changes), and a record long enough to hold several changes between feeder runs.

### Practice Exercise 5

Drop the 11 pairs that start at a seed row. (a) What is the persistence accuracy on the rest, and what skill can a model show there? (b) Assume, only to get a scale, that changes keep occurring in 1 of 1,529 pairs, whatever the time between the two rows, and that every run has 18 artifacts. After how many runs are 10 changes expected?

> **Answer:** (a) `1,529 − 11 = 1,518` pairs, none changed: accuracy 100%. E_ref is 0, so the skill score is undefined; a model can match persistence with no error or fall below it. (b) `10 × 1,529 = 15,290` pairs, and `15,290 / 18 = 849.4`, so 850 runs, against 87 feeder runs recorded so far. The assumption rests on one observed change, and that change lies on a 78.5-day pair, not a daily one: 850 is an order of magnitude, not a schedule.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the quality-trend files for [May](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-05.jsonl), [July](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-07.jsonl), [August](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-08.jsonl), [September](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-09.jsonl) and [October](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl) 2026 (there is no June file), the feeder script and the evolution record linked above. `extract.py` refuses to run if any of these files differs from its pinned Git blob.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-005/extract.py`, then `analyze.py` in the same folder; `analyze.py --check` compares a fresh run with the saved results. The [README](../../../fixtures/psychohistory/psy-005/README.md) lists every file, the self-checks and the negative controls.

**Method references.** Hyndman, R. J., and Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, 3rd edition, OTexts, [section 5.2](https://otexts.com/fpp3/simple-methods.html) (the naïve forecast, which is persistence for numeric series). Jolliffe, I. T., and Stephenson, D. B., editors (2012), *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, 2nd edition, Wiley (accuracy and skill scores). Murphy, A. H. (1996), "The Finley Affair: A Signal Event in the History of Forecast Verification", *Weather and Forecasting* 11, 3–20. Murphy, A. H. (1993), "What Is a Good Forecast? An Essay on the Nature of Goodness in Weather Forecasting", *Weather and Forecasting* 8, 281–293 (a forecast's quality against its value to a user).

**Not done.** No forecasting model was trained or run; the four models are imaginary. No interval was put on the base rate (PSY-006 treats rarely or never observed transitions) and no probability forecast was scored (PSY-016). The edit history of the evolution records was not read. No human subject review, learner trial, translation or publication of this lesson has taken place.

**Next check.** Count, in the Git history of `state/evolution/`, how often each truth value was re-examined and how often it changed. If labels are almost never re-examined, the conclusion changes from "this sample cannot distinguish a skilled model from persistence" to "this label is not a daily observable", and the forecast question should move to a quantity measured at every run.
