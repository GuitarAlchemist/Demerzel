---
module_id: psy-016-brier-score
department: psychohistory
course: "Probability Forecasts and the Brier Score"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-016
version: "0.1.0"
---

# Probability Forecasts and the Brier Score

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will turn a record of labels into a yes-or-no event, score stated probabilities with the Brier and logarithmic scores, measure skill against a base-rate forecast, and test whether a scoring rule is *proper*. **Project question:** how should a probability forecast about governance labels be scored, and what does the score reward?

[PSY-005](psy-005-persistence-baseline.md) scored the forecast "the label stays the same" by counting right and wrong calls. A forecaster who says "a change is 2% likely" is neither right nor wrong on one pair: the stated number needs a score of its own, built here on PSY-005's pairs. [PSY-017](psy-017-calibration-with-six-observations.md) treats calibration (do stated probabilities match observed frequencies?) on a handful of outcomes; [PSY-025](psy-025-capstone-preregistered-forecast.md) applies the score to a forecast written in advance.

## 1. An event, a stated probability, a score

**Observed.** At each run of a [feeder script](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), the repository's [quality trend](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) gains one row per governance artifact (a policy, a skill), with an effectiveness label (`effectiveness_to`): a truth value such as T (true) or U (unknown) for a written claim about the artifact. As in PSY-005, a *pair* is two consecutive rows of one artifact, both labelled. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/extract.py) snapshots the five files at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-016/observed-input.json): 1,548 rows, 18 artifacts, **1,529 pairs**. The label differs between the two rows in **1** pair. Eleven pairs start at a *seed row* (a recorded starting state) and end 78.5 days later at the first feeder run; the one change is among them. The other **1,518** pairs join two feeder runs, 0.001 to 6.453 days apart, and none changed.

The *event* is "the label differs at the artifact's next row"; the outcome `o` is 1 if it happened and 0 if not. A *probability forecast* states a number `p` between 0 and 1 for the event before the outcome is known. "Next row" is not a fixed span of time: a forecaster who states one `p` for every pair treats a 78.5-day step like a step of minutes.

The *Brier score* is the mean squared difference between stated probability and outcome:

```text
BS = (1/N) × sum of (p_i - o_i)²
```

Lower is better: 0 means always certain and right, 1 always certain and wrong. Brier (1950) adds the same term for "no change", which doubles every value (range 0 to 2); this lesson uses the common one-term form.

**Synthetic forecasters, computed scores.** Nobody issued forecasts for these pairs. [`scenarios.json`](../../../fixtures/psychohistory/psy-016/scenarios.json) defines imaginary forecasters by the probability each states, and [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/analyze.py) scores them on the observed outcomes ([`results.json`](../../../fixtures/psychohistory/psy-016/results.json)). Scores are rounded to six decimals, or nine where needed.

| Forecaster | States | Sum of squared errors | Brier score, 1,529 pairs | Brier score, 1,518 pairs |
|---|---|---|---|---|
| `never` | 0 | 1 | 0.000654022 | 0 |
| `base_rate` | 1/1,529 | 0.999346 | 0.000653594 | 0.000000428 |
| `one_percent` | 0.01 | 1.1329 | 0.000741 | 0.0001 |
| `five_percent` | 0.05 | 4.7225 | 0.003089 | 0.0025 |
| `coin` | 0.5 | 382.25 | 0.25 | 0.25 |

`never` is PSY-005's persistence forecast stated with certainty. For a forecast of 0 or 1 the Brier score is the error rate, here 1/1,529, PSY-005's base rate of change; `base_rate` states that share on every pair.

### Practice Exercise 1

A forecaster states 0.02 on every pair. Compute its sum of squared errors and its Brier score on the 1,529 pairs, then its Brier score on the 1,518 pairs between feeder runs.

> **Answer:** The changed pair contributes `(0.02 − 1)² = 0.9604`; the 1,528 unchanged pairs contribute `1,528 × 0.02² = 0.6112`. Sum `1.5716`; Brier score `1.5716 / 1,529 = 0.001028`. Between feeder runs nothing changed, so every pair contributes `0.02² = 0.0004`, and that is the score.

## 2. One pair carries the score

The *Brier skill score* compares a forecast with a reference on the same pairs, as PSY-005 did for accuracy, but this lesson replaces PSY-005's reference, persistence, with the base rate `b`, the share of pairs where the event happened, stated on every pair:

```text
skill = 1 - BS / BS_ref        BS_ref: the reference's Brier score on the same pairs
```

For the base-rate forecast `BS_ref = b × (1 − b)`. When the reference makes no error, skill is undefined, as it was for PSY-005's persistence: on the 1,518 pairs the reference states their base rate, 0, while the `base_rate` forecaster keeps 1/1,529.

