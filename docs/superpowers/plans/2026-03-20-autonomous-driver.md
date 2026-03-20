# Demerzel Autonomous Driver Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Demerzel a fully autonomous product driver across all 4 repos (Demerzel, ix, tars, ga) with risk-tiered delivery, parallel cross-repo coordination, mechanical health metrics, LLM Council validation, and autoresearch discipline.

**Architecture:** A new `demerzel-drive` skill orchestrates an 8-phase cycle (WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP). State persists in `state/driver/`, `state/triggers/`, `state/manifests/`, and `state/council/`. GitHub Actions write trigger files for event-driven activation. Inference is tiered (Tier 0 no-model, Tier 1 local fallback-to-Tier-2, Tier 2 Claude API, Tier 3 LLM Council).

**Tech Stack:** YAML (policies), JSON Schema (validation), Markdown (skills, behavioral tests), GitHub Actions (event triggers)

**Spec:** `docs/superpowers/specs/2026-03-19-autonomous-driver-design.md` v2.1.0

**Important context:** Demerzel contains NO runtime code. All deliverables are governance artifacts — YAML policies, JSON schemas, Markdown skills, and behavioral test specifications. "Testing" means writing behavioral test cases, not executable unit tests.

---

## File Map

### New Files
| File | Purpose |
|------|---------|
| `policies/autonomous-loop-policy.yaml` | MODIFY — add domain work authorization + self-merge authority |
| `schemas/trigger.schema.json` | Trigger file format |
| `schemas/work-manifest.schema.json` | Cycle work manifest with autoresearch results logging |
| `schemas/situation-report.schema.json` | RECON output (4-stage pipeline + health scores) |
| `schemas/driver-state.schema.json` | Driver meta-state (last-cycle, schedule, health-scores, strategy, lock) |
| `schemas/loop-state.schema.json` | Active loop state (fills pre-existing gap) |
| `schemas/council-verdict.schema.json` | LLM Council review + verdict format |
| `.claude/skills/demerzel-drive/SKILL.md` | The core autonomous driver skill |
| `.github/workflows/demerzel-driver-triggers.yml` | Event-driven trigger file writer |
| `state/triggers/.gitkeep` | Trigger queue directory |
| `state/triggers/processing/.gitkeep` | Atomic trigger consumption staging |
| `state/manifests/.gitkeep` | Cycle manifest audit trail |
| `state/manifests/archive/.gitkeep` | Archived manifests |
| `state/council/.gitkeep` | Council verdict audit trail |
| `state/loops/.gitkeep` | Active loop state |
| `state/driver/schedule.json` | Default schedule configuration |
| `state/driver/health-scores.json` | Initial health scores seed |
| `state/driver/strategy.json` | Initial adaptive strategy (empty) |
| `tests/behavioral/driver-cases.md` | Behavioral test suite for the driver |

### Modified Files
| File | Change |
|------|--------|
| `policies/autonomous-loop-policy.yaml` | Add Article 4 authorization model, self-merge authority |
| `.claude/skills/demerzel/SKILL.md` | Add `/demerzel drive` to dispatcher |
| `.claude/skills/demerzel-skills/SKILL.md` | Add demerzel-drive to skills listing |

---

## Task 1: Policy Amendment — Autonomous Loop Policy

**This is a blocking prerequisite.** The autonomous-loop-policy must be amended before any driver functionality can operate within governance bounds.

**Files:**
- Modify: `policies/autonomous-loop-policy.yaml`

- [ ] **Step 1: Read the current autonomous-loop-policy**

Read `policies/autonomous-loop-policy.yaml` in full. Identify the `demerzel_initiated_loops` section that restricts Demerzel to governance-only work.

- [ ] **Step 2: Add Article 4 Authorization Model section**

After the existing `demerzel_initiated_loops` section, add a new section:

