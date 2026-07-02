# AI/Human Delivery Ceremonies & Cadences

This document defines the ceremonies and cadence model for hybrid AI/human delivery within the GuitarAlchemist ecosystem, governed by Demerzel.

These ceremonies are designed to preserve the intent of Agile/XP practices while adapting to a workflow characterized by asynchronous agents, fan-out/fan-in parallel execution, GitHub-native work tracking, and the need to prevent human review bottlenecks.

**Core Philosophy:**
- **Asynchronous First:** Do not require meetings when an asynchronous GitHub artifact is sufficient.
- **Harness-Driven:** Agents operate within bounded scopes, and their work is verified via harnesses.
- **Human Authority:** AI agents do not approve their own work. Humans own intent, architecture, and merge decisions.

Related issues: #574 (Parent), #568 (Fan-out/Fan-in), #570 (Grooming), #547 (Mission Control).
Operating Doctrine context: [`docs/workflows/aiw-operating-doctrine.md`](../workflows/aiw-operating-doctrine.md)

---

## 1. Backlog Grooming for Agent-Ready Work
**Purpose:** Shape ambiguous requests into well-defined, "agent-ready" vertical slices. This aligns with the "Pocock lane" (shaping work before autonomy).
- **Inputs:** Vague user requests, unclassified issues, bug reports.
- **Participants / Workers:** Human Architect/Product Owner, AI Task Shaper (e.g., Navigator/Researcher).
- **Cadence:** Asynchronous, continuous; ideally evaluated daily or before Sprint Planning.
- **Outputs:** Shaped GitHub issues with explicit goals, non-goals, acceptance criteria, and a clear Definition of Ready (DoR).
- **Decision Owner:** Human Architect (validates issue shape).
- **GitHub Artifacts Updated:** Issues (labels updated e.g., `ready-for-agent`, descriptions finalized).
- **Stop Conditions:** Issue remains ambiguous, lacks acceptance criteria, or involves conflicting governance rules (U/C states).
- **Automated:** AI can draft issue descriptions, classify risk, and suggest architectural context.
- **Human Judgment:** Final approval of the issue scope, risk classification, and DoR before transitioning it to the "loop" (Cherny lane).

---

## 2. AI/Human Sprint Planning
**Purpose:** Align human capacity (for review/guidance) with AI capacity (for execution), defining the sprint scope to prevent overwhelming the "Fan-in Review" stage.
- **Inputs:** Agent-ready backlog, current human availability, token budget allocation, active Adaptive Fan-out Backpressure mode.
- **Participants / Workers:** Human Team (Architect, Reviewers), Seldon (Budget Router recommendations).
- **Cadence:** Weekly or bi-weekly asynchronous thread (via GitHub Discussions/Issues).
- **Outputs:** Committed sprint backlog, AI worker assignments, budget limits set for the iteration.
- **Decision Owner:** Human Lead/Architect.
- **GitHub Artifacts Updated:** Milestone/Project boards, Issue assignments, Issue milestones.
- **Stop Conditions:** Human review capacity is exceeded, Backpressure mode is DRAINING or HALTED.
- **Automated:** Seldon recommends assignments based on capability and cost; capacity forecasting.
- **Human Judgment:** Final commitment to sprint scope; prioritizing work based on strategic business value.

---

## 3. AFK Fan-Out Planning
**Purpose:** Use the Planner Execution Graph to safely spawn parallel AI tasks, ensuring dependencies are respected before wide execution begins.
- **Inputs:** Selected shaped issues, Execution Graph constraints (`depends_on`, `blocks`).
- **Participants / Workers:** Supervisor Agent (Orchestrator), AI Builders/Researchers.
- **Cadence:** Per-issue/epic, triggered when an agent-ready issue moves to execution.
- **Outputs:** Spawned sub-tasks, branched worktrees, initialized AI agent loops.
- **Decision Owner:** Demerzel / Supervisor Agent (bounded by policy).
- **GitHub Artifacts Updated:** Child issues linked to parents, branch creation, draft PRs opened.
- **Stop Conditions:** Missing dependencies in the Execution Graph; budget ceiling reached; "HALT-ALL" marker detected.
- **Automated:** Dependency resolution, branch creation, initial prompt dispatch to workers.
- **Human Judgment:** Only required if the Planner cannot resolve a safe fan-out graph, or if risk escalates.

---

