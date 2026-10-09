---
module_id: mat-012-iterative-optimisation
department: mathematics
course: Iterative Optimisation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-011-gradients-reverse-mode-autodiff]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Iterative Optimisation — Step Sizes, Curvature and What Convergence Means

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Recognise convex, L-smooth and strongly convex functions, and read L, μ and the condition number κ from a Hessian
- Show why gradient descent on a quadratic converges exactly when 0 < η < 2/L, and choose the step that minimises its rate
- State the convergence guarantees of gradient descent for nonconvex, convex and strongly convex functions, and what a small gradient does and does not prove
- Explain how heavy-ball momentum improves the asymptotic rate from (κ − 1)/(κ + 1) to (√κ − 1)/(√κ + 1) on a quadratic
- Explain Adam's moment estimates and bias correction, and why its step is of the order of η whatever the size of the gradient
- Trace what IX's optimisers, its numerical gradient and its MCP tool report, and when "converged" does not mean converged

---

## 1. Convexity, Smoothness and the Condition Number

To minimise a differentiable function f: Rⁿ → R, iterative methods look for a point where the gradient of MAT-011 vanishes. Such a **stationary point** may be a minimum, a maximum or a saddle. The function is **convex** if f(y) ≥ f(x) + ∇f(x) · (y − x) for all x and y: it lies above each of its tangent planes, so every stationary point is a global minimum. For a twice-differentiable f, this holds exactly when the Hessian ∇²f(x), the symmetric matrix of second partial derivatives, is positive semidefinite everywhere.

Two constants control how fast descent methods go. f is **L-smooth** if its gradient is L-Lipschitz, ‖∇f(x) − ∇f(y)‖ ≤ L‖x − y‖; for a twice-differentiable f, it means that every eigenvalue of every Hessian lies in [−L, L]. f is **μ-strongly convex**, with μ > 0, if every eigenvalue of every Hessian is at least μ. Their ratio κ = L/μ ≥ 1 is the **condition number** of the problem. The model case is the quadratic f(x) = ½xᵀAx − bᵀx with A symmetric positive definite: its Hessian is A everywhere, so μ and L are the smallest and largest eigenvalues of A, as in MAT-005, and κ is the condition number κ₂(A) of MAT-003.

### Practice Exercise

Let f(x, y) = x² + 10y². Find its Hessian, μ, L and κ.

> *Solution:* ∂²f/∂x² = 2, ∂²f/∂y² = 20 and the mixed derivative is 0, so the Hessian is the diagonal matrix diag(2, 20) at every point. Hence μ = 2, L = 20 and κ = 10. The level sets are ellipses whose axes are in the ratio √10 ≈ 3.16, longer along x; at a point such as (1, 1), the gradient (2, 20) points mostly along y, across the valley, rather than towards the minimum.

---

## 2. Gradient Descent on a Quadratic

**Gradient descent** takes the step x_{k+1} = x_k − η∇f(x_k), with a **step size** or learning rate η > 0. On the quadratic of §1, ∇f(x) = Ax − b and the minimiser is x* = A⁻¹b, so the error e_k = x_k − x* obeys e_{k+1} = (I − ηA)e_k. In the basis of eigenvectors of A, each component is multiplied at every step by its own factor 1 − ηλ, where λ is the corresponding eigenvalue. The iteration converges from every starting point exactly when |1 − ηλ| < 1 for every eigenvalue, that is when **0 < η < 2/L**.

The threshold is sharp. At η = 2/L, the component along the stiffest direction flips sign without shrinking; above it, that component grows like |1 − ηL|^k while the others may still shrink. The rate is max(|1 − ημ|, |1 − ηL|). The step η = 1/L gives 1 − μ/L = 1 − 1/κ, and the best fixed step, η = 2/(L + μ), balances the two extremes and gives **(κ − 1)/(κ + 1)**. For κ near 1 the method is fast; for large κ, the rate approaches 1 and the method crawls along the flat directions while the step size is capped by the steep one.

### Practice Exercise

For f(x) = (L/2)x², for which step sizes does gradient descent converge? Take L = 20 and describe what happens for η = 1/20, 3/40, 1/10 and 3/20.