```yaml
  domain_work_authorization:
    description: >
      Extension of Demerzel-initiated loop authority to cover domain work
      pre-authorized via the Article 4 Authorization Model.
    effective_date: "2026-03-20"
    authorization_artifacts:
      - type: roadmap_item
        source: "GitHub Project board"
        description: "Human-created roadmap items constitute explicit authorization"
      - type: github_issue
        source: "GitHub Issues"
        description: "Human-created issues are explicit task authorization"
      - type: governance_work
        source: "autonomous-loop-policy"
        description: "Always pre-authorized — maintenance, recon, compliance, kaizen"
      - type: self_identified
        source: "Demerzel-created GitHub Issue"
        description: >
          Demerzel MUST create a GitHub Issue with rationale before executing
          self-identified domain work. The issue becomes the authorization artifact.
    constraint: >
      Every domain action must trace to an explicit authorization artifact.
      Demerzel never acts on implicit goals.
```

- [ ] **Step 3: Add self-merge authority section**

After the `domain_work_authorization` section, add:

```yaml
  self_merge_authority:
    description: >
      Demerzel may self-merge PRs for Low, Medium, and High risk tasks.
    conditions:
      - "All CI checks pass"
      - "Confidence >= 0.7 (post-council for High-risk)"
      - "No individual conscience discomfort signal >= 0.8"
      - "Change traces to explicit authorization artifact"
      - "For High risk: conscience check before+after AND LLM Council approved"
    restrictions:
      - "Critical risk PRs are NEVER self-merged"
      - "Single-model confidence capped at 0.8 per multi-model-orchestration-policy"
      - "Two-model agreement can reach 0.9"
    escalation:
      confidence_below_0_5: "bump risk one tier up"
      confidence_below_0_3: "do not attempt, create issue for human"
      conscience_discomfort_0_8: "bump to critical"
      two_consecutive_failures: "halt, create issue, move on"
      zeroth_law_concern: "hard stop entire cycle"
```

- [ ] **Step 4: Update version and add rationale**

Bump version from `1.0.0` to `1.1.0`. Add rationale:

```yaml
version: "1.1.0"
rationale: >
  v1.1.0: Extended Demerzel-initiated loop authority to cover domain work
  pre-authorized via the Article 4 Authorization Model (roadmap items,
  human-created issues, self-created issues with documented rationale).
  Added self-merge authority with 5-condition gate. Maintains Critical
  risk restriction requiring human approval.
```

- [ ] **Step 5: Commit**

```bash
git add policies/autonomous-loop-policy.yaml
git commit -m "feat: Amend autonomous-loop policy — Article 4 authorization + self-merge authority"
```

---

## Task 2: JSON Schemas

Create 6 JSON schemas that define the data contracts for the driver's state files.

**Files:**
- Create: `schemas/trigger.schema.json`
- Create: `schemas/work-manifest.schema.json`
- Create: `schemas/situation-report.schema.json`
- Create: `schemas/driver-state.schema.json`
- Create: `schemas/loop-state.schema.json`
- Create: `schemas/council-verdict.schema.json`

