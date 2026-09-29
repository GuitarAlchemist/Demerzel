---
module_id: mat-009-estimation-uncertainty-sampling
department: mathematics
course: Estimation, Uncertainty and Reproducible Sampling
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Estimation, Uncertainty and Reproducible Sampling — What a Number From Data Can Claim

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Define the bias, variance and mean squared error of an estimator, and show why the sample variance divides by n − 1
- Say what a confidence interval and a p-value claim, and what they do not
- Choose between Welch's t-test, the Mann–Whitney test and the Kolmogorov–Smirnov test, and compute an exact small-sample p-value by counting
- Estimate error on new data by k-fold cross-validation, and say why the spread of the fold scores can understate its uncertainty
- Treat the seed, the generator and its version as part of an experiment's specification, and say what IX's sampling, cross-validation and test functions guarantee

---

## 1. Estimators, Bias and Variance

An **estimator** is a rule that turns a sample X₁, …, Xₙ into a guess θ̂ of an unknown quantity θ. The sample is random, so θ̂ is a random variable, and two numbers describe how good it is: its **bias** E[θ̂] − θ and its **variance** Var(θ̂). Together they give the **mean squared error**, E[(θ̂ − θ)²] = bias² + variance; expanding (θ̂ − E[θ̂] + E[θ̂] − θ)² shows it, since the cross term has expectation 0.

For independent draws with mean μ and variance σ², the **sample mean** X̄ = (X₁ + … + Xₙ)/n is unbiased, and Var(X̄) = σ²/n, since the variances of independent terms add. Its standard deviation σ/√n is the **standard error**: halving it takes four times as much data.

The variance is subtler. The deviations Xᵢ − X̄ are measured from X̄, which is fitted to the same data, so they are smaller on average than the deviations from μ: Σ(Xᵢ − X̄)² = Σ(Xᵢ − μ)² − n (X̄ − μ)², whose expectation is n σ² − n · σ²/n = (n − 1) σ². Dividing by n therefore underestimates σ² by the factor (n − 1)/n, and dividing by n − 1, **Bessel's correction**, removes the bias. Unbiased does not mean best: for normal data, dividing by n gives the smaller mean squared error. What matters is to say which one a number uses.

### Practice Exercise

IX's unit test for Welch's test uses the samples (1, 2, 3, 4, 5) and (2, 3, 4, 5, 6). Compute each sample's variance with n − 1 and with n, then the statistic t = (X̄₁ − X̄₂)/√(s₁²/n₁ + s₂²/n₂) and the Welch–Satterthwaite degrees of freedom (s₁²/n₁ + s₂²/n₂)²/((s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)).

> *Solution:* Both samples have the sum of squared deviations 4 + 1 + 0 + 1 + 4 = 10, so the variance is 10/4 = 5/2 with n − 1 and 10/5 = 2 with n. With 5/2, each mean has the squared standard error (5/2)/5 = 1/2, the denominator is √(1/2 + 1/2) = 1, and t = (3 − 4)/1 = −1. The degrees of freedom are 1/((1/2)²/4 + (1/2)²/4) = 1/(1/8) = 8. These are the values in the comment of IX's test (§6).

---

## 2. Confidence Intervals and p-Values

By the central limit theorem, X̄ is approximately normal for large n whatever the distribution of the Xᵢ, as long as σ is finite. Then X̄ ± 1.96 σ/√n is an approximate **95% confidence interval**: before the data are drawn, the probability that this random interval contains μ is 0.95. When s replaces σ, the multiplier comes from Student's t distribution with n − 1 degrees of freedom, and it is larger for small n.

The 95% belongs to the procedure, not to one interval. Once the data are in, a given interval contains μ or it does not. "μ lies in [a, b] with probability 0.95" is the statement of a Bayesian credible interval, read from a posterior distribution as in MAT-008, and it needs a prior.

