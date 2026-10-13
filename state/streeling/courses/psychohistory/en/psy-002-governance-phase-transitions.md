---
module_id: psy-002-governance-phase-transitions
department: psychohistory
course: "Testing Governance Regime Change as a Phase-Transition Analogy"
level: intermediate
prerequisites: [psy-001-intro-fractal-compounding]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
research_cycle: psychohistory-2026-03-23-001
version: "1.1.0"
---

# Testing Governance Regime Change

> **Department of Psychohistory** | Level: Intermediate | Duration: 35 minutes | Status: revised draft; subject and learner review pending

## Objectives

After this lesson, you will be able to:
- Distinguish a physical phase transition from a proposed analogy for governance change
- Identify five proposed indicators and one unmeasured variety hypothesis for investigating regime shifts
- Name the evidence needed before calling a governance change abrupt, continuous, or predictable
- Explain what evidence would be needed before requisite variety could be tested as a governance transition signal
- Design a monitoring dashboard from governance state files

---

## 1. The Analogy and Its Limits

In physics, water becomes ice at 0 degrees C. The molecules are the same, but their collective behavior changes qualitatively. This is a **phase transition** — the system shifts from one regime to another.

For Demerzel, “phase transition” is an analogy worth testing, not an observed law. A larger policy inventory can change work patterns, but the number of files alone cannot show a qualitative regime change or predict when one will occur. A test would define the behavior of interest, pin observations before and after a change, and compare alternative explanations.

### First-Order vs Second-Order Transitions

| Type | Physics Analogy | Governance Example |
|------|----------------|-------------------|
| First-order | Water → ice (abrupt, latent heat) | Kill switch activation as an **analogy** for an abrupt change |
| Second-order | Ferromagnet at Curie temperature (continuous) | Gradual workflow change as an **analogy**; no critical point measured |

Whether any governance change has the structure of a physical phase transition is untested here. The indicators below are investigation prompts, not predictors validated on past transitions.

---

## 2. Five Proposed Indicators and One Open Measurement

### Signal 1: Belief Distribution Skew

Demerzel's logic is hexavalent: T (True), P (Probable), U (Unknown), D (Doubtful), F (False), C (Contradictory). The ratio `T/U` is the **crystallization index** — how much of your knowledge has solidified. It is a four-state projection: the department weights files count only `total_T`, `total_F`, `total_U` and `total_C`, with no count for P or D, so the index cannot see a probable or doubtful belief, nor a move between T and P or between D and F. Computing it over all six values would need P and D counts that these files do not carry.

```
crystallization_index = total_T / max(total_U, 1)
```

If this ratio changes by more than two historical standard deviations, inspect the underlying counts and recording process. Two standard deviations are an illustrative investigation trigger, not a validated transition predictor; with sparse cycles the standard deviation may itself be unstable.

- **Rising rapidly:** More T relative to U is recorded; check whether reclassification or changed coverage explains it.
- **Falling rapidly:** More U relative to T is recorded; check whether new topics entered the inventory.

**Where to measure:** `state/streeling/departments/*.weights.json` → `metadata.total_T`, `metadata.total_U`

### Signal 2: Health Score Velocity

The governance health score R is Demerzel's resilience score, defined in `CONTEXT.md` as `R = injections_caught / injections_total`: the share of injected faults that detection catches. `state/resilience/history.json` records `overall_score` by chaos cycle, and root `governance-health.json` holds the latest value. A change in R describes those tests; it is not a thermodynamic potential or a measure of proximity to a regime boundary:

```
velocity = dR/dt (health score change per cycle)
```

| Pattern | Meaning |
|---------|---------|
| Velocity positive, accelerating | Reported score rose faster; inspect changed test cases |
| Velocity positive, decelerating | Reported score still rose, more slowly |
| Velocity near zero | Reported score changed little; no equilibrium claim follows |
| Velocity negative | Reported score fell; inspect test cases and detection changes |

**Illustrative dashboard bands, not empirical regime thresholds:** `<0.5`, `0.5–<0.7`, `0.7–<0.9`, and `≥0.9` can group displayed R values. These labels do not establish reactive, structured, proactive, or autonomous behavior. Such interpretations need separately measured outcomes and stable fault-injection cases.

### Signal 3: Policy Density Saturation

An added policy can help, do nothing, or add work. A descriptive change-per-file calculation is:

```
marginal_return = delta_R / delta_policy_count
```

Three near-zero values do not prove saturation. Policy changes can arrive with new tests, enforcement, personnel, or other policies, so `delta_R / delta_policy_count` does not isolate one policy's causal return. Compare matched fault-injection cases and record the concurrent changes before deciding whether a design change is needed.

Weighting by the number of constrained personas would still measure declared scope, not effectiveness. Treat it as a possible descriptive field, not a validated return metric.

### Signal 4: Cross-Repo Coupling Strength

Demerzel governs four repos (demerzel, ix, tars, ga). Record each repo's compliance rate once per cycle, and over a window of the last W cycles average the absolute values of the Pearson correlations of the six repo pairs (a single cycle gives one rate per repo, from which no correlation can be computed). Take W of at least 30 cycles, the same in every window you compare: with W = 2 every correlation is exactly ±1, and over short windows chance alone gives large values, since for two independent repos the expected |r| is about 0.8/√(W − 1), 0.27 at W = 10 and 0.15 at W = 30, against the 0.3 threshold below. Take absolute values because two repos that move in opposite directions, with a correlation near −1, are as tightly coupled as two that move together, and correlations of opposite sign would cancel in a signed mean. A constant series, such as a repo holding at 100%, has no correlation with anything: leave its pairs out, and compare two windows only over the pairs defined in both. A mean over a different set of pairs measures something else, and dropping weak pairs alone can lift it into the tightly coupled regime. If no pair remains, coupling is undefined for the window:

