---
module_id: net-004-semantic-backpressure-and-evidence-dependencies
department: network-science
course: "Test Semantic Backpressure with Evidence Dependencies"
level: intermediate
prerequisites: [net-003-worker-lane-coverage-and-fragility]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-12-004
version: "0.1.0"
---

# Test Semantic Backpressure with Evidence Dependencies

> **Department of Network Science** | Intermediate | 40 minutes | English hypothesis lesson; review and publication pending

## Objectives and project question

After this lesson, you can distinguish a capacity or mode cut from an unsatisfied evidence prerequisite, draw the receipt dependencies of one proposed action, evaluate a small compositional rule without confusing a missing receipt with a denial of authority, and state when the new rule should be rejected. **Project question:** could per-action evidence dependencies keep unrelated work moving while preventing a Streeling draft from being called reviewed or published before its required receipts exist? This is a design hypothesis, not a deployed Demerzel, Gaia, or Learn controller.

## 1. Start from the existing control

[NET-003](net-003-worker-lane-coverage-and-fragility.md) models Demerzel's worker-to-work-class graph. Its pinned [lane policy](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) and [advisory selector](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) cut assigned paths when a fan-out mode blocks their work class. A blocked class receives `SYSTEM.BACKPRESSURE_HIGH`. The selector also checks forbidden and assigned roles, but it does not inspect a course's subject-review evidence, a Learn source SHA, or a learner result. Its exit code 0 means evaluated; the decision is in the JSON payload. These are source observations at `ecdc6c27559bb1a11343cfad33687465893e9891`, not a report of current worker state.

Call backpressure **semantic** only if it depends on a declared property of the *requested outcome* and its evidence. For example, a mode rule may defer all new features during DRAINING. A proposed course-publication rule would instead defer `publish(NET-003)` when a required human review for the same source revision is missing, while allowing an unrelated audio-fixture analysis to proceed. Neither rule creates a human reviewer or grants merge authority. A simple review flag may already be enough; the dependency formulation earns its complexity only if it improves decisions in a measured comparison.

### Practice exercise 1: identify the source of backpressure

In DRAINING, Demerzel's pinned selector blocks `claude`'s primary `builder_fixer` role because `net_new_feature` is mode-blocked, but recommends its secondary `test_author` role because `fix` survives. Separately, a course has `review.completed=false`. Which condition is a mode cut, which could become an unsatisfied evidence prerequisite, and does either authorize publishing the course?

> **Answer:** The two lane decisions are mode and role decisions from the selector. The missing course review could leave a *proposed* publish prerequisite unsatisfied if the publication contract requires that review. Neither gives publication authority. A recommended test-author role does not satisfy a missing subject review or turn a draft into an approved course.

## 2. Draw action-to-receipt dependencies

Represent one candidate action `a` and its required evidence as a directed dependency graph with an explicit `all(a)` node. Each `receipt r -> all(a)` edge supplies one prerequisite; `all(a) -> a` enables the action only when every required receipt is present, valid for the declared scope, and bound to the same source revision. This arrow is a prerequisite, not a command to create a receipt. For `publish(NET-003)`, consider three candidate prerequisites: a committed course revision `S`, a Learn build made from `S`, and a human subject verdict on `S`. A learner attempt may come from an accessible prepublication pilot; otherwise it is a postpublication learning outcome, not a prerequisite to make the course accessible. This is a **teaching contract** for evaluation, not the current site's implemented deployment policy. Authorization and fluent localization review would be additional, separate gates for an actual release.

Define `ready(a,S)` as the conjunction of the action's declared receipt predicates. A missing human verdict is `unknown` or `not supplied`, not `false expertise`; a mismatched revision is an invalid binding, even if a reviewer liked an older version. Do not turn a count such as “two of three receipts” into partial permission. Keep the unsatisfied input visible. The graph should also contain an independent action, such as `analyze(AUD-003 fixture)`, with its own inputs; a missing NET-003 review should not automatically block that action.

### Practice exercise 2: evaluate an AND dependency

Suppose course source and a matching Learn build exist for `S`, but the subject verdict is absent. The audio-fixture analysis has its required input receipt. Which prerequisite is unsatisfied, and what remains runnable?

> **Answer:** The subject-verdict input to `all(publish)` is unsatisfied, so the `all` node cannot enable `publish(NET-003,S)` under the stated teaching contract. This is an AND prerequisite, not a one-edge graph cut: source and build inputs remain present. `analyze(AUD-003 fixture)` remains runnable through its independent inputs, and the draft can still be revised. The result is “publication prerequisites incomplete,” not “the entire agent system is halted.”

## 3. Compose a rule without inventing a runtime

The following is a **notation sketch**, not an implemented DSL or API:

```text
publish(course, S) <- all(
  committed(course, S),
  build_from(S),
  human_subject_review(course, S)
)
```

