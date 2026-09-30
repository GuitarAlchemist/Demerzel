---
module_id: mat-015-classical-mds-distance-preservation
department: mathematics
course: Classical MDS and Distance Preservation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Classical MDS and Distance Preservation — Recovering Points From Their Distances, and Knowing When You Cannot

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Turn a matrix of distances into a matrix of inner products by double centring, and explain why the result is fixed only up to a rigid motion
- State the criterion of Schoenberg, Young and Householder: a distance matrix is Euclidean exactly when its double-centred matrix is positive semidefinite
- Compute a classical MDS configuration, and show that on Euclidean distances it returns the PCA scores
- Recognise non-Euclidean dissimilarities from the negative eigenvalues of the double-centred matrix, and measure how much they distort the configuration
- Tell classical MDS apart from metric MDS by stress, from non-metric MDS and from Isomap
- Trace what IX's `classical_mds` guarantees, and where a silent clamp or an absolute tolerance changes the answer

---

## 1. From Distances to Inner Products

Suppose that only the distances dᵢⱼ between n points are known, and not the points themselves. The law of cosines links distances to inner products: ‖xᵢ − xⱼ‖² = ‖xᵢ‖² + ‖xⱼ‖² − 2 xᵢ · xⱼ. Inner products depend on the origin and distances do not, so the distances determine the inner products once an origin is chosen. Classical scaling chooses the centroid x̄. Write D⁽²⁾ for the matrix of squared distances d²ᵢⱼ, and J = I − (1/n) 11ᵀ for the **centring matrix**. The **double-centred matrix** B = −½ J D⁽²⁾ J has the entries bᵢⱼ = −½ (d²ᵢⱼ − rᵢ − rⱼ + g), where rᵢ is the mean of row i of D⁽²⁾ and g the mean of all its entries, and it equals the Gram matrix of the centred points: bᵢⱼ = (xᵢ − x̄) · (xⱼ − x̄). Every row of B sums to 0, because the centred points sum to 0. The centring must be applied to the squared distances; applied to the distances themselves, it has no geometric meaning.

Distances do not change when the points are translated, rotated or reflected, so no method can recover the configuration beyond such a **rigid motion**. Double centring removes the translation by putting the centroid at the origin; the rotation and the reflection remain, and §4 returns to them.

### Practice Exercise

Three points on a line are at mutual distances d₁₂ = 1, d₂₃ = 2 and d₁₃ = 3. Compute B and recover the points.

> *Solution:* D⁽²⁾ = [[0, 1, 9], [1, 0, 4], [9, 4, 0]], with row means 10/3, 5/3 and 13/3 and overall mean 28/9. Then b₁₁ = −½(0 − 20/3 + 28/9) = 16/9, and in the same way B = xxᵀ with x = (−4/3, −1/3, 5/3). B has rank 1 and the single nonzero eigenvalue ‖x‖² = 14/3, so the points lie on a line, at −4/3, −1/3 and 5/3: the points 0, 1 and 3 shifted by their mean 4/3. The reflected answer (4/3, 1/3, −5/3) fits the distances equally well.

---

## 2. When Is a Distance Matrix Euclidean?

A symmetric matrix D with zero diagonal is a **Euclidean distance matrix** if there are points x₁, …, xₙ in some ℝᵐ with dᵢⱼ = ‖xᵢ − xⱼ‖. The criterion of Schoenberg (1935) and of Young and Householder (1938) states that D is Euclidean exactly when B is positive semidefinite, and that the smallest dimension m that works is the rank of B. One direction is §1: a Gram matrix is PSD (MAT-013). For the other, a PSD matrix B factors as B = YYᵀ with Y = QΛ^(1/2) (MAT-005), and the rows of Y are points with the right distances, since bᵢᵢ + bⱼⱼ − 2bᵢⱼ = d²ᵢⱼ for any symmetric D with zero diagonal.

Since B1 = 0, and Jx = x whenever the entries of x sum to 0, xᵀBx = −½ xᵀD⁽²⁾x for such x: D is Euclidean exactly when xᵀD⁽²⁾x ≤ 0 for every x whose entries sum to 0. A single vector x with xᵀBx < 0 is a **witness** that no configuration, in any dimension, has these distances.

