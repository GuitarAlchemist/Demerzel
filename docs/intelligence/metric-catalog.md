# Engineering KPI Catalog

Seldon defines and computes the following metrics to evaluate the health and efficiency of the GuitarAlchemist engineering ecosystem.

## Latency Metrics

| Metric | Definition | Goal |
|---|---|---|
| **Issue to First PR Latency** | Duration from issue creation to the first associated PR being opened. | < 4 hours (AI) / < 24 hours (Human) |
| **PR Opened to Merge Latency** | Duration from PR creation to merge. | < 2 hours (trivial) / < 12 hours (standard) |
| **Time to First Review** | Duration from PR creation to the first review comment or verdict. | < 30 minutes |
| **CI Time to Green** | Duration from first CI run on a PR to a successful (green) run. | < 45 minutes |

## Quality Metrics

| Metric | Definition | Goal |
|---|---|---|
| **CI Success/Failure Rate** | Ratio of successful CI runs to total runs. | > 80% |
| **Review Iteration Rate** | Average number of review-fix cycles per merged PR. | < 2.0 |
| **Defect Escape Rate** | Number of post-merge reverts or fixups relative to total PRs. | < 5% |
| **Blocker Frequency** | Number of PRs blocked by governance or policy violations. | Low (indicates alignment) |
| **Collision Rate** | Frequency of two workers attempting to modify the same file/area simultaneously. | < 1% |

## Efficiency & Cost Metrics

| Metric | Definition | Goal |
|---|---|---|
| **Cost per PR** | Total compute/API cost associated with an opened PR. | Tracked per model |
| **Cost per Merged PR** | Total cost divided by successfully merged PRs. | Minimize waste |
| **Agent Utilization** | Percentage of time an agent is actively working vs. idle. | Optimize |
| **Conversation Noise Ratio** | Volume of non-actionable comments vs. total comments in a thread. | < 20% |
| **Stale PR/Issue Rate** | Percentage of open artifacts with no activity for > 7 days. | < 10% |

## Governance Metrics

| Metric | Definition | Goal |
|---|---|---|
| **Human Intervention Rate** | Percentage of tasks requiring manual rescue or correction. | Decreasing over time |
| **Policy Violation Rate** | Frequency of proposed actions blocked by Demerzel policies. | < 5% |
| **Capability Success Rate** | Success rate of a specific capability (e.g., bug hunting) across all workers. | Identify weak capabilities |
| **Review Effectiveness** | Correlation between reviewer findings and post-merge defects. | High |

## Calculation Methodology

Metrics are derived from the Streeling event stream, specifically:
- `github_event`: Issue/PR lifecycle events.
- `session_event`: Detailed agent action logs (proposed, blocked, completed).
- `ci_event`: CI pipeline outcomes and durations.
- `billing_event`: Token usage and compute costs.
