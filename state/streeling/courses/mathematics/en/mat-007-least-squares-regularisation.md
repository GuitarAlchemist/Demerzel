---
module_id: mat-007-least-squares-regularisation
department: mathematics
course: Least Squares, Regularisation and Identifiability
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-003-floating-point-conditioning, mat-006-svd-low-rank-approximation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Least Squares, Regularisation and Identifiability — When the Data Cannot Pin the Parameters Down

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Derive the normal equations from the orthogonality of the residual, and solve a small least-squares fit by hand
- Say when the parameters of a linear model are identifiable, and find the minimum-norm solution when they are not
- Explain why solving the normal equations loses twice as many digits as a solve through the SVD, and why centering a feature helps
- Write the ridge (Tikhonov) solution with the SVD, and explain why it is unique for every positive λ
- Say what IX's linear regression computes, where it fails, and what its failure does to the processes that call it

---

## 1. The Least-Squares Problem

A linear model predicts y from features: y ≈ X w, where the n × p **design matrix** X has one row per observation and one column per parameter. With more observations than parameters, the equations X w = y usually have no solution. **Least squares** chooses the w that minimises the length of the **residual** r = y − X w, that is ‖X w − y‖₂.

The vectors X w fill the column space of X, and the closest one to y is its orthogonal projection: the residual of the best w is orthogonal to every column of X. That is Xᵀ(y − X w) = 0, the **normal equations**

XᵀX w = Xᵀy.

Conversely, any w that satisfies them minimises the residual: for every other w′, X(w′ − w) lies in the column space, so ‖X w′ − y‖² = ‖X (w′ − w)‖² + ‖X w − y‖² by Pythagoras.

### Practice Exercise

Fit the line y = a + b x to the points (0, 0), (1, 1) and (2, 3).

> *Solution:* The rows of X are (1, 0), (1, 1) and (1, 2), and y = (0, 1, 3). Then XᵀX = [[3, 3], [3, 5]] and Xᵀy = (4, 7). The determinant is 15 − 9 = 6, so (a, b) = (1/6) · (5 · 4 − 3 · 7, −3 · 4 + 3 · 7) = (−1/6, 3/2). The fitted values are −1/6, 4/3 and 17/6, and the residual is (1/6, −1/3, 1/6): its sum is 0 and 0 · 1/6 + 1 · (−1/3) + 2 · 1/6 = 0, so it is orthogonal to both columns.

---

## 2. Identifiability

The parameters are **identifiable** when the data determine them: when the least-squares solution is unique. That holds exactly when X has **full column rank**. If X v = 0 for some v ≠ 0, then w + t v fits exactly as well as w for every t, and the data cannot tell these parameter vectors apart. If instead X v = 0 only for v = 0, then vᵀXᵀX v = ‖X v‖² > 0 for every v ≠ 0, so XᵀX is invertible and the normal equations have one solution.

Typical causes of rank deficiency are a feature that duplicates another, a feature that is a combination of others, a constant feature next to the bias, and fewer observations than parameters. When the rank is deficient, a single answer can still be chosen: the **minimum-norm solution** w⁺ = X⁺y, with the pseudo-inverse of MAT-006 §4, is the least-squares solution of smallest length. It has no component along the directions that the data cannot see.

### Practice Exercise

With X = [[1, 2], [1, 2]] and y = (3, 3), describe every least-squares solution, and give the minimum-norm one.

> *Solution:* Both rows say w₁ + 2 w₂ = 3, so every point of that line fits exactly, with residual 0; the direction (2, −1) satisfies X (2, −1) = 0 and cannot be seen. The shortest solution is orthogonal to (2, −1), so it is a multiple of (1, 2): t (1, 2) with t + 4 t = 3, that is w⁺ = (3/5, 6/5), of squared length 9/25 + 36/25 = 9/5.

---

## 3. Conditioning: Why Not the Normal Equations

