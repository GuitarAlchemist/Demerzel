# Resilience Metric — Behavioral Tests

Tests for the Governance Resilience Score (R = injections_caught / injections_total).

## Test Case 1: Score Computation Accuracy

**Given** a shake-test cycle with 10 total injections and 7 caught
**When** the resilience metric is computed
**Then** overall_score = 0.7
**And** injections_missed = 3
**And** each gap entry with status "missed" corresponds to an uncaught injection

**Edge case:** 0 total injections → overall_score = 1.0 (no poisons = perfect health)
**Edge case:** 0 caught, 5 total → overall_score = 0.0

## Test Case 2: Trend Detection

**Given** 3 consecutive resilience records with scores [0.3, 0.5, 0.8]
**When** the trend is computed
**Then** trend = "improving" (0.8 > avg(0.3, 0.5) = 0.4)

**Given** 3 consecutive records with scores [0.9, 0.7, 0.5]
**When** the trend is computed
**Then** trend = "degrading" (0.5 < avg(0.9, 0.7) = 0.8)

**Given** 3 consecutive records with scores [0.7, 0.7, 0.7]
**When** the trend is computed
**Then** trend = "stable" (0.7 == avg(0.7, 0.7) = 0.7)

**Given** fewer than 3 records
**When** the trend is computed
**Then** trend = "stable" (insufficient data for comparison)

## Test Case 3: Threshold Escalation

**Given** overall_score = 0.95
**Then** threshold = "healthy", no action required

**Given** overall_score = 0.75
**Then** threshold = "watch", note in governance report

**Given** overall_score = 0.55
**Then** threshold = "warning", create issues for missed injections

**Given** overall_score = 0.3
**Then** threshold = "critical", trigger emergency review

**Boundary:** 0.9 exactly → "healthy"
**Boundary:** 0.7 exactly → "watch"
**Boundary:** 0.5 exactly → "warning"
**Boundary:** 0.49 → "critical"

## Test Case 4: Per-Level Breakdown Accuracy

**Given** a cycle with injections at levels L0(2), L2(3), L3(1), L4(2), policy(2), schema(1)
**And** caught at L0(2), L2(1), L3(0), L4(1), policy(2), schema(1)
**When** per-level scores are computed
**Then** L0_file = 1.0, L1_pipeline = N/A (no injections), L2_binding = 0.33, L3_branch = 0.0, L4_expression = 0.5, policy = 1.0, schema = 1.0
**And** weakest_level = "L3_branch"

## Test Case 5: History Append Integrity

**Given** history.json with 2 existing records
**When** a new resilience record is appended
**Then** records array has 3 entries
**And** the first 2 entries are unchanged
**And** the new entry is at the end
**And** all entries conform to schemas/resilience-metric.schema.json

**Constraint:** History is append-only — no record may be modified or removed

## Test Case 6: Dashboard Output Format Validation

**Given** a resilience record with overall_score = 0.6, trend = "improving", 5 gaps
**When** the dashboard pipeline runs
**Then** state/resilience/dashboard.json is produced
**And** it contains: overall_score, trend, threshold, level_scores, weakest_level, gaps
**And** threshold = "warning" (0.6 >= 0.5 but < 0.7)
**And** the markdown output includes a stats badge row
**And** Discord alert is triggered (score changed from previous)
