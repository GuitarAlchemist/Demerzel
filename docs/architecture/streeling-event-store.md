# Streeling Event Store

## Overview
The Streeling Event Store is an append-only, durable repository for normalized GitHub events. It serves as the primary source of truth for all derived analytics and governance decisions.

## Storage Strategy
- **Append-Only**: Once an event is written, it is never modified or deleted.
- **Ordered Log**: Events are stored in the order they are observed, but also contain the original occurrence timestamp for chronological reconstruction.
- **Partitioning**: Events are partitioned by `org`, `repo`, and `occurred_at` (year/month/day) to facilitate efficient querying and analysis.
- **Format**: Events are stored as line-delimited JSON (JSONL) files to support streaming processing and simple append operations.

## Idempotency
To prevent duplicate event processing (e.g., from webhook retries), Streeling uses the `delivery_id` (sourced from `X-GitHub-Delivery`) as a unique constraint. Before appending a new event, the store checks if an event with the same `delivery_id` already exists.

## Data Retention and Durability
- **Durability Classes**:
    - `ephemeral`: Logs and transient states that may be purged after a period (e.g., 90 days).
    - `persistent`: Core events (PR merges, reviews, releases) that are kept indefinitely.
    - `versioned`: Artifacts that represent a snapshot in time and may have multiple versions.
- **Raw Payloads**: The original raw JSON payloads from GitHub are stored separately (e.g., in an object store) and referenced by the `raw_ref` field in the normalized event.

## Reprocessing
The use of an append-only event store allows for "time-travel" analytics. If a schema changes or a bug is found in the derivation logic, Seldon can reprocess the entire event history from the Streeling store to regenerate facts and metrics.
