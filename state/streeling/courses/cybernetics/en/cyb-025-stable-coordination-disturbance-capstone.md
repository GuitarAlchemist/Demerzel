---
module_id: cyb-025-stable-coordination-disturbance-capstone
department: cybernetics
course: "Governed loops: coordination capstone"
level: advanced
prerequisites: [cyb-011-lane-transition-graph, cyb-017-local-versus-global-stability, cyb-019-cross-repository-coupling, cyb-021-iteration-budget-admission, cyb-022-external-progress-measurement, cyb-023-receipt-chain-verification]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Stable Coordination Under Disturbance: An Evidence Capstone

> **Department of Cybernetics** | Advanced | 45 minutes

A worker can finish the wrong generation while the coordinator still displays healthy queue sizes. Another can repeat a valid completion and make a naive counter reach its target twice as fast. This capstone combines bounded admission, measurement, and receipt identity in one small event model. Stability here means preserving declared invariants and settling a finite trace; it is not a proof of dynamical stability for every distributed execution.

## Objectives

- Preserve request conservation and worker exclusivity after every event.
- Reject stale, duplicated, and invented-generation completions.
- Reconstruct a disturbed trace and identify its actual completed requests.
- Separate demonstrated safety from liveness assumptions and deployment claims.

## 1. State the Contract Before the Trace

There are three fictional requests, `r1`, `r2`, and `r3`, and two workers, A and B. Each request occupies exactly one of three sets: pending, active, or done. These sets must remain disjoint and their union must remain the original three requests. At most two requests may be active, and each worker owns at most one active request. A done set prevents duplicated completion from increasing the completed total.

An assignment carries an epoch: an integer that increases when that request is assigned again. Only a completion matching the active request, worker, and epoch may move it to done. A failed assignment returns the request to pending. We assume one sequential event processor with atomic state changes; distributed storage, worker crashes during persistence, and genuine concurrent transactions are outside this fixture.

**Exercise.** Pending contains `r3`, active contains `r1`, and done contains `r1` and `r2`. The total count is four. Is checking that total is at least three sufficient?

**Worked correction.** No. Request `r1` appears in two sets, violating exclusivity even though every original request is represented. Check disjointness, exact union, unique pending entries, active capacity, and unique worker ownership. A scalar count cannot replace these invariants.

## 2. Walk the Disturbance Numerically

The eleven-event fixture assigns `r1` to A at epoch one, assigns `r2` to B at epoch one, fails A's assignment, and completes B's. It then assigns `r1` to B at epoch two. A late completion from A at epoch one is ignored. B completes epoch two; a duplicate of that completion is ignored. Finally A receives `r3` at epoch one; an invented epoch ninety-nine completion is ignored, then the genuine epoch-one completion is accepted.

The active-request counts after these events are `1,2,1,0,1,1,0,0,1,1,0`. The done counts are `0,0,0,1,1,1,2,2,2,2,3`. Eight events change state; three disturbances produce observations without changing ownership. Completion is the exact done set `{r1,r2,r3}`, with active and pending empty, not a worker's self-report. The event sequence is synthetic, not a measurement of any real fleet.

**Exercise.** After the fifth event, which completion for `r1` is admissible: `(A,1)`, `(B,1)`, or `(B,2)`? Explain each decision.

**Worked correction.** Only `(B,2)` matches current ownership. `(A,1)` belongs to the failed assignment; `(B,1)` uses the current worker with the wrong epoch. Matching only request identity or only worker identity would accept an invalid result. The full tuple is the admission boundary.

## 3. Compose Controls Without Hiding Their Assumptions

CYB-021's budget applies to state-changing actions; an implementation must also bound observation traffic so endless stale messages cannot consume unlimited resources. The supplied trace has eleven observations and eight accepted actions. It demonstrates finite behavior for these inputs, but the coordinator class itself is not a production rate limiter. An external driver would need an independent observation allowance and a stopping receipt at exhaustion.

CYB-022 contributes the external completion measure: accepted unique requests, not log activity. CYB-023 contributes identity binding. The epoch check blocks obsolete evidence from releasing a current assignment, and deduplication keeps an already completed request from being counted again. These controls preserve safety in the model. Eventual completion still assumes workers produce results, valid events are delivered, and pending work eventually receives service. Silence can preserve every safety invariant forever while making no progress.

**Exercise.** Remove the last valid `r3` completion. Every invariant still passes. Should the journal say stable and complete?

**Worked correction.** Report invariant preservation but incomplete work: `r3` remains active and the done set has two requests. Record the last observed event and the missing result. Completion cannot be inferred from lack of errors. A deadline may stop observation, but its expiry produces a bounded unresolved result, not success.

## 4. Apply the Capstone and Inspect a Mutant

Run `cyb_governed_loops.py --json` using its actual package path. Record `CYB-025`, test ID `disturbance_capstone`, uses the `Coordinator` solution. Read `apply`: assignment checks capacity and worker ownership; completion and failure require exact active-tuple equality; every event checks the invariant. Positive control finishes the three unique requests. Negative controls preserve the active retry after the stale result, reject a duplicate, and reject the invented future epoch.

For a deliberately wrong design, delete the epoch-and-worker match and accept any completion with a known request ID. The stale event would complete `r1` while B still owns its retry. Conservation alone might remain apparently correct if the mutant deletes the active entry and adds done; the identity contract would nevertheless be violated. This illustrates why several invariants must be checked rather than treating one reassuring count as a complete correctness argument.

**Exercise.** Identify a new negative test for assignment rather than completion, and specify the expected result.

**Worked correction.** While A owns `r1`, attempt to assign `r3` to A. It must be ignored, leaving `r3` pending. Alternatively assign a third active request while both workers are busy; capacity must reject it. These tests extend the observation surface without contacting a real worker or creating a new framework.

[Offline solution and executable controls](../../../../../scripts/course-exercises/cyb_governed_loops.py): record `disturbance_capstone`.

## Two-Stage Assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Conceptual stage, four points: reconstruct the count trace, state disjointness, explain stale epochs, and distinguish safety from liveness. Require all four. Behavioral stage, four points: run the eleven-event trace, preserve the stale-retry counterexample, add the busy-worker assignment rejection, and document the incomplete trace without its last completion. Require correct outputs and truthful claims. No learner or live coordination system has been assessed by writing this lesson.

## Key Takeaways

- Conservation, exclusivity, and identity each need their own check.
- A stale epoch must not release or complete a current assignment.
- Settling one finite trace does not establish universal stability or liveness.

## Journal, Proof, and Synthesis

Record event index, request, owner, epoch, classification, state counts, invariant outcome, and exact done set. Preserve ignored disturbances as evidence rather than removing them from the trace. Synthesize: this implementation settled this finite synthetic trace and rejected three identity disturbances. It does not establish atomic distributed storage, arbitrary interleaving safety, fairness, throughput, deployment, or every possible disturbance. A new failure should revise the controller fixture and this capstone together.

## Further Reading and Overlap Boundary

CYB-002 surveys dampening mechanisms; this capstone tests the composition of identity and conservation controls. MAT-024 addresses mathematical stability, a stronger and different objective than finite event invariants. CS-002 surveys governed loops; the capstone requires reconstructing an adversarial trace. [Lamport's event-ordering paper](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) gives causal-order context; our request model and epoch contract are authored teaching choices. Translation and independent review remain pending.
