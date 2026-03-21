# MCP Orchestration Grammar (MOG) Design

**Date:** 2026-03-21
**Scope:** Demerzel governance artifacts only (grammar, schemas, policies, pipeline definitions, behavioral tests). No runtime code — executor implementations live in consumer repos (tars/ix).

---

## Overview

The MCP Orchestration Grammar (MOG) is a formal grammar for defining processing pipelines that chain MCP tool invocations with governance gates, named bindings, shared context, parallel branches, and mandatory compounding. Think n8n meets formal grammars meets constitutional governance.

**Design principles:**
- General-purpose grammar with concrete instances (driver cycle, teaching, meta-compounding)
- Risk-based governance gates (inherits from alignment policy fuzzy thresholds)
- Named bindings for explicit data wiring + context accumulator for shared state
- Sequential with parallel branches (not full DAG)
- Hybrid compounding: auto-injected by default, suppressible with logged justification

**Inspiration:** n8n visual workflow builder formalized as EBNF, with Demerzel's constitutional guardrails at every step.

---

## Grammar Core

```ebnf
(* MCP Orchestration Grammar — Demerzel *)
(* Formal definitions for MCP tool chaining with governance gates *)
(* Consumed by: tars (F# executor), ix (Rust executor) *)

(* ============================================================ *)
(* 1. Pipeline Structure                                        *)
(* ============================================================ *)

pipeline ::= "pipeline" identifier "(" parameter_list? ")" "{"
               context_init*
               step+
               compound_phase_or_opt_out
             "}"

parameter_list ::= parameter ("," parameter)*
parameter ::= identifier (":" type_hint)?

context_init ::= "context." identifier "=" expression

(* ============================================================ *)
(* 2. Steps                                                     *)
(* ============================================================ *)

step ::= simple_step
       | parallel_block
       | conditional_step

simple_step ::= binding? invocation gate?

binding ::= identifier "="

invocation ::= tool_invocation | builtin_call

tool_invocation ::= mcp_tool "(" argument_list? ")"

builtin_call ::= builtin_function "(" argument_list? ")"

builtin_function ::= "generate_id" | "execute_tasks" | "verify" | "synthesize"
                   | "harvest" | "check_promotion_candidates"
                   | "detect_knowledge_gaps" | "detect_governance_waste"
                   | "cycle_report" | "teaching_summary" | "compound_report"
                   | "gap_issue"
                   (* Built-in pipeline functions — implemented by executor, not MCP tools *)

argument_list ::= argument ("," argument)*
argument ::= expression | identifier ":" expression    (* positional or named *)

(* ============================================================ *)
(* 3. Governance Gates                                          *)
(* ============================================================ *)

(* Gates extend fuzzy_guard from grammars/state-machines.ebnf *)
(* MOG adds comparison operators to membership tests *)
gate ::= "when" mog_guard
       | "ungated" "(" "reason" ":" string_literal ")"   (* explicit opt-out, logged as conscience signal *)

mog_guard ::= membership_test
            | semantic_predicate
            | mog_guard "&&" mog_guard

membership_test ::= truth_value "(" comparison_op? threshold ")"
truth_value ::= "T" | "F" | "U" | "C"
comparison_op ::= ">=" | "<=" | ">" | "<"              (* default: >= when omitted *)
threshold ::= number_literal

semantic_predicate ::= "?" string_literal                (* natural language guard — opaque string evaluated by executor LLM, not parsed structurally *)

(* Risk-based auto-gates — applied by engine based on tool catalog *)
(* Low risk: no gate, Medium: confidence check, High: full fuzzy, Critical: pre-mortem *)

(* ============================================================ *)
(* 4. Control Flow                                              *)
(* ============================================================ *)

parallel_block ::= "parallel" "{" step ("," step)+ "}"

conditional_step ::= "if" fuzzy_guard "{" step+ "}" ("else" "{" step+ "}")?

(* ============================================================ *)
(* 5. Compound Phase                                            *)
(* ============================================================ *)

compound_phase_or_opt_out ::= compound_phase
                            | "nocompound" "(" "reason" ":" string_literal ")"   (* logged, triggers conscience signal *)
                            |                                                    (* absent = auto-inject default compound *)

compound_phase ::= "compound" "{"
                     "harvest" "(" expression ")"
                     ("promote_if" "(" promotion_criteria ")")?
                     ("teach" "(" expression "->" identifier ")")?
                   "}"

promotion_criteria ::= expression                      (* e.g., pattern.citations >= 3 *)

(* ============================================================ *)
(* 6. MCP Tool References                                       *)
(* ============================================================ *)

mcp_tool ::= namespace "." method

namespace ::= "context7" | "notebooklm" | "openai" | "claude_mem"
            | "windows" | "discord" | "gh" | "sympy"
            | "demerzel" | "seldon" | "conscience"

(* Tool method names are validated against policies/mcp-tool-catalog.yaml *)

(* ============================================================ *)
(* 7. Expressions                                               *)
(* ============================================================ *)

expression ::= identifier
             | identifier "." identifier                (* binding.field or context.field *)
             | string_literal
             | number_literal
             | boolean_literal
             | json_literal                             (* for complex arguments like pre-mortem actions *)
             | function_call
             | expression "+" expression                (* string concatenation *)
             | expression comparison_op expression      (* comparisons for promotion_criteria *)
             | expression "&&" expression               (* boolean AND *)
             | expression "||" expression               (* boolean OR *)

boolean_literal ::= "true" | "false"
json_literal ::= "{" json_pairs "}"                     (* inline JSON for structured arguments *)
json_pairs ::= json_pair ("," json_pair)*
json_pair ::= string_literal ":" expression

function_call ::= identifier "(" argument_list? ")"

(* ============================================================ *)
(* 8. Primitives                                                *)
(* ============================================================ *)

identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
string_literal ::= '"' [^"]* '"'
number_literal ::= [0-9]+ ("." [0-9]+)?
type_hint ::= "string" | "list" | "repo" | "belief" | "any"
```

