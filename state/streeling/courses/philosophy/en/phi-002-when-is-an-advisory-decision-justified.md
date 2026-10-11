---
module_id: phi-002-when-is-an-advisory-decision-justified
department: philosophy
course: "Philosophy: Evidence and Authority in Advisory Decisions"
level: intermediate
alchemical_stage: albedo
prerequisites: [phi-001-how-to-argue-well]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: philosophy-2026-10-11-002
version: "0.1.0"
---

# When Is an Advisory Decision Justified?

> **Department of Philosophy** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to distinguish schema conformance from justified advice, identify contract vocabulary drift, state who retains merge authority, and design a falsifiable evidence check.

## Project question and evidence boundary

**When may Demerzel recommend that a Guitar Alchemist (GA) pull request is ready for human merge?** Demerzel's [advisory decision document](https://github.com/GuitarAlchemist/Demerzel/blob/9ba9a29f6424ac8c1a6654c9b979b282a8cf216f/docs/architecture/demerzel-advisory-decisions.md) says that recommendations should cite specific Streeling event IDs or Seldon fact IDs, state reasons, and leave high-risk action such as merging to a human. Its [`advisory-decision` schema](https://github.com/GuitarAlchemist/Demerzel/blob/9ba9a29f6424ac8c1a6654c9b979b282a8cf216f/schemas/advisory-decision.schema.json) defines a structured, dry-run rule result. The [AIW rule-pack document](https://github.com/GuitarAlchemist/Demerzel/blob/9ba9a29f6424ac8c1a6654c9b979b282a8cf216f/docs/governance/aiw-rule-packs.md) explicitly calls the rule evaluation engine advisory, not a production runtime or replacement for human judgment. All three links pin Demerzel commit `9ba9a29f6424ac8c1a6654c9b979b282a8cf216f`.

This is a philosophical question with an operational answer. A decision can have a valid *form* while its reasons lack relevant evidence. Advice does not grant authority to act. [PHI-001](phi-001-how-to-argue-well.md) introduced premises, conclusions, and soundness; here we examine the steps between a serialized statement, supporting evidence, and an authorized decision maker. We test a **synthetic** example, not a live policy engine or GA PR.

## 1. A record can conform while its claim is unsupported

The schema requires a top-level `rule_result` object. Inside it, `rule_id`, `subject`, `decision`, `reason_codes`, `evidence_refs`, `next_actions`, and `confidence` are required. The `subject` may be `pull_request`, and `decision` may be `recommend`. However, the `evidence_refs` property is only an array of strings: the schema sets no minimum item count, no requirement for a Streeling or Seldon identifier, and no rule linking a reference to the named PR. Requiring a field does not require that the field contain useful evidence.

Consider this **synthetic teaching fixture**. `PR-EXAMPLE` is a placeholder, not an observed pull request; the rule ID and action are invented solely to probe the schema.

```json
{
  "rule_result": {
    "rule_id": "SYNTHETIC-PR-READINESS",
    "subject": "pull_request",
    "decision": "recommend",
    "reason_codes": [],
    "evidence_refs": [],
    "next_actions": ["ask a human to inspect PR-EXAMPLE"],
    "confidence": "high"
  }
}
```

This object passes the pinned JSON Schema: the required keys exist, each value has an allowed type, and `recommend` and `high` belong to their respective enums. That is a narrow, reproducible result about *shape*. No source supports a claim that PR-EXAMPLE passed CI, review, or policy gates. The advisory document's stated evidence principle is not satisfied by an empty list. Nor does the schema validate whether a nonempty string names a genuine event. Calling the fixture “high confidence” adds a label, not proof.

### Exercise 1 — Separate the three tests

Does the synthetic fixture (a) conform to the schema, (b) satisfy the advisory document's specific-evidence principle, and (c) authorize a GA merge? Cite the fields or sentences that decide each answer.

> **Answer:** (a) Yes. It has all required `rule_result` keys, with allowed `pull_request`, `recommend`, and `high` values; the schema permits empty arrays. (b) No. `evidence_refs: []` contains no specific Streeling event or Seldon fact ID. (c) No. The document reserves merging for human approval, and the rule-pack document calls this engine advisory and dry-run. A valid object is neither a supported readiness conclusion nor merge authority.

## 2. Evidence needs identity, relevance, and a date

Suppose a future record lists `"ci-run-123"` in `evidence_refs`. Can a reviewer retrieve that run, match it to the exact PR revision, and check its final result? A green check on an older commit might be genuine yet irrelevant to the current head.

For a merge recommendation, the advisory document says all governance gates, including CI, review, and policy, must have passed. The cited schema does not contain dedicated fields for a PR number, head SHA, CI state, review approval, or policy outcome. A producer could put explanatory strings in `reason_codes` or `evidence_refs`, but this shape alone cannot demonstrate that the required gates were checked. A human would need dated, target-matched records and a documented mapping from each gate to its evidence. The decision might then be well supported; it would still be a recommendation.

