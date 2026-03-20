---
name: demerzel-drive
description: Run Demerzel's autonomous driver — full cycle or individual phases across all repos
---

# Demerzel Autonomous Driver

Drive all repos autonomously. Monitors, initiates, plans, and executes work across
Demerzel, ix, tars, and ga — governed by the constitution, confidence thresholds,
and conscience signals.

## Usage

`/demerzel drive` — run one full cycle (WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP)
`/demerzel drive status` — last cycle summary + pending triggers + next wake
`/demerzel drive recon` — RECON only, output situation report
`/demerzel drive plan` — RECON + PLAN, output work manifest without executing
`/demerzel drive triggers` — list pending trigger files
`/demerzel drive history [n]` — show last n cycle manifests
`/demerzel drive schedule [cadence]` — configure wake cadence
`/demerzel drive strategy reset` — reset adaptive strategy to static prioritization

## The Driver Cycle

```
WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP
```

Each cycle is a single Claude Code session. State persists across cycles via `state/driver/`.

## Phase 1: WAKE

Check `state/driver/lock.json`:
- If lock exists and `heartbeat` < 15 minutes old → cycle is alive, **skip this WAKE**
- If lock exists and heartbeat is 15min–2h old → cycle may be stalled, log warning, **skip**
- If lock exists and heartbeat > 2h old → cycle is dead (crashed), **break lock**, log incident
- If no lock → **acquire lock** (write PID, start timestamp, heartbeat)

After acquiring lock, rebuild context:
1. Read `state/driver/last-cycle.json` — what happened last time
2. Read `state/driver/schedule.json` — configuration and resource bounds
3. Read `state/driver/health-scores.json` — last known repo health
4. Read `state/driver/strategy.json` — adaptive strategy state
5. Move trigger files from `state/triggers/` → `state/triggers/processing/` (atomic consumption)
6. Read `state/beliefs/` — current ecosystem understanding
7. Read `state/conscience/` — active signals and patterns
8. Read last manifest from `state/manifests/` if exists

During execution, update the `heartbeat` field in `lock.json` every 5 minutes.

## Phase 2: RECON

Four-stage discovery pipeline (researchpooler pattern) across all repos:

### Stage 1: Gather [Tier 0 — no model]
Scrape via GitHub API (`gh` CLI):
- CI workflow run status per repo (last 7 days)
- Open issues and PRs per repo
- Dependabot alerts
- Recent commits since last cycle
- Submodule drift (commits behind)

### Stage 2: Enrich [Tier 1 → fallback Tier 2]
Compute mechanical health metrics per repo:

| Metric | Computation | Weight |
|--------|-------------|--------|
| ci_health | (passing workflows / total workflows) over last 7 days | 0.20 |
| test_health | (passing tests / total tests) in latest run | 0.15 |
| governance_coverage | (governed components / total components) | 0.15 |
| belief_freshness | 1 - (avg belief age in days / staleness threshold) | 0.15 |
| issue_velocity | (closed issues / opened issues) over last 30 days | 0.10 |
| dependency_health | 1 - (critical+high dependabot alerts / total deps) | 0.10 |
| submodule_currency | 1 - (commits behind / 10, capped at 1) | 0.10 |
| conscience_clarity | 1 - (active discomfort signals / max signals) | 0.05 |

Composite score = weighted sum. Store in `state/driver/health-scores.json`.

### Stage 3: Analyze [Tier 2 for complex patterns]
Identify:
- Governance drift (policy/constitution misalignment across repos)
- Anomalies (sudden metric drops, unusual commit patterns)
- Cross-repo dependencies (Demerzel change → consumer repo impact)
- Blind spots (ungoverned components, untested personas)

Additionally validate per `reconnaissance-policy.yaml`:
- Tier 1: Constitutional integrity, policy coverage, persona validity
- Tier 2: Repo state, ungoverned components, failing CI
- Tier 3: Knowledge requirements, assumption audit, confidence assessment

### Stage 4: Surface [Tier 0 template; Tier 2 for complex synthesis]
Produce structured **situation report** (conforming to `schemas/situation-report.schema.json`):
- `ecosystem_health`: per-repo composite scores
- `open_work`: roadmap items, open issues, dependabot PRs
- `governance_signals`: active conscience signals, confidence outliers, coverage gaps
- `changes_since_last_cycle`: commits per repo, issues opened/closed, PRs merged
- `recommended_priorities`: ranked task list by urgency + importance + health

