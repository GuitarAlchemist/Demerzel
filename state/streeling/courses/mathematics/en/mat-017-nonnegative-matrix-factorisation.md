---
module_id: mat-017-nonnegative-matrix-factorisation
department: mathematics
course: Non-negative Matrix Factorisation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-006-svd-low-rank-approximation, mat-012-iterative-optimisation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Non-negative Matrix Factorisation — Parts, Multiplicative Updates and Factors That Are Not Unique

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- State the NMF problem, and bound its error from below with the SVD
- Derive the Lee–Seung multiplicative updates as scaled gradient steps, and say what their monotonicity proves and what it does not
- Show that NMF factors are defined at best up to scaling and order, and build exact factorisations that differ by more
- Explain why an absolute tolerance on the reconstruction error makes a stopping rule depend on the units of the data
- Tell identified parts from an arbitrary choice among equally good ones, with several seeds and a separable control
- Trace what IX's `NonNegativeMatrixFactorization` guarantees, and where its documentation, its tests and its stopping rule promise more than the code delivers

---

## 1. The Problem

Let V be an n × p matrix with nonnegative entries: n samples, p features. **Non-negative matrix factorisation** (NMF) looks for an n × k matrix W and a k × p matrix H, both with nonnegative entries, that minimise ‖V − WH‖_F². Paatero and Tapper (1994) introduced it as positive matrix factorisation, and Lee and Seung (1999) made it popular. Row i of V is approximated by Σ_c W_ic h_c, a combination of the k rows h_c of H with nonnegative weights: the rows of H are the **parts**, and W says how much of each part each sample contains. Nothing can be subtracted, so no part can cancel another. This is why NMF of face images gives localised features such as noses and eyes, and NMF of word counts gives topics, while the SVD of MAT-006 gives components with mixed signs.

The product WH has rank at most k, so the Eckart–Young–Mirsky theorem of MAT-006 bounds the error of every factorisation, nonnegative or not: ‖V − WH‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …). NMF can reach this bound only when one of the best rank-k approximations is a product of nonnegative factors of inner dimension k; when σₖ > σₖ₊₁ there is only one, the truncated SVD V_k. For k ≤ 2 this happens exactly when one of them has no negative entry, because a nonnegative matrix of rank at most 2 always has nonnegative factors of the same inner dimension (Cohen and Rothblum 1993). For larger k it can fail even for a nonnegative best approximation: the **nonnegative rank** can exceed the rank. The problem is also hard in general: Vavasis (2009) showed that deciding whether V has an exact NMF of inner dimension rank(V) is NP-hard.

For a fixed W, the objective is convex in H: it is a nonnegative least-squares problem, like those of MAT-007. The same holds in W for a fixed H, but not in both together. Already for 1 × 1 matrices, f(w, h) = (1 − wh)² is 0 at (2, 1/2) and at (1/2, 2), but (1 − 25/16)² = 81/256 at their midpoint (5/4, 5/4), where a convex function would be at most 0. The minimisers are not isolated points either, since (W, H) and (WD, D⁻¹H) give the same product (§3). Practical algorithms alternate between the two convex subproblems, and what they find depends on where they start.

### Practice Exercise

IX accepts every k from 1 to min(n, p). Show that k = min(n, p) is trivial.

> *Solution:* If k = p ≤ n, take W = V and H = I_p: both are nonnegative and WH = V, with error 0. If k = n ≤ p, take W = I_n and H = V. The bound of this section agrees, since σₖ₊₁ = 0 when k ≥ rank(V). NMF says something about the data only for k < min(n, p), where the samples must share parts.

---

## 2. Multiplicative Updates

The gradient of f(W, H) = ½‖V − WH‖_F² with respect to H is WᵀWH − WᵀV. Lee and Seung (2001) take a gradient step with a separate step size for each entry, η_ij = H_ij/(WᵀWH)_ij, and the step turns into a multiplication: H_ij − η_ij(WᵀWH − WᵀV)_ij = H_ij (WᵀV)_ij/(WᵀWH)_ij. In the same way, W_ij becomes W_ij (VHᵀ)_ij/(WHHᵀ)_ij. Each factor is a ratio of nonnegative numbers, so W and H stay nonnegative without any projection, and there is no step size to tune, where in MAT-012 the step size decides everything.