A **hypothesis test** fixes a null hypothesis H₀ and a statistic T. The **p-value** is the probability, computed under H₀, of a statistic at least as extreme as the one observed. It is not P(H₀ | data): as with the base rates of MAT-008, turning one into the other needs the prior probability of H₀. When T is continuous and H₀ holds, the p-value is uniform on [0, 1], so a test at the level α = 0.05 rejects a true null hypothesis 5% of the time. That is its whole guarantee, and it holds for one test chosen in advance. Running several tests and reporting the smallest p, or trying analyses until one works, multiplies the chances of a false positive: this is the **garden of forking paths**. The **Bonferroni correction** tests each of m hypotheses at α/m, which keeps the probability of any false rejection at most α, by the union bound.

### Practice Exercise

Twenty independent tests are run at α = 0.05, and every null hypothesis is true. What is the probability that at least one p-value falls below 0.05? What threshold does the Bonferroni correction use?

> *Solution:* Each p-value is uniform, so each test raises no alarm with probability 19/20, and all twenty stay silent with probability (19/20)^20 ≈ 0.358. At least one false positive therefore has the probability 1 − (19/20)^20 ≈ 0.64. Bonferroni tests each hypothesis at 0.05/20 = 0.0025, and the probability of any false rejection is then at most 20 · 0.0025 = 0.05.

---

## 3. Two-Sample Tests

Three tests in IX compare two samples, and they answer different questions:
- **Welch's t-test** asks whether the means differ. Its statistic divides the difference of the means by its estimated standard error, √(s₁²/n₁ + s₂²/n₂), without assuming equal variances, and its null distribution is approximated by Student's t with the Welch–Satterthwaite degrees of freedom. It relies on the sample means being close to normal.
- **The Mann–Whitney test** uses only ranks. Its statistic U counts the pairs (X₁ᵢ, X₂ⱼ) with X₁ᵢ > X₂ⱼ, a tie counting one half. Under the null hypothesis that all n₁ + n₂ observations are exchangeable, every choice of the ranks that belong to the first sample is equally likely, which gives U an exact distribution by counting. For large samples it is close to normal with the mean n₁ n₂/2.
- **The two-sample Kolmogorov–Smirnov test** takes the largest vertical gap D between the two empirical distribution functions. It reacts to any difference of distribution: location, spread or shape.

An **exact** test computes the p-value from the finite null distribution. An **asymptotic** test uses its large-sample limit, which can be far off for small samples. With three observations per sample there are C(6, 3) = 20 equally likely ways to place the ranks, and the most extreme outcome in each direction, every value of one sample below every value of the other, is a single arrangement.

### Practice Exercise

With three observations per sample, can an exact two-sided rank test give p < 0.05? What is its p-value for complete separation?

> *Solution:* No. Under H₀, each of the C(6, 3) = 20 rank sets of the first sample has the probability 1/20. Complete separation gives U = 0 or U = 9, one arrangement each, so its two-sided p-value is 2/20 = 0.1, and every other outcome gives a larger one. Complete separation is also the only way to get D = 1 in the Kolmogorov–Smirnov test, whose exact p-value is then 2/20 = 0.1 as well. A comparison of three against three cannot reach 0.05, whatever the data.

---

## 4. Cross-Validation

A model's error on the data it was fitted to is optimistic, since the fit has already adapted to their noise. **k-fold cross-validation** estimates the error on new data: it splits the n observations into k folds, fits the model k times, each time on k − 1 folds, and scores it on the fold left out, so that every observation is scored once, by a model that did not see it. **Stratified** folds keep the class proportions of the whole sample in each fold.

Two cautions follow from the construction. The k scores are not independent, since any two training sets share k − 2 folds, so the standard deviation of the fold scores divided by √k treats them as independent and can understate the uncertainty of their mean; Bengio and Grandvalet showed that no estimator of that variance is unbiased for every distribution. And cross-validation estimates the error of one procedure: choosing the best of many models on the same folds and reporting its score makes the score optimistic again, which nested cross-validation avoids.

How the fold scores are combined also matters. The mean of the fold accuracies weights each fold equally, and the accuracy of the pooled predictions weights each observation equally. They agree when the folds have the same size.

### Practice Exercise

Four test folds hold 6, 3, 3 and 3 observations, and a classifier gets 6, 1, 1 and 1 of them right. Compare the mean of the fold accuracies with the pooled accuracy.

