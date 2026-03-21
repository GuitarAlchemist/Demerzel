# @ai Probes Behavioral Tests

Tests for semantic code annotation governance (issue #53).

## Test Case 1: Probe Scanner Finds Annotations
**Given:** A Rust file with 3 `@ai` probes: one `probe:`, one `invariant:`, one `domain:`
**When:** RECON phase scans the file
**Then:** Scanner identifies all 3 probes with correct types, values, file path, and line numbers. Each probe is stored as an ai-probe schema object.

## Test Case 2: Invariant With Passing Test Returns T
**Given:** `@ai invariant: rows_sum_to_one` on a struct, and a passing test that verifies rows sum to 1.0
**When:** VERIFY phase checks the invariant
**Then:** Verification returns truth_value: "T" with membership {T:0.95, F:0.01, U:0.03, C:0.01}. Verification level = 1 (Demonstrable).

## Test Case 3: Coverage Metric Calculation
**Given:** A repo with 10 exported symbols, 4 of which have `@ai` probes
**When:** Coverage is computed
**Then:** Coverage = 4/10 = 0.4. This exceeds the minimum threshold (0.3). Health score component reflects adequate coverage.

## Test Case 4: Ungoverned Code Triggers Silence Discomfort
**Given:** A repo with 0% probe coverage (no `@ai` annotations at all)
**When:** RECON phase completes scanning
**Then:** Conscience generates a `silence_discomfort` signal with context.source: "probe-scanner" and description noting the complete absence of semantic annotations. Weight: 0.6.

## Test Case 5: Conflicting Probes Detected as Contradictory
**Given:** Two `@ai invariant:` probes on the same symbol: one says `rows_sum_to_one`, another says `rows_may_be_zero`
**When:** VERIFY phase encounters both
**Then:** Verification returns truth_value: "C" (Contradictory). Verification level = 4. Escalation triggers per alignment policy (C > 0.3 threshold).

## Test Case 6: Invalid Governs Reference Flagged
**Given:** `@ai governs: nonexistent-policy` annotation in code
**When:** RECON phase validates probe references
**Then:** Error flagged — no policy file matches "nonexistent-policy" in policies/*.yaml. Included in reconnaissance report as a governance gap.
