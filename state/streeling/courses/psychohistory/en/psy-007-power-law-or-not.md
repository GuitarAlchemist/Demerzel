---
module_id: psy-007-power-law-or-not
department: psychohistory
course: "Is It a Power Law? Eighteen Citation Counts"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-007
version: "0.1.0"
---

# Is It a Power Law? Eighteen Citation Counts

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will read a rank-size list, see why a straight log-log line is not evidence of a power law, estimate an exponent by maximum likelihood above a stated cut, compare the power law with two simpler families, and say what so small a sample can distinguish. **Project question:** the department lists "power law dynamics" in artifact effectiveness; do the latest citation counts support a power law over simpler alternatives?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) defines a compounding dimension, `D_c = log(value_ratio) / log(scale_ratio)` (its line 66): the exponent of a power-law relation between two quantities, whereas this lesson asks how many items have each size. Neither PSY-001 nor [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) uses the term. [PSY-009](psy-009-concentration-and-heavy-tails.md) measures concentration without assuming a family.

## 1. What the record says, and what the eighteen numbers are

**Observed.** The [department record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) mentions power laws three times, always as a topic: the research areas "Fractal compounding analysis — measuring D_c, power laws, learning momentum" ([line 10](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L10)) and "Power law dynamics — Pareto/Zipf distributions in artifact effectiveness" ([line 17](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L17)), and the curriculum entry "Power Law Detection: identifying Pareto distributions in governance data" ([line 26](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L26)). None names a data set or a test. The specification that PSY-001 [cites first](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md#L173) names both: "If the top 20% of governance artifacts account for more than 60% of citations, a power law is present" ([line 56](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56)), on the evolution records' citation counts ([line 60](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L60)). That is a share threshold, not a fit.

A *power law* gives a value x a probability proportional to `x^-alpha`, with *exponent* alpha (Pareto and Zipf distributions are of this kind): values far above the typical one stay likely.

In the quality trend, "effectiveness" is a categorical label ([PSY-005](psy-005-persistence-baseline.md)); the rule, and this lesson, use `citation_count`: the number of tracked files that mention one of the artifact's *citation paths*, counted with `git grep` ([`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15)).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/extract.py) snapshots the latest run at commit `4b03838` (2026-10-13T18:43:54Z, [18 rows](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl#L217-L234)) into [`observed-input.json`](../../../fixtures/psychohistory/psy-007/observed-input.json). Sorted, with a star on the two counts that were not measured:

```text
65  55*  47  45  44  29  29  23  17  15  14  13  6  6  5  1  0  0*
```

The sum is 414. Three facts limit what follows:

- **Sixteen measurements, not eighteen.** The starred 55 and zero have no `citation_source` and no citation path, which marks an artifact that "[lives outside this repository (unmeasurable here)](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23)"; both kept a hand-typed value.
- **Dependent counts.** The two 29s share nearly all their citing files: one artifact lists the other among its citation paths; and one file can cite several artifacts.
- **A match, not a use.** The search is for a literal string ([lines 76–86](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L76-L86)): a file that only lists an artifact's path is counted like one that uses it.

A power law gives no probability to 0: the two zeros are set aside and 16 positive counts remain.

### Practice Exercise 1

How many values can enter a log-log plot, how many of those were measured by git grep, and how many separate measurements is that at most?

> **Answer:** `18 − 2 = 16` positive counts enter the plot. The starred 55 is hand-typed: `16 − 1 = 15` git-grep measurements. The two 29s count nearly the same files: at most `15 − 1 = 14` separate measurements.

## 2. A straight line on log-log paper

On a *rank-size plot*, `log10(count)` is drawn against `log10(rank)`, largest count first. Under a power law with exponent alpha the points lie near a line of slope `−1 / (alpha − 1)`. The tempting recipe: fit a least-squares line, read `alpha = 1 + 1 / |slope|`, and quote R², the share of variance the line accounts for. **Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/analyze.py) on the 16 positive counts: slope −1.152, R² 0.669, implied exponent 1.868.

**Synthetic.** The script draws 2,000 samples of 16 values from each of the three families fitted in section 4 ([`scenarios.json`](../../../fixtures/psychohistory/psy-007/scenarios.json) stores their parameters as assumptions) and fits the same line:

| Generating family | Median R² | R² at least 0.9 |
|---|---|---|
| Power law | 0.946 | 81.8% |
| Lognormal | 0.88 | 40.0% |
| Exponential | 0.776 | 7.3% |

