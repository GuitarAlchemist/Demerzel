---
module_id: mat-025-allocation-games-bandits-penalties
department: mathematics
course: Allocation Under Constraints, Games, Bandits and Penalties
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-012-iterative-optimisation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Allocation Under Constraints, Games, Bandits and Penalties — What a Multiplier, an Equilibrium and a Regret Bound Can Promise

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Write the KKT conditions of a constrained allocation, solve a small one, and read each multiplier as a shadow price
- State linear-programming duality and complementary slackness, and solve a two-variable program and its dual by hand
- Find the Nash equilibria of a small bimatrix game by support enumeration, and say what fictitious play does and does not guarantee
- Compute the Shapley value of a cooperative game, test an allocation against the core, and explain why the two can disagree
- Define regret, compare ε-greedy with UCB1, and say what UCB1's bound assumes about the scale of the rewards
- Turn a constraint into a penalty for a search that only knows box bounds, and say when the penalty is exact
- Trace what IX's `ix-game`, `ix-rl` and `ix-evolution` crates compute, which of their outputs a test pins down, and what they leave out

---

## 1. Lagrange Multipliers and the KKT Conditions

An allocation chooses x to maximise a return f(x) under constraints g_i(x) ≤ c_i. When f is concave, each g_i is convex and some point satisfies every constraint strictly (**Slater's condition**), x* is optimal exactly when there are multipliers λ_i with:

```
∇f(x*) = Σ_i λ_i ∇g_i(x*)
g_i(x*) ≤ c_i
λ_i ≥ 0
λ_i (c_i − g_i(x*)) = 0
```

These are the **Karush–Kuhn–Tucker conditions** (Karush, 1939; Kuhn and Tucker, 1951): stationarity, primal feasibility, dual feasibility and complementary slackness. Complementary slackness says that a constraint with slack has a zero multiplier. A multiplier is also a price: if V(c) is the optimal value as a function of the limits, then under the same assumptions ∂V/∂c_i = λ_i wherever V is differentiable. λ_i is the **shadow price** of resource i, what one more unit of it is worth at the margin.

Split a budget of 10 between two activities that return ln(1 + x) and 2 ln(1 + y): maximise ln(1 + x) + 2 ln(1 + y) subject to x + y ≤ 10, with x, y ≥ 0. Stationarity gives 1/(1 + x) = λ and 2/(1 + y) = λ, so 1 + y = 2(1 + x). With the budget spent, x = 3, y = 7 and λ = 1/4, and the value is ln 4 + 2 ln 8 = 8 ln 2 ≈ 5.545177. A budget of 11 gives x = 10/3 and y = 23/3, and a value higher by about 0.240128, close to λ = 0.25: the multiplier predicts the first-order gain, and concavity makes the true gain a little smaller.

Now cap the second activity at y ≤ 5. The old solution violates the cap, so the cap binds: y = 5 and x = 5. Stationarity reads 1/6 = λ for x and 2/6 = λ + μ for y, where μ is the cap's multiplier, so λ = μ = 1/6. Both are nonnegative, so this is a KKT point, and since the problem is concave it is the optimum. The value drops to 3 ln 6 ≈ 5.375278.

### Practice Exercise

With the cap y ≤ 5 in place, raise it to 6 and keep the budget at 10. What does μ predict, and what is the actual gain?

> *Solution:* μ = 1/6 predicts a gain of about 0.166667. The new optimum is x = 4, y = 6, still on both constraints, since 1/5 = λ and 2/7 = λ + μ give λ = 1/5 and μ = 3/35, both positive. Its value is ln 5 + 2 ln 7 ≈ 5.501258, a gain of 0.125980: the first-order estimate overshoots, as it must for a concave return.

---

## 2. Linear Programming and Duality

When the return and the constraints are linear, the problem is a **linear program** (P), and it has a **dual** (D):

```
(P)  max { cᵀx : A x ≤ b, x ≥ 0 }
(D)  min { bᵀu : Aᵀu ≥ c, u ≥ 0 }
```

Every feasible u bounds the primal from above, since cᵀx ≤ (Aᵀu)ᵀx = uᵀAx ≤ uᵀb: this is **weak duality**. If either problem has an optimum, both do, with equal values: this is **strong duality**. At the optimum, each primal constraint and its dual variable satisfy complementary slackness, and the dual variables are the shadow prices of §1. The simplex method (Dantzig) walks from vertex to vertex of the feasible polygon, since a linear objective that has a maximum on it attains it at a vertex.

Two products earn 2 and 3 per unit. Machine A has 4 hours (x + y ≤ 4) and machine B has 6 hours (x + 3y ≤ 6). The vertices (0, 0), (4, 0), (0, 2) and (3, 1) earn 0, 8, 6 and 9, so the optimum is (3, 1) with 9. The dual minimises 4u + 6v subject to u + v ≥ 2 and u + 3v ≥ 3. Both primal variables are positive, so both dual constraints are tight: u = 3/2 and v = 1/2, with value 4 × 3/2 + 6 × 1/2 = 9. One more hour on machine A moves the optimum to (4.5, 0.5), which earns 10.5 = 9 + u.

Zero-sum games are linear programs. If A pays the row player, von Neumann's minimax theorem (1928) says that max_p min_q pᵀAq = min_q max_p pᵀAq. This common **value** is what the row player can guarantee, and an optimal p solves: maximise v subject to Aᵀp ≥ v·1, Σ p_i = 1, p ≥ 0. In rock–paper–scissors the value is 0, and the only optimal strategy is (1/3, 1/3, 1/3) for each player.

### Practice Exercise

Machine B's capacity rises from 6 to 7. Predict the new optimum from the dual, then check it.

> *Solution:* v = 1/2 predicts 9.5. The binding constraints are now x + y = 4 and x + 3y = 7, so y = 1.5 and x = 2.5, which earn 2 × 2.5 + 3 × 1.5 = 9.5. The other vertices, (4, 0) and (0, 7/3), earn 8 and 7, so the prediction holds. The optimum has moved, but the same two constraints bind; the prediction would fail only once another pair became binding, here once B's capacity left the range from 4 to 12.

---

## 3. Nash Equilibria and Support Enumeration

In a bimatrix game, player A chooses a row i and player B a column j; A receives a_ij and B receives b_ij. Mixed strategies p and q are probability vectors, and A's expected payoff is pᵀAq. A pair (p, q) is a **Nash equilibrium** when neither player gains by deviating alone. Since a payoff is linear in one's own strategy, it is enough to check the deviations to pure strategies. Nash (1950) proved that every finite game has an equilibrium, possibly mixed.

In equilibrium, every pure strategy a player uses earns the same expected payoff against the other's mix, and no unused one earns more: this is the **indifference principle**. **Support enumeration** guesses which strategies each player uses (the supports), solves the linear indifference equations, and keeps the solutions that are probability vectors and that no unused strategy beats. An m × n game has (2^m − 1)(2^n − 1) pairs of supports. In a nondegenerate game only supports of equal size can carry an equilibrium, and the number of equilibria is odd, as the Lemke–Howson algorithm shows (1964).

- **Prisoner's dilemma**, A = [[3, 0], [5, 1]] and B = Aᵀ. Defecting strictly dominates cooperating for both players. So (Defect, Defect), worth 1 each, is the only equilibrium, though cooperating would give each player 3.
- **Matching pennies**, A = [[1, −1], [−1, 1]] and B = −A. There is no pure equilibrium; indifference gives p = q = (1/2, 1/2).
- **Battle of the sexes**, A = [[3, 0], [0, 2]] and B = [[2, 0], [0, 3]]. There are two pure equilibria, paying (3, 2) and (2, 3), and a mixed one. B must make A indifferent, 3q = 2(1 − q), so q = 2/5. A must make B indifferent, 2p = 3(1 − p), so p = 3/5. Each player then expects 6/5, less than in either pure equilibrium.
- **Rock–paper–scissors.** The only equilibrium uses all three strategies, at (1/3, 1/3, 1/3); no support of size 1 or 2 carries one.

**Fictitious play** (Brown, 1951) is a learning rule: each round, each player best-responds to the empirical frequencies of the other's past play. Robinson (1951) proved that in zero-sum games every limit point of these frequencies is an equilibrium strategy, so they converge when the equilibrium is unique. Shapley (1964) showed that they need not in general. In a 3 × 3 game of the kind he used, with A the identity matrix and B = [[0, 1, 0], [0, 0, 1], [1, 0, 0]], the only equilibrium is uniform. The play nevertheless cycles through six pure profiles in runs whose lengths grow geometrically (§7), and the frequencies never settle.

### Practice Exercise

Find all equilibria of A = [[2, 0], [0, 1]], B = [[1, 0], [0, 2]], and each player's expected payoff in the mixed one.

> *Solution:* The two pure equilibria are (row 1, column 1) and (row 2, column 2). For the mixed one, B's mix makes A indifferent: 2q = 1 − q, so q = 1/3. A's mix makes B indifferent: p = 2(1 − p), so p = 2/3. A expects 2q = 2/3 and B expects p = 2/3. Three equilibria, an odd number, as for every nondegenerate game.

---

## 4. The Shapley Value and the Core

A cooperative game gives each coalition S of the n players a value v(S), with v(∅) = 0, and an allocation x divides v(N), the value of the grand coalition. Shapley (1953) showed that exactly one rule satisfies four axioms. Efficiency: the shares add up to v(N). Symmetry: interchangeable players get the same. Null player: a player who adds nothing gets nothing. Additivity: the shares of a sum of games are the sums of the shares. That rule is the **Shapley value**:

```
φ_i = Σ_{S ⊆ N∖{i}}  |S|! (n − |S| − 1)! / n!  ·  [v(S ∪ {i}) − v(S)]
```

that is, i's marginal contribution averaged over the n! orders in which the players can arrive. The **core** asks for stability instead of fairness (Gillies, 1959): x is in the core if it is efficient and no coalition can do better on its own, Σ_{i∈S} x_i ≥ v(S) for every S. The core can be empty. When it is not, it need not contain the Shapley value; for a convex game it does (Shapley, 1971).

In the **glove game**, players 1 and 2 each hold a left glove, player 3 a right glove, and a pair is worth 1. Player 3 adds 1 in every order except the two where it arrives first, so φ_3 = 4/6 = 2/3. Player 1 adds 1 only in the order (3, 1, 2), so φ_1 = φ_2 = 1/6. The core needs x_1 + x_3 ≥ 1, x_2 + x_3 ≥ 1 and every x_i ≥ 0, with x_1 + x_2 + x_3 = 1, which forces x_1 = x_2 = 0: the core is the single point (0, 0, 1). The Shapley value pays each left glove 1/6; the core pays them nothing, because two left gloves compete for one right glove. In the **majority game**, where any two of three players can split 1, the core is empty: the three pair constraints add up to 2(x_1 + x_2 + x_3) ≥ 3, while the shares must add up to 1. The Shapley value is 1/3 each.

The **Banzhaf index** (Banzhaf, 1965) counts, for each player, the coalitions that it turns from losing into winning, instead of averaging over orders. In a weighted vote with weights 3, 3, 3, 1 and 1 and a quota of 10, a winning coalition needs the three large members and one small one. The Shapley value is (0.3, 0.3, 0.3, 0.05, 0.05), and the normalised Banzhaf index is (3/11, 3/11, 3/11, 1/11, 1/11).

### Practice Exercise

Two players, with v({1}) = v({2}) = 0 and v({1, 2}) = 1. Give the Shapley value and the core.

> *Solution:* The Shapley value is 1/2 each, by symmetry and efficiency. The core is every (x, 1 − x) with 0 ≤ x ≤ 1, since each player alone can guarantee only 0. The Shapley value is its midpoint.

---

## 5. Bandits and Regret

A K-armed bandit has K reward distributions with unknown means μ_1, …, μ_K. Each round, the learner pulls one arm and observes only that arm's reward. The **regret** after T rounds is the expected shortfall against always pulling the best arm: R_T = T μ* − E[Σ_t r_t] = Σ_i Δ_i E[N_i(T)], where Δ_i = μ* − μ_i and N_i(T) counts the pulls of arm i. Lai and Robbins (1985) showed that a learner that does well on every bandit must pull each worse arm on the order of ln T times, so regret grows at least logarithmically.

**ε-greedy** pulls a uniformly random arm with probability ε and otherwise the arm with the best average. Its exploration never stops. Once its averages rank the arms correctly, each round costs ε times the mean gap of a uniform pull. With means 1, 2 and 3 and ε = 0.1, that is 0.1 × (2 + 1 + 0)/3 = 0.1 per round, a regret that grows linearly in T. **UCB1** (Auer, Cesa-Bianchi and Fischer, 2002) pulls each arm once, then the arm with the largest q_i + √(2 ln t / n_i), where q_i is the arm's average, n_i its number of pulls, and t the total. For rewards in [0, 1] it pulls a worse arm at most 8 ln T / Δ_i² + 1 + π²/3 times in expectation, a logarithmic regret. **Thompson sampling** (Thompson, 1933) draws a mean for each arm from its posterior and pulls the arm with the best draw.

The bound assumes rewards in [0, 1]. The bonus √(2 ln t / n_i) has no unit, while q_i has the unit of the reward, so multiplying every reward by c changes UCB1's choices unless the bonus is multiplied by c too. Two arms that always pay 0.5 and 0.4 show it with no randomness at all. After 10,000 rounds UCB1 has pulled the worse arm 877 times. If they pay 50 and 40, it pulls the worse arm once, in the warm-up, and not again in the 10,000 rounds. If they pay 0.005 and 0.004, it pulls the worse arm 4,918 times, close to half. A large scale is not safe either. Let the better arm's first payment be unlucky, 30 instead of 50, and every later one 50. UCB1 then does not return to it in the whole run: one pull, then 9,999 of the worse arm, a regret of 10 per round. The bonus √(2 ln t) grows without bound, so UCB1 would come back to it eventually, but to bridge a gap of 10 it needs ln t near 50.

### Practice Exercise

For two arms with rewards in [0, 1] and Δ = 0.1, how many pulls of the worse arm does UCB1's bound allow after T = 10,000 rounds? Compare with the 877 of the deterministic arms.

> *Solution:* 8 ln(10,000)/0.01 + 1 + π²/3 ≈ 7,372.6. The bound holds for every distribution in [0, 1], including the worst ones, so on this easy, noiseless pair it is loose by a factor of about 8.

---

## 6. Penalties: Constraints for a Search That Knows Only Boxes

A search that only knows box bounds l ≤ x ≤ u, as many evolutionary algorithms do, can still respect other constraints if they are moved into the objective. For an equality constraint h(x) = 0, the **quadratic penalty** minimises f(x) + (ρ/2) h(x)²; for g(x) ≤ 0 it uses max(0, g(x))². As ρ grows, its minimisers approach the constrained one, and ρ h(x_ρ) approaches the multiplier up to sign. For every finite ρ, though, they violate the constraint whenever its multiplier is nonzero. The **ℓ1 penalty** f(x) + ρ |h(x)| is **exact**: once ρ exceeds the modulus of the multiplier, the constrained minimiser is a local minimiser of the penalised function, and for a convex problem such as those here, its global minimiser (Nocedal and Wright, ch. 17). The price is a kink at the solution, where gradient methods struggle.

Minimise x² + y² subject to x + y = 2. The solution is x = y = 1, with multiplier λ* = 2, since stationarity reads 2x = λ. With the quadratic penalty, symmetry gives x = y = t with 2t + ρ(2t − 2) = 0, so t = ρ/(1 + ρ). ρ = 10 gives t ≈ 0.909091 and a violation of 2/11 ≈ 0.181818. ρ = 100 gives 0.990099 and 0.019802. The estimate ρ(2 − 2t) = 2ρ/(1 + ρ), that is 1.818182 and then 1.980198, approaches λ* = 2. With the ℓ1 penalty, minimise 2t² + ρ|2t − 2|. Below t = 1 the derivative is 4t − 2ρ, so the minimiser is t = min(ρ/2, 1). It is exact from ρ = 2 = λ* on, and infeasible below.

Clamping each coordinate into its interval, as a box-bounded search does, is not a penalty but a projection. It handles a box exactly, and nothing else.

### Practice Exercise

The budget problem of §1, written for a minimiser that only knows the box [0, 10]², becomes: minimise −ln(1 + x) − 2 ln(1 + y) + ρ max(0, x + y − 10). Which weights ρ make this ℓ1 penalty exact?

> *Solution:* Every ρ ≥ λ* = 1/4. At ρ = 1/4 itself, the penalty's slope cancels the objective's gradient (−1/4, −1/4) at (3, 7), and the penalised function is strictly convex, so (3, 7) is still its only minimiser. Below 1/4, one more unit of budget beyond 10 earns more, at the margin 1/(1 + x) = 1/4, than the penalty costs, so the minimiser overspends.

---

## 7. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of `nash.rs` and `cooperative.rs` in `crates/ix-game` and of `UCB1` and the greedy choice of `EpsilonGreedy` in `crates/ix-rl`. None of these draws a random number. The transcription reproduces the assertions of the deterministic tests this section cites. It does not reproduce runs that draw from IX's seeded `StdRng`, whose stream MAT-009 §6 explains is not a portable specification; for those, §8 states only qualitative predictions.

**Support enumeration: two kinds of support out of many.** [`support_enumeration`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L152) loops over every pair of supports, but [`solve_support`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L177) solves only two kinds: a pair of pure strategies, and the full support of a 2 × 2 game.

```rust
        // For 2x2 mixed strategy: solve indifference conditions
        if m == 2 && n == 2 && support_a.len() == 2 && support_b.len() == 2 {
            return self.solve_2x2_mixed();
        }

        None // General case would need linear programming
```

The module's documentation announces [Lemke–Howson](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L3), which the file does not contain, and the workspace has no linear-programming solver. On the 2 × 2 games of §3 the transcription finds every equilibrium: 1 for matching pennies, whose [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L365) checks only that an equilibrium near (1/2, 1/2) is among those found, not how many there are, and 3 for the battle of the sexes, whose test asserts only [at least 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L398). Rock–paper–scissors and Shapley's game are 3 × 3 and have only a mixed equilibrium, so the function returns an empty list. The MCP tool [`ix_game_nash`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1406) then answers `count: 0` for games that, by Nash's theorem, have an equilibrium, and nothing in the answer says that the search was partial. IX's guide states the limit plainly in its [second pitfall](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L175), yet its [fourth](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L179) says that support enumeration finds them all.

**Fictitious play: a phantom first move, and ties to the last strategy.** [`fictitious_play`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L247) starts each count [with one play of strategy 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L253). Among tied best responses it takes the last one, because Rust's `max_by` [returns the last of equal maxima](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L262). Its test runs the prisoner's dilemma for 1,000 rounds and asserts a Defect frequency [above 0.9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L413); the transcription defects in every round, so the only Cooperate in 1,001 counts is the phantom one. On matching pennies both players' frequencies after 100, 1,000, 10,000 and 100,000 rounds are within 0.054455, 0.016484, 0.006649 and 0.001605 of 1/2, as Robinson's theorem predicts. On Shapley's game they never settle. The runs of identical profiles have lengths 1, 2, 3, 6, 9, 13, 20, 30, 44, 65 and so on, and the ratio of each to the one before tends to about 1.466. After 100,000 rounds A's frequencies are (0.3822, 0.4399, 0.1779), far from (1/3, 1/3, 1/3). The function returns the frequencies without saying whether they converged, though its documentation warns that it [may not converge for all games](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L246). IX's guide says that fictitious play is [guaranteed to converge](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L177) for zero-sum games and for games with a unique equilibrium. Shapley's game, which the same pitfall cites next, has a unique equilibrium and cycles.

**Shapley value: exact, exponential, and outside the core.** [`shapley_value`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L53) sums the formula of §4 over the 2^(n−1) coalitions without each player, with factorials in [`u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L168). The [glove-game test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L194) asserts only that the right glove gets [more than a left glove](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L206) and that the shares add up to 1. The transcription gives (1/6, 1/6, 2/3), which [`is_in_core`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L82) rejects, while it accepts (0, 0, 1). For the core test's game, with 7, 5 and 3 for the pairs and 10 for all three, the Shapley value (13/3, 10/3, 7/3) is in the core. The module's documentation lists the [nucleolus](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L1), which the file does not implement. The crate's contracts say not to call the function [beyond about 20 players](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L39), because of a coalition-value cache that the function does not allocate. The limit is real for another reason: 21! is about 2.77 times 2^64, so from 21 players on the factorial of n overflows `u64`. Rust's `product` then panics when overflow checks are on, as in a debug build, and wraps modulo 2^64 otherwise.

**Bandits: ties to the last arm, and a bonus without a unit.** [`EpsilonGreedy::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L26) picks the best average [with `max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L33), so its first greedy pick, with every average at 0, is the last arm; the crate's contracts promise [the first](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L8). The same holds for the greedy action of [Q-learning](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/q_learning.rs#L55), whose contract also promises [the lowest index](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L14). It holds for [`first_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L29) too, which its contract says [breaks ties for the first bidder](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L12). [`second_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L46) sorts stably and does give a tie to the first bidder. In the ε-greedy test the best arm is [the last one](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L143), the one the tie-break favours. [`UCB1::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L62) adds the bonus of §5 with no scale parameter:

```rust
    pub fn select_arm(&self) -> usize {
        // Play each arm at least once
        for (i, &c) in self.counts.iter().enumerate() {
            if c == 0 {
                return i;
            }
        }

        let total = self.total_count as f64;
        self.q_values
            .iter()
            .enumerate()
            .map(|(i, &q)| {
                let bonus = (2.0 * total.ln() / self.counts[i] as f64).sqrt();
                (i, q + bonus)
            })
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
            .unwrap()
            .0
    }
```

§5's deterministic arms are runs of a transcription of this function. Its test checks only that [each of 5 arms is played once first](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L164), and no test measures regret. [Thompson sampling](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L91) sets each arm's variance to [1/n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L131). That is the posterior variance of the mean for rewards of variance 1 under a flat prior, and the contracts call it [a simplification](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L13). The MCP tool [`ix_bandit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2333) draws rewards with [standard deviation 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2355) from a generator [seeded with 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2342), and reports pulls and total reward, not regret.

**Evolution: boxes only.** The genetic algorithm and differential evolution take one interval for all coordinates ([`with_bounds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L57)) and [clamp](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L120) each child into it. There is no other constraint and no penalty helper, so §6's penalties are the caller's to write. The genetic algorithm's `mutation_rate` is not a rate. It is the [standard deviation of a Gaussian step](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L56), and each gene takes that step [with probability 0.3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L58). Differential evolution's [`pick_three`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L132) draws three distinct indices other than the current one, and [retries until it has them](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L134). With one, two or three individuals it never returns. The MCP tool `ix_evolution` passes the caller's [`population_size`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2417) on without a check.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

