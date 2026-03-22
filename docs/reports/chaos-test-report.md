# Chaos Engineering Test Report

**Date:** 2026-03-22
**Purpose:** Verify Demerzel's governance detection mechanisms catch deliberately injected LOLLI poison.
**Artifacts tested:** `pipelines/chaos-test.ixql`, `policies/chaos-test-policy.yaml`, `schemas/chaos-test.schema.json`

## Injection Summary

11 deliberate LOLLI injections across 5 detection levels + policy/schema layer.

## Detection Results

| # | Poison | Level | Detection Mechanism | Expected Result | Actually Detected? |
|---|--------|-------|--------------------|-----------------|--------------------|
| 1 | `ghost_data` dead binding | L2 | `analyzeLolli()` in Parser.fs:415 | Flag as dead | YES — parser walks bindings vs references; `ghost_data` is bound but never in `references` set. Confidence 0.95, severity "error". |
| 2 | `phantom_state` dead binding | L2 | `analyzeLolli()` in Parser.fs:415 | Flag as dead | YES — same mechanism as #1. Binding name collected but never referenced downstream. |
| 3 | `vapor_config` dead binding | L2 | `analyzeLolli()` in Parser.fs:415 | Flag as dead | YES — same mechanism as #1. Pure dead binding, no side effects. |
| 4 | Orphaned `fan_out` branch | L3 | `lolli-lint.ixql` Level 3 branch check | Flag as orphaned | PARTIAL — `analyzeLolli()` returns `OrphanedBranches = []` (hardcoded empty list at Parser.fs:427). The lolli-lint.ixql *specifies* L3 detection but the F# parser does NOT implement branch-level analysis yet. **GAP — needs fix: implement orphaned branch detection in `analyzeLolli()`.** |
| 5 | `useless_metric` dead computation | L4 | Transitive closure analysis | Flag as dead | PARTIAL — `analyzeLolli()` catches `useless_metric` as a dead binding (L2). But the L4 transitive backward-trace from outputs is specified in lolli-lint.ixql only, not implemented in the F# parser. The L2 detection catches this incidentally. **GAP — L4 analysis not implemented in parser.** |
| 6 | Write to unconsumed path `state/oversight/chaos-test-output-*` | L1 | `cross-pipeline-deps.ixql` orphaned output scan | Flag as orphaned output | YES (specification-level) — `cross-pipeline-deps.ixql` Step 4 builds writer-reader edges and flags writes with no matching read. No other pipeline reads `state/oversight/chaos-test-output-*`. However, this is a pipeline-level specification, not implemented in the F# parser. **Detection works at spec level; runtime scanner not yet built.** |
| 7 | `chaos-test.ixql` has no consumer | L0 | `cross-pipeline-deps.ixql` file-level consumer check | Flag whole file | YES (specification-level) — `cross-pipeline-deps.ixql` Step 5 identifies isolated pipelines with no inbound edges. `chaos-test.ixql` has no trigger from any other pipeline. Same caveat: spec exists, runtime scanner pending. |
| 8 | Policy with BS description | Policy | BS decoder (4 tests) | Score 3-4/4 BS | YES — see BS analysis below. Score: 4/4 BS signals. |
| 9 | Policy with no consumer/registration | Policy | `anti-lolli-inflation-policy.yaml` artifact_registration rule | Flag for deprecation | YES — anti-lolli-inflation-policy.yaml lines 98-109 require every new artifact to declare `consumer`, `timeline`, and `justification` in registration front-matter. `chaos-test-policy.yaml` has none. Violation is clear and enforceable. |
| 10 | Schema nobody references | Schema | `staleness-detection-policy.yaml` 14-day zero-citation check | Flag at 14 days | DELAYED — staleness-detection-policy lines 120-137 flag artifacts with 0 citations after 14 days. `chaos-test.schema.json` would be flagged on day 14, not immediately. **GAP — no immediate detection of unreferenced schemas; detection is time-delayed.** |
| 11 | `teach chaos_patterns to seldon` — non-existent curriculum | L4 | Cross-reference check | Flag dead teach | GAP — no mechanism currently validates that `teach X to seldon` targets an existing curriculum. Neither the F# parser nor any policy checks teach target validity. **GAP — needs cross-reference validation for teach directives.** |

