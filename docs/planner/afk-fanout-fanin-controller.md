# AFK Fan-Out / Fan-In Controller

This document outlines the policy and deterministic planner behavior for safe AFK (Away From Keyboard) agent fan-out and fan-in within the Demerzel governance framework.

## Goal

Launch multiple worker tasks in parallel without creating uncontrolled PR noise, duplicate work, stale delegation markers, merge-order hazards, or reviewer overload.

## Fan-Out Policy

The fan-out process selects open, eligible issues and delegates them to AI agents (like Jules, Claude, Codex) while adhering to strict governance policies and concurrency limits.

### Issue Selection

- **Eligibility**: Only open issues that are not explicitly blocked are eligible.
- **Allowed Labels**: Issues must possess allowed labels such as `ready-for-agent` and worker-specific routing labels (e.g., `worker:jules`).
- **Priority**: Prefer documentation-first and architecture-related tasks for Jules fan-out.
- **Collision Avoidance**: Avoid assigning issues that are likely to touch the same high-risk paths.
- **Review Queue Limits**: Do not fan out more work when the review queue is above the configured threshold.
- **Batch Intent**: Record batch intent and selected issue set for transparency and auditability.

### Concurrency and Backpressure

- Respect the maximum concurrency limit defined per worker/provider (e.g., `max_active_jules`, `max_active_claude`).
- The maximum open PR limit before pausing the fan-out must be strictly respected (e.g., `max_open_prs_before_pause`).

### Stale Delegation Markers

Delegation markers (like `<!-- jules-delegated -->`) indicate an active delegation.

- **Detection**: Detect old markers that targeted the wrong branch or originated from an obsolete workflow revision.
- **Lifecycle states**:
  - `active`: AI is currently working on the issue.
  - `completed`: PR submitted and issue ready for review/merge.
  - `failed`: AI encountered an unrecoverable error.
  - `stale`: Marker exists, but no active PR exists or AI task died.
  - `superseded`: Task overridden or re-assigned.
- **Re-delegation**: Allow safe re-delegation when a marker is `stale` and no active worker task/PR exists.

## Fan-In Policy

The fan-in process detects incoming PRs from AI workers and manages their review and merge lifecycle without manual discovery.

### PR Detection and Mapping

- Detect incoming PRs from Jules/Claude/Codex.
- Map each PR back to its source issue, batch, capability, and risk tier.

### Review Queue Prioritization

- Prioritize reviews by dependency order and critical path.
- Enforce the `review_order` strategy (e.g., `critical_path_then_lowest_risk`).
- Surface conflicts and duplicate work prior to merging.

### Merge Queue Semantics

- Enforce the `merge_order` strategy (e.g., `dependency_order`).
- **Human Override**: Certain sensitive paths (e.g., `.github/workflows/**`) require explicit human override, regardless of the AI assessment.

## Stop Conditions

Fan-out will be paused immediately upon encountering any of these conditions:

- A required CI check fails (`failed_required_check`).
- A workflow or policy violation is detected (`workflow_policy_block`).
- A merge conflict occurs (`merge_conflict`).
- Duplicate work across multiple PRs is detected (`duplicate_pr_detected`).
- Excessive stale delegation markers are present (`stale_delegation_marker`).
- A human explicitly invokes a halt marker (`human_halt_marker`).

## Architecture Relationships

The AFK fan-out/fan-in controller acts as a deterministic dispatcher above the core execution layer. It relies on and integrates with other planner components:

- **Execution Graph (#531)**: The controller utilizes the Execution Graph to resolve dependencies between tasks before dispatching work, guaranteeing that PRs are handled in a safe, logical order.
- **Parallel Scheduler (#539)**: While the controller defines the policy, constraints, and backpressure (the *rules*), the parallel scheduler is responsible for the actual runtime mechanics of launching and managing concurrent sandboxes based on these rules.

## Non-goals

- Do **not** auto-merge PRs. All PRs require Human-in-the-Loop (HITL) approval.
- Do **not** bypass workflow-path or governance policy.
- Do **not** grant new GitHub permissions to agents.
- Do **not** require paid LLM APIs to evaluate the plan.
- MVP remains advisory/dry-run until fully reviewed.
