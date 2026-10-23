---
module_id: psy-022-competing-explanations
department: psychohistory
course: "Competing Explanations: Comparing Models on Small Data"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-022
version: "0.1.0"
---

# Competing Explanations: Comparing Models on Small Data

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will fit three count distributions by maximum likelihood, rank them with AIC and BIC, measure how often they pick the true model at this sample size, and name the assumption the three share. **Project question:** the daily trigger counts can be "explained" as Poisson, geometric or negative binomial; which explanation do the data favour, how decisively, and what does the winner still fail to describe?

[PSY-008](psy-008-bursts-are-not-rates.md) showed that these counts are far more dispersed than a Poisson process and that busy days come in runs; [PSY-007](psy-007-power-law-or-not.md) and [PSY-010](psy-010-growth-curves-short-series.md) fit other families to other data.

## 1. Three candidates and their likelihoods

**Observed.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/extract.py) reads the 594 files of [`state/triggers/archived`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) at commit `4b03838` and writes [`observed-input.json`](../../../fixtures/psychohistory/psy-022/observed-input.json): one count per UTC calendar day, n = 119 days from 2026-03-20 to 2026-07-16, S = 594 events. 19 days have none, 63 have exactly one, the busiest has 109; the variance, 196.848669 (divisor n), dwarfs the mean, 4.991597.

Each candidate gives a probability to k events in a day and treats days as independent draws, so the log-likelihood (log L) is a sum over days:

```text
Poisson            P(k) = exp(-λ) λ^k / k!                 log L = S ln λ - n λ - Σ ln(x!)
geometric          P(k) = (1 - q) q^k                      log L = n ln(1 - q) + S ln q
negative binomial  P(k) = [r (r+1) ... (r+k-1) / k!] (r/(r+μ))^r (μ/(r+μ))^k
```

