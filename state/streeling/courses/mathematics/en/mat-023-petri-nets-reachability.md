---
module_id: mat-023-petri-nets-reachability
department: mathematics
course: Petri Nets and Reachability
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "55 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Petri Nets and Reachability — What Enumeration Proves, and When It Must Say Unknown

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 55 minutes

## Objectives

After this lesson, you will be able to:
- Define a Place/Transition net and its firing rule, and fire sequences by hand
- Build a reachability graph breadth first, and read deadlocks and their shortest witnesses off it
- Count reachable markings with a transfer matrix, and explain why state spaces grow exponentially
- Prove that a net is unbounded with a pumping witness, and say what failing to find one does not prove
- Read liveness and reversibility off the strongly connected components of a finite reachability graph
- Use the incidence matrix and P-invariants to prove boundedness and mutual exclusion without enumerating, and explain why the state equation is only a necessary condition
- Trace what IX's `ix-petri` crate decides, which of its verdicts survive a truncated search, and where it must answer `Unknown`

---

## 1. Places, Transitions and the Firing Rule

A **Place/Transition net** has a finite set of places, a finite set of transitions, and weighted arcs that run from a place to a transition or from a transition to a place, never between two places or two transitions. Write Pre(p, t) for the weight of the arc from place p to transition t, and Post(p, t) for the weight of the arc from t to p, with 0 where there is no arc. A **marking** m gives each place a number of tokens m(p) ≥ 0, and the net starts from an initial marking m0. A transition t is **enabled** at m when m(p) ≥ Pre(p, t) for every place p. **Firing** it gives the marking m′ = m − Pre(·, t) + Post(·, t): it consumes Pre(p, t) tokens from each input place and produces Post(p, t) in each output place. One transition fires at a time, and a firing is indivisible.

A one-slot buffer has two places, `empty` with one token and `full` with none, and two transitions: `produce` moves the token from `empty` to `full`, and `consume` moves it back. At m0 only `produce` is enabled; firing it gives full = 1, where only `consume` is enabled, and firing that gives m0 again. A place can be both an input and an output of the same transition, a **self-loop**: the transition needs the token to fire and puts it back.

Two facts follow from the rule, and the later sections rest on them. **Monotonicity**: if a sequence σ can fire from m, and m′ ≥ m place by place, then σ can fire from m′, since extra tokens never disable a transition. **Linearity**: the change that σ makes is the sum of the changes of its transitions, whatever their order, so σ changes m′ by exactly the vector by which it changes m.

### Practice Exercise

Place p holds 2 tokens and has an arc of weight 3 to transition t, which has one output arc to an empty place q. Is t enabled? And if p held 5 tokens?

> *Solution:* No: t needs 3 tokens from p, and p has 2. With 5 tokens t is enabled, and firing it leaves 2 tokens in p and 1 in q. Then t is disabled again, so it fires exactly once.

---

## 2. The Reachability Graph

A marking is **reachable** when some firing sequence leads to it from m0. The **reachability graph** has the reachable markings as vertices, and an edge from m to m′ labelled t whenever firing t at m gives m′. Build it breadth first: start from m0, take the markings in the order they were found, fire every transition enabled at each, and add each new marking to the end of the queue. A marking is **dead** when no transition is enabled at it, and a net is **deadlock-free** when no reachable marking is dead. Breadth-first search finds each marking first along a shortest firing sequence, so following each marking's parent back to m0 gives a shortest **witness**: a sequence that anyone can replay with the firing rule.

In Dijkstra's dining philosophers, n philosophers sit round a table with one fork between each pair of neighbours. Philosopher i thinks, takes the left fork i, then the right fork i + 1 (mod n), eats, and puts both forks back. As a net there are places THINK_i, WAIT_i (holding the left fork), EAT_i and FORK_i, with one token in each THINK_i and FORK_i, and transitions TAKE_LEFT_i, TAKE_RIGHT_i and RELEASE_i. For n = 3 the reachability graph has 14 markings and 27 edges. Exactly one marking is dead: each philosopher holds a left fork and waits for a right fork that a neighbour holds. Its witness is TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2. If each philosopher instead takes both forks in one transition, there are 4 reachable markings, with nobody eating or exactly one of the three eating, and none of them is dead.

