---
module_id: mat-020-markov-chains-hmm
department: mathematics
course: Markov Chains and Hidden Markov Models
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning, mat-019-graphs-centrality-spectral]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Markov Chains and Hidden Markov Models — Where a Chain Settles, and What a Hidden One Gives Away

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Write a Markov chain as a stochastic matrix, move a distribution forward with it, and find its stationary distribution
- State when a finite chain has a unique stationary distribution and when the distribution converges to it, and recognise a periodic chain on which it does not
- Compute hitting times, return times and absorption probabilities exactly, and say what a truncated simulation estimates instead
- Evaluate and decode a hidden Markov model with the forward–backward and Viterbi algorithms, and explain when the two decodings disagree
- Derive Baum–Welch as an instance of EM, and say what it guarantees and what it does not
- Trace what IX's `MarkovChain`, `HiddenMarkovModel`, their handlers and `model_code_evolution` guarantee, and where their guides, contracts and tests promise more than the code delivers

---

## 1. Markov Chains as Matrices

A Markov chain on the states 0 to n − 1 moves at each step from state i to state j with a probability P_ij that depends only on i: the next state depends on the past only through the present, which is the **Markov property**. The matrix P is **stochastic**: its entries are nonnegative and each row sums to 1. A distribution over the states is a row vector μ, and one step maps it to μP, so after t steps μ_t = μ_0 Pᵗ; the entry (Pᵏ)_ij is the probability of being at j k steps after being at i, and Pᵏ⁺ˡ = Pᵏ Pˡ (the Chapman–Kolmogorov equation).

A **stationary distribution** is a distribution π with πP = π: a left eigenvector of P for the eigenvalue 1. The eigenvalue 1 always exists, since P𝟙 = 𝟙, and no eigenvalue is larger in modulus: for a row vector x, Σ_j |Σ_i x_i P_ij| ≤ Σ_i |x_i| Σ_j P_ij, so ‖xP‖₁ ≤ ‖x‖₁. Whether π is unique, and whether μ_t approaches it, depends on the chain (§2).

The chain with two states, P = [[1 − a, a], [b, 1 − b]] with a + b > 0, shows everything at once. Its stationary distribution is π = (b, a)/(a + b), its other eigenvalue is 1 − a − b, and μ_t − π = (μ_0 − π)(1 − a − b)ᵗ: a difference (δ, −δ) is mapped to (1 − a − b)(δ, −δ). IX's own test uses the weather chain with a = 0.3 and b = 0.4, whose stationary distribution is (4/7, 3/7), and the distance to it shrinks by the factor 0.3 at each step.

### Practice Exercise

Check that π = (b, a)/(a + b) is stationary for the chain with two states, and that it is the only stationary distribution when a + b > 0.

> *Solution:* The first entry of πP is (b(1 − a) + ab)/(a + b) = b/(a + b), and the second is (ba + a(1 − b))/(a + b) = a/(a + b). A stationary (x, 1 − x) must send as much probability from 0 to 1 as from 1 to 0 at each step: x a = (1 − x) b, so x = b/(a + b), the only solution. When a = b = 0 nothing moves, and every distribution is stationary.

---

## 2. Stationary Distributions and Convergence

A chain is **irreducible** when every state can reach every other: the directed graph with an edge i → j whenever P_ij > 0 is strongly connected. The **period** of a state i is the greatest common divisor of the k ≥ 1 with (Pᵏ)_ii > 0; all the states of an irreducible chain share it, and the chain is **aperiodic** when it is 1. Two theorems then settle the questions of §1 for a finite chain (Norris 1997):

- An irreducible chain has exactly one stationary distribution, and every entry of it is positive. This is the Perron–Frobenius theorem of MAT-019 §1, in its form for irreducible nonnegative matrices, applied to P.
- If the chain is also aperiodic, μ_0 Pᵗ → π from every start. P is then **primitive**: some power Pᵏ has all its entries positive. Wielandt (1950) showed that k = (n − 1)² + 1 always suffices, and that his matrix needs it: i → i + 1 for i < n − 1, and n − 1 → 0 or 1 with probability ½ each, whose cycles have lengths n and n − 1.

