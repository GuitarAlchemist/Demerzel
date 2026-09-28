---
module_id: mat-005-symmetric-eigenproblems
department: mathematics
course: Symmetric Eigenproblems
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Symmetric Eigenproblems — The Directions a Matrix Only Stretches

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Find the eigenvalues and eigenvectors of a 2 × 2 matrix by hand
- State the spectral theorem for real symmetric matrices, prove its key steps, and show with counterexamples what fails without symmetry
- Use the Rayleigh quotient to bound the eigenvalues and to estimate one from an approximate eigenvector
- Carry out a Jacobi rotation and explain why the cyclic Jacobi method converges
- Explain why a repeated eigenvalue determines its eigenspace but not its eigenvectors, and test such output correctly
- Explain when power iteration fails, and say what IX's eigensolvers do and do not guarantee

---

## 1. Eigenvalues and Eigenvectors

A nonzero vector v is an **eigenvector** of a square matrix A, with **eigenvalue** λ, if

A v = λ v.

Along the direction of v, A only stretches, by the factor λ, and flips the direction if λ < 0. Since A v = λ v means (A − λI) v = 0 with v ≠ 0, the matrix A − λI is not invertible, so λ is a root of the **characteristic polynomial** det(A − λI) (MAT-004). For a 2 × 2 matrix, this polynomial is

λ² − (tr A) λ + det A,

where the trace tr A is the sum of the diagonal entries. For A = [[2, 1], [1, 2]], it is λ² − 4λ + 3 = (λ − 3)(λ − 1): the eigenvalues are 3, for v = (1, 1), and 1, for v = (1, −1).

Two counterexamples show that a real matrix need not give such a clean picture:
- **No real eigenvalue.** The rotation by 90° of MAT-004, R = [[0, −1], [1, 0]], has the characteristic polynomial λ² + 1, which has no real root: no direction of the plane is merely stretched by a quarter turn.
- **Too few eigenvectors.** The shear [[1, 1], [0, 1]] has the double eigenvalue 1, but only the multiples of (1, 0) are eigenvectors, so no basis of R² consists of its eigenvectors.

### Practice Exercise

Find the eigenvalues and eigenvectors of A = [[5, 2], [2, 2]], and check that the eigenvectors are orthogonal.

> *Solution:* tr A = 7 and det A = 10 − 4 = 6, so the characteristic polynomial is λ² − 7λ + 6 = (λ − 6)(λ − 1). For λ = 6, A − 6I = [[−1, 2], [2, −4]], whose rows both say x = 2y: v = (2, 1), and indeed A (2, 1) = (12, 6) = 6 · (2, 1). For λ = 1, A − I = [[4, 2], [2, 1]], whose rows both say y = −2x: w = (1, −2), and A (1, −2) = (1, −2). Finally v · w = 2 − 2 = 0.

---

## 2. The Spectral Theorem

A matrix is **symmetric** if Aᵀ = A, that is, if its entry in row i and column j equals the one in row j and column i. The two counterexamples of §1 are not symmetric, and that is no accident:

**Spectral theorem.** A real symmetric n × n matrix A has n real eigenvalues, counted with multiplicity, and an orthonormal basis of eigenvectors. Equivalently, A = Q Λ Qᵀ, where Q is **orthogonal** (QᵀQ = I; its columns are the eigenvectors) and Λ is the diagonal matrix of the eigenvalues.

In the basis of its eigenvectors, a symmetric matrix is just a scaling along perpendicular axes. Two steps of the proof are short:
- **Eigenvectors for different eigenvalues are orthogonal.** If A u = λ u and A v = μ v with λ ≠ μ, then λ (u · v) = (A u) · v = u · (A v) = μ (u · v), where the middle equality uses Aᵀ = A. So (λ − μ)(u · v) = 0, and u · v = 0.
- **The eigenvalues are real.** If A x = λ x for a complex vector x ≠ 0, then λ ‖x‖² = x̄ᵀ A x, and x̄ᵀ A x equals its own complex conjugate because A is real and symmetric. So λ is real.

The remaining step, that there are enough eigenvectors even when eigenvalues repeat, is an induction on n (MAT-001); Axler's book in the Research Basis gives it.

### Practice Exercise

With the eigenvectors of the §1 exercise, set Q = (1/√5) [[2, 1], [1, −2]] and Λ = diag(6, 1), and check that Q Λ Qᵀ = [[5, 2], [2, 2]].

