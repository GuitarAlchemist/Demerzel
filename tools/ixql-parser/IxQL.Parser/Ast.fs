namespace IxQL.Parser

/// IxQL Abstract Syntax Tree types
/// Maps to the 14 sections of sci-ml-pipelines.ebnf
module Ast =

    // ── Section 11: Pipeline Identity ──

    type Handle = Handle of string

    type Semver = Semver of string

    type TriggerSource =
        | CronTrigger of string
        | WebhookTrigger of provider: string * eventType: string
        | FileWatcherTrigger of pattern: string
        | ManualTrigger
        | OnInvokeTrigger

    type PipelineMetadata =
        { Version: Semver option
          Trigger: TriggerSource option
          Description: string option }

    // ── Section 1: Pipeline Architecture ──

    type Identifier = Identifier of string

    type StringLiteral = StringLiteral of string

    type FloatLiteral = FloatLiteral of float

    type Expression =
        | IdentExpr of Identifier
        | StringExpr of StringLiteral
        | FloatExpr of FloatLiteral
        | ToolCall of ToolInvocation
        | DotAccess of Expression * Identifier
        | ListExpr of Expression list

    and ToolInvocation =
        { Namespace: Identifier list
          Method: Identifier
          Args: Argument list }

    and Argument =
        | Positional of Expression
        | Named of Identifier * Expression

    // ── Tetravalent Logic ──

    type TruthValue = T | F | U | C

    type ComparisonOp =
        | GreaterEqual
        | LessEqual
        | GreaterThan
        | LessThan
        | Equal
        | NotEqual

    // ── Section 7: Governance Gates ──

    type GovernanceGate =
        | DataProvenanceCheck
        | BiasAssessment
        | ReversibilityCheck
        | ConfidenceCalibration
        | ExplanationRequirement

    // ── Section 12: Assertions ──

    type AssertionSeverity =
        | SevError
        | SevWarning
        | SevInfo

    type AssertionCondition =
        | NotNull
        | NoNulls
        | NullFraction of ComparisonOp * float
        | TypeCheck of string
        | RangeCheck of float * float
        | MinCheck of float
        | MaxCheck of float
        | MeanCheck of ComparisonOp * float
        | MetricCheck of Identifier * ComparisonOp * float
        | TruthCheck of ComparisonOp * float
        | TruthIsCheck of TruthValue
        | SchemaCheck of string
        | GovernanceCheck of GovernanceGate
        | GovernedCheck of string
        | CustomPredicate of Identifier * Expression list

    type AssertionCheck =
        { Condition: AssertionCondition
          Message: string option }

    type Assertion =
        { Severity: AssertionSeverity option
          Name: Identifier
          Subject: Expression
          Checks: AssertionCheck list }

    // ── Section 11: Routing Levels ──

    type RoutingLevel =
        | L0Exact of Handle
        | L1Alias of Identifier
        | L2Pattern of string
        | L3Semantic of intent: string * threshold: float option
        | L4Ambient of condition: Expression * target: PipelineRef

    and PipelineRef =
        | HandleRef of Handle
        | AliasRef of Identifier
        | SemanticRef of string

    // ── Section 10: MCP Orchestration ──

    type MogGuard =
        | MembershipTest of TruthValue * ComparisonOp option * float option
        | SemanticPredicate of Identifier * Expression list
        | GuardConjunction of MogGuard * MogGuard

    // ── Section 9: Reactive / Flow ──

    type FlowControl =
        | FanOut of Stage list
        | FanIn of Expression list * Stage
        | Filter of Expression
        | Throttle of rate: Expression * unit: Expression
        | RetryPolicy of maxAttempts: Expression * backoff: string
        | CircuitBreaker of maxFailures: Expression * resetDuration: Expression
        | Window of duration: Expression * aggregation: string
        | Debounce of Expression

    // ── Core Pipeline Stages ──

    and Stage =
        | BindingStage of Identifier * Stage
        | ToolCallStage of ToolInvocation
        | FlowStage of FlowControl
        | WhenStage of MogGuard * Stage
        | ChainStage of Stage * Stage
        | GovernanceGateStage of GovernanceGate
        | WriteStage of path: Expression * format: Expression
        | AlertStage of channel: string * template: Expression
        | GithubStage of action: string * target: Expression
        | LogStage of Expression
        | CompoundStage of CompoundStep list
        | AssertionStage of Assertion
        | InvokeStage of RoutingLevel
        | ParallelStage of Stage list
        | ExpressionStage of Expression

    and CompoundStep =
        | Harvest of Expression
        | Promote of Expression * MogGuard
        | Teach of Expression * Identifier
        | CompoundLog of Expression * Expression option

    // ── Section 14: Type Providers & Distillation ──

    type ProviderSource =
        | SchemaProvider of string
        | PipelineProvider of Handle
        | McpToolProvider of string
        | DatabaseProvider of string
        | CsvHeaderProvider of string

    type TypeDecl =
        { Name: Identifier
          Source: ProviderSource }

    // ── Top-level Pipeline Declaration ──

    type PipelineDeclaration =
        { Handle: Handle
          DisplayName: string option
          Metadata: PipelineMetadata
          Body: Stage list }

    /// A complete IxQL file can contain multiple top-level constructs
    type IxQLDocument =
        { Comments: string list
          Pipelines: PipelineDeclaration list
          Stages: Stage list
          Types: TypeDecl list
          Assertions: Assertion list }
