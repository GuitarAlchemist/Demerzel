# PSY-014 fixture: prediction horizons in the logistic map

The program, `analyze.py`, lives in `scripts/streeling_fixtures/psychohistory/psy-014/` because this repository keeps executable code under `scripts/`; the data files it reads and writes are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-014-prediction-horizons.md`.
Python 3.9 or later, standard library only. Everything here is synthetic: no file of the repository is read, so
there is no `extract.py` and no `observed-input.json`.

## Files

| File | Kind | What it is |
|---|---|---|
| `scenarios.json` | assumed and cited | Every assumption: the four settings of the map (r = 2.9, 3.2, 3.7, 4), the seed and count of the starting points, the initial errors and tolerances, the thresholds of the research cycle's hypothesis, the settings of the high-precision comparison, the inputs of the lesson's exercises and of the learner transfer task, and four exponents quoted from MAT-024 at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`. |
| `analyze.py` | script | Reads only `scenarios.json`, iterates the map, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py --check
```

One run takes about five seconds. `--check` recomputes the results and compares them with the saved file, ignoring
only CRLF against LF. `--scenarios` and `--output` name other files.

## Why the output is the same bytes everywhere

A chaotic orbit doubles a rounding difference at every step, so two platforms that disagree in the last bit of one
operation disagree completely fifty steps later. The script therefore avoids every operation whose last bit is not
fixed by the IEEE 754 standard:

- The map and the gaps use only `+`, `-`, `*`, `/` and `abs` on doubles, one operation per Python expression node
  and in a fixed order (the interpreter never fuses a multiplication with an addition).
- Logarithms and exponentials are the short series `ln` and `exp` written in the script, built from those four
  operations and from `math.frexp`, `math.ldexp` and `math.floor`, which are exact. `math.log` and `math.exp`
  appear only in a self-check that compares them with the series within 1e-13; no value from the C math library
  is stored. The one square root (the standard error of an exponent estimate) is `math.sqrt`, which the standard
  requires to be correctly rounded.
- The high-precision runs use Python integers only (see below); integer arithmetic is exact, and an integer is
  turned into a float by one correctly rounded division.
- Step counts are integers. A mean of step counts is rounded half up to 2 decimals from the integer total, which
  is stored next to it (`total`).
- Stored floats are rounded: exponents to 6 decimals, step counts and digits to 2, shares and ratios to 4, states
  to 6, gaps and required errors to 3 significant digits. Differences shown in the lesson (`mean_minus_formula`,
  `steps_per_digit`) are computed from the rounded figures, so they can be checked by hand. Two kinds of float are
  stored unrounded on purpose: the few distinct settled starting values of the stable regimes (`settled_values`),
  because the point is that they differ in the sixteenth decimal, and the second start 0.3 + 1e-12.
- Starting points come from `random.Random(20261013).random()`; no global random state, clock or machine property
  is used.
- A guard at the start compares the bits of a 50-step orbit, a logarithm and an exponential with constants in the
  script, and stops with an error on a platform where they differ.

Checked: the same bytes (SHA-256 of `results.json` identical) on CPython 3.9.25, 3.12.12 and 3.14.2 under Windows
x86-64 and on CPython 3.14.4 under Linux x86-64. Not run on macOS or on an ARM processor.

## The high-precision comparison

Doubles carry about 16 decimal digits, and the map loses one binary digit per step at r = 4. Some printed numbers
therefore belong to the map and others to the arithmetic. To tell them apart, `analyze.py` repeats some runs with
1,024-bit numbers held in Python integers: a state x is the integer x × 2^1024, the double r is taken at its exact
value, and one step is `r * x * (1 - x)` with exact integer products followed by one truncation. Starts are the same
doubles as elsewhere, converted exactly.

How far such a run is from the exact orbit of its starting double: for states between 0 and 1 and r ≤ 4,
|f(a) − f(b)| = r |a − b| |1 − a − b| ≤ 4 |a − b|, and a truncation loses less than 2^-1024. After n steps the
error is therefore below (4^n − 1) / 3 × 2^-1024. No run is longer than 400 steps, where the bound is 1.24e-68
(`high_precision.error_bound`). A stored step count could differ from the exact one only if a gap lay within that
distance of the tolerance.

What the comparison shows (`high_precision`):

- Gap table at r = 3.2: the zeros printed from step 20 on are the resolution of doubles. The median gap is 1.1e-17
  at step 20 and 1.33e-33 at step 60, which is what 1e-9 × e^(exponent × steps) gives. Where doubles still resolve
  the gap (every step at r = 2.9, steps 0 and 10 at r = 3.2) the two arithmetics agree to 3 significant digits.
- Horizons in the chaotic regimes, tolerance 0.1, ten initial errors: 3 of 10,000 horizons differ at r = 3.7 and 1
  of 10,000 at r = 4, by at most 2 steps; no mean moves by more than 0.01 step and the steps per digit are the
  same (6.46 and 3.32). The horizons belong to the map.
- A double run is first 0.1 away from the high-precision run of its own start after 53.27 steps on average at
  r = 4 (42 to 64) and 99.55 at r = 3.7 (81 to 148).
- The two runs of `beyond_the_horizon` (0.3 and 0.3 + 1e-12, r = 4) are first 0.1 apart at step 37 in both
  arithmetics. At step 100 the doubles hold 0.673899 and 0.002785, the other form of the map in doubles
  (`r * x - r * x * x`) holds 0.053317 and 0.995549, and the high-precision runs hold 0.991939 and 0.735222. Only
  the last pair describes the map from those two starting doubles; the double runs left their own orbits at steps
  52 and 51.

## Observed, computed, synthetic

- **Observed:** nothing.
- **Cited:** the exponents that MAT-024, section 2, prints for r = 2.9, 3.2, 3.7 and 4
  (−0.105361, −0.916291, 0.350235, 0.693135), copied by hand into `scenarios.json`. MAT-024 uses a start of 0.1,
  1,000 discarded steps and 10,000 averaged steps, which is exactly the first of this fixture's 100 blocks; the
  script stops if a first block differs from the printed value at 6 decimals.
- **Synthetic:** everything else. `transfer_task` describes a hypothetical delivery simulator, not Streeling.

## Sections of `results.json`

- `regimes`: per r, the Lyapunov exponent estimated from 1,000,000 steps (100 blocks of 10,000), its known value
  where one exists, the exponent the other sections use, and how many distinct starting points remain after
  settling. In each stable regime 2 remain, listed under `settled_values` with the number of starts on each, the
  size of the map's slope there and how far one step moves them: at r = 3.2 they are the two points of the cycle
  (0.286 apart, slopes 0.0835 and 1.9165, product 0.16 = 0.4²); at r = 2.9 they are the fixed point held as two
  doubles 6 spacings (6.66e-16) apart, between which the rounded map alternates.
- `gap_table`: 1,000 pairs started 1e-9 apart; median and largest gap every 10 steps; an exponent estimated from
  two medians, and from the mean of ln(gap ratio) over the pairs.
- `contraction`: where the exponent is negative, steps until an error of 1e-3 has fallen below 1e-6.
- `horizon`: for initial errors from 1e-3 to 1e-12 and tolerances 0.01 and 0.1, the first step at which each pair
  differs by the tolerance (mean, median, min, max over 1,000 pairs) next to `ln(tolerance / error) / exponent`.
  For the stable regimes, the number of combinations of pair, error and tolerance (20,000) and of distinct ones (40).
- `hypothesis_test`: the thresholds written into the research cycle before the first run, and whether each holds.
- `double_precision`: two algebraically equal forms of the map run from the same start, and the initial error a
  100-step horizon would need.
- `beyond_the_horizon`: two runs 1e-12 apart at r = 4, their states at step 100 and the share of steps below 0.25.
- `high_precision`: the comparison described above.
- `worked_examples`: the figures of the lesson's five exercises. For exercise 5, `by_interval` gives two counts for
  each re-measuring interval k from 8 to 20: the pairs whose horizon is later than k (one interval), and the
  forecasts that stay within tolerance at every one of the 60 steps when the forecast run restarts from the true
  state, with a fresh error of 1e-6, every k steps (the unit of the exercise's 95% criterion).
- `negative_controls`, `transfer_task`, `checks`.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 41 checks fails; `results.json` lists them under
`checks`. They include three known answers for the exponent (ln 0.9 at r = 2.9 and ln 0.4 at r = 3.2 within 1e-9,
ln 2 at r = 4 within 1e-4), the known share 1/3 of steps below 0.25 at r = 4 (within 0.01), two accounting
identities, the identity "steps gained = digits gained × steps per digit", the product of the slope sizes at the
settled values against e^(n × exponent), and a case worked by hand. For the high-precision runs: the error bound
at the step limit, one step from 3/4 − 2^-10 at r = 4 landing exactly on 3/4 + 2^-9 − 2^-18, and agreement with
the doubles within 5% wherever the median gap in doubles is at least 100 spacings (a bound set before the first
run). For exercise 5: over a span of one interval, the re-measured forecasts must be the pairs that last the
interval.

**Hand-computed case.** At r = 4 the point 0.75 is a fixed point (4 × 0.75 × 0.25 = 0.75). Start the second run
at 0.75 − 2^-10 and write its distance from 0.75 as e. Then 4 (0.75 + e)(0.25 − e) = 0.75 − 2e − 4e², so
e_next = −2e − 4e²:

```text
step      0          1          2          3          4          5          6          7
|e|   0.000977   0.001949   0.003914   0.007766   0.015774   0.030553   0.064839   0.112862
```

The gap first reaches 0.01 at step 4 and 0.1 at step 7; the script must find 4 and 7, and stores the eight gaps.

**Negative controls.** "No pair reaches the tolerance" in the two stable regimes (0 of 20,000 combinations each,
40 of them distinct) could pass with a detector that never fires. Two controls: the same detector reaches the
tolerance for all 20,000 combinations in each chaotic regime, and in the two-cycle regime it fires at step 1 when
the second run is started on the other point of the cycle (a gap of 0.286 that is still there after 500 steps).

## Limits

- One map with one variable and no noise; one seed; 1,000 pairs. The spread of the horizons (`min`, `max`) is the
  spread over those pairs only.
- In the two stable regimes the 1,000 settled starting points are 2 distinct numbers, so the 1,000 pairs there
  repeat two experiments, and every count over those pairs is a count over two experiments.
- The exponent at r = 3.7 has no closed form: it is an estimate with a standard error of about 0.0003.
- Initial errors below about 1e-13 cannot be set accurately in double precision; the smallest one used, 1e-12, is
  realized within 0.003% (`largest_relative_deviation_of_a_realized_starting_gap`).
- After about 53 steps at r = 4 (about 100 at r = 3.7) a double run no longer follows the orbit of its own start.
  States printed for later steps, and the counts of steps below 0.25 over 100,000 steps, are properties of this
  computation, reproducible bit for bit; they are not values of the map from those starts. The horizons were
  recomputed in high precision; the exponents, the contraction counts and the shares were not.
- Exercise 5 models a new measurement as a restart of the forecast run from the true state with an error of the
  same size as the first, moved toward the middle of the interval. Other error models were not tried.
- Nothing here measures the project. No Lyapunov exponent has been estimated for any project quantity.