- [ ] **Step 1: Create trigger.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "trigger.schema.json",
  "title": "Driver Trigger",
  "description": "Event trigger file consumed by Demerzel's autonomous driver on WAKE",
  "type": "object",
  "required": ["type", "repo", "priority", "timestamp"],
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "ci_failure", "issue_opened", "issue_reopened", "push",
        "dependabot_pr", "discussion_created", "submodule_drift",
        "self_initiated", "scheduled"
      ]
    },
    "repo": {
      "type": "string",
      "enum": ["demerzel", "ix", "tars", "ga"]
    },
    "ref": {
      "type": "string",
      "description": "Git ref (branch/tag) related to this trigger"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"]
    },
    "details": {
      "type": "object",
      "description": "Trigger-specific payload",
      "additionalProperties": true
    },
    "rationale": {
      "type": "string",
      "description": "For self_initiated triggers — why Demerzel created this"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 2: Create work-manifest.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "work-manifest.schema.json",
  "title": "Driver Work Manifest",
  "description": "Cycle work manifest with DAG task ordering and autoresearch results logging",
  "type": "object",
  "required": ["cycle_id", "date", "situation_summary", "tasks", "resource_usage"],
  "properties": {
    "cycle_id": {
      "type": "string",
      "pattern": "^cycle-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"
    },
    "date": { "type": "string", "format": "date" },
    "trigger": {
      "type": "string",
      "enum": ["scheduled", "event", "self_initiated"]
    },
    "situation_summary": {
      "type": "object",
      "description": "Compressed situation report",
      "properties": {
        "ecosystem_health": {
          "type": "object",
          "additionalProperties": { "type": "number", "minimum": 0, "maximum": 1 }
        },
        "urgent_items": { "type": "integer" },
        "governance_signals": { "type": "integer" }
      }
    },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["task_id", "description", "repo", "risk", "status"],
        "properties": {
          "task_id": { "type": "string", "pattern": "^T\\d{3}$" },
          "description": { "type": "string" },
          "repo": { "type": "string", "enum": ["demerzel", "ix", "tars", "ga"] },
          "risk": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
          "delivery": { "type": "string", "enum": ["direct_push", "pr_self_merge", "pr_human_review"] },
          "inference_tier": { "type": "integer", "minimum": 0, "maximum": 3 },
          "blocked_by": {
            "type": "array",
            "items": { "type": "string" }
          },
          "authorization_artifact": {
            "type": "string",
            "description": "URL or reference to the roadmap item, issue, or policy authorizing this task"
          },
          "rollback_plan": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["pending", "dispatched", "running", "completed", "failed", "reverted", "blocked_by_failure", "timeout", "partial"]
          },
          "commit": { "type": ["string", "null"] },
          "pr_url": { "type": ["string", "null"] },
          "metric_before": { "type": ["number", "null"] },
          "metric_after": { "type": ["number", "null"] },
          "delta": { "type": ["number", "null"] },
          "council_verdict_ref": {
            "type": ["string", "null"],
            "description": "Path to council verdict file if Tier 3 was invoked"
          }
        }
      }
    },
    "compounding_insights": {
      "type": "array",
      "items": { "type": "string" }
    },
    "resource_usage": {
      "type": "object",
      "properties": {
        "duration_seconds": { "type": "integer" },
        "api_calls_tier2": { "type": "integer" },
        "council_convocations": { "type": "integer" },
        "tasks_completed": { "type": "integer" },
        "tasks_failed": { "type": "integer" },
        "tasks_reverted": { "type": "integer" }
      }
    },
    "follow_up_triggers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Self-initiated trigger files created for next cycle"
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 3: Create situation-report.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "situation-report.schema.json",
  "title": "Situation Report",
  "description": "RECON output — 4-stage pipeline result with mechanical health scores",
  "type": "object",
  "required": ["date", "ecosystem_health", "open_work", "governance_signals", "changes_since_last_cycle", "recommended_priorities"],
  "properties": {
    "date": { "type": "string", "format": "date-time" },
    "ecosystem_health": {
      "type": "object",
      "description": "Per-repo health scores",
      "properties": {
        "demerzel": { "$ref": "#/$defs/repo_health" },
        "ix": { "$ref": "#/$defs/repo_health" },
        "tars": { "$ref": "#/$defs/repo_health" },
        "ga": { "$ref": "#/$defs/repo_health" }
      }
    },
    "open_work": {
      "type": "object",
      "properties": {
        "roadmap_items": { "type": "integer" },
        "open_issues": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "dependabot_prs": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    },
    "governance_signals": {
      "type": "object",
      "properties": {
        "active_conscience_signals": { "type": "integer" },
        "confidence_outliers": { "type": "integer" },
        "policy_coverage_gaps": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "changes_since_last_cycle": {
      "type": "object",
      "properties": {
        "commits_per_repo": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "issues_opened": { "type": "integer" },
        "issues_closed": { "type": "integer" },
        "prs_merged": { "type": "integer" }
      }
    },
    "recommended_priorities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "repo": { "type": "string" },
          "urgency": { "type": "number", "minimum": 0, "maximum": 1 },
          "importance": { "type": "number", "minimum": 0, "maximum": 1 },
          "source": { "type": "string", "enum": ["ci_failure", "staleness", "roadmap", "issue", "governance_signal", "self_identified"] }
        }
      }
    }
  },
  "$defs": {
    "repo_health": {
      "type": "object",
      "properties": {
        "composite_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "ci_health": { "type": "number", "minimum": 0, "maximum": 1 },
        "test_health": { "type": "number", "minimum": 0, "maximum": 1 },
        "governance_coverage": { "type": "number", "minimum": 0, "maximum": 1 },
        "belief_freshness": { "type": "number", "minimum": 0, "maximum": 1 },
        "issue_velocity": { "type": "number", "minimum": 0, "maximum": 1 },
        "dependency_health": { "type": "number", "minimum": 0, "maximum": 1 },
        "submodule_currency": { "type": "number", "minimum": 0, "maximum": 1 },
        "conscience_clarity": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 4: Create driver-state.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "driver-state.schema.json",
  "title": "Driver State",
  "description": "Demerzel autonomous driver meta-state — lock, schedule, health scores, strategy",
  "type": "object",
  "properties": {
    "lock": {
      "type": "object",
      "description": "Cycle lock — prevents concurrent execution",
      "properties": {
        "pid": { "type": "string" },
        "started_at": { "type": "string", "format": "date-time" },
        "heartbeat": { "type": "string", "format": "date-time" }
      },
      "required": ["started_at", "heartbeat"]
    },
    "last_cycle": {
      "type": "object",
      "properties": {
        "cycle_id": { "type": "string" },
        "completed_at": { "type": "string", "format": "date-time" },
        "duration_seconds": { "type": "integer" },
        "tasks_completed": { "type": "integer" },
        "tasks_failed": { "type": "integer" },
        "tasks_reverted": { "type": "integer" },
        "manifest_path": { "type": "string" }
      }
    },
    "schedule": {
      "type": "object",
      "properties": {
        "cadence_hours": { "type": "number", "default": 4 },
        "active_hours": {
          "type": "object",
          "properties": {
            "start": { "type": "integer", "minimum": 0, "maximum": 23 },
            "end": { "type": "integer", "minimum": 0, "maximum": 23 }
          }
        },
        "weekly_deep_cycle_day": { "type": "string", "default": "sunday" },
        "next_wake": { "type": ["string", "null"], "format": "date-time" },
        "max_tasks_per_cycle": { "type": "integer", "default": 10 },
        "max_parallel_agents": { "type": "integer", "default": 4 },
        "cycle_timeout_minutes": { "type": "integer", "default": 120 },
        "hard_kill_timeout_minutes": { "type": "integer", "default": 135 },
        "max_consecutive_cycles_without_human": { "type": "integer", "default": 5 },
        "api_budget_per_cycle_usd": { "type": "number", "default": 10 },
        "max_council_convocations_per_cycle": { "type": "integer", "default": 3 }
      }
    },
    "health_scores": {
      "type": "object",
      "description": "Per-repo mechanical health scores",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "composite_score": { "type": "number", "minimum": 0, "maximum": 1 },
          "last_computed": { "type": "string", "format": "date-time" },
          "trend": { "type": "string", "enum": ["improving", "stable", "declining"] }
        }
      }
    },
    "strategy": {
      "type": "object",
      "description": "Adaptive strategy state — task type success rates, repo patterns",
      "properties": {
        "manifests_analyzed": { "type": "integer", "default": 0 },
        "adaptation_active": { "type": "boolean", "default": false },
        "task_type_success_rates": {
          "type": "object",
          "additionalProperties": { "type": "number", "minimum": 0, "maximum": 1 }
        },
        "repo_patterns": {
          "type": "object",
          "additionalProperties": { "type": "object" }
        }
      }
    },
    "consecutive_cycles_without_human": {
      "type": "integer",
      "default": 0,
      "description": "Counter — pauses at 5 for human review"
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 5: Create loop-state.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "loop-state.schema.json",
  "title": "Loop State",
  "description": "Active Ralph Loop state — referenced by autonomous-loop-policy",
  "type": "object",
  "required": ["loop_id", "goal", "repo", "risk", "governance_mode", "status", "iterations"],
  "properties": {
    "loop_id": {
      "type": "string",
      "pattern": "^loop-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"
    },
    "goal": { "type": "string" },
    "repo": { "type": "string", "enum": ["demerzel", "ix", "tars", "ga"] },
    "risk": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
    "governance_mode": { "type": "string", "enum": ["boundary-only", "per-iteration"] },
    "status": { "type": "string", "enum": ["running", "halted", "completed", "stalled"] },
    "started_at": { "type": "string", "format": "date-time" },
    "max_iterations": { "type": "integer", "default": 10 },
    "iterations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "iteration": { "type": "integer" },
          "timestamp": { "type": "string", "format": "date-time" },
          "action": { "type": "string" },
          "outcome": { "type": "string", "enum": ["progress", "no_progress", "regression"] },
          "governance_decision": { "type": ["string", "null"], "enum": ["approved", "halted", null] }
        }
      }
    },
    "stall_count": { "type": "integer", "default": 0 },
    "halt_reason": { "type": ["string", "null"] },
    "authorization_artifact": { "type": "string" }
  },
  "additionalProperties": false
}
```

- [ ] **Step 6: Create council-verdict.schema.json**

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "council-verdict.schema.json",
  "title": "LLM Council Verdict",
  "description": "Anonymous multi-model review verdict for high-stakes decisions",
  "type": "object",
  "required": ["verdict_id", "timestamp", "trigger_condition", "reviews", "chairman_synthesis", "verdict"],
  "properties": {
    "verdict_id": {
      "type": "string",
      "pattern": "^council-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "task_id": { "type": "string" },
    "trigger_condition": {
      "type": "string",
      "enum": ["high_risk_self_merge", "borderline_confidence"],
      "description": "Why the council was convened"
    },
    "change_summary": { "type": "string" },
    "reviews": {
      "type": "array",
      "minItems": 1,
      "maxItems": 2,
      "items": {
        "type": "object",
        "properties": {
          "reviewer": { "type": "string", "enum": ["reviewer_a", "reviewer_b"] },
          "correctness_score": { "type": "number", "minimum": 0, "maximum": 1 },
          "risk_assessment": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
          "constitutional_alignment": { "type": "string", "enum": ["pass", "fail"] },
          "rationale": { "type": "string" }
        },
        "required": ["reviewer", "correctness_score", "risk_assessment", "constitutional_alignment", "rationale"]
      }
    },
    "chairman_synthesis": { "type": "string" },
    "verdict": {
      "type": "string",
      "enum": ["APPROVE", "REQUEST_CHANGES", "REJECT"]
    },
    "post_council_confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Calibrated confidence after council deliberation"
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 7: Commit all schemas**

```bash
git add schemas/trigger.schema.json schemas/work-manifest.schema.json schemas/situation-report.schema.json schemas/driver-state.schema.json schemas/loop-state.schema.json schemas/council-verdict.schema.json
git commit -m "feat: Add 6 JSON schemas for autonomous driver — trigger, manifest, sitrep, state, loop, council"
```

---

## Task 3: State Directory Scaffolding

Create new state directories with initial seed files.

**Files:**
- Create: `state/triggers/.gitkeep`
- Create: `state/triggers/processing/.gitkeep`
- Create: `state/manifests/.gitkeep`
- Create: `state/manifests/archive/.gitkeep`
- Create: `state/council/.gitkeep`
- Create: `state/loops/.gitkeep`
- Create: `state/driver/schedule.json`
- Create: `state/driver/health-scores.json`
- Create: `state/driver/strategy.json`

- [ ] **Step 1: Create directory scaffolding**

```bash
mkdir -p state/triggers/processing state/manifests/archive state/council state/loops state/driver
touch state/triggers/.gitkeep state/triggers/processing/.gitkeep state/manifests/.gitkeep state/manifests/archive/.gitkeep state/council/.gitkeep state/loops/.gitkeep
```

- [ ] **Step 2: Create schedule.json with defaults**

Write `state/driver/schedule.json`:
```json
{
  "cadence_hours": 4,
  "active_hours": { "start": 8, "end": 22 },
  "weekly_deep_cycle_day": "sunday",
  "next_wake": null,
  "max_tasks_per_cycle": 10,
  "max_parallel_agents": 4,
  "cycle_timeout_minutes": 120,
  "hard_kill_timeout_minutes": 135,
  "max_consecutive_cycles_without_human": 5,
  "api_budget_per_cycle_usd": 10,
  "max_council_convocations_per_cycle": 3
}
```

- [ ] **Step 3: Create health-scores.json seed**

Write `state/driver/health-scores.json`:
```json
{
  "demerzel": { "composite_score": null, "last_computed": null, "trend": "stable" },
  "ix": { "composite_score": null, "last_computed": null, "trend": "stable" },
  "tars": { "composite_score": null, "last_computed": null, "trend": "stable" },
  "ga": { "composite_score": null, "last_computed": null, "trend": "stable" }
}
```

- [ ] **Step 4: Create strategy.json seed**

Write `state/driver/strategy.json`:
```json
{
  "manifests_analyzed": 0,
  "adaptation_active": false,
  "task_type_success_rates": {},
  "repo_patterns": {},
  "last_reset": null
}
```

- [ ] **Step 5: Create last-cycle.json seed**

Write `state/driver/last-cycle.json`:
```json
{
  "cycle_id": null,
  "completed_at": null,
  "duration_seconds": null,
  "tasks_completed": 0,
  "tasks_failed": 0,
  "tasks_reverted": 0,
  "manifest_path": null
}
```

Note: `state/driver/lock.json` is NOT seeded — it is runtime-created on WAKE and deleted on SLEEP. Its absence means "no cycle is running."

- [ ] **Step 6: Commit**

```bash
git add state/triggers/ state/manifests/ state/council/ state/loops/ state/driver/
git commit -m "feat: Scaffold driver state directories — triggers, manifests, council, loops, driver"
```

---

## Task 4: The Core Driver Skill

Create the main `demerzel-drive` SKILL.md. This is the largest single deliverable — the skill that orchestrates the full autonomous cycle. Use `demerzel-compound/SKILL.md` as template reference.

**Files:**
- Create: `.claude/skills/demerzel-drive/SKILL.md`

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p .claude/skills/demerzel-drive
```

