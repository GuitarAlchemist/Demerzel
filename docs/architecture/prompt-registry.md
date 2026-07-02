# Prompt Registry

**Status:** Proposed / DRAFT
**Version:** 0.1.0
**Date:** 2026-07-02
**Owner:** Seldon (Chancellor of Streeling)

## Purpose

The Prompt Registry is a central repository for all structured prompts used within the GuitarAlchemist ecosystem. It decouples prompt engineering from implementation code, enables versioning, and provides Seldon with the data needed to make cost and capability-aware routing decisions.

## Registry Structure

Each prompt in the registry is defined by a unique ID and contains the following metadata:

| Field | Description |
|---|---|
| `prompt_id` | Unique identifier (e.g., `triage-v1`, `refactor-core-v2`). |
| `version` | Semver version of the prompt. |
| `intended_capability` | The capability this prompt fulfills (e.g., `classification`, `implementation`). |
| `recommended_model` | The model best suited for this prompt based on historical performance. |
| `expected_cost` | Average or estimated cost per invocation. |
| `success_rate` | Percentage of invocations that met success criteria. |
| `failure_modes` | Common ways this prompt fails (e.g., hallucinations, context overflow). |
| `evaluation_examples` | Link to a set of input/output pairs for evaluation. |
| `owner_source` | The team or individual responsible for this prompt. |
| `evidence_references` | Links to PRs or issues where this prompt was used successfully. |

## Integration with Routing

When Demerzel or a sub-agent needs to perform a task, they query the Prompt Registry by `capability`. The registry returns the optimal prompt and the `recommended_model`.

If the `recommended_model` exceeds the current budget tier, Seldon can suggest a fallback model from the registry that has a lower cost, even if it has a lower expected success rate.

## Evaluation and Evolution

Prompts are treated as first-class engineering artifacts. Changes to prompts must be:

1.  **Tested**: Validated against the `evaluation_examples`.
2.  **Reviewed**: Subject to the same peer review process as code.
3.  **Monitored**: Seldon tracks the live performance (success rate, cost) and updates the registry metadata accordingly.

## Local-First Prompts

The registry explicitly identifies prompts that are compatible with local models (e.g., Ollama/Llama 3). These are prioritized for Tier 3 tasks to maximize avoided cost from paid providers.
