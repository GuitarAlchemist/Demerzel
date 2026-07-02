# Planner Issue Grooming Gate

Version: 1.0.0
Status: Draft

## Goal

Add an issue grooming gate before AFK fan-out so Demerzel can decide whether an issue is ready to delegate, needs refinement, should be split, should be blocked, or should be routed to a different worker/capability.

## Problem

High throughput requires better issue hygiene. Some issues are broad epics, some are docs-first stories, some are implementation tasks, and some contain risky workflow, permission, or governance changes.

Without a grooming gate:
- Broad issues may be delegated before they are sliced into reviewable work.
- Stale delegation markers can hide failed or obsolete attempts.
- Worker labels can be correct but the issue can still lack enough paths, tests, output expectations, or stop conditions.
- Fan-out can overload fan-in because review complexity is not estimated first.
- Issues that need human clarification can be sent to agents too early.

## Grooming Decisions

The gate evaluates candidate issues and classifies them into one of the following decisions:

- `ready_to_delegate`: The issue is fully defined and safe for autonomous execution.
- `needs_scope_split`: The issue is too broad (e.g., an epic) and must be broken down.
- `needs_acceptance_criteria`: Missing clear, verifiable criteria for success.
- `needs_allowed_paths`: Missing definitions of what files or systems the agent is allowed to touch.
- `needs_test_plan`: Missing a plan for how the agent or reviewer will verify the change.
- `needs_risk_review`: The issue touches sensitive paths, workflows, or governance and requires explicit human approval.
- `blocked_by_dependency`: The issue depends on other incomplete work.
- `blocked_by_policy`: The issue violates Asimov or other governance policies.
- `stale_delegation_needs_retry`: A previous delegation failed or timed out and requires intervention.
- `human_clarification_required`: Ambiguous instructions that require human input before proceeding.

## Required Issue Signals

The grooming gate checks the issue for the following required signals:

- **Clear Goal**: A plain-language summary of what is to be achieved.
- **Deliverables**: The concrete artifacts expected to be produced or modified.
- **Acceptance Criteria**: Verifiable conditions that must be met.
- **Suggested Routing or Capability**: Which worker or capability lane is expected.
- **Expected Output Artifacts**: The specific artifacts (code, docs, config) the worker should generate.
- **Likely Touched Paths or Path Families**: Scope boundaries to prevent unintended modifications.
- **Dependency Links**: Explicit `#issue_id` links to dependent or blocking work.
- **Risk Tier**: Estimation of change risk.
- **Review Requirements**: Specific instructions on how the fan-in controller or reviewers should inspect the result.
- **Stop Conditions**: Defined limits (time, cost, scope) where the worker must halt.
- **Stale or Active Delegation Markers**: History of previous agent assignments.
- **Existing PRs**: Any linked PRs that indicate work is already in flight.

## Labels

The following labels facilitate the grooming state machine:

- `needs:grooming`: Needs review by the gate.
- `needs:split`: Classified as needing a scope split.
- `needs:acceptance-criteria`: Classified as needing criteria.
- `needs:allowed-paths`: Classified as missing allowed paths.
- `needs:test-plan`: Classified as needing a test plan.
- `groomed`: Successfully passed grooming and ready for fan-out.
- `batch:candidate`: Picked up by the planner for potential execution.
- `batch:paused`: Execution temporarily halted.

## Fan-Out Integration

The fan-out controller relies on the grooming gate for deterministic routing.

- The fan-out controller **must only** select issues that are explicitly labeled `groomed`, OR
- The fan-out controller **must only** select issues that pass the deterministic grooming check in a dynamic dry-run mode.

Issues failing the grooming check will not be delegated. They will be returned to the backlog with a short, actionable automated comment detailing the failure reason and the corresponding `needs:*` label.

## Fan-In Integration

Observations made during the fan-in phase (PR review and merge) must feedback into the grooming knowledge base.

When PRs return, the fan-in process checks for:
- **Issue too broad**: Review was impossible because the PR was too large.
- **Missing tests**: The agent could not verify their own work.
- **Unclear acceptance criteria**: The PR did not solve the actual human intent.
- **Path collision discovered**: The agent modified unexpected files.
- **Wrong worker selected**: The task required a capability the agent did not have.
- **Stale delegation marker detected**: The PR was generated from an outdated context.
- **Follow-up issue needed**: The work revealed further necessary tasks.

These signals are logged and used to improve the stringency or heuristics of future grooming decisions.

## Implementation Details

The MVP version of the grooming gate operates as an advisory dry-run checker. It evaluates the issue JSON structure and produces a decision payload (see `examples/planner/issue-grooming-decision.example.json`) without performing automatic mutations or requiring expensive models.
