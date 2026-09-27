---
module_id: mat-003-floating-point-conditioning
department: mathematics
course: Foundations of Numerical Computation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Floating-Point Arithmetic and Conditioning — When a Computer Loses Digits

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Explain why most real numbers, including 0.1, cannot be stored exactly in a computer
- State the standard model of floating-point rounding and the meaning of machine epsilon
- Distinguish forward error from backward error, and a badly conditioned problem from an unstable algorithm
- Prove the bound that defines the condition number of a linear system
- Estimate from κ(A) how many digits a computation can lose, and find where IX draws that line in its code

---

## 1. Numbers a Computer Can Store

A computer does not store real numbers. It stores a **finite** set of them. The usual format, IEEE 754 **binary64** (`f64` in Rust, `double` in C), packs a number into 64 bits: 1 sign bit, 11 exponent bits and 52 fraction bits. With the implicit leading 1, every stored number carries **53 significant bits**, about 16 decimal digits.

The stored numbers are not evenly spaced. Between 1 and 2 they are 2^-52 apart; between 2 and 4, twice as far apart; and so on. Two quantities describe this grid:
- **Machine epsilon** ε = 2^-52 ≈ 2.2 × 10^-16 is the gap between 1 and the next stored number.
- **Unit roundoff** u = ε/2 = 2^-53 ≈ 1.1 × 10^-16 is the largest relative error made when a real number (within range) is rounded to the nearest stored one.

A number is stored exactly only if it is a fraction whose denominator is a power of two (and it fits the range and the 53 bits). **0.1 = 1/10 is not**: its denominator contains the factor 5, so its binary expansion never ends, just as 1/3 = 0.333… never ends in decimal. The computer stores the nearest binary64 number instead. This is why `0.1 + 0.2 == 0.3` is not a safe test: each literal is rounded, the sum is rounded again, and nothing guarantees that the result lands on the same stored number as 0.3.

### Practice Exercise

Which of these numbers are stored exactly in binary64: 0.5, 0.75, 0.1, 1/3, 2^60?

> *Solution:* 0.5 = 2^-1, 0.75 = 2^-1 + 2^-2 and 2^60 are exact: each is a sum of a few powers of two, well within range. 0.1 and 1/3 are not: their denominators (10 and 3) are not powers of two, so their binary expansions are infinite and must be rounded.

---

## 2. The Standard Model of Rounding

IEEE 754 requires each basic operation to be **correctly rounded**: the computer returns the exact result, rounded to a stored number. With round-to-nearest, and as long as nothing overflows or underflows, this gives the **standard model**:

fl(x ∘ y) = (x ∘ y)(1 + δ), with |δ| ≤ u, for ∘ one of +, −, ×, ÷.

So a *single* operation is almost exact. Trouble comes from two places:
- **Accumulation.** A long computation makes many small errors, and they can add up.
- **Cancellation.** Subtracting two nearly equal numbers is exact or nearly exact, but it exposes the rounding errors that the operands *already* carried. The leading digits cancel; what remains is mostly noise.

### Practice Exercise

The number a = 1 + 10^-8 is stored with relative error at most u, and b = 1 is stored exactly. Bound the relative error of the computed difference â − b, ignoring the (tiny) error of the subtraction itself.

> *Solution:* The stored value is â = a(1 + δ) with |δ| ≤ u. Then â − b = (a − b) + aδ, so the relative error is |aδ| / |a − b| ≤ u(1 + 10^-8) / 10^-8 ≈ 10^8 · u ≈ 1.1 × 10^-8. The result has about 8 correct digits, not 16: the subtraction lost half of them.

---

## 3. Forward Error, Backward Error and Conditioning

Suppose we want y = f(x) and the computer returns ŷ.
- The **forward error** asks: how far is the answer from the truth? It is |ŷ − y| / |y|.
- The **backward error** asks: for which nearby input is ŷ the *exact* answer? It is the smallest relative perturbation |Δx| / |x| such that ŷ = f(x + Δx).

An algorithm is **backward stable** if its backward error is always of the order of u: it gives the exact answer to a slightly different question. Whether that answer is *close to the truth* depends on the problem, not the algorithm. The **condition number** measures how strongly the problem amplifies a relative change in its input. The two combine into the most useful rule of numerical analysis:

forward error ≲ condition number × backward error.

This separates two different failures: a **badly conditioned problem** (no algorithm can do much better) and an **unstable algorithm** (a better algorithm would).

### Practice Exercise

For a differentiable function, the relative condition number is |x · f′(x) / f(x)|. Compute it for f(x) = x − 1 and evaluate it at x = 1 + 10^-8.

> *Solution:* f′(x) = 1, so the condition number is |x / (x − 1)|. At x = 1 + 10^-8 it is (1 + 10^-8) / 10^-8 ≈ 10^8. This is the cancellation of §2 seen from the problem's side: any relative error in x is amplified about 10^8 times, whatever algorithm computes x − 1.

---

## 4. The Condition Number of a Matrix

