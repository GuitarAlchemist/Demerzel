# Seldon KPI Catalog v1

This catalog defines the Key Performance Indicators (KPIs) derived from Seldon facts, which are themselves derived from immutable Streeling events.

## 1. Velocity & Cycle Time
*   **Mean Time to Merge (MTTM):** Average time from PR creation to merge.
    *   *Formula:* `avg(pr_fact.merged_at - pr_fact.created_at)`
    *   *Source:* `pr_fact`
*   **Lead Time:** Time from first commit (or PR creation) to production deployment.
*   **PR Throughput:** Number of PRs merged per unit of time (e.g., weekly).
    *   *Source:* `pr_fact`

## 2. Engineering Quality (CI & Review)
*   **CI Success Rate:** Ratio of successful CI runs to total runs.
    *   *Source:* `pr_fact.ci_status`
*   **Review Coverage:** Percentage of PRs with at least one human or agent review.
    *   *Source:* `pr_fact.review_count`, `review_fact`
*   **Finding Density:** Average number of review findings per PR or per 100 LOC.
    *   *Source:* `review_finding_fact`, `pr_fact.lines_added`
*   **Rejection Rate:** Percentage of PRs that receive "Changes Requested" or are closed without merging.
    *   *Source:* `review_fact.state`, `pr_fact.state`

## 3. Worker Intelligence & Capability
*   **Capability Success Rate:** Success rate of a worker (agent/human) for a specific capability.
    *   *Source:* `worker_capability_fact.success_rate`
*   **Cost per Success:** Average cost incurred for a successful task completion using a specific capability.
    *   *Source:* `worker_capability_fact.avg_cost_usd`
*   **Worker Latency:** Average duration for a worker to complete a session using specific capabilities.
    *   *Source:* `worker_capability_fact.avg_duration_seconds`

## 4. Conversation Hygiene
*   **Hygiene Score:** Composite metric based on conversation quality signals.
    *   *Source:* `conversation_hygiene_fact.hygiene_score`
*   **Repetitive Noise Index:** Frequency of repetitive bot comments in a session.
    *   *Source:* `conversation_hygiene_fact.repetitive_comments_count`
*   **Actionless Turn Ratio:** Ratio of turns with no concrete tool use or observation to total turns.
    *   *Source:* `conversation_hygiene_fact.actionless_turns_count`

## 5. Cost & Efficiency
*   **Total Spend:** Aggregate USD spend by repo, actor, or model.
    *   *Source:* `worker_capability_fact.avg_cost_usd` * `total_uses`
*   **ROI per Feature:** (Estimated Value / Cost) - *Experimental*
