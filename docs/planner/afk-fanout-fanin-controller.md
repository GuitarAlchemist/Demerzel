# AFK Fan-out / Fan-in Controller

Related: #568, #529, #531, #539

## Purpose

The AFK fan-out / fan-in controller governs how Demerzel launches multiple agent tasks in parallel and how it brings the resulting work back into a safe review and merge flow.

The goal is throughput without chaos: launch enough work to keep agents busy, but pause before review queues, path collisions, stale delegation markers, or workflow policy blocks overload the human/Demerzel review loop.

## Operating principles

1. GitHub remains the work control plane.
2. Fan-out is advisory and bounded.
3. Fan-in is mandatory before additional fan-out.
4. Stale delegation markers must be classified before re-delegating.
5. Workflow and policy files require explicit human override before merge.
6. No automatic merge is allowed.
7. Every batch must be explainable from issue labels, dependency edges, PR metadata, and review evidence.

## Batch state

A batch is the durable unit of fan-out.

```yaml
afk_batch:
  batch_id: sprint0-seldon-planner-001
  status: proposed|active|paused|draining|complete|halted
  created_by: human|demerzel
  max_active_jules: 3
  max_active_claude: 2
  max_open_prs_before_pause: 5
  max_workflow_path_prs: 0
  issue_selection:
    required_labels:
      - ready-for-agent
    preferred_labels:
      - worker:jules
      - routing:architecture
    excluded_labels:
      - blocked
      - human-only
  stop_conditions:
    - failed_required_check
    - workflow_policy_block
    - merge_conflict
    - duplicate_pr_detected
    - stale_delegation_marker
    - human_halt_marker
    - review_queue_saturated
  fan_in:
    review_order: critical_path_then_lowest_risk
    merge_order: dependency_order
    pause_fanout_when_open_prs_at_or_above: 5
```

## Fan-out rules

The controller may select an issue only when all of these are true:

- the issue is open;
- required labels are present;
- the issue is not blocked by dependencies;
- no active PR is already mapped to the issue;
- no active agent task is known for the issue;
- stale delegation markers have been classified;
- predicted path collisions stay below configured thresholds;
- the batch remains under provider concurrency limits.

Docs-first and architecture issues are preferred for broad Jules fan-out. Code, workflow, permission, and policy changes require lower concurrency and stronger review gates.

## Fan-in rules

Every incoming PR must be mapped back to:

- source issue;
- batch id when known;
- worker/provider;
- capability;
- touched paths;
- risk tier;
- review stage;
- merge dependencies.

Fan-in pauses fan-out when:

- open PR count reaches the batch threshold;
- more than one PR touches the same high-risk path family;
- a required check fails;
- a workflow or governance policy file changed;
- human review is explicitly requested;
- merge order cannot be determined.

## Stale delegation marker lifecycle

The controller must distinguish these states:

| State | Meaning | Action |
|---|---|---|
| active | The marker maps to an active Jules task or open PR. | Do not re-delegate. |
| complete | A PR was created and merged/closed for the issue. | Do not re-delegate unless new work is requested. |
| failed | The workflow or worker failed before task creation. | Eligible for controlled retry. |
| stale | Marker came from an obsolete workflow, wrong target branch, or missing worker task. | Eligible for controlled retry. |
| superseded | Newer issue comment or label says another worker owns the task. | Do not re-delegate without human override. |

Old markers that mention a retired target branch are stale when no active Jules task or PR exists.

## Review queue ordering

The review queue is ordered by:

1. critical path blocker PRs;
2. low-risk docs/schema PRs;
3. PRs that unblock other fan-out lanes;
4. PRs with all checks green;
5. PRs requiring human override;
6. high-risk or workflow-path PRs last unless they unblock the batch.

## Merge queue ordering

The merge queue is deterministic:

1. dependency order from the execution graph;
2. PRs with no path collisions;
3. PRs with completed reviews;
4. lower-risk PRs before higher-risk PRs;
5. workflow/governance PRs only after explicit human approval.

## Minimal viable controller

The MVP can be dry-run only:

1. read open issues and labels;
2. read open PRs and changed files;
3. classify stale delegation markers;
4. propose a fan-out set;
5. propose a fan-in review queue;
6. explain why each issue/PR is included, skipped, paused, or blocked.

## Human override points

Human approval is required for:

- launching a batch above configured concurrency;
- retrying stale markers on high-risk issues;
- merging workflow, policy, permission, or governance changes;
- resuming after a halt marker;
- closing or superseding an agent task.

## Example policy

```yaml
throughput_policy:
  normal:
    max_active_jules: 3
    max_active_claude: 2
    max_open_prs_before_pause: 5
  cautious:
    max_active_jules: 1
    max_active_claude: 1
    max_open_prs_before_pause: 2
  blocked_paths:
    - .github/workflows/**
    - policies/**
    - constitutions/**
```

## Next implementation steps

- Add batch examples under `examples/planner/`.
- Add a dry-run planner command that produces a proposed batch state.
- Add stale-marker classification rules to the Jules delegation workflow or a companion planner script.
- Add fan-in review queue reporting to Mission Control.