Now solve a linear system A x = b, with A square and invertible. Suppose the right-hand side is perturbed: A(x + Δx) = b + Δb. How large can the relative change in x be?

**Theorem.** For any vector norm and its induced matrix norm,

‖Δx‖ / ‖x‖ ≤ κ(A) · ‖Δb‖ / ‖b‖, where κ(A) = ‖A‖ · ‖A⁻¹‖.

*Proof (direct, as in MAT-001):*
- Subtracting A x = b from A(x + Δx) = b + Δb gives A Δx = Δb, so Δx = A⁻¹ Δb and ‖Δx‖ ≤ ‖A⁻¹‖ · ‖Δb‖.
- From b = A x we get ‖b‖ ≤ ‖A‖ · ‖x‖, so 1 / ‖x‖ ≤ ‖A‖ / ‖b‖ (for b ≠ 0).
- Multiplying the two inequalities gives ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. ∎

In the Euclidean norm, κ₂(A) = σ_max / σ_min, the ratio of the largest to the smallest **singular value** of A. Geometrically, A maps the unit sphere to an ellipsoid; the singular values are the lengths of its semi-axes, so κ₂ measures how flattened that ellipsoid is. This lesson uses singular values as a black box; how they are computed (the SVD) is the subject of a later module.

**Rule of thumb.** A backward-stable solver in binary64 gives a relative forward error of roughly κ(A) · u. With u ≈ 10^-16, you can expect to lose about **log₁₀ κ(A)** of the roughly 16 significant digits. When κ(A) approaches 1/u ≈ 10^16, no digit of the answer can be trusted. This is an estimate from an upper bound, not a theorem about every case.

### Practice Exercise

Compute κ₂ of A = diag(1, 10^-8). How many of the 16 digits can a solution of A x = b lose?

> *Solution:* The singular values of a diagonal matrix are the absolute values of its diagonal entries: 1 and 10^-8. So κ₂(A) = 1 / 10^-8 = 10^8, and a solve can lose about 8 of the 16 significant digits.

---

## 5. Where IX Draws the Line

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that behaviour and does not change it.

