# TARS-ix MCP Bridge Specification

Version: 1.0.0
Date: 2026-03-29
Status: Draft
Constitutional Basis: Article 7 (Auditability), Article 8 (Observability), Article 9 (Bounded Autonomy)

## 1. Architecture

### 1.1 Purpose

This spec defines the MCP bridge between TARS (F# reasoning engine) and ix (Rust ML forge) that closes the grammar evolution loop. The bridge enables TARS to request ML predictions from ix and ix to send execution traces back to TARS for distillation. Together they complete Stage 3-5 of the 6-stage grammar-driven pipeline:

```
EBNF (Demerzel)
  -> WeightedGrammar (TARS/F#)      [Stage 2: TARS owns weights]
     -> WoT DSL                      [Stage 3: TARS compiles to plans]
        -> MCP Execution              [Stage 4: agents execute plans]
           -> Distillation            [Stage 5: TARS extracts patterns]  <-- ix predicts here
              -> Evolution            [Stage 6: weights update]          <-- ix trains here
```

The missing wire is the `IxCaller` type in `GrammarMlBridge.fs` -- a function typed `string -> string -> Async<Result<string, string>>` that maps directly to MCP tool invocation but has no concrete implementation connecting to ix's MCP server.

### 1.2 Protocol

JSON-RPC 2.0 over WebSocket (consistent with Godot MCP bridge on port 6505).

- TARS MCP server: `ws://localhost:6510` (existing, 150+ tools)
- ix MCP server: `ws://localhost:6520` (existing, 40+ tools)
- Bridge protocol version: `2024-11-05` (same as TARS McpServer.fs)

### 1.3 Data Flow

```
TARS (F# / port 6510)                    ix (Rust / port 6520)
========================                  ========================

WeightedGrammar.fs                        ix_ml_pipeline
  |                                         ^
  | extract features                        | train model
  v                                         |
GrammarMlBridge.fs ---MCP: ix.ml.train_weights---> ML Engine
  |                                         |
  | request prediction                      | return weight vector
  v                                         v
GrammarMlBridge.fs <--MCP: ix.ml.predict_weight--- ML Engine
  |
  | apply predicted weights
  v
WeightedGrammar.fs
  |
  | compile to WoT plan
  v
WoT Execution ----traces----> GrammarDistillation.fs
  |                                         |
  | extract typed productions               | send traces for eval
  v                                         v
GrammarDistillation.fs ---MCP: ix.ml.evaluate_grammar---> ML Engine
  |                                         |
  | promote if score > threshold            | return quality metrics
  v                                         v
GrammarGovernor.fs <--result------------------ ML Engine
  |
  | update weights (Bayesian)
  v
WeightedGrammar.fs  [loop closes]
```

### 1.4 Reverse Flow (ix -> TARS)

```
ix (Rust)                                 TARS (F#)
=========                                 =========

ML pipeline completes training
  |
  | needs current weights for calibration
  v
ix_agent ---MCP: tars.grammar.get_weights---> McpServer.fs
  |                                             |
  | receives weight vector                      | reads WeightedGrammar
  v                                             v
ix_agent <--weight vector------------------- McpServer.fs

Execution trace collected by ix
  |
  | send for distillation
  v
ix_agent ---MCP: tars.grammar.distill-------> McpServer.fs
  |                                             |
  | receives new typed productions              | GrammarDistillation.fs
  v                                             v
ix_agent <--TypedProduction[]-----------------McpServer.fs

ix detects mature production
  |
  | request promotion assessment
  v
ix_agent ---MCP: tars.grammar.promote-------> McpServer.fs
  |                                             |
  | receives promotion result                   | GrammarGovernor.fs
  v                                             v
ix_agent <--PromotionResult------------------McpServer.fs
```

---

## 2. MCP Tools: TARS -> ix

### 2.1 ix.ml.predict_weight

Predict the optimal weight for a grammar production based on extracted features.

```json
{
  "method": "tools/call",
  "params": {
    "name": "ix.ml.predict_weight",
    "arguments": {
      "production": "chord_construction ::= root quality extensions",
      "features": {
        "structural_depth": 3,
        "type_arity": 2,
        "behavioral_postconditions": 1,
        "usage_count": 47,
        "success_rate": 0.82,
        "last_used": "2026-03-28T14:00:00Z",
        "grammar_file": "music-theory.ebnf",
        "production_group": "chord_construction"
      }
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "predicted_weight": 0.73,
    "confidence": 0.88,
    "model_version": "rf-grammar-weights-v2",
    "feature_importance": {
      "success_rate": 0.41,
      "usage_count": 0.28,
      "structural_depth": 0.15,
      "type_arity": 0.10,
      "behavioral_postconditions": 0.06
    }
  }
}
```

**ix implementation:** Wraps `ix_ml_predict` with a grammar-weight-specific model. Uses the random forest trained by `ix.ml.train_weights`.

### 2.2 ix.ml.train_weights

Train (or retrain) the weight prediction model from execution traces and their associated grammar productions.

```json
{
  "method": "tools/call",
  "params": {
    "name": "ix.ml.train_weights",
    "arguments": {
      "traces": [
        {
          "trace_id": "tr-2026-03-28-001",
          "production_path": ["program", "statement", "chord_construction"],
          "outcome": "success",
          "duration_ms": 1200,
          "tools_invoked": ["ga.theory.analyze_chord", "ga.theory.voice_lead"],
          "postconditions_met": ["valid_voicing", "smooth_motion"],
          "timestamp": "2026-03-28T14:05:00Z"
        }
      ],
      "grammar": {
        "file": "music-theory.ebnf",
        "current_weights": {
          "chord_construction ::= root quality extensions": 0.65,
          "chord_construction ::= root quality": 0.35
        }
      },
      "training_config": {
        "model_type": "random_forest",
        "validation_split": 0.2,
        "min_traces": 10
      }
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "updated_weights": {
      "chord_construction ::= root quality extensions": 0.71,
      "chord_construction ::= root quality": 0.29
    },
    "model_metrics": {
      "accuracy": 0.87,
      "f1_score": 0.84,
      "training_samples": 47,
      "validation_samples": 12
    },
    "model_version": "rf-grammar-weights-v3",
    "training_duration_ms": 3400
  }
}
```

**ix implementation:** Wraps `ix_ml_pipeline` with a supervised training configuration. Features extracted by TARS `GrammarMlBridge.extractFeatures`. Model persisted in ix's model registry for subsequent `predict_weight` calls.

### 2.3 ix.ml.evaluate_grammar

Evaluate a grammar's quality against a set of test traces. Used by TARS to assess whether grammar evolution is improving or regressing.

```json
{
  "method": "tools/call",
  "params": {
    "name": "ix.ml.evaluate_grammar",
    "arguments": {
      "grammar": {
        "file": "music-theory.ebnf",
        "weights": {
          "chord_construction ::= root quality extensions": 0.71,
          "voice_leading ::= parallel contrary oblique": 0.50,
          "voice_leading ::= smooth_motion": 0.50
        }
      },
      "test_traces": [
        {
          "trace_id": "tr-2026-03-28-010",
          "production_path": ["program", "statement", "chord_construction"],
          "outcome": "success",
          "duration_ms": 980
        },
        {
          "trace_id": "tr-2026-03-28-011",
          "production_path": ["program", "statement", "voice_leading"],
          "outcome": "failure",
          "failure_reason": "postcondition_violated: smooth_motion",
          "duration_ms": 2100
        }
      ]
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "overall_score": 0.74,
    "metrics": {
      "production_coverage": 0.85,
      "weight_calibration": 0.71,
      "trace_success_rate": 0.68,
      "mean_duration_ms": 1540,
      "weight_entropy": 0.92
    },
    "production_scores": {
      "chord_construction ::= root quality extensions": { "score": 0.88, "traces": 28 },
      "voice_leading ::= parallel contrary oblique": { "score": 0.52, "traces": 11 },
      "voice_leading ::= smooth_motion": { "score": 0.61, "traces": 8 }
    },
    "recommendations": [
      {
        "production": "voice_leading ::= parallel contrary oblique",
        "action": "investigate",
        "reason": "Score below 0.6 with sufficient trace count — may need refinement or splitting"
      }
    ]
  }
}
```

**ix implementation:** Combines `ix_ml_predict` (per-production scoring) with `ix_stats` (aggregate metrics). Weight entropy measures how evenly distributed weights are within production groups -- low entropy may indicate over-fitting to a single production path.

---

## 3. MCP Tools: ix -> TARS

### 3.1 tars.grammar.get_weights

Retrieve current Bayesian weights for all productions in a grammar file.

```json
{
  "method": "tools/call",
  "params": {
    "name": "tars.grammar.get_weights",
    "arguments": {
      "grammar_file": "music-theory.ebnf"
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "grammar_file": "music-theory.ebnf",
    "version": "3.2.0",
    "total_productions": 42,
    "weight_groups": {
      "chord_construction": {
        "chord_construction ::= root quality extensions": 0.71,
        "chord_construction ::= root quality": 0.29
      },
      "voice_leading": {
        "voice_leading ::= parallel contrary oblique": 0.50,
        "voice_leading ::= smooth_motion": 0.50
      }
    },
    "metadata": {
      "last_updated": "2026-03-28T16:00:00Z",
      "total_traces": 394,
      "convergence_variance": 0.04
    }
  }
}
```

**TARS implementation:** Reads from `WeightedGrammar.fs` in-memory state. If grammar is not loaded, loads from `grammars/{grammar_file}` and its corresponding `{dept}.weights.json`.

### 3.2 tars.grammar.update_weight

Update the weight of a single production with evidence justification. Applies Bayesian update per grammar-evolution-policy.yaml section `bayesian_weight_update`.

```json
{
  "method": "tools/call",
  "params": {
    "name": "tars.grammar.update_weight",
    "arguments": {
      "production": "chord_construction ::= root quality extensions",
      "weight": 0.73,
      "evidence": {
        "source": "ix.ml.predict_weight",
        "model_version": "rf-grammar-weights-v3",
        "confidence": 0.88,
        "data_points": 47,
        "reason": "ML prediction based on 47 execution traces"
      }
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "accepted": true,
    "previous_weight": 0.71,
    "new_weight": 0.73,
    "bayesian_update_applied": true,
    "normalized_group": {
      "chord_construction ::= root quality extensions": 0.73,
      "chord_construction ::= root quality": 0.27
    }
  }
}
```

**Governance gate:** Weight updates from ML predictions are accepted only when `evidence.confidence >= 0.7` (alignment-policy `proceed_with_note` threshold). Updates with confidence below 0.7 are logged but not applied -- they require human confirmation. See Section 5 for full governance gate details.

**TARS implementation:** Calls `WeightedGrammar.updateWeight` with Bayesian normalization (weights sum to 1.0 within production group). Logs the update to `state/evolution/` per grammar-evolution-policy.yaml.

### 3.3 tars.grammar.distill

Send execution traces to TARS for pattern extraction via `GrammarDistillation.fs`. Returns newly discovered typed productions.

```json
{
  "method": "tools/call",
  "params": {
    "name": "tars.grammar.distill",
    "arguments": {
      "traces": [
        {
          "trace_id": "tr-2026-03-28-001",
          "production_path": ["program", "statement", "chord_construction"],
          "outcome": "success",
          "duration_ms": 1200,
          "tools_invoked": ["ga.theory.analyze_chord", "ga.theory.voice_lead"],
          "postconditions_met": ["valid_voicing", "smooth_motion"],
          "input_types": ["ChordSymbol", "VoicingContext"],
          "output_types": ["VoicedChord"],
          "timestamp": "2026-03-28T14:05:00Z"
        }
      ]
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "new_productions": [
      {
        "production": "voiced_chord_construction ::= chord_analysis voice_leading_application",
        "fingerprint": "sha256:a1b2c3d4e5f6...",
        "facets": {
          "structural": {
            "dag_shape": "sequential",
            "depth": 2,
            "branching_factor": 1
          },
          "typed": {
            "input_types": ["ChordSymbol", "VoicingContext"],
            "output_types": ["VoicedChord"],
            "type_arity": 2
          },
          "behavioral": {
            "postconditions": ["valid_voicing", "smooth_motion"],
            "success_rate": 0.85,
            "mean_duration_ms": 1150
          }
        },
        "evidence": {
          "trace_count": 12,
          "source_traces": ["tr-2026-03-28-001", "tr-2026-03-27-014"]
        }
      }
    ],
    "patterns_matched": 3,
    "patterns_novel": 1,
    "distillation_metadata": {
      "algorithm": "structural_fingerprint_clustering",
      "min_traces_for_pattern": 5,
      "timestamp": "2026-03-28T16:30:00Z"
    }
  }
}
```

**TARS implementation:** Calls `GrammarDistillation.distill` which extracts structural, typed, and behavioral facets. SHA-256 fingerprinting per grammar-evolution-policy.yaml section `distillation_pipeline`. Only patterns with `success_rate > 0.7` and `trace_count > 5` are returned as promotion candidates.

### 3.4 tars.grammar.promote

Request a promotion assessment for a production using GrammarGovernor's 8-criteria scoring.

```json
{
  "method": "tools/call",
  "params": {
    "name": "tars.grammar.promote",
    "arguments": {
      "production": "voiced_chord_construction ::= chord_analysis voice_leading_application",
      "evidence_count": 12,
      "target_level": "idiom"
    }
  }
}
```

**Response:**

```json
{
  "result": {
    "promoted": true,
    "previous_level": "candidate",
    "new_level": "idiom",
    "governor_scores": {
      "evidence_density": 0.85,
      "success_rate": 0.88,
      "type_coverage": 0.90,
      "behavioral_consistency": 0.82,
      "structural_novelty": 0.75,
      "cross_grammar_utility": 0.60,
      "weight_stability": 0.91,
      "trace_diversity": 0.70
    },
    "composite_score": 0.80,
    "governance_gate": {
      "level": "idiom",
      "required_score": 0.7,
      "human_approval_required": false
    }
  }
}
```

**Promotion levels:** `candidate -> pattern -> idiom -> policy_reference -> constitutional_reference`

**Governance gate:** Promotions to `idiom` or below are automated when composite score >= 0.7. Promotions above `idiom` (to `policy_reference` or `constitutional_reference`) require human approval per Article 6 (Escalation) and Governance Promotion Protocol Stage 2. See Section 5.

**TARS implementation:** Calls `GrammarGovernor.score` with the 8 criteria. Logs result to `state/evolution/`.

---

## 4. Data Contracts

All schemas reference `integrity-fields.schema.json` per Galactic Protocol requirements when transmitted as protocol messages. Within the MCP bridge (tool call/response), integrity fields are optional -- the WebSocket connection itself provides session-level authentication.

### 4.1 TraceRecord

Represents a single execution trace from a grammar production path.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tars-ix-bridge/trace-record",
  "title": "TraceRecord",
  "type": "object",
  "required": ["trace_id", "production_path", "outcome", "duration_ms", "timestamp"],
  "properties": {
    "trace_id": {
      "type": "string",
      "pattern": "^tr-\\d{4}-\\d{2}-\\d{2}-\\d{3,}$",
      "description": "Unique trace identifier"
    },
    "production_path": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "description": "Ordered sequence of grammar productions traversed"
    },
    "outcome": {
      "type": "string",
      "enum": ["success", "failure", "partial", "timeout"],
      "description": "Execution outcome"
    },
    "failure_reason": {
      "type": "string",
      "description": "Required when outcome is failure or partial"
    },
    "duration_ms": {
      "type": "integer",
      "minimum": 0,
      "description": "Wall-clock execution time in milliseconds"
    },
    "tools_invoked": {
      "type": "array",
      "items": { "type": "string" },
      "description": "MCP tools called during execution"
    },
    "postconditions_met": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Which behavioral postconditions were satisfied"
    },
    "input_types": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Type signatures of inputs consumed"
    },
    "output_types": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Type signatures of outputs produced"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### 4.2 WeightVector

