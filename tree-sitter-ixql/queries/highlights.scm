; IxQL — tree-sitter syntax highlighting queries
; Consumed by: Neovim (nvim-treesitter), VS Code (tree-sitter-vscode), Helix
; Scope names follow the tree-sitter standard for cross-editor compatibility.

; =========================================================
; Keywords — flow control and special forms
; =========================================================

[
  "when"
  "if"
  "else"
  "compound"
  "parallel"
  "fan_out"
  "fan_in"
  "filter"
  "throttle"
  "retry"
  "circuit_breaker"
  "window"
  "debounce"
  "assert"
  "assert_check"
  "--governed"
] @keyword

; Compound phase sub-keywords
[
  "harvest"
  "promote"
  "teach"
  "to"
  "log"
  "update_evolution_log"
] @keyword.operator

; Assertion condition keywords
[
  "not_null"
  "type"
  "range"
  "metric"
  "truth"
  "schema"
  "message"
] @keyword.operator

; Conclude / governance conclusion
[
  "conclude"
  "validated"
  "rejected"
  "inconclusive"
  "unstable"
  "overfitting_detected"
] @keyword.coroutine

; =========================================================
; Tetravalent truth values — distinct highlight
; =========================================================

(truth_value) @constant.builtin

; =========================================================
; Data sources — @function.builtin
; =========================================================

[
  "csv"
  "json"
  "parquet"
  "database"
  "api"
  "websocket"
  "watch"
  "sse"
  "webhook"
  "cron"
  "stdin"
  "subscribe"
  "cdc"
  "grpc"
  "governance_state"
  "git_history"
  "mcp_tool_output"
] @function.builtin

; =========================================================
; Preprocessing stages
; =========================================================

[
  "drop"
  "mean_impute"
  "median_impute"
  "knn_impute"
  "model_impute"
  "zscore"
  "iqr"
  "deduplication"
  "normalize"
  "standardize"
  "log_transform"
  "pca_reduction"
  "one_hot"
  "label_encode"
  "ordinal"
  "target_encode"
  "binary_encode"
  "frequency_encode"
  "word2vec"
  "tfidf"
  "sentence_transformer"
  "embedding"
  "feature_selection"
  "feature_creation"
  "feature_interaction"
  "polynomial_features"
  "time_features"
  "lag_features"
  "train_test_split"
  "train_val_test_split"
  "kfold_cv"
  "stratified_split"
  "time_series_split"
  "group_split"
] @function

; =========================================================
; Model stages — @type (distinct from preprocessing)
; =========================================================

[
  "logistic_regression"
  "decision_tree"
  "random_forest"
  "gradient_boosting"
  "svm"
  "knn"
  "naive_bayes"
  "neural_classifier"
  "linear_regression"
  "ridge"
  "lasso"
  "elastic_net"
  "decision_tree_regressor"
  "random_forest_regressor"
  "gradient_boosting_regressor"
  "neural_regressor"
  "kmeans"
  "dbscan_cluster"
  "hierarchical"
  "gaussian_mixture"
  "spectral"
  "pca"
  "tsne"
  "umap"
  "autoencoder"
  "isolation_forest_detector"
  "one_class_svm"
  "autoencoder_detector"
  "bayesian_linear"
  "gaussian_process"
  "hidden_markov"
  "variational_inference"
  "mcmc_sampler"
  "mlp"
  "cnn"
  "rnn"
  "lstm"
  "transformer"
  "graph_neural_network"
  "diffusion_model"
  "variational_autoencoder"
  "q_learning"
  "policy_gradient"
  "actor_critic"
  "mcts_agent"
] @type

; =========================================================
; ix-Specific patterns — @type.builtin (distinguished)
; =========================================================

[
  "karnaugh_optimization"
  "memristive_markov"
  "grammar_weight_learning"
  "governance_health_scorer"
  "citation_power_law"
  "compounding_dimension"
] @type.builtin

; =========================================================
; Evaluation stages
; =========================================================

[
  "accuracy"
  "precision"
  "recall"
  "f1_score"
  "auc_roc"
  "confusion_matrix"
  "log_loss"
  "mse"
  "rmse"
  "mae"
  "r_squared"
  "mape"
  "explained_variance"
  "silhouette_score"
  "calinski_harabasz"
  "davies_bouldin"
  "adjusted_rand_index"
  "normalized_mutual_info"
  "feature_importance"
  "shap_values"
  "partial_dependence"
  "lime_explanation"
  "attention_weights"
  "residual_analysis"
  "holdout"
  "cross_validation"
  "bootstrap"
  "time_series_validation"
  "nested_cv"
  "custom_metric"
  "evaluation"
] @function.method

; =========================================================
; Governance gates — @attribute (special visual weight)
; =========================================================

[
  "data_provenance_check"
  "bias_assessment"
  "reversibility_check"
  "confidence_calibration"
  "explanation_requirement"
] @attribute

; Governance level
[
  "minimal"
  "standard"
  "strict"
] @constant

; =========================================================
; Deployment & serving
; =========================================================

[
  "onnx"
  "pickle"
  "safetensors"
  "rust_native"
  "torchscript"
  "batch_inference"
  "real_time_api"
  "edge_deployment"
  "mcp_tool_integration"
  "embedded_in_pipeline"
  "drift_detection"
  "performance_tracking"
  "data_quality_check"
  "alert_on_degradation"
  "automatic_retrain_trigger"
] @function.builtin

; =========================================================
; Output sinks
; =========================================================

[
  "push"
  "write"
  "stdout"
  "post"
  "mcp_tool"
  "alert"
  "github"
  "notify"
  "mcp_register"
  "mcp_invoke"
] @function.builtin

; Sink target providers
[
  "discord"
  "gitlab"
  "generic"
] @constant

; =========================================================
; Ensemble combiners
; =========================================================

[
  "voting"
  "averaging"
  "stacking"
  "blending"
  "boosting_cascade"
] @constant.builtin

; =========================================================
; Backoff / aggregation constants
; =========================================================

[
  "constant"
  "linear"
  "exponential"
] @constant

[
  "count"
  "sum"
  "avg"
  "min"
  "max"
  "collect"
] @constant

; =========================================================
; Format specifiers
; =========================================================

[
  "text"
  "binary"
] @string.special

; =========================================================
; MCP namespaces (tars., ix., context7.)
; =========================================================

(namespace_path) @namespace

; Tool invocations — method name highlighted as a function
(tool_invocation
  "." @punctuation.delimiter
  (identifier) @function.method)

; =========================================================
; Operators
; =========================================================

[
  "→"
  "->"
  "=>"
  "<-"
  "+"
  ":"
] @operator

(comparison_op) @operator

(guard_conjunction "&&" @operator)

; =========================================================
; Binding names (lhs of <-)
; =========================================================

(binding_statement
  (identifier) @variable)

; Assertion name
(assertion_statement
  (identifier) @label)

; =========================================================
; Literals
; =========================================================

(string_literal) @string

(number_literal) @number

(float_literal) @number.float

(boolean_literal) @boolean

; =========================================================
; Comments
; =========================================================

(comment) @comment

; =========================================================
; Punctuation
; =========================================================

[
  "("
  ")"
  ","
  ".."
] @punctuation.delimiter