`ix_game_nash` answers `count: 0` for rock–paper–scissors. What is the equilibrium, and how could you approach it with IX as it stands?

> *Solution:* (1/3, 1/3, 1/3) for each player, the minimax strategy of §2. IX cannot solve for it, but the game is zero-sum, so `fictitious_play` approaches it: after 100,000 rounds every frequency is within 0.001077 of 1/3. `is_nash_equilibrium` confirms the uniform profile itself, with no deviation gaining anything.

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Support enumeration.** Run `support_enumeration` on matching pennies, the battle of the sexes, rock–paper–scissors and Shapley's game. Prediction: 1, 3, 0 and 0 equilibria; for the battle of the sexes, the mixed one at (0.6, 0.4) and (0.4, 0.6).
2. **Fictitious play.** Run `fictitious_play` on matching pennies and on Shapley's game for 100, 1,000, 10,000 and 100,000 rounds. Prediction: on matching pennies, A's frequency of the first strategy 0.554455, 0.483516, 0.499550 and 0.500625; on Shapley's game, A's frequencies after 100,000 rounds (0.3822, 0.4399, 0.1779).
3. **Shapley value and core.** Run `shapley_value` and `is_in_core` on the glove game and on the core test's game, and `shapley_value` and `banzhaf_index` on the weighted vote of §4. Prediction: the values of §4 and §7, (1/6, 1/6, 2/3) rejected and (0, 0, 1) accepted, (13/3, 10/3, 7/3) accepted.
4. **Ties.** Call `select_arm` on a new `EpsilonGreedy` with three arms and ε = 0, and run both auctions on two equal bids. Prediction: arm 2; the first-price auction goes to the second bidder, the second-price auction to the first.
5. **UCB1 and the reward's unit.** Run `UCB1` for 10,000 rounds on the deterministic arms of §5, at the three scales and with the unlucky first payment. Prediction: 877, 1 and 4,918 pulls of the worse arm; with the unlucky first payment at scale 100, 1 pull of the better arm.
6. **Regret on noisy arms.** Run `EpsilonGreedy` with ε = 0.1 and `UCB1` on three arms with means 1, 2 and 3 and Gaussian noise of standard deviation 1, as `ix_bandit` does, for 1,000, 10,000 and 100,000 rounds over 20 seeds, and compute the regret from the pulls. Prediction, qualitative only, since this lesson does not reproduce IX's generator: ε-greedy's regret per round stays near 0.1, while UCB1's falls as T grows.
7. **Differential evolution with three individuals.** Run `DifferentialEvolution` with a population of 4, then of 3, in a separate thread, waiting at most 10 seconds for its result. Prediction: the first returns, the second does not.

