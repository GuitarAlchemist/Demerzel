---
Status: Proposed / DRAFT
Version: 0.1.0
Date: 2026-07-02
Owner: Demerzel
---

# Multi-Provider AI Workforce Orchestration

Related: #455, #457

## Goal

Design a cheap, GitHub-centered workflow that can put multiple AI coding systems to work without coupling Demerzel to one vendor or one machine.

Target worker types:

- Claude Code CLI local sessions
- Claude Code remote/cloud sessions where available
- OpenAI Codex local/CLI/app/cloud-delegated workflows
- Google Jules GitHub/cloud tasks
- Gemini CLI and/or Gemini CLI GitHub Action
- Google Antigravity or similar multi-agent IDE surfaces
- Ollama local models on the developer machine
- Optional cloud-hosted local-model workers when the home machine is offline
- Existing Augment Code / diffusion-style code editing workflows, where they can be wrapped as bounded workers

GitHub should remain the coordination backbone: issues, labels, PRs, checks, workflow runs, artifacts, comments, and audit files.

## Why

The desired workflow is not one giant privileged agent. It should be a controlled AI workforce:

1. GitHub issues describe authorized work.
2. Demerzel classifies the task, risk, provider fit, runner requirement, and cost tier.
3. A provider adapter starts the right worker.
4. The worker runs in a bounded workspace/sandbox.
5. The worker returns evidence: branch/PR, diff summary, tests, logs, cost estimate, and review notes.
6. Demerzel gates decide whether the output can advance.

This lets the best available AI help with each task while keeping auditability, cost control, and local/cloud fallback.

## Architecture

### 1. GitHub as the Control Plane

Canonical state should live in GitHub:

- **Issues** = task contracts and authorization trace
- **Labels** = provider/risk/routing hints
- **PRs** = implementation output
- **Checks** = executable validation
- **Actions artifacts** = logs, summaries, structured result JSON
- **Comments** = human/council review decisions
- **Docs** = long-lived workflow design

### 2. Demerzel Dispatcher

Add or design a dispatcher layer that reads eligible GitHub issues and emits a normalized job spec.

Example job spec (see `schemas/aiw-job.schema.json`):

```yaml
job_id: aiw-0001
issue: 123
repo: GuitarAlchemist/Demerzel
risk: low|medium|high|critical
afk_eligible: true|false
provider_candidates:
  - claude-code-local
  - codex-cloud
  - gemini-cli-action
  - ollama-local
runner_requirement:
  os: windows|wsl|linux|any
  needs_gpu: false
  needs_network: limited
  needs_browser: false
cost_tier: free|cheap|paid|manual-approval
sandbox: podman|windows-vm|wsl-worktree|cloud-vm|none
allowed_paths:
  - scripts/
  - docs/workflows/
test_commands:
  - python -m unittest discover -s scripts -p 'test_*.py'
outputs_required:
  - branch_or_pr
  - test_log
  - summary
  - risk_notes
  - cost_notes
```

### 3. Provider Adapters

Each AI system should have a thin adapter with the same contract:

- `capabilities.json` — what the worker can do
- `invoke` — start task
- `status` — report progress
- `collect` — gather diff/logs/result
- `cancel` — stop task
- `cost` — estimate or record usage
- `safety` — sandbox and permission notes

Provider adapters should not own policy. They only execute bounded jobs. Demerzel owns routing and gates.

### 4. Runner Tiers

Use a tiered execution model:

#### Tier A — Local Preferred

When the developer machine is on:

- Windows self-hosted runner for Windows-specific tasks
- WSL self-hosted runner for Linux-style tooling
- Ollama local models for cheap analysis, triage, summarization, and first-pass review
- Podman or isolated worktrees for sandboxing

#### Tier B — GitHub-Hosted Fallback

When the local machine is off or unsuitable:

- Standard Ubuntu/Windows GitHub-hosted runners for lightweight tests and docs
- Larger runners only when explicitly justified
- No GPU unless the issue says GPU is required

#### Tier C — Provider Cloud Workers

For longer or higher-quality agent work:

- Claude Code remote/cloud
- Codex cloud-delegated tasks
- Jules cloud tasks
- Gemini CLI GitHub Action
- Antigravity-managed workflows, if exportable back to GitHub

### 5. Sandboxing Model

Prefer sandboxing in this order:

1. Disposable worktree + no secrets for low-risk docs/tests.
2. Podman container for Linux-compatible tasks.
3. WSL sandbox/worktree for local Linux tasks.
4. Windows VM for Windows-specific tasks or risky file operations.
5. Cloud VM only when local machine is offline or clean isolation is required.

Never give broad host access to an agent by default. Each job should declare paths, commands, network access, and expected outputs.

### 6. Cost Control

Add explicit cost routing (see #459 for more details on budget routing):

- `free-local`: Ollama/local scripts/static analysis
- `cheap-hosted`: standard GitHub-hosted runners
- `paid-agent`: Claude/Codex/Jules/Gemini cloud work
- `manual-approval`: expensive, GPU, long-running, or broad-scope jobs

Default strategy:

1. Use local/free analysis first.
2. Use cloud only when quality, isolation, or offline availability justifies it.
3. Record provider, runner, elapsed time, token/task estimate, and result quality.

## Relationship with Matt Pocock Skills

This orchestration layers onto the Matt Pocock skills (#455). Specifically, Matt Pocock skills (e.g. `/to-issues`, `/to-prd`, `/tdd`) are used by an agent or human to **shape** vague work into strict, deterministic job specs (Demerzel Dispatcher inputs) that have explicit acceptance criteria.

Once shaped, the issue flows through the dispatcher, which routes the work to the appropriate runner/sandbox/provider combo described above.

## Non-goals

- Do not create a single all-powerful agent account.
- Do not allow workers to self-assign unlimited scope.
- Do not bypass Demerzel HALT, council, checks, or review gates.
- Do not store secrets in artifacts, logs, prompts, or generated docs.
- Do not require expensive cloud runners for default work.
- Do not depend on one vendor as the only execution path.
