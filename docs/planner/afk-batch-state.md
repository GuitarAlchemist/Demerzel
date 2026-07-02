# AFK Batch State Model

This document specifies the data model representing an AFK (Away From Keyboard) agent batch. The batch state defines constraints, backpressure limits, stop conditions, and strategies for fan-out (task dispatch) and fan-in (review and merge).

## Schema Concept

The `afk_batch` object captures a snapshot of the batch intent and constraints.

```yaml
afk_batch:
  batch_id: sprint0-seldon-planner-001
  max_active_jules: 3
  max_active_claude: 2
  max_open_prs_before_pause: 5
  allowed_issue_labels:
    - ready-for-agent
    - worker:jules
  blocked_paths:
    - .github/workflows/**
  stop_conditions:
    - failed_required_check
    - workflow_policy_block
    - merge_conflict
    - duplicate_pr_detected
    - stale_delegation_marker
    - human_halt_marker
  fan_in:
    review_order: critical_path_then_lowest_risk
    merge_order: dependency_order
    require_human_override_for_workflows: true
```

## Field Definitions

### General Batch Constraints

- **`batch_id`** (`string`): A unique identifier for this batch execution. Useful for traceability and mapping PRs back to their origin.
- **`max_active_jules`** (`integer`): Maximum number of parallel tasks delegated to Jules.
- **`max_active_claude`** (`integer`): Maximum number of parallel tasks delegated to Claude.
- **`max_open_prs_before_pause`** (`integer`): Global backpressure limit. If the total number of unmerged PRs exceeds this limit, fan-out dispatch is paused.

### Scope Constraints

- **`allowed_issue_labels`** (`list of strings`): Issues must contain at least one of these labels to be eligible for fan-out.
- **`blocked_paths`** (`list of strings`): Glob patterns defining paths that agents are strictly forbidden to modify without explicit override. Attempting to modify these paths triggers a stop condition.

### Stop Conditions

The `stop_conditions` field (`list of strings`) enumerates events that immediately pause the fan-out loop:

- `failed_required_check`: A PR failed mandatory CI tests.
- `workflow_policy_block`: An agent attempted to modify protected workflow files.
- `merge_conflict`: An open PR encountered a merge conflict.
- `duplicate_pr_detected`: Overlapping work detected across PRs.
- `stale_delegation_marker`: A previous delegation remains unfulfilled without a linked active PR.
- `human_halt_marker`: A human triggered a safety halt (e.g., creating `governance/state/afk-halt.json`).

### Fan-In Strategies

The `fan_in` object configures how PRs are processed once submitted.

- **`review_order`** (`string`): Defines the priority for human review. `critical_path_then_lowest_risk` ensures foundational elements are reviewed before peripheral features.
- **`merge_order`** (`string`): Defines the strategy for merge queuing. `dependency_order` ensures dependent components merge after their prerequisites.
- **`require_human_override_for_workflows`** (`boolean`): Strict flag preventing auto-delegated changes to CI/CD workflows without an active human override.

## State Lifecycle

1. **Initialization**: A new `afk_batch` configuration is loaded.
2. **Fan-Out**: The controller iterates eligible issues. For each issue, it checks the backpressure limit (`max_open_prs_before_pause`), verifies worker concurrency limits, and delegates.
3. **Observation**: The controller monitors active PRs against the declared `stop_conditions`.
4. **Fan-In**: When PRs arrive, the controller applies the `fan_in` strategies to organize the review queue.
5. **Termination**: The batch completes when all delegated PRs are merged or closed, or halts if a stop condition is met.
