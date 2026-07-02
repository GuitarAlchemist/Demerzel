# Capability-Based Routing

This document defines the policy and mechanisms for routing work to AI capabilities rather than specific vendor products. This evolution of Harness-Driven Development (HDD) ensures vendor independence and optimized resource allocation.

## Routing Principles

1. **Capability First:** The Supervisor identifies the *what* (capability required) before selecting the *who* (worker).
2. **Authority Least-Privilege:** Workers are selected based on the minimum authority level required for the task.
3. **Deterministic Selection:** Initial routing is based on a deterministic scoring model; future iterations may use learned optimization (IX).
4. **Human Final Authority:** Architecture and final sign-off remain human capabilities.

## Routing Logic

### 1. Capability Identification
The Supervisor (Demerzel) analyzes the incoming Issue or PR to determine the primary capability required:
- **Research/Documentation:** -> `research`
- **Code Change/Feature:** -> `implementation` (preceded by `repository_navigation`)
- **Review/Policy Check:** -> `adversarial_review`
- **Bug/Vulnerability:** -> `bug_hunting` or `security_review`

### 2. Worker Selection
Once a capability is identified, the Supervisor selects a worker from the `capability-registry.md` using the **Scoring Model**.

### 3. Fallback Policy
If the primary worker for a capability is:
- **Busy:** Select the next highest scoring available worker.
- **Unavailable:** Escalate to backup workers listed in the registry.
- **Too Expensive:** Re-route to a lower cost-tier worker if risk thresholds allow.
- **Low-Confidence:** If a worker's self-reported confidence or historical success is < 0.5, the Supervisor MUST request a second opinion from a different worker or escalate to a human.

## Scoring Model (Deterministic v1)

Workers are scored on a scale of 0.0 to 1.0 across several dimensions:

| Field | Weight | Description |
| :--- | :--- | :--- |
| `capability_fit` | 0.3 | How well the worker matches the required capability. |
| `historical_success`| 0.2 | Observed performance on similar tasks. |
| `availability` | 0.1 | Current load and responsiveness. |
| `cost_fit` | 0.1 | Alignment with the issue's budget tier. |
| `risk_fit` | 0.1 | Alignment with the task's risk level. |
| `repo_context_fit` | 0.1 | Prior experience with the specific repository. |
| `confidence` | 0.1 | Worker's self-assessed confidence for the specific task. |

**Formula:** `Score = Σ (Field * Weight)`

## Policy FAQs

### How are cost ceilings enforced?
- Each routing request must specify a budget tier (Free, Low, Standard, High).
- Workers with `cost_tier > budget_tier` are excluded unless a human override is provided.
- Local models (Ollama) are prioritized for "Free" tiers.

### How are collisions avoided?
- The Supervisor maintains a `state/active_workers.json` registry.
- Workers touching the same repository or overlapping file sets are serialized or assigned to separate worktrees.
- Lock files (`skills-lock.json`) prevent concurrent modification of governance artifacts.

### Which capabilities are read-only?
- `repository_navigation`, `adversarial_review`, and `security_review` are read-only by default. They generate observations, not commits.

### Which capabilities can open PRs?
- `implementation`, `research` (for docs), and `bug_hunting` (for narrow fixes) are permitted to open PRs, subject to the Harness Signature Layer.

### Which actions require human approval?
- Any change to the `constitutions/` or `policies/`.
- Deployments to production environments.
- Budget overrides for high-cost workers.
- High-risk implementations (Risk > Medium).

## Supervisor Implications

This routing model aligns with **Harness-Driven Development (#482)** by treating workers as interchangeable components of the harness. It also reinforces the **Adversarial Review Policy (#477)** by ensuring that the `Critic` capability is distinct from the `Builder` capability for any non-trivial change.

The Supervisor no longer "calls Claude"; it "requests Implementation" and handles the result according to the governance pipeline.