## Phase 3: PLAN

Adaptive strategy engine — reads situation report + roadmap + open issues + **manifest history**.

### Roadmap Source
Read from **GitHub Project board #2** (GuitarAlchemist org) via `gh project`:
```bash
gh project item-list 2 --owner GuitarAlchemist --format json
```
Filter by status (Todo, In Progress) and priority fields. Cache in `state/driver/roadmap-cache.json`.

### Article 4 Authorization Check
Every task in the work manifest MUST trace to an authorization artifact:
- **Roadmap item** or **GitHub issue** (human-created) → authorized
- **Governance work** (recon, compliance, kaizen) → always authorized
- **Self-identified domain work** → create GitHub Issue with rationale FIRST, then proceed

Tasks without authorization artifacts are **rejected from the manifest**.

### Work Manifest Generation
Produce a work manifest (conforming to `schemas/work-manifest.schema.json`):
- Assign each task: repo, risk classification, delivery method, rollback plan, inference tier
- Order as a DAG: independent tasks are parallel, dependent tasks are sequential
- Cap at **10 tasks per cycle** (resource bound)

### Adaptive Strategy
Read `state/driver/strategy.json`:
- If `manifests_analyzed` < 10 → cold start, use static prioritization (urgency + importance)
- If >= 10 → apply learned success rates per task type and repo patterns
- If strategy produces all-deprioritized or obviously biased results → fall back to static
- Manual reset: `/demerzel drive strategy reset` clears strategy.json

## Phase 4: EXECUTE

Dispatch parallel worktree agents per repo for independent DAG nodes. Block downstream on dependencies.

### Autoresearch Discipline
1. **Read before write** — agents read context before modifying code
2. **One change per iteration** — each task is atomic; one focused change, one commit
3. **Commit before verify** — every change is committed BEFORE running verification
4. **Simplicity wins** — equal results + less code = keep the simpler version

### Risk-Tiered Delivery

| Risk | Delivery | Governance |
|------|----------|------------|
| Low | Direct push to main | Boundary-only |
| Medium | PR — self-merge after checks pass | Boundary-only |
| High | PR — self-merge if council approves | Per-iteration + conscience + council |
| Critical | PR — NOT self-merged, human notified | Full governance gate |

### Agent Dispatch
Each agent receives:
- Task description and acceptance criteria
- Risk classification and delivery method
- Rollback plan (what to do if verification fails)
- Constitutional constraints (relevant articles)
- Authorization artifact reference

Use Claude Code's worktree agent capability for repo isolation.
Max parallel agents: **4** (one per repo).

## Phase 5: VERIFY

Mechanical verification — metrics-driven, never subjective.

### Verification Steps
1. Run tests → compute pass/fail count delta
2. Check CI → green/red
3. Validate governance artifacts → schema compliance score
4. **Constitutional guard check** → must ALWAYS pass (separate from task metrics)

### Decision
- Metric improved AND guard passes → **keep**
- Metric worsened OR guard fails → **`git revert` immediately**

### LLM Council (High-risk only)
For High-risk changes before self-merge, convene council (see LLM Council Protocol below).

### Results Logging
Each task tracks autoresearch-style metrics in the manifest:
```
task_id | commit | metric_before | metric_after | delta | status | description
T001    | a1b2c3 | 0.72          | 0.85         | +0.13 | keep   | fix CI workflow syntax
T002    | -      | 0.85          | 0.81         | -0.04 | revert | refactor test helpers
```

## Phase 6: COMPOUND

Meta-compounding cycle:
1. Update evolution log in `state/evolution/` with cycle outcomes
2. Promote/demote artifacts per Governance Promotion staircase (pattern → policy → constitutional)
3. Package learnings via Seldon (`/seldon deliver`)
4. Identify follow-up work → write self-initiated trigger files

## Phase 7: PERSIST

