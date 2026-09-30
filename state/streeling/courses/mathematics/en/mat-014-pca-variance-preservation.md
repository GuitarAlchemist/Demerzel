---
module_id: mat-014-pca-variance-preservation
department: mathematics
course: PCA as Variance Preservation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation, mat-009-estimation-uncertainty-sampling]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# PCA as Variance Preservation — What the Principal Components Keep, and What They Do Not Promise

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Derive the principal components as the directions of largest variance, and show that they are eigenvectors of the covariance matrix
- Show that the same components minimise the squared reconstruction error, and compute that error from the discarded eigenvalues
- Compute PCA from the SVD of the centred data, and explain why that route is more accurate than forming the covariance matrix
- Read an explained-variance ratio correctly, and explain how units change the components
- Say when the principal components are not unique or not stable, and tell PCA apart from whitening
- Trace what IX's PCA computes, and where its ratio, its stopping test and its saved state depart from these definitions

---

## 1. Variance Along a Direction

Let x₁, …, xₙ be observations in p dimensions with mean x̄, and let X_c be the n × p matrix whose rows are xᵢ − x̄. The **sample covariance matrix** is S = X_cᵀX_c/(n − 1), with the n − 1 of MAT-009. For a unit vector w, the **scores** zᵢ = wᵀ(xᵢ − x̄) have mean 0 and sample variance wᵀSw. The first **principal component** is the unit vector that maximises this variance.

S is symmetric and positive semidefinite, so by MAT-005 the maximum of the Rayleigh quotient wᵀSw over unit vectors is its largest eigenvalue λ₁, reached at an eigenvector q₁. The second component maximises wᵀSw over unit vectors orthogonal to q₁, which gives λ₂ and q₂, and so on. The components are orthonormal, the scores along different components are uncorrelated, and their variances are λ₁ ≥ λ₂ ≥ … ≥ λ_p ≥ 0. The total variance, the trace of S, equals λ₁ + … + λ_p: PCA rotates the data without changing its total spread.

### Practice Exercise

Data with covariance S = [[2, 1], [1, 2]]. What is the first principal component, and which fraction of the total variance does it carry? Compare with the variance along (1, 0).

> *Solution:* S (1, 1) = (3, 3) and S (1, −1) = (1, −1), so the eigenvalues are 3 and 1, for (1, 1)/√2 and (1, −1)/√2. The first component is (1, 1)/√2, with variance 3 out of a total of 4, a fraction 3/4. Along (1, 0) the variance is only S₁₁ = 2: the correlation between the two coordinates tilts the direction of largest spread to the diagonal.

---

## 2. The Best Low-Dimensional Approximation

Keeping k components replaces each observation by x̂ᵢ = x̄ + Σⱼ≤ₖ zᵢⱼ qⱼ, its orthogonal projection onto the affine subspace through x̄ spanned by q₁, …, qₖ. By Pythagoras, ‖xᵢ − x̄‖² = ‖x̂ᵢ − x̄‖² + ‖xᵢ − x̂ᵢ‖². Summed over the observations, the left side is (n − 1) times the trace of S, fixed by the data, so maximising the variance kept is the same as minimising the squared **reconstruction error** Σ‖xᵢ − x̂ᵢ‖². The minimum is (n − 1)(λₖ₊₁ + … + λ_p), the discarded eigenvalues. This is the Eckart–Young theorem of MAT-006, applied to X_c: no other k-dimensional subspace does better.

### Practice Exercise

Take the four points B: (2, 0), (−2, 0), (0, 1) and (0, −1). Compute S, the total squared distance to the mean, and the reconstruction error with one component.

> *Solution:* The mean is 0, and X_cᵀX_c = [[8, 0], [0, 2]], so S = diag(8/3, 2/3). The total squared distance is 4 + 4 + 1 + 1 = 10 = 3 (8/3 + 2/3). The first component is the first axis, and projecting onto it leaves the residuals of (0, 1) and (0, −1), with squared error 1 + 1 = 2 = 3 · 2/3, the discarded eigenvalue times n − 1. The component keeps 8/(8 + 2) = 0.8 of the variance.

---

## 3. PCA Through the SVD

Write the SVD of MAT-006 as X_c = UΣVᵀ. Then S = VΣ²Vᵀ/(n − 1): the principal directions are the right singular vectors, the variances are λᵢ = σᵢ²/(n − 1), and the scores are X_cV = UΣ. Computing PCA this way never forms X_cᵀX_c, whose condition number is the square of that of X_c: forming it can lose twice as many digits, and the small components lose them first (MAT-003, MAT-007). Every singular vector, and so every component, is defined only up to sign: two correct programs can return q and −q, and their results must be compared up to sign.

