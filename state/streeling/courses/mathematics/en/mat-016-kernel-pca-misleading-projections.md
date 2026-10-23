---
module_id: mat-016-kernel-pca-misleading-projections
department: mathematics
course: Kernel PCA and Misleading Projections
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Kernel PCA and Misleading Projections — Principal Components in Feature Space, and Structure the Kernel Invents

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Derive Kernel PCA from the Gram-matrix form of PCA, and state what the kernel must satisfy
- Centre a kernel matrix in feature space, and explain why at most n − 1 components exist
- Normalise the eigenvectors, project training and new points, and check that the two projections agree
- Describe how the RBF bandwidth moves Kernel PCA between linear PCA and a projection that says nothing about the data
- Tell a separation made by the projection from structure in the data, with a bandwidth sweep and a negative control
- Trace what IX's `KernelPca` guarantees, and where its test, its documentation and a numerical threshold promise more than the code delivers

---

## 1. From PCA to Kernel PCA

MAT-014 computes PCA from the p × p covariance matrix. The same components come from the n × n matrix of inner products. If X_c is the centred data matrix with the SVD X_c = UΣVᵀ of MAT-006, the Gram matrix X_cX_cᵀ = UΣ²Uᵀ has the eigenvalues λᵢ = σᵢ² and the unit eigenvectors vᵢ, the columns of U, and the scores are X_cV_k = U_kΣ_k: the score of point j on component i is √λᵢ (vᵢ)ⱼ. This form uses the data only through the inner products xᵢ · xⱼ.

**Kernel PCA** (Schölkopf, Smola and Müller 1998) replaces each inner product by a kernel value k(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ), as defined in MAT-013: it is PCA of the images φ(xᵢ) in the feature space, computed without ever forming φ. The feature space of the polynomial kernel (γ x · y + c)^d has one coordinate per monomial of degree at most d, or exactly d when c = 0; that of the RBF kernel is infinite-dimensional, so PCA there is only possible through the kernel matrix K. The kernel must be positive semidefinite: otherwise no φ exists, and K can have negative eigenvalues, which are not variances. A component of Kernel PCA is a direction in feature space. Its scores are a nonlinear function of the input, while the method itself stays linear, in feature space.

### Practice Exercise

For the kernel k(x, y) = (x · y)² on ℝ², find a feature map φ, and compute k((1, 2), (3, 1)) both ways.

> *Solution:* (x · y)² = (x₁y₁ + x₂y₂)² = x₁²y₁² + 2x₁x₂y₁y₂ + x₂²y₂², so φ(x) = (x₁², √2 x₁x₂, x₂²). Directly, (1 · 3 + 2 · 1)² = 5² = 25. Through φ, φ(1, 2) = (1, 2√2, 4) and φ(3, 1) = (9, 3√2, 1), whose inner product is 9 + 12 + 4 = 25. PCA of the φ(xᵢ) looks for directions among the three quadratic monomials: an ellipse centred at the origin of the input becomes a plane in feature space.

---

## 2. Centring in Feature Space

PCA needs centred data, and the mean φ̄ of the images cannot be formed. It does not need to be: the inner products of the centred images are (φ(xᵢ) − φ̄) · (φ(xⱼ) − φ̄) = kᵢⱼ − rᵢ − rⱼ + g, where rᵢ is the mean of row i of K and g the mean of all its entries. In matrix form, K_c = JKJ with the centring matrix J = I − (1/n) 11ᵀ: the double centring of classical MDS, applied to K instead of −½ D⁽²⁾. For the RBF kernel the link is exact, since ‖φ(x) − φ(y)‖² = k(x, x) + k(y, y) − 2k(x, y) = 2 − 2k(x, y): Kernel PCA with an RBF kernel is classical MDS on the feature-space distances √(2 − 2kᵢⱼ), a connection that Williams (2002) studies.

The centred images sum to 0, so K_c 1 = 0: the vector of ones is always an eigenvector with eigenvalue 0, and at most n − 1 eigenvalues are nonzero. However large the feature space, n centred points span at most n − 1 of its dimensions, so Kernel PCA offers at most n − 1 components, each a combination of the training images.

