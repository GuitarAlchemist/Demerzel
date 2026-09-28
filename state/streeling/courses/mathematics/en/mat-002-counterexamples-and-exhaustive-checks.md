---
module_id: mat-002-counterexamples-and-exhaustive-checks
department: mathematics
course: Counterexamples, Witnesses and Exhaustive Checks
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "35 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Counterexamples, Witnesses and Exhaustive Checks — When Checking Cases Is a Proof

> **Department of Mathematics** | Stage: Nigredo (Beginner) | Estimated duration: 35 minutes

## Objectives

After this lesson, you will be able to:
- Tell a universal claim from an existential one, and say what refutes or establishes each
- Refute a universal claim with a single counterexample, and check a witness for an existential claim
- Explain when checking cases is a proof: on a finite domain, or on an infinite one reduced to finitely many cases
- Explain why random testing and unfinished searches can find counterexamples but cannot prove a universal claim
- Read what IX's tests of the dihedral group and its Petri-net analyser actually establish

---

## 1. Universal Claims and Counterexamples

A **universal claim** says that a property P holds for every element of a domain D: "for all x in D, P(x)". MAT-001 showed that no number of examples proves such a claim. The other direction is much cheaper: **one** x for which P(x) is false refutes it. Such an x is a **counterexample**. Logically, a counterexample is a witness for the negation: "not (for all x, P(x))" says the same as "there exists an x with not P(x)".

Two classic examples:
- **Euler's polynomial.** n² + n + 41 is prime for n = 0, 1, 2, …, 39: forty successes in a row. At n = 40 it gives 40² + 40 + 41 = 40 · 41 + 41 = 41 · 41 = 1681, which is not prime. Forty confirmations did not prove the claim; one counterexample refuted it.
- **Euler's sum-of-powers conjecture.** Euler conjectured that, for k ≥ 3, at least k positive k-th powers are needed to add up to a k-th power. The claim stood for nearly two centuries, until Lander and Parkin found, by a computer search, four fifth powers whose sum is a fifth power: 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵ = 61,917,364,224. Finding this counterexample took a machine search; checking it takes five powers and one addition.

### Practice Exercise

Show, without a calculator, that n² + n + 41 is not prime for n = 41.

> *Solution:* For n = 41, every term is a multiple of 41: 41² + 41 + 41 = 41 · (41 + 1 + 1) = 41 · 43. The number has the factors 41 and 43, so it is not prime.

---

## 2. Existential Claims and Witnesses

An **existential claim** says that at least one element has the property: "there exists x in D with P(x)". It is proved by a **witness**: an explicit x, together with a check that P(x) holds. A witness is only as good as its check, so the check must be one a reader can carry out.

- **Fermat numbers.** Fermat believed that every number 2^(2^n) + 1 is prime. Euler refuted this with the witness n = 5: 2^32 + 1 = 4,294,967,297 = 641 × 6,700,417. Anyone can check the product without redoing the search that found 641. The same witness proves the existential claim "some number 2^(2^n) + 1 is composite" and refutes the universal claim "every number 2^(2^n) + 1 is prime".
- **Necessary checks.** A necessary check is a quick test that every correct answer must pass. Failing it refutes the answer at once; passing it proves nothing. Comparing last digits is one: two equal integers end in the same digit, but so do many unequal ones.

Some existence proofs, such as certain proofs by contradiction, never construct a witness. This lesson deals only with the ones that do.

### Practice Exercise

Without computing the powers in full, check that 27⁵ + 84⁵ + 110⁵ + 133⁵ and 144⁵ end in the same digit. Does this prove the Lander–Parkin identity?

> *Solution:* The last digit of a power depends only on the last digit of the base. The last digits of 7, 7², …, 7⁵ are 7, 9, 3, 1, 7; those of 4, 4², …, 4⁵ are 4, 6, 4, 6, 4; those of 3, 3², …, 3⁵ are 3, 9, 7, 1, 3; and 0⁵ ends in 0. The left side therefore ends in the last digit of 7 + 4 + 0 + 3 = 14, which is 4, and 144⁵ ends in 4 as well. The check passes, but it is only necessary: it would also pass for a false identity whose two sides happen to end in the same digit. The identity is proved by computing both sides, which both equal 61,917,364,224.

