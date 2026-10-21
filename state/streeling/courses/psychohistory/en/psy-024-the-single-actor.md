---
module_id: psy-024-the-single-actor
department: psychohistory
course: "The Single Actor: When One Sender Is the Whole Ensemble"
level: intermediate
prerequisites: ["psy-004-how-large-is-large", "psy-009-concentration-and-heavy-tails"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-024
version: "0.1.0"
---

# The Single Actor: When One Sender Is the Whole Ensemble

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will count the actors that a record names, measure how concentrated their activity is, bound that measure when part of the record is lost, and say what the result establishes about who acted. **Project question:** aggregate laws assume many independent actors. Who actually generated the recorded events?

[PSY-002](psy-002-governance-phase-transitions.md) reads the ecosystem's aggregate behaviour as following statistical laws; [PSY-004](psy-004-how-large-is-large.md) shows how few independent agents fourteen correlated ones are worth. This module asks an earlier question: how many actors do the records contain? [PSY-009](psy-009-concentration-and-heavy-tails.md) measures the same log's concentration over days; this one, over actors.

## 1. One sender, and what "sender" means

**Observed.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/extract.py) reads the 594 files of [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) at commit `4b03838` and replaces every identity by a label before it writes [`observed-input.json`](../../../fixtures/psychohistory/psy-024/observed-input.json). All **594** archived events, from 2026-03-20 to 2026-07-16, carry the same `sender`, labelled *account A*, and the same `repo`. So do 8 later events left in the parent folder: 602 events with a readable sender, one account.

The [workflow file at the pin](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L75), a later version of the one that wrote these files (earlier versions were not read), sets `sender` to `github.actor`, which GitHub [defines](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) as "The username of the user that triggered the initial workflow run", and `repo` to the name of the repository it runs in. So:

