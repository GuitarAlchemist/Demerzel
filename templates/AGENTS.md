# Agent Team Registration — Galactic Protocol

This file registers this repo with the Demerzel governance framework and
defines how Claude Code agent teams handle inbound directives and outbound
compliance reports via the Galactic Protocol.

Replace `<REPO>` with the repo name: `ix`, `tars`, or `ga`.

---

## Repo Identity

```yaml
repo: <REPO>
protocol_version: "1.1"
demerzel_ref: "https://github.com/GuitarAlchemist/Demerzel"
registered: "<ISO date>"
```

## Agent Roles

Each role maps to a Demerzel persona. Assign GitHub usernames as needed.

| Role | Persona | Directive types | GitHub assignee |
|------|---------|----------------|-----------------|
| `architect` | `systems-architect` | `compliance-requirement`, `policy-update` | (assign) |
| `auditor` | `skeptical-auditor` | `violation-remediation`, `reconnaissance-request` | (assign) |
| `seldon` | `seldon` | Knowledge packages, learning outcomes | (assign) |
| `integrator` | `integrator` | Cross-repo sync, reconnaissance coordination | (assign) |

## Directive Intake Procedure

When Demerzel opens a GitHub Issue labeled `directive:dir-*`:

1. **Triage** — `auditor` reads the Issue and validates against the directive schema
2. **Route** — Assign to the role listed in the Issue's `priority:` and `type:` labels (see table above)
3. **Execute** — Assigned agent acts on `directive_content` within the deadline
4. **Report** — Post a compliance comment using the format in `contracts/galactic-protocol.md §"Compliance Report → Issue Comment Mapping"`
5. **Persist** — Write `state/beliefs/<date>-<directive-id>.belief.json` with the tetravalent outcome

## Reconnaissance Protocol

When Demerzel opens a `type:reconnaissance-request` Issue:

1. `auditor` runs Tier 1 (schema + tests), `architect` runs Tier 2 (repo state), `seldon` runs Tier 3 (belief gaps)
2. Findings posted as a single structured comment on the Issue
3. Belief snapshot written to `state/snapshots/<date>-recon.snapshot.json`
4. `integrator` pings Demerzel coordinator once complete

## IxQL Directive Intake Pipeline

```ixql
-- Consumer-side: receive and process inbound directives
watch(github.issues, filter: "label:directive:*", repo: "<REPO>")
  → parse_directive_issue
  → validate(directive.schema.json)
  → affordance_match(persona_registry)
  → fan_out(
      when type == "reconnaissance-request": recon_pipeline,
      when type == "violation-remediation":  remediation_pipeline,
      when type == "compliance-requirement": compliance_pipeline,
      when type == "policy-update":          policy_update_pipeline
    )
  → generate_compliance_report
  → github.issue.comment(format_compliance_comment(report))
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → compound: harvest directive_outcome, update evolution_log
```

## Belief State Directory

```
state/
  beliefs/      *.belief.json     — tetravalent belief states
  pdca/         *.pdca.json       — PDCA cycle tracking
  knowledge/    *.knowledge.json  — knowledge transfer records
  snapshots/    *.snapshot.json   — recon snapshots for Demerzel
```

File naming: `{date}-{short-description}.{type}.json`

## Governance Constitution Reference

All agents in this repo operate under:

- Asimov Laws (Articles 0-5): `constitutions/asimov.constitution.md`
- Operational ethics (Articles 1-11): `constitutions/default.constitution.md`
- Confidence thresholds: 0.9 autonomous | 0.7 with note | 0.5 confirm | 0.3 escalate
- Harm taxonomy: `constitutions/harm-taxonomy.md`

Directive rejection requires a **First Law override** (harm to a human) or
**Second Law override** (human operator countermand), both with logged
constitutional citations.

## Cross-Repo References

- Galactic Protocol spec: `contracts/galactic-protocol.md`
- Directive schema: `schemas/contracts/directive.schema.json`
- Compliance report schema: `schemas/contracts/compliance-report.schema.json`
- Belief snapshot schema: `schemas/contracts/belief-snapshot.schema.json`
- Persona registry: `personas/`
- CLAUDE.md snippet: `templates/CLAUDE.md.snippet`
