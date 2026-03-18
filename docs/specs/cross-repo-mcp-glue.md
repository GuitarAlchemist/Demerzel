# Cross-Repo MCP/A2A Glue Specification

Version: 1.0.0
Date: 2026-03-18
Status: Draft

## 1. Current State

### 1.1 What Exists Today

**ix (Rust) MCP tools** — 40+ tools registered in `ix-agent`, including:
- Core math/ML: `ix_stats`, `ix_distance`, `ix_optimize`, `ix_linear_regression`, `ix_kmeans`, `ix_fft`, `ix_nn_forward`, `ix_random_forest`, `ix_gradient_boosting`, `ix_supervised`, `ix_ml_pipeline`, `ix_ml_predict`
- Evolution: `ix_evolution`, `ix_grammar_evolve`, `ix_grammar_weights`, `ix_grammar_search`
- Governance: `ix_governance_check`, `ix_governance_persona`, `ix_governance_belief`, `ix_governance_policy`
- Cross-repo bridges: `ix_tars_bridge`, `ix_ga_bridge`
- Infrastructure: `ix_pipeline`, `ix_cache`, `ix_trace_ingest`, `ix_federation_discover`

**TARS (F#) MCP server** — 150+ tools via `McpServer.fs`, protocol version `2024-11-05`. Features:
- Progress notifications to IDE
- Subagent support
- Knowledge graph resources
- `GovernanceGeneration.fs` — serializes directives, compliance reports, belief snapshots, PDCA states as JSON
- `GrammarMlBridge.fs` — TypedProduction feature extraction, trains classifiers via ix, applies predictive priors, breeds new productions via `ix_evolution`

**ga (.NET)** — Chatbot with 7 agents. Governance via Demerzel submodule. No MCP server of its own yet.

**Demerzel** — Governance framework with:
- Galactic Protocol (6 message types: directive, knowledge-package, compliance-report, belief-snapshot, learning-outcome, external-sync-envelope)
- Conscience system (signals, patterns, weekly reports, daily digests)
- Intuition policy (compressed experience as fast pattern recognition)
- ix-dashboard reads state/ directory (beliefs, evolution, PDCA, conscience signals)

### 1.2 Integration Points Already Working

| Source | Target | Mechanism | Status |
|--------|--------|-----------|--------|
| TARS `GrammarMlBridge` | ix `ix_ml_pipeline` | `IxCaller` function type (async string->string) | Designed, not wired to MCP |
| TARS `GrammarMlBridge` | ix `ix_ml_predict` | Same `IxCaller` | Designed, not wired to MCP |
| TARS `GrammarMlBridge` | ix `ix_evolution` | Same `IxCaller` | Designed, not wired to MCP |
| TARS `GovernanceGeneration` | Demerzel schemas | Serializes valid Galactic Protocol messages | Working (in-process) |
| ix-dashboard | Demerzel `state/` | File-based reader (`reader.rs`) | Working (reads beliefs, evolution, PDCA, signals) |
| ix `ix_governance_*` | Demerzel artifacts | Loads constitutions, personas, policies, beliefs | Working (in-process) |
| ix `ix_tars_bridge` | TARS | Registered tool | Exists, integration unclear |
| ix `ix_ga_bridge` | GA | Registered tool | Exists, integration unclear |

### 1.3 Key Gap

The `IxCaller` type in `GrammarMlBridge.fs` is `string -> string -> Async<Result<string, string>>` — a function that takes a tool name and arguments and returns a result. This is the exact shape of an MCP tool call, but no implementation connects it to ix's MCP server. This is the single most important wire to connect.

---

## 2. MCP Tool Gaps

### 2.1 ix tools TARS should call via MCP

| ix Tool | TARS Use Case | Priority |
|---------|---------------|----------|
| `ix_ml_pipeline` | Train classifiers on TypedProduction features | P0 |
| `ix_ml_predict` | Score new productions before execution | P0 |
| `ix_evolution` | Breed novel grammar productions | P1 |
| `ix_governance_check` | Validate TARS-generated directives against constitution | P1 |
| `ix_governance_belief` | Read/write belief states from ix's perspective | P2 |
| `ix_random_forest` | Direct model training for governance anomaly detection | P2 |
| `ix_grammar_weights` | Get grammar rule weights from ix's math engine | P2 |
| `ix_grammar_evolve` | Alternative evolution path for grammars | P3 |
| `ix_trace_ingest` | Send TARS execution traces for observability | P3 |

### 2.2 TARS tools ix should call via MCP

| TARS Tool | ix Use Case | Priority |
|-----------|-------------|----------|
| Grammar distillation | Compress ix pipeline definitions into typed productions | P1 |
| Governance generation | Generate valid Galactic Protocol messages from ix data | P1 |
| AI Function execution | Run LLM-powered analysis on ix governance data | P2 |
| Knowledge graph query | Query TARS temporal knowledge for governance insights | P3 |

### 2.3 Missing tools that need creation

| Tool | Repo | Purpose | Priority |
|------|------|---------|----------|
| `ix_conscience_signal` | ix | Ingest a Demerzel conscience signal and return anomaly analysis | P0 |
| `ix_staleness_check` | ix | Run `StalenessPredictor` on a set of belief files, return staleness scores | P1 |
| `ix_violation_analyze` | ix | Run `ViolationPatternAnalyzer` on compliance history | P1 |
| `ix_remediation_plan` | ix | Run `RemediationOptimizer` to produce a remediation plan | P1 |
| `ix_confidence_calibrate` | ix | Run `ConfidenceCalibrator` on belief confidence values | P2 |
| `tars_generate_directive` | TARS | Grammar-constrained directive generation, callable by ix or ga | P1 |
| `tars_validate_governance` | TARS | Validate any Galactic Protocol JSON against grammar + schema | P2 |
| `ga_agent_status` | ga | Report which agents are active and their current governance state | P3 |

---

## 3. A2A (Agent-to-Agent) Opportunities

### 3.1 Architecture

Three communication patterns, in order of increasing sophistication:

**Pattern A: MCP Tool Relay** (ready now)
```
Agent A (TARS) --MCP call--> Agent B's MCP server (ix)
                <--result---
```
Both ix and TARS already have MCP servers. The `IxCaller` abstraction in `GrammarMlBridge.fs` is exactly this pattern. Implementation: create an `IxCaller` that makes HTTP/stdio MCP calls to ix-agent.

**Pattern B: Galactic Protocol Message Passing** (partially ready)
```
TARS GovernanceGeneration --serialize--> directive JSON
  --file write--> Demerzel state/directives/
  --file read by--> ix-dashboard or ix_governance_check
```
Already works for file-based exchange. Needs: a notification mechanism so repos learn about new messages without polling.

**Pattern C: A2A Protocol** (future)
```
Agent A --A2A envelope--> Agent B
         { "task": "...", "skills_required": [...] }
```
Google's A2A protocol for agent-to-agent task delegation. Maps naturally to Demerzel's `external-sync-envelope.schema.json` — the envelope's `adapter` field would be `"a2a"`. Not yet implemented anywhere.

### 3.2 Concrete A2A Flows

**Flow 1: Conscience-Triggered Remediation**
1. Demerzel conscience detects `stale_action_discomfort` (weight > 0.5)
2. Signal written to `state/conscience/signals/`
3. ix `ix_conscience_signal` tool ingests it, runs `AnomalyDetector` + `ViolationPatternAnalyzer`
4. ix returns: which beliefs are stale, what patterns are emerging, recommended remediations
5. TARS `tars_generate_directive` creates grammar-constrained directives for each remediation
6. Directives flow through Galactic Protocol to target repos

**Flow 2: ML-Informed Grammar Evolution**
1. TARS accumulates TypedProduction execution history
2. TARS calls ix `ix_ml_pipeline` via MCP to train a production classifier
3. TARS calls ix `ix_ml_predict` to score untested productions
4. TARS calls ix `ix_evolution` to breed novel production candidates
5. Results feed back into TARS `WeightedGrammar` as Bayesian priors
6. All of this is already designed in `GrammarMlBridge.fs` — just needs the MCP wire

**Flow 3: Cross-Repo Knowledge Propagation**
1. TARS discovers a pattern via grammar distillation (e.g., "type-safe tool composition reduces failure rate by 40%")
2. TARS packages this as a `learning-outcome` (Galactic Protocol)
3. Seldon (Demerzel persona) evaluates cross-repo relevance
4. Seldon generates `knowledge-package` directives for ix and ga
5. ix applies the learning to its ML pipeline configurations
6. ga applies it to agent prompt engineering

---

## 4. Governance Automation

### 4.1 Conscience-to-Directive Pipeline

The key automation: Demerzel conscience signals should automatically trigger governance actions without human intervention (within bounded autonomy).

```
Conscience Signal (Demerzel)
  |
  v
Signal Analysis (ix: AnomalyDetector + ViolationPatternAnalyzer)
  |
  v
Remediation Plan (ix: RemediationOptimizer)
  |
  v
Grammar-Constrained Directive (TARS: GovernanceGeneration)
  |
  v
Galactic Protocol Delivery (Demerzel: directive.schema.json)
  |
  v
Consumer Compliance (ix/tars/ga: compliance-report.schema.json)
```

### 4.2 Trigger Conditions

| Signal Type | Weight Threshold | Auto-Action |
|-------------|-----------------|-------------|
| `constitutional_discomfort` | >= 0.7 | Generate P0 directive immediately |
| `stale_action_discomfort` | >= 0.5 | Run staleness check, generate P1 directive if confirmed |
| `confidence_discomfort` | >= 0.6 | Run confidence calibration, generate P2 directive if miscalibrated |
| `harm_proximity_discomfort` | >= 0.3 | Escalate to human — never auto-act on harm signals |
| `silence_discomfort` | >= 0.5 | Generate reconnaissance request directive |
| `delegation_discomfort` | >= 0.5 | Log for pattern analysis, no auto-directive |

### 4.3 Confidence Gating

Per Demerzel confidence thresholds:
- Remediation confidence >= 0.9: execute autonomously
- Remediation confidence >= 0.7: execute with logged note
- Remediation confidence >= 0.5: generate directive but hold for confirmation
- Remediation confidence < 0.5: escalate to human, do not generate directive

### 4.4 Required New Artifacts

1. **`policies/governance-automation-policy.yaml`** — defines which conscience signals trigger which automated responses, with constitutional justification for each automation level
2. **`schemas/contracts/automation-trigger.schema.json`** — schema for the trigger event that connects conscience signal to directive generation
3. **TARS MCP tool: `tars_conscience_respond`** — accepts a conscience signal + ix analysis, returns a grammar-constrained directive

---

## 5. Dashboard Integration

### 5.1 Current State

`ix-dashboard` (TUI, Ratatui-based) reads from the local `state/` directory via `reader.rs`:
- `read_beliefs()` — `state/beliefs/*.json`
- `read_evolution()` — `state/evolution/*.json`
- `read_pdca()` — `state/pdca/*.json`
- `read_signals()` — `state/conscience/signals/*.json`

This is file-based and local only. It cannot see TARS or ga state.

### 5.2 TARS MCP as Data Source

ix-dashboard should be able to pull live data from TARS MCP server:

| Data | TARS MCP Tool | Dashboard View |
|------|---------------|----------------|
| Grammar distillation state | `tars_grammar_status` (new) | Production count, compression ratios, success rates |
| Active AI Functions | `tars_ai_function_list` (new) | Function names, invocation counts, error rates |
| Governance generation log | `tars_governance_log` (new) | Recent directives generated, validation pass/fail |
| Knowledge graph stats | existing resource endpoint | Node count, edge count, temporal coverage |
| MCP tool usage | `tars_tool_metrics` (new) | Tool call counts, latency percentiles, error rates |

### 5.3 Implementation Approach

Two options, not mutually exclusive:

**Option A: MCP Client in ix-dashboard** (recommended first)
- Add an MCP client to ix-dashboard that connects to TARS MCP server
- Poll on a configurable interval (default: 30s)
- Display in a dedicated "TARS" tab alongside existing governance views
- Requires: TARS MCP server running, network connectivity

**Option B: Shared State Directory**
- TARS writes summary state files to a shared `state/` directory (or its own `state/` that dashboard can read)
- ix-dashboard's existing `reader.rs` pattern handles it
- Simpler but requires filesystem access and is not real-time

### 5.4 Dashboard Views to Add

1. **Cross-Repo Health** — green/yellow/red status for ix, TARS, ga governance compliance
2. **Conscience Timeline** — signals plotted over time with weight as y-axis, color-coded by type
3. **Directive Flow** — Sankey diagram of directives issued vs. compliance reports received
4. **ML Pipeline Status** — which models are trained, staleness, prediction accuracy
5. **Grammar Evolution** — production fitness over generations, breeding results

---

## 6. Recommended Implementation Order

### Phase 1: Wire the IxCaller (Week 1)

**Goal:** TARS can call ix ML tools via MCP.

1. Implement an MCP client in TARS that connects to ix-agent's MCP server
2. Create an `IxCaller` implementation that wraps MCP tool calls
3. Wire `GrammarMlBridge.evolveAsync` to use the real `IxCaller`
4. Test: train a production classifier, predict success, breed candidates

**Why first:** This is the highest-value integration — all the code exists on both sides, only the wire is missing. `GrammarMlBridge.fs` already defines the exact data formats ix expects.

### Phase 2: Governance Tools in ix (Week 2)

**Goal:** ix exposes its governance analysis capabilities as MCP tools.

1. Add `ix_conscience_signal` tool (wraps `AnomalyDetector`)
2. Add `ix_staleness_check` tool (wraps `StalenessPredictor`)
3. Add `ix_violation_analyze` tool (wraps `ViolationPatternAnalyzer`)
4. Add `ix_remediation_plan` tool (wraps `RemediationOptimizer`)
5. Add `ix_confidence_calibrate` tool (wraps `ConfidenceCalibrator`)

**Why second:** These tools are the analytical backbone for automated governance. The Rust implementations exist in `ix-governance`; they just need MCP tool wrappers.

### Phase 3: TARS Directive Generation Tool (Week 3)

**Goal:** TARS exposes grammar-constrained governance generation as an MCP tool.

1. Register `tars_generate_directive` as an MCP tool in `McpServer.fs`
2. Register `tars_validate_governance` for schema validation
3. Register `tars_governance_log` for dashboard consumption
4. Test: generate a directive from an ix analysis result

**Why third:** Depends on Phase 2 outputs as inputs.

### Phase 4: Conscience Automation Pipeline (Week 4)

**Goal:** Conscience signals auto-trigger the full analysis-to-directive pipeline.

1. Create `governance-automation-policy.yaml` in Demerzel
2. Create `automation-trigger.schema.json` in Demerzel
3. Implement the signal-to-directive pipeline (conscience signal -> ix analysis -> TARS directive -> Galactic Protocol delivery)
4. Add confidence gating per Demerzel thresholds
5. Test with existing conscience signals (e.g., `sig-remediation-2026-03-18-001`)

**Why fourth:** This is the capstone — it composes Phase 2 and Phase 3 into an automated governance loop.

### Phase 5: Dashboard Cross-Repo Views (Week 5)

**Goal:** ix-dashboard shows live cross-repo governance health.

1. Add MCP client capability to ix-dashboard
2. Add TARS status tools (`tars_grammar_status`, `tars_tool_metrics`)
3. Build cross-repo health view
4. Build conscience timeline view
5. Build directive flow view

**Why last:** Observability is valuable but not blocking. The automation pipeline (Phase 4) works without a dashboard.

### Phase 6: A2A Protocol (Future)

**Goal:** Full agent-to-agent task delegation across repos.

1. Define A2A adapter for `external-sync-envelope.schema.json`
2. Implement A2A server in TARS (it has the most mature MCP server)
3. Implement A2A client in ix
4. Add ga MCP server so it can participate
5. Test: TARS delegates an ML training task to ix via A2A

**Why future:** A2A is an industry protocol still maturing. MCP tool calls (Phase 1-3) cover 80% of the use cases with less complexity.

---

## Appendix A: Key File References

| File | Repo | Role |
|------|------|------|
| `v2/src/Tars.Evolution/GrammarMlBridge.fs` | tars | Feature extraction + ix ML integration |
| `v2/src/Tars.Core/GovernanceGeneration.fs` | tars | Grammar-constrained Galactic Protocol message generation |
| `v2/src/Tars.Connectors/Mcp/McpServer.fs` | tars | MCP server (150+ tools, progress, subagents) |
| `crates/ix-agent/src/tools.rs` | ix | 40+ MCP tool definitions |
| `crates/ix-governance/src/lib.rs` | ix | Governance crate: StateReader, AnomalyDetector, etc. |
| `crates/ix-dashboard/src/reader.rs` | ix | File-based state reader for TUI dashboard |
| `contracts/galactic-protocol.md` | Demerzel | Protocol spec for cross-repo communication |
| `schemas/conscience-signal.schema.json` | Demerzel | Schema for conscience discomfort signals |
| `policies/proto-conscience-policy.yaml` | Demerzel | Conscience behavioral policy |
| `policies/conscience-observability-policy.yaml` | Demerzel | Conscience metrics and reporting |

## Appendix B: Data Flow Diagram

```
                         Demerzel (Governance)
                    ┌──────────┴──────────┐
                    │  Conscience System   │
                    │  Galactic Protocol   │
                    │  Constitutions       │
                    └──────┬──────┬────────┘
                           │      │
              directive    │      │  compliance-report
              signal       │      │  belief-snapshot
                           │      │
                    ┌──────▼──┐ ┌─▼────────┐
                    │  TARS   │ │    ix     │
                    │  (F#)   │ │  (Rust)   │
                    └────┬────┘ └────┬──────┘
                         │           │
          IxCaller MCP   │           │  ix_tars_bridge
          (Phase 1)      │◄─────────►│  ix_ga_bridge
                         │           │
                    ┌────▼────┐ ┌────▼──────┐
                    │ Grammar │ │ ML Engine │
                    │ Distill │ │ Governance│
                    │ GovGen  │ │ Dashboard │
                    └─────────┘ └───────────┘
                              │
                         ┌────▼────┐
                         │   ga    │
                         │ (.NET)  │
                         │ Chatbot │
                         └─────────┘
```
