---
module_id: mat-008-probability-conditional-reasoning
department: mathematics
course: Probability and Conditional Reasoning
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies, mat-003-floating-point-conditioning]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Probability and Conditional Reasoning — Updating a Belief on Evidence

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- State Kolmogorov's axioms, and derive the complement rule and inclusion–exclusion from them
- Compute conditional probabilities, and tell independence from conditional independence
- Apply Bayes' theorem, in probability form and in odds form, and explain why the base rate matters
- Update a Beta prior with binomial data, and say what the posterior mean hides
- Say what IX's Bayesian rule weights and its naive Bayes classifier compute, and where they break

---

## 1. The Axioms

A probability model has a **sample space** Ω, the set of possible outcomes; a collection of **events**, subsets of Ω that form a **σ-algebra**; and a probability P, defined on the events, that satisfies **Kolmogorov's axioms**. A σ-algebra contains Ω, the complement of each of its sets and the union of each sequence of its sets, and so also their intersections and differences. When Ω is finite or countable, the σ-algebra can be the set of all subsets of Ω. When Ω is uncountable, it may have to be smaller: the uniform probability on the real numbers between 0 and 1 cannot be extended to every subset while staying unchanged under shifts modulo 1 (Vitali's construction). The axioms are:
1. P(A) ≥ 0 for every event A.
2. P(Ω) = 1.
3. For pairwise disjoint events A₁, A₂, …, P(A₁ ∪ A₂ ∪ …) = P(A₁) + P(A₂) + ….

Everything else follows. Since A and its complement are disjoint and fill Ω, P(not A) = 1 − P(A), and P(∅) = 0. If A ⊆ B, then P(A) ≤ P(B). Splitting A ∪ B into disjoint pieces gives **inclusion–exclusion**: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). When Ω is finite and its outcomes are equally likely, P(A) = |A|/|Ω|, and probability is counting.

### Practice Exercise

Roll two fair dice. Compute P(the sum is 7) and P(at least one six), the second in two ways.

> *Solution:* The 36 ordered pairs are equally likely. The sum is 7 for (1, 6), (2, 5), (3, 4), (4, 3), (5, 2) and (6, 1), so P = 6/36 = 1/6. For at least one six, the complement "no six" has 5 · 5 = 25 pairs, so P = 1 − 25/36 = 11/36. By inclusion–exclusion, P(first is 6) + P(second is 6) − P(both are 6) = 1/6 + 1/6 − 1/36 = 11/36.

---

## 2. Conditional Probability and Independence

The **conditional probability** of A given B, for P(B) > 0, is P(A | B) = P(A ∩ B)/P(B): restrict the outcomes to B and renormalise. It gives the **multiplication rule** P(A ∩ B) = P(A | B) P(B), and, when the events B₁, …, B_k split Ω into disjoint pieces, the **law of total probability** P(A) = P(A | B₁) P(B₁) + … + P(A | B_k) P(B_k).

A and B are **independent** when P(A ∩ B) = P(A) P(B), which for P(B) > 0 means P(A | B) = P(A): learning B does not change the probability of A. Independence is not disjointness. Two disjoint events of positive probability are never independent, since learning one rules the other out. A and B are **conditionally independent** given C when P(A ∩ B | C) = P(A | C) P(B | C). Neither kind of independence implies the other: two tests on the same patient can be conditionally independent given the patient's disease status, yet dependent overall, since a first positive result makes the disease, and so a second positive result, more likely.

### Practice Exercise

With two dice, let A be "the first die shows 6". Compute P(A | the sum is 7), P(A | the sum is 11) and P(A | the sum is 12), and say which condition leaves A independent.

> *Solution:* P(A) = 1/6. Of the 6 pairs with sum 7, only (6, 1) has a first 6, so P(A | sum 7) = 1/6 = P(A): these two events are independent. The sum is 11 for (5, 6) and (6, 5), so P(A | sum 11) = 1/2. The sum is 12 only for (6, 6), so P(A | sum 12) = 1. Only the sum 7 leaves A independent.

