---
module_id: mat-024-dynamical-systems-stability-feedback
department: mathematics
course: Dynamical Systems, Stability and Feedback
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Dynamical Systems, Stability and Feedback — What a Derivative, an Exponent and a Rank Can Tell

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Find the fixed points and cycles of a map, decide their stability from a multiplier, and say when linearisation decides nothing
- Compute a Lyapunov exponent as the orbit average of log|f′|, and say what its sign does and does not tell about the attractor
- Locate period-doubling bifurcations, estimate Feigenbaum's δ from them, and explain why a scan with a fixed tolerance misplaces them
- Stabilise an unstable fixed point by OGY control, and say when the controller acts linearly, saturates, or is not needed at all
- Derive the scalar Kalman filter and its steady state, and explain why the Joseph form keeps a covariance honest where the short form does not
- Decide controllability and observability by the Kalman rank test, and read the margin and the tolerance on which a numerical rank depends
- Trace what IX's `ix-chaos` and `ix-signal` crates compute, which of their outputs a test pins down, and what they leave out

---

## 1. Fixed Points and Linearisation

A discrete dynamical system iterates a map: x_(k+1) = f(x_k). A **fixed point** x* satisfies f(x*) = x*. Write x_k = x* + e_k; a Taylor expansion gives e_(k+1) = f′(x*) e_k + O(e_k²), so near x* the error is multiplied at each step by the **multiplier** f′(x*). If |f′(x*)| < 1 the fixed point is asymptotically stable: small errors shrink by about that factor per step, and when the multiplier is negative they alternate in sign. If |f′(x*)| > 1 it is unstable. If |f′(x*)| = 1, linearisation decides nothing, and the higher-order terms settle the question. If f′(x*) = 0 the fixed point is **superstable**: the error is squared at each step.

The **logistic map** f(x) = r x (1 − x), with 0 ≤ r ≤ 4, maps [0, 1] into itself. For r > 1 it has a fixed point x* = 1 − 1/r besides 0, and since f′(x) = r(1 − 2x), the multiplier there is f′(x*) = 2 − r. At r = 2.5, x* = 0.6 and the multiplier is −0.5: errors halve and alternate. At r = 2, x* = 1/2 is superstable. At r = 3.2 the multiplier is −1.2, and x* repels.

A **cycle** of period p is a fixed point of the p-th iterate f^p, and by the chain rule its multiplier is the product of f′ along the cycle. For the logistic map the 2-cycle exists for r > 3, and its multiplier works out to 4 + 2r − r². It is stable while |4 + 2r − r²| < 1, that is, for 3 < r < 1 + √6 ≈ 3.449490. It is superstable at r = 1 + √5 ≈ 3.236068, where the cycle passes through x = 1/2. It is born at r = 3, where the fixed point's multiplier passes through −1, and it loses stability where its own multiplier reaches −1.

In n dimensions, x_(k+1) = F(x_k) is linearised with the Jacobian J of F at the fixed point, and the fixed point is stable when every eigenvalue of J has modulus less than 1, that is, when the **spectral radius** ρ(J) is below 1 (MAT-005). For a linear system x_(k+1) = A x_k, ρ(A) < 1 is necessary and sufficient for x_k → 0 from every start. It does not prevent transient growth. A = [[0.5, 10], [0, 0.5]] has ρ(A) = 0.5, but from x_0 = (0, 1) the first component of x_k is 10k · 0.5^(k−1): 10 at the first and second steps, 7.5 at the third, and below 1 only from the eighth. The eigenvalues fix the long run; for a non-normal A the norm, here about 10.02, bounds the short run. CYB-002 describes the dampening of oscillations between repositories in words; the multiplier is its quantitative form.

### Practice Exercise

At which r does the logistic map's fixed point x* = 1 − 1/r lose stability?

> *Solution:* The multiplier is f′(x*) = 2 − r, and |2 − r| < 1 holds for 1 < r < 3. At r = 3 the multiplier reaches −1 and the 2-cycle is born. At r = 3 itself linearisation decides nothing: the orbit still approaches x*, but so slowly that §2's exponent, averaged over 10,000 steps, comes out at −0.000359.

---

## 2. Lyapunov Exponents

Two orbits of a one-dimensional map that start δ_0 apart are, after n steps, about |δ_0| times the product of |f′(x_i)| along the orbit apart. The **Lyapunov exponent** is the average growth rate per step:

```
λ = lim (1/n) Σ_{i<n} ln|f′(x_i)|
```