> *Solution:* The columns (2, 1)/√5 and (1, −2)/√5 have length 1 and are orthogonal, so Q is orthogonal, and here Qᵀ = Q. Then [[2, 1], [1, −2]] · diag(6, 1) = [[12, 1], [6, −2]], and [[12, 1], [6, −2]] · [[2, 1], [1, −2]] = [[25, 10], [10, 10]]. The two factors 1/√5 give 1/5, and (1/5) · [[25, 10], [10, 10]] = [[5, 2], [2, 2]].

---

## 3. The Rayleigh Quotient

For a symmetric A and a vector x ≠ 0, the **Rayleigh quotient** is

R(x) = (xᵀ A x) / (xᵀ x).

If x is an eigenvector with eigenvalue λ, then R(x) = λ. In general, write x = c₁q₁ + … + cₙqₙ in an orthonormal basis of eigenvectors, with eigenvalues λ₁ ≥ … ≥ λₙ. Then

R(x) = (λ₁c₁² + … + λₙcₙ²) / (c₁² + … + cₙ²),

a weighted average of the eigenvalues. Two consequences follow:
- **Bounds.** λₙ ≤ R(x) ≤ λ₁ for every x ≠ 0, with equality at the eigenvectors: the largest eigenvalue is the maximum of R, and the smallest is its minimum. For a symmetric matrix, the induced 2-norm of MAT-004 is the largest |λᵢ|.
- **Accuracy.** If x is close to an eigenvector, R(x) is much closer to its eigenvalue: an error of order ε in the direction of x gives an error of order ε² in R(x).

### Practice Exercise

For A = diag(3, 1) and x = (1, 1/10), compute R(x) and its distance to the eigenvalue 3.

> *Solution:* xᵀ A x = 3 · 1 + 1 · 1/100 = 301/100 and xᵀ x = 101/100, so R(x) = 301/101. Its distance to 3 is 3 − 301/101 = 2/101, about 0.02, while the direction of x is off the eigenvector (1, 0) by an angle of about 1/10. The error in the eigenvalue is about twice the square of the error in the direction, as the second consequence says.

---

## 4. Jacobi Rotations

In 1846, Jacobi proposed to diagonalise a symmetric matrix by a sequence of plane rotations. Each step picks a pair of indices p < q and replaces A by JᵀAJ, where J rotates the plane of the coordinates p and q by an angle chosen to make the new entry a_pq zero. Since J is orthogonal, JᵀAJ has the same eigenvalues as A.

For the 2 × 2 block [[a_pp, a_pq], [a_pq, a_qq]] with a_pq ≠ 0, set θ = (a_qq − a_pp) / (2a_pq). The tangent t of the rotation angle is a root of t² + 2θt − 1 = 0, and the root of smaller absolute value, t = 1 / (θ + √(1 + θ²)) when θ ≥ 0 and t = 1 / (θ − √(1 + θ²)) when θ < 0, keeps the rotation small. With c = 1/√(1 + t²) and s = t c, the rotation gives the new diagonal entries

a_pp − t a_pq and a_qq + t a_pq,

and a zero in position (p, q).

Why the method converges: an orthogonal similarity keeps the sum of the squares of all the entries. The rotation turns the two off-diagonal entries a_pq into zeros and moves their weight to the diagonal, so the sum of the squares off the diagonal drops by exactly 2a_pq². A later rotation can make a zeroed entry nonzero again, so the **cyclic Jacobi method** sweeps over all the pairs repeatedly; the off-diagonal sum still decreases, and the method converges; when the eigenvalues are distinct, the convergence is eventually quadratic (Golub and Van Loan, ch. 8). The product V = J₁J₂J₃… of the rotations holds the eigenvectors as its columns.

### Practice Exercise

Apply one Jacobi rotation to A = [[5, 2], [2, 2]].

> *Solution:* θ = (2 − 5)/(2 · 2) = −3/4, so √(1 + θ²) = √(25/16) = 5/4 and t = −1/(3/4 + 5/4) = −1/2. The new diagonal entries are 5 − (−1/2) · 2 = 6 and 2 + (−1/2) · 2 = 1, and the off-diagonal entry is 0. One rotation diagonalises any symmetric 2 × 2 matrix: here it finds the eigenvalues 6 and 1 of §1, and the off-diagonal sum of squares drops from 2 · 2² = 8 to 0.

---

## 5. Repeated Eigenvalues