### Practice Exercise

Apply Kernel PCA with the linear kernel to the points 0, 1 and 3 of the real line. Compute K, K_c and the scores.

> *Solution:* K = xxᵀ = [[0, 0, 0], [0, 1, 3], [0, 3, 9]], with row means 0, 4/3 and 4 and overall mean 16/9. Then (K_c)₁₁ = 0 − 0 − 0 + 16/9 = 16/9, and in the same way K_c = x̃x̃ᵀ with x̃ = (−4/3, −1/3, 5/3), the centred points. K_c has rank 1, the single nonzero eigenvalue ‖x̃‖² = 14/3 and the unit eigenvector x̃/‖x̃‖, so the scores √(14/3) · x̃/‖x̃‖ = x̃ are the centred points, up to sign: with the linear kernel, Kernel PCA is PCA.

---

## 3. Normalisation and Out-of-Sample Projection

Let v be a unit eigenvector of K_c with eigenvalue λ > 0. The feature-space direction w = Σⱼ αⱼ (φ(xⱼ) − φ̄) with α = v/√λ has unit length, since ‖w‖² = αᵀK_cα = vᵀK_cv/λ = 1; this is the normalisation of Schölkopf, Smola and Müller. The score of training point i is the inner product of its centred image with w, (K_cα)ᵢ = λvᵢ/√λ = √λ vᵢ, the formula of §1.

A new point x is projected the same way, with the training statistics. Its centred kernel vector has the entries k̃ⱼ(x) = k(x, xⱼ) − m(x) − rⱼ + g, where m(x) is the mean of the k(x, xⱼ) over the training points, and its score is Σⱼ αⱼ k̃ⱼ(x). For a training point, k̃(xᵢ) is row i of K_c and the score is again √λ vᵢ, so the two routes must agree on the training set: that is the first check to run on any implementation. When λ = 0, v lies in the null space of K_c, no unit direction w can be built from it, and the right output is a column of zeros or no column at all.

Going back from a score to the input space is harder, because a point of feature space need not be the image of any input. This **pre-image problem** is solved only approximately: by iteration for the RBF kernel (Mika et al. 1999), or from distances (Kwok and Tsang 2004).

### Practice Exercise

Continue the exercise of §2: project the new point x = 2 with the linear kernel, through k̃(x) and α.

> *Solution:* k(2, xⱼ) = (0, 2, 6), with mean m = 8/3. With the row means 0, 4/3 and 4 and g = 16/9, k̃ = (0 − 8/3 − 0 + 16/9, 2 − 8/3 − 4/3 + 16/9, 6 − 8/3 − 4 + 16/9) = (−8/9, −2/9, 10/9). With v = x̃/‖x̃‖ and λ = 14/3, α = x̃/λ = (−2/7, −1/14, 5/14), and the score is (−8/9)(−2/7) + (−2/9)(−1/14) + (10/9)(5/14) = 16/63 + 1/63 + 25/63 = 2/3: the point 2 minus the training mean 4/3, as PCA would give.

---

## 4. The Bandwidth: From Linear PCA to a Projection of Nothing

MAT-013 followed the RBF Gram matrix K as γ varies. Centring changes both limits. For small γ, exp(−γd²) = 1 − γd² + O(γ²d⁴); centring removes the constant, and K_c ≈ −γ J D⁽²⁾ J = 2γB, where B is the double-centred matrix of classical MDS, the Gram matrix of the centred inputs. Kernel PCA then approaches linear PCA, with eigenvalues about 2γ times those of B and scores about √(2γ) times the PCA scores. On the points 0, 1 and 3 with γ = 0.001, the largest eigenvalue is about 9.29 · 10^-3, against 2γ · 14/3 ≈ 9.33 · 10^-3, and the scores divided by √(2γ) are −1.330, −0.334 and 1.663, against −4/3, −1/3 and 5/3.

