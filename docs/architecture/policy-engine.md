# Demerzel Policy Engine

This document outlines the design, boundaries, and components of the Demerzel Policy Engine, the core decision layer that enforces governance and orchestration rules across the AI workspace.

## Core Principle

```text
Rules decide the guard.
State machines enforce the lifecycle.
Events record what happened.
Humans/Demerzel own final authority.
```

## Purpose and Boundaries

The Demerzel Policy Engine evaluates structured context (events, state transitions, risk analyses) to emit **advisory decisions**.

### Boundaries
- **Lightweight:** It is not a monolithic "magic rules" engine. It maps defined conditions to standard reason codes.
- **Explicit Lifecycle:** Rules operate on explicitly defined state machines. The engine prevents state transitions that violate rules.
- **No Direct Mutation:** The MVP is strictly **advisory** and **dry-run**. It computes the "should this be allowed" output but delegates actual merging or execution to human reviewers or outer orchestration wrappers.
- **Human-in-the-Loop:** Auto-merge is strictly forbidden by project policies. The policy engine highlights risks and blocks unauthorized autonomous actions.
- **No Hidden State:** State must be explicitly tracked in the system, not implied via GitHub comment threads.

## Target Flow

```text
GitHub event
  -> normalized event
  -> lifecycle state update
  -> policy evaluation
  -> advisory decision
  -> human/Demerzel decision point
  -> optional action
  -> evidence captured
```

## Component Catalogs

### Rule Pack Catalog

Rules are logically grouped into packs to govern specific dimensions of the AI workflow:

1. **Safety & Security Pack**
   - Blocks secret leakage.
   - Enforces Asimov priority (e.g., cannot weaken constraints).
   - Blocks autonomous deployment/merge without human review.

2. **Lifecycle & Grooming Pack**
   - Enforces Definition of Ready (DoR) for issues before they can be routed to an agent.
   - Enforces Definition of Done (DoD) before PRs can be merged.
   - Ensures issues are shaped in the Pocock lane before autonomous execution.

3. **Budget & Token Economics Pack**
   - Prevents agent loops from running beyond predefined ceilings.
   - Recommends cheaper tools/models when appropriate.

4. **Review & Adversarial Pack**
   - Demands adversarial review for Tier 2/Tier 3 complexity tasks.
   - Enforces minimum conversation hygiene and halts repetitive loops.

### Reason Code Taxonomy

When the policy engine blocks or escalates an action, it provides a specific reason code to aid human review.

- `SAFE_001`: Allowed under default limits.
- `RISK_001`: High-risk file modified (e.g., constitution).
- `RISK_002`: Action blocked due to Asimov law violation.
- `RISK_003`: Auto-merge attempt blocked.
- `DOR_001`: Issue rejected for lack of shaping (Pocock lane requirement).
- `DOD_001`: PR rejected for lack of test coverage.
- `BUDGET_001`: Loop halted due to token threshold exceeded.
- `STATE_001`: Invalid lifecycle transition.
- `ESCALATE_001`: Sent to Demerzel/Human for review due to C-mass threshold > 0.3.

## Dry-run Evaluator Design (MVP)

The MVP policy evaluator operates in a dry-run mode:
1. **Input:** Receives the requested action, current state, and relevant payload (e.g., diff, agent log).
2. **Evaluation:** Evaluates the request against the active Rule Packs.
3. **Output:** Emits an **Advisory Decision** (schema: `advisory-decision.schema.json`).
4. **Action:** The system appends the decision payload as evidence and posts a summary comment to the GitHub thread. It does not automatically execute block or merge actions natively in GitHub until human intervention.

## Integration Points

The policy engine acts as the gatekeeper across several architectural areas:

- **Fan-out / Fan-in (#568):** Regulates how many concurrent tasks can be spawned and enforces rules for when fan-in merge requires human review.
- **Adaptive Backpressure (#584, #586):** Evaluates system load and HALT markers to block new issue creation or dispatch when backpressure is constrained or halted.
- **Worker Lanes (#570):** Ensures agents do not escape their assigned capability lanes (e.g., forcing a task to stay in the Karpathy exploration lane rather than executing a loop).
- **Mission Control / Supervisor (#579):** Provides the deterministic "Allow/Block/Escalate" verdict to the supervisor, keeping the supervisor logic declarative rather than imperative.