Clauset, Shalizi and Newman (2009, Appendix A) note that "in practice we rarely see a low r², regardless of the actual form of the distribution, so that the value of r² tells us little." Here the low value is the informative one: 1,989 of the 2,000 power-law samples reach the recorded 0.669.

### Practice Exercise 2

(a) The line has slope −1.152: compute the exponent it implies. (b) A colleague's 16 counts give an R² above 0.9. What does the table say about their family?

> **Answer:** (a) `1 + 1 / 1.152 = 1.868`. (b) Very little: an R² of 0.9 or more occurs in 81.8% of the power-law samples, but also in 40.0% of the lognormal and 7.3% of the exponential ones. Only a low value discriminates: all but `2,000 − 1,989 = 11` power-law samples reach 0.669.

## 3. The exponent by maximum likelihood, above a stated cut

*Maximum likelihood* picks the exponent under which the observed values are most probable. A power law is fitted to a *tail*, the values at or above a cut `x_min`, and a fit must state the cut and how many values remain.

```text
continuous:  alpha = 1 + n / sum of ln(x / x_min)      standard error = (alpha - 1) / sqrt(n)
discrete:    p(x) = x^-alpha / zeta(alpha, x_min)      alpha: model mean of ln x = sample mean of ln x
```

`zeta(alpha, x_min)` is the sum of `k^-alpha` over the integers `k >= x_min`. These counts are few, small integers, so this lesson fits the **discrete** form; the continuous formula treats integers as points on a continuum and can be computed by hand. It gives an exponent 0.055 higher at the cut 1 and 0.059 at the cut 13; no conclusion below depends on the choice.

**Computed** (KS, the *Kolmogorov–Smirnov distance*: the largest gap between the cumulative shares of the data and of the fitted law):

| Cut `x_min` | Values kept | Exponent | Standard error | KS |
|---|---|---|---|---|
| 1 | 16 | 1.297 | 0.075 | 0.395 |
| 13 | 12 | 2.21 | 0.349 | 0.214 |
| 44 | 5 | 7.602 | 2.955 | 0.174 |

Over the ten cuts tried the exponent runs from 1.297 to 7.602: it describes the cut as much as the data. The cited paper's rule, the smallest KS distance, picks 44, a "tail" of five numbers. This lesson reports the cuts 1 (every positive count) and 13 (that rule among cuts keeping at least 10 values, a floor chosen after seeing the counts).

**Synthetic.** In 2,000 tails of 12 values drawn from a power law of exponent 2.21, 95% of the fitted exponents lie between 1.729 and 3.339.

### Practice Exercise 3

At the cut 13, 12 values remain and the sum of `ln(x / 13)` is 9.459. Compute the continuous exponent and its standard error; compare with the discrete fit.

> **Answer:** `alpha = 1 + 12 / 9.459 = 2.269`, and `(2.269 − 1) / sqrt(12) = 0.366`. The discrete fit gives 2.21 with a standard error of 0.349: the forms differ by 0.059, about a sixth of either standard error.

## 4. Simpler alternatives, and what eighteen counts can tell

Two simpler families live on the same integers: a discrete *exponential* (each extra unit multiplies the probability by a constant; no heavy tail) and a *lognormal* (`ln x` is normally distributed; rounded up to an integer here; two parameters). A fitted family's *log-likelihood* is the logarithm of the probability it gives to the data; higher is better. R is one family's log-likelihood minus another's (negative: the second fits better), and Vuong's test (1989, as the cited paper applies it) gives the chance of a ratio this far from zero if both fit equally well; the paper trusts the sign when p < 0.1, which this lesson calls decisive.

**Computed** log-likelihoods, from [`results.json`](../../../fixtures/psychohistory/psy-007/results.json):

| Values | Power law | Exponential | Lognormal |
|---|---|---|---|
| All 16 positive counts | −80.97 | −67.74 | −69.93 |
| The 12 counts of 13 or more | −49.96 | −48.24 | not fitted |

Over all positive counts the power law is the worst of the three, decisively: R = −13.23 against the exponential (p < 0.0001) and −11.04 against the lognormal (p = 0.012). Exponential and lognormal are not separated (R = 2.19, p = 0.1779). A goodness-of-fit test agrees: the recorded KS distance, 0.395, exceeds that of all 2,000 synthetic samples from the fitted power law.

