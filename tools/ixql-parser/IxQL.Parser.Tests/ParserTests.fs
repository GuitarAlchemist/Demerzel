module IxQL.Parser.Tests.ParserTests

open Xunit
open IxQL.Parser.Ast
open IxQL.Parser.Parser

// ── Helper ──

let shouldSucceed result =
    match result with
    | Ok v -> v
    | Error e -> failwith $"Parse failed: {e}"

let shouldFail result =
    match result with
    | Ok _ -> failwith "Expected parse failure"
    | Error _ -> ()

// ══════════════════════════════════════════════════
// Expression parsing
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse identifier expression`` () =
    let result = parseExpression "signals" |> shouldSucceed
    match result with
    | IdentExpr (Identifier "signals") -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse string literal`` () =
    let result = parseExpression "\"hello world\"" |> shouldSucceed
    match result with
    | StringExpr (StringLiteral "hello world") -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse float literal`` () =
    let result = parseExpression "0.85" |> shouldSucceed
    match result with
    | FloatExpr (FloatLiteral v) -> Assert.Equal(0.85, v)
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse tool invocation`` () =
    let result = parseExpression "ix.io.read(\"state/beliefs/*.json\")" |> shouldSucceed
    match result with
    | ToolCall inv ->
        Assert.Equal(2, inv.Namespace.Length)
        Assert.Equal(Identifier "read", inv.Method)
        Assert.Equal(1, inv.Args.Length)
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse tool invocation with named args`` () =
    let result = parseExpression "tars.classify(severity: \"critical\", reason: \"test\")" |> shouldSucceed
    match result with
    | ToolCall inv ->
        Assert.Equal<Identifier list>([Identifier "tars"], inv.Namespace)
        Assert.Equal(Identifier "classify", inv.Method)
        Assert.Equal(2, inv.Args.Length)
        match inv.Args.[0] with
        | Named (Identifier "severity", StringExpr (StringLiteral "critical")) -> ()
        | _ -> failwith $"Expected named arg, got {inv.Args.[0]}"
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Stage parsing
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse binding stage`` () =
    let result = parseStage "signals <- ix.io.read(\"state/signals/*.json\")" |> shouldSucceed
    match result with
    | BindingStage (Identifier "signals", ToolCallStage inv) ->
        Assert.Equal(Identifier "read", inv.Method)
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse chain with arrow`` () =
    let result = parseStage "signals → filter(status)" |> shouldSucceed
    match result with
    | ChainStage _ -> ()
    | _ -> failwith $"Expected ChainStage, got {result}"

[<Fact>]
let ``parse when guard`` () =
    let result = parseStage "when T >= 0.8: tars.analyze(data)" |> shouldSucceed
    match result with
    | WhenStage (MembershipTest(T, Some GreaterEqual, Some 0.8), ToolCallStage _) -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse governance gate`` () =
    let result = parseStage "bias_assessment" |> shouldSucceed
    match result with
    | GovernanceGateStage BiasAssessment -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse confidence calibration gate`` () =
    let result = parseStage "confidence_calibration" |> shouldSucceed
    match result with
    | GovernanceGateStage ConfidenceCalibration -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse invoke exact`` () =
    let result = parseStage "invoke @driver-cycle" |> shouldSucceed
    match result with
    | InvokeStage (L0Exact (Handle "driver-cycle")) -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse invoke alias`` () =
    let result = parseStage "invoke #audit" |> shouldSucceed
    match result with
    | InvokeStage (L1Alias (Identifier "audit")) -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse route semantic`` () =
    let result = parseStage "route(\"check governance health\")" |> shouldSucceed
    match result with
    | InvokeStage (L3Semantic("check governance health", None)) -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse fan_out`` () =
    let input = "fan_out(tars.a(), tars.b())"
    let result = parseStage input |> shouldSucceed
    match result with
    | FlowStage (FanOut stages) ->
        Assert.Equal(2, stages.Length)
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse parallel stage`` () =
    let input = "parallel(tars.a(), tars.b(), tars.c())"
    let result = parseStage input |> shouldSucceed
    match result with
    | ParallelStage stages ->
        Assert.Equal(3, stages.Length)
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Compound block
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse compound block`` () =
    let input = """compound:
    harvest new_patterns
    promote findings if T >= 0.9
    teach findings to seldon"""
    let result = parseStage input |> shouldSucceed
    match result with
    | CompoundStage steps ->
        Assert.Equal(3, steps.Length)
        match steps.[0] with
        | Harvest _ -> ()
        | _ -> failwith $"Expected Harvest, got {steps.[0]}"
        match steps.[1] with
        | Promote (_, MembershipTest(T, Some GreaterEqual, Some 0.9)) -> ()
        | _ -> failwith $"Expected Promote, got {steps.[1]}"
        match steps.[2] with
        | Teach (_, Identifier "seldon") -> ()
        | _ -> failwith $"Expected Teach, got {steps.[2]}"
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Assertions (Section 12)
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse assertion with checks`` () =
    let input = """assert input_quality: csv("train.csv")
    assert_check(not_null, message: "Training data must be complete")"""
    let result = parseStage input |> shouldSucceed
    match result with
    | AssertionStage a ->
        Assert.Equal(Identifier "input_quality", a.Name)
        Assert.Equal(1, a.Checks.Length)
        Assert.Equal(NotNull, a.Checks.[0].Condition)
        Assert.Equal(Some "Training data must be complete", a.Checks.[0].Message)
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse assertion with metric check`` () =
    let input = """assert model_quality: random_forest
    assert_check(metric f1_score >= 0.85, message: "F1 must be >= 0.85")"""
    let result = parseStage input |> shouldSucceed
    match result with
    | AssertionStage a ->
        Assert.Equal(Identifier "model_quality", a.Name)
        match a.Checks.[0].Condition with
        | MetricCheck (Identifier "f1_score", GreaterEqual, 0.85) -> ()
        | c -> failwith $"Expected MetricCheck, got {c}"
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse assertion with schema check`` () =
    let input = """assert data_shape: parquet
    assert_check(schema: "schemas/feature-schema.json")"""
    let result = parseStage input |> shouldSucceed
    match result with
    | AssertionStage a ->
        match a.Checks.[0].Condition with
        | SchemaCheck "schemas/feature-schema.json" -> ()
        | c -> failwith $"Expected SchemaCheck, got {c}"
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Type Providers (Section 14)
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse type provider from pipeline`` () =
    let input = """type AuditResult = provided(pipeline(@gov-audit-001))"""
    let result = parseString input |> shouldSucceed
    Assert.Equal(1, result.Types.Length)
    let t = result.Types.[0]
    Assert.Equal(Identifier "AuditResult", t.Name)
    match t.Source with
    | PipelineProvider (Handle "gov-audit-001") -> ()
    | s -> failwith $"Expected PipelineProvider, got {s}"