Periodicity is not a technicality. The random walk on the path 0–1–2, P = [[0, 1, 0], [½, 0, ½], [0, 1, 0]], is irreducible with period 2, and its stationary distribution is (1/4, 1/2, 1/4), the d_i/(2m) of MAT-019 §2 with degrees 1, 2, 1 and m = 2. From the uniform start, one step gives (1/6, 2/3, 1/6) and the next gives (1/3, 1/3, 1/3) again: the distribution alternates forever, and π is the average of the two. For any irreducible chain the averages (1/T) Σ_(t<T) μ_0 Pᵗ converge to π, and the ergodic theorem says more: along a single run, the fraction of the first T steps spent in state j tends to π_j with probability 1, whatever the period.

A chain satisfies **detailed balance** when π_i P_ij = π_j P_ji for all i and j; summing over i then gives πP = π, so detailed balance is a quick way to find π, and such a chain is called reversible. The random walk on an undirected graph is reversible with π_i = d_i/(2m), since both sides equal 1/(2m) on each edge.

### Practice Exercise

Find the stationary distribution of P = [[0, 1], [1, 0]], and say whether μ_0 Pᵗ converges.

> *Solution:* By §1 with a = b = 1, π = (½, ½) is the only stationary distribution. From μ_0 = (x, 1 − x), μ_t alternates between (x, 1 − x) and (1 − x, x), so it converges only when x = ½, where it is constant from the start. The chain has period 2, and the eigenvalue −1 of P keeps the difference μ_0 − π alive, with its sign flipped at every step.

---

## 3. Hitting Times and Absorbing Chains

The **hitting time** of a state j is T_j = min{t ≥ 1 : X_t = j}. Conditioning on the first step gives, for every i ≠ j, h_i = 1 + Σ_(k≠j) P_ik h_k, where h_i is the expected hitting time from i: a linear system with one unknown per state other than j, whose solution is unique and finite when j can be reached from every state. From j itself the same step gives the expected **return time** m_jj = 1 + Σ_(k≠j) P_jk h_k, and Kac's formula states that m_jj = 1/π_j for an irreducible chain (Kac 1947). Collecting all the pairs in a matrix M, with J the matrix of ones and M_dg the diagonal of M, the system reads M = J + P(M − M_dg) (Kemeny and Snell 1960). The subtraction matters: the system M = J + PM has no solution (§6).

A state j with P_jj = 1 is **absorbing**. When every state can reach an absorbing one, list the transient states first, so that P = [[Q, R], [0, I]]. The **fundamental matrix** N = (I − Q)^-1 = I + Q + Q² + … counts visits: N_ik is the expected number of visits to the transient state k from i. The expected number of steps before absorption is t = N𝟙, and the matrix of absorption probabilities is B = NR. For a fair gambler's ruin on 0 to 4, with the transient states 1, 2, 3 and steps of ±1 with probability ½,

N = [[3/2, 1, 1/2], [1, 2, 1], [1/2, 1, 3/2]], t = (3, 4, 3),

so the game lasts k(4 − k) steps on average from k, and the column of B for the state 4 is (1/4, 1/2, 3/4) = k/4.

These exact answers cost one linear solve. A simulation that runs walks from i and stops each one after L steps can only average the walks that arrived, so it estimates E[T | T ≤ L], not E[T]. For a state that leaves at each step with probability p to an absorbing state, T is geometric, and with q = 1 − p,

E[T | T ≤ L] = 1/p − L qᴸ/(1 − qᴸ).

With p = 0.1 and L = 10 this is 4.6466, against E[T] = 10, and only 1 − 0.9^10 ≈ 65% of the walks arrive. Running more walks shrinks the noise but not this bias; a simulation must report how many walks arrived, and when the chain is known, the linear system gives the exact value.

### Practice Exercise

Find the expected return time to state 0 of the weather chain of §1 by conditioning on the first step, and check Kac's formula.