Lee and Seung prove that neither update increases ‖V − WH‖_F. At the current H they build a quadratic upper bound of f with a diagonal Hessian, whose entries are (WᵀWH)_a/H_a. The bound touches f at the current point, and its minimiser is exactly the update: an **auxiliary function**, or majorise–minimise step. The proof gives a non-increasing sequence of errors, bounded below by 0, so the errors converge. It does not show that the iterates converge, nor that their limit is a stationary point. Lin (2007) pointed out that no proof of convergence to a stationary point existed for these updates, and proposed modified updates whose limit points he proved to be stationary. Even a stationary point is only a necessary condition for a local minimum.

The update multiplies each entry, so an entry equal to 0 stays 0 whatever the gradient says, as long as the ratio is defined. Starting values must therefore be positive. If V has no zero row and no zero column, positive factors keep the numerators (WᵀV)_ij and (VHᵀ)_ij positive, so every entry stays positive, and an entry whose optimal value is 0 is approached gradually and never reached. A zero column of V, by contrast, makes the matching column of WᵀV zero, and the first update sets that column of H exactly to 0. The next exact update of that column is then 0 · 0/0, since (WᵀWH)_ij vanishes with the column of H: it is undefined, and the usual convention, which IX's ε in the denominators implements (§6), keeps it at 0. A zero row of V does the same to the matching row of W, through (VHᵀ)_ij and (WHHᵀ)_ij. For a worked example, take V = [[2, 1], [1, 2]], k = 1, W₀ = (1, 1)ᵀ and H₀ = (1, 1). Then W₀ᵀV = (3, 3) and W₀ᵀW₀H₀ = (2, 2), so H₁ = (3/2, 3/2); then VH₁ᵀ = (9/2, 9/2)ᵀ and W₀H₁H₁ᵀ = (9/2, 9/2)ᵀ, so W₁ = W₀. The error falls from ‖V − W₀H₀‖_F = √2 ≈ 1.414 to ‖V − W₁H₁‖_F = 1. The singular values of V are 3 and 1, so 1 is the bound of §1: one step reached the optimum.

### Practice Exercise

Let V = uvᵀ with u and v positive vectors, and k = 1. Show that one pair of updates, from any positive w and h, gives W₁H₁ = V exactly.

> *Solution:* wᵀV = (w · u)vᵀ and wᵀwh = ‖w‖²h, so H₁ = ((w · u)/‖w‖²) v: the entries of h cancel, and H₁ = αv with α > 0. Then VH₁ᵀ = α‖v‖²u and wH₁H₁ᵀ = α²‖v‖²w, so W₁ = u/α, and W₁H₁ = uvᵀ. The error is 0 after the first pair of updates, whatever the start; IX's rank-one test uses such a matrix (§6).

---

## 3. Factors That Are Not Unique

If WH = V, then (WD)(D⁻¹H) = V for every invertible k × k matrix D; the only question is whether WD and D⁻¹H stay nonnegative. For a positive diagonal D, a permutation, or a product of the two, they always do: NMF cannot tell the size of a part from the weight given to it, nor the order of the parts. These monomial matrices are the only nonnegative matrices whose inverse is also nonnegative. Before comparing runs, one therefore scales each part, for instance to sum 1, and matches the parts.

For particular factors, other matrices keep both factors nonnegative, and then the factorisation is not unique even after scaling. Take X = [[2, 1], [1, 2]], W = I and H = X, and D = [[1, a], [0, 1]], whose inverse is [[1, −a], [0, 1]]. Then W_a = [[1, a], [0, 1]] and H_a = [[2 − a, 1 − 2a], [1, 2]] satisfy W_aH_a = X, and both are nonnegative exactly when 0 ≤ a ≤ 1/2: a continuum of exact factorisations, related by no scaling or reordering. At a = 1/2, W = [[1, 1/2], [0, 1]] and H = [[3/2, 0], [1, 2]].

When rank(V) = k, every exact factorisation has the form (WQ, Q⁻¹H) for an invertible Q, because the columns of any other W must span the column space of V. Suppose that W contains a positive multiple of each unit row, so each part appears pure in some sample, and that H contains a positive multiple of each unit column, so each part has a feature that no other part uses. The rows of WQ then include multiples of the rows of Q, so Q ≥ 0, and the columns of Q⁻¹H include multiples of the columns of Q⁻¹, so Q⁻¹ ≥ 0: Q is monomial, and the factorisation is unique up to scaling and order. In the example above, W = I meets the first condition, but H = X has no unit column, which leaves room for the shear. Donoho and Stodden (2004) gave conditions of this kind for NMF to recover the true parts. Arora, Ge, Kannan and Moitra (2012) showed that the second condition alone, which they call separability, makes NMF computable in polynomial time.

