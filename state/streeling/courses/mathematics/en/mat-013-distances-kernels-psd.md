---
module_id: mat-013-distances-kernels-psd
department: mathematics
course: Distances, Kernels and Positive Semidefinite Matrices
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Distances, Kernels and Positive Semidefinite Matrices — When a Similarity Is Really an Inner Product

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- State the metric axioms, and decide whether a given distance satisfies them
- Recognise positive semidefinite matrices, test them with eigenvalues, and exhibit a witness when a matrix fails
- Explain what makes a kernel valid, and build or reject kernels with Gram matrices
- Describe how the bandwidth of the Gaussian kernel moves its Gram matrix between the identity and a rank-one matrix
- Use the Mahalanobis distance, and say which matrices make it a metric
- Trace what IX's distances, kernels and eigenvalue test guarantee, and where rounding or a silent clamp breaks an axiom

---

## 1. Metrics and What They Promise

A **metric** on a set is a function d(x, y) with four properties: d(x, y) ≥ 0; d(x, y) = 0 exactly when x = y; d(x, y) = d(y, x); and the **triangle inequality** d(x, z) ≤ d(x, y) + d(y, z). A **pseudometric** drops one half of the second axiom: distinct points may be at distance 0. Algorithms rely on these axioms: a nearest-neighbour index prunes a whole region with the triangle inequality, and a clustering method that merges points at distance 0 assumes they are the same point.

The Minkowski distances (Σ|xᵢ − yᵢ|^p)^(1/p) of MAT-004 are metrics for p ≥ 1. For p = 1/2 the triangle inequality fails: from (0, 0) to (1, 1) the formula gives (1 + 1)² = 4, while the detour through (1, 0) costs 1 + 1 = 2. The squared Euclidean distance fails too, on the points 0, 1 and 2 of the line: 4 > 1 + 1. It is useful for comparing distances, since squaring preserves their order, but it is not itself a metric.

### Practice Exercise

The cosine distance is 1 − cos θ, where θ is the angle between two nonzero vectors. Is it a metric? What about the angle θ itself?

> *Solution:* No. Take unit vectors at 0°, 45° and 90°. The distances between neighbours are 1 − √2/2 ≈ 0.2929 each, their sum 0.5858, while the distance from 0° to 90° is 1: the triangle inequality fails, so it is not even a pseudometric. The angle θ = arccos(cos θ) is a metric on the unit sphere: it is the length of the shortest arc, and here π/4 + π/4 = π/2, with equality. On vectors that are not normalised, the angle is only a pseudometric, since x and 2x are at angle 0.

---

## 2. Positive Semidefinite Matrices

A symmetric matrix A is **positive semidefinite** (PSD) if xᵀAx ≥ 0 for every vector x, and **positive definite** if xᵀAx > 0 for every x ≠ 0. By the spectral theorem of MAT-005, A = QΛQᵀ with Q orthogonal, so xᵀAx = Σλᵢ(qᵢ · x)²: A is PSD exactly when all its eigenvalues are ≥ 0, and positive definite when all are > 0. Every **Gram matrix** G = BBᵀ, whose entry (i, j) is the inner product of rows i and j of B, is PSD, since xᵀGx = ‖Bᵀx‖² ≥ 0. Conversely, every PSD matrix is a Gram matrix: A = (QΛ^(1/2))(QΛ^(1/2))ᵀ.

Three practical tests follow. The eigenvalue test computes the smallest eigenvalue and compares it with a tolerance, since rounding moves eigenvalues by about u‖A‖ (MAT-003). The **Cholesky factorisation** A = LLᵀ, with L lower triangular, succeeds exactly for positive definite matrices and costs about n³/3 operations, far less than an eigendecomposition. And a single vector x with xᵀAx < 0 is a **witness** that A is not PSD, easy to check by hand. Sylvester's criterion, that the leading principal minors are positive, characterises positive definite matrices only; for PSD, every principal minor must be ≥ 0, not just the leading ones.

### Practice Exercise

