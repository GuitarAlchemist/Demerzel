# Grammar-to-DSL Pipeline Architecture

**Date:** 2026-03-21
**Scope:** Documents how Demerzel EBNF grammars flow through tars modules to become executable, self-improving grammar systems.

---

## Pipeline Overview

```
Demerzel EBNF (governance specs)
    | consumption
    v
tars WeightedGrammar (Bayesian weights per rule)
    | compilation
    v
tars WoT DSL (parser + compiler -> execution plans)
    | execution
    v
tars MCP tools (151 tools with governance gates)
    | distillation
    v
tars GrammarDistillation (extract patterns from traces)
    | promotion
    v
Demerzel evolution log (U->T belief transitions)
```

This is a closed loop: grammars define structure, execution generates traces, distillation extracts new patterns, and successful patterns promote back into the grammar system.

---

## Stage 1: Demerzel EBNF Grammars (Source of Truth)

### What happens

Demerzel defines domain grammars as EBNF specifications. These are pure governance artifacts -- no runtime code. Each grammar encodes the valid structure of reasoning in a specific domain.

**Input:** Domain knowledge + governance constraints
**Transformation:** Human/AI authoring against constitution hierarchy
**Output:** `.ebnf` files in `grammars/`

### Demerzel artifacts

| Grammar | Domain | Department |
|---------|--------|------------|
| `grammars/scientific-method.ebnf` | Hypothesis-experiment-conclusion cycles | Research Methods |
| `grammars/state-machines.ebnf` | Tetravalent logic, fuzzy guards, promotion staircase | Core Governance |
| `grammars/music-theory.ebnf` | Scales, chords, progressions, voice leading | Music Theory |
| `grammars/guitar-technique.ebnf` | Fingering, picking, fretting patterns | Guitar Studies |
| `grammars/musicology-analysis.ebnf` | Formal analysis, style periods, cultural context | Musicology |
| `grammars/mathematical-proof.ebnf` | Axiom-lemma-theorem-proof structure | Mathematics |
| `grammars/acoustics-physics.ebnf` | Wave equations, resonance, psychoacoustics | Acoustics / Physics |
| `grammars/algorithms.ebnf` | Complexity, correctness, data structure selection | Computer Science |
| `grammars/psychohistory.ebnf` | Population dynamics, probabilistic prediction | Psychohistory (Seldon Plan) |

### tars counterparts (governance grammars)

tars maintains its own governance-specific EBNFs that consume Demerzel schema definitions:

| Grammar | Purpose | Path |
|---------|---------|------|
| `belief-snapshot.ebnf` | Serialization of tetravalent belief states | `v2/grammars/governance/` |
| `compliance-report.ebnf` | Galactic Protocol compliance output | `v2/grammars/governance/` |
| `governance-directive.ebnf` | Directive consumption from Demerzel | `v2/grammars/governance/` |
| `pdca-state.ebnf` | PDCA cycle state tracking | `v2/grammars/governance/` |

### Governance gates

- Constitutions are append-only (removals need explicit justification)
- New grammars must align with Asimov constitution Articles 0-5
- Grammar changes trigger schema validation against `schemas/persona.schema.json` when grammars reference persona capabilities

### Status: **Implemented**

All 9 Demerzel grammars and 4 tars governance grammars are authored and versioned.

---

## Stage 2: WeightedGrammar (Bayesian Weight Layer)

### What happens

tars wraps Demerzel's deterministic EBNF rules with probabilistic weights. Each rule gets a weight in [0.0, 1.0], a confidence score, and a success rate tracked from execution outcomes. This converts structural grammar into a PCFG (Probabilistic Context-Free Grammar) that steers rule selection.

**Input:** EBNF rules + execution history
**Transformation:** Softmax normalization + Bayesian update from outcomes
**Output:** `WeightedRule` records with `Weight`, `Confidence`, `SuccessRate`, `SelectionCount`

### tars modules involved

| Module | Path | Role |
|--------|------|------|
| `WeightedGrammar` | `v2/src/Tars.Evolution/WeightedGrammar.fs` | Core weight management, Bayesian updates, softmax normalization |
| `GrammarGovernor` | `v2/src/Tars.Evolution/GrammarGovernor.fs` | Policy enforcement on promotions (8-criteria scoring, 6/8 approval threshold) |
| `GrammarMlBridge` | `v2/src/Tars.Evolution/GrammarMlBridge.fs` | Feature extraction for ML prediction of rule success |

