# Behavioral Tests: LOLLI Lint Pipeline

**Pipeline:** `pipelines/lolli-lint.ixql`
**Companion:** `pipelines/cross-pipeline-deps.ixql`
**Version:** 1.0.0
**Date:** 2026-03-22

These tests verify that the LOLLI linter correctly detects dead values in IxQL pipelines
at all 5 levels, applies the correct auto-mitigation escalation tier, avoids false positives
on side-effect expressions, handles nested dead code, and computes accurate LOLLI scores.

---

## Test Suite: Dead Binding Detection (Level 2)

### TC-LLINT-01 — Pure dead binding flagged as error

**Scenario:** A pipeline defines a binding that is never referenced downstream and has no side effects.

**Input:**
```ixql
beliefs   <- ix.io.read("state/beliefs/*.belief.json")
evolution <- ix.io.read("state/evolution/*.evolution.json")
results   <- ix.io.read("state/results/*.json")
  → filter(status == "pending")
  → write("state/output/results.json", results)
```

**Expected behavior:**
- `beliefs` flagged: Level 2, kind = "dead_binding", confidence = 0.95, severity = "error"
- `evolution` flagged: Level 2, kind = "dead_binding", confidence = 0.95, severity = "error"
- `results` NOT flagged (referenced in write)
- Total dead bindings: 2 out of 3

**Pass condition:** Both dead bindings detected with correct confidence; live binding not flagged.

---

### TC-LLINT-02 — Cross-pipeline orphaned output (Level 0/1)

**Scenario:** Pipeline A writes to `state/oversight/weekly-digest.json`. No other pipeline in the
entire `pipelines/` or `examples/ixql/` directory reads from `state/oversight/weekly-digest*`.

**Input:**
```ixql
-- Pipeline A: weekly-digest.ixql
digest <- tars.summarize(scope: "weekly")
  → write("state/oversight/weekly-digest.json", digest)
```
```ixql
-- Pipeline B: ml-feedback-loop.ixql (reads state/oversight/ml-recommendations/*.json only)
ml_results <- ix.io.read("state/oversight/ml-recommendations/*.json")
```

**Expected behavior:**
- Level 0: `state/oversight/weekly-digest.json` flagged as orphaned output
- Level 1: write path has no matching read across all pipelines
- Severity: warning
- Confidence: 0.75 (might be consumed outside IxQL ecosystem)
- Report includes: pipeline name, output path, suggestion

**Pass condition:** Orphaned output detected; correct severity and confidence assigned.

---

### TC-LLINT-03 — Auto-mitigation at correct confidence tiers

**Scenario:** LOLLI lint detects 3 findings with different confidence levels.

**Input:**
```
Finding 1: dead_binding "unused_state", confidence = 0.95, no side effects
Finding 2: dead_binding "maybe_interpolated", confidence = 0.78, used in string template
Finding 3: orphaned_branch in fan_out, confidence = 0.45, dynamic dispatch possible
```

**Expected behavior:**
- Finding 1 (confidence >= 0.9): Tier 1 — action = "auto_remove"
  - Rationale includes "safe to remove"
  - Reversibility check applied (Article 3)
  - Reversibility = "git revert"
- Finding 2 (confidence >= 0.7, < 0.9): Tier 2 — action = "flag_for_review"
  - Review hint: "Check for string interpolation or external consumers"
  - No automatic removal
- Finding 3 (confidence < 0.7): Tier 3 — action = "escalate"
  - Escalation = "Article 6: human review required"
  - Explicitly does NOT auto-remove

**Pass condition:** Each finding routed to correct tier; no false auto-removals; governance gates applied.

---

### TC-LLINT-04 — False positive avoidance: side-effect bindings

**Scenario:** A binding is never referenced by name downstream, but its expression
contains a side effect (alert, write, ix.io.git).

**Input:**
```ixql
notification <- alert(discord, "Cycle complete: {{results.summary}}")
report       <- tars.synthesize(template: "governance-report")
  → write("state/reports/latest.json", report)
```

**Expected behavior:**
- `notification` classified as "dead_binding_with_side_effect"
  - Severity: "info" (not "error")
  - Confidence: 0.5 (low — side effect is the real purpose)
  - Tier 3: escalate (do NOT auto-remove)
  - Note: "Binding unreferenced but expression has side effects"
- `report` NOT flagged (referenced in write)

**Pass condition:** Side-effect binding NOT auto-removed; correctly downgraded to info severity with low confidence.

---

### TC-LLINT-05 — Nested dead code in fan_out (Level 3/4)

**Scenario:** A fan_out contains 3 branches. Branch 2 contains a nested parallel block.
One sub-branch of that parallel produces output that is never collected by any downstream binding.

**Input:**
```ixql
results <- fan_out(
    -- Branch 1: used
    data → filter(active) → tars.score(),

    -- Branch 2: nested dead code
    data → parallel(
        tars.analyze(mode: "structural"),      -- sub-branch A: used
        tars.analyze(mode: "semantic"),         -- sub-branch B: output never collected
        tars.analyze(mode: "governance")        -- sub-branch C: used
      ),

    -- Branch 3: orphaned — no side effects, output never used
    data → tars.classify(signal: "experimental")
  )
  → tars.synthesize(using: [branch_1, branch_2.sub_a, branch_2.sub_c])
```

