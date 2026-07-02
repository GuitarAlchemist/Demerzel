# GitHub Intelligence Pipeline Child Stories

This document decomposes the Durable GitHub Intelligence Pipeline epic into actionable child stories.

## Streeling: Observation and Ingestion

### [Story][Streeling][P0] Implement Normalized GitHub Event Schema v1
- **Goal**: Implement the `engineering-event.schema.json` in the Streeling ingestion service.
- **Tasks**:
    - Port schema to service-specific language (e.g., Rust/TypeScript).
    - Add validation logic for incoming payloads.

### [Story][Streeling][P0] Design Read-Only GitHub App and Webhook Model
- **Goal**: Configure a GitHub App with minimal permissions and set up a secure webhook receiver.
- **Tasks**:
    - Define manifest for the GitHub App.
    - Implement webhook signature verification.
    - Implement async queuing for webhook payloads.

### [Story][Streeling][P0] Build Dry-Run GitHub Event Collector
- **Goal**: Create a tool to backfill the event store from existing GitHub activity.
- **Tasks**:
    - Implement polling for recent Issues, PRs, and Workflows.
    - Transform raw GitHub API responses into normalized `engineering-event` records.

### [Story][Streeling][P0] Build Immutable Local Event Store Prototype
- **Goal**: Implement a basic version of the append-only event store using local JSONL files.
- **Tasks**:
    - Implement append-only writer with `delivery_id` de-duplication.
    - Organize storage by repo/date.

### [Story][Streeling][P1] Add Workflow Artifact Strategy for Durable Evidence
- **Goal**: Standardize how workflows export durable evidence to Streeling.
- **Tasks**:
    - Define a standard JSON schema for workflow evidence artifacts.
    - Update CI workflows to export these artifacts.

### [Story][Streeling][P1] Build Conversation Hygiene Detector
- **Goal**: Implement logic to identify noise and non-durable evidence in GitHub conversations.
- **Tasks**:
    - Implement noise scoring logic.
    - Detect non-durable (external) links without durable summaries.

## Seldon: Learning and Analytics

### [Story][Seldon][P0] Implement Derived Fact Model
- **Goal**: Implement the logic to generate facts (`pr_fact`, `review_fact`, etc.) from Streeling events.
- **Tasks**:
    - Create a batch processing job to consume Streeling JSONL files.
    - Generate and store derived facts.

### [Story][Seldon][P0] Build KPI Summarizer
- **Goal**: Compute high-level metrics (latency, failure rates, etc.) from Streeling events.
- **Tasks**:
    - Implement aggregations for defined KPIs.
    - Produce periodic repository health reports.

### [Story][Seldon][P1] Build Capability Scoring v1
- **Goal**: Implement evidence-backed capability scoring for workers.
- **Tasks**:
    - Map Streeling actions to capabilities.
    - Compute success/failure rates and reliability scores per worker/capability.

### [Story][Seldon][P1] Build Review Effectiveness Report
- **Goal**: Analyze the quality of PR reviews and their impact on code health.
- **Tasks**:
    - Correlate `review_finding_fact` with subsequent activity.
    - Identify high-impact vs. low-impact review patterns.

## Demerzel: Decision and Governance

### [Story][Demerzel][P0] Implement Advisory Decision Reporter
- **Goal**: Create a service that consumes Seldon facts and emits `advisory-decision` records.
- **Tasks**:
    - Implement the `advisory-decision.schema.json`.
    - Create a reporter that posts recommendations as GitHub comments or labels.

### [Story][Demerzel][P1] Implement Routing Recommendations
- **Goal**: Use worker capability scores to suggest the best worker for a given task.
- **Tasks**:
    - Integrate Seldon capability scores into the routing logic.
    - Emit `route` advisory decisions for new issues/PRs.
