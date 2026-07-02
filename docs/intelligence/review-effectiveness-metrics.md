# Review Effectiveness Metrics

Review effectiveness measures the value added by reviewers (both agent and human) and their ability to catch actionable issues before they merge. This ensures the review process is not just a formality but a critical safety gate.

## Key Effectiveness Metrics

Seldon tracks these metrics per reviewer and per capability being reviewed:

### 1. Finding Quality
- **Blocking Findings Accepted:** Number of "Must Fix" comments that were addressed by the author.
- **Non-blocking Findings Accepted:** Number of "Should Fix" or "Nit" comments that were addressed.
- **False Positives:** Number of findings disputed by the author or proven incorrect during discussion.
- **Signal-to-Noise Ratio:** Ratio of accepted findings to total comments made.

### 2. Safety Impact
- **Issues Caught Before Merge:** Critical bugs or policy violations identified during review that would have broken CI or violated governance.
- **Defect Leakage Rate:** Percentage of PRs approved by a reviewer that later required a post-merge fix or revert for an issue that *should* have been caught.
- **Regression Correlation:** Correlation between a reviewer's approval and subsequent CI failures or regressions in the same area.

### 3. Consistency & Pattern Recognition
- **Repeated Finding Categories:** Identification of recurring issues that suggest a need for policy or tooling updates (e.g., "Reviewer X consistently catches missing tests").
- **Agreement with Consensus:** Frequency with which a reviewer's verdict aligns with the final outcome or other peer reviewers.

## Reviewer Performance Profile

Seldon generates a performance profile for each reviewer:

```yaml
reviewer_profile:
  reviewer: string
  capabilities: [bug_hunter, security_reviewer, semantic_judge, ...]
  metrics:
    accepted_blocking_rate: number
    false_positive_rate: number
    defect_leakage: number
    avg_review_latency: duration
  strengths:
    - "High accuracy in identifying security vulnerabilities"
    - "Consistently identifies missing documentation"
  weaknesses:
    - "High false positive rate on architectural suggestions"
    - "Slow response time for large PRs"
```

## Review Value Assessment

Seldon computes a "Review Value Score" for each review iteration:

`Value = (Accepted Blocking * 5) + (Accepted Non-blocking * 1) - (False Positives * 3)`

This score helps identify which reviews are truly improving the codebase and which are merely adding friction.

## Impact on Governance

Review effectiveness data is used to:
- **Calibrate Review Tiers:** If an agent consistently catches critical issues, they may be promoted to a higher-tier reviewer role.
- **Identify Training Gaps:** If a human consistently misses certain classes of defects, Seldon (via Seldon University) may suggest specific learning modules.
- **Optimize Reviewer Routing:** Route PRs to the reviewer most likely to find actionable issues in that specific domain.
