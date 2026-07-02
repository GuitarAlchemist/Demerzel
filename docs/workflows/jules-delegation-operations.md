# Jules delegation operations

This document records the current, practical operating model for using Google Jules on Demerzel issues.

## Current reality

Demerzel supports two Jules paths:

1. **Human-applied `jules` label** — the preferred path today.
2. **GitHub Actions API delegation** through `.github/workflows/jules-auto-delegate.yml` — available only if `JULES_API_KEY` exists as a repository Actions secret.

As of this document, the API-key path should be treated as optional. If the key is not present, the workflow logs a notice in Actions and does not comment/spam issues.

## Labels and meaning

Use these labels together:

- `ready-for-agent` — the issue is shaped enough to be offered to an agent.
- `worker:jules` — Demerzel's routing hint that Jules is an appropriate worker.
- `jules` — the human-applied Jules trigger label.

Important distinction:

- `worker:jules` is Demerzel routing metadata.
- `jules` is the Jules pickup signal and should be applied manually by a human in the GitHub UI unless the official Jules API path is known to work.

## Why manual `jules` matters

The repository has observed that labels applied by bots or automation are not a reliable Jules pickup signal. Human-applied labels are the known practical fallback.

Therefore:

- assistants and bots may prepare issues with `ready-for-agent` and `worker:jules`;
- a human should apply `jules` to actually ask Jules to pick up the issue;
- the watcher should look for a Jules PR or a workflow/delegation marker afterward.

## Safe execution order for AIW-v0.1

Recommended order:

1. #463 — Operating doctrine
2. #465 — Lane classifier
3. #467 — Matt-before-AFK readiness gate
4. #459 — Budget router and NotebookLM adapter
5. #461 — Prompt and harness engineering
6. #471 — Cherny-style loop lifecycle
7. #457 — Multi-provider architecture
8. #455 — Matt skills configuration
9. #469 — Expert synthesis enrichment
10. #473 — Roadmap / hierarchy
11. #475 — Cross-repo triage router

Apply `jules` to only one to three issues at a time. Wait for PRs and review evidence before fanning out more work.

## Operating checklist

For each issue:

1. Confirm it has `ready-for-agent`.
2. Confirm it has `worker:jules`.
3. Manually apply `jules` in GitHub UI.
4. Watch for a Jules PR.
5. Review the PR for:
   - minimal scope;
   - linked issue;
   - tests or validation evidence;
   - risk notes;
   - no secrets;
   - no governance bypass;
   - no broad refactor unless explicitly authorized.
6. Merge only through the normal Demerzel review gates.

## API workflow behavior

`.github/workflows/jules-auto-delegate.yml` listens to `ready-for-agent` and `worker:jules`, but delegates only when both labels are present.

If `JULES_API_KEY` is missing, the workflow logs a notice and exits without commenting on the issue. This prevents repeated noise while keeping the API path ready for future use.

If `JULES_API_KEY` becomes available later:

1. Add it as repository secret `JULES_API_KEY`.
2. Re-run the workflow manually with `workflow_dispatch`, or re-apply `ready-for-agent`/`worker:jules`.
3. Keep the batch size small until the behavior is verified.

## Backpressure rules

Do not send the entire AIW queue to Jules at once.

Suggested limits:

- 1 issue if it is architecture-heavy or policy-adjacent.
- 2-3 issues if they are small docs/examples with clear acceptance criteria.
- Stop if Jules opens overlapping PRs or touches the same files repeatedly.
- Stop if PRs lack validation evidence.
- Stop if cost, queue depth, or review load becomes unclear.

## Recovery

If Jules does not pick up an issue after a manual `jules` label:

1. Remove and re-apply `jules` manually.
2. Check whether a previous PR already exists.
3. Check whether the issue is too broad and split it.
4. Prefer smaller follow-up tasks over repeated relabeling.

If the API workflow posts or logs a problem:

- `JULES_API_KEY` missing: use manual `jules` label or add the secret.
- AFK halt active: resolve or expire `governance/state/afk-halt.json` first.
- duplicate marker present: check the existing PR/comment before forcing another delegation.
