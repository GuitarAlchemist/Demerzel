# Worker Reliability Metrics

Worker reliability measures the consistency and dependability of a specific agent or human within the Harness ecosystem. While capability scoring focuses on *what* they can do, reliability focuses on *how* they do it.

## Reliability Dimensions

Seldon tracks the following reliability indicators for each worker:

### 1. Completion & Follow-through
- **Completion Rate:** Percentage of assigned tasks that reach a terminal state (merged or closed) vs. abandoned.
- **Scope Creep Frequency:** Rate at which a worker adds changes outside the original task's scope without justification.
- **Human Rescue Rate:** Frequency with which a human must intervene to fix an agent's work or unblock a stalled process.

### 2. Responsiveness
- **Time to First Response:** Average time from task assignment to the first action or comment.
- **Time to PR:** Average time from starting a task to opening the first PR.
- **Time to Fix after Review:** Speed at which a worker addresses review feedback.

### 3. Stability & Precision
- **CI Failure Frequency:** Rate of commits that break the build or fail tests.
- **False Confidence Frequency:** Frequency of a worker claiming a task is "done" or "verified" when it is not (e.g., tests fail or PR is rejected).
- **Tool Hallucination Rate:** Frequency of attempting to use non-existent tools or incorrect tool parameters.

## Reliability Report Structure

Seldon generates periodic reliability reports for each worker:

```yaml
worker_reliability:
  worker: string
  period: date_range
  overall_reliability_score: 0.0-1.0
  metrics:
    completion_rate: number
    avg_rescue_rate: number
    avg_response_latency: duration
    avg_ci_pass_rate: number
    false_confidence_events: integer
  anomalies:
    - "Sudden spike in CI failures on ga repo"
    - "Significant latency increase for implementation tasks"
  recommendation:
    - "Limit to Small tasks until CI pass rate improves"
    - "Escalate to human review for security-critical areas"
```

## Impact on Routing

Reliability scores serve as a multiplier for capability scores in the routing engine:

- **High Reliability (0.9+):** Recommended for autonomous work with minimal oversight.
- **Medium Reliability (0.7-0.9):** Recommended with standard peer review.
- **Low Reliability (< 0.7):** Requires high-tier human review or restricted affordances.
- **Unknown Reliability:** New workers are treated with caution (low trust) until a sufficient sample size is reached.
