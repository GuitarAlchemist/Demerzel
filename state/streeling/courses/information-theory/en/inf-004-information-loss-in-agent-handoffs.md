---
module_id: inf-004-information-loss-in-agent-handoffs
department: information-theory
course: Information Loss in Agent Handoffs
level: intermediate
prerequisites: [inf-002-optick-compact-vector-information-loss]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-12-004
version: "0.1.0"
---

# Information Loss in Agent Handoffs

> **Department of Information Theory** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Identify which facts a GA handoff note guarantees and which remain free-form claims.
- Demonstrate an information-losing collision between distinct delivery states.
- Calculate a decision loss for a small, explicitly synthetic handoff fixture.
- Design a compact handoff that retains the evidence needed for one named decision, while respecting source and authority boundaries.

## The project question

GA's pinned [Antigravity bridge](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Scripts/antigravity-bridge.ps1) lets one AI surface leave a note for another under `state/handoffs/`. The script records `from`, a timestamp, branch, a short Git head, the number of dirty working-tree lines, and a free-form handoff string. It describes the filesystem as the shared surface between the two AIs. This is useful navigation, but the script does not verify tests, review, writer ownership, or publication. The free-form string may mention them; their presence and truth are not enforced by the bridge.

The practical question is: **Can a short handoff preserve enough information for the next agent to decide whether a change is ready to integrate?** That question is narrower than asking whether the note is a good summary of an entire session. The answer depends on the decision and on evidence that the receiver can check. A branch and a headline may locate work, while a failed test or a competing writer changes the integration decision.

INF-002 demonstrated a many-to-one mapping from raw OPTIC-K vectors to compact vectors. The same mathematical shape appears here: two different delivery states can map to the same short headline. We use information theory as a lens on **decision-relevant loss**, not as a claim that GA's bridge implements an entropy code, that the classroom sample estimates a real incident rate, or that any handoff field by itself grants merge authority.

## 1. Separate location from evidence

Read the pinned script's [`Handoff` branch](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Scripts/antigravity-bridge.ps1#L102-L129). It writes a timestamped Markdown file and captures branch, short head, and a dirty-line count using Git. A short head helps locate a revision, but an exact reviewed artifact needs a full immutable commit and, when content changes independently, a file blob. A dirty-line count of zero tells us only what the local Git command counted at that moment; it does not establish that a test ran or passed. The note body is whatever the caller supplies to `-Handoff`.

The bridge's example says a task “landed” and points to tests. That example is guidance for a human writer, not a machine-checked success receipt. If the receiving agent's decision is *open the right file*, branch/head plus a path may be enough. If the decision is *integrate this change*, it also needs the exact source, writer scope, test result tied to that source, review outcome, and an authorized integration path. These are different receiver questions, so there is no universally sufficient one-line summary.

### Practice exercise 1: name the missing evidence

A note contains `branch=feature/audio`, `head=abc1234`, `working_tree_dirty_lines=0`, and `Audio work ready`. Which of the following are proven by the bridge: the branch name, a passing audio test, single-writer ownership, and review approval?

> **Answer:** The branch value is captured from local Git when the script writes the note. The script records no test verdict, ownership claim, or review verdict; `ready` is unverified prose. The short head and zero dirty-line count do not fill those gaps. Even the branch value is a local observation, not proof that the remote branch or its reviewed source has the same state later.

## 2. A small collision with a measurable consequence

The fixed [INF-004 fixture](../../../fixtures/information-theory/inf-004/handoff-cases.json) contains four invented cases, all with the headline `ready`. Each case carries three boolean facts: `tests_passed`, `single_writer`, and `review_approved`. For this **teaching decision only**, a case is eligible if all three are true. A real project would also need exact source and authorization checks; the toy model omits them to isolate one information-loss mechanism.

| Case | Headline | Tests passed | Single writer | Review approved | Toy eligibility |
|---|---|---|---|---|---|
| A | ready | yes | yes | yes | yes |
| B | ready | no | yes | yes | no |
| C | ready | yes | no | yes | no |
| D | ready | yes | yes | no | no |

The headline encoder maps four different evidence states to the same output. A receiver who sees only `ready` cannot distinguish A from B, C, or D. This proves a collision in the fixture; it does not prove how often a real GA handoff is misleading. The local [evaluator](../../../fixtures/information-theory/inf-004/evaluate_handoffs.py) reproduces the table and costs:

```powershell
python state/streeling/fixtures/information-theory/inf-004/evaluate_handoffs.py
```

