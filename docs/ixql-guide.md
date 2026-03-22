# IxQL — ML Pipeline & Reactive Data Flow Language

IxQL is a declarative language for composing ML pipelines, MCP orchestrations, and reactive data flows. Defined as an [EBNF grammar](../grammars/sci-ml-pipelines.ebnf) and executed by the [ix](https://github.com/GuitarAlchemist/ix) forge.

## Quick Start

```ixql
-- Simple classification pipeline
csv → normalize → random_forest → f1_score
```

Every IxQL pipeline is a governed artifact — constitutional gates can be inserted at any stage, and conclusions map to tetravalent logic (T/F/U/C).

## Grammar Structure (11 Sections)

| Section | What It Covers |
|---------|---------------|
| 1. Pipeline Architecture | Composition, ensembles |
| 2. Data Sources | CSV, JSON, Parquet, API, streaming, governance state, git history, MCP |
| 3. Preprocessing | Cleaning, transformation, feature engineering, splitting |
| 4. Models | Supervised, unsupervised, probabilistic, neural, reinforcement |
| 5. Evaluation | Metrics, validation strategies, interpretation (SHAP, LIME) |
| 6. Deployment | Serialization, serving, monitoring, drift detection |
| 7. Governance Integration | Bias assessment, reversibility, confidence calibration, explanation |
| 8. ix-Specific Patterns | Karnaugh, memristive Markov, grammar weights, compounding |
| 9. I/O & Reactive Patterns | WebSocket, file watcher, SSE, webhook, cron, message queues, flow control |
| 10. MCP Orchestration | Tool invocation, parallel tools, tetravalent gates, bindings, compound phases |
| 11. Evolution Hooks | Research cycles, distillation, external grammar consumption |

## Use Cases

### 1. Research Pipeline

Investigate a hypothesis, evaluate, and produce a course:

```ixql
-- Guitar studies: Is CAGED geometry learnable in 3 sessions?
department_state("guitar-studies")
  → question_generation("caged-learnability")
  → cross_model_validation(
       claude.research(question),
       gpt4o.research(question)
     )
  → evaluation(agreement_score, evidence_density)
  → when T >= 0.8: course_production("GTR-003", languages: ["en", "es", "fr"])
  → compound:
      harvest findings
      promote if T >= 0.9
      teach to seldon
```

### 2. Governed Ensemble

Combine models with constitutional gates between stages:

```ixql
-- Governance health scoring with bias checks
(governance_state → cleaning(missing: drop) → gradient_boosting → f1_score)
  + (governance_state → embedding("governance") → transformer → auc_roc)
  => stacking
  → bias_assessment          -- Article 10: Stakeholder Pluralism
  → confidence_calibration   -- Are probabilities well-calibrated?
  → explanation_requirement  -- Article 2: Transparency
  → when T >= 0.7: mcp_tool_integration("governance-health-scorer")
```

### 3. Reactive Governance

Real-time monitoring with automatic response:

```ixql
-- Watch beliefs for drift, alert if confidence drops
watch("state/beliefs/*.json")
  → debounce(5s)
  → governance_state
  → drift_detection
  → filter(drift_score > 0.3)
  → alert(discord, "Belief drift detected: {{belief.name}} confidence dropped to {{belief.confidence}}")

-- GitHub push triggers 3 parallel governance checks
webhook(github, "push")
  → fan_out(
      recon_pipeline,        -- Tier 1-3 reconnaissance
      staleness_check,       -- Per-category freshness
      readme_sync            -- Artifact count verification
    )
  → when any_failed: alert(discord, "Governance check failed: {{failed_checks}}")

-- Cron: daily research cycle at 6am
cron("0 6 * * *")
  → department_state(next_department)
  → question_generation
  → cross_model_validation
  → when T >= 0.8: course_production
  → compound: harvest, promote if T >= 0.9
```

### 4. MCP Orchestration (formerly MOG)

Chain MCP tool calls with tetravalent gates:

```ixql
-- Multi-repo analysis: resolve docs, analyze, train
result <- context7.resolve("react")
  → when T >= 0.8: analysis <- tars.analyze(result)
  → when T >= 0.7: features <- ix.ml.extract_features(analysis)
  → ix.ml.train(features, model: "gradient_boosting")
  → evaluation(f1_score, shap_values)
  → when T >= 0.9: mcp_register("react-analyzer", "Analyzes React codebases")

-- Parallel tool fanout with merge
parallel(
  tars.grammar.parse(input),
  ix.ml.classify(input),
  context7.query("react", input)
) → merge_results
  → when T >= 0.7: output
```

### 5. Streaming ML Pipeline

Process real-time data with windowed aggregation:

```ixql
-- Discord sentiment analysis with sliding window
websocket(discord, channel: "governance")
  → text
  → sentiment_model
  → window(1h, avg)
  → filter(avg_sentiment < 0.3)
  → alert(discord, "Negative governance sentiment trend detected")
  → compound: log sentiment_trend

-- Live model retraining on data arrival
watch("data/incoming/*.csv")
  → debounce(30s)
  → csv → cleaning → feature_engineering
  → train_test_split(0.8)
  → gradient_boosting(n_estimators: 200)
  → evaluation(f1_score, drift_detection)
  → when f1 >= 0.85: model_serialization(onnx)
  → when f1 < previous_f1: alert(discord, "Model degradation: {{f1}} < {{previous_f1}}")
```

### 6. ix Pattern: Memristive Markov Chain

Custom ix Rust pattern with governance:

```ixql
-- Conductance-weighted state transitions
streaming_source("sensor_data")
  → lag_features(window: 10)
  → memristive_markov(
      states: ["healthy", "degrading", "failed"],
      conductance_decay: 0.95,
      learning_rate: 0.01
    )
  → time_series_validation(walk_forward, horizon: 24h)
  → when T >= 0.8: mcp_tool_integration("health-predictor")
  → monitoring(drift_detection, alert_on_degradation)
```

### 7. Driver Cycle as IxQL

The 8-phase governance driver expressed as a pipeline:

```ixql
-- Demerzel Driver: WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP
cron("0 6 * * *")
  → wake(load_state, check_pending)
  → recon(
      tier1: schema_validation + test_coverage,
      tier2: repo_state + ci_status + submodules,
      tier3: assumptions + confidence_gaps + completeness_instinct
    )
  → plan(prioritize_by_weakness, select_tasks)
  → fan_out(tasks.map(t => execute(t)))
  → verify(tests_pass, governance_audit)
  → compound:
      harvest learnings
      promote if T >= 0.9
      teach to seldon
      update evolution_log
  → persist(state, beliefs, conscience)
  → sleep(schedule_next: "tomorrow 6am")
```

### 8. Fractal Compounding Pipeline

Self-similar compound operations at every scale:

```ixql
-- Level 0: Single step compounds its learning
step → harvest_learning → when worthy: promote

-- Level 1: Pipeline compounds step learnings
pipeline(step1, step2, step3)
  → compound: harvest(step_learnings), promote_if_worthy, teach

-- Level 2: Cycle compounds pipeline learnings
driver_cycle(pipeline1, pipeline2)
  → compound: harvest(pipeline_learnings), update_evolution_log

-- Level 3: Session compounds cycle learnings
session(cycle1, cycle2, cycle3)
  → compound: harvest(cycle_learnings), update_beliefs

-- Level 4: Evolution compounds session learnings
evolution_log → compound: harvest(session_learnings), compute_Dc, alert_if(Dc < 1.0)
```

## Tetravalent Pipeline Conclusions

Every IxQL pipeline maps its outcome to tetravalent logic:

| Outcome | Logic | Action |
|---------|-------|--------|
| Metrics meet threshold | **T** (validated) | Deploy / promote |
| Metrics fail threshold | **F** (rejected) | Reject / investigate |
| Inconclusive results | **U** (unknown) | Gather more data |
| Contradictory results | **C** (unstable) | Escalate to human |

## Governance Gates

Insert at any pipeline stage:

```ixql
pipeline
  → bias_assessment             -- Article 10: Stakeholder Pluralism
  → reversibility_check         -- Article 3: Can we roll back?
  → confidence_calibration      -- Are confidence levels honest?
  → explanation_requirement     -- Article 2: Can we explain?
  → data_provenance_check       -- Where did training data come from?
```

## Flow Control Patterns

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Fan-out | `fan_out(p1, p2, p3)` | Parallel execution |
| Fan-in | `fan_in(s1, s2) => pipeline` | Merge multiple sources |
| Filter | `filter(predicate)` | Conditional routing |
| Throttle | `throttle(100, per_second)` | Rate limiting |
| Retry | `retry(3, exponential)` | Fault tolerance |
| Circuit breaker | `circuit_breaker(5, reset: 30s)` | Stop cascading failures |
| Window | `window(1h, avg)` | Streaming aggregation |
| Debounce | `debounce(5s)` | Wait for changes to settle |

## References

- [Full EBNF grammar](../grammars/sci-ml-pipelines.ebnf) — 11 sections, ~300 productions
- [ix repo](https://github.com/GuitarAlchemist/ix) — Rust ML forge (runtime)
- [ix CLI issue](https://github.com/GuitarAlchemist/Demerzel/issues/103) — Parser + executor
- [LSP issue](https://github.com/GuitarAlchemist/Demerzel/issues/117) — VS Code support
- [Demerzel speaks IxQL](https://github.com/GuitarAlchemist/Demerzel/issues/104) — Governance as pipelines
