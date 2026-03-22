# ix CLI — IxQL Script Execution — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** ix repo (new `ix-cli` crate + `ix-ixql` parser crate)
**Issue:** #103
**Blocks:** #117 (IxQL LSP), #104 (Governance as IxQL)

## Overview

A Rust CLI that parses `.ixql` files against the IxQL grammar, validates pipeline structure, and executes stages. The `--governed` flag inserts constitutional gates between pipeline stages. The CLI is the runtime entry point for everything defined in `docs/ixql-guide.md` and `grammars/sci-ml-pipelines.ebnf`.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Parser library | pest | PEG grammar maps directly to EBNF; `.pest` file is the source of truth; easier LSP reuse |
| Crate split | `ix-ixql` (parser+AST) + `ix-cli` (binary) | LSP (#117) reuses `ix-ixql` without pulling in CLI deps |
| Execution model | Stage-by-stage with async boundaries | Each `→` is an await point; enables governed gates between stages |
| Governed mode | `--governed` flag inserts gates from Demerzel policies | Default: ungoverned (fast). Governed: constitutional checks at each `→` |
| Output format | JSON lines (default) + human-readable (--pretty) | JSON lines for piping to other tools; pretty for interactive use |
| Config | `ix.toml` in project root | Parser settings, default governance level, MCP endpoints |

## Section 1: Crate Architecture

### ix-ixql (library crate)

Parser, AST, and semantic analysis. No I/O, no execution.

```
crates/ix-ixql/
  src/
    lib.rs              # Public API
    grammar.pest        # PEG grammar (generated from EBNF)
    parser.rs           # pest parser → CST
    ast.rs              # Typed AST nodes
    ast/
      pipeline.rs       # Pipeline, Ensemble, FanOut, FanIn
      source.rs         # DataSource variants
      preprocess.rs     # Cleaning, Transform, Feature, Split
      model.rs          # Model variants
      eval.rs           # Metrics, Validation, Interpretation
      deploy.rs         # Serialization, Serving, Monitoring
      governance.rs     # Gates, Checks, Confidence thresholds
      reactive.rs       # Watch, Webhook, Cron, SSE, WebSocket
      mcp.rs            # Tool invocation, Parallel, Bindings
      flow.rs           # FanOut, FanIn, Filter, Throttle, Retry, CircuitBreaker, Window
      expr.rs           # Expressions, predicates, when-clauses
    semantic.rs         # Type checking, pipeline validation
    errors.rs           # Diagnostic errors with spans
    span.rs             # Source location tracking
  Cargo.toml
```

**Public API:**

```rust
/// Parse IxQL source into an AST
pub fn parse(source: &str) -> Result<Program, Vec<Diagnostic>>;

/// Parse a file
pub fn parse_file(path: &Path) -> Result<Program, Vec<Diagnostic>>;

/// Validate a parsed program (type check, pipeline coherence)
pub fn validate(program: &Program) -> Result<ValidatedProgram, Vec<Diagnostic>>;

/// Get completions at a position (for LSP)
pub fn completions(program: &Program, position: Position) -> Vec<Completion>;

/// Get hover info at a position (for LSP)
pub fn hover(program: &Program, position: Position) -> Option<HoverInfo>;

/// Get diagnostics for a program
pub fn diagnostics(program: &Program) -> Vec<Diagnostic>;
```

### ix-cli (binary crate)

The `ix` command-line tool. Depends on `ix-ixql`, `ix-pipeline`, `ix-governance`, and other ix crates.

```
crates/ix-cli/
  src/
    main.rs             # Entry point, clap argument parsing
    commands/
      run.rs            # ix run <file.ixql>
      check.rs          # ix check <file.ixql> (parse + validate, no execute)
      fmt.rs            # ix fmt <file.ixql> (format IxQL source)
      explain.rs        # ix explain <file.ixql> (show execution plan)
      repl.rs           # ix repl (interactive IxQL REPL)
    executor/
      mod.rs            # Pipeline executor orchestration
      stage.rs          # Single stage execution
      gate.rs           # Governance gate insertion
      context.rs        # Runtime context (variables, bindings, state)
    output/
      mod.rs            # Output formatting
      json.rs           # JSON lines output
      pretty.rs         # Human-readable output
      table.rs          # Tabular output for metrics
    config.rs           # ix.toml loading
  Cargo.toml
```

## Section 2: CLI Interface

```
ix — IxQL pipeline runner

USAGE:
    ix <COMMAND> [OPTIONS]

COMMANDS:
    run       Execute an IxQL pipeline
    check     Parse and validate without executing
    fmt       Format IxQL source code
    explain   Show execution plan without running
    repl      Interactive IxQL shell
    version   Print version info

GLOBAL OPTIONS:
    --governed          Enable constitutional gates between stages
    --governance-level  Governance strictness: minimal | standard | strict
    --config <path>     Path to ix.toml (default: ./ix.toml)
    --verbose           Verbose output
    --quiet             Suppress non-error output
```

### ix run

```
ix run <FILE.ixql> [OPTIONS]

OPTIONS:
    --governed              Insert constitutional gates
    --governance-level <L>  minimal | standard | strict (default: standard)
    --output <FORMAT>       json | pretty | table (default: json)
    --dry-run               Validate and show plan, don't execute
    --stage <N>             Execute only up to stage N
    --timeout <DURATION>    Global timeout (default: 5m)
    --var <KEY=VALUE>       Set pipeline variable
    --mcp-endpoint <URL>    MCP server endpoint
    --confidence <FLOAT>    Override confidence threshold (0.0-1.0)
```

**Examples:**

```bash
# Simple pipeline
ix run pipeline.ixql

# Governed execution with strict gates
ix run pipeline.ixql --governed --governance-level strict

# Dry run — show what would execute
ix run pipeline.ixql --dry-run --output pretty

# Pass variables
ix run pipeline.ixql --var dataset=train.csv --var epochs=100

# Execute only first 3 stages
ix run pipeline.ixql --stage 3
```

### ix check

```
ix check <FILE.ixql> [OPTIONS]

OPTIONS:
    --output <FORMAT>   json | pretty (default: pretty)
    --strict            Treat warnings as errors
```

Returns exit code 0 if valid, 1 if errors. Outputs diagnostics to stderr.

### ix fmt

```
ix fmt <FILE.ixql> [OPTIONS]

OPTIONS:
    --check             Check if formatted (exit 1 if not), don't modify
    --write             Write formatted output back to file (default: stdout)
    --indent <N>        Indentation width (default: 2)
```

### ix explain

```
ix explain <FILE.ixql> [OPTIONS]

OPTIONS:
    --output <FORMAT>   json | pretty | dot (default: pretty)
    --governed          Show governance gates in plan
```

Outputs the execution DAG: stage ordering, parallelism opportunities, data flow, and governance insertion points.

**Pretty output example:**

```
Pipeline: research-pipeline.ixql
  Stage 1: department_state("guitar-studies")     [source]
    → Stage 2: question_generation("caged")       [transform]
    → Stage 3: cross_model_validation             [fan-out: 2 models]
        ├─ claude.research(question)
        └─ gpt4o.research(question)
    → Stage 4: evaluation(agreement, evidence)    [eval]
    → Gate: when T >= 0.8                         [governed]
    → Stage 5: course_production("GTR-003")       [deploy]
    → Stage 6: compound                           [compound]

Stages: 6 | Gates: 1 | Parallelism: Stage 3 (2-way fan-out)
Estimated: ~3 API calls, ~2 file writes
```

### ix repl

Interactive IxQL shell for experimentation:

```
ix> csv("data.csv") → normalize → info
[tabular: 1000 rows × 15 cols, normalized]

ix> csv("data.csv") → normalize → random_forest → f1_score
{ "f1": 0.87, "logic": "T", "confidence": 0.87 }

ix> :governed on
Governance mode: standard

ix> csv("data.csv") → normalize → random_forest → f1_score
[gate] bias_assessment: passed
[gate] explanation_requirement: passed (SHAP available)
{ "f1": 0.87, "logic": "T", "confidence": 0.87 }

ix> :explain csv("data.csv") → normalize → random_forest → f1_score
[3 stages, 0 fan-outs, 2 governance gates in governed mode]
```

REPL commands (`:` prefix):
- `:governed on|off` — toggle governance
- `:explain <pipeline>` — show execution plan
- `:type <expr>` — show inferred type
- `:load <file>` — load and execute a .ixql file
- `:history` — show command history
- `:quit` — exit

## Section 3: Governance Integration

### The --governed Flag

When `--governed` is active, the executor inserts constitutional gates between pipeline stages. Gate behavior depends on `--governance-level`:

| Level | Gates Inserted | Confidence Required | Escalation |
|-------|---------------|-------------------|------------|
| minimal | bias_assessment only | >= 0.5 | Log warning |
| standard | bias + reversibility + confidence | >= 0.7 | Pause + prompt |
| strict | All 5 gates + provenance | >= 0.9 | Hard stop + report |

### Gate Types

From the IxQL grammar's Section 7 (Governance Integration):

| Gate | Constitutional Basis | What It Checks |
|------|---------------------|----------------|
| bias_assessment | Article 10 (Stakeholder Pluralism) | Model fairness across subgroups |
| reversibility_check | Article 3 (Reversibility) | Can this stage be rolled back? |
| confidence_calibration | Alignment policy thresholds | Are model probabilities well-calibrated? |
| explanation_requirement | Article 2 (Transparency) | Can the model explain its output? (SHAP/LIME) |
| data_provenance_check | Article 7 (Auditability) | Where did training data come from? |

### Gate Execution

```rust
/// A governance gate that runs between pipeline stages
pub trait GovernanceGate {
    /// Check if the gate passes
    fn check(&self, context: &StageContext) -> GateResult;

    /// Constitutional article this gate enforces
    fn article(&self) -> &str;

    /// Minimum governance level that activates this gate
    fn min_level(&self) -> GovernanceLevel;
}

pub enum GateResult {
    Pass,
    PassWithNote(String),
    Fail { reason: String, article: String },
    Escalate { reason: String, to: EscalationTarget },
}

pub enum EscalationTarget {
    Log,       // minimal: just log
    Prompt,    // standard: pause and ask human
    HardStop,  // strict: stop execution, write report
}
```

### Tetravalent Pipeline Conclusions

Every pipeline run produces a tetravalent conclusion:

```rust
pub enum TetravalentConclusion {
    True { confidence: f64, evidence: Vec<Evidence> },
    False { confidence: f64, evidence: Vec<Evidence> },
    Unknown { reason: String, suggested_action: String },
    Contradictory { conflicts: Vec<Conflict>, escalation: EscalationTarget },
}
```

Mapping rules:
- All metrics meet thresholds → `T` (confidence = min metric)
- Any metric fails threshold → `F` (confidence = 1 - worst metric)
- Insufficient data or inconclusive → `U`
- Metrics disagree (one passes, another fails on same data) → `C`

## Section 4: Parser Design

### pest Grammar Derivation

The `.pest` grammar is derived from `grammars/sci-ml-pipelines.ebnf` with these mappings:

| EBNF | pest PEG |
|------|----------|
| `::=` | `=` |
| `\|` (alternation) | `\|` |
| `+` (one or more) | `+` |
| `*` (zero or more) | `*` |
| `?` (optional) | `?` |
| `"literal"` | `"literal"` |
| `(* comment *)` | `// comment` |
| Whitespace | `WHITESPACE = _{ " " \| "\t" \| "\r" \| "\n" }` |
| `→` (arrow) | `arrow = { "→" \| "->" }` |
| `--` comment | `COMMENT = _{ "--" ~ (!NEWLINE ~ ANY)* }` |

### AST Core Types

```rust
/// Top-level program: one or more pipeline definitions
pub struct Program {
    pub pipelines: Vec<Pipeline>,
    pub span: Span,
}

/// A pipeline: stages connected by arrows
pub struct Pipeline {
    pub name: Option<String>,
    pub stages: Vec<Stage>,
    pub compound: Option<CompoundPhase>,
    pub span: Span,
}

/// A pipeline stage
pub enum Stage {
    Source(DataSource),
    Transform(Transform),
    Model(ModelSpec),
    Evaluation(EvalSpec),
    Deploy(DeploySpec),
    Gate(GovernanceGate),
    FanOut(Vec<Pipeline>),
    FanIn(Vec<Pipeline>),
    Binding(Binding),          // result <- tool.call(args)
    When(WhenClause, Box<Stage>),
    Compound(CompoundPhase),
    Custom(String, Vec<Arg>),  // extensible stage
}

/// When clause: tetravalent condition
pub struct WhenClause {
    pub logic_value: LogicValue,  // T, F, U, C
    pub operator: CompareOp,      // >=, <=, ==, !=
    pub threshold: f64,
    pub span: Span,
}
```

### Semantic Validation

After parsing, validate:

1. **Pipeline coherence** — output type of stage N matches input type of stage N+1
2. **Fan-out/fan-in balance** — every fan-out has a merge or each branch terminates
3. **Binding scope** — variables used in `when` clauses are defined by prior `<-` bindings
4. **MCP tool existence** — tool names resolve to known MCP tools (if catalog available)
5. **Model compatibility** — model type matches data shape (e.g., classifier for tabular)
6. **Gate placement** — governance gates only between stages, not inside stages
7. **Compound phase** — at most one per pipeline, must be last

## Section 5: Execution Model

### Stage-by-Stage Async

```rust
pub async fn execute(program: ValidatedProgram, config: Config) -> PipelineResult {
    let mut context = Context::new(config);

    for stage in program.stages() {
        // Insert governance gate if --governed
        if context.is_governed() {
            for gate in gates_for_stage(&stage, context.governance_level()) {
                match gate.check(&context) {
                    GateResult::Pass => {},
                    GateResult::PassWithNote(note) => context.log_note(note),
                    GateResult::Fail { reason, article } => {
                        return PipelineResult::Failed { stage, reason, article };
                    },
                    GateResult::Escalate { reason, to } => {
                        handle_escalation(to, &reason, &context).await?;
                    },
                }
            }
        }

        // Execute stage
        let output = execute_stage(&stage, &mut context).await?;
        context.set_stage_output(output);
    }

    // Map to tetravalent conclusion
    context.conclude()
}
```

### Fan-Out Parallelism

`fan_out` stages execute branches concurrently via tokio:

```rust
async fn execute_fan_out(branches: Vec<Pipeline>, context: &Context) -> Vec<StageOutput> {
    let handles: Vec<_> = branches.into_iter()
        .map(|branch| {
            let ctx = context.clone();
            tokio::spawn(async move { execute(branch, ctx).await })
        })
        .collect();

    futures::future::join_all(handles).await
        .into_iter()
        .map(|r| r.unwrap())
        .collect()
}
```

### MCP Tool Invocation

MCP tool calls use the ix-agent crate's existing MCP client:

```rust
async fn execute_mcp(tool: &str, args: &[Arg], context: &Context) -> StageOutput {
    let client = context.mcp_client();
    let result = client.call_tool(tool, args.to_json()).await?;
    StageOutput::from_mcp(result)
}
```

## Section 6: Configuration

### ix.toml

```toml
[ixql]
# Default governance level when --governed is used
governance_level = "standard"

# Confidence threshold override (0.0-1.0)
# confidence_threshold = 0.7

# Default output format
output = "json"

# Pipeline timeout
timeout = "5m"

[mcp]
# MCP server endpoints
endpoints = [
    { name = "tars", url = "http://localhost:3000" },
    { name = "context7", url = "http://localhost:3001" },
]

[governance]
# Path to Demerzel governance artifacts
demerzel_path = "../Demerzel"

# Constitution to enforce
constitution = "default.constitution.md"

# Additional policies to check
policies = ["alignment-policy.yaml", "self-modification-policy.yaml"]
```

## Section 7: Workspace Integration

### New crates to add to ix workspace

```toml
# In ix/Cargo.toml [workspace] members
"crates/ix-ixql",
"crates/ix-cli",
```

### Dependencies

```toml
# ix-ixql/Cargo.toml
[dependencies]
pest = "2"
pest_derive = "2"
thiserror = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"

# ix-cli/Cargo.toml
[dependencies]
ix-ixql = { path = "../ix-ixql" }
ix-pipeline = { path = "../ix-pipeline" }
ix-governance = { path = "../ix-governance" }
ix-agent = { path = "../ix-agent" }
ix-io = { path = "../ix-io" }
clap = { version = "4", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
colored = "3"
rustyline = "15"       # REPL line editing
serde_json = "1"
```

## Section 8: LSP Reuse Path

The `ix-ixql` crate is designed for LSP reuse (#117):

- `parse()` → syntax highlighting (token spans)
- `diagnostics()` → inline error/warning squiggles
- `completions()` → autocomplete at cursor position
- `hover()` → documentation on hover
- `validate()` → real-time pipeline validation

The LSP server will be a separate `ix-lsp` crate that depends on `ix-ixql` and implements the Language Server Protocol over `tower-lsp`.

## Dependencies on Demerzel

- `grammars/sci-ml-pipelines.ebnf` — source of truth for parser grammar
- `constitutions/` — governance gates reference constitutional articles
- `policies/alignment-policy.yaml` — confidence thresholds
- `schemas/` — output format validation

## Open Questions

1. **pest vs nom?** Pest maps more naturally to EBNF and produces better error messages. Nom is faster but requires manual AST construction. Recommendation: pest for clarity, benchmark later.
2. **How to keep .pest in sync with .ebnf?** Recommendation: `.pest` is derived artifact, generated by a script from `.ebnf`. Single source of truth remains the EBNF in Demerzel.
3. **REPL persistence?** Should the REPL save session state between invocations? Recommendation: optional `--history` flag, default no persistence.
4. **MCP transport?** stdio vs HTTP for MCP tool calls. Recommendation: HTTP default with stdio fallback, configurable in ix.toml.
