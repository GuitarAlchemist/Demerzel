---
module_id: psy-021-conservation-claims
department: psychohistory
course: "Conservation Claims You Can Check"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-021
version: "0.1.0"
---

# Conservation Claims You Can Check

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will sort statements that get called "conservation" into four kinds, audit a stock-and-flow identity on a real event log, and name the record a claim needs before it can fail. **Project question:** PSY-001 borrows Noether's theorem for "learning momentum". Which conservation statements about this project can actually be checked?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) announces a conservation law for governance. This module asks what such a law requires, then audits the nearest thing the repository offers: the bookkeeping of its trigger log. [PSY-008](psy-008-bursts-are-not-rates.md) and [PSY-009](psy-009-concentration-and-heavy-tails.md) read that log as arrivals, [PSY-024](psy-024-the-single-actor.md) asks who sent them, and [PSY-003](psy-003-review-throughput-and-compounding.md) applies similar identities to review queues.

## 1. Four things called conservation

In physics, a conservation law says that a number computed from the state of an isolated system keeps its value while the state changes: energy, momentum, electric charge. Noether's theorem (1918) is one source of such laws. It concerns a system whose motions make an *action* stationary, the action being one number computed from a whole history of the system. If a continuous family of transformations (shift every instant by the same amount, any amount) leaves the action unchanged, the theorem constructs a quantity that stays constant along every motion: energy for shifts in time, momentum for shifts in space. Nobody chooses the quantity; it is derived.

**Observed.** [Section 5 of PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md#L112) states the theorem as "every continuous symmetry of a system has a corresponding conserved quantity" and applies it: "In fractal compounding, the symmetry is **scale invariance** — the compound operation has the same shape at every level. The conserved quantity is **learning momentum (p_L)**", with

```text
p_L = (beliefs_gained_T - beliefs_lost_T) / cycles_elapsed
```

and "If your compounding process is consistent (symmetric across scales), p_L stays constant or grows. If you break the symmetry — by skipping compounding at some level, or by compounding differently at different scales — p_L decays."

**This is an analogy.** Its intuition is fair: a process run the same way at every level should keep yielding validated beliefs. But the theorem's conditions are not met (the author's reading, recorded in [`scenarios.json`](../../../fixtures/psychohistory/psy-021/scenarios.json)). No action is written for governance cycles. The symmetry links five named levels (step, pipeline, cycle, session, evolution): a discrete correspondence, not a continuous family. And p_L is defined by a formula and may grow, which a conserved quantity cannot.

A project does have conservation statements it can check: the accounting identities of a *stock*, the amount of something present at one moment (Meadows 2008).

```text
stock now = everything that came in - everything that went out
```

What such a statement is worth depends on whether the records could have made it false. This module uses four labels:

- **by construction**: true whatever the records say, by arithmetic or by how its sides are derived (often both come from the same records); it says nothing about the system;
- **auditable**: the records could have made it false, often because its sides were written separately;
- **not recorded**: one of the quantities was never written down;
- **analogy**: the vocabulary of a law without its conditions.

## 2. What the files at the pin can balance

**Observed.** A *trigger* is a small JSON file that a [GitHub workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) wrote into `state/triggers/` for each push, opened issue or created discussion, for an autonomous agent, the driver, to consume. Both were retired on 2026-07-18; the linked file is a later version. The reopened issues and failed CI runs it also handles never occur in the history. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/extract.py) snapshots [the folder](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) at commit `4b03838` into [`observed-input.json`](../../../fixtures/psychohistory/psy-021/observed-input.json): 603 event files.

| Type | Pending | Archived | Total |
|---|---|---|---|
| discussion_created | 5 | 252 | 257 |
| issue_opened | 3 | 135 | 138 |
| push | 0 | 207 | 207 |
| research_followup | 1 | 0 | 1 |
| Total | 9 | 594 | 603 |

"Pending" means still in `state/triggers/` itself; "archived" means in its sub-folder `archived/`; the third folder, `processing/`, is empty. Of the 603 files, 602 share one shape: six keys (`type`, `repo`, `ref`, `priority`, `details`, `timestamp`), with `event`, `sender` and `run_id` (the workflow run's unique id) inside `details`. No key records an archival time, a processing step or an outcome: a trigger that was processed and one that was abandoned look the same.

**Computed** from these files alone by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/analyze.py) into [`results.json`](../../../fixtures/psychohistory/psy-021/results.json):

