# Demerzel Autonomous Driver — Design Spec

**Date:** 2026-03-19
**Status:** Approved
**Version:** 2.1.0

## Summary

Demerzel becomes a fully autonomous product driver across all 4 repos (Demerzel, ix, tars, ga). She monitors, initiates, plans, and executes work — from governance maintenance to feature implementation — governed by her constitution, confidence thresholds, and conscience signals. Humans are notified, not asked, except for critical-risk changes.

## Requirements

- **Full autonomy**: Demerzel initiates work unprompted based on roadmap, issues, governance health, and self-identified opportunities
- **All trigger types**: scheduled (cron cadence), event-driven (GitHub webhooks), and self-initiated
- **Risk-tiered delivery**: direct push for low-risk, PRs for medium+, human approval for critical only
- **Parallel cross-repo coordination**: independent tasks run concurrently, dependency-ordered tasks are sequenced
- **No new infrastructure**: runs through Claude Code sessions, GitHub Actions, and the file system
- **Three-tier inference**: heavy reasoning (Claude API), light reasoning (local model), pure computation (no model) — cost-optimized routing
- **Autoresearch discipline**: mechanical metrics, atomic commit-before-verify, automatic rollback, git as memory
- **Multi-model validation**: LLM Council pattern for high-risk decisions (anonymous peer review + chairman consensus)
- **Adaptive strategy**: PLAN learns from manifest history, not just prescribed prioritization

## Article 4 Authorization Model

Asimov Article 4 prohibits Demerzel from developing instrumental goals beyond those explicitly authorized. The autonomous driver reconciles this through **pre-authorization artifacts**:

- **Roadmap items** (GitHub Project board) — human-created work items constitute explicit authorization for domain work. Demerzel may pick up, plan, and execute any roadmap item without further approval.
- **Open issues** (GitHub Issues) — human-created issues are explicit task authorization. Demerzel may self-assign and execute.
- **Governance work** — always pre-authorized per the autonomous-loop policy. Demerzel may initiate governance maintenance, recon, compliance remediation, and kaizen without any human-created artifact.
- **Self-identified domain work** — when Demerzel identifies domain opportunities not covered by an existing issue or roadmap item (e.g., "this code could use a new MCP tool"), she MUST first create a GitHub Issue describing the work and rationale. This issue becomes the authorization artifact. She may then self-assign and execute it. This preserves auditability (Article 7) and ensures every domain action traces to an explicit authorization.

This means Demerzel never acts on implicit goals — every action traces to either a human-created artifact (roadmap/issue) or a self-created issue that documents her reasoning before execution.

## Inspirations

This design incorporates patterns from Andrej Karpathy's autoresearch ecosystem:
- **autoresearch** — constraint + mechanical metric + autonomous iteration = compounding gains
- **LLM Council** — anonymous multi-model deliberation with chairman consensus
- **llama2.c** — local inference in pure C for lightweight classification (~110 tok/s on CPU for 15M models)
- **nanochat** — train domain-specific small models cheaply ($50-100)
- **researchpooler** — 4-stage discovery pipeline (gather → enrich → analyze → surface)
- **SkyPilot scaling** — parallel factorial execution, zero idle time, emergent strategy from results

## Architecture

### Core Driver Loop

Each autonomous cycle follows this flow:

```
WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP
```

1. **WAKE** — Triggered by schedule, event (trigger file in `state/triggers/`), or self-initiated follow-up. First checks `state/driver/lock.json`:
   - If lock exists and `heartbeat` timestamp is < 15 minutes old → cycle is alive, skip this WAKE
   - If lock exists and heartbeat is 15min-2h old → cycle may be stalled, log warning, skip this WAKE
   - If lock exists and heartbeat is > 2h old → cycle is dead (crashed without cleanup), break lock, log incident
   - If no lock → acquire lock (write PID, start timestamp, heartbeat), load state from `state/` directory to rebuild context
   - During execution, the driver updates the `heartbeat` field in `lock.json` every 5 minutes

