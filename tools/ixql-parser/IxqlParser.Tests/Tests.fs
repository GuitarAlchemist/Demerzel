module Tests

open Xunit
open IxqlParser.Ast
open IxqlParser.Parser

// ── Helper ──────────────────────────────────────────────────

let mustParse source =
    match parseIxql source with
    | Ok prog -> prog
    | Error msg -> failwithf "Parse failed: %s" msg

let mustParseExpr source =
    match parseExpr source with
    | Ok expr -> expr
    | Error msg -> failwithf "Parse failed: %s" msg

// ── Comments ────────────────────────────────────────────────

[<Fact>]
let ``Parse line comment`` () =
    let prog = mustParse "-- This is a comment\n"
    Assert.Equal(1, prog.Statements.Length)
    match prog.Statements.[0] with
    | Comment c -> Assert.Equal("This is a comment", c)
    | _ -> failwith "Expected Comment"

// ── Bindings ────────────────────────────────────────────────

[<Fact>]
let ``Parse simple binding with function call`` () =
    let prog = mustParse """signals <- ix.io.read("state/signals/*.json")
"""
    Assert.Equal(1, prog.Statements.Length)
    match prog.Statements.[0] with
    | Binding(name, FuncCall(fn, pos, _)) ->
        Assert.Equal("signals", name)
        Assert.Equal("ix.io.read", fn)
        Assert.Equal(1, pos.Length)
    | _ -> failwith "Expected Binding with FuncCall"

// ── Pipeline chains ─────────────────────────────────────────

[<Fact>]
let ``Parse pipeline with arrow operator`` () =
    let expr = mustParseExpr """csv -> normalize -> random_forest"""
    match expr with
    | Pipeline stages ->
        Assert.Equal(3, stages.Length)
    | _ -> failwith "Expected Pipeline"

[<Fact>]
let ``Parse pipeline with Unicode arrow`` () =
    let expr = mustParseExpr "csv \u2192 normalize \u2192 random_forest"
    match expr with
    | Pipeline stages -> Assert.Equal(3, stages.Length)
    | _ -> failwith "Expected Pipeline"

// ── Function calls with named args ──────────────────────────

[<Fact>]
let ``Parse function call with named arguments`` () =
    let expr = mustParseExpr """tars.analyze(mode: "drift")"""
    match expr with
    | FuncCall(name, _, named) ->
        Assert.Equal("tars.analyze", name)
        Assert.Equal(1, named.Length)
        Assert.Equal("mode", named.[0].Name)
    | _ -> failwith "Expected FuncCall"

// ── Filter expressions ──────────────────────────────────────

[<Fact>]
let ``Parse filter with comparison`` () =
    let expr = mustParseExpr """filter(confidence >= 0.7)"""
    match expr with
    | Filter(Comparison(Ident "confidence", GtEq, LitExpr(NumberLit n))) ->
        Assert.Equal(0.7, n)
    | _ -> failwith "Expected Filter with Comparison"

[<Fact>]
let ``Parse filter with boolean AND`` () =
    let expr = mustParseExpr """filter(age_days > 3 && status == "active")"""
    match expr with
    | Filter(BoolCombine(Comparison(_, Gt, _), And, Comparison(_, Eq, _))) -> ()
    | _ -> failwith "Expected Filter with BoolCombine"

// ── When guards ─────────────────────────────────────────────

[<Fact>]
let ``Parse tetravalent gate`` () =
    let expr = mustParseExpr """when T >= 0.7: tars.deploy()"""
    match expr with
    | When(TetravalentGate(T, GtEq, 0.7), FuncCall("tars.deploy", _, _)) -> ()
    | _ -> failwith "Expected When with TetravalentGate"

// ── fan_out ─────────────────────────────────────────────────

[<Fact>]
let ``Parse fan_out with multiple branches`` () =
    let expr = mustParseExpr """fan_out(pipeline_a, pipeline_b, pipeline_c)"""
    match expr with
    | FanOut branches -> Assert.Equal(3, branches.Length)
    | _ -> failwith "Expected FanOut"

// ── parallel ────────────────────────────────────────────────

[<Fact>]
let ``Parse parallel block`` () =
    let expr = mustParseExpr """parallel(health, analysis, triggers)"""
    match expr with
    | Parallel branches -> Assert.Equal(3, branches.Length)
    | _ -> failwith "Expected Parallel"

// ── Literals ────────────────────────────────────────────────

