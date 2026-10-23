---
module_id: mat-011-gradients-reverse-mode-autodiff
department: mathematics
course: Gradients and Reverse-Mode Automatic Differentiation
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Gradients and Reverse-Mode Automatic Differentiation — The Chain Rule Run Backwards on a Tape

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Compute gradients and Jacobians, and apply the chain rule to a composition as a product of matrices
- Write a computation as an evaluation trace and propagate derivatives through it in forward mode
- Run reverse mode on a tape, and explain why one reverse sweep gives a whole gradient
- Handle matrix products, broadcasting and reused values in a backward pass
- Use finite differences as an oracle, and choose the step that balances truncation and rounding error
- Trace what IX's autodiff tape, its finite-difference tests and its MCP tool do and do not guarantee

---

## 1. Derivatives, Gradients and the Chain Rule

For a function f: Rⁿ → R, the **partial derivative** ∂f/∂xᵢ is the rate of change of f when only xᵢ moves, and the **gradient** ∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ) collects them. It gives the best linear approximation f(x + d) ≈ f(x) + ∇f(x) · d for small d, and it points in the direction in which f increases fastest. For a function F: Rⁿ → Rᵐ, the **Jacobian** J_F(x) is the m × n matrix whose row i is the gradient of the i-th output: it is the matrix, in the sense of MAT-004, of the linear map that best approximates F near x.

The **chain rule** says that the linear approximation of a composition is the composition of the linear approximations: J_{G∘F}(x) = J_G(F(x)) J_F(x), a product of matrices, as in MAT-004. For a scalar function g of y = F(x), it reads ∇(g∘F)(x) = J_F(x)ᵀ ∇g(y): the gradient with respect to x is the gradient with respect to y multiplied by the transposed Jacobian. Every method in this lesson is a way of organising this product.

### Practice Exercise

Let f(x, y) = (xy + x)². Compute ∂f/∂x and ∂f/∂y at (1, 2).

> *Solution:* Write u = xy + x, so that f = u², with u = 3 and f = 9 at (1, 2). By the chain rule, ∂f/∂x = 2u · ∂u/∂x = 2u(y + 1) = 18, and ∂f/∂y = 2u · ∂u/∂y = 2u · x = 6.

---

## 2. Evaluation Traces and Forward Mode

A program computes f through a sequence of elementary operations, each with a known derivative. Written out with one name per intermediate value, the sequence is an **evaluation trace**, or Wengert list. For the function of §1:

v₁ = x, v₂ = y, v₃ = v₁v₂, v₄ = v₃ + v₁, v₅ = v₄², f = v₅.

**Forward mode** carries, next to each value vᵢ, its **tangent** v̇ᵢ, the derivative of vᵢ along a chosen input direction, and updates it with the local derivative of each operation: v̇₃ = v̇₁v₂ + v₁v̇₂, v̇₄ = v̇₃ + v̇₁, v̇₅ = 2v₄v̇₄. Seeding the inputs with a direction d gives at the output the directional derivative J d, a **Jacobian–vector product**, for a small constant multiple of the cost of evaluating f. A full gradient of f: Rⁿ → R therefore takes n forward sweeps, one per input.

Automatic differentiation is neither symbolic nor numerical differentiation. It never builds a formula for the derivative, so expressions do not swell, and loops and branches are handled as they run; and it uses no step size, so its result is exact up to the rounding of the operations themselves.

### Practice Exercise

Run forward mode on the trace above at (x, y) = (1, 2) with the seed (ẋ, ẏ) = (1, 0). What are v̇₃, v̇₄ and v̇₅? What does the seed (0, 1) give?

> *Solution:* v̇₁ = 1 and v̇₂ = 0. Then v₃ = 2 and v̇₃ = 1 · 2 + 1 · 0 = 2; v₄ = 3 and v̇₄ = 2 + 1 = 3; v₅ = 9 and v̇₅ = 2 · 3 · 3 = 18, which is ∂f/∂x. The seed (0, 1) gives v̇₃ = 1, v̇₄ = 1 and v̇₅ = 6, which is ∂f/∂y: two sweeps for two partial derivatives.