**Computed.** Each sum of squared errors splits into the changed pair's part and the rest:

| Forecaster | Share from the changed pair | Skill |
|---|---|---|
| `never` | 100% | −0.000654 |
| `base_rate` | 99.93% | 0 |
| `one_percent` | 86.51% | −0.133641 |
| `five_percent` | 19.11% | −3.725591 |
| `coin` | 0.07% | −381.500164 |
| `long_step_hedge` | 88.86% | 0.087885 |

For a forecaster that states one `p` everywhere, the score is `(p - b)² + b × (1 - b)`, the one-value case of Murphy's (1973) partition, reliability minus resolution plus uncertainty, in which the resolution is 0. The second term, the uncertainty, 0.000654 here, is the same for everyone. The first, the reliability, is all a constant forecaster controls: `(0.01 − 0.000654)² = 0.000087` for `one_percent`. So no constant forecast can beat the base rate of the pairs it is scored on: an identity, not a finding. Positive skill needs different probabilities on different pairs, higher where changes occur.

`long_step_hedge` (synthetic) does that with one rule: 0.1 when the earlier row is a seed row, 0.001 otherwise. It ranks first, ahead of `base_rate` and `never`, with a skill of 0.087885. But its probabilities were chosen by this lesson's author after seeing where the change was, and its whole lead comes from one pair: remove any one of the 1,528 unchanged pairs and the ranking stays as it is; remove the changed pair and those three places reverse.

**Hindsight.** `base_rate` also knows the answer: 1/1,529 could be stated only after every outcome was in. Its lead over `never` is 0.000000428, the square of 1/1,529. When the changed pair resolved, at the first feeder run, no pair had resolved before it, so the record offered no base rate to state.

On this record the first four forecasters score between 0.000596 and 0.000741, and the order of the first three rests on one pair. The score does separate them from `five_percent` and `coin`.

### Practice Exercise 2

Recompute `long_step_hedge`'s sum of squared errors from its two probabilities and the counts of section 1, then its Brier score and its skill. What remains of the sum without the changed pair?

> **Answer:** Changed pair, from a seed row: `(0.1 − 1)² = 0.81`. Ten unchanged pairs from a seed row: `10 × 0.1² = 0.1`. The 1,518 pairs between feeder runs: `1,518 × 0.001² = 0.001518`. Sum `0.911518`; Brier score `0.911518 / 1,529 = 0.000596`. The base rate's sum is `0.999346`, so skill `= 1 − 0.911518 / 0.999346 = 0.087885`. Without the changed pair `0.101518` remains over 1,528 pairs, a score of 0.000066: behind `never` (0) and `base_rate`, rank 3.

### Practice Exercise 3

How many of the 1,529 pairs would have to change before stating 0.01 everywhere scored better than stating 0? And for 0.05?

> **Answer:** With `k` changed pairs among `N`, `never` scores `k/N` and a constant `p` scores `[k(1 − p)² + (N − k)p²]/N`. The second is smaller when `Np² < 2kp`, that is `k > Np/2`. For 0.01: `1,529 × 0.01 / 2 = 7.645`, so 8 changes. For 0.05: `38.225`, so 39.

## 3. What "proper" means

A scoring rule is *proper* when a forecaster gets the best expected score by stating the probability they believe, and *strictly proper* when no other statement does as well (Gneiting and Raftery 2007).

**Synthetic.** Assume an event has true probability `t = 0.3` and a forecaster states `q` every time. The expected Brier score is `t(1 − q)² + (1 − t)q² = (q − t)² + t(1 − t)`. A tempting alternative, mean absolute error `|q − o|`, has expectation `t(1 − q) + (1 − t)q`.

| Stated `q` | Expected Brier score | Expected absolute error | Simulated mean Brier score |
|---|---|---|---|
| 0 | 0.3 | 0.3 | 0.30355 |
| 0.1 | 0.25 | 0.34 | 0.25284 |
| 0.3 | 0.21 | 0.42 | 0.21142 |
| 1 | 0.7 | 0.7 | 0.69645 |

The Brier score is lowest at `q = 0.3`, the truth. The absolute error is lowest at `q = 0`: it pays a forecaster who believes 30% to say "never". A seeded simulation (6,071 events in 20,000 cases) agrees.

Under the Brier score, misstating costs `(q − t)²` per forecast in expectation. For a rare event that is small: with `t = 0.02`, stating 0 costs 0.0004. Hence the near-equal first rows of section 1's table: the Brier score is proper, but it pays little for the difference between "never" and "rarely".

### Practice Exercise 4

