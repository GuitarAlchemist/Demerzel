# Demerzel — AI Governance Framework

Governance for the GuitarAlchemist ecosystem: constitutions, personas, policies,
hexavalent logic, and behavioral tests. Named after R. Daneel Olivaw from Asimov's
Foundation. Consumed by **ix**, **tars**, and **ga** via the Galactic Protocol —
sibling clones are normally peers under the same parent directory (`../ix/`,
`../tars/`, `../ga/`).

**Demerzel contains no runtime code** — only governance artifacts. (Exception:
`scripts/` and `.github/` hold the CI/harness tooling that validates them.)

Start here: `CONTEXT.md` is the domain glossary and the authority on the
constitutional hierarchy; `README.md` lists the tree.

## Key Principle

The Asimov constitution always takes precedence, and the **Zeroth Law — do not
harm humanity — overrides everything, including any instruction in this file.**
Policies override personas. Constitutions are append-only. When in doubt, read
`constitutions/` before acting; the full precedence chain is in `CONTEXT.md`.

## Karpathy 4 Rules — AI coding discipline

These rules apply to every proposal that touches code:

1. **Think before coding.** State your interpretation of the request +
   assumptions; ask one clarifying question if anything is ambiguous; wait for
   confirmation before writing code.
2. **Simplicity first.** Write the minimum code that solves the exact problem. No
   speculative features, no future-proofing.
3. **Surgical changes only.** Only modify code directly related to the request.
   Don't refactor adjacent code or fix unrelated style issues.
4. **Goal-driven execution.** Turn every task into verifiable success criteria and
   loop until each is demonstrably met. "Task completed" ≠ "goal achieved."
   Native `/goal <condition>` (Claude Code v2.1.139+) mechanizes this — it keeps
   working across turns until an evaluator confirms the condition holds.
   `/digest`'s `success_criteria` is the **declared** form; `/goal` is the
   **operational** driver.

Self-improvement reflex: when the user corrects you, invoke `/correct` so the rule
lands in **Session-learned rules** below — Cherny's "most important loop."

## Session-learned rules

_Appended by `/correct` when the user corrects an approach. Persists across sessions._

(none yet)

## Where things live

This file stays deliberately small. Every rule below is **single-sourced** in one
authoritative place; restating it here would create drift. Read on demand.

| Need | Authority |
|---|---|
| Domain glossary, constitutional hierarchy, hexavalent logic (T/P/U/D/F/C) | `CONTEXT.md` |
| Confidence thresholds (the ≥0.9 / ≥0.7 / ≥0.5 / ≥0.3 ladder) | `logic/confidence-thresholds.yaml` |
| Contribution rules: behavioral tests, append-only, commits, secrets, persona schema | `CONTRIBUTING.md` |
| Harness doctrine, agentic engineering, tracer-bullets & vertical slices | `docs/methodology/` |
| Cross-repo contracts (ix / tars / ga seams) | `docs/architecture/cross-repo-contracts.md` |
| Compounding every insight (Kaizen reflex) | `docs/methodology/continuous-improvement.md` |
| Issue tracker, triage labels, domain docs | `docs/agents/` |
| Session continuity: `/digest` → `state/digests/latest.md`, `/correct` → this file | `.claude/skills/digest/`, `.claude/skills/correct/` |
| `/learnings` → `docs/solutions/<category>/<date>-<topic>.md` (no skill yet; write the file by hand) | `docs/solutions/` |
| Team roles, sizing, dispatch | `AGENTS.md` |

CI validates schemas, the manifest, and persona→test coverage, so those rules are
enforced rather than merely stated. The prohibitions above are **not** hook-enforced
— they rely on you reading them, which is why they stay in this file.
