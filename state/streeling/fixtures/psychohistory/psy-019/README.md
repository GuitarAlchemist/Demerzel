# PSY-019 fixture: the average of forecasters who share a source

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-019/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-019-combining-correlated-forecasters.md`.
Python 3.9 or later, standard library only. Random numbers come from `random.Random(seed)` with the five seeds
stored in `scenarios.json`.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads four files and the council's five records as text, checks their shape and their Git blob ids, and writes `observed-input.json`: the multi-model orchestration policy (its `confidence_calibration` block and its `cross-validation` rule), the tribunal-panel script (the panel, what every persona is sent, the three verdicts and the score a persona may return, and every line that reads a score), the workflow that runs the panel (its `--model` argument) and the council script (its two reviewers, six phrases of its docstring kept with their whole lines, and the line that computes the council's confidence) and the council's records in `state/council` (each record's id, reviewers' scores, verdict and confidence, and the names of all its keys). |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`. It describes a setup. None of the four files holds a persona's answer or an outcome; the council's five records hold nine reviewer scores (reviewer_a 0.75 in all five, reviewer_b 0.3, 0.3, 0.3 and 0.85 in the last four) and no key naming an outcome. Nothing in it measures a correlation between agents. |
| `scenarios.json` | assumed | The error model, the grid (k = 1 to 14; rho = 0, 0.3, 0.6, 0.9), the sizes and seeds of the simulations, the thresholds of the research cycle's hypothesis, the invented split of the shared variance between context and model, the reading applied to the policy's settings, the yes/no question of `yes_no_outcome`, the inputs of the lesson's exercises and of the learner transfer task. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, computes the closed forms in exact fractions, runs the simulations and the self-checks, and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

