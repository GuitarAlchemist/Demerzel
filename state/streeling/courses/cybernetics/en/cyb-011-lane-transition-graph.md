---
module_id: cyb-011-lane-transition-graph
department: cybernetics
course: "Operational feedback: guarded execution states"
level: intermediate
prerequisites: [cyb-010-observable-stop]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Lane Transition Graphs: Legal Paths and Stale Events

> **Cybernetics** | Intermediate | 45 minutes | Provisional CYB-011

## Objectives

- Draw the five-state execution graph and identify forbidden shortcuts.
- Evaluate event, authorization and resource guards independently.
- Reject completion events from an earlier generation after resumption.
- Explain why graph validity alone does not establish concurrency safety.

A lane here means one logical unit of scheduled work. Its state describes the scheduler's contract, not a screen label. The permitted 2026-10-06 incident distinguished acceptance from durable completion and independent verification. We use that distinction to justify a separate completion guard; we do not reproduce the original project or claim this graph was its implementation. All transitions below execute on local values in an offline fixture.

## 1. State names need operational meanings

Use queued, running, draining, stopped and done. Queued work has no admitted execution. Running work owns an execution lease. Draining work admits nothing new and waits for accounted work to settle. Stopped work retains resumable state. Done work has a verified result and is terminal for this logical operation.

Our allowed directed edges are queued→running on admit; running→draining on stop; draining→stopped on drained; running→done on complete; stopped→queued on resume. Every other pair is illegal. We intentionally omit a failed state and cancellation rollback. An implementer needing them must specify new meanings and edges before changing the validator; mapping every failure to done would erase evidence.

### Practice exercise and worked correction

Can queued→done be accepted if an event says “complete” and has a verified flag? Can done→queued be used to start another task?

**Correction:** Neither edge exists. Verification does not authorize bypassing admission. Done is terminal for this task; a new task needs a new logical identity. This preserves the meaning of the completion record rather than changing yesterday's result into today's queue item.

## 2. Events and guards constrain each edge

An edge says where a transition may go; a **guard** says when it may happen. Admission requires authorization and a lease. Stop requires authorization. Drained requires zero in-flight work. Completion requires zero in-flight work and a verified result. Resume requires authorization and zero in-flight work.

The [W3C SCXML specification](https://www.w3.org/TR/scxml/#transition) distinguishes transition events, conditions and targets. Our small Python table borrows that general separation, not the SCXML execution algorithm. It implements no interpreter, hierarchy, parallel states or event queue. Defining “guard” prevents the common mistake of treating a named event as sufficient evidence for its intended effect.

### Practice exercise and worked correction

A lane is draining, count one. A drained event arrives with correct identity. Evaluate the edge and guard separately. Next evaluate running→done with count zero but unverified output.

**Correction:** Draining→stopped is a legal edge for drained, but its guard fails at count one. Running→done is legal for complete, but the result-verification guard fails. In both cases preserve the old state and record rejection; never partially apply the transition because one component passed.

## 3. Generation counters fence old observations

Associate the lane with generation three. A complete event also names generation three. After a successful resume, advance the generation to four. An old generation-three result then cannot complete the new run. This prevents an **ABA problem** in our model: the lane can return to the same visible state while referring to a different incarnation.

Trace queued(3)→running(3)→draining(3)→stopped(3)→queued(4). Subsequent admission retains four. The counter changes at resume, not at every intermediate edge, so all events for the active execution can share the incarnation identity. It is an arbitrary teaching policy; a production system may use unique run identifiers instead. Require event generation equal to current generation before applying any edge.

### Practice exercise and worked correction

Running generation four receives verified completion generation three and count zero. Why is it rejected, and why is comparing only state strings insufficient?

**Correction:** The generation guard fails even though completion's resource and verification guards pass. State strings say running in both incarnations. A stale observation can therefore look current unless execution identity is preserved. Resetting a counter to zero on restart would create another identity collision unless a durable outer identity distinguishes the restart.

## 4. Apply the graph without claiming a race fix

Execute the fixture with an absolute package path:

```text
python <package>/scripts/course-exercises/cyb_operations.py --json
```

Test ID `guarded_lane_graph` covers the five-state stop/resume path and a separate verified completion. Six rejection cases check illegal shortcut, busy drain, stale completion, unauthorized resume, unverified completion and restart from done. `transition` returns a new state/generation tuple only after validation. No mutable shared lane or external effect exists in this lesson's code.

Real concurrency requires atomic ownership of the read-check-write operation and fencing of side effects. Two callers could otherwise both read queued, both pass the guard and start duplicate work. A pure function cannot prevent that race. Similarly, incrementing a local counter does not stop an old worker writing directly to an unfenced sink. These are explicit integration gaps, not details a graph can wish away.

### Practice exercise and worked correction

Two threads read queued(4) and each has a lease boolean true. Both call the pure function successfully. What property is missing? Propose a test before proposing a new framework.

**Correction:** Exclusive admission is missing. Specify a single authoritative atomic claim or existing transactional compare-and-set, then interleave two contenders against it and require exactly one admitted winner. The fixture's offline graph checks do not run that experiment. Using two true booleans is no proof of exclusive ownership.

## Assessment, journal and synthesis

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Stage one: draw every allowed edge, give a failed guard example, and explain the generation-four stale event. Award two points each; require five of six and correct stale rejection. Stage two: change one event generation in a scratch trace, predict rejection, execute it and preserve the unchanged prior state. Require a correct trace, a negative receipt and an explanation of atomic integration limits before recording applied knowledge.

Journal the initial identity, event sequence, guards, resulting state and script hash. Synthesize graph validity separately from race safety: this model rejects the documented illegal transitions and stale events, but no concurrent scheduler, durable store or terminal integration was exercised. CYB-010 validates stop evidence; this course validates reachable states and fencing identities. CYB-016 will address token/transition behavior rather than duplicate this single-lane graph. IDs remain provisional, translations and independent review pending, and no learner result or publication is asserted.

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_operations.py).
