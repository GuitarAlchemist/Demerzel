---
module_id: cs-005-agent-handoff-evidence-contract
department: computer-science
course: Hand Off Agent Work as an Evidence Contract
level: intermediate
prerequisites: ["cs-002-governing-agentic-loops"]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-11-005
version: "0.1.0"
---

# Hand Off Agent Work as an Evidence Contract

> **Department of Computer Science** | Intermediate | 30 minutes | English draft; subject and learner review pending

## Objectives

You will inspect a GA handoff note, identify what it actually proves, test a fixed receiving-agent scenario, and write a next action that can be checked independently. The project problem is concrete: one agent finishes a GA change and another must decide whether to continue, inspect, or stop without inheriting an unsupported success claim.

## 1. Inspect the bridge before trusting the note

GA's [Antigravity bridge at commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Scripts/antigravity-bridge.ps1) has a `-Handoff` mode. It writes a Markdown file under `state/handoffs/` with `from`, `at`, `branch`, `head`, `working_tree_dirty_lines`, and the caller's free-text message. The script asks Git for the current branch, the latest **abbreviated** commit and subject, and the count of short-status lines. It neither runs tests nor checks that the message's claims are true. It does not capture a full revision, the changed-file list, an artifact hash, or the next agent's permissions. GA's [workspace guidance at the same commit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/CLAUDE.md) calls for actor, branch, goal, write scope, tests, evidence, and next ask in a handoff. Those are fields for the producer and receiver to verify, not guarantees supplied by the bridge.

The file is useful because it survives a context switch. It is a **claim with pointers**, not a live observation. The receiver must bind it to a specific checkout and revision and then follow its evidence. An abbreviated `head` and a count of dirty lines are clues; they do not identify the exact uncommitted content. A note in a Git-ignored handoff directory can exist after its original branch has moved.

### Practice exercise 1

From the pinned bridge source, list three fields generated from Git and three things that a receiver still needs to obtain independently before treating “tests passed” as a verified result.

> **Answer:** The script generates `branch`, abbreviated `head`, and `working_tree_dirty_lines`. The receiver still needs the full commit SHA (and current checkout), the exact test command with a result tied to that revision, and the actual diff or artifact plus its location and identity. The free-text message can name these, but the script does not verify them.

## 2. Make the contract small enough to check

A useful handoff names **actor**, **goal**, **branch and full revision**, **write scope**, **test evidence**, **output artifact**, and **next action**. The actor tells the receiver who made the claim; it does not confer authority. The revision says which committed source the claim describes. If there are uncommitted changes, record their paths and a diff or saved patch as well. Write scope names the files the next agent may change and any one-writer boundary. A test claim names the command, where it ran, the outcome, and the revision or worktree state it tested. “Not run” is a valid status; “passed” without an inspectable result is not.

The artifact is the thing to inspect: a path, commit, PR, receipt, or test log, with an identity such as a hash when a file can be replaced. The next action is a bounded instruction such as “inspect the diff and rerun this named test, then request review”; it should not silently authorize merge or publication. In a sibling-repository handoff, name the repository as well as the path. GA's `state/handoffs/` is a local coordination surface; an agent in Demerzel cannot infer that it has permission to read or write there.

Use this **fixed teaching fixture**, not a claim about a current GA session:

```text
H1: note in ga/state/handoffs/example.md
from: agent
branch: codex/example-voicing
head: a1b2c3d fix: adjust voicing selection
working_tree_dirty_lines: 2
body: "Done. Tests passed. Continue the PR."

H2: receiver's independent probe of the same checkout
branch: codex/example-voicing
full HEAD: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
git status --short: M Common/VoicingRule.cs; ?? state/results/voicing.json
test log: absent
claimed output receipt: absent
wrapper: running
```

The abbreviated H1 HEAD `a1b2c3d` does not match the prefix of H2's full `bbbb...` HEAD, so they are different committed revisions. The fixture does not say when H1 was written relative to H2 or whether either revision is an ancestor of the other. Do not invent that history. The handoff needs a revision and artifact check before work continues.

### Practice exercise 2

What can the receiver conclude from H1's dirty-line count of `2` and H2's short status? Compare the two HEAD values: can H1 describe H2's current committed revision, and what remains unknown?

> **Answer:** The note reported two status lines when it was made, while the probe now shows one modified path and one untracked path. Counts and path names alone do not show the bytes or whether the same two changes survived. H1's `a1b2c3d` is not the prefix of H2's `bbbb...` HEAD, so H1 and H2 identify different committed revisions. Their ancestry and chronology remain unknown. Inspect the current diff and untracked artifact before deciding what H1's claims still cover.