For a symmetric matrix, when an eigenvalue repeats, its **eigenspace**, the set of all v with A v = λ v, has a dimension equal to the multiplicity, so greater than 1. Without symmetry this can fail: the shear of §1 has the double eigenvalue 1 but a one-dimensional eigenspace. Every orthonormal basis of the eigenspace is then an equally correct set of eigenvectors.

Take B = I + J, where J is the 3 × 3 matrix of ones. Since J (1, 1, 1) = 3 · (1, 1, 1), and J v = 0 whenever the entries of v sum to 0, B has the eigenvalue 4 for (1, 1, 1) and the double eigenvalue 1 on the whole plane of the vectors whose entries sum to 0. Any two orthonormal vectors of that plane are a correct answer.

What is unique is the eigenspace, and with it the **orthogonal projector** onto it, P = uuᵀ + wwᵀ, which does not depend on the orthonormal basis u, w chosen. So a test of an eigensolver should check **invariants**, A v = λ v, VᵀV = I and A = V Λ Vᵀ, or compare projectors, and never compare the eigenvectors with a fixed expected list: even a simple eigenvector is only determined up to its sign.

The eigenvalues are well conditioned (MAT-003): adding a symmetric E to a symmetric matrix moves each eigenvalue by at most ‖E‖₂, which is Weyl's inequality. The eigenvectors are not: when two eigenvalues are close, a small change of the matrix can turn their eigenvectors a long way within the plane they span.

### Practice Exercise

Check that u = (1, −1, 0)/√2 and w = (1, 1, −2)/√6 are orthonormal eigenvectors of B = I + J for the eigenvalue 1, and that uuᵀ + wwᵀ = I − J/3.

> *Solution:* The entries of u, and those of w, sum to 0, so J u = J w = 0, hence B u = u and B w = w. Also u · w = (1 − 1 + 0)/√12 = 0, ‖u‖² = 2/2 = 1 and ‖w‖² = 6/6 = 1. Then uuᵀ = (1/2) [[1, −1, 0], [−1, 1, 0], [0, 0, 0]] and wwᵀ = (1/6) [[1, 1, −2], [1, 1, −2], [−2, −2, 4]]. Their sum has 1/2 + 1/6 = 2/3 or 0 + 4/6 = 2/3 on the diagonal, and −1/2 + 1/6 = −1/3 or 0 − 2/6 = −1/3 elsewhere: it is I − J/3, whose diagonal entries are 1 − 1/3 = 2/3 and whose other entries are −1/3. Another orthonormal basis of the plane gives the same matrix.

---

## 6. Power Iteration and Its Blind Spot

**Power iteration** is the simplest eigensolver: start from a unit vector v₀, repeat v ← A v / ‖A v‖, and estimate the eigenvalue by the Rayleigh quotient of v. If v₀ = c₁q₁ + … + cₙqₙ and |λ₁| > |λ₂| ≥ …, then

Aᵏ v₀ = c₁λ₁ᵏ q₁ + … + cₙλₙᵏ qₙ,

and the first term wins, with an error that shrinks like |λ₂/λ₁|ᵏ, **provided that c₁ ≠ 0**. Two things can go wrong:
- **A blind start.** If v₀ is orthogonal to q₁, then c₁ = 0, and in exact arithmetic the iteration never finds q₁. Rounding may bring in a tiny component along q₁, which then needs many steps to grow.
- **A stopping test that cannot tell.** "Stop when the estimate no longer changes" is met by an iteration stuck on the wrong eigenvector just as well as by one that has converged to the right one.

To find the next eigenpair, **deflation** replaces A by A − λ₁ v vᵀ, which moves the eigenvalue found to 0; any error in the first pair is passed on to the next.

### Practice Exercise

Run power iteration on A = [[2, −1], [−1, 2]] from v₀ = (1, 1)/√2. Which eigenvalue does it report, and which is the largest?

> *Solution:* A (1, 1) = (1, 1), so v₀ is an eigenvector for the eigenvalue 1. Every step returns v₀ itself, the Rayleigh quotient is 1 at every step, and a test on its change stops at once and reports 1. But A (1, −1) = (3, −3): the largest eigenvalue is 3, for (1, −1)/√2, which is orthogonal to v₀. The iteration was blind to it from the start.

---

## 7. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**The symmetric solver** (`crates/ix-math/src/eigen.rs`). [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46) is the cyclic Jacobi method of §4, with at most 100 sweeps and a tolerance of 10^-12. It returns the eigenvalues in descending order and the eigenvectors as the columns of a matrix. Its rotation, verbatim from lines 92–109, is the formula of §4:

