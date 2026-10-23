---
category: agentic
date: 2026-07-28
topic: Decision not to install JetBrains Air for the Demerzel repo
source: user question — https://air.dev/
---

# Decision: Do not install JetBrains Air for Demerzel

## Context

On 2026-07-28 the owner asked whether to install https://air.dev/ (JetBrains Air) for the Demerzel repo. Air is an agentic development environment that lets multiple coding agents (Claude, Codex, Gemini CLI, Junie, and ACP-compatible agents) run independent tasks in parallel via isolated worktrees or Docker containers.

## Evaluation

Air's value proposition — parallel agent execution, isolated worktrees, and cross-agent review — is strong for large implementation projects with many moving parts. However, the Demerzel repo is a governance-only framework: constitutions, policies, personas, schemas, state files, and CI harnesses. It has no runtime code, no services, and no complex build pipeline.

The repo already defines its own multi-agent workflow in `AGENTS.md` (Demerzel, Seldon, Architect, Auditor, Integrator) and consumes it through Augment/Claude Code skills and sub-agents. Adding Air would introduce a second, external orchestration layer whose model-role mappings do not align with the documented Demerzel team structure.

## Decision

**Do not install JetBrains Air in the Demerzel repo.**

Continue using the existing agentic stack: Augment/Claude Code for the session interface, the Demerzel skill set for governance-specific commands, and the Demerzel team roles from `AGENTS.md` for multi-agent work.

## Rationale

1. **Prefer-existing-tooling doctrine.** `docs/methodology/aiw-operating-doctrine.md` and `docs/methodology/continuous-improvement.md` favor compounding existing tools over adding new ones unless the new tool removes a bottleneck that current tooling cannot address. Demerzel's governance tasks are sequential and deliberative; parallel agent execution is not a bottleneck here.
2. **Single source of truth for roles.** `AGENTS.md` maps work to Architect (Opus), Auditor (Opus), Seldon (Sonnet), and Integrator (Sonnet). Air's generic agent model does not preserve these governance-specific constraints.
3. **No runtime code to orchestrate.** Air's isolated worktrees and Docker environments are designed for concurrent code changes. Demerzel's changes are surgical edits to schemas, policies, and state files; concurrent editing would increase merge risk without increasing throughput.
4. **Preview product overhead.** Air is in public preview and requires a JetBrains AI subscription or provider API keys. Adopting a preview tool for a governance repo would add credential, update, and compatibility maintenance without commensurate value.
5. **Scope discipline.** The recent governance audit (2026-07-25) surfaced drift precisely because the repo has strong schema and policy boundaries. Adding an external agent runner would widen the seam between "how Demerzel governs" and "how work is executed," making future audits harder.

## Consequences

- The Demerzel repo keeps its current agentic workflow.
- If parallel implementation work is needed across sibling repos (`../ix/`, `../tars/`, `../ga/`), Air can be re-evaluated for one of those runtime repos rather than for Demerzel.
- A new tool should only be proposed if it can be justified under the same prefer-existing-tooling and governance-audit standards used here.

## References

- `AGENTS.md` — Demerzel team structure and LLM-role mapping
- `docs/methodology/aiw-operating-doctrine.md` — prefer-existing-tooling rule
- `docs/methodology/continuous-improvement.md` — compounding over replacement
- `state/snapshots/2026-07-25-audit-level2.snapshot.json` — recent finding that motivated tighter schema/policy alignment
