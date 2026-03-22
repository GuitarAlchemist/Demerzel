# tars Native IxQL via F# Computation Expressions — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** tars repo (new `IxQL` module + `IxqlBuilder` CE class)
**Issue:** #131
**Relates to:** #103 (ix CLI), #117 (IxQL LSP)

## Overview

tars should speak IxQL natively through F# computation expressions (CEs). Instead of parsing `.ixql` text at runtime, pipelines become type-safe, composable F# code that fails to compile when invalid. The CE DSL mirrors every grammar production in `grammars/sci-ml-pipelines.ebnf`, integrates with tars `GrammarDistillation` for continuous weight updates, and can export pipelines as `.ixql` text for execution via the ix CLI (#103).

## Architecture Position

```
IxQL ecosystem:
├── grammars/sci-ml-pipelines.ebnf   — source of truth, defines syntax
├── ix CLI (Rust / #103)             — parse + execute .ixql text files
├── tars CE (F# / this spec)         — native F# DSL via computation expressions
├── IxQL LSP (Rust / #117)           — IDE support for .ixql text files
└── ga-client (React)                — pipeline visualization
```

The three runtime implementations (ix CLI, tars CE, LSP) share the same grammar semantics but serve different use cases:
- ix CLI: text-based, scriptable, shell-composable, governed execution
- tars CE: IntelliSense, compile-time type checking, F# ecosystem integration
- LSP: authoring assistance for `.ixql` text files

---

## Section 1: Tetravalent Conclusion as F# Discriminated Union

The IxQL grammar's tetravalent logic maps directly to a discriminated union. This is the core type that flows through every pipeline.

```fsharp
/// Tetravalent logic value — mirrors grammar Section 7
type LogicValue = T | F | U | C

/// Evidence record attached to a conclusion
type Evidence = {
    Source: string
    Value: float
    Threshold: float
    Passed: bool
}

/// Conflict record for contradictory conclusions
type Conflict = {
    Left: string * float   // (metric_name, value)
    Right: string * float
    Reason: string
}

/// The conclusion of any IxQL pipeline execution
/// Mirrors grammar: conclude ::= validated | rejected | inconclusive | unstable | overfitting_detected
[<RequireQualifiedAccess>]
type TetravalentConclusion =
    /// All metrics met thresholds — model validated (T)
    | True of confidence: float * evidence: Evidence list
    /// Any metric failed threshold — model rejected (F)
    | False of confidence: float * evidence: Evidence list
    /// Insufficient data or inconclusive — need more investigation (U)
    | Unknown of reason: string * suggestedAction: string
    /// Metrics disagree on same data — model unstable, escalate (C)
    | Contradictory of conflicts: Conflict list * escalation: EscalationTarget

and EscalationTarget =
    | Log          // minimal: record and continue
    | Prompt       // standard: pause and ask human
    | HardStop     // strict: stop, write governance report
```

Exhaustive matching is enforced by the compiler. Any handler that does not cover all four cases will not compile — governance completeness as a type property.

---

## Section 2: Grammar Production to CE Method Mapping

Every IxQL grammar production from `sci-ml-pipelines.ebnf` has a corresponding `IxqlBuilder` method. The mapping is mechanical and explicit.

| Grammar Production | CE Method | EBNF Section |
|---|---|---|
| `data_source` | `Source` | §2 |
| `preprocessing` | `Pipe` | §3 |
| `model` | `Train` | §4 |
| `evaluation` | `Evaluate` | §5 |
| `governance_gate` | `Gate` | §7 |
| `deployment` | `Deploy` | §6 |
| `tool_invocation` | `Mcp` | §10 |
| `fan_out` | `FanOut` | §9 |
| `reactive_source` / `file_watcher` | `Watch` | §9 |
| `output_sink` / `discord_sink` | `Alert` | §9 |
| `conclude` | `Conclude` | §7 |
| `mcp_compound` / `compound_step` | `Compound` | §10 |

