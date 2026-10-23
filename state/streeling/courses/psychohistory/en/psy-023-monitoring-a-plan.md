---
module_id: psy-023-monitoring-a-plan
department: psychohistory
course: "Monitoring a Plan: Tolerance Bands and Alarm Rules"
level: intermediate
prerequisites: ["psy-012-early-warning-false-alarms", "psy-004-how-large-is-large"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-023
version: "0.1.0"
---

# Monitoring a Plan: Tolerance Bands and Alarm Rules

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will count how often one look at a plan raises a false alarm, see why looking every week multiplies it, compare a fixed tolerance with Page's cumulative sum, and choose a threshold from costs before the data arrive. **Project question:** a long plan (25 courses in each of 21 departments) needs a rule for "we are off plan"; how often does a simple rule cry wolf, and how late does it notice a real slowdown?

The plan is a draft curriculum specification's figure, used as given and only for scale: the pinned repository does not state it. It holds [23 department records](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments), 21 of them with a course folder, and line 57 of its [README](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L57) reads "Streeling University — 23 departments, 21 course tracks", with no number of courses per track. No weekly output of the project was measured, so nothing here says whether the project is on or off its plan.

[PSY-012](psy-012-early-warning-false-alarms.md) calibrated an alarm for one look at a finished record; here the look is repeated every week, which is what inflates the false alarms. [PSY-010](psy-010-growth-curves-short-series.md) fits the growth history; this module assumes a schedule exists. Everything below is **synthetic**: assumptions in [scenarios.json](../../../fixtures/psychohistory/psy-023/scenarios.json), computed by [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-023/analyze.py), saved in [results.json](../../../fixtures/psychohistory/psy-023/results.json).

## 1. One look at the plan

The plan: 21 × 25 = 525 courses at 5 a week, so 105 weeks. Assume 10 drafts in work each week, each finished within the week with probability 1/2, independently. A week's output is then the number of heads among 10 fair coins: mean 5, variance 5/2, standard deviation 1.5811. The *shortfall* after t weeks is the planned total minus the actual total. On plan it has mean 0 and standard deviation `sqrt(5t/2)`: 8.0623 at week 26, 16.2019 at week 105.

Coins rather than normal noise make every probability an exact count over equally likely coin histories (2^10 = 1,024 per week); a seeded simulation of 20,000 runs then checks each exact figure, not the other way round.

Two rules can be checked at one week chosen in advance:

- A *weekly limit*: alarm when the week's output is at most 1. That happens in 1 + 10 = 11 of the 1,024 histories, 0.010742. Simulated first weeks: 215 of 20,000, 0.01075 (standard error 0.000729; exact 95% interval 0.009367 to 0.012278, as in [PSY-004](psy-004-how-large-is-large.md)).
- A *prediction band*: alarm when the shortfall is more than 2 standard deviations, `2 sqrt(5t/2)`.

### Practice Exercise 1

Check the band once, at week 26. Give the planned total, the band's width, the smallest whole shortfall that fires, and the actual total at or below which the alarm fires. The fixture counts a probability of 0.020247 for that look; why is it not the normal tail, 0.02275?

> **Answer:** Planned total `26 × 5 = 130`. Standard deviation `sqrt(26 × 5/2) = sqrt(65) = 8.0623`; two of them make 16.1245. The smallest whole shortfall above that is 17, so the alarm fires at a total of `130 − 17 = 113` or less. Output comes in whole courses, so the count (0.020247) is not the tail of a continuous normal variable (0.02275).

## 2. Looking every week

Checked every week, a weekly limit makes independent looks, with closed forms. For an alarm chance a per on-plan week:

```text
P(at least one alarm in T weeks) = 1 - (1 - a)^T
average run length               = 1 / a
```

The *average run length* (ARL) is the average number of weeks until the first alarm; section 6.3.2.3.1 of the NIST/SEMATECH handbook defines it as "the average number of samples (subgroups) taken before an action signal is given". For the limit 1, a = 11/1024 and the ARL is 93.09 weeks, shorter than the plan: the rule fires at least once in 0.678266 of on-plan plans. The fixture's recursion reproduces the formula exactly; the simulation gives 13,552 of 20,000, 0.6776 (standard error 0.003305).

The band checked every week makes dependent looks (week 27's shortfall is week 26's plus one week), so the product formula fails, and the probability that the shortfall crosses the band at least once in a horizon has no simple closed form. The recursion computes it exactly, week by week, from the histories not yet crossed. For the 2-standard-deviation band no single look exceeds 0.028332, yet the band fires at least once in 0.170761 of on-plan plans by week 105, 6.03 times the largest single look. The simulation: 3,380 of 20,000, 0.169 (standard error 0.00265). The sum of the 105 single looks, 2.359684, is a valid upper bound and a useless one.

### Practice Exercise 2

For the weekly limit "output at most 1": (a) give the ARL and the probability of at least one alarm by week 52; (b) using the bound `P(at least one alarm) ≤ T × a`, find the per-week chance that would hold the whole plan to 5%. Can any weekly limit achieve it?

> **Answer:** (a) `1024 / 11 = 93.09` weeks; `1 − (1 − 11/1024)^52 = 0.429713`. (b) `0.05 / 105 = 0.000476` (solving `1 − (1 − a)^105 = 0.05` exactly gives 0.000488). The strictest limit, an empty week, has `1/1024 = 0.000977`, about twice too much: no weekly limit is quiet enough. That limit still fires in 0.097502 of on-plan plans.

## 3. A tolerance and Page's cumulative sum

Two rules watch the accumulated shortfall. The *tolerance* fires when the shortfall reaches c courses. Page's *cumulative sum* (Page, 1954) scores each week as its shortfall minus a *reference value* k, and fires when the sum of the scores is at least the *decision interval* h above its lowest earlier value, counting the starting value 0. The handbook's statement: "If the distance between a plotted point and the lowest previous point is equal to or greater than h, one concludes that the process mean has shifted (increased)". The recursion below is equivalent; the two forms agree in every simulated run.

```text
tolerance:       S(t) = S(t-1) + 5 - output(t);              alarm when S(t) >= c
cumulative sum:  C(t) = max(0, C(t-1) + 5 - output(t) - k);  alarm when C(t) >= h
```

Here k = 1, half the 2 courses a week lost by the assumed slowdown: from week 53, 6 drafts in work, mean 3 courses, 60% of the plan. A rule is *calibrated* at the smallest whole threshold whose exact on-plan probability of an alarm within 105 weeks is at most 5%: c = 32 (31 gives 0.052439) and h = 8 (7 gives 0.084257). The *delay* is the number of slow weeks seen when the alarm comes, among plans still silent at week 52 (runs continue past week 105).

| Rule | On-plan alarm, exact | Simulated ± SE [exact 95% interval] | Mean delay, exact (simulated ± SE) | 90% of delays within |
|---|---|---|---|---|
| Tolerance 32, calibrated | 0.045372 | 0.0458 ± 0.001478 [0.042944, 0.048789] | 16.5 (16.56 ± 0.04) | 25 |
| Tolerance 40 | 0.012603 | 0.01185 ± 0.000765 [0.010397, 0.013448] | 20.44 (20.5 ± 0.04) | 29 |
| Cumulative sum 6 | 0.185318 | 0.18365 ± 0.002738 [0.178305, 0.189087] | 5.88 (5.87 ± 0.02) | 10 |
| Cumulative sum 8, calibrated | 0.037333 | 0.03655 ± 0.001327 [0.033992, 0.039244] | 7.85 (7.85 ± 0.02) | 12 |
| Cumulative sum 10 | 0.007136 | 0.0064 ± 0.000564 [0.005342, 0.007605] | 9.83 (9.82 ± 0.03) | 15 |

Within each rule, a quieter threshold means a later alarm: no threshold is free. At comparable false-alarm levels the cumulative sum flags the slowdown after 7.85 weeks on average against 16.5, a ratio of 0.4754; its ARL is 2,623.4 weeks on plan and 8.3 after a slowdown from zero. The tolerance is slower because it banks every surplus: a plan running ahead must first lose its lead. A week on plan scores −1 in the cumulative sum, so C drifts back to zero and forgets the past. One of 28 simulated 95% intervals misses its exact value (decision interval 9, 2.97 standard errors below), about one in twenty, as expected.

### Practice Exercise 3

An invented record of 12 weeks: 7, 6, 6, 5, 3, 4, 2, 3, 4, 2, 3, 3; the slowdown began in week 5. Compute S and C (k = 1) each week. Which calibrated rule fires, and when?

> **Answer:** Weekly shortfalls −2, −1, −1, 0, 2, 1, 3, 2, 1, 3, 2, 2. S: −2, −3, −4, −4, −2, −1, 2, 4, 5, 8, 10, 12: the tolerance (32) stays silent, 20 courses short, about `20 / 2 = 10` slow weeks more. Scores −3, −2, −2, −1, 1, 0, 2, 1, 0, 2, 1, 1, so C: 0, 0, 0, 0, 1, 1, 3, 4, 4, 6, 7, 8. The cumulative sum fires in week 12, the 8th slow week. The tolerance still carries the 4-course lead of weeks 1 to 4; the cumulative sum discarded it.

## 4. Choose the threshold from costs, and fix it before looking

A threshold chosen after reading the record has no known false-alarm rate: the record chose it.

### Practice Exercise 4

A colleague who reads the record every week sees at week 61 a shortfall of 25 courses, where the 2-standard-deviation band fires from 25. They report: "on plan, a shortfall this large at week 61 has a chance of 0.023586; the plan is off." Classify the claim and name the rule you would use instead.

> **Answer:** Unsupported. 0.023586 is the chance of one look at a week chosen in advance. The colleague would have reported any week at which the band was crossed, and that procedure fires in 0.170761 of on-plan plans within 105 weeks. Fix a rule before looking, calibrated on the whole plan: the tolerance 32 or the cumulative sum 8, each at most 5%.

The 5% target is itself a convention, not a cost. With assumed costs (a slowdown from week 53 with probability q = 1/2, each slow week before the alarm costing 2 courses, each false alarm costing F courses of review):

```text
expected cost = (1 - q) × P(false alarm) × F + q × mean delay × 2
```

For F = 20 the cheapest decision interval is 7 (7.7 courses); for F = 100 it is 9 (9.66). The calibrated 8 is the cheapest under neither.

### Practice Exercise 5

With q = 1/2, 2 courses per slow week and F = 20, compute from the table the expected cost of the decision intervals 6 and 8, and the false-alarm cost at which they tie.

> **Answer:** h = 6: `0.5 × 0.185318 × 20 + 0.5 × 5.88 × 2 = 1.85 + 5.88 = 7.73`. h = 8: `0.5 × 0.037333 × 20 + 0.5 × 7.85 × 2 = 0.37 + 7.85 = 8.22`. They tie when `0.5 × F × (0.185318 − 0.037333) = 7.85 − 5.88`, so `F = 1.97 / 0.0739925 = 26.62` from the table's rounded figures (26.55 from the exact ones). Below the tie h = 6 is cheaper; above it, h = 8.

**The strongest objection** is that every threshold belongs to its output model. PSY-010 found modules added in bursts, and [PSY-008](psy-008-bursts-are-not-rates.md) shows how a mean rate misleads for bursty arrivals. Keep the mean of 5 a week but deliver it in batches: 40 drafts in work one week in four, none otherwise. The weekly variance becomes 155/2, 31 times the steady one. The calibrated tolerance 32 then fires in 0.704574 of on-plan plans (simulated 0.7046 ± 0.003226), and the cumulative sum 8 in 1.000000 of them to six decimals (20,000 of 20,000 simulated, interval 0.999816 to 1). The tuning of k cuts too: for a milder slowdown (8 drafts, 80% of the plan) a slow week scores 0 on average, and the cumulative sum's mean delay, 41.45 weeks, exceeds the tolerance's 32.78; 0.261752 and 0.076485 of the plans still silent at week 52, respectively, are still unflagged when the plan ends. **This model cannot say which rule suits the project**: that needs the project's weekly output and a decision about which slowdown is worth detecting.

## Sources, limits, and next check

**Pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the README line and the department records cited above, for scale; no data file was read.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py`, then the same with `--check`, which compares a fresh run with the saved results. The [README](../../../fixtures/psychohistory/psy-023/README.md) lists the 24 self-checks, among them a case worked by hand and a negative control.

**Method references.** Page, E. S. (1954), "Continuous Inspection Schemes", *Biometrika* 41(1–2), 100–115, doi:10.1093/biomet/41.1-2.100. NIST/SEMATECH *e-Handbook of Statistical Methods*, section [6.3.2.3.1](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3231.htm), the source of both quotations, and section [6.3.2.3](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) on cumulative-sum charts. Brook, D., and Evans, D. A. (1972), "An approach to the probability distribution of cusum run length", *Biometrika* 59(3), 539–549, doi:10.1093/biomet/59.3.539 (the Markov-chain idea behind the fixture's recursion). Armitage, P., McPherson, C. K., and Rowe, B. C. (1969), "Repeated Significance Tests on Accumulating Data", *Journal of the Royal Statistical Society, Series A* 132(2), 235–244, doi:10.2307/2343787 (why repeated looks inflate an error rate).

**Not done.** No weekly output of the project was read. Page's 1954 article was not opened; his rule is stated as the handbook gives it. Only one-sided rules and one abrupt, permanent slowdown were studied; not two-sided rules, gradual drifts or estimating a slowdown's size. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Once a schedule exists, extract the project's weekly output (PSY-010's dated module additions are a start), estimate its variance and share of empty weeks, and recalibrate both rules on that dispersion. If output is bursty, the thresholds above would fire in most on-plan plans.
