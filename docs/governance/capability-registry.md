# Capability Registry

This registry defines the durable taxonomy of capabilities and the workers available to provide them within the ecosystem.

## Registry Version: 1

## Capability Taxonomy

| Capability | Role Name | Purpose |
| :--- | :--- | :--- |
| `repository_navigation` | Navigator | Repository analysis, dependency mapping, impact analysis, context preparation. |
| `implementation` | Builder | Code implementation, refactoring, tests, workflows. |
| `research` | Researcher | Research synthesis, methodology, ADRs, governance documentation. |
| `adversarial_review` | Critic | Architecture critique, governance critique, ambiguity detection, policy/safety review. |
| `bug_hunting` | Bug Hunter | Narrow defect finding, regression suspicion, PR review comments, test gap detection. |
| `security_review` | Security Reviewer | Secret exposure review, permission creep detection, workflow safety, supply-chain risk. |
| `orchestration` | Supervisor | Routing, metrics, escalation, collision avoidance, status monitoring. |
| `architecture` | Architect | Vision, product direction, strategic trade-offs, final authority. |

## Worker Registry

```yaml
workers:
  augment:
    capabilities:
      - repository_navigation
    authority: read_only
    cost_tier: existing_subscription_or_app
    preferred_for:
      - impact_analysis
      - pre_implementation_context

  claude:
    capabilities:
      - implementation
    authority: pr
    cost_tier: paid_or_subscription
    preferred_for:
      - complex_logic
      - heavy_refactoring

  jules:
    capabilities:
      - research
    authority: pr
    cost_tier: free_or_hosted
    preferred_for:
      - governance_docs
      - methodology_research

  gemini:
    capabilities:
      - adversarial_review
    authority: read_only_review
    cost_tier: paid_allowed_guarded
    preferred_for:
      - cross_file_policy_check
      - large_context_review

  codex:
    capabilities:
      - bug_hunting
      - security_review
    authority: review_or_pr
    cost_tier: subscription_or_platform
    preferred_for:
      - narrow_fix
      - security_scanning

  qodo:
    capabilities:
      - bug_hunting # PR-focused review
    authority: review
    cost_tier: subscription
    preferred_for:
      - pr_quality_gate

  sourcegraph:
    capabilities:
      - repository_navigation
    authority: read_only
    cost_tier: enterprise
    preferred_for:
      - multi_repo_context

  ollama_local:
    capabilities:
      - research # Basic summarization
      - bug_hunting # Basic classification
    authority: read_only
    cost_tier: free_local
    preferred_for:
      - low_risk_summarization
      - triage_classification

  demerzel:
    capabilities:
      - orchestration
    authority: supervisor
    cost_tier: infrastructure
    preferred_for:
      - governance_dispatch

  human:
    capabilities:
      - architecture
    authority: owner
    cost_tier: high
    preferred_for:
      - final_signoff
      - vision_setting
```
