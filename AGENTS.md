# Demerzel Agent Team

Team definition for Claude Code agent teams.

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

1. **Asimov Laws override everything** — no teammate can violate Articles 0-5.
2. **Confidence thresholds apply** per alignment policy; escalate to lead when `<0.5`.
3. **Conventional commits**, at least one per completed task.
4. **No secrets** — never commit tokens, credentials, or API keys.
5. **Test what you build** — behavioral test validation required.
6. **IxQL awareness** — governance pipelines are IxQL; think in pipelines.

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
