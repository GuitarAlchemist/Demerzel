---
module_id: cyb-020-central-versus-recursive-control
department: cybernetics
course: "Delegate Control Without Multiplying Authority"
level: intermediate
prerequisites: [cyb-001-vsm-ai-governance-mapping, cyb-019-cross-repository-coupling]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# CYB-020: Central Versus Recursive Control

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration candidate; English draft, review and translations pending

## Objectives

- Separate a centrally defined resource envelope from decisions delegated within it.
- Calculate a two-level allocation and prove its leaves cannot exceed the root budget.
- Reject over-allocation and stale authority using explicit counterexamples.
- Identify which temporal, fairness and concurrency guarantees an offline admission test leaves open.

## 1. Decide what authority is being delegated

A central controller can approve every action, or allocate bounded authority to branches that make local decisions. Recursive control repeats the allocation rule at each level. It does not mean that each child receives the entire parent budget. Here an envelope is the maximum number of unit-cost actions permitted for one fixed accounting interval. All quantities are nonnegative integers, actions consume one unit, and units cannot be borrowed from a later interval.

Our synthetic root permits 10 units. It delegates 4 to branch A and 6 to branch B. A divides its allocation into leaf caps [2,2]; B uses [3,3]. The leaves observe local demands [3,3,5,2]. This is a teaching tree with fixed grants, reliable observations and sequential decisions. It is not a description of live agents or a measured organizational deployment.

Central and recursive approaches can both respect 10. A central scheduler could inspect all four demands and choose an allocation within 10. The recursive scheme uses less global decision detail but constrains local choices through prior grants. Neither scheme's fairness, latency or throughput has been measured here.

### Practice exercise and correction

If B grants 6 to each of its two leaves, is its delegation valid? **Correction:** no. The children request 12 units from a branch authorized for 6. Repeating an allowance at each child multiplies authority instead of allocating it. The root's approval of B does not approve an additional 6.

## 2. Prove conservation before discussing performance

At every internal node require sum(child caps) <= parent cap. Each leaf serves min(its cap, its demand). The numerical result is [2,2,3,2], totaling 9. Leaf demands total 13; four requested units are unserved, while one allocated unit at B's second leaf is unused. That spare unit is not automatically available to another leaf. A reallocation would be a new decision requiring its own accounting.

The bound follows directly: each served value is at most its leaf cap; leaf caps under A sum to at most 4 and those under B sum to at most 6. Therefore total service is at most 4+6=10. Repeating this argument upward proves the same property for any finite allocation tree under these assumptions. This algebraic result is stronger than testing one demand vector, but applies only while grants refer to the same interval and resource.

### Practice exercise and correction

Why does safe service of 9 not demonstrate optimal allocation? **Correction:** total demand is 13 and the root allows 10. A permitted reallocation could potentially serve a tenth unit. Safety establishes the upper bound; optimality would require an objective, reallocation rules and a separate comparison. Equal-cost arithmetic does not establish fairness between learners or tasks.

## 3. Authority has a version as well as a quantity

An epoch is an integer identifying the currently valid grant configuration. The fixture's admission check accepts a request only when the grant epoch equals the current epoch and spent+request <= cap. At epoch 7, a leaf with cap 3, spent 1 and request 2 is admissible: 1+2=3. The same request after spending 2 is rejected: 2+2=4. A grant from epoch 6 is rejected even with ample unused capacity.

This is an epoch-validity check, not a complete time-expiring lease service. There is no wall clock, expiration deadline, authenticated issuer or distributed revocation protocol. Its callers must provide nonnegative cap and spent values and trustworthy current state. During real reconfiguration, work admitted under an old grant might still be running. Rejecting later old-epoch requests does not revoke those effects or reset their resource consumption. Define how outstanding work and remaining authority are transferred before using a new epoch.

### Practice exercise and correction

Two concurrent callers both read spent=1, cap=3, then request 2. Can both rely on a successful predicate? **Correction:** no. Each individually passes, but combined spending reaches 5. Admission and reservation must be one atomic operation on shared accounting state. The fixture is sequential and does not establish this guarantee.

## 4. Connect the contract to executable evidence

From the package overlay root, run:

```powershell
python scripts/course-exercises/cyb_systems.py --json
```

The exact experiment is `recursive_envelope_lease`. Solution function `validate_tree` rejects a negative root, negative children or children exceeding the parent; `admit_lease` tests epoch equality and remaining capacity. Inspect the recorded root, branches, leaves, demand and served trace. The positive control requires total service 9, total leaf allocation 10 and admission at the exact remaining-capacity boundary.

The negative control rejects three malformed allocations: root 10 with children [6,6], parent 4 with children [3,3], and root 10 with children [-1,5]. It also rejects a stale epoch and an over-budget request. The output's `naive_leaf_total: 24` denotes the unsafe hypothetical allocation of 6 to every leaf; it is a labeled comparison constant, not an executed mutant service trace. Do not present it as measured throughput.

### Practice exercise and correction

Would testing only [4,6] under root 10 detect a validator that always accepts? **Correction:** no. Successful inputs alone cannot distinguish correct validation from unconditional approval. The three invalid allocation checks must fail admission. Conversely, rejecting every input fails the valid boundary control. Both controls are necessary.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** explain delegated authority, derive the root bound, calculate the trace and distinguish an epoch check from revocation. Award one point each; require all four before application. Capture initial and revised beliefs with uncertainty; a quiz score does not generate numerical confidence.

**Behavioral, 4 points:** run the exact fixture, preserve its inputs and hash, show both controls, and document an atomic reservation requirement with reconfiguration accounting. Require all four and observed execution before confirming application. This authoring run assesses software, not a learner. Follow the existing Streeling policy's three-attempt limit and escalation procedure when comprehension remains unresolved.

## Journal, proof and synthesis

Record the grant tree, accounting interval, resource unit, epoch, demand, spending, rejected requests and fixture version. Attach the execution receipt and an explicit statement of absent concurrency and expiry tests. Synthesize: local allocation preserves the root envelope through conservation; delegation alone does not create new authority. The experiment exercises sequential boundary checks. It does not prove real-time response, fairness, durable accounting or live system viability.

CYB-001 supplies the VSM mapping and recursive-governance question; this module adds a worked resource contract. CYB-019 concerns event propagation identity, not resource grants. MAT-024 derives dynamical stability; budget conservation is not a stability certificate. CS-002 supplies general loop bounds, and CYB-021 applies iteration accounting to one task. Preserve those courses rather than duplicating their scope.

## Further reading

- Existing `cyb-001-vsm-ai-governance-mapping` and `cyb-002-active-dampening-cross-repo-oscillation`, inspected in this package's source snapshot.
- Package solution `scripts/course-exercises/cyb_systems.py`, experiment `recursive_envelope_lease`; the synthetic definitions and arithmetic above are its complete model assumptions.

*Locally authored under streeling-cyb-20261007; no Seldon research cycle, publication or learning outcome claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_systems.py).
