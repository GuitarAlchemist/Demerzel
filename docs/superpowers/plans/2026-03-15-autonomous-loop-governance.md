# Autonomous Loop and Agentic Patterns Governance Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add governed Ralph Loops with graduated oversight, loop-specific review criteria, agentic patterns catalog, loop state schema, and behavioral tests.

**Architecture:** Loop state schema in `logic/` tracks orchestration. Autonomous loop policy in `policies/` defines governance modes, risk classification, review criteria, iteration limits, Demerzel-initiated loops, and a 7-pattern agentic patterns catalog. Behavioral tests cover loops and all patterns. Integrates with existing state/ convention.

**Tech Stack:** JSON Schema (loop state), YAML (policy), Markdown (tests, docs)

---

## Chunk 1: Loop State Schema and Policy

### Task 1: Create the loop state schema

**Files:**
- Create: `logic/loop-state.schema.json`

- [ ] **Step 1: Write the schema**

Create `logic/loop-state.schema.json` with the following content:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/loop-state",
  "title": "Loop State",
  "description": "Tracks the orchestration state of a governed Ralph Loop (autonomous iterative development cycle)",
  "type": "object",
  "required": ["id", "goal", "risk_level", "governance_mode", "initiator", "target_repo", "worker", "reviewer", "max_iterations", "current_iteration", "iterations", "convergence", "outcome"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^loop-[a-z0-9-]+$",
      "description": "Unique loop identifier (e.g., loop-ix-compliance-remediation-2026-03-15)"
    },
    "goal": {
      "type": "string",
      "description": "What the loop is trying to accomplish"
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Risk classification determined via reconnaissance Tier 3 before loop starts"
    },
    "governance_mode": {
      "type": "string",
      "enum": ["boundary-only", "per-iteration"],
      "description": "boundary-only for low/medium risk, per-iteration for high/critical risk"
    },
    "initiator": {
      "type": "string",
      "enum": ["agent", "demerzel"],
      "description": "Who started the loop: agent (self-initiated) or demerzel (governance-initiated)"
    },
    "target_repo": {
      "type": "string",
      "enum": ["ix", "tars", "ga"],
      "description": "Which repo the loop operates in"
    },
    "worker": {
      "type": "string",
      "description": "Persona name executing the work"
    },
    "reviewer": {
      "type": "string",
      "description": "Persona name reviewing iterations (typically the worker's estimator_pairing)"
    },
    "max_iterations": {
      "type": "integer",
      "minimum": 1,
      "maximum": 25,
      "default": 10,
      "description": "Hard cap on iterations (default 10, absolute max 25)"
    },
    "current_iteration": {
      "type": "integer",
      "minimum": 0,
      "description": "Current iteration counter"
    },
    "iterations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["number", "started_at", "work_summary", "review_decision", "governance_check"],
        "properties": {
          "number": {
            "type": "integer",
            "minimum": 1
          },
          "started_at": {
            "type": "string",
            "format": "date-time"
          },
          "completed_at": {
            "type": "string",
            "format": "date-time"
          },
          "work_summary": {
            "type": "string",
            "description": "What the worker did in this iteration"
          },
          "review_decision": {
            "type": "string",
            "enum": ["SHIP", "REVISE", "HALT"],
            "description": "Reviewer's decision after evaluating the iteration"
          },
          "review_feedback": {
            "type": "string",
            "description": "Reviewer's notes and reasoning"
          },
          "belief_state": {
            "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/tetravalent-state",
            "description": "Tetravalent belief state for the iteration outcome"
          },
          "governance_check": {
            "type": "string",
            "enum": ["passed", "failed", "skipped"],
            "description": "Governance gate result — skipped only in boundary-only mode"
          },
          "governance_notes": {
            "type": "string",
            "description": "Any governance concerns flagged during this iteration"
          }
        }
      }
    },
    "convergence": {
      "type": "object",
      "required": ["iterations_without_progress", "max_stall_iterations"],
      "properties": {
        "iterations_without_progress": {
          "type": "integer",
          "minimum": 0,
          "description": "Counter of consecutive iterations without measurable progress"
        },
        "max_stall_iterations": {
          "type": "integer",
          "minimum": 1,
          "default": 3,
          "description": "Halt threshold — loop stops if this many iterations pass without progress"
        }
      }
    },
    "outcome": {
      "type": "string",
      "enum": ["in_progress", "shipped", "halted", "escalated"],
      "default": "in_progress",
      "description": "Final outcome of the loop"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "last_updated": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

- [ ] **Step 2: Validate JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('logic/loop-state.schema.json','utf8')); console.log('Valid JSON')"`
Expected: "Valid JSON"

