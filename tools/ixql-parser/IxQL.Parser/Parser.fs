namespace IxQL.Parser

open FParsec
open IxQL.Parser.Ast

/// FParsec-based IxQL parser
/// Parses IxQL pipeline files into the Ast types
module Parser =

    // ── Helpers ──

    let ws = spaces
    let ws1 = spaces1

    let lineComment: Parser<string, unit> =
        pstring "--" >>. restOfLine true

    let wsOrComment: Parser<unit, unit> =
        skipMany (choice [ws1 |>> ignore; lineComment |>> ignore])

    let str s = pstring s .>> wsOrComment
    let strReturn s v = pstring s >>. wsOrComment >>% v

    let betweenParens p = between (str "(") (str ")") p
    let betweenBraces p = between (str "{") (str "}") p
    let betweenQuotes p = between (pchar '"') (pchar '"') p .>> wsOrComment

    let comma = str ","

    // ── Primitives ──

    let pIdentifierRaw: Parser<string, unit> =
        let isFirst c = isLetter c || c = '_'
        let isRest c = isLetter c || isDigit c || c = '_' || c = '-'
        many1Satisfy2 isFirst isRest .>> wsOrComment

    let pIdentifier: Parser<Identifier, unit> =
        pIdentifierRaw |>> Identifier

    let pStringLiteral: Parser<StringLiteral, unit> =
        betweenQuotes (manySatisfy (fun c -> c <> '"'))
        |>> StringLiteral

    let pStringRaw: Parser<string, unit> =
        betweenQuotes (manySatisfy (fun c -> c <> '"'))

    let pFloatLiteral: Parser<FloatLiteral, unit> =
        pfloat .>> wsOrComment |>> FloatLiteral

    let pSemver: Parser<Semver, unit> =
        betweenQuotes (many1Satisfy (fun c -> isDigit c || c = '.'))
        |>> Semver

    let pHandle: Parser<Handle, unit> =
        pchar '@' >>. many1Satisfy (fun c -> isLetter c || isDigit c || c = '-' || c = '_')
        .>> wsOrComment |>> Handle

    // ── Tetravalent ──

    let pTruthValue: Parser<TruthValue, unit> =
        choice [
            strReturn "T" T
            strReturn "F" F
            strReturn "U" U
            strReturn "C" C
        ]

    let pComparisonOp: Parser<ComparisonOp, unit> =
        choice [
            strReturn ">=" GreaterEqual
            strReturn "<=" LessEqual
            strReturn ">" GreaterThan
            strReturn "<" LessThan
            strReturn "==" Equal
            strReturn "!=" NotEqual
        ]

    // ── Governance Gates ──

    let pGovernanceGate: Parser<GovernanceGate, unit> =
        choice [
            strReturn "data_provenance_check" DataProvenanceCheck
            strReturn "bias_assessment" BiasAssessment
            strReturn "reversibility_check" ReversibilityCheck
            strReturn "confidence_calibration" ConfidenceCalibration
            strReturn "explanation_requirement" ExplanationRequirement
        ]

    // ── Expressions (forward reference) ──

    let pExpression, pExpressionRef = createParserForwardedToRef<Expression, unit>()
    let pStage, pStageRef = createParserForwardedToRef<Stage, unit>()

    // ── Tool Invocation ──
    // e.g., ix.io.read("state/beliefs/*.belief.json")
    //       tars.classify(severity: "critical", reason: "unprocessed")

    let pArgument: Parser<Argument, unit> =
        choice [
            attempt (pIdentifier .>> str ":" .>>. pExpression |>> Named)
            pExpression |>> Positional
        ]

    let pArgList: Parser<Argument list, unit> =
        sepBy pArgument comma

    /// Tool invocation requires either dotted name (ns.method) or name(args)
    let pToolInvocation: Parser<ToolInvocation, unit> =
        let pDottedName =
            pipe2
                (pIdentifierRaw .>> pchar '.' .>> wsOrComment)
                (sepBy1 pIdentifierRaw (pchar '.') .>> wsOrComment)
                (fun first rest -> first :: rest)
        // Dotted name with optional args: ns.method(args?)
        let dottedForm =
            pipe2
                pDottedName
                (opt (betweenParens pArgList))
                (fun parts args ->
                    let ns = parts |> List.take (parts.Length - 1) |> List.map Identifier
                    let meth = parts |> List.last |> Identifier
                    { Namespace = ns; Method = meth; Args = defaultArg args [] })
        // Simple name with required args: name(args)
        let simpleForm =
            pipe2
                (pIdentifierRaw)
                (betweenParens pArgList)
                (fun name args ->
                    { Namespace = []; Method = Identifier name; Args = args })
        attempt dottedForm <|> simpleForm

    // ── Expression implementation ──

    let pExpressionAtom: Parser<Expression, unit> =
        choice [
            attempt (pToolInvocation |>> ToolCall)
            pStringLiteral |>> StringExpr
            attempt (pFloatLiteral |>> FloatExpr)
            pIdentifier |>> IdentExpr
        ]

    // Handle dot access: expr.field.field2
    let pDotAccess: Parser<Expression, unit> =
        pExpressionAtom .>>. many (pchar '.' >>. wsOrComment >>. pIdentifier)
        |>> fun (expr, fields) ->
            fields |> List.fold (fun acc field -> DotAccess(acc, field)) expr

    do pExpressionRef.Value <- pDotAccess

    // ── Trigger Sources ──

    let pTriggerSource: Parser<TriggerSource, unit> =
        choice [
            attempt (str "cron" >>. betweenParens pStringRaw |>> CronTrigger)
            attempt (str "webhook" >>. betweenParens (pStringRaw .>> comma .>>. pStringRaw)
                     |>> fun (p, e) -> WebhookTrigger(p, e))
            attempt (str "watch" >>. betweenParens pStringRaw |>> FileWatcherTrigger)
            strReturn "manual" ManualTrigger
            strReturn "on_invoke" OnInvokeTrigger
        ]

    // ── Pipeline Metadata ──

    let pVersionDecl = str "version:" >>. pSemver |>> Some
    let pTriggerDecl = str "trigger:" >>. pTriggerSource |>> Some
    let pDescriptionDecl = str "description:" >>. pStringRaw |>> Some

    let pMetadata: Parser<PipelineMetadata, unit> =
        pipe3
            (opt (attempt pVersionDecl) |>> Option.flatten)
            (opt (attempt pTriggerDecl) |>> Option.flatten)
            (opt (attempt pDescriptionDecl) |>> Option.flatten)
            (fun v t d -> { Version = v; Trigger = t; Description = d })

    // ── MOG Guards ──

    let pMogGuardAtom: Parser<MogGuard, unit> =
        choice [
            attempt (
                pTruthValue .>>. opt pComparisonOp .>>. opt (pfloat .>> wsOrComment)
                |>> fun ((tv, op), threshold) -> MembershipTest(tv, op, threshold)
            )
            attempt (
                pchar '?' >>. pIdentifier .>>. betweenParens (sepBy pExpression comma)
                |>> fun (id, args) -> SemanticPredicate(id, args)
            )
        ]

    let pMogGuard: Parser<MogGuard, unit> =
        chainl1 pMogGuardAtom (str "&&" >>% fun l r -> GuardConjunction(l, r))

    // ── Compound Steps ──

    let pCompoundStep: Parser<CompoundStep, unit> =
        choice [
            attempt (str "harvest" >>. pExpression |>> Harvest)
            attempt (str "promote" >>. pExpression .>> str "if" .>>. pMogGuard
                     |>> fun (e, g) -> Promote(e, g))
            attempt (str "teach" >>. pExpression .>> str "to" .>>. pIdentifier
                     |>> fun (e, id) -> Teach(e, id))
            attempt (str "log" >>. pExpression .>>. opt (str "to" >>. pExpression)
                     |>> fun (e, target) -> CompoundLog(e, target))
        ]

    let pCompoundBlock: Parser<CompoundStep list, unit> =
        str "compound:" >>. many1 (wsOrComment >>. pCompoundStep)

    // ── Routing Levels ──

    let pRoutingLevel: Parser<RoutingLevel, unit> =
        choice [
            // L0: invoke @handle
            attempt (str "invoke" >>. pHandle |>> L0Exact)
            // L1: invoke #alias
            attempt (str "invoke" >>. pchar '#' >>. pIdentifierRaw .>> wsOrComment
                     |>> (Identifier >> L1Alias))
            // L3: route("intent")
            attempt (str "route" >>. betweenParens (
                pStringRaw .>>. opt (comma >>. str "threshold:" >>. pfloat .>> wsOrComment)
                |>> fun (intent, thresh) -> L3Semantic(intent, thresh)
            ))
        ]

    // ── Flow Control ──

    let pFlowControl: Parser<FlowControl, unit> =
        choice [
            attempt (str "fan_out" >>. betweenParens (sepBy1 pStage comma) |>> FanOut)
            attempt (str "filter" >>. betweenParens pExpression |>> Filter)
            attempt (str "throttle" >>. betweenParens (pExpression .>> comma .>>. pExpression)
                     |>> fun (r, u) -> Throttle(r, u))
            attempt (str "retry" >>. betweenParens (pExpression .>> comma .>>. pStringRaw)
                     |>> fun (m, b) -> RetryPolicy(m, b))
            attempt (str "window" >>. betweenParens (pExpression .>> comma .>>. pStringRaw)
                     |>> fun (d, a) -> Window(d, a))
            attempt (str "debounce" >>. betweenParens pExpression |>> Debounce)
        ]

    // ── Assertion ──

    let pAssertionSeverity: Parser<AssertionSeverity, unit> =
        choice [
            strReturn "error" SevError
            strReturn "warning" SevWarning
            strReturn "info" SevInfo
        ]

    let pAssertionCondition: Parser<AssertionCondition, unit> =
        choice [
            strReturn "not_null" NotNull
            strReturn "no_nulls" NoNulls
            attempt (str "null_fraction" >>. pComparisonOp .>>. (pfloat .>> wsOrComment)
                     |>> fun (op, v) -> NullFraction(op, v))
            attempt (str "type" >>. str ":" >>. pIdentifierRaw |>> TypeCheck)
            attempt (str "schema" >>. str ":" >>. pStringRaw |>> SchemaCheck)
            attempt (str "governance" >>. str ":" >>. pGovernanceGate |>> GovernanceCheck)
            attempt (str "governed" >>. pIdentifierRaw |>> GovernedCheck)
            attempt (str "metric" >>. pIdentifier .>>. pComparisonOp .>>. (pfloat .>> wsOrComment)
                     |>> fun ((id, op), v) -> MetricCheck(id, op, v))
            attempt (str "truth" >>. str "is" >>. pTruthValue |>> TruthIsCheck)
            attempt (str "truth" >>. pComparisonOp .>>. (pfloat .>> wsOrComment)
                     |>> fun (op, v) -> TruthCheck(op, v))
            attempt (str "range" >>. str ":" >>. (pfloat .>> wsOrComment) .>> str ".." .>>. (pfloat .>> wsOrComment)
                     |>> fun (lo, hi) -> RangeCheck(lo, hi))
            attempt (str "min" >>. str ">=" >>. (pfloat .>> wsOrComment) |>> MinCheck)
            attempt (str "max" >>. str "<=" >>. (pfloat .>> wsOrComment) |>> MaxCheck)
        ]

    let pAssertionMessage: Parser<string, unit> =
        str "message:" >>. pStringRaw

    let pAssertionCheck: Parser<AssertionCheck, unit> =
        str "assert_check" >>. betweenParens (
            pAssertionCondition .>>. opt (comma >>. pAssertionMessage)
            |>> fun (cond, msg) -> { Condition = cond; Message = msg }
        )

    let pAssertion: Parser<Assertion, unit> =
        str "assert" >>.
        opt (attempt pAssertionSeverity) .>>.
        pIdentifier .>> str ":" .>>.
        pExpression .>>.
        many1 (wsOrComment >>. pAssertionCheck)
        |>> fun (((sev, name), subject), checks) ->
            { Severity = sev; Name = name; Subject = subject; Checks = checks }

    // ── Type Providers (Section 14) ──

    let pProviderSource: Parser<ProviderSource, unit> =
        choice [
            attempt (str "schema" >>. betweenParens pStringRaw |>> SchemaProvider)
            attempt (str "pipeline" >>. betweenParens pHandle |>> PipelineProvider)
            attempt (str "mcp_tool" >>. betweenParens pStringRaw |>> McpToolProvider)
            attempt (str "database" >>. betweenParens pStringRaw |>> DatabaseProvider)
            attempt (str "csv_header" >>. betweenParens pStringRaw |>> CsvHeaderProvider)
        ]

    let pTypeDecl: Parser<TypeDecl, unit> =
        str "type" >>. pIdentifier .>> str "=" .>> str "provided" .>>. betweenParens pProviderSource
        |>> fun (name, source) -> { Name = name; Source = source }

    // ── Stage implementation ──

    let pStageAtom: Parser<Stage, unit> =
        choice [
            // Binding: ident <- stage
            attempt (pIdentifier .>> str "<-" .>>. pStage |>> BindingStage)
            // When guard
            attempt (str "when" >>. pMogGuard .>> str ":" .>>. pStage |>> WhenStage)
            // Compound block
            attempt (pCompoundBlock |>> CompoundStage)
            // Governance gates (standalone)
            attempt (pGovernanceGate |>> GovernanceGateStage)
            // Assertion
            attempt (pAssertion |>> AssertionStage)
            // Invoke / routing
            attempt (pRoutingLevel |>> InvokeStage)
            // Flow control
            attempt (pFlowControl |>> FlowStage)
            // Parallel
            attempt (str "parallel" >>. betweenParens (sepBy1 pStage comma) |>> ParallelStage)
            // Write
            attempt (str "write" >>. betweenParens (pExpression .>> comma .>>. pExpression)
                     |>> fun (p, f) -> WriteStage(p, f))
            // Alert
            attempt (str "alert" >>. betweenParens (
                pStringRaw .>> comma .>>. pExpression
                |>> fun (ch, tmpl) -> AlertStage(ch, tmpl)))
            // Log
            attempt (str "log" >>. pExpression .>>. opt (str "to" >>. pExpression)
                     |>> fun (e, target) ->
                         CompoundStage [CompoundLog(e, target)])
            // Tool call (must be after keywords)
            attempt (pToolInvocation |>> ToolCallStage)
            // Plain expression
            attempt (pExpression |>> ExpressionStage)
        ]

    let pChain: Parser<Stage, unit> =
        chainl1 pStageAtom (str "→" <|> str "->" >>% fun l r -> ChainStage(l, r))

    do pStageRef.Value <-
        wsOrComment >>. pChain

    // ── Pipeline Declaration ──

    let pPipelineDeclaration: Parser<PipelineDeclaration, unit> =
        str "pipeline" >>.
        pHandle .>>.
        opt (attempt pStringRaw) .>>.
        betweenBraces (pMetadata .>>. many (wsOrComment >>. pStage))
        |>> fun ((handle, displayName), (meta, stages)) ->
            { Handle = handle
              DisplayName = displayName
              Metadata = meta
              Body = stages }

    // ── Top-level document ──

    /// Whitespace only (no comment consumption)
    let wsOnly: Parser<unit, unit> = skipMany (skipSatisfy (fun c -> c = ' ' || c = '\t' || c = '\r' || c = '\n'))

    let pTopLevel: Parser<Choice<PipelineDeclaration, Stage, TypeDecl, Assertion, string>, unit> =
        choice [
            attempt (pPipelineDeclaration |>> Choice1Of5)
            attempt (pTypeDecl |>> Choice3Of5)
            attempt (pAssertion |>> Choice4Of5)
            attempt (lineComment |>> Choice5Of5)
            attempt (pStage |>> Choice2Of5)
        ]

    let pDocument: Parser<IxQLDocument, unit> =
        wsOnly >>. many (pTopLevel .>> wsOnly) .>> eof
        |>> fun items ->
            let mutable comments = []
            let mutable pipelines = []
            let mutable stages = []
            let mutable types = []
            let mutable assertions = []
            for item in items do
                match item with
                | Choice1Of5 p -> pipelines <- p :: pipelines
                | Choice2Of5 s -> stages <- s :: stages
                | Choice3Of5 t -> types <- t :: types
                | Choice4Of5 a -> assertions <- a :: assertions
                | Choice5Of5 c -> comments <- c :: comments
            { Comments = List.rev comments
              Pipelines = List.rev pipelines
              Stages = List.rev stages
              Types = List.rev types
              Assertions = List.rev assertions }

    // ── Public API ──

    /// Parse an IxQL string into a document AST
    let parseString (input: string) : Result<IxQLDocument, string> =
        ParserRunner.runParser pDocument input

    /// Parse an IxQL file into a document AST
    let parseFile (path: string) : Result<IxQLDocument, string> =
        let input = System.IO.File.ReadAllText(path)
        parseString input

    /// Parse a single stage from a string
    let parseStage (input: string) : Result<Stage, string> =
        ParserRunner.runParser (wsOrComment >>. pStage .>> wsOrComment .>> eof) input

    /// Parse a single expression from a string
    let parseExpression (input: string) : Result<Expression, string> =
        ParserRunner.runParser (wsOrComment >>. pExpression .>> wsOrComment .>> eof) input
