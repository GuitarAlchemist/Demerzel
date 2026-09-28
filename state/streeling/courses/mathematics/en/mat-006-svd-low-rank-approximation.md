---
module_id: mat-006-svd-low-rank-approximation
department: mathematics
course: Singular Value Decomposition and Low-Rank Approximation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms, mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Singular Value Decomposition and Low-Rank Approximation — The Best Simplification of a Matrix

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- State the singular value decomposition and derive it from the spectral theorem of MAT-005
- Compute the SVD of a 2 × 2 matrix by hand
- Read the norm, rank, condition number and determinant of a matrix off its singular values
- State the Eckart–Young–Mirsky theorem and compute the error of a best rank-k approximation
- Choose a rank tolerance relative to the largest singular value, and explain why an absolute one fails
- Explain how one-sided Jacobi computes the SVD, and say what IX's implementation does and does not guarantee

---

## 1. Every Matrix Is a Rotation, a Stretch and a Rotation

**Singular value decomposition.** Every real m × n matrix A can be written

A = U Σ Vᵀ,

where U (m × m) and V (n × n) are orthogonal, and Σ (m × n) is zero except for its diagonal entries σ₁ ≥ σ₂ ≥ … ≥ 0, the **singular values**. The columns of V are the **right singular vectors**, those of U the **left singular vectors**, and A vᵢ = σᵢ uᵢ.

Read from right to left: Vᵀ turns the input, Σ stretches it along the coordinate axes, and U turns the result. The unit sphere becomes an ellipsoid whose semi-axes have lengths σᵢ and point along the uᵢ. With k = min(m, n), the **thin SVD** keeps only the first k columns of U and V; it is the form IX returns.

The SVD follows from the spectral theorem of MAT-005. The matrix AᵀA is symmetric, and xᵀAᵀAx = ‖Ax‖² ≥ 0, so its eigenvalues λᵢ are real and non-negative. Take an orthonormal basis v₁, …, vₙ of its eigenvectors, ordered so that λ₁ ≥ λ₂ ≥ … ≥ λₙ, and set σᵢ = √λᵢ. For i ≠ j, (A vᵢ) · (A vⱼ) = vᵢᵀAᵀA vⱼ = λⱼ (vᵢ · vⱼ) = 0, and ‖A vᵢ‖² = λᵢ = σᵢ². So the vectors uᵢ = A vᵢ / σᵢ, for σᵢ > 0, are orthonormal, and A vᵢ = σᵢ uᵢ; completing the uᵢ to an orthonormal basis gives A V = U Σ, that is A = U Σ Vᵀ.

Unlike eigenvalues (MAT-005 §1), singular values always exist and are real and non-negative, for every matrix: square or not, symmetric or not.

### Practice Exercise

Compute the SVD of B = [[3, 0], [4, 5]].

> *Solution:* BᵀB = [[3 · 3 + 4 · 4, 3 · 0 + 4 · 5], [0 · 3 + 5 · 4, 0 · 0 + 5 · 5]] = [[25, 20], [20, 25]]. Its trace is 50 and its determinant 625 − 400 = 225, so its eigenvalues are 45, for v₁ = (1, 1)/√2, and 5, for v₂ = (1, −1)/√2. So σ₁ = √45 = 3√5 and σ₂ = √5. Then u₁ = B v₁/σ₁ = (3, 9)/(√2 · 3√5) = (1, 3)/√10 and u₂ = B v₂/σ₂ = (3, −1)/(√2 · √5) = (3, −1)/√10, which are orthogonal: 3 − 3 = 0.

---

## 2. What the Singular Values Tell

The singular values summarise a matrix:
- **Norm.** ‖A‖₂ = σ₁: the induced 2-norm of MAT-004 is the largest stretch.
- **Size.** ‖A‖_F² = σ₁² + σ₂² + …, where the Frobenius norm ‖A‖_F is the square root of the sum of the squares of all the entries; multiplying by orthogonal matrices does not change it.
- **Rank.** The rank of A is the number of nonzero singular values.
- **Conditioning.** For a square invertible A, the condition number of MAT-003 is κ₂(A) = σ₁/σₙ.
- **Volume.** For a square A, |det A| = σ₁σ₂…σₙ: U and V keep lengths and angles, so they keep volumes, and by the product rule of MAT-004 only Σ changes them, by the product of its diagonal.