Synthetic. You believe an event has probability 0.2. Compute the expected Brier score and the expected absolute error if you state 0.2, and if you state 0. Which statement does each rule reward?

> **Answer:** Brier: stating 0.2 gives `0.2 × 0.8² + 0.8 × 0.2² = 0.16`; stating 0 gives `0.2 × 1² + 0.8 × 0² = 0.2`. The honest statement wins by `0.04 = (0 − 0.2)²`. Absolute error: stating 0.2 gives `0.2 × 0.8 + 0.8 × 0.2 = 0.32`; stating 0 gives `0.2`. That rule rewards a certainty the forecaster does not hold, so it is not proper.

## 4. The logarithmic score, and the strongest objection

The *logarithmic score* (Good 1952) is the mean of `−ln` of the probability given to what happened: `−ln p` when the event occurred, `−ln(1 − p)` when it did not. It is strictly proper too. **Computed** (natural logarithm):

| Forecaster | Logarithmic score, 1,529 pairs | Logarithmic score, 1,518 pairs |
|---|---|---|
| `never` | infinite | 0 |
| `base_rate` | 0.005449 | 0.000654 |
| `one_percent` | 0.013056 | 0.01005 |
| `five_percent` | 0.053219 | 0.051293 |
| `coin` | 0.693147 | 0.693147 |
| `long_step_hedge` | 0.003188 | 0.001001 |

Between feeder runs `never` is perfect under both scores. With the one event added, it is third under the Brier score, whose loss is capped at 1 per pair, and last under the logarithmic score, because `−ln 0` has no finite value. The Brier score forgives a certainty that fails once in 1,529 pairs; the logarithmic score never does.

### Practice Exercise 5

`one_percent`'s losses `−ln(…)` add up to 19.962083 over the 1,529 pairs; the changed pair supplies `−ln 0.01 = 4.60517`. Check its logarithmic score and give the changed pair's share. Then say which score a team should choose if nobody is to state 0 for something possible, and what in the tables shows it.

> **Answer:** `19.962083 / 1,529 = 0.013056`; the share is `4.60517 / 19.962083 = 23.07%`, against 86.51% of the same forecaster's squared error. The team should choose the logarithmic score: `never` goes from 0 on the 1,518 pairs to infinite once the changed pair is included, while its Brier score only moves from 0 to 0.000654.

**Answer to the project question.** Score a stated probability with a proper rule, against a reference that could have been stated in advance. The Brier score rewards honest probabilities that differ where outcomes differ; on this record the hindsight rule `long_step_hedge` leads `base_rate` by only 0.000057, and that lead hangs on one pair.

**The strongest objection to this reading** is that the event may not be a forecastable one. The single change lies on the 78.5-day step from a seed row, and PSY-005 reads it as a recorded retirement, not a drift. Between feeder runs nothing changed, so there both scores reward the smallest stated number. The 1,529 pairs are 18 artifacts read repeatedly, not independent trials, and no score here carries an error bar. **Under the Brier score this sample cannot rank `never`, `base_rate` and `long_step_hedge`: their order turns on one pair. Under the logarithmic score the same three trade places on that pair: with it `never` is last and infinite, without it first.**

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the five quality-trend files and the feeder script linked above. `extract.py` refuses to run if a file differs from its pinned Git blob.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-016/extract.py`, then `analyze.py` in the same folder. The [README](../../../fixtures/psychohistory/psy-016/README.md) lists the self-checks and the negative control.

**Method references.** Brier, G. W. (1950), "Verification of Forecasts Expressed in Terms of Probability", *Monthly Weather Review* 78(1), 1–3. Murphy, A. H. (1973), "A New Vector Partition of the Probability Score", *Journal of Applied Meteorology* 12(4), 595–600. Gneiting, T., and Raftery, A. E. (2007), "Strictly Proper Scoring Rules, Prediction, and Estimation", *Journal of the American Statistical Association* 102(477), 359–378, [doi:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437) (written there as a reward: their quadratic score of a yes/no forecast is minus Brier's two-term score, `−2(p − o)²`). Good, I. J. (1952), "Rational Decisions", *Journal of the Royal Statistical Society, Series B* 14(1), 107–114, [doi:10.1111/j.2517-6161.1952.tb00104.x](https://doi.org/10.1111/j.2517-6161.1952.tb00104.x).

**Not done.** No forecast was issued before its outcome: every forecaster is imaginary, and `base_rate` and `long_step_hedge` use hindsight. Calibration was not examined (PSY-017). No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Once the record holds several changes between feeder runs, score probabilities written down before each run against a reference fixed in advance. If a rule whose probability grows with the time between the two rows keeps positive skill there, "one pair decides the ranking" gives way to "the length of the step carries information".
