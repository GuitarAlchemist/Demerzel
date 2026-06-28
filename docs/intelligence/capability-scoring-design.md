# Capability Scoring Design

Capability scoring is Seldon's mechanism for evaluating how effectively different workers (AI models or humans) perform specific tasks. These scores are used to provide routing recommendations to Demerzel.

## The Scoring Model

Each worker/capability pair is assigned a `capability_score` based on observed outcomes in the Streeling event stream.

```yaml
capability_score:
  capability: implementation | research | adversarial_review | repository_navigation | bug_hunting | security_review
  worker: claude | jules | gemini | codex | augment | qodo | ollama_local | human
  historical_success: 0.0-1.0
  median_cycle_time: duration
  review_iteration_rate: number
  ci_failure_rate: 0.0-1.0
  cost_per_success: number
  confidence_calibration: 0.0-1.0
  sample_size: integer
```

### Component Breakdown

| Field | Description | Calculation |
|---|---|---|
| **Historical Success** | Percentage of tasks completed and merged without regression. | `merged_prs / (merged_prs + reverts + failures)` |
| **Median Cycle Time** | The middle value of time taken from assignment to completion. | `median(completion_timestamp - assignment_timestamp)` |
| **Review Iteration Rate** | Average number of times a worker had to revise work after review. | `total_revisions / total_tasks` |
| **CI Failure Rate** | Frequency of work triggering CI failures before being fixed. | `ci_failures / total_ci_runs` |
| **Cost per Success** | Average financial/compute cost per successful outcome. | `total_cost / successful_outcomes` |
| **Confidence Calibration** | Accuracy of the worker's self-reported confidence. | Correlation between `stated_confidence` and `success` |
| **Sample Size** | Number of observations used to compute the score. | Count of completed tasks |

## Evaluation Capabilities

Seldon tracks performance across these core capabilities:

1. **Implementation:** Translating a spec into working code.
2. **Research:** Exploring a codebase, finding relevant files, and explaining logic.
3. **Adversarial Review:** Identifying bugs, security flaws, and policy violations in others' work.
4. **Repository Navigation:** Effectively using tools to explore a complex file hierarchy.
5. **Bug Hunting:** Reproducing and fixing reported defects.
6. **Security Review:** Specifically scanning for vulnerabilities and secret leaks.

## Weighting & Decay

Scores are not static. Seldon applies the following logic:

- **Recency Bias:** Recent performances are weighted more heavily than older ones (exponential decay).
- **Complexity Weighting:** Successfully completing a "Large" task increases the score more than a "Small" task.
- **Confidence Intervals:** Workers with small sample sizes have lower confidence in their scores (reflected in recommendations).

## Data Sources

Scores are derived from:
- `github_event`: PR merges and reverts.
- `session_event`: Task assignment and completion.
- `ci_event`: Success/failure of specific commits.
- `qa_verdict`: Results of peer reviews (blocking vs. non-blocking).