---

## Section 3: IxqlBuilder Computation Expression

```fsharp
/// Pipeline stage — the unit of CE composition
type PipelineStage =
    | SourceStage of DataSource
    | PreprocessStage of PreprocessSpec
    | ModelStage of ModelSpec
    | EvalStage of EvalSpec
    | GateStage of GovernanceGate
    | DeployStage of DeploySpec
    | McpStage of McpToolCall
    | FanOutStage of IxqlPipeline list
    | WatchStage of WatchSpec
    | AlertStage of AlertSpec
    | ConcludeStage of LogicValue * float   // (logic, threshold)
    | CompoundStage of CompoundOp list

/// A compiled pipeline: ordered stages + metadata
and IxqlPipeline = {
    Name: string option
    Stages: PipelineStage list
    Governed: bool
    GovernanceLevel: GovernanceLevel
}

/// Governance strictness — mirrors CLI --governance-level
and GovernanceLevel = Minimal | Standard | Strict

/// Computation expression builder — IxQL native DSL
type IxqlBuilder() =

    // ── CE plumbing ────────────────────────────────────────────────

    member _.Bind(pipeline: IxqlPipeline, f: IxqlPipeline -> IxqlPipeline) =
        f pipeline

    member _.Return(x: IxqlPipeline) = x

    member _.ReturnFrom(x: IxqlPipeline) = x

    member _.Zero() =
        { Name = None; Stages = []; Governed = false; GovernanceLevel = Standard }

    member _.Combine(a: IxqlPipeline, b: IxqlPipeline) =
        { a with Stages = a.Stages @ b.Stages }

    member _.Delay(f: unit -> IxqlPipeline) = f()

    member _.For(seq: 'T seq, body: 'T -> IxqlPipeline) =
        seq |> Seq.map body |> Seq.fold (fun acc p -> { acc with Stages = acc.Stages @ p.Stages }) (IxqlBuilder().Zero())

    // ── Grammar productions ────────────────────────────────────────

    /// §2: data_source — pipeline entry point
    member _.Source(src: DataSource) =
        { IxqlBuilder().Zero() with Stages = [ SourceStage src ] }

    /// §3: preprocessing — cleaning, transformation, feature engineering, splitting
    member _.Pipe(spec: PreprocessSpec) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ PreprocessStage spec ] }

    /// §4: model — supervised, unsupervised, probabilistic, neural, RL
    member _.Train(spec: ModelSpec) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ ModelStage spec ] }

    /// §5: evaluation — metrics, validation strategy, interpretation
    member _.Evaluate(spec: EvalSpec) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ EvalStage spec ] }

    /// §7: governance_gate — constitutional checks between stages
    member _.Gate(gate: GovernanceGate) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ GateStage gate ] }

    /// §6: deployment — serialization, serving, monitoring
    member _.Deploy(spec: DeploySpec) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ DeployStage spec ] }

    /// §10: tool_invocation — MCP tool call (namespace.method(args))
    member _.Mcp(tool: McpToolCall) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ McpStage tool ] }

    /// §9: fan_out — parallel branch execution
    member _.FanOut(branches: IxqlPipeline list) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ FanOutStage branches ] }

    /// §9: file_watcher / reactive_source — watch a path for changes
    member _.Watch(spec: WatchSpec) =
        { IxqlBuilder().Zero() with Stages = [ WatchStage spec ] }

    /// §9: output_sink / discord_sink — send result to a channel
    member _.Alert(spec: AlertSpec) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ AlertStage spec ] }

    /// §7: conclude — emit tetravalent conclusion with threshold
    member _.Conclude(logic: LogicValue, threshold: float) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ ConcludeStage(logic, threshold) ] }

    /// §10: compound — harvest learnings after pipeline completes
    member _.Compound(ops: CompoundOp list) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Stages = pipeline.Stages @ [ CompoundStage ops ] }

    // ── Governed mode ──────────────────────────────────────────────

    /// Enable constitutional gates — equivalent to ix CLI --governed
    member _.Governed(level: GovernanceLevel) : IxqlPipeline -> IxqlPipeline =
        fun pipeline -> { pipeline with Governed = true; GovernanceLevel = level }

let ixql = IxqlBuilder()
```

