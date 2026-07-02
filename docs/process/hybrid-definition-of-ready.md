# Hybrid Definition of Ready (DoR)

Related: #576, #570, #461

## Purpose

The Hybrid Definition of Ready defines the criteria a candidate issue must meet before it is delegated to an AI worker or assigned to a human for delivery. The goal is to make issue readiness explicit enough that agents can work safely and humans can review efficiently.

A well-defined issue bounds the problem space, ensures safe execution, and limits context bloat, aligning with the [Harness-Driven Development](../methodology/harness-driven-development.md) methodology and Asimov constitutional priorities.

## Criteria for Readiness

A candidate issue should not be delegated (especially to an autonomous agent) until it provides sufficient detail across the following dimensions:

1. **Clear task goal:** What is the precise, achievable objective of the work?
2. **Context and source links:** Pointers to relevant `CONTEXT.md` sections, architectural decisions (`docs/adr/`), or related PRs.
3. **Allowed paths or likely path families:** Explicit restrictions on which directories or files may be modified (e.g., `docs/process/`, `scripts/`).
4. **Non-goals:** Explicit declarations of what *should not* be done (e.g., "no broad refactoring", "no policy changes").
5. **Expected output artifacts:** What tangible deliverables will be produced (e.g., a markdown file, an IxQL pipeline, a JSON schema)?
6. **Test or validation plan:** How will we know the change is correct? (e.g., `python scripts/validate_governance.py`).
7. **Stop conditions:** When should an agent halt and escalate? (e.g., "stop if tests fail repeatedly", "stop if budget exceeds $1").
8. **Risk tier:** Is this low risk (docs), medium risk (code), or high risk (policy/architecture)?
9. **Dependency links:** What other issues block this or are blocked by this?
10. **Suggested worker/capability:** Which persona or agent capability is best suited? (e.g., `worker:jules`, `worker:claude`, `routing:architecture`).
11. **Acceptance criteria:** Bulleted list of conditions that must be true to close the issue.
12. **Reviewer expectations:** Who needs to review this, and what specific feedback are they looking for?

## Work Type Distinctions

The rigor of the DoR scales with the type of work and its associated risk:

* **Docs:** Low risk. Focus on clear goals and allowed paths. Do not let missing polish or heavyweight ceremony stop clearly safe documentation work.
* **Code:** Medium risk. Demands rigorous test/validation commands, strict path bounds, and defined stop conditions.
* **Workflow / CI:** Medium-High risk. Requires sandbox isolation considerations and explicit rollback plans.
* **Architecture:** High risk. Should prefer outputting docs, schemas, examples, and tests. Requires an Architect (human or high-confidence AI) review.
* **Policy / Governance:** Critical risk. Changes to constitutions, rules, or core policies. Cannot be auto-merged. Must preserve Asimov priorities and requires explicit human/Demerzel tribunal approval.

## Relation to Grooming Gate (#570)

The DoR acts as the checklist for the issue grooming gate (#570). The grooming gate process evaluates incoming requests and issues against this definition. Only when an issue satisfies the DoR is it labeled `ready-for-agent` (or `ready-for-human`) and moved into the active execution pipeline.

## Relation to Prompt and Harness Discipline (#461)

The elements defined in this DoR feed directly into the AIW Prompt and Harness Engineering discipline (#461).
* The **allowed paths** and **non-goals** configure the bounds of the agent's workspace.
* The **test or validation plan** forms the verification step inside the harness loop.
* The **stop conditions** dictate when the harness should terminate execution and escalate.
An issue that fails the DoR cannot be safely wrapped in a task harness.

## Exceptions

Do not require every small issue to have heavyweight ceremony. Simple typos or trivial isolated fixes can use a summarized version of these criteria, provided the risk remains unambiguously low. This definition is not meant to block urgent human decisions.