- *By construction:* the type totals add up to 603: one count, split and added again.
- *Auditable, and holding:* 603 file names, all distinct, so no file sits in two folders; 602 run ids, all distinct; and the workflow file and the driver's skill file both state 594 orphaned triggers, which is what the archive holds.
- *Not recorded:* the folders suggest a closed pipe, `created = archived + pending + in processing`, but nothing at the pin counts what was created: the identity has no left side. The driver's [own rule](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md#L331) says why: "On WAKE: move triggers to `state/triggers/processing/` before reading, delete after processing." The designed exit leaves no file.

### Practice Exercise 1

From the table, compute the number of event files by folder and by type. Then find the sum in this section that could have disagreed with a number written independently of the files.

> **Answer:** By folder `9 + 0 + 594 = 603`; by type `257 + 138 + 207 + 1 = 603`. These cannot disagree: both add up one count again. The archive column can: `252 + 135 + 207 = 594` is counted from files, and 594 is also stated in two documents. They agree.

### Practice Exercise 2

Give each statement one of the four labels: (a) "no run id appears in two files"; (b) "every archived trigger was processed"; (c) "the counts by type add up to the number of files"; (d) "learning momentum is conserved".

> **Answer:** (a) Auditable: a copied file would have repeated an id; it holds, 602 distinct of 602. (b) Not recorded: no key records processing. (c) By construction. (d) Analogy: the theorem's conditions are missing.

## 3. The history supplies the missing side, and the identity fails

**Observed, from history.** `extract.py` also reads the Git history of the pinned commit: along the *first-parent chain* (the successive states of the main branch: 1,528 commits, 623 of which touch the folder) it lists every addition and deletion of a trigger file.

| Folder | Added | Deleted | Added − deleted | On disk |
|---|---|---|---|---|
| pending | 615 | 606 | 9 | 9 |
| in processing | 5 | 5 | 0 | 0 |
| archived | 594 | 0 | 594 | 594 |

So 615 trigger files were created, and the closed identity has a left side. **It fails:** 615 against 594 + 9 + 0 = 603. Twelve files, 1.95% of those created, are in no folder:

- 2 deleted from pending by `c5cca0c` and `49a573c`, each removing a "trigger file with invalid Windows filename";
- 5 deleted from `processing/` by `2b752a7`, "Driver cycle 002 complete — 9 tasks, all repos healthy";
- 5 deleted from pending by `a2c1ef0`, "docs(seldon): Markov + state-space model architecture and schemas (#605)".

The five deleted from `processing/` took the designed exit: the commit that moved them there says "consume 5 triggers", and no other trigger was ever moved there; the seven others left by other doors. And "594 orphans" is the size of the archive, not the number of triggers nobody consumed: 615 − 5 = 610 were never consumed (609 written by the producer): 594 archived, 9 pending and 7 removed.

With a *removed* term the books close: 615 = 603 + 12, every folder balances, and name by name the 603 files are where the history leaves them. **That closure is by construction.** Git stores snapshots and computes additions and deletions by comparing consecutive ones; adding the differences up returns the last snapshot, which is the files. The closure shows that the history was read completely (a negative control that erases one deletion record puts the books off by one), and nothing about the triggers. Two results could have come out otherwise: the 12, and the match between 613 commit subjects announcing a trigger and the files their commits added, one of the announced type each. Subject and file type both come from one variable of one workflow step, so this shows only that each run committed its own file. The other two files came with a commit reporting the driver's first autonomous cycle and with a research commit.

### Practice Exercise 3

Account for the 606 deletions from the pending folder. Then compute the closed-system discrepancy and the share of the created files that the archive holds.

> **Answer:** `5` moved to `processing/`, `594` moved to `archived/` and `2 + 5 = 7` deleted outright: `5 + 594 + 7 = 606`. Discrepancy `615 − 603 = 12`. Archive share `594 / 615 = 96.59%`.

**Synthetic.** Where a log and a shelf are counted separately, as in a warehouse, the balance itself can fail. `scenarios.json` holds five hand-written cases of eight imaginary events, answers fixed in advance:

