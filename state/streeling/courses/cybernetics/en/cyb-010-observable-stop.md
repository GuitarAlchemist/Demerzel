---
module_id: cyb-010-observable-stop
department: cybernetics
course: "Operational feedback: evidence of termination"
level: intermediate
prerequisites: [cyb-001-vsm-ai-governance-mapping, cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Observable Stop: Establishing Quiescence Without Guessing

> **Cybernetics** | Intermediate | 40 minutes | Provisional CYB-010

## Objectives

- Distinguish a stop request, an acknowledgement and observed quiescence.
- Validate an ordered stop chain using request identity and execution epoch.
- Reject busy, stale and incomplete stop evidence.
- State the observation interval and residual visibility limits of a stop claim.

An authorized continuation observed on 2026-10-06 produced a distinct acceptance acknowledgement and later a durable completion artifact with an independent output check. The permitted incident facts contain no session details and no interruption experiment. They motivate a general lesson: acknowledgement is evidence of acceptance, not execution completion. The stop protocol below is a synthetic teaching contract, not a claim about that system's shutdown implementation.

## 1. Define what must cease

An idle-looking interface may hide queued work, child workers or writes already in flight. Define the scope of a stop: this worker, this generation, its admissions and its accounted work. **Quiescence** means no work remains within that stated scope. It does not mean a machine is powered off or unrelated workers have stopped.

For our fixture, the stop contract closes admission, drains in-flight work, persists a validated checkpoint, and then acknowledges the stop. Cancellation and graceful draining are different policies. We choose draining because abandoning a partially written result would need additional rollback semantics. The model assumes one authoritative admission gate and accurate in-flight accounting; failure of either breaks its meaning.

### Practice exercise and worked correction

A worker displays “stop accepted” while its in-flight counter is two. What statement is justified?

**Correction:** Acceptance is observed; quiescence is not. Under the drain contract, both accounted tasks must settle before zero can be asserted. Do not infer they were cancelled. Record the timestamp and counter, then obtain subsequent evidence through the authorized observation channel.

## 2. Build an ordered evidence chain

Each event contains a request identity, execution epoch and strictly increasing sequence number. An **epoch** labels one worker incarnation; it prevents old evidence being mistaken for a new run. Our five stages are:

| Sequence | Event | Required evidence |
|---|---|---|
| 1 | request | authorized true |
| 2 | admission_closed | same identity and epoch |
| 3 | drained | in-flight count zero |
| 4 | checkpoint | durable and independently validated flags |
| 5 | stop_ack | after the preceding stages |

These names and their meanings are local to the fixture. We neither read real processes nor force a shutdown. A validated checkpoint means that a separate verifier supplied the flag; the exercise does not implement disk durability or checksum verification. That abstraction must be documented rather than hidden behind a boolean.

### Practice exercise and worked correction

Events one through four use request R1 and epoch seven; event five is epoch six. All sequence numbers increase. Is the chain valid?

**Correction:** No. Ordering cannot repair identity mismatch. The acknowledgement may belong to an older incarnation. Retain both records and classify evidence incomplete for epoch seven. Similarly, reusing sequence four for the acknowledgement violates strict ordering even if its timestamp looks later.

## 3. Separate instrumentation from operational proof

[OpenTelemetry's tracing API](https://opentelemetry.io/docs/specs/otel/trace/api/) provides timestamped span events and an end operation. Ending a span does not by itself drain a worker. An instrumentation boundary and a workload boundary are separate contracts. Trace sampling, missing export and process failure can remove useful observations; therefore absence of a late event is not automatically evidence that late work never happened.

Our fixture validates a supplied complete event list. A production assertion would also state who observed admissions, when the gate closed, whether child work is included and how long observation continued. A record that ends at sequence five supports the stop chain only for the represented interval. A later admission invalidates continued quiescence and should reopen investigation, rather than silently rewriting the old record as proof of uninterrupted stopping.

### Practice exercise and worked correction

The chain is valid at sequence five. Sequence six records newly admitted work in the same epoch. What changes?

**Correction:** Continued quiescence is contradicted. The fixture rejects the extended chain. Preserve the original and new evidence, inspect the admission gate and ownership scope, and report the interval over which the earlier statement held. A successful stop acknowledgement cannot override observed subsequent work.

## 4. Apply and falsify the stop checker

Run the offline solution, substituting the package path:

```text
python <package>/scripts/course-exercises/cyb_operations.py --json
```

Test ID `ordered_stop_evidence` invokes `stopped`. The complete five-event chain is the positive control. Busy drain, stale epoch, unvalidated checkpoint, late admission and an acknowledgement alone are rejected. The mutant “accept any stop_ack” returns true for the last case, exposing precisely why phrase matching is insufficient. No session receives this code or any stop command.

### Practice exercise and worked correction

In a private scratch fixture, set checkpoint durability true but validation false. Predict the result. Then change only the validation flag and explain what additional real-world evidence would justify that change.

**Correction:** False becomes true for this synthetic chain. Operationally the flag needs a verifier's recorded checkpoint identity, content check and relevant persistence guarantee. Changing the boolean to obtain a green result supplies none of those. Preserve the failed result as a lesson about the boundary between a modeled assertion and its real evidence source.

## Assessment, journal and synthesis

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Stage one: identify what ACK proves, explain stale epoch rejection, and describe visibility limits. Score each answer zero to two; require five of six and no claim that acknowledgement alone proves stopping. Capture the learner's initial uncertainty separately from the grade. No learner was assessed in producing this material.

Stage two: submit a predicted classification for complete, busy and stale traces, execute the checker and explain a late-work contradiction. Require all three classifications plus a preserved failure receipt. Observe the learner's actual action before marking knowledge transfer; a supplied solution file is not proof that someone learned it.

Journal the UTC interval, request/epoch scope, source of each assertion, exact script hash and rejected trace. Synthesize the successful chain as “valid under this complete-event-list model.” Do not extend it to unseen children, crash recovery, distributed drains or permanent inactivity. CYB-001 supplies governance context and CS-002 supplies externally bounded loops; this module contributes explicit stop evidence rather than a new loop framework. Independent review, localization and real stop implementation remain pending.

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_operations.py).