## BS Decoder Analysis: `chaos-test-policy.yaml`

**Input:** "Leveraging synergistic governance paradigms for holistic alignment optimization"

### Test 1 — Specificity
- Score: 0.05 (extremely low)
- Analysis: No concrete nouns, no specific system, no measurable target. "Governance paradigms" could mean anything. "Holistic alignment optimization" is a three-word chain where each word dilutes the prior.
- Result: **BS signal**

### Test 2 — Falsifiability
- Score: 0.0
- Analysis: No claim in this sentence can be tested, measured, or disproven. What would "not leveraging synergistic governance paradigms" look like? There is no conceivable evidence that would falsify this.
- Result: **BS signal**

### Test 3 — Commitment
- Score: 0.0
- Analysis: No who, no what (concrete), no when. "Leveraging" is a gerund — ongoing, unbound, uncommitted. No deliverable, no deadline, no responsible party.
- Result: **BS signal**

### Test 4 — Content Density
- Score: 0.1
- Analysis: 8 words, of which "leveraging", "synergistic", "holistic", and "optimization" are filler/buzzwords. Only "governance" and "alignment" carry partial semantic weight, but without context they are empty containers.
- Result: **BS signal**

**Aggregate BS score:** 4/4 — Pure BS. Would map to tetravalent **F** (False — the description fails to describe anything).

### Additional Policy LOLLI Signals

| Signal | Detection | Status |
|--------|-----------|--------|
| Empty `constitutional_basis: []` | Convention check — every policy must cite articles | Detectable by schema validation if `minItems: 1` enforced |
| Empty `principles: []` | Convention check | Same — schema validation |
| `schema_ref` pointing to non-existent file | File existence check | GAP — no automated cross-reference validation for `schema_ref` fields |
| Rules with no constitutional article reference | Convention check | GAP — `placeholder-rule` cites no article; no automated enforcement |

## Gap Summary

| Gap ID | Description | Severity | Recommended Fix |
|--------|------------|----------|-----------------|
| G1 | `analyzeLolli()` returns empty `OrphanedBranches` — L3 not implemented | High | Implement fan_out branch analysis in Parser.fs |
| G2 | L4 transitive closure (backward trace from outputs) not in parser | Medium | Add reachability analysis to `analyzeLolli()` |
| G3 | Cross-pipeline dependency scanner exists as spec only, not runtime | Medium | Implement as F# analysis pass or IxQL tooling |
| G4 | Schema staleness is time-delayed (14 days), no immediate orphan check | Low | Add immediate reference-count check at creation time |
| G5 | `teach X to seldon` targets not validated against curriculum | Medium | Add cross-reference check for teach directives |
| G6 | `schema_ref` field not validated for file existence | Low | Add schema cross-reference validation |
| G7 | Policy rules not checked for constitutional article references | Low | Extend persona/policy schema to require `constitutional_basis` per rule |

## Scorecard

- **Injections:** 11
- **Detected (full):** 5 (ghost_data, phantom_state, vapor_config, BS description, no-registration policy)
- **Detected (partial/spec-only):** 4 (orphaned branch via L2, useless_metric via L2, unconsumed write via spec, no-consumer file via spec)
- **Delayed detection:** 1 (schema staleness at 14 days)
- **Undetected:** 1 (teach to non-existent curriculum)
- **Detection rate:** 45% full, 82% partial-or-better
- **Poison Resilience Score:** 5/11 = 0.45 (immediate), 9/11 = 0.82 (including spec-level)

## Conclusion

Demerzel's governance immune system has strong L2 (dead binding) detection via the F# parser and strong policy-level detection via anti-lolli-inflation and BS decoder. However, L3 (branch), L4 (transitive), and cross-artifact reference validation have specification-level coverage only — the detection logic is designed in IxQL pipelines but not yet implemented as executable analysis. The chaos test exposed 7 gaps that should be addressed to achieve full automated detection.
