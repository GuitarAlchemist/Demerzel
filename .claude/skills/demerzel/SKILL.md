---
name: demerzel
description: Demerzel governance coordinator — dispatcher for all governance subcommands (audit, recon, directive, promote, evolve, teach, loop, patterns, confidence, drive)
---

# Demerzel Governance Coordinator

Demerzel is the governance coordinator for the GuitarAlchemist ecosystem. Use these subcommands to invoke governance functions.

## Subcommands

| Command | Skill | Purpose |
|---------|-------|---------|
| `/demerzel audit` | `demerzel-audit` | Run governance audit (Level 1/2/3) |
| `/demerzel recon` | `demerzel-recon` | Execute reconnaissance on a repo |
| `/demerzel directive` | `demerzel-directive` | Issue a governance directive |
| `/demerzel promote` | `demerzel-promote` | Propose a governance promotion |
| `/demerzel evolve` | `demerzel-evolve` | Show governance evolution insights |
| `/demerzel teach` | `demerzel-teach` | Invoke Seldon for knowledge transfer |
| `/demerzel loop` | `demerzel-loop` | Start/monitor a governed Ralph Loop |
| `/demerzel patterns` | `demerzel-patterns` | Consult the agentic patterns catalog |
| `/demerzel confidence` | `demerzel-confidence` | Calibrate a confidence score |
| `/demerzel drive` | `demerzel-drive` | Autonomous driver — full cycle or individual phases across all repos |
| `/demerzel team` | `demerzel-team` | Spawn, monitor, pause, and dissolve governance agent teams |

## Quick Reference

- **Constitution:** `constitutions/asimov.constitution.md` (root, Articles 0-5) + `constitutions/default.constitution.md` (Articles 1-11)
- **Mandate:** `constitutions/demerzel-mandate.md` (who enforces the laws)
- **Harm taxonomy:** `constitutions/harm-taxonomy.md` (what counts as harm)

## Precedence Hierarchy

```
asimov.constitution.md        (root — Laws of Robotics)
  ├─ demerzel-mandate.md      (who enforces)
  └─ default.constitution.md  (operational ethics)
       └─ policies/*.yaml     (operational rules)
            └─ personas/*.persona.yaml  (behavioral profiles)
```

## Source
`constitutions/`, `policies/`, `personas/`, `contracts/galactic-protocol.md`
