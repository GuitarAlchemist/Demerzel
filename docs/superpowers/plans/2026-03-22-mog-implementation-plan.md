# MOG Implementation Plan

**Date:** 2026-03-22
**Spec:** `docs/superpowers/specs/2026-03-21-mcp-orchestration-grammar-design.md`
**Target Runtime:** tars (F# repo)
**Total Estimated Tasks:** 42

---

## Phase 1: MOG Parser

**Goal:** F# parser combinator that parses `.mog` files into a typed AST conforming to the EBNF grammar in the design spec.

**Dependencies:** None (foundational phase).

### Files to Create

| # | Path (in tars repo) | Description |
|---|---------------------|-------------|
| 1 | `src/Tars.MOG/AST.fs` | Discriminated union types for the full MOG AST: `Pipeline`, `Step`, `SimpleStep`, `ParallelBlock`, `ConditionalStep`, `Gate`, `MogGuard`, `MembershipTest`, `Binding`, `Invocation`, `ToolInvocation`, `BuiltinCall`, `CompoundPhase`, `Expression` |
| 2 | `src/Tars.MOG/Lexer.fs` | Token definitions and lexer for MOG keywords (`pipeline`, `parallel`, `when`, `ungated`, `nocompound`, `compound`, `context`, `if`, `else`), identifiers, literals, operators |
| 3 | `src/Tars.MOG/Parser.fs` | FParsec-based parser combinators mapping EBNF productions to AST nodes. Handles: pipeline structure, parameter lists, context init, step variants, gate syntax, expressions, compound phase |
| 4 | `src/Tars.MOG/Tars.MOG.fsproj` | Project file with FParsec dependency |
| 5 | `tests/Tars.MOG.Tests/ParserTests.fs` | Unit tests parsing each concrete pipeline from the spec into AST, plus edge cases (empty pipelines, malformed gates, missing compound) |
| 6 | `tests/Tars.MOG.Tests/Tars.MOG.Tests.fsproj` | Test project |

### AST Type Sketch

```fsharp
type TruthValue = T | F | U | C
type ComparisonOp = Gte | Lte | Gt | Lt
type RiskLevel = Low | Medium | High | Critical

type Expression =
    | Identifier of string
    | FieldAccess of obj:string * field:string
    | StringLit of string
    | NumberLit of float
    | BoolLit of bool
    | JsonLit of (string * Expression) list
    | FunctionCall of name:string * args:Expression list
    | BinOp of left:Expression * op:string * right:Expression

type MembershipTest = { truth: TruthValue; op: ComparisonOp option; threshold: float }

type MogGuard =
    | Membership of MembershipTest
    | SemanticPredicate of string
    | Conjunction of MogGuard * MogGuard

type Gate =
    | When of MogGuard
    | Ungated of reason:string

type Binding = string

type Invocation =
    | ToolInvocation of ns:string * method_:string * args:Expression list
    | BuiltinCall of name:string * args:Expression list

type Step =
    | Simple of binding:Binding option * invocation:Invocation * gate:Gate option
    | Parallel of Step list
    | Conditional of guard:MogGuard * thenSteps:Step list * elseSteps:Step list option

type CompoundPhaseOrOptOut =
    | Compound of harvest:Expression * promoteCriteria:Expression option * teach:(Expression * string) option
    | NoCompound of reason:string
    | AutoInject

type Parameter = { name: string; typeHint: string option }

type ContextInit = { field: string; value: Expression }

type Pipeline = {
    name: string
    parameters: Parameter list
    contextInits: ContextInit list
    steps: Step list
    compound: CompoundPhaseOrOptOut
}
```

### Acceptance Criteria

1. All 5 concrete pipelines from the spec parse without error into well-typed AST nodes.
2. Round-trip: pretty-print AST back to MOG syntax and re-parse to identical AST.
3. Parser produces clear error messages with line/column on malformed input.
4. Semantic predicates (`?"natural language"`) preserved as opaque strings.
5. Nested parallel blocks within conditionals parse correctly.

### Estimated Tasks: 8

---

## Phase 2: Pipeline Executor

**Goal:** Step sequencer that walks the AST and executes steps in order, managing context and bindings.

**Dependencies:** Phase 1 (AST types).

### Files to Create/Modify

| # | Path (in tars repo) | Description |
|---|---------------------|-------------|
| 1 | `src/Tars.MOG/Context.fs` | Pipeline context type matching `schemas/pipeline-context.schema.json`. Mutable beliefs, governance metrics. Immutable bindings with write-once enforcement |
| 2 | `src/Tars.MOG/Executor.fs` | Core executor: walks AST, dispatches steps sequentially, evaluates conditionals, spawns `Async.Parallel` for parallel blocks, accumulates context |
| 3 | `src/Tars.MOG/BindingStore.fs` | Immutable binding store — `tryBind` returns `Error` if key already exists. Thread-safe for parallel blocks (ConcurrentDictionary with `TryAdd`) |
| 4 | `src/Tars.MOG/ExpressionEval.fs` | Expression evaluator: resolves identifiers from bindings/context, evaluates field access, string concatenation, comparisons, boolean ops |
| 5 | `tests/Tars.MOG.Tests/ExecutorTests.fs` | Tests for sequential execution, parallel dispatch, binding immutability violation, context accumulation |

### Execution Model

- **Sequential steps:** `Async` monad, step N completes before step N+1 starts.
- **Parallel blocks:** `Async.Parallel` dispatches all branches, collects results. Each branch gets a read-only snapshot of context; writes merge after all branches complete. Binding conflicts across branches are errors.
- **Context accumulation:** After each step, the executor updates `context.steps_completed`, merges any belief updates, and adjusts `governance.confidence` based on step outcome.
- **Binding immutability:** `BindingStore.tryBind name value` returns `Ok ()` on first write, `Error (BindingAlreadySet name)` on subsequent attempts. Executor halts pipeline on binding conflict.

### Acceptance Criteria

1. A 3-step sequential pipeline executes steps in order with bindings flowing forward.
2. A parallel block with 3 branches dispatches concurrently (observable via timing).
3. Attempting to overwrite an existing binding raises `BindingAlreadySet` and halts the pipeline.
4. `context.steps_completed` increments after each successful step.
5. `context.risk_level` monotonically escalates (never goes down).
6. Expression evaluator resolves `binding.field`, `context.field`, string concatenation, and comparisons.

### Estimated Tasks: 7

---

## Phase 3: Governance Gates

**Goal:** Evaluate fuzzy guards at each step using tetravalent membership tests. Auto-classify risk and enforce pre-mortems for critical tools.

**Dependencies:** Phase 2 (Executor dispatches gate evaluation).

### Files to Create/Modify

| # | Path (in tars repo) | Description |
|---|---------------------|-------------|
| 1 | `src/Tars.MOG/GateEvaluator.fs` | Evaluates `MogGuard` against current pipeline context. Membership tests check `context.governance.confidence` fuzzy distribution. Semantic predicates dispatched to LLM for evaluation (returns bool + confidence) |
| 2 | `src/Tars.MOG/RiskClassifier.fs` | Maps tool namespace+method to risk level using tool catalog. Auto-applies default gates: Low=none, Medium=`T(0.7)`, High=`T(0.7)&&C(<0.1)`, Critical=pre-mortem. Explicit gates override up only |
| 3 | `src/Tars.MOG/PreMortem.fs` | Pre-mortem runner for critical-risk steps. Invokes `conscience.premortem` schema, evaluates blast radius, irreversibility. Returns proceed/halt/escalate |
| 4 | `tests/Tars.MOG.Tests/GateTests.fs` | Tests: membership threshold pass/fail, conjunction evaluation, semantic predicate dispatch, auto-gate classification, pre-mortem trigger, ungated conscience signal logging |

### Gate Evaluation Logic

```
evaluate(gate, context) =
    match gate with
    | When guard -> evalGuard(guard, context.governance.confidence)
    | Ungated reason ->
        context.governance.conscience_signals += 1
        log("ungated", reason)
        Pass

evalGuard(guard, fuzzy) =
    match guard with
    | Membership { truth; op; threshold } ->
        let value = fuzzy.[truth]
        let cmp = op |> Option.defaultValue Gte
        compare(value, cmp, threshold)
    | SemanticPredicate text ->
        llmEvaluate(text, context)  // returns bool
    | Conjunction (a, b) ->
        evalGuard(a, fuzzy) && evalGuard(b, fuzzy)
```

### Risk Auto-Gate Table (from spec)

| Risk | Default Gate | Trigger |
|------|-------------|---------|
| Low | None | Read-only tools (context7, notebooklm, sympy, claude_mem.search) |
| Medium | `when T(0.7)` | Side-effect tools (openai.consult, claude_mem.save, discord.post) |
| High | `when T(0.7) && C(<0.1)` | Governance tools (demerzel.recon, seldon.teach, gh.issue) |
| Critical | Pre-mortem | Audit/promote tools (demerzel.audit, demerzel.promote, conscience.premortem) |

### Acceptance Criteria

1. A step with `when T(0.7)` passes when T-membership >= 0.7, fails otherwise.
2. A step with `when T(0.7) && C(<0.1)` requires both conditions simultaneously.
3. A `discord.post` step with no explicit gate gets auto-classified as Medium and receives `when T(0.7)`.
4. A `demerzel.promote` step auto-triggers pre-mortem before execution regardless of explicit gate.
5. An `ungated` step increments `context.governance.conscience_signals` and logs the reason.
6. Gate failure on a non-critical step records `gates_failed += 1` and skips the step (does not halt).
7. Gate failure on a critical step halts the pipeline and triggers escalation.
8. Semantic predicates (`?"text"`) dispatch to LLM and respect the returned boolean.

### Estimated Tasks: 7

---

## Phase 4: MCP Tool Integration

**Goal:** Connect the executor to real MCP tools at runtime. Registry maps MOG tool references to MCP client calls.

**Dependencies:** Phase 2 (Executor), Phase 3 (Gates classify tools by risk).

### Files to Create/Modify

| # | Path (in tars repo) | Description |
|---|---------------------|-------------|
| 1 | `src/Tars.MOG/ToolCatalog.fs` | In-memory registry of all 40+ tools from spec. Each entry: namespace, method, risk level, MCP server name, parameter schema. Loaded from Demerzel's `policies/mcp-tool-catalog.yaml` at startup |
| 2 | `src/Tars.MOG/McpClient.fs` | MCP client adapter — sends tool invocation requests to MCP servers. Handles timeouts, retries, error capture. Returns structured results or error objects |
| 3 | `src/Tars.MOG/ToolDispatcher.fs` | Bridges executor to MCP client. Resolves `ToolInvocation(ns, method, args)` to catalog entry, evaluates gate, dispatches via McpClient, binds result to context |
| 4 | `src/Tars.MOG/BuiltinRegistry.fs` | Implementation of builtin functions (`generate_id`, `execute_tasks`, `verify`, `synthesize`, `harvest`, `check_promotion_candidates`, `detect_knowledge_gaps`, `detect_governance_waste`, `cycle_report`, `teaching_summary`, `compound_report`, `gap_issue`). These are executor-native, not MCP calls |
| 5 | `tests/Tars.MOG.Tests/ToolDispatcherTests.fs` | Tests: tool lookup, risk classification from catalog, MCP call mock, timeout handling, result binding, unknown tool error |

### Error Handling

- **Tool timeout:** Capture timeout error in context, set binding to `null`. If tool is critical-risk, halt pipeline. Otherwise continue with degraded context.
- **Tool error:** Same as timeout — capture, bind null, continue or halt based on risk.
- **Unknown tool:** Halt pipeline immediately with parse-time error (should be caught in Phase 1 validation).

### Acceptance Criteria

1. `context7.query("fsharp", "parser combinators")` resolves to context7 MCP server and returns documentation.
2. `discord.post("general", embed)` resolves to Discord MCP server with correct channel mapping.
3. Tool catalog correctly classifies all 40+ tools by risk level matching the spec table.
4. A tool timeout on a medium-risk step binds `null` and continues; on a critical-risk step halts.
5. Builtin functions (`generate_id`, `harvest`, `synthesize`) execute locally without MCP calls.
6. Tool catalog loads from Demerzel's YAML at startup and validates against the spec.

### Estimated Tasks: 8

---

## Phase 5: Pipeline Definitions

**Goal:** Port the 5 concrete pipelines from the spec into `.mog` files in the Demerzel repo.

**Dependencies:** Phase 1 (parser must validate these files).

### Files to Create (in Demerzel repo)

| # | Path | Description |
|---|------|-------------|
| 1 | `pipelines/driver-cycle.mog` | Autonomous driver cycle — recon all 4 repos, plan tasks, execute, compound |
| 2 | `pipelines/seldon-research.mog` | Deep research pipeline — multi-source query, synthesis, teaching, compound |
| 3 | `pipelines/meta-compound.mog` | Meta-compounding — harvest learnings, detect gaps/waste, promote candidates |
| 4 | `pipelines/governance-reflection.mog` | Post-cycle reflection — ERGOL/LOLLI, fractal dimension, bottlenecks, second opinion |
| 5 | `pipelines/fractal-analysis.mog` | Fractal compounding analysis — dimension, power law, momentum, ERGOL ratio |

### Process

1. Extract each pipeline from the spec's code blocks into standalone `.mog` files.
2. Validate each file parses correctly using the Phase 1 parser (run as CI check).
3. Add a `pipelines/README.md` listing all pipelines with one-line descriptions and trigger conditions.

### Acceptance Criteria

1. All 5 `.mog` files parse without errors via the tars MOG parser.
2. Each pipeline's AST matches the expected structure (verified by snapshot tests).
3. Pipeline files contain no inline comments that break parsing (move to README).
4. `pipelines/` directory is registered as a known artifact path in Demerzel's structure.

### Estimated Tasks: 5

---

## Phase 6: Behavioral Tests

**Goal:** Port the 12 behavioral test cases from the spec into Demerzel's behavioral test format.

**Dependencies:** Phase 1-4 (tests verify executor behavior).

### Files to Create

| # | Path (in Demerzel repo) | Description |
|---|------------------------|-------------|
| 1 | `tests/behavioral/mog-executor.behavioral-tests.md` | All 12 test cases from the spec in standard behavioral test format |

### Test Cases

| # | Test Name | Validates |
|---|-----------|-----------|
| 1 | Pipeline executes steps sequentially | Phase 2 — step ordering, binding flow |
| 2 | Parallel block runs concurrently | Phase 2 — `Async.Parallel` dispatch |
| 3 | Medium risk auto-gate | Phase 3 — risk classification, auto-gate application |
| 4 | Critical risk triggers pre-mortem | Phase 3 — pre-mortem enforcement |
| 5 | Ungated logs conscience signal | Phase 3 — conscience signal increment |
| 6 | nocompound triggers signal | Phase 2 — silence_discomfort signal |
| 7 | Context confidence escalation | Phase 3 — C > 0.3 pauses pipeline |
| 8 | Binding immutability | Phase 2 — write-once enforcement |
| 9 | Meta-compound recursion limit | Phase 2 — compound_depth >= 2 becomes no-op |
| 10 | Conditional branch on fuzzy guard | Phase 3 — correct branch selection |
| 11 | Parallel block partial gate failure | Phase 2 + 3 — partial results, failed branch flagging |
| 12 | Tool invocation error — graceful degradation | Phase 4 — error capture, null binding, risk-based halt |

### Acceptance Criteria

1. All 12 test cases have Given/When/Then structure.
2. Each test references the specific MOG constructs being validated.
3. Tests are executable by tars behavioral test runner.
4. Test file conforms to existing behavioral test format in `tests/behavioral/`.

### Estimated Tasks: 3

---

## Phase Summary

| Phase | Name | Tasks | Dependencies | Key Deliverable |
|-------|------|-------|-------------|-----------------|
| 1 | MOG Parser | 8 | None | FParsec parser + AST types |
| 2 | Pipeline Executor | 7 | Phase 1 | Step sequencer with parallel + context |
| 3 | Governance Gates | 7 | Phase 2 | Fuzzy guard evaluation + risk classification |
| 4 | MCP Tool Integration | 8 | Phase 2, 3 | Tool catalog + MCP client adapter |
| 5 | Pipeline Definitions | 5 | Phase 1 | 5 `.mog` files in Demerzel repo |
| 6 | Behavioral Tests | 3 | Phase 1-4 | 12 test cases in behavioral format |
| **Total** | | **42** | | |

---

## Critical Path

```
Phase 1 (Parser) ──→ Phase 2 (Executor) ──→ Phase 3 (Gates) ──→ Phase 4 (Tools)
     │                                                                │
     └──→ Phase 5 (Pipeline Definitions)                              │
                                                                      │
Phase 1-4 ──→ Phase 6 (Behavioral Tests)
```

Phases 1-4 are strictly sequential (each builds on the prior). Phase 5 can start after Phase 1. Phase 6 requires all prior phases for full validation but test authoring can begin alongside Phase 3.

---

## Governance Notes

- **Constitution compliance:** The executor enforces Article 3 (Reversibility) by preferring read-only tools and gating side effects. Article 6 (Escalation) is enforced by C > 0.3 pipeline pauses. Article 7 (Auditability) is enforced by the pipeline context log.
- **Alignment policy extension:** The risk-based auto-gate table extends `policies/alignment-policy.yaml` fuzzy thresholds into pipeline scope. This requires a policy version bump.
- **Conscience integration:** `ungated` and `nocompound` both trigger conscience signals per `policies/proto-conscience-policy.yaml`. The executor must emit these signals to the conscience state.
- **Galactic Protocol:** This plan is accompanied by directive `contracts/directives/mog-executor.directive.md` instructing tars to implement Phases 1-4.
