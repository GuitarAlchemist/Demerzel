# Adaptive Fan-out Backpressure Policy

## Goal

Add an adaptive fan-out policy so Demerzel can keep throughput high without overloading fan-in review.

The controller should not treat fan-out as simply on/off. When fan-in blocks, it should reduce high-risk/new-work fan-out and redirect capacity toward grooming, review, draft-to-ready work, dependency analysis, and small docs-only tasks.

## Problem

After the first controlled fan-out, multiple draft PRs were produced (e.g., #565, #566, #567). While this proves the worker path is alive, it creates a fan-in bottleneck. If Demerzel keeps launching new work while draft PRs accumulate, human review and merge ordering become the limiting constraint.

## Adaptive Modes

The controller supports these modes based on backpressure thresholds:

### NORMAL
Use when the review queue is healthy.
- **Allowed work:** docs, schemas, low-risk implementation, small architecture updates.

### CONSTRAINED
Use when open PRs or active drafts approach the threshold.
- **Allowed work:** grooming, review, docs-only issues, dependency analysis, risk classification.
- **Blocked or reduced work:** broad feature PRs, high-risk path changes, workflow/policy changes without human approval.

### DRAINING
Use when fan-in is saturated.
- **Allowed work:** fan-in review, draft-to-ready work, conflict analysis, stale-marker classification, issue grooming, follow-up issue creation.
- **Blocked work:** new feature PRs, broad architecture PRs, workflow changes, permission/policy changes.

### HALTED
Use when a hard stop condition is present.
- **Examples:** workflow/policy block, repeated failed required checks, merge conflicts across several PRs, human halt marker, unsafe or ambiguous automation change.
- **Allowed work:** human review only, diagnostic notes, explicit recovery plan.

## Required Behavior

- Compute current mode from open PR count, draft count, failed checks, path risk, merge conflicts, and human markers.
- Reduce fan-out type before reducing fan-out to zero.
- Prefer grooming/review/docs-only work while fan-in is blocked.
- Pause new implementation work when the review queue is saturated.
- Resume normal fan-out only after fan-in drains below threshold.
- Explain why each issue is selected, delayed, or blocked.

## Fan-in Interaction

When fan-in blocks, the controller should generate one of:
- review queue recommendation;
- draft-to-ready recommendation;
- conflict/risk analysis recommendation;
- grooming batch recommendation;
- halt/recovery recommendation.

## Relationship to other components

- **Fan-out/fan-in controller (#568):** This adaptive policy provides the intelligence for the controller to regulate its dispatcher loop instead of a simple binary on/off switch.
- **Grooming gate (#570):** Redirects excess capacity during backpressure toward grooming the backlog.

## Non-goals

- Do not auto-merge PRs.
- Do not bypass human review.
- Do not launch additional high-risk work when review is saturated.
- Do not treat all PRs as equal; draft PRs, workflow PRs, and policy PRs carry different risk.