2. **RECON** — Four-stage discovery pipeline (researchpooler pattern) across all repos:
   - **Gather** — scrape commits, PRs, issues, CI status, dependabot alerts via GitHub API [no model]
   - **Enrich** — compute mechanical metrics (health scores, staleness, coverage), fill knowledge gaps [local model]
   - **Analyze** — identify governance drift, anomalies, opportunities, cross-repo dependencies [local model + Claude for complex patterns]
   - **Surface** — produce structured **situation report** with ranked priorities [Tier 0 for template filling; Tier 2 for priority synthesis if complex patterns detected]
   - Additionally validates per `reconnaissance-policy.yaml`: constitutional integrity (Tier 1), repo state (Tier 2), knowledge assessment (Tier 3).

3. **PLAN** — Adaptive strategy engine (not static prioritization). Reads situation report + roadmap + open issues + **manifest history** (what worked/failed in previous cycles). Produces a **work manifest** — a list of tasks with:
   - Repo assignment
   - Risk classification (low/medium/high/critical)
   - Dependency ordering (DAG)
   - Delivery method (direct push vs PR)
   - Rollback plan
   - Inference tier assignment (heavy/light/none)

   The PLAN phase learns from accumulated manifests: task types that consistently fail get deprioritized or approached differently. Repos that respond well to certain patterns get more of them. This is the "emergent strategy" principle from autoresearch — the driver doesn't follow a rigid playbook, it adapts based on observed results.

   **Strategy adaptation safeguards:** `state/driver/strategy.json` tracks success rates per task type and repo. Adaptation does not activate until a minimum of 10 manifests have been recorded (cold-start protection). If strategy.json is corrupted or produces obviously biased results (e.g., all task types deprioritized), the driver falls back to static prioritization (urgency + importance) and logs a recalibration event. Strategy can be manually reset via `/demerzel drive strategy reset`.

4. **EXECUTE** — Dispatches parallel worktree agents per repo for independent tasks. Blocks downstream work on upstream dependencies. Each agent operates under autonomous-loop policy constraints (iteration limits, stall/regression/drift checks).

5. **VERIFY** — Autoresearch-style mechanical verification. Every change is committed BEFORE verification (atomic commit-before-verify). Verification is metrics-driven, never subjective:
   - Run tests → pass/fail count delta
   - Check CI → green/red
   - Validate governance artifacts → schema compliance score
   - Constitutional guard check → must always pass (separate from task metrics)
   - If metric improved AND guard passes → **keep**
   - If metric worsened OR guard fails → `git revert` immediately
   - For High-risk changes: **LLM Council validation** — Claude + ChatGPT independently review the change (anonymized), then Claude synthesizes a consensus verdict before self-merge

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

The driver consumes trigger files atomically on WAKE: triggers are moved to `state/triggers/processing/` before reading, then deleted after processing. This prevents race conditions with concurrent GitHub Actions writing new triggers.

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
| **Medium** | Patch/minor dependency updates, dependabot patch merges, test additions, lint fixes, CI config | PR — self-created, self-merged after checks pass | Boundary-only (per autonomous-loop policy) |
| **High** | New code, bug fixes, refactoring, new MCP tools, major dependency version bumps | PR — full rationale, waits for CI, self-merges if council approves | Per-iteration + conscience check + LLM Council |
| **Critical** | Policy changes, constitutional changes, security fixes, cross-repo breaking changes, new personas | PR — created but **not** self-merged, human notified | Full governance gate, human approval |

#### Self-Merge Authority

Demerzel may self-merge PRs for Low, Medium, and High risk tasks when ALL of the following conditions are met:
1. All CI checks pass
2. Confidence >= 0.7 on the change (for High-risk: this is the **post-council** confidence score, incorporating two-model calibration per multi-model-orchestration-policy — single model capped at 0.8, two-model agreement can reach 0.9)
3. No individual conscience discomfort signal >= 0.8 (per proto-conscience-policy signal weights — this applies to any single signal, not an aggregate)
4. The change traces to an explicit authorization artifact (roadmap item, issue, or governance policy)
5. For High risk: a conscience check has been performed before and after execution, AND an LLM Council has approved