### Practice Exercise

For the matrix B of §1, give ‖B‖₂, ‖B‖_F, κ₂(B) and |det B| from its singular values, and check two of them directly.

> *Solution:* ‖B‖₂ = 3√5, ‖B‖_F = √(45 + 5) = √50, κ₂(B) = 3√5/√5 = 3 and |det B| = 3√5 · √5 = 15. Directly, the squares of the entries sum to 9 + 0 + 16 + 25 = 50, and det B = 3 · 5 − 0 · 4 = 15.

---

## 3. Low-Rank Approximation

Written column by column, the SVD is a sum of rank-1 matrices in decreasing order of importance:

A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + … .

Keeping the first k terms gives the **rank-k truncation** A_k.

**Eckart–Young–Mirsky theorem.** For every matrix X of rank at most k, ‖A − X‖₂ ≥ σₖ₊₁ and ‖A − X‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …), with equality for X = A_k.

The error of the truncation itself is easy to read: A − A_k = σₖ₊₁uₖ₊₁vₖ₊₁ᵀ + … is again written as an SVD, so its 2-norm is its largest singular value σₖ₊₁, and its Frobenius norm is the square root of the sum of the squares of its singular values. The hard part of the theorem is that no other matrix of rank k does better; the Research Basis gives the proofs. Two consequences follow: the error decreases as k grows and reaches 0 at k = rank A, and a matrix is "nearly of rank k" in the 2-norm exactly when σₖ₊₁ is small compared with σ₁; in the Frobenius norm, the whole tail √(σₖ₊₁² + σₖ₊₂² + …) must be small compared with ‖A‖_F. This is what compression, denoising and latent semantic analysis use.

### Practice Exercise

Give the best rank-1 approximation of A = diag(3, 2, 1) and its error in both norms. Then do the same for the matrix B of §1.

> *Solution:* The SVD of diag(3, 2, 1) is the matrix itself, with U = V = I, so A₁ = diag(3, 0, 0), with ‖A − A₁‖₂ = 2 and ‖A − A₁‖_F = √(4 + 1) = √5. For B, B₁ = 3√5 · u₁v₁ᵀ = 3√5 · [[1, 1], [3, 3]]/(√10 · √2) = (3/2) [[1, 1], [3, 3]]. Only σ₂ = √5 remains, so both errors equal √5. Check: B − B₁ = [[3/2, −3/2], [−1/2, 1/2]], whose squared entries sum to 9/4 + 9/4 + 1/4 + 1/4 = 5.

---

## 4. Numerical Rank

In floating-point arithmetic, a singular value that is zero in exact arithmetic usually comes out as a tiny nonzero number. "The rank is the number of nonzero σ" must then become "the number of σ above a tolerance", and the tolerance must be **relative** to σ₁: multiplying A by 10^6 multiplies every singular value by 10^6 and does not change the rank. A common convention, the one of NumPy's `matrix_rank`, is max(m, n) · σ₁ · ε, where ε = 2^-52 is the machine epsilon of MAT-003. An absolute tolerance measures the scale of the matrix, not its rank.

The same tolerance governs the **pseudo-inverse** A⁺ = V Σ⁺ Uᵀ, where Σ⁺ inverts the singular values above the tolerance and sets the others to 0; A⁺b is the least-squares solution of smallest norm. There the choice matters twice: a singular value kept just above the tolerance contributes the huge term 1/σ.

### Practice Exercise

A library declares every singular value below 10^-10 to be zero. Which rank does it report for 10^-12 · I₃, and which does the relative convention report?

> *Solution:* The three singular values of 10^-12 · I₃ all equal 10^-12, below 10^-10, so the library reports rank 0 for a matrix of rank 3. The relative tolerance is 3 · 10^-12 · ε, about 6.7 · 10^-28, far below 10^-12, so the relative convention reports rank 3. Only the relative answer stays the same when the matrix is rescaled.

---

## 5. Computing the SVD by One-Sided Jacobi