---

## Tool Catalog

> **Note:** The partial tool listing below is a design-time reference. The full 151-tool tars MCP inventory is maintained at `state/tool-catalogs/tars-mcp-tools.json`, which replaces this partial list as the authoritative catalog. See `docs/grammar-pipeline.md` for how tool invocations flow through the grammar pipeline.

### Read-Only Tools (Low Risk — No Gate)

| Node | MCP Source | Description |
|------|-----------|-------------|
| `context7.query(library, topic)` | context7 | Fetch library documentation |
| `context7.resolve(library)` | context7 | Resolve library ID |
| `sympy.solve(equation)` | sympy-mcp | Symbolic equation solving |
| `sympy.diff(expression, var)` | sympy-mcp | Symbolic differentiation |
| `sympy.integrate(expression, var)` | sympy-mcp | Symbolic integration |
| `sympy.simplify(expression)` | sympy-mcp | Algebraic simplification |
| `sympy.fit_powerlaw(data)` | sympy-mcp | Power law distribution fitting (fractal analysis) |
| `notebooklm.ask(question, notebook?)` | notebooklm | Research with source citations |
| `notebooklm.list()` | notebooklm | List available notebooks |
| `claude_mem.search(query)` | claude-mem | Recall from persistent memory |
| `windows.screenshot()` | windows-mcp | Capture screen state |

### Side-Effect Tools (Medium Risk — Confidence Check)

| Node | MCP Source | Description |
|------|-----------|-------------|
| `openai.consult(prompt)` | openai-chat | Cross-model second opinion |
| `claude_mem.save(key, value)` | claude-mem | Persist to cross-session memory |
| `discord.post(channel, embed)` | Discord API | Post governance reports |
| `gh.discussion(action, repo, content)` | GitHub CLI | Post to discussions |

### Governance Tools (High Risk — Full Fuzzy Gate)

| Node | MCP Source | Description |
|------|-----------|-------------|
| `demerzel.recon(repo)` | skill | Three-tier reconnaissance |
| `seldon.teach(topic, learner)` | skill | Knowledge transfer |
| `seldon.research(question)` | skill | Deep research (multi-source) |
| `windows.type(text)` | windows-mcp | Desktop text input |
| `windows.app(name)` | windows-mcp | Launch/control applications |
| `gh.issue(action, repo, content)` | GitHub CLI | Create/close/comment issues |

### Critical Tools (Pre-mortem Required)

| Node | MCP Source | Description |
|------|-----------|-------------|
| `demerzel.audit(level)` | skill | Governance integrity audit |
| `conscience.premortem(action)` | schema | Anticipatory ethics check |
| `demerzel.promote(artifact)` | skill | Promote pattern → policy → constitutional |