```rust
                let app = m[[p, p]];
                let aqq = m[[q, q]];
                // Compute Jacobi rotation angle that zeros the (p, q) entry
                // of the 2x2 submatrix [[app, apq], [apq, aqq]].
                let theta = (aqq - app) / (2.0 * apq);
                let t = if theta >= 0.0 {
                    1.0 / (theta + (1.0 + theta * theta).sqrt())
                } else {
                    1.0 / (theta - (1.0 + theta * theta).sqrt())
                };
                let c = 1.0 / (1.0 + t * t).sqrt();
                let s = t * c;

                // Update diagonal entries and zero the off-diagonal.
                m[[p, p]] = app - t * apq;
                m[[q, q]] = aqq + t * apq;
                m[[p, q]] = 0.0;
                m[[q, p]] = 0.0;
```

Its contract has three limits worth knowing:
- **It does not check symmetry.** It rejects empty and [non-square](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L64) input, but reads the entries above the diagonal as if the matrix were symmetric. The exercise below shows what it then returns.
- **It does not report convergence.** The [sweep loop](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L74) ends after 100 sweeps at most, and the function then returns [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L151) whether or not the tolerance was reached.
- **Its stopping test is not the one its comment states.** The comment speaks of the Frobenius norm of the off-diagonal part, but the [loop](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L78) sums the squares above the diagonal only. For a symmetric matrix that is half of the off-diagonal sum of squares, so the actual threshold on that norm is √2 · 10^-12: harmless here, and a reminder to read the code rather than the comment.

The tests check the right kind of property. [`test_eigenvectors_are_orthonormal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L189) and [`test_reconstruction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L210) check VᵀV = I and A = V Λ Vᵀ, the invariants of §5, on one 3 × 3 matrix. [`test_repeated_eigenvalues`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L231), however, uses the 4 × 4 identity: its off-diagonal part is already zero, so the loop stops before the first rotation and returns the identity it started from. The test passes without exercising a single rotation on a repeated eigenvalue; a matrix such as the I + J of §5 would force rotations.