---

## 3. Exhaustive Checks on Finite Domains

When the domain is **finite**, the rule of MAT-001 has an exception: checking P(x) for **every** x in D is a proof, called a **proof by exhaustion**. A universal claim over a finite domain is a finite list of statements joined by "and", and each of them has been checked.

The size of the check depends on how many variables the claim quantifies over. Take the **dihedral group D12**: the 24 rotations and reflections of a regular 12-gon, which music theory uses for the transpositions and inversions of the 12 pitch classes.
- A claim about one element, such as "every element has an inverse", needs 24 checks.
- A claim about two elements, such as "g · h = h · g", needs 24² = 576.
- A claim about three elements, such as **associativity**, (g · h) · f = g · (h · f), needs 24³ = 13,824.

A claim over an **infinite** domain can sometimes be reduced to finitely many cases. The reduction is a proof step; the checks do the rest.

### Practice Exercise

Prove that for every integer n, the remainder of n² divided by 4 is 0 or 1.

> *Solution:* Write n = 4q + r with r ∈ {0, 1, 2, 3}. Then n² = 16q² + 8qr + r², so n² and r² leave the same remainder when divided by 4. This reduces the infinite domain to four cases: r² = 0, 1, 4, 9 leave the remainders 0, 1, 0, 1. The claim holds in every case, so it holds for every integer. As a consequence, a sum of two squares leaves the remainder 0, 1 or 2 when divided by 4, never 3.

---

## 4. Proof or Check?

Write each element of D12 as a pair (i, a), where i counts rotation steps (0 to 11) and a = 1 marks a reflection. With σ(a) = (−1)^a, the product is

(i, a) · (k, b) = (i + σ(a) · k mod 12, a ⊕ b),

where ⊕ is addition modulo 2. The sign flip encodes the rule that a reflection reverses the direction of a rotation. This is the rule IX implements (§6).

**Theorem.** This product is associative, and the proof works for every modulus, not only 12.

*Proof (direct, as in MAT-001):* take g₁ = (i, a), g₂ = (k, b) and g₃ = (m, c), with every rotation part taken modulo 12.
- (g₁ · g₂) · g₃ = (i + σ(a)k, a ⊕ b) · (m, c) = (i + σ(a)k + σ(a ⊕ b)m, a ⊕ b ⊕ c).
- g₁ · (g₂ · g₃) = (i, a) · (k + σ(b)m, b ⊕ c) = (i + σ(a)k + σ(a)σ(b)m, a ⊕ b ⊕ c).
- The two agree because σ(a ⊕ b) = σ(a)σ(b): the sign of two combined reflection flags is the product of their signs. ∎

The proof and an exhaustive check do different jobs:
- The **proof** covers the formula, for every modulus. It says nothing about whether a given program implements the formula.
- An **exhaustive check** of a program's product over the 13,824 triples covers that program, for D12 only.

A check also detects only the errors it is sensitive to. Drop the sign flip, (i, a) · (k, b) = (i + k, a ⊕ b), and the product is still associative: it is another group, Z12 × Z2. An associativity check cannot see the missing sign. A check of the relation "reflection, then rotation, then reflection gives the inverse rotation" can.

There is a second road from pairs to triples. Let each element g = (i, a) act on the 12 pitch classes by the function π_g(p) = i + σ(a)p mod 12. If π_{g·h} = π_g ∘ π_h for every pair, and distinct elements give distinct functions, then associativity is inherited from the composition of functions, which is always associative: π_{(g·h)·f} = π_g ∘ π_h ∘ π_f = π_{g·(h·f)}, hence (g · h) · f = g · (h · f). A check over pairs, together with this argument, proves a claim about triples. §6 shows that IX has a test of exactly this form.

### Practice Exercise

A faulty implementation takes the sign from the second factor: (i, a) · (k, b) = (i + σ(b) · k mod 12, a ⊕ b). Show that it is not associative, using g₁ = (0, 0), g₂ = (1, 0) and g₃ = (0, 1).