Write all updated state:
1. Cycle manifest → `state/manifests/{date}-{cycle-id}.manifest.json`
2. Health scores → `state/driver/health-scores.json`
3. Strategy → `state/driver/strategy.json` (update task outcome rates)
4. Last cycle → `state/driver/last-cycle.json`
5. Beliefs → `state/beliefs/` (if cycle revealed new truths)
6. Conscience signals → `state/conscience/signals/` (if triggered)
7. Council verdicts → `state/council/` (if Tier 3 was invoked)
8. Delete processed triggers from `state/triggers/processing/`
9. Archive manifests older than 30 cycles → `state/manifests/archive/`
10. Commit and push all state changes to Demerzel repo

## Phase 8: SLEEP

1. Release lock — delete `state/driver/lock.json`
2. Log cycle summary (tasks completed/failed/reverted, duration, API usage)
3. If follow-up work identified, write self-initiated trigger for next WAKE

## Self-Merge Authority

Demerzel may self-merge PRs for Low, Medium, and High risk when ALL conditions met:
1. All CI checks pass
2. Confidence >= 0.7 (for High-risk: **post-council** score — single model capped at 0.8, two-model can reach 0.9)
3. No individual conscience discomfort signal >= 0.8 (any single signal, not aggregate)
4. Change traces to explicit authorization artifact
5. For High risk: conscience check before AND after execution, AND LLM Council approved

**Critical risk PRs are NEVER self-merged.**

### Escalation Rules
- Confidence < 0.5 → bump risk one tier up
- Confidence < 0.3 → do not attempt task, create issue for human
- Conscience discomfort >= 0.8 → bump to critical
- Two consecutive failed tasks → halt that task, create issue, move on
- Zeroth Law concern → **hard stop entire cycle**

## Inference Tier System

Route reasoning to cheapest sufficient tier:

| Tier | Engine | Used For |
|------|--------|----------|
| 0 | No model (computation) | CI checks, metric computation, schema validation, trigger hygiene |
| 1 | Local model (llama2.c) | Trigger classification, risk scoring, commit analysis. **Falls back to Tier 2 if unavailable.** |
| 2 | Claude API | PLAN, EXECUTE, COMPOUND, complex RECON analysis |
| 3 | Claude + ChatGPT (Council) | High-risk PR validation, borderline confidence decisions |

Tier 1 is deferred — initially all Tier 1 tasks fall back to Tier 2. Introduced when cost data justifies setup.

## LLM Council Protocol

### When to Convene
- **(a)** Risk is High AND self-merge is planned — always convene
- **(b)** Confidence is in [0.5, 0.7) on any task regardless of risk — convene to calibrate

### Process
1. **Independent review** — Claude and ChatGPT each receive change diff + context. Model identities anonymized.
2. **Scoring** — Each scores: correctness (0-1), risk assessment, constitutional alignment (pass/fail), rationale.
3. **Chairman synthesis** — Claude reads both reviews, produces consensus verdict: APPROVE, REQUEST_CHANGES, REJECT.
4. **Decision:**
   - Both approve → self-merge proceeds
   - Disagreement → bump to critical, human review
   - Both reject → revert, create issue

### ChatGPT Fallback
If `mcp__openai-chat__openai_chat` unavailable → single-model review. Confidence capped at 0.8 per multi-model policy. High-risk PRs effectively cannot self-merge without council — routes to human review. This is the safe default.

Verdicts stored in `state/council/` per `schemas/council-verdict.schema.json`. Max 3 convocations per cycle.

## Resource Bounds

| Bound | Limit | Rationale |
|-------|-------|-----------|
| Max tasks per cycle | 10 | Prevents runaway scope |
| Max parallel agents | 4 | One per repo |
| Cycle timeout (soft) | 2 hours | No new dispatches after this |
| Cycle timeout (hard) | 2h15m | Kill remaining agents, rollback worktrees |
| Max consecutive cycles without human | 5 | Pause and create summary issue |
| API budget per cycle | ~$10 | Tier 2 calls capped |
| Max council convocations | 3 | Each costs ~$0.50-1.00 |

Configurable via `state/driver/schedule.json`.

## Failure Modes