---

## 3. Reverse Mode and the Tape

**Reverse mode** runs the trace forward once, recording each operation and the values it will need on a **tape**, then walks the tape backwards. It carries for each value its **adjoint** v̄ᵢ = ∂f/∂vᵢ, the sensitivity of the output to that value. The output starts with the adjoint 1. Each operation passes to each of its inputs its own adjoint times the local partial derivative, and a value used by several operations receives the sum of the contributions: the chain rule sums over every path from the value to the output.

One reverse sweep gives the adjoint of every input, so the whole gradient of a scalar function costs a small constant multiple of one evaluation of f, whatever the number of inputs. In matrix terms, a reverse sweep computes a **vector–Jacobian product** v̄ᵀ J, where forward mode computes J d. The price is memory: every value that a local derivative needs must stay on the tape until the backward walk reaches it. Forward mode suits functions with few inputs and many outputs, reverse mode the opposite, such as a loss that depends on millions of parameters. Reverse mode applied to a neural network is **backpropagation**.

### Practice Exercise

Run reverse mode on the trace of §2 at (1, 2). Give the adjoints of v₄, v₃, x and y.

> *Solution:* v̄₅ = 1. Since v₅ = v₄², v̄₄ = 2v₄ · v̄₅ = 6. The sum v₄ = v₃ + v₁ passes 6 to v₃ and 6 to v₁. The product v₃ = v₁v₂ passes v̄₃ · v₂ = 12 to v₁ and v̄₃ · v₁ = 6 to v₂. So x̄ = 6 + 12 = 18 and ȳ = 6: both partial derivatives in one sweep. x is used twice, and its adjoint is the sum of the two contributions.

---

## 4. Arrays: Matrix Products, Broadcasting and Reuse

Machine-learning code applies the same rules to whole arrays. For Z = AB, with A of size m × k and B of size k × n, and a scalar loss L whose adjoint with respect to Z is the m × n array Z̄, the chain rule gives Ā = Z̄ Bᵀ and B̄ = Aᵀ Z̄. The shapes check themselves: Z̄ Bᵀ is m × n times n × k, the shape of A.

**Broadcasting** lets an operation combine arrays of different shapes by repeating the smaller one: adding a 1 × 3 row b to each row of a 2 × 3 matrix uses b twice. Each use sends back an adjoint, so b̄ is the sum of Z̄ over the rows. The general rule, often called **unbroadcasting**, sums the incoming adjoint over every axis that broadcasting created or stretched, back to the shape of the operand. **Reuse** is the same rule in another form: in x · x the same array is both operands, each operand receives Z̄ times the other, x, and the adjoint of x is their sum, 2x times Z̄ element by element.

### Practice Exercise

Let L = sum(AB) with A = [[0.1, −0.5, 1.2], [0.3, −0.8, 0.7]] and B = [[0.5, −0.2], [0.8, 1.1], [−0.4, 0.3]], written row by row. Compute Ā and B̄.

> *Solution:* The sum gives the adjoint 1 to every entry of Z = AB, so Z̄ is the 2 × 2 matrix of ones. Ā = Z̄ Bᵀ: both rows of Ā hold the row sums of B, (0.5 − 0.2, 0.8 + 1.1, −0.4 + 0.3) = (0.3, 1.9, −0.1). B̄ = Aᵀ Z̄: both columns of B̄ hold the column sums of A, (0.1 + 0.3, −0.5 − 0.8, 1.2 + 0.7) = (0.4, −1.3, 1.9). These are the arrays of IX's `verify_matmul_backward` (§6).

---

## 5. Finite Differences as an Oracle

Before trusting a hand-written backward pass, compare it with a difference quotient. Taylor's formula gives f(x ± h) = f(x) ± h f′(x) + (h²/2) f″(x) ± (h³/6) f‴(x) + …, so the **forward difference** (f(x + h) − f(x))/h = f′(x) + (h/2) f″(x) + … has a **truncation error** of order h, while in the **central difference** (f(x + h) − f(x − h))/(2h) the even-order terms cancel and the error is (h²/6) f‴(x) + …, of order h². For f(x) = x³ at 1, the central difference is exactly 3 + h², and the forward one 3 + 3h + h².