| Case | Created − listed | Same, minus recorded removals | Unbalanced folders | Misplaced items |
|---|---|---|---|---|
| clean | 0 | 0 | 0 | 0 |
| removal on record | 1 | 0 | 0 | 0 |
| unrecorded loss | 1 | 1 | 1 | 1 |
| unrecorded copy | −1 | −1 | 1 | 1 |
| loss and copy together | 0 | 0 | 0 | 2 |

### Practice Exercise 4

A dashboard shows the first three columns only, and all read 0. Which cases does that leave open, and which check separates them?

> **Answer:** Two: the clean case, and a loss and a copy that offset each other. Only the name-by-name comparison separates them: in the last case one event is expected in the archive and missing, and another is listed in two folders. Balanced counts show the net error, not the number of errors.

## 4. Turning the analogy into a claim that can fail

**Observed.** The [policy that defines p_L](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/compounding-metrics-policy.yaml#L124-L131) says where it is tracked: "state/driver/health-scores.json trend fields". At the pin [that file](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/health-scores.json) holds, for each of four repositories, a composite score, a date and a one-word trend: 0 values of p_L, and no count of beliefs. The same policy reads p_L three ways: constant, "symmetry preserved"; increasing, "healthy compounding"; decreasing, "symmetry broken; investigate root cause".

A claim says something only through the outcomes it forbids (Popper 1959). Between two cycles p_L can fall, stay or rise. Strict conservation forbids two of the three. PSY-001's first sentence forbids one, a fall while the process is consistent, provided consistency is recorded without looking at p_L; its second forbids another, no decay after a recorded break. The three-way reading forbids none: a fall is itself taken as the sign that the symmetry broke.

### Practice Exercise 5

Synthetic. Six imaginary cycles gained 6, 7, 5, 4, 6, 6 validated beliefs and lost 1, 2, 2, 3, 1, 1. A separate log says that the compound phase ran at all five levels in every cycle except the fourth. Compute p_L per cycle (cycles_elapsed = 1) and test the three versions.

> **Answer:** p_L = 5, 5, 3, 1, 5, 5. *Conservation:* p_L changes on 3 of the 5 steps: refuted. *PSY-001's first sentence:* 3 steps join two consistent cycles (1 to 2, 2 to 3, 5 to 6) and p_L falls on one, 2 to 3: refuted. *Three-way reading:* the steps are labelled stable, declining, declining, growing, stable; nothing contradicts it, and no series could. The series is invented; the record that makes the claim testable is a consistency log kept apart from p_L.

**The strongest objection to this lesson's reading** is that its left side is not production either. "Created" means "committed": the workflow at the pin [writes a file, then pulls and pushes](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L82-L90), and a run whose push failed left nothing in the repository. The 615 and the 12 are lower bounds. **This history cannot distinguish a workflow that never lost an event from one that lost events before they were committed.** GitHub's list of the workflow's runs would settle it.

## Sources, limits, and next check

**Observed** at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`: `state/triggers/` (checked by Git tree id), its Git history and the five files linked above.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-021/extract.py`, then `analyze.py` in the same folder; `analyze.py --check` compares a fresh run with the saved results. The [README](../../../fixtures/psychohistory/psy-021/README.md) gives a recount without the scripts.

**Method references.** Noether, E. (1918), "Invariante Variationsprobleme", *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257 ([EuDML](https://eudml.org/doc/59024)); English translation by M. A. Tavel, *Transport Theory and Statistical Physics* 1(3), 1971, doi:10.1080/00411457108231446. Meadows, D. H. (2008), *Thinking in Systems: A Primer*, Chelsea Green. Popper, K. (1959), *The Logic of Scientific Discovery*, Hutchinson. Chacon, S., and Straub, B. (2014), *Pro Git*, 2nd edition, Apress, ["What is Git?"](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F).

**Not done.** The content of the twelve deleted files was not read: their types and dates come from their names, the reasons for their deletion from commit subjects. Neither the workflow's run list nor its earlier versions were read. No value of p_L was computed from project data: the file named for it holds none, and no other source was searched. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** On GitHub, count the workflow runs that wrote a trigger and compare with the 613 producer commits. More runs than commits means events were lost before they were counted; equality means the 12 deletions are the whole loss.
