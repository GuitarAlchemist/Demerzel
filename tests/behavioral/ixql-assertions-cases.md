# IxQL Assertions — Behavioral Test Cases

**Grammar section:** 12 (Assertions)
**EBNF:** `grammars/sci-ml-pipelines.ebnf` — Section 12
**Issue:** GuitarAlchemist/Demerzel#135
**Constitutional basis:** Articles 1 (Truthfulness), 7 (Auditability), 8 (Observability)

---

## Overview

Assertions are first-class IxQL constructs that make pipeline expectations explicit and machine-checkable. Each assertion maps to a tetravalent conclusion:

| Assertion result | Tetravalent value | Behavior |
|---|---|---|
| All checks pass | T | Pipeline continues |
| A check fails (deterministic) | F | Halt (error) or warn (warning) |
| Check is inconclusive (insufficient data) | U | Triggers investigation; pipeline pauses |
| Checks give contradictory results | C | Escalate to human |

---

## Test Case 1: Null Check on Training Data

**Name:** `null_check_training_data`
**Grammar production:** `null_check`
**Constitutional basis:** Article 1 (Truthfulness) — fabricated completeness is a harm

```ixql
assert input_quality: csv("train.csv")
  assert_check(not_null, message: "Training data must have no nulls")
```

**Expected parse result:** Valid `assertion_statement`
- `assertion_subject` = `file_source(csv, "train.csv")`
- `assertion_check.assertion_condition` = `null_check(not_null)`
- `assertion_check.assertion_message` = `"Training data must have no nulls"`

**Runtime behavior:**
- If CSV has zero nulls: conclusion = T
- If CSV has any nulls: conclusion = F, pipeline halts with message
- If CSV is empty or unreadable: conclusion = U, investigation triggered

---

## Test Case 2: Metric Threshold on F1 Score

**Name:** `metric_threshold_f1`
**Grammar production:** `metric_check`
**Constitutional basis:** Article 8 (Observability) — metrics must be visible and thresholded

```ixql
assert model_quality: random_forest → f1_score
  assert_check(metric f1_score >= 0.85, message: "F1 must reach 0.85 before deployment")
```

**Expected parse result:** Valid `assertion_statement`
- `assertion_subject` = pipeline `random_forest → f1_score`
- `assertion_check.assertion_condition` = `metric_check(f1_score, >=, 0.85)`

**Runtime behavior:**
- `f1_score >= 0.85`: conclusion = T
- `f1_score < 0.85`: conclusion = F, deployment blocked
- Evaluation fails to run (data error): conclusion = U

---

## Test Case 3: Tetravalent Truth Check

**Name:** `truth_check_confidence`
**Grammar production:** `truth_check`
**Constitutional basis:** Article 6 (Escalation) — low-confidence conclusions must escalate

```ixql
assert confidence_gate: csv("test.csv") → random_forest → f1_score
  assert_check(truth >= 0.9, message: "Need T >= 0.9 confidence before production deploy")
```

**Expected parse result:** Valid `assertion_statement`
- `assertion_condition` = `truth_check(>=, 0.9)`

**Runtime behavior:**
- Conclusion truth value T with confidence >= 0.9: passes
- Conclusion T with confidence 0.7-0.9: F (insufficient confidence)
- Conclusion U or C: escalate per Article 6

---

## Test Case 4: Schema Conformance Check

**Name:** `schema_conformance_features`
**Grammar production:** `schema_check`
**Constitutional basis:** Article 1 (Truthfulness) — data must conform to declared schema

```ixql
assert feature_schema: parquet("features.parquet")
  assert_check(schema: "schemas/feature-schema.json", message: "Features must match contract schema")
  assert_check(type: tabular, message: "Model expects tabular data shape")
```

**Expected parse result:** Valid `assertion_statement` with two checks
- Check 1: `schema_check("schemas/feature-schema.json")`
- Check 2: `type_check(tabular)`

**Runtime behavior:**
- Both checks pass: T
- Schema mismatch: F, deployment blocked
- Type mismatch (e.g. image data received): F

---

## Test Case 5: Governance Compliance Assertion

**Name:** `governance_compliance_deploy`
**Grammar production:** `governance_check`
**Constitutional basis:** Article 9 (Bounded Autonomy) — deployment requires governance

```ixql
assert deployment_governed: random_forest → bias_assessment → real_time_api
  assert_check(governance: bias_assessment, message: "Bias assessment required for production")
  assert_check(governed standard, message: "Minimum standard governance required")
```

