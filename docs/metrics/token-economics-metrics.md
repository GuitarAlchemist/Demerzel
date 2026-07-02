# Token Economics Metrics

## Overview

Seldon is responsible for tracking and reporting on the economic performance of the AI workforce. This telemetry provides the evidence needed to refine routing policies and budget tiers.

## Core Metrics (KPIs)

Seldon should track the following metrics, derived from Streeling event streams:

| Metric | Description | Purpose |
|---|---|---|
| **Cost per PR** | Total USD cost (tokens + runner minutes) for a single PR. | Efficiency tracking. |
| **Cost per Merged PR** | Total cost for PRs that successfully reach the `merged` state. | ROI calculation. |
| **Cost per Issue** | Total cost to resolve a single GitHub issue. | Resource allocation. |
| **Cost per Capability** | Total cost spent on specific capabilities (e.g., `implementation`, `architecture`). | Identifies expensive domains. |
| **Cost per Worker** | Total cost attributed to a specific AI worker/agent. | Performance evaluation. |
| **Cost per Sprint** | Cumulative cost over a fixed development cycle. | Budget management. |
| **Token Usage by Model** | Breakdowns of tokens by provider (OpenAI, Anthropic, Google) and model. | Provider management. |
| **Cost per Accepted Finding** | Cost to generate a review finding that is subsequently fixed/accepted. | Review quality metric. |
| **Cost per Success** | Total cost divided by the number of tasks meeting their success criteria. | Intelligence ROI. |
| **Local-vs-Paid Ratio** | Ratio of tasks handled by local models vs. paid cloud models. | Target: Increasing local usage. |
| **Deterministic-vs-LLM Ratio**| Ratio of tasks resolved by deterministic tools vs. LLM judgment. | Target: Maximize deterministic tools. |
| **Avoided Cost** | Estimated USD saved by using local models/DuckDB instead of premium LLMs. | "False economy" detection. |

## Event Logging

To capture these metrics, all AI worker events must include a `cost_block` in their metadata:

```json
"cost_block": {
  "provider": "anthropic",
  "model": "claude-3-5-sonnet-20240620",
  "input_tokens": 1240,
  "output_tokens": 850,
  "cost_usd": 0.015,
  "duration_ms": 4500,
  "capability": "implementation",
  "tool_use": ["ripgrep", "file_read"]
}
```

## Reporting

Seldon generates a weekly **Economic Intelligence Report** that highlights:

1.  **Budget Burn Rate**: Are we on track for the monthly budget?
2.  **Intelligence Efficiency**: Which models are providing the best value per dollar?
3.  **Optimization Opportunities**: Where can LLM usage be replaced by deterministic tools or local models?
4.  **Regression Risks**: Are we seeing a drop in quality or success rate due to aggressive cost cutting?
