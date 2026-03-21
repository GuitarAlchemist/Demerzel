---
module_id: mat-001-proof-strategies
department: mathematics
course: Foundations of Mathematical Reasoning
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: mathematics
version: "1.0.0"
---

# Proof Strategies — How to Prove Things

> **Department of Mathematics** | Stage: Nigredo (Beginner) | Duration: 30 minutes

## Objectives

After this lesson, you will be able to:
- Explain what a mathematical proof is and why it matters
- Apply direct proof to establish a statement from known facts
- Apply proof by contradiction to show a statement must be true
- Apply proof by induction to prove statements about all natural numbers
- Recognize which proof strategy fits a given problem

---

## 1. What Is a Proof?

A proof is a logical argument that establishes, beyond all doubt, that a mathematical statement is true. Not probably true, not true in most cases — **always** true, in every possible situation the statement describes.

This is what makes mathematics unique among disciplines. In science, you gather evidence and form theories that could be overturned by new data. In mathematics, once something is proved, it stays proved forever. Euclid's proofs from 300 BCE are as valid today as they were then.

A proof starts from **axioms** (statements accepted as true) and **previously proved results**, then uses logical rules to arrive at the conclusion. Each step must follow inevitably from the previous steps.

Three common misconceptions:
- **"Examples prove things."** No. Showing that a statement works for 10, 100, or a million cases does not prove it works for all cases. One counterexample can destroy a conjecture that passed billions of tests.
- **"Proofs must be long and complicated."** Some of the most beautiful proofs are short. Elegance is valued.
- **"There is only one way to prove something."** Most theorems can be proved multiple ways. Choosing the right strategy is part of the art.

---

## 2. Direct Proof

A **direct proof** starts from what you know and reasons forward, step by step, to what you want to show.

**Structure:**
1. Assume the hypothesis (the "if" part of the statement)
2. Apply definitions, known results, and logical steps
3. Arrive at the conclusion (the "then" part)

**Example: Prove that the sum of two even numbers is even.**

*Statement:* If *a* and *b* are even, then *a + b* is even.

*Proof:*
- Since *a* is even, by definition *a = 2m* for some integer *m*.
- Since *b* is even, by definition *b = 2n* for some integer *n*.
- Then *a + b = 2m + 2n = 2(m + n)*.
- Since *m + n* is an integer, *a + b* is 2 times an integer, which is even by definition.

That is a complete proof. Every step follows logically. No gaps, no hand-waving.

**When to use direct proof:** When you can clearly see a path from hypothesis to conclusion. When definitions give you algebraic forms to manipulate. This is your default strategy — try it first.

### Practice Exercise

Prove that the product of two odd numbers is odd. (Hint: an odd number can be written as *2k + 1* for some integer *k*.)

> *Solution:* Let *a = 2m + 1* and *b = 2n + 1*. Then *ab = (2m+1)(2n+1) = 4mn + 2m + 2n + 1 = 2(2mn + m + n) + 1*. Since *2mn + m + n* is an integer, *ab* has the form *2k + 1*, so it is odd.

---

## 3. Proof by Contradiction

Sometimes the direct path is not obvious. **Proof by contradiction** takes a different approach: assume the opposite of what you want to prove, then show that this assumption leads to something impossible.

**Structure:**
1. Assume the negation of the statement you want to prove
2. Reason logically from that assumption
3. Arrive at a contradiction (something that is clearly false, or that contradicts a known fact)
4. Conclude that the assumption must be wrong, so the original statement is true

**Example: Prove that the square root of 2 is irrational.**

*Statement:* There is no fraction *p/q* (with *p, q* integers, *q* not zero, in lowest terms) such that *(p/q)^2 = 2*.

*Proof:*
- **Assume the opposite:** Suppose sqrt(2) is rational. Then sqrt(2) = *p/q* where *p* and *q* are integers with no common factors (lowest terms).
- Squaring both sides: *2 = p^2 / q^2*, so *p^2 = 2q^2*.
- This means *p^2* is even, which means *p* itself must be even (since the square of an odd number is odd). So *p = 2k* for some integer *k*.
- Substituting: *(2k)^2 = 2q^2*, so *4k^2 = 2q^2*, so *q^2 = 2k^2*.
- This means *q^2* is even, so *q* is even.
- But now both *p* and *q* are even, meaning they share a factor of 2. **This contradicts our assumption** that *p/q* was in lowest terms.
- Therefore, our assumption was wrong. The square root of 2 is irrational.

**When to use contradiction:** When you want to prove something does not exist, or when the statement involves words like "no," "cannot," or "impossible." Also useful when the direct approach gets tangled.

### Practice Exercise

Prove by contradiction that there is no largest integer. (Hint: assume there is a largest integer *N*, then consider *N + 1*.)

> *Solution:* Assume there exists a largest integer *N*. Then *N + 1* is also an integer (integers are closed under addition). But *N + 1 > N*, contradicting the assumption that *N* was the largest. Therefore, no largest integer exists.

---

## 4. Proof by Induction

**Induction** is your tool for proving statements about all natural numbers (or any infinite sequence). It works like a chain of dominoes.

