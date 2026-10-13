---
module_id: cs-007-typed-agent-evidence-and-backpressure
department: computer-science
course: Type Agent Evidence Before Composing Verdicts
level: intermediate
prerequisites: ["cs-005-agent-handoff-evidence-contract", "cs-006-ixql-pipeline-composition"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-11-007
version: "0.1.0"
---

# Type Agent Evidence Before Composing Verdicts

> **Department of Computer Science** | Intermediate | 40 minutes | English draft; subject and learner review pending

## Objectives and project question

You will distinguish a schema-valid record from evidence that supports its conclusion, carry a failure across an agent boundary without turning it into success, and evaluate a proposed rule for delaying downstream work when required evidence is missing. **Project question:** before a Demerzel QA agent writes or forwards a verdict, what must its upstream nodes deliver so the next agent can tell a real check from a placeholder? This lesson uses one pinned Phase 0 pipeline. Its typed envelope and semantic backpressure rule are *teaching proposals*, not features verified in the IXQL executor.

## 1. Inspect the declaration and the contract

At [Demerzel commit `c3bf622`](https://github.com/GuitarAlchemist/Demerzel/tree/c3bf6224386374fc0f74cfb36643e543b4bdcce2), [`pipelines/qa-architect-cycle.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/pipelines/qa-architect-cycle.ixql#L1-L15) calls itself a **Phase 0 skeleton**. Its comments explicitly exclude the real blast-radius analyzer, reviewer tribunal, PR comment or follow-up issue, and derived algedonic signal. It reads a trigger path with a fallback target, supplies an empty blast radius, and uses a one-entry reviewer chain whose note says there is no tribunal aggregation ([lines 23–55](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/pipelines/qa-architect-cycle.ixql#L23-L55)). The assembled verdict says `risk_tier: "P3"`, `verdict: "informational"`, and contains `evidence: [{kind: "manual_note", name: "phase0.skeleton", outcome: "n/a", ...}]` ([lines 66–90](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/pipelines/qa-architect-cycle.ixql#L66-L90)). These are source declarations. The lesson has no receipt showing the pipeline ran or wrote a file.

The vendored [QA verdict JSON Schema](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json#L14-L30) requires `target`, `risk_tier`, `verdict`, `blast_radius`, `evidence`, `reviewer_chain`, and other fields. Its conditional rule requires `P3` for an `informational` verdict ([lines 147–162](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json#L147-L162)); `reviewer_chain` needs at least one entry ([lines 96–102](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json#L96-L102)). An evidence item may be a `manual_note` with outcome `n/a` ([lines 260–297](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json#L260-L297)). Thus the schema permits the skeleton's *shape*; it does not claim that the note proves a real regression check or that the one reviewer entry represents a completed tribunal. `schema_version: 1` is a single field, not the whole schema.

### Practice exercise 1

The source declares `informational/P3`, one architecture reviewer with `score: null`, and one `manual_note/n/a`. Which of these statements can a schema check support: (a) the verdict has an allowed category pairing, (b) a regression test passed, (c) a multi-reviewer tribunal ran? Explain.

> **Answer:** Only (a) follows from the cited conditional schema rule, provided the whole object passes validation. The schema allows `manual_note/n/a` and a one-entry reviewer chain, so neither a passing test nor a tribunal follows from shape. The pipeline explicitly labels both the blast-radius result and reviewer chain as Phase 0 placeholders. Even (a) is a source-level expectation until a validator actually checks an emitted object.

## 2. Put a type at every agent boundary

For design discussion, give a node a result type such as `Result<Output, Error>` and make its output carry evidence. The following **proposed** notation is not IXQL syntax or a statement about its runtime:

```text
TriggerRead = Ok { target, source_path, source_revision }
            | Err { code, source_path, observed_at }
BlastCheck  = Ok { target_revision, result, evidence_receipt }
            | Err { code, target_revision, attempted_check }
VerdictDraft = { target, category, evidence_items, reviewer_receipts, provenance }
```

The producer owns the claim about what it attempted. The receiver checks that the target revision in the result matches the target revision it intends to judge. A receipt should identify the check, input revision, outcome, and location of an inspectable artifact. A schema value such as `kind: "test_run"` is a label; the JSON Schema does not authenticate a test log. If a node has no result, use `Err` or `Unknown` with a reason rather than fabricate `Ok {result: []}`. An empty successful result means “the check ran and found no items”; an unavailable check means “we do not know.”

`VerdictDraft` is an internal teaching type, not the QA verdict wire format. It omits required schema fields and uses different field names. A proposed composer must map and complete it into a `QaVerdict` with all required wire fields before applying the pinned JSON Schema; copying the draft directly into a validator would fail.

The pinned pipeline has `trigger_context <- ix.io.read(...) → default({...})`. The grammar and this source do not specify whether `default` applies only to a missing file, to malformed JSON, or to every read failure. A safer **proposed contract** would distinguish `Missing` from `Malformed` and `PermissionDenied`: only an explicitly authorized synthetic sweep could turn `Missing` into a documented fallback; the others would stop or seek repair. This is a design decision to test, not a description of observed IXQL behavior. A fallback also needs a provenance flag so a downstream node never mistakes its synthetic target for an actual PR trigger.

### Practice exercise 2

A proposed trigger node returns `Err {code: "PermissionDenied", source_path: "state/qa-architect/trigger.json"}`. A colleague replaces it with the fallback target and labels that target “read from trigger file.” What two errors have they made, and what output should the next node receive under the proposed contract?

> **Answer:** They turned a permission failure into a success and misattributed a synthetic target to a file that was not read. Under the proposed contract the next node receives `Err(PermissionDenied)` with the attempted path and no trusted trigger target; the QA computation stops or requests a permission repair. The checked-in IXQL line alone does not establish that its actual `default` behaves this way.

## 3. Propagate failure before an irreversible effect

The Phase 0 source declares `ix.io.write(verdict_path, verdict) → tars.validate(check: "verdict.schema_version == 1", ...)` ([lines 93–102](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/pipelines/qa-architect-cycle.ixql#L93-L102)). In the written order, the write precedes a check of one field. The rejection message says it refuses to persist a schema mismatch, but the displayed check cannot establish full JSON Schema validity, and the source gives no rollback receipt. We cannot infer that an invalid file was actually persisted, because this lesson did not execute the pipeline. We *can* say the declaration alone is insufficient to prove a before-write gate.

A proposed composition would first map `VerdictDraft` into a complete schema-shaped `QaVerdict`, validate that wire object against the pinned schema, verify the evidence receipt required for the intended claim, authorize the write, and finally inspect the write result. Each step returns `Ok` or `Err`. The evidence policy is separate from JSON Schema validation: a Phase 0 informational placeholder may be valid and useful, but it must stay labeled as such. A failure in mapping, validation, or evidence review yields no authorized write in this proposed design. A failed write yields an error receipt, not an accepted verdict. The design must be implemented and tested before anyone can say the pipeline enforces it.

### Practice exercise 3

Take a **synthetic wire-format verdict** identical to the Phase 0 verdict except `schema_version: 2`. If the source's `tars.validate` rejects that version, can its rejection prove that no write occurred? Give the expected result of the proposed validate-before-write design.

> **Answer:** No. The source places `ix.io.write` before the `schema_version` check, and there is no observed rollback, so a later rejection cannot by itself establish absence of a write. In the proposed design, after mapping to the complete wire object, full schema validation rejects `schema_version: 2` because the schema requires the integer constant `1`; the result is `Err(SchemaMismatch)`, and the write stage is not invoked. A test would need a call trace and file-state check to verify that behavior in an implementation.

### Practice exercise 4

A real reviewer call times out, but a composer inserts the Phase 0 `reviewer_chain` entry and reports “tribunal complete.” The JSON still has one reviewer, satisfying `minItems: 1`. What should the typed result be, and which check distinguishes this from a valid informational skeleton?

> **Answer:** The reviewer stage should return `Err(Timeout)` or an explicit unresolved result with the attempted role and target revision. The composer must not upgrade the placeholder to a completed tribunal. A claim-specific evidence check asks for receipts from the required reviewer roles and their outcomes; the schema's `minItems: 1` only checks array shape. An informational Phase 0 skeleton can remain clearly labeled as a skeleton, whereas a tribunal-complete claim needs separate runtime evidence.

## 4. Semantic backpressure is a hypothesis

**Backpressure** ordinarily slows a producer when a downstream consumer lacks capacity. A proposed *semantic* version would slow a verdict producer when the consumer cannot interpret or verify its evidence. The idea is falsifiable: require typed source identity, a completed check receipt, and a reviewer receipt before placing an item in a “ready for operational decision” queue. Otherwise retain it in an unresolved queue with a reason. This three-part rule is a **synthetic teaching policy**, not a Demerzel rule or an IXQL feature. It does not replace existing authority, review, or merge policy. The fixture below concerns commit-bound decisions; a scheduled sweep with `sha: null` would need a different stable target identity, such as a named snapshot revision, rather than an invented commit SHA.

Consider a fixed fixture with two available downstream slots and three candidate bundles. `A` has `sha: null`, `manual_note/n/a`, and the skeleton architecture entry. `B` has a pinned target SHA, a verifiable `test_run/pass` receipt, and a reviewer receipt for that same SHA. `C` has a pinned SHA and test receipt, but its reviewer call timed out. Under the proposed three-part rule, only `B` enters the ready queue. `A` and `C` remain unresolved, and one slot stays unused. The unused slot is deliberate: capacity alone is not evidence. `B` is ready only for the *specific operational decision defined by the policy*; the fixture does not authorize a merge or claim that a real GA test passed.

The hypothesis predicts fewer unsupported “ready” classifications and perhaps longer waiting time. Test it on labeled historical handoffs or in a controlled simulation: count false-ready decisions, unresolved age, and manual corrections with and without the rule. A good result would reduce false-ready decisions without unacceptable starvation. A falsifier would be unchanged or worse false-ready classification, or unresolved work that never receives a repair path. This lesson has not collected such measurements.

### Practice exercise 5

Apply the proposed rule to `A`, `B`, and `C`. How many of the two slots are filled, how many bundles wait, and what additional event could make `C` eligible? Does the exercise demonstrate that Demerzel currently applies semantic backpressure?

> **Answer:** One slot is filled by `B`; two bundles (`A` and `C`) wait; one slot remains unused. A successful reviewer retry with a receipt tied to `C`'s pinned target SHA could complete its three requirements. The fixture only checks the proposed rule's arithmetic and classification. It supplies no evidence that Demerzel currently implements or benefits from semantic backpressure.

## Sources, limits, and next check

The project evidence is the [pinned Phase 0 IXQL file](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/pipelines/qa-architect-cycle.ixql), the [vendored verdict schema](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json), and the [minimal structural validator](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/scripts/ixql-validate.js#L1-L4). The schema's metadata names GA as its canonical source at a separate SHA ([lines 6–12](https://github.com/GuitarAlchemist/Demerzel/blob/c3bf6224386374fc0f74cfb36643e543b4bdcce2/schemas/contracts/qa-verdict.schema.json#L6-L12)). The IXQL comment names `docs/contracts/qa-verdict.schema.json`, while this checkout's vendored file is at `schemas/contracts/qa-verdict.schema.json`; that path difference is a source-documentation issue, not proof that a run failed. The structural validator is not a full parser or executor. No verdict emission, schema check on emitted bytes, write trace, reviewer call, or backpressure measurement was run for this lesson. The next check is an isolated implementation test with an invalid draft and a denied reviewer call, recording the write call trace and artifact state. Human subject review, learner review, translation, and publication remain open.