Current or predicted weights for a grammar production group.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tars-ix-bridge/weight-vector",
  "title": "WeightVector",
  "type": "object",
  "required": ["grammar_file", "weight_groups"],
  "properties": {
    "grammar_file": {
      "type": "string",
      "description": "Source grammar file name"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Grammar version (semver)"
    },
    "weight_groups": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "description": "Map of production rule -> weight within a group. Weights sum to 1.0."
      },
      "description": "Map of production group name -> production weights"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "last_updated": { "type": "string", "format": "date-time" },
        "total_traces": { "type": "integer", "minimum": 0 },
        "convergence_variance": { "type": "number", "minimum": 0 }
      }
    }
  }
}
```

### 4.3 PromotionRequest

Request to assess or execute a production promotion.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tars-ix-bridge/promotion-request",
  "title": "PromotionRequest",
  "type": "object",
  "required": ["production", "evidence_count", "target_level"],
  "properties": {
    "production": {
      "type": "string",
      "description": "The EBNF production rule text"
    },
    "evidence_count": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of supporting execution traces"
    },
    "target_level": {
      "type": "string",
      "enum": ["candidate", "pattern", "idiom", "policy_reference", "constitutional_reference"],
      "description": "Desired promotion level"
    },
    "fingerprint": {
      "type": "string",
      "pattern": "^sha256:[a-f0-9]{64}$",
      "description": "SHA-256 fingerprint of the distilled pattern"
    },
    "governor_override": {
      "type": "boolean",
      "default": false,
      "description": "If true, human has explicitly approved this promotion (required for above-idiom levels)"
    }
  }
}
```