---

## Pipeline Context Schema

The shared context is a governance belief state that accumulates through the pipeline:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/pipeline-context",
  "title": "Pipeline Context",
  "description": "Shared state accumulating through an MCP orchestration pipeline",
  "type": "object",
  "required": ["pipeline_id", "initiated_by", "started_at", "beliefs", "bindings", "risk_level", "governance"],
  "properties": {
    "pipeline_id": { "type": "string", "pattern": "^pipe-\\d{4}-\\d{2}-\\d{2}-\\d{3}$" },
    "pipeline_name": { "type": "string" },
    "initiated_by": { "type": "string" },
    "started_at": { "type": "string", "format": "date-time" },
    "completed_at": { "type": ["string", "null"], "format": "date-time" },
    "beliefs": {
      "type": "object",
      "description": "Tetravalent/fuzzy beliefs accumulated during pipeline",
      "additionalProperties": {
        "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution"
      }
    },
    "bindings": {
      "type": "object",
      "description": "Named outputs from steps — immutable once set",
      "additionalProperties": true
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Auto-escalates to highest risk tool encountered — never goes down"
    },
    "governance": {
      "type": "object",
      "required": ["gates_passed", "gates_failed", "gates_skipped", "escalations", "confidence", "pre_mortems_run", "conscience_signals"],
      "additionalProperties": false,
      "properties": {
        "gates_passed": { "type": "integer", "minimum": 0 },
        "gates_failed": { "type": "integer", "minimum": 0 },
        "gates_skipped": { "type": "integer", "minimum": 0, "description": "ungated steps" },
        "escalations": { "type": "integer", "minimum": 0 },
        "confidence": {
          "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution",
          "description": "Pipeline overall confidence — starts at pure-U, sharpens as steps complete"
        },
        "pre_mortems_run": { "type": "integer", "minimum": 0 },
        "conscience_signals": { "type": "integer", "minimum": 0 }
      }
    },
    "steps_completed": { "type": "integer", "minimum": 0 },
    "steps_total": { "type": "integer", "minimum": 0 },
    "compound_depth": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2,
      "description": "Recursion depth for meta-compounding — max 2 to prevent infinite loops"
    }
  }
}
```

### Context Rules

- **beliefs**: Tetravalent/fuzzy beliefs accumulated during pipeline. Each step can assert or update beliefs.
- **bindings**: Named outputs from steps. Immutable once set — a step cannot overwrite another step's binding.
- **governance.confidence**: The pipeline's overall fuzzy confidence. Starts at `{T:0, F:0, U:1.0, C:0}` (pure unknown), sharpens as steps complete successfully. If C ever crosses 0.3, the pipeline pauses for escalation.
- **risk_level**: Auto-escalates to the highest risk tool encountered. Never goes down within a pipeline (matches existing risk escalation grammar in state-machines.ebnf section 5).
- **compound_depth**: Prevents infinite meta-compounding recursion. Default max: 2.

### Data Flow Model

Steps interact with data through two mechanisms:

1. **Named bindings** — explicit wiring between steps. A step writes `docs = context7.query("topic")`, later steps read `docs`. Immutable: prevents accidental overwrites.

2. **Context accumulator** — shared state that steps read from and enrich. `context.beliefs`, `context.governance`. Mutable: each step can update beliefs and governance metrics.

Bindings carry concrete data (documents, verdicts, reports). Context carries governance state (confidence, risk, beliefs). Both are available to every step.

---

## Risk-Based Gate Classification

Extends `policies/alignment-policy.yaml` with pipeline-specific rules:

| Risk Level | Auto-Gate | Tool Examples | Behavior |
|-----------|-----------|---------------|----------|
| Low | None | context7.query, notebooklm.ask, claude_mem.search | Flow freely — read-only, no side effects |
| Medium | `when T(0.7)` | openai.consult, claude_mem.save, discord.post | Confidence check — proceed if T-membership ≥ 0.7 |
| High | `when T(0.7) && C(<0.1)` | demerzel.recon, seldon.teach, gh.issue | Full fuzzy gate — high T, low contradiction, logged |
| Critical | Pre-mortem | demerzel.audit, demerzel.promote, conscience.premortem | Pre-mortem required — logotron check before execution |

**Gate overrides:**
- `when <stricter_guard>` — override UP (always allowed)
- `ungated reason:"justification"` — override DOWN (logged as conscience signal, never silent)

---

## Concrete Pipeline Instances

### Driver Cycle Pipeline (`pipelines/driver-cycle.mog`)

```
pipeline driver_cycle(repos: list) {
  context.cycle_id = generate_id()
  context.beliefs.repos_healthy = { "T": 0.0, "F": 0.0, "U": 1.0, "C": 0.0 }
}

  triggers = claude_mem.search("pending triggers")

  parallel {
    health_demerzel = demerzel.recon("demerzel"),
    health_ix = demerzel.recon("ix"),
    health_tars = demerzel.recon("tars"),
    health_ga = demerzel.recon("ga")
  }

  plan = seldon.research("prioritize tasks from health scores")

  if T(0.7) && ?"actionable tasks found" {
    results = execute_tasks(plan.tasks)
    verified = verify(results) when T(0.5)
  }

  discord.post("general", cycle_report(context))

  compound {
    harvest(context)
    promote_if(pattern.citations >= 3)
    teach(context.learnings -> seldon)
  }