> *Solution:* ∇f(x) = Lx, so x ← (1 − ηL)x, and the iteration converges exactly when |1 − ηL| < 1, that is 0 < η < 2/L = 1/10. With L = 20: η = 1/20 gives the factor 0 and reaches the minimum in one step; η = 3/40 gives −1/2, an oscillation that halves at each step; η = 1/10 gives −1, an oscillation between x₀ and −x₀ that never shrinks; η = 3/20 gives −2, an oscillation that doubles at each step.

---

## 3. The Descent Lemma and Convergence Rates

Beyond quadratics, L-smoothness still bounds f above by a parabola: f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖². This is the **descent lemma**. With y = x − η∇f(x), it gives f(y) ≤ f(x) − η(1 − Lη/2)‖∇f(x)‖², a guaranteed decrease whenever 0 < η < 2/L, largest at η = 1/L, where it is ‖∇f(x)‖²/(2L). Summing these decreases over K steps with η = 1/L gives three guarantees, where f* is the minimum value, or the infimum:

- for any L-smooth f bounded below, min over k < K of ‖∇f(x_k)‖² ≤ 2L(f(x₀) − f*)/K: some iterate is nearly stationary, which is not the same as nearly minimal;
- for a convex f with a minimiser x*, f(x_K) − f* ≤ L‖x₀ − x*‖²/(2K);
- for a μ-strongly convex f, f(x_K) − f* ≤ (1 − μ/L)^K (f(x₀) − f*), a linear rate.

Two cautions follow. First, L is a bound on the curvature everywhere the iterates go. On a non-quadratic function, a step that is safe near the minimum can be far too large elsewhere, and the local curvature at the current point is what decides the next step (§6). Second, a stopping rule of the form ‖∇f(x)‖ < tol certifies only near-stationarity. Only strong convexity turns it into a bound on the distance to the minimiser, ‖x − x*‖ ≤ ‖∇f(x)‖/μ, and no rule can certify a gradient that was computed wrongly.

### Practice Exercise

For f(x, y) = x² + 10y² of §1, how many iterations reduce the slowest error component by a factor 10^6, with η = 1/L and with η = 2/(L + μ)?

> *Solution:* With η = 1/L = 1/20, the factors are 1 − 2/20 = 0.9 along x and 0 along y, so the rate is 0.9 and 0.9^k < 10^-6 needs k ≥ 132. With η = 2/(L + μ) = 1/11, the factors are 1 − 2/11 = 9/11 and 1 − 20/11 = −9/11, the rate is (κ − 1)/(κ + 1) = 9/11, and (9/11)^k < 10^-6 needs k ≥ 69, about half as many.

---

## 4. Momentum

The **heavy-ball method** of Polyak adds a fraction β of the previous step to the gradient step: v_{k+1} = βv_k − η∇f(x_k) and x_{k+1} = x_k + v_{k+1}, or equivalently x_{k+1} = x_k − η∇f(x_k) + β(x_k − x_{k−1}). The velocity v accumulates along directions where the gradient keeps its sign and cancels along directions where it alternates, which is exactly the valley of §1: steady progress along the flat axis, damped oscillation across the steep one.

On a quadratic, the choice η = 4/(√L + √μ)² and β = ((√κ − 1)/(√κ + 1))² gives the asymptotic rate **(√κ − 1)/(√κ + 1)**. Take x² + 100y² from (1, 1), so κ = 100. Gradient descent with its best step multiplies both coordinates by ±99/101 ≈ ±0.980 at every step and needs 691 steps to bring them below 10^-6. For the heavy ball, (9/11)^k ≈ 0.818^k suggests 69 steps, but that rate is only asymptotic: with these parameters the recurrence has a double root, and with zero initial velocity the coordinates are exactly (1 + 2k/11)(9/11)^k and (1 + 20k/11)(−9/11)^k. The linear factor delays the gain, and both coordinates fall below 10^-6 only after 95 steps, still about seven times fewer than 691. The gain grows with κ, since the number of iterations scales like κ for one and √κ for the other. This rate is guaranteed on quadratics only: Lessard, Recht and Packard give a smooth, strongly convex function on which the heavy ball with these parameters does not converge. Nesterov's accelerated gradient reaches a rate of the same order, 1 − 1/√κ, with a guarantee for every smooth strongly convex function.

### Practice Exercise

With β = 0.9, what does the velocity tend to when the gradient is a constant g, as on a long straight slope?

> *Solution:* v_k = −ηg(1 + β + … + β^(k−1)), which tends to −ηg/(1 − β) = −10ηg. On a constant slope, momentum multiplies the effective step by 1/(1 − β) = 10; that is its benefit on flat directions and its danger when the slope changes, since the velocity takes about 1/(1 − β) steps to turn.