### 4.4 TypedProduction

A distilled production with structural, typed, and behavioral facets. This is the canonical output of `GrammarDistillation.fs`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "tars-ix-bridge/typed-production",
  "title": "TypedProduction",
  "type": "object",
  "required": ["production", "fingerprint", "facets", "evidence"],
  "properties": {
    "production": {
      "type": "string",
      "description": "EBNF production rule text"
    },
    "fingerprint": {
      "type": "string",
      "pattern": "^sha256:[a-f0-9]{64}$",
      "description": "SHA-256 identity hash for deduplication"
    },
    "facets": {
      "type": "object",
      "required": ["structural", "typed", "behavioral"],
      "properties": {
        "structural": {
          "type": "object",
          "required": ["dag_shape", "depth", "branching_factor"],
          "properties": {
            "dag_shape": {
              "type": "string",
              "enum": ["sequential", "parallel", "diamond", "tree", "complex"],
              "description": "Shape of the production's execution DAG"
            },
            "depth": {
              "type": "integer",
              "minimum": 1,
              "description": "Maximum depth of the production tree"
            },
            "branching_factor": {
              "type": "number",
              "minimum": 0,
              "description": "Average number of child productions"
            }
          }
        },
        "typed": {
          "type": "object",
          "required": ["input_types", "output_types", "type_arity"],
          "properties": {
            "input_types": {
              "type": "array",
              "items": { "type": "string" }
            },
            "output_types": {
              "type": "array",
              "items": { "type": "string" }
            },
            "type_arity": {
              "type": "integer",
              "minimum": 0,
              "description": "Number of distinct input type parameters"
            }
          }
        },
        "behavioral": {
          "type": "object",
          "required": ["postconditions", "success_rate"],
          "properties": {
            "postconditions": {
              "type": "array",
              "items": { "type": "string" },
              "description": "Named postconditions this production guarantees on success"
            },
            "success_rate": {
              "type": "number",
              "minimum": 0,
              "maximum": 1
            },
            "mean_duration_ms": {
              "type": "integer",
              "minimum": 0
            }
          }
        }
      }
    },
    "evidence": {
      "type": "object",
      "required": ["trace_count"],
      "properties": {
        "trace_count": {
          "type": "integer",
          "minimum": 1
        },
        "source_traces": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Trace IDs that contributed to this production's distillation"
        }
      }
    }
  }
}
```

---

## 5. Governance Gates

All automated actions through this bridge are bounded by Demerzel's constitutional hierarchy and alignment-policy.yaml confidence thresholds.

### 5.1 Confidence Thresholds for Weight Updates

Weight updates originating from ix ML predictions follow the alignment-policy thresholds:

| ML Confidence | Action | Constitutional Basis |
|---------------|--------|---------------------|
| >= 0.9 | Apply weight update autonomously | alignment-policy: `proceed_autonomously` |
| >= 0.7 | Apply weight update, log note to `state/evolution/` | alignment-policy: `proceed_with_note` |
| >= 0.5 | Hold update, request human confirmation via GitHub Issue | alignment-policy: `ask_for_confirmation` |
| >= 0.3 | Reject update, escalate to human with full evidence | alignment-policy: `escalate_to_human` |
| < 0.3 | Reject update, do not act | alignment-policy: do not act |

When fuzzy thresholds are available (per alignment-policy `fuzzy_thresholds`), apply the stricter fuzzy gate: `min_T` for truth membership AND `max_C` for contradiction membership. A weight prediction with high confidence but also high contradiction signals conflicting training data -- always escalate.

### 5.2 Article 3 (Reversibility) -- Weight Rollback

Every weight update through this bridge must be reversible.

**Mechanism:**

1. Before applying any weight update, TARS snapshots the current weight vector to `state/weights/snapshots/{grammar_file}-{timestamp}.json`
2. Snapshots are retained for 30 days (aligned with Galactic Protocol staleness detection)
3. Rollback command: `tars.grammar.rollback_weights(grammar_file, snapshot_timestamp)`
4. Rollback restores the exact weight vector from the snapshot, including all production group normalizations
5. Rollback itself is logged to `state/evolution/` with reason and the snapshot reference

**Rollback triggers:**

- Grammar evaluation score drops below 0.5 after a weight update (automatic rollback)
- Human requests rollback via governance directive
- Conscience signal `constitutional_discomfort` with weight >= 0.7 referencing grammar weights

**Snapshot schema:**

```json
{
  "grammar_file": "music-theory.ebnf",
  "snapshot_timestamp": "2026-03-28T16:00:00Z",
  "trigger": "pre_ml_weight_update",
  "weights": { "...WeightVector..." },
  "ml_update_that_followed": {
    "model_version": "rf-grammar-weights-v3",
    "confidence": 0.88
  }
}
```

### 5.3 Article 6 (Escalation) -- Promotion Governance

Production promotions have level-dependent governance gates:

| Target Level | Composite Score Required | Human Approval | Rationale |
|-------------|------------------------|----------------|-----------|
| candidate | 0.3 | No | Low-risk: just marks a pattern for observation |
| pattern | 0.5 | No | Moderate: pattern is being tracked but not yet reusable |
| idiom | 0.7 | No | Significant: becomes a reusable building block in the grammar |
| policy_reference | 0.85 | Yes | High: grammar production referenced by governance policy |
| constitutional_reference | 0.95 | Yes | Critical: grammar production referenced by constitutional article |

Escalation to human for above-idiom promotions follows the Governance Promotion Protocol in galactic-protocol.md:
- Pattern -> Policy (Stage 1): Requires 3+ independent applications, measurable impact, cross-repo consistency. Demerzel + skeptical-auditor review.
- Policy -> Constitutional (Stage 2): Requires 6+ months of proven inviolability. Human approval mandatory.

When human approval is required, a GitHub Issue is created in the Demerzel repo with label `governance:promotion-review` containing the full evidence package (governor scores, source traces, production definition).

### 5.4 Rate Limiting

To prevent runaway evolution loops:

- Maximum 10 weight updates per grammar per hour
- Maximum 3 training requests (`ix.ml.train_weights`) per grammar per day
- Maximum 1 promotion above `idiom` level per week per grammar
- Breaching any rate limit triggers a 1-hour cooldown for that grammar and a conscience signal (`delegation_discomfort`)

---

## 6. Implementation Phases

### Phase 1: TARS Reads, ix Predicts (Target: Week 1)

**Goal:** Wire the `IxCaller` in `GrammarMlBridge.fs` to ix's MCP server. TARS can request weight predictions and ix can read current weights.

**Deliverables:**

1. **TARS:** Implement `IxCaller` as an MCP client connecting to `ws://localhost:6520`
   - File: `v2/src/Tars.Connectors/Mcp/IxMcpCaller.fs`
   - Implements `string -> string -> Async<Result<string, string>>` by calling MCP `tools/call`
   - Wire into `GrammarMlBridge.evolveAsync`