---

## 3. Bayes' Theorem and Base Rates

Writing P(H ∩ E) in two ways with the multiplication rule gives **Bayes' theorem**:

P(H | E) = P(E | H) P(H)/P(E), with P(E) = P(E | H) P(H) + P(E | not H) P(not H).

P(H) is the **prior**, P(E | H) the **likelihood** and P(H | E) the **posterior**. Dividing the theorem for H by the theorem for "not H" gives the **odds form**: the posterior odds equal the prior odds times the **likelihood ratio** P(E | H)/P(E | not H). When several pieces of evidence are conditionally independent given H and given "not H", their likelihood ratios multiply, and the order in which they arrive does not matter.

A test for a condition that affects 1% of people has a sensitivity P(+ | ill) of 99% and a false-positive rate P(+ | healthy) of 5%. Then P(+) = 0.99 · 0.01 + 0.05 · 0.99 = 0.0099 + 0.0495 = 0.0594, and P(ill | +) = 0.0099/0.0594 = 1/6. After a positive result from a 99% sensitive test, five chances in six remain that the person is healthy, because healthy people are 99 times as numerous. Ignoring the prior in this way is the **base-rate fallacy**.

### Practice Exercise

The same person takes a second test, conditionally independent of the first given the disease status, and it is positive too. Use the odds form to update.

> *Solution:* After the first test, P(ill) = 1/6, which is odds of 1 to 5. The likelihood ratio of a positive result is 0.99/0.05 = 19.8. The posterior odds are 19.8/5 = 3.96, so P(ill | two positives) = 3.96/4.96 = 99/124, about 0.80. Bayes' theorem with the prior 1/6 gives the same number.

---

## 4. Conjugacy: the Beta–Binomial Model

Let θ be an unknown probability of success. The **Beta(α, β)** distribution, for α, β > 0, has a density proportional to θ^(α−1) (1 − θ)^(β−1) on [0, 1]; Beta(1, 1) is the uniform distribution. After s successes and f failures, the likelihood is proportional to θ^s (1 − θ)^f, so the posterior is proportional to θ^(α+s−1) (1 − θ)^(β+f−1): it is Beta(α + s, β + f). A prior whose posterior stays in the same family is **conjugate**, and here α and β act as pseudo-counts of successes and failures. The posterior mean is (α + s)/(α + β + s + f), and Beta(a, b) has the variance ab/((a + b)² (a + b + 1)).

Because the update only adds counts, the posterior depends on the data only through s and f: updates **commute**, and one observation at a time gives the same posterior as all of them at once. The mean alone hides how much is known. Beta(2, 2) and Beta(501, 501) both have the mean 1/2, but their variances are 1/20 and about 2.5 · 10^-4. A rule that should keep exploring uncertain options, such as **Thompson sampling**, which draws θ from each posterior and picks the largest draw, needs the whole distribution, not only its mean.

### Practice Exercise

Start from Beta(1, 1) and observe 3 successes and 1 failure. Give the posterior, its mean and its variance.

> *Solution:* Beta(1 + 3, 1 + 1) = Beta(4, 2), with the mean 4/6 = 2/3 and the variance 4 · 2/(6² · 7) = 8/252 = 2/63.

---

## 5. Naive Bayes and Computing in Log Space

Bayes' theorem classifies: P(class c | x) is proportional to P(c) p(x | c). **Naive Bayes** assumes that the features x₁, …, x_p are conditionally independent given the class, so that p(x | c) = p(x₁ | c) · … · p(x_p | c). **Gaussian naive Bayes** models each p(x_j | c) as a normal density, with a mean and a variance per class estimated from the training data.