If λ < 0, nearby orbits converge: the orbit is attracted to a stable fixed point or cycle. If λ > 0, nearby orbits separate exponentially while staying bounded, which is the signature of chaos. λ = 0 marks marginal behaviour, such as a bifurcation point or quasiperiodic motion. At a stable fixed point the terms ln|f′(x_i)| tend to ln|f′(x*)|, and so does their average, so λ = ln|f′(x*)|. On a stable cycle of period p, λ is ln|multiplier| divided by p. If the orbit passes exactly through a point where f′ = 0, the logarithm is −∞, and so is λ.

For the logistic map, starting from x_0 = 0.1, discarding 1,000 steps and averaging the next 10,000:

| r | 2.5 | 2.9 | 3.0 | 3.2 | 3.5 | 3.7 | 3.8 | 3.83 | 4.0 |
|---|---|---|---|---|---|---|---|---|---|
| λ | −0.693147 | −0.105361 | −0.000359 | −0.916291 | −0.872507 | 0.350235 | 0.428314 | −0.369511 | 0.693135 |
| Attractor | fixed point | fixed point | fixed point, marginal | 2-cycle | 4-cycle | chaotic | chaotic | 3-cycle | chaotic |

The theory checks out. At r = 2.5, λ = ln 0.5 = −0.693147, and at r = 2.9, λ = ln 0.9 = −0.105361. On the 2-cycle at r = 3.2 the multiplier is 4 + 6.4 − 10.24 = 0.16, and λ = (1/2) ln 0.16 = ln 0.4 = −0.916291. At r = 4 the exact value is ln 2 = 0.693147, and the run comes within 0.000012 of it. r = 3.83 lies in the period-3 window that opens at 1 + √8 ≈ 3.828427, inside the chaotic range: a negative exponent there is not an error. At r = 2 and r = 1 + √5 the orbit runs into x = 1/2 and λ = −∞.

The sign tells whether nearby orbits converge, not what they converge to: a fixed point, a 2-cycle and a 3-cycle all give λ < 0. To tell them apart, one counts the period (§3).

For a system in n dimensions there are n exponents. Benettin and his colleagues compute them by evolving n tangent vectors with the Jacobian along the orbit, re-orthonormalising them by a QR decomposition at each step, and averaging the logarithms of the diagonal of R. For a flow, which must be integrated in time, the integration scheme for the tangent vectors enters the result (§7).

### Practice Exercise

Compute λ at r = 2.9 without iterating, and explain why the same reasoning gives λ = (1/2) ln|4 + 2r − r²| on the 2-cycle.

> *Solution:* The orbit converges to x* = 1 − 1/2.9, where f′(x*) = 2 − 2.9 = −0.9, so the terms of the average tend to ln 0.9 and λ = ln 0.9 = −0.105361. On the 2-cycle the terms alternate between ln|f′(p)| and ln|f′(q)|, whose sum is the logarithm of the multiplier |f′(p) f′(q)| = |4 + 2r − r²|, so each step contributes half of it on average.

---

## 3. Period Doubling and Feigenbaum's Constant

As r grows past r_1 = 3, the fixed point gives way to a stable 2-cycle, which gives way at r_2 = 1 + √6 to a stable 4-cycle, then an 8-cycle, and so on: at r_k the multiplier of the 2^(k−1)-cycle passes through −1. Solving that condition by Newton's method, with 40 significant digits, gives:

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| r_k | 3 | 3.449489743 | 3.54409036 | 3.564407266 | 3.56875942 | 3.56969161 |

The gaps shrink geometrically. The ratios δ_k = (r_(k+1) − r_k) / (r_(k+2) − r_(k+1)) are 4.7514, 4.6563, 4.6682 and 4.6687, and they converge to **Feigenbaum's constant** δ = 4.669201…, the same for every smooth one-humped map with a quadratic maximum (Feigenbaum, 1978). The cascade accumulates at r_∞ ≈ 3.569946, which extrapolating the gaps with δ gives. Beyond r_∞ chaos alternates with periodic windows, such as the period-3 window of §2.

Finding these points from orbits is harder than it looks. A numerical period test iterates past a transient and returns the first p for which x_(k+p) comes back within a tolerance of x_k. Near r_k the cycle's multiplier is close to −1, so the orbit approaches the cycle slowly, and after a fixed transient it is still too far away for a fixed tolerance. A scan over r therefore sees a doubling where the convergence happens to pass the test, which may be before or after the true r_k (§7).

