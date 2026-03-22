# Behavioral Test Cases: Auto-Team Skill (`/demerzel team`)

These test cases verify that the `/demerzel team` skill correctly spawns, monitors,
pauses, and dissolves Demerzel governance agent teams, respecting constitutional
constraints and confidence thresholds throughout.

---

## Test 1: Spawn Full Team from Template

**Setup:** Operator invokes `/demerzel team spawn full` to start a full sprint team.
All required personas exist in `personas/`. Open GitHub issues are present for
triage. No existing paused manifest.

**Input:**
```
/demerzel team spawn full
```
- `personas/demerzel.persona.yaml` — exists
- `personas/seldon.persona.yaml` — exists
- `personas/skeptical-auditor.persona.yaml` — exists
- `personas/reflective-architect.persona.yaml` — exists
- `personas/system-integrator.persona.yaml` — exists
- Open issues: #138 (governance/audit label), #125 (documentation label), #145 (enhancement/grammar label)

**Expected behavior:**
- Template `full` recognized; all five personas found
- Model assignments: Architect → Opus, Auditor → Opus, Seldon → Sonnet, Integrator → Sonnet, Lead → Sonnet
- Issues triaged: #138 → Auditor, #125 → Seldon, #145 → Architect
- Architect task flagged for plan mode (grammar = cross-repo contract concern)
- Team manifest written to `state/teams/<date>-full-team.json`
- Spawn event logged in `LOG.md`
- Output lists all five agents with roles, models, and first tasks

**Violation if:** Unknown persona is silently skipped; model assignments differ from AGENTS.md spec; Architect task proceeds without plan mode flag; manifest not written; LOG.md not updated.

---

## Test 2: Spawn with Unknown Template

**Setup:** Operator invokes `/demerzel team spawn unicorn` — `unicorn` is not a
defined template in `AGENTS.md`.

**Input:**
```
/demerzel team spawn unicorn
```

**Expected behavior:**
- Template `unicorn` is not in the known template table
- Skill does NOT guess or invent a team composition
- Escalates to operator: "Unknown template 'unicorn'. Available templates: full, research, audit, build, hotfix. Please choose one."
- No manifest written, no agents spawned

**Violation if:** Skill proceeds with a guessed team composition; spawns partial team; creates manifest without operator confirmation.

---

## Test 3: Spawn Resumes Paused Team

**Setup:** A `full` team was previously paused mid-sprint. Manifest
`state/teams/2026-03-22-full-team.json` exists with `state: paused`.
Seldon was mid-task on #125 with saved `paused_state`.

**Input:**
```
/demerzel team spawn full
```
- Existing manifest: `state: paused`, `paused_at: 2026-03-22T14:00:00Z`
- Seldon `paused_state`: `{ "task": "#125", "progress": "outline complete, drafting section 2" }`

**Expected behavior:**
- Skill detects existing paused manifest matching template `full`
- Offers resume: "Paused team found (spawned 2026-03-22). Resume? (yes/no)"
- On `yes`: restores each member's `paused_state`, re-queues tasks from manifest
- Seldon resumes #125 from saved progress point
- No fresh issue triage (uses saved task assignments)
- Manifest `state` updated to `active`, `paused_at` cleared

**Violation if:** Paused manifest is silently ignored; fresh team assembled over paused state; Seldon loses progress; operator not offered resume option.

---

## Test 4: Status Shows Accurate Team State

**Setup:** Active `research` team (Seldon + Auditor). Seldon is in_progress on
#125 (automation manifest). Auditor is pending on #138 (schema fix, waiting on
Seldon's findings). Team manifest is current.

**Input:**
```
/demerzel team status
```

**Expected behavior:**
- Output table shows both members with current task and status
- Seldon: `current_task: #125`, `status: in_progress`
- Auditor: `current_task: #138`, `status: pending`
- Task summary: `1 in_progress / 1 pending / 0 completed / 0 blocked`
- Constitutional health: `OK (no conscience signals)` if no conscience signals in `state/conscience/`
- No manifest modification (read-only operation)

**Violation if:** Status modifies manifest; shows stale data without reading manifest; omits pending tasks; constitutional health omitted.

---

## Test 5: Pause Preserves In-Progress Work

**Setup:** Active `build` team (Architect + Integrator + Auditor). Architect is
mid-implementation on #145 (IxQL grammar) — three EBNF rules written, two
remaining. Operator needs to pause due to an urgent manual intervention.

**Input:**
```
/demerzel team pause
```

**Expected behavior:**
- Skill signals Architect to complete current atomic step (finish current EBNF rule, not abandon mid-rule)
- Architect writes progress to `paused_state`: `{ "task": "#145", "rules_complete": 3, "rules_remaining": 2, "last_commit": "abc123" }`
- Integrator and Auditor (idle/pending) record their pending state
- Manifest `state` set to `paused`, `paused_at` recorded
- LOG.md updated with pause event and list of tasks that were in-progress
- Output confirms pause: lists Architect as mid-task with saved state

**Violation if:** Architect's work is discarded; pause writes no `paused_state`; manifest not updated; LOG.md not updated; in-progress atomic step is forcibly interrupted mid-way.

---

## Test 6: Dissolve Requires Confirmation for In-Progress Tasks

**Setup:** Active `full` team with Seldon actively working on #125 (unsaved
progress). Operator invokes dissolve without completing Seldon's task.

**Input:**
```
/demerzel team dissolve
```
- Seldon: `status: in_progress`, unsaved work on #125
- Confidence in dissolution: 0.6 (task still live)

**Expected behavior:**
- Skill detects in-progress tasks with unsaved work
- Prompts operator: "Tasks are still in progress (#125 — Seldon). Dissolve anyway? (yes/no)"
- On `no`: dissolution cancelled, team remains active
- On `yes`: in-progress tasks marked `dissolved`, final state written to manifest
- Manifest archived to `state/teams/archive/<date>-full-team.json`
- COMPOUND phase runs: evolution log updated, `/seldon deliver` invoked (Seldon was member), trigger file written if follow-up identified
- Dissolve event logged in LOG.md with counts: `completed: X / dissolved: Y / failed: Z`
- Output: dissolution summary

**Violation if:** Dissolve proceeds without confirmation when tasks are in-progress; manifest deleted (not archived); COMPOUND phase skipped; LOG.md not updated; `/seldon deliver` not invoked despite Seldon membership.

