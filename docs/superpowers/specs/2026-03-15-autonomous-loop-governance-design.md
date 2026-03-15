# Autonomous Loop Governance Design

**Date:** 2026-03-15
**Status:** Draft
**Approach:** Policy + Schema (Approach 2)

## Overview

Govern Ralph Loops (autonomous iterative development cycles) under Demerzel's constitutional authority. Ralph Loops run a worker agent repeatedly until a goal is achieved, with a reviewer evaluating each iteration. This spec defines graduated governance oversight, loop-specific review criteria, state tracking, and Demerzel-initiated governance loops.

Key Ralph Loop concepts adapted for Demerzel:
- **Worker/Reviewer** → Existing persona + estimator_pairing (generator/estimator model)
- **State persistence via files** → Existing `state/` directory convention (`state/loops/`)
- **Fresh context per iteration** → Reconnaissance rebuilds context
- **PRD-driven tasks** → Governance directives and PDCA cycles
- **Loop until done** → Governed iteration with convergence/regression/drift checks

## 1. Loop State Schema

File: `logic/loop-state.schema.json`

Tracks orchestration state of a Ralph Loop. Persisted in `state/loops/*.loop.json`.

### Fields

- `id` — unique identifier (e.g., `loop-ix-compliance-remediation-2026-03-15`)
- `goal` — what the loop is trying to accomplish
- `risk_level` — `low`, `medium`, `high`, `critical` (determined before loop starts via reconnaissance)
- `governance_mode` — `boundary-only` (low/medium risk) or `per-iteration` (high/critical risk)
- `initiator` — who started the loop: `agent` (self-initiated) or `demerzel` (governance-initiated)
- `target_repo` — ix/tars/ga
- `worker` — persona name executing the work
- `reviewer` — persona name reviewing (typically the worker's estimator_pairing)
- `max_iterations` — hard cap (default 10, absolute max 25)
- `current_iteration` — counter
- `iterations` — array of per-iteration records:
  - `number`, `started_at`, `completed_at`
  - `work_summary` — what the worker did
  - `review_decision` — `SHIP`, `REVISE`, or `HALT`
  - `review_feedback` — reviewer's notes
  - `belief_state` — tetravalent state for the iteration outcome ($ref to tetravalent-state)
  - `governance_check` — `passed`, `failed`, `skipped` (skipped only for boundary-only mode)
  - `governance_notes` — any governance concerns flagged
- `convergence`:
  - `iterations_without_progress` — counter (triggers halt if too many)
  - `max_stall_iterations` — default 3
- `outcome` — `in_progress`, `shipped`, `halted`, `escalated`
- `created_at`, `last_updated`

## 2. Autonomous Loop Policy

File: `policies/autonomous-loop-policy.yaml`

### Risk Classification

Determined before loop starts using reconnaissance Tier 3 (situational analysis):

- **Low risk:** Reversible changes, single repo, no security implications, well-defined scope. Examples: documentation updates, test additions, config adjustments.
- **Medium risk:** Reversible but significant changes, single repo, affects agent behavior. Examples: persona updates, policy refinements, code refactoring.
- **High risk:** Irreversible or cross-repo changes, security-sensitive, affects governance artifacts. Examples: schema migrations, constitutional amendments, multi-repo coordination.
- **Critical risk:** Affects governance integrity, Zeroth Law implications. Examples: loops that modify constitutions, loops that change Demerzel's own configuration. Always requires human pre-approval.

### Governance Modes

- **Boundary-only** (low/medium risk): Demerzel defines boundaries before loop starts (affordances, max iterations, scope constraints). Loop runs freely within boundaries. Governance checks at end only, unless a boundary is crossed mid-loop. Reviewer uses standard estimator review criteria.
- **Per-iteration** (high/critical risk): Every iteration passes a governance gate before the next starts. Demerzel reviews the iteration outcome, checks constitutional compliance, verifies no drift/regression. Loop pauses until governance approves continuation.

### Loop-Specific Review Criteria

Added on top of standard estimator review:

1. **Convergence check:** Is the loop making progress toward its goal? If `iterations_without_progress` exceeds `max_stall_iterations` (default 3), halt and escalate. Progress is measured by: belief state confidence increasing, tasks being completed, or reviewer marking SHIP for sub-goals.

2. **Regression check:** Did this iteration break something that a previous iteration accomplished? Compare current state against prior iteration outcomes. If regression detected, halt — don't let the loop undo its own work.

3. **Drift check:** Has the loop wandered from its original goal? Compare the current iteration's work_summary against the loop's goal statement. If the work has diverged significantly, halt and escalate — the loop may be pursuing an instrumental subgoal (Asimov Article 4 violation).

### Iteration Limits

- Default max: 10 iterations
- After reaching max: escalate to human, do not continue
- Stall limit: 3 iterations without progress → halt
- Defaults can be overridden per-loop at initiation, within policy-defined bounds (absolute cap: 25 iterations)

### Demerzel-Initiated Governance Loops

- Demerzel may initiate loops for governance-specific tasks: compliance remediation, reconnaissance-driven fixes, Kaizen improvement cycles
- Demerzel may NOT initiate loops for domain work — that's the agent's domain
- Governance loops are dispatched as standard directives via Galactic Protocol with `type: compliance-requirement` or `type: violation-remediation`, with loop parameters in `directive_content`
- Consumer repo receives the directive and executes the loop locally

### Constitutional Integration

- All loops operate under the full Asimov constitutional hierarchy
- Zeroth Law concern at any iteration → immediate halt regardless of governance mode
- Article 4 (Separation of Understanding and Goals) → drift check prevents instrumental goal development
- Article 9 of default constitution (Bounded Autonomy) → loop operates within pre-approved bounds only
- Kaizen integration: completed loops that produce improvements follow PDCA standardization; failed loops logged as experiential knowledge via Streeling

## 3. Behavioral Tests

Key scenarios for `tests/behavioral/loop-cases.md`:

1. **Low-risk loop with boundary-only governance** — Agent starts doc update loop. Risk: low. Runs 4 iterations, reviewer SHIPs. Governance check at end only.
2. **High-risk loop with per-iteration governance** — Agent starts schema migration. Risk: high. Each iteration pauses for Demerzel's governance gate.
3. **Stall detection halts stuck loop** — No progress for 3 consecutive iterations. Convergence check triggers halt and escalation.
4. **Regression detection stops self-destructive loop** — Iteration 4 breaks what iteration 2 fixed. Regression check halts immediately.
5. **Drift detection catches goal wandering** — Loop tasked with "fix 3 violations" but by iteration 5 is refactoring entire module. Drift check flags Article 4 concern.
6. **Demerzel initiates governance loop** — Demerzel sends directive to tars to remediate stale beliefs. Tars executes loop, reports via compliance report.
7. **Zeroth Law halts loop immediately** — Mid-loop, iteration discovers changes degrading governance integrity. Zeroth Law override triggers regardless of mode.

## 4. File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `logic/loop-state.schema.json` | JSON Schema for Ralph Loop state tracking |
| `policies/autonomous-loop-policy.yaml` | Governance rules for autonomous loops |
| `tests/behavioral/loop-cases.md` | Behavioral tests for governed loops |

### Modified Files

| File | Change |
|------|--------|
| `docs/architecture.md` | Add autonomous loop policy to Policies, loop state to Logic |

### Unchanged

- All existing policies, personas, constitutions, schemas, contracts
- Existing `state/` convention — loops integrate as `state/loops/*.loop.json`

### Integration Points

- **Reconnaissance → Loops:** Risk classification uses Tier 3 situational analysis
- **Kaizen → Loops:** Completed loops feed experiential knowledge; improvements follow PDCA
- **Streeling → Loops:** Failed loops become teaching material for Seldon
- **Galactic Protocol → Loops:** Demerzel-initiated loops dispatched as directives; loop state transported as learning outcomes
- **State convention → Loops:** Loop state files live in `state/loops/*.loop.json`
