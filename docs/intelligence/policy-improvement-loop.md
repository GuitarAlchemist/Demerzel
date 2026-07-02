# Policy Improvement Loop

The Policy Improvement Loop is the mechanism by which Seldon's insights are translated into actionable governance changes in Demerzel. This closes the "Learn → Decide" gap.

## Periodic Intelligence Summaries

Seldon generates periodic (weekly/monthly) intelligence summaries that highlight systemic patterns and suggest adjustments.

### Suggested Improvements

| Suggestion Type | Basis | Example |
|---|---|---|
| **Capability Registry Weight Update** | Observed performance shift. | "Increase Jules' weight for implementation; decrease Gemini's." |
| **Workflow Noise Classification** | High conversation noise ratio. | "Mark DependencyUpdate bot as 'Advisory only' to reduce noise." |
| **Review Tier Adjustment** | High defect leakage or success rate. | "Escalate ga repo PRs to Tier 3 review for junior workers." |
| **Test Coverage Mandate** | Recurring failure category. | "Add mandatory integration tests for all new IxQL pipelines." |
| **Local Model Preference** | High cost/success for simple tasks. | "Route Small/Medium triage tasks to Ollama-local to save budget." |
| **Human Escalation Rule** | High collision or failure rate in domain. | "Escalate all changes to `constitutions/` to Human Architect review." |

## The Improvement Process

1. **Pattern Detection:** Seldon identifies a recurring issue or opportunity (e.g., "Reviewer X catches 80% of bugs in .NET code").
2. **Drafting Suggestion:** Seldon formulates a `PolicySuggestion` with evidence and rationale.
3. **Trigger:** Seldon creates a trigger event for Demerzel's driver.
4. **Review:** Demerzel's driver presents the suggestion during its `COMPOUND` phase.
5. **Enactment:** If Demerzel (or a Human Architect) approves, a PR is opened to update the relevant policy, persona, or registry in the `Demerzel` repo.

## Example Suggestion

```yaml
policy_suggestion:
  id: SUG-2026-004
  title: "Prefer Local Models for Triage"
  rationale: "Seldon observes that 90% of triage tasks for 'tars' repo are correctly handled by Ollama-local, with a 70% cost reduction compared to Claude."
  evidence:
    period: "2026-05-01 to 2026-06-01"
    sample_size: 150
    accuracy_delta: -2%
    cost_savings: "$45.00"
  action:
    target: "policies/routing-policy.yaml"
    modification: "Set default_worker: ollama_local for category: triage"
  status: pending_review
```

## Benefits of the Loop

- **Data-Driven Governance:** Policies evolve based on empirical evidence rather than intuition.
- **Continuous Optimization:** The system automatically identifies and corrects inefficiencies.
- **Reduced Human Burden:** Humans only review high-value, synthesized suggestions rather than raw event logs.