```
coupling = mean_{i<j} |pearson_correlation(rates_i[W], rates_j[W])|
```

| Coupling | Regime |
|----------|--------|
| < 0.3 | Low observed absolute correlation in this window |
| 0.3 - 0.7 | Middle illustrative band; investigate shared causes |
| > 0.7 | High observed absolute correlation; propagation is unproven |

A jump means these recorded series became more correlated in the chosen window; it does not establish causal coupling. The mean discards signs, so two repos improving while two decline in lockstep can give every pair `|r| = 1`. Inspect the signed pairs and common changes before proposing a coordination explanation. No phase transition follows from a correlation change alone.

### Signal 5: Conscience Signal Frequency

In statistical mechanics, fluctuations grow without bound as a system approaches a critical point, where the transition is continuous (second-order). Near the liquid–gas critical point this shows as **critical opalescence**: density fluctuations grow to the scale of the wavelength of light, and the fluid turns milky. Ordinary boiling, a first-order transition, has no such precursor.

It is a hypothesis that anomaly or escalation rates might change before some governance changes. This lesson has no time series that tests that hypothesis. A kill switch is an administrative event; labeling it “first-order” is metaphorical, not a measured physical classification.

```
signal_rate = conscience_signals_count / time_window
```

A 2x increase over 3 cycles is a reason to inspect the underlying events and their denominator. No transition threshold or direction has been validated for this signal.

**Where to measure:** `state/conscience/signals/` directory

### Signal 6: Requisite Variety as an Unvalidated Candidate

The revised [CYB-003](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) withdraws its earlier ratio of policy and persona counts. Counting distinct response labels and disturbance labels in one cycle would be reproducible, but their quotient would still ignore which response works for which disturbance. No matched disturbance → response → outcome series has been measured here. Therefore there is **no operational variety signal or 1.0 regime boundary** to plot yet.

A useful experiment would predefine disturbance classes, permitted responses, and acceptable outcomes, then record each matched event across cycles. Compare independently checked success and unresolved cases before interpreting any information measure. The claim that this becomes an order parameter for governance transitions remains a hypothesis, not a result of CYB-003.

---

## 3. Compare Evidence Before Naming a Regime

| Recorded quantity | Useful comparison | Missing gate |
|---|---|---|
| R by chaos cycle | Compare matched fault-injection cases | Stable case set and independently checked outcomes |
| T and U counts | Inspect changes in recorded belief mix | Stable coverage and P/D counts |
| Repo compliance rates | Compare aligned windows and signed correlations | Shared denominator and causal investigation |
| Requisite variety | Proposed disturbance → response → outcome experiment | Matched event series; no current ratio |

No number of aligned indicators currently establishes a phase transition. A useful claim names the observed workflow change, the revision and time window, and what other explanation was tested.

---

## 4. Practice Exercise

Using the current Demerzel governance state:

1. Calculate the crystallization index from the psychohistory weights file:
   - `total_T = ?`, `total_U = ?`
   - `crystallization_index = total_T / max(total_U, 1)`

2. Take R as the `overall_score` of the latest record in `state/resilience/history.json`. Which illustrative display band contains it? What score would cross the next band, and what additional evidence would be needed to claim a real workflow change?

3. In the same file, cycle chaos-003 records, in `metafixes_applied`, a new policy file and a section added to an existing policy, and in `level_deltas` a gain at level L4, while R rose from 0.64 (chaos-002) to 0.73. Compute the aggregate return of that cycle's changes. Why can the 0.09 rise not be credited to the new policy alone, and what observation would isolate its return? Between chaos-003 and chaos-004, R rose to 0.82 without a new policy file: what does that say about measuring returns per policy count?

4. **Thought experiment:** If all three consumer repos (ix, tars, ga) suddenly report 100% compliance, does that establish a phase transition or even a real improvement? What evidence would you request?

> **Answer to 4:** No. Check the denominator and policy versions, whether tests changed, whether exceptions disappeared from the records, and whether independent outcomes improved. The reported jump alone does not classify a physical or governance transition.

---

## Key Takeaways

- A qualitative workflow shift alone does not establish a physical phase transition or a predictive law
- Five proposed signals can be inspected in existing records; requisite variety remains an unmeasured sixth candidate
- A variety measure needs matched disturbances, responses, and outcomes before it can be tested as a transition signal
- No physical transition order or advance-warning threshold has been established for governance changes here
- Inspect several independently measured indicators and outcomes; the “3+ signals” rule is unvalidated

## Further Reading

- [PSY-001: Introduction to Fractal Compounding](psy-001-intro-fractal-compounding.md) — prerequisite on D_c and ERGOL/LOLLI
- [CYB-003: Measuring Requisite Variety Without Inventing Capacity](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) — the measurement limits and proposed experiment
- [CYB-001: VSM and AI Governance Mapping](../../cybernetics/en/cyb-001-vsm-ai-governance-mapping.md) — structural prerequisites
- Statistical mechanics of phase transitions (Landau theory, order parameters, critical exponents)
- Asimov's Foundation — psychohistory predicts aggregate trends, not individual events

---
*Produced by Seldon Auto-Research psychohistory-2026-03-23-001 on 2026-03-23.*
*Research question: What measurable signals in file-based AI governance state indicate that a governance system is approaching a phase transition?*
*Belief: T (confidence: 0.80) — Claude + GPT-4o agreement, NotebookLM unavailable*
