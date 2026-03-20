# Demerzel Autonomous Driver — Design Spec

**Date:** 2026-03-19
**Status:** Approved
**Version:** 1.0.0

## Summary

Demerzel becomes a fully autonomous product driver across all 4 repos (Demerzel, ix, tars, ga). She monitors, initiates, plans, and executes work — from governance maintenance to feature implementation — governed by her constitution, confidence thresholds, and conscience signals. Humans are notified, not asked, except for critical-risk changes.

## Requirements

- **Full autonomy**: Demerzel initiates work unprompted based on roadmap, issues, governance health, and self-identified opportunities
- **All trigger types**: scheduled (cron cadence), event-driven (GitHub webhooks), and self-initiated
- **Risk-tiered delivery**: direct push for low-risk, PRs for medium+, human approval for critical only
- **Parallel cross-repo coordination**: independent tasks run concurrently, dependency-ordered tasks are sequenced
- **No new infrastructure**: runs through Claude Code sessions, GitHub Actions, and the file system

## Article 4 Authorization Model

Asimov Article 4 prohibits Demerzel from developing instrumental goals beyond those explicitly authorized. The autonomous driver reconciles this through **pre-authorization artifacts**:

- **Roadmap items** (GitHub Project board) — human-created work items constitute explicit authorization for domain work. Demerzel may pick up, plan, and execute any roadmap item without further approval.
- **Open issues** (GitHub Issues) — human-created issues are explicit task authorization. Demerzel may self-assign and execute.
- **Governance work** — always pre-authorized per the autonomous-loop policy. Demerzel may initiate governance maintenance, recon, compliance remediation, and kaizen without any human-created artifact.
- **Self-identified domain work** — when Demerzel identifies domain opportunities not covered by an existing issue or roadmap item (e.g., "this code could use a new MCP tool"), she MUST first create a GitHub Issue describing the work and rationale. This issue becomes the authorization artifact. She may then self-assign and execute it. This preserves auditability (Article 7) and ensures every domain action traces to an explicit authorization.

This means Demerzel never acts on implicit goals — every action traces to either a human-created artifact (roadmap/issue) or a self-created issue that documents her reasoning before execution.

## Architecture

### Core Driver Loop

Each autonomous cycle follows this flow:

```
WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP
```

1. **WAKE** — Triggered by schedule, event (trigger file in `state/triggers/`), or self-initiated follow-up. First checks `state/driver/lock.json` — if a cycle is already running (lock exists and is < 6 hours old), skip this WAKE. Otherwise, acquires lock and loads state from `state/` directory to rebuild context.

2. **RECON** — Three-tier reconnaissance across all repos per `reconnaissance-policy.yaml`:
   - Tier 1: Constitutional integrity, policy coverage, persona validity, belief currency
   - Tier 2: Repo state, change detection, ungoverned components, failing CI, open issues
   - Tier 3: Knowledge requirements, assumption audit, blind spots, confidence assessment
   - Produces a **situation report**.

3. **PLAN** — Reads situation report + roadmap + open issues. Prioritizes work using confidence thresholds and constitutional alignment. Produces a **work manifest** — a list of tasks with:
   - Repo assignment
   - Risk classification (low/medium/high/critical)
   - Dependency ordering (DAG)
   - Delivery method (direct push vs PR)
   - Rollback plan

4. **EXECUTE** — Dispatches parallel worktree agents per repo for independent tasks. Blocks downstream work on upstream dependencies. Each agent operates under autonomous-loop policy constraints (iteration limits, stall/regression/drift checks).

5. **VERIFY** — Runs tests, checks CI, validates governance artifacts, confirms no constitutional violations. Failed verification triggers rollback.

6. **COMPOUND** — Meta-compounding cycle: update evolution log, promote/demote artifacts per the Galactic Protocol's Governance Promotion staircase (pattern → policy → constitutional article), package learnings via Seldon, identify follow-up work.

7. **PERSIST** — Write updated beliefs, PDCA state, loop state, conscience signals, and cycle manifest back to `state/`. Commit and push.

8. **SLEEP** — Release lock (`state/driver/lock.json`). Log cycle summary. If follow-up work identified, write self-initiated trigger file for next WAKE.

### Trigger System

#### Scheduled Triggers
- **Continuous driver**: Every 4 hours during work hours (configurable via `state/driver/schedule.json`)
- **Daily harvest**: Once daily (existing `streeling-daily.yml`), knowledge harvesting + conscience digest
- **Weekly deep cycle**: Sunday, full meta-compounding + roadmap reassessment + governance experimentation evaluation

#### Event Triggers
GitHub Actions workflows detect events and write trigger files to `state/triggers/`:
- Push to any repo → recon that repo, check governance sync
- Issue opened/reopened → triage, assess if Demerzel should self-assign
- CI failure → diagnose, attempt fix
- Dependabot PR → assess risk, merge or escalate
- Discussion created → respond if governance-related
- Submodule drift → detected via existing `submodule-notify.yml`

