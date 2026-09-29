---
module_id: mat-010-information-entropy-divergences
department: mathematics
course: Entropy, Divergences and Mutual Information
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Entropy, Divergences and Mutual Information — Measuring Uncertainty and the Cost of a Wrong Model

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Compute the entropy of a discrete distribution in bits and in nats, and show that the uniform distribution maximises it
- Relate joint and conditional entropy by the chain rule, and compute the mutual information of two variables
- Compute the Kullback–Leibler divergence, prove that it is non-negative, and explain why it is not a distance
- Use the Jensen–Shannon divergence when a symmetric, bounded comparison is needed
- Say how estimates of entropy and mutual information from samples are biased, and trace what IX's entropy, divergence and delay functions guarantee

---

## 1. Surprise and Entropy

An outcome of probability p carries the **surprisal** −log p: a certain outcome carries none, and each halving of the probability adds one unit. The **entropy** of a discrete random variable X with distribution p₁, …, p_K is its expected surprisal, H(X) = −Σ pᵢ log pᵢ, with 0 log 0 = 0, the limit of p log p as p → 0. The base of the logarithm is the unit: base 2 gives **bits**, the natural logarithm gives **nats**, and 1 bit = ln 2 ≈ 0.693 nats.

Entropy is 0 exactly when one outcome is certain, and it is at most log K, with equality exactly for the uniform distribution; §3 proves the bound. Shannon's source coding theorem gives it an operational meaning: no uniquely decodable binary code can use fewer than H(X) bits per symbol on average, and codes exist that come within one bit of it.

### Practice Exercise

What is the entropy of the uniform distribution on 8 outcomes, in bits and in nats? What is the entropy of (1/2, 1/4, 1/8, 1/8), and how does it compare with the uniform distribution on 4 outcomes?

> *Solution:* Each outcome has surprisal log₂ 8 = 3 bits, so H = 3 bits, which is 3 ln 2 ≈ 2.079 nats. For (1/2, 1/4, 1/8, 1/8), H = 1/2 · 1 + 1/4 · 2 + 1/8 · 3 + 1/8 · 3 = 1/2 + 1/2 + 3/8 + 3/8 = 7/4 bits, below log₂ 4 = 2 bits. The code 0, 10, 110, 111 has exactly this average length, 1.75 bits.

---

## 2. Joint Entropy, Conditional Entropy and Mutual Information

For two variables, the **joint entropy** H(X, Y) is the entropy of the pair, and the **conditional entropy** H(Y | X) = Σₓ p(x) H(Y | X = x) is the uncertainty left in Y once X is known. They satisfy the **chain rule** H(X, Y) = H(X) + H(Y | X), and conditioning never increases entropy on average: H(Y | X) ≤ H(Y).

The **mutual information** is the reduction of uncertainty about one variable that the other brings: I(X; Y) = H(Y) − H(Y | X) = H(X) + H(Y) − H(X, Y). It is symmetric, it is never negative, and it is 0 exactly when X and Y are independent in the sense of MAT-008. Unlike a correlation coefficient, it detects any dependence, not only a linear one, and it is unchanged by any one-to-one relabelling of either variable.

### Practice Exercise

X is a fair bit, and Y equals X except that it is flipped with probability 1/4. Compute I(X; Y) in bits.

> *Solution:* Y is a fair bit too, so H(Y) = 1. Given X, Y is uncertain only through the flip, so H(Y | X) = h(1/4), where h(q) = −q log₂ q − (1 − q) log₂(1 − q). h(1/4) = 1/4 · 2 + 3/4 · log₂(4/3) = 2 − (3/4) log₂ 3 ≈ 0.811, so I(X; Y) = 1 − h(1/4) = (3/4) log₂ 3 − 1 ≈ 0.189 bits. The joint table (3/8, 1/8; 1/8, 3/8) gives the same value through H(X) + H(Y) − H(X, Y).

---

## 3. The Kullback–Leibler Divergence

The **Kullback–Leibler divergence** of p from q is KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), summed over the outcomes with pᵢ > 0. It is +∞ as soon as q gives probability 0 to an outcome that p allows. **Gibbs' inequality** states that KL(p ‖ q) ≥ 0, with equality exactly when p = q. Since ln x ≤ x − 1, −KL(p ‖ q) = Σ pᵢ ln(qᵢ/pᵢ) ≤ Σ pᵢ (qᵢ/pᵢ − 1) = Σ qᵢ − 1 ≤ 0, where the sums run over pᵢ > 0. With q uniform, KL(p ‖ q) = log K − H(p), which proves the bound of §1.