Rounding pulls the other way. Each computed value of f carries an error of about u|f|, or more if computing f itself loses accuracy, where u = 2^-53 ≈ 1.1 · 10^-16 is the unit roundoff of MAT-003, and the quotient divides it by h. The error of the central difference is therefore about E(h) = h²|f‴|/6 + u|f|/h: it falls like h² as h shrinks, then grows like 1/h, a U-shaped curve whose minimum lies near h = (3u|f|/|f‴|)^(1/3), of the order of u^(1/3) ≈ 5 · 10^-6 for quantities of order 1, with an error of the order of u^(2/3) ≈ 10^-11. For the forward difference, the best step and the best error are both of the order of √u ≈ 10^-8. A central-difference check can thus confirm about ten digits of a gradient, no more, and it needs two evaluations per input: an oracle for tests, not a way to train.

Two cases escape this model. If f is a polynomial of degree at most 2 in the perturbed variable, then f‴ = 0 and the central difference has no truncation error at all: the check sees only rounding. And at a kink, where f has no derivative, the two methods can legitimately disagree.

### Practice Exercise

Compute the forward and central differences of f(x) = x³ at x = 1 with h = 0.1, and explain why their errors have different orders. What does the central difference give for |x| at 0?

> *Solution:* (1.331 − 1)/0.1 = 3.31, an error of 0.31 = 3h + h², of order h; (1.331 − 0.729)/0.2 = 3.01, an error of 0.01 = h², of order h². In the expansions of f(x + h) and f(x − h), the even-order terms have the same sign and cancel in the difference, leaving 2h f′(x) plus terms in h³. For |x| at 0, the central difference is (h − h)/(2h) = 0 for every h, while the one-sided differences give 1 and −1: |x| has no derivative at 0, and 0 is only one admissible choice, a convention IX also uses for the modulus of a spectrum (§6).

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX's tests.