The singular values of XᵀX are the squares of those of X (MAT-006), so κ₂(XᵀX) = κ₂(X)² when X has full column rank. By the rule of thumb of MAT-003, a solve through the normal equations can lose about 2 log₁₀ κ₂(X) digits. A solve through the SVD, w = V Σ⁻¹ Uᵀ y for full column rank, or through a QR factorisation, works on X itself and loses about log₁₀ κ₂(X) when the residual is small. When the residual is large, the least-squares problem itself contains a κ² term, and no algorithm avoids it.

Forming XᵀX can even destroy the information outright. **Läuchli's matrix** X = [[1, 1], [δ, 0], [0, δ]] has the singular values √(2 + δ²) and δ, so it has full rank for every δ ≠ 0. But XᵀX = [[1 + δ², 1], [1, 1 + δ²]], and for δ = 10^-8, δ² = 10^-16 is below half the machine epsilon of MAT-003: fl(1 + δ²) = 1, and the stored XᵀX is [[1, 1], [1, 1]], exactly singular. The SVD of X still finds δ.

Conditioning also depends on how the model is written. Take the feature x = c + (0, 1, 2) with a bias. For c = 0 the problem is tame; for large c, the column x is nearly parallel to the column of ones, and the second pivot of XᵀX falls like 2/c². Subtracting the mean of the feature, **centering**, removes the problem: with x − x̄ = (−1, 0, 1), XᵀX = diag(2, 3). The fitted line is the same, written around x̄ instead of 0.

### Practice Exercise

For x = c + (0, 1, 2) with a bias column, show that eliminating the first column of XᵀX leaves the second pivot 6/(3c² + 6c + 5).

> *Solution:* XᵀX = [[Σx², Σx], [Σx, 3]] with Σx = 3c + 3 and Σx² = c² + (c + 1)² + (c + 2)² = 3c² + 6c + 5. The second pivot is 3 − (Σx)²/Σx² = (3 (3c² + 6c + 5) − (3c + 3)²)/Σx² = (9c² + 18c + 15 − 9c² − 18c − 9)/Σx² = 6/(3c² + 6c + 5), about 2/c² for large c.

---

## 4. Ridge Regression

**Ridge regression**, or **Tikhonov regularisation**, minimises ‖X w − y‖² + λ ‖w‖² for a chosen λ > 0. Setting the gradient to zero gives (XᵀX + λI) w = Xᵀy. XᵀX is positive semidefinite, since vᵀXᵀX v = ‖X v‖² ≥ 0 (§2), so every eigenvalue of XᵀX + λI is at least λ > 0, and the solution is unique for every λ > 0, even when X is rank-deficient. With the SVD of MAT-006,

w_λ = Σᵢ σᵢ/(σᵢ² + λ) (uᵢ · y) vᵢ.

Compared with the pseudo-inverse, which multiplies uᵢ · y by 1/σᵢ, ridge multiplies it by the **filter factor** σᵢ²/(σᵢ² + λ): close to 1 when σᵢ² ≫ λ, close to 0 when σᵢ² ≪ λ. Ridge therefore damps the directions that the data barely determine instead of cutting them off at a tolerance, and w_λ tends to X⁺y as λ tends to 0. The price is a bias towards 0. The bias term of the model is usually left out of the penalty, and the features are centered first, so that shrinking does not depend on where the origin is.

### Practice Exercise

For X = [[1, 2], [1, 2]] and y = (3, 3) of §2, compute the ridge solution w_λ, and check its limit as λ tends to 0.

> *Solution:* XᵀX = [[2, 4], [4, 8]] and Xᵀy = (6, 12). Try w = α (1, 2): the first equation gives (2 + λ) α + 8 α = 6, so α = 6/(10 + λ), and the second gives 4 α + 2 (8 + λ) α = 12, the same α. So w_λ = (6/(10 + λ)) (1, 2), for instance (1/2, 1) for λ = 2. As λ tends to 0, w_λ tends to (3/5, 6/5), the minimum-norm solution of §2.

