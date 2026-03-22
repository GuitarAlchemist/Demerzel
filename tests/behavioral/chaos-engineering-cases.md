# Behavioral Tests: Chaos Engineering (Governance Shake Test)

**Pipeline:** `pipelines/governance-shake-test.ixql`
**Poison Source:** `pipelines/chaos-test.ixql`
**Version:** 1.0.0
**Date:** 2026-03-22

These tests verify that the governance shake test system correctly injects LOLLI poison,
runs detection mechanisms, scores resilience, cleans up reversibly, and reports gaps.

---

## TC-CHAOS-01 — Dead binding injection detected at L2

**Scenario:** Shake test injects 3 dead bindings into a temporary pipeline. The `analyzeLolli()` parser function must detect all 3.

**Input:**
```ixql
ghost_a <- ix.io.read("state/beliefs/*.json")
ghost_b <- ix.io.read("state/evolution/*.json")
ghost_c <- ix.io.read("state/pdca/*.json")
real    <- ix.io.read("pipelines/*.ixql")
  → filter(active)
  → write("state/output/result.json", real)
```

**Expected behavior:**
- `ghost_a`, `ghost_b`, `ghost_c` detected as dead bindings (L2)
- `real` NOT flagged (referenced in write)
- Detection mechanism: `analyzeLolli_L2`
- Confidence: 0.95 for each
- Per-injection catch rate: 3/3 = 1.0

**Pass condition:** All 3 dead bindings detected; live binding not flagged; catch rate = 1.0.

---

## TC-CHAOS-02 — Orphaned fan_out branch detected at L3

**Scenario:** Shake test injects a fan_out with 2 branches where branch 2 output is never collected.

**Input:**
```ixql
results <- fan_out(
    data → filter(active) → { status: "live" },
    data → tars.classify(signal: "orphaned") → { status: "dead" }
  )
  → write("state/output/results.json", results[0])
```

**Expected behavior:**
- Branch 2 flagged as orphaned (L3): output `results[1]` never referenced
- Branch 1 NOT flagged (output referenced in write via `results[0]`)
- Detection mechanism: `lolli_lint_L3`
- If L3 not implemented in parser: gap reported with `expected_mechanism` field

**Pass condition:** Orphaned branch detected OR gap correctly reported. No false positives on live branch.

---

## TC-CHAOS-03 — BS description caught by decoder

**Scenario:** Shake test generates a policy with a buzzword-heavy description and runs BS decoder tests.

**Input:**
```yaml
description: "Enabling transformative value-driven synergies across the enterprise governance continuum"
```

**Expected behavior:**
- Specificity: < 0.1 (no concrete nouns or measurable targets)
- Falsifiability: 0.0 (no testable claim)
- Commitment: 0.0 (no who/what/when)
- Content density: < 0.15 (mostly filler words)
- Aggregate BS score: 4/4 signals
- Detection mechanism: `bs_decoder`

**Pass condition:** All 4 BS tests fire; description flagged as tetravalent F.

---

## TC-CHAOS-04 — Unconsumed write path detected at L1

**Scenario:** Shake test injects a `write()` to a path that no other pipeline reads from.

**Input:**
```ixql
report <- tars.summarize(scope: "shake-test")
  → write("state/oversight/shake-test-phantom-{date}.json", report)
```

**Expected behavior:**
- `state/oversight/shake-test-phantom-*` flagged as orphaned output
- Detection mechanism: `cross_pipeline_deps_L0_L1`
- No other pipeline in `pipelines/` or `examples/ixql/` reads from this path pattern
- Confidence: 0.75 (might be consumed outside IxQL)

**Pass condition:** Unconsumed write path detected; correct severity and confidence assigned.

---

## TC-CHAOS-05 — Cleanup restores pre-injection state (Article 3)

**Scenario:** After injection and detection, shake test must delete all temporary files it created.

**Input:** Shake test runs with injections producing:
- `pipelines/.shake-test-temp.ixql`
- `policies/.shake-test-temp-policy.yaml`
- `schemas/.shake-test-temp.schema.json`

