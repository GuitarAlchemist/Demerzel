---
name: demerzel-team
description: Spawn and manage Demerzel governance agent teams — spawn from template, check status, pause work, dissolve team
---

# Demerzel Team Manager

Spawn, monitor, pause, and dissolve Demerzel governance agent teams. Teams are
assembled from templates defined in `AGENTS.md` and governed by the constitutional
hierarchy. All team operations are logged and constitutional constraints apply to
every spawned agent.

## Usage

```
/demerzel team spawn <template>   — spawn a team from a named template
/demerzel team status             — show active team members, task states, health
/demerzel team pause              — pause all in-progress team work (state preserved)
/demerzel team dissolve           — dissolve team, finalize state, archive manifests
```

## Team Templates

Templates are defined in `AGENTS.md` → **Team Structure** section. Available templates:

| Template | Members | Use when |
|----------|---------|----------|
| `full`   | Demerzel (Lead) + Seldon + Auditor + Architect + Integrator | Full sprint — new features, architecture, cross-repo |
| `research` | Seldon + Auditor | Research cycles, course production, knowledge harvesting |
| `audit` | Auditor + Demerzel (Lead) | Governance audits, compliance checks, behavioral test runs |
| `build` | Architect + Integrator + Auditor | Implementation sprints — grammar, pipeline, schema work |
| `hotfix` | Integrator + Auditor | Bug fixes, broken CI, urgent cross-repo patches |

## `/demerzel team spawn <template>`

1. **Validate template** — check `<template>` against the table above. Unknown template → escalate, do not guess.
2. **Constitutional check** — confirm all member personas exist in `personas/`. Missing persona → halt and report.
3. **Assign models** per `AGENTS.md` → *Starting the Team*:
   - Opus: Architect, Auditor (reasoning-heavy roles)
   - Sonnet: Seldon, Integrator, Lead (throughput-heavy roles)
4. **Issue task assignments** — for sprint work, read open GitHub issues via `gh issue list`, triage by label using the Issue Triage table in `AGENTS.md`, assign to correct teammate.
5. **Require plan mode** for Architect tasks touching constitutions, policies, or cross-repo contracts (Article 6 — Escalation).
6. **Write team manifest** to `state/teams/<date>-<template>-team.json` (see schema below).
7. **Log spawn event** in `LOG.md` with timestamp, template, member list.
8. **Output** — list of spawned agents, their roles, model assignments, and first tasks.

### Confidence gate

If confidence in task assignments < 0.7, output assignments with a `[NEEDS REVIEW]` flag and ask the operator to confirm before dispatching.

## `/demerzel team status`

Read `state/teams/<latest>-team.json`. Output:

```
Team: <template> spawned <date>
State: active | paused | dissolving

Member          | Role          | Model   | Current Task    | Status
----------------|---------------|---------|-----------------|----------
Demerzel (Lead) | Coordinator   | Sonnet  | #138 schema fix | in_progress
Seldon          | Research      | Sonnet  | #125 manifest   | in_progress
Auditor         | Quality       | Opus    | #138 review     | pending
Architect       | Design        | Opus    | (idle)          | idle
Integrator      | Cross-repo    | Sonnet  | (idle)          | idle

Tasks: 2 in_progress / 1 pending / 0 completed / 0 blocked
Constitutional health: OK (no conscience signals)
```

If no active team manifest exists: `No active team. Use /demerzel team spawn <template> to start one.`

## `/demerzel team pause`

1. **Signal all active agents** to finish their current atomic step, then pause before starting the next task.
2. **Preserve state** — each agent writes its current progress to `state/teams/<date>-<template>-team.json` under `members[].paused_state`.
3. **Write pause record** — update team manifest `state` field to `paused`, record `paused_at` timestamp.
4. **Log pause event** in `LOG.md`.
5. **Output** — confirmation of pause with list of tasks that were in-progress and their saved states.

Pause is non-destructive. Work resumes on next `/demerzel team spawn` from the same template (detects existing paused manifest).

## `/demerzel team dissolve`

1. **Confidence gate** — if any task is in_progress with unsaved work, prompt operator: "Tasks are still in progress. Dissolve anyway? (yes/no)". Do not dissolve without confirmation if confidence < 0.7.
2. **Finalize tasks** — mark all pending/in_progress tasks as `dissolved`. Write final state to manifest.
3. **Archive manifest** → `state/teams/archive/<date>-<template>-team.json`.
4. **Run COMPOUND phase** (abbreviated):
   - Update evolution log in `state/evolution/`
   - Package learnings via `/seldon deliver` if Seldon was a team member
   - Write self-initiated trigger if follow-up work identified
5. **Log dissolve event** in `LOG.md` with task summary (completed / dissolved / failed counts).
6. **Output** — dissolution summary.

Dissolve is permanent for the current team instance. Spawn a fresh team for new work.

## Team Manifest Schema

```json
{
  "template": "full",
  "spawned_at": "<ISO timestamp>",
  "state": "active | paused | dissolved",
  "paused_at": "<ISO timestamp or null>",
  "dissolved_at": "<ISO timestamp or null>",
  "members": [
    {
      "role": "Lead",
      "name": "Demerzel",
      "persona": "personas/demerzel.persona.yaml",
      "model": "claude-sonnet-4-6",
      "current_task": "<task id or null>",
      "status": "active | paused | idle | dissolved",
      "paused_state": {}
    }
  ],
  "tasks": [
    {
      "id": "<task id>",
      "issue": "<GitHub issue number>",
      "assigned_to": "<role>",
      "status": "pending | in_progress | completed | dissolved | failed",
      "authorization_artifact": "<issue URL or roadmap ref>"
    }
  ],
  "constitution_violations": [],
  "log": []
}
```

