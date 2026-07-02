# Durable GitHub Intelligence Pipeline

## Overview
The Durable GitHub Intelligence Pipeline is a organization-wide system designed to capture GitHub activity once, derive analytics from immutable event streams, and provide high-quality decision support for Demerzel. It decouples decision logic from GitHub APIs, ensuring resilience and auditability.

## Architecture Flow
1. **GitHub**: Source of activity (Issues, PRs, Comments, Workflows, etc.).
2. **Streeling**: Observability layer. Responsible for event ingestion via webhooks or polling.
3. **Immutable Event Store**: Append-only durable history of all observed GitHub events.
4. **Seldon**: Analytics layer. Derives facts, metrics, scoring, and recommendations from the event store.
5. **Demerzel**: Governance layer. Consumes Seldon facts to make advisory decisions and enforce policy.

## Integration Principles
- **Event Sourcing**: The system's state is derived from an append-only stream of events.
- **Immutability**: Once an event is recorded in the Streeling store, it is never modified.
- **Read-Only First**: Integration with GitHub uses minimum read-only permissions to reduce risk.
- **Deterministic Schema**: Events and facts follow strict schemas before any AI interpretation occurs.
- **Derived Facts**: Analytics are recalculated from the event stream rather than repeatedly parsing GitHub conversations.
- **Advisory Decisions**: Demerzel produces recommendations and reports; it does not perform auto-merges or direct mutations of GitHub state without human-in-the-loop (HITL) approval.

## GitHub App Permission Model
To maintain security and minimize blast radius, the Streeling GitHub App requires the following **read-only** permissions:

| Resource | Permission | Purpose |
|----------|------------|---------|
| Issues | Read | Capture issue creation, labels, and assignments. |
| Pull Requests | Read | Capture PR lifecycle, reviewers, and diff metadata. |
| Issue Comments | Read | Capture conversation history and bot interactions. |
| PR Reviews | Read | Capture review outcomes and iteration counts. |
| PR Review Comments | Read | Capture granular feedback on code changes. |
| Check Runs / Suites | Read | Capture CI/CD results and time-to-green. |
| Actions | Read | Capture workflow runs, jobs, and performance. |
| Contents | Read | (Optional) Access to repository files for path clustering. |
| Metadata | Read | Basic repository info (mandatory for all Apps). |

## Webhook Ingestion
The Streeling receiver handles incoming webhooks with the following strategy:
- **Signature Verification**: All payloads must be verified using the App's webhook secret.
- **Asynchronous Processing**: Responds with 202 Accepted immediately and queues the payload for processing.
- **Idempotency**: Uses the `X-GitHub-Delivery` ID to ensure events are not processed multiple times.
- **Raw Storage**: Stores the raw JSON payload reference for future reprocessing or audit.