> *Solution:* On the left, g₁ · g₂ = (0 + 1, 0) = (1, 0), then (1, 0) · (0, 1) = (1 − 0, 1) = (1, 1). On the right, g₂ · g₃ = (1 − 0, 1) = (1, 1), then g₁ · (1, 1) = (0 − 1, 1) = (11, 1). Since (1, 1) ≠ (11, 1), this one triple refutes associativity: one counterexample among the 13,824 triples is enough.

---

## 5. When the Search Is Incomplete

Searches are asymmetric:
- A counterexample found by a **partial** search is conclusive. It refutes the universal claim, however little of the domain was explored.
- A partial search that finds **no** counterexample proves nothing about the part it did not explore.

**Random testing** is a partial search. QuickCheck (Claessen and Hughes, 2000) made it a routine tool: you state a property, and the tool checks it on many randomly generated inputs, reporting any input on which it fails. A reported failure is a counterexample. A thousand passes are evidence, not a proof: on an infinite domain, the unexplored part is still infinite. On a small finite domain, an exhaustive check does better, because it is a proof; for associativity in D12 it has only 13,824 cases.

An honest tool keeps the difference visible. A **Petri net** models a system as tokens moving between places; a *marking* is a state of the system, and a marking is *dead* when nothing can happen from it. IX's Petri-net analyser, the subject of MAT-023, explores the markings a net can reach and returns one of three verdicts for each property ([`Verdict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L89)):
- `Holds`: the property holds, and here is what was measured;
- `Fails`: the property fails, and here is the counterexample;
- `Unknown`: the property was not decided within the exploration limits, and here is why.

`Unknown` is never counted as a pass: the method [`holds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L100) is true only for `Holds`.

### Practice Exercise

An analyser stops at its state limit after exploring a million markings, none of them dead, and reports deadlock freedom as `Unknown`. A colleague concludes that the net is deadlock-free. What is wrong? And if the analyser had found a dead marking among its first ten states, would stopping early weaken that result?

> *Solution:* "No reachable marking is dead" is a universal claim over all reachable markings, and the analyser explored only some of them. A dead marking may lie among the others, so `Unknown` is the honest answer and the colleague's conclusion does not follow. A dead marking that was found is a counterexample: the firing sequence that reaches it can be replayed from the initial marking, whatever was left unexplored. Stopping early does not weaken it.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it. It has not run IX's tests: whether they pass at this commit is a question for the experiment of §7.

**The dihedral group.** [`DihedralElement`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L16) stores a rotation from 0 to 11 and a reflection flag, and implements the [`Group`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L6) trait. Its product, verbatim from `dihedral.rs` lines 66–77, is the rule of §4:

```rust
    fn compose(&self, other: &Self) -> Self {
        // (r^i s^j)(r^k s^l) = r^(i + (-1)^j · k) s^(j+l).
        // The sign flip encodes sr = r^(-1)s: rotation "conjugates" through reflection.
        let i = self.rotation as i16;
        let k = other.rotation as i16;
        let sign: i16 = if self.reflected { -1 } else { 1 };
        let new_rot = (i + sign * k).rem_euclid(12) as u8;
        Self {
            rotation: new_rot,
            reflected: self.reflected ^ other.reflected,
        }
    }
```

The test [`group_law_exhaustive_closure_and_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L137) is exhaustive over elements and pairs, not triples:
- for each of the 24 elements, it asserts g · g⁻¹ = e, g⁻¹ · g = e, e · g = g and g · e = g;
- for each of the 576 pairs, it asserts that the rotation of g · h is below 12 ([line 148](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L148));
- it asserts that the 576 products include all 24 elements ([line 158](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L158)).