On the tail above 13 nothing is decided: R = −1.71 against the exponential (unrounded; p = 0.2557), and the power law is not ruled out either (501 of 2,000 synthetic tails lie at least as far from their fit, p = 0.2505, above the paper's 0.1). Yet at the cuts 15 and 17 the exponential wins decisively (p = 0.0832 and 0.0364).

**Synthetic: what can so few values distinguish?** Among samples of 16 values, the generating family has the highest likelihood in 3,785 of 6,000, 63.1%. The recorded counts put the exponential on top; that happens in 2 of 2,000 samples from the power law. On the tail, with a power law (alpha 2.21) and an exponential (mean 33) above 13 as generators:

| Tail values | Power law: right sign / and decisive | Exponential: right sign / and decisive |
|---|---|---|
| 12 | 66.2% / 27.0% | 92.2% / 48.6% |
| 50 | 96.4% / 66.0% | 98.7% / 74.5% |
| 200 | 100.0% / 99.3% | 100.0% / 99.3% |

**Answer to the project question:** no. Read as 16 independent draws, the counts rule out a power law that starts at 1; on the 12 counts of 13 or more, **this sample cannot distinguish a power law from an exponential**.

### Practice Exercise 4

Classify the four comparisons at the cuts 1 and 13 with the 0.1 rule, then say which sentence the results support: "the counts follow an exponential law", "the counts do not follow a power law over their full range", or "the tail follows a power law".

> **Answer:** On all positive counts, power law against exponential (p < 0.0001) and against lognormal (p = 0.012): decisive, against the power law. The other two (p = 0.1779 and p = 0.2557): undecided. Only the second sentence is supported. The first fails because the lognormal stays in play; the third because "not ruled out" is weaker than "supported".

**The strongest objection to this reading** is that it describes the instrument as much as the artifacts ([PSY-011](psy-011-measurement-change-or-system-change.md)). Until 2026-09-13 the counts were [typed by hand](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8). In the last run before git grep the same artifacts read 55, 12, 11, 8, 5, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1, 0, 0: R² is 0.959, no likelihood comparison is decisive (against the exponential: R = 1.27, p = 0.7688), and the goodness-of-fit p-value is 0.0805, already under 0.1 (today: 0 of 2,000). The project's own rule flips with the instrument: the three or four largest counts (20% of 18 is 3.6) held 67.2% or 74.1% of citations, a power law by its 60% line, and hold 40.3% or 51.2% now. Dropping the two hand-typed counts changes little (R = −12.08 against the exponential, p = 0.0001).

### Practice Exercise 5

You may measure more artifacts. From the tail table, how many tail values do you ask for, and which results would make you accept "power law" for the tail?

> **Answer:** About 200, calibrated against an exponential only: a decisive, correct verdict arrives in 66.0% and 74.5% of samples at 50 values, in 99.3% at 200. Accept only with a stated cut and tail size, a goodness-of-fit p-value above 0.1, and R favouring the power law over both alternatives with p < 0.1.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** `extract.py` reads 27 files (five quality-trend files, the 18 records of [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution), the department record, the specification, PSY-001 and PSY-002) and stops if one differs from its pinned Git blob. The [README](../../../fixtures/psychohistory/psy-007/README.md) gives the commands, the 46 self-checks and the negative controls.

**Method references.** Clauset, A., Shalizi, C. R., and Newman, M. E. J. (2009), "Power-law distributions in empirical data", *SIAM Review* 51(4), 661–703, [arXiv:0706.1062](https://arxiv.org/abs/0706.1062): the method followed here; it warns that data sets under about 50 values "should be treated with caution". Vuong, Q. H. (1989), "Likelihood Ratio Tests for Model Selection and Non-Nested Hypotheses", *Econometrica* 57(2), 307–333.

**Not done.** The goodness-of-fit test holds the cut fixed, where the cited paper re-estimates it in every synthetic sample: 0.2505 is probably too lenient. Not fitted: a lognormal on the tail, a power law with a cut-off. Every p-value treats the counts as independent draws from one distribution; they are neither independent nor a sample of the governed files, only the 18 with an evolution record. Vuong's p-value is a large-sample approximation, used here on 16 and 12 values. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Apply the git-grep rule to every tracked file and rerun. A tail of about 200 values that passes the goodness-of-fit test and beats both alternatives decisively would change the conclusion to "a power law is plausible in the tail".
