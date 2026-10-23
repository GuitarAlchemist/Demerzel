# PSY-007 fixture: is it a power law? Eighteen citation counts

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-007/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-007-power-law-or-not.md`.
Python 3.9 or later, standard library only. Every random draw comes from `random.Random(seed).random()` with the seeds
stored in `scenarios.json`.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the five `state/quality-trend/*.jsonl` files, the 18 `state/evolution/*.evolution.json` records, the department record, the two published lessons (PSY-001, PSY-002) and `logic/fractal-compounding.md`, the specification PSY-001 gives as its first source; checks their shape and their Git blob ids; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: for each of the 18 artifacts of the latest run (2026-10-13T18:43:54Z) its `citation_count`, its `citation_source`, its citation paths and its count in the last run before git grep was used; the citation path shared by two artifacts, with the one that lists it and the one counted on its own name; the specification's power-law detection rule (line 56), the lines that name its data and the line of PSY-001 that cites it; the three strings of the department record that mention a power law, with their line numbers; the count of such lines in PSY-001 and PSY-002 (0 and 0). |
| `scenarios.json` | assumed | Rounding, the three family definitions, the cut rules, the 0.1 threshold, seeds, replicate counts, generator parameters, and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, runs the self-checks and writes `results.json`. |
| `results.json` | computed and synthetic | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-007/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-007/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-007/analyze.py --check
```

Each script finishes in a few seconds. Add `-B` to keep Python from writing a `__pycache__`
folder. `analyze.py` writes the same bytes on every run: LF line endings, `indent=2`, insertion-ordered keys, exponents
rounded to 3 decimals, log-likelihoods to 2, slopes, R squared and distances to 3, probabilities and p-values to 4,
percentages to 1. Float sums use `math.fsum`, which is correctly rounded on every Python version. The saved file was
reproduced byte for byte under Python 3.9, 3.12 and 3.14 on Windows and under Python 3.14 on Linux. `--check`
recomputes the results and compares them with the saved file, ignoring only CRLF against LF.

Artifact names and citation paths are written with a space on each side of every slash
(`policies / alignment-policy.yaml`): the repository's producer, `scripts/evolution_metrics.py`, counts every tracked
file that contains an artifact's path as a literal string, and a data file that listed the paths unspaced would raise
the very counts this module studies.

`extract.py` stops with exit code 1 when a source file is missing or malformed, when the latest run and the evolution
records disagree on an artifact or a count, or when a source file is not the blob of the pinned commit (the nightly
feeder appends rows, so this happens on any later checkout). `--allow-drift` snapshots newer data anyway and records
`"commit": null`; the lesson's numbers then no longer apply.

## What is computed

Three families, all as distributions on the integers `x >= x_min`, so that their likelihoods are comparable:

- **power law** (discrete, the zeta distribution): `p(x) = x^-alpha / zeta(alpha, x_min)`. The exponent solves
  "model mean of ln x = sample mean of ln x", found by false position; the Hurwitz zeta function is a 16-term sum
  plus an Euler-Maclaurin tail. The continuous closed form `1 + n / sum ln(x / x_min)` and the half-shift
  approximation `1 + n / sum ln(x / (x_min - 1/2))` are stored next to it.
- **exponential** (discrete, the geometric distribution): `p(x) = (1 - q) q^(x - x_min)`, with `q = m / (m + 1)` and
  `m` the mean excess over `x_min`.
- **lognormal**, rounded up to the next integer: `p(x) = Phi((ln x - mu) / sigma) - Phi((ln(x - 1) - mu) / sigma)`,
  fitted for `x_min = 1` only by Newton steps in `(mu / sigma, 1 / sigma)`, where the log-likelihood is concave. The
  other common discretisation (round to nearest, conditioned on `x >= 1`) is fitted to the recorded counts as a check:
  its log-likelihood is 0.62 higher and the ranking of the families does not change.

Sections of `results.json`:

- **Observed:** `observed` (the rank-size table, zeros, ties, the two counts not measured by git grep, the shared
  citation path, the department's strings, the specification's detection rule).
- **Computed from the observed counts:** `share_rule` (the specification's rule, top 20% of artifacts holding more
  than 60% of citations, on the recorded and on the hand-typed counts), `rank_plot`, `power_law_fit` (one row per
  cut), `families_on_all_positive_counts`, `bootstrap` (2,000 resamples of the 18 counts), `sensitivity` (the 16
  measured counts alone; the hand-typed counts of the same artifacts on 2026-09-13).
- **Synthetic:** `simulation_all_positive` (2,000 samples of 16 values from each fitted family), `simulation_tail`
  (2,000 tails of 12, 50 and 200 values above 13 from a power law and from an exponential), `goodness_of_fit` (the
  observed Kolmogorov-Smirnov distance against the synthetic power-law samples), the same test on the hand-typed
  counts (`sensitivity.before_git_grep.goodness_of_fit`), `sampler_checks`, `transfer_task` (a hypothetical
  registry, closed forms a learner can compute by hand, and the discrete fits, which reverse the sign of the
  comparison at `x_min = 1`).

A simulated share out of 2,000 has a standard error of at most 1.2 percentage points.

## Self-checks and controls

`analyze.py` aborts instead of writing a result when one of its checks fails; `results.json` lists them under
`checks`. They include four known values of the zeta function, its derivative against a central difference, the
probabilities of each family summing to 1, five cases worked by hand (the continuous exponent of 2, 4, 8 above 2 is
`1 + 1 / ln 2`; the exponential fit of 1, 2, 3 has `q = 1/2`; counts `720 / rank` give slope -1 and R squared 1;
differences 1, 2, 3 give `R = 6` and `p = erfc(3)`; the share rule passes 2 of 10 artifacts holding 61 of 100
citations and fails them at 60), the Kolmogorov-Smirnov distance against a scan of every integer, the lognormal's gradient and Hessian against central differences, the Newton fit against a nested
golden-section search, each sampler against its probability formula, and the share of synthetic samples whose
largest value stays within 65 against its closed form.

Results that could pass on nothing are listed under `negative_controls` with a case where the same procedure returns
something: no exponential or lognormal sample has the power law on top (it is on top in 932 of 2,000 power-law
samples); no power-law sample is as far from its fit as the recorded counts (501 of 2,000 are on the tail); no line of
PSY-001 or PSY-002 mentions a power law (3 strings of the department record do). At 200 tail values the comparison
finds the generator in all 2,000 samples of each family, so its failures at 12 values come from the sample size.

## Limits

- Eighteen counts, sixteen of them positive, two of them not measured by git grep, two that share one citation path:
  the fits treat them as independent draws from one distribution, which they are not. They are also a selection,
  the artifacts that have an evolution record, not a sample of the governed files.
- The goodness-of-fit p-value holds `x_min` fixed; the full procedure of Clauset, Shalizi and Newman re-estimates it in
  every synthetic sample.
- The p-value of a log-likelihood ratio (Vuong 1989) is a large-sample approximation; the synthetic tails show how it
  behaves at 12 values.
- A naive difference of two normal distribution functions underflows for the large values that power-law samples
  contain, which silently lowers the lognormal's likelihood; `analyze.py` uses the complementary error function in the
  tails and density times width for narrow intervals (checked against 60-digit arithmetic while writing the fixture,
  outside the repository).
- The tail verdict depends on the cut: the ratio test is decisive for the exponential at the cuts 5, 6, 15 and 17,
  undecided at 13; the rule that picks 13 was written after seeing the counts.
- Not fitted: a lognormal above a cut greater than 1, a power law with an exponential cut-off, a stretched exponential.
- The power-law sampler is Devroye's rejection method for the zeta distribution (Devroye 1986, *Non-Uniform Random
  Variate Generation*, Springer), extended here to `x_min > 1`.