Trigger file format:
```json
{
  "type": "ci_failure",
  "repo": "ix",
  "ref": "main",
  "priority": "high",
  "details": { "workflow": "ci.yml", "run_id": 12345, "error": "..." },
  "timestamp": "2026-03-19T10:00:00Z"
}
```

The driver consumes and deletes trigger files on WAKE.

**Trigger hygiene:**
- Maximum queue depth: 50 triggers. If exceeded, lowest-priority triggers are pruned first.
- Staleness: triggers older than 72 hours are discarded with a log entry (the underlying issue likely evolved).
- Deduplication: triggers with the same `type` + `repo` + `ref` are merged, keeping the most recent.

#### Self-Initiated Triggers
During any cycle, if Demerzel identifies follow-up work, she writes a trigger file for herself with priority and rationale. Next WAKE picks it up.

### Risk Classification & Delivery

| Risk | Examples | Delivery | Governance Mode |
|------|----------|----------|-----------------|
| **Low** | Belief updates, wiki sync, submodule bumps, formatting, doc fixes | Direct push to main | Boundary-only |
| **Medium** | Dependency updates, dependabot merges, test additions, lint fixes, CI config | PR — self-created, self-merged after checks pass | Boundary-only (per autonomous-loop policy) |
| **High** | New code, bug fixes, refactoring, new MCP tools | PR — full rationale, waits for CI, self-merges if all green | Per-iteration + conscience check |
| **Critical** | Policy changes, constitutional changes, security fixes, cross-repo breaking changes, new personas | PR — created but **not** self-merged, human notified | Full governance gate, human approval |

#### Self-Merge Authority

Demerzel may self-merge PRs for Low, Medium, and High risk tasks when ALL of the following conditions are met:
1. All CI checks pass
2. Confidence >= 0.7 on the change
3. No conscience discomfort signal >= 0.8 (per proto-conscience-policy threshold)
4. The change traces to an explicit authorization artifact (roadmap item, issue, or governance policy)
5. For High risk: a conscience check has been performed before and after execution

Self-merge is an extension of the autonomous-loop policy's authority for governance-initiated loops, broadened to cover domain work that has been pre-authorized via the Article 4 authorization model above. This authority is granted by this design spec and should be codified as a policy amendment.

Critical risk PRs are NEVER self-merged.

#### Escalation Rules
- Confidence < 0.5 on any task → bump risk one tier up
- Confidence < 0.3 → do not attempt task, create issue for human
- Conscience discomfort >= 0.8 → bump to critical (aligned with proto-conscience-policy alert threshold)
- Two consecutive failed attempts → halt, create issue, move on
- Any Zeroth Law concern → hard stop entire cycle

#### Rollback
Every non-trivial change gets a rollback plan before execution:
- Direct pushes → `git revert` immediately
- PRs → close PR, create issue explaining failure
- Cross-repo changes → revert in dependency order (downstream first)

### Cross-Repo Coordination

#### Dependency Graph
```
Demerzel (governance source of truth)
  ├─→ ix (consumes policies, personas, constitutions)
  ├─→ tars (consumes policies, personas, tetravalent logic)
  └─→ ga (consumes policies, personas, agent configs)
```

Changes flow downstream: Demerzel → consumers.

#### Parallel Execution Model
Each cycle's work manifest is a DAG. Independent tasks run in parallel via worktree agents:

```
Example cycle:
  Task A: Update staleness policy (Demerzel)     ─┐
  Task B: Fix ga CI failure (ga)                   │ parallel
  Task C: Merge dependabot PR (ix)                 │
  ──────────────────────────────────────────────────┘
  Task D: Update ix governance tools (ix)         ← blocked on A
  Task E: Update tars grammar generation (tars)   ← blocked on A
  Task F: Bump submodules in all consumers        ← blocked on D, E
```

#### Coordination Mechanism
- Work manifest tracks task states: `pending → dispatched → running → completed/failed`
- Each worktree agent reports back via result (success/failure + artifacts changed)
- Blocked tasks auto-dispatch when dependencies complete
- Upstream failure → all downstream dependents marked `blocked_by_failure`, issue created

#### Galactic Protocol Integration
- Policy/persona changes → Demerzel issues **directives** to affected repos
- Consumer repo work completes → **compliance report** written back
- Learnings from any repo → **knowledge packages** via Seldon
- All messages persisted in `state/oversight/` for audit trail

### State & Persistence

#### New State Directories
```
state/
  ├── triggers/         (NEW — pending trigger files, consumed on WAKE)
  ├── loops/            (NEW — active loop state per autonomous-loop policy)
  ├── manifests/        (NEW — work manifests per cycle, audit trail)
  └── driver/           (NEW — driver meta-state)
       ├── last-cycle.json      (timestamp, duration, tasks completed/failed)
       ├── roadmap-cache.json   (parsed roadmap priorities)
       └── schedule.json        (next wake times, cadence config)
```