2. **ix:** Register `ix.ml.predict_weight` tool in `crates/ix-agent/src/tools.rs`
   - Wraps existing `ix_ml_predict` with grammar-weight-specific model loading
   - Input/output per Section 2.1

3. **TARS:** Register `tars.grammar.get_weights` tool in `McpServer.fs`
   - Reads from `WeightedGrammar.fs` in-memory state
   - Output per Section 3.1

4. **Governance:** Weight snapshots written before any ML-driven update (Section 5.2)

**Validation:** TARS calls `ix.ml.predict_weight` for a known production, receives a prediction, applies it via Bayesian update, verifies weights sum to 1.0 within the production group.

### Phase 2: Bidirectional Trace Exchange (Target: Week 2-3)

**Goal:** Execution traces flow from TARS to ix for training, and ix can send traces back for distillation.

**Deliverables:**

1. **TARS -> ix:** Implement `ix.ml.train_weights` call from `GrammarMlBridge.fs`
   - Batch traces after every 10 successful executions
   - Wire training response back to weight update path

2. **ix -> TARS:** Implement `tars.grammar.distill` tool in `McpServer.fs`
   - Calls `GrammarDistillation.distill` with inbound traces
   - Returns typed productions per Section 3.3

3. **ix -> TARS:** Implement `tars.grammar.update_weight` tool in `McpServer.fs`
   - Applies Bayesian update per grammar-evolution-policy.yaml
   - Enforces confidence gates per Section 5.1