For large γ, every off-diagonal kᵢⱼ tends to 0, K tends to I and K_c to J, whose eigenvalues are 1, n − 1 times, and 0. Every unit vector orthogonal to 1 is then an eigenvector, so the components are whatever basis the eigensolver returns. In feature space, the images of distinct points become orthogonal, all at distance √2 from one another: a regular simplex, which looks the same from every direction.

Between these limits, what Kernel PCA shows depends on γ, and no value is right in general. MAT-013 mentions a common starting value, σ equal to the median distance between points, with γ = 1/(2σ²): a place to start, not a guarantee that the structure one looks for will appear.

### Practice Exercise

For n distinct points and γ → ∞, what does Kernel PCA with k components return, and what does it tell about the data?

> *Solution:* K_c tends to J, so the n − 1 nonzero eigenvalues all tend to 1, and any orthonormal basis of the vectors orthogonal to 1 is a valid set of eigenvectors. The k columns returned are whichever vectors the eigensolver produces, scaled by √1 = 1: a projection of a regular simplex, which says nothing about the data. Any pattern in such a plot, clusters included, comes from the solver.

---

## 5. Misleading Projections: Two Rings and a Negative Control

Two concentric rings are the standard showcase of Kernel PCA. No linear projection separates them (see the exercise), but the RBF kernel can, through one particular component. Take m points on each ring, at the same angles. The configuration is unchanged by the rotations and reflections of a regular m-gon, and K_c commutes with the permutations of the points that they induce. The vectors that these permutations fix are those constant on each ring; they form a plane that contains 1 and that K_c maps to itself, so the other direction of that plane, s = (1, …, 1, −1, …, −1)/√(2m), is an exact eigenvector, with the eigenvalue λ_rad = sᵀKs. Its scores are +√(λ_rad/(2m)) on one ring and −√(λ_rad/(2m)) on the other: each ring collapses to a single value, a perfect separation. Every other eigenvector can be chosen orthogonal to that plane, so its scores average to 0 on each ring. Without s, every affine function of the kept scores has the same mean on both rings, so it cannot be positive on one ring and negative on the other: whether the kept components separate the rings by a line or a hyperplane depends only on whether s is among them, that is, on the rank of λ_rad, and that rank depends on γ and on the geometry. The rings may still differ in radius in such a plot, as below, but only a nonlinear rule can use that.

IX's test data have four points on each of the rings of radii 1 and 2. At γ = 0.5, the eigenvalues of K_c are about 1.531 twice, 1.216, 0.672 = λ_rad, 0.333 twice, 0.148 and 0: the radial component ranks fourth, and it ranks fourth for every γ of the sweep of §7, from 0.001 to 10. The first two components form a tied pair that records the angle of each point: each inner point lands at the same angle as its outer neighbour, at a radius of about 0.583 against 0.653 for the outer ring. The ratio of 2 between the radii shrinks to about 1.12, and no line separates the two squares.

With the inner radius changed to 0.3 and the outer to 1, the radial component ranks fourth up to γ = 0.5, third at γ = 1, and first above γ ≈ 1.597. Its lead over the next eigenvalue reaches about 0.357 at γ = 5 and falls to about 1.2 · 10^-4 at γ = 50. The same data thus show no separation at γ = 1 and a perfect one at γ = 5. A separation that holds in a window of γ is a property of the data and of γ together, and reporting it requires the window.

A **negative control** is a data set without the structure sought. Take the eight evenly spaced points 0, 1, …, 7 of a line: they have no clusters. At γ = 0.001 the first component is essentially the line, and its largest gap between consecutive scores is 0.145 of the range, against 1/7 ≈ 0.143 for exactly even spacing. At γ = 0.1 and at every larger γ of the sweep, the first component is no longer monotone: both ends fold back while the middle stretches, and for γ = 2, 5 and 10 the gap between points 3 and 4 reaches 0.347 of the range, more than twice the even gap. A histogram of that component shows two groups of four points. This is the **horseshoe** effect of local kernels (Diaconis, Goel and Holmes 2008): the kernel sees only near neighbours, and the leading eigenvectors of such matrices bend a line into an arch, often with its ends curled inward. Any criterion that declares the rings separated should be run on such a control, and must fail there.

