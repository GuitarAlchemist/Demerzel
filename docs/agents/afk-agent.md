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
  workflows. Merge is human/gate-decided (self-merge automation deferred).
- **First proven:** the AFK agent was first proven end-to-end on 2026-06-22.

## Risk gating (from autonomous-loop-policy.yaml)
- `critical` (touches constitutions/policies): never implemented; agent comments
  "needs human pre-approval" and skips.
- `high`/`medium`/`low`: implemented; PR opened for review.

## Safety
- Podman sandbox: no host file damage / env exfiltration.
- HALT (`~/.demerzel/HALT-ALL`) honored before any work.
- Every action traces to the issue number (audit).

## Deferred (graduation steps)
Self-hosted Actions runner (event-driven), parallel sandboxes, self-merge
automation, ga/ix/tars rollout, video+TTS PR walkthroughs.