Setting the derivative to zero gives closed forms: λ = S/n and q = S/(n + S). For the negative binomial, μ = S/n and r is the zero of the score d(log L)/dr, found by a one-parameter search; its variance is μ + μ²/r (the geometric's is μ + μ², at r = 1). **Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/analyze.py):

| Model | Estimates | log L |
|---|---|---|
| Poisson | λ = 4.991597 | −1007.841 |
| geometric | q = 594/713 = 0.8331 | −321.518 |
| negative binomial | r = 0.430337, μ = 4.991597 | −298.913 |

**Checking the search.** Bisection of the score (relative tolerance 1e-10 on r) returns 0.430337 from three brackets, [1e-6, 1e6], [0.01, 100] and [0.2, 3]. A golden-section search on log L agrees within 1e-6, and recovers the Poisson and geometric closed forms. The score changes sign once on a grid from 1e-4 to 1e4: one maximum. At r = 1 the negative binomial log L equals the geometric one; at r = 10^6 it approaches the Poisson one as theory predicts.

### Practice Exercise 1

From n = 119 and S = 594, compute λ and q. Using ln(1 − q) = −1.790358 and ln q = −0.182602, rebuild the geometric log-likelihood. Why must the negative binomial reach at least that value, whatever the data?

> **Answer:** `λ = 594 / 119 = 4.991597`; `q = 594 / (119 + 594) = 594/713 = 0.8331`. Then `log L = 119 × (−1.790358) + 594 × (−0.182602) = −213.0526 − 108.4656 = −321.5182`, or −321.518. With r = 1 the negative binomial is the geometric, so its maximum over r cannot be lower: the larger model's gain is guaranteed, only its size is information.

## 2. Price the extra parameter: AIC and BIC

```text
AIC = 2k - 2 log L
BIC = k ln(n) - 2 log L        k = free parameters, ln(119) = 4.779123
```

Lower is better; k is 1, 1 and 2; each parameter costs 2 AIC points and 4.779 BIC points. **Computed**, from log L rounded to three decimals:

| Model | AIC | ΔAIC | BIC | ΔBIC |
|---|---|---|---|---|
| Poisson | 2017.682 | 1415.856 | 2020.461 | 1413.077 |
| geometric | 645.036 | 43.21 | 647.815 | 40.431 |
| negative binomial | 601.826 | 0 | 607.384 | 0 |

Both criteria rank negative binomial, geometric, Poisson. Twice the log-likelihood gain from freeing r is 45.21.

**How decisive, on the sources' scales.** Burnham and Anderson (2004, p. 271) give "simple rules of thumb" for ΔAIC: up to 2, "substantial support"; 4 to 7, "considerably less support"; above 10, "essentially no support" (2 to 4 and 7 to 10 are unnamed). Kass and Raftery (1995, p. 777) grade twice the log Bayes factor, which a BIC difference roughly approximates (p. 778): 0 to 2 "not worth more than a bare mention", 2 to 6 positive, 6 to 10 strong, above 10 very strong, "not a calibration" but "a rough descriptive statement". On both scales the geometric and the Poisson are far behind.

**What the numbers are not.** A ΔAIC of 43.21 is not a probability that the geometric is false or the negative binomial true. Burnham and Anderson read a large ΔAIC as making a model less plausible as "the best approximating model in the candidate set"; discussing BIC (p. 279), they add that a posterior model probability near 1 "does not justify an inference" that the model is truth, which "requires an a priori certainty that the true model is in the model set".

### Practice Exercise 2

From log L = −321.518 (geometric) and −298.913 (negative binomial), with ln 119 = 4.779123, compute both models' AIC and BIC and the two differences. Read each difference on its cited scale.

> **Answer:** AIC: `2 + 643.036 = 645.036` and `4 + 597.826 = 601.826`, difference 43.21: "essentially no support" for the geometric. BIC: `4.779123 + 643.036 = 647.815` and `9.558246 + 597.826 = 607.384`, difference 40.431: "very strong" on the Kass and Raftery scale. Rules of thumb on a ranking, not probabilities.

## 3. How often do the criteria pick the true model?

**Synthetic.** Each fitted model generated 5,000 seeded samples of independent days at four lengths (two shown), and all three models were refitted to each. Share where each criterion picked the true generator (AIC / BIC):

| True generator | 15 days | 119 days |
|---|---|---|
| Poisson | 95.62% / 97.54% | 93.62% / 98.62% |
| geometric | 82.06% / 88.32% | 84.30% / 97.08% |
| negative binomial | 57.28% / 49.84% | 100% / 99.94% |

At 119 days the errors run one way: with the geometric true, AIC picks the negative binomial in 785 of 5,000 samples (15.70%), BIC in 146 (2.92%). Theory predicts this: the geometric is the negative binomial at r = 1, so twice the gain from freeing r behaves in large samples as a chi-square with 1 degree of freedom (Wilks 1938), and exceeds 2 with probability 0.1573 and ln 119 with probability 0.0288. Both seeded shares are within two standard errors of these. No geometric sample came near the observed gain of 45.21 (largest 12.934); 622 negative binomial samples reached it.

**Computed: what carries the ranking.** Refitting after leaving out the busiest days:

| Busiest days left out | r | ΔAIC (G − NB) | ΔBIC (G − NB) |
|---|---|---|---|
| 0 | 0.430337 | 43.21 | 40.431 |
| 1 (109 events) | 0.493112 | 25.996 | 23.226 |
| 2 (109, 72) | 0.556301 | 15.182 | 12.42 |
| 4 (45 or more) | 0.736965 | 1.578 | −1.167 |
| 11 (18 or more) | 2.702526 | 10.178 | 7.496 |

The four busiest days, two pairs of neighbours (21–22 March, 27–28 June), carry the decisive gap. With eleven out, the negative binomial wins again with r = 2.7, less dispersed than the geometric: one name, two shapes. Adding back the twelve trigger files deleted without being archived (a count borrowed from PSY-009) gives 44.566 and 41.787: no change.

### Practice Exercise 3

Synthetic. An imaginary 15-day log gives a BIC 1.1 lower for the geometric. At that length, with the parameters fitted above, BIC picks the geometric in 4,416 of 5,000 seeded samples when the geometric is true, and in 2,502 of 5,000 when the negative binomial is true. What do you report?

> **Answer:** 1.1 lies in the 0 to 2 band, "not worth more than a bare mention". The check agrees: a geometric pick is `4,416 / 2,502 = 1.76` times as frequent under the geometric as under the negative binomial. Report both as compatible with the log; 1.76 is not a probability that the geometric is true.

### Practice Exercise 4

Leave out the four busiest days: 115 days, log L −247.501 (geometric) and −245.712 (negative binomial), ln 115 = 4.744932. Which model does each criterion pick, and by how much?

> **Answer:** AIC: `2 + 495.002 = 497.002` against `4 + 491.424 = 495.424`, negative binomial by 1.578. BIC: `4.744932 + 495.002 = 499.747` against `9.489864 + 491.424 = 500.914`, geometric by 1.167. The criteria disagree, both by under 2: the 43.21-point verdict rests on 4 of 119 days.

## 4. The assumption all three share

**Computed: an absolute check.** The criteria only rank; expected days per band show what each fit describes:

| Events in the day | Observed | Poisson | geometric | negative binomial |
|---|---|---|---|---|
| 0 | 19 | 0.81 | 19.86 | 40.00 |
| 1 | 63 | 4.04 | 16.55 | 15.85 |
| 2 | 13 | 10.07 | 13.78 | 10.43 |
| 3 to 11 | 13 | 103.44 | 55.51 | 36.50 |
| 12 to 44 | 7 | 0.64 | 13.27 | 15.62 |
| 45 or more | 4 | 0.00 | 0.03 | 0.60 |

The winner gains in the tail (0.60 expected days with 45 events or more, against 0.03) and pays in the body (Exercise 5).

**Order.** Shuffling the days leaves all three log-likelihoods unchanged (a self-check), but the data are not order-free: the lag-1 autocorrelation of the counts is 0.4587, reached by 3 of 10,000 shuffles (95th percentile 0.1454); on ranks (each count replaced by its rank, ties sharing their mean rank) it is 0.3861, reached by none. Controls: a shuffled order scores −0.0057, the sorted days 0.7209. Busy days follow busy days: the shared assumption of independent, identically distributed days is false here.

**Synthetic: what dependence does to the criteria.** In a *sticky geometric* process each day repeats the previous count with probability 0.46, otherwise drawing afresh from the fitted geometric, so every day still has the geometric distribution. Over 5,000 samples of 119 days, AIC picks the negative binomial in 2,008 (40.16%, against 15.70% for independent days) and BIC in 961 (19.22%, against 2.92%): runs look like extra dispersion. Only 1 sample reached a gain of 45.21: such runs alone rarely produce the observed gap. The negative binomial is the least bad of three models of independent days, not a description of how triggers arrive.

**The strongest objection to this lesson's reading:** the four days are data, not noise; a gain of 45.21 appeared in no independent geometric sample and in 1 of 5,000 sticky ones, so the negative binomial rightly captures a heavier tail. The tail is heavier. What remains open is whether one negative binomial, drawn afresh each day, produced it: the four days are two episodes, not four independent draws, and the misfit at 0 and 1 events says the body is wrong. **This sample cannot distinguish a negative binomial marginal (the distribution of one day's count) from a mixture of ordinary days and rare burst episodes.** A longer log with many more episodes would settle it, or a two-regime model compared with the negative binomial on data neither was fitted to.