### Practice Exercise

Compute the singular values of the centred matrix of B, the variances they give, and the condition numbers of X_c and of S.

> *Solution:* The columns of X_c are (2, −2, 0, 0) and (0, 0, 1, −1). They are orthogonal, with norms √8 and √2, so σ₁ = √8 and σ₂ = √2, and λ = 8/3 and 2/3 as in §2. κ(X_c) = √8/√2 = 2, while κ(S) = (8/3)/(2/3) = 4 = κ(X_c)².

---

## 4. Explained Variance and Units

The **explained-variance ratio** of component i is λᵢ/(λ₁ + … + λ_p) = λᵢ/trace(S). Its denominator is the total variance, the sum of all p eigenvalues, not only of those kept; it can be computed from the diagonal of S without any eigenvalue. The ratio says how much of the spread a component carries, not whether it matters: a direction of small variance can be the one that separates two classes.

Covariance PCA depends on the units of each variable. Multiplying one variable by 100 multiplies its variance by 10^4 and pulls the first component towards it. **Standardised PCA** divides each variable by its standard deviation first, which amounts to the eigenvectors of the correlation matrix: it removes the units, and gives every variable the same weight by decision. Multiplying all variables by the same factor, on the other hand, must leave the components unchanged and multiply every variance by the square of the factor.

### Practice Exercise

Height has standard deviation 0.1 m and weight 10 kg, and they are uncorrelated. What is the first principal component, and its ratio? What changes if height is measured in centimetres?

> *Solution:* S = diag(0.01, 100), so the first component is the weight axis, with ratio 100/100.01 ≈ 0.9999. In centimetres, the height has standard deviation 10 and variance 100, so S = diag(100, 100): the two variances are equal, the first component is not unique, and each axis carries 1/2. Neither answer says which variable matters more; the units decided.

---

## 5. Uniqueness, Stability and Whitening

If λ₁ = λ₂, every unit vector in their two-dimensional eigenspace is a valid first component, and different correct programs return different ones. If λ₁ and λ₂ are close, the component exists but is fragile: by the Davis–Kahan theorem, a perturbation E of S, from noise or rounding, can rotate q₁ by an angle θ with sin θ up to about ‖E‖ divided by the **eigengap** λ₁ − λ₂. The power iteration of MAT-005 feels the same gap: the tangent of its angle to q₁ shrinks by the factor λ₂/λ₁ at each step, and **deflation**, which subtracts λ v vᵀ to find the next component, passes the remaining error on.

PCA does not **whiten**. Its scores keep the variances λᵢ; whitening divides the score along qᵢ by √λᵢ for each component with λᵢ > 0, so that the whitened data have the identity as covariance on those components; a direction of zero variance cannot be rescaled, and is dropped or regularised. Whitening puts the directions of smallest variance, often mostly noise, on the same footing as the largest.

### Practice Exercise

When does the first principal component fail to be unique? For S = diag(2/3, 2r²/3) with r = 0.999, power iteration starts from (1, 1)/√2. How many steps bring the tangent of its angle to the first axis below 10^-6?

> *Solution:* When λ₁ = λ₂: any unit vector of their eigenspace is then a valid first component. Here Sᵏ(1, 1) is proportional to (1, r²ᵏ), so the tangent after k steps is r²ᵏ, and the ratio per step is λ₂/λ₁ = r² = 0.998001. The condition r²ᵏ < 10^-6 needs k ≥ 6905 steps. After 1000 steps, the tangent is still r^2000 ≈ 0.135, an angle of about 7.7°.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of `fit`, `power_iteration`, `deflate` and `explained_variance_ratio` into Python, whose floats are IEEE binary64 like Rust's `f64`: they are predictions, and §7 proposes to check them.