`all` is a pure conjunction over typed receipt checks. Each check returns a bounded verdict and the evidence identity it examined. A failed lookup must carry a reason such as `missing`, `stale_revision`, or `invalid_scope`; collapsing those into one false bit would hide the corrective action. A later authorization check is not another factual receipt that an agent may manufacture. This sketch composes predicates at the level of an action and its proof obligations, rather than asking agents to exchange low-level API calls. It does not specify a parser, effect executor, locking protocol, or governance authority.

### Practice exercise 3: detect revision drift

A human verdict names source SHA `S0`, while the build and proposed publication name `S1`. All three receipt *types* are present. What does the sketch return, and why would checking only receipt counts be wrong?

> **Answer:** `human_subject_review(course,S1)` is unsatisfied because the verdict binds to `S0`, so `publish(course,S1)` is deferred under the sketch. Three files are not three valid proofs for one revision. The operator needs a new review of `S1` or a documented reviewer decision that explicitly covers its diff; the notation itself cannot decide substantive equivalence.

## 4. Try to disprove the extra mechanism

The strongest counterargument is that existing `review.completed` and `publish.completed` flags, a source-SHA guard, and ordinary CI checks may express this case more simply. A graph and DSL could duplicate policy, produce stale or circular dependencies, block useful work through a false positive, add review latency, and create an attractive but unauthorized “green” indicator. A receipt may be syntactically present yet substantively wrong. A semantic prerequisite rule can therefore be worse than a clear manual checklist.

Compare the candidate with that simpler baseline on a finite set of real, redacted course changes and deliberately altered receipts. Before testing, define outcomes: false admission of an unreviewed or stale-source publication must remain zero; count unnecessary blocks of independent work; measure decision time; and record whether reviewers can explain each decision. Reject the candidate if it adds no observable accuracy or throughput benefit over the simple flags, if it hides a required human decision, or if its proof obligations cannot be maintained at actual source-change rates. An independent adversarial review must inspect the rule before it becomes normative.

### Practice exercise 4: find a false positive

A global gate blocks every Demerzel task while NET-003 lacks a human subject verdict. The team also needs to rerun an unrelated IX signal fixture whose inputs and authority are already available. Which metric would expose the error, and what is the simpler correction?

> **Answer:** Count this as an unnecessary block of independent work. Scope the review gate to `publish(NET-003,S)` and its dependent actions, leaving the IX fixture path alone. A per-action checklist could make the same correction without a new DSL; the dependency graph is justified only if it handles additional cases better.

## 5. Apply the hypothesis to a pinned project record

At Demerzel source commit [`29e83e0`](https://github.com/GuitarAlchemist/Demerzel/blob/29e83e08120cba99452020c54c31680c28b32c3e/state/streeling/course-productions/cp-network-science-2026-10-11-003.json), NET-003's production record has `review.completed=false` and `publish.completed=false`. The English course has a [local selector-replay receipt](../../../reviews/net-003-selector-replay-2026-10-12.json), but that receipt proves only the bounded advisory selector experiment. It is not a human subject verdict, a learner outcome, or a Learn deployment receipt. The separate [Learn sync guard](https://github.com/spareilleux/learn/blob/3f4de745f56e81f237159997473253546d7f6d64/scripts/sync-streeling.mjs) rejects a dirty Demerzel source checkout when claiming its HEAD as provenance; it does not approve course content. The record and guard are concrete project artifacts, while the proposed evidence-dependent rule remains unimplemented.

### Practice exercise 5: write an evidence-bounded decision

Using only those pinned artifacts, write the status for `publish(NET-003,S)` and one next action. Name one observation that would falsify a claim that a future semantic-backpressure rule improved this workflow.

> **Answer:** Publication is not admissible under the teaching contract: the record explicitly leaves review and publish false, and the selector replay is not a subject verdict. Continue source and review preparation; obtain a human subject verdict bound to the accepted revision before reconsidering publication. A learner attempt can be collected through an accessible prepublication pilot or evaluated as a postpublication learning outcome. If a tested rule admits publication without its declared prerequisites, it violates the zero-false-admission guard. If it makes exactly the same decisions as the existing flags while adding delay and maintenance, its claimed benefit is also falsified. The pinned record does not prove that any such rule is deployed.

## Evidence and limits

- The pinned Demerzel selector and policy establish mode and role behavior only. The NET-003 replay is a dry-run source experiment; it does not observe live lanes.
- The pinned NET-003 production record establishes draft phase flags at one revision. A later edit may change them, so re-read the exact source and review receipts before acting.
- `semantic backpressure`, the dependency graph, the notation, and the benchmark are proposed concepts. They need a real baseline comparison, explicit authority boundaries, learner testing, translation, Learn preview, and public readback before any operational or educational approval. An independent AI adversarial review identified and prompted corrections to the graph and pilot assumptions; it does not replace a human subject review.