### Key types

- `WeightedRule` -- grammar rule annotated with weight, confidence, success rate, selection count, source attribution
- `WeightConfig` -- softmax temperature, decay factor, minimum weight floor, prior success rate
- `RuleSource` -- tracks provenance: `Tars | GuitarAlchemist | MachinDeOuf | Evolved | Manual`
- `PromotionCriteria` -- 8 criteria evaluated by GrammarGovernor for promotion decisions

### Three-force architecture

The WeightedGrammar documentation describes three forces that govern rule evolution:

1. **Grammar constraints** (EBNF, WoT DSL) -- guarantees structural validity
2. **PCFG weights** (WeightedGrammar) -- steers probabilistic preferences
3. **Semantic validation** (GrammarGovernor) -- catches nonsensical compositions

### Demerzel artifacts that participate

- `policies/alignment-policy.yaml` -- confidence thresholds that map to weight floors
- `grammars/state-machines.ebnf` section 4 -- promotion staircase that GrammarGovernor enforces
- `schemas/fuzzy-distribution.schema.json` -- tetravalent confidence representation

### Governance gates

- GrammarGovernor enforces 8-criteria scoring:
  - Approve: >= 6/8 criteria AND minimum occurrences met
  - Defer: 4-5/8 criteria (needs more evidence)
  - Reject: < 4/8 criteria OR insufficient occurrences
- Promotions to `DslClause` level and above require a rollback expansion path
- Overlap detection prevents duplicate patterns at the same promotion level

### MCP tool interface

| Tool | Operation |
|------|-----------|
| `grammar_weights` | View current rule weights and statistics |
| `grammar_update` | Submit execution outcome for Bayesian weight update |

### Status: **Implemented**

WeightedGrammar, GrammarGovernor, and GrammarMlBridge are complete in tars v2. MCP tools for weight viewing and Bayesian update are registered.

---

## Stage 3: WoT DSL (Parser + Compiler)

### What happens

The Workflow-of-Thought (WoT) DSL provides a concrete syntax for composing grammar rules into executable workflows. The parser reads `.wot.trsx` files, builds an AST, and the compiler transforms the AST into execution plans that chain MCP tool invocations.

**Input:** `.wot.trsx` source files referencing grammar rules
**Transformation:** Parse -> AST -> Type check -> Compile -> Execution plan
**Output:** Typed execution plans with governance gates

### tars modules involved

| Module | Path | Role |
|--------|------|------|
| `WotParser` | `v2/src/Tars.DSL/Wot/WotParser.fs` | Full EBNF parser with error recovery, forgiving syntax |
| `WotAST` | `v2/src/Tars.DSL/Wot/WotAST.fs` | Abstract syntax types for parsed workflows |
| `WotCompiler` | `v2/src/Tars.DSL/Wot/WotCompiler.fs` | Compiles AST to execution plans |
| `WotLanguageServer` | `v2/src/Tars.LSP/WotLanguageServer.fs` | LSP server: diagnostics, hover, completion |

### Language server capabilities

The LSP server (`WotLanguageServer.fs`) provides IDE integration for `.wot.trsx` files:

- **Diagnostics** -- real-time parse error reporting via `DiagnosticsPublisher`
- **Document store** -- concurrent document tracking with `ConcurrentDictionary`
- **Parse result caching** -- stores `Result<DslWorkflow, ParseError list>` per document URI
- Built on OmniSharp LSP protocol implementation

### Connection to Demerzel grammars

The WoT DSL references Demerzel grammars indirectly: grammar rules define what node kinds, edge topologies, and governance gates are valid. The parser enforces structural validity while WeightedGrammar steers which rule combinations are preferred.

tars EBNF files that define the DSL's own syntax:
- `v2/grammars/wot.ebnf` -- WoT workflow structure
- `v2/grammars/cortex.ebnf` -- reasoning node types
- `v2/grammars/fsharp.ebnf` -- F# computation expression integration
- `v2/grammars/intent_plan.ebnf` -- intent-to-plan mapping
- `v2/grammars/repair_proposal.ebnf` -- self-repair syntax

