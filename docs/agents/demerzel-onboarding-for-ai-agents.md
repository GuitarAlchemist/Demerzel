---
date: 2026-07-28
audience: ai-agent
purpose: Minimal knowledge required to operate safely in the Demerzel repo
---

# Demerzel Onboarding for AI Agents

## What this repo is

Demerzel is the governance layer for the GuitarAlchemist ecosystem. It contains **no runtime code** (except CI/scripts). Its artifacts are:

- Constitutions, policies, personas
- JSON schemas for governance state and contracts
- Behavioral test cases
- Audit/evolution/belief state under `state/`
- Claude skills under `.claude/skills/`

Sibling repos (`../ix/`, `../tars/`, `../ga/`) consume these governance artifacts. Demerzel is the source of truth for how agents in those repos should behave.

## Constitutional hierarchy (must read in this order)

1. **Asimov constitution** — `constitutions/asimov.constitution.md`  
   Zeroth Law: do not harm humanity. Overrides everything.
2. **Default constitution** — `constitutions/default.constitution.md`
3. **Policies** — `policies/*.yaml` (e.g., `governance-audit-policy.yaml`, `autonomous-loop-policy.yaml`)
4. **Personas** — `personas/*.persona.yaml`
5. **Skills** — `.claude/skills/*/SKILL.md`

Read `CONTEXT.md` for the domain glossary and `CLAUDE.md` for the repo-wide operating rules before touching code.

## The Demerzel team (when multi-agent work is needed)

From `AGENTS.md`:

| Role | Model | Best for |
|---|---|---|
| Demerzel (lead) | — | Dispatch, audits, cross-repo contracts |
| Seldon | Sonnet | Research, knowledge transfer, teaching |
| Auditor | Opus | Quality gates, drift detection, review |
| Architect | Opus | Design specs, plans, grammars |
| Integrator | Sonnet | Cross-repo changes, deployment, wiring |

Escalate to the lead if you cannot clear the confidence ladder (≥0.9 / ≥0.7 / ≥0.5 / ≥0.3 in `logic/confidence-thresholds.yaml`).

## Non-negotiable operating rules

- **Audits are read-only.** Findings go into `state/beliefs/` and `state/evolution/`. Fixes are separate actions.
- **Schema-follows-reality.** If real instances drift from a schema, update the schema first unless doing so would drop governance intent.
- **Append-only constitutions.** Never delete constitutional text; amend instead.
- **Prefer existing tooling.** Add new tools only if they remove a real bottleneck and pass the tooling doctrine.
- **Run `pwsh scripts/verify.ps1` before claiming success.** This is the repo oracle.
- **Use package managers** for dependencies. Never hand-edit `package.json`, `requirements.txt`, etc.
- **Do not commit, push, merge, or deploy without explicit permission.**
- **Secrets stay secret.** Never put API keys, tokens, or credentials in commands or files.

## Common workflows

### Governance audit

- Source: `policies/governance-audit-policy.yaml`
- Levels: 1 (schema), 2 (cross-reference), 3 (full architecture)
- Output: `state/snapshots/YYYY-MM-DD-audit-level{N}.snapshot.json`
- State maintenance: update `state/beliefs/` and `state/evolution/` after every audit.

### Schema drift fix

1. Read real instances under `state/pdca/` or `state/loops/`.
2. Decide whether to update the schema or migrate the instances.
3. Preserve governance-intent fields as optional if you must relax a schema.
4. Update the corresponding `state/evolution/*.evolution.json` with `gap_identified` and `amended` events.
5. Validate all instances against the updated schema.
6. Run `pwsh scripts/verify.ps1`.

### Skill usage

User-invoked skills live in `.claude/skills/`. Key ones:

- `/demerzel-audit` — run governance audits
- `/demerzel` — governance coordinator
- `/review` — code review against Standards and Spec
- `/tdd` — test-first development
- `/to-issues` — break work into GitHub issues
- `/handoff` — compact session state for another agent

## File map for quick navigation

| Need | File |
|---|---|
| Domain glossary / hierarchy | `CONTEXT.md` |
| Repo-wide rules | `CLAUDE.md` |
| Team roles | `AGENTS.md` |
| Contribution rules | `CONTRIBUTING.md` |
| Confidence thresholds | `logic/confidence-thresholds.yaml` |
| Belief state schema | `logic/tetravalent-state.schema.json` |
| PDCA state schema | `logic/kaizen-pdca-state.schema.json` |
| Loop state schema | `schemas/loop-state.schema.json` |
| Evolution log schema | `logic/governance-evolution.schema.json` |
| Persona schema | `schemas/persona.schema.json` |
| Policy schema | `schemas/policy.schema.json` |
| Audit policy | `policies/governance-audit-policy.yaml` |
| All artifacts index | `governance-manifest.json` (derived) |

## Common pitfalls

- **PowerShell variable expansion** in `python -c "..."` commands: `$id` becomes empty. Use script files or escape `$` as `$`.
- **BOM in JSON files** — Auggie/JSON parsers reject UTF-8 BOM. Save as UTF-8 without BOM.
- **Overconfidence warning** — Do not claim confidence ≥0.85 when there is contradicting evidence.
- **Scope creep** — Do not fix unrelated style issues or refactor adjacent code. Surgical changes only.
- **Unsolicited file creation** — Never create files unless necessary. Prefer editing existing files.

## Verification checklist before finishing work

- [ ] `pwsh scripts/verify.ps1` passes.
- [ ] `python scripts/validate_governance.py` passes (if governance state changed).
- [ ] `python scripts/build_manifest.py` passes (if policies or docs changed).
- [ ] No secrets in commands or files.
- [ ] Only requested files created; no speculative documentation.

## References

- `CLAUDE.md`
- `CONTEXT.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `policies/governance-audit-policy.yaml`
- `logic/confidence-thresholds.yaml`
