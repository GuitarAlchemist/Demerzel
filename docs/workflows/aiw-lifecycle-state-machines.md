# AIW Lifecycle State Machines

This document outlines the explicit lifecycle state machines for AI Worker (AIW) entities across the Demerzel ecosystem. These state machines provide stable, deterministic state inputs for policy evaluation, preventing "hidden state" that relies purely on unstructured conversation or LLM context.

## Guiding Principles

1. **Explicit over Implicit:** If an AI worker is doing work, the state of that work must be explicitly represented in a tracked state machine.
2. **Deterministic Inputs:** The Demerzel Policy Engine uses these states to evaluate transitions.
3. **No Hidden State:** We do not rely on "reading the GitHub comments" to know what stage of work an agent is in.
4. **Hexavalent alignment:** States should be clearly categorizable or evaluate cleanly within our governance frameworks.

## 1. Issue Lifecycle

The Issue lifecycle tracks the progression of an idea from creation to being shaped and ready for work, to completion.

**Valid States:**
- `raw`: Newly created, unshaped issue.
- `shaping`: Currently being defined in the Pocock lane (clarifying constraints, acceptance criteria).
- `ready`: Shaped, meets Definition of Ready (DoR), waiting for a worker assignment.
- `in_progress`: Assigned to a worker, actively being executed.
- `blocked`: Execution halted (e.g., due to missing information or a policy violation).
- `resolved`: Completed and verified, related PRs merged.
- `closed_wontfix`: Rejected or abandoned.

**Allowed Transitions:**
- `raw` -> `shaping`, `closed_wontfix`
- `shaping` -> `ready`, `closed_wontfix`
- `ready` -> `in_progress`, `blocked`, `closed_wontfix`
- `in_progress` -> `blocked`, `resolved`
- `blocked` -> `in_progress`, `closed_wontfix`

## 2. Pull Request (PR) Lifecycle

The PR lifecycle manages the validation and review of code changes proposed by an AI worker.

**Valid States:**
- `draft`: Code is being written, not ready for review.
- `verifying`: Running CI/CD, tests, and automated policy checks.
- `in_review`: Undergoing human or adversarial AI review.
- `changes_requested`: Reviewers found issues; sent back to the worker.
- `approved`: Review passed, meets Definition of Done (DoD).
- `merged`: Merged into the target branch.
- `closed_unmerged`: Rejected or abandoned.

**Allowed Transitions:**
- `draft` -> `verifying`, `closed_unmerged`
- `verifying` -> `in_review`, `draft` (if checks fail)
- `in_review` -> `changes_requested`, `approved`
- `changes_requested` -> `draft`, `verifying`
- `approved` -> `merged`, `closed_unmerged`

## 3. WorkPackage / Task Lifecycle

WorkPackages define the granular chunks of work assigned to specific AI capabilities.

**Valid States:**
- `pending`: Task created, not yet started.
- `dispatched`: Sent to an AI worker or sub-agent.
- `executing`: Worker is actively processing the task.
- `yielding`: Worker paused to ask for human input or missing context.
- `completed`: Worker finished the task successfully.
- `failed`: Worker encountered an unrecoverable error.
- `halted`: Task forcibly stopped by policy or Demerzel supervisor.

**Allowed Transitions:**
- `pending` -> `dispatched`
- `dispatched` -> `executing`, `failed`
- `executing` -> `yielding`, `completed`, `failed`, `halted`
- `yielding` -> `executing`, `halted`

## 4. Review Lifecycle

The Review state machine tracks the adversarial or human review process for a specific artifact or PR.

**Valid States:**
- `unassigned`: Review required but no reviewer selected.
- `assigned`: Sent to a reviewer (human or AI).
- `auditing`: Actively being reviewed.
- `commented`: Feedback provided, but no definitive verdict yet.
- `request_changes`: Definitively rejected until changes are made.
- `approved`: Definitively approved.

**Allowed Transitions:**
- `unassigned` -> `assigned`
- `assigned` -> `auditing`
- `auditing` -> `commented`, `request_changes`, `approved`
- `commented` -> `auditing`, `request_changes`, `approved`

## 5. Execution Episode (Agent Loop) Lifecycle

An Execution Episode tracks the micro-lifecycle of a single Cherny-lane agent loop (e.g., plan -> execute -> verify).

**Valid States:**
- `initializing`: Setting up context and tools.
- `planning`: Deriving a plan from the task.
- `acting`: Executing tool calls or writing code.
- `observing`: Evaluating the results of the actions.
- `reflecting`: Comparing observations against the goal.
- `success`: Loop achieved goal.
- `budget_exhausted`: Loop stopped due to token/cost limits.
- `max_iterations_reached`: Loop stopped to prevent runaway recursion.

**Allowed Transitions:**
- `initializing` -> `planning`
- `planning` -> `acting`
- `acting` -> `observing`
- `observing` -> `reflecting`
- `reflecting` -> `success`, `planning` (re-plan), `budget_exhausted`, `max_iterations_reached`