> *Solution:* From state 1 the chain moves to 0 with probability 0.4 at each step, so h_1 = 1 + 0.6 h_1 and h_1 = 2.5. From 0, the next step stays at 0 with probability 0.7, which is a return after one step, or moves to 1 with probability 0.3: m_00 = 1 + 0.3 · 2.5 = 1.75 = 7/4. The stationary distribution gives π_0 = 4/7, and 1/π_0 = 7/4.

---

## 4. Hidden Markov Models: Evaluation and Decoding

In a **hidden Markov model**, a chain of states q_1, …, q_T is not observed; each state emits a symbol o_t, which is. The model has an initial distribution ν, a transition matrix A and an emission matrix B, with B_ik the probability that state i emits the symbol k. The probability of the observations and one path q is ν_(q_1) B_(q_1, o_1) Π_(t≥2) A_(q_(t−1), q_t) B_(q_t, o_t), and Rabiner (1989) lists three problems: the probability P(O) of the observations, the most likely hidden states, and the parameters that make the observations likely.

The **forward algorithm** computes P(O) without listing the nᵀ paths. With α_1(i) = ν_i B_i(o_1) and α_(t+1)(j) = (Σ_i α_t(i) A_ij) B_j(o_(t+1)), α_t(i) is the probability of the first t observations with q_t = i, and P(O) = Σ_i α_T(i), in O(T n²) operations. The backward variables β_T(i) = 1 and β_t(i) = Σ_j A_ij B_j(o_(t+1)) β_(t+1)(j) give the probability of the later observations from q_t = i, and γ_t(i) = α_t(i) β_t(i)/P(O) is the posterior probability of the state i at time t. Since α_t shrinks roughly geometrically with t, it underflows on long sequences; implementations rescale each α_t to sum to 1 with a factor c_t and add the logarithms: log P(O) = Σ_t log c_t.

**Viterbi's algorithm** replaces the sum by a maximum. In logarithms, δ_1(i) = log(ν_i B_i(o_1)) and δ_t(j) = max_i (δ_(t−1)(i) + log A_ij) + log B_j(o_t), with a pointer to the maximising i; following the pointers back from the best final state gives the most probable path as a whole (Viterbi 1967; Forney 1973). **Posterior decoding** takes instead, at each t, the state with the largest γ_t(i). It maximises the expected number of correct states, but the sequence it returns need not be a possible path.

IX's weather model has the hidden states Rainy (0) and Sunny (1), the symbols Walk, Shop and Clean, ν = (0.6, 0.4), A = [[0.7, 0.3], [0.4, 0.6]] and B = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]. For Walk, Shop, Clean, P(O) = 8403/250000 = 0.033612; the most probable path is Sunny, Rainy, Rainy, with probability 42/3125 = 0.01344, and the posterior probability of Sunny is 0.7683, 0.3759 and 0.1360 at the three steps. Here the two decodings agree. They disagree in a model with three states and a single symbol, so that the observations carry no information: ν = (0.4, 0.3, 0.3), state 0 stays at 0, state 1 moves to 2, and state 2 stays at 2. After two steps, γ_1 = (0.4, 0.3, 0.3) and γ_2 = (0.4, 0, 0.6), so posterior decoding returns (0, 2), a path of probability 0, since 0 never moves to 2; Viterbi returns (0, 0), with probability 0.4.

### Practice Exercise

Show that Σ_i α_t(i) β_t(i) = P(O) for every t.

> *Solution:* α_t(i) is the probability of o_1, …, o_t and q_t = i, and β_t(i) is the probability of o_(t+1), …, o_T given q_t = i. Given the present state, the later observations do not depend on the earlier ones (the Markov property of the hidden chain, where each symbol depends only on its state), so the product is the probability of all the observations and q_t = i. Summing over i gives P(O).

---

## 5. Learning: Baum–Welch as EM