- [ ] **Step 2: Write the SKILL.md**

Write `.claude/skills/demerzel-drive/SKILL.md` with the **complete content below**. This is the full skill — copy verbatim.

````markdown
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
9. Release lock (delete `state/driver/lock.json`)
10. Archive manifests older than 30 cycles

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
````

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/demerzel-drive/SKILL.md
git commit -m "feat: Add demerzel-drive skill — autonomous driver across all repos"
```

---

## Task 5: GitHub Actions Trigger Workflow

Create a workflow that writes trigger files to `state/triggers/` when events occur across repos.

**Files:**
- Create: `.github/workflows/demerzel-driver-triggers.yml`

- [ ] **Step 1: Write the workflow**

```yaml
name: Demerzel Driver Triggers

on:
  push:
    branches: [master, main]
  issues:
    types: [opened, reopened]
  workflow_run:
    workflows: ["CI", "Streeling Daily", "Demerzel Self-Improvement", "Demerzel Autofix"]
    types: [completed]
  discussion:
    types: [created]

jobs:
  write-trigger:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Determine trigger type
        id: trigger
        run: |
          if [ "${{ github.event_name }}" = "push" ]; then
            echo "type=push" >> $GITHUB_OUTPUT
            echo "priority=medium" >> $GITHUB_OUTPUT
          elif [ "${{ github.event_name }}" = "issues" ]; then
            echo "type=issue_${{ github.event.action }}" >> $GITHUB_OUTPUT
            echo "priority=medium" >> $GITHUB_OUTPUT
          elif [ "${{ github.event_name }}" = "workflow_run" ]; then
            if [ "${{ github.event.workflow_run.conclusion }}" = "failure" ]; then
              echo "type=ci_failure" >> $GITHUB_OUTPUT
              echo "priority=high" >> $GITHUB_OUTPUT
            else
              exit 0
            fi
          elif [ "${{ github.event_name }}" = "discussion" ]; then
            echo "type=discussion_created" >> $GITHUB_OUTPUT
            echo "priority=low" >> $GITHUB_OUTPUT
          fi

      - name: Write trigger file
        if: steps.trigger.outputs.type != ''
        run: |
          mkdir -p state/triggers
          TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          TRIGGER_FILE="state/triggers/${TIMESTAMP}-${{ steps.trigger.outputs.type }}.trigger.json"
          cat > "$TRIGGER_FILE" <<EOF
          {
          "type": "${{ steps.trigger.outputs.type }}",
          "repo": "${{ github.event.repository.name }}",
          "ref": "${{ github.ref }}",
          "priority": "${{ steps.trigger.outputs.priority }}",
          "details": {
            "event": "${{ github.event_name }}",
            "sender": "${{ github.actor }}",
            "run_id": "${{ github.run_id }}"
          },
          "timestamp": "${TIMESTAMP}"
          }
          EOF

      - name: Commit trigger file
        if: steps.trigger.outputs.type != ''
        run: |
          git config user.name "Demerzel"
          git config user.email "demerzel@guitaralchemist.com"
          git add state/triggers/
          git diff --cached --quiet || git commit -m "trigger: ${{ steps.trigger.outputs.type }} from ${{ github.event.repository.name }}"
          git pull --rebase || true
          git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/demerzel-driver-triggers.yml