[<Fact>]
let ``Parse string literal`` () =
    let expr = mustParseExpr "\"hello world\""
    match expr with
    | LitExpr(StringLit s) -> Assert.Equal("hello world", s)
    | _ -> failwith "Expected StringLit"

[<Fact>]
let ``Parse integer literal`` () =
    let expr = mustParseExpr "42"
    match expr with
    | LitExpr(IntLit n) -> Assert.Equal(42, n)
    | _ -> failwith "Expected IntLit"

[<Fact>]
let ``Parse float literal`` () =
    let expr = mustParseExpr "0.95"
    match expr with
    | LitExpr(NumberLit n) -> Assert.Equal(0.95, n)
    | _ -> failwith "Expected NumberLit"

// ── List expressions ────────────────────────────────────────

[<Fact>]
let ``Parse list expression`` () =
    let expr = mustParseExpr """["a", "b", "c"]"""
    match expr with
    | ListExpr items -> Assert.Equal(3, items.Length)
    | _ -> failwith "Expected ListExpr"

// ── Head ────────────────────────────────────────────────────

[<Fact>]
let ``Parse head`` () =
    let expr = mustParseExpr "head(5)"
    match expr with
    | Head n -> Assert.Equal(5, n)
    | _ -> failwith "Expected Head"

// ── Throttle ────────────────────────────────────────────────

[<Fact>]
let ``Parse throttle`` () =
    let expr = mustParseExpr "throttle(4, concurrent)"
    match expr with
    | Throttle(count, unit) ->
        Assert.Equal(4, count)
        Assert.Equal("concurrent", unit)
    | _ -> failwith "Expected Throttle"

// ── Window ──────────────────────────────────────────────────

[<Fact>]
let ``Parse window`` () =
    let expr = mustParseExpr "window(1h, avg)"
    match expr with
    | Window(dur, agg) ->
        Assert.Equal("1h", dur)
        Assert.Equal("avg", agg)
    | _ -> failwith "Expected Window"

// ── Debounce ────────────────────────────────────────────────

[<Fact>]
let ``Parse debounce`` () =
    let expr = mustParseExpr "debounce(5s)"
    match expr with
    | Debounce dur -> Assert.Equal("5s", dur)
    | _ -> failwith "Expected Debounce"

// ── Invoke ──────────────────────────────────────────────────

[<Fact>]
let ``Parse invoke with handle`` () =
    let expr = mustParseExpr "invoke @gov-audit-001(level: 3)"
    match expr with
    | Invoke(handle, args) ->
        Assert.Equal("gov-audit-001", handle)
        Assert.Equal(1, args.Length)
        Assert.Equal("level", args.[0].Name)
    | _ -> failwith "Expected Invoke"

// ── Compound block ──────────────────────────────────────────

[<Fact>]
let ``Parse compound block with harvest and teach`` () =
    let prog = mustParse """compound:
    harvest findings
    teach findings to seldon
"""
    Assert.Equal(1, prog.Statements.Length)
    match prog.Statements.[0] with
    | Compound directives ->
        Assert.Equal(2, directives.Length)
        match directives.[0] with
        | Harvest(Ident "findings") -> ()
        | _ -> failwith "Expected Harvest"
        match directives.[1] with
        | Teach(Ident "findings", Ident "seldon") -> ()
        | _ -> failwith "Expected Teach"
    | _ -> failwith "Expected Compound"

// ── Amdahl's Law analysis ───────────────────────────────────

[<Fact>]
let ``Amdahl analysis identifies serial stages`` () =
    let prog = mustParse """data <- ix.io.read("input.csv")
result <- data -> normalize -> classify
"""
    let serial, par, fraction = analyzeSerialFraction prog
    Assert.True(serial > 0, "Should have serial stages")
    Assert.Equal(0, par)
    Assert.Equal(1.0, fraction)

[<Fact>]
let ``Amdahl analysis identifies parallel stages in fan_out`` () =
    let prog = mustParse """results <- fan_out(pipeline_a, pipeline_b, pipeline_c)
"""
    let serial, par, fraction = analyzeSerialFraction prog
    Assert.True(par > 0, "Should have parallel stages")
    Assert.True(fraction < 1.0, "Serial fraction should be < 1.0")