The **Baum–Welch algorithm** fits ν, A and B to an observed sequence (Baum et al. 1970). Its E-step computes the posteriors γ_t(i) and ξ_t(i, j) = α_t(i) A_ij B_j(o_(t+1)) β_(t+1)(j)/P(O), the probability of the move from i to j between t and t + 1. Its M-step sets ν̂_i = γ_1(i), Â_ij = Σ_(t<T) ξ_t(i, j)/Σ_(t<T) γ_t(i) and B̂_ik = Σ_(t : o_t = k) γ_t(i)/Σ_t γ_t(i): expected counts divided by expected totals. This is the EM algorithm of MAT-018 §3 with the hidden path as the missing data (Dempster, Laird and Rubin 1977), and it inherits the same guarantee and the same limits: the likelihood never decreases, but the iterates may settle on a local maximum or a saddle point instead of the global maximum.

Four consequences follow from the formulas:
- **Zeros stay zero.** A zero in A, B or ν makes every term of the corresponding expected count zero (see the exercise).
- **Symmetry is kept.** If swapping two states leaves the model unchanged, their posteriors are equal and so are their re-estimated parameters, as for the identical components of MAT-018 §3.
- **One sequence gives one start.** ν̂ = γ_1 comes from the first time step of the only sequence, so as the model sharpens it often ends up putting probability 1 on a single state.
- **States have no names.** Any relabelling of the states gives the same likelihood; the states are identifiable only up to a permutation.

Take the sequence 0, 1, 0, 1, … of length 100, two states and two symbols. The model that alternates without fail, with A = [[0, 1], [1, 0]], B the identity and ν = (1, 0), gives it probability 1, the maximum. From the fully symmetric start, ν = (½, ½), every entry of A equal to ½ and both emission rows (0.6, 0.4), one M-step gives both emission rows the frequencies (½, ½) of the data and leaves everything else at ½. Under that model every sequence of length 100 has probability 2^-100, so the log-likelihood is 100 ln ½ ≈ −69.3147, and the next M-step changes nothing: a fixed point that is not a maximum. IX's test starts slightly asymmetric instead (§6).

### Practice Exercise

Show that an M-step never turns a zero of A, B or ν into a positive value, as long as the state concerned has positive posterior mass, so that the ratio is defined.

> *Solution:* If A_ij = 0, every ξ_t(i, j) contains the factor A_ij, so each is 0, their sum is 0, and Â_ij = 0. If B_ik = 0, then α_t(i) = 0 at every t with o_t = k, so γ_t(i) = 0 there and the numerator of B̂_ik is 0. If ν_i = 0, then α_1(i) = 0 and ν̂_i = γ_1(i) = 0. A zero entered by mistake is therefore permanent, and a structural zero, a move the model must forbid, is kept.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of `crates/ix-graph/src/markov.rs`, of `crates/ix-graph/src/hmm.rs`, of the two handlers below and of `model_code_evolution`, with a replica of the `StdRng` of rand 0.9 for the simulations, checked against draws from rand itself. These numbers are predictions, and §7 proposes to check them.

**The chain and its handler.** [`MarkovChain::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L20) checks that the matrix is square and that every row sums to 1 [within 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L27); as IX's contracts [say](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L8), it does not reject negative entries. [`stationary_distribution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L56) starts from the [uniform distribution](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L58) and runs:

```rust
        for _ in 0..max_iter {
            let new_dist = dist.dot(&self.transition);
            let diff = (&new_dist - &dist).mapv(f64::abs).sum();
            dist = new_dist;
            if diff < tol {
                break;
            }
        }
```

The MCP tool `ix_markov` calls [`markov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1320), which passes its `steps` parameter as `max_iter` with a [tolerance of 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1327) and adds [`is_ergodic(100)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1328) to its reply. [`mean_first_passage`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L94) simulates walks, stops each one after `max_steps`, and ends with:

```rust
        if reached == 0 {
            f64::INFINITY
        } else {
            total_steps as f64 / reached as f64
        }
```