KL measures the cost of a wrong model. The **cross-entropy** H(p, q) = −Σ pᵢ log qᵢ equals H(p) + KL(p ‖ q): coding data from p with the ideal code lengths −log₂ qᵢ of q costs KL(p ‖ q) extra bits per symbol on average, and minimising the log loss of a classifier minimises the divergence of its model from the data. KL is not a distance: it is not symmetric, and it does not satisfy the triangle inequality. Mutual information is itself a divergence, I(X; Y) = KL(p(x, y) ‖ p(x) p(y)), the cost of assuming independence.

### Practice Exercise

Let p = (3/4, 1/4) and q = (1/2, 1/2). Compute KL(p ‖ q) and KL(q ‖ p) in nats.

> *Solution:* KL(p ‖ q) = 3/4 · ln(3/2) + 1/4 · ln(1/2) = (3/4) ln 3 − ln 2 ≈ 0.131, which is also ln 2 − H(p). KL(q ‖ p) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3) ≈ 0.144. The two directions differ, and swapping the arguments can even turn a finite value into +∞: KL((1, 0) ‖ (1/2, 1/2)) = ln 2, while KL((1/2, 1/2) ‖ (1, 0)) is infinite.

---

## 4. The Jensen–Shannon Divergence

The **Jensen–Shannon divergence** compares p and q with their mixture m = (p + q)/2: JS(p, q) = ½ KL(p ‖ m) + ½ KL(q ‖ m) = H(m) − (H(p) + H(q))/2. It is symmetric, and it is always finite, since m is positive wherever p or q is. It is bounded by ln 2: m ≥ p/2, so each pᵢ/mᵢ ≤ 2 and KL(p ‖ m) ≤ ln 2, and the same holds for q. The bound is reached exactly when p and q have disjoint supports. JS is the mutual information between a fair coin that chooses p or q and the outcome then drawn, and its square root is a metric.

### Practice Exercise

Compute JS((1, 0), (1/2, 1/2)) in nats and in bits, and compare it with the bound.

> *Solution:* m = (3/4, 1/4). KL((1, 0) ‖ m) = ln(4/3), and KL((1/2, 1/2) ‖ m) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3). So JS = (1/2) ln(4/3) + (1/4) ln(4/3) = (3/4) ln(4/3) ≈ 0.216 nats, which is (3/4) log₂(4/3) ≈ 0.311 bits, well below ln 2 ≈ 0.693 nats, one bit. It is finite although one of the two KL divergences between these distributions is not.

---

## 5. Estimating Information From Samples

In practice p is unknown, and the **plug-in estimator** replaces it with the observed frequencies. The plug-in entropy is biased downward: frequencies fit the sample, and outcomes that were not observed contribute nothing. For N observations of K outcomes, Miller's first-order expansion gives E[Ĥ] ≈ H − (K − 1)/(2N) nats. The plug-in mutual information is biased upward: for independent variables with B_X and B_Y bins, 2N Î is the G-statistic of a test of independence, approximately χ² with (B_X − 1)(B_Y − 1) degrees of freedom, so E[Î] ≈ (B_X − 1)(B_Y − 1)/(2N) nats although the true value is 0.

Continuous variables add a choice of bins. With bins of width Δ, the binned entropy is close to h(X) − log Δ, where h is the differential entropy, so it grows without bound as the bins shrink; two binned entropies are comparable only with the same bins and range. A plug-in KL divergence is infinite as soon as a bin is empty in the sample from q and not in the sample from p, and smoothing the counts makes it finite, but the value then depends on the smoothing.

### Practice Exercise

A fair coin is tossed twice, and the entropy is estimated from the two outcomes. What is the expected plug-in estimate in nats, and how does it compare with the true entropy?

