---
module_id: psy-012-early-warning-false-alarms
department: psychohistory
course: "Early-Warning Signals and Their False Alarms"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-008-probability-conditional-reasoning", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-012
version: "0.1.0"
---

# Early-Warning Signals and Their False Alarms

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will compute two rolling indicators, variance and lag-1 autocorrelation, summarise each trend with one rank statistic, and measure an alarm rule on both sides: how often it fires when a system approaches a tipping point, and how often when nothing approaches. **Project question:** PSY-002 proposes signals for a coming regime shift; how often do rising variance and rising autocorrelation appear in a system that is not approaching any transition?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md), which builds on [PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md), lists six signals and asks for three or more to converge. This module takes the literature's two best-studied early-warning indicators and measures, for these two, what PSY-002 does not give for its six: a false-alarm rate. Sections 1 to 3 are **synthetic**: assumed inputs in [scenarios.json](../../../fixtures/psychohistory/psy-012/scenarios.json), computed by [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/analyze.py), saved in [results.json](../../../fixtures/psychohistory/psy-012/results.json). Section 4 alone uses **observed** project data. Instrument changes belong to PSY-011, chaos to PSY-014.

## 1. Why a system slows down before it tips

A *fold bifurcation* is the simplest tipping point: as a *control parameter* q changes, a stable resting state and an unstable threshold approach each other, meet and vanish, and the system jumps elsewhere. The fixture uses the textbook form dx/dt = r + x², written with r = −q², with noise added:

```text
x[t+1] = x[t] + h * (x[t]^2 - q[t]^2) + e[t]      h = 0.005, e ~ Normal(0, 1)
resting state x = -q     unstable threshold x = +q     fold at q = 0
```

Near the resting state a small disturbance d shrinks by a fixed factor per step:

```text
d[t+1] ≈ phi * d[t]       phi = 1 - 2 * h * q
variance = 1 / (1 - phi^2)       lag-1 autocorrelation = phi
```

The second line is the standard result for an *AR(1) process*, where each value is phi times the previous one plus fresh noise; *lag-1 autocorrelation* is the correlation between the series and itself one step later. As q falls toward 0, phi rises toward 1: recovery slows, so fluctuations last longer (autocorrelation up) and pile up (variance up). This *critical slowing down* is the mechanism behind the early-warning signals reviewed by Scheffer et al. (2009).

In the fixture q falls in a straight line from 50 to 10 and never reaches the fold: at the end the unstable threshold is still 8.72 fluctuation standard deviations away, and no approaching run crossed it.

The estimator (section 2) is first tested on known answers. On 200,000 points of stationary AR(1) with phi = 0.9 it returns variance 5.2742 (theory 5.2632) and autocorrelation 0.9002; the fold simulator held at q = 25 returns 0.7513 against a predicted 0.75. Short windows read low: over 1,000 **synthetic** runs with phi = 0.9, the mean estimated autocorrelation is 0.555 in a window of 25 points, 0.7279 at 50, 0.8641 at 200 and 0.8913 at 800, and the mean variance at 25 points is 1.7243 against a true 5.2632. The bias is worst for a slow system, where the signal is supposed to appear.

### Practice Exercise 1

Compute phi, the variance and the standard deviation of the fluctuations at the start (q = 50) and at the end (q = 10) of the approach. By what factor does the variance grow? How many steps does it take to lose half of a disturbance at each end (solve phi^k = 0.5)?

> **Answer:** Start: phi = 1 − 2 × 0.005 × 50 = 0.5, variance 1 / (1 − 0.25) = 1.3333, standard deviation 1.1547. End: phi = 0.9, variance 1 / (1 − 0.81) = 5.2632, standard deviation 2.2942. The variance grows by a factor of 3.9474. With k = ln 0.5 / ln phi, half a disturbance is lost in 1 step at the start and 6.58 steps at the end.

## 2. Two rolling indicators and one trend number

An analyst has one series and cannot see q. The usual recipe (Dakos et al. 2012) slides a *window* of W consecutive points along the series and computes both indicators at each position. The fixture first removes the best-fitting straight line inside each window: the resting level itself drifts, here by 34.64 starting standard deviations, and a drifting level would be counted as variance.

```text
e[u] = y[u] - (a + b * u)        u = 0 .. W-1
variance        = sum(e[u]^2) / (W - 2)
autocorrelation = sum(e[u] * e[u+1]) / sum(e[u]^2)
```

A series of n points gives m = n − W + 1 rolling values of each indicator. *Kendall's tau*, a rank correlation with time, says in one number whether they rise: among the P = m(m − 1)/2 pairs of positions, C are concordant (the later value is larger), D discordant (it is smaller) and t tied (equal). The program computes the tie-corrected form, tau-b.

```text
tau = (C - D) / sqrt(P * (P - t))       +1 always rising, -1 always falling
    = (C - D) / P                       when no two values are equal (t = 0)
M   = min(tau of variance, tau of autocorrelation)       alarm when M >= T
```

