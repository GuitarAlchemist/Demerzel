---
module_id: cyb-022-external-progress-measurement
department: cybernetics
course: "Governed loops: measurement integrity"
level: intermediate
prerequisites: [cyb-005-measured-signal-and-setpoint, cyb-021-iteration-budget-admission]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# External Progress: Measure Improvement Without Moving the Target

> **Department of Cybernetics** | Intermediate | 40 minutes

A busy worker can repeatedly rewrite a report without resolving a single defect. A changed file hash establishes a change, not useful progress. An observed authorized continuation produced an acknowledgement before a durable result and a separate exact-output verification. That abstract incident motivates the distinction; this lesson uses invented artifact revisions, not the original material, identities, or sessions.

## Objectives

- Classify progress, stall, regression, and stale validation from a numerical trace.
- Keep a fixed target distinct from a worker's completion claim.
- Tie a measurement to the artifact revision it actually checked.
- Reject hash changes and fresh timestamps as sufficient evidence of improvement.

## 1. Choose an External Residual

A residual is the remaining distance from an agreed target. Our synthetic checker counts unmet requirements in a ten-item fixture. The target version is `v1`; completion requires a residual of zero. An independent checker measures the candidate artifact, while the worker proposes edits. Independence here means a separate specified decision rule, not necessarily a separate human or machine. If the same faulty rule creates and checks an answer, agreement can still be wrong.

The residual is meaningful only for this fixed finite checklist. Ten easy satisfied checks may conceal an omitted requirement. Consequently the target specification and checker identity belong in the evidence. A worker cannot remove two difficult requirements, report eight out of eight passed, and claim improvement against the original ten-item target.

**Exercise.** Version one has ten requirements and two unmet ones. The worker replaces the target with eight requirements, all satisfied. Is the residual zero evidence of completion?

**Worked correction.** Not for the original task. The candidate changed the measurement contract. Classify it `target_changed`, keep the original unresolved status, and request an authorized scope decision before judging the new target. A denominator change is not a correction of the missing requirements.

## 2. Follow the Numerical Trace

Start with revision zero, artifact `a0`, and residual ten. Candidate revisions one through four report residuals eight, eight, five, and zero. Each has a different artifact identifier and a validator that checked that exact revision. The classifications are progress, stall, progress, and complete. On the stall, the controller keeps the last accepted baseline rather than treating cosmetic work as useful improvement.

Our admission rule requires a newer revision, a fixed target, a current validation reference, a finite nonnegative measurement, a lower residual, and a different artifact. A larger residual is regression; an equal residual is stall. This strict monotonic rule suits the synthetic checklist but not every research process. Temporary regression may be worthwhile in another process, provided that process declares a different rule before the experiment.

**Exercise.** From accepted revision one with residual eight, classify revision two with residual eleven, then revision three with residual five and `validated_revision: 1`.

**Worked correction.** Eleven is regression. Five with a validator pointing at revision one is stale validation; the number cannot be assigned to revision three. Neither should replace the accepted baseline. A later timestamp does not repair the mismatch between measured artifact and proposed artifact.

## 3. Separate Signals That Look Alike

An acknowledgement says the recipient recognized the request. A work status says processing is underway. A durable result says an artifact exists. A verifier says a particular artifact meets particular checks. These signals answer different questions. They can arrive at different times, be duplicated, or refer to different generations. Polling more often increases observation frequency; it does not make an acknowledgement a completion receipt.

Suppose a report changes only its timestamp while its residual stays eight. Hash-only detection calls it progress; our rule calls it stall. Now suppose the residual improves from ten to eight while the artifact identity remains `a0`. That measurement is unexplained: either the old measurement was wrong, the checker changed, or the artifact identity is incomplete. The correct response is investigation, not an invented causal story.

**Exercise.** Choose the strongest supported claim from these observations: new timestamp, different hash, residual decrease linked to a checked revision, worker says done.

**Worked correction.** Only the linked residual decrease supports improvement under the current rule. A timestamp proves freshness of a report field; a hash proves different bytes; a done statement is a claim requiring verification. None alone demonstrates that the original requirements were met.

## 4. Apply the Checker and Challenge It

Run `cyb_governed_loops.py --json` using the script's actual package path. The `CYB-022` record, test ID `external_progress`, preserves the residual trace and classification sequence. Read solution function `assess_progress`: validation identity is checked before arithmetic is used. Positive control accepts eight, then five, then zero. Negative controls reject stale validation, a moved target, an unexplained same-artifact improvement, and an increased residual. The changed-artifact/equal-residual case defeats a hash-only implementation.

The fixture uses simple identifiers as stand-ins for artifact identities. A real integration should use stable content identities and pin checker versions; string inequality alone cannot authenticate content. Nor does an externally calculated residual cover requirements absent from the checklist. These are explicit limits to the evidence, not reasons to abandon measurement.

**Exercise.** Modify a candidate so the artifact identifier changes but its residual remains eight. What result and journal entry are correct?

**Worked correction.** Expect `stall`. Record that bytes or identity changed without accepted checklist improvement. Preserve the candidate if it has explanatory value, but do not consume it as evidence of progress. A bounded continuation may still inspect the stall; its budget is governed by CYB-021.

[Offline solution and executable controls](../../../../../scripts/course-exercises/cyb_governed_loops.py): record `external_progress`.

## Two-Stage Assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Conceptual stage, four points: correctly classify the four-state trace, explain a moved target, reject hash-only progress, and identify stale validation. Require all four, with written reasons. Behavioral stage, four points: run the exact fixture, produce an equal-residual counterexample, produce a stale-validator counterexample, and preserve expected versus actual results. Require both rejected cases and the positive zero-residual completion. The course provides an assessment; it does not assert a learner's belief or behavior changed.

## Key Takeaways

- Keep the target fixed and bind each measurement to a revision.
- A changed artifact with unchanged residual is a stall in this model.
- Completion applies only to the checklist actually evaluated.

## Journal, Proof, and Synthesis

Record target version, baseline revision, candidate identity, measured revision, checker version, residual, classification, and continuation decision. Include rejected evidence rather than silently dropping it. Synthesize the strongest claim: this checked revision improved the stated checklist, under the stated rule. Do not generalize it to usefulness, perceptual quality, deployment, or every possible defect. If the checker is corrected, rerun the affected trace and revise this lesson's worked correction.

## Further Reading and Overlap Boundary

CS-002 introduces an external progress test; this lesson exposes its hash-only simplification through measurement counterexamples. CYB-005 concerns signals and setpoints; CYB-022 adds artifact-to-validator binding. CYB-023 will add an ordered receipt chain. [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) offers general context for documenting evaluation limits. Our checklist and classifications are authored teaching definitions, not findings measured across a fleet. Translation and independent review remain pending.
