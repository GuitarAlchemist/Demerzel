---
module_id: fut-003-agent-substitution-readiness-drill
department: futurology
course: Rehearse an Agent Substitution Without Losing Evidence
level: early-intermediate
prerequisites: [fut-002-routing-embedder-revisit-triggers]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: futurology-2026-10-12-003
version: "0.1.0"
---

# Rehearse an Agent Substitution Without Losing Evidence

> **Department of Futurology** | Early intermediate | 35 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will specify a small capability contract, evaluate a synthetic replacement-agent drill, and write a measurable trigger for revisiting the current setup. **Project question:** if a more capable agent or tool appears during the pre-AGI period, how can GA and Streeling try it without losing the evidence that makes its work reviewable and publishable? This lesson does not predict when such a system will arrive. It treats a new agent as a candidate implementation of a workflow with observable outputs.

The [GA agentic-engineering guide at `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/methodology/agentic-engineering.md) recommends improving the harness, keeping clear module seams, using bounded queues, and making review efficient. Those are project design choices, not evidence that any agent is interchangeable today. [FUT-002](fut-002-routing-embedder-revisit-triggers.md) asks when GA should reopen one routing-embedder decision. Here we widen the question to the *agent that performs a course task* and the evidence it must hand to the next stage. The decision remains reversible: compare a candidate on a small, representative task set before changing the normal lane.

## 1. Specify what must survive a substitution

Imagine that an agent drafts or edits a Streeling lesson. The next worker needs to know exactly what source was checked, what tests ran, what a human reviewed, and what the public site actually serves. The draft [review-candidate generator at Demerzel `74d425d`](https://github.com/GuitarAlchemist/Demerzel/blob/74d425dcd2ad92b4712160e3f5df7b2472c12b97/scripts/streeling_review_candidates.py) indexes source Git blobs for triage; its output explicitly does not grant human approval. The draft [Learn receipt work](https://github.com/spareilleux/learn/pull/170) explores carrying exact source identity into rendered pages. Neither draft proves a production end-to-end handoff.

A useful **proposed** interface between stages is:

```text
Draft(source_revision, artifact)
  -> Checked(same_source_revision, named_checks)
  -> HumanReviewed(same_source_revision, reviewer_verdict)
  -> PublicReadback(same_source_revision, URL, observation)
```

This notation is a teaching sketch, **not an implemented DSL or a guarantee supplied by type names**. A real boundary needs authenticated provenance and replayable checks. `HumanReviewed` cannot be produced by the drafting agent simply because it emitted that word; the reviewer and verdict must come from an authorized human process. `PublicReadback` needs a fetch of the deployed page at the intended revision. If a lesson changes after review, the previous verdict does not automatically apply to the new bytes.

For a bounded trial, require at least these observations per task: input source identity; output and review target identities; named build and targeted checks; a human review outcome; anonymous public readback; elapsed time; and corrections needed. These are candidate acceptance fields, not claims that today's agents or site already record them all. A more powerful model might still require a different prompt or tool adapter. The contract is about verifiable behavior at the seam, not about identical internal reasoning.

### Practice Exercise 1

The output reports `fixture-A-v2`, while its input and synthetic review target say `fixture-A-v1`. The build passes. Can the old verdict authorize publication of that output? What must happen next?

> **Answer:** No. The reviewed and output source identities differ, so the old verdict does not cover the changed output. Inspect the change and obtain a verdict bound to the new exact source before publication. A passing build checks a different property.

## 2. Run a deliberately small synthetic drill

The pinned [fixture and evaluator at Demerzel `7892390`](https://github.com/GuitarAlchemist/Demerzel/tree/789239053dfeca9f044d2f893a3f277cb4ed9d8d/state/streeling/fixtures/futurology/fut-003) contain four imaginary adapters and the same three labeled cases, `A`, `B`, and `C`. Each row has source, output, and review target labels, a verdict label, three named checks, minutes, and correction count. All `approved` strings are **fictional fixture values**, not human review receipts. The `public_readback` string is likewise a fixture check, not a site fetch. Run `python state/streeling/fixtures/futurology/fut-003/evaluate_drill.py` from the Demerzel root to reproduce the table.

| Synthetic adapter | Admissible cases | Median minutes, only when all cases pass | Corrections, only when all cases pass | Reason to retain or reject |
|---|---:|---:|---:|---|
| `current` | 3/3 | 40 | 2 | Comparison baseline |
| `portable` | 3/3 | 32 | 2 | Candidate for a larger trial |
| `fast` | 1/3 | not reported | not reported | A changes source identity; B lacks public readback |
| `shortcut` | 0/3 | not reported | not reported | All three review verdicts are pending |

The evaluator treats source identity, review outcome, and required checks as **hard gates**. It reports a median only for an adapter that passes all comparable cases. This avoids praising a fast run that skipped the costly part of delivery. The same cases and the same gates make the synthetic comparison internally consistent, but three made-up tasks say nothing about actual model reliability, tool costs, learner value, or expected time savings. The calculated difference, `40 - 32 = 8` minutes, is a fixture result only.

### Practice Exercise 2

The `fast` adapter finishes case B in 16 minutes. Its source labels agree and its synthetic verdict says `approved`. Why is case B rejected, and how many of `fast`'s three cases are admissible?

> **Answer:** Case B lacks the required `public_readback` check. Case A has a source-identity mismatch; only C passes. Thus `fast` is 1/3 admissible. The fixture does not prove that any actual page is public even for C.

### Practice Exercise 3

Compute the medians of `current` (`40, 44, 39`) and `portable` (`31, 32, 34`). What is their difference, and what performance claim would still be unjustified?

> **Answer:** Sorted values are `39, 40, 44` and `31, 32, 34`, giving medians 40 and 32 minutes. The difference is eight synthetic minutes. It would be unjustified to claim an eight-minute real saving, lower monetary cost, or greater reliability without running comparable real cases and recording the complete evidence chain.

## 3. Choose a trigger and a falsifier before switching

An **if/then trigger** is more useful than saying “switch when AI becomes better.” For example: *if a candidate adapter passes the same source, review, check, and public-readback gates on a predeclared set of real GA/Streeling tasks, then run a limited comparison; expand only if accepted public outcomes and reviewer effort improve without a higher correction rate.* The threshold and task mix must be chosen before examining results. One could start with an equal number of audio, DSL, and course-publication tasks, but that allocation is a proposed trial design, not a validated sample size.

The strongest counterargument is that a common interface can hide important differences. An agent may need different context, permissions, or prompts; forcing identical instructions can handicap it. The trial should keep **outcome gates identical** while allowing documented adapter-specific setup. Record time spent on setup, human review, retries, and repair. If an apparent speed gain disappears once those costs are included, the substitution is not an operational improvement. If a new agent can draft more courses but human verdicts and correct public readbacks stay flat, the end-to-end course goal has not accelerated.

The simplest alternative is to keep the current agent and improve a verifier or reviewer packet. Reject the substitution hypothesis if a comparable trial fails any hard gate, raises correction rate, or gives no sustained gain in correctly reviewed and publicly read-back work. A single failed task may call for diagnosis rather than permanent exclusion; an unreviewed output cannot be promoted by averaging it with successful tasks. The decision record should include the source commit and blob, task class, evaluator version, reviewer identity, site readback, environment, and elapsed time. Cost and latency are measurements to add, not values to invent.

### Practice Exercise 4

Suppose a real replacement agent drafts 20 lessons where the current agent drafts 10 in the same period, but human approvals and correct public readbacks both remain at four. Which metric improved, which outcome did not, and what work might help first?

> **Answer:** Draft throughput doubled. Authenticated approvals and correct public readbacks stayed at four, so this observation does not show faster delivery of usable courses. Inspect reviewer workload, source-bound packets, publication, and readback before adding more drafting capacity. Compare correction and learner outcomes as guardrails.

### Practice Exercise 5

Write a short decision for the synthetic `portable` adapter: what can the fixture support, what would trigger a real trial, and one result that would falsify a switch?

> **Answer:** The fixture supports only that `portable` passes the three *simulated* hard-gated cases and has median 32 synthetic minutes versus 40 for `current`. A real trial is triggered by an available candidate that can produce the required evidence on a predeclared representative task set with the same outcome gates. Failure to preserve exact source identity or human/public evidence, or no sustained accepted-output gain after counting setup and correction time, would falsify a switch. The fixture alone authorizes no production change.

## Sources, limits, and next check

Project context comes from the pinned [GA harness and queue guide](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/methodology/agentic-engineering.md), the [Demerzel triage generator](https://github.com/GuitarAlchemist/Demerzel/blob/74d425dcd2ad92b4712160e3f5df7b2472c12b97/scripts/streeling_review_candidates.py), and the draft [Learn exact-source receipt PR](https://github.com/spareilleux/learn/pull/170). The [input, evaluator, and result](https://github.com/GuitarAlchemist/Demerzel/tree/789239053dfeca9f044d2f893a3f277cb4ed9d8d/state/streeling/fixtures/futurology/fut-003) are synthetic and reproducible at commit `789239053dfeca9f044d2f893a3f277cb4ed9d8d`. The sketch is a proposed composable contract, not a deployed DSL. No real alternate-agent run, authenticated human verdict, learner trial, production switch, or public course readback was performed for FUT-003. The next check is human subject review of the scenario and a blinded learner attempt before localizing or publishing the lesson.
