---
module_id: mat-004-vectors-matrices-norms
department: mathematics
course: Vectors, Matrices, Norms and Linear Maps
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Vectors, Matrices, Norms and Linear Maps — What a Matrix Does to Space

> **Department of Mathematics** | Stage: Nigredo (Beginner) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Describe a vector space and write a vector in coordinates with respect to a basis
- Recognise a linear map and build its matrix from the images of the basis vectors
- Explain why the matrix product is the composition of linear maps, and why it is associative but not commutative
- Read the determinant as a signed volume and estimate the cost of computing it by cofactor expansion
- State the norm axioms, use the p-norms, and show why the p = 1/2 "norm" is not one
- Say what IX's linear-algebra and distance functions do and do not guarantee

---

## 1. Vectors and Vector Spaces

A **vector** in Rⁿ is a list of n real numbers, x = (x₁, …, xₙ). Vectors are added and multiplied by numbers (**scalars**) component by component: (1, 2) + (3, 4) = (4, 6) and 3 · (1, 2) = (3, 6).

A **vector space** is any set with such an addition and scalar multiplication that obey the familiar rules: addition is associative and commutative, there is a zero vector and every vector has a negative, and scalar multiplication distributes over both additions. Rⁿ is the main example, but not the only one: the polynomials a₀ + a₁t + a₂t² of degree at most 2 form a vector space too, and behave exactly like the triples (a₀, a₁, a₂).

A **linear combination** of vectors v₁, …, vₖ is a sum c₁v₁ + … + cₖvₖ. A **basis** is a list of vectors such that every vector of the space is a linear combination of them in exactly one way; the numbers cᵢ are then the **coordinates** of the vector in that basis. The **standard basis** of R² is e₁ = (1, 0), e₂ = (0, 1), and the coordinates of (3, 4) in it are just 3 and 4. In another basis the same vector has other coordinates.

### Practice Exercise

Find the coordinates of (3, 4) in the basis u = (1, 1), w = (1, −1).

> *Solution:* We need a and b with a · (1, 1) + b · (1, −1) = (3, 4), that is a + b = 3 and a − b = 4. Adding the equations gives 2a = 7, so a = 7/2; subtracting them gives 2b = −1, so b = −1/2. Check: 7/2 · (1, 1) − 1/2 · (1, −1) = (7/2 − 1/2, 7/2 + 1/2) = (3, 4).

---

## 2. Linear Maps and Their Matrices

A map L from one vector space to another is **linear** if it respects both operations:

L(u + v) = L(u) + L(v) and L(c · v) = c · L(v), for all vectors u, v and scalars c.

Rotations about the origin, reflections across a line through the origin and scalings are linear. A translation x ↦ x + b with b ≠ 0 is not: every linear map sends 0 to 0, because L(0) = L(0 · 0) = 0 · L(0) = 0.

A linear map is determined by what it does to a basis. If x = x₁e₁ + … + xₙeₙ, then L(x) = x₁L(e₁) + … + xₙL(eₙ). So we write the images L(e₁), …, L(eₙ) as the **columns** of a matrix A, and computing L(x) becomes the matrix–vector product A x: x₁ times the first column, plus x₂ times the second, and so on. For example, the rotation by 90° sends e₁ = (1, 0) to (0, 1) and e₂ = (0, 1) to (−1, 0), so its matrix is

R = [[0, −1], [1, 0]],

written row by row.

### Practice Exercise

Find the matrix S of the reflection across the line y = x, and check that it sends (1, 2) to (2, 1).

> *Solution:* The reflection swaps the two coordinates, so it sends e₁ = (1, 0) to (0, 1) and e₂ = (0, 1) to (1, 0). These images are the columns: S = [[0, 1], [1, 0]]. Then S (1, 2) = 1 · (0, 1) + 2 · (1, 0) = (2, 1).

---

## 3. Composition Is the Matrix Product

If B is the matrix of a linear map M and A that of L, then applying M first and L second is again linear, and its matrix is the **product** AB: by definition, (AB) x = A (B x). Working out the columns gives the usual rule

(AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ,

which needs the number of columns of A to equal the number of rows of B. Note the order: in (AB) x, the map B acts **first**.

Two properties follow from this definition:
- **The product is associative**: (AB)C = A(BC). Both sides are the composition "C, then B, then A", and composing functions is always associative. No computation with entries is needed.
- **The product is not commutative**: in general AB ≠ BA, because doing two things in the opposite order is usually a different thing.

### Practice Exercise

With R = [[0, −1], [1, 0]] (rotation by 90°) and F = [[1, 0], [0, −1]] (reflection across the x-axis), compute RF and FR and describe each as a geometric map.

> *Solution:* RF = [[0 · 1 + (−1) · 0, 0 · 0 + (−1) · (−1)], [1 · 1 + 0 · 0, 1 · 0 + 0 · (−1)]] = [[0, 1], [1, 0]], the reflection across the line y = x. FR = [[1 · 0 + 0 · 1, 1 · (−1) + 0 · 0], [0 · 0 + (−1) · 1, 0 · (−1) + (−1) · 0]] = [[0, −1], [−1, 0]], the reflection across the line y = −x. Since RF ≠ FR, the order matters: "reflect, then rotate" is not "rotate, then reflect".

---

## 4. The Determinant as a Volume

For a 2 × 2 matrix, det [[a, b], [c, d]] = ad − bc. Its absolute value is the **area** of the parallelogram spanned by the two columns (a, c) and (b, d), and its sign says whether the map keeps the orientation of the plane (+) or reverses it (−). In n dimensions, |det A| is the factor by which A multiplies volumes. Three facts follow from that picture:
- det(AB) = det A · det B: applying B and then A multiplies volumes by both factors.
- det A = 0 exactly when A squashes space onto a lower dimension, that is, when its columns are linearly dependent and A has no inverse.
- A rotation has determinant 1 and a reflection −1: both keep areas, and only the reflection reverses orientation.

For larger matrices, the **cofactor expansion** along the first row reduces an n × n determinant to n determinants of size n − 1:

det A = Σⱼ (−1)ʲ⁺¹ a₁ⱼ det A₁ⱼ,

where A₁ⱼ is A with its first row and column j removed. It is a correct definition but an expensive algorithm. **Gaussian elimination** needs a number of operations of the order of n³. It adds multiples of one row to another, which leaves the determinant unchanged, and exchanges rows, which changes its sign. So det A is the product of the pivots, times −1 for each row exchange: for [[0, 1], [1, 0]], one exchange gives the pivots 1 and 1, and det = −1.

### Practice Exercise

An implementation applies the cofactor expansion recursively and stops at 2 × 2 matrices, which it computes directly. How many 2 × 2 determinants does it evaluate for an n × n matrix? Compare the count for n = 10 with 10³.

> *Solution:* Let D(n) be the count. D(2) = 1, and an n × n matrix makes n calls of size n − 1, so D(n) = n · D(n − 1). By induction (MAT-001), D(n) = n!/2: it holds for n = 2, since 2!/2 = 1, and if D(n − 1) = (n − 1)!/2, then D(n) = n · (n − 1)!/2 = n!/2. For n = 10, that is 10!/2 = 1,814,400 determinants of size 2, against a number of elimination steps of the order of 10³ = 1000. For n = 20, 20!/2 is about 1.2 × 10^18.

---

## 5. Norms: Measuring Length

A **norm** assigns a length ‖x‖ to every vector and obeys three axioms:
- **Positivity:** ‖x‖ ≥ 0, and ‖x‖ = 0 only for x = 0.
- **Homogeneity:** ‖c · x‖ = |c| · ‖x‖ for every scalar c.
- **Triangle inequality:** ‖x + y‖ ≤ ‖x‖ + ‖y‖.

Every norm gives a **distance** d(x, y) = ‖x − y‖, and the triangle inequality for the norm becomes the one for distances: d(x, z) ≤ d(x, y) + d(y, z). Going around by y is never shorter than going directly.

The **p-norms** on Rⁿ are ‖x‖ₚ = (|x₁|ᵖ + … + |xₙ|ᵖ)^(1/p), for p ≥ 1, and ‖x‖∞ = maxᵢ |xᵢ|, which is their limit as p grows. For x = (3, 4):
- ‖x‖₁ = 3 + 4 = 7, the Manhattan length;
- ‖x‖₂ = √(9 + 16) = 5, the Euclidean length;
- ‖x‖∞ = 4, the largest component.

For p ≥ 1 the triangle inequality holds: that is **Minkowski's inequality**. For p < 1 the same formula still gives a number, but not a norm.

A matrix also has norms. The one **induced** by a vector norm is ‖A‖ = max ‖A x‖ / ‖x‖ over x ≠ 0, the largest factor by which A stretches a vector. It is the norm behind the condition number of MAT-003.

### Practice Exercise

For p = 1/2, define d(x, y) = (|x₁ − y₁|^(1/2) + |x₂ − y₂|^(1/2))². Show that it breaks the triangle inequality for x = (0, 0), y = (1, 0) and z = (1, 1).

> *Solution:* d(x, y) = (1 + 0)² = 1 and d(y, z) = (0 + 1)² = 1, while d(x, z) = (1 + 1)² = 4. So d(x, z) = 4 > 2 = d(x, y) + d(y, z): going around by y is shorter than going directly. This one counterexample shows that the p = 1/2 formula is not a norm.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**Linear algebra** (`crates/ix-math/src/linalg.rs`):
- [`matmul`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L8) and [`matvec`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L19) compute AB and A x, and return `DimensionMismatch` when the number of columns of A does not match the other operand.
- [`trace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L151) sums the diagonal of a square matrix.
- [`determinant`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L35) is documented as "cofactor expansion, suitable for small matrices". Its recursion, verbatim from `linalg.rs` lines 43–59, is the algorithm of the §4 exercise:

```rust
fn det_recursive(a: &Array2<f64>) -> f64 {
    let n = a.nrows();
    if n == 1 {
        return a[[0, 0]];
    }
    if n == 2 {
        return a[[0, 0]] * a[[1, 1]] - a[[0, 1]] * a[[1, 0]];
    }

    let mut det = 0.0;
    for j in 0..n {
        let minor = minor_matrix(a, 0, j);
        let sign = if j % 2 == 0 { 1.0 } else { -1.0 };
        det += sign * a[[0, j]] * det_recursive(&minor);
    }
    det
}
```

- `linalg.rs` has no function that returns a matrix norm. In `ix-math`, the Frobenius norm appears only inside algorithms, as a stopping criterion, and as a [test helper](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L237) in `svd.rs`.

**Distances** (`crates/ix-math/src/distance.rs`): [`euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L18), [`manhattan`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L37) and [`chebyshev`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L77) are the distances of the 2-, 1- and ∞-norms. [`minkowski`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L46) computes the p-distance and refuses p < 1, verbatim from lines 46–57:

```rust
pub fn minkowski(a: &Array1<f64>, b: &Array1<f64>, p: f64) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    if p < 1.0 {
        return Err(MathError::InvalidParameter("p must be >= 1".into()));
    }
    let sum: f64 = a
        .iter()
        .zip(b.iter())
        .map(|(x, y)| (x - y).abs().powf(p))
        .sum();
    Ok(sum.powf(1.0 / p))
}
```

The guard encodes §5: it keeps `minkowski` where Minkowski's inequality holds. The p = 1/2 counterexample therefore cannot be computed with IX's `minkowski`, which returns an error; it is a computation by hand, as in the §5 exercise.

The tests check examples, not properties. [`test_minkowski_equals_euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L116) compares `minkowski` with p = 2 and `euclidean` on one pair of points, (0, 0) and (3, 4); the other distance tests also use one or two fixed pairs each. No test in `distance.rs` states the triangle inequality or another norm axiom. Elsewhere in IX, [`test_cpu_triangle_inequality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-gpu/src/distance.rs#L193) states it for the GPU crate's own Euclidean distance matrix, but checks a single triple of points. As MAT-001 explains, such examples can refute a property but cannot prove it.

**Not every "distance" is a metric.** [`cosine_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L72) returns 1 − cos θ, where θ is the angle between the vectors. It does not satisfy the triangle inequality: for x = (1, 0), y = (1, 1) and z = (0, 1), it gives d(x, z) = 1, but d(x, y) + d(y, z) = 2 − √2 ≈ 0.59.

### Practice Exercise

The guard in `minkowski` rejects p < 1, but it lets p = ∞ (`f64::INFINITY`) through. Using the standard rules of floating-point powers — x^0 = 1 for every x, and for p = ∞, t^p is 0 when 0 ≤ t < 1, 1 when t = 1 and ∞ when t > 1 — predict what `minkowski` returns for p = ∞, and compare it with `chebyshev`.

> *Solution:* With p = ∞, each term |x − y|^p is 0, 1 or ∞, so `sum` is 0, a positive whole number, or ∞. The last step raises it to the power 1/p = 1/∞ = 0, and x^0 = 1 for every x, including 0 and ∞. So `minkowski` returns 1 for every pair of vectors, even for a = b, where a distance must be 0. The limit of the p-distance as p grows is the ∞-distance, but substituting p = ∞ into the formula does not compute that limit: `chebyshev` is the right function, and it returns 0 for a = b and 4 for (0, 0) and (3, 4). This is a prediction from the rules above, not a run: the experiment of §7 checks it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **The triangle inequality on a grid.** For the 25 points of R² with integer coordinates from −2 to 2, check d(x, z) ≤ d(x, y) + d(y, z) over all 15,625 triples for `manhattan`, `euclidean`, `chebyshev` and `minkowski` with p = 3. Prediction: no violation larger than 10^-12. Where the exact values are equal, rounding can still make the two sides differ in their last bits, which is why the comparison needs a tolerance (MAT-003).
2. **p below 1.** Call `minkowski` with p = 1/2 on the points of the §5 exercise. Prediction: `InvalidParameter("p must be >= 1")`.
3. **p = ∞.** Call `minkowski` with p = `f64::INFINITY` on (0, 0) and (0, 0), and on (0, 0) and (3, 4). Prediction: 1 for both, against 0 and 4 from `chebyshev`.
4. **Large p.** Call `minkowski` with p = 1000 on (0, 0) and (3, 4). Prediction: ∞, because 3^1000 exceeds the largest binary64 number, although the exact result is a little above 4.
5. **The cost of cofactor expansion.** Time `determinant` for n = 2 to 11 on fixed matrices, and check det(AB) = det A · det B on 3 × 3 matrices with small integer entries. Predictions: from n = 3 on, each step multiplies the time by roughly n, as the count n!/2 of the §4 exercise suggests; and the product rule holds exactly, because every intermediate value is an integer small enough to be stored exactly.

### Practice Exercise

Step 1 checks every triple of the grid. Does it prove the triangle inequality for these distances on R²?

> *Solution:* No. The grid has 25 points, while R² is infinite, so the check is exhaustive on a finite subset only (MAT-001). What proves the inequality is Minkowski's inequality, for every p ≥ 1. The check tests something else: that IX's code computes these distances without an error large enough to break the inequality on those points.

---

## 8. Common Pitfalls

- **Multiplying in the wrong order.** In (AB) x the map B acts first, and AB ≠ BA in general.
- **Calling every map "linear".** A linear map sends 0 to 0; a translation does not.
- **Computing large determinants by cofactor expansion.** The cost grows like n!; elimination costs of the order of n³.
- **Reading a small determinant as "almost singular".** det(10^-1 · I₂₀) = 10^-20, yet this matrix only scales by 10^-1 and has condition number 1 (MAT-003).
- **Treating any distance formula as a metric.** The p-formula with p < 1 and the cosine distance both break the triangle inequality.
- **Substituting p = ∞ into a formula.** A limit is not a value of the formula: use the ∞-norm itself.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Vector space** | A set with an addition and a scalar multiplication obeying the usual rules, such as Rⁿ |
| **Basis** | A list of vectors through which every vector is written as a linear combination in exactly one way |
| **Linear map** | A map with L(u + v) = L(u) + L(v) and L(c · v) = c · L(v) |
| **Matrix of a linear map** | The matrix whose columns are the images of the basis vectors |
| **Matrix product** | The matrix of a composition: (AB) x = A (B x) |
| **Determinant** | The signed factor by which a square matrix multiplies volumes; zero exactly when the matrix is not invertible |
| **Norm** | A length function that is positive, homogeneous and satisfies the triangle inequality |
| **p-norm** | ‖x‖ₚ = (Σ |xᵢ|ᵖ)^(1/p) for p ≥ 1, and ‖x‖∞ = max |xᵢ| |
| **Triangle inequality** | ‖x + y‖ ≤ ‖x‖ + ‖y‖, or for distances d(x, z) ≤ d(x, y) + d(y, z) |
| **Induced matrix norm** | ‖A‖ = max ‖A x‖ / ‖x‖ over x ≠ 0: the largest stretching factor of A |

---

## Self-Check Assessment

**1. Why is the map x ↦ x + (1, 0) not linear?**
> A linear map sends 0 to 0, since L(0) = L(0 · 0) = 0 · L(0) = 0. This map sends 0 to (1, 0).

**2. Why is the matrix product associative but not commutative?**
> It is the composition of linear maps. Composition of functions is always associative, so (AB)C = A(BC). The order of two maps usually matters: the rotation R and the reflection F of §3 give RF ≠ FR.

**3. Prove that ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ for every x in Rⁿ.**
> If the largest component in absolute value is xₖ, then ‖x‖∞² = xₖ² ≤ x₁² + … + xₙ² = ‖x‖₂². And ‖x‖₁² = (|x₁| + … + |xₙ|)² is the sum of the squares xᵢ² plus the products 2|xᵢ||xⱼ|, which are ≥ 0, so ‖x‖₁² ≥ ‖x‖₂². Taking square roots of these non-negative numbers gives the claim.

**4. IX's `minkowski` refuses p = 1/2. Is that a limitation or a guarantee?**
> A guarantee: below p = 1 the formula breaks the triangle inequality (§5), so refusing it keeps every result a genuine distance. The guard does not cover p = ∞, which it lets through and for which the formula returns 1 whatever the points (§6).

**Pass criteria:** Write vectors in a basis, build the matrix of a linear map, multiply matrices and explain why the order matters, read and count the cost of a determinant, and use the norm axioms to tell a norm from a formula that is not one, including in IX's distance functions.

---

## Research Basis

- S. Axler, *Linear Algebra Done Right*, 4th ed., Springer, 2024: vector spaces, linear maps and their matrices, determinants
- G. Strang, *Introduction to Linear Algebra*, 6th ed., Wellesley-Cambridge Press, 2023: the matrix product as composition, elimination, determinants and norms
- G. H. Hardy, J. E. Littlewood and G. Pólya, *Inequalities*, Cambridge University Press, 1934: Minkowski's inequality
- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019: the special values of the power function used in §6
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