### Practice Exercise 5

The fitted negative binomial gives P(0) = 0.336109 and P(1) = 0.13316. Compute the expected empty and one-event days in 119, compare with the log, and rewrite "the daily trigger counts follow a negative binomial distribution" as a claim these results support.

> **Answer:** `119 × 0.336109 = 40.00` empty days against 19, and `119 × 0.13316 = 15.85` one-event days against 63: the winner misses the two commonest counts by factors of about 2 and 4. A supported claim: "Of three models of independent days, AIC and BIC prefer the negative binomial; the preference rests on four days in two episodes, the fit misses the common counts, and the days are not independent."

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the archived trigger folder linked above; `extract.py` refuses a folder that differs from the pin.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-022/extract.py`, then `analyze.py` in the same folder; `analyze.py --check` compares a fresh run with the saved [`results.json`](../../../fixtures/psychohistory/psy-022/results.json). Seeds and settings are in [`scenarios.json`](../../../fixtures/psychohistory/psy-022/scenarios.json); the [README](../../../fixtures/psychohistory/psy-022/README.md) lists the self-checks, a hand-worked case and the negative controls.

**Method references.** Akaike, H. (1974), "A new look at the statistical model identification", *IEEE Transactions on Automatic Control* 19(6), 716–723. Schwarz, G. (1978), "Estimating the Dimension of a Model", *The Annals of Statistics* 6(2), 461–464. Kass, R. E., and Raftery, A. E. (1995), "Bayes Factors", *Journal of the American Statistical Association* 90(430), 773–795 ([authors' copy](https://sites.stat.washington.edu/raftery/Research/PDF/kass1995.pdf)). Burnham, K. P., and Anderson, D. R. (2004), "Multimodel Inference: Understanding AIC and BIC in Model Selection", *Sociological Methods & Research* 33(2), 261–304. Wilks, S. S. (1938), "The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses", *The Annals of Mathematical Statistics* 9(1), 60–62.

**Not done.** No model of dependence between days was fitted, no small-sample correction of AIC was applied, and no comparison was made on held-out data (PSY-018 treats that). No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Fit a two-state model (ordinary and burst days, each with a probability of staying) to the 119 counts: if it reproduces the 19 empty days, the 63 one-event days and a lag-1 autocorrelation near 0.46, the reading changes from "least bad of three" to "two regimes".
