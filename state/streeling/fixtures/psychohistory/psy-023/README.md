# PSY-023 fixture: alarm rules for a plan

The program, `analyze.py`, lives in `scripts/streeling_fixtures/psychohistory/psy-023/` because this repository keeps executable code under `scripts/`; the data files it reads and writes are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-023-monitoring-a-plan.md`.
Python 3.9 or later, standard library only. Everything here is synthetic: no file of the repository is read, so
there is no `extract.py` and no `observed-input.json`, and no weekly output of the project was measured.

## Files

| File | Kind | What it is |
|---|---|---|
| `scenarios.json` | assumed | Every assumption: the plan (21 × 25 = 525 courses at 5 a week, 105 weeks), the weekly output model (10 drafts in work, each finished in the week with probability 1/2), the slowdown (6 drafts from week 53) and its variants, the four families of alarm rules and their thresholds, the calibration target (at most 1/20), the seeds and run counts, the thresholds of the research cycle's hypothesis, the bursty-output objection, the costs, the inputs of the lesson's exercises, the hand-computed cases, the negative control and the learner transfer task. |
| `analyze.py` | script | Reads only `scenarios.json`, computes every figure exactly, checks it against a seeded simulation, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py --check
```

One run takes about 6 seconds on the author's Windows machine (11 seconds under WSL). `--check` recomputes the
results and compares them with the saved file, ignoring only CRLF against LF. `--scenarios` and `--output` name
other files.

## Two routes to every figure

**Exact.** Each week a fixed number of drafts is in work and each draft is finished with probability 1/2, so a
week's output is a number of heads among fair coins, and every history of a plan is one of 2^(drafts × weeks)
equally likely coin histories. For each rule the script carries, week by week, the number of histories in each
state of the rule that have not yet raised an alarm (the cumulative shortfall for the tolerance rule, Page's sum
for the cumulative-sum rule); a history leaves the count in the week of its first alarm. These counts are Python
integers, and the probabilities are fractions: nothing is approximated before the final rounding. Delays after a
slowdown are summed as `mean delay = sum over d of P(delay > d)`, until the share still silent is below 10^-18
(`delay.stop_below`); the cumulative-sum rule's average run length is solved exactly from its linear equations.
"Calibrated" means the smallest whole threshold whose exact on-plan probability of at least one alarm in 105 weeks
is at most 1/20.

**Simulated.** Three seeded sets of 20,000 runs (`random.Random(seed).random()`, seeds in `scenarios.json`; a
week with d drafts counts the top d bits of one draw as d coins): plans on plan, plans with the slowdown, and plans
with bursty output. Every simulated share is stored with its count, its binomial standard error and its exact
(Clopper–Pearson) 95% interval, and, where an exact value exists, its distance from it in standard errors; every
simulated mean delay with its standard error. The simulation shares the model with the exact route, so it checks
the arithmetic and the code, not the model.

## Why the output is the same bytes everywhere

- Exact figures are integers and fractions; a fraction is rounded half to even only when it is stored.
- No logarithm, exponential or power from the C math library enters the output. The floating-point functions used
  are `+`, `-`, `*`, `/`, `math.sqrt` and `math.fsum`, which IEEE 754 and Python define to the last bit; the exact
  intervals are built from the binomial terms by those operations and located by bisection.
- Draws come from `random.Random(seed).random()`, which is the same Mersenne Twister on every platform; no global
  random state, clock or machine property is used.
- Stored floats are rounded: probabilities to 6 decimals, weeks and costs to 2, courses and ratios to 4, distances
  in standard errors to 2.

Checked: the same bytes (SHA-256 of `results.json` identical) on CPython 3.9.25, 3.12.12 and 3.14.2 under Windows
x86-64 and on CPython 3.14.5 under Linux x86-64 (WSL). Not run on macOS or on an ARM processor.

## Observed, computed, synthetic

- **Observed:** nothing. The project question's plan (25 courses in each of 21 departments) is a figure from a draft
  curriculum specification that is not in the repository. At Demerzel commit
  `4b03838800dcd4894f1e026461979bff1d985ca8` the repository holds 23 department records, 21 of them with a course
  folder, and its README counts 23 departments and 21 course tracks with no number of courses per track. The 21, the
  25 and the weekly output are inputs.
- **Synthetic:** everything in `results.json`. `transfer_task` describes a hypothetical two-person team, not
  Streeling. No governance artifact's path appears in these files: the repository's metrics count every tracked
  file containing such a path as a citation of that artifact, and a course fixture must not move that count.

## Sections of `results.json`

- `plan`: the plan's size, the weekly output distribution (ways out of 1,024), its mean and variance, the slowdown,
  and the standard deviation of the cumulative output at six weeks.
- `single_look`: one look at one week, by counting: a weekly limit, and the prediction band of z standard
  deviations at six weeks, with the simulated first week and the normal-tail constant 0.02275 next to them.