### Practice Exercise

Why can no linear projection separate two concentric rings centred at the origin?

> *Solution:* A linear projection maps x to u · x for some unit vector u; the first component of PCA is one such map. A full ring of radius r maps onto the whole interval [−r, r], so the inner ring's interval lies inside the outer ring's, and every threshold strictly between −r₁ and r₁ has points of both rings on each side. For IX's four points per ring, each outer point is twice the inner point at the same angle, so each outer score is twice an inner score; the inner scores take both signs, so the outer scores extend beyond them at both ends, and no threshold separates the rings. Keeping more linear components does not help: a linear map sends the two rings to two nested ellipses, one a scaled copy of the other.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of `fit_transform`, `transform`, `compute_kernel` and `symmetric_eigen` into Python, whose floats are IEEE binary64 like Rust's `f64`: they are predictions, and §7 proposes to check them.

**Kernel PCA** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L96) builds K, centres it with the [formula of §2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L129), hands K_c to [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L135), the Jacobi method of MAT-005, and keeps the first `n_components` pairs. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L169) centres the kernel vectors of new points with the [training statistics](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L205) and [multiplies them by the stored alphas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L210). The module is a library only: [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L7) exports it and no other Rust file in the repository refers to it, so no MCP tool, DuckDB function or pipeline stage offers Kernel PCA. The normalisation and the training projection read:

```rust
        // Take top-k alphas and lambdas.
        let mut alphas = Array2::<f64>::zeros((n, self.n_components));
        let mut lambdas = Array1::<f64>::zeros(self.n_components);
        for r in 0..self.n_components {
            let lambda = eigenvalues[r].max(0.0);
            lambdas[r] = lambda;
            // Normalize alphas so that lambda * alpha.alpha = 1 (standard Kernel PCA convention)
            let norm = if lambda > 1e-12 { lambda.sqrt() } else { 1.0 };
            for i in 0..n {
                alphas[[i, r]] = eigenvectors[[i, r]] / norm;
            }
        }
```

```rust
        // Project training data. The closed form is
        // X_projected[i, r] = sqrt(lambda_r) * eigenvector[i, r]
        let mut projected = Array2::<f64>::zeros((n, self.n_components));
        for r in 0..self.n_components {
            let scale = lambdas[r].sqrt();
            for i in 0..n {
                projected[[i, r]] = eigenvectors[[i, r]] * scale;
            }
        }
```