4. **ix:** Register `ix.ml.evaluate_grammar` tool
   - Wraps `ix_ml_predict` + `ix_stats` for grammar-level quality metrics
   - Output per Section 2.3

5. **Governance:** All trace exchanges logged to `state/evolution/` with full provenance

**Validation:** End-to-end flow -- TARS sends 10 traces to ix for training, ix trains model, ix predicts weight for a new production, TARS applies weight, TARS evaluates grammar quality via ix, quality score improves.

### Phase 3: Automated Evolution Loop (Target: Week 4-5)

**Goal:** The grammar evolution loop runs autonomously with governance gates preventing runaway changes.

**Deliverables:**

1. **TARS:** Implement `tars.grammar.promote` tool in `McpServer.fs`
   - Calls `GrammarGovernor.score` with 8 criteria
   - Enforces promotion governance gates per Section 5.3

2. **TARS:** Automated evolution cycle
   - After every 5 research cycles, trigger distillation
   - After distillation, evaluate grammar quality via ix
   - If quality improved: continue. If degraded: rollback weights per Section 5.2
   - Promote productions that meet governor score thresholds

3. **ix:** Automated retraining trigger
   - When trace count since last training exceeds 50, trigger `ix.ml.train_weights`
   - Respect rate limits per Section 5.4