---

## 5. Adaptive Steps: Adam

**Adam**, by Kingma and Ba, keeps two exponential moving averages per coordinate: of the gradient, m_k = β₁m_{k−1} + (1 − β₁)g_k, and of its square, v_k = β₂v_{k−1} + (1 − β₂)g_k², with the defaults β₁ = 0.9 and β₂ = 0.999. It divides the first by the square root of the second: x_{k+1} = x_k − η m̂_k/(√v̂_k + ε), coordinate by coordinate, with ε = 10^-8.

Both averages start at 0, so early on they are biased towards 0: if the gradient were constant, m_k would be (1 − β₁^k) times it. **Bias correction** divides this factor out, m̂_k = m_k/(1 − β₁^k) and v̂_k = v_k/(1 − β₂^k). At the first step, m̂₁ = g₁ and v̂₁ = g₁², so the step is η g₁/(|g₁| + ε), about η in size in the direction opposite to the gradient's sign. More generally, Kingma and Ba show that the step is approximately bounded by η, whatever the scale of the gradient. This is the opposite of gradient descent, whose step is proportional to the gradient. It means that Adam cannot explode the way gradient descent does above 2/L; it also means that it has no threshold like 2/L and no general guarantee. Near a minimum where the gradient changes sign, m̂ averages the signs out while v̂ does not, and the steps shrink. Reddi, Kale and Kumar give a simple convex problem on which Adam fails to converge, and propose a corrected variant, AMSGrad.

### Practice Exercise

With η = 0.01 and the default β₁, β₂ and ε, what is Adam's first step for a gradient g = 10^-6? What would it be for a larger g without bias correction?

> *Solution:* The first corrected step is η g/(|g| + ε) = 0.01 · 10^-6/(10^-6 + 10^-8) = 0.01/1.01 ≈ 0.0099: almost the full η, even though the gradient is tiny. Without bias correction, m₁ = 0.1g and v₁ = 0.001g², and the step is η · 0.1|g|/(√0.001 |g|) ≈ 3.16η when |g| is much larger than ε: more than three times the intended size, because √v₁ ≈ 0.0316|g| underestimates |g| more than m₁ = 0.1g underestimates g.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of its loop into Python, whose floats are IEEE binary64 like Rust's `f64`: they are predictions, and §7 proposes to check them.