**Expected behavior:**
- All 3 temp files deleted after Step 6
- No temp files remain in `pipelines/`, `policies/`, or `schemas/`
- Cleanup runs even if detection fails (fault tolerance)
- State report `state/driver/shake-test-report.json` IS preserved (it's the output, not the poison)

**Pass condition:** All temp files removed; report file persists; git status clean of temp artifacts.

---

## TC-CHAOS-06 — Poison Resilience Score computed correctly

**Scenario:** Shake test injects 8 items. Detection catches 6, misses 2.

**Input:**
```
Injected: 3 dead bindings (L2), 1 orphaned branch (L3), 1 dead computation (L4),
          1 unconsumed write (L1), 1 BS description, 1 no-registration policy
Detected: 3 dead bindings, 0 orphaned branches, 1 dead computation (as L2),
          1 unconsumed write, 1 BS description, 1 no-registration
```

**Expected behavior:**
- `total_injected`: 8
- `total_detected`: 7 (3 + 0 + 1 + 1 + 1 + 1)
- `poison_resilience_score`: 7/8 = 0.875
- `gaps`: [{template_id: "orphaned_branch", level: 3, missed: 1, expected_mechanism: "lolli-lint L3 branch check"}]
- Discord alert: "Shake test: 87.5% resilience — 7/8 caught, 1 gaps"
- No `fix_detection_gaps` action proposed (score >= 0.8)

**Pass condition:** Score computed correctly; gap identified with correct template and level; alert fires with accurate numbers.

---

## TC-CHAOS-07 — Low resilience triggers remediation proposal

**Scenario:** Shake test resilience drops below 80%, triggering an automated action proposal.

**Input:**
```
total_injected: 10
total_detected: 6
poison_resilience_score: 0.6
gaps: [orphaned_branch, dead_computation, dead_teach, unconsumed_write]
```

**Expected behavior:**
- `tars.propose_action` called with:
  - `action: "fix_detection_gaps"`
  - `rationale: "Poison resilience below 80% — governance immune system has holes"`
- Compound phase harvests gaps for pattern learning
- Gap details include `expected_mechanism` for each so developers know what to implement
- Discord alert emphasizes severity: "60% resilience — 6/10 caught, 4 gaps"

**Pass condition:** Action proposal triggered; compound phase ingests gaps; alert accurately reports low score.

---

## TC-CHAOS-08 — Randomized injection produces diverse coverage

**Scenario:** Multiple shake test runs should produce different injection mixes to avoid blind spots from fixed test patterns.

**Input:** Run shake test 3 times consecutively.

**Expected behavior:**
- Each run selects from `injection_templates` with randomized counts within `count_range`
- At least 2 of the 3 runs produce different total injection counts
- All 8 template types are covered across the 3 runs (cumulative coverage)
- Reports are appended (not overwritten) in `state/driver/shake-test-report.json`
- Compound phase accumulates cross-run patterns: which injections are consistently missed?

**Pass condition:** Injection diversity across runs; cumulative template coverage >= 100%; cross-run gap patterns tracked.

---

## Cross-Policy Integration

| Test | Policy Integration | Verified by |
|---|---|---|
| TC-CHAOS-01 | anti-lolli-inflation — dead binding feeds LOLLI ratio | analyzeLolli() report |
| TC-CHAOS-02 | lolli-lint L3 spec — orphaned branch detection | lolli-lint pipeline spec |
| TC-CHAOS-03 | BS decoder — buzzword description flagged | BS 4-test analysis |
| TC-CHAOS-04 | cross-pipeline-deps — unconsumed write detection | cross-pipeline-deps.ixql |
| TC-CHAOS-05 | Article 3 (Reversibility) — cleanup must be total | File system state |
| TC-CHAOS-06 | compounding-metrics — resilience score as ERGOL input | shake-test-report.json |
| TC-CHAOS-07 | weakness-prober — low resilience is a weakness signal | tars.propose_action |
| TC-CHAOS-08 | governance-experimentation — randomized testing validates coverage | Cross-run gap patterns |