A "similarity" gives 1 to points at most one step apart on the line: T = [[1, 1, 0], [1, 1, 1], [0, 1, 1]] for the points 0, 1 and 2, written row by row. Is T PSD?

> *Solution:* No. For x = (1, −1, 1), Tx = (0, 1, 0), so xᵀTx = −1 < 0: x is a witness. The eigenvalues are 1 − √2 ≈ −0.414, 1 and 1 + √2 ≈ 2.414; they sum to the trace 3, and their product is the determinant −1. All the diagonal entries are positive and every row looks like a similarity, yet T is not the Gram matrix of any vectors.

---

## 3. Kernels

A **kernel** k(x, y) is a similarity that is an inner product in some feature space: k(x, y) = φ(x) · φ(y) for a map φ. A function k is a **positive definite kernel** when every Gram matrix Kᵢⱼ = k(xᵢ, xⱼ), for every finite set of points, is PSD; by the Moore–Aronszajn theorem, this is exactly the condition for such a φ to exist, possibly with values in an infinite-dimensional space. Mercer's theorem states the same condition for continuous kernels through their integral operator. Sums, products and positive multiples of kernels are kernels, which is how most kernels are built.

The three classical kernels are the **linear** kernel x · y; the **polynomial** kernel (γ x · y + c)^d, a kernel when d is a positive integer, γ > 0 and c ≥ 0; and the **Gaussian** or **RBF** kernel exp(−γ‖x − y‖²), a kernel for every γ > 0. Every kernel defines a distance in feature space, d_k(x, y)² = k(x, x) + k(y, y) − 2k(x, y), a pseudometric in general and a metric when φ is injective. The cosine similarity is the linear kernel of the normalised vectors x/‖x‖, and its kernel distance is √(2 − 2 cos θ), the chord between them: the square root of twice the cosine distance of §1 is a metric on the unit sphere, while the cosine distance itself is not.

### Practice Exercise

Is k(x, y) = (xy − 1)² a kernel on the real line? Use the points 0, 1 and 2.

> *Solution:* No. Its Gram matrix on 0, 1 and 2 is [[1, 1, 1], [1, 0, 1], [1, 1, 9]]. The principal minor on the points 0 and 1, [[1, 1], [1, 0]], has determinant −1 < 0, so the matrix is not PSD. Here c = −1 < 0: expanding gives (xy)² − 2xy + 1, and the term −2xy subtracts a kernel. With c = +1, (xy + 1)² = φ(x) · φ(y) for φ(x) = (x², √2 x, 1).

---

## 4. The Bandwidth of the Gaussian Kernel

The parameter γ of the RBF kernel sets the scale at which points count as similar, often written γ = 1/(2σ²) with a bandwidth σ. As γ grows, every off-diagonal entry tends to 0 and K tends to the identity: every point is similar only to itself, and a method built on K memorises its training set. As γ shrinks, every entry tends to 1 and K tends to the all-ones matrix, whose eigenvalues are n, 0, …, 0: every point looks like every other.

Between the two, K is PSD but can be badly conditioned. On the points 0, 1 and 2 of the line, the smallest eigenvalue of K is about 0.489 for γ = 1, 0.0124 for γ = 0.1, 1.3 · 10^-4 for γ = 0.01 and 1.3 · 10^-6 for γ = 10^-3, where the condition number reaches about 2.2 · 10^6: by the rule of MAT-003, a solve with K can lose six digits. With more points or a smaller γ, an exactly PSD matrix can have a computed eigenvalue slightly below 0, so an eigenvalue test must accept values down to a tolerance proportional to n u ‖K‖, and must not treat every negative number as a verdict. A common starting value sets σ to the median distance between points.

### Practice Exercise

For n distinct points, what do the RBF Gram matrix and its eigenvalues tend to as γ → ∞ and as γ → 0?

> *Solution:* As γ → ∞, exp(−γ‖xᵢ − xⱼ‖²) → 0 for i ≠ j, so K → I, with all eigenvalues equal to 1: perfectly conditioned, and no two points similar. As γ → 0, every entry tends to 1, so K → 11ᵀ, with eigenvalues n and 0 repeated n − 1 times: the smallest eigenvalues tend to 0 and the condition number grows without bound.