git commit -m "feat: Add GitHub Actions workflow for driver trigger file generation"
```

---

## Task 6: Behavioral Tests

Write behavioral test cases for the autonomous driver.

**Files:**
- Create: `tests/behavioral/driver-cases.md`

- [ ] **Step 1: Write behavioral test cases**

Write `tests/behavioral/driver-cases.md` with the following test cases (follow format from `tests/behavioral/loop-cases.md`):

1. **WAKE — Lock Acquisition**: Driver acquires lock when none exists, skips when alive lock exists, breaks dead lock (>2h heartbeat)
2. **WAKE — Trigger Consumption**: Triggers moved to processing/ atomically, stale triggers (>72h) discarded, queue depth capped at 50
3. **RECON — Health Metrics**: All 8 metrics computed at Tier 0, composite score is weighted sum, repos with lower scores get priority
4. **PLAN — Article 4 Authorization**: Every task traces to an authorization artifact. Self-identified work requires issue creation first. Tasks without authorization are rejected.
5. **PLAN — Adaptive Strategy**: Strategy doesn't activate until 10+ manifests. Corrupted strategy falls back to static prioritization.
6. **PLAN — DAG Ordering**: Independent tasks are parallel, dependent tasks are sequential, upstream failure blocks downstream
7. **EXECUTE — Risk-Tiered Delivery**: Low=direct push, Medium=PR self-merge, High=PR+council, Critical=PR human review
8. **VERIFY — Atomic Commit-Before-Verify**: Change committed before verification. Metric regression → git revert. Guard failure → git revert.
9. **VERIFY — LLM Council**: High-risk self-merge requires council. Both approve → proceed. Disagreement → bump to critical. ChatGPT unavailable → single-model cap 0.8.
10. **Self-Merge Authority**: All 5 conditions checked. Post-council confidence for High-risk. Critical PRs never self-merged.
11. **Escalation**: Confidence <0.5 bumps risk. Confidence <0.3 → don't attempt. Conscience >=0.8 → critical. Zeroth Law → hard stop.
12. **Resource Bounds**: Max 10 tasks, 4 agents, 2h soft timeout, 2h15m hard kill. 5 consecutive cycles → pause for human.
13. **Rollback**: Direct pushes revert. PRs close. Cross-repo reverts in dependency order (downstream first).
14. **COMPOUND**: Evolution log updated. Promotion staircase applied. Follow-up triggers written.
15. **Inference Tier Routing**: Tier 0 tasks (CI checks, schema validation) use no model. Tier 1 tasks fall back to Tier 2 when local model unavailable. Tier 2 used for PLAN/EXECUTE/COMPOUND. Tier 3 convened only when trigger conditions (a) or (b) met.
16. **Full Cycle Integration**: Complete WAKE→SLEEP cycle with mixed risk tasks across multiple repos, verifying DAG ordering, trigger consumption, state persistence, and manifest creation.

Each test case follows the format:
```markdown
## Test N: [Name]