### Practice Exercise

Show that (WD)(D⁻¹H) = WH for every invertible D. Why does a positive diagonal D keep both factors nonnegative, while a diagonal D with a negative entry does not?

> *Solution:* By associativity, (WD)(D⁻¹H) = W(DD⁻¹)H = WH. A diagonal D = diag(d_1, …, d_k) multiplies column c of W by d_c and row c of H by 1/d_c. When every d_c is positive, no sign changes. When d_c < 0, column c of W and row c of H change sign, so one of them acquires a negative entry unless both are zero, which happens only when part c is unused. The factorisation is therefore defined at best up to positive scalings and reorderings of the parts.

---

## 4. Stopping Rules and Units

Multiply V by c > 0 and start from √c W₀ and √c H₀. In the H update, (√cW)ᵀ(cV) = c^(3/2) WᵀV and (√cW)ᵀ(√cW)(√cH) = c^(3/2) WᵀWH, so the ratio is unchanged and the new H is √c times the old one; the W update behaves the same way. By induction, every iterate on cV is √c times the corresponding iterate on V, and every error is c times as large. The updates do not depend on the units of the data.

A stopping rule can bring the units back. A rule that stops when the error changes by less than τ, in absolute terms, becomes on cV the rule with tolerance τ/c on V: multiplying the data by 1000, as when metres become millimetres, makes the rule 1000 times stricter, and dividing them by 1000 makes it 1000 times looser. A relative rule, such as |e_t − e_(t+1)| ≤ τ e_t, gives the same number of iterations in every unit, and so does a tolerance on a stationarity measure taken relative to its first value, the kind of rule Lin (2007) uses. As in MAT-012, a small change certifies little: it proves no minimum and, after §3, nothing about the factors, since the error is flat along whole families of factorisations.

Additive constants break the equivariance in the same way. A floor on a starting value, or an ε added to a denominator, is a length in the units of the data, and matters when the data are small compared with it. IX has both (§6).

### Practice Exercise

Complete the argument for the W update: if W_t and H_(t+1) on cV are √c times the iterates on V, show that the W update on cV gives √c W_(t+1). What changes when ε is added to the denominators?

> *Solution:* (cV)(√cH)ᵀ = c^(3/2) VHᵀ and (√cW)(√cH)(√cH)ᵀ = c^(3/2) WHHᵀ, so the ratio is unchanged, and √cW times it is √c W_(t+1). With ε, the denominator becomes c^(3/2)(WHHᵀ)_ij + ε, and the ratio changes by a relative amount of the order of ε/(c^(3/2)(WHHᵀ)_ij): negligible for ordinary data, but not once c^(3/2)(WHHᵀ)_ij approaches ε.

---

## 5. Seeds, Parts and a Separable Control

IX's test `test_nmf_error_decreases` (§6) factorises V = [[1, 0, 2], [0, 3, 1], [2, 1, 0], [1, 2, 1]] with k = 2 and 300 iterations. By §1, no factorisation of inner dimension 2 has an error below σ₃ ≈ 1.699561. The truncated SVD V₂ has the smallest entry about 0.158, so by Cohen and Rothblum it has nonnegative factors of inner dimension 2, which reach the bound. Every factorisation that reaches the bound has WH = V₂, since the best rank-2 approximation is unique when σ₂ > σ₃. And since V₂ has no zero entry, there is room to tilt its parts as in the shear of §3: V₂ has a whole family of optimal factorisations.

The transcription of IX's code (§6) predicts, for seeds 42, 0 and 100, the errors 1.6996, 1.6997 and 1.6997 after 51, 46 and 56 iterations, all within 0.0002 of the bound. Scale each part to sum 1, and call part B the one with the most weight on the second feature. It is (0.035, 0.793, 0.173), (0.031, 0.789, 0.180) and (0.000, 0.832, 0.167), and the weight of sample 1, the row (1, 0, 2), on part B is 0.174, 0.011 and 0.000. The three runs agree on the error, and disagree on whether sample 1 contains part B.