Two numerical points decide whether this works. First, a product of many small densities underflows, so the computation adds log-probabilities instead, and it normalises with the **log-sum-exp** trick: subtract the largest log score before exponentiating, which leaves the ratios unchanged and makes the largest term exp(0) = 1. Second, the variance formula E[x²] − E[x]² subtracts two nearly equal numbers when the mean is large compared with the spread, and the cancellation of MAT-003 destroys the difference. Subtracting the mean first, the **two-pass** formula mean((x − x̄)²), or Welford's one-pass update avoids it.

### Practice Exercise

Two classes have the log scores −1000 and −1002. What goes wrong if you exponentiate them directly, and what probabilities does log-sum-exp give?

> *Solution:* e^-1000 is below the smallest positive binary64 number, about 4.9 · 10^-324, so both exponentials round to 0 and the normalisation is 0/0. Subtracting the maximum gives exp(0) = 1 and e^-2, so the probabilities are 1/(1 + e^-2) ≈ 0.881 and 0.119.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**Bayesian rule weights** (`crates/ix-grammar/src/weighted.rs`). A `WeightedRule` starts from the [uniform Beta(1, 1) prior](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L31) and stores as its weight the [mean of the Beta distribution](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L13). [`bayesian_update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L57) is the conjugate update of §4, verbatim from lines 57–66:

```rust
pub fn bayesian_update(rule: &WeightedRule, success: bool) -> WeightedRule {
    let mut updated = rule.clone();
    if success {
        updated.alpha += 1.0;
    } else {
        updated.beta += 1.0;
    }
    updated.weight = updated.alpha / (updated.alpha + updated.beta);
    updated
}
```

- **The update is correct, and it commutes exactly.** The counts are whole numbers, exact in binary64 up to 2^53, so any order of the same observations gives the same α, β and weight, bit for bit. [`test_bayesian_update_success`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L145) checks one success from Beta(1, 1).
- **The selection sees only the mean, through a flat softmax.** [`softmax`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L83) gives each rule a probability proportional to exp(weight/T), and [`select_weighted`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L111) samples at T = 1. The weights that `bayesian_update` derives from a Beta prior lie between 0 and 1, so at T = 1 no such rule is more than e ≈ 2.72 times as likely as another: a rule of weight 0.99 against a rule of weight 0.01 is chosen with the probability 1/(1 + e^-0.98) ≈ 0.727. Beta(2, 2) and Beta(501, 501) give the same weight, so a rule tried twice and a rule tried a thousand times are treated alike; this is not Thompson sampling.
- **The MCP tool trusts its input.** The handler of `ix_grammar_weights` reads [`alpha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1559) and `beta` without checking that they are positive, as a Beta distribution requires, and accepts a [`weight`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1561) that may disagree with them, or even lie outside [0, 1]; the softmax uses that weight for every rule the request does not update. Its temperature [defaults to 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1601).

**Naive Bayes** (`crates/ix-supervised/src/naive_bayes.rs`). `GaussianNaiveBayes` works in log space and subtracts the [largest log score](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L101) before exponentiating, as §5 recommends. Its variance is the other formula of §5, verbatim from lines 52–59:

```rust
            let mean = class_data.mean_axis(ndarray::Axis(0)).unwrap();
            let var = class_data
                .mapv(|v| v * v)
                .mean_axis(ndarray::Axis(0))
                .unwrap()
                - &mean.mapv(|v| v * v);
            // Add small epsilon to avoid division by zero
            let var = var.mapv(|v| v.max(1e-9));
```

