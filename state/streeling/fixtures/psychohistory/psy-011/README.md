# PSY-011 fixture: instrument changes in the citation counts

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-011/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-011-measurement-change-or-system-change.md`.
Python 3.9 or later, standard library only. No random number is drawn, so there is no seed.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads `state/quality-trend/*.jsonl`, the two scripts that produce the citation counts (`scripts/quality_trend.py`, `scripts/evolution_metrics.py`) and the 18 `state/evolution/*.evolution.json` records, checks their shape, their Git blob ids and the code lines the lesson quotes, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot (artifact names and citation paths as labels, see below) at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the 88 run timestamps; for each of the 18 artifacts five aligned columns with one cell per run (`citation_count`, `delta_citations`, `citation_source`, `rebaseline`, the `baseline` flag) and the citation paths, count, source and `last_cited` of its evolution record; the quoted code lines; the counts made by `extract.py`. |
| `scenarios.json` | assumed | The alarm rule (2 standard deviations, at least 3 earlier steps), two thresholds that describe the spacing of the runs, seven imaginary rows for the feeder's rule, and the hypothetical defect log of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, re-implements lines 90-99 of the pinned feeder, classifies every row, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-011/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-011/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-011/analyze.py --check
```

The three commands finish in a few seconds. `analyze.py` writes the same bytes on every run (LF line endings,
`indent=2`, insertion-ordered keys, ratios rounded to 6 decimals, percentages to 2, means, standard deviations, days and steps per day
to 4). Every decision of the alarm rule is taken on exact fractions; the only floating-point operations are the conversion
of an exact fraction, one square root and a doubling, which give the same bits on every platform. `--check` recomputes the results and compares them with
the saved file, ignoring only CRLF against LF.

`extract.py` stops with exit code 1 when a source file is missing, when a row lacks a key or has a malformed value,
when a quoted code line no longer contains the expected text, or when a source file is not the blob of the pinned
commit (the nightly feeder appends rows, so this happens on any later checkout). `--allow-drift` snapshots newer data
anyway and records `"commit": null`; the lesson's numbers then no longer apply, and `analyze.py` may stop on a
self-check that describes the pinned data (one instrument change, in one run).

## Artifact names are labels

Artifact names and citation paths are written with a space on each side of every slash
(`policies / alignment-policy.yaml`): the repository's producer, `scripts/evolution_metrics.py`, counts every tracked
file that contains one of an artifact's citation paths as a literal string, and a module that listed the paths
unspaced would raise the very counts it studies. `extract.py` passes every artifact name and every citation path
through one function, `label()`, when it reads them, whether or not the name is a plain path
(`skills / demerzel-drive + policies / autonomous-loop-policy v1.1.0`, `crates / memristive-markov (ix)`): a name
without a slash is unchanged, and a trailing slash stays as ` /` (`scripts / afk_backends /`). Removing the
spaces around each slash gives the name back, and `extract.py` stops if two artifact names would share a label.
The artifacts stay in the order of their names in the repository. No file of this module holds a citation path
literally: the two scripts and the two folders it reads are not citation paths of any artifact.

## Observed, computed, synthetic

- **Observed:** the cells, timestamps, evolution-record fields and code lines in `observed-input.json`.
- **Computed from the observed data:** `observed`, `feeder_rule.reproduction_on_observed_rows`, `instrument_change`,
  `classification`, `total_series`, `two_sigma` and `negative_controls` in `results.json`. The alarm rule of
  `two_sigma` is an analysis choice stored in `scenarios.json`, not an alarm the project runs.
- **Synthetic:** `feeder_rule.rule_cases` (imaginary rows) and `transfer_task` (a hypothetical defect log).

## How a row is classified

Each row is compared with the previous row of the same artifact, reading a missing `citation_source` as null, as the
feeder does:

| Class | Condition |
|---|---|
| `no_count` | the row has no `citation_count` (the 11 seed rows) |
| `first_count` | the row has a count and no earlier row of the artifact has one |
| `instrument_change` | the previous row has a count and another `citation_source` |
| `same_instrument` | the previous row has a count and the same `citation_source` |

"The count changed" is defined only for the last two classes. The three step series of `two_sigma` start after the
first feeder run: the step of the summed count (`total`), the sum of `delta_citations` as recorded
(`recorded_delta`), and the summed steps of `same_instrument` rows only.

A step is per run, and the runs are not evenly spaced: `two_sigma.run_spacing` gives the 86 gaps between
consecutive feeder runs (from 122 seconds to 6.4533 days, median 0.9986 days). `two_sigma.per_day` therefore applies the
same rule to each step divided by the gap since the previous run, in days. It flags the same runs as the rule per
run in the three series.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 64 named checks fails; `results.json` lists them
under `checks`. They include a recount of every count made by `extract.py` through a second code path, the accounting
identities (the four classes sum to the rows; rows minus artifacts = pairs of consecutive rows of one artifact = pairs from a row without a count +
pairs across an instrument change + same-instrument pairs; for every run, the step of the total = first counts +
steps at the instrument change + same-instrument steps, and the recorded `delta_citations` = first counts +
same-instrument steps), the agreement of each artifact's latest row with its evolution record, and the reproduction
of the recorded `delta_citations` (1,537 rows) and `rebaseline` flags (576 rows) by the re-implemented rule. The same
identities are checked on the transfer task and on a case worked by hand:

```text
runs        1  2  3  4  5  6
a  count    -  3  3  9  9 11     source  - - - g g g    ('-' : no count, or no citation_source key)
b  count    .  .  2  2  2  2     source  . . - - n n    ('.' : no row; 'n' : key present, null)

a: run 1 seed row; run 2 first count (delta 3); run 4 instrument change 3 -> 9 (flag, delta 0);
   run 6 same-instrument change +2 (delta 2)
b: run 3 first count (delta 2); run 5 null after a missing key: same instrument, no flag
10 rows = 1 without count + 2 first counts + 1 instrument change + 6 same instrument
3 non-zero deltas, 2 count changes, 1 row is both; totals 0, 3, 5, 11, 11, 13 = deltas 7 + hidden step 6
```

For the alarm rule: after the steps 1, 3, 1, 3 (mean 2, population standard deviation 1) a step of 6 is flagged, a
step of 4 is not, and 5 is the smallest step that is; after an all-zero history any non-zero step is flagged. Per
day, after 1, 3, 1, 3 a step of 6 in three days (2 per day) is not flagged and a step of 3 in half a day (6 per
day) is; and with equal gaps the rule per day must flag exactly the steps that the rule per run flags.

Four results could pass on nothing: "0 count changes where no source is recorded", "0 non-zero deltas at an
instrument change", "0 flags the rule does not reproduce" and "16 instrument-change rows, all flagged". The negative
controls plant one defect at a time in a copy of the rows (a count raised by one for one run, a delta of 5 on a
rebaseline row, a flag where the source did not change, a source changed without a flag) and confirm that the
matching counter moves (0 to 2, 0 to 1, 0 to 1, 16 to 17 with one unreproduced flag).

A fifth could too: "the rule per day flags the same runs as the rule per run". Its control moves the last non-zero
step of the total (+8 on 2026-10-03) from its gap of 80,407 seconds to the shortest observed gap, 122 seconds: the
step per day goes from 8.5963 to 5665.5738 and the rule per day flags it, while the rule per run still does not.

## Limits

- The snapshot keeps the citation columns only; effectiveness labels belong to PSY-005.
- Rows written before 2026-09-13 lack `citation_source` and `rebaseline`: an earlier version of the feeder wrote
  them. The fixture reads the feeder at the pinned commit only and reports that its rule reproduces those rows; it
  does not read the earlier versions.
- "Same instrument" means "same `citation_source` label". A change of the producer's code, of its exclusion list or
  of an artifact's `citation_paths` that keeps the label is invisible to the fixture, as it is to the feeder.
- Git history is not part of the fixture. The lesson's two statements about history (the producer script's single
  commit, and the files added between the runs of 2026-10-02 and 2026-10-03) were read once with the commands listed
  in `state/streeling/reviews/psy-011-review-brief.md`.
- One instrument change and four same-instrument steps, all four in one run: every statement about "what changes
  look like" rests on these.