### Practice Exercise

Predict r_6 from r_3, r_4 and r_5 with δ ≈ 4.669, and compare with the table.

> *Solution:* r_6 ≈ r_5 + (r_5 − r_4)/4.669 = 3.56875942 + 0.00435215/4.669 ≈ 3.569692. The table gives 3.56969161: the geometric law already holds to about one part in ten million of r.

---

## 4. Controlling Chaos: OGY and Pyragas

A chaotic attractor contains infinitely many unstable periodic orbits, among them the fixed point x*. Ott, Grebogi and Yorke (1990) proposed to stabilise one of them with small changes to a parameter. Linearise in both the state and the parameter: x_(k+1) − x* ≈ f_x (x_k − x*) + f_r (r_k − r_0), where f_x and f_r are the partial derivatives at (x*, r_0). The perturbation

```
δr_k = −(f_x / f_r) (x_k − x*)
```

cancels the linear term, so the next deviation is of second order. Since the perturbation must stay small, it is clamped to |δr| ≤ δr_max, and the controller acts linearly only inside the window |x − x*| ≤ δr_max |f_r| / |f_x|. Outside the window it saturates, and it is the chaotic orbit itself that eventually brings the state into the window.

For the logistic map at r_0 = 3.8: x* = 0.736842, f_x = 2 − r_0 = −1.8, f_r = x*(1 − x*) = 0.193906, and with δr_max = 0.1 the window has half-width 0.010773. Starting from x_0 = 0.5 with control from step 50, the perturbation saturates at steps 50 to 55. At step 56 the deviation is 1.0407e-2, inside the window, and the next ones are 8.7741e-4, 6.3042e-6, 3.2578e-10 and 2.2204e-16. Each is about 8.2 times the square of the one before, and the ratio tends to 8.1971: once the linear term is cancelled, the quadratic terms −r_0 e² + (1 − 2x*) e δr are what remains.

Pyragas (1992) proposed a control for flows that needs no model: add K (x(t − τ) − x(t)) to the dynamics, where τ is the period of the orbit to stabilise. On that orbit the term vanishes, so the control costs nothing once it has succeeded; τ must match the period.

### Practice Exercise

With δr_max = 0.05 instead of 0.1, what is the half-width of the window, and what changes?

> *Solution:* 0.05 × 0.193906 / 1.8 ≈ 0.005386, half as wide. The chaotic orbit enters a narrower window less often, so the wait before capture is longer on average. Once the orbit is inside, convergence is the same, since the linear term is cancelled whatever δr_max is.

---

## 5. The Kalman Filter as Optimal Linear Estimation

A linear model has a hidden state x_k = F x_(k−1) + w_k, observed as z_k = H x_k + v_k, with independent noises w ~ N(0, Q) and v ~ N(0, R). The **Kalman filter** alternates two steps:

```
predict:  x⁻ = F x            P⁻ = F P Fᵀ + Q
update:   S = H P⁻ Hᵀ + R     K = P⁻ Hᵀ S⁻¹
          x = x⁻ + K (z − H x⁻)
          P = (I − K H) P⁻
```

The gain K minimises the posterior error variance among all linear updates, and with Gaussian noise the estimate is the conditional mean of the state given the measurements (Kalman, 1960).

In the scalar case F = H = 1, a constant measured with noise, take Q = 0.01 and R = 1. In steady state P⁻ = P + Q and P = P⁻ R / (P⁻ + R), so P⁻² − Q P⁻ − Q R = 0 and P⁻ = (Q + √(Q² + 4QR)) / 2 = 0.105125. The steady gain is K = P⁻ / (P⁻ + R) = 0.095125, and the posterior variance is P = K R = 0.095125. Each new measurement then gets weight 0.095, an exponential forgetting over about 1/K ≈ 10.5 measurements. Starting from x = 0 with P = 1, the measurements 5.2, 4.8, 5.1, 4.9, 5.0, 5.3, 4.7, 5.1, 4.9 and 5.0, whose mean is 5.0, give the estimates 2.6129, 3.3540, 3.8055, 4.0373, 4.2120, 4.3869, 4.4325, 4.5225, 4.5703 and 4.6219, as the gain falls from 0.5025 to 0.1201. After ten measurements the estimate is still 0.3781 short of 5: the prior x = 0 still weighs.

