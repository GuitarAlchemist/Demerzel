---
module_id: psy-019-combining-correlated-forecasters
department: psychohistory
course: "Combining Forecasters Who Share a Source"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-019
version: "0.1.0"
---

# Combining Forecasters Who Share a Source

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will write the mean squared error of an average of k forecasts with correlated errors, find the floor that no head count gets under, compare one more forecaster of the same kind with one from another source, and say what agreement shows. **Project question:** does averaging the judgments of several agents help when they read the same context?

[PSY-016](psy-016-brier-score.md) scores one forecast; this module scores an *average of forecasts* with the arithmetic of [PSY-004](psy-004-how-large-is-large.md).

## 1. What the judges share

**Observed** at the pinned commit, and snapshotted by [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/extract.py) into [`observed-input.json`](../../../fixtures/psychohistory/psy-019/observed-input.json):

- The [multi-model orchestration policy](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/multi-model-orchestration-policy.yaml#L198-L203) sets `single_model: max 0.8`, `two_model_agreement: 0.9` and `two_model_disagreement: 0.5`. Its `cross-validation` rule requires agreement from at least two models and names claude and chatgpt, which its model registry assigns to two providers.
- The [tribunal-panel script](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) would send one pull request to 5 personas. Every prompt carries the same title, body, file list and diff excerpt; only the persona and its stated concern differ, and the workflow passes one `--model`. Each persona returns `block`, `merge_with_followups` or `pass`, and may return a `score`, "0..1 confidence in this PR for my concern (1 = clean)"; the verdict is strictest-wins, not an average.
- The [council script](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py#L12-L35) pairs a static analyzer's check with a model's review, two reviewers it calls "deliberately heterogeneous", and keeps the minimum of their scores; a two-review verdict, it says, "lifts the single-model confidence cap honestly", an assumption no file measures.

None of them holds a persona's answer or an outcome; the council's five recorded verdicts hold nine scores (reviewer_a's is 0.75 every time) and no outcome. **No correlation between the project's agents has been measured: not by this module, and not in any file it read.** Everything below is **synthetic**.

A *forecast* is a number stated before the outcome is known; its *error* is the forecast minus the outcome. The model gives forecaster i the error

```text
error_i = bias + sigma × ( sqrt(rho) × C + sqrt(1 − rho) × I_i )
```

C, the *common part*, is drawn once per occasion and shared by all; I_i, the *individual part*, is drawn for each forecaster; both have mean 0 and variance 1. Each error then has variance sigma², and two errors have correlation rho, the common share of that variance. Agents can share the *context* (what the excerpt omits, every reader misses) and the *model* (the habits of one set of weights); one scenario splits rho = 0.6 into 0.3 for each, an invented split. Everyone forecasting one event also shares what nobody could foresee in its outcome: no head count or other source removes it, and it inflates the correlation of errors scored against outcomes. Until section 4's last paragraph, errors are measured from the best possible forecast, without it.

### Practice Exercise 1

Under that split, give the error correlation between a persona of the panel and (a) another persona of the panel; (b) a reviewer on another model reading the same excerpt; (c) a second run of the panel's model given other material; (d) a reviewer on another model given other material. Which case is a sixth persona?

> **Answer:** (a) Both parts are common: `0.3 + 0.3 = 0.6`. (b) The context only: 0.3. (c) The model only: 0.3. (d) Nothing: 0. A sixth persona is case (a): one more forecaster, the same rho. These values classify sources; they measure nothing.

## 2. The variance of an average

Take bias = 0. The *mean squared error* (MSE), the average of the squared error over many occasions, is then the error variance. An average of k forecasts leaves the common part untouched, while the mean of k individual parts has variance 1/k:

```text
MSE of the average of k forecasts = sigma² × ( rho + (1 − rho) / k )
floor, however large k            = rho × sigma²
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/analyze.py) checks it without sampling: with parts of +1 or −1, all 32,768 sign patterns for k = 14 give the averages of C², C × mean(I) and mean(I)² as exactly 1, 0 and 1/k.

**Computed from the closed form**, in units of one forecaster's MSE (sigma² = 1), four decimals:

| Forecasters k | rho = 0 | rho = 0.3 | rho = 0.6 | rho = 0.9 |
|---|---|---|---|---|
| 5 | 0.2 | 0.44 | 0.68 | 0.92 |
| 14 | 0.0714 | 0.35 | 0.6286 | 0.9071 |
| floor | 0 | 0.3 | 0.6 | 0.9 |
| 14, simulated | 0.0716 | 0.3504 | 0.6284 | 0.9061 |

**Synthetic check.** The last row comes from 200,000 seeded occasions with uniform parts. In all 56 cells (k = 1 to 14) the simulation is within 1.02 standard errors of the closed form, and at least 82.26 from sigma²/k in the 39 cells with rho > 0 and k ≥ 2.

### Practice Exercise 2

Five forecasters have rho = 0.3. Compute the MSE of their average and that of five independent forecasters. Of what averaging can ever remove, how much have the five removed?

> **Answer:** `0.3 + 0.7 / 5 = 0.44`, against `1 / 5 = 0.2`. The floor is 0.3, so averaging can remove at most `1 − 0.3 = 0.7`; the five have removed `1 − 0.44 = 0.56`, and `0.56 / 0.7 = 80%`. That share is `1 − 1/k` at any rho: correlation does not slow the averaging, it shrinks what there is to average away.

## 3. Head count against another source

Call *worth* the number of independent forecasters whose average has the same MSE: `k / (1 + (k − 1) rho)`, never more than `1 / rho` (Clemen and Winkler 1985). It is PSY-004's effective sample size, applied to errors: fourteen forecasters are worth 2.857 at rho = 0.3, 1.591 at 0.6 and 1.102 at 0.9.

One more forecaster of the same kind lowers the MSE by `sigma² (1 − rho) / (k (k − 1))`: from 13 to 14 at rho = 0.6, by 0.002198, or 0.35% (7.14% for independent forecasters).

**Synthetic.** Thirteen forecasters at rho = 0.6 (MSE 0.6308), then a fourteenth of the same accuracy:

| The fourteenth shares | Correlation with a panel member | MSE, equal weights | MSE, best weights |
|---|---|---|---|
| context and model | 0.6 | 0.6286 | 0.6286 |
| one of the two | 0.3 | 0.5888 | 0.5246 |
| neither | 0 | 0.5490 | 0.3868 |

*Best weights* minimise the MSE of the weighted average (Bates and Granger 1969). With v the MSE of the panel's average, c the newcomer's correlation with a panel member and sigma² = 1:

```text
weight of the newcomer = (v − c) / (v + 1 − 2c)        MSE = (v − c²) / (v + 1 − 2c)
```

A fourteenth with nothing in common lowers the MSE by 12.97% with one vote in fourteen and by 38.68% with its best weight, 0.3868 (with c = 0, weight, MSE and drop coincide): the thirteen are worth 1.585 forecasters and it adds one.

### Practice Exercise 3

A panel of 5 has rho = 0.6. Option A: grow it to 14 of the same kind. Option B: keep 5 and add one independent forecaster of the same accuracy. Compute the MSE of A, of B with equal weights, and of B with the best weight.

> **Answer:** A: `0.6 + 0.4 / 14 = 0.6286`. B with equal weights: the five contribute `5 + 5 × 4 × 0.6 = 17` variances and covariances, the outsider 1 and no covariance, so `18 / 6² = 0.5`. B with the best weight: `v = 0.6 + 0.4 / 5 = 0.68` and `c = 0`, so the weight is `0.68 / 1.68 = 0.4048` and the MSE 0.4048. One outsider with one vote in six beats nine more insiders, and goes under their floor of 0.6.

## 4. What an average cannot remove, and what agreement shows

**A shared bias.** If every forecaster leans the same way, the MSE of the average is `bias² + sigma² (rho + (1 − rho) / k)`. **Synthetic**, with bias = 0.5 and rho = 0.3: 1.25 for one forecaster, 0.6 for fourteen, above a floor of 0.55. A bias can be estimated from scored forecasts and subtracted; the common part changes with each occasion and cannot.

### Practice Exercise 4

With bias = 0.5 and rho = 0.3, a team of 14 can either double to 28, or score its past forecasts and subtract the bias it finds. Which lowers the MSE more?

> **Answer:** Now: `0.25 + 0.3 + 0.7 / 14 = 0.6`, of which the bias is `0.25 / 0.6 = 41.67%`. Doubling: `0.25 + 0.3 + 0.7 / 28 = 0.575`, 4.17% lower. Subtracting the bias: `0.3 + 0.7 / 14 = 0.35`, 41.67% lower. Subtracting wins, if the bias is stable and known.

**Agreement.** The *spread* of a panel, the mean squared distance of its forecasts from their own average, needs no outcome. But the common part cancels from it: its expected value is `sigma² (1 − rho) (k − 1) / k`. With k = 14 and rho = 0.9, the forecasts sit 0.30 from their average while that average sits 0.95 from the best forecast (root mean squares); at rho = 0 the figures are 0.96 and 0.27. **Of two panels of equally accurate forecasters, the one that agrees more closely has, in expectation, the less accurate average.**

**A reading that the policy does not state.** Take 0.8 as the probability p that a model is right on a yes/no question, and rho as the correlation between "model 1 is right" and "model 2 is right". Two wrong answers to a yes/no question coincide, so, with q = 1 − p,

```text
P(right | the two agree) = (p² + rho p q) / (p² + q² + 2 rho p q)
```

That is 0.941 at rho = 0, 0.844 at 0.6 and 0.8 at 1, and the policy's 0.9 exactly at rho = 7/32 = 0.21875. When the two disagree, each is right half the time at any rho: the policy's 0.5.

### Practice Exercise 5

Two personas of the panel, on one excerpt and one `--model`, agree on whether to block (a yes/no reading of their three verdicts), and a colleague applies the policy's 0.9. Under the reading above, compute what their agreement is worth at rho = 0 and at rho = 0.6, then decide.

> **Answer:** At rho = 0: `0.64 / 0.68 = 0.941`. At rho = 0.6: `(0.64 + 0.6 × 0.16) / (0.68 + 2 × 0.6 × 0.16) = 0.736 / 0.872 = 0.844`. Decision: not supported. The 0.9 needs a rho of at most 0.21875; the policy's rule pairs models from two providers, which these personas are not; and nobody has measured rho for either pair.

**The strongest objection to this reading** is that every rho here is invented. The personas judge different concerns; if that makes their errors nearly independent, five of them remove 80% of one persona's MSE (section 2). One shared excerpt argues for a high rho, different instructions for a low one: **this module cannot tell a rho of 0.1 from a rho of 0.9.** Outcomes alone do not settle it. **Synthetic**: on a yes/no question whose true probability lies between 0.3 and 0.7, five personas miss it by 0.21 (standard deviation); 84% of one persona's MSE is the unforeseeable part, and `1 − (k / (k − 1)) × spread / error variance` tends to 0.843 for personas sharing nothing, 0.937 at rho = 0.6 (90% of 1,000 logs of 20 pull requests: 0.79 to 0.87, and 0.91 to 0.95).

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the files linked in section 1, the [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) that runs the panel, and the council's five records. `extract.py` stops if one of them differs from its pinned Git blob.

**Fixture.** From the repository root, `python -I -B scripts/streeling_fixtures/psychohistory/psy-019/extract.py`, then `analyze.py` and `analyze.py --check` in the same folder. Assumptions: [`scenarios.json`](../../../fixtures/psychohistory/psy-019/scenarios.json). Every number above: [`results.json`](../../../fixtures/psychohistory/psy-019/results.json). Self-checks and limits: [README](../../../fixtures/psychohistory/psy-019/README.md).

**Method references.** Bates, J. M., and Granger, C. W. J. (1969), "The Combination of Forecasts", *Operational Research Quarterly* 20(4), 451–468, doi:10.1057/jors.1969.103. Clemen, R. T., and Winkler, R. L. (1985), "Limits for the Precision and Value of Information from Dependent Sources", *Operations Research* 33(2), 427–442, doi:10.1287/opre.33.2.427.

**Not done.** No agent was run and no outcome was read: the correlation between the project's agents is unknown. The model gives every forecaster the same accuracy and every pair the same correlation, and draws light-tailed errors, which flatters the sizing above. The panel's strictest-wins rule and the council's minimum are not modelled. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** On each pull request, ask every persona and one *outsider*, an agent on another model given other material, for the probability of a yes/no event (a revert within a month), and record the outcome. The unforeseeable part cancels in `(persona–persona covariance − persona–outsider covariance) / (persona variance − persona–outsider covariance)`, which tends to rho if the outsider shares nothing else with the panel (less if it shares context or model, more if its errors run against the panel's; the log cannot tell). In the synthetic setting, 500 pull requests separate rho = 0 from 0.6 (90% of logs: −0.22 to 0.15, and 0.49 to 0.67); 100 do not. Unlike PSY-004's log, this one needs outcomes. An estimate near 0 would make five personas worth five forecasters; one near 0.6, worth 1.471, and the next agent should read something else.
