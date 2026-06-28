# Harness-Driven Development (HDD)

Version: 1.0.0
Status: Active
Parent: #475
Related: #477, #479, GuitarAlchemist/.github#7, GuitarAlchemist/tars#101, GuitarAlchemist/ga#486

## Vision

**Harness-Driven Development (HDD)** is an engineering methodology where a deterministic Harness/Supervisor orchestrates specialized AI agents while humans retain responsibility for architecture, product vision, and governance.

The objective is not to replace software engineers. The objective is to elevate the human engineer from primary implementer to architect, reviewer, and system designer.

> *Motto: Build the system that builds the software, instead of building the software directly.*

## Core Principles

### 1. GitHub is the work system
GitHub is the source of truth for planning and delivery.
- **Issues** are planning units.
- **Pull requests** are delivery units.
- **Labels** encode governance and routing policy (see [Triage Labels](../agents/triage-labels.md)).
- **GitHub Actions** provide deterministic verification.
- **Comments** are part of the control loop.

### 2. Agents are specialized
Agents are routed according to observed strengths, not treated as interchangeable chatbots.
- **Claude**: implementation, refactoring, tests, workflows.
- **Jules**: research, documentation, governance, ADRs, schemas.
- **Codex or other reviewers**: adversarial review, narrow bug finding, policy checks.
- **Local models**: cheap/free retrieval, summarization, dry-run analysis, lightweight classification.

### 3. The Harness is the control plane
The Harness (Supervisor) orchestrates the flow of work:
- Observes GitHub activity and classifies issues/PRs.
- Routes tasks to the best available agent.
- Manages agent concurrency to avoid collisions.
- Requests self-review and adversarial review.
- Monitors CI and risk reports.
- Escalates only genuine blockers or strategic architecture decisions to humans.
- Records outcomes for future routing optimization.

### 4. Adversarial review by default
Quality is maintained through multi-layered review tiers, ensuring no non-trivial PR is judged only by its author.
- **Deterministic checks**: CI, build, tests, lint, docs health, risk report.
- **Author self-review**: The authoring agent checks scope, acceptance criteria, and regressions.
- **Cross-agent/adversarial review**: A different agent reviews from a skeptical perspective (see [Review Independence](../review-independence.md)).
- **Tribunal**: High-risk changes require multiple reviewers or explicit human review.
- **Human architecture review**: Final authority remains with the human for strategic decisions.

### 5. Policies are explicit
Governance rules live in versioned repository artifacts, not hidden in chat history or model weights.
- [Constitutions](../../constitutions/asimov.constitution.md) and [Governance Model](../governance-model.md).
- [Issue templates](../../.github/ISSUE_TEMPLATE/feature_request.md) and `issue_meta` schemas.
- Label taxonomy and routing policies.
- Cost budgets and permission boundaries.
- Kill-switch / [Halt policy](../../scripts/demerzel_halt.py).

### 6. Deterministic before AI
Prefer deterministic mechanisms (scripts, schema validation, static routing) when they are sufficient. LLMs should be invoked only when judgment, synthesis, or adversarial reasoning adds value.

### 7. The system learns
The Harness records outcomes to improve routing based on evidence:
- Cycle time and merge rate.
- Review iterations and defects found.
- CI failure rates and cost.
- Task type vs. agent success profiles.

## Roles

### Human
- **Vision & Architecture**: Defines the "what" and the "why".
- **Product Direction**: Sets priorities and strategic goals.
- **Final Approval**: Retains authority for strategic changes and exception handling.

### Supervisor / Harness
- **Orchestration**: Scheduling, routing, and collision avoidance.
- **Governance**: Enforcement of policies and quality gates.
- **Ops**: Cost awareness, escalation, and metrics collection.

### Agents
- **Execution**: Specialized implementation and evidence production.
- **Self-Review**: Initial validation of own work.
- **Collaboration**: Communicating through GitHub artifacts.

## Roadmap

### Phase 1 — GitHub Governance (Current)
- Shared issue templates and label taxonomy.
- `issue_meta` schema implementation.
- Manual orchestration via GitHub comments and labels.

### Phase 2 — Deterministic Supervisor
- GitHub watcher and issue classifier.
- Automated agent routing and PR status monitoring.
- Adversarial review automation and escalation rules.

### Phase 3 — IX-assisted Routing
- Outcome tracking and agent performance profiles.
- Learned routing suggestions and confidence calibration.

### Phase 4 — Self-improving Engineering Organization
- Supervisor opens improvement issues.
- Agents implement tracer bullets; adversarial review validates.
- Human retains architectural authority.

## Adoption & Ecosystem Scope

This methodology applies to all repositories in the Guitar Alchemist ecosystem:
- **GA**: Primary implementation and user-facing features.
- **TARS**: Theory validator and core logic.
- **IX**: ML, routing, and learning systems.
- **Demerzel**: Governance, policy, and orchestration specs.
- **Hari**: Research and specialized knowledge.

### Cost Notes
HDD bootstrap is designed to be **free/local by default**. Paid model calls (e.g., Claude 3.5 Sonnet, GPT-4) are only justified for high-complexity implementation or final adversarial reviews where local or cheaper models (e.g., Llama 3, Gemini Flash) lack the required reasoning depth.

## Alignment

- **Adversarial Review**: Aligns with [Demerzel #477](../review-independence.md) requirements for producer-reviewer split and cross-vendor review.
- **GitHub Governance**: Aligns with [.github#7](https://github.com/GuitarAlchemist/.github/issues/7) regarding standardized templates, labels, and metadata.