## 4. Fan-In Review Ceremony
**Purpose:** Consolidate asynchronous AI work, enforce Harness-Driven Development (HDD) checks, and secure human authorization before merging.
- **Inputs:** Draft PRs, completed test logs, AI Critic adversarial review findings, Harness Verification artifacts.
- **Participants / Workers:** Human Reviewer(s), AI Critic (Adversarial Reviewer), CI/CD pipelines.
- **Cadence:** Continuous, asynchronous, triggered by PR readiness (Draft to Open transition).
- **Outputs:** Approved and merged PR, or requested changes.
- **Decision Owner:** Human Reviewer.
- **GitHub Artifacts Updated:** PR comments, PR status (Approved/Changes Requested/Merged).
- **Stop Conditions:** Failed tests, missing evidence refs, Asimov policy violation detected, unresolved AI Critic concerns.
- **Automated:** CI tests, AI Critic initial adversarial pass, schema validations, conversation hygiene checks.
- **Human Judgment:** Assessing code quality, architectural alignment, addressing subjective UX or edge-case business logic. *Agents never approve their own work.*

---

## 5. Async Daily / Mission Control Snapshot
**Purpose:** Provide a unified view of system health, AI agent status, token budgets, and bottleneck indicators across the ecosystem.
- **Inputs:** Streeling event streams, Seldon KPI metrics, active PR queues, current Backpressure state.
- **Participants / Workers:** Seldon (Data aggregation), Human Team (Consumers).
- **Cadence:** Daily (automated generation).
- **Outputs:** A generated Mission Control report (e.g., `docs/status/mission-control.json` or dashboard update).
- **Decision Owner:** Seldon (Generator), Human Team (Acts on data).
- **GitHub Artifacts Updated:** Status pages, automated daily discussion thread or issue comment.
- **Stop Conditions:** (None, this is a passive observability ceremony).
- **Automated:** Aggregation of metrics, generation of the snapshot, updating status dashboards.
- **Human Judgment:** Deciding to adjust fan-out backpressure, reallocate budgets, or intervene in stuck PRs based on the report.

---

## 6. Agent Work Demo / PR Walkthrough
**Purpose:** Allow the AI agent to explain complex changes autonomously, making human review faster and reducing cognitive load.
- **Inputs:** Merged or complex PRs, Execution Graph history, AI worker logs.
- **Participants / Workers:** AI Builder/Researcher, Human Reviewers/Stakeholders.
- **Cadence:** As needed, usually for Epics or large architectural changes.
- **Outputs:** A recorded summary (text, generated diagrams, or scripted automated walkthroughs) explaining "why" decisions were made.
- **Decision Owner:** Human Reviewer (consumes and acknowledges).
- **GitHub Artifacts Updated:** PR description updates, specific "Walkthrough" comments on PRs.
- **Stop Conditions:** PR is too small to warrant a walkthrough (enforced by size thresholds).
- **Automated:** Generation of the summary, extraction of key architectural decisions from logs.
- **Human Judgment:** Evaluating whether the agent's explanation aligns with the original intent.

---

## 7. AI Retro / Learning Loop
**Purpose:** Analyze completed work and failures to refine prompts, update schemas, adjust policy weights, and improve the Demerzel governance framework.
- **Inputs:** Completed sprint data, PR rejection reasons, Streeling history, Seldon KPI deviations.
- **Participants / Workers:** Seldon (Analysis), Human Architect, AI Researcher.
- **Cadence:** End of sprint (Bi-weekly) or triggered after a major incident.
- **Outputs:** Updated system prompts, modified governance schemas, new test fixtures, adjusted capability scoring.
- **Decision Owner:** Human Architect.
- **GitHub Artifacts Updated:** PRs modifying `docs/governance/`, `schemas/`, or `policies/`.
- **Stop Conditions:** No actionable insights found.
- **Automated:** Seldon identifies patterns of failure (e.g., "Agent X fails 40% of PRs in area Y") and suggests prompt or schema updates.
- **Human Judgment:** Approving systemic changes to governance or routing policies.

---

## 8. Emergency Halt / Resume Ceremony
**Purpose:** Provide an immediate, system-wide stop to all autonomous execution when safety, budget, or architectural integrity is threatened.
- **Inputs:** Critical alert, budget overrun, severe policy violation, manual human trigger.
- **Participants / Workers:** Demerzel Policy Engine, Human Administrator.
- **Cadence:** Ad-hoc, emergency only.
- **Outputs:** System in HALTED state (`~/.demerzel/HALT-ALL` marker active), active loops terminated safely.
- **Decision Owner:** Human Administrator (for manual trigger and resume), Demerzel (for automated trigger based on thresholds).
- **GitHub Artifacts Updated:** Global status flag, issue creation for the incident.
- **Stop Conditions:** (This ceremony *is* a stop condition).
- **Automated:** Demerzel detecting a threshold breach and executing `demerzel_halt.py`.
- **Human Judgment:** Investigating the root cause, resolving the issue, and manually clearing the HALT marker to resume operations.