### Practice Exercise

Step 6 compares regret on one fixed noise model. How would you make the comparison fair between the two algorithms?

> *Solution:* Draw the rewards in advance, one stream per arm, so that the k-th pull of an arm returns the same reward whichever algorithm pulls it. Compute the regret from the pulls and the true means, not from the rewards received, and report its spread over the seeds, not one run.

---

## 9. Common Pitfalls

- **Reading an empty list of equilibria as "no equilibrium".** Every finite game has one; an empty list from a partial enumeration says only that the search did not find it.
- **Trusting fictitious play to converge.** In zero-sum games its frequencies approach equilibrium strategies; in general they need not, even with a unique equilibrium. Check the frequencies against the best responses.
- **Taking the Shapley value for a stable allocation.** Fairness and stability are different axioms; test the core separately.
- **Using a multiplier far from the margin.** It is a derivative; a large change in a resource needs the problem solved again.
- **Treating a quadratic penalty's answer as feasible.** Unless the multiplier is zero, it violates the constraint for every finite weight; an ℓ1 penalty with a weight above the multiplier does not.
- **Calling a clamp a constraint handler.** It handles a box, and nothing else.
- **Comparing bandit algorithms by total reward on one seed.** Regret against the best arm is the measure, and one seed is one sample.
- **Feeding UCB1 rewards outside [0, 1].** Rescale the rewards, or the bonus, to the range of the reward.
- **Assuming that a tie goes to the first index.** Rust's `max_by` returns the last of equal maxima and `min_by` the first; a stable sort keeps the input order.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **KKT conditions** | Stationarity, feasibility, nonnegative multipliers and complementary slackness; necessary and sufficient for a concave problem under Slater's condition |
| **Shadow price** | The multiplier of a constraint: the marginal value of one more unit of its resource |
| **Linear-programming duality** | The dual bounds the primal, and at an optimum both have the same value |
| **Nash equilibrium** | A profile of strategies from which no player gains by deviating alone |
| **Support enumeration** | Guessing the strategies each player uses and solving the indifference equations |
| **Fictitious play** | Each player best-responds to the empirical frequencies of the other's past play |
| **Shapley value** | The average marginal contribution over all orders of arrival; the unique rule with efficiency, symmetry, null player and additivity |
| **Core** | The efficient allocations that no coalition can improve on by itself |
| **Regret** | The expected shortfall against always pulling the best arm |
| **UCB1** | Pull the arm with the largest average plus √(2 ln t / n_i), after one pull of each |
| **Quadratic penalty** | f + (ρ/2) h²: infeasible for every finite ρ when the multiplier is nonzero, with ρ h approaching the multiplier |
| **Exact penalty** | f + ρ \|h\|: exact once ρ exceeds the modulus of the multiplier |