- `repo` cannot vary: the recorder was installed in one repository. "One repo" says where the instrument stood, not that the other repositories were quiet.
- `sender` names an *account*, the credentials under which a push, an issue or a discussion reached the platform. The code-owners file names one maintainer, the only owner on its 7 rule lines; `extract.py` confirms that it is account A.
- An account is neither a person nor an agent. [`AGENTS.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/AGENTS.md) defines a team of 5 agent roles, yet none of an event's 9 keys names a role, a persona, a session or a model: whatever acts through the maintainer's credentials is recorded as account A.

"One actor" is therefore a statement about the record's resolving power: it resolves accounts, and it found one.

To measure concentration, give each of k actors its *share* s of the events:

```text
H = s_1² + s_2² + … + s_k²    concentration index: 1/k for k equal actors, 1 for one
N = 1 / H                      effective number of actors: equal actors that give this H
```

H is the sum of squared shares (Simpson's index; economists call it the Herfindahl–Hirschman index). For the archive, H = 1 and N = 1.

**The archive is a survivor set. Computed** from commits and trees: 615 trigger events were ever added (plus one schedule file), 603 remain at the pin, **12** were deleted without being archived. A file's `sender` is in its content, which this clone cannot read. The history shows only that commits under the workflow's identity added 11 of them, with subjects naming an event type and the same repository (on the 602 surviving events, subject and file agree), and that the twelfth, a `self_initiated` trigger and not a repository event, was added by another commit under author A's string, whose subject reports the driver's first autonomous cycle. Their senders can be bounded, not known.

### Practice Exercise 1

Take the worst case for "one sender": each of the 12 deleted files came from a different account, none of them account A. Compute H and N for the 606 events. Then suppose that all 12 came from one other account.

> **Answer:** Twelve new senders: `H = (594² + 12 × 1²) / 606² = 352,848 / 367,236 = 0.960821` and `N = 1.0408`. One new sender: `H = (594² + 12²) / 606² = 352,980 / 367,236 = 0.961180` and `N = 1.0404`. Account A keeps at least `594 / 606 = 98.02%`. Every assignment gives N between 1 and 1.0408: one new sender per file adds the least to the sum of squared counts, all on the largest account the most. These senders are assumptions: the loss cannot turn one sender into an ensemble.

## 2. A scale for N

**Synthetic.** [`scenarios.json`](../../../fixtures/psychohistory/psy-024/scenarios.json) defines imaginary ensembles of 14 actors, the head count in the department's key principle; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/analyze.py) computes:

| Imaginary ensemble | H | N | Half-coverage count | Relative spread |
|---|---|---|---|---|
| 14 equal actors | 0.071429 | 14 | 8 | 0.2673 |
| 14 actors, rank r has 1/r of the first one's events | 0.149063 | 6.7086 | 3 | 0.3861 |
| 14 actors, each half the one before | 0.333374 | 2.9996 | 1 | 0.5774 |
| 14 actors, one holds 90% | 0.810769 | 1.2334 | 1 | 0.9004 |
| 1 actor | 1 | 1 | 1 | 1 |

The *half-coverage count* is the smallest number of actors who together hold more than half of the events: a count-based relative of the "bus factor" (truck factor), which Avelino and colleagues estimate from who authored which files.

N matters for a statistical law because of what averaging does. Suppose an aggregate averages over events, each actor weighing in by its share, and the actors behave independently with the same variability:

```text
variance of the aggregate = H × variance of one actor
relative spread           = sqrt(H) = 1 / sqrt(N)
```

The aggregate fluctuates like an average of N equal actors. The law of large numbers needs a large N; at N = 1 the "aggregate" is the actor and nothing is averaged. A seeded simulation of 20,000 occasions per ensemble returns N = 14.08, 6.72, 2.98, 1.24 and 1.00 for the five rows.

### Practice Exercise 2

A log of 100 events has three actors with 50, 30 and 20 events. Compute H, N, the half-coverage count and the relative spread.

> **Answer:** `H = 0.5² + 0.3² + 0.2² = 0.38` and `N = 1 / 0.38 = 2.6316`. The largest actor holds exactly half, which is not more than half, so the half-coverage count is 2. Relative spread: `sqrt(0.38) = 0.6164`, about 62% of one actor's if the three are independent.

### Practice Exercise 3

Classify each statement as observed, computed, synthetic or unsupported, with the reason: (a) all 594 archived events carry one sender; (b) counting the deleted files, N is at most 1.0408; (c) 14 equal actors give a relative spread of 0.2673; (d) one person generated every event.

> **Answer:** (a) Observed: a count on the pinned files. (b) Computed, from an observed count and a worst-case assumption. (c) Synthetic: it holds for imaginary, independent actors. (d) Unsupported: `sender` names the account that triggered a run; no field records the person, session or agent behind it.

## 3. A second record: commit authors

**Observed**, with git commands that read commits and trees only: 1,599 commits lead to the pin, under **2** author strings, *author A* with 860 and *author B* with 739. **Computed:**

| Record | An identity is | Identities | Largest share | H | N |
|---|---|---|---|---|---|
| Trigger archive | the `sender` | 1 | 100% | 1 | 1 |
| Archive plus 12 deleted files, each a new sender (assumption) | the `sender` | 13 | 98.02% | 0.960821 | 1.0408 |
| Commits | the author string | 2 | 53.78% | 0.502863 | 1.9886 |
| Commits | the author address | 3 | 46.22% | 0.387065 | 2.5835 |
| Commits without the 613 with the trigger subject | the author string | 2 | 87.22% | 0.777082 | 1.2869 |

N = 1.99 says "two actors of equal weight". Four properties of the record say otherwise; each is a limit of the instrument, not a judgment on anyone's work.

- **An author is a configured string.** Author B is the name that [four workflows set before they commit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L85). 613 of its 739 commits carry the trigger workflow's subject, one per trigger file. Without them, 860 against 126 give N = 1.2869 (a reading chosen after seeing the counts).
- **One contributor, several identifiers.** Author A commits under two addresses (622 and 238). Git records who wrote a change (the author) and who recorded it (the committer): a committer string that never authors, with a no-reply address at the hosting platform's domain, created 215 of the 238, consistent with commits made on the platform. Counting addresses gives three "authors" and N = 2.5835; the repository's `.mailmap`, which maps addresses to identities, merges the two.
- **One identifier, several contributors.** 615 of author A's 860 commits (71.51%) carry a `Co-authored-by` [trailer](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors): 620 lines, 610 with a no-reply address at one domain, 4 with a name ending in `[bot]`, 4 naming account A itself. Counts by author ignore trailers.
- **Squashing.** 279 subjects end with a pull-request number (9 are merge commits, not squashes), and that committer string created 228 of those commits. A squash merge [combines all commits of a pull request into a single commit](https://docs.github.com/en/pull-requests/reference/pull-request-merges), with one author field.

### Practice Exercise 4

Compute H and N for the commit authors (860 and 739), then without the 613 commits that carry the trigger workflow's subject. Which is the right number?

> **Answer:** `H = (860² + 739²) / 1,599² = 1,285,721 / 2,556,801 = 0.502863` and `N = 1.9886`. Without the 613, author B keeps `739 − 613 = 126`: `H = (860² + 126²) / 986² = 755,476 / 972,196 = 0.777082` and `N = 1.2869`. Neither is "the" number: N measures labels under a counting rule. Report the rule with it, and fix the rule before looking.

## 4. What an ensemble of one supports

Every event with a readable sender was triggered through one account, in one repository; the commits come under one main author string and one workflow identity. These records describe one account's working rhythm. The bursts of [PSY-008](psy-008-bursts-are-not-rates.md) and the concentration of PSY-009 are properties of that rhythm, not laws about a population of agents: no population is recorded.

**The strongest objection to this reading** is that the instrument made uniformity likely: `sender` records who triggered a run, in one repository, for three kinds of event. One person working alone would produce this record; so would many agent sessions acting under the maintainer's credentials. The workflow pushed 613 commits under author B, yet only 214 `push` triggers were ever written: if every run that a push started left one in the history, at least 399 of those pushes started none. Commit [`eb230fb`](https://github.com/GuitarAlchemist/Demerzel/commit/eb230fb8d66c48b39a0b01eac99a738791f59e9f) later moved its pushes "to master over a write deploy key, not GITHUB_TOKEN"; pushes with that token start no run, as GitHub [documents](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow). **This log cannot distinguish one actor from many agents behind one account.** The trailers of section 3 hint at the second and cannot count them; reading the 12 deleted files would settle only whether a second account exists.

Data that would describe many independent actors: an identifier of the acting agent or session on every event, written by the tool that acts and not inferred from credentials; events from every repository; an effective number well above 1 (shares count, not heads); and evidence of independence (PSY-004). Literature, not evidence: in Asimov's *Foundation and Empire* the plan is thrown off course when one individual, the Mule, falls outside the statistics; here no crowd is recorded to stand out from.

### Practice Exercise 5

A new log tags each event with a persona id: 1,400 events, one persona with 1,010 and thirteen with 30 each. The criterion was fixed in advance: to speak of an aggregate of "about 14 actors", N must be at least 10. (a) Decide. (b) Decide again if the thirteen double their output. (c) What remains to be shown if N ever passes?

> **Answer:** (a) `H = (1,010² + 13 × 30²) / 1,400² = 1,031,800 / 1,960,000 = 0.526429` and `N = 1.8996`: no. (b) `H = (1,010² + 13 × 60²) / 1,790² = 1,066,900 / 3,204,100 = 0.332980` and `N = 3.0032`: still no; fourteen equal personas would give 14. (c) That a persona id marks a separate decision-maker, not a label on one model reading one context, and that the personas' decisions are not strongly correlated (PSY-004). The log is imaginary.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the files linked or named above and the 1,599 commits that lead to the pin. `extract.py` stops if a pinned value differs.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-024/extract.py`, then `analyze.py`; `--check` compares a fresh run with [`results.json`](../../../fixtures/psychohistory/psy-024/results.json). The [README](../../../fixtures/psychohistory/psy-024/README.md) gives the labelling rule, the git commands and the checks.

**Method references.** Simpson, E. H. (1949), "Measurement of Diversity", *Nature* 163, 688 (the sum of squared shares). Laakso, M., and Taagepera, R. (1979), "'Effective' Number of Parties: A Measure with Application to West Europe", *Comparative Political Studies* 12(1), 3–27 (N = 1/H). Avelino, G., Passos, L., Hora, A., and Valente, M. T. (2016), "A Novel Approach for Estimating Truck Factors", *24th IEEE International Conference on Program Comprehension*, 1–10.

**Not done.** No deleted file was read. No sender or author string was matched to a person, and the two records were not joined: a platform username and an author string are different identifiers. Trailer names were counted, not classified or authenticated. No other repository was read, no agent's decision was observed, and no truck factor was estimated. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** In a full clone, read the `sender` of the 12 deleted files: another account among them would change "one sender" to "N at most 1.0408", nothing else. The conclusion would change only with a record that identifies the acting agent on each event: N over agents could then be computed.
