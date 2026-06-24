---
category: agentic
date: 2026-06-22
topic: Pocock harness philosophy + AFK agents
source: sources/chats/matt-pocock-david-ondrej-agentic-workflow.md
---

# Surprises from the Pocock × Ondrej transcript

- **"Queue, not loop."** Matt explicitly deflates the Ralph-loop hype as "mostly
  nonsensical." Real AFK work is a task queue (GitHub issues + labels) with
  HITL checkpoints pushed rightward — which is exactly what
  `demerzel-driver-triggers.yml` + `demerzel-autofix.yml` already are. We were
  ~70% of the way to an AFK system without naming it.
- **Abilities leak context.** Every model-invokable skill spends context window
  on its description, every session. Procedures (user-invoked) don't. This is a
  concrete cost argument for the `demerzel-context-budget` discipline.
- **A cheaper model + better harness == a smarter model + worse harness.** "How
  do you optimize token spend? Have a codebase that's easier to change." Guardrails
  reduce the tokens an agent spends banging its head against the wall.
- **Sandbox is non-negotiable for AFK.** Un-sandboxed agents "randomly delete your
  home directory or exfiltrate env vars." Hence Docker for the AFK harness.
- **Closing advice:** delete every skill/MCP/CLAUDE.md, observe the bare agent,
  then layer back only chosen procedures.