M demands that both indicators rise, as PSY-002's convergence does. Three thresholds T are compared:

- **textbook test**: each tau must be "significant at 5%" by the standard one-sided formula, which treats the m values as independent: T = 1.645 × sqrt(2(2m + 5) / (9m(m − 1)));
- **fixed**: T = 0.5;
- **calibrated**: T is the value that 5% of 1,000 separate stationary runs reach (AR(1), phi = 0.7, same n and W), the surrogate-series idea of Dakos et al. (2012).

### Practice Exercise 2

Six consecutive rolling values are 0.8, 0.5, 1.1, 1.4, 1.2, 1.9 (invented). Count the concordant and discordant pairs and compute tau. Does this indicator alone reach T = 0.5?

> **Answer:** 6 × 5 / 2 = 15 pairs. Two are discordant, (0.8, 0.5) and (1.4, 1.2), so C = 13, D = 2 and tau = (13 − 2) / 15 = 0.7333, above 0.5.

## 3. Detection and false alarms, measured

For each record length n and each window (a quarter and a half of n), the fixture ran 1,000 approaching runs and 1,000 runs of each stationary control: AR(1) with phi = 0.5, 0.7 and 0.9. The *detection rate* is the share of approaching runs in which the alarm fires; the *false-alarm rate* is that share among control runs. Each rate under a given threshold has a standard error of at most 1.58 percentage points; the calibrated thresholds, estimated from 1,000 runs and shown to two decimals, add their own error. All values are **synthetic** percentages; false alarms are listed for phi = 0.5/0.7/0.9.

| n/W | Textbook: false alarms | Fixed: detection | Fixed: false alarms | Calibrated T | Calibrated: detection | Calibrated: false alarms |
|---|---|---|---|---|---|---|
| 100/25 | 21.6/21.4/26.7 | 6.0 | 0.9/2.0/2.2 | 0.40 | 12.4 | 4.4/4.8/5.0 |
| 100/50 | 26.5/29.2/32.8 | 29.7 | 8.7/11.3/10.7 | 0.63 | 18.9 | 3.4/5.2/4.7 |
| 400/100 | 28.6/30.7/36.9 | 49.8 | 2.6/4.5/4.1 | 0.46 | 55.8 | 3.7/5.6/5.1 |
| 400/200 | 30.8/32.9/41.5 | 78.2 | 9.6/11.3/15.1 | 0.64 | 65.3 | 4.6/4.5/6.1 |
| 1,600/400 | 31.2/35.8/40.7 | 97.6 | 3.1/3.9/5.5 | 0.50 | 97.6 | 3.1/3.9/5.5 |
| 1,600/800 | 33.2/38.2/43.7 | 99.6 | 11.0/14.0/17.2 | 0.66 | 99.0 | 4.4/6.4/8.0 |

Four readings:

1. **The project question.** In the stationary controls both taus are positive in 334 to 461 of 1,000 runs, and the textbook test, nominally at most 5%, fires in 21.4% to 43.7%. Neighbouring windows share all but one point, so m rolling values are far from m independent observations.
2. **The threshold depends on the window.** T = 0.5 gives 0.9% to 5.5% false alarms with quarter windows and 8.7% to 17.2% with half windows.
3. **Near 5% false alarms, detection depends on record length.** The calibrated rule detects this approach in 12.4% to 18.9% of runs at 100 points, 55.8% to 65.3% at 400, and 97.6% to 99.0% at 1,600 (a longer record is here the same change in q spread over more steps: a slower approach).
4. **The calibrated threshold is an estimate.** On fresh runs at phi = 0.7 it fires in 3.9% to 6.4%, across the three controls in 3.1% to 8.0%; 1,000 runs do not separate its sampling error from a dependence on phi.

Two checks. A linear twin (an AR(1) whose coefficient follows the same path from 0.5 to 0.9, with no moving level and no fold) fires within 3.7 percentage points of the fold in every row and rule, so the detections come from the slowing down. Without the straight-line removal, detection by the fixed rule at n = 400, W = 200 falls from 78.2% to 3.3%.

### Practice Exercise 3

At n = 100, W = 50, the fixed rule fired in 297 of 1,000 approaching runs and in 113 of 1,000 stationary runs (phi = 0.7). Suppose 1 monitored system in 10 really approaches a fold. What share of alarms is true?

> **Answer:** P(alarm) = 0.1 × 0.297 + 0.9 × 0.113 = 0.1314; the true share is 0.0297 / 0.1314 = 0.226, about 23 alarms in 100.

### Practice Exercise 4

A colleague runs the textbook test on a 400-point record with W = 200, finds both indicators "significant at 5%" and concludes that chance is excluded. Classify the claim, and name the threshold you would require and its cost.

