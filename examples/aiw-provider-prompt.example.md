# Example AIW Provider Prompt

## Role

You are acting as: `docs-worker`.

You are executing one bounded AIW task under Demerzel governance.

## Task

Add a documentation-only clarification to the AIW budget router.

## Source of truth

- Issue: `#461`
- Related artifacts:
  - `docs/workflows/aiw-budget-router.md`
  - `docs/workflows/aiw-matt-readiness-gate.md`
- Current lane: `loop`
- Autonomy mode: `draft`

## Context bundle

- `docs/workflows/aiw-budget-router.md`
- `docs/workflows/aiw-matt-readiness-gate.md`
- `docs/workflows/aiw-prompt-harness-engineering.md`

Context bundle SHA: `sha256:example-context-bundle`

## Allowed scope

Allowed paths:

- `docs/workflows/`
- `examples/`

Allowed operations:

- `read`
- `write-doc`
- `run-command`

## Non-goals

Do not:

- change runtime code;
- change policy or HALT behavior;
- create or modify secrets;
- open a merge decision;
- expand beyond documentation and examples.

## Constraints

```yaml
budget:
  tier: free-local
  max_total_tokens: 50000
  max_model_calls: 2
  max_retries: 0
  max_runner_minutes: 10
  max_cost_usd: 0.00
  approval_required_above_usd: 1.00
```

Network: `blocked`.
Commands:

- `pwsh scripts/verify.ps1`

## Required process

1. Confirm the requested change is docs-only.
2. Edit only the allowed paths.
3. Keep the patch small.
4. Run `pwsh scripts/verify.ps1` or stop with a clear reason if the harness cannot run it.
5. Produce a diff summary, validation evidence, and risk notes.
6. Stop if the change requires runtime code or governance authority.

## Required outputs

- diff summary;
- changed files;
- validation command and result;
- risk notes;
- stop reason.

## Stop conditions

Stop if:

- the issue asks for runtime implementation;
- policy or HALT changes are needed;
- files outside allowed paths are required;
- validation cannot be run or explained;
- a secret or credential is needed;
- budget would exceed the cap.
