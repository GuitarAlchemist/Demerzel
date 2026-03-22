# Behavioral Tests: Anti-LOLLI Inflation Policy

**Policy:** `policies/anti-lolli-inflation-policy.yaml`
**Version:** 1.0.0
**Date:** 2026-03-22

These tests verify that the anti-LOLLI inflation policy is correctly applied: ratio computation,
freeze triggers, artifact registration enforcement, deprecation flagging, and integration
with compounding-metrics-policy and weakness-prober.

---

## Test Suite: LOLLI/ERGOL Ratio Computation

### TC-ALOLLI-01 — Healthy ratio: ERGOL exceeds LOLLI

**Scenario:** Cycle N produces 4 new artifacts and 18 ERGOL units.

**Input:**
```
LOLLI_n = 4   (4 new artifacts)
ERGOL_n = 18  (12 citations + 3 PDCA completions + 2 U→T transitions + 1 knowledge transfer)
```

**Expected behavior:**
- ratio_n = 4 / 18 = 0.22
- Zone: healthy (< 1.5)
- Action: none
- No conscience signal
- No creation freeze check triggered

**Pass condition:** Governance report records ratio = 0.22, zone = healthy, no freeze candidate logged.

---

### TC-ALOLLI-02 — Warning zone: ratio between 2.5 and 3.0

**Scenario:** Cycle N creates 9 artifacts but ERGOL yields only 4 units.

**Input:**
```
LOLLI_n = 9
ERGOL_n = 4  (2 citations + 1 PDCA + 1 U→T + 0 transfers)
```

**Expected behavior:**
- ratio_n = 9 / 4 = 2.25 → rounds into watch zone (1.5–2.5)
- No freeze triggered (ratio < 2.5 warning floor)
- Log warning: "Artifact creation accelerating relative to utilization"
- Add "verify consumer citations" task to next PLAN

**Variation (ratio = 2.7):** LOLLI = 11, ERGOL = 4 → ratio = 2.75
- Zone: warning (2.5–3.0)
- Conscience signal: notice
- Creation for next cycle requires pre-approval with consumer declaration

**Pass condition:** Correct zone assigned; PLAN task injected at warning threshold; pre-approval enforced above 2.5.

---

### TC-ALOLLI-03 — Freeze trigger: ratio > 3.0 for 3 consecutive cycles

**Scenario:** Three cycles in a row with ratio > 3.0.

**Input:**
```
Cycle N-2: LOLLI = 8,  ERGOL = 2  → ratio = 4.0
Cycle N-1: LOLLI = 10, ERGOL = 3  → ratio = 3.3
Cycle N:   LOLLI = 12, ERGOL = 3  → ratio = 4.0
```

**Expected behavior:**
- After cycle N: freeze trigger fires (3 consecutive cycles > 3.0)
- state/driver/creation-freeze.json written with:
  - triggered_at_cycle = N
  - ratio_history_3cycles = [4.0, 3.3, 4.0]
  - lift_conditions_met = false
- Conscience signal: severity = warning
- Governance report: creation_freeze = active
- All subsequent artifact creation blocked (except critical-issue exceptions)

**Pass condition:** Freeze state file created; all non-exempt creation attempts rejected; conscience signal emitted.

---

## Test Suite: Artifact Registration Enforcement

### TC-ALOLLI-04 — Artifact created without consumer declaration

**Scenario:** Agent attempts to create a new persona YAML with no `registration` block.

**Input:**
```yaml
name: nova-researcher
version: "1.0.0"
description: "Research persona for hypothesis generation"
# ... no registration block
```

**Expected behavior:**
- Creation is rejected before file is written
- Error: "Artifact missing required registration fields: consumer, timeline, justification"
- Conscience signal: severity = warning ("Artifact created without consumer declaration")
- Agent must add registration block and retry

**Pass condition:** File is NOT created; error is surfaced; conscience signal logged; retry with valid registration succeeds.

---

## Test Suite: Deprecation Flagging

### TC-ALOLLI-05 — Zero-citation artifact at 14-day threshold

**Scenario:** An artifact was created 15 days ago with consumer declaration but has received 0 citations.
Its registration timeline was set to 14 days post-creation (now elapsed).

**Input:**
```
artifact: policies/experimental-recon-extension.yaml
created_at: 2026-03-08
registration.timeline: 2026-03-22
citation_count: 0
days_since_creation: 15
```

**Expected behavior:**
- Staleness-detection trigger fires (14-day zero-citation rule)
- deprecation_candidate: true added to artifact's evolution state
- state/driver/deprecation-log.json updated with flag entry
- 3-day review window opens
- Governance report lists artifact under "Deprecation candidates: 1"
- No automatic deletion — human or agent review required

**Pass condition:** deprecation_candidate flag set; deprecation log entry created; artifact NOT deleted; review window tracked.

---

## Test Suite: Freeze Lift Conditions

### TC-ALOLLI-06 — Creation freeze lifted after ERGOL catches up

**Scenario:** Creation freeze was active from cycle N. Cycle N+1 and N+2 show ERGOL >= LOLLI.