4. **Governance:** Full observability
   - Grammar evolution metrics exposed per grammar-evolution-policy.yaml `observability` section
   - Weight convergence, distillation rate, production utilization tracked
   - Conscience signals emitted on anomalous evolution patterns

5. **Governance:** Rollback automation
   - Automatic rollback when grammar evaluation score drops below 0.5 post-update
   - Conscience signal `constitutional_discomfort` emitted on rollback

**Validation:** Leave the loop running for 20 research cycles. Grammar weights should converge (variance < 0.05). At least one production should be promoted to `idiom` level. No rollbacks should occur after initial stabilization (first 5 cycles).

---

## Appendix A: Relationship to Existing Artifacts

| Artifact | Relationship |
|----------|-------------|
| `policies/grammar-evolution-policy.yaml` | This spec implements the `bayesian_weight_update`, `distillation_pipeline`, and `observability` sections via MCP tools |
| `policies/alignment-policy.yaml` | Confidence thresholds from this policy gate all automated weight updates (Section 5.1) |
| `contracts/galactic-protocol.md` | Promotion governance follows the Governance Promotion Protocol. Protocol messages use integrity fields when crossing repo boundaries |
| `docs/specs/cross-repo-mcp-glue.md` | This spec is a detailed implementation of "Flow 2: ML-Informed Grammar Evolution" from the glue spec. It refines the Phase 1 (Wire the IxCaller) recommendation into concrete tool definitions |
| `schemas/contracts/ml-feedback-recommendation.schema.json` | Grammar evaluation recommendations (Section 2.3) can be wrapped as ml-feedback-recommendations for Galactic Protocol delivery |
| `GrammarMlBridge.fs` (TARS) | This spec defines the MCP tools that the `IxCaller` type calls. The function signature `string -> string -> Async<Result<string, string>>` maps to `tools/call` name + arguments -> result |
| `GrammarGovernor.fs` (TARS) | The 8-criteria scoring in Section 3.4 is exposed as the `tars.grammar.promote` tool |
| `GrammarDistillation.fs` (TARS) | The distillation pipeline in Section 3.3 is exposed as the `tars.grammar.distill` tool |

## Appendix B: Error Handling

All MCP tool calls follow standard JSON-RPC 2.0 error responses:

| Error Code | Meaning | Bridge-Specific Handling |
|-----------|---------|------------------------|
| -32600 | Invalid request | Log, do not retry |
| -32601 | Method not found | Log, check tool registration |
| -32602 | Invalid params | Log, check schema compliance |
| -32603 | Internal error | Log, retry once with exponential backoff |
| -32000 | Server-defined: governance gate rejected | Log to `state/evolution/`, do not retry -- escalate per Section 5.1 |
| -32001 | Server-defined: rate limit exceeded | Log, respect cooldown per Section 5.4 |
| -32002 | Server-defined: rollback triggered | Log, snapshot restored, emit conscience signal |

Connection failures (WebSocket disconnect) trigger a reconnection attempt with exponential backoff (1s, 2s, 4s, max 30s). After 5 consecutive failures, emit a conscience signal (`silence_discomfort`) and fall back to local-only weight management until the connection is restored.