---

## 5. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**The fit** (`crates/ix-supervised/src/linear_regression.rs`). [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L57) appends a column of ones for the bias and solves the normal equations with an explicit inverse, verbatim from lines 57–74:

```rust
    fn fit(&mut self, x: &Array2<f64>, y: &Array1<f64>) {
        let n = x.nrows();
        // Add bias column (column of ones)
        let ones = Array2::ones((n, 1));
        let x_aug = ndarray::concatenate(Axis(1), &[x.view(), ones.view()]).unwrap();

        // Normal equation: w = (X^T X)^{-1} X^T y
        let xtx = x_aug.t().dot(&x_aug);
        let xty = x_aug.t().dot(y);

        // Solve via inverse (fine for small/medium datasets)
        let xtx_inv = ix_math::linalg::inverse(&xtx).expect("X^T X is singular");
        let w = xtx_inv.dot(&xty);

        let p = x.ncols();
        self.weights = Some(w.slice(ndarray::s![..p]).to_owned());
        self.bias = w[p];
    }
```

Three consequences follow from §3 and from MAT-003:
- **It squares the condition number.** Every fit pays κ₂(X)², and the bias column makes an offset feature nearly collinear with it.
- **Its verdict depends on scale and offset.** [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) answers `Singular` when a pivot falls [below 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110), an absolute threshold (MAT-003). For x = c + (0, 1, 2), the second pivot 6/(3c² + 6c + 5) falls below it once c exceeds about 1.41 · 10^6, so three readings of a Unix timestamp in seconds, of the order of 10^9, taken one second apart, make the fit fail although the design has full rank. Below that point, the fit returns without error, however many digits are lost; the exercise at the end of this section shows how many.
- **It panics.** The `expect` of line 68 turns `Singular` into a panic, and the callers handle it differently.

**What the panic does to the callers.** [`ix-duck`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L111) documents the panic and [catches it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L114), returning an SQL error. The handler of the MCP tool `ix_linear_regression` calls [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L285) with no such guard, and so does the [ML pipeline](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L791). The MCP server runs each [`tools/call`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L175) on its own worker thread, which writes the response only [after the handler returns](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L184). `ix_linear_regression` is registry-backed, like most core tools according to a [comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1292) in `tools.rs`, and registry-backed calls go through `dispatch_action`, which holds a global lock while the tool runs, verbatim from `crates/ix-agent/src/registry_bridge.rs` lines 236–243:

```rust
    let chain_guard = middleware_chain()
        .lock()
        .expect("middleware chain mutex poisoned");

    let result = {
        let mut wc = WriteContext { read: cx, sink };
        chain_guard.dispatch(&mut wc, action, &RegistryLookupHandler)
    };
```

Reading this code predicts three effects of a single request that makes `fit` panic:
1. The worker thread ends without writing a response, so the client waits for an answer that never comes.
2. The panic unwinds while `chain_guard` is held, and a Rust `Mutex` is **poisoned** when a thread panics while holding it.
3. From then on, every registry-backed call panics on the `expect` of [line 238](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238), and gets no response either, until the server restarts.

Two more facts:
- **Its schema names the wrong key.** The published input schema of `ix_linear_regression` requires [`"X"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L839), while the handler reads [`"x"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L270). JSON keys are case-sensitive, so a client that follows the schema is predicted to get the error "Missing or invalid field 'x'". IX's own demo sends `"x"`, and its [comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/demo/scenarios/sprint_oracle.rs#L71) says so.
- **The tests stay in the easy cases.** [`test_linear_regression_multivariate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L152) fits exact data on the four points of {1, 2}², a well-conditioned design, with a tolerance of 10^-6. `ix-duck` [tests](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L283) that exactly collinear columns give an SQL error rather than a panic. No test covers an offset or a nearly collinear design, where the fit returns without error.

IX's `ix-supervised` and `ix-math` crates have no ridge or lasso regression and no QR factorisation. The SVD route of §3 is available through [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73), with the caveats of MAT-006, and IX already has a relative rank check, [`RankReport.deficiency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L356), in `ix-signal`, which a fit could consult before solving. Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Predict what `fit` returns for x = c + (0, 1, 2) and y = 2x + 1, whose exact answer is the slope 2 and the bias 1, at c = 10^6 and at c = 10^7.