No test in `dihedral.rs` states associativity. The test [`action_composition_matches_group_composition`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L135) does more than it seems. For each of the 576 pairs and each of nine sample pitch-class sets x, it asserts (g · h) · x = g · (h · x), where the action [`apply`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L40) is written separately from `compose`: it sends each pitch class p to −p if the element is a reflection, then rotates. That is the function π_g of §4. One sample set, the C major triad {0, 4, 7}, is sent by the 24 elements to 24 different sets: the 12 major and the 12 minor triads. So for each pair only one element sends {0, 4, 7} to g · (h · {0, 4, 7}), namely the true product of D12, and the test forces `compose` to return it. If this test passes, all 576 products are correct, and associativity follows from the proof of §4 without any loop over triples.

**The Petri-net analyser.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) explores the reachable markings up to its limits. Its deadlock verdict, verbatim from `analysis.rs` lines 483–491, is the asymmetry of §5 in code:

```rust
    let deadlock_free = if deadlock_count > 0 {
        Verdict::Fails(deadlocks)
    } else if complete {
        Verdict::Holds(Vec::new())
    } else {
        Verdict::Unknown {
            reason: unknown("deadlock freedom"),
        }
    };
```

A dead marking that was found gives `Fails` whether or not the exploration finished: as the comment above this code says ([line 460](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L460)), its witness sequence reaches it from the initial marking and firing is deterministic. The absence of dead markings gives `Holds` only when the exploration finished (`complete`), and `Unknown` otherwise. The test [`witness_sequences_are_shortest_and_replayable`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L809) builds a small net with a short and a long route to the same dead marking, asserts that the reported witness is the short one, `a_short`, and replays it with `fire` to check that it reaches the reported marking.

**Property-based testing.** IX declares the `proptest` library, a Rust tool in the QuickCheck family, in its workspace manifest ([`Cargo.toml` line 211](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L211)) and in five crates, but at this commit no Rust file uses it. In IX, property-based testing is theory, not practice.

### Practice Exercise

Which assertion of `group_law_exhaustive_closure_and_inverse` can never fail, and why? Then consider a faulty product that differs from IX's in one entry only: (1, 1) · (2, 1) returns (5, 0) instead of (11, 0). Which of the two D12 tests above would catch it?

> *Solution:* "The rotation of g · h is below 12" can never fail: `compose` reduces the rotation with `rem_euclid(12)`, which always returns a value from 0 to 11, and an assertion that cannot fail checks nothing. The faulty product passes every assertion in `dihedral.rs`: the identity and inverse assertions only use pairs that contain e or an element and its inverse, and (2, 1) is not the inverse of (1, 1), since each reflection is its own inverse; the 576 products still include all 24 elements; and the other tests of the file use other products. Yet the faulty rule is not associative: with g₁ = (1, 0), g₂ = (0, 1) and g₃ = (2, 1), (g₁ · g₂) · g₃ = (1, 1) · (2, 1) = (5, 0), while g₂ · g₃ = (0 − 2, 0) = (10, 0) and g₁ · (10, 0) = (11, 0). The action test catches it: π_(1,1) ∘ π_(2,1) sends p to 1 − (2 − p) = p − 1, which is π_(11,0), so only (11, 0) sends {0, 4, 7} to the right set.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results.

1. **Associativity, exhaustively.** Check (g · h) · f = g · (h · f) with IX's `compose` for all 13,824 triples and count the failures. Prediction: none, by the proof of §4.
2. **Negative controls.** Run the same checker on the faulty rule of the §4 exercise and on the one-entry fault of the §6 exercise. Prediction: at least one failing triple for each, including the two triples found by hand above. A checker that reports no failure here is broken, and its verdict in step 1 would mean nothing.
3. **What IX's tests detect.** Restate the assertions of `group_law_exhaustive_closure_and_inverse` and `action_composition_matches_group_composition` as checks of an arbitrary product rule, and apply them to IX's `compose` and to the two faults. Prediction: IX's `compose` passes both; the one-entry fault passes the first and fails the second; the rule of the §4 exercise fails both, the first one already at e · g = g, since e · (1, 1) = (0 − 1, 1) = (11, 1).
4. **Replaying a witness.** Build the net of `witness_sequences_are_shortest_and_replayable`, run `analyze` with the default limits, and replay the reported witness with `fire`. Prediction: deadlock freedom is `Fails`, the witness is `a_short`, and the replay reaches the reported dead marking.