### Governance gates

- Parser validates structural conformance (force 1)
- Compiler applies governance gates from Demerzel alignment policy
- Type checking ensures node input/output types compose correctly (categorial grammar)

### Status: **Implemented**

Parser, AST, compiler, and LSP server are all operational in tars v2.

---

## Stage 4: MCP Tool Execution

### What happens

Compiled execution plans invoke MCP tools with governance gates at each step. The MOG (MCP Orchestration Grammar) defines pipeline structure, risk-based gating, and context accumulation.

**Input:** Execution plans from WoT compiler
**Transformation:** Tool invocation with tetravalent confidence checks
**Output:** Execution results + traces + governance metrics

### tars modules involved

The full 151-tool MCP inventory is cataloged in `state/tool-catalogs/tars-mcp-tools.json` (Demerzel). Tool invocations flow through tars's MCP server infrastructure.

### Demerzel artifacts that participate

| Artifact | Role |
|----------|------|
| `grammars/state-machines.ebnf` | Risk escalation (section 5), fuzzy guards (section 9) |
| `policies/alignment-policy.yaml` | Confidence thresholds (0.3/0.5/0.7/0.9 bands) |
| `policies/autonomous-loop-policy.yaml` | Bounds on autonomous execution |
| `schemas/pipeline-context.schema.json` | Shared state schema for pipelines |
| `docs/superpowers/specs/2026-03-21-mcp-orchestration-grammar-design.md` | MOG grammar + pipeline instances |

### Risk-based governance gates

| Risk Level | Auto-Gate | Behavior |
|-----------|-----------|----------|
| Low | None | Read-only tools flow freely |
| Medium | `when T(0.7)` | Confidence check before side effects |
| High | `when T(0.7) && C(<0.1)` | Full fuzzy gate, logged |
| Critical | Pre-mortem required | Anticipatory ethics check before execution |

### Status: **Implemented**

MCP tool infrastructure is operational. MOG grammar is specified, pipeline executor partially implemented in tars.

---

## Stage 5: Grammar Distillation (Pattern Extraction)

### What happens

After execution, traces are analyzed to extract reusable patterns. The distiller produces three orthogonal facets for each discovered pattern, enabling independent evolution of structure, types, and behavior.

**Input:** Execution traces (node sequences, tool calls, outcomes)
**Transformation:** Trace analysis -> facet extraction -> typed production rules
**Output:** `TypedProduction` records with structural, typed, and behavioral facets

### tars modules involved

| Module | Path | Role |
|--------|------|------|
| `GrammarDistillation` | `v2/src/Tars.Evolution/GrammarDistillation.fs` | High-level distiller: extracts three facets from traces |
| `GrammarDistill` | `v2/src/Tars.Core/GrammarDistill.fs` | Low-level primitives: JSON shape distillation, field extraction, prompt hints |
| `WeightedGrammar` | `v2/src/Tars.Evolution/WeightedGrammar.fs` | Receives distilled rules for Bayesian weight assignment |
| `GrammarMlBridge` | `v2/src/Tars.Evolution/GrammarMlBridge.fs` | Extracts numeric features for ML-assisted prediction |

### Three distillation facets

1. **Structural** -- DAG shape: node kinds (reason/work) + edge topology. Captures workflow shape independent of content.
2. **Typed** -- Input/output type signatures per node with composability check. Enables categorial grammar reasoning about whether patterns can chain.
3. **Behavioral** -- Post-conditions that held during execution + tool constraints. Captures "what made this pattern succeed."

### Closed loop architecture

```
Trace -> Distiller -> TypedProduction -> WeightedGrammar -> PatternSelector -> Execution -> Trace
```

Each iteration strengthens high-performing patterns (weight increase) and weakens failing ones (weight decay). The `GrammarMlBridge` adds predictive priors so new patterns start with informed weights rather than uniform priors.

### Key types from distillation

- `TypedSlot` -- named slot with Kind, InputType, OutputType
- `DistilledEdge` -- directed edge in the distilled DAG
- `DistillationFacet` -- `Structural | Typed | Behavioral` discriminated union
- `TypedProduction` -- complete distilled rule with ID (hash of structural fingerprint), facets, and trace count
- `ProductionFeatures` -- numeric feature vector for ML (slot count, edge count, reason ratio, tool diversity, etc.)