---

## Self-Check Assessment

**1. `support_enumeration` returns an empty list for a 3 × 3 game. What do you know?**
> Nothing about existence: by Nash's theorem the game has an equilibrium. IX solves only pure supports and the full support of a 2 × 2 game, so an equilibrium that mixes in a 3 × 3 game is out of its reach. Rock–paper–scissors is an example, with its only equilibrium at (1/3, 1/3, 1/3).

**2. In the glove game, why is the Shapley value not in the core?**
> Both are efficient, but the core also requires every coalition to get at least its value. The Shapley value gives players 1 and 3 together 1/6 + 2/3 = 5/6, less than the 1 they can make alone. The only allocation that satisfies every coalition is (0, 0, 1).

**3. A service feeds UCB1 rewards measured in milliseconds saved, in the hundreds. What goes wrong?**
> The bonus √(2 ln t / n_i) stays of order 1 while the averages differ by tens. After the warm-up UCB1 is all but greedy: one unlucky first latency can shut out the better arm for any practical number of rounds, because the bonus grows only like √(ln t). Rescale the rewards to [0, 1], or scale the bonus by the range.

**4. A genetic algorithm with box bounds must respect x + y ≤ 10. What can you do?**
> Add a penalty to the objective. The ℓ1 penalty ρ max(0, x + y − 10) is exact once ρ exceeds the constraint's multiplier. A quadratic penalty is only approximately feasible. Clamping handles the box and does nothing for the sum.

