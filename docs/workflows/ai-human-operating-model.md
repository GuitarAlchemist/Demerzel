# AI/Human Agile-XP Operating Model

This document defines the operating model for hybrid AI/human delivery in Demerzel and the GuitarAlchemist ecosystem. It adapts Agile, XP, and agentic engineering practices to a system where humans own intent, architecture, review, and merge decisions, while AI workers perform bounded research, drafting, implementation, and review tasks.

Related: #573 (epic root), #568 (batch controller), #570 (grooming gate), #547 (mission control), #529.

## Operating Model Vision

The delivery pipeline operates through a series of explicit gates and bounded loops to prevent noise and ensure quality.

```text
Backlog
  -> Issue Grooming Gate (#570)          [Human + AI shaping]
  -> AI/Human Planning                   [Human defines architecture/boundaries]
  -> Fan-out Batch Controller (#568)     [Automated delegation & dispatch]
  -> Agent Work                          [AI implementation / Pocock/Cherny loops]
  -> Fan-in Review Queue                 [Asynchronous queueing]
  -> Human Merge / Override              [Human gatekeeper & Demerzel audit]
  -> Retro / Learning Loop               [System improvement]
  -> Updated prompts, policies, labels, and workflows
```

## Human Authority vs. Agent Autonomy

To ensure Asimov compliance and risk control, boundaries must be explicit:

- **Human Authority:** Owns product intent, architectural design, review of output, and final merge decisions. Humans define the policies and grammars that constrain the agents.
- **Agent Autonomy:** Owns bounded drafting, research, and test-driven implementation. AI workers act within explicitly defined scopes (e.g., via the Fan-out Batch Controller #568) and must adhere to the Karpathy/Pocock/Cherny lanes (see `docs/workflows/aiw-operating-doctrine.md`).
- **No Automatic Merge:** AI workers cannot merge their own PRs.
- **Independent Verification:** AI workers are not trusted reviewers of their own work. Review requires cross-model verification or human approval.

## Hybrid Ceremonies and Cadences

Agile/XP ceremonies are adapted for an asynchronous, multi-agent environment:

1. **Async Daily / Mission Control (#547):** A centralized dashboard/queue where humans review the current state of fan-out operations, blocked agents, and PRs awaiting review, replacing a synchronous daily standup.
2. **Issue Grooming (#570):** A continuous gate where issues are shaped into "Definition of Ready" before being delegated.
3. **AI/Human Planning:** Short, strategic sessions (often just a documented plan in the PR or issue) where the human defines the *what* and the *boundaries*, leaving the tactical *how* to the AI.
4. **Retro / Learning Loop:** Post-merge or post-sprint reflection. The outputs of these retrospectives strictly feed into compounding improvements for prompts, policies, labels, and workflows (the "harness").

## Hybrid Definition of Ready (DoR) and Definition of Done (DoD)

### Definition of Ready (DoR)
Before an issue passes the Grooming Gate (#570) and enters the Fan-out controller (#568), it must:
- Have a clear, bounded scope (no "refactor the world" tasks).
- Explicitly define non-goals.
- Provide testable acceptance criteria.
- Specify allowed file paths and constraints.
- Fit within the current budget cap for the assigned routing tier.

### Definition of Done (DoD)
Before a PR is approved by a human for merge, it must:
- Meet all acceptance criteria.
- Pass all automated tests and Demerzel governance checks.
- Include validation/evidence of correct behavior (e.g., screenshots, command outputs).
- Contain risk notes, if applicable.
- Demonstrate no unauthorized modifications to external architecture or secrets.

## XP Adaptation for Agent Workers

Extreme Programming (XP) practices translate to agentic operations as follows:
- **Test-Driven Development (TDD):** Agents should be prompted to write or run tests first. The harness must provide easy commands to execute tests locally (e.g., `npm test`, `pytest`).
- **Small Releases / Small Slices:** Tasks are broken down into vertical, fully integrated slices rather than broad horizontal layers (the Tracer-bullet approach).
- **Continuous Integration:** Agent PRs trigger CI pipelines that automatically enforce formatting, static analysis, and Demerzel hexavalent logic validations.
- **Pair Programming:** Replaced by cross-model review and human-in-the-loop (HITL) architecture pairing during the planning phase.

## Child Epics & Follow-ups

This framework requires continuous refinement. Child epics to be tracked include:
1. Formalize AI/Human ceremonies and cadences.
2. Refine the Hybrid DoR and DoD implementation.
3. Standardize XP practices (e.g., agent TDD harnesses).
4. Establish explicit working agreements and boundary enforcement.
5. Build the Async Daily / Mission Control dashboard (#547).
6. Automate the Retro/Learning Loop to feed prompt/policy updates.
