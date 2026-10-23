---
review_agents: [code-simplicity-reviewer, security-sentinel, performance-oracle, architecture-strategist]
plan_review_agents: [code-simplicity-reviewer]
---

# Review Context

Add project-specific review instructions here.
These notes are passed to all review agents during /workflows:review and /workflows:work.

- Demerzel contains NO runtime application code — only governance artifacts (personas, constitutions, policies, schemas, contracts, tests) plus operational Python emitters in `scripts/` (stdlib-first, unittest). Flag any PR that adds runtime application code.
- Constitutions are append-only; removals need explicit justification. Schemas follow reality — enum extensions require evidence of actual usage.
- Every persona change needs a matching behavioral test in `tests/behavioral/`.
- Watch for verification theater: checks that always pass by vacuity (empty diff ranges, gates on absent inputs) are worse than no checks.
- New artifacts need a consumer — flag artifact types with no emitter or reader (LOLLI trap).
- `.github/` and `schemas/` are blocked paths: risk-report fails closed on PRs touching them (human merge review by design).
