# PSY-018 fixture: a rolling-origin backtest of citation counts, and three leaks

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-018/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-018-backtesting-without-leakage.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads `state/quality-trend/*.jsonl`, checks each row's shape and each file's Git blob id, checks the blob ids of the two scripts the lesson quotes (`scripts/quality_trend.py`, of which it reads line 99, and `scripts/evolution_metrics.py`), and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the 88 run timestamps and, for each of the 18 artifacts, five run-aligned strings (`citation_count`, `delta_citations`, the `baseline` flag, the `rebaseline` flag, `citation_source`), plus the counts made by `extract.py`. |
| `scenarios.json` | analysis choices and assumptions | The rule that defines a series, the least number of training rows, the bounds for "about a day", the test share of the split in time, the seed of the cross-check, the extrapolation assumption and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, rebuilds every count from the strings, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

An artifact name is a data label here, written by `extract.py` with a space on each side of every slash
(`policies / alignment-policy.yaml`): `scripts/evolution_metrics.py` counts each tracked file that contains an
artifact's path as one citation of it, and files about the counts must not raise them.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-018/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-018/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-018/analyze.py --check
```

The three commands take about two seconds in total. `analyze.py` writes the same bytes on every run: LF line
endings, `indent=2`, insertion-ordered keys, exact fractions (`fractions.Fraction`) rounded only when stored, to 6
decimals for values, 2 for percentages and 3 for days. An `exact` field gives the unrounded fraction, left out when its
denominator has more than 12 digits. `--check` recomputes the results and compares them with the saved file, ignoring
only CRLF against LF.

`extract.py` stops with exit code 1 when a source file is missing, when a row lacks a key, has a malformed timestamp,
a `citation_count` that is not a non-negative integer, an unknown `citation_source`, a duplicate (timestamp, artifact)
or a count that is absent on a row not flagged `baseline` (or present on one that is); when line 99 of the feeder is
not the expected rule; or when a source file is not the blob of the pinned commit (the nightly feeder appends rows, so
this happens on any later checkout). `--allow-drift` snapshots newer data anyway and records `"commit": null`; the
lesson's numbers then no longer apply.

## Observed, computed, assumed

- **Observed:** the counts, deltas, flags and timestamps in `observed-input.json`, and line 99 of the feeder script.
- **Computed from the observed data:** `observed`, `variation`, `series`, `rolling_origin`, `scaled_error`, `leakage`,
  `dependence` (except its `extrapolation`), `whole_record_contrast` and `negative_controls` in `results.json`.
- **Analysis choices** (in `scenarios.json`, each one a decision a reviewer may challenge): a series restarts at a row
  flagged `rebaseline`; a forecast needs two earlier rows; the split in time tests on the last quarter of a series.
  `leakage.cut_sweep` repeats the leak comparison for every other cut.
- **Assumed:** `dependence.extrapolation` (a constant frequency of change runs).
- **Synthetic:** `transfer_task` (hypothetical weekly counts for the learner task).

One random draw exists: 20,000 seeded random splits (`random.Random(18018).random()`) that check the exact average over
all random splits through a second code path. No result of the lesson depends on it.

## Definitions

- A *series* is one artifact under one instrument: its rows that carry a count, restarted at each row flagged
  `rebaseline: true`. Rows are numbered from 1 inside a series.
- A *forecast* has an origin row t and predicts row t + 1 from rows 1 to t only: persistence `y_t`, mean so far
  `(y_1 + ... + y_t) / t`, drift `y_t + (y_t - y_1) / (t - 1)`. Each row with at least two rows before it is a target
  once.
- The *scale* at origin t is the mean absolute change between consecutive rows among rows 1 to t; the scaled error is
  `|error| / scale` and is undefined while the scale is 0.
- The *fitted level* of the leak comparison is the mean of the training rows, used as the forecast of every test row.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 35 checks fails; `results.json` lists them under
`checks`. They include a recount of every count made by `extract.py` through a second code path, the accounting
identities (rows with a count = rows - seed rows; pairs = rows with a count - artifacts; pairs inside a series = pairs -
pairs ending at a rebaseline row; forecasts = pairs inside a series - series), the feeder's rule for `delta_citations`
on all 1,537 counted rows, a closed form for a series with one step, a listing of every split for small series, and a
case worked by hand:

```text
series   5 5 5 7 7 7        targets: rows 3 to 6 (4 forecasts)
persistence   errors 0 2 0 0                      sum 2
mean so far   forecasts 5, 5, 5.5, 5.8            errors 0 2 1.5 1.2      sum 47/10
drift         forecasts 5, 5, 7 + 2/3, 7 + 2/4    errors 0 2 -2/3 -1/2    sum 19/6
scale at origins 2 to 5:  0, 0, 2/3, 1/2
last two rows as test:  level 5.5 from rows 1-4 (MAE 1.5), level 6 from all six rows (MAE 1)
```

For a series with c rows at one level, then a step d to a second level, n rows in all, and two training rows:

```text
persistence  sum of |errors| = d
mean so far  sum of |errors| = d * c * (1/c + 1/(c+1) + ... + 1/(n-1))
drift        sum of |errors| = d * (1 + 1/c + 1/(c+1) + ... + 1/(n-2))
```

The ratios between the three methods therefore depend only on c and n, not on the counts: the four observed series
that vary (c = 21, n = 32) give the same ratios by construction.

Three results could pass on nothing: "0 rows break the feeder's rule", "30 series never vary" and "the leaked feature
makes no error". The negative controls plant a defect in a copy of the snapshot and confirm that the counters move:
one count raised by 1 (count changes 20 to 22, broken deltas 0 to 2, series that vary 4 to 5, persistence error 8 to
10, leaked-feature misses 0 to 2), one `delta_citations` set to 1 (broken deltas 0 to 1, leaked-feature misses 0 to 1)
and one `rebaseline` flag removed (series 34 to 33, persistence error 8 to 68).

## Limits

- The snapshot keeps the citation counts, their deltas and three flags; labels, violations and compliance rates are
  left to other modules.
- Four counts change inside a series, in one run and by the same step: every ranking of methods in `results.json`
  rests on that single event.
- "Typed by hand" for the counts before a rebaseline row is the description given in `scripts/evolution_metrics.py`
  at the pinned commit; the fixture checks that file's blob id and does not test the claim.
- The fixture reads no git history. The lesson's sentence about commit `98625c3` (26 translated lessons added
  between the runs of 2026-10-02 and 2026-10-03, six of which spell the paths, two per artifact that changed) was checked by hand, with
  `git log --name-status` on the pinned commit and a search of the added files as they stand at the pin; it is not in
  `results.json`.
- One step ahead is one run ahead. The time between an origin and its target ranges from 0.001 to 6.453 days.
- The random-split formula handles a series with at most two distinct values, which is all this record and the
  transfer task contain.
- No forecasting model beyond the three benchmark methods was fitted or run.
