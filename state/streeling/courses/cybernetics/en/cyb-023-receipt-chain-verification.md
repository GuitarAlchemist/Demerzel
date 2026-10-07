---
module_id: cyb-023-receipt-chain-verification
department: cybernetics
course: "Governed loops: delivery evidence"
level: intermediate
prerequisites: [cyb-010-observable-stop, cyb-022-external-progress-measurement]
estimated_duration: "45 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Receipt Chains: Connect a Request to the Artifact Actually Verified

> **Department of Cybernetics** | Intermediate | 45 minutes

An acknowledgement and a completion receipt can both be genuine while referring to different work. A retry may produce generation two while a late result from generation one arrives afterward. A controller needs evidence that binds identity, stage, and artifact rather than a search for the word done. This lesson constructs a small inspectable chain; it is an integrity exercise, not a new transport or cryptographic authentication system.

## Objectives

- Distinguish submitted, accepted, completed, and verified receipts.
- Reject a chain with the wrong request, generation, artifact, or order.
- Recalculate a content digest and detect an altered chain entry.
- Explain why an internally consistent hash chain cannot establish truthful authorship.

## 1. Assign a Claim to Each Stage

Submission records the sender's attempt to deliver work. Acceptance records recipient recognition. Completion records a result artifact. Verification records a checker outcome for that artifact. A successful submission call is evidence about transport, not a recipient acknowledgement. Acceptance does not prove completion, and completion does not establish that the result is correct.

The authorized incident summarized in the writing brief exposed these as separate events: acknowledgement preceded a durable result, then an independent exact-output check. Our fixture uses a fictional request `exercise-job`, generation two, and answer `[2,4]`. It repeats the artifact digest in all four records to simplify teaching. A real protocol might know the result digest only at completion; it must then define an explicit binding from request evidence to result evidence rather than requiring an impossible early value.

**Exercise.** A transport reports success, but the only durable recipient record is accepted. Which delivery claims are supported?

**Worked correction.** Submission and acceptance are supported. Completion and verification remain unestablished. Report the strongest demonstrated stage, preserve its evidence, and continue read-only observation within scope. Sending a duplicate request simply because the result is not yet visible can create a second action rather than more evidence about the first.

## 2. Link Identity Before Ordering

Each synthetic record contains request identity, generation, stage, index, artifact digest, predecessor digest, and verification outcome. The expected stage sequence is submitted, accepted, completed, verified, with indices zero through three. Generation is an attempt family identifier; it is not a timestamp and cannot be inferred from how recent the screen looks.

Suppose generation one finished late after generation two started. A perfectly formatted verified chain for generation one must still fail a check expecting generation two. Likewise a valid chain for another request does not become evidence for this one. Lamport's event-ordering work distinguishes causal order from merely reading physical clock values; here the explicit predecessor relation expresses the fixture's required order. It does not claim every concurrent event has a unique physical ordering.

**Exercise.** You receive four valid hashes for the expected artifact, but acceptance precedes submission in the array. Can sorting by timestamp rescue the chain?

**Worked correction.** No. The supplied chain fails its declared stage and predecessor contract. Investigate source records and causal links. Sorting a display may aid inspection, but it cannot create missing evidence or repair a predecessor field. The fixture rejects reordered entries even when their individual digests remain valid.

## 3. Detect Changes Without Claiming Authentication

Our digest serializes a JSON object with sorted keys, compact separators, and forbidden nonfinite values, then applies SHA-256. This consistent representation prevents harmless key-order differences from changing the fixture's digest. Each record's hash excludes its own hash field; the next record stores that hash as its predecessor. The validator recalculates every digest and compares the artifact digest with the actual artifact supplied to it.

Changing the completed entry's artifact without recomputing its hash fails integrity checking. Recomputing every hash after fabricating all entries can produce a self-consistent fraudulent chain. Hashes establish a relationship between bytes; they do not prove who observed those bytes or whether the checker was honest. A trusted evidence boundary requires authenticated writers, protected storage, and a credible verifier. None is implemented here.

**Exercise.** A worker invents a passing verification result and recomputes the whole chain correctly. What does `verify_chain` prove?

**Worked correction.** It proves structural consistency under the fixture contract, not honest verification. Check the verifier's authority and retained execution evidence separately. Calling a content hash a signature would overstate the implementation. Preserve this limitation in the synthesis, even when every automated assertion passes.

## 4. Apply the Validator to Counterexamples

Run the package's `cyb_governed_loops.py --json` by its actual path. Record `CYB-023`, test ID `receipt_chain`, uses `make_chain` and `verify_chain`. The positive control accepts the four-stage chain for the expected answer and generation. Negative controls reject a two-stage chain, a tampered completed entry, an incorrect generation, a different request, reordered entries, and an altered answer. These controls test different bindings; six identical malformed strings would not provide comparable coverage.

The final record must contain `verification_passed: true`. That field is a claim whose trust depends on the boundary discussed above. The exercise deliberately does not implement a production signing service, persistent transport, or retry scheduler. Its code belongs to offline course fixtures and must not become a consumer runtime dependency.

**Exercise.** Replace the expected answer `[2,4]` with `[2,5]` while leaving the receipt chain unchanged. Predict the result, then run the check.

**Worked correction.** Rejection occurs at the artifact binding. An exact-output checker for one answer does not verify a different answer. Retain both the previous chain and the failed comparison as evidence of the boundary; do not overwrite the chain to make the test appear successful.

[Offline solution and executable controls](../../../../../scripts/course-exercises/cyb_governed_loops.py): record `receipt_chain`.

## Two-Stage Assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Conceptual stage, four points: correctly identify the strongest stage, explain generation binding, diagnose reordered entries, and state the authentication limitation. Require all four before application. Behavioral stage, four points: run the positive chain, reject wrong generation, reject wrong artifact, and preserve exact expected versus actual results. Require every case. This follows Streeling's understanding-then-behavior structure without claiming an observed learner or assigning invented confidence values.

## Key Takeaways

- Bind receipts to request, generation, order, and artifact.
- Acceptance, completion, and verification support different claims.
- A consistent hash chain establishes integrity relationships, not honest authorship.

## Journal, Proof, and Synthesis

Record request label, generation, artifact identity, ordered stages, verifier identity, expected digest, outcome, and trust assumptions. Store synthetic identifiers only for this exercise. Synthesize that the validator establishes a complete internally consistent chain for one artifact under one contract. It cannot prove real delivery, honest execution, publication, or a different task's completion. A future authenticated implementation needs new evidence, not a stronger adjective in this journal.

## Further Reading and Overlap Boundary

[Python hashlib documentation](https://docs.python.org/3/library/hashlib.html) documents the digest API used by the fixture. [Lamport, Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) supports the distinction between causal relations and clock readings. CYB-022 measures progress; CYB-023 binds delivery stages to identity and content. CS-002's checkpoint overview does not supply these replay and artifact-mismatch exercises. Translation and independent review remain pending.