[<Fact>]
let ``Amdahl analysis mixed serial and parallel`` () =
    let prog = mustParse """data <- ix.io.read("input.csv")
enriched <- data -> normalize
results <- fan_out(pipeline_a, pipeline_b)
final <- results -> output
"""
    let serial, par, fraction = analyzeSerialFraction prog
    Assert.True(serial > 0, "Should have serial stages")
    Assert.True(par > 0, "Should have parallel stages")
    Assert.True(fraction > 0.0 && fraction < 1.0, "Fraction should be between 0 and 1")

// ── Multi-statement programs ────────────────────────────────

[<Fact>]
let ``Parse multi-statement program with comments`` () =
    let prog = mustParse """-- Phase 1: Load data
signals <- ix.io.read("state/signals/*.json")
-- Phase 2: Process
processed <- signals -> filter(confidence >= 0.5)
"""
    Assert.Equal(4, prog.Statements.Length)

// ── Markdown comments ────────────────────────────────────────

[<Fact>]
let ``Parse markdown comment`` () =
    let prog = mustParse "--- ## Step 1: Safety Gate\n"
    Assert.Equal(1, prog.Statements.Length)
    match prog.Statements.[0] with
    | MarkdownComment c -> Assert.Equal("## Step 1: Safety Gate", c)
    | _ -> failwith "Expected MarkdownComment"

[<Fact>]
let ``Markdown comment distinct from line comment`` () =
    let prog = mustParse "--- **bold** doc\n-- plain note\n"
    Assert.Equal(2, prog.Statements.Length)
    match prog.Statements.[0] with
    | MarkdownComment _ -> ()
    | _ -> failwith "Expected MarkdownComment for ---"
    match prog.Statements.[1] with
    | Comment _ -> ()
    | _ -> failwith "Expected Comment for --"

// ── LOLLI Analysis ──────────────────────────────────────────

[<Fact>]
let ``analyzeLolli detects dead binding`` () =
    let prog = mustParse """data <- ix.io.read("input.csv")
unused <- ix.io.read("other.csv")
result <- data -> normalize
"""
    let report = analyzeLolli prog
    Assert.Contains("unused", report.DeadBindings)
    Assert.DoesNotContain("data", report.DeadBindings)
    Assert.True(report.LolliScore > 0.0, "Should have non-zero LOLLI score")

[<Fact>]
let ``analyzeLolli correctly excludes referenced bindings`` () =
    let prog = mustParse """signals <- ix.io.read("state/signals/*.json")
processed <- signals -> filter(confidence >= 0.5)
output <- processed -> tars.deploy()
"""
    let report = analyzeLolli prog
    Assert.DoesNotContain("signals", report.DeadBindings)
    Assert.DoesNotContain("processed", report.DeadBindings)
    Assert.Equal(3, report.TotalBindings)

[<Fact>]
let ``analyzeLolli handles fan_out references`` () =
    let prog = mustParse """data <- ix.io.read("input.csv")
results <- fan_out(data, data, data)
"""
    let report = analyzeLolli prog
    Assert.DoesNotContain("data", report.DeadBindings)

// ── L3: Orphaned fan_out branch detection ───────────────────

[<Fact>]
let ``L3 detects orphaned fan_out branch`` () =
    // pipeline_a and pipeline_b are defined as bindings, but branch_c is not
    let prog = mustParse """data <- ix.io.read("input.csv")
pipeline_a <- data -> normalize
pipeline_b <- data -> classify
result <- fan_out(pipeline_a, pipeline_b, branch_c)
output <- result -> write("out.json")
"""
    let report = analyzeLolli prog
    // branch_c is not defined as a binding — orphaned
    Assert.True(report.OrphanedBranches.Length > 0, "Should detect orphaned fan_out branches")
    Assert.Contains("branch_c", report.OrphanedBranches)
    Assert.DoesNotContain("pipeline_a", report.OrphanedBranches)
    Assert.DoesNotContain("pipeline_b", report.OrphanedBranches)

[<Fact>]
let ``L3 no orphaned branches when all referenced`` () =
    let prog = mustParse """pipeline_a <- ix.io.read("a.csv")
pipeline_b <- ix.io.read("b.csv")
result <- fan_out(pipeline_a, pipeline_b)
output <- result -> write("out.json")
"""
    let report = analyzeLolli prog
    // pipeline_a and pipeline_b are referenced as bindings AND as fan_out branches
    // Since they appear in both bindings and references, they are not orphaned
    Assert.DoesNotContain("pipeline_a", report.OrphanedBranches)
    Assert.DoesNotContain("pipeline_b", report.OrphanedBranches)