In the JSON files the policy's path is written `policies / multi-model-orchestration-policy.yaml`, with a space on
each side of the slash: the repository's citation metric counts every tracked file that contains a governance
artifact's path as a literal string, and a data file must not move the metric that sibling modules study.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-019/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-019/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-019/analyze.py --check
```

`extract.py` takes under a second and `analyze.py` a few seconds. `extract.py` stops with exit code 1 when a source
file is missing, when a line it expects cannot be read, or when a file is not the blob of the pinned commit;
`--allow-drift` snapshots the newer files anyway and records `"commit": null`, which `analyze.py` refuses.
`--check` recomputes the results and compares them with the saved file, ignoring only CRLF against LF.

## Why the output is the same bytes everywhere

- Closed forms are `fractions.Fraction` values, rounded once, half to even, to 6 decimals (percentages to 2).
- The simulations use `+`, `-`, `*` and `/` on doubles and `math.sqrt`, which IEEE 754 requires to be correctly
  rounded. Totals are explicit running sums in a fixed order; `sum()` is never applied to floats, because its
  algorithm changed in Python 3.12. No logarithm, exponential or `gauss` is used.
- A draw is `(random.Random(seed).random() - 0.5) * sqrt(12)`: uniform between −√3 and √3, mean 0, variance 1.
- Simulated values, standard errors and square roots are stored with 4 decimals (6 in `last_forecaster`, whose
  differences are small), distances in standard errors with 2, computed before rounding.
- A guard at the start compares the literal used for √12 with `math.sqrt(12.0)` and the bits of one seeded draw
  with a constant, and stops on a platform where they differ.

Checked by the author: `observed-input.json` and `results.json` come out as the same bytes on CPython 3.9.25,
3.12.12 and 3.14.2 under Windows x86-64 and on CPython 3.14.4 under Linux x86-64 (WSL). macOS was not tried.

## Observed, computed, synthetic

- **Observed:** `observed-input.json`, and `observed_setup` in `results.json` (the counts are made again from the
  rows and compared).
- **Computed from one observed number under a stated reading:** `agreement_of_two` takes 0.8, 0.9 and 0.5 from the
  policy and reads them as probabilities of being right on a yes/no question. The policy does not say that they
  are; the reading is this module's.
- **Computed from assumed inputs, exactly:** `closed_form`, `exact_enumeration`, `newcomer`, `worked_examples`,
  `transfer_task`.
- **Synthetic (seeded simulation):** `simulation`, `last_forecaster`, `direct_check`, `spread`, `shared_bias`,
  `newcomer_simulation`, `scored_log`, `yes_no_outcome`. `scored_log` and `yes_no_outcome` take their number of
  agents, 5, from the panel in the snapshot; nothing else in these sections is observed.

## The model

```text
error_i = bias + sigma * ( sqrt(rho) * C + sqrt(1 - rho) * I_i )
```

`C` is drawn once per occasion and shared by every forecaster; `I_i` is drawn per occasion and per forecaster; both
have mean 0 and variance 1. Each error then has variance `sigma^2`, two errors have correlation `rho`, and the
average of k errors has the mean squared error `bias^2 + sigma^2 (rho + (1 - rho) / k)`.

## Sections of `results.json`

- `closed_form`: for each rho and each k from 1 to 14, the mean squared error of the average, its square root, the
  number of independent forecasters the group is worth, `k / (1 + (k - 1) rho)`, and what one more forecaster removes.
- `exact_enumeration`: errors of +1 or −1 instead of draws. Every sign pattern is listed (32,768 for k = 14) and the
  three averages that the derivation uses come out exactly: 1, 0 and 1/k.
- `simulation`: 200,000 seeded occasions; each of the 56 cells against its closed form, in units of the
  simulation's own standard error, and the control described below.
- `last_forecaster`: what the fourteenth forecaster removes, measured in pairs on the same occasions.
- `direct_check`: the first 1,000 occasions again, each error built on its own and the errors averaged one by one.
- `spread`: how far the forecasts are from their own average, next to how far that average is from the outcome
  (the best forecast possible, in the lesson's words).
- `shared_bias`: every forecaster off by the same 0.5; 100,000 occasions; k = 1, 5, 14.
- `newcomer` and `newcomer_simulation`: thirteen forecasters at rho = 0.6 and a fourteenth of four kinds, with
  equal weights and with the weights that minimise the variance; one independent newcomer at every rho of the grid.
- `agreement_of_two`: two yes/no judges, each right with probability 0.8, for several correlations.
- `scored_log`: 1,000 simulated logs of 20 and of 100 occasions for 5 agents, and the range of the estimate of
  rho that each length gives, for errors that leave out the part of the outcome nobody could foresee. The lesson
  no longer quotes it; `yes_no_outcome` shows why.
- `yes_no_outcome`: a yes/no outcome whose true probability p is uniform between 0.3 and 0.7, five personas and
  one outsider who forecast p with parts of ±0.21, scored against the outcome. Closed forms: the outcome's
  unforeseeable part has variance E[p(1 − p)] = 71/300, 84.29% of one persona's mean squared error; the spread
  estimate tends to the correlation of the scored errors, 0.84293 when the personas share nothing and 0.937172 at
  rho = 0.6; the estimate against the outsider tends to rho, because that part cancels. 1,000 seeded logs of 20,
  100 and 500 pull requests give the 5th, 50th and 95th percentiles of both estimates.
- `hypothesis_test`: the thresholds written before the first run, and whether each holds.
- `worked_examples`, `transfer_task`, `checks`.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 35 checks fails; `results.json` lists them under
`checks` with the number of times each was evaluated. The agreement between the simulation and the closed form is
not one of them: it is the hypothesis, and it is reported under `hypothesis_test` whatever the outcome.

**Hand-computed case.** Two forecasters, rho = 0.36, so that √rho = 0.6 and √(1 − rho) = 0.8 exactly, and every
part is +1 or −1. The error of the average is `0.6 C + 0.8 (I_1 + I_2) / 2`:

```text
C    I_1  I_2    error of the average    squared
+1   +1   +1          1.4                 1.96
+1   +1   -1          0.6                 0.36
+1   -1   +1          0.6                 0.36
+1   -1   -1         -0.2                 0.04
-1   +1   +1          0.2                 0.04
-1   +1   -1         -0.6                 0.36
-1   -1   +1         -0.6                 0.36
-1   -1   -1         -1.4                 1.96
```

The eight squares add to 5.44, so the mean squared error is 5.44 / 8 = 0.68, and the closed form gives
0.36 + 0.64 / 2 = 0.68. The script must find 0.68 by both routes, in exact fractions.

**Other known answers.** rho = 0 gives `sigma^2 / k`; one forecaster has a mean squared error of `sigma^2` at every
rho; a fourteenth forecaster of the panel's own kind gives the closed form for k = 14, and equal weights are then
the best weights; an independent newcomer with the best weight adds exactly 1 to the panel's worth; the
two-estimator formula for the best weight equals the exact solution of the full 14-by-14 system of weights
(Gauss-Jordan elimination in fractions); the three cases of two judges sum to 1, and each judge keeps the accuracy
p and the pair the correlation rho; E[p(1 − p)] from the moments of the uniform equals the integral, in exact
fractions; every simulated yes/no forecast lies between 0 and 1; the outsider estimate's denominator is never
zero; a log of 500 pull requests gives a narrower outsider range than a log of 20.

**An identity that can fail.** On each of 8,000 cases (1,000 occasions, four values of rho, k = 5 and k = 14) the
squared error of the average must equal the mean squared error of the forecasters minus their spread, within 1e-12.

**Negative controls.**

- "The simulation agrees with the closed form within 4 standard errors" could pass with standard errors that are
  too large. The same test is applied to a formula that is wrong when rho > 0, `sigma^2 / k`: it is rejected in all
  39 cells with rho > 0 and k ≥ 2, by at least 82.26 standard errors.
- The table's cells are too coarse to tell k = 13 from k = 14 (a drop of 0.002198 at rho = 0.6 against a standard
  error of 0.0013). `last_forecaster` therefore compares the two on the same occasions: the simulated drop is
  12.75 of its standard errors away from zero and 20.26 away from the independent drop.
- The identity is evaluated again with a stale average (that of one forecaster too few): it fails in 8,000 of
  8,000 cases.

## Limits

- One error model: every forecaster has the same accuracy and every pair the same correlation; forecasts are
  numbers combined by a weighted average. The project's panel combines verdicts by a strictest-wins rule, and its
  council keeps the minimum of two reviewers' scores; this arithmetic describes neither.
- The draws are uniform, so light-tailed. The closed forms hold for any distribution with these variances and
  correlations, but the standard errors, and above all the ranges in `scored_log` and `yes_no_outcome`, would be wider with
  heavy tails.
- The split of rho = 0.6 into a context share of 0.3 and a model share of 0.3 is invented. So is every value of rho.
- The estimate of rho in `scored_log` divides by the mean squared error of one agent, in a model without bias
  and without the outcome's unforeseeable part; with that part, it measures the outcome (`yes_no_outcome`).
  With a shared bias left in, it counts the bias as shared error: 0.4 instead of 0.25 in the transfer task
  (`transfer_task.q5_what_agreement_shows`).
- The best weights are computed from the true correlations. Weights estimated from a short record are noisier,
  which this fixture does not simulate.
- `agreement_of_two` rests on a reading of the policy's settings that the policy does not state, on two judges of
  equal accuracy, and on a yes/no question, where two wrong answers necessarily coincide.
- The estimate against the outsider assumes the outsider shares nothing with the panel but the outcome. If its
  errors share a correlation c with each persona's (with the personas' error variance), it tends to
  (rho − c) / (1 − c): less than rho when c > 0 (shared context or model), more when c < 0. The log cannot measure c.
- Nothing here measures the project's agents. No persona's answer and no outcome was read; the council's nine
  scores come without outcomes, and reviewer_a's never varies. The correlation between the agents' errors has
  not been estimated.
