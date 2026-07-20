# Harness-Driven Development (HDD)

**Status:** Reference Engineering Methodology
**Scope:** Guitar Alchemist Ecosystem (GA, TARS, IX, Demerzel, Hari)

> "Build the system that builds the software, instead of building the software directly."

## Vision

Harness-Driven Development (HDD) is an engineering methodology where a deterministic Harness/Supervisor orchestrates specialized AI agents while humans retain responsibility for architecture, product vision, and governance.

The objective is not to replace software engineers. The objective is to elevate the human engineer from primary implementer to architect, reviewer, and system designer. HDD treats the environment, validation mechanisms, and orchestration routing (the "harness") as the primary software artifacts, while specific functional code is increasingly written by specialized models reacting to that harness.

## Core Principles

### 1. GitHub is the Work System

The source of truth and control plane interface is GitHub.
- **Issues** are the primary planning units.
- **Pull Requests** are the delivery units.
- **Labels** encode governance, routing policy, and task state.
- **GitHub Actions** provide deterministic verification.
- **Comments** are part of the control loop (commands, clarifications, agent discussions).

### 2. Agents are Specialized

Agents are not interchangeable chatbots; they should be routed according to observed strengths and tailored capabilities.
Initial routing model examples:
- **Claude:** Implementation, refactoring, tests, complex workflows.
- **Jules:** Research, documentation, governance, ADRs, schema design.
- **Codex / Skeptical Reviewers:** Adversarial review, narrow bug finding, policy adherence checks.
- **Local Models:** Cheap/free retrieval, summarization, dry-run analysis, lightweight classification.

### 3. The Harness is the Control Plane

The Harness (or Supervisor) acts as the deterministic coordinator. It should:
- Observe GitHub activity.
- Classify issues and PRs (e.g., via `issue_meta`).
- Route tasks to the best available agent.
- Keep agents busy without causing file/path collisions.
- Request self-review and adversarial review.
- Monitor CI, risk reports, and budget consumption.
- Escalate only genuine blockers, ambiguity, or architecture decisions.
- Record outcomes for future routing improvements.

### 4. Adversarial Review by Default

No non-trivial pull request should be judged solely by the authoring agent.
*Explicitly aligns with Demerzel #477 (Adversarial Review).*

**Review Tiers:**
1. **Deterministic Checks:** CI, build, tests, lint, docs health, risk report.
2. **Author Self-Review:** The authoring agent checks against scope, acceptance criteria, and obvious regressions.
3. **Cross-Agent/Adversarial Review:** A different agent reviews from a skeptical perspective.
4. **Tribunal:** Governance, security, schema, architecture, or high-risk changes require multiple reviewers or explicit human review.
5. **Human Architecture Review:** Final authority remains with the human for strategic decisions.

### 5. Policies are Explicit

Important rules must live in versioned repository artifacts, not only in chat history.
Examples include:
- Issue templates
- Label taxonomy
- `issue_meta` schemas (*Aligns with `.github#7`*)
- Routing policy
- Review tiers
- Cost budgets
- Permission boundaries
- Merge policy
- Kill-switch / halt policy

### 6. Deterministic Before AI

Prefer deterministic mechanisms when they are sufficient. LLMs should only be invoked when judgment, synthesis, translation, or adversarial reasoning adds value.

**Why deterministic mechanisms precede LLM calls:**
- They are 100% reliable and do not hallucinate.
- They execute magnitudes faster.
- They incur negligible cost.
- Examples: scripts, schema validation, GitHub Actions, static routing rules, diff classifiers, dry-run reports.

### 7. The System Learns

The Harness should record outcomes and gradually improve routing based on observed evidence:
- Cycle time
- Merge rate
- Number of review iterations
- Defects found by each reviewer
- CI failure rate
- Scope creep frequency
- Cost per task
- Confidence calibration
- Task type vs agent success

IX can later utilize these metrics to replace hard-coded routing rules with learned, dynamic routing decisions.

---

## Roles

### Human
- **Vision:** Sets the North Star for the ecosystem.
- **Architecture:** Defines system boundaries, core schemas, and interfaces.
- **Product Direction:** Determines *what* gets built and prioritizes the backlog.
- **Final Approval:** Retains authority for strategic changes and architectural shifts.
- **Exception Handling:** Resolves deadlocks when agents disagree or escalate ambiguity.

### Supervisor / Harness
- **Scheduling & Routing:** Matches tasks to appropriate agent capabilities.
- **Governance Enforcement:** Ensures policies and templates are respected.
- **Quality Gates:** Triggers CI, linters, and adversarial reviews.
- **Cost Awareness:** Monitors execution budgets to prevent runway burn.
- **Collision Avoidance:** Manages concurrency to avoid merge conflicts.
- **Escalation & Metrics:** Collects telemetry and escalates unresolvable states.