“All checks passed” is an empirical claim about a revision and time. “Ready to merge” also applies a policy standard. “Merge it” asks an authorized actor to act. If one check is missing, record an unresolved gate or request review. The [rule-pack catalog](https://github.com/GuitarAlchemist/Demerzel/blob/9ba9a29f6424ac8c1a6654c9b979b282a8cf216f/docs/governance/aiw-rule-packs.md) names Merge Readiness, but does not show that any particular PR was evaluated.

### Exercise 2 — Audit a proposed citation

A **synthetic** advisory points to `ci-run-123` and says “GA PR-EXAMPLE is ready.” List three facts the reviewer must check before treating that reference as evidence for the CI part of the claim. Does a passing CI run alone establish the full readiness claim?

> **Answer:** Retrieve `ci-run-123` and verify it exists; confirm its repository, PR/head SHA, and time match the revision being judged; confirm the run completed with the required checks passing. Passing CI alone does not establish review and policy gates, which the advisory document also includes in merge readiness. The fixture provides no real CI result.

## 3. A documented contract can drift across artifacts

The pinned artifacts use different vocabularies. The advisory document lists `route`, `hold`, `request_review`, `escalate`, `recommend_merge`, and `no_action` as decision types. The schema's `decision` enum is `allow`, `block`, `warn`, `escalate`, and `recommend`. Consequently, the document's literal `recommend_merge` value fails schema validation, while schema-valid `recommend` does not by itself specify a merge recommendation. Do not silently treat the two terms as identical.

The document calls for a numeric confidence score from 0 to 1 and speaks of a `reasons` field. The schema instead requires a categorical `confidence` string (`low`, `medium`, or `high`) and `reason_codes`. A numeric `0.9` or a lone `reasons` key is not the object the schema describes. The rule-pack document's example uses the schema vocabulary. These observations establish *documented contract drift at this revision*. They do not establish which artifact a running service follows, whether a migration exists elsewhere, or that any production decision was malformed.

The prose rule, machine-readable schema, and particular decision are separate objects. Where they disagree, preserve that question for the contract owners; an invented translation prevents reproducible review.

### Exercise 3 — Identify exact drift

Which of the following literal fields or values belong to the pinned schema: `decision: "recommend_merge"`, `decision: "recommend"`, `confidence: 0.9`, `confidence: "high"`, `reasons`, and `reason_codes`? What conclusion may you draw from the mismatch?

> **Answer:** The schema accepts `decision: "recommend"`, `confidence: "high"`, and the required `reason_codes` field. It rejects the literal `recommend_merge` enum value and numeric confidence, and `reasons` alone cannot replace the required `reason_codes`. The documents disagree in vocabulary at the pinned revision. This establishes a contract-reading issue, not observed live-engine behavior or permission to equate their terms.

## 4. Advice and authority are separate

Use a second **synthetic scenario**: PR-EXAMPLE changes a GA component; the reviewer has a CI run for an earlier head SHA, has no review approval for the current head, and has not found a policy result. It would be unjustified to present this PR as ready. The advisory document explicitly lists a hold for CI failures or missing evidence and a request for review. The schema can represent a warning or escalation, while `next_actions` can describe the needed human steps. Choosing the exact rule code would depend on a defined rule pack, which this lesson has not executed. The point is to record the gap rather than infer success from silence.

Authority adds a separate boundary. The advisory document's disallowed MVP actions include auto-merge, direct code push, branch protection changes, and worker permission grants. The rule-pack document likewise says the evaluation engine does not mutate GitHub state directly and does not bypass review or merge gates. The schema's description calls the decision dry-run and advisory. Thus even a fully evidenced readiness recommendation would be a reason for an authorized human to inspect and decide, not an instruction that grants the engine merge rights.

Evidence review addresses mistaken readiness claims; an explicit decision owner prevents an advisory from becoming an unauthorized merge. Product copy should preserve that distinction: “Recommended for human review” does not mean “approved for merge.”

### Exercise 4 — Choose defensible advice

For the synthetic PR-EXAMPLE scenario, write one defensible advisory sentence and name two missing records. May an advisory agent auto-merge after those records arrive?

> **Answer:** “Hold the readiness recommendation while the current head's CI result, review approval, and policy outcome are checked.” Two missing records are a completed required CI run tied to the current head SHA and a review approval for that revision; the policy result must also be established. No. The advisory document prohibits auto-merge in the MVP and keeps the final merge decision with a human.

## 5. Make the claim falsifiable

The narrow claim tested here is: **at the pinned revision, schema validation alone does not enforce the advisory document's specific-evidence requirement.** A direct counterexample is the valid empty-evidence fixture. The claim would fail if the pinned schema rejected that fixture because it required a nonempty, source-specific reference. It does not. Future revisions could strengthen the schema, while a runtime evaluator could enforce constraints beyond schema validation. Neither possibility changes the result about this pinned artifact.

A field study could test *actual* recommendation quality. Define a date window and enumerate GA PR readiness decisions. Retain each decision, target head SHA and evaluation time, cited IDs, and corresponding CI, review, and policy evidence. Count unresolved or target-mismatched references; record ambiguity separately. One unsupported recommendation would falsify a claim that *every* recommendation in that window was evidenced. No operational decisions were analyzed here.

### Exercise 5 — State a test and its limits

Write a falsifier for the lesson's narrow schema claim, then give one observation that would falsify the stronger hypothetical claim “all GA merge-readiness recommendations in a declared window have target-matched supporting evidence.” Does this lesson establish that stronger claim?

> **Answer:** The narrow claim would be false if the pinned schema rejected the complete synthetic fixture solely because `evidence_refs` was empty or lacked a specific source ID; it validates instead. One actual recommendation in the declared window with an unresolved citation or a CI result for another head SHA would refute the stronger universal claim. This lesson has no operational decision corpus and establishes nothing about the frequency of such cases.

## Limits and research basis

This lesson compares three pinned Demerzel artifacts and validates a synthetic JSON object against their schema. It does not demonstrate which document is authoritative for an implementation, that the policy engine ran, that GA PRs were evaluated, or that any human accepted a recommendation. The document and schema might reflect different design stages; their mismatch is visible, but its cause is not established here. A future course revision should check the then-current contract, trace real evidence references, and ask the contract owners how vocabulary is mapped before making operational claims. Human subject review, learner testing, localization, Learn synchronization, and public readback remain pending.