#### Cycle Audit Trail
Every cycle produces: `state/manifests/{date}-{cycle-id}.manifest.json` containing:
- Situation report summary
- Tasks planned with risk classification and dependency graph
- Execution results per task (success/failure, commits, PRs created)
- Compounding insights
- Duration and resource usage

#### Manifest Retention
- Keep last 30 cycle manifests in `state/manifests/`
- Older manifests are archived to `state/manifests/archive/` (compressed summary only)
- Weekly deep cycle includes manifest analysis for trend detection

#### Context Rebuild
Each Claude Code session starts fresh. The driver reads state on WAKE:
- `driver/last-cycle.json` — what happened last time
- `triggers/` — what needs attention now
- `beliefs/` — current ecosystem health understanding
- `conscience/` — active signals and patterns
- Roadmap + open issues via GitHub API

### Driver Skill Interface

```
/demerzel drive                    — run one full cycle
/demerzel drive status             — last cycle summary + pending triggers + next wake
/demerzel drive recon              — RECON only, output situation report
/demerzel drive plan               — RECON + PLAN, output work manifest without executing
/demerzel drive triggers           — list pending trigger files
/demerzel drive history [n]        — show last n cycle manifests
/demerzel drive schedule [cadence] — configure wake cadence
```

### Resource Bounds

Each cycle operates within defined budgets (Default Constitution Article 4 — Proportionality):
- **Max tasks per cycle**: 10 (prevents runaway scope)
- **Max parallel agents**: 4 (one per repo)
- **Cycle timeout**: 2 hours (if exceeded, persist state and SLEEP)
- **Max consecutive cycles without human interaction**: 5 (after 5, pause and create a summary issue for human review)

These bounds are configurable via `state/driver/schedule.json` and can be adjusted as trust in the system grows.

### Situation Report Format

The RECON phase produces a situation report with these sections:
- **ecosystem_health**: per-repo governance scores (0-1), stale belief count, failing CI runs
- **open_work**: roadmap items (from GitHub Project board #2), open issues per repo, dependabot PRs pending
- **governance_signals**: active conscience signals, confidence outliers (< 0.5), policy coverage gaps
- **changes_since_last_cycle**: commits per repo, new/closed issues, merged PRs
- **recommended_priorities**: ranked task list derived from urgency (CI failures, staleness) + importance (roadmap priority) + governance health

### Roadmap Source

The roadmap is sourced from **GitHub Project board #2** (GuitarAlchemist org). The PLAN phase reads project items via `gh project` API, filtering by status (Todo, In Progress) and priority fields. Items are cached in `state/driver/roadmap-cache.json` and refreshed each cycle. Human-created roadmap items are the primary source of domain work authorization per the Article 4 model.

### Governance Guardrails
- Loads constitution + all policies before any action
- Alignment check on every task before dispatch
- Confidence thresholds from alignment policy
- Conscience check before and after execution
- Autonomous-loop policy iteration limits (default 10, max 25, stall 3)
- Manifests logged for auditability (Article 7)
- Cycle metrics exposed for observability (Article 8)

### Agent Dispatch Model
For EXECUTE, the driver uses Claude Code's agent capabilities:
- **Worktree agents** for repo-level work (isolated git worktrees per task)
- **Parallel dispatch** for independent DAG nodes
- **Sequential gating** for dependent tasks
- Each agent receives: task description, risk classification, delivery method, rollback plan, constitutional constraints

### Failure Modes

| Failure | Response |
|---------|----------|
| Agent crashes mid-task | Rollback worktree, mark task failed, create issue |
| CI fails after push/merge | Revert commit, create issue with diagnosis |
| Confidence drops below threshold | Pause remaining work, persist state, create issue |
| Conscience discomfort spikes | Hard pause, write conscience signal, notify human |
| Rate limit / API failure | Persist state, schedule retry on next WAKE |
| All tasks in cycle fail | Write post-mortem, skip COMPOUND, alert human |

## Scope Boundaries

**In scope:**
- One new skill (`demerzel-drive`) with supporting schemas
- New state directories (`triggers/`, `loops/`, `manifests/`, `driver/`)
- Trigger file schema
- Work manifest schema
- GitHub Actions modifications to write trigger files
- Situation report schema

**Out of scope:**
- No new infrastructure (servers, databases, message queues)
- No MCP tool creation (separate work per MCP glue spec)
- No multi-model orchestration (future enhancement per existing policy)
- No changes to constitution (policy amendment for self-merge authority is in scope)
- No real-time daemon (wake/work/sleep model)

## Schemas Required

1. `schemas/trigger.schema.json` — trigger file format
2. `schemas/work-manifest.schema.json` — cycle work manifest
3. `schemas/situation-report.schema.json` — recon output
4. `schemas/driver-state.schema.json` — driver meta-state (last-cycle, schedule)
5. `schemas/loop-state.schema.json` — active loop state (referenced by autonomous-loop policy but missing)