[<Fact>]
let ``parse type provider from mcp_tool`` () =
    let input = """type ChordAnalysis = provided(mcp_tool("ga.chord.analyze"))"""
    let result = parseString input |> shouldSucceed
    Assert.Equal(1, result.Types.Length)
    match result.Types.[0].Source with
    | McpToolProvider "ga.chord.analyze" -> ()
    | s -> failwith $"Expected McpToolProvider, got {s}"

[<Fact>]
let ``parse type provider from csv_header`` () =
    let input = """type FeatureRow = provided(csv_header("data/features.csv"))"""
    let result = parseString input |> shouldSucceed
    match result.Types.[0].Source with
    | CsvHeaderProvider "data/features.csv" -> ()
    | s -> failwith $"Expected CsvHeaderProvider, got {s}"

// ══════════════════════════════════════════════════
// Pipeline Declaration (Section 11)
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse pipeline declaration with metadata`` () =
    let input = """pipeline @driver-cycle "Driver Cycle" {
    version: "1.0.0"
    trigger: cron("0 6 * * *")
    invoke @gov-audit-001
}"""
    let result = parseString input |> shouldSucceed
    Assert.Equal(1, result.Pipelines.Length)
    let p = result.Pipelines.[0]
    Assert.Equal(Handle "driver-cycle", p.Handle)
    Assert.Equal(Some "Driver Cycle", p.DisplayName)
    Assert.Equal(Some (Semver "1.0.0"), p.Metadata.Version)
    match p.Metadata.Trigger with
    | Some (CronTrigger "0 6 * * *") -> ()
    | t -> failwith $"Expected CronTrigger, got {t}"
    Assert.True(p.Body.Length >= 1)

// ══════════════════════════════════════════════════
// Comments
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse with line comments`` () =
    let input = """-- This is a comment
signals <- ix.io.read("state/signals.json")
-- Another comment"""
    let result = parseString input |> shouldSucceed
    Assert.True(result.Comments.Length >= 1)
    Assert.Equal(1, result.Stages.Length)

// ══════════════════════════════════════════════════
// Multi-stage document parsing
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse multi-stage document`` () =
    let input = """-- Load state
beliefs <- ix.io.read("state/beliefs/*.belief.json")
evolution <- ix.io.read("state/evolution/*.evolution.json")

-- Validate
level_1 <- fan_out(
    tars.validate_schema("schemas/persona.schema.json"),
    tars.validate_schema("json-schema-meta")
)

-- Gate
confidence_calibration"""
    let result = parseString input |> shouldSucceed
    Assert.True(result.Stages.Length >= 3)
    Assert.True(result.Comments.Length >= 1)

// ══════════════════════════════════════════════════
// Tetravalent guard combinations
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse truth value T`` () =
    let result = parseStage "when T: tars.proceed()" |> shouldSucceed
    match result with
    | WhenStage (MembershipTest(T, None, None), _) -> ()
    | _ -> failwith $"Unexpected: {result}"

[<Fact>]
let ``parse truth value with conjunction`` () =
    let result = parseStage "when T >= 0.7 && C < 0.1: tars.proceed()" |> shouldSucceed
    match result with
    | WhenStage (GuardConjunction(MembershipTest(T, Some GreaterEqual, Some 0.7),
                                   MembershipTest(C, Some LessThan, Some 0.1)), _) -> ()
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Routing Levels
// ══════════════════════════════════════════════════

[<Fact>]
let ``parse route with threshold`` () =
    let result = parseStage "route(\"find related research\", threshold: 0.8)" |> shouldSucceed
    match result with
    | InvokeStage (L3Semantic("find related research", Some 0.8)) -> ()
    | _ -> failwith $"Unexpected: {result}"

// ══════════════════════════════════════════════════
// Error cases
// ══════════════════════════════════════════════════

[<Fact>]
let ``empty input produces empty document`` () =
    let result = parseString "" |> shouldSucceed
    Assert.Empty(result.Pipelines)
    Assert.Empty(result.Stages)

[<Fact>]
let ``comments-only input`` () =
    let input = """-- just a comment
-- and another"""
    let result = parseString input |> shouldSucceed
    Assert.Equal(2, result.Comments.Length)
    Assert.Empty(result.Stages)
