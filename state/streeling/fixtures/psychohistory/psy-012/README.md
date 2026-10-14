# PSY-012 fixture: early-warning indicators and their false alarms

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-012-early-warning-false-alarms.md`.
Python 3, standard library only. Verified with CPython 3.14.2 on Windows and CPython 3.14.4 on Linux (WSL);
older Python versions were not run.

## Files

| File | Kind | What it is |
|---|---|---|
| `scenarios.json` | synthetic | Every assumption of the simulation: the fold model, the stationary controls, series lengths, window fractions, number of runs, alarm rules, all seeds, the hand cases, and the inputs of the learner's transfer task. |
| `analyze.py` | script | Runs the self-checks, the simulation and the transfer answers from `scenarios.json`, counts the variation in `observed-input.json`, and writes `results.json`. |
| `extract.py` | script | Reads `state/quality-trend/*.jsonl` of the pinned Demerzel commit and writes `observed-input.json`. |
| `observed-input.json` | observed | Source commit, source paths with their Git blob ids, row/run/day/artifact counts, and for each of the 18 artifacts its `citation_count`, `violation_count` and `compliance_rate` series as run-length segments, with the timestamps of its measured runs. |
| `results.json` | computed | Output of `analyze.py`. Floats are rounded to 4 decimals (`float_decimals`). The sections `self_checks`, `theory`, `simulation`, `tipping_positive_control` and `transfer_task` are synthetic; `observed_quality_trend` is computed from the observed extract. |

## Regenerate

From the repository root:

```sh
python -I state/streeling/fixtures/psychohistory/psy-012/extract.py
python -I state/streeling/fixtures/psychohistory/psy-012/analyze.py
```

The first command rewrites `observed-input.json`, the second `results.json`. To compare a second run byte for byte:

```sh
python -I state/streeling/fixtures/psychohistory/psy-012/analyze.py --output /tmp/psy-012-second.json
cmp state/streeling/fixtures/psychohistory/psy-012/results.json /tmp/psy-012-second.json
```

`analyze.py` takes `--input` (the extract), `--scenarios` and `--output`; each defaults to the file next to the
script. With `--check` it recomputes and exits 1 if the saved results differ, without writing. `extract.py` takes
`--repo-root` (root of the checkout) and `--output`. Both write LF line ends on
every platform. `analyze.py` took about 20 seconds on the author's machine (13.5 seconds under WSL);
`extract.py` takes under a second.

`extract.py` exits with status 1 and a message if the folder is missing, if the set of `.jsonl` files differs from the
pinned commit, if a file's Git blob id differs from the one recorded for commit
`4b03838800dcd4894f1e026461979bff1d985ca8` (the quality trend grows every night), or if a row has an unexpected
shape. The blob id is computed on the content with CRLF normalised to LF, so a Windows checkout with
`core.autocrlf=true` verifies too. Compare with `git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/quality-trend/`.

## What is observed and what is synthetic

- **Observed**: only `observed-input.json`, read from the repository at the pinned commit. `analyze.py` reads
  that file and never the repository, so its results do not move when the nightly data grows.
- **Computed from observed data**: `results.json` → `observed_quality_trend`. It counts how many series are constant,
  how many consecutive pairs change, at which runs, and how many rolling windows hold a single value. No variance,
  autocorrelation or trend statistic is computed on project data (`indicators_computed` is `false`).
- **Synthetic**: everything else. The fold model, the AR(1) controls and all rates come from assumed inputs and
  seeded pseudo-random numbers (`random.Random(seed)`, one generator per batch, seeds in `scenarios.json`). They
  are not measurements of the GuitarAlchemist ecosystem and not forecasts.

## Checks built into the script

`analyze.py` stops with an `AssertionError` if any of these fails:

- Kendall's tau: a hand case (13 concordant, 2 discordant, tau = 11/15), the limits +1 and -1, a tie case, and the
  fast method against the pairwise definition on 20 random sequences with ties.
- One four-point window computed by hand (residuals -0.3, -0.1, 1.1, -0.7; variance 0.9; autocorrelation -0.85/1.8).
- Running sums against a direct computation on 540 windows, with and without detrending.
- Detrending removes an added straight line exactly; negative control: without detrending the same line inflates
  the variance at least 146-fold.
- Known answers: on 200,000 points of AR(1) the variance is within 5% of `1 / (1 - phi^2)` and the lag-1
  autocorrelation within 0.02 of `phi`, for phi = 0.5, 0.7, 0.9; negative control: the wrong formula
  `1 / (1 - phi)` is rejected by the same tolerance. The fold simulator held at q = 25 matches its linearisation.
- Accounting: tipped + analysed = runs; alarm counts fall as the threshold rises; a joint alarm count never exceeds
  either single-indicator count; the four joint probabilities of the predictive-value table sum to 1.
- Calibration: the threshold lets through at most the allowed number of calibration runs, and on independent runs of
  the same model the calibrated rule fires within three standard errors of its 5% target.
- Positive control for the tipping detector: the main batches hold no tipped run, so a batch with four times the
  noise is run to show the detector finds some (41 of 200).
- Count of constant windows on an invented five-point series.

Nine deliberate one-line breakages of the script (wrong lagged term, wrong tie handling, wrong noise scale, wrong
divisor, halved fold step, off-by-one window test, disabled tipping test, max instead of min, shifted alarm
comparison) were each run on a scratch copy of the final script, with 400 runs per batch at 100 points; every one
stopped on an assertion. Two further breakages passed because they do not change the result: starting the
calibration search six places lower (the search loop walks back up), and testing for tipping at 1e9 instead of at
the unstable point (a tipped run blows up past both).

## Limits

- One approach scenario: the local AR(1) coefficient goes from 0.5 to 0.9 and the record stops 8.72 fluctuation
  standard deviations short of the unstable point. A closer or more distant end changes every detection rate.
- The resting level moves in a straight line by design (q linear in time), the friendly case for the straight-line
  detrending used here. A parameter moved linearly in q squared bends the level; that case was not simulated.
- Controls are stationary AR(1) series only. Changing noise levels, seasonality, measurement changes and selection
  of cases after the fact are not simulated; each can raise the indicators without any transition.
- 1,000 runs per batch: a rate has a standard error of at most 1.58 percentage points. The calibrated threshold is
  itself estimated from 1,000 runs.
- The alarm statistic (the smaller of two Kendall taus) and the within-window detrending are this fixture's
  simplifications. They are not the procedure of any cited paper.
- Byte-identical output was checked on two runs on Windows and one on Linux with CPython 3.14. Gaussian draws use
  `random.Random.normalvariate`, whose values are plain arithmetic on the generator's uniforms; other Python
  versions and platforms were not tested.
