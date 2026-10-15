# PSY-022 fixture: three count models, two criteria, one shared assumption

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-022/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-022-competing-explanations.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the 594 files of `state/triggers/archived/`, checks each file's keys against its name, checks the folder against the pinned commit, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the number of events on each of the 119 UTC calendar days from 2026-03-20 to 2026-07-16 (empty days included), plus the counts made by `extract.py`. |
| `scenarios.json` | assumed and cited | The three candidate models, the search settings, the bands, the seeds and sample sizes of the seeded checks, the sensitivity choices, one borrowed count (`deleted_triggers`), the two cited scales, the thresholds that make the research cycle's hypothesis checkable, and the hypothetical help desk of the learner transfer task. Nothing in it is measured by this fixture. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, fits the three models, runs the seeded checks and the self-checks, and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-022/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-022/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-022/analyze.py --check
```

`extract.py` takes under a second; `analyze.py` takes 7 to 15 seconds (5,000 samples in each of 13 seeded cells,
10,000 shuffles). `analyze.py` accepts `--input`, `--scenarios` and `--output`; their defaults are the files above.
`--check` recomputes everything and compares it with the saved `results.json`, ignoring only CRLF against LF.

The output is the same byte for byte on every run and every platform. It was compared under CPython 3.9.25,
3.12.12 and 3.14.2 on Windows and 3.14.4 on Linux. To get there, `analyze.py` uses no function of the C maths
library whose last bit may differ between platforms: the logarithm and the chi-square tail are series built from
`+ - * /`, square roots are `math.sqrt` (correctly rounded by IEEE 754), floats are added in a fixed order by an
explicit loop (the built-in `sum` changed its algorithm in Python 3.12), and every random draw is
`random.Random(seed).random()`, which CPython specifies. A fingerprint check stops the program if two logarithms or
one seeded draw differ from their expected bits. Numbers are stored rounded (log-likelihoods, AIC and BIC to 3
decimals, parameters to 6, shares to 4); a criterion is computed from the rounded log-likelihood and a difference from
the rounded criteria, so that a reader can redo each step by hand from the figures stored next to it.

## The pin

The folder holds 594 files, so `extract.py` embeds one digest instead of 594 blob ids:

- the file count, 594;
- the manifest digest `3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393`: the SHA-256 of the
  lines `<blob id> <path>`, sorted by path, one per file. Reproduce it with
  `git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum`;
- the folder's Git tree id `2da37c16496d39c0c9137897c8be2b0c6d6b7978`, recomputed from the blob ids and visible in
  `git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/triggers/`.

`extract.py` stops with exit code 1 when the folder is missing, when a file name does not have the form
`<timestamp>Z-<type>.trigger.json`, when a file lacks one of its six keys or its three `details` keys, when its JSON
`timestamp` or `type` disagrees with its name, or when the count, the digest or the tree id differs from the pin.
`--allow-drift` snapshots a changed folder anyway and records `"commit": null`; the lesson's numbers then no longer
apply. Tried once on a copy outside the repository: one added byte in one file, then one removed file, each stopped
the script; the unchanged copy passed.

The counts agree with PSY-008, which extracts the same folder: 594 events, 100 active days, 19 empty days, a busiest
day of 109 events.

## Observed, computed, synthetic, cited

- **Observed:** the 119 daily counts in `observed-input.json`. Only `state/triggers/archived/` is read.
- **Computed from the observed data:** `observed`, `fits`, `optimiser`, `adequacy`, `sensitivity.rows`,
  `dependence.observed_days`, `hypothesis_test` and `worked_examples` (exercises 1, 2, 4 and 5).
- **Synthetic:** `recovery` (samples of independent days drawn from each fitted model), `dependence.sticky_geometric`
  (an assumed process whose days repeat the previous count with probability 0.46), `dependence.controls`,
  `negative_controls`, the shares of `worked_examples.exercise_3` (an imaginary two-week log) and `transfer_task` (a
  hypothetical help desk).
- **Borrowed:** `sensitivity.with_deleted_triggers_added_back`. Twelve trigger files were deleted without being
  archived, seven dated 2026-03-20 and five dated 2026-06-30 (PSY-009 reads them from the history;
  `git log --diff-filter=D --name-only 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/` lists them).
  This fixture does not read the history: the two counts are an input in `scenarios.json`. Added back, they leave the
  ranking unchanged (geometric minus negative binomial: 44.566 AIC points, 41.787 BIC points, against 43.21 and
  40.431 without them).
- **Cited:** `cited_scales`, two rules of thumb quoted from Burnham and Anderson (2004, p. 271) and Kass and Raftery
  (1995, p. 777), with what each source says about its own scale. Neither is a probability that a model is true.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 37 checks fails; `results.json` lists them under
`checks` with the number of times each was evaluated. They include:

- the arithmetic: the series logarithm against `math.log` on 4,000 points (within 1e-13) and the series chi-square
  tail against `math.erfc` (within 1e-12); these comparisons use the C library only to check, never to compute;
- a recount of the counts made by `extract.py`, and the accounting identities (the frequency table, the bands and the
  picks of each criterion each add up to their totals; each fitted distribution sums to 1 and has the sample mean);
- the optimiser against known answers: a golden-section search on the log-likelihood returns the closed-form Poisson
  lambda and geometric q from three starting intervals each (within 1e-6); the negative binomial r found by bisecting
  the score (relative tolerance 1e-10) is the same from three brackets and agrees with a golden-section search on
  the log-likelihood itself from three other intervals; at that r the log-likelihood peaks at mu = mean; the score
  changes sign exactly once on a grid of 213 points from 1e-4 to 1e4;
- the limits: at r = 1 the negative binomial log-likelihood equals the geometric one (within 1e-9), and at r = 1e6 it
  exceeds the Poisson one by n (variance - mean) / (2 r) within 0.1%; a sample whose variance does not exceed its mean
  is fitted at the Poisson limit;
- a case worked by hand:

```text
counts 0, 1, 3        n = 3, sum = 4, mean = 4/3
Poisson               4 ln(4/3) - 4 - ln(3!)        = 1.150728 - 4 - 1.791759      = -4.641031
geometric, q = 4/7    3 ln(3/7) + 4 ln(4/7)          = -2.541894 - 2.238463         = -4.780357
neg. binomial, r = 2  P(0) = 0.6^2 = 0.36, P(1) = 2 x 0.36 x 0.4 = 0.288, P(3) = 4 x 0.36 x 0.4^3 = 0.09216
                      ln(0.36 x 0.288 x 0.09216)                                    = -4.650675