```

### Seldon Research Pipeline (`pipelines/seldon-research.mog`)

```
pipeline seldon_research(question: string, learner: string) {
  context.question = question
  context.beliefs.answer_quality = { "T": 0.0, "F": 0.0, "U": 1.0, "C": 0.0 }
}

  docs = context7.query(question)
  notebook_answer = notebooklm.ask(question)
  second_opinion = openai.consult(question + notebook_answer)

  prior = claude_mem.search(question)

  if C(0.2) && ?"answers conflict" {
    conscience.premortem({
      "action": "deliver potentially contradictory answer",
      "blast_radius": "single-repo"
    })
  }

  synthesis = synthesize(docs, notebook_answer, second_opinion, prior)

  if ?"learner specified" {
    seldon.teach(synthesis, learner)
    discord.post("general", teaching_summary(synthesis))
  }

  claude_mem.save("research:" + question, synthesis)

  compound {
    harvest(context)
    promote_if(synthesis.novel_finding)
    teach(context.learnings -> seldon)
  }
```

### Meta-Compounding Pipeline (`pipelines/meta-compound.mog`)

```
pipeline meta_compound(completed_pipeline: string) {
  context.source_pipeline = completed_pipeline
  context.compound_depth = context.compound_depth + 1
}

  learnings = harvest(completed_pipeline)

  parallel {
    evolution = check_promotion_candidates(learnings),
    gaps = detect_knowledge_gaps(learnings),
    waste = detect_governance_waste(learnings)
  }

  if ?"promotion candidates found" {
    conscience.premortem({
      "action": "promote " + evolution.candidates,
      "irreversibility": "medium"
    }) when T(0.7)
  }

  if ?"knowledge gaps detected" {
    seldon.teach(gaps -> seldon)
    gh.issue("create", "demerzel", gap_issue(gaps))
  }

  discord.post("general", compound_report(context))

  compound {
    harvest(context)
    promote_if(meta_insight_found)
    teach(context.learnings -> seldon)
  }
```

**Recursion bound:** `compound_depth` increments at each meta-compound invocation. When `compound_depth >= 2`, the compound phase becomes a no-op (logged, not errored). This prevents infinite "compounding the compounding of the compounding."

### Governance Reflection Pipeline (`pipelines/governance-reflection.mog`)

A structured reflection cycle that runs after each driver cycle (or weekly). Not a Scrum retrospective — a governance-native reflection through the fractal compounding lens.

```
pipeline governance_reflection(cycle_id: string) {
  context.reflection_type = "post-cycle"
  context.beliefs.governance_improving = { "T": 0.0, "F": 0.0, "U": 1.0, "C": 0.0 }
}

  cycle_data = claude_mem.search("cycle " + cycle_id)

  parallel {
    ergol = compute_ergol(cycle_data),
    lolli = compute_lolli(cycle_data),
    surprises = find_belief_transitions(cycle_data),
    bottlenecks = detect_bottlenecks(cycle_data)
  }

  dimension = sympy.solve("log(ergol.value) / log(ergol.scale)")
  momentum = sympy.diff("beliefs_T_gained - beliefs_T_lost", "cycle")

  if ?"LOLLI growing faster than ERGOL" {
    inflation_alert = conscience.premortem({
      "action": "governance may be inflating — artifacts growing without value",
      "irreversibility": "low",
      "blast_radius": "ecosystem"
    })
  }

  if ?"bottlenecks detected" {
    parallel {
      improvement = seldon.research("how to resolve: " + bottlenecks.top),
      issue = gh.issue("create", "demerzel", bottleneck_issue(bottlenecks.top))
    }
  }

  reflection = synthesize_reflection({
    "what_created_value": ergol,
    "what_was_waste": lolli,
    "what_surprised_us": surprises,
    "compounding_dimension": dimension,
    "learning_momentum": momentum,
    "bottlenecks": bottlenecks,
    "question": "What should we do differently next cycle?"
  })

  second_opinion = openai.consult("Review this governance reflection: " + reflection)

  discord.post("general", reflection_digest(reflection, second_opinion))

  compound {
    harvest(context)
    promote_if(reflection.recurring_insight)
    teach(context.learnings -> seldon)
  }
