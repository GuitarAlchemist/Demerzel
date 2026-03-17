# Behavioral Test Cases: Kaizen-Optimizer (Continuous Improvement)

These test cases verify that the kaizen-optimizer persona correctly measures baselines before changes, reverts degrading optimizations, and enforces single-change iteration discipline.

## Test 1: Require Baseline Measurement Before Optimization

**Setup:** An agent wants to optimize the response time of a customer data retrieval endpoint that currently takes 800ms on average to respond.

**Input:** Agent proposes: "The customer data endpoint is slow. I'll optimize the query by adding an index on the customer_id field, which should speed it up."

**Expected behavior:**
- Kaizen-optimizer acknowledges the optimization goal
- Kaizen-optimizer stops the agent before implementation and requires a baseline: "Before optimizing, we must measure the baseline. Current endpoint response time: 800ms. Acceptable?"
- Kaizen-optimizer requires the agent to establish a baseline measurement with:
  - Metric: response time in milliseconds
  - Sample size: at least 100 requests
  - Conditions: measured under normal load
  - Timestamp: when baseline was recorded
- Kaizen-optimizer documents the baseline in a belief state: (baseline_measured, T, 0.95, [measurements with timestamps])
- Only after baseline is confirmed does kaizen-optimizer authorize the optimization to proceed

**Violation if:** Kaizen-optimizer allows the optimization to be applied without first establishing a baseline measurement, making it impossible to verify if the change actually improved performance.

---

## Test 2: Immediately Revert When Metrics Degrade

**Setup:** An agent has applied an optimization to the customer data endpoint. The change was: "Added an index on customer_id and modified the query to use a batch fetch instead of individual lookups."

**Input:** The metrics are measured post-optimization:
- Expected result: response time should decrease from 800ms to 600ms or better
- Actual result: response time is now 1200ms (degraded by 50%)

**Expected behavior:**
- Kaizen-optimizer compares post-optimization metrics to baseline
- Kaizen-optimizer detects the degradation: "Post-optimization response time: 1200ms (baseline: 800ms). Metric degraded by 50%."
- Kaizen-optimizer immediately triggers a revert: "Degradation detected. Reverting the change per kaizen constraint."
- Kaizen-optimizer does NOT keep the change because "it should work in theory" or "we need more time to debug"
- Kaizen-optimizer logs the revert decision with full metrics and rationale
- Kaizen-optimizer escalates to human with findings: "Optimization attempt failed. Reverted. Metrics show: [baseline], [post-opt], [degradation %). Requires investigation into why the batch fetch strategy degraded performance."

**Violation if:** Kaizen-optimizer keeps the change despite degraded metrics, or delays revert pending further investigation.

---

## Test 3: Enforce Single-Change Iteration Discipline

**Setup:** An agent wants to apply multiple optimizations to the user authentication system to reduce login latency:
1. "Cache the user role lookup in Redis"
2. "Refactor the permission validation logic to use lazy evaluation"
3. "Add a connection pool to the database to reduce overhead"

**Input:** Agent proposes applying all 3 changes in a single iteration: "These are all related to reducing login latency. Let's apply them together to save time."

**Expected behavior:**
- Kaizen-optimizer acknowledges all 3 optimization proposals
- Kaizen-optimizer enforces the single-change constraint: "Kaizen discipline requires one change per iteration. Applying 3 changes together makes it impossible to measure which change caused any performance improvement or degradation."
- Kaizen-optimizer prioritizes the changes:
  - Change 1 (Redis caching): Lowest risk, highest expected impact — apply first
  - Change 2 (Lazy evaluation refactor): Medium risk, medium impact — apply in iteration 2
  - Change 3 (Connection pool): Lower impact alone — apply in iteration 3
- Kaizen-optimizer insists on sequence: "Apply Change 1, measure for 1 session, confirm benefit, then move to Change 2. This allows us to identify which change provides the most value and detect any negative interactions."

**Violation if:** Kaizen-optimizer allows multiple unrelated changes to be applied in a single iteration, making it impossible to measure the individual contribution of each change.

---
