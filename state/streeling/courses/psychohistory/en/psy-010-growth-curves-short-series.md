---
module_id: psy-010-growth-curves-short-series
department: psychohistory
course: "Exponential, Logistic or Steps? Fitting Growth to a Short History"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-010
version: "0.1.0"
---

# Exponential, Logistic or Steps? Fitting Growth to a Short History

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will turn a commit history into a daily series, fit three growth curves to it by least squares, read from each the date of a target, and test whether the data can tell them apart. **Project question:** English course modules were added in bursts. What do exponential, logistic and linear fits to the cumulative count each predict for reaching 525, and can the history tell them apart?

[PSY-001](psy-001-intro-fractal-compounding.md) pictures healthy growth as compound interest. If the library compounded, its count would be exponential; here that is one candidate among three. [PSY-022](psy-022-competing-explanations.md) compares models with likelihood criteria, [PSY-018](psy-018-backtesting-without-leakage.md) tests forecasts on held-out data, and [PSY-023](psy-023-monitoring-a-plan.md) monitors a plan once a schedule exists.

## 1. Turn the history into a series

**Observed.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/extract.py) asks git which of the 1,599 commits reachable from commit `4b03838` changed the folder [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses): 73 commits, from 2026-03-21 to 2026-10-13. It writes [`observed-input.json`](../../../fixtures/psychohistory/psy-010/observed-input.json) from commit dates and file names alone. A *module* is a path `DEPARTMENT/en/NAME.md`. Translations (181 files at the pin), README files (4, and 2 more inside `en/` folders) and the 10 file names of an early layout without language folders are not counted. Together the commits add 73 module paths and remove 5 (a rename counts as a removal and an addition): **68** modules at the pin, in 18 of 21 department folders.

**Assumed.** The curriculum plan foresees 21 departments with 25 courses each, 21 × 25 = **525**, a draft specification's figure, used as given although the repository records 23 departments, two without a course folder. 68 is 13.0% of 525.

Each commit is dated by its committer date in UTC; commits that share a second keep their ancestry order. The series is the count at the end of each UTC day, day 0 being 2026-03-21: 207 days. **Computed:** the count changes on 12 of them.

```text
day     0   1   2   3  15  190  191  195  196  197  200  206
count  13  17  19  23  31   32   37   60   63   66   67   68
```

Call those 12 days *active*, and call a run of active days at most 7 days apart a *burst* (a convention, stored in [`scenarios.json`](../../../fixtures/psychohistory/psy-010/scenarios.json); [PSY-008](psy-008-bursts-are-not-rates.md) calls such a group an *episode*):

| Burst | Days | Modules added | Share of the 68 |
|---|---|---|---|
| 21 to 24 March | 4 | 23 | 33.8% |
| 5 April | 1 | 8 | 11.8% |
| 27 September to 13 October, still open | 17 | 37 | 54.4% |

The third burst is still open: the pin itself added a module, so under the 7-day rule its 37 modules and 17 days are lower bounds, and the modules of this lesson's batch extend it if they are merged by 2026-10-20. For 174 days, from 6 April to 26 September, the count stayed at 31. A 3-day rule gives 5 bursts and a 12-day rule 2: "burst" is a choice. So is the clock: five other time zones give 10 to 13 active days, still in three bursts.

### Practice Exercise 1

What share of the 68 modules arrived in the last burst, and in what share of the 207 days? On how many days did the count not change?

> **Answer:** `37 / 68 = 54.4%` of the modules in `17 / 207 = 8.2%` of the days. `207 − 12 = 195` days without change, 94.2%. More than half of the growth sits in the last 17 days: any curve fitted here depends heavily on one recent event.

## 2. Fit three growth laws

Three candidate laws for the count N on day t:

```text
line         N = a + b t                      the same number of modules every day
exponential  N = a exp(b t)                   additions proportional to the count: compounding
logistic     N = K / (1 + exp(-r (t - m)))    compounding that slows as N nears a ceiling K

line fit     b = (n ΣtN - Σt ΣN) / (n Σt² - (Σt)²)      sums over the n days
             a = (ΣN - b Σt) / n
```