The triangle inequality is necessary but not sufficient. In a Euclidean space, equality d(a, c) = d(a, b) + d(b, c) forces b to lie on the segment from a to c, at the prescribed distances from both. Shortest-path distances in a graph often reach this equality, and then the constraints can contradict one another.

### Practice Exercise

The star graph K₁,₃ has a centre joined to three leaves. Its shortest-path distances are 1 from the centre to each leaf and 2 between leaves, and they satisfy the triangle inequality. Are they Euclidean?

> *Solution:* No. Each pair of leaves is at distance 2 = 1 + 1 through the centre, so in a Euclidean space the centre would be the midpoint of every pair of leaves. The midpoint of leaves 1 and 2 and that of leaves 1 and 3 coincide only if leaves 2 and 3 do, yet they are 2 apart. In numbers: D⁽²⁾ has row means 3/4 for the centre and 9/4 for the leaves, and overall mean 15/8, so the centre's diagonal entry of B is b₀₀ = −½(0 − 3/2 + 15/8) = −3/16 < 0. The unit vector e₀ is a witness, and the eigenvalues of B are 2, 2, 0 and −1/4.

---

## 3. Classical MDS and PCA

**Classical multidimensional scaling** (Torgerson 1952), which Gower (1966) calls principal coordinate analysis, computes the eigendecomposition B = QΛQᵀ with λ₁ ≥ λ₂ ≥ …, keeps the k largest eigenvalues, and returns the n × k configuration Y = Q_kΛ_k^(1/2): row i holds the coordinates of point i. When D is Euclidean, YYᵀ is the best approximation of B of rank k in the Frobenius norm (Eckart–Young, MAT-006); in general, it is the best positive semidefinite one. This criterion on B, often called **strain**, is what classical MDS optimises, rather than the distances themselves.

When D comes from points with a centred data matrix X_c of size n × p, B = X_cX_cᵀ. With the SVD X_c = UΣVᵀ of MAT-006, B = UΣ²Uᵀ, so the nonzero eigenvalues of B are the σᵢ², which are n − 1 times the variances of MAT-014, and Y = U_kΣ_k = X_cV_k: classical MDS returns exactly the PCA scores, up to the sign of each column. Gower described this duality between the n × n and the p × p eigenproblems. MDS is the natural choice when only distances are known, or when p is much larger than n. PCA is cheaper when n is large and p small: its eigenproblem is p × p, and it never forms the n² distances.

### Practice Exercise

MAT-014 found the variances 8/3 and 2/3 for the four points (±2, 0) and (0, ±1). What are the eigenvalues of B for these points, and what configuration does classical MDS return with k = 2?

> *Solution:* The points are already centred, so B = X_cX_cᵀ, whose nonzero eigenvalues are those of X_cᵀX_c = diag(8, 2): n − 1 = 3 times 8/3 and 2/3. The other two eigenvalues are 0, since B has rank 2. The eigenvectors are (1, −1, 0, 0)/√2 for 8 and (0, 0, 1, −1)/√2 for 2, and multiplying them by √8 and √2 gives back the points (±2, 0) and (0, ±1), up to the sign of each coordinate.

---

## 4. What Distances Cannot Tell: Rigid Motions and Ties

The configuration returned by classical MDS is centred, but the data do not determine its orientation. Each eigenvector can be replaced by its opposite, which reflects the configuration. When two eigenvalues are equal, any orthonormal basis of their eigenspace serves as well as another, so the configuration can be rotated freely in that plane. The unit square is the simplest case: its matrix B has eigenvalues 1, 1, 0 and 0, and every rotation of the square about its centre is an equally valid answer. Two MDS maps of the same data, from two libraries or two runs, can therefore differ by a rotation or a reflection without either being wrong.

To compare two configurations Y₁ and Y₂, compare their distances, or align them first: the orthogonal matrix R that minimises ‖Y₁ − Y₂R‖_F is R = WZᵀ, where Y₂ᵀY₁ = WΣZᵀ is an SVD (Schönemann 1966). This **orthogonal Procrustes** alignment removes exactly the ambiguity that distances leave.

### Practice Exercise

Why can classical MDS recover a configuration only up to a rigid motion, and which part of that motion does it fix?

