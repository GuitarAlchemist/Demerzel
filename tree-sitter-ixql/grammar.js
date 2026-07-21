/**
 * tree-sitter grammar for IxQL — ML Pipeline & Reactive Data Flow Language
 *
 * Based on: grammars/sci-ml-pipelines.ebnf
 * Consumed by: ix-lsp crate (incremental parsing), VS Code extension
 * See: docs/superpowers/specs/2026-03-24-ixql-lsp-design.md
 *
 * Grammar sections mirror the EBNF:
 *   1. Pipeline Architecture
 *   2. Data Sources
 *   3. Preprocessing
 *   4. Models
 *   5. Evaluation
 *   6. Deployment
 *   7. Governance Integration
 *   8. ix-Specific Patterns
 *   9. I/O & Reactive Patterns
 *  10. MCP Orchestration
 *  11. Evolution Hooks
 *  12. Assertions
 */

module.exports = grammar({
  name: "ixql",

  extras: ($) => [$.comment, /\s/],

  word: ($) => $.identifier,

  // GLR conflicts. Every entry here is a place where one token of lookahead is
  // not enough to decide a reduction; tree-sitter forks, parses both ways, and
  // keeps the branch that yields a valid tree. We prefer this over prec.right,
  // which hard-codes one interpretation and silently misparses the other. Each
  // conflict below is either a rule against its own optional/repeat boundary (a
  // self-conflict, written as a single-rule entry) or two rules that share a
  // prefix. They were surfaced one at a time by `tree-sitter generate`; the set
  // is minimal in the sense that removing any one reintroduces a generate error.
  //
  //   namespace_path        `a.b.c` — extend the path vs. stop for tool_invocation's trailing `.method`
  //   streaming_source_expr `stdin` with an optional trailing format_spec, before the next statement
  //   output_sink_expr      `stdout` with an optional trailing format_spec (the `stdin` case's twin)
  //   preprocessing_stage   a stage's optional trailing clauses vs. the next `->` stage
  //   guard_conjunction     `a && b && c` associativity
  //   simple_pipeline       a bare data_source vs. a data_source that begins an arrow chain
  //   conditional_step_expr dangling-else: bind `else` to the nearest `if`
  //   pipeline_expr/ensemble_pipeline  a simple_pipeline alone vs. the first arm of an ensemble
  conflicts: ($) => [
    [$.namespace_path],
    [$.streaming_source_expr],
    [$.output_sink_expr],
    [$.preprocessing_stage],
    [$.guard_conjunction],
    [$.simple_pipeline],
    [$.conditional_step_expr],
    [$.pipeline_expr, $.ensemble_pipeline],
  ],

  rules: {
    // =========================================================
    // Top-level: a document is a sequence of statements
    // =========================================================

    source_file: ($) =>
      repeat(
        choice(
          $.pipeline_statement,
          $.reactive_pipeline_statement,
          $.mcp_pipeline_statement,
          $.assertion_statement,
          // binding_statement is intentionally NOT a top-level statement. The
          // spec (sci-ml-pipelines.ebnf) defines `binding_step` only as an
          // mcp_step, and mcp_step_expr already includes it. Listing it here as
          // well made `identifier <- ...` reducible two ways and blocked
          // generate. Removed to match the spec; bindings still parse inside
          // MCP pipelines.
          $.comment,
        ),
      ),

    // =========================================================
    // Section 1: Pipeline Architecture
    // =========================================================

    pipeline_statement: ($) =>
      seq(
        optional(seq($.identifier, "<-")),
        $.pipeline_expr,
        optional($.governance_annotation),
      ),

    pipeline_expr: ($) =>
      choice($.ensemble_pipeline, $.simple_pipeline),

    simple_pipeline: ($) =>
      seq(
        $.data_source,
        repeat(seq($.arrow, $.pipeline_stage)),
      ),

    ensemble_pipeline: ($) =>
      seq($.simple_pipeline, "+", $.simple_pipeline, "=>", $.combiner),

    pipeline_stage: ($) =>
      choice(
        $.preprocessing_stage,
        $.model_stage,
        $.evaluation_stage,
        $.deployment_stage,
        $.governance_gate,
        $.flow_control_expr,
        $.mcp_step_expr,
        $.compound_phase,
        $.assertion_check,
      ),

    // =========================================================
    // Section 2: Data Sources
    // =========================================================

    data_source: ($) =>
      choice(
        $.file_source,
        $.database_source,
        $.api_source,
        $.streaming_source_expr,
        $.governance_state_source,
        $.git_history_source,
        $.mcp_tool_source,
        $.identifier, // named data source reference
      ),

    file_source: ($) =>
      seq(
        choice("csv", "json", "parquet"),
        "(",
        $.string_literal,
        optional(seq(",", $.format_spec)),
        ")",
      ),

    database_source: ($) =>
      seq("database", "(", $.string_literal, ")"),

    api_source: ($) =>
      seq("api", "(", $.string_literal, ")"),

    streaming_source_expr: ($) =>
      choice(
        seq("websocket", "(", $.string_literal, optional(seq(",", $.string_literal)), ")"),
        seq("watch", "(", $.path_pattern, ")", optional($.debounce_expr)),
        seq("sse", "(", $.string_literal, ")"),
        seq("webhook", "(", $.provider, ",", $.string_literal, ")"),
        seq("cron", "(", $.string_literal, ")"),
        // `stdin` may carry an optional format_spec. Because source_file is a
        // bare repeat with no statement terminator, a format_spec keyword (csv,
        // json, ...) can also begin the *next* statement (file_source starts
        // with `csv`/`json`/`parquet`). One token of lookahead cannot tell
        // `stdin csv(...)` (one source) from `stdin` / `csv(...)` (two
        // statements). The [$.streaming_source_expr] conflict lets the parser
        // decide by which reading actually yields a valid tree.
        seq("stdin", optional($.format_spec)),
        seq("subscribe", "(", $.string_literal, ",", $.string_literal, ")"),
        seq("cdc", "(", $.string_literal, ",", $.string_literal, ")"),
        seq("grpc", "(", $.string_literal, ",", $.string_literal, ")"),
      ),

    governance_state_source: ($) => "governance_state",
    git_history_source: ($) => "git_history",
    mcp_tool_source: ($) => seq("mcp_tool_output", "(", $.string_literal, ")"),

    provider: ($) =>
      choice("github", "discord", "gitlab", "generic"),

    path_pattern: ($) => $.string_literal,
    format_spec: ($) => choice("json", "csv", "text", "binary"),

    // =========================================================
    // Section 3: Preprocessing
    // =========================================================

    preprocessing_stage: ($) =>
      choice(
        $.cleaning_expr,
        $.transformation_expr,
        $.feature_engineering_expr,
        $.splitting_expr,
        seq(
          $.cleaning_expr,
          $.arrow,
          $.feature_engineering_expr,
          $.arrow,
          $.splitting_expr,
        ),
      ),

    cleaning_expr: ($) =>
      seq(
        choice(
          "drop",
          "mean_impute",
          "median_impute",
          "knn_impute",
          "model_impute",
          "zscore",
          "iqr",
          "isolation_forest",
          "dbscan",
          "deduplication",
        ),
        optional($.call_args),
      ),

    transformation_expr: ($) =>
      seq(
        choice(
          "normalize",
          "standardize",
          "log_transform",
          "pca_reduction",
          "one_hot",
          "label_encode",
          "ordinal",
          "target_encode",
          "binary_encode",
          "frequency_encode",
          "word2vec",
          "tfidf",
          "sentence_transformer",
          "embedding",
        ),
        optional($.call_args),
      ),

    feature_engineering_expr: ($) =>
      seq(
        choice(
          "feature_selection",
          "feature_creation",
          "feature_interaction",
          "polynomial_features",
          "time_features",
          "lag_features",
        ),
        optional($.call_args),
      ),

    splitting_expr: ($) =>
      seq(
        choice(
          "train_test_split",
          "train_val_test_split",
          "kfold_cv",
          "stratified_split",
          "time_series_split",
          "group_split",
        ),
        optional($.call_args),
      ),

    // =========================================================
    // Section 4: Models
    // =========================================================

    model_stage: ($) =>
      seq(
        choice(
          // Supervised classification
          "logistic_regression",
          "decision_tree",
          "random_forest",
          "gradient_boosting",
          "svm",
          "knn",
          "naive_bayes",
          "neural_classifier",
          // Supervised regression
          "linear_regression",
          "ridge",
          "lasso",
          "elastic_net",
          "decision_tree_regressor",
          "random_forest_regressor",
          "gradient_boosting_regressor",
          "neural_regressor",
          // Unsupervised clustering
          "kmeans",
          "dbscan_cluster",
          "hierarchical",
          "gaussian_mixture",
          "spectral",
          // Dimensionality
          "pca",
          "tsne",
          "umap",
          "autoencoder",
          // Anomaly
          "isolation_forest_detector",
          "one_class_svm",
          "autoencoder_detector",
          // Probabilistic
          "bayesian_linear",
          "gaussian_process",
          "hidden_markov",
          "variational_inference",
          "mcmc_sampler",
          // Neural
          "mlp",
          "cnn",
          "rnn",
          "lstm",
          "transformer",
          "graph_neural_network",
          "diffusion_model",
          "variational_autoencoder",
          // Reinforcement
          "q_learning",
          "policy_gradient",
          "actor_critic",
          "mcts_agent",
          // ix-specific patterns
          "karnaugh_optimization",
          "memristive_markov",
          "grammar_weight_learning",
          "governance_health_scorer",
          "citation_power_law",
          "compounding_dimension",
        ),
        optional($.call_args),
      ),

    // =========================================================
    // Section 5: Evaluation
    // =========================================================

    evaluation_stage: ($) =>
      seq(
        choice(
          "accuracy",
          "precision",
          "recall",
          "f1_score",
          "auc_roc",
          "confusion_matrix",
          "log_loss",
          "mse",
          "rmse",
          "mae",
          "r_squared",
          "mape",
          "explained_variance",
          "silhouette_score",
          "calinski_harabasz",
          "davies_bouldin",
          "adjusted_rand_index",
          "normalized_mutual_info",
          "feature_importance",
          "shap_values",
          "partial_dependence",
          "lime_explanation",
          "attention_weights",
          "residual_analysis",
          "holdout",
          "cross_validation",
          "bootstrap",
          "time_series_validation",
          "nested_cv",
          "custom_metric",
          "evaluation",
        ),
        optional($.call_args),
      ),

    // =========================================================
    // Section 6: Deployment
    // =========================================================

    deployment_stage: ($) =>
      choice(
        $.serialization_expr,
        $.serving_expr,
        $.monitoring_expr,
        $.output_sink_expr,
      ),

    serialization_expr: ($) =>
      seq(
        choice("onnx", "pickle", "safetensors", "rust_native", "torchscript"),
        optional($.call_args),
      ),

    serving_expr: ($) =>
      seq(
        choice(
          "batch_inference",
          "real_time_api",
          "edge_deployment",
          "mcp_tool_integration",
          "embedded_in_pipeline",
        ),
        optional($.call_args),
      ),

    monitoring_expr: ($) =>
      seq(
        choice(
          "drift_detection",
          "performance_tracking",
          "data_quality_check",
          "alert_on_degradation",
          "automatic_retrain_trigger",
        ),
        optional($.call_args),
      ),

    // =========================================================
    // Section 7: Governance Integration
    // =========================================================

    governance_gate: ($) =>
      seq(
        choice(
          "data_provenance_check",
          "bias_assessment",
          "reversibility_check",
          "confidence_calibration",
          "explanation_requirement",
        ),
        optional($.call_args),
      ),

    governance_annotation: ($) =>
      seq("--governed", optional($.governance_level)),

    governance_level: ($) =>
      choice("minimal", "standard", "strict"),

    conclude_expr: ($) =>
      seq(
        "conclude",
        choice(
          "validated",
          "rejected",
          "inconclusive",
          "unstable",
          "overfitting_detected",
        ),
      ),

    // =========================================================
    // Section 8: ix-Specific Patterns & Combiners
    // =========================================================

    combiner: ($) =>
      seq(
        choice("voting", "averaging", "stacking", "blending", "boosting_cascade"),
        optional($.call_args),
      ),

    // =========================================================
    // Section 9: I/O & Reactive Patterns
    // =========================================================

    reactive_pipeline_statement: ($) =>
      seq(
        optional(seq($.identifier, "<-")),
        $.reactive_source_expr,
        "=>",
        choice($.pipeline_expr, $.flow_control_expr),
        optional(seq("=>", $.output_sink_expr)),
      ),

    reactive_source_expr: ($) => $.streaming_source_expr,

    output_sink_expr: ($) =>
      choice(
        seq("push", "(", $.string_literal, optional(seq(",", $.string_literal)), ")"),
        seq("write", "(", $.string_literal, ",", $.format_spec, ")"),
        seq("stdout", optional($.format_spec)),
        seq("post", "(", $.string_literal, ",", $.string_literal, ")"),
        seq("mcp_tool", "(", $.string_literal, ",", $.string_literal, ")"),
        seq("alert", "(", "discord", ",", $.string_literal, ")"),
        seq("github", "(", $.string_literal, ",", $.string_literal, ")"),
        seq("notify", "(", $.string_literal, ",", $.string_literal, ")"),
      ),

    flow_control_expr: ($) =>
      choice(
        $.fan_out_expr,
        $.fan_in_expr,
        $.filter_expr,
        $.throttle_expr,
        $.retry_expr,
        $.circuit_breaker_expr,
        $.window_expr,
        $.debounce_expr,
      ),

    fan_out_expr: ($) =>
      seq(
        "fan_out",
        "(",
        $.pipeline_expr,
        repeat1(seq(",", $.pipeline_expr)),
        ")",
      ),

    fan_in_expr: ($) =>
      seq(
        "fan_in",
        "(",
        $.data_source,
        repeat1(seq(",", $.data_source)),
        ")",
        "=>",
        $.pipeline_expr,
      ),

    filter_expr: ($) =>
      seq("filter", "(", $.predicate_expr, ")"),

    throttle_expr: ($) =>
      seq("throttle", "(", $.number_literal, ",", $.time_unit, ")"),

    retry_expr: ($) =>
      seq("retry", "(", $.number_literal, ",", $.backoff_strategy, ")"),

    circuit_breaker_expr: ($) =>
      seq("circuit_breaker", "(", $.number_literal, ",", $.string_literal, ")"),

    window_expr: ($) =>
      seq("window", "(", $.string_literal, ",", $.aggregation, ")"),

    debounce_expr: ($) =>
      seq("debounce", "(", $.string_literal, ")"),

    backoff_strategy: ($) =>
      choice("constant", "linear", "exponential"),

    aggregation: ($) =>
      choice("count", "sum", "avg", "min", "max", "collect"),

    time_unit: ($) =>
      choice("ms", "s", "m", "h"),

    // =========================================================
    // Section 10: MCP Orchestration
    // =========================================================

    mcp_pipeline_statement: ($) =>
      seq(
        $.mcp_step_expr,
        repeat(seq($.mcp_arrow, $.mcp_step_expr)),
        optional($.compound_phase),
      ),

    mcp_step_expr: ($) =>
      choice(
        $.tool_invocation,
        $.parallel_tools_expr,
        $.gated_tool_expr,
        $.binding_statement,
        $.conditional_step_expr,
      ),

    tool_invocation: ($) =>
      seq(
        $.namespace_path,
        ".",
        $.identifier,
        "(",
        optional($.arg_list),
        ")",
      ),

    namespace_path: ($) =>
      seq($.identifier, repeat(seq(".", $.identifier))),

    parallel_tools_expr: ($) =>
      seq(
        "parallel",
        "(",
        $.tool_invocation,
        repeat1(seq(",", $.tool_invocation)),
        ")",
      ),

    gated_tool_expr: ($) =>
      seq("when", $.mog_guard, ":", $.mcp_step_expr),

    // Spec: `binding_step ::= identifier "<-" mcp_step`. The earlier
    // `choice($.mcp_step_expr, $.pipeline_expr)` widened the RHS beyond the
    // spec and made a binding indistinguishable from a pipeline_statement's
    // optional `identifier <-` prefix. Narrowed to the spec form.
    binding_statement: ($) =>
      seq($.identifier, "<-", $.mcp_step_expr),

    conditional_step_expr: ($) =>
      seq(
        "if",
        $.mog_guard,
        $.mcp_step_expr,
        optional(seq("else", $.mcp_step_expr)),
      ),

    mog_guard: ($) =>
      choice(
        $.membership_test,
        $.semantic_predicate,
        $.guard_conjunction,
      ),

    membership_test: ($) =>
      seq(
        $.truth_value,
        optional(seq($.comparison_op, $.float_literal)),
      ),

    truth_value: ($) =>
      choice("T", "F", "U", "C"),

    guard_conjunction: ($) =>
      seq($.mog_guard, "&&", $.mog_guard),

    semantic_predicate: ($) =>
      seq("?", $.identifier, "(", optional($.arg_list), ")"),

    comparison_op: ($) =>
      choice(">=", "<=", ">", "<"),

    compound_phase: ($) =>
      seq(
        "compound",
        ":",
        repeat1($.compound_step),
      ),

    compound_step: ($) =>
      choice(
        seq("harvest", $.expression),
        seq("promote", $.expression, "if", $.mog_guard),
        seq("teach", $.expression, "to", $.identifier),
        seq("log", $.expression),
        seq("update_evolution_log", $.expression),
      ),

    // =========================================================
    // Section 12: Assertions
    // =========================================================

    assertion_statement: ($) =>
      seq(
        "assert",
        $.identifier,
        ":",
        $.assertion_pipeline,
      ),

    // Spec (sci-ml-pipelines.ebnf:453): `assertion_pipeline ::= assertion_subject
    // assertion_check+` — the checks are JUXTAPOSED, not arrow-joined. The earlier
    // `repeat(seq($.arrow, $.assertion_check))` required an arrow before each
    // check, which (a) could not parse the canonical arrow-less form used by every
    // example in the EBNF and in tests/behavioral/ixql-assertions-cases.md, and
    // (b) when an arrow was present, absorbed the "check" into the subject's own
    // pipeline_expr as a pipeline_stage, leaving this rule's check list dead. An
    // assertion subject that is itself an arrow pipeline still works: those arrows
    // belong to pipeline_expr, not to the check separator.
    assertion_pipeline: ($) =>
      seq(
        $.assertion_subject,
        repeat1($.assertion_check),
      ),

    // Spec lists data_source | pipeline_expr | ... | identifier as alternatives,
    // but they are mutually reducible: pipeline_expr -> simple_pipeline is a
    // data_source followed by an (optionally empty) arrow chain, and data_source
    // already covers a bare identifier. Keeping all three as direct choices made
    // every assertion subject ambiguous. pipeline_expr subsumes the others, so a
    // subject like `csv("train.csv")` or `random_forest -> f1_score` still parses;
    // it simply nests one level deeper. Since this grammar had never generated,
    // there was no prior CST for consumers to depend on -- this is the first
    // shape, not a breaking change to an existing one.
    assertion_subject: ($) =>
      $.pipeline_expr,

    assertion_check: ($) =>
      seq(
        "assert_check",
        "(",
        $.assertion_condition,
        optional(seq(",", "message", ":", $.string_literal)),
        ")",
      ),

    assertion_condition: ($) =>
      choice(
        seq("not_null"),
        seq("type", ":", $.string_literal),
        seq("range", ":", $.number_literal, "..", $.number_literal),
        seq("metric", $.identifier, $.comparison_op, $.float_literal),
        seq("truth", $.comparison_op, $.float_literal),
        seq("schema", ":", $.string_literal),
        $.mog_guard,
        $.identifier, // named predicate
      ),

    // =========================================================
    // Primitives & Shared Rules
    // =========================================================

    arg_list: ($) =>
      seq($.expression, repeat(seq(",", $.expression))),

    call_args: ($) =>
      seq("(", optional($.arg_list), ")"),

    expression: ($) =>
      choice(
        $.number_literal,
        $.float_literal,
        $.string_literal,
        $.boolean_literal,
        $.truth_value,
        $.tool_invocation,
        $.identifier,
      ),

    predicate_expr: ($) =>
      choice(
        $.mog_guard,
        $.identifier,
        seq($.identifier, $.comparison_op, $.expression),
      ),

    // Arrows — IxQL uses both → (U+2192) and -> (ASCII)
    arrow: ($) => choice("→", "->"),
    mcp_arrow: ($) => choice("→", "->"),

    identifier: ($) => /[a-zA-Z_][a-zA-Z0-9_]*/,

    number_literal: ($) => /[0-9]+/,

    float_literal: ($) => /[0-9]+\.[0-9]+/,

    string_literal: ($) =>
      seq('"', /[^"]*/, '"'),

    boolean_literal: ($) =>
      choice("true", "false"),

    // Comments: -- to end of line (IxQL convention from EBNF)
    comment: ($) =>
      token(seq("--", /.*/)),
  },
});