Early stopping does not explain it. With the tolerance set to 0 and 20,000 iterations, the three runs are predicted to end with errors that round to 1.699561, the bound, and with the weights 0.185, 0.007 and 0.000 for sample 1. A finite run does not show that the iterates converge, or that their limits attain the bound (§2); it shows that after 20,000 iterations the three runs are still three different factorisations, all within rounding of the bound.

A **separable control** is data whose factorisation is known to be unique. Take V = [[1, 0, 2], [0, 1, 1], [1, 1, 3], [2, 1, 5]], which is WH for W = [[1, 0], [0, 1], [1, 1], [2, 1]] and H = [[1, 0, 2], [0, 1, 1]]. W contains both unit rows and H both unit columns, so by §3 the factorisation is unique up to scaling and order, with the parts (1/3, 0, 2/3) and (0, 1/2, 1/2) once scaled to sum 1. With IX's default of 200 iterations, seeds 42, 0 and 100 are predicted to return both parts within 0.01, with errors of 0.018, 0.027 and 0.018. None of the three runs stops before the cap: entries that should be 0 approach 0 slowly (§2), and the last change, over the four iterations from the check after iteration 196 to the final one after iteration 200, stays above 10^-4, at 0.00044, 0.00096 and 0.00040.

The two cases pull apart two things one would like a stop to mean. On the test matrix, IX's rule stops while the parts are arbitrary; on the control, it never stops while the parts are right. Reading meaning into the parts needs evidence that they are identified, such as agreement across seeds after scaling and matching, not a stop or a small error.

### Practice Exercise

In the second paragraph, why can the three runs disagree on the weight of sample 1 while agreeing on the error?

> *Solution:* The three products are all close to V₂, the unique best rank-2 approximation, so the three errors are close to σ₃. The product does not determine the factors: V₂ has no zero entry, so, as with the shear of §3, its parts can be tilted within the plane they span while both factors stay nonnegative. Along such a family the product, and so the error, stays the same, while the weight of each sample on each part changes; the weight of sample 1 on part B is one of the quantities that change.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of `fit_transform` and `transform` into Python, with a replica of rand 0.9's `StdRng` (ChaCha12, seeded through PCG32) that reproduces the crate's own draws. Python's floats are IEEE binary64 like Rust's `f64`; the sums can differ from ndarray's in the last bits, far below the margins of the values stated. These numbers are predictions, and §7 proposes to check them.

**NMF** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L105) rejects [k = 0 and k > min(n, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L112) and [negative entries](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119). It draws W and then H from [`StdRng::seed_from_u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L129), runs the updates of §2 with ε in the denominators, and measures the error with [`frobenius_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L241), the norm itself, not its square, every fifth iteration and after the last one allowed. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L183) keeps H, draws a new W [from the same seed](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L202) and runs [50 updates of W](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L213). The defaults are [200 iterations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L74) and [seed 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L77). The module is a library only: [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L11) exports it and no other Rust file in the repository refers to it, so no MCP tool or pipeline stage offers NMF. The initialisation and the stopping test read:

```rust
        let mean = v.mean().unwrap_or(1.0).abs().max(1e-3);
        let scale = (mean / self.n_components as f64).sqrt();
        let mut rng = StdRng::seed_from_u64(self.seed);
        let mut w = Array2::<f64>::zeros((n_samples, self.n_components));
        for e in w.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
        let mut h = Array2::<f64>::zeros((self.n_components, n_features));
        for e in h.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
```

```rust
            if iter % 5 == 0 || iter == self.max_iterations - 1 {
                let err = frobenius_distance(v, &w.dot(&h));
                final_err = err;
                if convergence.converged((prev_err - err).abs()) {
                    break;
                }
                prev_err = err;
            }
```