**Expected parse result:** Valid `assertion_statement`
- Check 1: `governance_check(bias_assessment)`
- Check 2: `governance_check(governed standard)`

**Runtime behavior:**
- `bias_assessment` gate runs and passes, governance level >= standard: T
- Gate missing from pipeline: F at parse time (static analysis)
- Gate present but fails at runtime: F, halt and log

---

## Test Case 6: Assertion with Error Severity and Binding

**Name:** `assertion_severity_binding`
**Grammar production:** `assertion_full`, `conclusion_binding`
**Constitutional basis:** Article 7 (Auditability) — named results are logged

```ixql
quality_verdict <- assert error model_performance: csv("holdout.csv") → random_forest → f1_score
  assert_check(metric f1_score >= 0.80, message: "Minimum performance threshold")
  assert_check(not_null, message: "Holdout data must be complete")
```

**Expected parse result:** Valid `assertion_result`
- `conclusion_binding` = `quality_verdict`
- `assertion_severity` = `error`
- Bound result: tetravalent value (T/F/U/C)

**Runtime behavior:**
- All checks pass: `quality_verdict = T`, continues
- Any check fails: `quality_verdict = F`, pipeline halts (severity = error)
- Bound result written to governance audit log

---

## Test Case 7: Custom Predicate Assertion

**Name:** `custom_predicate_domain`
**Grammar production:** `custom_predicate`
**Constitutional basis:** Article 9 (Bounded Autonomy) — extensible governance hooks

```ixql
assert domain_validity: csv("guitar_data.csv")
  assert_check(is_guitar_frequency_range(min_hz: 80, max_hz: 6000), message: "Data must be in guitar frequency range")
  assert_check(no_clipping, message: "Audio data must not be clipped")
```

**Expected parse result:** Valid `assertion_statement`
- Check 1: `custom_predicate(is_guitar_frequency_range, [min_hz: 80, max_hz: 6000])`
- Check 2: `custom_predicate(no_clipping)`

**Runtime behavior:**
- Custom predicates are resolved at runtime against registered predicate library
- If predicate not found: conclusion = U (unknown — triggers investigation)
- Predicate returns true: T; false: F

---

## Test Case 8: Assertion on Governance State Source

**Name:** `assertion_governance_state`
**Grammar production:** `assertion_subject` using `governance_state_source`
**Constitutional basis:** Article 3 (Reversibility) — governance state must be rollback-ready

```ixql
assert governance_health: governance_state
  assert_check(schema: "schemas/belief-state.schema.json", message: "Belief state must conform to schema")
  assert_check(not_null, message: "Governance state must not be empty")
  assert_check(truth >= 0.7, message: "Governance state must have sufficient confidence")
```

**Expected parse result:** Valid `assertion_statement`
- `assertion_subject` = `governance_state_source`
- Three chained checks: schema, null, truth threshold

**Runtime behavior:**
- Reads `state/` directory from Demerzel repo
- Schema validation via `belief-state.schema.json`
- If state files are missing: U (insufficient evidence)
- If state is inconsistent (contradictory beliefs): C, escalate

---

## Grammar Coverage Summary

| Production | Test Cases |
|---|---|
| `null_check` | TC1, TC6, TC8 |
| `metric_check` | TC2, TC6 |
| `truth_check` | TC3, TC8 |
| `schema_check` | TC4, TC8 |
| `type_check` | TC4 |
| `governance_check` | TC5 |
| `assertion_severity` | TC6 |
| `conclusion_binding` | TC6 |
| `custom_predicate` | TC7 |
| `governance_state_source` as subject | TC8 |
| pipeline_expr as subject | TC2, TC3, TC5, TC6 |
| file_source as subject | TC1, TC4 |

---

## Integration with Tetravalent Logic

All assertion results integrate with the tetravalent framework:

```
assert_check passes     → T (feeds into pipeline logic gates)
assert_check fails      → F (triggers halt or warn per severity)
assert_check unresolved → U (triggers investigation cycle)
assert_check contradicts → C (escalates to human per Article 6)
```

Assertion results can be bound (TC6) and used as MCP orchestration guards:

```ixql
quality <- assert error model_quality: csv("test.csv") → random_forest → f1_score
  assert_check(metric f1_score >= 0.85)

-- Use assertion result as a tetravalent gate
when quality T >= 0.9: real_time_api(model)
```
