# Directive: MOG Executor Implementation

**Directive ID:** DIR-2026-03-22-001
**Type:** implementation
**From:** Demerzel (Governance)
**To:** tars (F# reasoning repo)
**Priority:** High
**Issued:** 2026-03-22
**Compliance Deadline:** 2026-04-05

## Context

The MCP Orchestration Grammar (MOG) design spec defines a formal grammar for chaining MCP tool invocations with governance gates, named bindings, shared context, parallel branches, and mandatory compounding. The grammar and pipeline definitions live in Demerzel. The executor runtime lives in tars.

**Design spec:** `docs/superpowers/specs/2026-03-21-mcp-orchestration-grammar-design.md`
**Implementation plan:** `docs/superpowers/plans/2026-03-22-mog-implementation-plan.md`

## Directive

tars SHALL implement the MOG executor as a new `Tars.MOG` project with the following components:

### 1. MOG Parser (Phase 1)

- Create `src/Tars.MOG/` with AST types (`AST.fs`), lexer (`Lexer.fs`), and FParsec parser (`Parser.fs`).
- The parser MUST handle all EBNF productions from the spec: pipeline structure, parameter lists, context init, step variants (simple, parallel, conditional), gate syntax (membership tests, semantic predicates, conjunctions), expressions, and compound phase.
- All 5 concrete pipelines from the spec MUST parse without error.
- Parser errors MUST include line and column information.

### 2. Pipeline Executor (Phase 2)

- Create `Executor.fs`, `Context.fs`, `BindingStore.fs`, `ExpressionEval.fs`.
- Sequential steps execute via F# `Async` monad; parallel blocks via `Async.Parallel`.
- Bindings are write-once (immutable after first assignment). Binding conflicts halt the pipeline.
- Context accumulates governance metrics: `steps_completed`, `risk_level` (monotonically escalating), `governance.confidence` (fuzzy distribution).

### 3. Governance Gates (Phase 3)

- Create `GateEvaluator.fs`, `RiskClassifier.fs`, `PreMortem.fs`.
- Evaluate fuzzy membership tests against `context.governance.confidence`.
- Auto-classify tool risk from catalog: Low=no gate, Medium=`T(0.7)`, High=`T(0.7)&&C(<0.1)`, Critical=pre-mortem.
- Semantic predicates (`?"text"`) dispatch to LLM for boolean evaluation.
- `ungated` steps increment conscience signal count and log justification.
- C > 0.3 in pipeline confidence triggers escalation pause.

### 4. MCP Tool Integration (Phase 4)

- Create `ToolCatalog.fs`, `McpClient.fs`, `ToolDispatcher.fs`, `BuiltinRegistry.fs`.
- Load tool catalog from Demerzel's `policies/mcp-tool-catalog.yaml`.
- MCP client adapter handles timeouts, retries, error capture.
- Builtin functions (`generate_id`, `harvest`, `synthesize`, etc.) execute locally.
- Tool errors on non-critical steps bind `null` and continue; critical-risk errors halt.

## Compliance Requirements

1. **Unit tests:** Each phase MUST include unit tests in `tests/Tars.MOG.Tests/`.
2. **Schema conformance:** Pipeline context MUST conform to `schemas/pipeline-context.schema.json`.
3. **Constitution compliance:** Executor MUST enforce Articles 3 (Reversibility), 6 (Escalation), 7 (Auditability) from the default constitution.
4. **Conscience signals:** `ungated` and `nocompound` MUST emit signals per `policies/proto-conscience-policy.yaml`.

## Compliance Report

Upon completion of each phase, tars SHALL submit a compliance report to Demerzel via:
```
contracts/compliance/tars-mog-phase-{N}.compliance.md
```

Each report MUST include:
- Phase number and name
- Files created/modified
- Test results (pass/fail counts)
- Any deviations from the implementation plan with justification
- Remaining blockers for the next phase

## Reference

- Design spec: `docs/superpowers/specs/2026-03-21-mcp-orchestration-grammar-design.md`
- Implementation plan: `docs/superpowers/plans/2026-03-22-mog-implementation-plan.md`
- Pipeline context schema: `schemas/pipeline-context.schema.json`
- Alignment policy: `policies/alignment-policy.yaml`
- Proto-conscience policy: `policies/proto-conscience-policy.yaml`
- Tool catalog (to be created): `policies/mcp-tool-catalog.yaml`