- **The ring test does not test a separation.** [`test_rbf_kernel_separates_rings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L264) fits [two components with γ = 0.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L276) on the rings of §5 and asserts only that the [mean square of the first component](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L283) is [above 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L285). The transcription predicts the picture of §5: two concentric squares at radii of about 0.583 and 0.653, which no line separates, and a mean square of about 0.191, which passes. The module's example runs the same data and settings under the comment ["Two rings of points — impossible to separate with linear PCA"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L29), and asserts only [the number of columns](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L42).
- **IX's note on the test gives the right verdict for the wrong reason.** The note [`kernel-pca-symmetric-centroid-trap.md`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L7) explains why an earlier version of the test, which compared the ring centroids of the first component, failed: every ["component of the projection has zero mean within each symmetric ring"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L45). Its verdict, ["This is not a Kernel PCA bug."](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L47), stands, but not its reason: §5 shows that the claim holds for every component but one: the radial component, fourth at γ = 0.5, has the ring means ±0.290 and no spread within a ring. The earlier test failed because that component was not among the two kept, not because symmetry forbids a separation. The note's alternative of [pairwise separation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L65) would have failed on the two components kept: an inner point is about 0.070 from its outer neighbour and 0.824 from the next inner point. The note also recommends asking ["what would this assertion look like on completely random data?"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L77) The replacement assertion fails that check: the mean square of the first component is λ₁/n for any data, and on the evenly spaced line of §5 with γ = 0.5 it is about 0.250, higher than on the rings.
- **A component with a tiny eigenvalue is projected two ways.** The [threshold](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L144) keeps α = v instead of v/√λ when 0 < λ ≤ 10^-12, so on the training points `transform` returns λv where `fit_transform` returns √λ v, a factor √λ apart. For the points (±1, 0) and (0, ±5 · 10^-7) with the linear kernel and two components, λ₂ = 5 · 10^-13: `fit_transform` gives the second coordinates ±5 · 10^-7, the true projections, and `transform` gives about ±3.54 · 10^-13. No test compares the two routes: [`test_transform_out_of_sample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L308) checks only [the shape](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L314) of its output.
- **The documentation describes alphas that the code does not store.** The module documentation gives the projection as [`alpha_r[i] * sqrt(lambda_r)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L17) and calls the stored alphas the [eigenvectors of the centred kernel matrix](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L71), but the code stores the [eigenvectors divided by √λ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L146), as its own [comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L143) intends. With the stored alphas, the documented formula returns vᵢ instead of √λ vᵢ. The code's own [training projection](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L156) multiplies the eigenvectors by √λ and is right.
- **A NaN kernel still returns `Ok`.** MAT-013 noted that the polynomial kernel, with a [degree of type `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) raised with [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), gives NaN when a negative base meets a fractional degree. The fit does not stop there. The grand mean spreads the NaN to every entry of K_c, `symmetric_eigen` runs all its [100 sweeps](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) on NaN, and the [clamp](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) turns each NaN eigenvalue into 0, because Rust's `f64::max` returns the other operand when one is NaN. On the square (±1, 0), (0, ±1) with degree 1.5, γ = 1 and c = 0, where k((1, 0), (−1, 0)) = (−1)^1.5, the transcription predicts 600 rotations, then `Ok`, with every projection NaN and every λ equal to 0.
- **The tests check shapes more than properties.** Of the six tests, the [linear test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L243) checks a real property, monotone scores along a line. The ring test checks a mean square that almost any data pass, the [polynomial test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L292) and the transform test check shapes, and the last two check that `n_components` = 0 and `n_components` ≥ n are rejected. None varies γ, compares `transform` with `fit_transform`, or runs a negative control.
- **No pre-image and no bandwidth selection.** `KernelPca` has no pre-image, no rule or search for γ, and no check that the kernel matrix is positive semidefinite.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

IX's ring test keeps two components with γ = 0.5. Compute λ_rad = sᵀKs for its data, with s = (1, 1, 1, 1, −1, −1, −1, −1)/√8, and explain why the ring means of the first component are equal while those of the fourth are not.

