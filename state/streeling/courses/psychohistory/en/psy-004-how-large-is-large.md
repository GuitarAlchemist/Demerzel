---
module_id: psy-004-how-large-is-large
department: psychohistory
course: "How Large Is Large? Aggregate Predictability with Fourteen Agents"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-002-governance-phase-transitions"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-004
version: "0.1.0"
---

# How Large Is Large? Aggregate Predictability with Fourteen Agents

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will put an exact interval on a share observed among a few yes/no agents, say how its width shrinks as the group grows, and replace the head count by an effective sample size when the agents share a cause. **Project question:** the department says the aggregate behaviour of 14 personas across 4 repos follows mathematical laws. How wide is the uncertainty on an aggregate of 14, and what does shared context do to it?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) states the aggregate follows statistical laws, and reads correlation between repos as a coupling signal. [PSY-019](psy-019-combining-correlated-forecasters.md) applies the same arithmetic to forecast errors; [PSY-024](psy-024-the-single-actor.md) asks who acted in the recorded events.

## 1. What the record states and what the repository holds

**Observed.** The [department record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) ends its key principle with: "One agent's decision is unpredictable, but the aggregate behavior of 14 personas across 4 repos follows mathematical laws." [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/extract.py) snapshots that record, and the files the sentence could refer to, into [`observed-input.json`](../../../fixtures/psychohistory/psy-004/observed-input.json).