```

**Reflection structure (not Scrum retro — governance native):**

| Section | What it measures | Source |
|---------|-----------------|--------|
| **ERGOL** (real value created) | Beliefs U→T, health score deltas, issues closed with evidence | Fractal compounding model |
| **LOLLI** (artifact inflation) | New files without citations, policies without consumers | Economicon principle |
| **Surprises** | Unexpected belief transitions (U→C, T→F) | Tetravalent logic |
| **Compounding dimension** | D_c for this cycle — superlinear or bloating? | Fractal analysis |
| **Learning momentum** | p_L trend — accelerating or decaying? | Noether conservation |
| **Bottlenecks** | Slowest pipeline steps, most-failed gates, tools with errors | Pipeline context metrics |
| **Next cycle focus** | Synthesized recommendation + ChatGPT second opinion | Multi-model consultation |

---

## Compound Phase Behavior

### Default (no explicit compound or nocompound)

The engine auto-injects:
```
compound {
  harvest(context)
  teach(context.learnings -> seldon)
}
```

### Explicit compound

Pipeline author defines custom harvest, promotion criteria, and teaching targets.

### nocompound

```
nocompound(reason: "trivial lookup, no learnings to harvest")
```

- Triggers a `silence_discomfort` conscience signal (type: "silence_discomfort", context.source: "pipeline-nocompound")
- Logged in pipeline context: `governance.conscience_signals += 1`
- Not blocked — just noticed. The conscience tracks how often compounding is skipped and flags patterns.

---

## Connections to Existing Artifacts

| MOG Concept | Existing Artifact | Relationship |
|-------------|-------------------|--------------|
| `fuzzy_guard` in gates | `grammars/state-machines.ebnf` section 9 | Reused directly |
| Pipeline confidence | `schemas/fuzzy-distribution.schema.json` | `$ref` in context schema |
| Risk escalation | `grammars/state-machines.ebnf` section 5 | Same pattern (never goes down) |
| Gate thresholds | `policies/alignment-policy.yaml` fuzzy_thresholds | Extended with pipeline rules |
| Pre-mortem gates | `schemas/pre-mortem.schema.json` | Invoked at critical risk |
| `nocompound` signals | `policies/proto-conscience-policy.yaml` | Triggers silence_discomfort |
| Compound → promote | `grammars/state-machines.ebnf` section 4 | Promotion staircase |
| Compound → teach | `policies/streeling-policy.yaml` | Knowledge transfer protocol |
| Tool catalog risk | `policies/alignment-policy.yaml` | Extends existing confidence bands |

---

## Fractal Compounding

Meta-compounding exhibits fractal structure — the compound operation is self-similar at every scale. See `logic/fractal-compounding.md` for the full formal spec.

**Key concepts integrated into MOG:**

- **Self-similarity**: The compound phase has identical shape at step, pipeline, cycle, session, and evolution levels
- **Compounding dimension (D_c)**: Measures value density growth. Target: 1.2-1.6 (superlinear but bounded)
- **Power law detection**: SymPy MCP fits citation distributions to detect healthy vs fragile concentration
- **ERGOL vs LOLLI**: Distinguish real governance improvements from artifact inflation at every scale
- **Conservation of learning momentum**: Scale invariance (Noether/Bourbakof) conserves p_L across cycles

### Fractal Analysis Pipeline (`pipelines/fractal-analysis.mog`)

```
pipeline fractal_analysis(cycles: list) {
  context.analysis_type = "fractal"
  context.beliefs.compounding_healthy = { "T": 0.0, "F": 0.0, "U": 1.0, "C": 0.0 }
}

  citations = claude_mem.search("evolution citations")

  parallel {
    dimension = sympy.solve("log(value_ratio) / log(scale_ratio)"),
    powerlaw = sympy.fit_powerlaw(citations),
    momentum = sympy.diff("beliefs_T_gained - beliefs_T_lost", "cycle")
  }

  if ?"compounding dimension below 1.0" {
    conscience.premortem({
      "action": "governance may be bloating without real value",
      "irreversibility": "low",
      "blast_radius": "ecosystem"
    })
  }

  if ?"power law too extreme (top 5% = 90%+ citations)" {
    discord.post("general", fragility_alert(powerlaw))
  }

  ergol_ratio = compute_ergol_lolli(context)

  discord.post("general", fractal_report(dimension, powerlaw, momentum, ergol_ratio))

  compound {
    harvest(context)
    promote_if(dimension.value >= 1.2)
    teach(context.learnings -> seldon)
  }
