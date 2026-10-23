---
module_id: psy-015-belief-contagion-small-population
department: psychohistory
course: "Belief Contagion in a Small Population"
level: intermediate
prerequisites: ["mat-020-markov-chains-hmm", "mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-015
version: "0.1.0"
---

# Belief Contagion in a Small Population

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will compute a reproduction number and its threshold, find the final size that a deterministic epidemic curve predicts, simulate the same model one event at a time, and read the distribution from which a single run is drawn. **Project question:** the department lists "belief state epidemiology". If a belief spreads among 14 agents, how much does one run differ from the deterministic epidemic curve?

[PSY-002](psy-002-governance-phase-transitions.md) reads a shift in belief labels as a sign of regime change; this module asks what a model of spreading can forecast. [PSY-004](psy-004-how-large-is-large.md) studies 14 agents whose answers share a cause, and [PSY-017](psy-017-calibration-with-six-observations.md) the calibration belief met in section 1.

## 1. The model, and what "infected" means here

**Observed.** The [department record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) lists, as research area 7 of 10, "Belief state epidemiology — how beliefs spread across agents and repos", and its key principle speaks of "14 personas across 4 repos". [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/extract.py) snapshots what the repository records about beliefs at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-015/observed-input.json): the 8 current belief files of [`state/beliefs/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs) and 13 archived ones. No proposition appears under two holders (0 of 21), but this count could not have shown sharing: the 12 files with content have one evaluator, the governance persona Demerzel, and the other 9 are empty scaffolds.

Two current files name a source outside their evaluator: `confidence-calibration` and `remediation-effectiveness` each rest on one evidence item, an `ml-feedback-recommendation` message whose rationale and confidence [the applying script](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py) copies into Demerzel's belief. Its schema says "from an ix ML pipeline to Demerzel"; the two messages are not in the repository, so the sender is known from that description and the script's docstring only. Each is one hop, from a document to one holder.

Two record types are designed to hold an agent's beliefs: a [belief snapshot](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/contracts/belief-snapshot.schema.json) (one agent's beliefs at a given time) and a [knowledge state](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/knowledge-state.schema.json) (a teacher, a learner, the learner's belief before and after). Of the 722 JSON files under `state/`, course library excluded, none has the shape of either (the test recognises their three sample files) and none has a key naming a teacher, a learner or a message's sender (`origin_repo`, `origin_agent`). Under these tests no file records a holder passing a belief on, a second hop, or an agent exposed without adopting. No rate can be estimated, so everything below is **synthetic**.

**Analogy.** In the SIR model of epidemiology, an agent is *susceptible* (S) until it adopts the belief, *infected* (I) while it holds the belief and passes it on, and *recovered* (R) once it no longer passes it on. "Infected" does not mean wrong or harmful; it names the state of transmitting. Among N agents, each holder passes the belief to agents picked at random at rate β and stops transmitting at rate γ:

```text
adoption:            (S, I) -> (S-1, I+1)   at rate beta*S*I/N
stops transmitting:  (S, I) -> (S, I-1)     at rate gamma*I
R0 = beta/gamma
P(next event is an adoption) = R0*S / (R0*S + N)
```

The *basic reproduction number* R0 is the mean number of agents one holder converts in a large population when everybody else is susceptible. The last line is the *embedded jump chain*: it says which event comes next and ignores when. The *final size*, the number of agents that ever held the belief, depends only on that order, so [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/analyze.py) draws no waiting time.

Assumptions, in [`scenarios.json`](../../../fixtures/psychohistory/psy-015/scenarios.json): N = 14 (the key principle's count; PSY-004 finds 17 persona files at the pin) and N = 1,400; one initial holder; R0 = 0.8, 1.2 and 3.

### Practice Exercise 1

With N = 14, R0 = 3 and one initial holder, what is the probability that the first event is an adoption? That the belief is never passed on? Recompute the second for N = 1,400.

> **Answer:** With S = 13, `3×13 / (3×13 + 14) = 39/53 = 0.7358`. Otherwise the only holder stops first and the belief ends with it: `14/53 = 0.2642`. For N = 1,400: `1,400 / (3×1,399 + 1,400) = 1,400/5,597 = 0.2501`.

## 2. The deterministic curve and its threshold

Replace counts by shares s, i, r of a large population and random events by their mean rates, with time in mean holding periods (1/γ):

```text
ds/dt = -R0*s*i        di/dt = R0*s*i - i        dr/dt = i
holders increase while R0*s > 1
final size z:   1 - z = s0 * exp(-R0*z)
```

This is the *mean-field* curve: every agent feels the average of all the others. At its *threshold*, R0 × s = 1, each holder is replaced by exactly one. The *final-size equation* gives the share z that ever holds the belief.

**Synthetic.** For 14 agents (s0 = 13/14) the equation gives 3.13 agents at R0 = 0.8, 6.65 at R0 = 1.2 and 13.24 at R0 = 3. At R0 = 3 the integrated curve rises to 4.55 simultaneous holders after 1.59 holding periods and ends at the same 13.24 (the known-answer check). At R0 = 1.2 it peaks at 1.07 holders yet ends at 6.65.

### Practice Exercise 2

For N = 14 and one initial holder, compute R0 × S/N at the start for the three values of R0. Where it exceeds 1, after how many adoptions do holders stop increasing?

> **Answer:** `0.8 × 13/14 = 0.7429`, `1.2 × 13/14 = 1.1143`, `3 × 13/14 = 2.7857`. At R0 = 0.8 the curve never rises. Holders increase while S exceeds N/R0: `14/1.2 = 11.67`, so growth stops once S is 11, after `13 − 11 = 2` adoptions; `14/3 = 4.67`, so once S is 4, after `13 − 4 = 9`.

## 3. Fourteen agents: the distribution one run comes from

**Synthetic.** Runs at each final size, over 10,000 runs for each R0 ([`results.json`](../../../fixtures/psychohistory/psy-015/results.json), section `cases`):

```text
final size     1     2    3    4    5    6    7    8    9   10   11   12    13    14
R0 = 0.8    5708  1553  818  520  364  273  231  176  133  101   65   41    11     6
R0 = 1.2    4706  1253  751  504  451  371  319  302  324  291  261  244   153    70
R0 = 3      2664   606  267  167  124  114  119  112  175  237  414  809  1464  2728
```

- **R0 = 3 has two humps.** 2,664 runs never get past the first holder and 4,192 end at 13 or 14. The deterministic 13.24 lies inside the upper hump: 5,001 runs end at 12, 13 or 14, within 1.4 agents (a tenth of the population) of it. The curve describes half of the runs.
- **The mean falls in the valley.** It is 8.38, and sizes 5 to 8 are the four rarest outcomes.
- **R0 = 1.2 has one hump, at 1, and a long shelf**, like R0 = 0.8 on the other side of the threshold. Only 992 runs end at 6, 7 or 8, around the deterministic 6.65.

**Computed check.** Summing over every path of the same chain gives exact probabilities with no random number (fractions at N = 14, floating-point sums at N = 1,400). In all six cases the simulated counts stay within 2.65 standard errors of them, and the test rejects counts simulated with another R0.

### Practice Exercise 3

From the R0 = 3 row: what share of the runs ends with at most 2 agents, and with at least 12? What share ends at 8 or 9, the whole numbers around the mean? Is "about 8 agents" a usable forecast?

> **Answer:** `2,664 + 606 = 3,270` runs, 32.70%. `809 + 1,464 + 2,728 = 5,001` runs, 50.01%. `112 + 175 = 287` runs, 2.87%. No: the two ends hold `3,270 + 5,001 = 8,271` runs, 82.71%. For a two-humped outcome, state both humps and their shares, not the average.

## 4. A hundred times more agents, and the strongest objection

**Synthetic.** The same model with N = 1,400. "Near" means within a tenth of the population of the deterministic final size; an "early fade-out" ends at or below a tenth of the population (1 agent of 14, 140 of 1,400).

| R0 | Deterministic final size | Runs near it | Early fade-outs |
|---|---|---|---|
| 0.8 | 4.96 | 9,995 | 9,995 |
| 1.2 | 443.03 | 1,097 | 8,455 |
| 3 | 1,316.74 | 6,634 | 3,366 |

**Size does not remove the fade-out.** At N = 1,400 and R0 = 3, 3,366 runs die out early; the exact probability is 0.3339. While nearly everybody is susceptible, each holder independently converts a random number of others, geometric with mean R0 because the holding time is exponential. That *branching process* dies out with probability 1/R0 when R0 exceeds 1: here 0.3333. With a fixed holding time the value would be 0.0595: the fade-out share rests on that assumption too. At R0 = 1.2 the count of fade-outs depends on the cut.

**What size buys is separation.** At N = 1,400 and R0 = 3 no run ended between 16 and 1,256 agents, and 90% of the 6,634 runs above the cut ended between 1,293 and 1,337: once a run has taken off, 1,316.74 is a sharp forecast. At N = 14 no gap separates the humps.

The fade-out risk falls with the number m of initial holders: the branching value is 1/R0 to the power m, and the exact probabilities at N = 1,400 and R0 = 3 are 0.3339, 0.1117, 0.0374 and 0.0042 for m = 1, 2, 3 and 5.

### Practice Exercise 4

Compute the branching value for R0 = 3 and m = 1, 2, 3 and 5, and compare it with the exact probabilities above. What is the smallest m that brings the risk of an early fade-out below 5%?

> **Answer:** `1/3 = 0.3333`, `1/9 = 0.1111`, `1/27 = 0.0370` and `1/243 = 0.0041`, close to the exact values. Three holders: 0.0374 is below 0.05, while two leave 0.1117. Size alone is not enough; several initial holders are.

**The strongest objection to this reading** is that SIR may be the wrong family of models. It needs holders who convert other agents one by one. Personas that read the same governance files can instead acquire a belief together, from a common source: a broadcast, with no chain, no reproduction number and no fade-out. What is recorded leans that way: the two sample knowledge states name one teacher, the department's head persona, and the two recorded adoptions both come from a document. **This fixture cannot distinguish contagion from broadcast: two adoptions from a document and no chain are too few to tell.** A transmission record would settle it, with six items per agent and proposition: who holds it, what it says, from whom it came, when it was adopted, when the agent stopped passing it on, and who else was exposed without adopting. The knowledge-state schema has keys for four and, through its assessment of one learner at a time, for part of the sixth; the belief snapshot has keys for three; neither records when a holder stops.

### Practice Exercise 5

Classify each statement as observed, synthetic, analogy or unsupported, with the reason: (a) two current belief files rest on a message from another pipeline; (b) with R0 = 3, about a quarter of the runs among 14 agents never pass the belief on; (c) an agent that holds a belief is infected; (d) beliefs spread among the project's personas with R0 above 1.

> **Answer:** (a) Observed in the two files and in the script that writes them; the sender is read from the schema's description, not from the messages. (b) Synthetic: 2,664 of 10,000 runs (exact probability 14/53), under assumed rates. (c) Analogy: a word borrowed from epidemiology for "holds it and passes it on". (d) Unsupported: no file read here records a holder passing a belief to another agent, so R0 cannot be estimated; the six-item record would make it observable.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** `extract.py` refuses to run if one of its 32 files, or either folder it lists (722 JSON files under `state/`, 11 contract schemas), differs from the pin. `results.json` lists the 42 self-checks; the [README](../../../fixtures/psychohistory/psy-015/README.md) gives the commands and the controls.

**Method references.** Kermack, W. O., and McKendrick, A. G. (1927), "A Contribution to the Mathematical Theory of Epidemics", *Proceedings of the Royal Society of London, Series A* 115, 700–721 (deterministic model, threshold, final size). Bailey, N. T. J. (1975), *The Mathematical Theory of Infectious Diseases and its Applications*, 2nd edition, Griffin. Whittle, P. (1955), "The Outcome of a Stochastic Epidemic: A Note on Bailey's Paper", *Biometrika* 42, 116–122 (minor outbreaks and 1/R0).

**Not done.** No rate was estimated from project data: the three values of R0 are assumed. Only the final size was simulated, and only uniform mixing: no network, no unequal agents, no second adoption. The shape and key tests cover JSON files under `state/`; beyond one YAML belief file (no evaluator; 10 of its 49 evidence items cite `GPT-4o`), no YAML, Markdown or other repository was read. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Keep the six-item record for a handful of propositions. If most adoptions name a document or a single teacher as their source, replace this model by a broadcast model. If they name other agents, estimate R0 from the adoptions per holder and compare the observed final sizes with section 3.