**Two callers, two ways to meet the precondition.** The handler of the MCP tool `ix_eigen`, [`eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L469), rejects [non-finite entries](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L483) and any asymmetry larger than a [relative tolerance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L491) of 10^-9, and [`eigen_rejects_non_symmetric`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1173) tests the rejection on [[1, 2], [3, 4]]. The CMA-ES optimiser instead [replaces its covariance matrix C by (C + Cᵀ)/2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-acoustic-tune/src/cmaes.rs#L181) before calling the solver; Self-Check question 3 shows why that is the right repair.

**Plain PCA does not use this solver.** The module comment of `eigen.rs` asks the workspace to [call into it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L8) rather than duplicate it, but `crates/ix-unsupervised/src/pca.rs` still extracts principal components by power iteration and [deflation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). Its power iteration, verbatim from lines 103–137:

```rust
fn power_iteration(matrix: &Array2<f64>, max_iter: usize, tol: f64) -> (f64, Array1<f64>) {
    let n = matrix.nrows();

    // Initialize with a non-zero vector
    let mut v = Array1::from_elem(n, 1.0 / (n as f64).sqrt());

    let mut eigenvalue = 0.0;

    for _ in 0..max_iter {
        // Multiply: v_new = M * v
        let v_new = matrix.dot(&v);

        // Compute eigenvalue (Rayleigh quotient)
        let new_eigenvalue = v.dot(&v_new);

        // Normalize
        let norm = v_new.dot(&v_new).sqrt();
        if norm < 1e-15 {
            break;
        }
        let v_normalized = &v_new / norm;

        // Check convergence
        if (new_eigenvalue - eigenvalue).abs() < tol {
            eigenvalue = new_eigenvalue;
            v = v_normalized;
            break;
        }

        eigenvalue = new_eigenvalue;
        v = v_normalized;
    }

    (eigenvalue, v)
}
```

The start vector is always (1, …, 1)/√n, and the loop stops when the Rayleigh estimate changes by less than `tol`, which [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176) sets to 10^-10: both blind spots of §6. Consider the six points (1, −1), (−1, 1), (1, 0), (−1, 0), (0, 1) and (0, −1). Their mean is 0 and their covariance matrix is [[4, −2], [−2, 4]]/5, with the eigenvalue 6/5 for (1, −1)/√2 and 2/5 for (1, 1)/√2. The start vector (1, 1)/√2 is the eigenvector of the smaller one, as in the §6 exercise. After deflation, the matrix is close to [[3/5, −3/5], [−3/5, 3/5]], which sends the start vector to nearly zero, so the second call should stop at its first norm test, keeping the start vector and the estimate 0. Our reading of the code therefore predicts that `PCA` with two components returns (1, 1)/√2 as its first component, with variance 2/5, and the same vector again as its second, with variance 0. Such a pair would fail [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288), which checks orthogonality on another data set. The eigenvalues 6/5 and 2/5 are well separated: the failure comes from the fixed start vector, not from close eigenvalues. This is a prediction, not a run (§8), and a limitation of the pinned code for IX's owners to fix, not a behaviour to copy.

### Practice Exercise

Trace `symmetric_eigen` by hand on the non-symmetric matrix A = [[1, 2], [3, 4]]. What does it return, and how would a check of A v = λ v catch the problem?

> *Solution:* The first sweep has one pair, (0, 1). The loop reads a_pq = 2, the entry above the diagonal, with a_pp = 1 and a_qq = 4, so θ = 3/(2 · 2) = 3/4, √(1 + θ²) = 5/4 and t = 1/(3/4 + 5/4) = 1/2. The new diagonal is 1 − (1/2) · 2 = 0 and 4 + (1/2) · 2 = 5, the off-diagonal entries are set to 0, and the next sweep stops. The function returns the eigenvalues (5, 0), with no error: these are the eigenvalues of [[1, 2], [2, 4]], the matrix whose lower entry mirrors the upper one. The true eigenvalues of A are (5 ± √33)/2, about 5.37 and −0.37. For λ = 5 the returned vector is v = (1, 2)/√5, and A v = (5, 11)/√5 ≠ 5 v = (5, 10)/√5: the residual A v − λ v = (0, 1)/√5 is far from 0. The values the eigenvalues depend on, θ, √(1 + θ²), t and the new diagonal, are all exact in binary64, so this reading predicts exactly (5, 0); §8 checks it.

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Invariants.** Call `symmetric_eigen` on [[5, 2], [2, 2]], on the 3 × 3 matrix of IX's own tests, and on I + J of sizes 3 and 4. Check A v = λ v, VᵀV = I and A = V Λ Vᵀ entry by entry within 10^-9, the tolerance of IX's tests. Prediction: all hold, with the eigenvalues 6 and 1, then 4, 1, 1, then 5, 1, 1, 1.
2. **The eigenspace, not the vectors.** For I + J of size 3, build uuᵀ + wwᵀ from the two returned eigenvectors for the eigenvalue 1, and compare it with I − J/3. Prediction: equal within 10^-9, whichever vectors the solver chose.
3. **Asymmetric input.** Call `symmetric_eigen` on [[1, 2], [3, 4]]. Prediction: exactly (5, 0), with no error. Call `ix_eigen` on the same matrix. Prediction: an error whose message contains "symmetric".
4. **PCA's blind spot.** Fit `PCA` with two components on the six points of §7. Prediction: both components equal (1, 1)/√2 up to sign and rounding, the variances are close to 2/5 and 0, and `explained_variance_ratio` reports 1 and 0. For comparison, `symmetric_eigen` on the same covariance matrix returns 6/5 and 2/5.

### Practice Exercise

If step 4 goes as predicted, the first component "explains" 100% of the variance. Why is that no evidence that it is the right axis, and what simple check exposes the problem?

> *Solution:* The ratio divides each returned variance by the sum of the returned variances, not by the total variance of the data, so a method that misses the main axis can still report 100%. The total variance is the trace of the covariance matrix, which is also the sum of its eigenvalues (§1): 4/5 + 4/5 = 8/5. The returned variances add up to 2/5, so 6/5 of the variance, three quarters of it, is unaccounted for.

---

## 9. Common Pitfalls

- **Feeding a symmetric solver a non-symmetric matrix.** It answers another question, without an error: check symmetry, or repair it, first.
- **Comparing eigenvectors with a fixed expected list.** Their sign is free, and with a repeated eigenvalue so is the whole basis: test invariants or projectors.
- **Trusting "the estimate stopped changing".** An iteration stuck on the wrong eigenvector stops changing too.
- **Starting power iteration from a fixed "neutral" vector.** Whatever the vector, some matrices have their dominant eigenvector orthogonal to it.
- **Writing a test that never runs the algorithm.** On the identity, a Jacobi solver performs no rotation at all.
- **Reading the comment instead of the code.** The two can disagree, as with the stopping test of `symmetric_eigen`.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Eigenvector, eigenvalue** | A nonzero v with A v = λ v: a direction that A only stretches, by the factor λ |
| **Characteristic polynomial** | det(A − λI), whose roots are the eigenvalues |
| **Symmetric matrix** | A square matrix with Aᵀ = A |
| **Orthogonal matrix** | A square matrix Q with QᵀQ = I: its columns are orthonormal |
| **Spectral theorem** | A real symmetric matrix is A = Q Λ Qᵀ, with Q orthogonal and Λ real and diagonal |
| **Rayleigh quotient** | R(x) = xᵀAx / xᵀx, a weighted average of the eigenvalues of a symmetric A |
| **Jacobi rotation** | A plane rotation J chosen so that JᵀAJ has a zero in a chosen off-diagonal position |
| **Eigenspace** | All v with A v = λ v for a given λ; its dimension can exceed 1 |
| **Orthogonal projector** | uuᵀ + wwᵀ + … for an orthonormal basis u, w, … of a subspace; it does not depend on the basis |
| **Power iteration** | Repeating v ← A v / ‖A v‖, which finds the dominant eigenvector if the start has a component along it |
| **Deflation** | Replacing A by A − λ v vᵀ to remove an eigenpair already found |

---

## Self-Check Assessment

**1. Why must the eigenvectors of a symmetric matrix for the eigenvalues 3 and 1 be orthogonal?**
> If A u = 3u and A v = v, then 3 (u · v) = (A u) · v = u · (A v) = u · v, using Aᵀ = A. So 2 (u · v) = 0, and u · v = 0.

**2. For a symmetric A with eigenvalues λ₁ ≥ … ≥ λₙ, why is the maximum of the Rayleigh quotient λ₁, and where is it reached?**
> R(x) is a weighted average of the eigenvalues, with weights cᵢ² ≥ 0 (§3), so it is at most λ₁. It equals λ₁ at x = q₁, an eigenvector for λ₁.

**3. CMA-ES replaces a covariance matrix C by S = (C + Cᵀ)/2 before calling `symmetric_eigen`. Why is S the nearest symmetric matrix to C?**
> Write C = S + K with K = (C − Cᵀ)/2, so that Kᵀ = −K. For every symmetric X, the matrix S − X is symmetric, and a symmetric matrix is orthogonal to K for the inner product Σ xᵢⱼyᵢⱼ that defines the Frobenius norm: the terms for (i, j) and (j, i) cancel, and K has zeros on its diagonal. So ‖C − X‖² = ‖S − X‖² + ‖K‖², which is smallest exactly for X = S. For a covariance matrix that drifted from symmetry by rounding, K is tiny, and S is the natural repair.

**4. IX's `test_repeated_eigenvalues` passes. What does it show about repeated eigenvalues?**
> Very little: on the identity the off-diagonal part is zero, so the solver stops before any rotation and returns the identity it started from. A test with I + J would force rotations, and would have to check invariants or the projector, since the eigenvectors for the eigenvalue 1 are not unique.

**Pass criteria:** Find the eigenpairs of a 2 × 2 matrix by hand, use the spectral theorem and its counterexamples, bound and estimate eigenvalues with the Rayleigh quotient, carry out a Jacobi rotation, test an eigensolver's output through invariants when eigenvalues repeat, and spot the preconditions and blind spots of IX's eigensolvers.

---

## Research Basis

- G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013, ch. 8: the symmetric eigenproblem, the Jacobi method, power iteration and Weyl's inequality
- B. N. Parlett, *The Symmetric Eigenvalue Problem*, SIAM Classics in Applied Mathematics, 1998: the Rayleigh quotient and the sensitivity of eigenvectors
- L. N. Trefethen and D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lectures 24–30: eigenvalue algorithms, power iteration and the Jacobi method
- C. G. J. Jacobi, "Über ein leichtes Verfahren, die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen", *Journal für die reine und angewandte Mathematik* 30, 1846: the rotation method
- S. Axler, *Linear Algebra Done Right*, 4th ed., Springer, 2024: the spectral theorem and its proof
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §7 links to its line
- Experiment: proposed in §8, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