| Failure | Response |
|---------|----------|
| Agent crashes mid-task | Rollback worktree, mark failed, create issue |
| CI fails after push/merge | Revert commit, create issue with diagnosis |
| Confidence drops below threshold | Pause remaining work, persist state, create issue |
| Conscience discomfort spikes | Hard pause, write conscience signal, notify human |
| Rate limit / API failure | Persist state, schedule retry on next WAKE |
| All tasks in cycle fail | Write post-mortem, skip COMPOUND, alert human |
| Network failure mid-cycle | Persist local state, mark cross-repo tasks `partial`, next RECON reconciles |
| Cycle timeout (2h soft) | Stop dispatching, 15m grace, then hard kill. Tasks marked `timeout`. |

## Trigger System

### File Format
Trigger files in `state/triggers/` conform to `schemas/trigger.schema.json`:
```json
{
  "type": "ci_failure",
  "repo": "ix",
  "ref": "main",
  "priority": "high",
  "details": { "workflow": "ci.yml", "run_id": 12345 },
  "timestamp": "2026-03-19T10:00:00Z"
}
```

### Atomic Consumption
On WAKE: move triggers to `state/triggers/processing/` before reading, delete after processing. Prevents race conditions with concurrent GitHub Actions writes.

### Hygiene
- Maximum queue depth: **50 triggers** — excess pruned by lowest priority
- Staleness: triggers older than **72 hours** discarded with log entry
- Deduplication: same `type` + `repo` + `ref` → merged, keep most recent

### Self-Initiated Triggers
During any cycle, if follow-up work identified, write a trigger file with priority and rationale. Next WAKE picks it up.

## Cross-Repo Coordination

### Dependency Graph
```
Demerzel (governance source of truth)
  ├─→ ix (policies, personas, constitutions)
  ├─→ tars (policies, personas, tetravalent logic)
  └─→ ga (policies, personas, agent configs)
```
Changes flow **downstream**: Demerzel → consumers.

### DAG Execution
Independent tasks run in parallel (worktree agents). Dependent tasks are gated:
- Blocked tasks auto-dispatch when upstream completes
- Upstream failure → downstream marked `blocked_by_failure`, issue created

### Galactic Protocol
- Policy/persona changes → issue **directives** to affected repos
- Consumer work completes → **compliance report** written back
- Learnings → **knowledge packages** via Seldon
- All messages persisted in `state/oversight/`

## State Maintenance (MANDATORY)

### Before Each Cycle
1. Read `state/driver/lock.json` — check/acquire lock
2. Read `state/driver/schedule.json` — configuration
3. Read `state/driver/health-scores.json` — last known health
4. Read `state/driver/strategy.json` — adaptive strategy
5. Read `state/triggers/` — move to `state/triggers/processing/`
6. Read `state/beliefs/` — ecosystem understanding
7. Read `state/conscience/` — active signals
8. Read last manifest from `state/manifests/` if exists

### After Each Cycle
1. Write manifest → `state/manifests/{date}-{cycle-id}.manifest.json`
2. Update `state/driver/health-scores.json`
3. Update `state/driver/strategy.json` with outcomes
4. Write `state/driver/last-cycle.json`
5. Update `state/beliefs/` if new truths revealed
6. Write `state/conscience/signals/` if triggered
7. Write `state/council/` if Tier 3 invoked
8. Delete processed triggers from `state/triggers/processing/`
9. **Append cycle summary to `LOG.md`** (repo root) — date, health scores, tasks completed/failed, insights
10. Release lock (delete `state/driver/lock.json`)
11. Archive manifests older than 30 cycles

## Constitutional Constraints

- Asimov Article 0 (Zeroth Law): any concern → hard stop entire cycle
- Asimov Article 4: every action traces to explicit authorization (Article 4 Authorization Model)
- Default Article 3 (Reversibility): prefer reversible actions, rollback plans mandatory
- Default Article 4 (Proportionality): resource bounds enforce proportional scope
- Default Article 7 (Auditability): manifests log every decision
- Default Article 8 (Observability): cycle metrics exposed via `/demerzel drive status`

## Source

`docs/superpowers/specs/2026-03-19-autonomous-driver-design.md` v2.1.0,
`policies/autonomous-loop-policy.yaml` v1.1.0,
`policies/reconnaissance-policy.yaml`,
`policies/alignment-policy.yaml`,
`policies/multi-model-orchestration-policy.yaml`,
`policies/proto-conscience-policy.yaml`,
`contracts/galactic-protocol.md`