- **The stopping rule depends on the units of the data.** The [tolerance of 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L75), documented as a ["Convergence tolerance on the Frobenius reconstruction error"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L55), is compared by [`converged`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/convergence.rs#L46), with a strict `<`, to the change in the error between two checks. The checks come after iterations 1, 6, 11 and so on, and after the last iteration allowed, so the first change spans one iteration and the later ones five, except that a run reaching the default cap of 200 ends with a change over four, from iteration 196 to 200. The starting scale s = √(mean/k) grows like √c, so as long as the mean stays above the floor of 10^-3, the whole run is equivariant (§4) up to the effect of ε, which is negligible unless the entries approach it, and the tolerance is absolute. On the matrix of §5 with seed 42, multiplied by 0.001, 1 and 1000, the transcription predicts 16, 51 and 86 iterations, with errors of 1.7360, 1.6996 and 1.69956 times the factor, against the bound 1.699561.
- **The documentation promises more than the updates are known to give.** The module documentation says that convergence is ["guaranteed (not necessarily to a global optimum, but to a local one)."](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L24) Lee and Seung prove that the exact updates never increase the error. That the iterates converge to a stationary point, let alone a local minimum, is not proven for these updates (§2), and IX's stopping rule tests for neither (§4, §5). The transcription agrees with the monotonicity: over 30 seeds on each of the three test matrices of sizes 3 × 3, 4 × 3 and 4 × 4 with k = 2, 300 iterations each, the largest rise from one iteration to the next is about 6.7 · 10^-16, a rounding error.
- **The error test does not test the updates.** [`test_nmf_error_decreases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L320) never compares the final error with the initial one. It asserts that the error is [below](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L332) the [sum of the entries](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L330), Σvᵢⱼ = 14. The zero factorisation already has the error ‖V‖_F = √26 ≈ 5.10, and ‖V‖_F ≤ Σvᵢⱼ for every nonnegative V. Before any update, the error is below 5.49 for every seed (see the exercise below), so the test would still pass with the update loop deleted. Lee and Seung's monotonicity covers the exact updates, not IX's, which add ε to the denominators and can raise the error by amounts of the order of ε: from V = W = H = 1, an exact factorisation, one update of H gives the error ε/(1 + ε). That the assertion still holds after the updates for every seed is therefore not proven here; the transcription predicts it for the 200 seeds tried, with no error above 4.9 at any check and every final error below 1.7. With seed 42, the transcription predicts an initial error of 4.545 and a final one of 1.6996, after 51 iterations.
- **The rank-one test is solved by the first update.** [`test_nmf_rank_one_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L258) and the module's example use V = uuᵀ with u = (1, 2, 3). By the exercise of §2, the first pair of updates reproduces it from any positive start, up to the effect of ε. The first check sees a change equal to the whole initial error, about 12.363 for seed 42, and cannot stop; the second one can. The transcription predicts 6 iterations for every seed, and an error of about 4 · 10^-11 for seed 42, far below the [threshold of 0.1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L267). The test checks a real property, but not the iteration: any method that makes one exact rank-one step passes it. The example asserts only [the number of columns](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L39).
- **Nothing warns that the parts are not unique.** The documentation recommends NMF because it ["produces a parts-based"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L7) ["decomposition that is often more interpretable"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L8). The seed has a [builder](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L97), but no test varies it and no document mentions §3. §5 gives the predicted consequence on the error test's own matrix: weights of 0.174, 0.011 and 0.000 for sample 1 on the same part, from seeds 42, 0 and 100.
- **NaN and +∞ entries are accepted.** The [check](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119) `x < 0.0` is false for NaN and for +∞, so a matrix with such an entry passes it; −∞ is rejected. Its mean is NaN, and the [floor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L127) turns it into 10^-3, because Rust's `f64::max` returns the other operand when one is NaN. After the first iteration every entry of W is NaN, and after the second every entry of H too; the change is NaN, `converged` never holds, and the transcription predicts all 200 iterations, then `Ok`, with W, H and the error all NaN. An entry equal to +∞ ends the same way, with every entry of W and H NaN from the first iteration on: the mean is then +∞, which the floor keeps, so the starting factors are not finite. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L196) has the same check.
- **Other gaps.** [`test_nmf_transform_matches_shape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L302) checks [shapes and signs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L316) only, and no test compares `transform` on the training data with the W returned by `fit_transform`. There is no structured initialisation such as NNDSVD, no restart over seeds, no relative tolerance, no regularisation, no objective other than the Frobenius norm, and no flag for a run that reached the cap: [`n_iter`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L66) equal to `max_iterations` is the only sign.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

IX's error test starts from W₀ and H₀ with entries u · s + ε, where u is uniform on [0, 1) and s = √(mean/k). Show that before any update, the error is below 5.49 whatever the seed.

> *Solution:* The 12 entries sum to 14, so the mean is 7/6 and s² = 7/12 for k = 2. Each entry of W₀H₀ is a sum of two products of numbers in [ε, s + ε), so it lies strictly between 0 and 2(s + ε)² = 7/6 + δ, where δ = 4sε + 2ε² is below 10^-9 for IX's ε of 10^-10. An entry v of V therefore differs from the matching entry of W₀H₀ by less than 7/6 + δ for each of the three zeros, and by less than v for the five ones, the three twos and the three. The squared error is below 3(7/6 + δ)² + 5 + 12 + 9 = 1083/36 + 7δ + 3δ², and 1083/36 ≈ 30.083 while 5.49² ≈ 30.140, so the error is below 5.49, less than half of 14.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **The error test's matrix.** Call `fit_transform` with k = 2, 300 iterations and seed 42 on the matrix of §5. Prediction: `n_iter` equal to 51 and an error of 1.6996, within 10^-4.
2. **A monotone error.** For i = 1, …, 300, repeat step 1 with `with_tolerance(0.0)` and `with_max_iterations(i)`. Since `converged` is a strict `<`, each run stops after exactly i iterations and reports the error after i. Prediction: the error never rises by more than 10^-15, and decreases toward 1.699561.
3. **Seeds.** Repeat step 1 with the seeds 0 to 9, scale each part to sum 1, and find the weight of sample 1 on part B. Prediction: every error within 0.00024 of 1.699561, and weights ranging from 0.000 to 0.112.
4. **Units.** Repeat step 1 on 0.001 V and on 1000 V. Prediction: 16 and 86 iterations, against 51 for V, with errors of 1.7360 and 1.69956 times the factor.
5. **Separable control.** Repeat step 3 on the control of §5 with the default of 200 iterations. Prediction: every run uses all 200 iterations, and both parts agree with (1/3, 0, 2/3) and (0, 1/2, 1/2) within 0.01.
6. **A NaN entry.** Replace one entry of the matrix of §5 by NaN, and call `fit_transform` with k = 2 and the default settings. Prediction: `Ok`, `n_iter` equal to 200, and W, H and the error all NaN.

### Practice Exercise

In step 4, why does 0.001 V stop after 16 iterations with a higher error, when its iterates are, up to the effect of ε, those of V scaled?

> *Solution:* On 0.001 V every error is 0.001 times the error on V (§4), up to the effect of ε: IX adds the same ε to the starting entries and to the denominators whatever the units, which breaks the exact scaling, but at 10^-10 it is negligible here. The tolerance of 10^-4 therefore amounts to 0.1 in the units of V. In those units, the transcription predicts changes of 2.363, 0.208, 0.143 and 0.094 at the checks after iterations 1, 6, 11 and 16. The change 0.094 is the first below 0.1, so the run stops after 16 iterations, at 1.7360 in the units of V, while the run on V goes on until the change falls below 10^-4, after 51 iterations. A relative tolerance would give the same answer in both units.

---

## 8. Common Pitfalls

- **Reading meaning into the parts of a single run.** Run several seeds, scale and match the parts, and report what agrees.
- **Taking a stop for a solution.** A change below a tolerance proves no minimum and identifies no factors; on the test matrix of §5, the stop comes while the parts are arbitrary.
- **Using an absolute tolerance on data in arbitrary units.** Rescale the data to a fixed norm, or use a relative rule.
- **Choosing k by the error alone.** The best error can only fall as k grows, and it reaches 0 at k = min(n, p), where the factorisation is trivial.
- **Starting an entry at 0.** Multiplicative updates never move it; start from positive values.
- **Comparing factors column by column.** Scale and order are arbitrary; scale each part and match the parts first.
- **Writing a test that the zero factorisation passes.** Compare with the initial error, or with the bound of §1.
- **Passing NaN to a fit that only rejects negative entries.** Check that every entry is finite before fitting.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Non-negative matrix factorisation (NMF)** | Approximating V ≥ 0 by WH with W ≥ 0 and H ≥ 0 of inner dimension k |
| **Part** | A row of H; each sample is a nonnegative combination of the parts |
| **Multiplicative update** | A gradient step with entrywise step sizes that becomes a multiplication by a ratio of nonnegative terms |
| **Auxiliary function** | An upper bound of the objective that touches it at the current point, so that minimising it cannot increase the objective |
| **Nonnegative rank** | The smallest k for which V = WH exactly with nonnegative factors; it is at least rank(V) |
| **Scaling ambiguity** | (WD)(D⁻¹H) = WH for every positive diagonal D |
| **Identifiability** | The property that V determines the factors, up to scaling and order |
| **Separability** | The condition that each part has a feature that no other part uses |
| **Absolute tolerance** | A stopping threshold stated in the units of the data |
| **Separable control** | Data whose factorisation is known to be unique, on which a method must return the same parts from every seed |

---

## Self-Check Assessment

**1. A colleague shows the topics of one NMF run with seed 42, and interprets topic 3. What do you ask for?**
> Runs with other seeds, with the topics scaled and matched, to see whether topic 3 comes back; the errors of those runs, and the bound of §1; the number of iterations against the cap; and the same pipeline on a separable control, where the topics must agree across seeds. As §5 shows, runs whose errors agree within 0.0002 can disagree on which samples contain a part.

**2. Why can a multiplicative update not move an entry that is 0, and what does that imply for the start?**
> The update multiplies the entry by a ratio, so 0 stays 0 whatever the gradient says, as long as the ratio is defined (§2). The start must therefore be positive, as IX's small offset ε ensures, and, unless V has a zero row or column, an entry that should end at 0 approaches it only gradually, which slows the stop, as on the separable control of §5.

**3. The same measurements take 86 iterations in IX's NMF when expressed in grams, 51 in kilograms and 16 in tonnes. Which run is right?**
> None is privileged: the updates are the same up to scale, ε aside, and only the stopping rule differs, because IX's tolerance of 10^-4 is absolute. In tonnes it amounts to a tolerance 1000 times looser than in kilograms. Rescale the data to a fixed norm, or use a relative rule, and report the error relative to ‖V‖_F.

**4. `test_nmf_error_decreases` asserts that the final error is below the sum of the entries. What would a meaningful assertion look like?**
> One that fails when the updates do not work: for instance, that the final error is below the initial one by a margin, or within a small factor of the bound σ₃ of §1, 1.699561 on the test's matrix. The current assertion holds even for the zero factorisation, whose error is √26 ≈ 5.10, below 14.

**Pass criteria:** State the NMF problem and its SVD bound, derive the multiplicative updates and say what their monotonicity proves, show why the factors are not unique and when they are, explain why an absolute tolerance depends on the units, design a seed comparison with a separable control, and trace where IX's documentation, tests and stopping rule promise more than the code delivers.

---

## Research Basis

- J. E. Cohen and U. G. Rothblum, "Nonnegative ranks, decompositions, and factorizations of nonnegative matrices", *Linear Algebra and its Applications* 190, 1993: nonnegative rank, and the rank-2 case
- P. Paatero and U. Tapper, "Positive matrix factorization: a non-negative factor model with optimal utilization of error estimates of data values", *Environmetrics* 5, 1994: the problem
- D. D. Lee and H. S. Seung, "Learning the parts of objects by non-negative matrix factorization", *Nature* 401, 1999: parts-based representations
- D. D. Lee and H. S. Seung, "Algorithms for non-negative matrix factorization", *Advances in Neural Information Processing Systems* 13, 2001: multiplicative updates and their monotonicity
- D. Donoho and V. Stodden, "When does non-negative matrix factorization give a correct decomposition into parts?", *Advances in Neural Information Processing Systems* 16, 2004: conditions for unique parts
- C.-J. Lin, "On the convergence of multiplicative update algorithms for nonnegative matrix factorization", *IEEE Transactions on Neural Networks* 18, 2007: stationarity of the limit, and modified updates
- C. Boutsidis and E. Gallopoulos, "SVD based initialization: a head start for nonnegative matrix factorization", *Pattern Recognition* 41, 2008: NNDSVD initialisation
- S. A. Vavasis, "On the complexity of nonnegative matrix factorization", *SIAM Journal on Optimization* 20, 2009: NP-hardness
- S. Arora, R. Ge, R. Kannan and A. Moitra, "Computing a nonnegative matrix factorization — provably", *Proceedings of the ACM Symposium on Theory of Computing*, 2012: separability
- N. Gillis, *Nonnegative Matrix Factorization*, SIAM, 2020: algorithms, identifiability and stopping rules
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
