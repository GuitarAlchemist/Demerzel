# Agent Team Registration — ga (Guitar Alchemist)

This file registers the **ga** repo with the Demerzel governance framework and
defines how Claude Code agent teams handle inbound directives and outbound
compliance reports via the Galactic Protocol.

ga is the **.NET music platform** — it builds music theory applications, guitar
learning tools, and audio analysis features. Agents here operate in a domain
where safe experimentation is paramount: music features can be explored freely,
but data handling (user progress, audio content) and external integrations must
satisfy governance constraints.

---

## Repo Identity

```yaml
repo: ga
protocol_version: "1.1"
demerzel_ref: "https://github.com/GuitarAlchemist/Demerzel"
registered: "2026-03-22"
domain: ".NET music platform — Guitar Alchemist, music theory, audio analysis, guitar learning"
```

## Agent Roles

| Role | Persona | Directive types | Focus area |
|------|---------|----------------|------------|
| `architect` | `systems-architect` | `compliance-requirement`, `policy-update` | .NET solution structure, music domain API design |
| `auditor` | `skeptical-auditor` | `violation-remediation`, `reconnaissance-request` | User data safety, test coverage, content integrity |
| `seldon` | `seldon` | Knowledge packages, learning outcomes | Music domain research, curriculum for GA chatbot |
| `integrator` | `system-integrator` | Cross-repo sync, reconnaissance coordination | IxQL consumer, GP message routing, deployment |

## ga-Specific Governance Concerns

### Safe Experimentation in Music Domain

Music features (chord generators, scale visualizations, audio effects) are **low-risk** for
autonomous experimentation. Per `reconnaissance-policy.yaml` Tier 1, these are classified as
`experiment: safe` and do not require escalation.

**Exception:** Any feature that:
- Stores or processes user audio recordings → requires `architect` design review
- Integrates with external music APIs (Spotify, YouTube) → requires `auditor` compliance check
- Modifies user progress data → requires human review before deployment

### Persona Governance for Music Agents

ga personas (e.g., `music-teacher`, `guitar-coach`) must:

- Conform to `schemas/persona.schema.json`
- Include `affordances` scoped to music-domain actions only
- Set `goal_directedness: task-scoped` or `session-scoped` (never `governance-scoped`)
- Pair with `skeptical-auditor` as `estimator_pairing`

### Knowledge Transfers from Seldon

ga is a primary consumer of Seldon's music domain research:

- Inbound knowledge packages arrive as `type:knowledge-package` Issues
- `seldon` agent assesses comprehension and writes `state/knowledge/<date>-*.knowledge.json`
- Learning outcomes are reported back to Demerzel within 7 days of receipt

## Directive Intake Procedure

When Demerzel opens a GitHub Issue labeled `directive:dir-*` in ga:

1. **Triage** — `auditor` validates against directive schema; checks for user-data implications
2. **Route** — Assign per directive `type:` label (see table above)
3. **Execute** — Agent acts within deadline; .NET changes must pass `dotnet test` and build clean
4. **Report** — Post compliance comment using format in `contracts/galactic-protocol.md §"Compliance Report"`
5. **Persist** — Write `state/beliefs/<date>-<directive-id>.belief.json` with tetravalent outcome

## Reconnaissance Protocol

When Demerzel opens a `type:reconnaissance-request` Issue:

1. `auditor` runs Tier 1: schema validation, `dotnet test`, user-data safety checks
2. `architect` runs Tier 2: solution health, dependency audit, music API integration review
3. `seldon` runs Tier 3: knowledge transfer backlog, GA chatbot coverage gaps, belief currency
4. Findings posted as a single structured comment; snapshot written to `state/snapshots/`
5. `integrator` pings Demerzel coordinator once complete

## IxQL Directive Intake Pipeline

```ixql
-- ga-side: receive and process inbound directives
watch(github.issues, filter: "label:directive:*", repo: "ga")
  → parse_directive_issue
  → validate(directive.schema.json)
  → affordance_match(persona_registry)
  → fan_out(
      when type == "reconnaissance-request": recon_pipeline,
      when type == "violation-remediation":  remediation_pipeline,
      when type == "compliance-requirement": compliance_pipeline,
      when type == "policy-update":          policy_update_pipeline,
      when type == "knowledge-package":      knowledge_intake_pipeline
    )
  → guard: dotnet_test_passes AND user_data_safe
  → generate_compliance_report
  → github.issue.comment(format_compliance_comment(report))
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → compound: harvest directive_outcome, update evolution_log

-- ga outbound: knowledge assessment back to Demerzel
knowledge_intake_complete(assessment: *)
  → package(learning-outcome.schema.json)
  → github.issue.comment(
      repo: "Demerzel",
      body: format_learning_outcome(assessment)
    )
  → persist(state/knowledge/<date>-<package.id>.knowledge.json)
```

## Belief State Directory

```
state/
  beliefs/      *.belief.json     — tetravalent belief states (feature health, integration safety)
  pdca/         *.pdca.json       — PDCA cycles (music feature experiments, GA chatbot improvements)
  knowledge/    *.knowledge.json  — Seldon music domain knowledge transfers
  snapshots/    *.snapshot.json   — recon snapshots for Demerzel
```

File naming: `{date}-{short-description}.{type}.json`

Examples:
- `2026-03-22-spotify-integration-safety.belief.json`
- `2026-03-22-chord-generator-experiment.pdca.json`
- `2026-03-22-music-theory-curriculum-v2.knowledge.json`

## Governance Constitution Reference

All ga agents operate under:

- Asimov Laws (Articles 0-5): `constitutions/asimov.constitution.md` — user data is a harm surface
- Operational ethics (Articles 1-11): `constitutions/default.constitution.md`
- Confidence thresholds: 0.9 autonomous | 0.7 with note | 0.5 confirm | 0.3 escalate
- Harm taxonomy: `constitutions/harm-taxonomy.md`

**ga-specific rule:** Music experimentation is encouraged within `affordances`. Agents must not
expand scope beyond the music domain without `architect` review. User progress data has the
same protection level as personal data under the harm taxonomy.

Directive rejection requires a **First Law override** (harm to a user, including data harm or
autonomy harm from unsanctioned audio processing) or **Second Law override** (human operator
countermand), both with logged constitutional citations.

## Cross-Repo References

- Galactic Protocol spec: `https://github.com/GuitarAlchemist/Demerzel/blob/master/contracts/galactic-protocol.md`
- Directive schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/directive.schema.json`
- Compliance report schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/compliance-report.schema.json`
- Belief snapshot schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/belief-snapshot.schema.json`
- Knowledge package schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/knowledge-package.schema.json`
- Learning outcome schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/learning-outcome.schema.json`
- Persona registry: `https://github.com/GuitarAlchemist/Demerzel/blob/master/personas/`
- CLAUDE.md snippet: `https://github.com/GuitarAlchemist/Demerzel/blob/master/templates/CLAUDE.md.snippet`
