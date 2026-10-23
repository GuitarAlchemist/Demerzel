---
module_id: mat-003-floating-point-conditioning
department: mathematics
course: Floating-Point Arithmetic and Conditioning
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Floating-Point Arithmetic and Conditioning — When a Computer Loses Digits

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Explain why most real numbers, including 0.1, cannot be stored exactly in a computer
- State the standard model of floating-point rounding and the meaning of machine epsilon
- Distinguish forward error from backward error, and a badly conditioned problem from an unstable algorithm
- Prove the bound that defines the condition number of a linear system
- Estimate from κ(A) how many digits a computation can lose, and find where IX draws that line in its code

---

## 1. Numbers a Computer Can Store

A computer does not store real numbers. It stores a **finite** set of them. The usual format, IEEE 754 **binary64** (`f64` in Rust, `double` in C), packs a number into 64 bits: 1 sign bit, 11 exponent bits and 52 fraction bits. With the implicit leading 1, every **normal** stored number carries **53 significant bits**, about 16 decimal digits. The tiny **subnormal** numbers near zero give up that leading 1 and have fewer.

The stored numbers are not evenly spaced. Between 1 and 2 they are 2^-52 apart; between 2 and 4, twice as far apart; and so on. Two quantities describe this grid:
- **Machine epsilon** ε = 2^-52 ≈ 2.2 × 10^-16 is the gap between 1 and the next stored number.
- **Unit roundoff** u = ε/2 = 2^-53 ≈ 1.1 × 10^-16 is the largest relative error made when a real number in the **normal range** is rounded to the nearest stored one. Below that range, among the subnormals, the relative error can be much larger: 2^-1075 rounds to 0, a relative error of 1.

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
- The *stored* H_n is already not H_n, because entries such as 1/3 are rounded: fl(H_n) = H_n + ΔH with ‖ΔH‖ ≤ u‖H_n‖ in the ∞-norm. §4 bounds perturbations of b, not of A. For A, the standard result is: if κ(A) · δ < 1 with δ = ‖ΔA‖ / ‖A‖, then ‖(A + ΔA)⁻¹ − A⁻¹‖ / ‖A⁻¹‖ ≤ κ(A)δ / (1 − κ(A)δ) (Higham 2002). So even a perfect inversion of fl(H_n) has a relative error of up to about κ · u while κ · u is small, and an unbounded one once κ · u ≥ 1, where the rounded matrix may even be singular.
- For a symmetric matrix A, κ∞(A) / n ≤ κ₂(A) ≤ κ∞(A), where κ∞ uses the maximum-row-sum norm. This **band** is a theorem about the norms of **one and the same** matrix.

