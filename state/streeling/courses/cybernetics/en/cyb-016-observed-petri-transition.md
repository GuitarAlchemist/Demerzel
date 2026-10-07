---
module_id: cyb-016-observed-petri-transition
department: cybernetics
course: "Verify an Observed Petri Transition"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation, cyb-015-failure-recovery-logical-identity]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Verify an Observed Petri Transition

> **Department of Cybernetics** | Intermediate | 45 minutes | Provisional integration ID; translations and review pending

## Objectives

- Map a bounded worker lifecycle to places, tokens and transitions.
- Check whether an observed before/after pair matches an enabled firing.
- Detect a skipped transition and a missing resource release with explicit counterexamples.
- Separate model invariants, observed evidence and atomic commitment requirements.

MAT-023 already teaches Petri nets, reachability, invariants and limits of enumeration. This module applies a small part of that mathematics to operational observation. It does not replace MAT-023 or claim that a diagram validates a live lane. CYB-011 addresses general lifecycle graphs; here a separate capacity token makes resource conservation explicit.

## 1. Represent one task and one worker slot

A Petri net has places holding token counts and transitions consuming and producing tokens according to arcs. A transition must have enough input tokens before firing. The Petri Nets 2000 tutorial presents Place/Transition net occurrence rules and marking graphs. [Jörg Desel, Place/Transition Nets I](https://www2.informatik.uni-hamburg.de/tgi/PetriNets/introductions/pn2000_introtut.pdf), printed pages 85–90.

Our places are `(ready, running, done, free)`. Initial marking is `(1,0,0,1)`: one task awaits work and one worker slot is free. `start` consumes one ready token and one free token, producing one running token. It yields `(0,1,0,0)`. `finish` consumes one running token and produces one done token and one free token, yielding `(0,0,1,1)`.

The free token describes capacity, not another task. Confusing those types would double the apparent task count. We model one task, one slot and successful finishing only. Cancellation, failure, drain, retries and creation of further tasks are omitted; this bounded example cannot describe an entire deployment without extending its places and transitions.

### Practice Exercise 1

At marking `(1,0,0,0)`, may `start` fire? Why can a queue still have ready work when no start is enabled?

**Worked correction:** No: the free input token is missing. Ready work and available execution capacity are separate requirements. A backlog does not authorize unlimited workers. Investigate the capacity owner instead of silently adding a free token to make the diagram move.

## 2. Calculate the expected successor

For each place, successor count equals current count minus the transition's input weight plus its output weight. The fixture's `fire` first rejects insufficient input tokens, then calculates this successor. A modeled transition specifies what **would** happen if it fires; an observation validator additionally compares that expected successor with the recorded after-state.

Two invariants hold in this model: `ready + running + done = 1` and `running + free = 1`. The first conserves the task across its lifecycle. The second conserves the single execution slot. After correct finish, both hold. A defective finish that produces done but forgets free yields `(0,0,1,0)`: task conservation still holds, while resource conservation fails.

### Practice Exercise 2

An audit checks only task conservation and accepts `(0,0,1,0)` as complete. What did it miss? Is preserving both invariants sufficient to identify which transition occurred?

**Worked correction:** It missed the slot release. Both invariants are necessary checks for these transitions, but alone do not identify the event. Initial and final markings both satisfy them; skipping `start` and reporting `finish` still violates the enabling rule. Check the named transition and full before/after pair.

## 3. Validate observations, not intended arrows

The observed-step validator receives a before marking, a named transition and an after marking. It calculates the expected successor and compares exactly. The positive trace is initial → start → running → finish → done. The first negative control names `finish` at the initial marking: no running token exists, so it is rejected. The second names `finish` at the running marking but records the missing-release state; it is rejected despite conserving the task.

In an operational receipt, include task identity, model version, observation version, before state, event, after state and evidence origin. Without identity, one worker's start might be paired with another worker's finish. Without a consistent snapshot, counts from different times can fabricate an impossible marking. A completion marker is useful evidence but does not automatically reveal every intermediate transition or resource release.

### Practice Exercise 3

Only a final artifact and a completion marker are available. May you report that the exact modeled start and finish transitions were independently observed?

**Worked correction:** No. The final artifact may support completion under its own contract, but the intermediate transitions were not observed. Report the narrower result and missing trace. Do not turn a plausible reconstruction into a claim of direct measurement.

## 4. Close the stale-observation commitment gap

Two controllers may both read version zero with one ready task and one free slot. Each computes a valid start. Validation alone does not stop both from acting. The fixture demonstrates a version check: the first proposal commits only when its expected version equals the current version, increments it, and causes the second version-zero proposal to be rejected. Exactly one proposal commits.

This arithmetic illustrates compare-and-set semantics; it is not a concurrent database implementation. A real controller needs an atomic check and update in the storage or resource owner, together with a contract connecting admission to the actual effect. Otherwise a valid token model and a valid receipt can coexist with duplicate execution. CYB-015 handles identity and unknown effects; neither course supplies a new orchestration framework.

### Practice Exercise 4

A controller checks the version, launches a worker, then updates the version. A second controller checks during the launch. Is this equivalent to the fixture's commitment boundary?

**Worked correction:** No. Both can pass before either updates the version. Reserve capacity atomically before launch, define rollback or reconciliation if launch fails, and test that interleaving. A comment saying “atomic” cannot replace the resource owner's actual guarantee.

## Code application and two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

```powershell
python overlay/scripts/course-exercises/cyb_resilience.py --json
```

Inspect `CYB-016`, test `observed_firing_with_resource_token`. The JSON records arc weights, all three markings, the valid observed trace, two rejected observations and one committed stale proposal. The source includes the solution; run from an isolated copy when changing arcs.

**Conceptual, 4 points:** explain the two token types (1), calculate both successors (1), distinguish invariants from event evidence (1), and locate the stale-read race (1). Require all four with a reasoned revised belief before application; the score is not calibrated confidence.

**Behavioral, 4 points:** reproduce the positive trace (1), reject skipped start (1), reject missing release (1), and propose a new failure transition with stated conservation consequences (1). Observe the learner's next relevant action before recording transfer. Escalate unresolved understanding after three teaching attempts under Streeling policy. The author has executed controls, not assessed a learner.

## Journal, proof and synthesis

Record model and script hashes, place order, arc weights, snapshot identity, expected and observed successors, rejected traces and atomicity assumptions. Synthesize what the model predicted, what the experiment actually observed and what would falsify the implementation mapping. Change code and course together when an omitted failure state becomes necessary.

The evidence validates this synthetic trace and these counterexamples. It proves neither fleet liveness nor safe drain, exhaustive reachability, concurrent atomicity or correctness of deployed receipts. MAT-023 supplies deeper analysis; implementation-level observations remain necessary.

## Further Reading

- Existing MAT-023, `mat-023-petri-nets-reachability.md`: mathematical treatment and enumeration limits.
- Existing CYB-002: coordination survey; new CYB-011 and CYB-015: lifecycle and recovery boundaries.
- [Petri Nets 2000 introductory tutorial](https://www2.informatik.uni-hamburg.de/tgi/PetriNets/introductions/pn2000_introtut.pdf), primary author tutorial verified 2026-10-07; P/T-net section, printed pages 85–90.

*Local English draft; no live lane audit, publication or learner outcome is claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_resilience.py).