> *Solution:* For c = 10^7 the second pivot is about 2/c² = 2 · 10^-14, below 10^-12, so `inverse` answers `Singular` and `fit` panics. For c = 10^6 it is about 2 · 10^-12, just above the threshold, so `fit` returns. Its answer is decided by rounding in a pivot that small against entries of the order of 3 · 10^12: κ₂(XᵀX) is about 1.5 · 10^24, beyond anything binary64 can resolve. Here the entries of XᵀX and Xᵀy are integers below 2^53, so they are exact, and a transcription of `inverse` predicts the slope 2 + 2^-11 = 2.00048828125 and the bias exactly 0. The fitted values at the data are then off by about 487, with no error raised. This is a prediction from reading the code, not a run; §6 checks it.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **The offset sweep.** For c = 10^0, 10^1, …, 10^7, fit x = c + (0, 1, 2), y = 2x + 1 with `LinearRegression`, catching the panic in the lab harness. Prediction: the slope is within 10^-9 of 2 for c ≤ 10^3; at c = 10^5 the slope is 2 − 2^-18 and the bias 1.5; at c = 10^6 the slope is 2 + 2^-11 and the bias 0; at c = 10^7 `fit` panics with "X^T X is singular". On the centered feature (−1, 0, 1), the same data give the slope exactly 2 and the bias 2c + 3, the fitted value at x̄, within a relative 10^-15, at every c.
2. **Normal equations against the SVD.** Take x₁ = N · (1, 2, 3, 4), x₂ = x₁ + (1, −1, −1, 1) and y = x₁ + x₂ + 1, so that the exact weights are 1, 1 and 1, and κ₂ grows like 10 N. For N = 10^0, …, 10^7, compare `fit` with the SVD route: `pseudo_inverse` of the design with its ones column, at the tolerance max(m, n) · σ₁ · ε of MAT-006, applied to y. Prediction: the largest weight error of `fit` is below 10^-9 for N ≤ 10^3, about 3 · 10^-5 at N = 10^5 and about 0.25 at N = 10^7, with no error raised; the SVD route stays below 10^-7 at every N.
3. **The MCP server after a panic.** In a disposable `ix-mcp` process, never a shared one, send `ix_linear_regression` the data of step 1 at c = 10^7, then a well-posed `ix_stats` call. Prediction: neither call receives a response, and the server's error output shows the panic "X^T X is singular", then "middleware chain mutex poisoned".
4. **The schema.** Send `ix_linear_regression` well-posed data under the key `"X"`, as the schema requires. Prediction: the error "Missing or invalid field 'x'".

### Practice Exercise

Step 2 predicts an error of about 0.25 for the normal equations at N = 10^7, while the SVD route stays below 10^-7. Estimate both from the condition number.

> *Solution:* κ₂ of the design is about 10 N = 10^8. The normal equations work with κ₂² ≈ 10^16, and 10^16 times ε ≈ 2.2 · 10^-16 is of order 1: no digit is guaranteed, and an error of 0.25 is within that bound. The SVD route works with κ₂ ≈ 10^8, which predicts an error of about 10^8 · 2.2 · 10^-16 ≈ 2 · 10^-8, consistent with staying below 10^-7. These are orders of magnitude from the rule of thumb of MAT-003, not bounds.

---

## 7. Common Pitfalls