The **one-sided Jacobi method** (Hestenes, 1958) never forms AᵀA, whose condition number is the square of that of A when A has full column rank (MAT-003). It rotates pairs of columns of A itself, which multiplies A on the right by plane rotations, until all the columns are orthogonal. At that point A V = W, where V is the product of the rotations and the columns of W are orthogonal: their norms are the singular values, and the normalised columns form U.

For two columns a_p and a_q, the rotation is the Jacobi rotation of MAT-005 §4 applied to the 2 × 2 matrix [[a_p · a_p, a_p · a_q], [a_p · a_q, a_q · a_q]], a block of AᵀA computed from the two columns alone. After the rotation the two columns are orthogonal. As in MAT-005, a later rotation can spoil an earlier one, so the method sweeps over all the pairs repeatedly.

### Practice Exercise

Apply one rotation to the columns a_p = (3, 4) and a_q = (0, 5) of the matrix B of §1, with the update a_p ← c a_p − s a_q and a_q ← s a_p + c a_q.

> *Solution:* a_p · a_p = 25, a_q · a_q = 25 and a_p · a_q = 20, so θ = (25 − 25)/(2 · 20) = 0, which gives t = 1 and c = s = 1/√2. The new columns are ((3, 4) − (0, 5))/√2 = (3, −1)/√2 and ((3, 4) + (0, 5))/√2 = (3, 9)/√2. They are orthogonal, since 9 − 9 = 0, with norms √10/√2 = √5 and √90/√2 = 3√5: the singular values of §1. Normalising them gives u₂ = (3, −1)/√10 and u₁ = (1, 3)/√10.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**The solver** (`crates/ix-math/src/svd.rs`). [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100) is the one-sided Jacobi method of §5, with at most 50 sweeps and a tolerance of 10^-12. It returns the thin SVD, with the singular values in descending order. The test that skips an already orthogonal pair is [relative](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L136) to the sizes of the two columns, so the rotations do not depend on the scale of A. The comment on the stopping test claims the same property, verbatim from lines 168–176:

```rust
        // Scale-invariant stopping criterion: the off-diagonal Frobenius
        // mass should be a small fraction of the matrix's total Frobenius
        // mass. Using an absolute threshold (the old behavior) meant that
        // well-scaled matrices converged in 1-2 sweeps while any matrix
        // with entries much larger than `tol` stayed above the threshold
        // indefinitely.
        if off_diag_sum_sq < tol * tol * a_frob_sq {
            break;
        }
```

Its contract has four limits worth knowing:
- **The stopping test is not scale-invariant.** `off_diag_sum_sq` adds up the squares of the products a_p · a_q, which are entries of AᵀA: multiplying A by s multiplies it by s⁴. `a_frob_sq` is ‖A‖_F², multiplied by s². The two sides have different degrees: the test asks for √`off_diag_sum_sq` < (10^-12/‖A‖_F) · ‖A‖_F², a tolerance of 10^-12/‖A‖_F relative to the size of AᵀA, instead of 10^-12. When ‖A‖_F is large, that tolerance falls below what is usually left once the method has converged: the pairs the skip test leaves alone, whose product is below 10^-12 relative to the column sizes but not zero, and rounding (MAT-003). For such a matrix the test is never met, and the call runs all 50 sweeps: the result stays accurate, since nothing rotates any more, but it costs many times more. Only products that are exactly zero still stop it early, as for a multiple of the identity, whose first sweep finds `off_diag_sum_sq` = 0. When ‖A‖_F is of the order of 10^-12 or less, the test is met at the end of the first sweep, which, with more than two columns, can leave them far from orthogonal. Comparing `off_diag_sum_sq` with `tol * tol * a_frob_sq * a_frob_sq` would give both sides the degree 4.
- **The promise is not checked.** The doc comment says ["Guaranteed to converge for any real matrix"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L97). The theory does guarantee it, but the [sweep loop](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L123) stops after 50 sweeps, and the function then returns [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L209) whether or not the stopping test was met.
- **One absolute threshold remains.** The left singular vectors are extracted by the loop below, verbatim from lines 195–207. A column of U is filled only when its singular value exceeds `tol`, the absolute 10^-12; otherwise it stays zero, and `reconstruct` then drops that term. The singular values scale with A, but this test does not, like the pivot threshold of `inverse` in MAT-003. The exercise below shows the consequence.

