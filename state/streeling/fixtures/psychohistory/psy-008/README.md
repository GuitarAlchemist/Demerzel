# PSY-008 fixture: daily counts of the archived trigger log against a Poisson benchmark

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-008/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-008-bursts-are-not-rates.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the 594 files of `state/triggers/archived/`, the pattern record `state/patterns/anti-pattern-003-push-triggered-spam.pattern.json` and two workflow files, checks their shape and their Git ids, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: one string per event (`<UTC timestamp> <type>`), the counts made by `extract.py`, the fields of the pattern record, and what the two workflow files say (retirement date and trigger types of the producer; cron lines of the scheduled workflow). |
| `scenarios.json` | assumed | Analysis choices (the claim under test, the bands, the window lengths, the day-boundary offsets, the quantile rule), the seed of the control log, the hypothetical log of the learner transfer task, and one borrowed count, `deleted_triggers` (below). Nothing in it is measured by this fixture. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts the days, runs the self-checks and writes `results.json`. `analyze()` calls one function per section of that file, in the file's order. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-008/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-008/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-008/analyze.py --check
```

Add `-B` to keep Python from writing a `__pycache__` folder. Each command finishes within a few seconds. Both
scripts write the same bytes on every run (LF line endings, `indent=2`, insertion-ordered keys). `--check` recomputes
the results and compares them with the saved file, ignoring only CRLF against LF.

Rounding: ratios, probabilities, means, variances and indices to 6 decimals; percentages and expected numbers of days
to 2 decimals; a probability too small for 6 decimals is stored as a mantissa with 2 decimals and a power of ten.
Counts, means and variances are exact fractions (`exact` holds the unrounded value). The Poisson probabilities are
summed in integer arithmetic over 300 terms (the terms left out weigh less than 1e-200), so no `exp`, `log` or `pow`
of the C library reaches a stored digit; the only floating-point function is `sqrt`. The one random draw is the
control log, from `random.Random(20261013).random()`.

**Every variance is the sample variance, with divisor n − 1.**

## How the trigger folder is pinned

The folder holds 594 files, so `extract.py` embeds one digest instead of 594 blob ids:

- the file count, 594;
- the manifest digest `3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393`: the SHA-256 of the
  lines `<blob id> <path>`, sorted by path, one per file. Reproduce it with
  `git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum`;
- the folder's Git tree id `2da37c16496d39c0c9137897c8be2b0c6d6b7978`, recomputed from the blob ids and visible in
  `git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/triggers/`.

The three other source files are pinned by their blob ids. `extract.py` stops with exit code 1 when a file is missing,
when a trigger file lacks one of its six keys, when its file name disagrees with its JSON `timestamp` or `type`, or
when any id differs from the pin. `--allow-drift` snapshots a changed folder anyway and records `"commit": null`; the
lesson's numbers then no longer apply. Tried once by hand on a copy outside the repository: one changed byte, one
removed file and one edited pattern record each stopped the script.

## Observed, computed, synthetic

- **Observed:** the 594 timestamps and types, the pattern record, and the lines read from the two workflow files.
  Only `state/triggers/archived/` is analysed; the few trigger files of `state/triggers/` outside the archive are
  left out.
- **Computed from the observed data:** `observed`, `daily_counts`, `composition`, `windows`, `day_boundary`,
  `uncertainty_of_the_mean`, `planning` and `lesson_exercises` in `results.json`.
- **A benchmark, not data:** `poisson_benchmark` is the Poisson distribution with the observed mean. It is the
  reference for "independent events at a constant rate"; it is not fitted against alternatives.
- **Synthetic:** `negative_controls` (three logs built from assumed rules) and `transfer_task` (a hypothetical log).
- **Sensitivity to a borrowed count:** `deleted_triggers`. PSY-009 reads the repository history and reports twelve
  trigger files deleted without being archived, seven dated 2026-03-20 and five dated 2026-06-30
  (`git log --diff-filter=D --name-only 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/` lists them). This
  fixture does not read the history: the two counts are an input in `scenarios.json`. Added to the daily counts,
  they give 606 events, a mean of 5.092437 and an index of dispersion of 39.400375 (39.770216 without them);
  2026-03-20 becomes a twelfth burst day, the episodes stay two and the four busiest days are unchanged.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 35 checks fails; `results.json` lists them under
`checks`. They include a recount of the counts made by `extract.py` through a second code path, the accounting
identities (active days + empty days = calendar days; per-type counts = daily counts; the bands, the weekday classes,
the windows and the burst episodes each add up to the totals), the identity "ratio of standard errors squared = index
of dispersion", the Poisson series against its own parameter, and two cases worked by hand:

```text
counts 0 1 1 2 6     n = 5, sum 10, sum of squares 42
mean 10/5 = 2        sample variance (42 - 100/5) / 4 = 5.5        index 5.5 / 2 = 2.75
median (3rd smallest) 1        80% quantile (4th smallest) 2

Poisson, mean 2      P(0) = e^-2 = 0.135335      P(X <= 2) = 5 e^-2 = 0.676676
                     P(X >= 6) = 1 - (109/15) e^-2 = 0.016564      99% quantile 6
```

"The index of dispersion is far above 1" could come from code that always returns a large value. The controls
answer that: the same functions return 0.001684 for the 594 events spread evenly over the 119 days, 1.234264 for a
seeded log that places each event on a uniformly drawn day (accepted band 1 ± 4 standard deviations, 0.479244 to
1.520756), and 14.413105 once 100 events are added to one day of the even log.

## Limits

- One repository, one producer workflow, 119 days. The bursts sit in two episodes, so nothing here estimates how
  often bursts occur.
- The archive is what survived: 594 is every event still archived, not every run of the producer. Twelve deleted
  files are known (`deleted_triggers`); whether overlapping runs lost others was not checked.
- A timestamp is the moment the producer workflow wrote the file, not the moment of the push, issue or discussion.
- The standard deviation of the index under a Poisson process, `sqrt(2 / (n - 1))`, is the chi-square approximation;
  it sets a scale and is not an exact test.
- Blocks of 7 and 17 days start at the first day of the log; they are not calendar weeks.
- The cron lines are read from `streeling-daily.yml` as it is at the pin. Nothing in a trigger file says which
  discussion or which workflow caused it.
- No count distribution is fitted or compared (PSY-022), and no concentration measure is computed (PSY-009).
