---
module_id: psy-014-prediction-horizons
department: psychohistory
course: "Prediction Horizons: How Fast Small Errors Grow"
level: intermediate
prerequisites: ["mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-014
version: "0.1.0"
---

# Prediction Horizons: How Fast Small Errors Grow

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will run a model twice from almost the same start, measure how the difference between the runs changes, summarise it as a Lyapunov exponent, and turn that into a *prediction horizon*: the number of steps for which a forecast stays within a stated tolerance. **Project question:** how far ahead can a deterministic model be trusted when its starting state is known only approximately?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) says that psychohistory can "predict the broad strokes" but not individual events, and [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) that individual changes are unpredictable while aggregate behaviour follows statistical laws. Neither says how far ahead a forecast holds, or what better knowledge of the present buys: this module answers both for a small model, with the exponent of section 2 of [MAT-024](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-024-dynamical-systems-stability-feedback.md). Early-warning signals belong to [PSY-012](psy-012-early-warning-false-alarms.md), alarm rules to PSY-023. Every result below is **synthetic**: it describes the model, not the project.

## 1. Run the model twice

A *deterministic* model contains no randomness: the same start always gives the same run. The standard small example is the *logistic map* (May 1976), which updates a state x between 0 and 1 by

```text
x_next = r * x * (1 - x)
```

where r is a fixed setting. After a transient the state stays on an *attractor*: one fixed point at r = 2.9, a cycle of two points at r = 3.2, an irregular band at r = 3.7 and at r = 4. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-014/analyze.py) draws 1,000 seeded starting points ([`scenarios.json`](../../../fixtures/psychohistory/psy-014/scenarios.json)), lets each settle for 1,000 steps, then runs it twice: once as it is, once moved by an *initial error* of 1e-9. The *gap* is the absolute difference between the two runs at the same step.

**Synthetic.** Median gap of the 1,000 pairs, from `gap_table` in [`results.json`](../../../fixtures/psychohistory/psy-014/results.json):

| Step | r = 2.9 | r = 3.2 | r = 3.7 | r = 4 |
|---|---|---|---|---|
| 0 | 1e-9 | 1e-9 | 1e-9 | 1e-9 |
| 10 | 3.49e-10 | 1.05e-13 | 4.85e-8 | 1.04e-6 |
| 20 | 1.22e-10 | 0 | 1.72e-6 | 0.00107 |
| 30 | 4.24e-11 | 0 | 6.14e-5 | 0.537 |
| 60 | 1.8e-12 | 0 | 0.173 | 0.36 |

A `0` means a gap too small for the program's 64-bit numbers (section 3), not a zero gap: recomputed with 1,024-bit numbers, the median at r = 3.2 is 1.1e-17 at step 20.

In the first two columns the error shrinks. These *stable regimes* forget their start: the 1,000 settled starts have collapsed onto the attractor, the two points of the cycle at r = 3.2 and, at r = 2.9, the fixed point, held by rounding as two numbers 6.66e-16 apart. So these 1,000 pairs repeat two experiments. In the *chaotic regimes* of the last two columns the gap grows by a roughly constant factor per step: *sensitive dependence on initial conditions*. Then it stops: a gap cannot exceed the size of the attractor.

### Practice Exercise 1

At r = 2.9 a small error is multiplied by 0.9 at each step. Check this against the table over ten steps, then compute how many steps bring an error of 1e-3 below 1e-6.

> **Answer:** `0.9^10 = 0.3487`, and the table gives `3.49e-10 / 1e-9 = 0.349`. An error falls by a factor of 1,000 in `ln(1e-6 / 1e-3) / ln(0.9) = −6.9078 / −0.105361 = 65.56` steps, so 66 steps; the fixture counts 66 in both experiments. Here a forecast improves with time, provided the starting error is small.

## 2. The rate: a Lyapunov exponent

While a gap is small, one step multiplies it by the size of the map's slope at the current state, |r (1 − 2x)|. The *Lyapunov exponent* λ is the average of the logarithm of that factor along a long run:

```text
λ = average of ln|r * (1 - 2 * x)| along the run
gap after n steps ≈ initial error * e^(λ * n)      while the gap stays small
```

A negative λ means that errors shrink; a positive one, that they grow by a factor e^λ per step on average. **Synthetic**, from 1,000,000 steps per setting:

