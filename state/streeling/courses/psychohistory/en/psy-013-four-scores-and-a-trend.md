---
module_id: psy-013-four-scores-and-a-trend
department: psychohistory
course: "Four Scores and a Trend: Reading the Resilience History"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-013
version: "0.1.0"
---

# Four Scores and a Trend: Reading the Resilience History

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will put an exact interval on a score of eleven trials, test a step between two scores, account for several tests on the same four numbers, and say what a reused test set measures. **Project question:** the resilience history shows 0.00, 0.64, 0.73, 0.82 over four cycles; which of these steps is distinguishable from chance, and what does a repeated injection set measure?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) reads this score as a regime indicator and its change as a velocity. This module asks how much change eleven trials can show. [PSY-004](psy-004-how-large-is-large.md) builds the exact interval used here, [PSY-011](psy-011-measurement-change-or-system-change.md) treats changes of instrument, and PSY-023 designs alarm rules.

## 1. Read the record before computing

**Observed** at commit `4b03838`. The project defines the resilience score as `R = injections_caught / injections_total` ([glossary](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/CONTEXT.md#L48), [metric policy](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/resilience-metric-policy.yaml)). An *injection* is a defect planted on purpose. The [chaos-test report](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/chaos-test-report.md) lists eleven in three files, for example a binding that nothing reads in [`chaos-test.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/chaos-test.ixql), a policy whose description is deliberately meaningless, a schema that nothing references. Each has one of seven *levels* (L0, a whole file, to L4, one expression, then policy and schema) and an expected detector.

[`history.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json) holds four records, `chaos-001` to `chaos-004`, stamped within 20 hours on 2026-03-22 and 2026-03-23; the pinned commit is dated 204 days later. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/extract.py) snapshots it into [`observed-input.json`](../../../fixtures/psychohistory/psy-013/observed-input.json), and [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/analyze.py) confirms that the eleven injection names are identical in all four records: the set is reused, not redrawn. The README states the claim examined here: "Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles" ([line 132](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L132)).

| Cycle | Caught (recorded) | Status labels of the 11 injections |
|---|---|---|
| chaos-001 | 0 | 11 missed |
| chaos-002 | 7 | 6 automated, 2 spec-only, 2 manual, 1 delayed-14d |
| chaos-003 | 8 | 6 automated, 2 policy-enforceable, 2 spec-only, 1 delayed-14d |
| chaos-004 | 9 | 6 automated, 3 policy-enforceable, 2 spec-only |

Three facts come before any statistics:

- **What "caught" means.** The [report of `chaos-003`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/shake-metafix-cycle-001.md) marks an injection caught when its status is `automated` or `policy-enforceable`, and calls the second human-executable rules, "NOT yet automated tooling".
- **Cycle 2 does not add up.** That rule gives 6, the record's level scores imply 5, and 7 is recorded.
- **The baseline depends on the scorer.** The chaos-test report, dated the same day as `chaos-001`, scores the same eleven injections 5/11 "immediate" and 9/11 "including spec-level". The history records 0.

The folder's three other files, `2026-03-23-red-team-cycle-00N.json`, are another series (14 attack scenarios graded PASS, PARTIAL or FAIL), not the detail of these cycles.

### Practice Exercise 1

Apply the rule "caught = automated or policy-enforceable" to the four rows of the table. Where does it disagree with the recorded count? Then score cycle 2 from its level scores: 1.0 for L2 (three injections) and for L3 (one), 0.5 for L4 (two), 0 elsewhere.

> **Answer:** The rule gives 0, 6, 8, 9 against the recorded 0, 7, 8, 9: only cycle 2 disagrees. Level scores: `3 × 1 + 1 × 1 + 2 × 0.5 = 5`. The record supports 7, 6 or 5 for one cycle, and no set of status labels reproduces all four recorded counts (`status_rules` in [`results.json`](../../../fixtures/psychohistory/psy-013/results.json)). The sections below use 7 and say what changes with 6 or 5.

## 2. Put an interval on each score

Treat a cycle as 11 independent trials with one detection rate p, as if the injections were a random sample of the defects that matter (an assumption that section 4 questions). The *exact (Clopper–Pearson) 95% interval* is the set of rates that the count does not reject: its lower bound is the p at which "this many or more" has probability 0.025, its upper bound the p at which "this many or fewer" has probability 0.025.

**Computed** (bounds rounded to three decimals):

| Cycle (caught) | 95% interval | Policy bands touched |
|---|---|---|
| chaos-001 (0/11) | 0–0.285 | critical |
| chaos-002 (7/11) | 0.308–0.891 | critical, warning, watch |
| chaos-003 (8/11) | 0.390–0.940 | all four |
| chaos-004 (9/11) | 0.482–0.977 | all four |

The metric policy cuts R at 0.5, 0.7 and 0.9 into critical, warning, watch and healthy. The latest score, 0.82, reads "watch" ("proactive" in PSY-002), but its interval is 0.49 wide and touches every band. The first interval overlaps none of the others; the last three overlap one another.

### Practice Exercise 2

For 0 of n the upper bound has a closed form, `1 − 0.025^(1/n)`; for n of n the lower bound is `0.025^(1/n)`. These belong to the two-sided interval; a one-sided 95% bound, as in [PSY-006](psy-006-transition-matrix-from-counts.md), uses 0.05. (a) Compute both for n = 11. (b) A fresh set is caught in full. How large must it be for the lower bound to reach the "healthy" cut, 0.9?

> **Answer:** (a) `0.025^(1/11) = 0.715`: 0 of 11 gives an upper bound of `1 − 0.715 = 0.285`, and 11 of 11 a lower bound of 0.715, still in "watch". (b) The bound reaches 0.9 when `0.9^n ≤ 0.025`. `0.9^35 = 0.02503` is too large and `0.9^36 = 0.02253` is small enough: 36 injections, all caught.

## 3. Test each step, then count the tests

**Computed.** *Fisher's exact test* compares two counts as two independent samples. Fix the margins: 11 trials per cycle, and the total caught in both. If the cycles share one rate, every way of placing those catches among the 22 trials is equally likely. The *p-value* used here is two-sided: the total probability of all tables no more probable than the observed one. The one-sided value (the later cycle is higher) is half as large for the first step.

| Cycles compared (counts) | Two-sided p |
|---|---|
| 1 to 2 (0/11, 7/11) | 0.0039 |
| 2 to 3 (7/11, 8/11) | 1 |
| 3 to 4 (8/11, 9/11) | 1 |
| 1 to 4 (0/11, 9/11) | 0.0002 |

**Four tests on four numbers.** Four independent tests at the 5% level give at least one false positive (a p below 0.05 when nothing differs) 18.5% of the time (`1 − 0.95^4`). The *Bonferroni correction* compares each p with `0.05 / 4 = 0.0125` and holds whatever the dependence between tests. Here the tests share counts, and an exact test on 11 trials is conservative: over every way to place the 24 recorded catches among the 44 trials, one test alone falls below 0.05 in 1.78% of arrangements and at least one of the four in 6.2%. The correction changes no verdict in the table, but it decides two other readings:

- **The design is paired.** The same injections are rescored, so the matching test is the *exact sign test* (McNemar's test in exact form): if nothing changed, an injection whose result differs is as likely to have moved one way as the other. From cycle 1 to cycle 2, seven gains and no loss give a two-sided p of `2 × (1/2)^7 = 0.0156`, above 0.0125 (six gains, by status labels: 0.031).
- **Cycle 2's count.** With 6 in place of 7, Fisher's p is 0.0124; with 5 it is 0.035.

**One step or three?** For the three later cycles, an exact test of "one common rate" (Freeman–Halton) gives p = 0.88 and a one-sided exact trend test (Cochran–Armitage, scores 0, 1, 2) p = 0.24. Three independent cycles of 11 at their pooled rate, 8/11, rise strictly in 8.5% of cases. The policy labels a cycle "improving" when its R exceeds the average of the previous two; on such cycles that rule says "improving" 45% of the time, and twice running 18%.

On the recorded counts and Fisher's test, the first step is the only one distinguishable from chance (on the paired test it passes with three comparisons and fails with four); the two later steps are not, under any reading above.

### Practice Exercise 3

Compute by hand the one-sided Fisher p-value for cycle 1 to cycle 2, then the two-sided one.

> **Answer:** With 7 catches among 22 trials and none in cycle 1, cycle 1's 11 trials all come from the 15 misses: `C(15,11) / C(22,11) = 1,365 / 705,432 = 0.0019`. The mirror table (7 then 0) is equally probable and no other table is as improbable, so the two-sided value is twice that: 0.0039.

### Practice Exercise 4

From cycle 2 to cycle 3 the status labels show two injections going from missed to caught, none the other way. Give the two-sided sign-test p-value. Then decide whether the first step's paired p-value survives a Bonferroni correction for three tests (the consecutive steps) and for four (adding first against last).

> **Answer:** `2 × (1/2)^2 = 0.5`: no evidence of a change. First step: `2 × (1/2)^7 = 1/64 = 0.0156`. With three tests the threshold is `0.05 / 3 = 0.0167` and the step passes; with four it is 0.0125 and the step fails. The verdict depends on how many comparisons you admit to having made.

## 4. What a reused injection set measures

**Observed.** Each later record says what was built before it was scored. `chaos-002`: three detections implemented in a parser, after which six injections name one function, `analyzeLolli()`, as their detector. `chaos-003`: two fixes at the policy level, and the two policy injections change status. `chaos-004`: two fixes at the schema level, one a test file "including injection #10 regression test", and injection 10, the unreferenced schema, is the one that changes. No injection goes back from caught to missed.

From cycle 2 on, R on this set therefore counts how many of eleven known defects now have a detector or a written rule: a sound progress measure for a repair list, but not the detection rate on defects nobody has planted yet, which is what the name "resilience" suggests. **Analogy:** a model tuned against its own test set keeps a rising score that no longer estimates performance on new data (Dwork et al. 2015).

**Synthetic** (no such set exists). A *held-out set*, written by someone who has not read the fixes and scored once before any repair, would estimate that rate. With 11 held-out injections, a two-sided Fisher test against 9/11 falls below 0.05 only at 3 caught or fewer (p = 0.030; 4 caught gives 0.080).

**The strongest objection to this lesson** is that its chance model fits neither the set nor the scoring. The injections were not sampled; a status records whether a detector exists, not a noisy run; and injections move together: level scores are 0 or 1 in every cycle but one. With the 7 levels as units (0, 2, 4, 5 fully scored), the first step has p = 0.46 and first against last 0.021, above 0.0125. The baseline moves too: with the report's 5/11 in place of 0, cycle 2 gives p = 0.67 and cycle 4 gives 0.18. **This record cannot distinguish a jump in detection from a change in what was counted as caught.** The next check below would settle it.

### Practice Exercise 5

Synthetic. A fifth cycle records 11 of 11 on the same set, and the status line reads R = 1.00, "healthy". A colleague then writes 11 new injections without reading the fixes; 4 are caught. (a) What does the 1.00 establish? (b) Does 4/11 differ from the last recorded 9/11? State your criterion.

> **Answer:** (a) That all eleven known defects now have a detector or a rule, not how new defects fare; even read as a fresh sample, 11 of 11 leaves rates down to 0.715. (b) Criterion: a two-sided Fisher p below 0.05. 4/11 against 9/11 gives 0.080, so the two are not distinguishable; 3/11 would give 0.030.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the four files of [`state/resilience/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience), the two reports, the metric policy, the glossary, the README line and the three injection files. `extract.py` refuses to run if one differs from its pinned blob or the folder gains a file.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py`, then `analyze.py` in the same folder. The [README](../../../fixtures/psychohistory/psy-013/README.md) lists the self-checks and negative controls, [`scenarios.json`](../../../fixtures/psychohistory/psy-013/scenarios.json) the analysis choices.

**Method references.** Clopper, C. J., and Pearson, E. S. (1934), "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial", *Biometrika* 26(4), 404–413. Dunn, O. J. (1961), "Multiple Comparisons Among Means", *Journal of the American Statistical Association* 56, 52–64 (the Bonferroni correction). Agresti, A. (2013), *Categorical Data Analysis*, 3rd edition, Wiley (exact tests, McNemar's test). Dwork, C., and five co-authors (2015), "The Reusable Holdout: Preserving Validity in Adaptive Data Analysis", *Science* 349, 636–638.

**Not done.** No injection was replayed, and the parser the records name ([`Parser.fs`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/tools/ixql-parser/IxqlParser/Parser.fs), in this repository) was not built or run: the fixture reads the records only. No held-out set exists. The four comparisons were chosen after the four scores were known. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Write the scoring rule down, apply it to the first report's eleven verdicts and to every cycle, then score a held-out set once. If the rule puts the baseline near 5/11, the conclusion changes from "one large step, then a plateau" to "no distinguishable step". Separately, build the parser and apply `analyzeLolli` to `pipelines/chaos-test.ixql`: the records credit it with six injections.