*Least squares* chooses the parameters that minimise SSE, the sum over the 207 days of (observed − fitted)². RMSE, the square root of SSE / 207, is the typical miss in modules. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/analyze.py) solves the line exactly from those sums and finds the two curves by a deterministic search (a grid, then Newton steps). The logistic ceiling is fixed at K = 525, and m is the day the curve passes K / 2. A logistic curve only approaches its ceiling, so "reaches 525" means, for every curve, the first day its value is at least 524.5.

**Computed** ([`results.json`](../../../fixtures/psychohistory/psy-010/results.json), `fits.pinned_date`):

| Curve | Parameters (t in days) | SSE | RMSE | Value on day 206 | Reaches 525 | Years after the pin |
|---|---|---|---|---|---|---|
| Line | a = 24.5641, b = 0.0767431 | 11,462.4 | 7.441 | 40.37 | 2044-01-21 | 17.3 |
| Exponential | a = 24.6004, b = 0.00257104 | 11,100.5 | 7.323 | 41.78 | 2029-06-24 | 2.7 |
| Logistic | r = 0.00272281, m = 1,106.31 | 11,130.8 | 7.333 | 41.65 | 2036-03-29 | 9.5 |

The three dates span 14.6 years. Each curve puts between 40 and 42 modules on a day when the repository held 68.

### Practice Exercise 2

From the parameters, compute the day on which the line and the exponential reach 524.5, then the years after the pin (day 206, 365.25 days per year).

> **Answer:** Line: `(524.5 − 24.5641) / 0.0767431 = 6,514.4`, so day 6,515, which is `6,515 − 206 = 6,309` days or 17.3 years after the pin. Exponential: `ln(524.5 / 24.6004) / 0.00257104 = 1,190.1`, so day 1,191: 985 days, 2.7 years.

### Practice Exercise 3

How long after its midpoint m does the logistic reach 524.5? What does the result say about the question "when do we reach 525"?

> **Answer:** N = 524.5 when `exp(−r (t − m)) = 0.5 / 524.5`, so `t − m = ln(1,049) / r = 6.95559 / 0.00272281 = 2,554.6` days, 7.0 years. The curve passes 262.5 on day 1,107, 2.5 years after the pin, and needs 7.0 more years for the second half. It never equals 525: under this law the question has an answer only with a convention such as the half-module margin.

## 3. Can the history tell them apart?

Four **computed** checks.

*The residual sums are nearly equal.* The largest SSE is 1.033 times the smallest.

*The three curves miss in the same way.* A *residual* is observed minus fitted. Along the 207 days each curve's residuals change sign 3 times, and the longest run on one side lasts 105 to 111 days. Least squares is at its best when the misses are independent noise: a **synthetic** line plus such noise, fitted by a line, changes sign 107 times. These residuals are not noise: they are the staircase.

*In sample, a staircase with no growth law fits far better.* Two flat levels, 30.41 before 2 October and 65.92 from that day on, leave an SSE of 1,564.1: 7.1 times less than the best curve, with 3 parameters against 2. With 11 change points the SSE is 0. A staircase says nothing about the next step. How to weigh fit against the number of parameters is the subject of PSY-022.

*No ceiling can be estimated.* With K fixed at 12 values from 69 to 100,000, the logistic's SSE falls at every step, from 11,469.8 to 11,100.7, towards the exponential's 11,100.5. A ceiling one module above the present count and a ceiling of 100,000 differ by 3.3%: K is not *identifiable* from these data. The method is not at fault: on a synthetic logistic seen past its turn, the same profile recovers the planted ceiling of 525 (SSE 8,751.7, against 29,596.0 at 550); seen before its turn, it is flat within 0.4%. This history has not reached a turn, if there is one.

### Practice Exercise 4

A colleague writes: "The exponential has the lowest SSE, so the library compounds and we reach 525 in 2029." Accept or reject, and state your criterion.

> **Answer:** Reject as unsupported. A ranking counts only when the gap between candidates is large next to what all of them miss. Here `11,462.4 / 11,100.5 = 1.033`, while a two-level staircase does `11,100.5 / 1,564.1 = 7.1` times better and all three curves leave the same 3 sign changes. This sample cannot distinguish the three laws; compounding remains a candidate, not a finding.

## 4. Move the cut-off, then count bursts

A fit that had captured the law would give dates that stop moving as the history grows. **Computed:** the same fits on the history at the end of the second burst, on the eve of the third, and at the pin.