> *Solution:* Translations, rotations and reflections preserve every distance, so two configurations related by one of them have the same distance matrix, and nothing computed from the distances can tell them apart. Double centring fixes the translation by putting the centroid at the origin. The rest is left to the eigensolver: the sign of each eigenvector and, when eigenvalues tie as for the square, the choice of basis in their eigenspace.

---

## 5. Non-Euclidean Dissimilarities, Stress and Isomap

When B has negative eigenvalues, no configuration in any dimension reproduces D, and classical MDS keeps only positive eigenvalues. Dropping the negative ones changes the distances, and their size measures how far D is from Euclidean. Mardia (1978) proposed the fraction Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ|, which stays below 1 whenever negative eigenvalues are present. A plot of all the eigenvalues, negative ones included, is the best guide to choosing k.

The 4-cycle C₄, four points in a ring with shortest-path distances 1 between neighbours and 2 across, is the smallest example. As for the star, d(0, 2) = d(0, 1) + d(1, 2) and d(0, 2) = d(0, 3) + d(3, 2) would make points 1 and 3 both the midpoint of 0 and 2, yet they are 2 apart. B has the eigenvalues 2, 2, 0 and −1, and Mardia's fraction for k = 2 is 4/5.

Classical MDS is one member of a family. **Metric MDS** minimises a **stress**, such as Σ (dᵢⱼ − ‖yᵢ − yⱼ‖)², directly on the distances and by iteration; SMACOF, which works by majorisation, is the standard algorithm, and the classical solution is a common starting point (Borg and Groenen 2005). **Non-metric MDS** (Kruskal 1964) uses only the order of the dissimilarities: it fits a monotone transformation of them together with the configuration, which suits ratings and rankings whose numerical values mean little. **Isomap** (Tenenbaum, de Silva and Langford 2000) runs classical MDS on the shortest-path distances of a neighbourhood graph, to unroll data that lie on a curved surface; those distances are graph distances and, like those of C₄, they need not be Euclidean.

### Practice Exercise

For C₄, compute B, its eigenvalues, and the distances of the classical MDS configuration with k = 2.

> *Solution:* Every row of D⁽²⁾ is a rotation of (0, 1, 4, 1), with mean 3/2, and the overall mean is 3/2, so bᵢᵢ = 3/4, bᵢⱼ = 1/4 between neighbours and −5/4 across. The vector (1, −1, 1, −1)/2 is an eigenvector for −1, the vector of ones for 0, and the plane orthogonal to both carries the double eigenvalue 2. Dropping −1 adds ¼ vvᵀ to B, with v = (1, −1, 1, −1), which gives diagonal entries 1, entries 0 between neighbours and −1 across: the configuration is a square with side √2 ≈ 1.414 and diagonal 2. The distances across are exact, those between neighbours are stretched from 1 to 1.414, and Mardia's fraction is 4/(2 + 2 + 0 + 1) = 4/5.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of `classical_mds`, `pairwise_euclidean` and `symmetric_eigen` into Python, whose floats are IEEE binary64 like Rust's `f64`: they are predictions, and §7 proposes to check them.

**MDS** (`crates/ix-unsupervised`). [`classical_mds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L49) rejects [k = 0 and k ≥ n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L60), squares the input after averaging it with its transpose, double-centres it with the [formula of §1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L89), and hands B to [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L95), the Jacobi method of MAT-005. Its only caller outside tests is the DuckDB table function `ix_mds_project`, which [caps k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L344) at the number of features and at n − 1, and [builds the distances](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L345) from the input vectors with `pairwise_euclidean`; no MCP tool exposes MDS. Through IX's own interfaces, classical MDS therefore only sees Euclidean distances computed from features, where §3 shows that it returns the PCA scores. The squaring and the configuration read:

```rust
    // Square and symmetrize the distance matrix.
    let mut sq = Array2::<f64>::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            let d = 0.5 * (distances[[i, j]] + distances[[j, i]]);
            sq[[i, j]] = d * d;
        }
    }
```

```rust
    // Full symmetric eigendecomposition via ix-math::eigen — returns pairs
    // already sorted in descending order, so we just take the top k.
    let (eigenvalues, eigenvectors) = symmetric_eigen(&b)?;

    let mut embedding = Array2::<f64>::zeros((n, k));
    for r in 0..k {
        let lambda = eigenvalues[r].max(0.0);
        let scale = lambda.sqrt();
        for i in 0..n {
            embedding[[i, r]] = eigenvectors[[i, r]] * scale;
        }
    }
