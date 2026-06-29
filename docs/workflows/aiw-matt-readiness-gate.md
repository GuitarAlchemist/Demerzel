# AIW Matt-before-AFK Readiness Gate

Related: #463, #465, #467, `docs/workflows/aiw-operating-doctrine.md`, `docs/workflows/aiw-lane-classifier.md`.

## Purpose

AFK implementation is only allowed after the issue has been shaped into a small, testable, bounded slice.

This gate turns the Pocock lane into an explicit readiness check before any issue can move to `loop` or AFK `patch` / `pr` mode.

## Required readiness block

```yaml
matt_readiness:
  vertical_slice: true
  shared_language: true
  allowed_paths:
    - docs/workflows/
  non_goals:
    - no policy changes
    - no broad refactor
  test_commands:
    - python scripts/validate_governance.py
  tdd_required: false
  evidence_required:
    - diff_summary
    - validation_log
    - risk_notes
  stop_conditions:
    - missing_context
    - repeated_validation_failure
    - budget_exceeded
    - risk_escalation
  afk_ready: true
```

## Minimum fields for AFK readiness

`afk_ready: true` requires:

- a single vertical slice;
- allowed paths;
- explicit non-goals;
- at least one validation or test command;
- evidence requirements;
- stop conditions;
- a budget cap or explicit low-cost constraint;
- no high or critical governance risk.

## Gate behavior

When readiness fails:

- keep or move the issue to `aiw/lane/shape`;
- do not invoke implementation agents;
- allow only observe, draft, triage, or issue-shaping work;
- request clarification or split the issue.

When readiness passes:

- the issue may move to `aiw/lane/loop`;
- a harnessed worker may produce a branch or PR;
- budget, risk, HALT, and review gates still apply.

## Blocking rules

AFK `patch` and `pr` modes are blocked when:

- no test or validation command is present;
- allowed paths are missing;
- non-goals are missing;
- stop conditions are missing;
- the issue touches policy, constitution, secrets, HALT, merge authority, or high/critical risk;
- the issue is classified as `explore`, `shape`, `verify`, or `govern` instead of `loop`.

## Passing example

```yaml
aiw_classification:
  lane: loop
  afk_eligible: true
matt_readiness:
  vertical_slice: true
  shared_language: true
  allowed_paths:
    - docs/workflows/
  non_goals:
    - no runtime code
  test_commands:
    - python scripts/validate_governance.py
  evidence_required:
    - diff_summary
    - validation_log
  stop_conditions:
    - missing_context
    - validation_failure
  afk_ready: true
```

## Failing example

```yaml
aiw_classification:
  lane: shape
  afk_eligible: false
matt_readiness:
  vertical_slice: false
  allowed_paths: []
  test_commands: []
  non_goals: []
  stop_conditions:
    - missing_context
  afk_ready: false
  reason: "missing scope, allowed paths, non-goals, and validation command"
```

## Non-goals

- This gate does not invoke providers.
- This gate does not approve merges.
- This gate does not override Demerzel risk or HALT authority.
- This gate does not make high-risk work autonomous.
