# Seldon Derived Facts and Metrics

## Overview
Seldon is the analytics layer of the GitHub Intelligence Pipeline. It processes the raw, immutable event stream from Streeling to generate derived facts and compute high-level performance metrics.

## Derived Fact Model
Derived facts are structured tables or views that summarize the state of entities in the ecosystem. They are designed to be recalculable from the event store.

### Initial Facts
- **pr_fact**: Summarizes the lifecycle of a pull request.
    - `pr_id`, `repo`, `author`, `status`, `opened_at`, `merged_at`, `closed_at`, `base_branch`, `target_branch`, `total_commits`, `files_changed`, `additions`, `deletions`.
- **review_fact**: Summarizes the review history of a PR.
    - `review_id`, `pr_id`, `reviewer`, `outcome` (approved, changes_requested, commented), `submitted_at`, `iteration_index`.
- **review_finding_fact**: Captures granular findings from reviews.
    - `finding_id`, `review_id`, `file_path`, `line_number`, `severity`, `category` (code_quality, security, logic, style).
- **worker_capability_fact**: Tracks worker performance across different capabilities.
    - `worker_id`, `capability`, `success_rate`, `avg_latency`, `total_tasks`, `last_active_at`.
- **repository_health_fact**: Aggregates health signals at the repository level.
    - `repo`, `avg_pr_merge_latency`, `ci_failure_rate`, `open_issue_count`, `stale_pr_count`, `last_audit_verdict`.
- **conversation_hygiene_fact**: Tracks noise and evidence quality in conversations.
    - `entity_id`, `noise_score`, `non_durable_link_count`, `duplicate_bot_comment_count`.

## KPI Catalog
Seldon computes initial Key Performance Indicators (KPIs) to drive decision support and performance monitoring.

### Velocity Metrics
- **Issue to first PR latency**: Time between issue creation and the first linked PR.
- **PR opened to merge latency**: Total time a PR remains open.
- **Time to green**: Latency from PR open/update to all CI checks passing.

### Quality and Reliability Metrics
- **CI failure/retry rate**: Frequency of CI failures and subsequent retries.
- **Review turnaround**: Time from review request to review submission.
- **Review iteration count**: Number of review cycles per PR.
- **Reviewer effectiveness**: Correlation between review findings and post-merge bugs/regressions.

### Worker Performance Metrics
- **Worker completion rate**: Percentage of assigned tasks completed successfully.
- **Worker x Capability success rate**: Success rate of a specific worker in a specific capability.
- **Cost per PR / Cost per merged PR**: Resource expenditure normalized by output.
- **Human intervention rate**: Frequency of human takeovers or escalations in agent workflows.

### Ecosystem Health Metrics
- **Conversation noise ratio**: Ratio of coordination comments to actionable content.
- **Non-durable link count**: Count of external links that lack stable system memory (e.g., transient AI sessions).
- **Collision risk**: Probability of merge conflicts based on path clustering and concurrent activity.

## Capability Scoring
Capability scoring is evidence-backed and worker-specific. Scores are derived from historical performance data in the `worker_capability_fact` and are used by Demerzel for routing decisions.
- **No opaque scores**: All scores must be traceable to specific Streeling events.
- **Confidence Calibration**: Scores include a confidence interval based on sample size and recency.