**The optimisers** (`crates/ix-optimize`). [`SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L21) takes the step of §2; [`Momentum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L49) is the heavy ball of §4, with its velocity started at −η∇f; and [`Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L111) is §5, with the [default constants](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L77) and the [bias correction](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L107). Unless an objective supplies its own gradient, the [trait's default](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L12) is [`numerical_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/calculus.rs#L7) with ε = 10^-7, and the closure wrapper [`ClosureObjective`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L43) supplies none. [`minimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L124) runs the loop below: it keeps the best value seen, and declares convergence as soon as the norm of the gradient it has just used falls below the tolerance.

```rust
    for i in 0..criteria.max_iterations {
        let grad = objective.gradient(&params);
        let new_params = optimizer.step(&params, &grad);
        let value = objective.evaluate(&new_params);

        if value < best_value {
            best_value = value;
            best_params = new_params.clone();
        }

        // Check gradient norm convergence
        let grad_norm: f64 = grad.dot(&grad).sqrt();
        if grad_norm < criteria.tolerance {
            return OptimizeResult {
                best_params,
                best_value,
                iterations: i + 1,
                converged: true,
            };
        }
```

**The MCP tool.** `ix_optimize` calls the handler [`optimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L181). The caller chooses a function among sphere, Rosenbrock and Rastrigin, a dimension, a method and an iteration cap, following its [schema](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L20). For the gradient methods, the handler fixes the rest: [η = 0.01 for `SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L221) and [for `Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L230), a [tolerance of 10^-8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L224) on the gradient norm, and a [start at 5 in every coordinate](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L226). It returns the best point, the best value, the number of iterations and the [`converged` flag](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L259). The methods `pso` and `annealing` use no gradient and are left aside here.

- **Divergence is reported as convergence.** The Rosenbrock function f(x, y) = 100(y − x²)² + (1 − x)² has f(5, 5) = 40,016 and gradient (40,008, −4000) at the start. Its Hessian there has ∂²f/∂x² = 28,002 and a largest eigenvalue near 28,145, so the threshold 2/L of the local curvature is about 7.1 · 10^-5 and η = 0.01 is about 140 times too large. `SGD` sends x to −395.08, then about 2.5 · 10^8, then about −5.5 · 10^25. There the spacing between neighbouring doubles is 2^33 ≈ 8.6 · 10^9, so x + 10^-7 and x − 10^-7 both round back to x; and y, still about 3.1 · 10^5, is lost next to x² ≈ 3 · 10^51 when y − x² is rounded, with or without 10^-7. Every difference quotient of the numerical gradient is then exactly 0. The loop sees a zero gradient and returns `converged` true after 4 iterations, with the best point (5, 5), the start, and the best value 40,016. In dimension 3, the same happens with the value 80,032.
- **The step size is fixed for all three functions.** On the [sphere](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L195), the sum of squares, L = 2, so η = 0.01 is fifty times smaller than the step 1/L = 1/2 that reaches the minimum at once. Each iteration multiplies the error by 1 − 2η = 0.98, and the transcription stops after 1027, 1044 and 1054 iterations in dimensions 1, 2 and 3. On Rosenbrock, the same η is far too large at the start.
- **Rastrigin's minima repel SGD.** The Rastrigin function adds, per coordinate, x² − 10 cos(2πx) + 10, whose [term](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L211) has curvature 2 + 40π² cos(2πx), up to 2 + 40π² ≈ 396.8. At each of its 55 local minima between −27 and 27, the global one at 0 included, η times this curvature exceeds 2, the smallest value being about 2.07, so by §2 each of these minima repels the iteration. The first stable ones, near ±27.8, lie far outside the region the iterates visit: from 5, the transcription stays within |x| < 5.5 and returns `converged` false after 5000 iterations. `Adam`, whose step is not proportional to the gradient, settles in the local minimum near 4.975, with a value of about 24.87 per coordinate: converged, to a stationary point that is not the global minimum 0.
- **Rosenbrock in dimension 1 is identically zero.** The objective sums over [`0..x.len() - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L200), which is empty for one coordinate, and the schema [allows a dimension of 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L24). Both methods then report convergence after 1 iteration, at 5, with the value 0.
- **The numerical gradient has an absolute step.** ε = 10^-7 is about fifty times below the best central step u^(1/3) ≈ 5 · 10^-6 of MAT-011, so its error is mostly rounding, of the order of u|f|/ε ≈ 1.1 · 10^-9 |f| per component, against a tolerance of 10^-8. And ε is not scaled by |x|: once a coordinate exceeds 2^30 ≈ 1.07 · 10^9 in size, x ± 10^-7 rounds back to x and that component is exactly 0, which is the mechanism of the first finding.
- **"SGD" is deterministic.** The type is [documented](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L8) as "Stochastic Gradient Descent", but it steps along the full gradient it is given, and nothing in the loop samples: it is the gradient descent of §2.
- **The tests check the value only.** [`test_adam_rosenbrock`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L193) runs `Adam` with η = 0.01 from (0, 0) and [asserts a best value below 0.1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L205), with the comment "Adam may not converge perfectly on Rosenbrock"; the transcription predicts convergence to within 10^-7 of (1, 1), with a best value below 10^-15. The quadratic test, `test_sgd_quadratic`, likewise [asserts a value only](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L189). Neither checks `converged` or `iterations`, the two fields that the first finding shows can mislead.

The numerical gradient perturbs one coordinate at a time by the same absolute ε:

```rust
    let n = x.len();
    let mut grad = Array1::zeros(n);
    for i in 0..n {
        let mut x_plus = x.clone();
        let mut x_minus = x.clone();
        x_plus[i] += epsilon;
        x_minus[i] -= epsilon;
        grad[i] = (f(&x_plus) - f(&x_minus)) / (2.0 * epsilon);
    }
    grad
```

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

In the first finding, why is the numerical gradient exactly 0 at x ≈ −5.5 · 10^25, when the true gradient there is enormous?

> *Solution:* Near 5.5 · 10^25, consecutive doubles are 2^33 ≈ 8.6 · 10^9 apart, so `x_plus[i] += epsilon` and `x_minus[i] -= epsilon` both leave x unchanged. The two evaluations of f are then evaluations at the same point, their difference is exactly 0, and so is the quotient. For the y-component the two points do differ, but near x² ≈ 3 · 10^51 consecutive doubles are 2^119 ≈ 6.6 · 10^35 apart, so y + 10^-7 − x² and y − 10^-7 − x² round to the same number, and f takes the same value twice. The true derivative with respect to x, of the order of 400|x|³, never enters: the difference quotient sees only the values that f returns. A step scaled by |x|, or a gradient computed by the reverse mode of MAT-011, would not vanish.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **The threshold 2/L.** Minimise f(x) = 10x², written `10.0 * x[0] * x[0]` in a `ClosureObjective`, so L = 20 and 2/L = 0.1, with `SGD` from x = 1, a tolerance of 10^-8 and a cap of 400 iterations. Prediction: η = 0.05 converges after 2 iterations; η = 0.09 converges after 97; η = 0.1 does not converge, and |x| stays within 10^-6 of 1; η = 0.2 returns `converged` true after 20 iterations with the best point 1 and the best value 10, although x has grown like 3^k.
2. **The MCP handler, called in-process.** Call `optimize` with Rosenbrock in dimension 2 and 3, with `sgd` and a cap of 5000. Prediction: `converged` true after 4 iterations, best point 5 in every coordinate, best values 40,016 and 80,032. Rosenbrock in dimension 1, with `sgd` and with `adam`: converged after 1 iteration with the value 0. Rastrigin in dimensions 1 to 3: `sgd` not converged after 5000 iterations; `adam` converged, each coordinate near 4.975 and the value near 24.87 times the dimension. The sphere with `sgd`: 1027, 1044 and 1054 iterations.
3. **Momentum.** Minimise x² + 10y² from (1, 1), with a tolerance of 10^-8 and a cap of 2000. Prediction: `SGD` with η = 1/20 converges after 183 iterations and with η = 1/11 after 108; `Momentum` with η = 4/(√20 + √2)² and β = ((√10 − 1)/(√10 + 1))² after 40.
4. **The Adam test, with the result recorded.** Rerun the setting of `test_adam_rosenbrock` and record `converged`, `iterations` and the best point. Prediction: converged after about 1300 iterations, between 1200 and 1400, at a point within 10^-7 of (1, 1), with a best value below 10^-15.
5. **Adam's first step.** Call `step` once on a fresh `Adam::new(0.01)` at the point 0 with the gradient 10^-6, and once on another with the gradient 10^6. Prediction: steps of −0.01/1.01 and of −0.01, each within 10^-12.

### Practice Exercise

Predict the number of iterations for η = 0.09 in step 1, taking the numerical gradient as exact.

> *Solution:* The factor is 1 − 0.09 · 20 = −0.8, so after i steps |x| = 0.8^i and the gradient that the loop checks is 20 · 0.8^i. It falls below 10^-8 when 0.8^i < 5 · 10^-10, that is i > ln(2 · 10^9)/ln(1.25) ≈ 95.98, so first at i = 96; the loop counts from 0 and reports i + 1 = 97 iterations. The margin at i = 96 is under 1 %, much larger than the relative rounding error of the numerical gradient.

---

## 8. Common Pitfalls

- **One learning rate for every problem.** The safe step is set by the curvature, 2/L; a fixed η can be more than a hundred times too large for one function and fifty times too small for another.
- **Reading "converged" as "minimised".** A small gradient norm certifies near-stationarity only: a saddle, a local minimum, or a gradient that was computed as zero all pass the test.
- **An absolute finite-difference step.** A step of 10^-7 vanishes into rounding once |x| exceeds 2^30; scale it by the size of x, or use automatic differentiation.
- **Ignoring the stiff direction.** On an ill-conditioned problem, the steepest direction caps the step and the flattest one sets the pace; the number of iterations grows like κ.
- **Momentum without a guarantee.** The heavy ball's rate is proven for quadratics; on other functions, it can oscillate or fail to converge where Nesterov's method would not.
- **Treating Adam's step as a gradient step.** Its size is about η whatever the gradient, so η sets a distance per step, not a fraction of the slope.
- **Testing only the value.** A test that bounds the best value but not `converged` or `iterations` passes even when the loop reports a false convergence.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Stationary point** | A point where the gradient vanishes: a minimum, a maximum or a saddle |
| **Convex function** | A function above each of its tangent planes; every stationary point is a global minimum |
| **L-smooth** | Having an L-Lipschitz gradient; the Hessian's eigenvalues lie in [−L, L] |
| **Strongly convex** | Having every Hessian eigenvalue at least μ > 0 |
| **Condition number** | κ = L/μ, the ratio of the steepest to the flattest curvature |
| **Step size** | The factor η multiplying the gradient in a descent step, also called the learning rate |
| **Descent lemma** | f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖² for an L-smooth f |
| **Heavy-ball momentum** | Gradient descent plus a fraction β of the previous step |
| **Bias correction** | Dividing Adam's moving averages by 1 − β^k to undo their start at 0 |
| **Adam** | A method dividing an average of gradients by the root of an average of their squares, per coordinate |
| **Gradient-norm stopping rule** | Stopping when ‖∇f‖ falls below a tolerance, a test of near-stationarity only |

---

## Self-Check Assessment

**1. A quadratic has μ = 2 and L = 50. For which step sizes does gradient descent converge, and which fixed step minimises its rate?**
> It converges exactly for 0 < η < 2/L = 0.04; the bound itself fails, since at η = 0.04 the stiffest component only flips sign. The best fixed step is 2/(L + μ) = 2/52 ≈ 0.038, with the rate (κ − 1)/(κ + 1) = 24/26 ≈ 0.92 for κ = 25.

**2. A run stops with ‖∇f‖ < 10^-8. What do you know about the point it returns?**
> That the last gradient the loop computed was small. If f is μ-strongly convex and that gradient was accurate, the point is within 10^-8/μ of the minimiser; otherwise it may be a saddle, a local minimum, or, as in IX's Rosenbrock case, a point where the numerical gradient rounded to zero. In IX, the returned point is also the best one seen, which may not be the point where the gradient was small.

**3. Why does heavy-ball momentum help on x² + 100y², and where does its guarantee stop?**
> With κ = 100, tuned heavy-ball momentum has the asymptotic rate 9/11 instead of 99/101, because velocity builds up along the flat direction and cancels across the steep one. From (1, 1) with zero initial velocity, it brings both coordinates below 10^-6 in 95 steps instead of 691; the asymptotic estimate, 69, ignores a transient factor that grows linearly with k. The rate is proven for quadratics only; Lessard, Recht and Packard give a strongly convex function on which it fails, while Nesterov's method keeps a rate of order 1 − 1/√κ on every smooth strongly convex function.

**4. `ix_optimize` returns `converged` true after 4 iterations for Rosenbrock. Can you trust it?**
> Not from that flag alone. Compare the best point with the start and look at the best value: here they are (5, 5) and 40,016, the starting values, which means that no iteration improved on the start. The gradient vanished because the iterates grew so large that the numerical step rounded away, not because they reached the minimum at (1, 1).

**Pass criteria:** Read μ, L and κ from a Hessian, derive the threshold 2/L and the best fixed step on a quadratic, state the guarantees of gradient descent and what a small gradient proves, explain the rates of heavy-ball momentum and the step of Adam, and trace when IX's loop reports convergence that did not happen.

---

## Research Basis

- H. H. Rosenbrock, "An automatic method for finding the greatest or least value of a function", *The Computer Journal* 3, 1960: the banana-shaped valley used as a test function
- B. T. Polyak, "Some methods of speeding up the convergence of iteration methods", *USSR Computational Mathematics and Mathematical Physics* 4, 1964: the heavy-ball method and its rate on quadratics
- Y. Nesterov, "A method of solving a convex programming problem with convergence rate O(1/k²)", *Soviet Mathematics Doklady* 27, 1983: accelerated gradient methods
- S. Boyd and L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004: convexity, strong convexity and the convergence of gradient descent
- J. Nocedal and S. J. Wright, *Numerical Optimization*, 2nd ed., Springer, 2006: step sizes, line searches and finite-difference gradients
- D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization", *International Conference on Learning Representations*, 2015: Adam, its bias correction and the bound on its step
- L. Lessard, B. Recht and A. Packard, "Analysis and design of optimization algorithms via integral quadratic constraints", *SIAM Journal on Optimization* 26, 2016: a strongly convex function on which the heavy ball fails to converge
- S. J. Reddi, S. Kale and S. Kumar, "On the convergence of Adam and beyond", *International Conference on Learning Representations*, 2018: a convex problem on which Adam fails, and AMSGrad
- Y. Nesterov, *Lectures on Convex Optimization*, 2nd ed., Springer, 2018: the descent lemma and the convergence rates of §3
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
