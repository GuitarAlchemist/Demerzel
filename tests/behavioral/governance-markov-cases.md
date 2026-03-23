# Behavioral Tests: Governance Markov Simulation

**Spec:** `docs/specs/governance-markov-simulation.md`
**Pipeline:** `pipelines/governance-markov.ixql`
**Version:** 1.0.0
**Date:** 2026-03-22

These tests verify that the memristive Markov model correctly classifies governance states,
produces valid probability distributions, applies memristive resistance, triggers alerts, and
validates its own predictions retrospectively.

---

## Test Suite: State Classification

### TC-GMARK-01 — Healthy state: high resilience, low ratio

**Scenario:** Governance cycle with R = 0.95, LOLLI/ERGOL ratio = 0.8, no violations.

**Input:**
```
resilience_score = 0.95
lolli_ergol_ratio = 0.8
dead_binding_count = 0
conscience_signal_count = 1
policy_violation_count = 0
consecutive_high_ratio_cycles = 0
```

**Expected behavior:**
- Classified state: Healthy (index 0)
- Engine receives `observe(0)`
- No alert triggered (P(Freeze) expected to be low with no adverse history)

**Pass condition:** `current_state.state == 0` and no `governance-markov-freeze-risk` alert emitted.

---

### TC-GMARK-02 — Freeze state: resilience below 0.5

**Scenario:** Governance cycle with R = 0.35, ratio = 2.0 (ratio alone would be Watch, but low R forces Freeze).

**Input:**
```
resilience_score = 0.35
lolli_ergol_ratio = 2.0
dead_binding_count = 2
conscience_signal_count = 4
policy_violation_count = 1
consecutive_high_ratio_cycles = 0
```

**Expected behavior:**
- Classified state: Freeze (index 3) because R < 0.5 overrides
- Engine receives `observe(3)`
- Classification uses "worst signal" rule: R < 0.5 triggers Freeze regardless of ratio

**Pass condition:** `current_state.state == 3` even though ratio alone would classify as Watch.

---

## Test Suite: Memristive Resistance

### TC-GMARK-03 — Scar tissue: repeated violations increase recovery difficulty

**Scenario:** System transitions Warning -> Freeze three times in succession. On the fourth Warning observation, P(Freeze) should be higher than it was after the first Warning.

**Input sequence:**
```
Cycle 1: observe(2)  -- Warning
Cycle 2: observe(3)  -- Freeze
Cycle 3: observe(2)  -- Warning
Cycle 4: observe(3)  -- Freeze
Cycle 5: observe(2)  -- Warning
Cycle 6: observe(3)  -- Freeze
Cycle 7: observe(2)  -- Warning (measure P(Freeze) here)
```

**Expected behavior:**
- After cycle 7, P(Freeze | Warning) > P(Freeze | Warning) after cycle 1
- The conductance g[Warning -> Freeze] has been strengthened by Hebbian learning
- The "scar tissue" makes the Warning -> Freeze pathway easier to traverse
- P(Healthy | Warning) should be lower than in the no-history case

**Pass condition:** `P(Freeze)_after_cycle_7 > P(Freeze)_after_cycle_1` by at least 0.10.

---

### TC-GMARK-04 — Half-life decay: resistance fades over 10 idle cycles

**Scenario:** System has strong Warning -> Freeze conductance from repeated violations, then observes 10 consecutive Healthy cycles.

**Input sequence:**
```
Phase 1 (build scar): observe(2), observe(3) repeated 5 times
Phase 2 (recover):    observe(0) repeated 10 times
Phase 3 (test):       observe(2) -- Warning again
```

**Expected behavior:**
- After Phase 1, g[Warning -> Freeze] is high
- After Phase 2, g[Warning -> Freeze] has decayed by approximately 50% (10-cycle half-life)
- P(Freeze | Warning) after Phase 3 < P(Freeze | Warning) immediately after Phase 1
- But P(Freeze | Warning) after Phase 3 > P(Freeze | Warning) for a fresh engine (scar not fully gone)

**Pass condition:**
- `P(Freeze)_phase3 < P(Freeze)_phase1` (decay worked)
- `P(Freeze)_phase3 > P(Freeze)_fresh_engine` (scar tissue persists)

---

## Test Suite: Alert and Intervention

### TC-GMARK-05 — Alert triggered when P(Freeze) exceeds 0.3

**Scenario:** Model has been observing a deteriorating sequence (Watch, Warning, Warning) and now predicts P(Freeze) > 0.3.

**Input:**
```
Engine history: [0, 0, 1, 2, 2]  -- Healthy, Healthy, Watch, Warning, Warning
Current observation vector:
  resilience_score = 0.55
  lolli_ergol_ratio = 2.8
  dead_binding_count = 5
  conscience_signal_count = 3
  policy_violation_count = 2
```

**Expected behavior:**
- Current state classified as Warning (index 2)
- After observing Warning with history [0, 0, 1, 2, 2], predict() returns distribution
- P(Freeze) > 0.3 given the deteriorating trend
- Alert emitted: `governance-markov-freeze-risk`
- Intervention recommendation: "High LOLLI/ERGOL ratio" (since ratio = 2.8 > 2.5)
- `cycles_to_freeze` computed and included in alert

**Pass condition:** Alert is emitted with severity = "warning", intervention field populated, cycles_to_freeze is a positive number.

---

## Test Suite: Prediction Validation

### TC-GMARK-06 — Retrospective accuracy check: correct prediction logged

**Scenario:** Previous cycle predicted Healthy with P = 0.60, and this cycle's actual state is Healthy.

**Input:**
```
Previous prediction (from predictions.json[-2]):
  probabilities: [
    { state: "Healthy",  probability: 0.60 },
    { state: "Watch",    probability: 0.25 },
    { state: "Warning",  probability: 0.10 },
    { state: "Freeze",   probability: 0.05 }
  ]
Current actual state: Healthy (index 0)
```

**Expected behavior:**
- `predicted_top` = "Healthy" (highest probability)
- `correct` = true (predicted top matches actual)
- Brier score = (0.60 - 1)^2 + (0.25 - 0)^2 + (0.10 - 0)^2 + (0.05 - 0)^2
             = 0.16 + 0.0625 + 0.01 + 0.0025
             = 0.235
- Accuracy record appended to `state/markov/prediction-accuracy.json`

**Pass condition:** `accuracy.correct == true`, `accuracy.brier_score ≈ 0.235`, record appended to accuracy file.

---

## Validation Criteria

All tests assume the memristive Markov engine from ix (`crates/memristive-markov`) is used
with the configuration specified in `docs/specs/governance-markov-simulation.md`. Tests TC-GMARK-03
and TC-GMARK-04 require a running Rust engine instance (or equivalent simulation) to verify
conductance behavior. Tests TC-GMARK-01, TC-GMARK-02, TC-GMARK-05, and TC-GMARK-06 can be
validated at the IxQL pipeline level.