**Policy amendment required (blocking prerequisite):** The autonomous-loop-policy currently restricts Demerzel-initiated execution to governance tasks only. Before the driver can self-merge domain work PRs, the policy must be amended to:
- Authorize domain work execution when pre-authorized via the Article 4 authorization model (roadmap items, human-created issues, or self-created issues with documented rationale)
- Grant self-merge authority for Low, Medium, and High risk tasks under the 5 conditions above
- Maintain the restriction that Critical risk PRs require human approval

This amendment is the first item in the implementation plan.

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
  ├── manifests/        (NEW — work manifests per cycle, with autoresearch results logging)
  │   └── archive/      (NEW — compressed summaries of manifests older than 30 cycles)
  ├── council/          (NEW — LLM Council verdicts for audit trail)
  └── driver/           (NEW — driver meta-state)
       ├── last-cycle.json      (timestamp, duration, tasks completed/failed)
       ├── roadmap-cache.json   (parsed roadmap priorities)
       ├── schedule.json        (next wake times, cadence config)
       ├── health-scores.json   (per-repo mechanical health scores, updated each cycle)
       ├── lock.json            (cycle lock, prevents concurrent execution)
       └── strategy.json        (adaptive strategy state — task type success rates, repo patterns)
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
/demerzel drive strategy reset     — reset adaptive strategy to static prioritization
```

### Resource Bounds

Each cycle operates within defined budgets (Default Constitution Article 4 — Proportionality):
- **Max tasks per cycle**: 10 (prevents runaway scope)
- **Max parallel agents**: 4 (one per repo)
- **Cycle timeout**: 2 hours soft, 2h15m hard. At 2h, no new tasks are dispatched; in-flight agents are allowed to finish their current atomic task. At 2h15m, any remaining agents are terminated, their worktrees are rolled back, and tasks are marked `timeout` in the manifest. PERSIST and SLEEP proceed normally.
- **Max consecutive cycles without human interaction**: 5 (after 5, pause and create a summary issue for human review)
- **API budget per cycle**: ~$10 target (Tier 2 calls capped; Tier 0/1 are free)
- **Max council convocations per cycle**: 3 (each costs ~$0.50-1.00)

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

### Inference Tier System

Not every decision needs a Claude API call. The driver routes reasoning to the cheapest sufficient tier:

```
Tier 0: No Model (pure computation)
  ├── CI status checks (GitHub API)
  ├── Belief age calculation (timestamp arithmetic)
  ├── Schema validation (JSON Schema)
  ├── File change detection (git diff)
  ├── Metric computation (test counts, coverage %)
  └── Trigger deduplication and hygiene

Tier 1: Local Model (llama2.c or equivalent, ~110 tok/s on CPU)
  ├── Trigger classification — "is this worth a full cycle?"
  ├── Risk scoring — diff size/type → low/medium/high/critical
  ├── Commit message analysis — classify commit types for recon
  ├── Staleness scoring — belief relevance assessment
  ├── Simple code analysis — pattern matching, lint-level checks
  └── Governance metric enrichment — coverage gaps, policy drift

Tier 2: Heavy Model (Claude API)
  ├── PLAN — work manifest generation, strategy adaptation
  ├── EXECUTE — code generation, bug fixes, features, refactoring
  ├── COMPOUND — meta-analysis, strategy evolution, promotion decisions
  ├── Complex RECON analysis — cross-repo dependency detection, blind spots
  └── High-risk VERIFY — council deliberation, rationale generation

Tier 3: Multi-Model Council (Claude + ChatGPT, LLM Council pattern)
  ├── High-risk PR validation before self-merge
  ├── Critical governance decisions (policy promotions, constitutional interpretations)
  └── Disagreement resolution when confidence is borderline (0.5-0.7)