- **Solving least squares with an explicit inverse of XᵀX.** It squares the condition number; solve through QR or the SVD.
- **Fitting raw offsets.** Timestamps, coordinates and other features far from 0 compared with their spread make the bias column nearly collinear with them; center them first.
- **Reading "no error" as "a correct fit".** At c = 10^6, `fit` is predicted to return a wrong answer without any warning.
- **Letting a numerical failure panic in a server.** Return an error instead, and never let a panic unwind while a lock is held: the lock is poisoned for every later caller.
- **Regularising the bias.** The penalty should shrink the slopes, not the level of the data.
- **Trusting a schema without a call that uses it.** A schema and a handler can disagree on a single letter.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Design matrix** | The n × p matrix X with one row per observation and one column per parameter |
| **Residual** | r = y − X w, what the model leaves unexplained |
| **Normal equations** | XᵀX w = Xᵀy: the residual is orthogonal to every column of X |
| **Identifiability** | The data determine the parameters uniquely: X has full column rank |
| **Minimum-norm solution** | w⁺ = X⁺y, the shortest least-squares solution |
| **Läuchli's matrix** | [[1, 1], [δ, 0], [0, δ]]: full rank, but fl(XᵀX) is singular for small δ |
| **Centering** | Subtracting the mean of a feature before fitting, so that it is orthogonal to the bias column |
| **Ridge (Tikhonov) regression** | Minimising ‖X w − y‖² + λ ‖w‖², with the unique solution (XᵀX + λI)⁻¹Xᵀy |
| **Filter factor** | σᵢ²/(σᵢ² + λ), the weight ridge gives to the i-th singular direction |
| **Mutex poisoning** | The state of a Rust lock after a thread panicked while holding it; later `lock` calls return an error |

---

## Self-Check Assessment

**1. Why does forming XᵀX square the condition number?**
> The singular values of XᵀX are σᵢ², so for X of full column rank κ₂(XᵀX) = σ_max²/σ_min² = κ₂(X)².

**2. Why is the least-squares solution unique exactly when X has full column rank?**
> If X v = 0 with v ≠ 0, then w + t v fits as well as w for every t. If X v = 0 only for v = 0, then vᵀXᵀX v = ‖X v‖² > 0, so XᵀX is invertible and the normal equations have exactly one solution.

**3. Why does ridge have a unique solution for every λ > 0, even when X is rank-deficient?**
> XᵀX is positive semidefinite, since vᵀXᵀX v = ‖X v‖² ≥ 0, so every eigenvalue of XᵀX + λI is at least λ > 0, and the matrix is invertible.

**4. IX's `test_linear_regression_multivariate` passes. What does it tell you about offset or collinear data?**
> Nothing: it fits exact data on the four points of {1, 2}², a small and well-conditioned design. The failures of §5 need a large offset or nearly collinear columns, which no test covers.

**Pass criteria:** Derive and solve the normal equations for a small fit, decide identifiability and give the minimum-norm solution, explain the κ² of the normal equations and the effect of centering, write the ridge solution with its filter factors, and trace what IX's regression computes and what its panic does to its callers.

---

## Research Basis

- Å. Björck, *Numerical Methods for Least Squares Problems*, SIAM, 1996: normal equations, QR and SVD solves, and their accuracy
- L. N. Trefethen and D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lectures 11, 18 and 19: least squares, its conditioning, and the stability of its algorithms
- P. Läuchli, "Jordan-Elimination und Ausgleichung nach kleinsten Quadraten", *Numerische Mathematik* 3, 1961: the matrix whose normal equations lose it
- A. N. Tikhonov, "Solution of incorrectly formulated problems and the regularization method", *Soviet Mathematics Doklady* 4, 1963: regularisation
- A. E. Hoerl and R. W. Kennard, "Ridge regression: biased estimation for nonorthogonal problems", *Technometrics* 12, 1970: ridge regression
- T. Hastie, R. Tibshirani and J. Friedman, *The Elements of Statistical Learning*, 2nd ed., Springer, 2009, §3.4: shrinkage methods
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §5 links to its line
- Experiment: proposed in §6, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
