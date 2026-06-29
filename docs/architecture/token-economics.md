# Token Economics

## Philosophy

Token economics in the GuitarAlchemist ecosystem is not merely about minimizing cost. It is about optimizing for the best combination of:

- **Capability fit**: Does the model/tool have the required intelligence for the task?
- **Cost**: What is the financial impact of the operation?
- **Latency**: How quickly can the result be produced?
- **Reliability**: How consistent is the performance?
- **Evidence quality**: Does the output provide durable, verifiable evidence?
- **Risk**: What is the potential for harm (LawZero, etc.) if the model fails?
- **Reproducibility**: Can the result be reliably recreated?

The Harness should use expensive reasoning models only where they create significant leverage, while defaulting to cheaper or deterministic tools for routine operations.

## Budget Tiers

We categorize tasks into three budget tiers to guide model and tool selection.

| Tier | Name | Description | Expected Volume | Preferred Models/Tools |
|---|---|---|---|---|
| **Tier 1** | Heavy Reasoning / Architecture | Strongest models for architecture, roadmap, policy design, adversarial review, and strategic decisions. | Low | GPT-4o, Claude 3.5 Sonnet/Opus, Gemini 1.5 Pro |
| **Tier 2** | Production Implementation | Strong implementation agents for code generation, refactoring, tests, and PR fixes. | Medium | Claude 3.5 Sonnet, GPT-4o, specialized coding models |
| **Tier 3** | Cheap Classification & Summarization | Local/small models or deterministic tools for triage, label prediction, hygiene, and low-risk extraction. | High | Ollama (local), small hosted models (Llama 3, etc.), DuckDB |

## Capability Budget Policy

The following policy maps specific capabilities to budget tiers and preferred tools.

```yaml
capability_budget:
  architecture:
    budget_tier: premium_reasoning
    preferred_tools: [gpt-4o, claude-3-5-sonnet, gemini-1-5-pro]
  implementation:
    budget_tier: strong_builder
    preferred_tools: [claude-3-5-sonnet, codex]
  classification:
    budget_tier: cheap_or_local
    preferred_tools: [ollama, small_model, deterministic_rules]
  analytics:
    budget_tier: deterministic
    preferred_tools: [duckdb]
  search:
    budget_tier: deterministic_or_indexed
    preferred_tools: [sourcegraph, augment, ripgrep]
```

## Optimization Strategy

Seldon uses these tiers to generate advisory routing recommendations. The goal is to maximize the "Intelligence ROI" by ensuring that every token spent contributes meaningfully to the completion of the task while adhering to the budget constraints defined in `docs/workflows/aiw-budget-router.md`.
