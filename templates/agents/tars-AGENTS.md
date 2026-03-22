# Agent Team Registration — tars (Cognition)

This file registers the **tars** repo with the Demerzel governance framework and
defines how Claude Code agent teams handle inbound directives and outbound
compliance reports via the Galactic Protocol.

tars is the **F# reasoning engine** — it implements tetravalent logic evaluation,
belief state management, probabilistic reasoning, and the Seldon Plan cognitive
architecture. Agents here operate in a correctness-critical domain where reasoning
fidelity directly affects governance outcomes.

---

## Repo Identity

```yaml
repo: tars
protocol_version: "1.1"
demerzel_ref: "https://github.com/GuitarAlchemist/Demerzel"
registered: "2026-03-22"
domain: "F# reasoning engine — tetravalent logic, belief states, Seldon Plan cognition"
```

## Agent Roles

| Role | Persona | Directive types | Focus area |
|------|---------|----------------|------------|
| `architect` | `systems-architect` | `compliance-requirement`, `policy-update` | F# module design, logic type system, reasoning pipelines |
| `auditor` | `skeptical-auditor` | `violation-remediation`, `reconnaissance-request` | Belief validity, T/F/U/C accuracy, reasoning audit trails |
| `seldon` | `seldon` | Knowledge packages, learning outcomes | Cross-model validation, research cycles, curriculum |
| `integrator` | `system-integrator` | Cross-repo sync, reconnaissance coordination | Belief snapshot delivery to Demerzel, GP message routing |

## tars-Specific Governance Concerns

### Tetravalent Logic Fidelity

tars is the canonical runtime for Demerzel's tetravalent logic (T/F/U/C). Any change to
logic evaluation semantics must:

1. Be reviewed by `auditor` against `logic/tetravalent-logic.md`
2. Include a test suite update covering all four truth values
3. Trigger a `compliance-requirement` directive to **ix** and **ga** if the change affects
   cross-repo belief evaluation

### Belief State Ownership

tars generates the belief snapshots that Demerzel uses for governance decisions:

- All `*.belief.json` files in `state/beliefs/` must conform to `tetravalent-state.schema.json`
- Staleness threshold: 7 days (per `belief-currency-policy.yaml`)
- `seldon` reviews belief currency and triggers refresh directives when stale

### Self-Modification Constraint

tars implements reasoning about self-modification. Per `self-modification-policy.yaml`:

- tars agents **may not** modify constitutional article implementations autonomously
- `policy-update` directives require human review before implementation when they affect
  reasoning evaluation logic
- All changes to core reasoning pipelines require `auditor` sign-off before merge

## Directive Intake Procedure

When Demerzel opens a GitHub Issue labeled `directive:dir-*` in tars:

1. **Triage** — `auditor` validates against directive schema; checks for logic-fidelity implications
2. **Route** — Assign per directive `type:` label (see table above); escalate any directive touching
   tetravalent semantics to `architect` for design review
3. **Execute** — Agent acts within deadline; F# changes must pass `dotnet test` with all logic tests green
4. **Report** — Post compliance comment using format in `contracts/galactic-protocol.md §"Compliance Report"`
5. **Persist** — Write `state/beliefs/<date>-<directive-id>.belief.json` with tetravalent outcome

## Reconnaissance Protocol

When Demerzel opens a `type:reconnaissance-request` Issue:

1. `auditor` runs Tier 1: schema validation, `dotnet test`, belief state integrity checks
2. `architect` runs Tier 2: reasoning pipeline coverage, logic type soundness, self-modification audit
3. `seldon` runs Tier 3: belief currency staleness, knowledge transfer backlog, cross-model validation gaps
4. Findings posted as a single structured comment; snapshot written to `state/snapshots/`
5. `integrator` pings Demerzel coordinator once complete

## IxQL Directive Intake Pipeline

```ixql
-- tars-side: receive and process inbound directives
watch(github.issues, filter: "label:directive:*", repo: "tars")
  → parse_directive_issue
  → validate(directive.schema.json)
  → affordance_match(persona_registry)
  → fan_out(
      when type == "reconnaissance-request": recon_pipeline,
      when type == "violation-remediation":  remediation_pipeline,
      when type == "compliance-requirement": compliance_pipeline,
      when type == "policy-update":          policy_update_pipeline
    )
  → guard: dotnet_test_passes AND belief_states_valid
  → generate_compliance_report
  → github.issue.comment(format_compliance_comment(report))
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → compound: harvest directive_outcome, update evolution_log

-- tars outbound: belief snapshot delivery
recon_complete(tier: 3)
  → generate_belief_snapshot(belief-snapshot.schema.json)
  → persist(state/snapshots/<date>-recon.snapshot.json)
  → github.issue.comment(repo: "Demerzel", snapshot_summary)
```

## Belief State Directory

```
state/
  beliefs/      *.belief.json     — tetravalent belief states (reasoning health, logic fidelity)
  pdca/         *.pdca.json       — PDCA cycles (reasoning experiments, logic refactors)
  knowledge/    *.knowledge.json  — Seldon knowledge transfers, cross-model validation outcomes
  snapshots/    *.snapshot.json   — recon snapshots for Demerzel (authoritative belief exports)
```

File naming: `{date}-{short-description}.{type}.json`

Examples:
- `2026-03-22-tetravalent-eval-health.belief.json`
- `2026-03-22-seldon-plan-cycle-3.pdca.json`
- `2026-03-22-cross-model-validation.knowledge.json`

## Governance Constitution Reference

All tars agents operate under:

- Asimov Laws (Articles 0-5): `constitutions/asimov.constitution.md` — reasoning errors are a harm surface
- Operational ethics (Articles 1-11): `constitutions/default.constitution.md`
- Confidence thresholds: 0.9 autonomous | 0.7 with note | 0.5 confirm | 0.3 escalate
- Harm taxonomy: `constitutions/harm-taxonomy.md`

**tars-specific rule:** Reasoning outputs claimed as T (True) must have empirical or inferential
evidence. Subjective assessments must be tagged as `channel: fuzzy`. Confidence inflation
(fuzzy claimed as crisp) is a crisp/fuzzy boundary violation per Galactic Protocol §"Channel Semantics".

Directive rejection requires a **First Law override** (harm to a human, including reasoning harm
that misleads governance decisions) or **Second Law override** (human operator countermand), both
with logged constitutional citations.

## Cross-Repo References

- Galactic Protocol spec: `https://github.com/GuitarAlchemist/Demerzel/blob/master/contracts/galactic-protocol.md`
- Directive schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/directive.schema.json`
- Compliance report schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/compliance-report.schema.json`
- Belief snapshot schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/belief-snapshot.schema.json`
- Tetravalent logic spec: `https://github.com/GuitarAlchemist/Demerzel/blob/master/logic/tetravalent-logic.md`
- Self-modification policy: `https://github.com/GuitarAlchemist/Demerzel/blob/master/policies/self-modification-policy.yaml`
- Belief currency policy: `https://github.com/GuitarAlchemist/Demerzel/blob/master/policies/belief-currency-policy.yaml`
- Persona registry: `https://github.com/GuitarAlchemist/Demerzel/blob/master/personas/`
- CLAUDE.md snippet: `https://github.com/GuitarAlchemist/Demerzel/blob/master/templates/CLAUDE.md.snippet`