**Expected behavior:**
- Branch 2, sub-branch B: Level 4, kind = "unreachable_expression", confidence = 0.8
  - Detected via backward trace from synthesize inputs
- Branch 3: Level 3, kind = "orphaned_branch", confidence = 0.85
  - No side effects → severity = "warning"
- Detection works at arbitrary nesting depth
- Report includes full path: `fan_out[1] → parallel[1]` for sub-branch B
- Does NOT false-positive on branches that contribute to the synthesize call

**Pass condition:** Nested dead code detected at correct depth; orphaned branch flagged; contributing branches left alone.

---

### TC-LLINT-06 — LOLLI score computation accuracy

**Scenario:** A pipeline has 12 total bindings. 3 are dead (Level 2), 1 is an orphaned branch (Level 3).

**Input:**
```
Pipeline: governance-audit.ixql
Total bindings: 12
Dead bindings (Level 2): beliefs, evolution, unused_config
Orphaned branches (Level 3): fan_out[2] branch
Live bindings: 8
Side-effect bindings: 1 (alert — correctly excluded from dead count)
```

**Expected behavior:**
- Per-file LOLLI score = 3 / 12 = 0.25 (25%)
  - Only Level 2 dead bindings count toward the ratio
  - Orphaned branches reported separately
- Aggregate LOLLI across all pipelines computed correctly
- Report breakdown:
  - by_level: { 0: 0, 1: 0, 2: 3, 3: 1, 4: 0 }
  - by_severity: { error: 3, warning: 1, info: 0 }
- When aggregate_lolli > 0.2: Discord alert fired
- When aggregate_lolli > 0.3: creation_freeze_check proposed

**Pass condition:** LOLLI score computed correctly; severity breakdown accurate; threshold-based alerts trigger at correct levels.

---

## Test Suite: Cross-Pipeline Dependency Graph

### TC-LLINT-07 — Dependency edge construction and orphan detection

**Scenario:** Three pipelines with partial connectivity.

**Input:**
```
Pipeline A (driver-cycle.ixql):
  reads:  state/beliefs/*.belief.json
  writes: state/driver/health-scores.json, state/driver/manifest-{date}.json

Pipeline B (weakness-probe.ixql):
  reads:  state/driver/health-scores.json, state/beliefs/*.belief.json
  writes: state/driver/weakness-report.json

Pipeline C (research-cycle.ixql):
  reads:  state/streeling/departments/*.json
  writes: state/streeling/departments/*.weights.json
```

**Expected behavior:**
- Edge: A → B via `state/driver/health-scores.json`
- No edge A → C (C doesn't read A's outputs)
- No edge B → C or C → B
- `state/driver/manifest-{date}.json` flagged as orphaned output (no reader)
- `state/driver/weakness-report.json` flagged as orphaned output (no reader)
- Static paths (constitutions/, policies/, etc.) excluded from orphan checks
- Isolated pipelines correctly identified

**Pass condition:** Correct edges built; orphaned outputs flagged; static paths excluded; no false orphan inputs.

---

### TC-LLINT-08 — Circular dependency detection

**Scenario:** Pipeline A writes X, Pipeline B reads X and writes Y, Pipeline C reads Y and writes Z,
Pipeline A reads Z — forming a cycle A → B → C → A.

**Input:**
```
Pipeline A: reads state/feedback/z.json, writes state/feedback/x.json
Pipeline B: reads state/feedback/x.json, writes state/feedback/y.json
Pipeline C: reads state/feedback/y.json, writes state/feedback/z.json
```

**Expected behavior:**
- Cycle detected: [A, B, C, A]
- Severity: critical
- Note: "Circular data dependency — pipelines may deadlock"
- Report includes the full cycle path

**Pass condition:** Cycle correctly identified; severity = critical; full path reported.

---

## Cross-Policy Integration

| Test | Policy Integration | Verified by |
|---|---|---|
| TC-LLINT-01 | anti-lolli-inflation-policy — dead binding feeds LOLLI ratio | lolli-lint-report.json |
| TC-LLINT-02 | completeness-instinct — orphaned output triggers weakness probe | weakness-report.json |
| TC-LLINT-03 | Article 3 (Reversibility) — auto-removal gated; Article 6 (Escalation) — uncertain cases escalate | mitigations.tier assignment |
| TC-LLINT-04 | proto-conscience — side-effect false positive avoidance prevents erroneous conscience signal | conscience signal NOT emitted |
| TC-LLINT-05 | governance-audit (Level 2 cross-ref) — nested dead code caught by audit | audit-report findings |
| TC-LLINT-06 | anti-lolli-inflation-policy — aggregate LOLLI score feeds creation freeze check | creation-freeze.json |
| TC-LLINT-07 | cross-pipeline-deps — dependency graph feeds Level 0/1 lint | cross-pipeline-deps.json |
| TC-LLINT-08 | staleness-detection — circular deps may indicate stale design | staleness-detection trigger |
