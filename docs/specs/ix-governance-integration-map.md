# ix ↔ Demerzel/Seldon Integration Map

How Demerzel and Seldon leverage ix's 32+ ML/math crates for smarter governance.

## Demerzel — Governance Intelligence

| ix Crate | Demerzel Use Case | Input | Output |
|----------|-------------------|-------|--------|
| **ix-graph** | Artifact dependency analysis | Governance artifact cross-references | Dependency graph, critical path, cycle detection, orphan identification |
| **ix-graph** | Belief propagation | Beliefs + evidence chains | Which beliefs are upstream/downstream, cascade impact of a belief change |
| **ix-search** | Optimal remediation planning | Gap space + available actions | Best remediation sequence (A* through action space) |
| **ix-search** | MCTS for policy exploration | Policy alternatives + outcome estimates | Most promising policy modifications to try |
| **ix-game** | Multi-agent governance equilibria | Persona capabilities + constraints | Nash equilibria between competing governance concerns |
| **ix-game** | Stakeholder impact analysis | Affected parties + preferences | Shapley values — fair attribution of governance burden |
| **ix-supervised** | Gap auto-remediation classifier | Historical gap data + outcomes | Predict: auto-fix vs. escalate for new gaps |
| **ix-supervised** | Compliance risk scoring | Repo metrics + violation history | Risk score per repo, prioritize recon targets |
| **ix-unsupervised** | Violation pattern clustering | Historical compliance reports | Systemic patterns vs. one-off incidents |
| **ix-unsupervised** | Governance artifact similarity | Policy/persona text embeddings | Detect redundant or overlapping artifacts |
| **ix-ensemble** | Confidence calibration | Historical beliefs + outcomes | Calibrated confidence thresholds per domain |
| **ix-probabilistic** | Governance state prediction | Belief state sequences | HMM/Viterbi: predict next governance state transitions |
| **ix-probabilistic** | Stale belief forecasting | Update timestamps + topic volatility | Probability distribution of when beliefs go stale |
| **ix-signal** | Compliance trend analysis | Compliance rates over time | FFT: detect periodic patterns, anomalies in governance health |
| **ix-signal** | Evolution log time series | Citation/violation counts over time | Trend detection, seasonal governance patterns |
| **ix-chaos** | Governance stability analysis | Evolution metrics over time | Lyapunov exponents: is governance trending toward chaos or stability? |
| **ix-chaos** | Bifurcation detection | Policy threshold sensitivity | Find threshold values where small changes cause large governance shifts |
| **ix-optimize** | Budget optimization | Experiment costs + outcomes | Optimal budget allocation across experiments (Pareto frontier) |
| **ix-optimize** | Remediation strategy tuning | Auto-remediation parameters + success rates | Optimal confidence thresholds, risk classifications |
| **ix-nn** | Governance anomaly detection | All state data streams | Neural anomaly detector: flag unusual governance state changes |
| **ix-adversarial** | Governance robustness testing | Constitutional rules + attack scenarios | Adversarial probes: find governance rules that can be gamed |
| **ix-evolution** | Policy evolution search | Current policies + fitness function | Evolutionary search for improved policy configurations |
| **ix-pipeline** | Governance analytics pipeline | All of the above | DAG orchestration of governance ML workflows |

## Seldon — Teaching Intelligence

| ix Crate | Seldon Use Case | Input | Output |
|----------|-----------------|-------|--------|
| **ix-graph** | Knowledge dependency mapping | Curriculum topics + prerequisites | Optimal learning path through knowledge graph |
| **ix-graph** | Learner knowledge state visualization | Belief states per topic | Knowledge map showing mastered/unknown/confused areas |
| **ix-supervised** | Comprehension prediction | Learner responses + belief states | Predict: will this learner understand the next concept? |
| **ix-supervised** | Teaching style selection | Learner profile + topic | Classify: narrative vs. structured vs. socratic for this learner+topic |
| **ix-nn** | Adaptive teaching model | Teaching interactions + outcomes | Neural model that improves teaching effectiveness over time |
| **ix-grammar** | Structured knowledge packages | Governance rules + formal grammar | Parse and validate knowledge package structure |
| **ix-grammar** | Assessment question generation | Topic + difficulty level | Generate assessment questions from formal grammar of the domain |
| **ix-search** | Curriculum optimization | Topics + dependencies + time constraints | Optimal teaching sequence (shortest path to competence) |
| **ix-search** | Knowledge gap identification | Current belief states + target states | A* search for most efficient gap-closing sequence |
| **ix-rl** | Adaptive difficulty | Learner performance history | Reinforcement learning: tune difficulty to maximize learning rate |
| **ix-signal** | Learning velocity tracking | Assessment scores over time | Trend analysis: is the learner accelerating, plateauing, or regressing? |
| **ix-probabilistic** | Belief state inference | Partial observations of learner knowledge | Bayesian inference: estimate full knowledge state from limited observations |
| **ix-game** | Multi-learner resource allocation | Multiple learners + teaching capacity | Fair allocation of Seldon's attention across learners |

## Implementation Priority

### Phase 1 — Quick Wins (use existing ix crates as-is)
1. **ix-graph** for artifact dependency analysis — Demerzel already has cross-reference data
2. **ix-signal** for compliance trend analysis — evolution logs are time series
3. **ix-supervised** for gap classification — historical PDCA data as training set
4. **ix-search** for curriculum optimization — Seldon already designs learning paths

### Phase 2 — ML Feedback Loop (the 5 governance pipelines)
5. **ix-ensemble** for confidence calibration
6. **ix-probabilistic** for staleness prediction
7. **ix-unsupervised** for violation pattern detection
8. **ix-supervised** for remediation optimization
9. **ix-nn** for anomaly detection

### Phase 3 — Advanced Intelligence
10. **ix-game** for multi-agent governance equilibria
11. **ix-chaos** for stability analysis
12. **ix-adversarial** for robustness testing
13. **ix-evolution** for policy search
14. **ix-rl** for adaptive teaching

## Architecture

```
Demerzel state/          ix ML Pipelines           Seldon teaching
    │                         │                         │
    ├─ beliefs/*.json ──────→ ix-supervised ──────→ calibrated thresholds
    ├─ evolution/*.json ────→ ix-signal ─────────→ trend alerts
    ├─ pdca/*.json ─────────→ ix-ensemble ───────→ strategy optimization
    ├─ oversight/*.json ────→ ix-unsupervised ───→ pattern reports
    │                         │
    │                    ix-pipeline (DAG)
    │                         │
    └─────────────────────────┘ (feedback loop)
```

## Galactic Protocol Messages

All ix → Demerzel ML feedback uses `ml-feedback-recommendation.schema.json`.
All Demerzel → ix data exports use `knowledge-package.schema.json`.
Seldon → ix teaching data uses `learning-outcome.schema.json`.

## Cost Awareness

Each pipeline has a compute budget. Demerzel tracks costs per the experimentation policy:
- Phase 1 pipelines: negligible (CPU-only, small data)
- Phase 2 pipelines: low ($1-5/month, batch processing)
- Phase 3 pipelines: medium ($5-20/month, continuous analysis)
