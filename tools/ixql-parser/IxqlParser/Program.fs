open IxqlParser.Ast
open IxqlParser.Parser

[<EntryPoint>]
let main argv =
    let sample = """-- Simple pipeline test
data <- ix.io.read("state/beliefs/*.json")
"""
    match parseIxql sample with
    | Ok prog ->
        printfn "Parsed %d statements" prog.Statements.Length
        let serial, par, fraction = analyzeSerialFraction prog
        printfn "Amdahl analysis: %d serial, %d parallel, %.1f%% serial fraction" serial par (fraction * 100.0)
        0
    | Error msg ->
        eprintfn "Parse error: %s" msg
        1
