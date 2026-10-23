---
module_id: psy-006-transition-matrix-from-counts
department: psychohistory
course: "Estimate a Transition Matrix from Observed Counts"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "mat-020-markov-chains-hmm"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-006
version: "0.1.0"
---

# Estimate a Transition Matrix from Observed Counts

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will turn a log of labels into a matrix of counts, estimate transition probabilities from it, bound a transition that was never observed, and say what smoothing and a uniform matrix add to the data. **Project question:** the repository stores a uniform 4-state governance transition matrix with no observations; what does a matrix estimated from the label transitions we do have look like, and what can it not say?

[PSY-005](psy-005-persistence-baseline.md) scored the forecast "nothing changes" on these labels; this module bounds the chance of change it left open. Stationary distributions and hitting times come from [MAT-020](../../mathematics/en/mat-020-markov-chains-hmm.md).

## 1. Count the transitions, then divide

**Observed.** A daily job runs [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), the *feeder*: it appends one row per governance *artifact* (a policy, a schema, a skill) to [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), and the rows of one execution form a *run*. Each row carries `effectiveness_to`, the truth value given to a written proposition about the artifact: T (true), P (probable), U (unknown), D (doubtful), F (false) or C (contradictory). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/extract.py) snapshots the five files at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-006/observed-input.json): 1,548 rows, 88 runs, 18 artifacts.

A *transition* is a consecutive-row pair, as in PSY-005: one artifact's label in a row and in its next row. That gives 1,548 − 18 = 1,530 row pairs; one starts at an unlabelled row, leaving **1,529**. The *count matrix* holds the number of pairs from each label (row) to each label (column):

```text
from \ to     T     P     U     D     F     C    pairs
T           775     0     0     0     0     0      775
P             0   406     0     0     0     0      406
U             0     0   174     0     1     0      175
D             0     0     0     0     0     0        0
F             0     0     0     0    86     0       86
C             0     0     0     0     0    87       87
```

**Computed.** Treat the labels as a *Markov chain*: the next label depends only on the current one, through a fixed matrix of probabilities, the same for every artifact. The *maximum-likelihood estimate*, the matrix that makes the observed pairs most probable, is each row of counts divided by its total (Anderson and Goodman 1957):

