# AFK Agent

The AFK ("away from keyboard") agent is the *implement* step of Demerzel's task
queue. It connects the existing trigger/triage queue to the existing PR review
gates.

## Contract
- **Trigger:** an open GitHub issue labelled `agent-implement`.
- **Authorization:** the issue itself (pre-authorized domain work per
  `policies/autonomous-loop-policy.yaml` → `github_issue`). Governance edits are
  always-pre-authorized governance work.
- **Execution:** `scripts/run_afk_cycle.py` (governor) → `../afk-harness`
  (sandcastle + Podman) runs headless Claude Code with
  `prompts/afk-implement.prompt.md`.
- **Output:** a branch `agent/issue-<n>` + a PR linked to the issue.
- **Review:** the existing `agent-blackbox.yml` + `cross-model-review.yml`
  workflows. Merge is council-gated: low/medium PRs may self-merge once the
  LLM council approves (see below); anything else requires a human merge.
- **First proven:** the AFK agent was first proven end-to-end on 2026-06-22.
- **Self-merge proven:** graduated council-gated self-merge went live on
  2026-06-24 (PR #388).

## Risk gating (from autonomous-loop-policy.yaml)
- `critical` (touches constitutions/policies): never implemented; agent comments
  "needs human pre-approval" and skips.
- `high`/`medium`/`low`: implemented; PR opened for review.

## Safety
- Podman sandbox: no host file damage / env exfiltration.
- HALT (`~/.demerzel/HALT-ALL`) honored before any work.
- Every action traces to the issue number (audit).

## Parallelism
The governor processes the queue concurrently (`--max-parallel`, default 3),
each agent in its own ephemeral clone of the repo so there are no git races on
the shared `.git`. The whole queue is always processed (waves of `--max-parallel`),
never truncated. `--backend local` (per-agent clone + Podman) is the default;
`--backend remote` (Vercel isolated sandboxes) is a reserved seam, not yet
implemented.

## Deferred (graduation steps)
Self-hosted Actions runner (event-driven), `--backend remote` Vercel sandboxes
(scale beyond one machine), self-merge automation, ga/ix/tars rollout, video+TTS
PR walkthroughs.
