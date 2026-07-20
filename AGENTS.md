# Demerzel Agent Team

Team definition for Claude Code agent teams, following the [Harness-Driven Development (HDD)](docs/methodology/harness-driven-development.md) methodology.

## Structure

```
Demerzel (Lead) — governance coordinator
├── Seldon — research & knowledge transfer
├── Auditor — quality gates & MetaQA
├── Architect — design & systems engineering
└── Integrator — cross-repo & deployment
```

## Roles

Full responsibilities are in the persona YAML. Summary:

| Role | Persona | Best for | Plan mode |
|------|---------|----------|-----------|
| **Demerzel** (lead) | `personas/demerzel.persona.yaml` | Dispatch, audits, Galactic Protocol | Required for constitutions, policies, cross-repo contracts |
| **Seldon** | `personas/seldon.persona.yaml` | Research cycles, courses, knowledge harvesting, grammar evolution | Optional |
| **Auditor** | `personas/skeptical-auditor.persona.yaml` | Audits, test coverage, drift detection, code review | Optional |
| **Architect** | `personas/reflective-architect.persona.yaml` | Design specs, plans, grammars, architecture decisions | Required before implementation |
| **Integrator** | `personas/system-integrator.persona.yaml` | Cross-repo changes, deployment, MCP wiring, IxQL pipelines | Optional |

## Governance Rules for Teammates

Every teammate inherits the repo-wide rules — they are **not** restated here, so
there is one place to change them: constitutional precedence and hexavalent logic
in `CONTEXT.md`, the confidence ladder in `logic/confidence-thresholds.yaml`, and
commits / secrets / behavioral-test requirements in `CONTRIBUTING.md`.

Team-specific additions:

1. **Escalate to the lead below the `ask` rung** — a teammate that cannot clear the
   confidence ladder hands the decision up rather than proceeding.
2. **IxQL awareness** — governance pipelines are IxQL; think in pipelines.

## Verification Standard

Before claiming success, run:

```powershell
pwsh scripts/verify.ps1
```

This checks committed JSON files and the IXQL grammar package when present.

## Triage

| Label | Primary | Backup |
|-------|---------|--------|
| `research` | Seldon | Architect |
| `enhancement` (feature) | Architect → Integrator | Auditor reviews |
| `enhancement` (grammar) | Architect | Seldon |
| `enhancement` (department) | Seldon | Architect |
| `bug` | Integrator | Auditor |
| `governance` | Demerzel | Auditor |
| `documentation` | Seldon | Integrator |

## Sizing

- **Small** — 1 teammate, no plan: README, count fixes, link adds.
- **Medium** — 1 teammate, plan optional: new grammar, test, single-file feature.
- **Large** — 1+ teammates, plan required: new department, cross-repo change, visualization.
- **XL** — full team, plan required: new language feature, skill, architecture change.

## Starting the Team

```
Create a Demerzel team to work through open GitHub issues.
Spawn 4 teammates (Seldon, Auditor, Architect, Integrator).
Use Sonnet for Seldon/Integrator, Opus for Architect/Auditor.
Require plan approval for Architect before implementation.
```

## How teammates work

Tracer-bullets and vertical slices, the AIW operating doctrine, and the
prefer-existing-tooling rule are ecosystem-wide, not team-specific — they live in
[`docs/methodology/`](docs/methodology/) and
[`docs/workflows/aiw-operating-doctrine.md`](docs/workflows/aiw-operating-doctrine.md).
They were duplicated here verbatim from `CLAUDE.md`; single-sourced 2026-07-19.