> *Solution:* The fold accuracies are 1, 1/3, 1/3 and 1/3, whose mean is (1 + 1)/4 = 1/2. The pooled accuracy is (6 + 1 + 1 + 1)/15 = 9/15 = 3/5. The large fold counts for one fold in four in the first number and for 6 observations in 15 in the second; §6 shows how IX can produce such folds.

---

## 5. Resampling and the Seed

The **bootstrap** estimates the sampling distribution of a statistic from the sample itself: draw n observations with replacement, recompute the statistic, repeat many times, and read the spread or the quantiles of the results. A resample misses a given observation with the probability (1 − 1/n)^n, which tends to 1/e ≈ 0.368, so it contains about 63% of the distinct observations. The **percentile interval**, between the 2.5% and 97.5% quantiles of the bootstrap statistics, is the simplest bootstrap confidence interval. It needs no formula for the standard error, but it inherits the bias of the statistic and can be poor for small n.

Resampling, shuffling folds and initialising models all consume random numbers, so their results depend on the generator. A **pseudo-random generator** is a deterministic function: the same algorithm, started from the same **seed**, produces the same stream. The seed alone does not specify that stream. What a run draws is specified by the seed, the algorithm, the version of the library that implements it, and the order in which the program consumes the numbers; change any of them and the draws may change. A result that holds for one seed is a result about that seed. Reporting it after trying several seeds is another path in the garden of forking paths, so a run should fix its seed before seeing the data, or report the spread over many seeds.

### Practice Exercise

For a sample of n = 10 observations, what is the probability that a given observation is missing from a bootstrap resample, and how many distinct observations does a resample contain on average?

> *Solution:* Each of the 10 draws misses it with the probability 9/10, so it is missing with the probability (9/10)^10 ≈ 0.349, a little below 1/e ≈ 0.368. By linearity of expectation, the number of distinct observations averages 10 · (1 − (9/10)^10) ≈ 6.51.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**Sampling** (`crates/ix-math/src/random.rs`). [`seeded_rng`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L10) builds a `StdRng` from a `u64` seed, and [`shuffle_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L35) and [`sample_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L43) take such a generator as an argument. The four helpers defined between them take none. Lines 9–17, verbatim, show the seeded constructor and the first helper; the three others have the same shape:

```rust
/// Create a seeded RNG for reproducibility.
pub fn seeded_rng(seed: u64) -> StdRng {
    StdRng::seed_from_u64(seed)
}

/// Random matrix from uniform distribution [low, high).
pub fn uniform_matrix(rows: usize, cols: usize, low: f64, high: f64) -> Array2<f64> {
    Array2::random((rows, cols), Uniform::new(low, high).unwrap())
}
```