### ML integration points (via GrammarMlBridge)

1. **Feature extraction** -- `TypedProduction -> ProductionFeatures -> ix training data`
2. **Predictive priors** -- `ix_ml_predict -> Bayesian prior for new productions`
3. **Grammar breeding** -- `ix_evolution -> breed new productions from top performers`

### Governance gates

- GrammarGovernor evaluates promotion candidates before they advance levels
- 8-criteria scoring prevents half-baked patterns from polluting the grammar
- Rollback expansion paths required for high-level promotions

### Status: **Implemented**

GrammarDistillation and GrammarDistill are complete. ML bridge is implemented but ix integration is partially connected.

---

## Stage 6: Promotion to Demerzel Evolution Log

### What happens

Patterns that survive distillation and accumulate sufficient evidence promote into Demerzel's governance state. This closes the loop: execution evidence becomes governance knowledge.

**Input:** Distilled patterns with sufficient evidence (citations >= 3)
**Transformation:** Belief state update: U -> T (unknown becomes verified)
**Output:** Updated `state/evolution/` entries, belief state transitions

### Demerzel artifacts that participate

| Artifact | Role |
|----------|------|
| `state/evolution/` | Evolution log tracking pattern lifecycle |
| `state/beliefs/` | Tetravalent belief state persistence |
| `state/knowledge/` | Knowledge state snapshots |
| `grammars/state-machines.ebnf` section 4 | Promotion staircase definition |
| `policies/kaizen-policy.yaml` | Continuous improvement tracking |
| `policies/self-modification-policy.yaml` | Constraints on self-modification |

### Promotion staircase (from state-machines.ebnf)

Patterns advance through levels as evidence accumulates:

```
Pattern (observed) -> Idiom (recurring) -> DslClause (formalized) -> Language Feature (embedded)
```

Each level requires increasing evidence thresholds and governance approval.

### Governance gates

- Constitution hierarchy applies: Asimov Laws (Articles 0-5) override all promotions
- Self-referential promotions (grammar promoting itself) trigger escalation
- Conscience policy monitors for governance inflation (LOLLI vs ERGOL)

### Status: **Partially implemented**

Evolution log and belief state persistence are in place. Automated promotion from distillation traces to evolution entries is specified but requires manual trigger.

---

## Cross-Cutting Concerns

### F# Computation Expressions

tars leverages F# computation expressions as the bridge between grammar specifications and executable workflows. The WoT DSL compiles down to computation expression builders that:

- Sequence reasoning steps with `let!` bindings
- Apply governance checks at `do!` boundaries
- Handle errors with `try/with` mapped to tetravalent C (contradiction)
- Support parallel composition via `Async.Parallel`

The grammar -> CE connection is what makes Demerzel's declarative EBNF specifications executable in tars's runtime.

### Galactic Protocol

Cross-repo communication follows the Galactic Protocol contract:
- Demerzel sends governance directives (grammar updates, policy changes)
- tars returns compliance reports (execution outcomes, distilled patterns)
- Belief states synchronize through `state/` directory conventions

### Department Mapping

Each Demerzel grammar maps to a Streeling University department, which determines:
- Which persona archetypes can invoke the grammar
- What confidence thresholds apply (department-specific calibration)
- Where distilled patterns promote to in the evolution hierarchy

---

## Summary Table

| Stage | Input | Output | tars Module | Demerzel Artifact | Status |
|-------|-------|--------|-------------|-------------------|--------|
| 1. EBNF | Domain knowledge | `.ebnf` files | -- | `grammars/*.ebnf` | Implemented |
| 2. Weights | EBNF + history | `WeightedRule` | `WeightedGrammar.fs` | `policies/alignment-policy.yaml` | Implemented |
| 3. DSL | `.wot.trsx` | Execution plans | `WotParser.fs`, `WotCompiler.fs` | `grammars/state-machines.ebnf` | Implemented |
| 4. Execution | Plans | Traces + results | MCP server | MOG spec, tool catalog | Implemented |
| 5. Distillation | Traces | `TypedProduction` | `GrammarDistillation.fs` | -- | Implemented |
| 6. Promotion | Productions | Evolution entries | `GrammarGovernor.fs` | `state/evolution/` | Partial |