---

## Section 4: Type-Safe Pipeline Composition

The type system enforces pipeline validity at compile time. Invalid stage orderings become type errors, not runtime failures.

### Stage Output Types

```fsharp
/// The data shape flowing between stages
/// Mirrors grammar: data_shape ::= tabular | time_series | graph | text | image | audio | multimodal
[<RequireQualifiedAccess>]
type DataShape =
    | Tabular of rows: int option * cols: int option
    | TimeSeries of frequency: string option
    | Graph of nodes: int option
    | Text
    | Image
    | Audio
    | Multimodal of DataShape list
    | Predictions of DataShape               // output of a model
    | Metrics of string list                 // output of evaluation
    | Unknown                                // unresolved at compile time
```

### Phantom-Type Pipeline (Advanced, Optional)

For maximum compile-time safety, pipelines can be typed by their current output shape using phantom types:

```fsharp
/// Pipeline parameterized by its output shape
/// Invalid compositions (e.g., Predictions → Train) become type errors
type TypedPipeline<'Output> = TypedPipeline of IxqlPipeline

/// Only Tabular data can enter a classification model
let trainClassifier (p: TypedPipeline<DataShape.Tabular>) : TypedPipeline<DataShape.Predictions> = ...

/// Only Predictions can enter classification evaluation
let evaluateClassifier (p: TypedPipeline<DataShape.Predictions>) : TypedPipeline<DataShape.Metrics> = ...

/// This would be a compile error:
/// evaluateClassifier (trainClassifier (TypedPipeline source))  // ✓
/// evaluateClassifier source                                    // ✗ — type mismatch
```

Phantom types are opt-in. The base `IxqlBuilder` uses `DataShape.Unknown` to allow exploratory pipelines; the `StrictIxqlBuilder` uses phantom types for production pipelines where shape safety is required.

### Governance Gate Enforcement at Compile Time

When `Governed = true`, the `IxqlValidator` module checks that required gates are present before compilation proceeds:

```fsharp
module IxqlValidator =

    type ValidationError =
        | MissingEvaluation of afterModel: string
        | UngovernedDeploy of deployStage: string
        | MissingCompound
        | FanOutWithoutMerge of branchCount: int
        | GateAfterDeploy of gateName: string

    /// Validate a pipeline before execution
    /// Returns Error if any constitutional requirement is violated
    let validate (pipeline: IxqlPipeline) : Result<IxqlPipeline, ValidationError list> =
        let errors = ResizeArray<ValidationError>()

        // Must have evaluation after any model
        let hasModel = pipeline.Stages |> List.exists (function ModelStage _ -> true | _ -> false)
        let hasEval  = pipeline.Stages |> List.exists (function EvalStage _  -> true | _ -> false)
        if hasModel && not hasEval then
            errors.Add(MissingEvaluation "unnamed model")

        // Governed pipelines must have gates before deploy
        if pipeline.Governed then
            let deployIdx = pipeline.Stages |> List.tryFindIndex (function DeployStage _ -> true | _ -> false)
            let gateBeforeDeploy =
                deployIdx
                |> Option.map (fun i -> pipeline.Stages |> List.take i |> List.exists (function GateStage _ -> true | _ -> false))
                |> Option.defaultValue true
            if not gateBeforeDeploy then
                errors.Add(UngovernedDeploy "deploy")

        if errors.Count = 0 then Ok pipeline
        else Error (List.ofSeq errors)
```

---

## Section 5: Usage Examples

### Example 1: Basic Supervised Pipeline