### Practice Exercise

Two work lanes share one working tree and one stash stack. Lane 0 takes the tree, then the stash; lane 1 takes the stash, then the tree. Each lane releases both at the end of its work and becomes ready again. Find a dead marking and a shortest witness. How many markings are reachable?

> *Solution:* Lane 0 takes the tree and lane 1 takes the stash. Each lane now holds its first resource and waits for the one the other lane holds, and nothing is enabled. The witness has two firings, one grab per lane. The reachable markings are: both lanes ready; lane 0 holding the tree; lane 0 holding both; lane 1 holding the stash; lane 1 holding both; and the dead marking. That makes six.

---

## 3. Counting Reachable Markings

The state space of a net grows much faster than the net. When the philosophers take both forks at once, a reachable marking is a set of eating philosophers in which no two are neighbours, since neighbours share a fork, and every such set can be reached by letting its members take their forks one after another. Counting these sets is a **transfer-matrix** computation. Walk round the table and record whether each philosopher eats, with the rule that an eater is followed by a non-eater. The matrix A = [[1, 1], [1, 0]] lists the allowed steps, and the number of allowed walks that close up after n steps is the trace of A^n. That trace is φ^n + ψ^n, where φ = (1 + √5)/2 and ψ = (1 − √5)/2 are the eigenvalues of A: the Lucas numbers.

When the philosophers take the left fork first, each one thinks (T), waits holding the left fork (W) or eats (E). Fork i is held by philosopher i in W or E, and by philosopher i − 1 in E. So the only forbidden pattern is an E followed by a W or an E. In the order T, W, E the transfer matrix is M = [[1, 1, 1], [1, 1, 1], [1, 0, 0]]. Its characteristic polynomial is λ(λ² − 2λ − 1), with eigenvalues 0 and 1 ± √2, so the number of allowed configurations is Q(n) = (1 + √2)^n + (1 − √2)^n, the companion Pell numbers, which satisfy Q(n) = 2Q(n − 1) + Q(n − 2). Every allowed configuration is reachable: let the eaters take both forks first, then let the waiters take their left forks. §6 shows that no other marking is. The breadth-first enumeration agrees:

| n | 2 | 3 | 4 | 5 | 6 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| Left fork first: reachable markings | 6 | 14 | 34 | 82 | 198 | 39,202 | 94,642 |
| Both forks at once: reachable markings | 3 | 4 | 7 | 11 | 18 | 322 | 521 |

Each extra philosopher multiplies the first row by about 1 + √2, and the second by about φ. Thirteen philosophers already have 94,642 reachable markings, more than the 50,000 that IX's analyser explores by default (§7).

### Practice Exercise

Compute Q(6) from Q(4) = 34 and Q(5) = 82, and check the result against (1 + √2)^6 + (1 − √2)^6.

> *Solution:* Q(6) = 2 × 82 + 34 = 198. Since (1 + √2)² = 3 + 2√2, the cube gives (1 + √2)^6 = (3 + 2√2)³ = 27 + 54√2 + 72 + 16√2 = 99 + 70√2. In the same way (1 − √2)^6 = 99 − 70√2, and the sum is 198.

---

## 4. Boundedness and the Pumping Witness

A place is **k-bounded** when no reachable marking puts more than k tokens in it, and a net is **bounded** when some k works for every place. A 1-bounded net is called **safe**. A bounded net has finitely many reachable markings, so breadth-first search ends. An unbounded net has infinitely many, and no enumeration of them ends.

Suppose m is reachable, m′ is reachable from m by a sequence σ, and m′ **strictly covers** m: m′ ≥ m place by place, and m′ ≠ m. Then the net is unbounded. By monotonicity σ can fire again from m′, and by linearity it adds the same vector d = m′ − m, which is nonnegative and nonzero. Repeating σ reaches m + kd for every k, so some place grows without limit. The pair (m, m′), with the sequence between them, is a **pumping witness**.