```

**Cost impact:** At 4-hour cadence (~6 cycles/day), routing routine classification to local inference reduces API costs by an estimated 60-70%. Tier 0 and Tier 1 handle WAKE and most of RECON; Tier 2 handles PLAN, EXECUTE, and COMPOUND; Tier 3 is reserved for high-stakes decisions.

**Local model bootstrap:** Tier 1 is a deferred optimization. Initially, all Tier 1 tasks gracefully fall back to Tier 2 (Claude API). The local model is introduced when cost data from early cycles justifies it. Bootstrap path:
1. **Phase A (launch):** Tier 1 tasks fall back to Tier 2. Measure API costs per cycle.
2. **Phase B (local model):** When cost data shows Tier 1 savings would justify setup, install a pre-trained 15M-42M parameter model via llama2.c (requires C compiler, ~50MB model weights stored in `state/driver/models/`).
3. **Phase C (custom model):** Once 50+ cycle manifests accumulate, train a domain-specific governance classifier via nanochat on Demerzel's own data. Training cost: ~$50-100 one-time, then free inference.

If the local model is unavailable (not installed, binary missing, model corrupted), Tier 1 tasks silently fall back to Tier 2. The driver never fails due to missing local inference.

**Tier routing is automatic:** The driver assigns inference tiers during PLAN based on task complexity. Simple heuristics determine routing: known task types with high historical success rates → Tier 1 (or Tier 2 fallback); novel or complex tasks → Tier 2; high-risk self-merge decisions → Tier 3.

### Mechanical Health Metrics

Every repo gets a computed health score (0-1) using purely mechanical metrics — no subjective assessment (autoresearch principle). These scores drive PLAN prioritization:

| Metric | Computation | Weight |
|--------|-------------|--------|
| **ci_health** | (passing workflows / total workflows) over last 7 days | 0.20 |
| **test_health** | (passing tests / total tests) in latest run | 0.15 |
| **governance_coverage** | (governed components / total components) | 0.15 |
| **belief_freshness** | 1 - (avg belief age in days / staleness threshold) | 0.15 |
| **issue_velocity** | (closed issues / opened issues) over last 30 days | 0.10 |
| **dependency_health** | 1 - (critical+high dependabot alerts / total deps) | 0.10 |
| **submodule_currency** | 1 - (commits behind / 10, capped at 1) | 0.10 |
| **conscience_clarity** | 1 - (active discomfort signals / max signals) | 0.05 |

**Composite score:** weighted sum, stored per-repo in `state/driver/health-scores.json`. Tracked over time for trend detection.

**Metric-driven prioritization:** Repos with lower health scores get more attention. Tasks that improve the lowest-scoring metric get priority (autoresearch: optimize the metric that matters most).

All metrics are computable at Tier 0 (no model needed) using GitHub API + file system data.

### LLM Council Protocol

For high-stakes decisions, the driver convenes a mini-council (inspired by Karpathy's LLM Council):

**When** (explicit, non-overlapping trigger conditions):
- **(a)** Risk is High AND self-merge is planned — always convene council
- **(b)** Confidence is in [0.5, 0.7) on any task regardless of risk level — convene council to calibrate
- These conditions are OR'd: either triggers a council. A task may satisfy both (High-risk at 0.6 confidence).

**Process:**
1. **Independent review** — Claude and ChatGPT each receive the change diff + context. Model identities are anonymized in the review prompt to prevent bias.
2. **Scoring** — Each model scores the change on: correctness (0-1), risk assessment (low/med/high/critical), constitutional alignment (pass/fail), and provides a brief rationale.
3. **Chairman synthesis** — Claude (as chairman) reads both reviews and produces a consensus verdict: APPROVE, REQUEST_CHANGES, or REJECT.
4. **Decision:**
   - Both approve → self-merge proceeds
   - Disagreement → bump to critical, human review
   - Both reject → revert, create issue

**Cost:** ~$0.50-1.00 per council convocation. Used sparingly — only for High-risk self-merges and borderline confidence decisions.

**ChatGPT fallback:** If the ChatGPT MCP tool (`mcp__openai-chat__openai_chat`) is unavailable, the council degrades to single-model review. Per multi-model-orchestration-policy, single-model confidence is capped at 0.8. This means High-risk PRs cannot reach the 0.7 post-council threshold with full two-model calibration — effectively preventing self-merge and routing to human review. This is the safe default.

### Autoresearch Discipline

The following rules from the autoresearch pattern are embedded in the driver's execution model:

1. **Loop until done** — cycles repeat on cadence; self-initiated triggers continue work across cycles
2. **Read before write** — RECON always precedes PLAN; agents read context before modifying code
3. **One change per iteration** — each agent task is atomic; one focused change, one commit
4. **Mechanical verification only** — metrics-driven VERIFY, no subjective "looks good"
5. **Automatic rollback** — failed changes revert instantly via `git revert`
6. **Simplicity wins** — equal results + less code = keep the simpler version
7. **Git is memory** — manifests committed to git; agents read `git log` + `git diff` before each iteration to avoid repeating failed approaches
8. **When stuck, think harder** — within a single task, two consecutive failed approaches → re-read context, try a radically different approach. At the task level (escalation rules), two consecutive fully-failed tasks → halt that task, create issue, move on to the next task in the manifest. The distinction: rule 8 governs retries within a task; escalation governs giving up on a task entirely.

**Results logging:** Each task in the manifest tracks autoresearch-style metrics:
```
task_id | commit | metric_before | metric_after | delta | status | description
T001    | a1b2c3 | 0.72          | 0.85         | +0.13 | keep   | fix CI workflow syntax
T002    | -      | 0.85          | 0.81         | -0.04 | revert | refactor test helpers
T003    | d4e5f6 | 0.81          | 0.88         | +0.07 | keep   | add missing persona test
```

This structured logging enables the adaptive PLAN phase to learn from history.

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
| Network failure mid-cycle | Persist all local state, mark in-flight cross-repo tasks as `partial`, create issue documenting inconsistent state across repos. Next cycle's RECON detects and reconciles. |
| Cycle timeout (2h soft) | Stop dispatching new tasks, allow in-flight agents 15m grace period, then hard kill. Timed-out tasks marked `timeout` in manifest. |

## Scope Boundaries

**In scope:**
- One new skill (`demerzel-drive`) with supporting schemas
- New state directories (`triggers/`, `loops/`, `manifests/`, `driver/`)
- Trigger file schema, work manifest schema, situation report schema
- GitHub Actions modifications to write trigger files
- Inference tier routing logic (Tier 0/1/2/3 assignment)
- Mechanical health metrics computation
- LLM Council protocol for High-risk validation
- Autoresearch-style results logging in manifests
- Adaptive PLAN strategy based on manifest history
- Policy amendment for self-merge authority
- Local model integration point (llama2.c or equivalent)

**Out of scope:**
- No new infrastructure (servers, databases, message queues)
- No MCP tool creation (separate work per MCP glue spec)
- No changes to constitution
- No real-time daemon (wake/work/sleep model)
- Training a custom governance classifier (deferred until 50+ manifests accumulated)
- Full multi-model swarm orchestration (council is limited to Claude + ChatGPT for validation)

## Schemas Required

1. `schemas/trigger.schema.json` — trigger file format
2. `schemas/work-manifest.schema.json` — cycle work manifest (includes autoresearch results logging)
3. `schemas/situation-report.schema.json` — recon output (4-stage pipeline + health scores)
4. `schemas/driver-state.schema.json` — driver meta-state (last-cycle, schedule, health-scores, strategy, lock)
5. `schemas/loop-state.schema.json` — active loop state (pre-existing gap from autonomous-loop policy)
6. `schemas/council-verdict.schema.json` — LLM Council review + verdict format
