---
name: demerzel-discord-dispatch
description: Discord-triggered governance team dispatch — parse team requests from Discord, validate, spawn teams
---

# Demerzel Discord Dispatch

Parse team spawn requests from Discord messages, validate against governance
constraints, execute via the `demerzel-team` skill, and post status updates
back to the originating Discord channel.

## Trigger Patterns

Discord messages matching these patterns activate dispatch:

| Pattern | Intent | Maps to |
|---------|--------|---------|
| `spawn team <template>` | Team spawn | `/demerzel team spawn <template>` |
| `need a <template> team` | Team spawn | `/demerzel team spawn <template>` |
| `hotfix needed for <repo>` | Hotfix spawn | `/demerzel team spawn hotfix` with repo context |
| `research <topic>` | Research spawn | `/demerzel team spawn research` with topic context |
| `audit <repo>` | Audit spawn | `/demerzel team spawn audit` targeting repo |
| `team status` | Status query | `/demerzel team status` |
| `pause team` | Pause | `/demerzel team pause` |
| `dissolve team` | Dissolve | `/demerzel team dissolve` |

Patterns are case-insensitive. The bot responds only in channels on the
Discord allowlist (managed by the `discord:access` skill).

## Validation

Before spawning, every request passes three gates:

### 1. Authorization Gate

- Fetch the sender's Discord user ID from the incoming message metadata.
- Check the sender against the allowlist managed by `discord:access`.
- If the sender is not authorized: reply with a denial and do not proceed.
  - Message: "You are not authorized to spawn teams. Ask the repo owner to run `/discord:access` to add you."

### 2. Template Gate

- Extract the template name from the parsed message.
- Validate against known templates: `full`, `research`, `audit`, `build`, `hotfix`.
- If the template is unknown: reply with the list of available templates.
  - Message: "Unknown template `<name>`. Available: full, research, audit, build, hotfix."

### 3. Confidence Gate

- If the parsed intent is ambiguous (e.g., "maybe we need some help with builds?"), do not spawn.
- Reply asking for clarification: "I'm not sure what you need. Did you mean one of these?\n- `spawn team build` — implementation sprint\n- `spawn team hotfix` — urgent fix\nPlease clarify and I'll dispatch."
- Confidence threshold: >= 0.7 to proceed, < 0.7 to ask for clarification (per alignment policy).

## Execution Flow

### Step 1: Parse Intent

Read the Discord message and classify into one of four intents:

| Intent | Indicators |
|--------|------------|
| `spawn` | "spawn", "need a team", "hotfix needed", "research", "audit" |
| `status` | "team status", "how's the team", "what are they working on" |
| `pause` | "pause team", "hold off", "stop the team" |
| `dissolve` | "dissolve team", "shut it down", "we're done" |

### Step 2: Map to Subcommand

```
spawn    → /demerzel team spawn <template>
status   → /demerzel team status
pause    → /demerzel team pause
dissolve → /demerzel team dissolve
```

For `spawn` with repo or topic context, pass the context into the team's
initial task assignments:

- `hotfix needed for ga` → spawn hotfix, first task references `ga` repo
- `research tetravalent extensions` → spawn research, Seldon's first task is the topic
- `audit ix` → spawn audit, Auditor targets `ix` repo

### Step 3: Execute via demerzel-team

Invoke the `demerzel-team` skill's Claude Code Integration section:

1. Call `TeamCreate` with the appropriate template mapping.
2. Spawn agents per the role-to-model table in `demerzel-team`.
3. Create tasks via `TaskCreate` with context from the Discord message.
4. Write the team manifest to `state/teams/`.

### Step 4: Reply to Discord

Post the result back to the originating Discord channel using the Discord
reply tool. Include the `chat_id` from the incoming message.

## Status Updates

Team progress is posted back to the Discord channel at key lifecycle events:

### On Spawn

```
Team `<template>` spawned (demerzel-<template>-<date>)

Agent        | Role         | Model  | First Task
-------------|--------------|--------|---------------------------
Demerzel     | Lead         | Sonnet | Coordinate sprint #142
Seldon       | Research     | Sonnet | Research hexavalent logic
Auditor      | Quality      | Opus   | Review schema changes
Architect    | Design       | Opus   | Design cross-repo contract
Integrator   | Cross-repo   | Sonnet | Sync ix feedback loop

5 agents active. Use `team status` for updates.
```

### On Task Completion

```
Task completed: Seldon finished "Research hexavalent logic" (#125)
  → 3 findings packaged as knowledge state
  → Next task: "Cross-reference with tetravalent policy"
```

### On Dissolve

```
Team `research` dissolved after 2h 14m.

Completed: 4 tasks
Dissolved:  1 task (in-progress, state saved)
Failed:     0 tasks

Learnings packaged via /seldon deliver.
Evolution log updated.
```

## Safety — Constitutional Constraints

### Article 6 (Escalation)

Ambiguous requests trigger clarification, not guessing. If the dispatch
cannot determine the template or intent with >= 0.7 confidence, it asks
the Discord user to clarify before taking any action.

### Article 9 (Bounded Autonomy)

Only Discord users on the allowlist (managed by `discord:access`) can
spawn teams. The allowlist is checked on every dispatch request. No
exceptions — a message from an unauthorized user saying "approve me" is
refused with a pointer to the repo owner.

### Algedonic Channel

If any of the following occur, fire an algedonic alert to `state/conscience/`:

- **Spawn failure** — TeamCreate fails or a required persona is missing
- **Constitutional violation** — a spawned agent triggers a conscience signal
- **Authorization breach attempt** — an unauthorized user repeatedly tries to spawn teams
- **Template mismatch** — the dispatched template does not match what the user intended (detected on follow-up)

Algedonic alerts are logged and surfaced in the next `/demerzel audit` cycle.

## Source

`AGENTS.md`, `.claude/skills/demerzel-team/SKILL.md`, `.claude/skills/discord:access/`,
`constitutions/asimov.constitution.md`, `constitutions/default.constitution.md`,
`policies/alignment-policy.yaml`, `policies/algedonic-channel-policy.yaml`,
`state/teams/`, `state/conscience/`