```text
estimate p(a→b) = n_ab / n_a      n_ab = pairs from a to b, n_a = pairs starting at a
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/analyze.py) writes it to [`results.json`](../../../fixtures/psychohistory/psy-006/results.json): 1 on the diagonal for T, P, F and C, 174/175 = 0.994286 for U→U and 1/175 = 0.005714 for U→F. Read literally, the matrix says that four labels never change and that an unknown label waits 175 pairs on average, then always turns false. All of it rests on one pair.

A matrix also belongs to one step length, and these pairs mix at least two. 1,518 pairs join two consecutive feeder runs (gaps of 0.001 to 6.453 days, median 0.999). The other 11 start at a *seed row* (flagged `baseline: true`, stamped 2026-05-01) and end at the first feeder run, 78.5 days later; the single change, U to F, is one of them. Between feeder runs the estimate is the identity matrix on five labels.

### Practice Exercise 1

From the count matrix, estimate row U. What is the estimate for row D? What does row U become on the 1,518 pairs between feeder runs, where it has 172 pairs and no exit?

> **Answer:** `174 / 175 = 0.994286` for U→U, `1 / 175 = 0.005714` for U→F, 0 elsewhere. Row D is `0 / 0`, undefined: the data are silent, which is not an estimate of zero. Between feeder runs the row is `172 / 172 = 1` for U→U: the matrix's only off-diagonal estimate comes from a 78.5-day pair.

## 2. Bound what was never observed

A zero count does not make a probability zero. A transition with probability p at each of n independent trials stays unseen, a *clean* record, with probability (1 − p)^n. The *upper bound* is the largest p that a clean record does not reject at the 5% level:

```text
(1 − p)^n = 0.05   →   exact 95% upper bound = 1 − 0.05^(1/n)
rule of three: about 3 / n, since −ln 0.05 = 2.9957
```

The *rule of three* is the shortcut described by Hanley and Lippman-Hand (1983). **Computed** for leaving each label, one pair counting as one trial:

| Label left | Clean pairs | Exact bound | 3/n |
|---|---|---|---|
| T | 775 | 0.386% | 0.387% |
| P | 406 | 0.735% | 0.739% |
| C | 87 | 3.385% | 3.448% |
| F | 86 | 3.423% | 3.488% |
| any label, between feeder runs | 1,518 | 0.197% | 0.198% |

Row U has one exit in 175 pairs; its bound, 2.682%, is the p at which "at most one exit in 175 pairs" has probability 0.05 (Clopper and Pearson 1934). Row D has no trial, hence no bound below 100%. The rule of three exceeds the exact bound by 1.9% of that bound at 86 pairs and by 15.9% at 10 trials.

The bounds are one-sided ([PSY-004](psy-004-how-large-is-large.md) and [PSY-013](psy-013-four-scores-and-a-trend.md) use the two-sided interval, 0.025 in each tail) and taken one row at a time; together they hold at less than 95%. **The strongest objection** is the word "independent". A label is a written assessment that changes only when its record is edited, and one sitting may cover many artifacts. At one extreme of dependence between artifacts, where the labels of a run change together or not at all, a run is one trial: the 86 steps between feeder runs then bound the chance of change at 3.423% per pair, not 0.197%. If instead each artifact's label is one assessment, the trials are the artifacts: row T has nine and rows F and C one each; 0 of 9 left T, a bound of 28.313% over the whole record, and one artifact gives no bound below 95%. This sample cannot place the truth; the edit history of `state/evolution/`, where the assessments are written, would show how labels are revised.

### Practice Exercise 2

Compute the exact bound and the rule of three for leaving F (86 pairs, no exit). A colleague concludes that "F is final". What do the data support?

> **Answer:** `1 − 0.05^(1/86) = 0.034234` and `3 / 86 = 0.034884`. The data support "the chance of leaving F at one pair is below 3.423%, at the 95% level, if the 86 pairs are independent trials", not "F is final". The 86 pairs are one artifact read on 87 consecutive runs: counted as one assessment, they give no bound below 95%.

## 3. Smoothing is a prior, and a prior is a claim

*Add-one smoothing* adds a pseudo-count of 1 to every cell before dividing, so that no estimate is zero:

```text
smoothed p(a→b) = (n_ab + 1) / (n_a + k)      k = number of labels, here 6
```

It is the average of the matrices still plausible after the data when, before them, every set of row probabilities was held equally plausible: a *uniform prior*. **Computed:**

- Row D, no pairs: every destination gets 1/6. Without data, add-one returns the uniform row.
- Row U among the 11 seed-row pairs (2 stay, 1 goes to F): staying falls from 2/3 to (2 + 1)/(3 + 6) = 1/3, and 4/9 of the probability lands on four destinations never observed.
- Row T, 775 pairs: leaving gets 5/781 = 0.64%, above the 0.386% bound.

For every clean row of 5 to 2,000 pairs, add-one over six labels claims more exits than the row allows at the 95% level; a pseudo-count of 0.5 never does in that range. The pseudo-counts on the five exits, 5 or 2.5 against the rule's 3, decide this, not the data.

**Observed.** The repository holds a seed table over these six letters: the `belief_hexavalent` machine of [`state/driver/transition-weights.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L22). It keeps T with weight 0.9 and [lists U→F as forbidden](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L49). **Computed under an assumption the file does not state**, that one table step is one pair: the table expects 492.4 changed labels among the 1,518 pairs between feeder runs, where none occurred. The one change on record, U→F, is a jump the table forbids in one step (0.0825 in two, through D or C); a 78.5-day pair cannot show how many steps it spanned. A nearly empty count matrix can thus still rule out a candidate at a stated step length. Read as a prior, a zero is the opposite of add-one's excess: no amount of data can raise it.

### Practice Exercise 3

Apply add-one over six labels to row F (86 pairs, all F→F): give the smoothed probabilities of staying and of leaving, and compare the latter with Exercise 2's bound.

> **Answer:** Staying: `(86 + 1) / (86 + 6) = 87/92 = 0.945652`. Each other label gets `1/92`, so leaving gets `5/92 = 0.054348`, or 5.435%, above the 3.423% bound: the smoothed row asserts more change than its own 86 pairs allow at the 95% level.

## 4. What the stored uniform matrix asserts