```fsharp
let chordRecognitionPipeline =
    ixql {
        let! p = ixql.Source(Csv "chord-dataset.csv")
        let! p = ixql.Pipe(Normalize) p
        let! p = ixql.Pipe(TrainTestSplit 0.8) p
        let! p = ixql.Train(RandomForest { NEstimators = 100; MaxDepth = 10 }) p
        let! p = ixql.Evaluate(F1Score) p
        let! p = ixql.Conclude(T, 0.8) p
        return p
    }
```

### Example 2: Governed Pipeline with Gates

```fsharp
let governedDeployPipeline =
    ixql {
        let! p = ixql.Source(ParquetFile "training-data.parquet")
        let! p = ixql.Pipe(Normalize) p
        let! p = ixql.Train(GradientBoosting { NEstimators = 200 }) p
        let! p = ixql.Evaluate(AucRoc) p
        let! p = ixql.Gate(BiasAssessment) p
        let! p = ixql.Gate(ReversibilityCheck) p
        let! p = ixql.Gate(ConfidenceCalibration) p
        let! p = ixql.Deploy(McpToolIntegration "model-v2") p
        let! p = ixql.Conclude(T, 0.9) p
        let! p = ixql.Compound [
            Harvest "evaluation_metrics"
            Promote "model-v2" |> IfLogic(T, 0.9)
            UpdateEvolutionLog "governed-deploy-success"
        ] p
        return ixql.Governed Standard p
    }
```

### Example 3: Fan-Out Cross-Model Validation

Mirrors the grammar's `ensemble_pipeline` and `fan_out` productions:

```fsharp
let crossValidationPipeline =
    ixql {
        let question = "Does CAGED improve chord recognition accuracy?"

        let claudeBranch = ixql {
            let! p = ixql.Mcp({ Namespace = "tars"; Method = "research"; Args = [Arg question] }) (ixql.Zero())
            return p
        }

        let gpt4oBranch = ixql {
            let! p = ixql.Mcp({ Namespace = "openai"; Method = "research"; Args = [Arg question] }) (ixql.Zero())
            return p
        }

        let! p = ixql.Source(GovernanceState "guitar-studies") (ixql.Zero())
        let! p = ixql.FanOut [ claudeBranch; gpt4oBranch ] p
        let! p = ixql.Evaluate(AgreementScore) p
        let! p = ixql.Conclude(T, 0.8) p
        return p
    }
```

### Example 4: Reactive Pipeline with Watch

```fsharp
let fileWatchPipeline =
    ixql {
        let! p = ixql.Watch({ Path = "data/*.csv"; Debounce = TimeSpan.FromSeconds 2.0 })
        let! p = ixql.Pipe(Normalize) p
        let! p = ixql.Train(RandomForest { NEstimators = 100; MaxDepth = 10 }) p
        let! p = ixql.Evaluate(F1Score) p
        let! p = ixql.Alert({ Channel = Discord "governance-alerts"; MessageTemplate = "Retrain complete: {f1}" }) p
        return p
    }
```

---

## Section 6: GrammarDistillation Integration

tars already has `GrammarDistillation` — execution traces from IxQL CE pipelines feed weight updates back into the grammar, closing the learning loop.

### Execution Trace

```fsharp
/// Trace record emitted by each stage during execution
type StageTrace = {
    Stage: string
    InputShape: DataShape
    OutputShape: DataShape
    DurationMs: int64
    Metrics: Map<string, float>
    LogicValue: LogicValue option
    Confidence: float option
    GateResults: (string * bool) list    // (gate_name, passed)
}

/// Full pipeline execution trace
type PipelineTrace = {
    PipelineName: string option
    Stages: StageTrace list
    Conclusion: TetravalentConclusion
    TotalDurationMs: int64
    GovernanceLevel: GovernanceLevel option
}
```

### Weight Update Loop