**Protocol.** The Learn lab [`code/streeling-mathematics`](https://github.com/spareilleux/learn/tree/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics) pins IX at `e35138b9`. Its predictions were written and hashed before any compile ([`preregistration.md`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/preregistration.md), SHA-256 `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20`). For n = 2 to 16 it builds fl(H_n) and the same matrices multiplied by 2^-20 and 2^20. Multiplying by a power of two is exact in binary floating point, so it changes the scale and not the conditioning. For each matrix it records:
- `kappa_inf`: κ∞ of the exact H_n, from the exact integer inverse; `kappa_2`: σ₁ / σ_n from IX's `svd` of the stored fl(H_n); `band`: whether `kappa_2` lies between `kappa_inf` / n and `kappa_inf`. **Correction:** these two columns describe two different matrices, so `band` is a mixed comparison, not the theorem above;
- `inverse`: IX's answer, `ok` or `Singular`; `fwd_err`: its forward error ‖X − H_n⁻¹‖∞ / ‖H_n⁻¹‖∞ against the exact inverse; `residual`: ‖H_n X − I‖∞;
- `rank`: the rank at the `ix_svd` tolerance σ₁ · 10^-10; `pinv_res`: the residual of that truncated `pseudo_inverse`; `pinv0_fwd`: the forward error of `pseudo_inverse(0.0)`.

**Measured** on Windows 11 x86-64 (rustc 1.94.0), copied from [`expected/mat003_conditioning.txt`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/expected/mat003_conditioning.txt) (SHA-256 `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`):

```text
 n  kappa_inf  kappa_2    band  inverse   fwd_err   residual  rank  pinv_res  pinv0_fwd
 2  2.70e1     1.93e1     ok    ok        2.96e-16  0.00e0       2  4.44e-16  4.44e-16
 3  7.48e2     5.24e2     ok    ok        5.97e-15  1.51e-14     3  3.02e-14  5.64e-15
 4  2.84e4     1.55e4     ok    ok        5.55e-14  5.19e-13     4  1.28e-12  1.59e-13
 5  9.44e5     4.77e5     ok    ok        7.26e-13  1.14e-11     5  3.84e-11  4.79e-12
 6  2.91e7     1.50e7     ok    ok        8.89e-11  9.57e-10     6  7.61e-10  1.62e-10
 7  9.85e8     4.75e8     ok    ok        3.02e-9   5.51e-8      7  1.01e-8   2.22e-9
 8  3.39e10    1.53e10    ok    ok        4.82e-9   1.04e-6      7  1.39e0    5.78e-8
 9  1.10e12    4.93e11    ok    ok        3.05e-6   2.54e-4      8  1.36e0    2.55e-4
10  3.54e13    2.10e12    out   ok        1.10e-4   9.91e-3      8  1.47e0    1.00e0
11  1.23e15    2.72e12    out   Singular  -         -            8  1.66e0    1.00e0
12  4.12e16    1.51e12    out   Singular  -         -            9  1.52e0    1.00e0
13  1.32e18    4.31e12    out   Singular  -         -            9  1.83e0    1.00e0
14  4.54e19    7.66e13    out   Singular  -         -           11  3.62e0    1.00e0
15  1.54e21    1.26e14    out   Singular  -         -            9  1.90e0    1.00e0
16  5.06e22    9.71e14    out   Singular  -         -            9  1.98e0    1.00e0
```

```text
Refusal boundary, by scale (the true kappa does not change with scale)
  scale 1      first Singular: 11             worst accepted fwd_err: 1.10e-4 at n = 10
  scale 2^-20  first Singular: 6              worst accepted fwd_err: 7.26e-13 at n = 5
  scale 2^20   first Singular: none up to 16  worst accepted fwd_err: 1.04e0 at n = 14
  scale 1 verdicts: 2:ok 3:ok 4:ok 5:ok 6:ok 7:ok 8:ok 9:ok 10:ok 11:S 12:S 13:S 14:S 15:S 16:S

Scaling by 2^k is exact in binary floating point; is the answer?
  inverse(2^k H) == inverse(H) / 2^k bit for bit: 13 of 13 accepted pairs
  IX kappa_2 bit-identical at the three scales: 5 of 15

Controls
  I * 2^-40: kappa = 1, inverse Singular
  I * 2^-39: kappa = 1, inverse ok, inverse == I * 2^39: true
  [[1,2],[2,4]]: inverse Singular, rank(sigma_1 * 1e-10) = 1
  exact H_3^-1 = [[9, -36, 30], [-36, 192, -180], [30, -180, 180]], H_3 * H_3^-1 == I exactly: Some(true)
  checker on a wrong inverse (I for H_3^-1): residual 1.42e0
```

**Pre-registered predictions and verdicts:**

| Prediction | Measured | Verdict |
|---|---|---|
| `inverse(H_n)` first returns `Singular` at n = 11 | first `Singular` at n = 11, then at every n up to 16 | confirmed |
| The refusal tracks scale, not conditioning | I · 2^-40 (κ = 1) refused, I · 2^-39 accepted; 2^-20 · H_n refused from n = 6; 2^20 · H_n never refused up to n = 16, with a forward error of 1.04e0 at n = 14 | confirmed |
| Every accepted inverse has a forward error ≤ n · κ∞ · u | holds; the worst is 1.10e-4, at n = 10 | confirmed |
| `inverse(2^k H_n)` = `inverse(H_n)` / 2^k, bit for bit | 13 of 13 accepted pairs | confirmed |
| `rank(σ₁ · 10^-10)` first drops below n at n = 8 | rank 7 at n = 8; the truncated residual is at least 1.36 from there on | confirmed |
| IX's κ₂ stays inside the band up to n = 11 | inside for n = 2 to 9 only; below κ∞ / n from n = 10 | **refuted** as pre-registered, but the band mixes H_n and fl(H_n): see the correction below |
| IX's κ₂ is bit-identical at the three scales | 5 of 15 sizes | **refuted** |

**What the run shows:**
- The `Singular` boundary is set by the absolute pivot threshold, not by the matrix. The same matrices, only rescaled, are refused from n = 6 or never refused at all. At scale 2^20, `inverse` answers at n = 14 with a forward error of 1.04e0 — no correct digit — and raises no error.
- **Correction.** An earlier version of this lesson read the `band` failures as proof that IX's `svd` returns a wrong κ₂. A review pointed out that the band compares κ∞ of the exact H_n with the κ₂ that IX computes for the stored fl(H_n), while the theorem only relates norms of one matrix. For an ill-conditioned H_n, rounding the entries can change the condition number substantially. So the fact that `kappa_2` falls below `kappa_inf` / n from n = 10 is an **observation**: the reported value is not κ₂(H_n), but the run cannot tell how much of the gap comes from rounding the input and how much from the SVD. Settling it would need a reference for the same stored matrix, such as κ of fl(H_n) computed in higher precision, which this lab does not have. The `rank` column is no longer monotone either (11 at n = 14, then 9 at n = 15), which is also only an observation.
- IX's κ₂ changes under an exact rescaling for all but 5 of the 15 sizes. The cause is **not identified**; it is left as an open reproduction for IX, not explained or fixed here.
- `pseudo_inverse(0.0)`, which keeps every singular value, has a forward error of 1.00e0 from n = 10: no correct digit either.
- The rule of thumb of §4 remains theory, not a measured law: the measured errors stay below n · κ∞ · u, and at n = 10 (κ∞ = 3.54e13) the error is 1.10e-4.

**Platforms.** The numbers were measured on one machine. Hosted CI then reran the lab on Linux x86-64, Windows x86-64 and macOS arm64 (rustc 1.98.1; [Learn PR #24](https://github.com/spareilleux/learn/pull/24), [run 36335008098](https://github.com/spareilleux/learn/actions/runs/36335008098)) and reproduced this output byte for byte, including a digest of the raw bits of every computed value (`0ffcce71a1dffe45`). Identical output shows that the computation is **reproducible** on those platforms. It does not show that it is **correct**: correctness needs an independent reference for the same problem, such as the exact inverse behind `fwd_err`, and identical output only means that every platform makes exactly the same errors.

### Practice Exercise

Using κ₂(H_n) ≈ e^(3.5n) and the rule of thumb of §4, estimate the size n at which a computed inverse of H_n has no trustworthy digit left.

> *Solution:* No digit survives once κ₂ reaches about 1/u ≈ 10^16. Solving e^(3.5n) = 10^16 gives n = 16 · ln 10 / 3.5 ≈ 36.8 / 3.5 ≈ 10.5. The growth law hides a constant factor and the 1 / √n term, so this is only an order of magnitude. In the measured table, κ∞ first exceeds 10^16 at n = 12 (4.12e16), with the true κ₂ between κ∞ / n and κ∞; `inverse` still answers at n = 10 with a forward error of 1.10e-4 and refuses from n = 11.

---

## 7. Common Pitfalls

- **Comparing computed floats with `==`.** Compare with a tolerance chosen from the problem, and make it relative when the scale varies.
- **Trusting a small residual.** A small residual r = b − A x̂ does not mean a small error: by the theorem of §4 with Δb = −r, the relative error can be as large as κ(A) · ‖r‖ / ‖b‖.
- **Trusting a computed condition number near 1/u.** κ is computed in floating point too, from rounded input: in §6, the κ₂ that IX reports for the stored fl(H_n) is below the lower bound for the exact H_n from n = 10. It is therefore not the condition number of the problem you meant, whatever the share of rounding and of the SVD in the gap.
- **Reading "not singular" as "well conditioned".** An absolute pivot threshold, like the one in `inverse`, measures scale, not conditioning.
- **Inverting to solve.** Computing A⁻¹ and then A⁻¹ b does more work than solving A x = b directly and is usually less accurate; forming XᵀX squares κ.
- **Believing printed digits.** Printing 17 digits does not make them correct; log₁₀ κ of them may be noise.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **binary64** | The IEEE 754 64-bit floating-point format: 53 significant bits for normal numbers, about 16 decimal digits |
| **Machine epsilon (ε)** | The gap between 1 and the next stored number: 2^-52 in binary64 |
| **Unit roundoff (u)** | The largest relative error of rounding to nearest in the normal range: u = ε/2 = 2^-53 |
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
> No. `inverse` only refuses when a pivot falls below the absolute threshold 10^-12. A matrix with a large κ and larger pivots is inverted silently, and the result can lose about log₁₀ κ digits. A κ₂ computed with IX's `svd` is only a diagnostic, not a proof of accuracy: near 1/u that estimate can itself be unreliable (§6). Check against an independent reference, such as a known exact inverse or an independently validated condition estimate, before trusting the digits.

**Pass criteria:** Explain the binary64 grid and the standard model, distinguish forward from backward error, prove the κ(A) bound, and use κ to predict and explain digit loss, including in IX's `inverse`.

---

## Research Basis

- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019: the binary64 format and correctly rounded operations
- D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys* 23(1), 5–48, 1991, doi:10.1145/103162.103163
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002: the standard model, forward and backward error, and condition numbers of linear systems
- J. Todd, 1954, National Bureau of Standards Applied Mathematics Series 39: the growth of the condition number of Hilbert matrices
- M.-D. Choi, "Tricks or Treats with the Hilbert Matrix", *American Mathematical Monthly* 90(5), 1983: the integer entries of the inverse
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §5 links to its line
- Measurements: Learn lab `code/streeling-mathematics/` at commit `c8135fa508fcb9d35593e8dedbb925c44282b3a2` (Learn PR #24), which pins IX at the same commit; expected output SHA-256 `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`, pre-registration SHA-256 `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20`; measured on Windows 11 x86-64 (rustc 1.94.0), output reproduced by hosted CI on Linux, Windows and macOS (run 36335008098)
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
