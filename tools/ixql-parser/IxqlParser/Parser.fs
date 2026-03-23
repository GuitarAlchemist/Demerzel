namespace IxqlParser

open FParsec
open IxqlParser.Ast

/// IxQL FParsec Parser
/// Parses the IxQL pipeline language into an AST.
module Parser =

    // ── Helpers ──────────────────────────────────────────────────

    let ws = spaces
    let ws1 = spaces1

    /// Parse string then consume trailing whitespace
    let symbol s = pstring s .>> ws

    /// Parse between parentheses
    let parens p = between (symbol "(") (symbol ")") p

    /// Parse between square brackets
    let brackets p = between (symbol "[") (symbol "]") p

    /// Comma-separated list
    let commaSep p = sepBy (p .>> ws) (symbol ",")

    // ── Comments ────────────────────────────────────────────────

    let markdownComment: Parser<Expr, unit> =
        pstring "---" >>. restOfLine true |>> (fun s -> MarkdownComment(s.Trim()))

    let lineComment: Parser<Expr, unit> =
        pstring "--" >>. restOfLine true |>> (fun s -> Comment(s.Trim()))

    // ── Identifiers ─────────────────────────────────────────────

    let identChar = letter <|> digit <|> anyOf "_-"

    let identifier: Parser<string, unit> =
        many1Chars2 (letter <|> pchar '_') identChar .>> ws

    /// Dotted identifier: a.b.c (also allows underscores and hyphens in segments)
    let dottedIdent: Parser<string, unit> =
        many1Chars2 (letter <|> pchar '_') (identChar <|> pchar '.') .>> ws

    /// Duration-like token: 1h, 5s, 30s, etc. (digit-prefixed alphanumeric)
    let durationToken: Parser<string, unit> =
        many1Chars (letter <|> digit) .>> ws

    // ── Literals ────────────────────────────────────────────────

    let stringLiteral: Parser<Literal, unit> =
        let normalChar = noneOf "\"\\"
        let escapedChar = pchar '\\' >>. anyChar
        between (pchar '"') (pchar '"')
            (manyChars (normalChar <|> escapedChar))
        |>> StringLit .>> ws

    let numberLiteral: Parser<Literal, unit> =
        pfloat .>> ws |>> fun n ->
            if n = System.Math.Floor(n) && n >= float System.Int32.MinValue && n <= float System.Int32.MaxValue then
                IntLit(int n)
            else
                NumberLit n

    let boolLiteral: Parser<Literal, unit> =
        (stringReturn "true" (BoolLit true) <|> stringReturn "false" (BoolLit false)) .>> ws

    let literal = (stringLiteral <|> numberLiteral <|> boolLiteral)

    // ── Forward references ──────────────────────────────────────

    let expr, exprRef = createParserForwardedToRef<Expr, unit>()
    let predicate, predicateRef = createParserForwardedToRef<Predicate, unit>()
    let condition, conditionRef = createParserForwardedToRef<Condition, unit>()
    let compoundDirective, compoundDirectiveRef = createParserForwardedToRef<CompoundDirective, unit>()

    // ── Comparison operators ────────────────────────────────────

    let comparisonOp: Parser<ComparisonOp, unit> =
        choice [
            attempt (symbol ">=" >>% GtEq)
            attempt (symbol "<=" >>% LtEq)
            attempt (symbol "==" >>% Eq)
            attempt (symbol "!=" >>% NotEq)
            symbol ">" >>% Gt
            symbol "<" >>% Lt
        ]

    // ── Tetravalent ─────────────────────────────────────────────

    let tetravalentValue: Parser<TetravalentValue, unit> =
        choice [
            stringReturn "T" T
            stringReturn "F" F
            stringReturn "U" U
            stringReturn "C" C
        ] .>> ws

    // ── String with interpolation ───────────────────────────────

    let interpolatedString: Parser<Expr, unit> =
        let textPart = many1Chars (noneOf "\"{}") |>> TextPart
        let exprPart = between (pstring "{{") (pstring "}}") (dottedIdent |>> (Ident >> ExprPart))
        let curlyFallback = pstring "{" |>> (fun s -> TextPart s)
        let part = (attempt exprPart) <|> curlyFallback <|> textPart
        between (pchar '"') (pchar '"') (many part) .>> ws
        |>> fun parts ->
            if parts |> List.forall (function TextPart _ -> true | _ -> false) then
                let text = parts |> List.map (function TextPart s -> s | _ -> "") |> String.concat ""
                LitExpr(StringLit text)
            else
                InterpolatedString parts

    // ── Named arguments ─────────────────────────────────────────

    let namedArg: Parser<NamedArg, unit> =
        attempt (identifier .>> symbol ":" .>>. expr)
        |>> fun (name, value) -> { Name = name; Value = value }

    /// Parse argument list — mix of positional and named args
    let argList: Parser<Expr list * NamedArg list, unit> =
        let positionalOrNamed =
            (attempt (namedArg |>> Choice2Of2))
            <|> (expr |>> Choice1Of2)
        commaSep positionalOrNamed |>> fun items ->
            let pos = items |> List.choose (function Choice1Of2 e -> Some e | _ -> None)
            let named = items |> List.choose (function Choice2Of2 n -> Some n | _ -> None)
            (pos, named)

    // ── List expression ─────────────────────────────────────────

    let listExpr = brackets (commaSep expr) |>> ListExpr

    // ── Invoke ──────────────────────────────────────────────────

    let invokeExpr =
        symbol "invoke" >>. pchar '@' >>. identifier .>>. parens (commaSep namedArg)
        |>> fun (handle, args) -> Invoke(handle, args)

    // ── fan_out / parallel / filter / head / write / alert ──────

    let fanOutExpr =
        symbol "fan_out" >>. parens (commaSep expr) |>> FanOut

    let parallelExpr =
        symbol "parallel" >>. parens (commaSep expr) |>> Parallel

    let filterExpr =
        symbol "filter" >>. parens predicate |>> Filter

    let headExpr =
        symbol "head" >>. parens (pint32 .>> ws) |>> Head

    let writeExpr =
        symbol "write" >>. parens (
            expr .>>. opt (symbol "," >>. identifier)
        ) |>> fun (path, fmt) -> Write(path, fmt)

    let alertExpr =
        symbol "alert" >>. parens (
            expr .>> symbol "," .>>. expr
        ) |>> fun (ch, msg) -> Alert(ch, msg)

    let throttleExpr =
        symbol "throttle" >>. parens (
            pint32 .>> ws .>> symbol "," .>>. identifier
        ) |>> fun (count, unit) -> Throttle(count, unit)

    let windowExpr =
        symbol "window" >>. parens (
            durationToken .>> symbol "," .>>. identifier
        ) |>> fun (dur, agg) -> Window(dur, agg)

    let debounceExpr =
        symbol "debounce" >>. parens durationToken |>> Debounce

    // ── Function call ───────────────────────────────────────────

    let funcCall =
        attempt (
            dottedIdent .>>. parens argList
            |>> fun (name, (pos, named)) -> FuncCall(name, pos, named)
        )

    // ── Simple ident ────────────────────────────────────────────

    let identExpr = dottedIdent |>> Ident

    // ── Atomic expression ───────────────────────────────────────

    let atomicExpr: Parser<Expr, unit> =
        choice [
            attempt invokeExpr
            attempt fanOutExpr
            attempt parallelExpr
            attempt filterExpr
            attempt headExpr
            attempt writeExpr
            attempt alertExpr
            attempt throttleExpr
            attempt windowExpr
            attempt debounceExpr
            attempt funcCall
            attempt listExpr
            attempt interpolatedString
            literal |>> LitExpr
            identExpr
        ]

    // ── When guards ─────────────────────────────────────────────

    let whenExpr: Parser<Expr, unit> =
        symbol "when" >>. condition .>> symbol ":" .>>. expr
        |>> fun (cond, body) -> When(cond, body)

    // ── Compound block ──────────────────────────────────────────

    let harvestDir = symbol "harvest" >>. expr |>> Harvest

    let promoteDir =
        symbol "promote" >>. expr .>>. opt (symbol "if" >>. condition)
        |>> fun (target, cond) -> Promote(target, cond)

    let teachDir =
        symbol "teach" >>. expr .>> symbol "to" .>>. expr
        |>> fun (what, dest) -> Teach(what, dest)

    let logDir =
        symbol "log" >>. expr .>> symbol "to" .>>. expr
        |>> fun (what, dest) -> Log(what, dest)

    let compoundWhenDir =
        symbol "when" >>. condition .>> symbol ":" .>>. compoundDirective
        |>> fun (cond, dir) -> CompoundWhen(cond, dir)

    do compoundDirectiveRef.Value <-
        choice [
            attempt harvestDir
            attempt promoteDir
            attempt teachDir
            attempt logDir
            attempt compoundWhenDir
        ]

    let compoundBlock =
        symbol "compound:" >>. many1 (ws >>. compoundDirective .>> ws)
        |>> Compound

    // ── Predicates ──────────────────────────────────────────────

    let inListPred =
        attempt (expr .>> symbol "in" .>>. (brackets (commaSep expr) <|> parens (commaSep expr)))
        |>> fun (e, vals) -> InList(e, vals)

    let comparisonPred =
        attempt (expr .>>. comparisonOp .>>. expr)
        |>> fun ((l, op), r) -> Comparison(l, op, r)

    let atomicPredicate =
        attempt inListPred
        <|> attempt comparisonPred

    do predicateRef.Value <-
        let boolOp =
            (symbol "&&" >>% And) <|> (symbol "||" >>% Or)
        chainl1 atomicPredicate (boolOp |>> fun op -> (fun l r -> BoolCombine(l, op, r)))

    // ── Conditions ──────────────────────────────────────────────

    let tetravalentGate =
        attempt (tetravalentValue .>>. comparisonOp .>>. pfloat .>> ws)
        |>> fun ((tv, op), threshold) -> TetravalentGate(tv, op, threshold)

    let negatedCond =
        attempt (pchar '!' >>. identifier) |>> NegatedCondition

    do conditionRef.Value <-
        choice [
            attempt tetravalentGate
            attempt negatedCond
            attempt (predicate |>> BoolCondition)
            identifier |>> IdentCondition
        ]

    // ── Pipeline operator ───────────────────────────────────────

    let pipelineOp: Parser<unit, unit> =
        (pstring "\u2192" <|> pstring "->") >>. ws >>% ()

    // ── Top-level expression ────────────────────────────────────

    let primaryExpr: Parser<Expr, unit> =
        choice [
            attempt compoundBlock
            attempt whenExpr
            attempt atomicExpr
        ]

    let pipelineExpr =
        sepBy1 primaryExpr (attempt pipelineOp)
        |>> fun exprs ->
            match exprs with
            | [single] -> single
            | multiple -> Pipeline multiple

    // ── Wire up the expr forward ref ────────────────────────────

    do exprRef.Value <- pipelineExpr

    // ── Statements ──────────────────────────────────────────────

    let bindingStmt: Parser<Expr, unit> =
        attempt (
            identifier .>> symbol "<-" .>>. pipelineExpr
            |>> fun (name, body) -> Binding(name, body)
        )

    let statement: Parser<Expr, unit> =
        ws >>. choice [
            attempt markdownComment
            lineComment
            bindingStmt
            pipelineExpr
        ] .>> ws

    // ── Program ─────────────────────────────────────────────────

    let program: Parser<Program, unit> =
        ws >>. many statement .>> eof
        |>> fun stmts -> { Statements = stmts }

    // ── Public API ──────────────────────────────────────────────

    let parseIxql (source: string) : Result<Program, string> =
        match run program source with
        | ParserResult.Success(result, _, _) -> Result.Ok result
        | ParserResult.Failure(errorMsg, _, _) -> Result.Error errorMsg

    let parseExpr (source: string) : Result<Expr, string> =
        match run (ws >>. pipelineExpr .>> eof) source with
        | ParserResult.Success(result, _, _) -> Result.Ok result
        | ParserResult.Failure(errorMsg, _, _) -> Result.Error errorMsg

    // ── LOLLI Analysis: Dead Binding Detection ─────────────────

    /// Collects all binding names defined in the AST (left side of <-)
    let rec private collectBindings (expr: Expr) : string list =
        match expr with
        | Binding(name, body) -> name :: collectBindings body
        | Pipeline stages -> stages |> List.collect collectBindings
        | FanOut exprs | Parallel exprs -> exprs |> List.collect collectBindings
        | FanIn(sources, sink) -> (sources |> List.collect collectBindings) @ collectBindings sink
        | When(_, body) -> collectBindings body
        | Compound directives -> directives |> List.collect collectBindingsFromDirective
        | Ensemble(pipelines, combiner) -> (pipelines |> List.collect collectBindings) @ collectBindings combiner
        | MapExpr(source, _, body) -> collectBindings source @ collectBindings body
        | _ -> []

    and private collectBindingsFromDirective (dir: CompoundDirective) : string list =
        match dir with
        | Harvest e | Promote(e, _) -> collectBindings e
        | Teach(what, dest) -> collectBindings what @ collectBindings dest
        | Log(what, dest) -> collectBindings what @ collectBindings dest
        | CompoundWhen(_, d) -> collectBindingsFromDirective d

    /// Collects all referenced names (identifiers used in expressions)
    let rec private collectReferences (expr: Expr) : string list =
        match expr with
        | Ident name -> [name]
        | Binding(_, body) -> collectReferences body
        | Pipeline stages -> stages |> List.collect collectReferences
        | FanOut exprs | Parallel exprs | ListExpr exprs -> exprs |> List.collect collectReferences
        | FanIn(sources, sink) -> (sources |> List.collect collectReferences) @ collectReferences sink
        | FuncCall(_, pos, named) ->
            (pos |> List.collect collectReferences) @ (named |> List.collect (fun na -> collectReferences na.Value))
        | DotAccess(e, _) -> collectReferences e
        | Filter pred -> collectRefsFromPredicate pred
        | When(cond, body) -> collectRefsFromCondition cond @ collectReferences body
        | Compound directives -> directives |> List.collect collectRefsFromDirective
        | Ensemble(pipelines, combiner) -> (pipelines |> List.collect collectReferences) @ collectReferences combiner
        | MapExpr(source, _, body) -> collectReferences source @ collectReferences body
        | Write(path, _) -> collectReferences path
        | Read path -> collectReferences path
        | Alert(ch, msg) -> collectReferences ch @ collectReferences msg
        | Invoke(_, named) -> named |> List.collect (fun na -> collectReferences na.Value)
        | InterpolatedString parts ->
            parts |> List.collect (function ExprPart e -> collectReferences e | _ -> [])
        | _ -> []

    and private collectRefsFromPredicate (pred: Predicate) : string list =
        match pred with
        | Comparison(l, _, r) -> collectReferences l @ collectReferences r
        | BoolCombine(l, _, r) -> collectRefsFromPredicate l @ collectRefsFromPredicate r
        | InList(e, vals) -> collectReferences e @ (vals |> List.collect collectReferences)
        | NotPred p -> collectRefsFromPredicate p

    and private collectRefsFromCondition (cond: Condition) : string list =
        match cond with
        | BoolCondition pred -> collectRefsFromPredicate pred
        | IdentCondition name -> [name]
        | NegatedCondition name -> [name]
        | _ -> []

    and private collectRefsFromDirective (dir: CompoundDirective) : string list =
        match dir with
        | Harvest e -> collectReferences e
        | Promote(e, _) -> collectReferences e
        | Teach(what, dest) -> collectReferences what @ collectReferences dest
        | Log(what, dest) -> collectReferences what @ collectReferences dest
        | CompoundWhen(cond, d) -> collectRefsFromCondition cond @ collectRefsFromDirective d

    // ── L3: Orphaned fan_out branch detection ─────────────────

    /// Collects fan_out branch identifiers that are used inside a fan_out
    /// but whose output is never referenced by the parent binding context.
    /// A fan_out(a, b, c) is orphaned if a branch's result is never consumed
    /// downstream of the fan_out — detected by checking if the branch name
    /// appears as a reference outside the fan_out itself.
    let rec private collectFanOutBranches (expr: Expr) : string list =
        match expr with
        | Binding(_, body) -> collectFanOutBranches body
        | Pipeline stages -> stages |> List.collect collectFanOutBranches
        | FanOut exprs ->
            // Each branch identifier inside a fan_out
            let branchNames =
                exprs |> List.choose (fun e ->
                    match e with
                    | Ident name -> Some name
                    | FuncCall(name, _, _) -> Some name
                    | _ -> None)
            branchNames
        | Parallel exprs -> exprs |> List.collect collectFanOutBranches
        | FanIn(sources, sink) -> (sources |> List.collect collectFanOutBranches) @ collectFanOutBranches sink
        | When(_, body) -> collectFanOutBranches body
        | Compound directives -> directives |> List.collect collectFanOutBranchesFromDir
        | Ensemble(pipelines, combiner) -> (pipelines |> List.collect collectFanOutBranches) @ collectFanOutBranches combiner
        | MapExpr(source, _, body) -> collectFanOutBranches source @ collectFanOutBranches body
        | _ -> []

    and private collectFanOutBranchesFromDir (dir: CompoundDirective) : string list =
        match dir with
        | Harvest e | Promote(e, _) -> collectFanOutBranches e
        | Teach(what, dest) -> collectFanOutBranches what @ collectFanOutBranches dest
        | Log(what, dest) -> collectFanOutBranches what @ collectFanOutBranches dest
        | CompoundWhen(_, d) -> collectFanOutBranchesFromDir d

    /// Detects orphaned fan_out branches: branch identifiers inside fan_out()
    /// that are not defined as bindings in the program. If a fan_out references
    /// an identifier that was never bound, its output cannot be collected.
    /// Function calls (e.g., pipeline_a()) are excluded — they produce their own results.
    let private detectOrphanedBranches (prog: Program) : string list =
        let allFanOutBranches =
            prog.Statements |> List.collect collectFanOutBranches |> Set.ofList
        let allBindings =
            prog.Statements |> List.collect collectBindings |> Set.ofList
        // A fan_out branch is orphaned if it's an identifier not defined
        // as a binding anywhere in the program — it's a dangling reference
        // whose output cannot be collected by any downstream consumer.
        allFanOutBranches
        |> Set.toList
        |> List.filter (fun name -> not (Set.contains name allBindings))

    // ── L4: Transitive closure — reachability from outputs ────

    /// Collects all output sinks: write(), alert(), teach, log, promote, harvest
    let rec private collectOutputRefs (expr: Expr) : string list =
        match expr with
        | Write(path, _) -> collectReferences path
        | Alert(ch, msg) -> collectReferences ch @ collectReferences msg
        | Binding(_, body) -> collectOutputRefs body
        | Pipeline stages -> stages |> List.collect collectOutputRefs
        | FanOut exprs | Parallel exprs -> exprs |> List.collect collectOutputRefs
        | FanIn(sources, sink) -> (sources |> List.collect collectOutputRefs) @ collectOutputRefs sink
        | When(_, body) -> collectOutputRefs body
        | Compound directives -> directives |> List.collect collectOutputRefsFromDir
        | Ensemble(pipelines, combiner) -> (pipelines |> List.collect collectOutputRefs) @ collectOutputRefs combiner
        | MapExpr(source, _, body) -> collectOutputRefs source @ collectOutputRefs body
        | _ -> []

    and private collectOutputRefsFromDir (dir: CompoundDirective) : string list =
        match dir with
        | Harvest e -> collectReferences e
        | Promote(e, _) -> collectReferences e
        | Teach(what, dest) -> collectReferences what @ collectReferences dest
        | Log(what, dest) -> collectReferences what @ collectReferences dest
        | CompoundWhen(_, d) -> collectOutputRefsFromDir d

    /// Checks if a statement (top-level expression) contains any output sink
    let rec private hasOutputSink (expr: Expr) : bool =
        match expr with
        | Write _ | Alert _ -> true
        | Binding(_, body) -> hasOutputSink body
        | Pipeline stages -> stages |> List.exists hasOutputSink
        | FanOut exprs | Parallel exprs -> exprs |> List.exists hasOutputSink
        | FanIn(sources, sink) -> (sources |> List.exists hasOutputSink) || hasOutputSink sink
        | When(_, body) -> hasOutputSink body
        | Compound directives -> directives |> List.exists hasOutputSinkDir
        | Ensemble(pipelines, combiner) -> (pipelines |> List.exists hasOutputSink) || hasOutputSink combiner
        | MapExpr(source, _, body) -> hasOutputSink source || hasOutputSink body
        | _ -> false

    and private hasOutputSinkDir (dir: CompoundDirective) : bool =
        match dir with
        | Harvest _ | Promote _ | Teach _ | Log _ -> true  // compound directives are outputs
        | CompoundWhen(_, d) -> hasOutputSinkDir d

    /// Build a dependency map: binding name -> set of names it references
    let private buildDependencyMap (stmts: Expr list) : Map<string, Set<string>> =
        let rec collect (expr: Expr) : (string * Set<string>) list =
            match expr with
            | Binding(name, body) ->
                let refs = collectReferences body |> Set.ofList
                (name, refs) :: collect body
            | Pipeline stages -> stages |> List.collect collect
            | FanOut exprs | Parallel exprs -> exprs |> List.collect collect
            | FanIn(sources, sink) -> (sources |> List.collect collect) @ collect sink
            | When(_, body) -> collect body
            | _ -> []
        stmts |> List.collect collect |> Map.ofList

    /// Transitive closure: given a set of "needed" names, walk backwards
    /// through the dependency map to find all transitively needed bindings.
    let private transitiveClosure (depMap: Map<string, Set<string>>) (seeds: Set<string>) : Set<string> =
        let rec walk (frontier: Set<string>) (visited: Set<string>) =
            if Set.isEmpty frontier then visited
            else
                let newVisited = Set.union visited frontier
                let nextFrontier =
                    frontier
                    |> Set.toList
                    |> List.collect (fun name ->
                        match Map.tryFind name depMap with
                        | Some deps -> Set.toList deps
                        | None -> [])
                    |> Set.ofList
                    |> fun s -> Set.difference s newVisited
                walk nextFrontier newVisited
        walk seeds Set.empty

    /// Detect unreachable bindings: bindings not on any path to an output.
    /// Traces backwards from write/alert/compound outputs to find all
    /// transitively needed bindings, then flags the rest.
    let private detectUnreachable (prog: Program) : string list =
        let allBindings =
            prog.Statements |> List.collect collectBindings |> Set.ofList
        // Collect names directly referenced by output sinks
        let outputRefs =
            prog.Statements |> List.collect collectOutputRefs |> Set.ofList
        // Also: bindings whose body itself contains an output sink are "needed"
        let bindingsWithOutputs =
            prog.Statements |> List.collect (fun stmt ->
                match stmt with
                | Binding(name, body) when hasOutputSink body -> [name]
                | _ -> [])
            |> Set.ofList
        let seeds = Set.union outputRefs bindingsWithOutputs
        let depMap = buildDependencyMap prog.Statements
        let reachable = transitiveClosure depMap seeds
        // Unreachable = bound but not reachable from any output
        allBindings
        |> Set.toList
        |> List.filter (fun name -> not (Set.contains name reachable))

    // ── Teach target validation ──────────────────────────────────

    /// Known Seldon curriculum departments (Streeling University)
    let private knownSeldonCurriculum = Set.ofList [
        "audio-engineering"; "cognitive-science"; "computer-science"
        "cybernetics"; "data-visualization"; "futurology"
        "guitar-alchemist-academy"; "guitar-studies"; "mathematics"
        "music"; "musicology"; "philosophy"; "physics"
        "product-management"; "psychohistory"; "world-music-languages"
        // The generic "seldon" target is always valid (routes to Seldon Plan)
        "seldon"
    ]

    /// Collect all teach targets from the program
    let rec private collectTeachTargets (expr: Expr) : string list =
        match expr with
        | Binding(_, body) -> collectTeachTargets body
        | Pipeline stages -> stages |> List.collect collectTeachTargets
        | FanOut exprs | Parallel exprs -> exprs |> List.collect collectTeachTargets
        | FanIn(sources, sink) -> (sources |> List.collect collectTeachTargets) @ collectTeachTargets sink
        | When(_, body) -> collectTeachTargets body
        | Compound directives -> directives |> List.collect collectTeachTargetsFromDir
        | Ensemble(pipelines, combiner) -> (pipelines |> List.collect collectTeachTargets) @ collectTeachTargets combiner
        | MapExpr(source, _, body) -> collectTeachTargets source @ collectTeachTargets body
        | _ -> []

    and private collectTeachTargetsFromDir (dir: CompoundDirective) : string list =
        match dir with
        | Teach(_, dest) ->
            match dest with
            | Ident name -> [name]
            | _ -> []
        | CompoundWhen(_, d) -> collectTeachTargetsFromDir d
        | _ -> []

    /// Validate teach targets against known Seldon curriculum.
    /// Returns list of invalid target names.
    let private validateTeachTargets (prog: Program) : string list =
        let targets =
            prog.Statements |> List.collect collectTeachTargets
        targets
        |> List.filter (fun name -> not (Set.contains name knownSeldonCurriculum))
        |> List.distinct

    // ── Combined LOLLI Analysis ─────────────────────────────────

    /// Analyze LOLLI: find dead (unreferenced) bindings, orphaned fan_out
    /// branches, unreachable computations, and invalid teach targets.
    /// Returns a LolliReport with all findings and a composite score.
    let analyzeLolli (prog: Program) : LolliReport =
        let bindings =
            prog.Statements |> List.collect collectBindings
        let references =
            prog.Statements |> List.collect collectReferences |> Set.ofList
        let dead =
            bindings |> List.filter (fun name -> not (Set.contains name references))
        let orphaned = detectOrphanedBranches prog
        let unreachable = detectUnreachable prog
        let invalidTeach = validateTeachTargets prog
        let total = bindings.Length
        let totalIssues = dead.Length + orphaned.Length + unreachable.Length + invalidTeach.Length
        let score =
            if total = 0 && totalIssues = 0 then 0.0
            elif total = 0 then 1.0
            else float totalIssues / float (max total totalIssues)
        { DeadBindings = dead
          OrphanedBranches = orphaned
          UnreachableBindings = unreachable
          InvalidTeachTargets = invalidTeach
          TotalBindings = total
          LolliScore = score }

    // ── Amdahl's Law: Serial Fraction Analysis ─────────────────

    /// Identifies whether pipeline stages are serial or parallelizable.
    /// fan_out and parallel blocks are parallel; everything else is serial.
    /// Returns (serial_count, parallel_count, serial_fraction).
    let analyzeSerialFraction (prog: Program) : int * int * float =
        let rec countStages (expr: Expr) =
            match expr with
            | Pipeline stages ->
                stages |> List.map countStages |> List.fold (fun (s, p) (s2, p2) -> (s + s2, p + p2)) (0, 0)
            | FanOut exprs | Parallel exprs ->
                let innerCounts = exprs |> List.map countStages
                let totalInner = innerCounts |> List.fold (fun (s, p) (s2, p2) -> (s + s2, p + p2)) (0, 0)
                (fst totalInner, snd totalInner + List.length exprs)
            | Binding(_, body) -> countStages body
            | When(_, body) -> countStages body
            | Compound _ -> (1, 0)
            | Filter _ | FuncCall _ | Write _ | Read _ | Alert _ -> (1, 0)
            | _ -> (1, 0)
        let serial, par =
            prog.Statements
            |> List.map countStages
            |> List.fold (fun (s, p) (s2, p2) -> (s + s2, p + p2)) (0, 0)
        let total = serial + par
        let fraction = if total = 0 then 0.0 else float serial / float total
        (serial, par, fraction)