```fsharp
module IxqlRunner =

    /// Execute a pipeline and return result + trace
    let executeWithTrace (pipeline: IxqlPipeline) : Async<TetravalentConclusion * PipelineTrace> =
        async {
            let! (conclusion, trace) = PipelineExecutor.run pipeline
            return conclusion, trace
        }

/// Extension point: feed traces into GrammarDistillation
module GrammarDistillationBridge =

    /// Update grammar weights from a completed pipeline trace
    /// Feeds back into grammars/sci-ml-pipelines.ebnf weight annotations
    let updateFromTrace (trace: PipelineTrace) (grammarId: string) : Async<unit> =
        async {
            let weights =
                trace.Stages
                |> List.map (fun s -> {
                    Production = s.Stage
                    Weight = s.Confidence |> Option.defaultValue 0.5
                    Evidence = s.Metrics
                })
            do! GrammarDistillation.updateWeights(grammarId, weights)
        }

    /// Composite: execute and immediately feed distillation
    let executeAndLearn (pipeline: IxqlPipeline) (grammarId: string) : Async<TetravalentConclusion> =
        async {
            let! conclusion, trace = IxqlRunner.executeWithTrace pipeline
            do! updateFromTrace trace grammarId
            return conclusion
        }
```

Usage:

```fsharp
let result =
    GrammarDistillationBridge.executeAndLearn
        chordRecognitionPipeline
        "sci-ml-pipelines"
    |> Async.RunSynchronously

match result with
| TetravalentConclusion.True(conf, _)          -> printfn "Validated (confidence: %.2f)" conf
| TetravalentConclusion.False(conf, _)         -> printfn "Rejected (confidence: %.2f)" conf
| TetravalentConclusion.Unknown(reason, _)     -> printfn "Unknown: %s" reason
| TetravalentConclusion.Contradictory(cs, _)   -> printfn "Contradictory: %d conflicts" cs.Length
```

---

## Section 7: Interop — Export CE Pipelines as .ixql Text

