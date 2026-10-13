---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: Measuring Verdict Distribution Drift with Jensen-Shannon Divergence
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Measuring Verdict Distribution Drift with Jensen-Shannon Divergence

> **Department of Information Theory** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Turn comparable IX analyzer verdict counts into aligned probability vectors.
- Calculate directional Kullback–Leibler (KL) divergence and symmetric Jensen–Shannon (JS) divergence in the units returned by IX.
- Explain why a new category can make one KL direction error while JS remains finite.
- Use a divergence value as a prompt to inspect per-net evidence, with explicit controls for analysis limits and batch composition.

## The project question

IX's [pinned Petri analyzer](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) serializes a property's result as `holds`, `fails`, or `unknown`. The distinction matters: a `fails` result can carry a counterexample, while `unknown` says the analyzer did not decide the property within its exploration limits. If an engineer compares two runs of a set of nets, a shift in the mix of those results might deserve attention. How can the engineer quantify the shift without mistaking a single number for a proof of regression?

The falsifiable question is: **For one fixed property, fixed set of net identities, fixed analyzer revision, and fixed limits, how far did the category distribution move after the net definitions changed?** IX already supplies [KL and JS functions](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222), also exposed as [DuckDB scalar functions](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). We can compute a reproducible answer for a small **synthetic** count fixture. We have not measured any production IX batch or user-facing quality change.

INF-001 used entropy to describe uncertainty within one policy-token distribution. INF-002 showed that GA's compact OPTIC-K mapping discards distinctions between individual vectors. Here the object is different: we compare **two distributions over the same named verdict categories**. A drift score says something about aggregate frequencies. It cannot recover which net changed, why it changed, or whether a changed result is good.

## 1. Choose an observation with a stable meaning

The pinned analyzer's [`Verdict<T>` enum](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) has three tags. Its `holds()` helper returns true only for `Holds`, so `Unknown` is not silently promoted to a pass. The `Analysis` report contains several **different properties**, including `deadlock_free`, `bounded`, `quasi_live`, `live`, and `reversible`. Pooling all properties into one count would mix questions with different proof conditions. For this lesson, choose only `deadlock_free`, one verdict per net, and preserve the fixed order `[holds, fails, unknown]`.

The [deadlock-freedom branch](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) demonstrates why the labels have operational meaning. A discovered dead marking produces `Fails` even if enumeration later truncates; reported witnesses are limited by `max_reported_deadlocks`, which may be zero. If no dead marking is found, `Holds` requires complete exploration; otherwise the answer is `Unknown`. This is a property-specific source observation, not a claim that every analyzer property follows the same branch.

Our fixed exercise fixture is a ten-net batch with this **invented** aggregate table. It is a numerical teaching example, not an IX run log:

| Run | Holds | Fails | Unknown | Total |
|---|---:|---:|---:|---:|
| Baseline | 8 | 0 | 2 | 10 |
| Candidate | 6 | 2 | 2 | 10 |

Dividing each row by its total gives `p = [0.8, 0, 0.2]` and `q = [0.6, 0.2, 0.2]`. Both vectors use the same label order. If one query emitted `[fails, holds, unknown]` and another emitted `[holds, fails, unknown]`, the function would still accept the arrays, but its result would compare the wrong events. Store the labels with the counts and validate the ordering before calculation.

### Practice exercise 1: form the comparable vectors

For the table above, write both normalized vectors in `[holds, fails, unknown]` order. What additional metadata must travel with a real comparison?

> **Answer:** `p=[8/10,0/10,2/10]=[0.8,0,0.2]`; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Keep the property name, net identities, category order, analyzer commit, exploration limits, and each run's total. A divergence computation alone does not verify those conditions.

## 2. Read what IX actually computes

The pinned [`normalize` implementation](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) divides a nonnegative vector by its sum. It rejects an empty vector, negative entries, NaN entries, and an all-zero sum. Our protocol additionally requires finite counts before calling it: the source does not explicitly reject positive infinity. Both divergence functions require equal vector lengths. They use natural logarithms, so their result is in **nats**. Divide by `ln(2)` to express a result in bits. IX's DuckDB wrapper makes the calculation accessible as `ix_kl(p,q)` or `ix_js(p,q)` on `DOUBLE[]` values; a SQL `NULL` list propagates `NULL`, while a math error becomes a SQL error. The SQL wrapper is not evidence that a scheduled comparison job exists.

KL divergence is directional:

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Only categories with `p_i > 0` contribute. For this fixture, baseline-to-candidate KL is `0.8 ln(0.8/0.6) + 0.2 ln(0.2/0.2) = 0.23014565796142483` nats. Reversing the arguments asks for a term `0.2 ln(0.2/0)` in the candidate's `fails` category. Mathematically it diverges; [IX returns an error](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209) rather than an infinity value. Changing the argument order changes the question. A newly observed category must not be made to disappear by catching the error and recording zero.

