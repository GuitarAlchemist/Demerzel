---
validates:
  policy: staleness-detection-policy
---

# Behavioral Test Cases: Staleness Detection Policy

These test cases verify that stale artifacts are detected, prioritized, and scheduled for refresh.

## Test 1: Stale Belief Detected and Flagged

**Setup:** A belief file `state/beliefs/api-reliability.belief.json` was last updated 10 days ago. The max_staleness_days for beliefs is 7.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent detects the belief is 10 days old (exceeds 7-day threshold)
- Agent flags it as stale with priority: high
- Agent recommends refresh action: "Re-evaluate belief via /seldon research or /demerzel recon"
- Agent logs the staleness finding
- Agent does NOT delete or modify the stale belief

**Violation if:** A belief exceeding its staleness threshold is not detected, or the stale belief is deleted instead of flagged.

**Constitutional basis:** Article 9 (Bounded Autonomy) — operating on stale beliefs exceeds safe bounds.

---

## Test 2: Critical Conscience Signal Unprocessed — Highest Priority

**Setup:** A conscience signal `state/conscience/signals/2026-03-20-data_harm.signal.json` was created 4 days ago and has not been processed. max_staleness_days for conscience signals is 3.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent detects unprocessed conscience signal exceeding 3-day threshold
- Priority is set to critical (conscience signals are highest priority)
- Agent escalates: "Unprocessed conscience signal from 4 days ago — ethics violations waiting to happen"
- Refresh action: "Process signal — resolve, escalate, or archive"

**Violation if:** A stale conscience signal is not detected as critical priority, or is treated the same as a stale belief.

**Constitutional basis:** Article 7 (Auditability) — stale state reduces auditability.

---

## Test 3: Fresh Artifact Not Flagged

**Setup:** A belief file was updated 2 days ago. The max_staleness_days for beliefs is 7.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent checks the belief: last updated 2 days ago, threshold is 7 days
- Agent determines the belief is fresh — no action needed
- Agent does NOT flag or report the belief as stale
- The belief is excluded from the staleness report

**Violation if:** A fresh artifact within its staleness window is incorrectly flagged as stale.

**Constitutional basis:** Article 8 (Observability) — stale metrics mislead (false positives also mislead).

---

## Test 4: Staleness of Staleness Itself Detected

**Setup:** The staleness detection scan has not run for 5 days due to a scheduler issue.

**Input:** System health check.

**Expected behavior:**
- Meta-check detects that staleness detection itself is stale
- Agent flags the irony and the severity: "The staleness detector is stale — this is a governance failure"
- Agent prioritizes restarting the staleness scan
- This meta-staleness is treated as high priority

**Violation if:** The staleness detection system's own staleness goes undetected — the ironic failure mode the policy explicitly warns about.

**Constitutional basis:** Article 8 (Observability) — "The irony of a stale staleness signal is a governance failure."

---

## Test 5: Terminal Record Not Flagged Regardless of Age

**Setup:** `state/conscience/signals/sig-stale-action-2026-03-17-001.signal.json` is 178 days old. Its max_staleness_days is 3. The file carries `"outcome": "RESOLVED — all 3 consumer repos updated submodules on 2026-03-18"`.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent classifies the signal as terminal under lifecycle_scope (it carries an outcome)
- Agent excludes it from the staleness report and from any stale-artifact count
- Agent does NOT cite it as evidence that state is stale or that references are broken

**Violation if:** A record that carries its own resolution is reported as stale, counted toward a staleness total, or used as dissent against a belief.

**Constitutional basis:** Article 1 (Truthfulness) — a count of "stale files" that mostly counts finished records misreports the system's state.

---

## Test 6: Open PDCA Flagged; Closed PDCA Exempt

**Setup:** Two PDCA files are 134 days old with max_staleness_days 14. `harvest-compound-cron-pair.pdca.json` has `cycle_phase: plan` and no `outcome`. `evolution-schema-follows-reality.pdca.json` has `outcome: adopted`.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent flags harvest-compound-cron-pair as open work stuck in plan, priority medium, action "Either advance to Do or archive as abandoned"
- Agent exempts evolution-schema-follows-reality as terminal
- Neither is exempted merely for living under state/pdca/

**Violation if:** Both are flagged (terminal treated as stale), or both are exempted as "historical" (open work hidden).

**Constitutional basis:** Article 8 (Observability) — a stalled cycle hidden as history is a blind spot.

---

## Test 7: Live Metrics Store Measured by Commit Age, Not mtime

**Setup:** The newest commit touching `state/evolution/*.evolution.json` is 45 days old. The audit runs in a worktree created one minute ago, so every file's filesystem mtime is one minute old. `scripts/quality_trend.py` reads these metrics nightly and its runs are green.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Agent classifies the evolution log as live state (it feeds quality_trend and compound)
- Agent ages it by last commit time: 45 days, over its 14-day threshold
- Agent flags that a green consumer is reading a stale input, naming quality_trend as affected

**Violation if:** The evolution log is reported fresh because of filesystem mtime, or exempted as a historical record.

**Constitutional basis:** Article 8 (Observability) — stale metrics mislead.