---

## 5. The Mahalanobis Distance

For a random vector with covariance matrix S, the **Mahalanobis distance** is d_M(x, y) = √((x − y)ᵀ M (x − y)) with M = S⁻¹. It measures differences in units of the spread along each direction: with S = diag(4, 1), the points (2, 0) and (0, 0) are at distance 1, as far apart as (0, 1) and (0, 0). If S = LLᵀ is a Cholesky factorisation, d_M(x, y) = ‖L⁻¹(x − y)‖: the Mahalanobis distance is the Euclidean distance after **whitening** the data.

The matrix M decides whether d_M is a metric. If M is symmetric positive definite, it is. If M is only PSD, directions in its null space are invisible, and d_M is a pseudometric. If M has a negative eigenvalue, the quantity under the square root can be negative, and d_M is not a distance at all. Only the symmetric part (M + Mᵀ)/2 enters the quadratic form, so a non-symmetric M hides what it actually measures.

### Practice Exercise

Let M = [[1, 2], [0, 1]]. Its determinant is 1, so it is invertible. Is √((x − y)ᵀ M (x − y)) a metric?

> *Solution:* No. With d = x − y, dᵀMd = d₁² + 2d₁d₂ + d₂² = (d₁ + d₂)². It is never negative, but it vanishes whenever d₂ = −d₁: the points (1, −1) and (0, 0) are distinct and at distance 0. The symmetric part [[1, 1], [1, 1]] has eigenvalues 2 and 0, so the "distance" is a pseudometric that sees only d₁ + d₂. Invertibility of M is not the condition; positive definiteness of its symmetric part is.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of the functions below into Python, whose floats are IEEE binary64 like Rust's `f64`: they are predictions, and §7 proposes to check them.