> *Solution:* Within the inner ring the squared distances are 2 between neighbours and 4 across; within the outer ring, 8 and 16; between the rings, 1 at the same angle, 5 at a right angle and 9 across. Summing K over ordered pairs with γ = 0.5, the inner block gives 4 + 8e^−1 + 4e^−2 ≈ 7.484, the outer block 4 + 8e^−4 + 4e^−8 ≈ 4.148 and each block between the rings 4e^−0.5 + 8e^−2.5 + 4e^−4.5 ≈ 3.127, so λ_rad ≈ (7.484 + 4.148 − 2 × 3.127)/8 ≈ 0.672. That is below 1.531, 1.531 and 1.216, so s is the fourth eigenvector, and a fit with two components does not keep it. The first component belongs to the tied pair, orthogonal to the plane of vectors constant on each ring, so its mean on each ring is 0; the fourth is s itself, with the scores ±√(0.672/8) ≈ ±0.290.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Linear kernel.** Call `fit_transform` with the linear kernel and one component on the points 0, 1 and 3, then `transform` on the point 2. Prediction: ±(−4/3, −1/3, 5/3) and ±2/3, with the same sign, within 10^-12.
2. **The rings.** Call `fit_transform` on the data of `test_rbf_kernel_separates_rings` with seven components, for each γ of the sweep 0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5 and 10, and find the component whose scores are constant on each ring. Prediction: it is the fourth for every γ; at γ = 0.5 the eigenvalues are those of §5, the fourth component has the ring means ±0.290, and the first two place the rings at radii of about 0.583 and 0.653.
3. **Rings with inner radius 0.3.** Repeat step 2 with the inner ring at radius 0.3 and the outer at 1, adding γ = 1.5, 1.6 and 50. Prediction: the radial component is fourth up to γ = 0.5, third at 1 and 1.5, and first from 1.6 on, with a lead of about 0.357 at γ = 5 and 1.2 · 10^-4 at γ = 50.
4. **Negative control.** Call `fit_transform` with two components on the points 0, 1, …, 7 of a line, over the same sweep. Prediction: the first component is monotone up to γ = 0.05 and folds at both ends from 0.1 on; its largest gap lies between points 3 and 4 and is 0.145 of the range at γ = 0.001 and 0.347 at γ = 2, 5 and 10; at γ = 0.5, the mean square of the first component is about 0.250, above the 0.191 of the rings.
5. **Transform against fit.** On the points (±1, 0) and (0, ±ε) with the linear kernel and two components, compare `transform` on the training points with `fit_transform`, for ε = 10^-6 and 5 · 10^-7. Prediction: agreement within 10^-15 for ε = 10^-6; for ε = 5 · 10^-7, second coordinates of about ±5 · 10^-7 and ±3.54 · 10^-13.
6. **A fractional degree.** Call `fit_transform` with two components and the polynomial kernel of degree 1.5, γ = 1 and c = 0 on the points (±1, 0) and (0, ±1). Prediction: `Ok`, with every projection NaN and both λ equal to 0.

### Practice Exercise

In step 5, for which ε does IX's threshold make `transform` disagree with `fit_transform`, and by what factor?

> *Solution:* The points are already centred, and the nonzero eigenvalues of K_c = XXᵀ are 2 and 2ε², with the unit eigenvector v₂ = (0, 0, 1, −1)/√2 for 2ε². The threshold keeps α = v₂ when 2ε² ≤ 10^-12, that is when ε ≤ (5 · 10^-13)^(1/2) ≈ 7.07 · 10^-7. `fit_transform` then returns √(2ε²) v₂, the true coordinates ±ε, while `transform` returns K_c v₂ = 2ε² v₂, the coordinates ±√2 ε²: a factor √2 ε, about 7.07 · 10^-7 at ε = 5 · 10^-7, where the coordinates are ±5 · 10^-7 and about ±3.54 · 10^-13. Returning a zero column for such components, in both routes, would make them agree.

---

## 8. Common Pitfalls

- **Reading a separation off one value of γ.** Report the range of γ over which it holds, and the rank of the component that carries it.
- **Skipping the negative control.** Run the same pipeline on data without the structure; a criterion that passes there measures nothing.
- **Asserting a property that every input has.** A nonzero variance, a correct shape or a finite value holds for almost any data; a test must be able to fail when the property is absent.
- **Assuming that the first components carry the structure.** The component that separates may rank third or fourth; look at more components, and at the eigenvalues, before concluding that a kernel failed.
- **Centring a new point with its own statistics.** A new point must be centred with the training row means and grand mean, or its score is not comparable with the training scores.
- **Trusting a projection at large γ.** When K is close to the identity, the nonzero eigenvalues are all close to 1 and the components are arbitrary.
- **Comparing two Kernel PCA runs coordinate by coordinate.** Tied eigenvalues, as for the rings, make every rotation of the tied pair an equally valid answer.
- **Using a kernel that is not positive semidefinite.** Its negative eigenvalues have no variance to explain, and clamping them at 0 hides the problem.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Kernel PCA** | PCA of the feature-space images φ(xᵢ), computed from the kernel matrix |
| **Kernel trick** | Replacing inner products by kernel values, so that φ is never formed |
| **Centred kernel matrix** | K_c = JKJ, the inner products of the centred images |
| **Dual coefficients** | The weights α = v/√λ that express a unit feature-space direction through the training images |
| **Out-of-sample projection** | The score Σⱼ αⱼ k̃ⱼ(x) of a new point, centred with the training statistics |
| **Bandwidth** | The scale set by γ in the RBF kernel exp(−γ‖x − y‖²) |
| **Radial component** | For rings with the same angles, the eigenvector constant on each ring and orthogonal to 1, which separates them |
| **Negative control** | Data without the structure sought, on which a detection criterion must fail |
| **Horseshoe effect** | The bending of a line into an arch by the leading eigenvectors of a local kernel |
| **Pre-image problem** | Finding an input whose image is closest to a given point of feature space |