**Pass criteria:** Write and solve the KKT conditions of a small allocation and read its multipliers as prices; solve a two-variable linear program and its dual; find the equilibria of a small bimatrix game and say when fictitious play converges; compute a Shapley value and test the core; define regret and say what UCB1's bound assumes; choose an exact penalty weight; and say which of IX's outputs its tests pin down.

---

## Research Basis

- W. Karush, *Minima of Functions of Several Variables with Inequalities as Side Constraints*, M.Sc. thesis, University of Chicago, 1939, and H. W. Kuhn and A. W. Tucker, "Nonlinear programming", *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*, 1951: the KKT conditions
- S. Boyd and L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004, chapter 5: duality, Slater's condition and shadow prices
- G. B. Dantzig, *Linear Programming and Extensions*, Princeton University Press, 1963: the simplex method and linear-programming duality
- J. von Neumann, "Zur Theorie der Gesellschaftsspiele", *Mathematische Annalen* 100, 1928: the minimax theorem
- J. F. Nash, "Equilibrium points in n-person games", *Proceedings of the National Academy of Sciences* 36, 1950: every finite game has an equilibrium
- C. E. Lemke and J. T. Howson, "Equilibrium points of bimatrix games", *Journal of the Society for Industrial and Applied Mathematics* 12, 1964: the Lemke–Howson algorithm and the odd number of equilibria
- G. W. Brown, "Iterative solution of games by fictitious play", in *Activity Analysis of Production and Allocation*, Wiley, 1951, and J. Robinson, "An iterative method of solving a game", *Annals of Mathematics* 54, 1951: fictitious play, and its convergence in zero-sum games
- L. S. Shapley, "Some topics in two-person games", in *Advances in Game Theory*, Annals of Mathematics Studies 52, 1964: a game in which fictitious play cycles
- L. S. Shapley, "A value for n-person games", in *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28, 1953: the Shapley value
- D. B. Gillies, "Solutions to general non-zero-sum games", in *Contributions to the Theory of Games IV*, Annals of Mathematics Studies 40, 1959: the core
- L. S. Shapley, "Cores of convex games", *International Journal of Game Theory* 1, 1971: the Shapley value of a convex game lies in its core
- J. F. Banzhaf III, "Weighted voting doesn't work: a mathematical analysis", *Rutgers Law Review* 19, 1965: the Banzhaf index
- T. L. Lai and H. Robbins, "Asymptotically efficient adaptive allocation rules", *Advances in Applied Mathematics* 6, 1985: the logarithmic lower bound on regret
- P. Auer, N. Cesa-Bianchi and P. Fischer, "Finite-time analysis of the multiarmed bandit problem", *Machine Learning* 47, 2002: UCB1 and its bound
- W. R. Thompson, "On the likelihood that one unknown probability exceeds another in view of the evidence of two samples", *Biometrika* 25, 1933: Thompson sampling
- T. Lattimore and C. Szepesvári, *Bandit Algorithms*, Cambridge University Press, 2020: regret, ε-greedy and UCB
- J. Nocedal and S. J. Wright, *Numerical Optimization*, 2nd edition, Springer, 2006, chapter 17: quadratic and exact penalty methods
- N. Nisan, T. Roughgarden, É. Tardos and V. V. Vazirani (eds.), *Algorithmic Game Theory*, Cambridge University Press, 2007: support enumeration and the computation of equilibria
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §7 links to its line
- Experiment: proposed in §8, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