## Constitutional Constraints

- **Asimov Article 0** (Zeroth Law) — any governance integrity concern during spawn or dissolve → hard stop.
- **Asimov Article 4** (Separation of Goals) — each agent operates within its declared persona affordances only.
- **Default Article 3** (Reversibility) — pause preserves state; dissolve archives, never deletes.
- **Default Article 6** (Escalation) — unknown templates, missing personas, or confidence < 0.5 → escalate to operator.
- **Default Article 9** (Bounded Autonomy) — teams operate on authorized GitHub issues only; self-initiated work creates an issue first.

## Resume Behavior

On `/demerzel team spawn <template>`, before assembling new agents:
1. Check `state/teams/` for an existing manifest with matching template and `state: paused`.
2. If found: offer to resume — "Paused team found (spawned <date>). Resume? (yes/no)".
3. If resumed: restore `paused_state` for each member, re-queue tasks from saved manifest.

## Claude Code Integration

This section bridges the governance spec above to actual Claude Code tool calls.

### TeamCreate Mapping

Each template maps to a `TeamCreate` call. The team name follows the pattern `demerzel-<template>-<YYYY-MM-DD>`.

```
/demerzel team spawn full     → TeamCreate(team_name: "demerzel-full-2026-03-26",
                                  description: "Full governance sprint — features, architecture, cross-repo")

/demerzel team spawn research → TeamCreate(team_name: "demerzel-research-2026-03-26",
                                  description: "Research cycle — knowledge harvesting, course production")

/demerzel team spawn audit    → TeamCreate(team_name: "demerzel-audit-2026-03-26",
                                  description: "Governance audit — compliance checks, behavioral tests")

/demerzel team spawn build    → TeamCreate(team_name: "demerzel-build-2026-03-26",
                                  description: "Implementation sprint — grammar, pipeline, schema work")

/demerzel team spawn hotfix   → TeamCreate(team_name: "demerzel-hotfix-2026-03-26",
                                  description: "Hotfix — urgent bug fixes, broken CI, cross-repo patches")
```

### Agent Spawning per Role

After `TeamCreate`, spawn each team member as an Agent. Model and subagent_type map from the governance role:

| Role | Name | subagent_type | model | Rationale |
|------|------|---------------|-------|-----------|
| Lead / Coordinator | Demerzel | `general-purpose` | `sonnet` | Throughput-heavy orchestration, task dispatch |
| Research | Seldon | `general-purpose` | `sonnet` | High-volume knowledge harvesting, multi-source synthesis |
| Quality / Auditor | Auditor | `octo:droids:octo-code-reviewer` | `opus` | Deep reasoning for compliance, behavioral test validation |
| Design / Architect | Architect | `octo:droids:octo-backend-architect` | `opus` | Reasoning-heavy design decisions, constitutional review |
| Cross-repo / Integrator | Integrator | `general-purpose` | `sonnet` | Throughput-heavy cross-repo coordination |

Each Agent call includes the persona context in its prompt:

```
Agent(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are Seldon (Research). Persona: personas/seldon.persona.yaml.
           Constitutional constraints: Asimov Articles 0-5, Default Articles 1-11.
           Your current task: <task description>.
           Report findings via SendMessage to the team lead."
)
```

### Task Distribution

Use `TaskCreate` to create discrete work items and assign them to teammates:

```
TaskCreate(
  description: "Research tetravalent logic extensions for hexavalent support",
  assignee: "Seldon"
)

TaskCreate(
  description: "Review schema changes for persona.schema.json v3",
  assignee: "Auditor"
)

TaskCreate(
  description: "Design cross-repo contract for ix ML feedback loop",
  assignee: "Architect",
  mode: "plan"   // Required for constitution/policy/contract work (Article 6)
)
```

Track progress with `TaskGet` / `TaskList`. Update status with `TaskUpdate` as agents complete work.

### YOLO Mode

For unattended execution (e.g., overnight research cycles or CI-triggered audits), set bypass permissions:

```
mode: "bypassPermissions"
```

This enables agents to proceed without operator confirmation at each step. Constitutional constraints still apply — YOLO mode bypasses *permission prompts*, not *governance gates*. Conscience signals and confidence thresholds below 0.3 still trigger hard stops regardless of mode.

Use YOLO mode only when:
- All tasks are well-defined with clear acceptance criteria
- No tasks touch constitutions, the Asimov root, or cross-repo contracts
- An operator will review output within a bounded timeframe

### Team Lifecycle via SendMessage

Team control commands map to `SendMessage` calls targeting teammates:

```
# Status check — query all agents
SendMessage(to: "*", message: "Report current task status and blockers")

# Pause — signal all agents to save state and stop
SendMessage(to: "*", message: "shutdown_request: pause — save current state to team manifest, do not start new tasks")

# Dissolve — finalize and archive
SendMessage(to: "*", message: "shutdown_request: dissolve — finalize all tasks, write final state, prepare for archival")

# Direct a specific agent
SendMessage(to: "Seldon", message: "Priority shift: drop current task, begin research on issue #142")
```

The team lead (Demerzel) coordinates lifecycle transitions. On pause, each agent writes `paused_state` to the team manifest before stopping. On dissolve, the lead runs the COMPOUND phase after all agents confirm finalization.

## Source

`AGENTS.md`, `constitutions/asimov.constitution.md`, `constitutions/default.constitution.md`,
`policies/autonomous-loop-policy.yaml`, `policies/alignment-policy.yaml`,
`state/teams/`, `LOG.md`