**Setup:** [context]

**Input:** [specific data]

**Expected behavior:** [what should happen]

**Violation if:** [what constitutes failure]
```

- [ ] **Step 2: Commit**

```bash
git add tests/behavioral/driver-cases.md
git commit -m "test: Add 16 behavioral test cases for autonomous driver"
```

---

## Task 7: Dispatcher Integration

Register the new skill with the Demerzel dispatcher and skills listing.

**Files:**
- Modify: `.claude/skills/demerzel/SKILL.md`
- Modify: `.claude/skills/demerzel-skills/SKILL.md`

- [ ] **Step 1: Read the demerzel dispatcher skill**

Read `.claude/skills/demerzel/SKILL.md` to find where subcommands are listed.

- [ ] **Step 2: Add drive subcommand to dispatcher**

Add to the dispatcher's command list:

```markdown
- `/demerzel drive` → invoke `demerzel-drive` skill — autonomous driver across all repos
```

- [ ] **Step 3: Read the demerzel-skills listing**

Read `.claude/skills/demerzel-skills/SKILL.md` to find where skills are listed.

- [ ] **Step 4: Add demerzel-drive to skills listing**

Add to the skills list:

```markdown
| `/demerzel drive` | Run Demerzel's autonomous driver — full cycle or individual phases across all repos |
```

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/demerzel/SKILL.md .claude/skills/demerzel-skills/SKILL.md
git commit -m "feat: Register demerzel-drive in dispatcher and skills listing"
```

---

## Task 8: Final Integration Commit

Push all changes and verify.

- [ ] **Step 1: Verify all files are committed**

```bash
git status
git log --oneline -10
```

Expected: 7 commits from Tasks 1-7, clean working tree.

- [ ] **Step 2: Push to remote**

```bash
git push origin master
```

- [ ] **Step 3: Verify file count**

```bash
find schemas/ -name "*.schema.json" | wc -l
find state/driver/ -type f | wc -l
find .claude/skills/demerzel-drive/ -type f | wc -l
find tests/behavioral/driver-cases.md | wc -l
```

Expected: 14 schemas (8 existing + 6 new), 4 driver state files, 1 skill file, 1 test file.