The converse is what makes boundedness decidable. If the net is unbounded, the breadth-first tree of distinct reachable markings is infinite, and each marking has finitely many children, so by Kőnig's lemma the tree has an infinite branch m0, m1, m2, …. By **Dickson's lemma**, every infinite sequence of vectors of natural numbers has indices i < j with m_i ≤ m_j, and on a branch of distinct markings m_i ≠ m_j: the branch contains a pumping witness. Karp and Miller turned this argument into the coverability tree, which decides boundedness for every net. Neither lemma bounds how far apart i and j lie, so a search that looks for the pair only a fixed number of steps back can miss it (§7).

### Practice Exercise

A net has one place `queue` and one transition `grow`, with no input arc and one output arc to `queue`. Give a pumping witness. Then add a place `ticket` holding one token, with an arc from `ticket` to `grow` and an arc from `grow` back to `ticket`. Is the net still unbounded?

> *Solution:* At m0 the queue is empty, and firing `grow` gives queue = 1, which strictly covers m0: the witness is m0, queue = 1, and the sequence `grow`. With the ticket, `grow` takes the ticket and puts it back, so it can still fire forever. The witness becomes ticket = 1, then ticket = 1 and queue = 1, again with `grow`. A self-loop does not limit how often a transition fires.

---

## 5. Liveness, Reversibility and Strongly Connected Components

