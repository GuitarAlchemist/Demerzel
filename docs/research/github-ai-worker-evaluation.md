# GitHub AI Worker Evaluation

This document evaluates various AI workers as potential capability providers within the Harness-Driven Development (HDD) framework. The goal is to move from vendor-locked dependencies to a capability-based routing model.

## Evaluation Framework

Workers are evaluated based on their performance, cost, and suitability for specific roles within the ecosystem.

| Worker | Primary Role(s) | Strength | Weakness |
| :--- | :--- | :--- | :--- |
| **Augment Code** | Navigator | Deep repository intelligence, impact analysis. | Proprietary, requires indexing. |
| **Claude** | Builder | Code implementation, refactoring, test generation. | Costly at high volumes. |
| **Jules** | Researcher | Governance documentation, research synthesis. | Limited implementation breadth. |
| **Gemini** | Critic | Adversarial review, policy checking, long context. | Variable code implementation quality. |
| **Codex** | Bug Hunter / Security | Narrow defect finding, security review. | Context window limitations. |
| **Qodo** | PR Reviewer | PR quality review, test-gap analysis. | Specific to PR workflow. |
| **Sourcegraph Amp** | Navigator | Codebase-wide context and navigation. | Requires Sourcegraph infrastructure. |
| **GitHub Agent HQ** | Supervisor | Upstream dispatch surface, GitHub-native. | Evolving, may have platform lock-in. |
| **JetBrains AI** | Navigator / Builder | IDE-integrated navigation and implementation. | Local to IDE, harder to use in AFK loops. |
| **Local Ollama** | Utility / Classifier | Low-cost classification, summarization, dry-runs. | Limited capability for complex logic. |

## Capability Provider Details

### 1. Augment Code (Navigator)
- **Capability:** Repository Intelligence & Impact Analysis.
- **Suitability:** High. Excels at understanding complex dependencies and preparing context for builders.
- **Authority:** Read-only.
- **Cost Tier:** Existing subscription/app.

### 2. Claude (Builder)
- **Capability:** Implementation, Refactoring, Tests.
- **Suitability:** Very High. Currently the benchmark for reliable code generation and complex refactoring.
- **Authority:** PR.
- **Cost Tier:** Paid/Subscription.

### 3. Jules (Researcher)
- **Capability:** Research Synthesis, Methodology, Governance.
- **Suitability:** High. Tailored for maintaining the Demerzel governance corpus.
- **Authority:** PR (for documentation).
- **Cost Tier:** Free/Hosted.

### 4. Gemini via Google AI Studio (Critic)
- **Capability:** Adversarial Review, Architecture Critique.
- **Suitability:** High. Massive context window allows for reviewing entire repos against policy.
- **Authority:** Read-only review.
- **Cost Tier:** Paid (guarded).

### 5. Codex (Bug Hunter / Security Reviewer)
- **Capability:** Narrow defect finding, security review, second implementation opinion.
- **Suitability:** Medium-High. Good for specific, scoped verification tasks.
- **Authority:** Review or PR (narrow fix).
- **Cost Tier:** Subscription/Platform.

### 6. Qodo (PR Reviewer)
- **Capability:** PR Quality, Test-Gap Analysis.
- **Suitability:** High for specific PR gates.
- **Authority:** Review.
- **Cost Tier:** Subscription.

### 7. Sourcegraph Amp (Navigator)
- **Capability:** Large-scale repository navigation.
- **Suitability:** High for very large or multi-repo contexts.
- **Authority:** Read-only.
- **Cost Tier:** Enterprise.

### 8. GitHub Agent HQ (Supervisor)
- **Capability:** Agent Orchestration.
- **Suitability:** Potential upstream dispatcher.
- **Authority:** Orchestration.
- **Cost Tier:** Platform-native.

### 9. JetBrains AI / Local IDE Agents
- **Capability:** Local Navigation & Implementation.
- **Suitability:** Best for developer-in-the-loop (DITL) support.
- **Authority:** Local.
- **Cost Tier:** IDE Subscription.

### 10. Local Ollama Models
- **Capability:** Classification, Summarization, Dry-runs.
- **Suitability:** High for non-critical, high-volume tasks that benefit from zero marginal cost.
- **Authority:** Internal/Read-only.
- **Cost Tier:** Free/Local.
