# PSY-009 fixture: concentration of the archived trigger log

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-009/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-009-concentration-and-heavy-tails.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the 594 files of `state/triggers/archived/`, the retired driver's skill file and the workflow that wrote the triggers, checks their shape and their pins, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: one row per event (`<timestamp> <type>`), the events per calendar day, the counts made by `extract.py`, and what the two design files state (queue limit, staleness limit, deduplication rule, "never scheduled", 594 orphaned triggers). |
| `scenarios.json` | assumed | Every analysis choice (which top-k, the quantile rule, the median rule, PSY-008's burst threshold and episode gap, the day-boundary offsets, the type subsets, the dates of reading), the capacity rule and its plans, the synthetic control (number of logs, seeds, tolerances), the cases worked by hand, two imaginary logs for an exercise and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts everything from the event rows, runs the self-checks and writes `results.json`. `analyze()` calls one function per section of `results.json`, in the order in which the self-checks are recorded. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-009/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-009/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-009/analyze.py --check
```

`extract.py` takes about a second and `analyze.py` about three. `analyze.py` writes the same bytes on every run and
on every machine: LF line endings, `indent=2`, insertion-ordered keys, and no `exp`, `log` or power on floats (the
only floating-point step is `rng.random() * days` in the generator of the synthetic logs). Every stored number is an
integer count or an exact fraction of integers, rounded half up once when it is written (shares to 6 decimals,
percentages and means to 2, Gini coefficients to 4). `--check` recomputes the results and compares them
with the saved file, ignoring only CRLF against LF.

The folder is pinned as a whole, not file by file: `extract.py` rebuilds the Git blob id of each trigger file, then the
Git tree id of the folder and the SHA-256 of the lines `<blob id> <path>`, and compares the file count (594), the tree
id (`2da37c16496d39c0c9137897c8be2b0c6d6b7978`) and the digest
(`3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393`) with the values of the pinned commit. To
reproduce the digest without the script:

```text
git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum
```

The two design files are pinned by their Git blob ids. `extract.py` stops with exit code 1 when the folder or a file
is missing, a trigger file has an unexpected name, key set or timestamp, its name disagrees with its JSON, a pattern
no longer matches a design file exactly once, or a pin differs. `--allow-drift` snapshots other data anyway and
records `"commit": null`; the lesson's numbers then no longer apply.

`observed-input.json` writes the paths of the two design files with a space on each side of every slash: the
repository counts, for each governed file, the tracked files that contain its path as a literal string, and a data
file must not add to the count of a file it only records.

## Observed, computed, synthetic

- **Observed:** the event rows, the daily counts and `design` in `observed-input.json`. `design` records what the
  repository *states* about the consumer of these triggers; it is not a measurement of any consumer.
- **Computed from the observed data:** `observed`, `busiest_days`, `lorenz_and_gini`, `mean_and_median`, and in
  `robustness` the sections `day_boundary` and `type_subsets`.
- **Synthetic:** `poisson_control` (2,000 seeded logs with the observed total and number of days, each event on a day
  drawn uniformly at random), `capacity` (an assumed handling rule applied to the observed daily counts and to the
  synthetic logs), `robustness.deduplicated_once_a_day` (the design's stated rule with an assumed daily wake),
  `candidate_logs` (two imaginary summaries) and `transfer_task` (a hypothetical support desk).

Two rules give a middle value and they differ. The median is the middle value of the sorted counts, and the mean of
the two middle values when their number is even. A percentile is read by nearest rank, the value at position
`ceil(p * n / 100)`, so the 50th percentile of an even number of values is the lower of the two: on the first 12 days
the median is 4.5 and the 50th percentile is 4 (`mean_and_median.read_to_date`).

## Plans sized before the end of the log

Every plan of `capacity.plans` is sized on the 119 days it is then run on. `capacity.plans_sized_on_an_earlier_reading`
measures what that hindsight is worth: each plan is sized on the days read up to the end of March, April, May and June
(`mean_and_median.read_to_date` gives the percentiles read on those dates), then run on the days that follow, with an
empty queue on the first of them. The 95th percentile read on 2026-05-31 is 8, against 24 on the whole log, and a
capacity of 8 leaves 199 late events on the 46 days left. With fewer than 100 days read, the 99th percentile by
nearest rank is the busiest day read so far.

## The Gini coefficient, and the cases worked by hand

With the n daily counts sorted in increasing order, x_1 <= ... <= x_n, and T their total:

```text
G = sum over i of (2i - n - 1) * x_i / (n * T)

all days equal         3 3 3 3     weights -3 -1 1 3     sum 0                    G = 0
one day holds all      0 0 0 0 10  last weight 2*5-5-1=4 sum 40   40/(5*10)       G = 4/5 = (n - 1)/n
toy log                0 1 1 2 6   weights -4 -2 0 2 4   0-2+0+4+24 = 26  26/50   G = 13/25 = 0.52
toy log, active days   1 1 2 6     weights -3 -1 1 3     -3-1+2+18 = 16   16/40   G = 2/5 = 0.40
identity               G_all = 1 - (m/n)(1 - G_active) = 1 - (4/5)(3/5) = 13/25   (m active days of n)
```

`analyze.py` asserts these values, the two limits again for n = 2, 5 and 119, and that the formula agrees exactly with
two other definitions (one minus twice the area under the Lorenz polygon; the mean absolute difference between two
days divided by twice the mean) on every list it measures in full.

The capacity rule (handle at most `capacity` events a day, oldest first, after the day's arrivals; the rest waits;
unused capacity is lost) is checked on this case, with a capacity of 2 and a tolerance of 1 day:

```text
day        0  1  2  3  4
arrivals   1  7  0  0  2
handled    1  2  2  2  2     waits 0 | 0 0 | 1 1 | 2 2 | 3 0
backlog    0  5  3  1  1     the event left on day 4 arrived that day: undetermined, not late
handled 9, on the arrival day 4, late (wait > 1 day) 3, left 1, longest wait 3 days, largest backlog 5
```

## Self-checks and negative controls

`analyze.py` aborts instead of writing a result when one of its 41 checks fails; `results.json` lists them under
`checks`. They include a recount of every count made by `extract.py` through a second code path, the accounting
identities (quiet days plus the other days hold all events; months partition the log; type subsets partition the
events; handled plus left equals arrivals for every simulated plan; a reading date splits the log into days read and
days left), the hand-computed cases above, the median of an odd and of an even number of values, a known answer for
the generator (the mean number of empty days over the 2,000 logs against the exact expectation
`119 * (118/119) ** 594 = 0.7917`), agreement of a second batch drawn with another seed, "more capacity never
makes more events late" over every capacity from 1 to 109, and that each pair of busiest days lies inside one of
PSY-008's episodes (days of at least 12 events at most 7 days apart: 21 to 27 March and 21 June to 2 July, 86 days
apart), the two pairs inside different ones.

Results that could pass on nothing have a control:

- "0 of 2,000 synthetic logs are as concentrated as the observed one": the observed log is added to the batch and
  every comparison must then count exactly 1.
- "moving the day boundary changes the shares": a boundary moved by 0 hours must reproduce the UTC counts, and one
  moved by 24 hours must shift the dates and change no count.
- "no late event with a capacity of 34": one unit less must leave a late event (it leaves 4), and a capacity of 0
  must handle nothing. The same holds for the smallest sufficient capacity of the days left after each reading date.
- "the 95th percentile never leaves a late event in the synthetic logs": the number of logs with a late event is
  counted for the mean plan too, where it must be more than half of the logs (it is 1,919 of 2,000).

## Limits

- One log of 119 days from one repository. Its four busiest days are two pairs of neighbouring days, so the top-four
  share rests on two episodes.
- The snapshot holds the files archived at the pin. The Git history lists 12 trigger files deleted earlier without
  being archived (the lesson names the commits); they are not in the snapshot and no number here counts them.
- Every plan of `capacity.plans` is sized with hindsight. The four earlier readings are one log read on four dates,
  with an empty queue assumed at each restart: an illustration, not a test of a sizing rule.
- A trigger file records that the producing workflow fired, not that work was needed. The design's own deduplication
  rule would have merged the 594 files into far fewer triggers (`robustness.deduplicated_once_a_day`).
- The capacity rule is assumed. The repository states that the consumer was never scheduled, so no waiting time,
  backlog or handled count in `capacity` was measured. The 72-hour limit is read at one-day resolution.
- The synthetic control fixes the total and the number of days; it is the benchmark of "no concentration beyond
  chance", not a model of the project. Fitting a distribution to the counts is left to other modules.
- `largest_backlog_day_index_from_0` counts days from the first day of the list, starting at 0.