A transition is **dead** when no reachable marking enables it, and a net with no dead transition is **quasi-live** (level L1 in Murata's classification). A net is **live** (level L4) when, from every reachable marking, every transition can still fire after some sequence. A net is **reversible** when m0 can be reached again from every reachable marking. These properties differ. Take a place `q` with one token, a transition `loop` that takes the token and puts it back, and a transition `never` whose input place is empty. That net is deadlock-free, since `loop` is always enabled, but it is neither quasi-live nor live.

On a finite reachability graph these properties are read off the **strongly connected components**, the maximal sets of markings that can all reach one another. The components form an acyclic graph, and a component is **terminal** when no edge leaves it.

**Theorem.** A net whose reachability graph is finite is live exactly when every transition labels an edge inside every terminal component. *Proof.* From any reachable marking some terminal component can be reached: following edges from component to component must stop, since the component graph is finite and acyclic. If t fires inside every terminal component, then from any marking one reaches a terminal component, and inside it every marking reaches every other, including one where t is enabled. So t can still fire. Conversely, suppose t labels no edge inside a terminal component K. Then t is enabled at no marking of K, because firing it would add an edge, and no edge leaves K. From a marking of K the net never leaves K, so t never fires again.

The net is reversible exactly when the whole graph is one component, since every marking is reachable from m0 by construction. A dead marking is a terminal component on its own, with no edge, so a net with a deadlock and at least one transition is not live. For three philosophers taking the left fork first, the 14 markings form two components: the dead marking, which is terminal, and the other 13, from which it can be reached. Liveness therefore fails for all nine transitions, and reversibility fails as well, since m0 cannot be reached from the dead marking.

### Practice Exercise

Show that a live net with at least one transition is deadlock-free, and give a deadlock-free net that is not reversible.

> *Solution:* Let m be reachable and let t be a transition. Liveness says that some sequence from m ends with t. If m were dead, only the empty sequence could fire from it, and it does not contain t. For the second part, take a place p with one token, an empty place q, a transition `go` from p to q, and a transition `stay` that takes the token from q and puts it back. `stay` keeps firing, so no marking is dead, but once `go` has fired the token never returns to p: the net is not reversible, and it is not live either.

---

## 6. The Incidence Matrix and Invariants

Enumeration visits the markings one at a time; linear algebra reasons about all of them at once. The **incidence matrix** C = Post − Pre has one row per place and one column per transition, and column t is the change that firing t makes. If σ leads from m0 to m and the vector x counts how often each transition occurs in σ, linearity gives the **state equation** m = m0 + C x.

A **P-invariant** is a nonzero vector y with yᵀ C = 0. Multiplying the state equation by yᵀ gives yᵀ m = yᵀ m0 for every reachable marking: a weighted sum of tokens is conserved. If y ≥ 0 and y(p) > 0, then y(p) m(p) ≤ yᵀ m = yᵀ m0, so place p never holds more than yᵀ m0 / y(p) tokens. A net whose places are all covered by nonnegative P-invariants is therefore bounded, from any initial marking, without enumerating anything.

For the philosophers taking the left fork first, two families of P-invariants hold for every n:
- THINK_i + WAIT_i + EAT_i = 1: each philosopher is in exactly one state;
- FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1: fork i is on the table, held by philosopher i, or held by philosopher i − 1 as a right fork.

Each place appears in at least one of them with weight 1, so the net is safe for every n, including 13, where enumeration within the default budget cannot finish. The second family also proves mutual exclusion: EAT_i + EAT_(i−1) ≤ 1, so neighbours never eat at the same time, and this is why §3 found no markings beyond the allowed configurations. For n = 3 the 12 places and 9 transitions give a matrix of rank 6, and these six invariants span all the P-invariants.

A **T-invariant** is a nonzero vector x ≥ 0 with C x = 0: a sequence whose counts are x returns to the marking it started from, if it can fire at all. TAKE_LEFT_i, TAKE_RIGHT_i, RELEASE_i is one.

The state equation is necessary for reachability, not sufficient. Take places `gate` and `out`, both empty, and one transition t with arcs from `gate` to t, from t to `gate` and from t to `out`. Column t of C is (0, 1), since the self-loop cancels. The marking out = 1 satisfies the state equation with x = (1), yet t is never enabled, and m0 is the only reachable marking. The incidence matrix cannot see a self-loop. Deciding reachability exactly is possible (Mayr, 1981), but no algorithm can do it within primitive-recursive time: the problem is Ackermann-complete, with the upper bound from Leroux and Schmitz (2019) and the lower bound from Czerwiński and Orlikowski, and from Leroux (2021).

### Practice Exercise

In the two-lane pump of §2, find a P-invariant that contains the place of free trees, and one that contains the stash. Check that the dead marking satisfies both. Could these invariants alone have predicted the deadlock?

> *Solution:* The tree is free, held by lane 0 while it waits for the stash or works, or held by lane 1 while it works: free trees + lane 0 holding its first resource + lane 0 holding both + lane 1 holding both = 1. Likewise, stash + lane 0 holding both + lane 1 holding its first resource + lane 1 holding both = 1. In the dead marking both lanes hold their first resource, which gives 0 + 1 + 0 + 0 = 1 and 0 + 0 + 1 + 0 = 1. The invariants say which markings are possible, not which are reachable or dead: the deadlock is shown by its witness, and the invariants cannot rule it out.

---

## 7. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a transcription into Python of `net.rs`, `analysis.rs` and `models.rs` in `crates/ix-petri`, and of the net built in `tests/worktree_pump.rs`. The transcription reproduces the assertions of the tests in those files, with two exceptions: it skips the test that compares two JSON serialisations, and for malformed nets it checks that they are refused, not which error is raised. These numbers are predictions, and §8 proposes to check them.

**The firing rule and its order.** [`is_enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L216) checks m(p) ≥ Pre(p, t) place by place, and [`fire`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L239) [consumes the pre-set before producing the post-set](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L237), so a self-loop behaves as §1 says:

```rust
        let mut next = marking.0.clone();
        for &(p, w) in &tr.pre {
            next[p] -= w;
        }
        for &(p, w) in &tr.post {
            next[p] = next[p].checked_add(w).ok_or_else(|| PetriError::Overflow {
                transition: tr.id.clone(),
                place: self.places[p].id.clone(),
            })?;
        }
        Ok(Marking(next))
```

[`build`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L389) [sorts the places](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L402) and the transitions by id and rejects duplicate ids, and [`enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L229) returns transitions in that order. The breadth-first numbering and every witness are therefore the same on every run.

**Exploration, and what truncation means.** [`explore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L225) builds the graph of §2 breadth first. A new marking beyond [`max_states`, 50,000 by default](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L67), is [refused, and the graph is marked truncated](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L260); so is a firing whose [token count would overflow](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L245) a 64-bit integer. A truncated graph contains markings some of whose successors were refused and never recorded, and IX does not mistake them for dead ones: it asks [the net, not the graph](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L464), whether a marking enables anything.

**Which verdicts survive truncation.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) returns `Holds`, `Fails` or `Unknown` for each property, using the arguments of §2 to §5. The table shows which verdicts it gives after a truncated run:

| Property | IX decides from a truncated run | IX decides only from a complete run |
|---|---|---|
| Deadlock freedom | `Fails`, with the number of dead markings found and, [by default, up to 8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L68) of them with their shortest witnesses | `Holds` |
| Boundedness | `Fails`, with a pumping witness | `Holds`, with the bound of each place |
| Quasi-liveness | `Holds`, once every transition has fired | `Fails`, with the transitions that never fired |
| Liveness (L4) and reversibility | Nothing | `Holds` or `Fails`, from the components of §5 |

This is MAT-002's asymmetry. An existential claim is settled by one example, found at any point of the search: some reachable marking is dead, some sequence pumps, each transition fires somewhere. A universal claim is settled only by the whole graph. The verdicts for [deadlock](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L483), [boundedness](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L494), [quasi-liveness](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L527), and [liveness and reversibility](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L538) follow the table line by line. The last row is IX's choice, not a logical necessity, as *Other gaps* below explains. An unbounded net is never explored completely, so only the middle column can ever apply to it.

**Liveness and reversibility, as §5 proves them.** [`liveness_and_reversibility`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L604) marks a component terminal when no edge leaves it, and fails liveness for each transition that labels no edge inside some terminal component. Reversibility holds when there is [one component](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L640). The components come from an [iterative Tarjan](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L367), so a deep graph cannot overflow the stack.

**The pumping witness is sought on one path, at most 512 steps back.** When a marking is discovered, [`strictly_covered_ancestor`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L300) walks back along its breadth-first parents, [at most 512 of them](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L51), looking for one that it strictly covers:

```rust
    fn strictly_covered_ancestor(&self, state: usize) -> Option<usize> {
        let wide_total = |m: &Marking| -> u128 { m.tokens().iter().map(|&t| u128::from(t)).sum() };
        let total = wide_total(&self.markings[state]);
        let mut cursor = self.parent[state].map(|(p, _)| p);
        let mut walked = 0usize;
        while let Some(a) = cursor {
            if walked >= MAX_COVERING_WALK {
                return None;
            }
            walked += 1;
            if wide_total(&self.markings[a]) < total
                && self.markings[state].strictly_covers(&self.markings[a])
            {
                return Some(a);
            }
            cursor = self.parent[a].map(|(p, _)| p);
        }
        None
    }
```

A pair it reports is a proof, by §4. A pair it misses leaves boundedness `Unknown`, as the comment says: cutting the walk short ["can only *miss* a witness"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L292). The miss does not depend on the budget. Take a ring of L places around which one token circulates, and let one transition of the ring also add a token to a counter place. The nearest strictly covering pair on any path is then L firings apart. With L = 512 the transcription finds the witness at the 513th marking; with L = 513 it finds none at any budget, and the net, although unbounded, is reported `Unknown`.

**Known answers.** [`dining_philosophers`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L32) builds both protocols of §2. One test checks, [for n = 2 to 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L110), that taking the left fork first deadlocks and taking both at once does not; another fixes [the dead marking for n = 3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L153). The pump of §2 is [`opposite_acquisition_orders_wedge_the_pump`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L92). Other tests there show that a [canonical acquisition order](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L138) removes the deadlock for 2 to 4 lanes, and that [one lane out of order](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L162) brings it back. The crate's plan records a run on the six-philosopher file published by pnml.org: [729 markings and 3,402 edges](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/plans/2026-09-08-feat-ix-petri-place-transition-nets.md#L111), with two dead markings. Read with Python's standard XML parser and fed to the transcription, the same file gives the same numbers.

**Where the default budget stops.** Thirteen philosophers taking the left fork first have 94,642 reachable markings (§3). The dead marking lies 13 firings from m0, and breadth-first order discovers 94,121 markings before it. With the default budget of 50,000 the analysis stops among markings nine firings from m0, and it reports deadlock freedom as `Unknown`. Yet the deadlock is in the model, and its witness, TAKE_LEFT_00 to TAKE_LEFT_12, is easy to write down and replay. Quasi-liveness holds, since every transition fires within the budget; boundedness is `Unknown`, although the P-invariants of §6 prove the net safe in one line. IX's guide lists [P- and T-invariants, siphons and traps](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L201) as not implemented, and as worth adding ["the day a net in this repository is too big for `max_states`"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L203).

**Other gaps.** The crate promises each property ["with a witness"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/lib.rs#L6), and deadlocks and unboundedness have one. A quasi-liveness `Holds` [carries none](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L528), not even one firing of each transition. A failed liveness verdict names transitions, but no marking from which they can never fire again. The reversibility verdict is a [`Verdict<()>`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L201), so its failure carries no marking from which m0 is unreachable. For the philosophers taking the left fork first, the liveness failure lists all the transitions, because the terminal component is the dead marking; the deadlock verdict is the informative one. Liveness and reversibility are computed only from a complete graph, so a truncated run that finds a dead marking reports both as `Unknown`. Yet by §5 that marking already proves that both fail: nothing fires from it, and m0, from which a truncated run has fired something, cannot be reached from it. There is no coverability tree, so an unbounded net whose witness the walk misses stays `Unknown`. The same analysis is exposed to SQL as [`ix_petri_analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/petri.rs#L10) and to agents as the MCP tool `ix_petri_analyze`, registered as the skill [`petri.analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/petri.rs#L137). Both refuse a budget whose worst-case memory exceeds [512 MiB](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/json.rs#L123).

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

A run on the thirteen philosophers with a budget of 94,122 markings is truncated. Which verdicts can it decide?

> *Solution:* The dead marking is the 94,122nd marking discovered, so it fits within the budget: deadlock freedom fails, with the witness of thirteen TAKE_LEFT firings. Quasi-liveness holds, since every transition fires within the budget. Boundedness remains `Unknown`: proving it by enumeration needs the whole graph, and 520 markings are missing from it. IX also leaves liveness and reversibility `Unknown`, although the dead marking already proves that both fail (§5).

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Counting.** Run `analyze` with the default limits on both protocols for n = 2 to 12. Prediction: the counts of §3, complete runs, one dead marking when the left fork is taken first and none otherwise.
2. **The budget edge.** Run the thirteen philosophers taking the left fork first with `max_states` set to 50,000, 94,121, 94,122 and 94,642. Prediction: deadlock freedom `Unknown` for the first two budgets; `Fails` at 94,122, truncated, with the dead marking at state 94,121; at 94,642 a complete run, safe, neither live nor reversible.
3. **The walk limit.** Build the ring of §7 with L = 512 and L = 513, and run it with `max_states` set to 5,000. Prediction: with L = 512, boundedness `Fails` with a pumping witness from state 0 to state 512 over 512 firings; with L = 513, boundedness `Unknown` and no witness.
4. **Invariants.** Build the incidence matrix from the `pre` and `post` fields of `transitions()` for n = 3 and n = 5, and check the 2n invariants of §6. Prediction: yᵀ C = 0 for each of them, and C has rank 2n.
5. **A file IX did not write.** Read pnml.org's six-philosopher file with `read_pnml` and analyse it. Prediction: 30 places, 30 transitions, 729 markings, 3,402 edges, two dead markings, safe, neither live nor reversible.
6. **Two nets from GA.** Read the two PNML examples of GA's IxqlViewer component, [`petri-producer-consumer.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-producer-consumer.pnml) and [`petri-pipeline-lifecycle.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-pipeline-lifecycle.pnml), and analyse them. Prediction: the producer–consumer net, with 6 places and 4 transitions, has 12 markings and 20 edges, and is 2-bounded, deadlock-free, live and reversible. The pipeline lifecycle net, with 12 places and 8 transitions, has 8 markings and 8 edges; it is safe and quasi-live, but neither live nor reversible, and deadlock freedom `Fails` with three dead markings, succeeded, failed and cancelled, reached in four firings, two firings and one firing.

### Practice Exercise

In step 2 a single marking of budget separates `Unknown` from `Fails`. Why is that not a sign of instability?

> *Solution:* The order of discovery is fixed (§7), so the dead marking is always the 94,122nd discovered, and a budget of 94,121 stops one marking short of it. `Unknown` there is a refusal, not a guess, and it contradicts neither verdict. A larger budget explores the same markings first and then more, so it can turn `Unknown` into a verdict but never reverse one.

---

## 9. Common Pitfalls

- **Reading `Unknown` as `Holds`.** A search that stopped early has found no deadlock among the markings it saw, which says nothing about the others.
- **Taking a truncated state count for the size of the state space.** A run stopped at 50,000 markings has seen 50,000 markings, and the full space may be far larger.
- **Expecting an ancestor walk to find every pumping witness.** A pair further back than the walk reaches is missed at any budget; only a complete method, such as Karp and Miller's coverability tree, decides boundedness.
- **Reading every dead marking as a bug.** The final states of a workflow are dead markings by design, as in GA's pipeline lifecycle (§8); a deadlock verdict points to a defect only where the model says work should go on.
- **Using the state equation as a reachability test.** It is necessary, not sufficient, and it cannot see self-loops.
- **Reading "not live" as "has a deadlock".** A net can be deadlock-free and still have a transition that never fires again.
- **Reading a P-invariant as a proof of reachability.** An invariant rules markings out; only a witness shows that a marking is reached.
- **Forgetting how fast the space grows.** Each philosopher who takes the left fork first multiplies the reachable markings by about 2.4, so a model that is small on paper can exceed any budget.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Place/Transition net** | Places, transitions, and weighted arcs between a place and a transition in either direction |
| **Marking** | A number of tokens for each place; the state of the net |
| **Firing rule** | A transition is enabled when each input place holds at least the arc weight; firing it consumes and produces tokens accordingly |
| **Reachability graph** | The reachable markings, with an edge for each firing |
| **Dead marking** | A marking at which no transition is enabled |
| **Witness** | A firing sequence from m0 that anyone can replay to check a claim |
| **k-bounded, safe** | No reachable marking puts more than k tokens in a place; safe means 1-bounded |
| **Pumping witness** | A reachable marking m and a marking m′ reachable from m and strictly covering it, which prove unboundedness |
| **Quasi-live (L1)** | Every transition fires in some reachable marking |
| **Live (L4)** | From every reachable marking, every transition can still fire |
| **Reversible** | m0 can be reached again from every reachable marking |
| **Terminal component** | A strongly connected component of the reachability graph that no edge leaves |
| **Incidence matrix** | C = Post − Pre; column t is the change made by firing t |
| **State equation** | m = m0 + C x, a necessary condition for reaching m |
| **P-invariant** | A nonzero vector y with yᵀ C = 0; the weighted token sum yᵀ m is conserved |
| **T-invariant** | A nonzero vector x ≥ 0 with C x = 0; a sequence with these counts returns to its starting marking |
| **Transfer matrix** | A matrix of allowed steps, whose powers count the allowed sequences |

---

## Self-Check Assessment

**1. An analyser stops at 50,000 markings, finds no dead one, and reports deadlock freedom as `Unknown`, but every transition has fired. What can you conclude?**
> That the net is quasi-live: each transition fires in some reachable marking, and each firing is a witness. Nothing follows about deadlock freedom, since a dead marking may lie among the markings that were not explored; for thirteen philosophers one does.

**2. Why does a reachable marking m, with a marking m′ reachable from m that strictly covers it, prove unboundedness, while failing to find such a pair proves nothing?**
> The sequence from m to m′ can fire again from m′, by monotonicity, and adds the same nonzero vector each time, by linearity. Failing to find a pair proves nothing, because the search may have stopped before the pair appears, or, as in IX, looked only a fixed number of steps back along one path.

**3. How can the dining philosophers be safe for every n when the analyser cannot finish for n = 13?**
> The P-invariants THINK_i + WAIT_i + EAT_i = 1 and FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1 hold for every n, and they cover every place with weight 1. They bound every place by 1 without listing a single marking.

**4. IX reports that liveness fails for all nine transitions of three philosophers. What does this add to the deadlock verdict?**
> Nothing. The only terminal component is the dead marking, where no transition fires, so every transition is missing from it. The deadlock verdict says more, since it gives the marking and the witness TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2.

**Pass criteria:** Fire a Place/Transition net by hand; build its reachability graph and give a shortest witness for a deadlock; count reachable markings with a transfer matrix; prove unboundedness with a pumping witness and explain what its absence does not show; read liveness and reversibility off the terminal components; prove boundedness and mutual exclusion with P-invariants and explain why the state equation is not sufficient; and say which of IX's verdicts a truncated run can decide.

---

## Research Basis

- C. A. Petri, *Kommunikation mit Automaten*, doctoral thesis, 1962: the origin of Petri nets
- T. Murata, "Petri nets: Properties, analysis and applications", *Proceedings of the IEEE* 77, 1989: the firing rule, the liveness levels L0 to L4, the incidence matrix and invariants
- R. M. Karp and R. E. Miller, "Parallel program schemata", *Journal of Computer and System Sciences* 3, 1969: the coverability tree and the decidability of boundedness
- L. E. Dickson, "Finiteness of the odd perfect and primitive abundant numbers with n distinct prime factors", *American Journal of Mathematics* 35, 1913: the lemma on vectors of natural numbers
- D. Kőnig, "Über eine Schlussweise aus dem Endlichen ins Unendliche", *Acta Scientiarum Mathematicarum* 3, 1927: infinite finitely branching trees have infinite branches
- E. W. Mayr, "An algorithm for the general Petri net reachability problem", *Proceedings of the 13th ACM Symposium on Theory of Computing*, 1981: reachability is decidable
- W. Czerwiński and Ł. Orlikowski, "Reachability in vector addition systems is Ackermann-complete", and J. Leroux, "The reachability problem for Petri nets is not primitive recursive", both in *Proceedings of the 62nd IEEE Symposium on Foundations of Computer Science*, 2021: the lower bound
- J. Leroux and S. Schmitz, "Reachability in vector addition systems is primitive-recursive in fixed dimension", *Proceedings of the 34th Annual ACM/IEEE Symposium on Logic in Computer Science*, 2019: the Ackermann upper bound
- R. E. Tarjan, "Depth-first search and linear graph algorithms", *SIAM Journal on Computing* 1, 1972: strongly connected components
- E. W. Dijkstra, "Hierarchical ordering of sequential processes", *Acta Informatica* 1, 1971: the dining philosophers
- E. G. Coffman, M. J. Elphick and A. Shoshani, "System deadlocks", *ACM Computing Surveys* 3, 1971: the conditions for deadlock, among them circular wait
- ISO/IEC 15909-2:2011, *High-level Petri nets — Part 2: Transfer format*: PNML, the interchange format IX reads
- OEIS A000032 (Lucas numbers) and A002203 (companion Pell numbers): the counts of §3
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §7 links to its line
- GA source at commit `b030c3f05e92189f9cb569d0fe0457ba6269e564`: the two PNML examples of §8
- Experiment: proposed in §8, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