### Practice exercise 3

H1 says “Tests passed.” The receiver finds no test log. Write the strongest truthful status and the minimum evidence needed to upgrade it.

> **Answer:** Status: **test pass claimed, not verified**. Ask for the exact command, execution result, and checkout/revision plus dirty-state identity used for the run, or rerun the test in the inspected checkout and save the output. A new pass on H2 would verify H2, not retroactively prove H1's earlier claim.

## 3. Separate presence, progress, and completion

The [CS-004 wmux observation](../../../fixtures/computer-science/cs-004/wmux-dogfood-observation.md) is a real bounded example. A provider ran and exited with code 0, but sibling-repository reads and the receipt write were denied. The marker-aware wrapper found neither the required marker nor the artifact. The coordinator therefore recorded that **no review was completed**. A `running` wrapper shows process state at an instant. A delivered prompt shows dispatch. Even exit code 0 says only that a process ended successfully according to that process. None proves the requested artifact exists or satisfies the task.

The [narrow retry record](../../../fixtures/computer-science/cs-004/review-followup-20261004.md) describes a stronger observation: the declared reads and write appeared in the pane, a receipt file existed with the exact marker, and the wrapper verified it. That supports a bounded advisory review at that point in time. It still does not turn the review into a published course or prove all future agent runs can read sibling repositories.

### Practice exercise 4

For the first CS-004 attempt, classify “prompt delivered,” “wrapper running,” “provider exit 0,” and “review completed.” Which observed facts decide the last claim?

> **Answer:** The first three are dispatch, transient process status, and provider termination, respectively. “Review completed” is false for that attempt: two required reads and the receipt write were denied, and the wrapper found no completion marker or artifact. The receiver should record the failed capability boundary and a bounded permission preflight as the next action.

## 4. Write a receiver-ready handoff

Suppose a GA agent has edited a voicing rule but has not run tests. A receiver can use the following shape. Replace placeholders only with observed values:

```text
actor: <agent identity and surface>
goal: <one user-visible behavior to verify>
repository / checkout: <repo and absolute worktree path>
branch / full HEAD: <branch and 40-character SHA>
uncommitted state: <status paths plus diff or patch identity>
write scope / owner: <exact paths the next actor may edit; current writer>
tests: NOT RUN; <specific command proposed for this checkout>
artifact: <diff, receipt, or output path and hash, or MISSING>
next action: <one bounded inspection or test, then report result>
```

If a source path is inaccessible, report **not assessed**. If a receipt is missing, report **missing**. Do not reconstruct missing evidence from chat history. The receiver should confirm the checkout, resolve the commit, inspect the diff and artifact, and run or examine the named test before continuing. This is an evidence contract because each field either has a check or an explicit unknown state.

### Practice exercise 5

Rewrite H1's body as a handoff the H2 receiver can act on without claiming unobserved success. Include all seven contract elements and a next action within H2's evidence boundary.

> **Answer:** “Actor: agent (surface unknown). Goal: evaluate the voicing-selection change. Repository/checkout: GA, H2 checkout path to be recorded. Branch/full HEAD: `codex/example-voicing` at `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` as observed by H2; H1 identifies a different committed revision, with ancestry and chronology unknown. Write scope/owner: not specified; hold edits until the owner and allowed paths are confirmed. Uncommitted state: `Common/VoicingRule.cs` modified and `state/results/voicing.json` untracked; inspect their content. Tests: H1 claims a pass, but no log is present, so not verified. Artifact: claimed receipt absent; current untracked JSON requires inspection and identity. Next action: resolve H1's commit against H2, inspect diff and JSON, obtain or rerun the exact test in H2, and report evidence before continuing the PR.” The unknown actor surface, scope, and missing receipt remain explicit.

## Sources and limits

The bridge and GA guidance above are pinned to GA commit `dc2e74cbd992a298f67efb928b5b3754615e1924`; the CS-004 observations are pinned to [Demerzel commit `6bc584d`](https://github.com/GuitarAlchemist/Demerzel/blob/6bc584d7ca1cd9eb1b1481e1100eeeb74e983863/state/streeling/fixtures/computer-science/cs-004/wmux-dogfood-observation.md). H1 and H2 are explicitly synthetic and establish no current process or repository status. The CS-004 retry's full local receipt is outside this course repository, so this lesson relies on its checked summary, not an independent reread of that receipt. No new agent run, subject review, learner trial, localization review, or publication is claimed. [CS-002](cs-002-governing-agentic-loops.md) covers loop bounds; this lesson covers the transfer of evidence between actors.