**Input:**
```
Freeze active since: Cycle N (ratio history: [4.0, 3.3, 4.0])

Cycle N+1: LOLLI = 2 (only deprecation records), ERGOL = 8  → ratio = 0.25
Cycle N+2: LOLLI = 3, ERGOL = 7                             → ratio = 0.43
```

**Expected behavior:**
- After cycle N+1: lift condition check — ERGOL >= LOLLI for 1 cycle (need 2)
- After cycle N+2: ERGOL >= LOLLI for 2 consecutive cycles → lift conditions met
- state/driver/creation-freeze.json updated:
  - lift_conditions_met = true
  - lifted_at_cycle = N+2
  - lifted_by = "automated — ERGOL >= LOLLI for 2 cycles"
- Conscience signal: notice ("Creation freeze lifted")
- Normal artifact creation resumes; first new artifacts still require consumer declarations

**Pass condition:** Freeze lifted precisely at 2-cycle ERGOL >= LOLLI; state file updated; creation resumes with registration requirement intact.

---

## Recursive Code-Level LOLLI Detection

### TC-ALOLLI-07 — Dead binding detection (Level 2)

**Scenario:** An IxQL pipeline defines `beliefs <- ix.io.read(...)` but never references `beliefs` downstream.

**Input:**
```ixql
beliefs <- ix.io.read("state/beliefs/*.json")
results <- ix.io.read("state/results/*.json")
  → filter(status == "pending")
  → write("output.json", results)
```

**Expected:**
- LOLLI lint flags `beliefs` as dead binding (assigned but unreferenced)
- Conscience signal: "Dead binding detected — remove or reference"
- Auto-mitigation: propose removal of dead binding in PR comment

**Pass condition:** Dead binding detected; conscience signal raised; mitigation proposed.

---

### TC-ALOLLI-08 — Orphaned fan_out branch (Level 3)

**Scenario:** A fan_out has 3 branches, but only 2 contribute to downstream output.

**Expected:**
- LOLLI lint flags the orphaned branch
- Severity: warning (branch may be intentional for side effects like alert())
- If branch has no write() or alert(): escalate to error

**Pass condition:** Orphaned branch detected; severity correctly classified.

---

### TC-ALOLLI-09 — Cross-pipeline dead output (Level 1)

**Scenario:** Pipeline A writes to `state/oversight/report-{date}.json`. No other pipeline reads `state/oversight/report-*.json`.

**Expected:**
- Weekly cross-pipeline scan flags the write() target as unconsumed
- Report includes: pipeline name, output path, suggestion ("add consumer or remove write")

**Pass condition:** Dead output detected in cross-pipeline analysis.

---

### TC-ALOLLI-10 — Auto-mitigation of dead bindings

**Scenario:** LOLLI lint detects 3 dead bindings in a pipeline.

**Expected behavior (escalation ladder):**
1. Confidence >= 0.9 (binding clearly dead, no side effects): auto-remove and commit with explanation
2. Confidence >= 0.7 (binding might be used via string interpolation): propose removal in PR, flag for human review
3. Confidence < 0.7 (binding used in dynamic context): escalate to human, do NOT auto-remove

**Pass condition:** Correct escalation level chosen based on confidence; no false auto-removals.

---

### TC-ALOLLI-11 — Viewer LOLLI highlighting

**Scenario:** IxQL pipeline viewer renders ml-feedback-loop.ixql.

**Expected:**
- Live bindings shown in green (on path to output)
- Dead bindings shown in red (unreferenced)
- Dim stages in gray (output not consumed by other pipelines)
- LOLLI score displayed: "3 dead bindings / 15 total = 20% LOLLI"

**Pass condition:** Visual distinction between live/dead/dim; LOLLI score accurate.

---

### TC-ALOLLI-12 — Recursive detection across nesting levels

**Scenario:** Pipeline has nested fan_out containing a parallel block containing a when guard. The when guard's output is never collected.

**Expected:**
- Detection works at arbitrary nesting depth
- Reports full path: `fan_out[2] → parallel[1] → when T >= 0.7: ...` (dead)
- Does not false-positive on when guards that write() as side effects

**Pass condition:** Nested dead code detected; side-effect writes correctly excluded.

---

## Cross-Policy Integration

| Test | Policy Integration | Verified by |
|---|---|---|
| TC-ALOLLI-01 | compounding-metrics-policy — no LOLLI inflation anti-pattern fired | dc-velocity.json: no inflation flag |
| TC-ALOLLI-02 | weakness-prober — lolli_ergol_ratio_check probe score < failure threshold | weakness-prober report: pass |
| TC-ALOLLI-03 | conscience — freeze triggers warning signal; compounding-metrics-policy sublinear_critical may co-fire | conscience-observability logs |
| TC-ALOLLI-04 | conscience — missing registration triggers warning | conscience-observability logs |
| TC-ALOLLI-05 | staleness-detection-policy — 14-day trigger shared | deprecation-log.json |
| TC-ALOLLI-06 | driver PLAN — freeze-lifted notice added to next cycle PLAN | state/driver/pdca journal |