**The tape** (`crates/ix-autograd`). Each operation pushes a [`TapeNode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L22), holding its name, the handles of its inputs and its value, onto an append-only [`Tape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L41), which a [`DiffContext`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L90) carries. The [documented operations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L6) are `add`, `sub`, `mul`, `sum`, `matmul`, `div_scalar`, `mean` and `variance`, the last two composed from the others; there is no `exp`, `log` or activation function, so apart from an FFT operation behind a feature flag, every function built from them is a polynomial in the inputs, `div_scalar` dividing only by a constant. [`backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L382) walks the tape [in reverse index order](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L391), a valid reverse topological order because an operation's inputs are always pushed before it, and [adds](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L438) each contribution to the adjoint of its input, the rule of §3. The backward pass of `matmul` computes [Z̄ Bᵀ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L249) and [Aᵀ Z̄](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L251), and `unbroadcast`, below, is the rule of §4. `variance` [squares its residual](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L365) as `mul(ctx, residual, residual)`, the same handle twice, and relies on that accumulation.

```rust
fn unbroadcast(mut grad: ArrayD<f64>, target_shape: &[usize]) -> ArrayD<f64> {
    while grad.ndim() > target_shape.len() {
        grad = grad.sum_axis(Axis(0));
    }
    for (i, &t) in target_shape.iter().enumerate() {
        if t == 1 && grad.shape()[i] != 1 {
            let summed = grad.sum_axis(Axis(i));
            grad = summed.insert_axis(Axis(i));
        }
    }
    grad
}
```

- **Shape errors panic instead of returning an error.** The comment on `add` reads [`// ndarray broadcasts automatically; errors if incompatible`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L78), but `&av + &bv` returns an array, not a `Result`, so it cannot report an error: at the version IX declares, 0.17, ndarray panics when two shapes cannot be broadcast, and `sub` and `mul` use the same operators. `matmul` [checks that both inputs have rank 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L193) but not that the inner dimensions agree, and [`dot`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L215) panics when they differ. The crate defines a [`ShapeMismatch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L83) error for such cases, and only the FFT operation [returns it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L139). A 5 × 3 matrix times a 2 × 1 matrix therefore ends in a panic, not in an `Err`.
- **A flat target changes the loss without an error.** The [schema of `ix_autograd_run`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1366) accepts each input as "1-D, 2-D, or scalar", and [`parse_array_d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4359) turns a flat list into a [one-dimensional array](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4376). [`build_graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L56) then [subtracts the target](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L73) from the prediction without checking shapes. With y as a 5 × 1 column the residual is 5 × 1; with the same five numbers as a flat y of shape 5, broadcasting makes it 5 × 5 and compares every prediction with every target. On the inputs of the MCP test, the loss becomes 0.16316 instead of 0.15116, and the gradient of w changes with it, without any error. The [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L47) passes y as a column and [checks the loss only](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L75) for being finite and non-negative, which both values are. These numbers come from a transcription, not a run; §7 checks them.
- **The execution mode changes nothing.** A `DiffContext` [stores an `ExecutionMode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L94), and [`VerifyFiniteDiff`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L41) is documented as the mode that [runs the finite-difference verifier](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L38) on every tool. No code acts on the mode, which only the `Debug` output prints: every operation pushes onto the tape in every mode, including `Eager`, documented as ["plain values, no tape"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L25), whose forward pass the tool trait says [runs "pure numeric"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tool.rs#L37). The verifier, [`verify_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L43), is a function of the test file, not of the library, and outside its own definition the only code that names `VerifyFiniteDiff` is a test [asserting its predicates](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L108). `ix_autograd_run` [always runs in `Train`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4314).
- **The finite-difference tests cannot see truncation error.** The 17 checks that run by default use ε = 10^-6, close to the best central step of §5, and an absolute tolerance of 10^-5, loosened to 10^-4 in five of them; the comments on the [variance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L628) and [mean-squared-error](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L718) tests give the depth of the chain as the reason. But every function they check, restricted to the one element perturbed, is a polynomial of degree at most 2: sums, products of two factors, a matrix product, a mean, a variance, a squared error. For such a function the central difference is exact apart from rounding, whatever the depth of the chain, so the tests measure rounding alone, about u|f|/ε ≈ 10^-10 for values of order 1, far below both tolerances. The one non-polynomial check, [`verify_rfft_magnitude_backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L887), sits behind the [`fft-autograd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L885) feature, which only one CI job [enables](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.github/workflows/ci.yml#L111).
- **A kink gets a convention.** The backward pass of `rfft_magnitude` [sets the gradient to 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L152) wherever a magnitude is below 10^-15, the choice of §5 for |x| at 0. Its comment speaks of magnitudes that are exactly zero; the threshold also zeroes the gradient of a magnitude of 10^-16, which is not.
- **Every tool ignores the upstream adjoint.** The four differentiable tools, for [linear regression](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L139), the [variance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_variance.rs#L64), the [mean](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_mean.rs#L60) and the [squared error](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/mse_loss.rs#L109), receive the upstream gradients as an unused `_out_grads` and [seed their own output with 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L144). Inside a longer reverse sweep, the rule of §3 multiplies by the incoming adjoint; these tools always return the gradient of their own output, as if it were the final loss. `ix_autograd_run` runs one tool at a time, so it is not affected today; a pipeline that chained tools would be.

The verifier compares each analytical gradient with a central difference and an absolute tolerance:

```rust
        for (flat_idx, &analytical) in grad_values.iter().enumerate().take(input.len()) {
            let f_plus = perturbed_loss(&forward, &inputs, name, flat_idx, epsilon);
            let f_minus = perturbed_loss(&forward, &inputs, name, flat_idx, -epsilon);
            let numerical = (f_plus - f_minus) / (2.0 * epsilon);
            let diff = (numerical - analytical).abs();
            if diff > tolerance {
```

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Why does a flat y of length 5 give a 5 × 5 residual in `build_graph`, and what does the loss then compute?

> *Solution:* The prediction has shape 5 × 1 and a flat y has shape 5. Broadcasting first treats y as a 1 × 5 row, then stretches both to 5 × 5, so entry (i, j) of the residual is ŷᵢ − yⱼ. The mean of its 25 squares compares every prediction with every target, not each with its own: with ŷ = (0.16, 0.58, −0.31, 0.09, 0.66) and the test's y, it is 0.16316 instead of 0.15116. Nothing fails, because the shapes are compatible; only a shape check where the data enter, or a test on the value, catches it.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process, never against a running MCP server.

1. **The worked example.** Build f(x, y) = (xy + x)² from `input`, `mul`, `add`, `mul` and `sum` on the one-element tensors x = [1] and y = [2], and call `backward` with the seed 1. Prediction: the adjoints of x and y are exactly 18 and 6.
2. **The U-shaped curve.** Build f(x) = sum(x · x · x) with two `mul` operations at x = [1]; its reverse-mode gradient is exactly 3. Compare it with central and forward differences of the tape's forward value for h = 10^-1, 10^-2, …, 10^-12. Prediction: the central error equals h² within 1 % for h from 10^-1 to 10^-3, reaches its minimum, below 10^-9, between h = 10^-7 and 10^-5, and exceeds 10^-6 at h = 10^-12; the forward error is close to 3h for large h and is smallest between h = 10^-9 and 10^-7, at a larger value than the central minimum.
3. **The quadratic blind spot.** Repeat step 2 with sum(x · x), whose gradient is 2. Prediction: no h² branch; for h from 10^-1 to 10^-6 the central error stays below 10^-10.
4. **The matrix product.** With the arrays of `verify_matmul_backward`, compute the gradient of sum(AB). Prediction: both rows of Ā equal (0.3, 1.9, −0.1) and both columns of B̄ equal (0.4, −1.3, 1.9), within 10^-15.
5. **A flat target.** Call the handler `autograd_run` with the inputs of the MCP test, once with y as a column and once flat. Prediction: the losses 0.15116 and 0.16316, within 10^-12, the second without an error and with a different gradient of w.
6. **Mismatched shapes.** Under `std::panic::catch_unwind`, call `matmul` on a 5 × 3 and a 2 × 1 matrix, and `add` on a 2 × 3 and a 2 × 2 matrix. Prediction: both calls panic, and neither returns an `Err`.
7. **The modes.** Build the linear-regression graph in each of the four modes. Prediction: the tape holds 10 nodes in every mode, and no finite-difference check runs.

### Practice Exercise

In step 2, with f(x) = x³ at 1, the error model of §5 reads E(h) = h² + u/h. Which h minimises it, and what error does it predict at the bottom of the curve?

> *Solution:* E′(h) = 2h − u/h² vanishes when h³ = u/2 = 2^-54, so h = 2^-18 ≈ 3.8 · 10^-6. There E = 2^-36 + 2^-35 = 3 · 2^-36 ≈ 4.4 · 10^-11. The grid of step 2 brackets this point with h = 10^-6 and 10^-5, which is why the prediction places the minimum between 10^-7 and 10^-5, below 10^-9: the model gives the size of the rounding error, not its exact value.

---

## 8. Common Pitfalls

- **Overwriting instead of accumulating.** A value used twice must receive the sum of its adjoints; overwriting keeps one path and silently halves the derivative of x · x.
- **Forgetting to unbroadcast.** The adjoint of a broadcast operand must be summed back to the shape of that operand.
- **Choosing the finite-difference step blindly.** Too large and truncation dominates, too small and rounding does; take about u^(1/3) for central differences and √u for forward ones, scaled by the size of x.
- **Checking only quadratic functions.** Their central differences are exact up to rounding, so the check never meets truncation error; include a cubic or a transcendental function.
- **Checking at a kink.** At the corner of |x|, of a maximum or of a modulus, the derivative does not exist, and finite differences and autodiff may legitimately differ.
- **Trusting silent broadcasting.** Compatible but unintended shapes give a wrong number instead of an error; check shapes where the data enter.
- **Dropping the upstream adjoint.** A backward pass inside a longer chain must multiply by the adjoint it receives; seeding 1 is right only for the final loss.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Gradient** | The vector of partial derivatives of a scalar function, pointing where it increases fastest |
| **Jacobian** | The matrix of partial derivatives of a vector function, the matrix of its best linear approximation |
| **Chain rule** | The Jacobian of a composition is the product of the Jacobians |
| **Evaluation trace** | The sequence of elementary operations a program performs, also called a Wengert list |
| **Tangent** | In forward mode, the derivative of an intermediate value along a chosen input direction |
| **Adjoint** | In reverse mode, the derivative of the output with respect to an intermediate value |
| **Forward mode** | Propagates tangents along with the evaluation; one sweep gives a Jacobian–vector product |
| **Reverse mode** | Walks the trace backwards; one sweep gives a vector–Jacobian product, the whole gradient of a scalar |
| **Tape** | The record of the trace and of the values that the reverse sweep needs |
| **Unbroadcasting** | Summing an adjoint over the axes that broadcasting expanded, back to the shape of the operand |
| **Central difference** | (f(x + h) − f(x − h))/(2h), with a truncation error of order h² and a rounding error of order u/h |

---

## Self-Check Assessment

**1. A loss depends on 10^6 parameters. Why is reverse mode preferred over forward mode and over finite differences to compute its gradient?**
> One reverse sweep gives all 10^6 partial derivatives for a small constant multiple of the cost of one evaluation. Forward mode needs one sweep per parameter, and central differences need 2 · 10^6 evaluations and confirm only about ten digits. The price of reverse mode is memory: the tape keeps the intermediate values.

**2. On a tape, why does x · x receive the adjoint 2x, and what would a walker that overwrote adjoints instead of adding them return?**
> Both inputs of the operation are the same node, and each receives the incoming adjoint times the other factor, x; their sum is 2x. A walker that overwrote would keep one contribution and return x, half the derivative.

**3. IX's finite-difference tests pass. What do they establish?**
> That the backward passes agree with central differences, at the chosen points and within the tolerance, for sums, products, a matrix product, means, variances and squared errors. These functions have degree at most 2 in each element, so the central difference is exact up to rounding: the tests catch a wrong derivative formula, but they never exercise truncation error, non-polynomial functions outside the gated FFT test, or shape errors.

**4. `ix_autograd_run` returns a finite, non-negative loss for your data. Can you trust it?**
> Not without checking shapes. A flat y broadcasts against the 5 × 1 prediction into a 5 × 5 residual and gives another finite, non-negative loss, 0.16316 instead of 0.15116 on the test data. Send y as an n × 1 column, and compare the shape of the returned prediction with that of y.

**Pass criteria:** Compute gradients and Jacobians and apply the chain rule, run forward and reverse mode by hand on an evaluation trace, derive the backward rules for matrix products, broadcasting and reuse, choose a finite-difference step from the balance of truncation and rounding, and trace what IX's tape, tests and MCP tool guarantee.

---

## Research Basis

- R. E. Wengert, "A simple automatic derivative evaluation program", *Communications of the ACM* 7, 1964: the evaluation trace and forward mode
- S. Linnainmaa, "Taylor expansion of the accumulated rounding error", *BIT Numerical Mathematics* 16, 1976: reverse accumulation of derivatives
- D. E. Rumelhart, G. E. Hinton and R. J. Williams, "Learning representations by back-propagating errors", *Nature* 323, 1986: backpropagation
- A. Griewank and A. Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, 2nd ed., SIAM, 2008: tapes, adjoints and the cost of a reverse sweep
- A. G. Baydin, B. A. Pearlmutter, A. A. Radul and J. M. Siskind, "Automatic differentiation in machine learning: a survey", *Journal of Machine Learning Research* 18, 2018: forward and reverse mode, and how they differ from symbolic and numerical differentiation
- P. E. Gill, W. Murray and M. H. Wright, *Practical Optimization*, Academic Press, 1981: the choice of finite-difference intervals
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