**Structure:**
1. **Base case:** Prove the statement is true for the first value (usually *n = 0* or *n = 1*)
2. **Inductive step:** Assume the statement is true for some arbitrary value *n = k* (the **inductive hypothesis**). Then prove it must also be true for *n = k + 1*.
3. **Conclusion:** Since the base case is true and each case implies the next, the statement is true for all natural numbers.

Why does this work? If domino 1 falls (base case), and every falling domino knocks down the next one (inductive step), then all dominoes fall.

**Example: Prove that the sum 1 + 2 + 3 + ... + n = n(n+1)/2 for all positive integers n.**

*Base case (n = 1):*
- Left side: 1
- Right side: 1(1+1)/2 = 1
- They match. Base case holds.

*Inductive step:*
- **Inductive hypothesis:** Assume 1 + 2 + ... + k = k(k+1)/2 for some positive integer *k*.
- **Show it holds for k + 1:** We need 1 + 2 + ... + k + (k+1) = (k+1)(k+2)/2.
- Starting from the left side: 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) (using the inductive hypothesis)
- = (k+1)(k/2 + 1) = (k+1)(k+2)/2
- This matches the formula for *n = k + 1*. The inductive step holds.

*Conclusion:* By induction, the formula holds for all positive integers *n*.

**When to use induction:** When the statement is about all natural numbers (or all values from some starting point). Look for formulas involving *n*, statements like "for all *n* >= 1," or recursive definitions.

### Practice Exercise

Prove by induction that *2^n > n* for all positive integers *n*.

> *Solution:*
> *Base case (n = 1):* 2^1 = 2 > 1. True.
> *Inductive step:* Assume 2^k > k. Then 2^(k+1) = 2 * 2^k > 2k (by the hypothesis). Since 2k = k + k >= k + 1 for all k >= 1, we have 2^(k+1) > k + 1.
> By induction, 2^n > n for all positive integers n.

---

## 5. Choosing Your Strategy

When faced with a statement to prove, ask yourself these questions:

| Question | If Yes, Try... |
|----------|---------------|
| Can I get from hypothesis to conclusion using definitions and algebra? | Direct proof |
| Does the statement say something is impossible, or that something doesn't exist? | Contradiction |
| Is the statement about all natural numbers, or does it have a recursive structure? | Induction |
| Am I stuck with direct proof? | Try contradiction as an alternative |

In practice, mathematicians often attempt direct proof first. If that stalls, they switch to contradiction. If the statement is about natural numbers, induction is usually the right choice.

Some statements can be proved by any of the three methods. As you gain experience, you develop intuition for which approach will be cleanest.

---

## 6. Common Pitfalls

- **Assuming what you are trying to prove.** This is called "begging the question" or circular reasoning. In direct proof, your starting point must be the hypothesis, not the conclusion.
- **Forgetting the base case in induction.** Without the base case, you have no starting domino. The inductive step alone proves nothing.
- **Not clearly stating the inductive hypothesis.** Be explicit: "Assume the statement holds for *n = k*." Then use this assumption to prove the *k + 1* case.
- **In contradiction, not actually reaching a contradiction.** You must arrive at something that is definitively false — not just weird or unexpected.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Proof** | A logical argument establishing that a mathematical statement is true in all cases |
| **Axiom** | A statement accepted as true without proof, serving as a starting point |
| **Direct proof** | Reasoning forward from hypothesis to conclusion using definitions and logic |
| **Proof by contradiction** | Assuming the negation of the desired conclusion and deriving a contradiction |
| **Proof by induction** | Proving a base case and an inductive step to establish a statement for all natural numbers |
| **Inductive hypothesis** | The assumption that the statement holds for *n = k*, used in the inductive step |
| **Counterexample** | A single case showing a statement is false — one counterexample disproves a universal claim |

---

## Self-Check Assessment

**1. What is the fundamental difference between a proof and a large collection of examples?**
> A proof establishes truth for all cases through logical deduction. Examples only show specific cases work and cannot rule out an unexamined counterexample.

**2. In proof by contradiction, what are the three steps after assuming the negation?**
> Reason logically from the assumption, arrive at a statement that contradicts a known fact, then conclude the assumption was false.

**3. What are the two components of a proof by induction?**
> The base case (proving the statement for the first value) and the inductive step (proving that if the statement holds for *k*, it also holds for *k + 1*).

**4. You want to prove that no even number greater than 2 is prime. Which strategy would you use?**
> Direct proof: by definition, an even number greater than 2 can be written as *2k* where *k > 1*, so it has factors 1, 2, k, and 2k — meaning it has a factor other than 1 and itself, so it is not prime.

**Pass criteria:** Successfully apply direct proof, contradiction, and induction to simple examples, and explain when each strategy is appropriate.

---

## Research Basis

- Proof is the defining methodology of mathematics, dating to ancient Greek mathematics
- Direct proof, contradiction, and induction cover the vast majority of undergraduate proof techniques
- Common proof errors (circular reasoning, missing base case) are well-documented in mathematics education research
- Pedagogically, learning proof strategies before specific mathematical content improves long-term reasoning ability
- Sources: Mathematics education consensus, Streeling Department of Mathematics curriculum
- Belief state: T(0.92) F(0.01) U(0.05) C(0.02)