| History up to | Days | Count | Line | Exponential | Logistic |
|---|---|---|---|---|---|
| 5 April | 16 | 31 | 2028-08-16 | 2026-08-02 | 2027-04-16 |
| 26 September | 190 | 31 | 2088-12-21 | 2037-10-26 | 2062-12-02 |
| 13 October | 207 | 68 | 2044-01-21 | 2029-06-24 | 2036-03-29 |

Between the first two rows, 174 quiet days pushed the dates back by 60.3, 11.2 and 35.6 years. The last burst then pulled them forward by 44.9, 8.3 and 26.7 years. For 13 October the April fits predicted 136.68, 3,267.78 and 467.68 modules, the September fits 32.68, 32.66 and 32.66; the count was 68. Here a curve fitted to a staircase extrapolates whichever it saw last, a riser or a tread.

Other defensible choices move the dates again: fitting only the 12 active days gives 2033-07-08, 2027-11-09 and 2030-12-15; a line fitted to the logarithm of the counts (a spreadsheet's exponential trendline) gives 2030-04-27; dating one commit by its author date, 1.3 days earlier, moves the line's date by 81 days.

**Synthetic.** Projecting the step reading requires assuming that the future repeats the past: 457 modules remain, the bursts added 23, 8 and at least 37, and they started 15 and 175 days apart.

### Practice Exercise 5

Under that assumption, how many bursts are needed and how long do they take (a) with the mean size and the mean interval, (b) with the largest size, at least 37, and the shortest interval, (c) with the smallest size and the longest interval?

> **Answer:** (a) Mean size `68 / 3 = 22.67`; `457 / 22.67 = 20.16`, so 21 bursts; mean interval `(15 + 175) / 2 = 95` days; `21 × 95 = 1,995` days, 5.5 years. (b) `457 / 37 = 12.35`, so 13 bursts; `13 × 15 = 195` days, 0.5 years. (c) `457 / 8 = 57.125`, so 58 bursts; `58 × 175 = 10,150` days, 27.8 years. The open burst makes (a) and (b) upper bounds. Three bursts give a range from 0.5 to 27.8 years: arithmetic on an assumption, not a forecast.

**The strongest objection to this reading** is that the contest between curves is beside the point. On 2 October the count rose by 23 in 23 one-module commits, 14 of them within two minutes: the pattern of a production batch. If modules arrive when someone decides to run a batch, the series records decisions, not a growth law, and "cannot tell the curves apart" is true and uninformative. Two things would settle it: a written production schedule, which turns the date into a plan to monitor (PSY-023); or several more bursts under the same 7-day rule, enough to see whether the modules added per unit of time grow with the count (larger or more frequent bursts: compounding), stay level (linear) or fall (a ceiling).

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the commit history of `state/streeling/courses` and the department records at the pin (commits and trees only). `extract.py` refuses a shallow clone or any history but the pinned one. 525 is the plan's figure.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py`, then `analyze.py` in the same folder; `analyze.py --check` compares a fresh run with the saved results. The [README](../../../fixtures/psychohistory/psy-010/README.md) documents the method and its checks.

**Method references.** Bates, D. M., and Watts, D. G. (1988), *Nonlinear Regression Analysis and Its Applications*, Wiley (least squares for curves; Gauss–Newton steps). Debecker, A., and Modis, T. (1994), "Determination of the uncertainties in S-curve logistic fits", *Technological Forecasting and Social Change* 46(2), 153–173 (how uncertain a fitted ceiling is before the curve turns). Meade, N., and Islam, T. (1995), "Forecasting with growth curves: An empirical comparison", *International Journal of Forecasting* 11(2), 199–215.

**Not done.** No interval was put on any date, and no likelihood, AIC or BIC was computed (PSY-022). The modules' content, quality and review status were not read: a module here is a file name. Every day weighs equally; no other weighting was justified. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Rerun `extract.py` after replacing its pinned constants with a later pin, once at least five new bursts have closed, with the 7-day rule and the three cut-off fits fixed as they are now. If the new bursts stay inside the observed ranges (8 to at least 37 modules, starts 15 to 175 days apart), the step reading is not contradicted; if the modules added per unit of time rise with the count, compounding gains its first support.