```

- **Non-Euclidean input is embedded without a signal.** The module documentation calls MDS ["a perfect fit"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L16) for ["Non-metric similarity data"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L17) and for [graphs through their shortest-path distances](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L18). The function never reports a negative eigenvalue: it [replaces each one by 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L99) before the square root. On C₄ with k = 2, it returns the square of side √2 of §5, with a mean distance error of 2(√2 − 1)/3 ≈ 0.276; k = 3 gives the same distances, since the third eigenvalue is 0. On the star, with k = 2 or 3, the leaves form an equilateral triangle of side 2 and the centre lands at its centroid, 2/√3 ≈ 1.155 from each leaf instead of 1, for a mean error of about 0.077. On the 6-cycle, whose B has the eigenvalues 6, 6, 3/2, 0, −2 and −2, k = 5 returns a fifth column of zeros. Non-metric data, in the sense of Kruskal's method, call for a fit to ranks, which the function does not perform; it treats every number as a distance.
- **Negative and asymmetric entries pass silently.** The documentation says that the function [symmetrizes defensively](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L48). It [averages dᵢⱼ and dⱼᵢ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L71) whatever their difference, and [squares the result](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L72), so a negative entry loses its sign: [[0, −1], [−1, 0]] gives the same embedding ±0.5 as [[0, 1], [1, 0]], and a pair of entries 0 and 2 becomes a distance of 1, without an error. Neither the sign, the symmetry nor the zero diagonal is checked.
- **An absolute tolerance collapses small configurations.** `symmetric_eigen` stops when the off-diagonal norm is [below 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47), an [absolute test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82), as MAT-013 showed for PSD testing. For the unit square scaled by s, the only off-diagonal entries of B are −s²/2 at (0, 2) and (1, 3), whose norm is s²/√2. At s = 2^-19 ≈ 1.91 · 10^-6, two rotations recover the square. At 2^-20 ≈ 9.54 · 10^-7 and below, no rotation happens: the eigenvalues are the diagonal entries s²/2, the eigenvectors are coordinate vectors, and with k = 2 two neighbouring corners land s/√2 from the origin, on different axes, while the other two land at the origin. The mean distance error is then 0.5 s, half the side. `ix_mds_project` computes the same distances, bit for bit, from the corners of the scaled square, so points about a micrometre apart, with coordinates in metres, are enough to trigger it.
- **The tests use Euclidean input only.** The [square test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L150) requires a mean error [below 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L162) where the predicted error is about 1.5 · 10^-16, and the [coplanar test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L166) uses five points in a plane. None of the five tests of `mds.rs` embeds a non-Euclidean matrix or a small configuration, or compares the result with PCA.
- **Only classical MDS.** `crates/ix-unsupervised` offers no stress minimisation, SMACOF, non-metric MDS or Isomap; the documentation mentions Isomap only as a user of MDS.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

IX embeds the star with k = 2 and with k = 3 and returns the same distances. Why, and where does the centre go?

> *Solution:* B has the eigenvalues 2, 2, 0 and −1/4. With k = 3, the third column comes from the eigenvalue 0, up to rounding, and its eigenvector (1, 1, 1, 1)/2 shifts every point by the same tiny amount, which changes no distance. The eigenvalue −1/4 is dropped in both cases, and nothing in the result says so. Dropping it adds ¼ vvᵀ to B, with v = (3, −1, −1, −1)/√12, which makes the centre's row zero and gives the leaves bᵢᵢ = 4/3 and bᵢⱼ = −2/3: the leaves form an equilateral triangle of side 2 around the origin, and the centre sits at the origin, 2/√3 ≈ 1.155 from each leaf. Mardia's fraction, 4/(4 + 1/4) = 16/17 ≈ 0.941, would have flagged the loss.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Euclidean input.** Call `classical_mds` on the distances of the points 0, 1 and 3 with k = 1, and on `pairwise_euclidean` of (±2, 0) and (0, ±1) with k = 2. Prediction: ±(−4/3, −1/3, 5/3) within 10^-12, and the four points themselves, up to the sign of each column, within 10^-12.
2. **Against PCA.** Call `ix_mds_project` with k = 2 on the ten points of Lindsay Smith's tutorial, and compute the PCA scores from the SVD of the centred data. Prediction: the columns agree up to sign within 10^-12.
3. **The unit square.** Call `classical_mds` with k = 2 on the distance matrix of `test_mds_recovers_2d_square`. Prediction: a mean distance error below 10^-15, about 1.5 · 10^-16.
4. **Graph distances.** Call `classical_mds` on C₄ and on the star with k = 2 and k = 3, compute their matrices B as in §1, and pass them to `symmetric_eigen`. Prediction: the eigenvalues of §5 and §2 within 10^-12, negative ones included; for C₄, a square of side √2 and a mean error of about 0.276 for both values of k; for the star, leaves 2 apart, a centre about 1.155 from each, and a mean error of about 0.077. On the 6-cycle with k = 5, a fifth column of zeros.
5. **Invalid input.** Call `classical_mds` with k = 1 on [[0, −1], [−1, 0]], on [[0, 1], [1, 0]] and on [[0, 0], [2, 0]]. Prediction: all three return `Ok`, with the embedding ±0.5.
6. **Scale.** Call `classical_mds` with k = 2 on the unit square scaled by 2^-19, 2^-20 and 2^-21, and `ix_mds_project` with k = 2 on the corners (0, 0), (s, 0), (s, s) and (0, s) for s = 2^-19 and 2^-20. Prediction: at 2^-19 the square is recovered; at 2^-20 and 2^-21, two corners sit at the origin and the mean error is 0.5 s.

### Practice Exercise

For which scale factors s does `symmetric_eigen` return the diagonal of B unchanged for the unit square scaled by s, and why does that make 2^-20 the first power of two to fail?

> *Solution:* B scales as s², and its off-diagonal entries are −s²/2 at (0, 2) and (1, 3) and 0 elsewhere, so the norm that the loop compares with 10^-12 is √(2 · s⁴/4) = s²/√2. It is below 10^-12 when s < (√2 · 10^-12)^(1/2) ≈ 1.19 · 10^-6. The power 2^-20 ≈ 9.54 · 10^-7 is below that, while 2^-19 ≈ 1.91 · 10^-6 is above. Below the threshold, the four eigenvalues all equal s²/2 up to rounding, and the two eigenvectors kept are coordinate vectors, which leave the other two corners at the origin. A relative test, comparing the off-diagonal norm with the norm of B, would not depend on s.

---

## 8. Common Pitfalls

- **Centring the distances instead of their squares.** Double centring turns squared distances into inner products; applied to plain distances, it gives a matrix with no geometric meaning.
- **Trusting a map built from non-Euclidean dissimilarities.** Look at the negative eigenvalues of B before reading distances off the picture; a negative eigenvalue comparable to the kept ones means that the map distorts the data.
- **Taking the triangle inequality as enough.** Graph distances, such as those of a star or a cycle, satisfy it and are still not Euclidean.
- **Comparing two maps coordinate by coordinate.** Signs and, for tied eigenvalues, whole rotations are arbitrary; align the maps with Procrustes, or compare distances.
- **Calling classical MDS "metric MDS" or "non-metric MDS".** It minimises strain on B; stress minimisation and fits to ranks are different methods, with different results on non-Euclidean data.
- **Asking for more dimensions than there are positive eigenvalues.** The extra columns come from zero or clamped negative eigenvalues; they add nothing.
- **Using an absolute tolerance.** A stopping test that ignores the size of B makes the answer depend on the units of the distances.
- **Symmetrising without looking.** A negative or strongly asymmetric "distance" is usually a data error; averaging and squaring hides it.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Centring matrix** | J = I − (1/n) 11ᵀ, which subtracts the mean |
| **Double-centred matrix** | B = −½ J D⁽²⁾ J, the Gram matrix of the centred points when D is Euclidean |
| **Euclidean distance matrix** | A matrix of the distances between points of some ℝᵐ |
| **Schoenberg criterion** | D is Euclidean exactly when B is positive semidefinite; the dimension needed is the rank of B |
| **Classical MDS** | The configuration Q_kΛ_k^(1/2) built from the k largest eigenvalues of B, also called principal coordinate analysis |
| **Strain** | The discrepancy between B and the Gram matrix of the configuration, which classical MDS minimises |
| **Stress** | The discrepancy between the given distances and those of the configuration, which metric MDS minimises |
| **Non-metric MDS** | MDS that fits only the order of the dissimilarities |
| **Mardia's criterion** | The share Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ| of the eigenvalues of B kept by a configuration of dimension k |
| **Orthogonal Procrustes** | The rotation or reflection that best aligns one configuration with another, computed from an SVD |
| **Isomap** | Classical MDS on the shortest-path distances of a neighbourhood graph |

---

## Self-Check Assessment

**1. An MDS map of 50 products looks convincing, and its double-centred matrix has a largest eigenvalue of 40 and a smallest of −25. What do you conclude?**
> The dissimilarities are far from Euclidean: no configuration reproduces them, and dropping a negative eigenvalue more than half the size of the largest moves many distances. Since the second eigenvalue is at most 40, Mardia's fraction for a map in two dimensions is at most 80/105 ≈ 0.76. Read the map with caution; metric or non-metric MDS by stress may fit the data better, or the dissimilarity itself may need rethinking.

**2. Why does classical MDS on the Euclidean distances of a data set give the same picture as PCA, and when would you still use MDS?**
> Because B = X_cX_cᵀ, whose eigenvectors scaled by the singular values are the PCA scores X_cV_k. Use MDS when only distances are available, or when features far outnumber observations; use PCA when observations are many and features few.

**3. Two runs of MDS on the same data return maps that differ by a rotation of 30°. Is one of them wrong?**
> Not necessarily. If the two largest eigenvalues of B are equal, or nearly so, any rotation in their plane fits the distances as well, and the eigensolver picks one. Compare the distances of the two maps, or align them with orthogonal Procrustes; if they agree, both are right.

**4. IX's `classical_mds` returns an embedding for shortest-path distances on a cycle, without any warning. What do you check before using it?**
> Compute B and its eigenvalues with `symmetric_eigen`, since `classical_mds` clamps negative eigenvalues at 0 without reporting them. For C₄, the eigenvalue −1 next to two eigenvalues 2 shows that the map stretches the sides from 1 to √2. Check the scale too: with distances around 10^-6 or smaller, the absolute tolerance of the eigensolver can skip the rotations entirely.

**Pass criteria:** Double-centre a distance matrix and recover a configuration, decide whether a distance matrix is Euclidean and produce a witness when it is not, relate classical MDS to PCA, explain the ambiguities of reflection and rotation, measure the effect of negative eigenvalues, distinguish classical, metric and non-metric MDS, and trace where IX's `classical_mds` hides a negative eigenvalue or collapses a small configuration.

---

## Research Basis

- I. J. Schoenberg, "Remarks to Maurice Fréchet's article …", *Annals of Mathematics* 36, 1935: which distance spaces embed in Hilbert space
- G. Young and A. S. Householder, "Discussion of a set of points in terms of their mutual distances", *Psychometrika* 3, 1938: the Gram matrix of distances and the dimension needed
- W. S. Torgerson, "Multidimensional scaling: I. Theory and method", *Psychometrika* 17, 1952: classical scaling
- J. B. Kruskal, "Multidimensional scaling by optimizing goodness of fit to a nonmetric hypothesis", *Psychometrika* 29, 1964: stress and non-metric MDS
- J. C. Gower, "Some distance properties of latent root and vector methods used in multivariate analysis", *Biometrika* 53, 1966: principal coordinates and the duality with PCA
- P. H. Schönemann, "A generalized solution of the orthogonal Procrustes problem", *Psychometrika* 31, 1966: aligning two configurations
- K. V. Mardia, "Some properties of classical multi-dimensional scaling", *Communications in Statistics — Theory and Methods* 7, 1978: goodness of fit in the presence of negative eigenvalues
- J. B. Tenenbaum, V. de Silva and J. C. Langford, "A global geometric framework for nonlinear dimensionality reduction", *Science* 290, 2000: Isomap
- I. Borg and P. J. F. Groenen, *Modern Multidimensional Scaling*, 2nd ed., Springer, 2005: stress, SMACOF and classical scaling
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
