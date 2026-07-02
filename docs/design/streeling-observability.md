# Streeling Engineering Observability Platform

## Overview
Streeling is the engineering observability platform for the GuitarAlchemist Harness. Its primary responsibility is to observe, collect, and normalize signals from the ecosystem. It does not decide, route, merge, or optimize—it provides the evidence layer for Demerzel (governance) and Seldon (learning).

## Scope

### 1. GitHub Event Ingestion
Capture and normalize events from GitHub:
- Issues: opened, closed, labeled, commented.
- Pull Requests: opened, updated, closed, merged.
- Commits: pushed.
- Reviews: submitted, comments created.
- Bot activity: comments from agents (Claude, Jules, Gemini, etc.).

### 2. CI/Workflow Telemetry
Capture metadata and status from GitHub Actions and other CI pipelines:
- Workflow name, run ID, status, conclusion, duration.
- Association with PRs and commits.
- Failure/success state and retry counts.
- Identification of merge-blocking vs. advisory checks.

### 3. Agent Activity Timeline
Maintain a unified timeline of activity for all workers (human and AI):
- Normalized activity stream across Claude, Jules, Gemini, Codex, Augment, and GitHub Actions.
- Historical context for agent collaboration quality.

### 4. Cost Telemetry
Capture visible cost signals:
- Token spend and model/provider used.
- Estimated USD cost and runner minutes.
- Markers for paid API vs. free/local execution.

### 5. Collision Detection
Track active work to detect potential conflicts:
- Overlap in repository, branch, issue, or PR.
- File/path cluster analysis to identify agents touching the same files.
- Worker identity and capability tracking.

### 6. Conversation Hygiene Metrics
Measure the quality and signal/noise ratio of ecosystem communication:
- Bot comment density per PR.
- Detection of non-durable or broken external links.
- Identification of duplicate or non-actionable status comments.

## Supervisor Event Feed Contract
Streeling exposes a normalized feed to Demerzel. Every event in the feed follows the `engineering-event` schema:

```yaml
event:
  id: string
  observed_at: timestamp
  source: github|workflow|agent|manual
  repo: string
  issue_or_pr: string
  actor: string
  worker: claude|jules|gemini|codex|augment|github-actions|human|unknown
  capability: implementation|research|review|observability|unknown
  event_type: issue|pr|comment|review|workflow|status|cost|collision
  severity: info|action_needed|blocked|risk|success
  durable_url: string
  summary: string
  raw_ref: string
```

## Implementation Strategy (Tracer Bullet)
The initial implementation focuses on a dry-run collector that:
1. Reads recent PR/issue/workflow metadata from the GitHub API (or local mocks).
2. Maps raw data to the normalized engineering event schema.
3. Emits JSON records for ingestion by the Supervisor.

## Cost & Bootstrapping Notes
- **Free Tier First:** Use GitHub APIs (Issues, PRs, Actions) which are available within the free tier for public/local repos.
- **Local Storage:** Store normalized events as JSONL in the `state/streeling/` directory to avoid external database dependencies during the bootstrap phase.
- **No LLM Required:** Streeling's normalization logic should be deterministic and not require calling paid LLM APIs for the base observation layer.

## Responsibility Split
- **Streeling:** Observe and normalize.
- **Seldon:** Learn from normalized signals.
- **Demerzel:** Decide based on evidence.
- **IX:** Optimize execution.
- **Human:** Architect and final authority.