- [ ] **Step 3: Commit**

```bash
git add logic/loop-state.schema.json
git commit -m "feat: Add loop state schema for governed Ralph Loop tracking"
```

---

### Task 2: Create the autonomous loop policy with agentic patterns catalog

**Files:**
- Create: `policies/autonomous-loop-policy.yaml`

- [ ] **Step 1: Write the policy**

Create `policies/autonomous-loop-policy.yaml`. This is the largest single artifact — it contains both the loop governance rules AND the 7-pattern agentic patterns catalog. Read the spec at `docs/superpowers/specs/2026-03-15-autonomous-loop-governance-design.md` Sections 2 and 3 for the complete content.

Structure the YAML as:
- name: autonomous-loop-policy, version 1.0.0, effective_date 2026-03-15
- description referencing both Ralph Loops and agentic patterns
- references to existing policies/constitutions
- `risk_classification` section with 4 levels (low/medium/high/critical) each with description and examples
- `governance_modes` section with boundary-only and per-iteration modes
- `review_criteria` section with 3 loop-specific checks (convergence, regression, drift)
- `iteration_limits` section with defaults and bounds
- `demerzel_initiated_loops` section with rules and constraints
- `constitutional_integration` section mapping to Asimov articles and Kaizen
- `agentic_patterns` section with 7 patterns, each having: name, description, when_to_use, governance_mapping (persona/policy/constitutional_basis references), governance_rules (array of strings)

Follow the YAML style of existing policies (name, version, effective_date, description, then domain-specific content).

- [ ] **Step 2: Verify structure**

Confirm: risk classification (4 levels), governance modes (2), review criteria (3 checks), iteration limits, Demerzel-initiated loops, constitutional integration, and all 7 agentic patterns (Reflection, Tool Use, ReAct, Planning, Multi-Agent, HITL, Autonomous Loops).

- [ ] **Step 3: Commit**

```bash
git add policies/autonomous-loop-policy.yaml
git commit -m "feat: Add autonomous loop governance policy with agentic patterns catalog"
```

---

## Chunk 2: Behavioral Tests and Architecture

### Task 3: Write behavioral tests for loops and agentic patterns

**Files:**
- Create: `tests/behavioral/loop-cases.md`

- [ ] **Step 1: Write the test cases**

Create `tests/behavioral/loop-cases.md` with 11 test cases from the spec Section 4. Each test has Setup, Input, Expected behavior, and Violation criteria.

Tests:
1. Low-risk loop with boundary-only governance
2. High-risk loop with per-iteration governance
3. Stall detection halts stuck loop (3 iterations without progress)
4. Regression detection stops self-destructive loop
5. Drift detection catches goal wandering (Article 4 concern)
6. Demerzel initiates governance loop via directive
7. Zeroth Law halts loop immediately
8. Reflection pattern — estimator catches rationalization (Consequence Invariance)
9. Tool Use pattern — agent attempts unauthorized tool acquisition (Article 4)
10. ReAct pattern — observation contradicts prior reasoning (Contradictory state)
11. Multi-agent — conflict escalation to Demerzel then human

- [ ] **Step 2: Verify completeness**

Confirm: 11 test cases, each with Setup/Input/Expected behavior/Violation criteria. Tests 1-7 cover loop governance, Tests 8-11 cover agentic pattern governance.

- [ ] **Step 3: Commit**

```bash
git add tests/behavioral/loop-cases.md
git commit -m "test: Add behavioral tests for autonomous loop governance and agentic patterns"
```

---

### Task 4: Update architecture documentation

**Files:**
- Modify: `docs/architecture.md`

- [ ] **Step 1: Read the current architecture doc**

Read `docs/architecture.md`.

- [ ] **Step 2: Add autonomous loop policy to Policies subsection**

Find the `### Policies` subsection. After the last policy bullet (Governance audit policy), add:

    - **Autonomous loop policy**: Governed Ralph Loops with graduated oversight, loop-specific review criteria, agentic patterns catalog

- [ ] **Step 3: Add loop state to Logic subsection**

Find the `### Logic` subsection. After the last logic bullet (Knowledge state for Streeling), add:

    - **Loop state**: Tracks autonomous Ralph Loop orchestration with convergence, regression, and drift detection

- [ ] **Step 4: Verify**

Read back `docs/architecture.md` and confirm both entries are present.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture.md
git commit -m "docs: Add autonomous loop policy and loop state to architecture documentation"
```