```rust
    // Take top-k columns.
    let mut v_sorted = Array2::<f64>::zeros((n, k));
    for (rank, (sig, orig)) in sigma_col.into_iter().take(k).enumerate() {
        singular_values[rank] = sig;
        if sig > tol {
            for i in 0..m {
                u[[i, rank]] = work[[i, orig]] / sig;
            }
        }
        for i in 0..n {
            v_sorted[[i, rank]] = v[[i, orig]];
        }
    }
```

- **The caller chooses the rank tolerance.** [`rank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) and [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) compare the singular values with an absolute `tol` passed by the caller, and making it relative is the caller's job. Two callers do so, differently. The handler of the MCP tool `ix_svd`, [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L627), uses [σ₁ · 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639). The state-space rank test uses [max(m, n) · σ₁ · ε](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L397), the convention of §4, with a [note](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L395) that the Jacobi SVD leaves a singular value that is zero in exact arithmetic near 10^-16 · σ₁ rather than at 0.

[`truncated_svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L223) computes the full SVD and keeps its first k components: the A_k of §3. The MCP tool `ix_svd` does not offer it: its [input schema](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L435) takes a matrix and nothing else.

Two tests deserve a closer look. [`test_svd_scale_invariance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L327) checks that scaling A [by 10^6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L333) scales the singular values and keeps the reconstruction accurate. Its comment says the relative criterion fixed the old one, which "would have required many more sweeps to converge (or failed to converge within the default 50)". The assertions check accuracy, not sweeps: ‖10^6 · A‖_F is about 10^7, so by the first limit above the stopping test asks for a relative tolerance of about 10^-19, below the rounding level of MAT-003, and the call is predicted to run all 50 sweeps, the case the comment describes as fixed. The test also scales only upward, while the absolute threshold above acts downward. [`test_truncated_svd_rank_1_approx`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L305) checks that the rank-1 truncation of A = [[1, 2], [3, 4], [5, 6]] has a relative Frobenius error [below 0.10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L315). Eckart–Young gives the exact value: AᵀA = [[35, 44], [44, 56]] has the characteristic polynomial λ² − 91λ + 24, with roots (91 ± √8185)/2, so σ₁ ≈ 9.53, σ₂ ≈ 0.514, ‖A‖_F = √91 and the best relative error is σ₂/√91 ≈ 0.054. The test would also accept an approximation up to 1.8 times worse than the best one.

**MAT-003's open question.** In the Learn lab, MAT-003 measured that IX's κ₂ of the stored Hilbert matrices fl(H_2) to fl(H_16) changes, for 10 of the 15 sizes, when the matrix is multiplied by 2^-20 or 2^20, and it left the cause open. The stopping test accounts for it. Multiplying by a power of two is exact, and as long as nothing underflows or overflows, as here, so is every operation of `svd` on the scaled matrix: each product, each rotation and each skip decision is that of fl(H_n), times a power of two. Only the number of sweeps can differ, and where the extra sweeps still rotate, the bits change. A Python transcription of `svd` that follows the summation order of `ndarray` predicts from 2 to 4 sweeps at 2^-20, from 2 to 6 at scale 1, and all 50 at 2^20. It reproduces the 15 values of κ₂ that the lab printed, to the three digits printed, and its count of 5 identical sizes out of 15. That is analysis, not an IX run; step 4 of §7 lets the lab check it with [`svd_with_opts`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L105), which caps the number of sweeps.

### Practice Exercise

With A = [[1, 2], [3, 4], [5, 6]], predict what `svd(10^-13 · A).reconstruct()` and `svd(10^-12 · A).reconstruct()` return.

> *Solution:* A has two columns, so a single rotation makes them orthogonal, whatever the stopping test decides, and that rotation depends only on ratios of the column products, so it is the rotation used for A. The singular values therefore come out as those of A times the scale, up to rounding. For 10^-13 · A, they are about 9.53 · 10^-13 and 5.14 · 10^-14, both below 10^-12: both columns of U stay zero, and `reconstruct` returns the zero matrix, a relative error of 1. For 10^-12 · A, they are about 9.53 · 10^-12, kept, and 5.14 · 10^-13, dropped: `reconstruct` silently returns the rank-1 truncation, with a relative error of about 0.054, which is exactly the Eckart–Young error of the test above and looks plausible. This is a prediction from reading the code, not a run; §7 checks it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Eckart–Young for every k.** On A = [[1, 2], [3, 4], [5, 6]] and on M = [[1, 2, 3], [4, 5, 6], [7, 8, 10]], the matrix of IX's [MCP test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1311), compute ‖A − A_k‖_F with `truncated_svd` for every k, and compare it with √(σₖ₊₁² + …) computed from `svd`. Prediction: equal within 10^-9 · ‖A‖_F, decreasing in k, and 0 up to rounding at k = rank A.
2. **A scale sweep.** For s = 10^-14, 10^-13, …, 10^12, compute the singular values of s · A and of s · M divided by s, and the relative error of `reconstruct`. Prediction for A: the singular values match those of A within a relative 10^-12 at every scale; the relative error is below 10^-12 for s ≥ 10^-11, about 0.054 for s = 10^-12, and exactly 1 for s ≤ 10^-13. Prediction for M: the singular values match within a relative 10^-12 for s ≥ 10^-10; for s ≤ 10^-13, where the loop stops after the first sweep, at least one of them is wrong by more than 100%.
3. **The cost of scale.** Time many calls of `svd` on A and on 10^6 · A, and on M and 10^6 · M. Prediction: the scaled calls take several times longer, since they run all 50 sweeps.
4. **MAT-003's puzzle.** For n = 2 to 16, compute `svd_with_opts(2^20 · fl(H_n), k, 10^-12)` for k = 1 to 6 and divide its singular values by 2^20. At that scale the stopping test is never met, so exactly k sweeps run. Prediction: the result reproduces bit for bit the singular values of `svd(fl(H_n))` for a first value of k, and those of `svd(2^-20 · fl(H_n))` divided by 2^-20 for a second one: k = 2 and 2 for n = 2, 4 and 3 for n = 3 to 6, 5 and 4 for n = 7 to 14, and 6 and 4 for n = 15 and 16.
5. **Rank conventions.** Call `ix_svd` on [[1, 2], [2, 4]]. Prediction: rank 1. Call `rank` with the tolerance 10^-10 on the SVD of 10^-12 · I₃. Prediction: 0, against 3 with the relative convention of §4.
6. **The test's bound.** Compute the relative error of the rank-1 truncation of the test matrix. Prediction: 0.054 to three decimal places, against the bound 0.10 that the test checks.

### Practice Exercise

Suppose step 2 confirms that the singular values of s · A are proportional to s at every scale. Why is that not enough to trust `svd` at every scale?

> *Solution:* First, the singular values can be right while U is wrong: below 10^-12, the columns of U stay zero although the singular values are correct. Second, A has only two columns, so one rotation settles it, and an early stop after the first sweep cannot show there; M, with three columns, is predicted to show it. A trustworthy check tests the invariants of the whole decomposition, A = U Σ Vᵀ and orthonormal columns of U for every nonzero singular value, as in MAT-005 §5, on matrices with more than two columns, and at every scale, not only the one the tests use.

---

## 8. Common Pitfalls

- **Computing singular values as square roots of the eigenvalues of AᵀA.** Forming AᵀA squares the condition number of a matrix of full column rank, and the small singular values lose accuracy first.
- **Using an absolute rank threshold.** It measures the scale of the matrix, not its rank.
- **Trusting the singular values alone.** U and V can be broken while the singular values are right: test A = U Σ Vᵀ.
- **Testing a known quantity with a loose bound.** When a theorem gives the exact error, a test with a bound almost twice as large lets errors through.
- **Confusing singular values with eigenvalues.** For a symmetric matrix, the singular values are the absolute values of the eigenvalues, but not in general: the shear of self-check 2 has the eigenvalues 1 and 1.
- **Comparing quantities of different degrees.** A test is scale-invariant only if both sides scale alike: a sum of squared entries of AᵀA has degree 4 in A, ‖A‖_F² has degree 2.
- **Reading a comment as a guarantee.** "Guaranteed to converge" is a theorem about the method, and "scale-invariant" a claim about the code; the code still has to report the first and a test has to check the second.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Singular value decomposition** | A = U Σ Vᵀ, with U and V orthogonal and Σ diagonal with entries σ₁ ≥ σ₂ ≥ … ≥ 0 |
| **Singular values** | The diagonal entries of Σ: the square roots of the eigenvalues of AᵀA |
| **Left and right singular vectors** | The columns uᵢ of U and vᵢ of V, with A vᵢ = σᵢ uᵢ |
| **Thin SVD** | The SVD keeping only the first min(m, n) columns of U and V |
| **Frobenius norm** | ‖A‖_F, the square root of the sum of the squares of all the entries, equal to √(σ₁² + σ₂² + …) |
| **Rank-k truncation** | A_k = σ₁u₁v₁ᵀ + … + σₖuₖvₖᵀ |
| **Eckart–Young–Mirsky theorem** | A_k is a best approximation of rank at most k, with errors σₖ₊₁ in the 2-norm and √(σₖ₊₁² + …) in the Frobenius norm |
| **Numerical rank** | The number of singular values above a tolerance relative to σ₁ |
| **Pseudo-inverse** | A⁺ = V Σ⁺ Uᵀ, which inverts the singular values above the tolerance |
| **One-sided Jacobi** | Rotating pairs of columns of A until they are orthogonal; their norms are the singular values |

---

## Self-Check Assessment

**1. Why are the singular values of every real matrix real and non-negative, when its eigenvalues need not be?**
> They are the square roots of the eigenvalues of AᵀA, which is symmetric, so its eigenvalues are real (MAT-005), and satisfies xᵀAᵀAx = ‖Ax‖² ≥ 0, so they are non-negative.

**2. The shear S = [[1, 1], [0, 1]] has the eigenvalue 1, twice. What are its singular values, and what is κ₂(S)?**
> SᵀS = [[1, 1], [1, 2]] has the characteristic polynomial λ² − 3λ + 1, with roots (3 ± √5)/2. Their square roots are σ₁ = (1 + √5)/2, the golden ratio, and σ₂ = (√5 − 1)/2, its inverse, since ((1 ± √5)/2)² = (3 ± √5)/2. So κ₂(S) = σ₁/σ₂ = (3 + √5)/2, about 2.62, although both eigenvalues are 1: for a non-symmetric matrix, the eigenvalues do not show the conditioning.

**3. Why is the 2-norm error of the best rank-k approximation σₖ₊₁ and not √(σₖ₊₁² + σₖ₊₂² + …)?**
> The singular values of A − A_k are σₖ₊₁, σₖ₊₂, …, and the 2-norm of a matrix is its largest singular value, σₖ₊₁. The Frobenius norm adds up the squares of all of them.

**4. IX's `test_svd_scale_invariance` passes. What does it guarantee about scale, and what does it miss?**
> It checks that scaling up by 10^6 keeps the singular values and the reconstruction accurate. It misses the cost: at that scale the stopping test is never met, and the call is predicted to run all 50 sweeps. It also misses scaling down, where the absolute threshold of 10^-12 on the singular values leaves columns of U at zero, and `reconstruct` silently drops terms (§6).

**Pass criteria:** Derive and compute an SVD by hand, read the norm, rank, conditioning and determinant off the singular values, compute best low-rank approximations and their errors, choose a relative rank tolerance, carry out a one-sided Jacobi rotation, and spot where IX's SVD depends on the scale of its input.

---

## Research Basis

- C. Eckart and G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1, 1936: the best low-rank approximation in the Frobenius norm
- L. Mirsky, "Symmetric gauge functions and unitarily invariant norms", *Quarterly Journal of Mathematics* 11, 1960: the same result for every unitarily invariant norm, including the 2-norm
- M. R. Hestenes, "Inversion of matrices by biorthogonalization and related results", *Journal of the Society for Industrial and Applied Mathematics* 6, 1958: the one-sided Jacobi method
- J. Demmel and K. Veselić, "Jacobi's method is more accurate than QR", *SIAM Journal on Matrix Analysis and Applications* 13, 1992: the accuracy of Jacobi methods
- L. N. Trefethen and D. Bau, *Numerical Linear Algebra*, SIAM, 1997, lectures 4–5: the SVD, its geometry and low-rank approximation
- G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013, chapters 2 and 8: the SVD, numerical rank and Jacobi SVD methods
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