| r | λ estimated | λ known | e^λ |
|---|---|---|---|
| 2.9 | −0.105361 | ln 0.9 = −0.105361 | 0.9 |
| 3.2 | −0.916291 | ln 0.4 = −0.916291 | 0.4 |
| 3.7 | 0.3547 ± 0.0003 | no closed form | 1.426 |
| 4 | 0.693144 | ln 2 = 0.693147 | 2 |

At r = 3.7 there is only the estimate; its standard error comes from 100 blocks of 10,000 steps. MAT-024 prints 0.350235 from 10,000 steps: the first block of this run, reproduced to six decimals.

The exponent is an average: at r = 3.2 the slope has size 1.9165 at one point of the cycle and 0.0835 at the other, and their product is 0.16 = 0.4².

### Practice Exercise 2

Estimate λ from two entries of the gap table: for r = 4 from steps 0 and 20, for r = 3.2 from steps 0 and 10. Why is step 30 unusable for r = 4?

> **Answer:** r = 4: `ln(0.00107 / 1e-9) / 20 = 13.8832 / 20 = 0.6942`, against ln 2 = 0.6931. r = 3.2: `ln(1.05e-13 / 1e-9) / 10 = −9.1616 / 10 = −0.9162`, against −0.9163. At step 30 the median gap is 0.537: growth has stopped at the size of the attractor.

## 3. The horizon, and the price of a digit

Call *tolerance* the largest gap that the user of a forecast accepts, and *horizon* the first step at which the gap reaches it. Setting the gap equal to the tolerance in the growth law gives

```text
horizon ≈ ln(tolerance / initial error) / λ
steps gained per extra decimal digit of precision = ln(10) / λ
```

**Synthetic.** Mean horizon of the 1,000 pairs for a tolerance of 0.1, next to the formula:

| Initial error | r = 3.7: mean | formula | r = 4: mean | formula |
|---|---|---|---|---|
| 1e-3 | 12.93 | 12.98 | 6.79 | 6.64 |
| 1e-6 | 32.56 | 32.46 | 16.78 | 16.61 |
| 1e-9 | 51.54 | 51.93 | 26.78 | 26.58 |
| 1e-12 | 71.05 | 71.41 | 36.69 | 36.54 |

From 1e-3 to 1e-12, nine more digits, the mean horizon gains 58.12 steps at r = 3.7 and 29.9 at r = 4: 6.46 and 3.32 steps per digit, against 6.49 and 3.32 from the formula. **In a chaotic regime each digit of precision buys the same small number of steps.** The thresholds written into the research cycle's hypothesis before the first run all held: slope within 10% of the formula's, offset at most 5 steps and varying by less than 2 (measured: −0.39 to 0.22 steps).

Where λ is negative there is no horizon: at r = 2.9 and r = 3.2, none of the 20,000 combinations of pair, error and tolerance reached a tolerance (40 distinct combinations each: the settled starts are 2 numbers). A detector that never fires would give the same zero: as a control, a run started on the other point of the two-cycle, 0.286 away, is flagged at step 1 and stays 0.286 away. "No horizon" holds for small errors only.

The arithmetic sets its own horizon. A *double*, Python's 64-bit number format, carries 15.95 decimal digits: between 0.5 and 1, neighbouring values are 2^-53 ≈ 1.11e-16 apart. Rounding acts like an initial error: against a run from the same start with 1,024-bit numbers, a double run is 0.1 away after 53.27 steps on average at r = 4 and 99.55 at r = 3.7; beyond that it is no longer the map's orbit from its start. The horizons above still belong to the map: with those numbers, 3 of 10,000 horizons (ten initial errors) change at r = 3.7 and 1 of 10,000 at r = 4, by at most 2 steps.

### Practice Exercise 3

At r = 3.7, take λ = 0.355 and a tolerance of 0.1. Compute the horizon for an initial error of 1e-6, then what improving the error to 1e-9 buys.

> **Answer:** `ln(0.1 / 1e-6) / 0.355 = 11.5129 / 0.355 = 32.43` steps (measured mean 32.56). Each digit is worth `ln(10) / 0.355 = 6.49` steps, so three digits buy 19.46 steps and the horizon becomes 51.89. A measurement 1,000 times more precise extends the horizon by `19.46 / 32.43 = 0.60`, or 60%.

### Practice Exercise 4

At r = 4, which initial error would keep a forecast within 0.1 for 100 steps? Can a double provide it?

