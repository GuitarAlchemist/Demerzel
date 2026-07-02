# AIW Markov and State-Space Models

**Status:** Proposed (Epic #596)
**Owner:** Seldon (Intelligence Layer)
**Scope:** Distill AI/human work history into stochastic and control-oriented models that help Demerzel understand, predict, and steer delivery.

## Overview

As Demerzel manages the AI-human Agile-XP operating model, she needs to understand which states lead to successful merges, which get stuck, and which worker/capability combinations reduce cycle time. By treating the lifecycle of issues and pull requests as a stochastic process, we can build models that predict outcomes, identify bottlenecks, and recommend control actions without relying on black-box heuristics.

This document outlines two primary approaches:
1. **Markov Chain Models** over lifecycle history to predict transition probabilities and durations.
2. **State-Space Control Models** to represent the delivery system's global state and evaluate control inputs (like fan-out backpressure modes).

## Markov Model Concepts

The Markov model represents lifecycle history as transition probabilities. The state space consists of discrete lifecycle states for issues and pull requests.

### State Space (Candidate Lifecycle States)
- `issue.grooming`
- `issue.ready`
- `issue.delegated`
- `pr.draft`
- `pr.ready_for_review`
- `pr.merge_candidate`
- `pr.merged`
- `pr.rejected` (absorbing state)
- `issue.stuck` (absorbing state)

### Model Variants
1. **Lifecycle Markov Chain:** Predicts the next state and time-to-transition for a generic issue or PR.
2. **Capability-Stream Markov Chain:** Conditioned on the worker and capability stream (e.g., Jules doing docs vs. Claude doing code).
3. **Absorbing-State Analysis:** Evaluates the probability of reaching `pr.merged` versus `pr.rejected` or `issue.stuck`.

### Example Output (Markov Transition)
```yaml
markov_transition:
  from_state: pr.draft
  to_state: pr.ready_for_review
  probability: 0.62
  median_duration_hours: 7.5
  worker: jules
  capability_stream: docs_schema
  sample_size: 42
```

## State-Space Control Concepts

The state-space model represents the entire delivery system as a state vector, with advisory control inputs derived from Seldon's intelligence pipeline.

### State Vector (Candidate Variables)
- `open_agent_prs`: Total number of agent-generated PRs currently open.
- `draft_agent_prs`: Number of agent-generated PRs in draft state.
- `review_queue_depth`: Number of PRs awaiting human or adversarial review.
- `active_jules_tasks`: Number of active assignments for worker `jules`.
- `active_claude_tasks`: Number of active assignments for worker `claude`.
- `blocked_issues`: Number of issues with stale markers or failed checks.
- `stale_markers`: Count of stale delegation or review markers.
- `failed_checks`: Count of recent CI or governance check failures.
- `fanout_mode`: Current Adaptive Fan-out Backpressure mode.

### Control Inputs (Candidate Policies)
Control inputs represent advisory actions Demerzel can take to steer the system state.
- `pause_new_feature_fanout` (boolean): Stops assigning new feature work to agents.
- `assign_claude_draft_to_ready` (boolean): Promotes draft PRs using Claude.
- `request_gemini_read_only_review` (boolean): Requests adversarial review without write permissions.
- `run_duckdb_probe` (string): Triggers a specific analytical query (e.g., `fanin.queue.saturation.v1`).

### Example Output (State-Space Vector)
```yaml
state_vector:
  open_agent_prs: 3
  draft_agent_prs: 3
  review_queue_depth: 3
  active_jules_tasks: 0
  active_claude_tasks: 0
  blocked_issues: 0
  stale_markers: 0
  failed_checks: 0
  fanout_mode: draining

control_inputs:
  pause_new_feature_fanout: true
  assign_claude_draft_to_ready: true
  request_gemini_read_only_review: true
  run_duckdb_probe: fanin.queue.saturation.v1
```

## Integration Points

These models integrate with the existing GuitarAlchemist ecosystem layers:

- **Streeling (Observe):** Immutable event streams from GitHub activity form the base data for these models (#490).
- **Seldon (Learn):** The intelligence layer that computes these models and derives advisory facts (#492).
- **DuckDB (Local Probes):** Local DuckDB SQL queries prototype the intelligence logic (#594).
- **IX (Optimize):** Local memristive-markov crates provide the underlying stochastic engine.
- **Demerzel (Decide):** The policy engine and lifecycle machines consume these models to adjust fan-out/fan-in backpressure (NORMAL / CONSTRAINED / DRAINING / HALTED) (#568, #579, #588, #592).

## Non-Goals and Constraints

To preserve the Asimov priority and safe autonomy:
- **No replacement of deterministic policy gates:** Probabilistic scoring will not override hard rules (e.g., test coverage requirements).
- **No auto-merge:** Output from these models remains strictly advisory; HITL approval is always required for merges.
- **No raw authority:** Low-confidence predictions (e.g., P < 0.5) must not drive automated control inputs.
- **Local-first MVP:** The models should rely on local data structures and DuckDB queries before considering cloud ML platforms.
- **Read-only evaluation:** The models evaluate state; they do not directly mutate GitHub state themselves.