> **Answer:** Unsupported. On stationary series with phi = 0.7 this test fires in 32.9% of runs, not 5%: it assumes independent values while rolling windows overlap. Require a threshold calibrated on a stationary model fitted to that record. In the fixture's own setting that is M ≥ 0.64, which fired in 4.5% of independent control runs and detected 65.3% of approaches: about one real approach in three is missed.

## 4. What the recorded quality trend can and cannot show

**Observed.** The repository's pinned [quality trend](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) holds 1,548 rows: 18 governance artifacts measured in 88 runs on 83 days. [extract.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/extract.py) checks each source file against its Git blob and writes [observed-input.json](../../../fixtures/psychohistory/psy-012/observed-input.json). Each artifact has 81 to 87 measured runs of three numbers. **Computed** from that extract:

- `compliance_rate` and `violation_count`: all 18 series hold one value; 0 changes in 1,519 pairs of consecutive rows of one artifact ([PSY-005](psy-005-persistence-baseline.md) counts 1,518: one such pair starts at an unlabelled row).
- `citation_count`: 2 series are constant; the other 16 change, 20 times in 1,519 pairs, and all 20 changes fall on two runs (16 series on 2026-09-13, 4 on 2026-10-03).

This record can show persistence, the subject of [PSY-005](psy-005-persistence-baseline.md), and two dated steps; whether those steps are the instrument or the system is PSY-011's question.

It cannot show either early-warning signal. In a window whose values are all equal the variance is 0 and the autocorrelation is 0 / 0: undefined, not low. That is every window of two fields and 689 of the 1,105 windows of 25 runs for citation counts; elsewhere the only variation is a step. Critical slowing down concerns recovery from many small shocks, and a counter that registers no small shock carries no recovery speed. So the fixture computes no indicator on project data, and the missing trend is evidence neither that the governance system is far from a shift nor that it is near one. Even a fluctuating series of this length (81 to 87 points) would be short by the simulation's standard, and the simulated rates rest on an assumed approach and time scale that have no project counterpart.

### Practice Exercise 5

In observed-input.json, the citation counts of `policies/alignment-policy.yaml` are 3 for 55 runs, then 42 for 21 runs, then 44 for 11 runs. How many windows of 25 runs does this series have, and how many are constant? What are the two indicators in a constant window? Should you run the trend test? State your criterion.

> **Answer:** 87 − 25 + 1 = 63 windows. A window is constant only inside one segment; the 21-run and 11-run segments are shorter than 25, so only the first 55 runs qualify: 55 − 25 + 1 = 31 windows. The other 32 straddle a step. In a constant window the variance is 0 and the autocorrelation is 0 / 0, undefined. Do not run the test: the indicators need fluctuation inside every window, and here all the variation is two steps.

## Sources, limits, and next check

**Sources.** Observed: the pinned quality-trend folder; the fixture's [README](../../../fixtures/psychohistory/psy-012/README.md) gives the commands. Method references: Scheffer et al. (2009), "Early-warning signals for critical transitions", *Nature* 461, 53–59, [doi:10.1038/nature08227](https://doi.org/10.1038/nature08227); Dakos et al. (2012), "Methods for detecting early warnings of critical transitions in time series illustrated using simulated ecological data", *PLoS ONE* 7(7), e41010, [doi:10.1371/journal.pone.0041010](https://doi.org/10.1371/journal.pone.0041010); Boettiger and Hastings (2012), "Quantifying limits to detection of early warning for critical transitions", *Journal of the Royal Society Interface* 9, 2527–2539, [doi:10.1098/rsif.2012.0125](https://doi.org/10.1098/rsif.2012.0125); Boettiger and Hastings (2012), "Early warning signals and the prosecutor's fallacy", *Proceedings of the Royal Society B* 279, 4734–4739, [doi:10.1098/rspb.2012.2085](https://doi.org/10.1098/rspb.2012.2085).

**Limits.** One approach (phi from 0.5 to 0.9), one noise level, a level drifting in a straight line by design. The controls are stationary AR(1) only: changing noise, seasonality, an instrument change, or choosing cases after a shift happened (the prosecutor's fallacy) can each raise the indicators with no transition, so these rates describe the friendliest kind of "nothing approaching". The M rule and the within-window detrending are this fixture's simplifications, not a cited paper's procedure. No human review, learner trial, translation or publication of this lesson has taken place.

**Strongest objection.** The poor detection at 100 points may belong to this recipe, not to early warning as such: a model-based likelihood test of the kind Boettiger and Hastings argue for uses the data more efficiently, and a record ending nearer the fold carries a stronger signal. Running such a test, and a closer approach, on the same seeded series at equal false-alarm rates would settle it; that was not done.

**Next check.** A per-run quantity that changes in most consecutive pairs, recorded with an unchanged instrument for several hundred runs, would make it possible to calibrate such a rule for the project. Even then a silent rule would not exclude a transition: at 400 points it caught 55.8% to 65.3% of the simulated approaches.