**Distances** (`crates/ix-math`). [`distance.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L60) provides the Euclidean, Manhattan, Minkowski, Chebyshev and cosine functions; the Minkowski distance [rejects p < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L48), the condition of §1. The MCP tool `ix_distance`, through the handler [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L148), offers the Euclidean, Manhattan and [cosine](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L163) metrics. [`GeometricSpace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L38) puts eleven distances behind one [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L87) function, among them the [Mahalanobis distance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L61), which takes an inverse covariance from the caller; the module is [exported](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/lib.rs#L14), and no code outside its own tests calls it. The cosine functions read:

```rust
/// Cosine similarity (not distance). Returns value in [-1, 1].
pub fn cosine_similarity(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    let dot: f64 = a.dot(b);
    let norm_a = a.dot(a).sqrt();
    let norm_b = b.dot(b).sqrt();
    if norm_a < 1e-12 || norm_b < 1e-12 {
        return Ok(0.0);
    }
    Ok(dot / (norm_a * norm_b))
}

/// Cosine distance = 1 - cosine_similarity.
pub fn cosine_distance(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    cosine_similarity(a, b).map(|s| 1.0 - s)
}
```

- **A cosine distance can be negative.** For x = (1, 1, 1), the dot product is 3 and each norm is √3, but the product of the two rounded norms is 2.9999999999999996, so the similarity of x with itself is 1 + 2^-52 and its [distance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L73) to itself is −2^-52 ≈ −2.2 · 10^-16. Nothing clamps the value, so the documented range [−1, 1] and the axiom d ≥ 0 both fail; for x = (1, 1) the self-distance is +2^-52 instead. The spherical distance of `GeometricSpace` does [clamp its cosine](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L113). The DuckDB extension states the [invariant](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/udf.rs#L224) "identical vectors -> 0.0", and its test uses [(1, 2, 3)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/lib.rs#L311), for which the rounding happens to be exact.
- **A zero vector is at distance 1 from itself.** When a norm is below 10^-12, the similarity [returns 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L66), so the cosine distance of 0 to 0 is 1. The spherical distance makes the [opposite choice](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L111): the zero vector is at distance 0 from every vector, including (1, 0) and (0, 1), which are π/2 apart, so the triangle inequality fails through it.
- **A negative Mahalanobis form is clamped to 0.** The Mahalanobis branch below checks [only the shape](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L136) of the matrix, not its symmetry or definiteness, and [takes the maximum with 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L145) before the square root. With the "inverse covariance" diag(1, −1), the points (1, 1) and (0, 0) are at distance 0, and so are (0, 1) and (0, 0), whose quadratic form is −1: no error is raised, and each pair of distinct points gets distance 0. With [[1, 2], [0, 1]], the matrix of §5, the pair (1, −1) and (0, 0) also gets 0.
- **Hamming's tolerance breaks the triangle inequality.** The Hamming distance counts coordinates that [differ by more than 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L168). Equality up to a tolerance is not transitive: for the one-coordinate points 0, 6 · 10^-13 and 1.2 · 10^-12, the distances are 0, 0 and 1.
- **Chebyshev ignores NaN.** The Chebyshev distance takes a [running maximum with `f64::max`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L82), which returns the other operand when one is NaN: (NaN, 0) and (0, 0) are at Chebyshev distance 0, while their Euclidean distance is NaN.
- **Kernels are not validated, and negative eigenvalues are clamped.** Kernel PCA offers the [`Kernel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L53) variants of §3, with a [polynomial degree of type `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) raised with [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), and an [RBF](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L232) that accepts γ of either sign. Nothing rejects c < 0, a fractional degree or γ < 0, which can give Gram matrices that are not PSD, or NaN entries when a negative base is raised to a fractional power, and the fit [replaces each negative eigenvalue by 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) without reporting it. The module documentation says custom kernels can be added by [implementing the `Kernel` trait](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L20), but `Kernel` is an enum, not a trait.
- **The eigenvalue test depends on the scale.** IX has no PSD test and no Cholesky factorisation, so the eigenvalue test of §2 must go through [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46), the Jacobi method of MAT-005, whose tolerance of [10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) is absolute. Its [stopping test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82) passes before the first rotation for 10^-13 T, the matrix of §2 scaled down, so the function returns the diagonal, 10^-13 three times, and an indefinite matrix passes as PSD. At 8 · 10^-13 T it stops after one sweep of three rotations with about −2.9 · 10^-13 instead of the exact 8 · 10^-13 (1 − √2) ≈ −3.3 · 10^-13.

The Mahalanobis branch of `distance`:

```rust
        GeometricSpace::Mahalanobis { inv_cov } => {
            let n = a.len();
            if inv_cov.shape() != [n, n] {
                return Err(MathError::DimensionMismatch {
                    expected: n,
                    got: inv_cov.shape()[0],
                });
            }
            let diff = a - b;
            let sx = inv_cov.dot(&diff);
            let acc = diff.dot(&sx);
            Ok(acc.max(0.0).sqrt())
        }
```

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Why is the cosine distance of (1, 1, 1) to itself negative, while that of (1, 2, 3) to itself is exactly 0?

> *Solution:* The code divides the dot product by the product of two separately rounded square roots. For (1, 1, 1), √3 rounds to a double whose square, 2.9999999999999996, is just below 3, so 3 divided by it is 1 + 2^-52 and 1 minus that is −2^-52. For (1, 2, 3), the dot product is 14, and the rounded √14 squared happens to round back to exactly 14, so the similarity is exactly 1. Whether the self-distance is 0, slightly positive or slightly negative depends on how one rounding falls, which is why a distance built from a similarity should be clamped at 0, or computed as ‖x/‖x‖ − y/‖y‖‖²/2, which is never negative.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Gram matrices.** On the points (0, 0), (1, 0), (0, 1), (1, 1) and (2, 1), build the Gram matrices of the linear kernel, of the RBF kernel with γ = 0.5 and of the polynomial kernel (x · y + 1)², and pass each to `symmetric_eigen`. Prediction: the linear matrix has rank 2, with its three smallest eigenvalues within 10^-12 of 0; the smallest eigenvalues of the other two are about 0.133 and 0.298. With c = −1 in the polynomial kernel, and with γ = −0.5 in the RBF kernel, the smallest eigenvalues are about −1.08 and −12.6.
2. **The threshold similarity and its scale.** Pass T of §2 to `symmetric_eigen`. Prediction: its smallest eigenvalue is 1 − √2 within 10^-12. Then pass 10^-13 T and 8 · 10^-13 T. Prediction: the first returns 10^-13 three times; the second returns a smallest eigenvalue near −2.9 · 10^-13.
3. **Mahalanobis.** Call `distance` with `Mahalanobis` and `inv_cov` equal to diag(1, −1), on (1, 1) and (0, 0), then on (0, 1) and (0, 0); then with [[1, 2], [0, 1]] on (1, −1) and (0, 0). Prediction: all three return `Ok(0.0)`.
4. **Cosine.** Call the handler `distance` with `metric` set to `cosine` on a = b = (1, 1, 1), then on a = b = (1, 1), then on two zero vectors. Prediction: −2^-52, +2^-52 and 1.
5. **Hamming and Chebyshev.** Compute the Hamming distances among the one-coordinate points 0, 6 · 10^-13 and 1.2 · 10^-12, and the Chebyshev distance between (NaN, 0) and (0, 0). Prediction: 0, 0 and 1, and 0.
6. **The bandwidth.** On the points 0, 1 and 2, pass the RBF Gram matrices for γ = 1, 0.1, 0.01 and 10^-3 to `symmetric_eigen`. Prediction: smallest eigenvalues about 0.489, 0.0124, 1.3 · 10^-4 and 1.3 · 10^-6, each within 10^-12 of a reference eigensolver, and all positive.

### Practice Exercise

In step 2, for which scale factors c does `symmetric_eigen` return the diagonal of cT without a single rotation?

> *Solution:* The loop sums the squares above the diagonal, here 2c², and stops when the square root is below 10^-12, that is when √2 c < 10^-12, or c < 10^-12/√2 ≈ 7.07 · 10^-13. For all such c, the function returns c three times and the matrix looks positive definite. The threshold is absolute, so it has nothing to do with whether the matrix is PSD; a relative test, comparing the off-diagonal norm with the norm of the matrix, would not depend on c.

---

## 8. Common Pitfalls

- **Calling any dissimilarity a distance.** 1 − cos θ, the squared Euclidean distance and the Minkowski formula with p < 1 all fail the triangle inequality; check the axioms before using an index or a method that relies on them.
- **Trusting a similarity matrix because it looks right.** Positive diagonal and sensible entries do not make a matrix PSD; look for its smallest eigenvalue or for a witness x with xᵀAx < 0.
- **Testing PSD with the leading minors.** Sylvester's criterion characterises positive definite matrices; for PSD, all principal minors must be ≥ 0.
- **Treating a tiny negative eigenvalue as a verdict.** Rounding moves eigenvalues by about u‖A‖; compare with a tolerance scaled to the matrix, not with 0 or with an absolute constant.
- **Using a kernel outside its domain.** A polynomial kernel with c < 0 or a fractional degree, or an RBF with γ < 0, can give Gram matrices that are not PSD; clamping the negative eigenvalues afterwards hides the error.
- **Inverting a covariance and hoping.** The Mahalanobis distance needs a symmetric positive definite matrix; invertibility is not enough, and a clamp at 0 turns an error into a distance of 0.
- **Building a distance from a similarity without a clamp.** 1 − s can be negative by rounding when s should be 1; clamp at 0 or use a formula that cannot go negative.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Metric** | A function that is non-negative, zero only between equal points, symmetric, and satisfies the triangle inequality |
| **Pseudometric** | A metric that may give distance 0 to distinct points |
| **Triangle inequality** | d(x, z) ≤ d(x, y) + d(y, z) |
| **Positive semidefinite matrix** | A symmetric matrix with xᵀAx ≥ 0 for every x, equivalently with no negative eigenvalue |
| **Gram matrix** | The matrix of inner products of a set of vectors, always PSD |
| **Witness** | A vector x with xᵀAx < 0, proving that A is not PSD |
| **Cholesky factorisation** | A = LLᵀ with L lower triangular, which exists exactly for positive definite matrices |
| **Positive definite kernel** | A function whose Gram matrices are all PSD, equivalently an inner product of feature vectors |
| **RBF kernel** | exp(−γ‖x − y‖²), a kernel for every γ > 0, with bandwidth σ given by γ = 1/(2σ²) |
| **Mahalanobis distance** | √((x − y)ᵀ S⁻¹ (x − y)), the Euclidean distance after whitening by the covariance S |
| **Whitening** | A linear change of coordinates that turns a covariance matrix into the identity |

---

## Self-Check Assessment

**1. A clustering library accepts any "distance". Which axioms does it rely on, and which of 1 − cos θ, the angle θ and the squared Euclidean distance satisfy them?**
> Non-negativity, identity of indiscernibles, symmetry and the triangle inequality; the last is what lets an index prune a search. The angle is a metric on the unit sphere. 1 − cos θ fails the triangle inequality, as 0°, 45° and 90° show, and the squared Euclidean distance fails it on 0, 1 and 2.

**2. A 500 × 500 kernel matrix has a smallest computed eigenvalue of −3 · 10^-14, and its largest is 400. Is the kernel invalid?**
> Not on that evidence. A backward-stable eigensolver moves eigenvalues by a small multiple of u‖K‖, here u‖K‖ ≈ 400 · 1.1 · 10^-16 ≈ 4.4 · 10^-14, and the multiple grows with n, so −3 · 10^-14 is within rounding of 0. A valid kernel with nearly dependent points produces exactly this. A clearly negative eigenvalue, or a witness x that stays negative in exact arithmetic, would settle it.

**3. Why does the Mahalanobis distance need a positive definite matrix, and what does IX return when it is not?**
> With a positive definite M, (x − y)ᵀM(x − y) > 0 for x ≠ y and d_M is the Euclidean distance after whitening. A PSD but singular M collapses the directions of its null space, and an indefinite M makes the form negative for some pairs. IX checks only the shape and clamps negative forms to 0, so both failures come back as a distance of 0, without an error.

**4. `ix_distance` returns a cosine distance of −2.2 · 10^-16 for two identical vectors. Is that a bug in your data?**
> No. It is rounding in IX's formula: the product of the two rounded norms can fall just below the dot product, which makes the similarity exceed 1. Clamp the result at 0 before using it as a distance, and do not rely on exact zeros for identical inputs.

**Pass criteria:** State and check the metric axioms, test a matrix for positive semidefiniteness and produce a witness when it fails, decide whether a function is a kernel from its Gram matrices, explain the effect of the RBF bandwidth on conditioning, give the condition for the Mahalanobis distance to be a metric, and trace where IX's distances and eigenvalue test break an axiom.

---

## Research Basis

- M. Fréchet, "Sur quelques points du calcul fonctionnel", *Rendiconti del Circolo Matematico di Palermo* 22, 1906: metric spaces
- J. Mercer, "Functions of positive and negative type, and their connection with the theory of integral equations", *Philosophical Transactions of the Royal Society A* 209, 1909: positive definite kernels and integral operators
- P. C. Mahalanobis, "On the generalised distance in statistics", *Proceedings of the National Institute of Sciences of India* 2, 1936: the Mahalanobis distance
- I. J. Schoenberg, "Metric spaces and positive definite functions", *Transactions of the American Mathematical Society* 44, 1938: when a distance comes from an inner product, and the Gaussian kernel
- N. Aronszajn, "Theory of reproducing kernels", *Transactions of the American Mathematical Society* 68, 1950: the feature space of a positive definite kernel
- B. Schölkopf and A. J. Smola, *Learning with Kernels*, MIT Press, 2002: kernels, Gram matrices and their construction
- R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013: positive semidefinite matrices, Cholesky and Sylvester's criterion
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