- **The public random helpers cannot be reproduced.** `uniform_matrix`, [`normal_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L20), `uniform_vector` and `normal_vector` call [`random`](https://docs.rs/ndarray-rand/0.16.0/ndarray_rand/trait.RandomExt.html) from `ndarray-rand`, which seeds a new generator from `rand`'s thread-local generator, itself seeded by the operating system, on every call. No argument can make two calls agree, and the tests in `random.rs` check only their shapes. `Uniform::new` fails when low ≥ high, so the [`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L16) panics for an empty range, such as `uniform_matrix(2, 2, 1.0, 1.0)`.
- **A seed is not yet a portable specification.** The documentation of `rand` 0.9 describes [`StdRng`](https://docs.rs/rand/0.9.2/rand/rngs/struct.StdRng.html) as non-portable: "any future library version may replace the algorithm and results may be platform-dependent". It points to [`rand_chacha`](https://docs.rs/rand_chacha/0.9.0/rand_chacha/), whose generators it calls portable. IX's workspace asks for [`rand = "0.9"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L102), a range of versions, and its [`.gitignore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.gitignore#L3) excludes `Cargo.lock`, the file that would record the version a build used. So `seeded_rng(42)` repeats its stream within one build, but pinning IX at `e35138b9` does not by itself fix that stream. The workspace already depends on [`rand_chacha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L103).
- **`sample_indices` shortens its answer silently.** It [draws `k.min(n)` indices](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L45), so asking for 10 indices out of 5 returns 5, with no error.
- **Cross-validation is seeded, with a hidden default.** [`KFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L64) and `StratifiedKFold` shuffle by default with the [seed 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L76), and [`cross_val_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L245) passes its `seed` argument to a [`StratifiedKFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L312). That split [deals each class round-robin](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L193) starting from the first fold every time, so three classes of 5 observations with k = 4 give test folds of 6, 3, 3 and 3, the case of §4's exercise. With the labels (0, 0, 1, 1) and k = 3, the third fold is empty although n ≥ k, and if the model accepts an empty input, [`accuracy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/metrics.rs#L98) then divides 0 by 0, which is NaN in binary64.
- **No confidence interval.** IX's crates have no bootstrap or confidence-interval function. The only resampling is inside the random forest, which [draws n indices with replacement](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-ensemble/src/random_forest.rs#L66) for each tree from a seeded generator, and does not report the out-of-bag error that the observations left out of each resample, about 37%, would allow.

**Two-sample tests** (`crates/ix-math/src/inference.rs`). The file says that it follows SciPy's conventions and pins its tests to SciPy values. [`welch_t_test`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L340) uses the [n − 1 variance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L349) of §1, and [`welch_t_test_matches_scipy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L624) checks the t = −1 of §1's exercise, and a p-value within 2 · 10^-3 of SciPy's 0.3466. The two rank tests compute asymptotic p-values only. The Mann–Whitney p-value goes through this tail function, verbatim from lines 386–389:

```rust
/// Upper tail of the standard normal: `P(Z > z)`.
fn normal_sf(z: f64) -> f64 {
    0.5 * (1.0 - erf(z / std::f64::consts::SQRT_2))
}
```

- **Small p-values become exactly 0.** [`erf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L373) is the Abramowitz–Stegun approximation 7.1.26, within 1.5 · 10^-7 of the true value. For large z, the computed erf rounds to 1 and 1 − erf is exactly 0: a transcription of these lines predicts that [`mann_whitney_u`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L283) returns p = 0 once z exceeds about 8.38, where the true normal tail is still about 5 · 10^-17. For 50 observations against 50, complete separation gives z ≈ 8.61 and p = 0, while its exact p-value is 2/C(100, 50), tiny but positive. A p-value of 0 from this function means "below about 10^-16", not "impossible"; computing the complementary error function directly avoids the cancellation.
- **The Kolmogorov–Smirnov p-value is not SciPy's.** The [doc comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L242) names SciPy's `method='asymp'`, but the code [applies Stephens' correction](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L273) inside the Kolmogorov series, as Numerical Recipes does. In SciPy 1.17.1, that option instead evaluates the distribution of D for a sample size of N = n₁ n₂/(n₁ + n₂), rounded, so the two p-values differ. On tiny samples IX's value can be far too small: for (0, 1, 2) against (10, 11, 12), the samples of [IX's test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L590), the formula gives about 0.033, while the exact p-value is 0.1 (§3). The test only [asserts p < 0.2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L592), which both values pass.

**A test that cannot fail.** [`test_hurst_random_walk`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L208) draws its ±1 steps from [`rand::rng()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L211), a generator seeded by the operating system, so each run tests different data. Its comment expects H ≈ 0.5 for a random walk. But [`hurst_exponent`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L97) [accumulates the deviations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L116) itself, so it expects the steps, and the test passes it the walk, their running sum. For such an integrated series the rescaled range grows like the window size itself, which predicts H near 1, not 0.5. The assertion [0.1 < H < 1.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L221) accepts both values, so the test cannot detect the confusion. Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

For (0, 1, 2) against (10, 11, 12), D = 1 and N = 3 · 3/6 = 3/2. Compute the p-value of IX's formula, 2 e^(−2t²) with t = (√N + 0.12 + 0.11/√N) · D, since the next terms of the series are negligible here, and compare it with the exact p-value of §3.

> *Solution:* √(3/2) ≈ 1.225, so t ≈ 1.225 + 0.12 + 0.090 ≈ 1.435, 2t² ≈ 4.12, and 2 e^(−4.12) ≈ 0.033. The next term, 2 e^(−8t²), is about 10^-7. The exact p-value is 2/20 = 0.1: the formula reports significance at 0.05 for a comparison that §3 showed can never reach it. This is arithmetic on the code, not a run; §7 checks it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Same seed, same stream.** For s = 0, …, 999, call `shuffle_indices(10, &mut seeded_rng(s))` twice. Prediction: the two permutations are identical for every s. Record the version of `rand` from the build's `Cargo.lock` next to the results.
2. **Different seeds, stable statistic.** For the same 1000 seeds, count the fixed points of each permutation. Prediction: the counts vary with the seed, and their mean is within 0.1 of 1, the expected number of fixed points of a uniform random permutation.
3. **The unseeded helpers.** Call `uniform_vector(5, 0.0, 1.0)` twice. Prediction: the two vectors differ. Then call `uniform_matrix(2, 2, 1.0, 1.0)`. Prediction: a panic from the `unwrap` of `Uniform::new`.
4. **Truncated sampling.** Call `sample_indices(5, 10, &mut seeded_rng(0))`. Prediction: 5 distinct indices and no error.
5. **Test tails.** Call `mann_whitney_u` on 0, …, 49 against 100, …, 149, then on 0, …, 39 against 100, …, 139. Prediction: U₁ = 0 both times, with p = 0 exactly for 50 against 50 and a positive p of the order of 10^-14 for 40 against 40. Call `ks_two_sample` on (0, 1, 2) against (10, 11, 12). Prediction: D = 1 and p ≈ 0.033.
6. **Folds.** Split the labels (0, 0, 1, 1) with `StratifiedKFold::new(3)`, and five labels of each of three classes with `StratifiedKFold::new(4)`. Prediction: test folds of sizes 2, 2 and 0, then 6, 3, 3 and 3. Then run `cross_val_score` with `KNN::new(1)` on four points carrying the first labels, and report whether the third score is NaN or the call panics.
7. **The Hurst test.** Build the walks of `test_hurst_random_walk` from 100 seeded generators instead of `rand::rng()`, and apply `hurst_exponent` to the walks and to their steps. Prediction: H near 1 for the walks and near 0.5 for the steps, all inside (0.1, 1.5).

### Practice Exercise

Step 2 predicts a mean within 0.1 of 1 over 1000 seeds. Where does that margin come from?

> *Solution:* Let Iᵢ indicate that position i is fixed. Each Iᵢ has the expectation 1/10, so the number of fixed points has the expectation 10 · 1/10 = 1. Each Iᵢ has the variance (1/10)(9/10), and for i ≠ j, P(both fixed) = 1/90, so the covariance is 1/90 − 1/100 = 1/900. The variance is 10 · 9/100 + 90 · 1/900 = 9/10 + 1/10 = 1. The mean over 1000 independent seeds has the standard deviation 1/√1000 ≈ 0.032, and three of them, about 0.095, fit inside 0.1. This treats the seeds as giving independent uniform permutations, which is what a good generator approximates; the seed makes the run repeatable, not more random.

---

## 8. Common Pitfalls

- **Reporting an estimate without its uncertainty.** A mean without a standard error or an interval cannot be compared with anything.
- **Reading a p-value as the probability that the null hypothesis is true.** It is computed by assuming that hypothesis.
- **Reading "not significant" as "no effect".** A small sample may lack the power to detect anything: three against three can never reach 0.05.
- **Choosing the test after seeing the data.** Fix the test, the metric and the threshold first, or correct for the number of tests.
- **Trusting asymptotic p-values on tiny samples.** Count the exact null distribution when the samples are small.
- **Treating fold scores as independent.** Their spread divided by √k can understate the uncertainty of the cross-validated mean.
- **Treating a seed as the whole specification.** Record the generator, the library version and the order of the draws, and report results over several seeds.
- **Writing a test that its alternative also passes.** A bound wide enough to accept both H ≈ 0.5 and H ≈ 1 checks neither.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Estimator** | A rule that turns a sample into a guess of an unknown quantity |
| **Bias** | E[θ̂] − θ, the average error of an estimator |
| **Standard error** | The standard deviation of an estimator, σ/√n for the sample mean |
| **Bessel's correction** | Dividing the sum of squared deviations by n − 1, which makes the variance estimator unbiased |
| **Confidence interval** | A random interval that contains the true value with a stated probability, before the data are drawn |
| **p-value** | The probability under the null hypothesis of a statistic at least as extreme as the one observed |
| **Exact test** | A test whose p-value comes from the finite null distribution, often by counting |
| **Cross-validation** | Estimating the error on new data by fitting on part of the data and scoring on the rest, in turn |
| **Bootstrap** | Estimating a sampling distribution by resampling the data with replacement |
| **Seed** | The initial state of a pseudo-random generator; with the algorithm and its version, it fixes the stream |
| **Garden of forking paths** | The inflation of false positives when the analysis is chosen after seeing the data |

---

## Self-Check Assessment

**1. Why does dividing by n underestimate the variance?**
> The deviations are measured from X̄, which is fitted to the same data and lies closer to them than μ: E[Σ(Xᵢ − X̄)²] = (n − 1) σ², so dividing by n gives (n − 1) σ²/n on average.

**2. A study reports p = 0.03. Why is the probability that the null hypothesis is true not 0.03?**
> The p-value is the probability of data at least this extreme given H₀, not the probability of H₀ given the data. Turning one into the other needs the prior probability of H₀ and the behaviour of the data under the alternative, as with Bayes' theorem in MAT-008.

**3. Two runs of the same program with the same seed give different results. Name three possible causes.**
> A different version of the generator's library, a different algorithm behind the same name, a different order or number of draws, or randomness that does not come from the seeded generator at all, such as IX's `uniform_matrix`.

**4. IX's `test_hurst_random_walk` passes. What does it tell you about `hurst_exponent`?**
> Little: the bound 0.1 < H < 1.5 accepts both the value 0.5 that its comment expects and the value near 1 that the walk it builds should give, and its data change on every run.

**Pass criteria:** Compute the bias and standard error of simple estimators, interpret a confidence interval and a p-value, count an exact small-sample null distribution, explain what k-fold cross-validation estimates and what the spread of its folds misses, state what a seed does and does not fix, and trace what IX's sampling, cross-validation and two-sample tests guarantee.

---

## Research Basis

- L. Wasserman, *All of Statistics*, Springer, 2004: estimators, confidence intervals, tests and the bootstrap
- B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993: the bootstrap and percentile intervals
- B. L. Welch, "The generalization of 'Student's' problem when several different population variances are involved", *Biometrika* 34, 1947: Welch's test
- H. B. Mann and D. R. Whitney, "On a test of whether one of two random variables is stochastically larger than the other", *Annals of Mathematical Statistics* 18, 1947: the U test
- N. Smirnov, "Table for estimating the goodness of fit of empirical distributions", *Annals of Mathematical Statistics* 19, 1948: the two-sample statistic
- M. A. Stephens, "Use of the Kolmogorov–Smirnov, Cramér–von Mises and related statistics without extensive tables", *Journal of the Royal Statistical Society B* 32, 1970: the small-sample correction
- M. Abramowitz and I. A. Stegun, *Handbook of Mathematical Functions*, National Bureau of Standards, 1964, formula 7.1.26: the erf approximation
- W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, *Numerical Recipes*, 3rd ed., Cambridge University Press, 2007: the Kolmogorov–Smirnov routine that IX follows
- Y. Bengio and Y. Grandvalet, "No unbiased estimator of the variance of K-fold cross-validation", *Journal of Machine Learning Research* 5, 2004: why no estimate of the uncertainty of a cross-validated mean is unbiased for every distribution
- A. Gelman and E. Loken, "The garden of forking paths", 2013: data-dependent analysis
- A. A. Anis and E. H. Lloyd, "The expected value of the adjusted rescaled Hurst range of independent normal summands", *Biometrika* 63, 1976: the small-sample behaviour of the rescaled range
- The documentation of `rand` 0.9 and `rand_chacha` 0.9, linked in §6: the portability of seeded generators
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