**Observed.** [`state/markov/transition-matrix.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/transition-matrix.json) has four states, Healthy, Watch, Warning and Freeze, and 0.25 in every cell; its note begins "Uniform prior — no observations yet." [`predictions.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/predictions.json) holds an empty list, and the `engine-state.json` named by the note is not in the folder. The [specification](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L29) assigns one of the four states to each governance cycle as a whole, from a resilience score and an artifact-inflation ratio (LOLLI/ERGOL) alone.

**Computed.** This is row D again: add-one without data, with k = 4. All rows being equal, the next state does not depend on the current one. From Healthy, a Freeze has probability 0.25 at the next cycle, 0.578125 within 3 cycles and 0.943686 within 10; the expected wait for the first Freeze is 4 cycles, and in the long run a quarter of all cycles are frozen. The specification's formula, [`cycles_to_freeze = log(0.5) / log(P(not_freeze))`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L151), gives 2.409 cycles for P(not_freeze) = 0.75 (where the chance of a Freeze reaches one half, not the mean wait), while its [alert](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L168), raised "When P(Freeze) > 0.3", stays silent.

**Synthetic.** [`scenarios.json`](../../../fixtures/psychohistory/psy-006/scenarios.json) defines an imaginary "sticky" matrix that keeps each state with probability 0.97 and spreads the rest evenly. Its stationary distribution is the same, yet a Freeze within 10 cycles has probability 0.095618 and the expected wait is 100 cycles. Long-run shares do not identify a matrix; the uniform one is the memoryless member of that family, a specific claim and not a neutral one.

**Two state spaces.** The labels describe 18 artifacts; the governance states describe the whole system, one per cycle. No label enters that classification, so the label counts say nothing about Healthy→Freeze. A recorded state per cycle would: 59 transitions out of Healthy, none into Freeze, would bring the bound on that transition down to 5%. None is recorded: the prediction log is empty.

### Practice Exercise 4

Starting in Healthy, compute the probability of a Freeze within 3 cycles and the expected wait for the first Freeze, under the stored matrix and under the sticky one (each other state: 0.01).

> **Answer:** Stored: every cycle is a Freeze with probability 0.25, so `1 − 0.75^3 = 37/64 = 0.578125` and the wait is `1 / 0.25 = 4` cycles. Sticky: from any other state a Freeze has probability 0.01, so `1 − 0.99^3 = 0.029701` and `1 / 0.01 = 100` cycles.

### Practice Exercise 5

A teammate wants to fill the governance matrix from the label matrix: "labels almost never change, so Healthy stays Healthy". Accept or reject, with your criterion. How many consecutive cycles without a Freeze would reject the stored 0.25 at the 5% level?

> **Answer:** Reject. A count is evidence only for the state space and the step it was counted in: the labels are truth values of 18 artifacts, the governance states classify the whole system once per cycle, and the specification classifies a cycle without any label. `0.75^10 = 0.056314` is above 0.05 and `0.75^11 = 0.042235` is below: 11 consecutive cycles without a Freeze.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the five quality-trend files, two of the three `state/markov/` files, the specification and the seed table linked above. The fixture's [README](../../../fixtures/psychohistory/psy-006/README.md) gives the commands and the checks.

**Method references.** Anderson, T. W., and Goodman, L. A. (1957), "Statistical Inference about Markov Chains", *Annals of Mathematical Statistics* 28(1), 89–110, [doi:10.1214/aoms/1177707039](https://doi.org/10.1214/aoms/1177707039). Hanley, J. A., and Lippman-Hand, A. (1983), "If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators", *JAMA* 249(13), 1743–1745, [doi:10.1001/jama.1983.03330370053031](https://doi.org/10.1001/jama.1983.03330370053031). Clopper, C. J., and Pearson, E. S. (1934), "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial", *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).

**Not done.** No governance state was classified, so nothing about the 4-state matrix was tested, although the classifier's inputs were recorded a few times: [four resilience scores](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json), which PSY-013 reads, and [one ratio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json). The Markov assumption and the constancy of the matrix over time were not tested: one change gives nothing to test them on. Scoring probability forecasts on these labels belongs to [PSY-016](psy-016-brier-score.md). No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Compare the `assessment` blocks across the Git history of `state/evolution/` to count how often each truth value was re-examined. If that is a handful of times, the per-pair bounds give way to far wider per-assessment bounds, and the identity matrix of section 1 records unrevised files, not stable artifacts.