**PCA** (`crates/ix-unsupervised`). `PCA` computes the covariance matrix [with n − 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L168), then extracts each component by [power iteration](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L103), with at most 1000 steps and the tolerance 10^-10 [set by `fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176), and removes it by [deflation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). MAT-005 has shown that the fixed start vector (1, …, 1)/√p can miss the dominant direction entirely; the findings below are different ones. The MCP tool `ix_pca` calls `PCA` through the handler [`pca`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L370), which [rejects](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L382) more components than features, and the ML pipeline uses it only when its `pca_components` option is [below the column count](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L539). The ratio and the fit read:

```rust
    /// Get explained variance ratios (proportion of total variance per component).
    pub fn explained_variance_ratio(&self) -> Option<Array1<f64>> {
        self.explained_variance.as_ref().map(|ev| {
            let total = ev.sum();
            if total > 0.0 {
                ev / total
            } else {
                ev.clone()
            }
        })
    }
```

```rust
    fn fit(&mut self, x: &Array2<f64>) {
        let n = x.nrows();
        let p = x.ncols();
        let k = self.n_components.min(p);

        // Compute column means
        let mean = x.mean_axis(Axis(0)).unwrap();

        // Center the data
        let mut centered = x.clone();
        for mut row in centered.rows_mut() {
            row -= &mean;
        }

        // Compute covariance matrix: (1/(n-1)) X^T X
        let cov = centered.t().dot(&centered) / (n.max(2) - 1) as f64;

        // Extract top-k eigenvectors via repeated power iteration + deflation
        let mut components = Array2::zeros((k, p));
        let mut explained_variance = Array1::zeros(k);
        let mut current_cov = cov;

        for i in 0..k {
            let (eigenvalue, eigenvector) = power_iteration(&current_cov, 1000, 1e-10);
            components.row_mut(i).assign(&eigenvector);
            explained_variance[i] = eigenvalue.max(0.0);
            current_cov = deflate(&current_cov, eigenvalue, &eigenvector);
        }

        self.components = Some(components);
        self.explained_variance = Some(explained_variance);
        self.mean = Some(mean);
    }
```

- **The ratio divides by the variance kept, not by the total.** `ev` holds only the k variances computed, so with one component the ratio is 1 as soon as the variance found is positive, whatever share of the total it carries. When that variance is 0, as for constant data or for points along (1, −1), which the start vector misses, the other branch returns [0]. On the ten points of Lindsay Smith's tutorial, the data of IX's skill test, the first component carries a fraction 0.963 of the variance, and the ratio reports 1; on the isotropic points (±1, 0) and (0, ±1), where the true fraction is 1/2, it also reports 1. With k = p the sum is the trace when power iteration finds every eigenvalue, as on the same ten points, where the ratio is right: 0.9632 and 0.0368. On the six points of MAT-005, whose dominant direction the start vector misses, it finds 2/5 and 0 against a trace of 8/5, and the ratio reads [1, 0]. The output schema promises the ["Fraction of total variance carried by each component"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L187). Two tests assert the ratio with one component, [above 0.99](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L237) and [above 0.9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L978): both pass on any data whose first variance found is positive.
- **The stopping test depends on the scale of the data.** Power iteration stops when the Rayleigh estimate [changes by less than 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L126), an absolute threshold. Multiplying the data by a power of two is exact in binary64, so every step of the fit scales exactly, except that comparison. On the four points B of §2:
  - at scale 1, the first call takes 11 steps and the first component is within 2 · 10^-5 degrees of the first axis;
  - at 2^-16, the first component is 0.9° off, the variances are about 2.66 s² and 0.30 s² instead of (8/3) s² and (2/3) s², and the ratio is 0.90 instead of 0.8;
  - from 2^-17 ≈ 7.6 · 10^-6 to 2^-24, the first Rayleigh estimate (5/3) s² is already below 10^-10, so each call stops after one multiplication. Both components are (4, 1)/√17, 14° from the first axis, with variances (5/3) s² and (15/34) s², and a ratio of 34/43 ≈ 0.791;
  - below that, the [guard on the norm of the product](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L120), 10^-15, stops the loop before the estimate is kept, and the call returns the variance 0 with the start vector: at 2^-25 for the second call only, so the ratio reads [1, 0], and from 2^-26 ≈ 1.5 · 10^-8 on for both calls, so it reads [0, 0].
- **Orthogonality is only as good as the stopping test.** Stopping on the eigenvalue leaves an error of a larger order in the vector, and deflation passes it on. On B, the dot product of the two components is about −7.2 · 10^-7 at scale 1, −1.1 · 10^-5 at 2^-4 and −7.3 · 10^-4 at 2^-10. [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288) requires [less than 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L306) on data whose two leading variances, 2.82 and 0.0133, are far apart; there the predicted dot product is −1.9 · 10^-8. None of the seven tests of `pca.rs` compares the components with an eigensolver or with the SVD.
- **Close eigenvalues run into the cap silently.** On (±1, 0) and (0, ±r), the variances are 2/3 and 2r²/3, and the iterates are proportional to (1, r²ᵏ) as in §5. The first call takes 50 steps for r = 0.9 and about 390 for r = 0.99. For r = 0.999 it stops at the cap of 1000 with the first component about 7.7° off, and nothing in the result says that the iteration did not converge.
- **A saved model can fail to load.** `fit` keeps [min(n_components, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L156) components, but `save_state` stores the [requested count](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L75), and `load_state` [reshapes with it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L89). With three components requested on two features, the state holds four numbers for a 3 × 2 shape, and loading it panics with ["PcaState components dimensions mismatch"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L90). The handler and the pipeline never request more components than features, but a direct caller of `PCA::new` is not protected.
- **The transform does not whiten.** It [projects the centred data](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L198) on the components, so the scores keep the variances λᵢ, as §5 describes.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Why does `explained_variance_ratio` return 1 whenever one component is requested and its variance is positive, and which denominator would make it a fraction of the total variance?

> *Solution:* With one component, `ev` has a single entry λ̂₁, and `ev / total` divides it by itself; only λ̂₁ = 0 escapes, and then the ratio is [0]. The fraction of the total variance needs λ̂₁/trace(S), where trace(S) is the sum of the p diagonal entries of the covariance matrix, which `fit` computes and then discards. On the ten points of Lindsay Smith's tutorial that gives 1.284/(1.284 + 0.0491) ≈ 0.963. A test that would catch the bug needs data whose first component carries a known fraction clearly below its threshold, such as the isotropic points, whose fraction is 1/2.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **The ratio.** Call the handler `pca` on the ten points of Lindsay Smith's tutorial with `n_components` 1, then 2, and on the isotropic points (±1, 0) and (0, ±1) with 1. Prediction: [1], then about [0.9632, 0.0368], then [1]; the trace of the covariance gives the true fractions 0.963 and 1/2 for the one-component cases.
2. **Against the SVD.** Fit `PCA` with two components on the ten points, and compute `svd` of the centred matrix. Prediction: the components equal the right singular vectors up to sign, the first within 10^-6 degrees and the second within 10^-5 degrees, and the variances equal σ²/9 within 10^-12.
3. **Scale.** Fit `PCA` with two components on B multiplied by 1, 2^-4, 2^-10, 2^-16, 2^-17, 2^-20, 2^-25 and 2^-26. Prediction: the values of §6, from a first component within 2 · 10^-5 degrees of the first axis at scale 1 to the same component (4, 1)/√17 twice at 2^-17 and 2^-20, then the ratios [1, 0] at 2^-25 and [0, 0] at 2^-26.
4. **Orthogonality.** On the data of `test_pca_components_orthogonal` and on B at the scales of step 3, compute the dot product of the two components. Prediction: about −1.9 · 10^-8 on the test data, and −7.2 · 10^-7, −1.1 · 10^-5 and −7.3 · 10^-4 on B at 1, 2^-4 and 2^-10.
5. **Close eigenvalues.** Fit on (±1, 0) and (0, ±r) for r = 0.9, 0.99 and 0.999. Prediction: the first component is within 0.002° of the first axis for r = 0.9, about 0.024° off for r = 0.99, and about 7.7° off for r = 0.999.
6. **Save and load.** Fit `PCA::new(3)` on the ten points, call `save_state`, then `load_state` inside `std::panic::catch_unwind`. Prediction: the fit and the transform succeed with two components, and `load_state` panics with the message of §6.

### Practice Exercise

For which scale factors s does the first call of power iteration stop after a single multiplication on B · s, and why does that make 2^-17 the first power of two to do so?

> *Solution:* The first estimate is compared with the initial value 0, so the loop stops at once when v₀ᵀ(s² S)v₀ < 10^-10, with v₀ = (1, 1)/√2 and v₀ᵀSv₀ = (8/3 + 2/3)/2 = 5/3. That means (5/3) s² < 10^-10, or s < √(6 · 10^-11) ≈ 7.75 · 10^-6. The power 2^-17 ≈ 7.63 · 10^-6 is below it, while 2^-16 ≈ 1.53 · 10^-5 is above. Far below, the call still stops after one multiplication, but through the guard on the norm of the product: ‖s²Sv₀‖ = (√34/3) s² < 10^-15 when s < √(3 · 10^-15/√34) ≈ 2.27 · 10^-8, so from 2^-26 ≈ 1.49 · 10^-8 on, with 2^-25 ≈ 2.98 · 10^-8 still above, the variance returned is 0. The data are the same up to units; only the absolute thresholds see the difference.

---

## 8. Common Pitfalls

- **Dividing by the variance kept.** The explained-variance ratio needs the trace of the covariance matrix; the sum of the retained eigenvalues makes a single component explain everything.
- **Mixing units in covariance PCA.** A variable with a large numerical spread dominates the first component; standardise when the units are arbitrary, and say that you did.
- **Reading variance as importance.** A small component can carry the signal that matters; the ratio measures spread, not relevance.
- **Comparing components without allowing for sign.** q and −q are the same component; compare |qᵀq′|, or fix a sign convention.
- **Trusting a component with a small eigengap.** When λ₁ ≈ λ₂, interpret the subspace they span, not each direction.
- **Forming XᵀX when the SVD is available.** It squares the condition number and loses the small components first.
- **Stopping on an absolute change.** A tolerance that ignores the size of the matrix makes the answer depend on the units; compare changes with the size of the eigenvalue.
- **Confusing PCA with whitening.** PCA rotates; whitening also rescales, and amplifies the directions of smallest variance.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Sample covariance matrix** | S = X_cᵀX_c/(n − 1), for the centred data matrix X_c |
| **Principal component** | A unit eigenvector of S; the first maximises the variance of the projected data |
| **Score** | The coordinate wᵀ(x − x̄) of an observation along a component |
| **Total variance** | The trace of S, equal to the sum of its eigenvalues |
| **Explained-variance ratio** | λᵢ divided by the total variance |
| **Reconstruction error** | The sum of squared distances from the observations to their projections, (n − 1) times the discarded eigenvalues |
| **Eckart–Young theorem** | The truncated SVD is the best approximation of given rank in the Frobenius norm |
| **Standardised PCA** | PCA of the correlation matrix, after dividing each variable by its standard deviation |
| **Eigengap** | λ₁ − λ₂, which controls how stable the first component is |
| **Deflation** | Subtracting λ v vᵀ from a matrix to remove an eigenpair already found |
| **Whitening** | Rescaling the scores by 1/√λᵢ, for the components with λᵢ > 0, so that their covariance becomes the identity |

---

## Self-Check Assessment

**1. A tool reports that one principal component explains 100% of the variance of a data set. What do you check before believing it?**
> Whether the ratio divides by the total variance. Compute the trace of the covariance matrix and compare it with the first eigenvalue; IX's `explained_variance_ratio`, for example, returns 1 whenever only one component is kept and its variance is positive. A genuine 100% means the centred data lie on a line.

**2. Two libraries return the first components (0.6, 0.8) and (−0.6, −0.8) on the same data. Is one of them wrong?**
> No. Eigenvectors and singular vectors are defined up to sign, so both describe the same component; the scores differ only in sign. Compare |qᵀq′|, which is 1 here.

**3. IX's PCA gives different components on the same measurements in centimetres and in kilometres. Is that a property of PCA?**
> No. Multiplying every variable by the same factor multiplies S by its square and leaves the eigenvectors unchanged. The difference comes from the absolute tolerance of 10^-10 in IX's power iteration, which the small variances in kilometres fall under. Rescaling a single variable, by contrast, does change the components.

**4. A sample gives λ₁ = 1.00 and λ₂ = 0.99. How far would you trust the direction of the first component?**
> Not far. The eigengap is 0.01, so by Davis–Kahan a perturbation of S of size 0.001 could already rotate the component by an angle whose sine is about 0.1. Report the plane of the first two components, and check its stability, for example by resampling.

**Pass criteria:** Derive the principal components from the variance, relate them to the reconstruction error and to the SVD of the centred data, compute an explained-variance ratio with the right denominator, explain the effect of units, sign and small eigengaps, tell PCA from whitening, and trace where IX's ratio, stopping test and saved state depart from the definitions.

---

## Research Basis

- K. Pearson, "On lines and planes of closest fit to systems of points in space", *Philosophical Magazine* 2, 1901: the best-fitting subspace
- H. Hotelling, "Analysis of a complex of statistical variables into principal components", *Journal of Educational Psychology* 24, 1933: principal components as directions of largest variance
- C. Eckart and G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1, 1936: the best low-rank approximation
- C. Davis and W. M. Kahan, "The rotation of eigenvectors by a perturbation. III", *SIAM Journal on Numerical Analysis* 7, 1970: the stability of eigenvectors and the eigengap
- I. T. Jolliffe, *Principal Component Analysis*, 2nd ed., Springer, 2002: PCA, explained variance and scaling
- L. I. Smith, "A tutorial on principal components analysis", 2002: the ten-point example used by IX's skill test
- G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013: the SVD, power iteration and deflation
- I. T. Jolliffe and J. Cadima, "Principal component analysis: a review and recent developments", *Philosophical Transactions of the Royal Society A* 374, 2016: standardised PCA and interpretation
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