tars can serialize any CE pipeline to `.ixql` text for execution by the ix CLI (#103), sharing, or storage in `pipelines/`.

```fsharp
module IxqlSerializer =

    /// Serialize a CE pipeline to .ixql text
    /// Output is valid input to: ix run <file.ixql>
    let toIxql (pipeline: IxqlPipeline) : string =
        let sb = System.Text.StringBuilder()

        pipeline.Name |> Option.iter (fun n -> sb.AppendLine($"-- {n}") |> ignore)

        if pipeline.Governed then
            let level = match pipeline.GovernanceLevel with
                        | Minimal  -> "minimal"
                        | Standard -> "standard"
                        | Strict   -> "strict"
            sb.AppendLine($"-- governed: {level}") |> ignore

        let stages =
            pipeline.Stages
            |> List.map stageToIxql

        sb.Append(stages |> String.concat "\n→ ") |> ignore
        sb.ToString()

    and stageToIxql = function
        | SourceStage src          -> dataSourceToIxql src
        | PreprocessStage spec     -> preprocessToIxql spec
        | ModelStage spec          -> modelToIxql spec
        | EvalStage spec           -> evalToIxql spec
        | GateStage gate           -> gateToIxql gate
        | DeployStage spec         -> deployToIxql spec
        | McpStage call            -> mcpToIxql call
        | FanOutStage branches     -> fanOutToIxql branches
        | WatchStage spec          -> watchToIxql spec
        | AlertStage spec          -> alertToIxql spec
        | ConcludeStage(lv, thr)   -> $"conclude(when {lv} >= {thr})"
        | CompoundStage ops        -> compoundToIxql ops

    /// Save to disk
    let saveToFile (pipeline: IxqlPipeline) (path: string) : unit =
        let text = toIxql pipeline
        System.IO.File.WriteAllText(path, text)
```

Round-trip property: a CE pipeline serialized to `.ixql` and parsed by ix CLI should produce equivalent behavior.

---

## Section 8: Module Structure in tars

```
src/
  IxQL/
    IxqlBuilder.fs          -- CE builder class (Section 3)
    Types.fs                -- DataSource, ModelSpec, EvalSpec, etc.
    TetravalentConclusion.fs -- DU from Section 1
    IxqlValidator.fs        -- Compile-time checks (Section 4)
    IxqlRunner.fs           -- Async execution engine
    IxqlSerializer.fs       -- Export to .ixql text (Section 7)
    GrammarDistillationBridge.fs -- Feed traces to distillation (Section 6)
    Stages/
      DataSources.fs        -- Csv, Json, Parquet, GovernanceState, etc.
      Preprocessing.fs      -- Normalize, Split, Encode, etc.
      Models.fs             -- RandomForest, GradientBoosting, etc.
      Evaluation.fs         -- F1Score, AucRoc, SilhouetteScore, etc.
      Governance.fs         -- GovernanceGate DU, gate execution
      Deployment.fs         -- Onnx, McpToolIntegration, etc.
      Mcp.fs                -- McpToolCall, namespace resolution
      Flow.fs               -- FanOut, Watch, Alert, Compound
```

---

## Section 9: Constitutional Basis

| CE Feature | Constitutional Article | Rationale |
|---|---|---|
| `Gate` method required before `Deploy` in governed mode | Article 3 (Reversibility) | Deployments must be reversible by default |
| `Evaluate` required after `Train` | Article 1 (Truthfulness) | Claims about model quality must be measured |
| `TetravalentConclusion` exhaustive matching | Article 2 (Transparency) | All four logic states must be explicitly handled |
| `Compound` for capturing learnings | Article 7 (Auditability) | Execution traces must be preserved |
| `IxqlValidator` before execution | Article 9 (Bounded Autonomy) | Pipelines must be validated before running |
| `GrammarDistillationBridge` | Kaizen policy | Every execution is a learning opportunity |

---

## Section 10: Relationship to ix CLI and LSP

| Concern | ix CLI (#103) | tars CE (this spec) | IxQL LSP (#117) |
|---|---|---|---|
| Input | `.ixql` text files | F# CE syntax | `.ixql` text in editor |
| Validation timing | Runtime (parse + validate) | Compile time (type checker) | Edit time (LSP diagnostics) |
| Primary users | Shell scripts, CI/CD | tars agents, F# code | VS Code, Claude Code |
| Governance gates | `--governed` flag | `ixql.Governed Level` | Suggestions + code actions |
| Interop | Consumes `.ixql` files | Exports `.ixql` via `IxqlSerializer` | Reads `.ixql` files |
| Shared parser | `ix-ixql` crate | F# type system (no text parser) | `ix-ixql` crate |

tars CE and ix CLI are complementary, not competing. tars is used for pipeline development in F# with full type safety; ix CLI is used for executing those same pipelines from the command line or CI. `IxqlSerializer` bridges the two.

---

## Open Questions

1. **Phantom types in default builder?** Using phantom types for every pipeline adds syntactic overhead. Recommendation: provide both `IxqlBuilder` (untyped, permissive) and `StrictIxqlBuilder` (phantom-typed, strict). Consumer chooses based on safety requirements.
2. **Async execution model?** tars already uses `async { }` CEs. IxQL stages that call MCP tools need async boundaries. Recommendation: `IxqlPipeline` executes as `Async<TetravalentConclusion>` throughout.
3. **Shared type definitions with ix?** `DataShape`, `GovernanceLevel`, and `TetravalentConclusion` are defined in both Rust (ix-ixql) and F# (tars). Recommendation: Demerzel schemas become the single source of truth; both implementations derive from the same JSON Schema definitions in `schemas/`.
4. **Hot reload for watched pipelines?** The `Watch` stage listens for file changes. Should the CE pipeline itself be reloadable when the F# source changes? Recommendation: out of scope for v1; use ix CLI's `watch` mode for hot-reload scenarios.