[<Fact>]
let ``L3 mixed orphaned and consumed branches`` () =
    // alpha is defined as a binding; orphan_x is not
    let prog = mustParse """alpha <- ix.io.read("a.csv")
result <- fan_out(alpha, orphan_x)
merged <- result -> write("out.json")
"""
    let report = analyzeLolli prog
    // orphan_x has no binding — orphaned branch
    Assert.Contains("orphan_x", report.OrphanedBranches)
    // alpha is a binding — not orphaned
    Assert.DoesNotContain("alpha", report.OrphanedBranches)

// ── L4: Transitive closure — unreachable bindings ───────────

[<Fact>]
let ``L4 detects unreachable binding with no path to output`` () =
    let prog = mustParse """data <- ix.io.read("input.csv")
useless <- ix.io.read("junk.csv")
result <- data -> normalize
final <- result -> write("output.json")
"""
    let report = analyzeLolli prog
    Assert.Contains("useless", report.UnreachableBindings)
    Assert.DoesNotContain("data", report.UnreachableBindings)
    Assert.DoesNotContain("result", report.UnreachableBindings)
    Assert.DoesNotContain("final", report.UnreachableBindings)

[<Fact>]
let ``L4 all bindings reachable when chain leads to output`` () =
    let prog = mustParse """raw <- ix.io.read("input.csv")
clean <- raw -> normalize
result <- clean -> classify
output <- result -> write("output.json")
"""
    let report = analyzeLolli prog
    Assert.Empty(report.UnreachableBindings)

[<Fact>]
let ``L4 detects unreachable with compound output`` () =
    let prog = mustParse """findings <- ix.io.read("data.json")
orphan <- ix.io.read("other.json")
compound:
    harvest findings
    teach findings to seldon
"""
    let report = analyzeLolli prog
    Assert.Contains("orphan", report.UnreachableBindings)
    Assert.DoesNotContain("findings", report.UnreachableBindings)

[<Fact>]
let ``L4 transitive chain — intermediate bindings are reachable`` () =
    let prog = mustParse """step1 <- ix.io.read("input.csv")
step2 <- step1 -> normalize
step3 <- step2 -> classify
alert("ops-channel", step3)
"""
    let report = analyzeLolli prog
    Assert.Empty(report.UnreachableBindings)

// ── Teach target validation ─────────────────────────────────

[<Fact>]
let ``Teach to seldon is valid`` () =
    let prog = mustParse """findings <- ix.io.read("data.json")
compound:
    teach findings to seldon
"""
    let report = analyzeLolli prog
    Assert.Empty(report.InvalidTeachTargets)

[<Fact>]
let ``Teach to known department is valid`` () =
    let prog = mustParse """findings <- ix.io.read("data.json")
compound:
    teach findings to psychohistory
"""
    let report = analyzeLolli prog
    Assert.Empty(report.InvalidTeachTargets)

[<Fact>]
let ``Teach to non-existent curriculum is invalid`` () =
    let prog = mustParse """findings <- ix.io.read("data.json")
compound:
    teach findings to chaos_patterns
"""
    let report = analyzeLolli prog
    Assert.Contains("chaos_patterns", report.InvalidTeachTargets)

[<Fact>]
let ``Teach to multiple targets — mixed valid and invalid`` () =
    let prog = mustParse """findings <- ix.io.read("data.json")
compound:
    teach findings to seldon
    teach findings to fake_department
    teach findings to mathematics
"""
    let report = analyzeLolli prog
    Assert.Contains("fake_department", report.InvalidTeachTargets)
    Assert.DoesNotContain("seldon", report.InvalidTeachTargets)
    Assert.DoesNotContain("mathematics", report.InvalidTeachTargets)

// ── Error handling ──────────────────────────────────────────

[<Fact>]
let ``Parse error returns Error result`` () =
    let result = parseIxql "<<<invalid>>>"
    match result with
    | Error _ -> ()
    | Ok _ -> failwith "Expected parse error"

// ── Pipeline with filter and function call ──────────────────

[<Fact>]
let ``Parse binding with pipeline chain`` () =
    let prog = mustParse """classified <- signals -> filter(status == "active") -> tars.classify(severity: "high")
"""
    Assert.Equal(1, prog.Statements.Length)
    match prog.Statements.[0] with
    | Binding("classified", Pipeline stages) ->
        Assert.Equal(3, stages.Length)
    | _ -> failwith "Expected Binding with Pipeline"