### Practice exercise 2: construct the counterexample

Which pair of cases is enough to disprove the claim “the headline `ready` uniquely determines eligibility”? What information was lost?

> **Answer:** A and B have the same headline, but A passes all three toy gates while B fails the test gate. Their identical encoded value has different eligibility, so the headline cannot determine the decision. A and C or A and D also work. At least the distinguishing gate value was lost.

## 3. Price the wrong decision, then challenge the model

The fixture assigns an invented cost of 10 units to accepting an ineligible case and 1 unit to rejecting an eligible one. These are classroom weights, not observed defect costs. A headline-only receiver must take the same action for all four cases. `accept all` makes three false accepts: total cost `3 × 10 = 30`, mean cost `30/4 = 7.5`. `reject all` makes one false rejection: total cost `1`, mean cost `1/4 = 0.25`. Given this sample and these asymmetric costs, the lower-cost constant action is to reject all. The point is not to recommend blanket rejection; it is to show why a compressed message can force a poor choice.

With the three evidence booleans available and trusted **within the toy fixture**, the receiver applies the toy rule to each case and makes no classification error, for mean cost zero. In a live workflow, merely adding boolean text would not make it trustworthy. Tests should link to a command, result, and exact revision; ownership to a claim or agreed write scope; review to an identifiable verdict on the exact blob. A receiver can then verify each link instead of trusting a self-reported status.

### Practice exercise 3: calculate the decision loss

For the four rows and displayed costs, calculate the mean loss of `accept all`, `reject all`, and the full-evidence toy rule. Which constant action is cheaper here?

> **Answer:** `accept all`: three false accepts cost 30 total, so `7.5` per case. `reject all`: A alone is a false rejection costing 1 total, so `0.25` per case. The full-evidence rule classifies all four toy rows correctly and costs `0`. Rejecting all is the cheaper **constant** action for this invented sample and cost choice, not a general project policy.

### Practice exercise 4: test sensitivity

Keep the four cases but change the false-accept cost from 10 to `0.1`, leaving false rejection at 1. Which constant action has lower mean cost? What does the reversal teach?

> **Answer:** `accept all` now costs `3 × 0.1 / 4 = 0.075`; `reject all` remains `1/4 = 0.25`, so accepting all is cheaper under the new weights. The best action depends on the decision's loss model. Neither set of invented costs estimates the real cost of a bad integration or proves what GA should automate.

## 4. Keep the minimum checkable handoff

For an integration decision, propose a handoff record with a **full** commit and relevant blob IDs; repo, branch, and worktree; the single writer and write scope; test command, exit result, and source revision; review verdict and reviewed blob; and the exact next requested action. The recipient should independently compare those references against the current checkout and review state. This is a candidate handoff contract, not an assertion that the current GA bridge emits or validates it. It is intentionally task-specific: a visual navigation handoff may need a screenshot or file line instead of a review verdict.

Why not copy an entire transcript? It may contain much irrelevant context, stale claims, and material the receiver cannot check quickly. The better design question is which facts are **sufficient for the named next action** and which uncertainty must remain explicit. A compact record can point to larger immutable artifacts. If the references cannot be resolved or the reviewed blob differs, the integration decision should stop for new evidence, not silently infer success from the word `ready`.

### Practice exercise 5: write a falsifiable handoff

You receive `GA audio change ready; tests pass`. Write the minimum follow-up fields needed to decide whether to integrate it. Name one observation that would refute a claimed `ready` state.

> **Answer:** Ask for the full GA commit and changed blob IDs, worktree/branch, one-writer write scope, exact audio test command and result tied to that commit, review verdict tied to those blobs, and the requested integration action or authority. If the recorded test ran on a different commit, a reviewer saw a different blob, or another writer owns the same files, the claimed integration readiness is refuted. This does not require the note to prove audio quality; that needs its own listening and signal-evaluation protocol.

## Limits and next check

The pinned GA script at commit `dc2e74cbd992a298f67efb928b5b3754615e1924` establishes what the bridge writes, not the truth of any past handoff. The four rows and costs are synthetic. The evaluator checks arithmetic and basic fixture shape; it does not measure compression in bits, real agent error rates, test provenance, or merge safety. The next bounded experiment would sample actual authorized handoffs, define the recipient decision in advance, compare each note with immutable test/review/source receipts, and count missing decision-critical facts. Privacy and authorization would govern that sampling. A failure to reduce wrong or delayed decisions compared with the existing bridge would reject the proposed richer format.