- [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) uses Gauss–Jordan elimination with partial pivoting. It returns `MathError::Singular` when the largest available pivot has magnitude below 10^-12 ([line 110](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110)). That threshold is **absolute**: it depends on the scale of A, not on κ(A).
- [`SvdResult::rank(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) and [`pseudo_inverse(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) keep only the singular values strictly above `tol`, an absolute tolerance chosen by the caller. The `ix_svd` agent tool chooses a **relative** one, σ₁ · 10^-10 ([`handlers.rs` line 639](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639)).
- IX has **no condition-number function**. κ₂ must be computed as σ_max / σ_min from [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100).
- [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L68) solves the normal equations XᵀX w = Xᵀy with `inverse(...).expect("X^T X is singular")`, so any `Singular` verdict becomes a panic rather than an error. Forming XᵀX also squares the condition number: for X with full column rank, κ₂(XᵀX) = κ₂(X)², because the singular values of XᵀX are the squares of those of X.

The pivot test, verbatim from `linalg.rs` lines 110–112:

```rust
        if max_val < 1e-12 {
            return Err(MathError::Singular);
        }
```

### Practice Exercise

Using only the code above, predict what `inverse` returns for A = 10^-13 · I₂ (the 2 × 2 identity scaled by 10^-13) and for A = [[1, 2], [2, 4]]. Which verdict says something about the matrix, and which only about its scale?

> *Solution:* Both return `Singular`. For 10^-13 · I₂, the first pivot has magnitude 10^-13 < 10^-12, so `inverse` stops, although κ₂ = 1 (perfect conditioning) and the inverse, 10^13 · I₂, is easy to compute. For [[1, 2], [2, 4]], the second row is twice the first, so the matrix is exactly singular; IX's own test [`test_singular_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L219) checks this case. Only the second verdict describes the matrix. The first describes its scale, and conversely a matrix with an enormous κ but pivots above 10^-12 is inverted without any warning.

---

## 6. Experiment: Hilbert Matrices in IX

The Hilbert matrix H_n is the n × n matrix with entries 1 / (i + j − 1). It is the classic test of ill-conditioning:
- H_n is symmetric positive definite, so it is **invertible for every n** in exact arithmetic.
- Its exact inverse has **integer entries** (Choi 1983), which gives an exact reference to measure errors against.
- κ₂(H_n) grows like (1 + √2)^(4n) / √n, roughly e^(3.5n) (Todd 1954): each extra row and column multiplies it by about (1 + √2)^4 ≈ 34.
- The *stored* H_n is already not H_n, because entries such as 1/3 are rounded. By §4, even a perfect algorithm then inherits an error of up to about κ · u.

**Protocol.** For n = 2 to 12, a Learn lab that pins IX at `e35138b9` builds H_n, computes κ₂ from IX's `svd`, inverts H_n with `inverse` and with `pseudo_inverse`, measures the residuals and the error against the exact integer inverse, and records the first n, if any, at which `inverse` returns `Singular`.

**Predictions, written before the run:**
1. κ₂ computed from `svd` grows roughly geometrically in n.
2. The number of correct digits in the computed inverse falls roughly like 16 − log₁₀ κ₂.
3. Any `Singular` verdict for H_n reflects the absolute pivot threshold of §5, not a true singularity, since H_n is invertible for every n.

<!-- MAT003-LAB-RESULTS: pending. Fill only by pasting the Learn lab output and cite its artefact hash. -->
> **Measured results pending.** The table of measured values will be copied from the Learn lab run, with its artefact hash, before publication. No number in this section is estimated by hand.

### Practice Exercise

Using κ₂(H_n) ≈ e^(3.5n) and the rule of thumb of §4, estimate the size n at which a computed inverse of H_n has no trustworthy digit left.

> *Solution:* No digit survives once κ₂ reaches about 1/u ≈ 10^16. Solving e^(3.5n) = 10^16 gives n = 16 · ln 10 / 3.5 ≈ 36.8 / 3.5 ≈ 10.5. The growth law hides a constant factor and the 1 / √n term, so this is an order-of-magnitude estimate; the measured table tells you where it actually happens.

---

## 7. Common Pitfalls

- **Comparing computed floats with `==`.** Compare with a tolerance chosen from the problem, and make it relative when the scale varies.
- **Trusting a small residual.** A small residual r = b − A x̂ does not mean a small error: by the theorem of §4 with Δb = −r, the relative error can be as large as κ(A) · ‖r‖ / ‖b‖.
- **Reading "not singular" as "well conditioned".** An absolute pivot threshold, like the one in `inverse`, measures scale, not conditioning.
- **Inverting to solve.** Computing A⁻¹ and then A⁻¹ b does more work than solving A x = b directly and is usually less accurate; forming XᵀX squares κ.
- **Believing printed digits.** Printing 17 digits does not make them correct; log₁₀ κ of them may be noise.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **binary64** | The IEEE 754 64-bit floating-point format: 53 significant bits, about 16 decimal digits |
| **Machine epsilon (ε)** | The gap between 1 and the next stored number: 2^-52 in binary64 |
| **Unit roundoff (u)** | The largest relative error of rounding to nearest: u = ε/2 = 2^-53 |
| **Cancellation** | Loss of correct digits when subtracting nearly equal numbers that already carry errors |
| **Forward error** | The distance between the computed answer and the true answer |
| **Backward error** | The smallest input perturbation for which the computed answer is exact |
| **Backward stable** | Describes an algorithm whose backward error is always of the order of u |
| **Condition number** | How strongly a problem amplifies relative changes in its input; for a matrix, κ(A) = ‖A‖ · ‖A⁻¹‖ |
| **Singular value** | A semi-axis length of the image of the unit sphere under A; κ₂(A) = σ_max / σ_min |
| **Hilbert matrix** | The matrix with entries 1 / (i + j − 1): invertible but extremely ill-conditioned |

---

## Self-Check Assessment

**1. Why is 0.1 not stored exactly in binary64, while 0.75 is?**
> 0.75 = 3/4 has a power-of-two denominator, so its binary expansion is finite. 0.1 = 1/10 has the factor 5 in its denominator, so its binary expansion is infinite and must be rounded.

**2. An algorithm is backward stable, yet its answer has only 4 correct digits. Is the algorithm at fault?**
> Not necessarily. Forward error ≲ condition number × backward error. With a backward error near 10^-16, 4 correct digits point to a condition number near 10^12: the problem, not the algorithm, loses the digits.

**3. State and prove the bound that defines κ(A) for A x = b.**
> ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. Proof: Δx = A⁻¹ Δb gives ‖Δx‖ ≤ ‖A⁻¹‖ ‖Δb‖, and b = A x gives 1 / ‖x‖ ≤ ‖A‖ / ‖b‖; multiply the two.

**4. IX's `inverse` returns a matrix without error. Does that mean the result is accurate?**
> No. `inverse` only refuses when a pivot falls below the absolute threshold 10^-12. A matrix with a large κ and larger pivots is inverted silently, and the result can lose about log₁₀ κ digits. Compute κ₂ from `svd` to know.

**Pass criteria:** Explain the binary64 grid and the standard model, distinguish forward from backward error, prove the κ(A) bound, and use κ to predict and explain digit loss, including in IX's `inverse`.

---

## Research Basis

- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019: the binary64 format and correctly rounded operations
- D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys* 23(1), 5–48, 1991, doi:10.1145/103162.103163
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002: the standard model, forward and backward error, and condition numbers of linear systems
- J. Todd, 1954, National Bureau of Standards Applied Mathematics Series 39: the growth of the condition number of Hilbert matrices
- M.-D. Choi, "Tricks or Treats with the Hilbert Matrix", *American Mathematical Monthly* 90(5), 1983: the integer entries of the inverse
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §5 links to its line
- Measurements: pending the Learn lab `code/streeling-mathematics/`, which pins IX at the same commit
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.80) F(0.02) U(0.15) C(0.03)
