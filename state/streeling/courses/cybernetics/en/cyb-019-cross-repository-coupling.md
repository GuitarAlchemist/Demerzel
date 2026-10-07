---
module_id: cyb-019-cross-repository-coupling
department: cybernetics
course: "Bound a Cross-Repository Feedback Cycle"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation, cyb-017-local-versus-global-stability]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# CYB-019: Cross-Repository Coupling

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration candidate; English draft, review and translations pending

## Objectives

- Draw a dependency graph with an explicit meaning for each directed edge.
- Trace a cyclic notification and distinguish transport activity from new work.
- Implement generation-scoped deduplication without suppressing a legitimate new generation.
- State which durability and concurrency guarantees the local experiment leaves untested.

## 1. Local success can create remote work

A repository rarely owns every consequence of its output. Publishing a contract change in A may cause B to regenerate a client. B's result may then cause A to update a compatibility record. Define an edge A→B to mean “applying a change at A schedules the same generation for B.” It does not mean that A imports B, nor that B has authorized a write. Ambiguous arrows make dependency diagrams difficult to audit.

Our synthetic graph has A→B and B→A. A root event carries generation g1. No new semantic change is created when a notification is forwarded; it is the same generation. Processing A schedules B, processing B schedules A, and so on. Every local handler completes successfully, while the composed system remains busy. We therefore need a system-level acceptance condition, not merely handler exit codes.

### Practice exercise and correction

List the first six applications without deduplication. **Correction:** A/g1, B/g1, A/g1, B/g1, A/g1, B/g1. There are six handler applications but only two distinct repository/generation pairs. A metric counting handler completions would exaggerate useful progress.

## 2. Preserve causal identity

The solution keeps a set of processed keys `(repository, generation)`. Before applying an event, check whether that pair was processed. If so, consume the duplicate without applying or forwarding it. Otherwise, record the pair, apply it and schedule dependents. The sequence becomes A/g1, B/g1; the returning A/g1 is skipped, and the pending queue empties.

The repository component matters: recording only g1 globally would incorrectly suppress B's first application. The generation component matters too: recording only A would suppress a later real change at A. A generation must identify the actual change or root cause, not each network attempt. Minting a new generation on every forward would bypass the guard and restore the cycle. These are domain decisions; a random identifier alone does not specify their meaning.

### Practice exercise and correction

Should A/g2 run after A/g1? **Correction:** yes when g2 identifies a new semantic change. It has a different key. But retrying the same g1 under a new random label is not a new change; it defeats deduplication. Document how the generation is assigned and propagated before relying on this guard.

## 3. Bound inspection without disguising failure

The fixture stops inspecting the mutant after 12 applications. It reports the remaining pending event and `bounded: false`. This is a test-harness limit, not a controller cure. Silently declaring completion at that point would hide the loop. The negative control must expose remaining work. An acyclic A→B→C positive control processes three applications even without deduplication, proving that an ordinary dependency chain can terminate.

The local simulation is sequential, in memory and failure-free. A production implementation would need to coordinate the processed-key record with the actual effect. Recording before an effect can lose work after a crash; recording after an effect can repeat work after a crash. Concurrent deliveries can both observe absence unless the admission operation is atomic. This lesson identifies those gaps rather than claiming exactly-once behavior from a Python set.

Google's engineering account describes how failure and overload can propagate through dependencies. That motivates checking the composed system; it does not validate our generation guard on any production deployment. See [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).

### Practice exercise and correction

The inspection cap is reached with one event pending. What status belongs in the receipt? **Correction:** bounded inspection ended with unresolved work. Record applications=12, pending=1 and the repeated generation. Do not label the workflow completed, drained or globally stable.

## 4. Apply a guard and test its false-positive boundary

From the package overlay root, run:

```powershell
python scripts/course-exercises/cyb_systems.py --json
```

The exact experiment `cross_repo_generation_cycle` uses solution function `propagate`. It checks two applications and an empty queue for g1 with deduplication. It also runs g2, which must produce two applications; otherwise the guard is too broad. The mutant disables deduplication and must retain pending work after 12 applications. The acyclic control must process A, B and C exactly once in its simple chain.

For a deeper exercise, draw a diamond A→B, A→C, B→D, C→D. Under the same semantics, D/g1 should apply once even though two notifications arrive. A guard that works only for two-node cycles may fail this convergence pattern. If B and C make different semantic changes, however, they need distinct generations and cannot safely be collapsed. The diagram and identity definition must agree before selecting the expected result.

### Practice exercise and correction

Why can a changed filename be an insufficient generation key? **Correction:** repeated changes to the same filename are distinct changes, while one causal change may affect several filenames. Use a domain-specific immutable change identity or equivalent verified content/version identity, and preserve the rule in the receipt. This fixture uses g1/g2 labels solely to teach that distinction.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** define the arrow, trace the mutant, explain both key components, and identify the crash/concurrency gap. Require all four before application. Record initial and revised beliefs and explain disagreements; numerical confidence is not generated from this score.

**Behavioral, 4 points:** run the four scenarios, retain pending-work evidence, demonstrate g2 is not suppressed, and predict the diamond result under a stated identity rule. Require four points plus observed code execution before marking transfer. No learner outcome is claimed by the author. If understanding remains unresolved after three attempts, follow the existing policy escalation.

## Journal, proof and synthesis

Keep graph version, root identity, ordered applications, skipped duplicates, pending events, inspection cap and exact guard version. Record both the successful g1 drain and the failed mutant. Synthesize: the guard bounds this finite sequential graph for one immutable generation; it allows a new generation to run. It does not prove atomic effect execution, durable recovery or behavior when handlers generate new semantic changes indefinitely. CYB-002 discusses dampening channels between repositories; this module examines causal coupling and the identity of repeated work. CYB-011 addresses lane transitions and CYB-016 Petri transitions, rather than this dependency-event identity. CS-002/004 discuss general agentic completion and effect boundaries; their full course content remains separate.

## Further reading

- [Google SRE, Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), practitioner primary source, inspected 2026-10-07.
- Existing `cyb-002-active-dampening-cross-repo-oscillation`; preserve its dampening analysis instead of duplicating it.

*Locally authored under streeling-cyb-20261007; no Seldon research cycle, publication or learning outcome claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_systems.py).
