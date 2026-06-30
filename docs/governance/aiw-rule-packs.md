# Demerzel AIW Rule Packs (Advisory Policy Engine)

This document catalogs the rule packs used by the Demerzel Policy Engine to make **advisory** decisions for AI/human delivery, as defined in Epic #589.

> **Important:** The rule evaluation engine is strictly an **advisory and dry-run** component.
> - It does **not** mutate GitHub state directly.
> - It does **not** replace or encode final human judgment.
> - It is **not** a production runtime.
> - It does **not** bypass review or merge gates.

## Rule Pack Catalog

The following rule packs are defined for the AI Worker (AIW) Policy Engine:

1. **Grooming Readiness:** Evaluates if an issue or task has sufficient detail and is ready for the Pocock lane shaping.
2. **Capability Stream Routing:** Determines the required capabilities and routes to the appropriate capability streams.
3. **Worker Lane Selection:** Advises on which execution lane (e.g., shape, explore, verify, loop) best fits the task based on scope and constraints.
4. **Composite Lane Fallback:** Provides fallback recommendations when a primary lane is blocked or incapable.
5. **Fan-out Eligibility:** Determines if a complex task can be safely fanned out into smaller, independent sub-tasks.
6. **Fan-in Queue Ordering:** Defines the priority and sequencing for aggregating parallel task results and reviewing them.
7. **Adaptive Backpressure Mode:** Evaluates system capacity and recommends throttling, draining, or normal fan-out modes to prevent fan-in overload.
8. **Stale Delegation Markers:** Identifies stalled or abandoned delegated tasks that require human intervention or reassignment.
9. **Risk Tier Classification:** Assesses the risk of a change (e.g., modifying Asimov laws, changing build config) to assign appropriate gates.
10. **Review Requirement Selection:** Advises on the necessary review rigor (adversarial, security, architectural) based on the risk tier.
11. **Merge Readiness:** Evaluates whether all constraints, tests, and human-in-the-loop approvals are satisfied for a PR.
12. **Policy Exception Handling:** Defines advisory overrides when conflicting policies arise, delegating the final verdict to human authority.

## Rule Output Contract

Every rule evaluation must emit an `advisory-decision` adhering to `schemas/advisory-decision.schema.json`.

Example output:
```yaml
rule_result:
  rule_id: "GRM-001"
  subject: "issue"
  decision: "warn"
  reason_codes: ["MISSING_ACCEPTANCE_CRITERIA"]
  evidence_refs: ["issue#123_body"]
  next_actions: ["request_clarification"]
  confidence: "high"
```

## Reason-code Taxonomy

The taxonomy uses a dot-delimited format `CATEGORY.SUBCATEGORY.SPECIFIC_REASON`.

- `SCOPE.TOO_BROAD` / `SCOPE.UNDEFINED`
- `CAPABILITY.MISMATCH` / `CAPABILITY.UNAVAILABLE`
- `RISK.HIGH_RISK_PATH` / `RISK.GOVERNANCE_MUTATION`
- `REVIEW.MISSING_APPROVAL` / `REVIEW.EVIDENCE_LACKING`
- `STATE.STALE` / `STATE.BLOCKED`
- `SYSTEM.BACKPRESSURE_HIGH` / `SYSTEM.CAPACITY_EXCEEDED`

## Rule Versioning Strategy

Rule packs are versioned using SemVer.
- Major versions denote changes in the output contract or fundamentally new policy constraints.
- Minor versions denote new rules within a pack or modified logic that does not break the contract.
- Patch versions cover bug fixes in rule logic.
Rules are updated as `state/evolution` markers and synced against `governance-manifest.json`.

## Relationship to Other Initiatives

- **#588 Policy Engine:** The rule packs defined here provide the logical ruleset for the Policy Engine (#588) to evaluate.
- **#568 / #570 / #579 / #584 / #586:** These related issues establish the context and metrics (like token economics, capacity, and backpressure) that rules evaluate (e.g., Adaptive Backpressure relies on capacity telemetry, Risk Tier relies on governance definitions).