```

- the order: the three log-likelihoods of the shuffled days equal those of the days in calendar order;
- the hypothesis: the large-sample shares that AIC and BIC pick the over-large model when the geometric is true
  (0.1573 and 0.0288, from the chi-square tail with 1 degree of freedom) are compared with the seeded shares, and the
  comparison is reported, not enforced.

## Negative controls

Two results could pass on nothing. "No tie between the criteria" could come from code that never reports a tie: ten
empty days give three log-likelihoods of 0 and a reported tie between the two one-parameter models. "The observed
lag-1 autocorrelation is reached by 3 of 10,000 shuffles" could come from a test that always returns a small count:
the same test returns 3,352 of 10,000 for one shuffled order treated as if observed, and 0 for the days sorted by
count.

## Limits

- One repository, one producer workflow, 119 days. The decisive gap between the negative binomial and the geometric
  rests on four days in two pairs of neighbouring days (`sensitivity.rows`).
- The archive is what survived; twelve deleted files are known (`deleted_triggers`), whether others were lost was not
  checked.
- The three candidates treat the days as independent and identically distributed. The data are not
  (`dependence.observed_days`), and no model of the dependence was fitted.
- No small-sample correction of AIC (AICc) and no out-of-sample comparison was made.
- The seeded shares carry Monte Carlo error: a share near 0.16 measured on 5,000 samples has a standard error near
  0.005. The sample size was raised from 2,000 to 5,000 for that reason, before the lesson was written.