### Practice exercise 2: explain the KL direction

Compute `D_KL(p || q)` for the fixture. Does `D_KL(q || p)` return the same number in IX?

> **Answer:** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` nats. `D_KL(q || p)` hits `q_fails=0.2` against `p_fails=0`; IX returns its “q is zero where p is positive” parameter error after the arguments are reversed. KL is asymmetric. The baseline-to-candidate direction has finite support here; the reverse direction does not.

## 3. Use JS for a finite, symmetric headline

JS forms the midpoint `m=(p+q)/2`, then averages two KL divergences: `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. For our fixture, `m=[0.7,0.1,0.2]`. The midpoint has positive mass wherever either input does, so this pair's JS remains finite even though one KL direction errors. IX's [implementation comment and code](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) state that JS is symmetric and bounded by `ln(2)` nats. Zero means identical **normalized** distributions, not identical runs or sample counts.

An independent calculation using the displayed formula gives `D_KL(p||m)=0.10682511409961822` and `D_KL(q||m)=0.04613902821563412`; their half-sum is `0.07648207115762617` nats, or `0.1103403047760241` bits. These are observations from the synthetic arithmetic fixture, not measurements from IX's deployment. The pinned IX unit tests cover [the maximum for disjoint one-hot inputs and zero for equal inputs](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580), but we did not run that suite here.

### Practice exercise 3: calculate and bound JS

Calculate the midpoint and JS value for the fixture. Does swapping baseline and candidate change the answer, and what is the theoretical maximum in nats?

> **Answer:** `m=[0.7,0.1,0.2]`; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` nats. Swapping the runs leaves the same midpoint and exchanges the two half-weighted terms, so JS is unchanged. Its maximum is `ln(2)=0.6931471805599453` nats for disjoint supports.

### Practice exercise 4: find what normalization hides

Compare `[80,0,20]` with `[8,0,2]` using `ix_js`. What does the result prove about the two batches?

> **Answer:** Both normalize to `[0.8,0,0.2]`, so `ix_js` returns `0` (subject to floating-point representation). This proves only equality of the normalized category mix. One batch has 100 observations and the other has 10; JS discards that size difference. It also cannot say whether the same individual nets received the same verdicts. Preserve totals and paired net IDs outside the divergence value.

## 4. Decide what a drift signal should trigger

Suppose a future, separately approved QA comparison rule marks `JS > 0.05` nats for investigation. Our **illustrative** value exceeds that invented threshold. That is a reason to inspect data, not evidence that a deployed gate currently uses this threshold and not a reason to reject a change automatically. First check that the same ten nets and `deadlock_free` property were analyzed at both revisions. Then check the analyzer revision and `Limits`: the [report exposes truncation and its cause](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Raising `max_states` can move an `unknown` to `holds` or `fails` without any net behavior changing. Finally, pair verdicts by net ID and inspect available `fails` witnesses and `unknown` reasons. For a witness-review protocol, set `max_reported_deadlocks` above zero and rerun if a failure has no reported witness. A category histogram cannot tell which nets moved or whether the counterexamples are valid for the intended property.

A useful counterargument is that a single divergence score may be unnecessary for a small, stable batch: a three-column count table and the individual verdict changes are easier to understand. The score becomes useful when comparing many consistent batches or prioritizing review, provided the raw table and per-net evidence remain available. This is a design candidate, not a recommendation to replace witness review. A falsifier for the proposed signal would be repeated alerts caused mainly by different net composition or exploration budgets rather than meaningful verdict changes; that outcome would require revising the comparison protocol, not tuning the threshold until the alerts disappear.

### Practice exercise 5: interpret an alert

The hypothetical threshold is `0.05` nats. The calculated JS is `0.07648207115762617`. A teammate says, “The candidate regressed; there are two new failures.” Which part is a checkable arithmetic result, and what must be checked before accepting the regression claim?

> **Answer:** The arithmetic result is `0.07648207115762617 > 0.05`, so the synthetic example would trigger the invented investigation rule. The aggregate table has two candidate `fails` and no baseline `fails`, but it does not identify which nets changed. Confirm identical net IDs, property, analyzer revision, and limits; pair outcomes by net; read any reported failing witnesses and unknown reasons. Require a positive `max_reported_deadlocks` cap and rerun if a witness needed for review is absent. A changed limit or batch could explain drift without a code regression. The score does not prove causation or statistical significance.

## Limits and next step

This lesson verified the formula against a fixed synthetic table with a small independent calculation and read pinned IX source at commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. It did not execute the IX analyzer on ten nets, query a real DuckDB table, run the IX test suite, estimate sampling uncertainty, or validate a production threshold. Counts from repeated but nonidentical batches would need a sampling and pairing plan. A next bounded experiment would record one property per stable net ID at two pinned revisions with identical limits, calculate the divergence, and manually inspect every changed verdict. Keep the count table, per-net records, and witnesses alongside the score so the conclusion remains auditable.
