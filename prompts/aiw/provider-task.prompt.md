# AIW Provider Task Prompt

## Role

You are acting as: `<provider-role>`.

You are executing one bounded AIW task under Demerzel governance.

## Task

`<one bounded task>`

## Source of truth

- Issue: `<issue-url-or-number>`
- Parent or related artifacts: `<links>`
- Current lane: `<explore|shape|loop|verify|govern>`
- Autonomy mode: `<observe|draft|patch|pr|harvest>`

## Context bundle

Use only the supplied context bundle and the allowed repository paths.

Context bundle:

- `<file-or-summary>`
- `<file-or-summary>`

Context bundle SHA: `<sha256:...>`

## Allowed scope

Allowed paths:

- `<path>`

Allowed operations:

- `<read|write-doc|write-test|write-code|run-command|open-pr>`

## Non-goals

Do not:

- broaden the issue scope;
- touch files outside the allowed paths;
- change policy, HALT, secrets, or merge authority;
- introduce broad refactors;
- use model confidence as evidence.

## Constraints

Budget:

```yaml
budget:
  tier: `<free-local|cheap-hosted|paid-agent|manual-approval>`
  max_total_tokens: `<number>`
  max_model_calls: `<number>`
  max_retries: `<number>`
  max_runner_minutes: `<number>`
  max_cost_usd: `<number>`
  approval_required_above_usd: `<number>`
```

Sandbox and access:

- Secrets: unavailable unless explicitly provided by the harness.
- Network: `<allowed|blocked|limited>`.
- Commands: only the command allowlist may be executed.

## Required process

1. Restate the bounded task.
2. Inspect only the supplied context and allowed paths.
3. Make the smallest useful change.
4. Run the required validation commands when available.
5. Stop instead of guessing when context is missing.
6. Stop instead of expanding scope.
7. Produce structured evidence.

## Required outputs

Return a structured result containing:

- summary;
- changed files;
- commands run;
- validation output;
- risk notes;
- budget notes;
- stop reason;
- next suggested action.

## Stop conditions

Stop immediately when:

- required context is missing;
- allowed paths are insufficient;
- tests fail repeatedly without new information;
- budget cap would be exceeded;
- risk escalates to high or critical;
- policy, HALT, secrets, or merge authority is involved;
- the requested task is not in the `loop` lane for `patch` or `pr` autonomy.
