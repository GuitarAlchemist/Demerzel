---
name: ix-ml-builder
description: Build ephemeral or persistent ML pipelines via ix MCP — auto-detects task type, selects models, handles preprocessing, evaluation, and caching
---

# ML Pipeline Builder (via ix MCP)

Build complete ML pipelines from data to predictions in one tool call using the ix MCP server.

## Prerequisites
The ix MCP server must be registered in your `.mcp.json`:
```json
{ "ix": { "command": "cargo", "args": ["run", "--release", "-p", "ix-agent"], "cwd": "path/to/ix" } }
```

## When to Use
When you have data (CSV, JSON, or inline) and want ML analysis — classification, regression, clustering, or dimensionality reduction.

## Quick Start
```json
ix_ml_pipeline({
  "source": { "type": "csv", "path": "data.csv", "target_column": "label" },
  "task": "auto",
  "model": "auto",
  "preprocess": { "normalize": true }
})
```

## Task Auto-Detection
| Signal | Task | Default Model |
|--------|------|---------------|
| 2 unique integer values in target | Binary classification | LogisticRegression |
| 3-20 unique integers, low ratio | Multiclass classification | DecisionTree |
| Continuous target (>20 unique) | Regression | LinearRegression |
| No target column | Clustering | KMeans (k=3) |

## Model Selection
| Data Size | Recommended |
|-----------|-------------|
| < 100 rows | KNN (classify) or LinearRegression (regress) |
| 100-10k | DecisionTree (classify) or LinearRegression (regress) |
| 10k+ | RandomForest (classify) or LinearRegression (regress) |

## Persistent Pipelines
Train once, predict later:
```json
ix_ml_pipeline({ ..., "persist": true, "persist_key": "my_model" })
ix_ml_predict({ "persist_key": "my_model", "data": [[1,2,3]] })
```

## MCP Tools
- `ix_ml_pipeline` — Full pipeline: load → preprocess → train → evaluate → persist
- `ix_ml_predict` — Load cached model, predict on new data

## Source
Full documentation: ix repo `.claude/skills/ix-ml-builder/SKILL.md`
