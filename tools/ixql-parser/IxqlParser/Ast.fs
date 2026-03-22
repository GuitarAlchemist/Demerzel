namespace IxqlParser

/// IxQL Abstract Syntax Tree
/// Covers pipeline declarations, stages, routing, MCP orchestration,
/// tetravalent gates, compound blocks, and flow control.
module Ast =

    /// Tetravalent logic values
    type TetravalentValue =
        | T  // True — verified with evidence
        | F  // False — refuted with evidence
        | U  // Unknown — insufficient evidence
        | C  // Contradictory — conflicting evidence

    /// Comparison operators used in filters and guards
    type ComparisonOp =
        | Eq       // ==
        | NotEq    // !=
        | Gt       // >
        | GtEq     // >=
        | Lt       // <
        | LtEq     // <=

    /// Boolean connectives in filter predicates
    type BoolOp =
        | And  // &&
        | Or   // ||

    /// Literal values
    type Literal =
        | StringLit of string
        | NumberLit of float
        | IntLit    of int
        | BoolLit   of bool

    /// Named argument in a function call: key: value
    type NamedArg = { Name: string; Value: Expr }

    /// Expressions — the core of IxQL
    and Expr =
        /// Identifier: variable name or dotted path (e.g., signal.severity)
        | Ident of string
        /// Literal value
        | LitExpr of Literal
        /// List expression: [a, b, c]
        | ListExpr of Expr list
        /// Function/method call: name(args...)
        | FuncCall of name: string * positional: Expr list * named: NamedArg list
        /// Dotted access: expr.field
        | DotAccess of Expr * string
        /// Pipeline chain: expr → expr
        | Pipeline of Expr list
        /// Binding: name <- expr
        | Binding of name: string * body: Expr
        /// fan_out block
        | FanOut of Expr list
        /// parallel block
        | Parallel of Expr list
        /// fan_in block
        | FanIn of sources: Expr list * sink: Expr
        /// filter(predicate)
        | Filter of Predicate
        /// when guard: tetravalent or boolean condition
        | When of condition: Condition * body: Expr
        /// Compound block: harvest, promote, teach, log directives
        | Compound of CompoundDirective list
        /// Ensemble: (pipeline1) + (pipeline2) => combiner
        | Ensemble of pipelines: Expr list * combiner: Expr
        /// Map expression: items.map(x => body)
        | MapExpr of source: Expr * param: string * body: Expr
        /// Comment (preserved in AST for tooling/LSP)
        | Comment of string
        /// I/O operations
        | Write of path: Expr * format: string option
        | Read of path: Expr
        | Alert of channel: Expr * message: Expr
        /// Throttle: throttle(count, unit)
        | Throttle of count: int * unit: string
        /// Window: window(duration, aggregation)
        | Window of duration: string * aggregation: string
        /// Debounce: debounce(duration)
        | Debounce of duration: string
        /// Head: head(n)
        | Head of int
        /// Invoke skill: invoke @handle(args)
        | Invoke of handle: string * named: NamedArg list
        /// Interpolated string: "text {{expr}} text"
        | InterpolatedString of parts: StringPart list

    /// Parts of an interpolated string
    and StringPart =
        | TextPart of string
        | ExprPart of Expr

    /// Filter predicates
    and Predicate =
        | Comparison of left: Expr * op: ComparisonOp * right: Expr
        | BoolCombine of left: Predicate * op: BoolOp * right: Predicate
        | InList of expr: Expr * values: Expr list
        | NotPred of Predicate

    /// Conditions for 'when' guards
    and Condition =
        /// Tetravalent gate: when T >= 0.7
        | TetravalentGate of value: TetravalentValue * op: ComparisonOp * threshold: float
        /// Boolean condition: when x > 5
        | BoolCondition of Predicate
        /// Bare tetravalent: when T, when F, when U, when C
        | BareTetravalent of TetravalentValue
        /// Identifier condition: when department_arg
        | IdentCondition of string
        /// Negated condition: when !expr
        | NegatedCondition of string

    /// Compound block directives
    and CompoundDirective =
        | Harvest of Expr
        | Promote of target: Expr * condition: Condition option
        | Teach of what: Expr * destination: Expr
        | Log of what: Expr * destination: Expr
        | CompoundWhen of condition: Condition * directive: CompoundDirective

    /// Routing levels (L0 exact → L4 ambient)
    type RoutingLevel =
        | L0_Exact     // Direct invocation by handle
        | L1_Named     // Route by skill name
        | L2_Tagged    // Route by capability tags
        | L3_Inferred  // Route by semantic similarity
        | L4_Ambient   // Broadcast to all matching

    /// Top-level IxQL program
    type Program = { Statements: Expr list }
