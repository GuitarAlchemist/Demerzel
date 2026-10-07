---
module_id: cyb-015-failure-recovery-logical-identity
department: cybernetics
course: "Failure Recovery and Logical Operation Identity"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation, cyb-013-circuit-breaker-probe-budget]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Failure Recovery and Logical Operation Identity

> **Department of Cybernetics** | Intermediate | 45 minutes | Provisional integration ID; translations and review pending

## Objectives

- Distinguish known failure, known completion and unknown outcome after a timeout.
- Preserve logical identity across retry attempts and reject changed intent under an old key.
- Reconcile an effect receipt before deciding whether another effect is justified.
- Demonstrate duplicate effects with a retry mutant and state the atomicity limit.

CYB-002 covers backoff; CYB-013 covers admission after failure. Neither decides what happened to an already submitted operation. CS-004 discusses this issue in an audio pipeline. This module supplies a domain-neutral, executable recovery contract rather than repeat that audio experiment.

## 1. Locate the failure in the effect timeline

An operation has at least these stages: prepare intent, submit, apply the effect, record its result, return the reply, verify the result. A reply can disappear after the effect succeeds. A client timeout therefore says something about the observation channel, not necessarily about the effect.

A permitted abstract operational observation from 2026-10-06 showed an authorized continuation producing a distinct acknowledgment, then a durable completion marker and an independent output check. The acknowledgment did not prove completion. We use that distinction as incident motivation, without importing another course's material or private transcript. The numerical ledger below is entirely synthetic and does not reproduce that session.

For an unknown outcome, write `unknown_after_submission`, retain the logical operation key, and inspect the documented evidence surface. If it returns a verified result, reconcile that result. If it returns authoritative evidence that no effect occurred, a bounded retry may be considered under the operation's contract. Absence of a result from a stale replica is not authoritative nonexecution.

### Practice Exercise 1

A service accepts a request, but the client receives no final reply. Which of these descriptions is warranted: failed, completed, or unknown? What does an acknowledgment add?

**Worked correction:** Outcome remains unknown. Acceptance narrows what the receiver reported, but does not establish an applied and verified effect. Preserve both observations separately. A timeout before a connection was established can warrant a different conclusion only if the transport contract establishes that no submission reached the receiver.

## 2. Make logical identity survive transport attempts

Our synthetic operation has key `logical-17` and payload `amount=10`. The service records the payload and result under that key. A repeated request with the same key and payload returns the original result; it performs no new effect. A request with the same key but `amount=11` is rejected as changed intent. Two independent operations may have identical payloads, so a hash of parameters alone cannot always represent user intent.

AWS describes caller-provided request identifiers, changed-parameter validation, and atomic handling of the identifier with the associated effect. [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). This is a contract principle; our fixture does not call AWS or establish that a particular local tool offers this contract.

The identifier names a logical operation; each network attempt may also have its own attempt number for diagnosis. Replacing the logical key on every retry converts transport uncertainty into another logical effect. Keeping the key is only safe where the receiver actually implements deduplication and retains its record for the relevant interval.

### Practice Exercise 2

Two musicians independently request the same export settings. Should both operations share a key derived only from those settings?

**Worked correction:** No. Identical settings do not prove identical intent. Use separate logical identities for independently requested exports, while reusing each identity across its own retries. Scope the identity to the authorized caller and contract; do not infer deduplication from a coincidentally identical filename.

## 3. Inject the lost reply at the dangerous boundary

The fixture's `Ledger.execute` models an atomic visibility boundary: an effect count and receipt become available together. Its injected timeout occurs **after** that modeled commit but **before** returning the reply. After the exception, effect count is one. Inspecting the recorded result recovers the artifact identity. Executing with the same key returns the same result, leaving count one. Changed payload is rejected.

The negative control executes the identical payload under `attempt-1`, loses its reply, and then executes under `attempt-2`. Effect count becomes two. The mutant runs the same modeled server implementation, so the test isolates identity loss rather than changing unrelated infrastructure. Both calls may return plausible artifact data; only the effect count exposes duplication.

### Practice Exercise 3

Suppose receipt writing and effect writing are separate durable steps. Can the in-memory test guarantee recovery after a crash between them?

**Worked correction:** No. The fixture assumes atomic visibility and does not implement durability. A receipt-first crash could report work that never happened; an effect-first crash could lose deduplication and duplicate work on replay. Supply a transactional storage boundary, an authoritative effect query, or an explicit manual reconciliation procedure, then test the actual crash window.

## 4. Recover the right stage of the workflow

Run:

```powershell
python scripts/course-exercises/cyb_resilience.py --json
```

Inspect `CYB-015`, test `lost_reply_same_logical_key`. Expected results are one effect, equality of recovered and replayed results, and rejection of changed intent. The executed mutant has two effects. The solution uses only memory; it writes no external artifact and makes no claim about exactly-once distributed execution.

For code application, separate production from validation. If an artifact exists but its independent validator crashes, preserve its identity and rerun the validator after repairing it. Resubmitting generation may create another effect and blur which artifact was assessed. If artifact provenance is missing, record that gap; do not invent a receipt retroactively. Choose a retry budget and a stopping rule before running the recovery experiment.

### Practice Exercise 4

Generation completed, but a schema validator cannot read its reference file. Should the recovery execute generation again? What would justify a new generation?

**Worked correction:** Repair the reference and validate the preserved output first. A new generation requires a distinct authorized intent or evidence that the existing artifact cannot satisfy the contract, with the previous outcome retained. A validator failure is not itself evidence of generator failure.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** locate the lost-reply boundary (1), distinguish unknown from failed (1), explain logical versus attempt identity (1), and identify the durability assumption (1). Require all four and a reasoned belief revision before application. A numerical quiz score is not a calibrated belief confidence.

**Behavioral, 4 points:** inject the timeout after effect application (1), recover without another effect (1), reject changed intent (1), and execute a fresh-key mutant that duplicates the effect (1). Observe a learner-generated receipt before recording successful transfer. Streeling's maximum three teaching attempts applies to unresolved understanding; the author run is not a learner observation.

## Journal, proof and synthesis

Record failure point, logical key, attempts, payload, effect count, recovered result, mutant result and storage assumptions. In the synthesis, identify which observation changed the recovery decision and which code boundary needs stronger durability. Update the course when an actual implementation falsifies the model.

The evidence proves behavior of this serialized synthetic ledger under one lost-reply injection. It does not prove durable atomicity, authorization, retention against late requests, real tool idempotency or operational recovery. Those remain explicit integration questions.

## Further Reading

- CYB-002 and CYB-013: backoff and admission, retained as different mechanisms.
- Existing CS-004, `cs-004-composable-agentic-audio-loop.md`: domain-specific audio recovery and validation boundaries.
- [AWS Builders' Library, Malcolm Featonby](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), verified 2026-10-07.

*Local English draft; no actual Seldon research cycle, publication, or learner outcome is claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_resilience.py).