- **On a periodic chain, the answer depends on the parity of `steps`.** On the path 0–1–2 of §2, the iterates alternate between the uniform vector and (1/6, 2/3, 1/6), the change is 2/3 at every pass, and the loop runs to `max_iter`: `ix_markov` returns (1/6, 2/3, 1/6) for an odd `steps` and (1/3, 1/3, 1/3) for an even one, never (1/4, 1/2, 1/4), and nothing in the reply says that the loop did not converge. IX's contracts do warn that the caller [cannot tell](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L11) convergence from the cutoff; `is_ergodic` is false here, which is the only hint. On [[0, 1], [1, 0]] the function returns (½, ½) after one pass, because the uniform start is already stationary: the success says nothing about convergence. IX's guide says that this chain ["never actually converges"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L195), which is true of `state_distribution` from other starts, not of this function.
- **Negative entries pass.** The rows of [[1.1, −0.1], [0.5, 0.5]] sum to 1, and `ix_markov` returns about (1.25, −0.25) as the stationary distribution, a true solution of πP = π with a negative entry, together with `is_ergodic` false. `HiddenMarkovModel::new` [rejects negative values](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L80).
- **`is_ergodic` tests whether every entry of Pᵏ exceeds [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L144)**, and the handler always takes k = 100. An irreducible aperiodic chain can fail in two ways. Wielandt's matrix on 11 states needs (11 − 1)² + 1 = 101 steps, so P^100 still has a zero entry and the answer is false; on 10 states it needs 82, and the answer is true. The chain [[1 − ε, ε], [ε, 1 − ε]] with ε = 10^-12 mixes so slowly that the off-diagonal entries of P^100 are just under 100ε = 10^-10, and the answer is again false. A positive answer is correct, since a positive power proves the chain irreducible and aperiodic; there is no test of irreducibility or of the period.
- **`mean_first_passage` averages only the walks that arrived.** A walk that has not reached the target after `max_steps` is [dropped](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L119) without being counted, so the result estimates the E[T | T ≤ L] of §3, with L = `max_steps`. On [[0.9, 0.1], [0, 1]], from 0 to 1 with 10 000 walks and the seed 42, the transcription predicts 4.6178 with `max_steps` 10, where 6449 walks arrive, and 10.1787 with 1000, against the exact 10. IX's guide asks for ["at least 10,000 simulations"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L189), which reduces the noise and not this bias, and names the exact system "M = 1 + P * M", which has no solution (see the exercise). There is no exact hitting time, fundamental matrix or absorption probability; [`AbsorbingChain`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L149) only lists the states whose [diagonal entry is exactly 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L157).
- **`model_code_evolution` predicts a fall that its data never showed.** In `crates/ix-code`, [`model_code_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L303) bins a history of quality scores into states, counts the transitions, adds [10^-6 to every cell](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L356) before normalising, and reports as the mean time to the lowest-quality bin the value of [`mean_first_passage` with 200 walks of at most 1000 steps](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L381). A bin that was never left has no counts, so its row is uniform. For the rising history 0, 1, 2, 3 with 4 states, the top bin was never left, and the model predicts a fall to the lowest bin in about 7 steps (6.99998 exactly for this matrix, 7.53 from the simulation), for a quality that only rose. For 1, 2, …, 8, the top bin was only ever followed by itself: the exact mean time is about 1.0 × 10^6 steps, but only one of the 200 walks reaches the lowest bin within 1000 steps, and the function reports 878. Its test, [`test_markov_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L591), checks the row sums and the lengths only, and nothing else calls the function.
- **The Viterbi handler checks the model but not the symbols.** [`viterbi`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1339) builds the model with [`HiddenMarkovModel::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1353) but never compares the observations with the number of emission columns, so a symbol out of range indexes past the emission matrix, which panics in `ndarray`. The DuckDB function `ix_viterbi` [rejects it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L531) with an SQL error, as its [invariant](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L517) promises. For an impossible sequence, such as 0 then 1 under a model whose states never change and always emit their own index, every score is −∞, the [strict comparison](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L268) never fires, the path defaults to state 0 at every step, and the JSON output writes the log-probability −∞ as `null`.
- **NaN passes both constructors.** A NaN sum makes [`(row_sum - 1.0).abs() > 1e-6`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L57) false, and a NaN entry makes [`v < 0.0`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L77) false, so neither check rejects it, in `HiddenMarkovModel::new` as in `MarkovChain::new`. JSON cannot carry NaN, so only Rust callers can reach this.
- **The code, the guide and the contracts disagree about Baum–Welch.** [`baum_welch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L330) clones the model, returns the trained copy as `Result<Self, String>`, and stops when the log-likelihood changes by [less than `tol`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L353). IX's contracts say that it ["MUTATES the HMM in place and returns the final log-likelihood"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L14), without a guarantee of monotonic improvement "due to numerical underflow", and that it does [not return a Result](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L24). The scaled recursions exist to avoid underflow, and by §5 EM never lowers the likelihood, as IX's own [HMM guide](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/hidden-markov-models.md#L214) says; on the sequence of IX's test, the transcription finds every one of the 50 steps an increase.
- **Some tests would pass on wrong code.** [`test_baum_welch_improves_likelihood`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L627) asserts that the log-likelihood after training is at least the one before [minus 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L637), which a `baum_welch` returning its input unchanged would satisfy. The transcription predicts −14.6565 before and −13.0797 after 50 steps, with an initial distribution collapsed to (0, 1) within 10^-55, the single-sequence effect of §5. [`test_forward_backward_consistency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L738) announces that the forward log-probability ["should match what we compute from alpha alone"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L739), then checks only that γ lies in [0, 1] and that the log-probability is finite. [`test_baum_welch_recovers_parameters`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L687) trains on the alternating sequence of §5 from a slightly asymmetric start; the transcription predicts that it reaches the alternating model of §5, with log-likelihood 0, after 7 re-estimations. That test only [checks that the emissions specialise](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L709), which is the right check, since no true parameters generated the data.
- **The catalogue names the wrong crate.** The catalogue that `ix_explain_algorithm` sends lists the HMM as ["ix_probabilistic::HMM (viterbi)"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5844); `ix-probabilistic` holds Bloom, count-min and cuckoo filters and HyperLogLog, and the HMM lives in `ix_graph::hmm`.
- **Other gaps.** There is no exact stationary distribution from a linear solve, no test of irreducibility or of the period, no exact hitting time or absorption analysis, no Baum–Welch on several sequences, no sampling from a hidden Markov model, and no MCP operation for the forward algorithm, posterior decoding or Baum–Welch: `ix_markov` and `ix_viterbi` are the only two.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Show that the system M = J + PM named in IX's guide has no solution, and that the system of §3 gives Kac's formula.

> *Solution:* Let π be a stationary distribution. Multiplying M = J + PM on the left by π gives πM = πJ + πM, since πP = π; as the entries of π sum to 1, πJ is the row of ones, so 0 = (1, …, 1), which is impossible. The system of §3, M = J + P(M − M_dg), gives instead πM = πJ + πM − πM_dg, so πM_dg = (1, …, 1): π_j m_jj = 1 for every j, which is Kac's formula.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Parity.** Call `markov` with the path chain of §2 and `steps` 1, then 100. Prediction: (1/6, 2/3, 1/6), then (1/3, 1/3, 1/3), with `is_ergodic` false both times; the average of the two is (1/4, 1/2, 1/4).
2. **Ergodicity.** Call `is_ergodic(100)` on Wielandt's matrix with 10 and 11 states, and on the two-state chain with ε = 10^-12. Prediction: true, false, false; and true for 11 states with `is_ergodic(101)`.
3. **Truncation.** Call `mean_first_passage` on [[0.9, 0.1], [0, 1]] from 0 to 1 with 10 000 walks and the seed 42, and `max_steps` 10, then 1000; then from 0 back to 0 on the weather chain of §1, with 10 000 walks of at most 1000 steps and the seed 7. Prediction: 4.6178, 10.1787, and 1.7538 against Kac's 7/4.
4. **Code evolution.** Call `model_code_evolution` on 0, 1, 2, 3 and on 1, 2, …, 8, with 4 states. Prediction: the current state 3 both times, and a mean time to critical of 7.53, then 878.
5. **Weather.** Build IX's weather model and call `forward`, `viterbi` and `forward_backward` on Walk, Shop, Clean. Prediction: exp of the log-probability 0.033612, the path Sunny, Rainy, Rainy with log-probability ln 0.01344, and a posterior of Sunny of 0.7683, 0.3759 and 0.1360.
6. **Decoders.** Call `map_estimate` and `viterbi` on the three-state model of §4 with two observations; then call the `viterbi` handler on the observations 0, 1 of the model whose states never change, then with the symbol 2, in a child process. Prediction: (0, 2), then (0, 0) with probability 0.4; the path (0, 0) with a `null` log-probability; then a panic.
7. **Baum–Welch.** Run `baum_welch` on the alternating sequence of length 100 from the symmetric start of §5 and from the start of IX's test, with 100 steps and a tolerance of 10^-10. Prediction: every parameter ½ and the log-likelihood −69.3147 after 2 steps; the alternating model and the log-likelihood 0 after 7.

### Practice Exercise

Why is the prediction for `max_steps` 1000 in step 3 not exactly 10, and is it biased?

> *Solution:* A walk misses the target in 1000 steps with probability 0.9^1000, about 1.7 × 10^-46, so the truncation bias is negligible there. The difference is sampling noise: T has standard deviation √0.9/0.1 ≈ 9.49, so the mean of 10 000 walks has a standard error of about 0.095, and 10.1787 is about 1.9 standard errors above 10. Another seed would land elsewhere around 10, whereas with `max_steps` 10 every seed lands near 4.6466.

---

## 8. Common Pitfalls

- **Reading a power-iteration result as stationary without checking it.** Compute ‖πP − π‖₁; on a periodic chain the iterates oscillate, and averaging many consecutive iterates, or solving the linear system, gives π.
- **Trusting convergence from the uniform start.** On a chain whose stationary distribution is uniform, the first pass already stops, whatever the period.
- **Taking "every entry of P^100 above 10^-10" as ergodicity.** Irreducibility is a strong-connectivity question on the graph of positive entries, and the period is a greatest common divisor of cycle lengths; answer both directly.
- **Averaging only the walks that arrived.** Report how many arrived, or solve the linear system of §3.
- **Predicting from rows that the data never filled.** A state that was never left has no evidence for its row, and smoothing makes that row uniform; report the counts behind each row.
- **Reading a posterior decoding as a path.** Each state is the most likely at its own step, and the sequence may be impossible; use Viterbi for a path.
- **Starting Baum–Welch from a symmetric model or with zeros you did not mean.** Symmetry is a fixed point and zeros are permanent; start from several random points and keep the best likelihood.
- **Learning the initial distribution from a single sequence.** It collapses onto one state; fix it, or train on several sequences.
- **Sending `ix_viterbi` a symbol at or above the number of emission columns.** The MCP handler panics; check the symbols first, or use the DuckDB function, which returns an error.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Stochastic matrix** | A matrix with nonnegative entries whose rows each sum to 1 |
| **Stationary distribution** | A distribution π with πP = π |
| **Irreducible chain** | A chain in which every state can reach every other |
| **Period** | The greatest common divisor of the lengths of the returns of a state to itself |
| **Primitive matrix** | A nonnegative matrix with a power whose entries are all positive |
| **Detailed balance** | π_i P_ij = π_j P_ji for all i and j, which makes π stationary |
| **Hitting time** | The first time t ≥ 1 at which the chain is in a given state |
| **Fundamental matrix** | N = (I − Q)^-1 of an absorbing chain, whose entries count the expected visits |
| **Hidden Markov model** | A Markov chain of unobserved states, each of which emits an observed symbol |
| **Forward algorithm** | The recursion that computes the probability of the observations in O(T n²) operations |
| **Viterbi path** | The most probable sequence of hidden states given the observations |
| **Baum–Welch algorithm** | The EM algorithm for the parameters of a hidden Markov model |

---

## Self-Check Assessment

**1. `ix_markov` returns (1/6, 2/3, 1/6) as the stationary distribution of a chain, with `is_ergodic` false. What do you conclude, and how do you get π?**
> Check πP = π first: here the result maps to (1/3, 1/3, 1/3), so it is not stationary. The chain is the periodic path of §2, the loop ran to `steps` without converging, and with an even `steps` the answer would have been uniform. Average two consecutive iterates, or solve π(P − I) = 0 with the entries of π summing to 1: (1/4, 1/2, 1/4).

**2. A report says, from `model_code_evolution`, that a crate will reach critical quality in 878 commits on average. What do you ask before believing it?**
> How many of the 200 walks reached the lowest bin: the value averages only those, and on the rising history of §6 only one of them did, while the exact mean for that matrix is about 10^6. Then which rows of the matrix rest on data: a bin that was never left gets a uniform row, which alone can create a path to the lowest bin. Finally, whether a chain with a few binned states fits the history at all.

**3. Viterbi and posterior decoding disagree on a sequence. Which one do you report?**
> It depends on the question. For the most probable sequence of states as a whole, for instance to segment a signal, report the Viterbi path; to get as many states right as possible, report the posterior decoding, with its probabilities, and say that its sequence may be impossible, as (0, 2) is in the model of §4.

**4. Baum–Welch stops after two steps with every parameter equal to ½. Is the implementation broken?**
> Not necessarily. A start in which swapping the states leaves the model unchanged stays symmetric under EM (§5), and on the alternating sequence it reaches a fixed point with log-likelihood 100 ln ½, far below the maximum 0. Break the symmetry, run several random starts and keep the best likelihood, and check the answer against the data.

**Pass criteria:** Write a chain as a stochastic matrix and find its stationary distribution; state when it is unique and when the distribution converges to it; compute hitting times, return times and absorption probabilities, and say what a truncated simulation estimates; evaluate and decode a hidden Markov model and explain when the decodings disagree; derive Baum–Welch as EM and state its guarantee and its limits; and trace where IX's guides, contracts, handlers and tests promise more than the code delivers.

---

## Research Basis

- A. A. Markov, "Extension of the law of large numbers to dependent quantities" (in Russian), *Izvestiya of the Physico-Mathematical Society at Kazan University* 15, 1906: the first chains
- M. Kac, "On the notion of recurrence in discrete stochastic processes", *Bulletin of the American Mathematical Society* 53, 1947: the mean return time
- H. Wielandt, "Unzerlegbare, nicht negative Matrizen", *Mathematische Zeitschrift* 52, 1950: the exponent of a primitive matrix
- J. G. Kemeny and J. L. Snell, *Finite Markov Chains*, Van Nostrand, 1960: the fundamental matrix and mean first passage times
- A. J. Viterbi, "Error bounds for convolutional codes and an asymptotically optimum decoding algorithm", *IEEE Transactions on Information Theory* 13, 1967: the Viterbi algorithm
- L. E. Baum, T. Petrie, G. Soules and N. Weiss, "A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains", *Annals of Mathematical Statistics* 41, 1970: the Baum–Welch algorithm and its monotonicity
- G. D. Forney, "The Viterbi algorithm", *Proceedings of the IEEE* 61, 1973: the algorithm as a shortest path
- A. P. Dempster, N. M. Laird and D. B. Rubin, "Maximum likelihood from incomplete data via the EM algorithm", *Journal of the Royal Statistical Society, Series B* 39, 1977: EM
- L. R. Rabiner, "A tutorial on hidden Markov models and selected applications in speech recognition", *Proceedings of the IEEE* 77, 1989: the three problems, scaling and posterior decoding
- J. R. Norris, *Markov Chains*, Cambridge University Press, 1997: irreducibility, periodicity, convergence and the ergodic theorem
- O. Cappé, E. Moulines and T. Rydén, *Inference in Hidden Markov Models*, Springer, 2005: smoothing, decoding and identifiability
- D. A. Levin, Y. Peres and E. L. Wilmer, *Markov Chains and Mixing Times*, American Mathematical Society, 2009: convergence rates
- R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013: primitive matrices and Wielandt's bound
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