The update P = (I − KH) P⁻ is right only for the optimal gain. The **Joseph form** P = (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ holds for any gain and stays symmetric and positive semidefinite in floating point. With P⁻ = 1 and R = 1 the optimal gain 0.5 gives P = 0.5 both ways. With a gain of 0.8, imposed or degraded by rounding, the true posterior variance is 0.2² × 1 + 0.8² × 1 = 0.68, but the short form reports 0.2: it understates the uncertainty more than threefold.

### Practice Exercise

With Q = 0.04 and R = 1, find the steady-state P⁻ and K. Does the filter now follow changes faster or slower?

> *Solution:* P⁻ = (0.04 + √(0.0016 + 0.16)) / 2 ≈ 0.220998, and K = 0.220998 / 1.220998 ≈ 0.180998. The gain is almost twice as large: the filter trusts the model less, follows changes faster, and passes more measurement noise into its estimate.

---

## 6. Controllability and Observability

A linear time-invariant system x_(k+1) = A x_k + B u_k, y_k = C x_k, with n states, is **controllable** when the input can steer any state to any other in finitely many steps, and **observable** when the outputs determine the initial state. After n steps from x_0 = 0, the reachable states are the column space of the **controllability matrix** [B, AB, …, A^(n−1) B]. By the Cayley–Hamilton theorem A^n is a combination of I, A, …, A^(n−1), so further powers add nothing, and the system is controllable exactly when this matrix has rank n (Kalman). Likewise it is observable exactly when the **observability matrix** [C; CA; …; C A^(n−1)] has rank n. The two are dual: (A, C) is observable exactly when (Aᵀ, Cᵀ) is controllable. Hautus's test names the culprit: (A, B) is controllable exactly when [A − λI, B] has rank n for every eigenvalue λ of A. For a diagonal A with distinct eigenvalues, mode i is controllable exactly when row i of B is nonzero, and observable exactly when column i of C is nonzero.

The discrete double integrator A = [[1, 1], [0, 1]], B = [0; 1], C = [1, 0] has [B, AB] = [[0, 1], [1, 1]] and [C; CA] = [[1, 0], [1, 1]], both of rank 2, with singular values φ = 1.618034 and 1/φ = 0.618034. The modal system A = diag(1, 2, 3), B = [1; 1; 0], C = [1, 1, 0] has [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [0, 0, 0]], of rank 2, with singular values 4.838, 0.7735 and 0: its third mode is neither reachable nor visible, and [A − 3I, B] has rank 2.

A computer decides rank by counting the singular values above a tolerance. The LAPACK and NumPy convention takes max(rows, cols) × σ_max × ε, with ε = 2^(−52): 3.22e-15 for the modal system. A change of basis x → Tx, with T = [[1, 2, 0], [0, 1, 1], [1, 0, 2]] (det T = 4), turns (A, B, C) into (TAT⁻¹, TB, CT⁻¹), with no zero left to read. The ranks do not change: the transformed controllability matrix has singular values 11.76 and 0.7791, and a third that is 0 in exact arithmetic and a rounding residue of order 1e-16 in floating point, against a tolerance of 7.84e-15.

The smallest singular value, the **margin**, is the 2-norm distance to the nearest matrix of lower rank (Eckart–Young, MAT-006). With A = diag(1, 1 + 1e-10) and C = [1, 1], the observability matrix has singular values of about 2 and 5e-11: observable, but two modes that the output cannot practically tell apart. With A = diag(1, 3) they are 3.414214 and 0.585786.

Powers of A also degrade the computation. For A = diag(1, 2, …, n) and B a column of ones, the controllability matrix is a Vandermonde matrix, and Vandermonde matrices are notoriously ill-conditioned (Gautschi, 1975). With singular values computed to 60 digits and the tolerance above, n = 12 gives σ_max = 8.057e11, σ_min = 1.139e-4 and a tolerance of 2.147e-3, hence rank 11, for a system that is controllable: its eigenvalues are distinct and B touches every mode. Scaling A by 1/12 brings σ_max down to 5.143 and the tolerance to 1.37e-14, and the rank back to 12. Scaling helps without curing: scaled the same way, n = 20 has σ_min = 1.541e-16 against a tolerance of 3.009e-14, and rank 18. The staircase algorithms of Paige and of Van Dooren (1981) reduce (A, B) by orthogonal transformations and never form the powers.

### Practice Exercise

In the modal system, replace B by [1; 1; 1]. Is it controllable now? And observable?

> *Solution:* Controllable: B touches every mode and the eigenvalues are distinct, and [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [1, 3, 9]] is a Vandermonde matrix with determinant (2 − 1)(3 − 1)(3 − 2) = 2. Still not observable: C = [1, 1, 0] misses the third mode, and the observability matrix keeps rank 2.

---

## 7. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of `lyapunov.rs`, `bifurcation.rs` and `control.rs` in `crates/ix-chaos`, and of `kalman.rs` and `state_space.rs` in `crates/ix-signal`. The transcription reproduces the assertions of the tests this section cites. It does not cover `bifurcation_diagram`, `drive_response_sync`, the constant-velocity filter, or the construction and simulation tests of the state-space model. These numbers are predictions, and §8 proposes to check them.

**The exponent of a map, and the name it is given.** [`mle_1d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L8) averages ln|f′| along the orbit after a transient, and [returns −∞](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L23) at the first |f′| below 1e-15. The MCP tool `ix_chaos_lyapunov` is the handler [`chaos_lyapunov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1436), which runs it on the logistic map [from x_0 = 0.1 with a transient of 1,000](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1449) and names the result with [a threshold of 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1450), by [`classify_dynamics`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L160):

```rust
pub fn classify_dynamics(mle: f64, threshold: f64) -> DynamicsType {
    if mle > threshold {
        if mle > 10.0 {
            DynamicsType::Divergent
        } else {
            DynamicsType::Chaotic
        }
    } else if mle > -threshold {
        DynamicsType::Periodic
    } else {
        DynamicsType::FixedPoint
    }
}
```

The enum's documentation describes [`FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L150) as convergence to a fixed point and [`Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L152) as a quasiperiodic orbit or limit cycle, which is how the exponents of a flow read. For a map, §2 shows that every stable cycle has λ < 0. The tool therefore names the 2-cycle at r = 3.2, the 4-cycle at r = 3.5 and the 3-cycle at r = 3.83 `FixedPoint`. It names r = 3 `Periodic`, where the fixed point is about to lose stability and no cycle exists yet. IX's own loop-metric tests pin two more consequences: a NaN exponent fails every comparison and [falls through to `FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L279), and a [stalled loop is `Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L256). The tests of `mle_1d` check that [r = 4 gives ln 2 within 0.05](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L179), where the transcription is within 0.000012, and that [r = 3.2 gives a negative value](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L195).

**The spectrum: RK4 for the state, Euler for the tangents.** [`lyapunov_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L43) integrates the state with [a fourth-order Runge–Kutta step](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L65), but moves the tangent vectors by [one Euler step, with the Jacobian taken at the state already updated](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L92), then re-orthonormalises them by [modified Gram–Schmidt](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L106). For the linear flow ẋ = a x the exact exponent is a, but an Euler step multiplies a tangent vector by 1 + a dt, so the function returns ln|1 + a dt| / dt. With dt = 0.01 that is −1.005034 for a = −1 and 0.995033 for a = +1: a bias of about a² dt / 2 that more steps do not remove. The function has no test, and nothing in the workspace calls it; only IX's chaos-theory guides show it in examples.

**Period detection with a fixed tolerance.** [`detect_period`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L61) compares the iterates after the transient with [the first one](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L77). Its test checks [periods 1 and 2 at r = 2.5 and 3.2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L159); with the test's settings the transcription also finds 4 at r = 3.5, 8 at 3.55, 16 at 3.566, 3 at 3.83, and no period at 3.8. [`find_period_doublings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L92) scans r uniformly, detects the period [with a tolerance of 1e-8 and at most 64](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L108), and records r wherever the period is twice the previous point's; [a point without a period resets the comparison](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L110). On [2.9, 3.57] from x_0 = 0.5, the transcription gives:

| Scan points | Transient | Doublings reported | Ratios from them |
|---|---|---|---|
| 68 | 1,000 | 3.55 | none |
| 68 | 10,000 | 3.45, 3.55 | none |
| 671 | 1,000 | 2.985, 3.444, 3.542, 3.569 | 4.684, 3.63 |
| 671 | 10,000 | 2.999, 3.449, 3.565, 3.569 | 3.879, 29.0 |

The first doubling is at r = 3, yet the third row reports 2.985, where the fixed point is still stable. There the multiplier is −0.985, and after 1,000 steps the orbit is still about 1e-8 from x*. One step later it lies on the other side, about 1.99e-8 from the starting iterate, which fails the tolerance; two steps later it is 2.99e-10 away, which passes, so the scan sees period 2. None of the rows comes near δ. [`feigenbaum_delta`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L124) itself only takes the ratios. Its [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L170) feeds it four hard-coded points, from which it gets 4.7515 and 4.6578, and asserts only that the first ratio lies between 3 and 6. `find_period_doublings` has no test.

**OGY: the test passes without control.** [`ogy_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L17) computes the perturbation of §4 and [clamps it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L42). Its [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L154) is §4's run, and it asserts that the last state lies [within 0.1 of x*](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L176). The transcription locks within 2.2e-16 from step 60. Without any control, the state at step 199 is 0.0892 from x*, which passes as well. From x_0 = 0.3, 0.6 and 0.9 the uncontrolled distances are 0.0876, 0.1653 and 0.1481. Over 10,000 starting points drawn uniformly (Python's `random`, seed 0), 28.28% end within 0.1 with no control at all, and all of them lock within 1e-12 with it. The test's tolerance cannot tell control from chance.

**Pyragas: a delay one step short.** [`pyragas_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L57) keeps the delayed states in a ring buffer that starts as [`delay_steps` copies of x_0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L68):

```rust
    for step in 0..steps {
        trajectory.push(x.clone());

        let mut dx = dynamics(&x);

        // Apply Pyragas control after startup
        if step >= control_start && step >= delay_steps {
            let delayed = &history[step % delay_steps];
            for i in 0..n {
                dx[i] += gain * (delayed[i] - x[i]);
            }
        }

        // Euler integration (simple for demonstration)
        for i in 0..n {
            x[i] += dt * dx[i];
        }

        history[step % delay_steps] = x.clone();
    }
```

At step k it reads slot k mod d, which step k − d wrote after its update, with the state x_(k−d+1). The control term therefore uses x(t − (d − 1) dt), not x(t − d dt). With `delay_steps` = 1 it reads the current state and the control term is zero, whatever the gain. With 0 the first remainder it computes panics: at line 78 if control starts at step 0, at line 89 otherwise. The example in IX's guide passes [628 steps for one period of 2π at dt = 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/chaos-theory/chaos-control.md#L112), so the effective delay is 627 steps. The function has no test.

**Kalman: the short form, and a guard built around its panic.** [`KalmanFilter::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L36) sets [H = 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L39), Q = 0.01 I, R = I and P = I, and the crate's contracts say these [defaults are not a usable filter](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L12). [`update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L65) inverts S [with `expect("Innovation covariance singular")`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L76) and updates P by [the short form](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L82). The [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L134) is §5's scalar run, and it asserts that the last estimate lies [within 0.5 of 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L161); the transcription ends at 4.6219, 0.3781 away. The MCP handlers refuse a measurement noise below [1e-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L956). Their documentation explains that the floor prevents the panic, notes that the update ["uses `P = (I − KH)P`, not the Joseph form"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L937), and records [a measured table](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L940) in which q = r = 1e-13 panics from four samples on.

**Rank tests with a margin and a tolerance.** [`StateSpaceModel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L121) builds the [controllability](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L265) and [observability](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L282) matrices with n blocks, which its comments justify by Cayley–Hamilton. [`rank_report`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L372) uses [the tolerance of §6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L396) and reports the [smallest singular value as the margin](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L400). The tests pin §6's examples: the [double integrator](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L232), the [dark third mode](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L241), the [same system after the change of basis](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L257), and the [two margins](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L391). A filter whose control matrix was never set [gives rank 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L475). The comment on the test's change of basis says [det = −3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L53); the determinant is 4, which does no harm, since any invertible matrix serves. The module documentation warns that for a large spectral radius [the rank may be reported low](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L66) and that a staircase algorithm is not implemented. §6 shows the effect from n = 12 with eigenvalues 1 to 12. The state-space model is not exposed through MCP.

**What is absent.** Nothing in `ix-signal` or `ix-chaos` tests stability by the spectral radius. The one field named `spectral_radius` in the workspace, in a [reservoir network](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L12), [rescales the weights by their largest absolute entry](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L34), which is not the spectral radius. There is no Lyapunov equation, no LQR and no PID controller. IX's gap matrix distinguishes the [two Lyapunovs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L171): the exponent, which IX has, and the Lyapunov function, a stability certificate from solving AᵀPA − P = −Q, which it [plans](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L314).

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

The tool `ix_chaos_lyapunov` answers `FixedPoint` for the logistic map at r = 3.5. What is the attractor, and how would you find out with IX?

> *Solution:* A stable 4-cycle. Its exponent, −0.872507, is below −0.01, hence the name, which only says that nearby orbits converge. `detect_period` with the test's settings returns 4.

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **A sweep of λ(r).** Run `mle_1d` on the logistic map for r from 2.5 to 4.0 in steps of 0.001, from x_0 = 0.1 with 10,000 iterations after a transient of 1,000, and name each value with `classify_dynamics` at 0.01. Prediction: at the r of §2's table, its values to six decimals; `Chaotic` at 3.7, 3.8 and 4.0; `FixedPoint` at 3.2, 3.5 and 3.83; `Periodic` at 3.0.
2. **The doubling scan.** Run `find_period_doublings` on [2.9, 3.57] from x_0 = 0.5 with the four settings of §7. Prediction: the four rows of its table, including the doubling at 2.985.
3. **OGY with and without control.** Run IX's test as written, then with `control_start` = 200, so that control never starts. Prediction: a final distance of 2.2e-16 with control, 0.0892 without; both pass the test's tolerance of 0.1.
4. **The Pyragas delay.** Run `pyragas_control` on a two-dimensional oscillator with `delay_steps` = 1, once with gain 0 and once with gain 5. Then run it with `delay_steps` = 0. Prediction: the two runs with a delay of 1 give the same trajectory bit for bit; a delay of 0 panics.
5. **The scalar filter.** Run the test's filter, then the same filter over 200 measurements of 0. Prediction: the ten estimates of §5 to four decimals; after 200 steps a gain and a covariance of 0.095125.
6. **The rank under powers.** Build A = diag(1, …, n) with B a column of ones, and run `controllability` for n = 12, then with A scaled by 1/12, and for n = 14 scaled by 1/14. Prediction: ranks 11, 12 and 14. The singular values nearest the tolerance lie a factor of 3 or more from it, so a floating-point SVD should not change these ranks. §6's n = 20 is left out: one of its singular values lies within a factor of 2.5 below the tolerance.

### Practice Exercise

Step 3 predicts that the test passes with and without control. What test would separate the two?

> *Solution:* One that asserts what only control achieves. For example: a final distance below 1e-12, which the controlled run reaches by step 60 and the uncontrolled one does not; or capture from many starting points. With control, all 10,000 random starts lock within 1e-12, while without it, 28.28% end within 0.1 by chance.

---

## 9. Common Pitfalls

- **Reading a negative exponent as a fixed point.** Every stable cycle of a map has λ < 0; the period has to be counted separately.
- **Reading "Periodic" as "a cycle".** For a map an exponent near zero marks marginal behaviour, such as a bifurcation point, not a stable cycle.
- **Trusting linearisation at |f′(x*)| = 1.** There the higher-order terms decide, and convergence, if any, is slow.
- **Taking ρ(A) < 1 to mean "never grows".** A non-normal A can amplify a state many times before it decays.
- **Locating bifurcations with one tolerance and one transient.** Near a bifurcation convergence is slowest, so that is where a fixed test errs.
- **Accepting a control test that passes without control.** A tolerance looser than the uncontrolled spread proves nothing.
- **Using the short covariance update with a gain that is not optimal.** Only the Joseph form stays correct for any gain.
- **Reading full rank as "well controllable" or "well observable".** The margin says how far the system is from losing the property; scale the system before comparing margins.
- **Forming high powers of A.** The Kalman matrices inherit the conditioning of A's powers; orthogonal staircase reductions avoid them.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Fixed point** | A state x* with f(x*) = x* |
| **Multiplier** | f′(x*) at a fixed point, or the product of f′ along a cycle; stability needs modulus below 1 |
| **Superstable** | A fixed point or cycle with multiplier 0, where errors are squared at each step |
| **Spectral radius** | The largest modulus of an eigenvalue; ρ(A) < 1 makes x_(k+1) = A x_k converge to 0 |
| **Lyapunov exponent** | The average of ln\|f′\| along an orbit: the exponential rate at which nearby orbits separate |
| **Period-doubling bifurcation** | A parameter value where a cycle's multiplier passes through −1 and a cycle of twice the period is born |
| **Feigenbaum's constant** | δ = 4.669201…, the limit of the ratios of successive gaps between doublings |
| **OGY control** | Small parameter changes that cancel the linear deviation from an unstable fixed point |
| **Kalman filter** | The recursive linear estimator that minimises the posterior error variance |
| **Joseph form** | The covariance update (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ, valid for any gain |
| **Controllability, observability** | The input can steer any state to any other; the outputs determine the initial state |
| **Kalman rank test** | Controllability and observability hold exactly when the matrices [B, …, A^(n−1) B] and [C; …; C A^(n−1)] have rank n |
| **Margin** | The smallest singular value of a test matrix: its distance to a matrix of lower rank |

---

## Self-Check Assessment

**1. A tool reports λ = −0.37 and "FixedPoint" for a one-dimensional map. What do you know about the attractor?**
> That nearby orbits converge, so the attractor is stable: a fixed point or a stable cycle of any period. At r = 3.83 the logistic map gives exactly this answer for a 3-cycle. The period has to be counted separately.

**2. Why does OGY converge quadratically once it has captured the orbit, and why does it need a window?**
> The perturbation cancels the linear term of the deviation, so what remains is of second order. The window comes from the clamp on the perturbation: only within |x − x*| ≤ δr_max |f_r| / |f_x| can the controller cancel the linear term exactly, and outside it, it waits for the chaotic orbit to bring the state in.

**3. A filter uses the update P = (I − KH) P⁻ with a gain that rounding has moved away from the optimum. What goes wrong?**
> The short form holds only for the optimal gain. With any other gain it misstates the covariance; with P⁻ = 1, R = 1 and K = 0.8 it reports 0.2 instead of the true 0.68, so the filter becomes overconfident. The Joseph form gives 0.68 for any gain.

**4. The system A = diag(1, …, 12), B = ones is controllable, yet a rank test reports 11. Is the test wrong?**
> In exact arithmetic the rank is 12, since the eigenvalues are distinct and B touches every mode. But the controllability matrix is a Vandermonde matrix with σ_max ≈ 8.1e11 and σ_min ≈ 1.1e-4. The smallest singular value lies below the relative tolerance of 2.1e-3, so numerically the matrix cannot be told from a rank-11 one. Scaling A by 1/12 restores rank 12; a staircase algorithm avoids the powers altogether.

**Pass criteria:** Decide the stability of a fixed point or cycle from its multiplier; compute a Lyapunov exponent and say what its sign does not tell; estimate Feigenbaum's δ from bifurcation points and explain why a scan misplaces them; compute the OGY window and explain the quadratic convergence; derive the scalar Kalman steady state and explain the Joseph form; decide controllability and observability by the rank test and read the margin and the tolerance; and say which of IX's outputs its tests pin down.

---

## Research Basis

- S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2nd edition, Westview Press, 2015: fixed points, linearisation, the logistic map and bifurcations
- R. M. May, "Simple mathematical models with very complicated dynamics", *Nature* 261, 1976: the logistic map
- M. J. Feigenbaum, "Quantitative universality for a class of nonlinear transformations", *Journal of Statistical Physics* 19, 1978: the constant δ
- G. Benettin, L. Galgani, A. Giorgilli and J.-M. Strelcyn, "Lyapunov characteristic exponents for smooth dynamical systems and for Hamiltonian systems", *Meccanica* 15, 1980: the spectrum by repeated orthonormalisation
- E. Ott, C. Grebogi and J. A. Yorke, "Controlling chaos", *Physical Review Letters* 64, 1990: OGY control
- K. Pyragas, "Continuous control of chaos by self-controlling feedback", *Physics Letters A* 170, 1992: delayed feedback control
- R. E. Kalman, "A new approach to linear filtering and prediction problems", *Journal of Basic Engineering* 82, 1960: the Kalman filter
- R. E. Kalman, "On the general theory of control systems", *Proceedings of the First IFAC Congress*, 1960: controllability, observability and duality
- R. S. Bucy and P. D. Joseph, *Filtering for Stochastic Processes with Applications to Guidance*, Interscience, 1968: the Joseph form
- M. L. J. Hautus, "Controllability and observability conditions of linear autonomous systems", *Indagationes Mathematicae* 31, 1969: the eigenvalue test
- C. C. Paige, "Properties of numerical algorithms related to computing controllability", *IEEE Transactions on Automatic Control* 26, 1981, and P. Van Dooren, "The generalized eigenstructure problem in linear system theory", same volume: why the powers of A should not be formed, and the staircase reduction
- W. Gautschi, "Norm estimates for inverses of Vandermonde matrices", *Numerische Mathematik* 23, 1975: the conditioning of Vandermonde matrices
- C. Eckart and G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1, 1936: the margin as a distance
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §7 links to its line
- Experiment: proposed in §8, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
