-- Seldon DuckDB Prototype Queries
-- Run with: duckdb -c ".read scripts/duckdb/seldon_prototypes.sql"

-- 1. Load Streeling events
CREATE TABLE IF NOT EXISTS streeling_events AS
SELECT * FROM read_json_auto('fixtures/streeling/*.jsonl');

-- 2. pr_fact: Derived from pull_request events
CREATE OR REPLACE VIEW pr_fact AS
WITH pr_events AS (
    SELECT
        (data->>'$.number')::INTEGER as pr_number,
        repository as repo,
        actor as author,
        action,
        timestamp::TIMESTAMP as ts,
        (data->>'$.lines_added')::INTEGER as added,
        (data->>'$.lines_removed')::INTEGER as removed
    FROM streeling_events
    WHERE event_type = 'pull_request'
),
pr_lifecycle AS (
    SELECT
        pr_number,
        repo,
        max(author) as author, -- Simplified for prototype
        min(CASE WHEN action = 'opened' THEN ts END) as created_at,
        max(CASE WHEN action = 'merged' THEN ts END) as merged_at,
        max(CASE WHEN action = 'closed' AND action != 'merged' THEN ts END) as closed_at,
        max(added) as lines_added,
        max(removed) as lines_removed
    FROM pr_events
    GROUP BY pr_number, repo
)
SELECT
    *,
    CASE
        WHEN merged_at IS NOT NULL THEN 'merged'
        WHEN closed_at IS NOT NULL THEN 'closed'
        ELSE 'open'
    END as state,
    date_diff('second', created_at, coalesce(merged_at, closed_at)) as cycle_time_seconds
FROM pr_lifecycle;

-- 3. review_fact: Derived from pull_request_review events
CREATE OR REPLACE VIEW review_fact AS
SELECT
    data->>'$.review_id' as review_id,
    (data->>'$.pull_request_number')::INTEGER as pr_number,
    repository as repo,
    actor as reviewer,
    timestamp::TIMESTAMP as submitted_at,
    data->>'$.state' as state
FROM streeling_events
WHERE event_type = 'pull_request_review';

-- 4. review_finding_fact: Derived from review_finding events
CREATE OR REPLACE VIEW review_finding_fact AS
SELECT
    data->>'$.finding_id' as finding_id,
    data->>'$.review_id' as review_id,
    data->>'$.category' as category,
    data->>'$.severity' as severity,
    data->>'$.file_path' as file_path,
    (data->>'$.line_number')::INTEGER as line_number
FROM streeling_events
WHERE event_type = 'review_finding';

-- 5. conversation_hygiene_fact: Derived from conversation_hygiene events
CREATE OR REPLACE VIEW conversation_hygiene_fact AS
SELECT
    data->>'$.session_id' as session_id,
    actor,
    (data->>'$.hygiene_score')::FLOAT as hygiene_score,
    (data->>'$.repetitive_comments')::INTEGER as repetitive_comments_count,
    (data->>'$.oversized_comments')::INTEGER as oversized_comments_count,
    (data->>'$.actionless_turns')::INTEGER as actionless_turns_count,
    (data->>'$.evidence_links')::INTEGER as evidence_links_count,
    timestamp::TIMESTAMP as timestamp
FROM streeling_events
WHERE event_type = 'conversation_hygiene';

-- 6. worker_capability_fact (Historical rollup from agent_session events)
CREATE OR REPLACE VIEW worker_capability_fact AS
SELECT
    actor as worker_id,
    unnest(data->'$.capabilities_used') as capability,
    count(*) as total_uses,
    sum(CASE WHEN data->>'$.status' = 'success' THEN 1 ELSE 0 END) as success_count,
    sum(CASE WHEN data->>'$.status' = 'success' THEN 1 ELSE 0 END) * 1.0 / count(*) as success_rate,
    avg((data->>'$.duration_seconds')::FLOAT) as avg_duration_seconds,
    avg((data->>'$.cost_usd')::FLOAT) as avg_cost_usd,
    max(timestamp::TIMESTAMP) as last_used_at
FROM streeling_events
WHERE event_type = 'agent_session'
GROUP BY worker_id, capability;

-- KPI Examples --

-- KPI: Mean Time to Merge (MTTM) in Hours
SELECT
    repo,
    avg(cycle_time_seconds) / 3600 as mttm_hours
FROM pr_fact
WHERE state = 'merged'
GROUP BY repo;

-- KPI: Finding Density
SELECT
    p.repo,
    count(f.finding_id) * 100.0 / sum(p.lines_added) as findings_per_100_loc
FROM pr_fact p
JOIN review_fact r ON p.pr_number = r.pr_number AND p.repo = r.repo
JOIN review_finding_fact f ON r.review_id = f.review_id
GROUP BY p.repo;
