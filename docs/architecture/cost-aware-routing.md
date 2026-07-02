# Cost-Aware Routing

## Overview

Cost-aware routing is the mechanism by which the GuitarAlchemist ecosystem selects the most appropriate and cost-effective tool or model for a given task. This is an advisory function performed by Seldon, providing recommendations to Demerzel.

## Routing Hierarchy

The router follows a strict hierarchy when selecting tools:

1.  **Deterministic Tools First**: If a task can be performed by a deterministic tool (e.g., `ripgrep`, `duckdb`, custom scripts), that tool is selected.
2.  **Local Models Second**: If a deterministic tool is insufficient, but the task is low-risk (e.g., summarization, classification, triage), a local model (via Ollama) is preferred.
3.  **Specialized Hosted Models Third**: For tasks requiring more intelligence but still within a specific domain (e.g., code generation), specialized hosted models or smaller cloud models are used.
4.  **Premium Reasoning Models Last**: Premium models (e.g., Claude 3.5 Opus, GPT-4o) are reserved for high-stakes reasoning, architecture, and strategic decisions where the value justifies the cost.

## Deterministic-First Policy

To avoid "LLM-by-default" patterns, the following tasks *must* attempt a deterministic approach before escalating:

- **Analytics and Metrics**: Use DuckDB or specialized scripts.
- **Search and Navigation**: Use `ripgrep`, `fd`, or specialized indexers.
- **Syntax Validation**: Use compilers, linters, or tree-sitter.
- **Dependency Analysis**: Use repo-specific package managers or graph tools.

## Escalation Rules

Escalation to a higher-cost tier is only permitted when:

-   A lower-tier tool has failed to produce sufficient evidence.
-   The task risk is classified as High or Critical (requiring premium reasoning).
-   The required context window exceeds the capacity of local/cheap models.
-   The "Matt-readiness" gate (`docs/workflows/aiw-matt-readiness-gate.md`) indicates that the task is ready for a high-capability agent.

## Seldon's Advisory Role

Seldon observes the stream of engineering events from Streeling and generates routing recommendations. These recommendations include:

-   **Suggested Tool/Model**: Based on the `capability_budget` policy in `docs/architecture/token-economics.md`.
-   **Estimated Cost**: Based on historical usage and prompt complexity.
-   **Confidence Score**: Seldon's confidence that the suggested tool can complete the task.

Demerzel uses these signals to make the final routing decision, ensuring that the project stays within its token budget while maintaining high engineering standards.

## Reference

For operational details on budget blocks and provider selection, see `docs/workflows/aiw-budget-router.md`.
