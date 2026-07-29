# AFK Backend Adapter Contract

**Date:** 2026-07-29  
**Status:** Proposed / design complete, awaiting implementation  
**Related:** #872, #873, #471, #863, #776

## Problem

`scripts/run_afk_cycle.py` today hardcodes three invocation paths:

- `claude-code` — headless `claude -p` on the subscription
- `local` — Podman sandcastle running `../afk-harness/.sandcastle/main.mts`
- `remote` — a stub that returns "not implemented"

Each path is wired directly into `_process_issue`, with branching logic for whether the backend needs a local clone, how it prepares the environment, and how it maps to the AIW budget provider. Adding a new tool (e.g., GitHub Copilot CLI, JetBrains AI, a cloud OpenAI worker) means editing the governor and adding more branches. That is the opposite of tool-agnostic.

## Goal

Make the AFK governor backend-agnostic. Any AI tool that can implement a GitHub issue and return a branch with commits should be pluggable through a small adapter module, with no changes to the governor. The same backend abstraction should work for:

- **desktop tools** (local CLI, IDE agent, container) that run on this host;
- **cloud tools** (remote sandbox, API endpoint, serverless worker) that do not need a local clone.

## Decision

Introduce an abstract `AFKBackend` contract in `scripts/afk_backends/__init__.py` and load concrete adapters through a registry in `config/afk-backends.yaml`. The governor calls every adapter through the same methods.

### Contract

```python
class AFKBackend(ABC):
    @abstractmethod
    def prepare(self) -> tuple[bool, str]: ...
    @abstractmethod
    def needs_local_repo(self) -> bool: ...
    @abstractmethod
    def invoke(self, issue: dict, repo_path: str | None) -> dict: ...
    @abstractmethod
    def estimate_cost(self, issue: dict) -> dict: ...
    def cancel(self) -> None: ...
```

### Return shape of `invoke`

Every adapter returns the same dict, which the governor already understands:

```python
{
  "branch": str | None,
  "commits": list[str],
  "blocked": str | None,
}
```

This is the same shape produced by the sandcastle harness and the headless Claude Code path today. The governor's push/PR/loop-state logic remains unchanged.

### `needs_local_repo`

- **True** for desktop/container backends: the governor prepares an ephemeral clone, checks out a branch, and passes the path.
- **False** for cloud backends: the adapter receives `repo_path=None` and may pass the GitHub origin URL to the worker instead.

### `prepare`

Called once per cycle before any issue is processed. It is the adapter's responsibility to check prerequisites such as:

- the CLI tool is installed;
- Podman machine is running;
- the cloud endpoint is reachable;
- required credentials are present.

A failed `prepare` aborts the whole cycle deterministically, before any budget is spent.

### `estimate_cost`

Used by the AIW budget gate to reserve budget before invocation. The adapter returns a dict with recognized keys such as `estimated_cost_usd`, `estimated_total_tokens`, `estimated_runner_minutes`. The budget gate already parses these from the issue body; the adapter's estimate can supplement or override them.

### Registry mapping

A declarative registry file will map backend names to adapter classes, execution mode, and budget provider:

```yaml
backends:
  claude-code:
    adapter: scripts.afk_backends.claude_code.ClaudeCodeBackend
    execution_mode: desktop
    provider: claude-code-cli
  local:
    adapter: scripts.afk_backends.sandcastle.SandcastleBackend
    execution_mode: desktop
    provider: anthropic-api
  remote:
    adapter: scripts.afk_backends.remote.RemoteBackend
    execution_mode: cloud
    provider: cloud-worker
```

This removes the hardcoded `BACKEND_PROVIDER` dict from `run_afk_cycle.py` and fixes the spend-attribution bug in #863 at the config/policy layer.

## Consequences

- **Pros:** New tools are added without touching the governor. Cloud and desktop backends share the same governance path. The budget provider mapping is visible and version-controlled.
- **Cons:** A small amount of upfront refactoring is required before the first new tool is added. The registry adds a new file to validate and maintain.

## First steps

1. Land the contract in `scripts/afk_backends/__init__.py` (#872).
2. Extract the existing `claude-code` and `local` paths into adapter modules (#873).
3. Add the registry loader and `config/afk-backends.yaml` (#875).
4. Fix the `local` backend provider mapping to close #863 (#877).
5. Implement the `remote` cloud-worker adapter (#879).
6. Add a generic `shell` adapter as proof of abstraction (#882).
7. Update docs and policy (#884).