- **The variance cancels for offset features.** For class data c + (0, 1, 2), whose variance is 2/3, a transcription of these lines, with the sequential sums that `ndarray` uses for fewer than 8 rows, predicts the computed variance 0.671875 at c = 10^7, 2 at c = 10^8, and exactly 0 at c = 10^9. The `ndarray` crate's own `var_axis` uses Welford's update.
- **The floor is absolute.** A computed variance of 0 or less becomes 10^-9, whatever the scale of the feature, as with the absolute thresholds of MAT-003. At c = 10^9, it turns the computed 0 into 10^-9 where the true variance is 2/3, and the classifier becomes certain.
- **A missing class panics.** `fit` sets the number of classes to [the largest label plus one](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L37). If a label below it has no example, that class has no rows, `mean_axis` returns `None` for an empty axis, and the [`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L52) panics.
- **The test stays in the easy case.** [`test_gaussian_nb`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L127) fits six well-separated points near the origin and checks a training accuracy above 0.8. It checks no probability, no offset and no missing label.

**Through the MCP server.** The `naive_bayes` operation of `ix_supervised` converts the labels with [`as usize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2615), which truncates 1.5 to 1 and saturates −1 to 0, and it calls `fit` with no guard. The tool is declared as the skill [`supervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L665), and [every skill of the registry](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L320) becomes a registry-backed MCP tool, whose calls run while `dispatch_action` holds a global `Mutex`. Reading this code predicts that a panic in `fit` leaves the call without a response and poisons that mutex, after which every registry-backed call panics on the [`expect`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238) of the lock, until the server restarts. Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

For the classes c + (0, 1, 2) and c + (4, 5, 6) and the point c + 2.5, the exact posterior of the first class is 1/(1 + e^-3) ≈ 0.953. Using the computed variances above, predict what `predict_proba` returns at c = 10^8 and at c = 10^9.

> *Solution:* Both classes get the same computed variance v, so the normalising terms cancel and only the squared distances count: 1.5² = 2.25 to the first mean and 2.5² = 6.25 to the second, since the means c + 1 and c + 5 are computed exactly here. The gap between the log scores is (6.25 − 2.25)/(2v) = 2/v, which is 3 for the true v = 2/3. At c = 10^8, v = 2 gives the gap 1 and the probability 1/(1 + e^-1) ≈ 0.731. At c = 10^9, v = 10^-9 gives the gap 2 · 10^9, e^(−2 · 10^9) underflows to 0, and the probability is exactly 1. The first answer is too unsure and the second is certain; both come from the variance, not from the data. This is a prediction from reading the code, not a run; §7 checks it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Commutation.** Apply `bayesian_update` from Beta(1, 1) to the same 10^3 observations in three orders: as recorded, reversed, and all successes first. Prediction: identical α, β and weight, bit for bit.
2. **The flat softmax.** Build two rules with α, β = 99, 1 and 1, 99, whose weights are 0.99 and 0.01, and call `select_weighted` 10^5 times with a seeded generator. Prediction: the first rule's frequency is 0.727 within 0.005.
3. **The offset sweep.** For c = 10^0, …, 10^9, fit `GaussianNaiveBayes` on the classes c + (0, 1, 2) and c + (4, 5, 6), and call `predict_proba` at c + 2.5. Prediction: within 10^-4 of 0.9526 for c ≤ 10^6, about 0.9515 at c = 10^7, about 0.7311 at c = 10^8, and exactly 1 at c = 10^9. Subtracting the mean of the training feature, c + 3, from every value first gives 0.9526 at every c.
4. **The missing class.** Call `fit` with the labels (0, 0, 2, 2). Prediction: the panic "called `Option::unwrap()` on a `None` value". Then, in a disposable `ix-mcp` process, never a shared one, send `ix_supervised` the `naive_bayes` operation with those labels, followed by a well-posed `ix_stats` call. Prediction: neither call receives a response, and the server's error output shows that panic, then "middleware chain mutex poisoned".

### Practice Exercise

Step 2 predicts 0.727 within 0.005 for 10^5 draws. Where does that margin come from?

> *Solution:* Each draw picks the first rule with the probability p ≈ 0.727, independently of the others, so the count is binomial and the frequency has the standard deviation √(p (1 − p)/n) = √(0.727 · 0.273/10^5) ≈ 0.0014. Three standard deviations, about 0.0042, fit inside 0.005. This assumes that the generator behaves like independent uniform draws; the seed makes the run repeatable, not more random.

---

## 8. Common Pitfalls

- **Swapping P(E | H) and P(H | E).** The sensitivity of a test is not the probability of the disease after a positive result.
- **Ignoring the base rate.** The same evidence moves a rare hypothesis much less than a common one.
- **Treating disjoint events as independent.** Disjoint events of positive probability are always dependent.
- **Multiplying likelihood ratios of dependent evidence.** Two results multiply only if they are conditionally independent given each hypothesis.
- **Reporting a posterior mean without its spread.** The mean of Beta(2, 2) and Beta(501, 501) is the same; what is known is not.
- **Computing a variance as E[x²] − E[x]².** Subtract the mean first.
- **Multiplying many small probabilities directly.** Add their logarithms, and normalise with log-sum-exp.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Sample space** | The set Ω of possible outcomes; events are subsets of it that form a σ-algebra |
| **Kolmogorov's axioms** | P(A) ≥ 0, P(Ω) = 1, and additivity over disjoint events |
| **Conditional probability** | P(A \| B) = P(A ∩ B)/P(B), for P(B) > 0 |
| **Independence** | P(A ∩ B) = P(A) P(B): learning one event does not change the probability of the other |
| **Conditional independence** | P(A ∩ B \| C) = P(A \| C) P(B \| C) |
| **Bayes' theorem** | P(H \| E) = P(E \| H) P(H)/P(E) |
| **Likelihood ratio** | P(E \| H)/P(E \| not H), the factor by which evidence multiplies the odds of H |
| **Base-rate fallacy** | Judging P(H \| E) from P(E \| H) while ignoring the prior P(H) |
| **Conjugate prior** | A prior whose posterior stays in the same family, such as Beta for binomial data |
| **Naive Bayes** | A classifier that assumes the features are conditionally independent given the class |
| **Log-sum-exp** | Normalising log scores by subtracting their maximum before exponentiating |

---

## Self-Check Assessment

**1. Why can two disjoint events of positive probability not be independent?**
> P(A ∩ B) = P(∅) = 0, while P(A) P(B) > 0.

**2. A test has a sensitivity of 99%. Why is the probability of the disease after a positive result not 99%?**
> The posterior also depends on the prior and on the false-positive rate. With a prevalence of 1% and a false-positive rate of 5%, it is 1/6: most positive results come from the many healthy people.

**3. Why do Beta–Binomial updates commute?**
> The posterior Beta(α + s, β + f) depends on the data only through the numbers of successes s and failures f, which do not depend on the order of the observations.

**4. IX's `test_gaussian_nb` passes. What does it tell you about offset features?**
> Nothing: its points lie near the origin, where E[x²] − E[x]² loses nothing. The cancellation needs a mean that is large compared with the spread of the class.

**Pass criteria:** Derive consequences of Kolmogorov's axioms, compute conditional probabilities and check independence, apply Bayes' theorem in both forms with a base rate, update a Beta prior and state its mean and variance, normalise log scores with log-sum-exp, and trace what IX's rule weights and naive Bayes classifier compute and where they break.

---

## Research Basis

- A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung*, Springer, 1933: the axioms
- J. K. Blitzstein and J. Hwang, *Introduction to Probability*, 2nd ed., CRC Press, 2019: conditional probability, Bayes' theorem and the Beta–Binomial model
- E. T. Jaynes, *Probability Theory: The Logic of Science*, Cambridge University Press, 2003: probability as extended logic, and the odds form of Bayes' theorem
- D. Kahneman and A. Tversky, "On the psychology of prediction", *Psychological Review* 80, 1973: neglect of base rates
- W. R. Thompson, "On the likelihood that one unknown probability exceeds another in view of the evidence of two samples", *Biometrika* 25, 1933: Thompson sampling
- B. P. Welford, "Note on a method for calculating corrected sums of squares and products", *Technometrics* 4, 1962: a stable one-pass variance
- T. F. Chan, G. H. Golub and R. J. LeVeque, "Algorithms for computing the sample variance: analysis and recommendations", *The American Statistician* 37, 1983: why E[x²] − E[x]² fails
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