---

## Self-Check Assessment

**1. A colleague shows a Kernel PCA plot of gene-expression data at γ = 3, with two clear clusters, and nothing else. What do you ask for?**
> The same plot over a range of γ, with the range where the clusters stay apart; the eigenvalues, to see which component carries the split and whether it ties with others; and the same pipeline on a negative control, such as the data with each feature permuted independently, which keeps the distribution of each feature and destroys the joint structure. The clusters must not appear there. As §5 shows, evenly spaced points on a line can show a gap of more than twice the even spacing at large γ.

**2. Why can Kernel PCA with the linear kernel never separate two concentric rings, while an RBF kernel sometimes can?**
> With the linear kernel, Kernel PCA is PCA, a linear projection, and no linear projection separates the rings. The RBF feature space contains, for rings with the same angles, a direction whose scores are constant on each ring; it separates them perfectly, but only when its eigenvalue ranks among the components kept, which depends on γ and on the geometry.

**3. IX's `transform` and `fit_transform` disagree on the training points for one component. What do you check?**
> The eigenvalue of that component. IX keeps α = v when 0 < λ ≤ 10^-12, so `transform` returns λv where `fit_transform` returns √λ v. Such a component carries no usable variance: drop it, or reduce `n_components`.

**4. A test named `test_rbf_kernel_separates_rings` asserts that the first component has a mean square above 10^-4. What would a meaningful assertion look like?**
> One that fails when the rings are not separated: for instance, that some kept component has all inner scores on one side of a threshold and all outer scores on the other, with a margin, together with the same check failing on a negative control. With IX's data and two components at γ = 0.5, that test would fail, which is the honest outcome; with four components, it would pass on the fourth.

**Pass criteria:** Derive Kernel PCA from the Gram form of PCA, centre a kernel matrix and explain the bound of n − 1 components, normalise the dual coefficients and project new points, describe the limits in γ, analyse the rings by symmetry, design a bandwidth sweep with a negative control, and trace where IX's `KernelPca` test, documentation and threshold promise more than the code delivers.

---

## Research Basis

- J. Mercer, "Functions of positive and negative type, and their connection with the theory of integral equations", *Philosophical Transactions of the Royal Society A* 209, 1909: positive kernels
- B. Schölkopf, A. Smola and K.-R. Müller, "Nonlinear component analysis as a kernel eigenvalue problem", *Neural Computation* 10, 1998: Kernel PCA, centring in feature space and the normalisation of the dual coefficients
- S. Mika, B. Schölkopf, A. Smola, K.-R. Müller, M. Scholz and G. Rätsch, "Kernel PCA and de-noising in feature spaces", *Advances in Neural Information Processing Systems* 11, 1999: pre-images by iteration
- C. K. I. Williams, "On a connection between kernel PCA and metric multidimensional scaling", *Machine Learning* 46, 2002: Kernel PCA with isotropic kernels and MDS
- B. Schölkopf and A. J. Smola, *Learning with Kernels*, MIT Press, 2002: kernels, centring and out-of-sample projection
- J. T. Kwok and I. W. Tsang, "The pre-image problem in kernel methods", *IEEE Transactions on Neural Networks* 15, 2004: pre-images from distances
- P. Diaconis, S. Goel and S. Holmes, "Horseshoes in multidimensional scaling and local kernel methods", *Annals of Applied Statistics* 2, 2008: the horseshoe effect
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