### Agents
- **Specialized Execution:** Writes code, documentation, or tests based on specific personas (Builder, Researcher, Bug Hunter, etc.).
- **Self-Review:** Validates their own work before requesting review.
- **Evidence Production:** Generates logs, traces, and reasoning artifacts.
- **Collaboration:** Communicates through GitHub artifacts (PRs, issues, comments).

---

## Ecosystem Adoption Terminology

How the Guitar Alchemist ecosystem adopts the HDD methodology:

- **Demerzel:** The *Governance Core*. Owns the policies, schemas (e.g. `issue_meta`), role definitions, and adversarial review standards.
- **IX:** The *Optimization Engine*. Observes the harness telemetry and builds machine learning models to transition static routing to learned, probabilistic routing over time.
- **TARS:** The *Validation Substrate*. Enforces deterministic theory validation and strict type constraints before AI review is even requested.
- **Hari:** The *Forecaster*. Anticipates dependency, capacity, and architectural constraints based on the Harness's recorded throughput.
- **GA (Guitar Alchemist):** The *Application Target*. The .NET ecosystem where the methodology is applied in practice to build the actual end-user product.

---

## Roadmap

### Phase 1 — GitHub Governance
- Shared issue templates.
- Label taxonomy.
- `issue_meta` schema definition.
- Research and governance documentation (this document).
- Manual orchestration through GitHub comments.

### Phase 2 — Deterministic Supervisor
- GitHub watcher integration.
- Issue classifier implementation.
- Agent router logic.
- PR status monitor.
- Automated adversarial review requester.
- Basic escalation rules.

### Phase 3 — IX-Assisted Routing
- Outcome and metric tracking.
- Agent performance profiling.
- Learned routing suggestions based on historical success.
- Confidence calibration for automated tasks.

### Phase 4 — Self-Improving Engineering Organization
- Supervisor autonomously opens improvement issues based on systemic failures.
- Agents implement tracer bullets for architectural exploration.
- Robust adversarial review completely validates changes.
- Human retains ultimate architectural authority.

---

## Cost Notes

HDD is designed to be **free/local by default** during bootstrapping and routine operations:
- The Harness relies on deterministic (free) logic whenever possible.
- Local models are preferred for cheap tasks like lightweight classification, retrieval, or dry-runs.
- Paid LLM calls (e.g., Claude, Opus, Gemini) are only utilized when deep judgment, complex reasoning, implementation, or high-tier adversarial review justifies the expense.

---

## Tracer Bullets and Vertical Slices

Adopted ecosystem-wide from aihero.dev (2026-06-14). Counters AI's "build the
whole thing at once" failure mode. Restored to this file 2026-07-19, when
`CLAUDE.md` was decomposed and pointed here.

- **Tracer-bullet first.** For any non-trivial feature, build the smallest
  **end-to-end** slice that touches *every* layer, test it, get feedback, then
  expand — never build layers in isolation. Context-window constraints make the
  discipline non-negotiable.
- **Vertical, not horizontal, decomposition.** Each task or PR is a thin slice
  cutting through all integration layers, surfacing unknowns early, rather than a
  horizontal layer completed across the whole system.

This is the same instinct as §6 *Deterministic Before AI* applied to scope: prove
the seam works before investing in either side of it.

## Harness Doctrine (Pocock delta, 2026-06-22)

Reconciles with the Karpathy 4 Rules and the Cherny session-continuity patterns —
**agree = keep, diverge = adjust**.

- **Harness ≈ model (50/50), stay agent-agnostic.** Optimize the harness (prompts,
  skills, codebase, sandbox) as much as the model, and don't over-fit to one model.
  A codebase that is *easy to change* lets a *cheaper* model do the same work.
  Optimize **AX (Agent Experience)** the way you optimize DX.
- **Queue, not loop.** A backlog of scoped tasks with human checkpoints pushed as
  far right as safe beats an infinite loop. Our queue is `BACKLOG.md` plus
  `demerzel-driver-triggers.yml` → `state/triggers/*.trigger.json`.
- **Procedures over abilities.** Skills the user invokes ("procedures") keep their
  descriptions out of the context window; model-invoked "abilities" leak a
  description each. Prefer procedures. *(Tension with superpowers' model-in-control
  stance — documented rather than resolved.)*
- **Delete → observe → layer back.** Periodically strip skills/MCP/instructions to
  a blank slate, watch the bare agent, then re-add only what you choose.
  `demerzel-context-budget` is the tool for this.
- **Review the system, not just the code.** If someone keeps stealing your bike,
  buy a lock. Reinforces the `metafix` + ml-feedback loop.
- **Strategic > tactical (Ousterhout).** AI ate tactical programming; be the
  strategic delegator. Converges with Karpathy R1 and R4.