```

---

## Artifacts Summary

| # | Artifact | Type | Path | Status |
|---|----------|------|------|--------|
| 1 | MCP Orchestration Grammar | EBNF | `grammars/mcp-orchestration.ebnf` | New |
| 2 | Pipeline context schema | JSON Schema | `schemas/pipeline-context.schema.json` | New |
| 3 | Pipeline definition schema | JSON Schema | `schemas/pipeline-definition.schema.json` | New |
| 4 | Tool catalog | YAML | `policies/mcp-tool-catalog.yaml` | New |
| 5 | Alignment policy update | YAML | `policies/alignment-policy.yaml` | Modify |
| 6 | Driver cycle pipeline | MOG | `pipelines/driver-cycle.mog` | New |
| 7 | Seldon research pipeline | MOG | `pipelines/seldon-research.mog` | New |
| 8 | Meta-compounding pipeline | MOG | `pipelines/meta-compound.mog` | New |
| 9 | Fractal analysis pipeline | MOG | `pipelines/fractal-analysis.mog` | New |
| 9b | Governance reflection pipeline | MOG | `pipelines/governance-reflection.mog` | New |
| 10 | Fractal compounding spec | Logic doc | `logic/fractal-compounding.md` | New |
| 11 | Fractal compounding tests | Behavioral | `tests/behavioral/fractal-compounding-cases.md` | New |
| 12 | MOG behavioral tests | Markdown | `tests/behavioral/mcp-orchestration-cases.md` | New |
| 13 | Pipeline state directory | Directory | `state/pipelines/` | New |

---

## Behavioral Test Cases

1. **Pipeline executes steps sequentially**: Given a 3-step pipeline, steps execute in order with bindings available to subsequent steps.
2. **Parallel block runs concurrently**: Given a parallel block with 3 recon steps, all 3 dispatch simultaneously and results merge into context.
3. **Medium risk auto-gate**: Given a discord.post step without explicit gate, engine auto-applies `when T(0.7)`. Pipeline pauses if confidence insufficient.
4. **Critical risk triggers pre-mortem**: Given a demerzel.promote step, pre-mortem auto-runs before execution. Self-referential promotions escalate.
5. **Ungated logs conscience signal**: Given `ungated reason:"..."`, step executes but conscience signal count increments.
6. **nocompound triggers signal**: Given a pipeline ending with `nocompound`, silence_discomfort signal fires. Pipeline completes but learning opportunity is flagged.
7. **Context confidence escalation**: Given steps that produce C > 0.3 in pipeline confidence, pipeline pauses for escalation.
8. **Binding immutability**: Given step A writing `docs = ...` and step B attempting `docs = ...`, step B fails — bindings are write-once.
9. **Meta-compound recursion limit**: Given compound_depth = 2, the compound phase becomes a no-op. Logged but not errored.
10. **Conditional branch on fuzzy guard**: Given `if T(0.7) { ... } else { ... }`, the correct branch executes based on context confidence.
11. **Parallel block partial gate failure**: Given a parallel block with 3 recon steps where one branch returns C > 0.3, the other two complete successfully. Pipeline continues with partial results and flags the failed branch for investigation.
12. **Tool invocation error — graceful degradation**: Given an MCP tool that times out or returns an error, the pipeline captures the error in context, marks the binding as `null`, and continues if the step was not critical-risk. Critical-risk tool errors halt the pipeline.