- `weekly_limit`: an alarm for any week at or under a limit (0, 1, 2): independent looks, so the closed forms
  `1 − (1 − a)^T`, an average run length of `1/a` weeks and a mean delay of `1/b` weeks (b the chance in a slow week)
  must agree with the recursion; and the per-week chance a 5% target over 105 weeks would need.
- `prediction_band_every_week`: the band checked every week (z = 2, 5/2, 3): probability of at least one alarm by
  week 13 to 210, against the largest single look and the sum of the single looks.
- `tolerance`, `cumulative_sum`: per threshold, the probability of at least one alarm on plan, the simulated share
  with its interval, and the delay after the slowdown (mean, 90th percentile, simulated mean); for the cumulative
  sum also the average run length on plan and after a slowdown, and the calibrated thresholds.
- `change_week`, `milder_slowdown`, `bursty_output`: the calibrated rules when the slowdown starts in another week,
  when it is milder (8 drafts, 80% of the plan), and when output of the same mean comes in batches.
- `costs`: the cheapest decision interval under assumed costs.
- `hypothesis_test`: the thresholds written into the research cycle before the first run, and whether each holds.
- `worked_examples`: the figures of the lesson's exercises, intermediate values included.
- `controls`, `simulation_against_exact`, `transfer_task`, `checks`.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 24 checks fails; `results.json` lists them under
`checks`. They include the accounting identity of the recursion (histories still silent plus histories with an
alarm this week equal the silent histories of the week before times the ways of a week, evaluated 14,257 times),
the binomial tail of one look reproduced by the recursion, the closed forms of the weekly limit, the bounds
`largest single look ≤ P(at least one alarm) ≤ sum of the single looks`, two exact routes to the cumulative-sum
delays, the reflection principle, the calibrations (the threshold meets the target and the next lower one does
not), and every simulated figure within 4.5 standard errors of its exact value.

**Hand-computed case.** Two drafts in work, 1 course a week planned, 3 weeks: a week's output is 0, 1 or 2 in
1, 2 and 1 of its 4 coin histories, so its shortfall is +1, 0 or −1, and there are 4^3 = 64 histories.

- Tolerance 2 (alarm once the cumulative shortfall reaches 2): +1, +1 in weeks 1 and 2 fires in week 2, whatever
  week 3 does: 1 × 1 × 4 = 4 histories. Firing first in week 3 needs a sum of 2 in three weeks without +1, +1 at the
  start: +1, 0, +1 (1 × 2 × 1 = 2) and 0, +1, +1 (2 × 1 × 1 = 2). In all 4 + 2 + 2 = **8 of 64**.
- Page's sum with reference value 0 and decision interval 2, in its recursive form C = max(0, C + shortfall): the
  same 4 histories fire in week 2; in week 3 a history fires when C = 1 after week 2 and week 3 brings +1. C = 1
  after +1, 0 (2 histories), 0, +1 (2) and −1, +1 (1), so 5 more: **9 of 64**. The extra history is −1, +1, +1:
  its cumulative shortfall is −1, 0, 1 and never reaches 2, but the sum forgets the early surplus (C = 0, 1, 2).

The script must find 8 and 9.

**Known answers.** For a walk of single steps up or down, the reflection principle gives the probability that the
highest value in n steps reaches c as `P(end ≥ c) + P(end > c)`; for 20 steps and level 4 the recursion must give
exactly the same fraction, 200965/524288, against 131975/524288 for one look at the end. With 0 alarms in n runs the
upper limit u of the exact interval must solve `(1 − u)^n = 0.025` (n = 20, u = 0.168433).

**Negative controls.** Agreement with the exact figures could pass on a lenient test. The simulated share of
on-plan runs with an alarm at the calibrated tolerance, 32, is compared with the exact probability of a tolerance
of 30: it must be more than 4.5 standard errors away, and is 8.67. Page's two forms (the sum of the scores against
its lowest earlier value, and the recursion) must give the same highest value in all 20,000 on-plan runs and the
same alarm weeks in all 20,000 slowdown runs; 731 on-plan runs reach the calibrated interval, so the comparison
does not pass on runs without alarms.

## Limits

- Weeks are independent and so are drafts: no trend, no seasonality, no week that depends on the one before. Real
  output is likely burstier; `bursty_output` shows what thresholds calibrated on steady output then do.
- The slowdown is abrupt, permanent and of one size; the reference value 1 of the cumulative sum is tuned to it.
- The costs are a crude model: one slowdown at week 53 or none, one review per false alarm.
- 28 simulated shares are compared with exact values; one 95% interval (decision interval 9 on plan, 274 of 20,000
  runs, 2.97 standard errors from the exact value) does not cover it, about what 1 in 20 predicts. The three sets of
  runs are reused across thresholds, so the comparisons are not independent.
- Page's 1954 article was not opened; the scheme is stated as the NIST/SEMATECH handbook gives it, and its two forms
  are checked against each other, not against the article.
- Nothing here measures the project.
