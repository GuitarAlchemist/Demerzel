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

## Routing by Knowledge Type (parametric vs contextual)

The hierarchy above routes by **risk and stakes**. That is necessary but not
sufficient: it tends to send *every* hard task to a premium model, because "hard"
reads as "high-stakes". A second, orthogonal question sharpens it — **which kind of
knowledge does this task actually draw on?**

- **Parametric knowledge** lives in the model's weights (breadth, prior art,
  unprompted alternatives, "have you considered X?"). **Planning, grilling,
  architecture, and design exploration depend on it** — a bigger model is
  genuinely better here, because you are paying for what it knows that you did not
  put in the window.
- **Contextual knowledge** lives in the prompt (the agreed plan, the spec, the
  files already in context). **Implementation depends mostly on this** — once a
  task is well-scoped and the plan and seams are decided, a cheaper model performs
  close to a frontier one, because the hard thinking is already in the window.

**The rule:** *plan with the strongest model available; implement with the cheapest
model that clears the bar.* A difficult feature does **not** by itself justify a
premium implementation model — an under-specified one does. If implementation
quality is poor, the first remedy is a better plan/spec in context, not a bigger
model.

This composes with, and does not replace, the tier hierarchy: deterministic tools
still come first, and a high-**risk** change still escalates for review regardless
of which model produced the diff.

> Wiring note: `state/driver/aiw-worker-lanes.json` already classifies every role by
> `work_class` (`groom`/`review`/`navigate` are planning-shaped; `net_new_feature`/
> `fix` are implementation-shaped). That field is the natural hook for making this
> rule executable in `scripts/aiw_lane_selector.py`; it is documented doctrine
> today, not yet an enforced selector.

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
