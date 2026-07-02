# AIW Composite Worker Lanes

Related: #584, #579, #568, #570, #573, #487, #485, #565, #566, #567, #586

## Goal

Define composite worker lanes so AI workers can shift between compatible work types when their primary lane is idle, without violating governance, permissions, or review boundaries.

The objective is to avoid dormant lanes while keeping fan-out/fan-in controlled.

## Problem

Single-purpose lanes create idle capacity:

- Jules may be idle when fan-in is saturated and no docs-first work should be launched;
- Claude may be idle when there are no safe implementation fixes ready;
- Gemini/Codex may be idle when no formal review is requested;
- Augment may be idle when no explicit navigation task exists.

But blindly moving agents into any work type is unsafe. The system needs composite lanes with ordered fallback roles and hard forbidden actions.

## Composite lane model

Each worker should have:

- a primary role;
- secondary roles;
- forbidden roles;
- allowed modes by fan-out state;
- expected output artifacts;
- escalation/stop conditions.

### Definitions

```yaml
composite_lanes:
  jules:
    primary: docs_first_researcher
    secondary:
      - issue_groomer
      - process_drafter
      - architecture_summarizer
    forbidden:
      - merge_decider
      - secret_handler
      - high_risk_workflow_editor_without_human_review
  claude:
    primary: builder_fixer
    secondary:
      - draft_to_ready_helper
      - test_author
      - review_feedback_applier
      - lightweight_groomer
    forbidden:
      - final_merge_decider
      - self_review_approver
  gemini:
    primary: read_only_critic
    secondary:
      - architecture_reviewer
      - policy_ambiguity_reviewer
      - risk_classifier
    forbidden:
      - code_pusher
      - label_mutator
      - merge_decider
  codex:
    primary: focused_patch_helper
    secondary:
      - test_suggester
      - code_review_helper
      - alternative_implementation_proposer
    forbidden:
      - broad_architecture_owner
      - autonomous_merge_actor
  augment:
    primary: navigator
    secondary:
      - impact_mapper
      - dependency_mapper
      - path_collision_checker
      - stale_marker_investigator
    forbidden:
      - merge_decider
      - policy_override_actor
```

## Adaptive use by mode

### NORMAL

Allowed:
- primary lane work;
- small secondary work when no primary work is ready.

### CONSTRAINED

Allowed:
- grooming;
- review;
- docs-only;
- navigation;
- risk classification;
- draft-to-ready assistance.

Reduced:
- new feature work;
- broad architecture changes.

### DRAINING

Allowed:
- fan-in review;
- draft-to-ready;
- conflict/risk analysis;
- stale marker classification;
- issue grooming;
- follow-up issue creation.

Blocked:
- net-new feature work;
- broad architecture PRs;
- workflow or policy changes without explicit human review.

### HALTED

Allowed:
- diagnostics;
- human-readable recovery plans;
- read-only review.

Blocked:
- new PRs;
- state mutation;
- permission changes.

## Scheduling rule

When an agent's primary lane has no eligible work, the scheduler should search secondary roles in priority order, but only within the current adaptive fan-out mode.

The scheduler should explain:
- why the primary lane was idle;
- which secondary role was selected;
- why that role is safe in the current mode;
- what output artifact is expected;
- what stop condition applies.

## Relationship to other governance concepts

- **Relationship to #584 (non-Jules lanes):** This policy provides the structure for the different lanes described in #584, formalizing their boundaries, primary, and secondary capabilities.
- **Relationship to #579 (adaptive fan-out):** This policy operationalizes adaptive fan-out by defining exactly *what* work can happen in CONSTRAINED, DRAINING, and HALTED modes, allowing idle capacity to shift to safe review/grooming work without increasing fan-out burden.
- **Relationship to #570 (grooming gate):** Idle workers (like Jules or Claude in CONSTRAINED mode) can shift their capacity to grooming gate tasks, helping to unblock the pipeline without creating new unreviewed code.

## Limitations and MVP constraints

- Do not let composite lanes erase worker boundaries.
- Do not allow review agents to approve their own work.
- Do not bypass #579 backpressure.
- Do not use idle capacity as a reason to launch unsafe work.
- Do not grant new permissions implicitly.

*Note: The MVP of this scheduling rule remains advisory/dry-run until reviewed and explicitly promoted by Demerzel.*