> *Solution:* With probability 1/2 the tosses agree, the frequencies are (1, 0) and Ĥ = 0; with probability 1/2 they differ, the frequencies are (1/2, 1/2) and Ĥ = ln 2. So E[Ĥ] = (ln 2)/2 ≈ 0.347, half the true value ln 2 ≈ 0.693. The first-order correction (K − 1)/(2N) = 1/4 would only bring it to about 0.60: the expansion assumes N large compared with K.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**Divergences** (`crates/ix-math/src/inference.rs`). [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L176), [`kl_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L187) and [`js_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L212) work in nats, and they first pass their inputs through `normalize`, so any non-negative weights are accepted and scaling them changes nothing. `kl_divergence` [returns an error](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L199) when q is 0 where p is positive, instead of +∞, and the doc comment of `js_divergence` [states the bound](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L211) [0, ln 2]. The test [`entropy_and_divergences`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L569) checks the uniform distribution on 4 outcomes, a point mass, KL((1, 0) ‖ (1/2, 1/2)) = ln 2, JS of disjoint supports and the error case. The DuckDB extension exposes the three functions to SQL as [`ix_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L143), [`ix_kl`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L192) and [`ix_js`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L205).

```rust
fn normalize(p: &[f64]) -> Result<Vec<f64>, MathError> {
    if p.is_empty() {
        return Err(MathError::EmptyInput);
    }
    if p.iter().any(|&v| v < 0.0 || v.is_nan()) {
        return Err(MathError::InvalidParameter(
            "probability vector must be non-negative".into(),
        ));
    }
    let total: f64 = p.iter().sum();
    if total <= 0.0 {
        return Err(MathError::InvalidParameter(
            "probability vector sums to zero".into(),
        ));
    }
    Ok(p.iter().map(|v| v / total).collect())
}
```

- **An overflowing total gives three different answers.** `normalize` rejects [negative and NaN weights](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L161) but not +∞, and its [sum](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L166) can overflow. For the weights (10^308, 10^308), the total 2 · 10^308 exceeds the largest `f64`, about 1.8 · 10^308, so it becomes +∞ and every normalised weight becomes 0. `shannon_entropy` then skips every term and returns −0.0 instead of ln 2, `kl_divergence` against (1, 3) returns 0 instead of about 0.144, and `js_divergence` returns the error "probability vector sums to zero", because it normalises the zero vector again. A weight of +∞ passes the check and normalises to NaN: for (+∞, 1), the entropy is again −0.0, KL against (1, 1) is 0, and JS fails with "must be non-negative". These are predictions from a line-by-line transcription, not a run; MAT-003 covers overflow, and §7 checks them.
- **The bounds hold only up to rounding.** KL ≥ 0 and JS ≤ ln 2 are theorems about exact sums, and the computed sums are rounded. The transcription returns a KL slightly below 0, down to about −5 · 10^-16, on over a third of 10^5 random near-equal pairs, and a JS slightly above ln 2, by at most about 3 · 10^-16, on some nearly disjoint pairs. IX's test compares with a tolerance, as it should; a caller that tests `kl >= 0.0` exactly can fail.
- **The same name measures something else in `ix-code`.** Its [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L145) takes raw values, counts them in equal-width bins, and [divides the entropy in bits by log₂ of the number of bins](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L176), which gives a number in [0, 1]. It returns 0 when the range is at most [`f64::EPSILON`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L152) in absolute terms, so the values 10^-20 and 2 · 10^-20, which differ by a factor of 2, get the entropy 0, while 1 and 2 get 1/log₂ 10 ≈ 0.301 with 10 bins.
- **Perplexity is consistent.** Both t-SNE implementations compare an entropy in nats with the natural logarithm of the target perplexity, [in `ix-manifold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L182), whose [`entropy_of`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L242) uses `ln`, and [in `ix-unsupervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/tsne.rs#L75). The perplexity is therefore e^H with H in nats, the same number as 2^H with H in bits.
- **The cross-entropy loss is clamped.** [`binary_cross_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L18) clamps the predictions [10^-12 away from 0 and 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L19), so a confident wrong prediction costs about 27.63 nats per element instead of +∞.
- **Mutual information exists only inside `optimal_delay`.** No IX function computes I(X; Y). [`optimal_delay`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L29) estimates the mutual information between a series and its lagged copy from a [two-dimensional histogram](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L71), and it returns the last lag before the estimate [first rises](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L77), the rule of Fraser and Swinney. Its estimate is the plug-in one, with the upward bias of §5.
- **Its test accepts every possible result.** [`test_optimal_delay_sine`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L188) passes 2000 samples of a sine of period 100, with at most 50 lags and 16 bins. Its [comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L194) expects about 25, a quarter period, but it only [asserts](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L197) a lag between 1 and 50, and on this input the function cannot return anything else: its result lies between 1 and the smaller of the lag limit and n/2, here 50. A transcription predicts 5. The binned estimate falls to 1.584 nats at lag 5 and rises to 1.628 at lag 6, so the first-rise rule stops there. With 1 bin every estimate is 0, the estimate never rises, and the function returns the lag limit, 50. With 0 bins, [`num_bins - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L43) underflows and the call panics: on the subtraction when overflow checks are on, as in the default debug build, and otherwise on an index out of bounds.

```rust
        let delay = optimal_delay(&data, 50, 16);
        // Optimal delay for a sine wave should be around T/4 = 25
        // The mutual information method can vary; accept a wider range
        assert!(
            (1..=50).contains(&delay),
            "Optimal delay for sine: {}",
            delay
        );
```

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Why does `shannon_entropy` return −0.0 for the weights (10^308, 10^308), and what would it return if `normalize` first divided every weight by the largest one?

> *Solution:* The sum 10^308 + 10^308 = 2 · 10^308 exceeds the largest `f64`, about 1.8 · 10^308, so it rounds to +∞, and each weight divided by +∞ is 0. The filter keeps only positive weights, the sum of no terms is 0, and its negation is −0.0. Dividing by the largest weight first gives (1, 1), whose sum 2 is exact, then (1/2, 1/2), whose entropy is ln 2 ≈ 0.693. This is arithmetic on the code, not a run; §7 checks it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Nominal values.** Call `shannon_entropy` on eight equal weights, `kl_divergence` on (3, 1) against (1, 1) and back, and `js_divergence` on (1, 0) and (1, 1). Prediction: 3 ln 2 ≈ 2.079, then 0.131 and 0.144, then (3/4) ln(4/3) ≈ 0.216, each within 10^-12.
2. **Overflow and infinity.** Call the three functions on (10^308, 10^308), with (1, 3) as the second argument, then on (+∞, 1) with (1, 1). Prediction: −0.0, 0 and the error "sums to zero", then −0.0, 0 and the error "must be non-negative".
3. **Bounds under rounding.** Draw 10^5 pairs of near-equal and of nearly disjoint weight vectors from a seeded generator. Prediction: some KL values below 0 and some JS values above ln 2, all within 10^-15 of the bound.
4. **Plug-in bias.** For 100 seeds, draw 1999 pairs of independent uniform values, sort each coordinate into 16 equal bins, and compute Î = Ĥ(X) + Ĥ(Y) − Ĥ(X, Y) with `shannon_entropy` on the counts. Prediction: every Î is positive, and their mean is close to 15²/(2 · 1999) ≈ 0.056 nats.
5. **The delay.** Call `optimal_delay` on the sine of `test_optimal_delay_sine` with 16 bins, 1 bin and 0 bins. Prediction: 5, then 50, then a panic.
6. **The binned entropy.** Call `ix-code`'s `shannon_entropy` on (0, 1) with 2 bins, on (10^-20, 2 · 10^-20) with 10 bins, and on (1, 2) with 10 bins. Prediction: 1, then 0, then 1/log₂ 10 ≈ 0.301.
7. **The clamp.** Call `binary_cross_entropy` with the prediction 0 and the target 1. Prediction: 12 ln 10 ≈ 27.63.

### Practice Exercise

In step 4, why does the mean stay positive although the variables are independent, and what mean would ten times as many pairs give?

> *Solution:* The plug-in estimate is the divergence of the observed joint frequencies from the product of the observed marginals, and sampling noise alone makes them differ, so Î > 0 on almost every sample. Its mean is about (B_X − 1)(B_Y − 1)/(2N) = 225/3998 ≈ 0.056 nats. With ten times as many pairs, it falls ten times, to about 0.0056: the bias shrinks like 1/N, and a positive estimate is evidence of dependence only when it clearly exceeds what independent data give, for example after shuffling one of the variables.

---

## 8. Common Pitfalls

- **Mixing bits and nats.** One bit is ln 2 ≈ 0.693 nats. IX's `inference.rs` works in nats, and `ix-code` reports normalised bits.
- **Treating KL as a distance.** It is not symmetric and has no triangle inequality; use JS, or its square root, when a symmetric comparison is needed.
- **Letting q vanish where p does not.** KL is then infinite, and smoothing makes it finite only at the price of a value that depends on the smoothing.
- **Trusting a plug-in estimate from few samples.** Entropy comes out too low and mutual information too high; compare with shuffled data.
- **Comparing binned entropies across different bins.** The binned entropy of a continuous variable depends on the bin width as much as on the data.
- **Testing a bound exactly in floating point.** A computed KL can be −10^-16; compare with a tolerance.
- **Writing a test whose accepted range is every possible output.** Assert the value the comment expects, with the tolerance the method allows.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Surprisal** | −log p, the information carried by an outcome of probability p |
| **Entropy** | The expected surprisal of a random variable, −Σ pᵢ log pᵢ |
| **Bit and nat** | The units of entropy for base-2 and natural logarithms; 1 bit = ln 2 nats |
| **Conditional entropy** | H(Y \| X), the uncertainty left in Y once X is known |
| **Mutual information** | I(X; Y) = H(X) + H(Y) − H(X, Y), zero exactly under independence |
| **KL divergence** | KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), the cost of using q when the data follow p |
| **Cross-entropy** | H(p, q) = H(p) + KL(p ‖ q), the log loss of the model q on data from p |
| **Gibbs' inequality** | KL(p ‖ q) ≥ 0, with equality exactly when p = q |
| **Jensen–Shannon divergence** | The average KL divergence of p and q from their mixture; symmetric and at most ln 2 |
| **Plug-in estimator** | An estimate that replaces the unknown distribution with the observed frequencies |
| **Perplexity** | e^H with H in nats, the effective number of equally likely outcomes |

---

## Self-Check Assessment

**1. Why is the entropy of a distribution on K outcomes at most log K, with equality only for the uniform distribution?**
> KL(p ‖ u) = log K − H(p) for the uniform distribution u, and Gibbs' inequality makes it non-negative, with equality exactly when p = u.

**2. KL(p ‖ q) = 0.131 and KL(q ‖ p) = 0.144. Which one is the distance between p and q?**
> Neither. KL is not symmetric: each direction answers its own question, the cost of assuming q for data from p or the reverse. A symmetric comparison needs JS or its square root.

**3. Two variables, binned into 16 values each, give a plug-in mutual information of 0.05 nats on 2000 observations. Is this evidence of dependence?**
> No. Independent variables give about 15²/(2 · 2000) ≈ 0.056 nats on average with these bins, so 0.05 is what no dependence at all looks like. Comparing with shuffled pairs would show it.

**4. IX's `test_optimal_delay_sine` passes. What does it tell you about `optimal_delay`?**
> Only that the call does not panic on that input: the test accepts every lag from 1 to 50, which is every value the function can return, and not the quarter period that its comment expects.

**Pass criteria:** Compute entropy, conditional entropy and mutual information in bits and in nats, compute and interpret the KL and Jensen–Shannon divergences, prove Gibbs' inequality and the bound log K, explain the biases of plug-in estimates, and trace what IX's entropy, divergence, loss and delay functions guarantee.

---

## Research Basis

- C. E. Shannon, "A mathematical theory of communication", *Bell System Technical Journal* 27, 1948: entropy, mutual information and source coding
- S. Kullback and R. A. Leibler, "On information and sufficiency", *Annals of Mathematical Statistics* 22, 1951: the divergence
- T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley, 2006: chain rules, Gibbs' inequality, coding and differential entropy
- J. Lin, "Divergence measures based on the Shannon entropy", *IEEE Transactions on Information Theory* 37, 1991: the Jensen–Shannon divergence and its bound
- D. M. Endres and J. E. Schindelin, "A new metric for probability distributions", *IEEE Transactions on Information Theory* 49, 2003: the square root of JS is a metric
- G. A. Miller, "Note on the bias of information estimates", in *Information Theory in Psychology*, Free Press, 1955: the bias of the plug-in entropy
- L. Paninski, "Estimation of entropy and mutual information", *Neural Computation* 15, 2003: the bias of plug-in estimators
- A. M. Fraser and H. L. Swinney, "Independent coordinates for strange attractors from mutual information", *Physical Review A* 33, 1986: the delay at the first minimum of the mutual information
- L. van der Maaten and G. Hinton, "Visualizing data using t-SNE", *Journal of Machine Learning Research* 9, 2008: perplexity
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