- The record lists 4 consumer repos, as stated. [`personas/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/personas) holds **17** persona files, 3 more than stated; it held 14 at [commit `e9fe8b7`](https://github.com/GuitarAlchemist/Demerzel/tree/e9fe8b7d711ede390b602896e4a5c571d0ad1f67/personas), which added the record on 2026-03-21 (read with `git ls-tree`, outside the fixture).
- A persona file describes a role and records no decision.
- One [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) would send one pull request to a panel of **5** personas, each judging it for a different concern and answering `block`, `merge_with_followups` or `pass`. All five get the same title, body, file list and truncated diff, and the [run](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) sets one `--model`. Comments there say the workflow was "observed failing on every sibling-pr-opened dispatch" and "silently never produced a verdict" without a permission the file grants; no verdict is stored at the pin, where its folder, `state/quality/verdicts/`, does not exist.
- Among the files read, the only recorded answers of several reviewers to one question are in [`state/council/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/council): 5 verdicts on one pull request, dated 2026-06-24, with 9 `pass` or `fail` reviews, at most 2 per verdict (the [schema](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/council-verdict.schema.json)'s limit). The reviewers are two roles, an automated check (`reviewer_a`) and a language-model reviewer (`reviewer_b`) per the [script that writes them](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py), never a persona (0 of 9). In the 4 verdicts with two reviews, the answers agree once and differ three times.

**Computed.** The largest group that the snapshot shows answering one question has 2 members; the workflow's panel has 5, not 14, and no verdict. So this fixture cannot test the claim. Everything below is **synthetic**: "agents" that answer yes or no with assumed probabilities.

### Practice Exercise 1

Classify each statement as observed, computed from observed data, or unsupported by the snapshot, and give the reason: (a) `personas/` holds 17 persona files; (b) three of the four two-review verdicts are split; (c) the five council verdicts are five independent observations of reviewer agreement; (d) the aggregate behaviour of 14 personas follows a statistical law.

> **Answer:** (a) Observed: a file count at the pinned commit. (b) Computed from the observed reviews: in 3 of the 4 verdicts with two reviews, the answers differ. (c) Unsupported: all 5 concern one pull request within one hour, and `reviewer_a` answers `pass` in 5 of 5; that is closer to one occasion repeated than to five. (d) Unsupported: the largest recorded group has 2 members, no review names a persona, and the panel of 5 has left no verdict.

## 2. Fourteen independent agents

Take n agents who each say yes with the same unknown probability p, independently. The *share* of yes, k/n, estimates p. The law of large numbers says that the share approaches p as n grows; its standard deviation (SD), `sqrt(p (1 - p) / n)`, says how fast. An *exact 95% interval* (Clopper and Pearson) keeps every p under which the observed count k falls in neither 2.5% tail (two-sided; [PSY-006](psy-006-transition-matrix-from-counts.md)'s one-sided bound puts all 5% in one tail):

```text
lower bound: the p for which  P(X >= k) = 0.025
upper bound: the p for which  P(X <= k) = 0.025      X ~ Binomial(n, p)
if all n say yes: lower bound = 0.025^(1/n), upper bound = 1
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/analyze.py) sums the binomial terms and solves for p by bisection. **Computed from assumed inputs** (half of the agents say yes; three decimals):

| Agents | Exact 95% interval | Width | SD at p = 0.5 |
|---|---|---|---|
| 14 | 0.230 to 0.770 | 0.539 | 0.134 |
| 100 | 0.398 to 0.602 | 0.203 | 0.050 |
| 10,000 | 0.490 to 0.510 | 0.020 | 0.005 |

Fourteen agents split evenly are compatible with any p from 0.23 to 0.77, over half the scale. The width shrinks with the square root of the group: 100 agents give an interval 2.652 times narrower (`sqrt(100 / 14) = 2.673`). The normal approximation `n = z² p (1 - p) / h²`, with z = 1.959964 and p = 0.5, asks for 384.146, so 385 agents, for a half-width h of 5 points.

For 14 agents this interval contains p at least 95.5% of the time at all 99 values of p from 0.01 to 0.99 ([`results.json`](../../../fixtures/psychohistory/psy-004/results.json)). A panel of 5 says less still: if all five say yes, the lower bound is `0.025^(1/5) = 0.478`.

### Practice Exercise 2

All 14 agents say yes. (a) Compute the lower bound of the exact 95% interval. (b) How many independent agents must be unanimous before that bound reaches 0.95?

> **Answer:** (a) `0.025^(1/14) = 0.768`: unanimity among 14 independent agents allows a yes probability as low as 0.77. (b) `0.025^(1/n) >= 0.95` gives `n >= ln 0.025 / ln 0.95 = 71.917`, so 72 agents.

## 3. Agents that share a cause

The panel of section 1 gives its five personas one diff and one model setting: agents of one project can share causes. **Synthetic, assumed model:** on each occasion (one question put to every agent) a shared signal says yes with probability p. Each agent copies it with probability c and otherwise decides alone, yes with probability p. Every agent still says yes with probability p, but two answers now have the correlation `rho = c²`. Then:

```text
variance of the share  = p (1 - p) / n × (1 + (n - 1) rho)
design effect          = 1 + (n - 1) rho
effective sample size  = n / (1 + (n - 1) rho)        tends to 1 / rho as n grows
```

The *effective sample size* is the number of independent agents whose share would vary as much as this group's; *design effect* is Kish's term for the factor between them. For 14 agents and p = 0.5, from the exact count distribution and 50,000 simulated occasions per row:

| rho | Design effect | Effective sample size | SD of the share | Yes counts on at least 95% of occasions | Simulated ÷ independent variance |
|---|---|---|---|---|---|
| 0 | 1.0 | 14 | 0.134 | 3 to 11 | 0.990 |
| 0.1 | 2.3 | 6.087 | 0.203 | 2 to 12 | 2.291 |
| 0.3 | 4.9 | 2.857 | 0.296 | 1 to 13 | 4.926 |
| 0.6 | 8.8 | 1.591 | 0.396 | 0 to 14 | 8.792 |

Row 1 is the known-answer check: rho = 0 gives back the binomial variance.

Adding agents does not repair this. At rho = 0.1 the effective sample size is 6.087 for 14 agents, 9.174 for 100 and 9.991 for 10,000, under a ceiling of `1 / rho = 10`, and the SD of the share cannot go below `sqrt(rho p (1 - p)) = 0.158`. The law of large numbers still averages out what each agent decides alone, but not the shared signal: the share of 10,000 agents settles near 0.658 or 0.342 (the yes probability given the signal), not 0.5. Under such a shared cause, the mismatch of section 1 matters little: at rho = 0.3, 17 agents are worth 2.931 independent ones, against 2.857 for 14.

### Practice Exercise 3

A team has 100 agents with rho = 0.3. Compute the design effect and the effective sample size. How many agents would it need for an effective sample size of 5?

> **Answer:** Design effect `1 + 99 × 0.3 = 30.7`; effective sample size `100 / 30.7 = 3.257`. An effective sample size of 5 cannot be reached: the ceiling is `1 / 0.3 = 3.333`. Only a lower rho raises the ceiling, and 5 needs a rho below `1 / 5 = 0.2`.

## 4. What ignoring the shared cause costs, and the strongest objection

**Synthetic.** Apply section 2's interval to agents that share a cause, as if independent. With p = 0.5 it contains p on 98.7% of occasions at rho = 0, 90.6% at 0.1, 64.5% at 0.3 and 20.4% at 0.6: at rho = 0.3, a "95%" interval here holds two times in three.

An imaginary dashboard reports that 12 of 14 agents approve and calls it a strong consensus. Read as independent answers, the count supports that: the exact interval, 0.572 to 0.982, excludes an even split. But when p is 0.5, at least 12 of the 14 agents give the same answer on 1.3% of occasions if they are independent, 9.4% at rho = 0.1, 35.5% at 0.3 and 79.6% at 0.6.

### Practice Exercise 4

Decide whether the dashboard may report "strong consensus" under this criterion: 12 or more agreeing agents must occur on fewer than 5% of occasions under an even split.

> **Answer:** It depends on a number nobody has measured. Independent agents give 1.3%, below 5%: allowed. A rho of 0.1 gives 9.4% and 0.3 gives 35.5%: not allowed. The decision is "not yet": "12 of 14" is strong evidence only if the agents answer almost independently.

**The strongest objection to this reading** is that sections 3 and 4 rest on one invented model and invented values of rho. A second model with the same correlations (each occasion draws a shared level q from a Beta distribution, and every agent says yes with probability q) gives exactly the same variance and effective sample size, which depend on rho alone. The tails do not: at rho = 0.3 all 14 agents agree on 10.7% of occasions, against 2.8% in the first model. More important, the personas' rho is unknown. If it is near 0, section 2 is the whole answer. **Nothing in this module can distinguish that case from a rho of 0.6.**

A decision log would measure it: one yes/no answer per occasion and per persona, from which rho is estimated as `(b - m²) / (m (1 - m))`, m being the share of yes and b that of agent pairs both saying yes. **Synthetic sizing:** a log detects a shared cause when its estimate exceeds the 95th percentile of logs simulated at rho = 0. With 14 agents, logs of 20 occasions detect rho = 0.1 in 2,312 of 2,500 (92%) and rho = 0.3 in all 2,500. With the panel's 5 agents, they detect rho = 0.3 in 9,447 of 10,000 (94%) but rho = 0.1 in 3,608 (36%); logs of 100 occasions detect rho = 0.1 in 1,759 of 2,000 (88%).

### Practice Exercise 5

A team wants the share of yes among its agents to fall within 5 points of the long-run rate p = 0.5 on 95% of occasions. (a) What SD of the share does that require, and how many independent agents? (b) The agents turn out to have rho = 0.1. Can the team reach the target by adding agents?

> **Answer:** (a) `0.05 / 1.959964 = 0.0255`, and `n = 1.959964² × 0.25 / 0.05² = 384.146`: about 385 independent agents by the normal approximation. Counted exactly, 385 agents land within 5 points on 94.7% of occasions; every group from 399 to 1,000 reaches 95%. (b) No. With rho = 0.1 the SD cannot go below `sqrt(0.1 × 0.25) = 0.158`, and the effective sample size cannot pass `1 / 0.1 = 10`, against the 385 needed. The team must lower rho or accept a wider band.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the files linked in section 1.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-004/extract.py`, then `analyze.py` in the same folder. Assumptions and seeds: [`scenarios.json`](../../../fixtures/psychohistory/psy-004/scenarios.json). Self-checks and negative controls: [README](../../../fixtures/psychohistory/psy-004/README.md).

**Method references.** Clopper, C. J., and Pearson, E. S. (1934), "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial", *Biometrika* 26(4), 404–413. Kish, L. (1965), *Survey Sampling*, Wiley (the design effect).

**Not done.** No decision of any persona was read and no correlation between personas was estimated; this fixture read the tribunal panel without running it. The agents are exchangeable (one p and one rho for all) and answer only yes or no; the panel's personas have different concerns and three possible answers. Two generating models were tried, both at p = 0.5. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** The panel's verdicts would be the decision log: its script stores one outcome per persona in each. Once runs succeed and 100 verdicts exist, estimate rho. An estimate near 0 would make section 2 the answer; one of 0.3 or more would make the panel's five voices worth at most 2.273 independent ones, and fourteen such voices at most 2.857.
