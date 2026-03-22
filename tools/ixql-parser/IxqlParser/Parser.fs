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