### Practice Exercise

Why must step 2 succeed before anyone trusts step 1?

> *Solution:* A checker that reports "no failure" might be right, or might be unable to fail, like the assertion "rotation below 12" of §6. Running it on rules known to be wrong shows that it can detect a failure. Only then does its silence on IX's `compose` mean something: together with the proof of §4, it says that this code implements an associative product.

---

## 8. Common Pitfalls

- **Reading many confirmations as a proof.** Euler's polynomial passed forty cases and failed the forty-first.
- **Checking the wrong number of variables.** A claim about triples is not checked by a loop over pairs, unless an argument like the one in §4 connects them.
- **Writing assertions that cannot fail.** Make sure each assertion would fail for some wrong implementation; otherwise it tests nothing.
- **Counting `Unknown` as a pass.** "No counterexample found within the limits" is not "no counterexample".
- **Trusting a checker that has never failed.** Run it on a known fault first: a negative control.
- **Mistaking a necessary check for a verification.** Matching last digits make an identity plausible, not true.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Universal claim** | A claim that a property holds for every element of a domain: "for all x, P(x)" |
| **Existential claim** | A claim that at least one element has a property: "there exists x with P(x)" |
| **Counterexample** | An element for which a universal claim fails; one is enough to refute it |
| **Witness** | An explicit element, with a check, that proves an existential claim |
| **Proof by exhaustion** | A proof that checks every case of a finite domain, or the finitely many cases an infinite one reduces to |
| **Necessary check** | A test that every correct answer passes: failing it refutes, passing it proves nothing |
| **Random testing** | Checking a stated property on many randomly generated inputs: it finds counterexamples but proves nothing about the inputs it skips |
| **Negative control** | Running a checker on a case known to be wrong, to show that it can fail |
| **Associativity** | (g · h) · f = g · (h · f) for all g, h, f: a claim about triples |
| **Dihedral group D12** | The 24 rotations and reflections of a regular 12-gon, used for the transpositions and inversions of pitch classes |

---

## Self-Check Assessment

**1. A property has held for the first million positive integers. Is it proved?**
> No. It is a universal claim over an infinite domain, and a million cases leave infinitely many unchecked; n² + n + 41 was prime forty times before it failed. A proof is needed, possibly one that reduces the claim to finitely many cases.

**2. Why do 13,824 checks prove that a D12 product is associative, while 10,000 random triples of integers prove nothing about an operation on all integers?**
> D12 has 24 elements, so its 13,824 triples are all the cases: the check is a proof by exhaustion. 10,000 random integer triples leave infinitely many untested, and any of them could be a counterexample.

**3. Can a check over the 576 pairs of D12 establish associativity?**
> Not by itself: associativity is a claim about triples, and a check over pairs does not even state it. It can together with an argument that connects pairs to triples, such as an action: if π_{g·h} = π_g ∘ π_h for every pair and distinct elements act differently, associativity follows from that of function composition. IX's action test has this form.

**4. IX's Petri analyser reports deadlock freedom as `Unknown`. What can you conclude?**
> Only that no dead marking was found in the part explored before the limit. Nothing follows about the rest, so it is not a pass. Had a dead marking been found, the verdict would be `Fails`, with a replayable witness, even after an early stop.

**Pass criteria:** Refute a universal claim with a counterexample, check a witness, recognise when a finite check is a proof, and explain why random tests and unfinished searches do not prove universal claims, including in IX's tests and its Petri analyser.

---

## Research Basis

- I. Lakatos, *Proofs and Refutations: The Logic of Mathematical Discovery*, Cambridge University Press, 1976: the role of counterexamples in how mathematics develops
- L. J. Lander and T. R. Parkin, "Counterexample to Euler's conjecture on sums of like powers", *Bulletin of the American Mathematical Society* 72, 1079, 1966
- K. Claessen and J. Hughes, "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs", *Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP 2000)*, 268–279, doi:10.1145/351240.351266
- Euler's polynomial n² + n + 41 and his factorisation of 2^32 + 1 are classical; every number in this lesson can be checked by hand or by direct computation
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §5 and §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