> **Answer:** `0.1 × e^(−0.693147 × 100) = 0.1 × 2^−100 = 7.89e-32`, which needs 31.1 decimal digits. A double has 15.95, so no. With one spacing of doubles as the initial error the formula gives `ln(0.1 / 1.11e-16) / 0.693147 = 49.68` steps, close to the 53.27 measured.

## 4. Beyond the horizon, and what a plan can use

Past the horizon the state is lost, but not everything is. **Synthetic:** two runs at r = 4 from 0.3 and 0.3 + 1e-12 are 0.1 apart at step 37, in doubles and in 1,024-bit numbers alike. At step 100 the two computed runs hold 0.673899 and 0.002785, numbers that already depend on rounding: from the same starts the 1,024-bit runs give 0.991939 and 0.735222. Yet over 100,000 steps the first computed run spends 33,353 steps below 0.25 and the second 33,525, against a known share of 1/3. The statistics of the attractor stay predictable when the state is not: the model-sized version of PSY-002's claim about aggregates.

### Practice Exercise 5

A forecast at r = 4 must stay within 0.1 at each of 60 steps. Option A: measure the start once, to 1e-12 instead of 1e-6. Option B: keep 1e-6 and measure again every k steps. Of 1,000 such forecasts, 972 stay within tolerance at all 60 steps for k = 10, 960 for 11, 924 for 12 and 284 for 16. Which option, and which longest k, keeps at least 95% of the 60-step forecasts within tolerance?

> **Answer:** A fails: the formula horizon at 1e-12 is 36.54 steps and the longest of the 1,000 measured horizons is 49. B works up to k = 11, that is 6 measurements: `960 / 1,000 = 96.0%`, against 92.4% for k = 12. Choosing k = 16, the formula horizon 16.61 rounded down, keeps only 28.4%: a horizon is a distribution, here from 9 to 24 steps around a mean of 16.78. The criterion is its low end, and the remedy is to measure again, not to measure better.

**Analogy, not a measurement.** A roadmap is a long forecast from an approximately known present. If the process behind it amplifies small differences, more detail about today buys a fixed, small extension; measuring again and forecasting distributions are what help. If it damps them, long forecasts are cheap. Nobody has measured a Lyapunov exponent for this project: this lesson cannot say which case applies.

**The strongest objection** is that the logistic map is one number under a fixed rule. A project has many variables, people who react to forecasts, and outside shocks; with shocks, errors grow even from a perfectly known start, and this horizon formula need not hold. A project series scored in [PSY-005](psy-005-persistence-baseline.md) does not settle it: "nothing changes" was right for 1,528 of 1,529 pairs of consecutive rows (unevenly spaced), which shows labels that rarely change, or a record that nobody revises, not how forecast errors grow. **This fixture cannot distinguish a chaotic, a noisy and a stable project.** Dated forecasts of one project quantity, scored by lead time, could begin to: error that grows exponentially and then levels off indicates a positive exponent; error that stays flat, a stable regime; error present from the first step that grows without an exponential phase, a noisy one.

## Sources, limits, and next check

**Pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** PSY-001, PSY-002 and MAT-024. The fixture reproduces the four exponents that MAT-024 prints for these settings; the count of row pairs in section 4 is PSY-005's.

**Fixture.** From the repository root, `python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py`, then the same with `--check`. It reads only `scenarios.json` and runs 41 self-checks; its [README](../../../fixtures/psychohistory/psy-014/README.md) explains why the output is byte-identical across platforms and lists the limits.

**Method references.** May, R. M. (1976), "Simple mathematical models with very complicated dynamics", *Nature* 261, 459–467. Lorenz, E. N. (1963), "Deterministic nonperiodic flow", *Journal of the Atmospheric Sciences* 20, 130–141 (sensitive dependence on initial conditions). Strogatz, S. H. (2015), *Nonlinear Dynamics and Chaos*, 2nd edition, Westview Press (Lyapunov exponents and the time horizon of a prediction).

**Not done.** No project data was analysed and no exponent was estimated for any project quantity. One map with one variable, no noise and one seed was studied. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Archive a dated forecast of one project quantity at each run, such as the module count of [PSY-010](psy-010-growth-curves-short-series.md), and plot error against lead time once enough forecasts have resolved. Exponential growth followed by a plateau would be a first indication of a positive exponent, not yet an estimate; a flat curve would say that the horizon is not what limits the plan.
