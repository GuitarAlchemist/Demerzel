# Agent Team Registration — ix (Machine Forge)

This file registers the **ix** repo with the Demerzel governance framework and
defines how Claude Code agent teams handle inbound directives and outbound
compliance reports via the Galactic Protocol.

ix is the **Rust ML forge** — it builds machine learning pipelines, memristive-Markov
models, and IxQL processing infrastructure. Agents here operate in a performance-
and correctness-critical environment. Rust safety guarantees are a first-class
governance concern.

---

## Repo Identity

```yaml
repo: ix
protocol_version: "1.1"
demerzel_ref: "https://github.com/GuitarAlchemist/Demerzel"
registered: "2026-03-22"
domain: "Rust ML forge — memristive-Markov, IxQL pipelines, ML feedback"
```

## Agent Roles

| Role | Persona | Directive types | Focus area |
|------|---------|----------------|------------|
| `architect` | `systems-architect` | `compliance-requirement`, `policy-update` | Rust crate structure, pipeline design |
| `auditor` | `skeptical-auditor` | `violation-remediation`, `reconnaissance-request` | Safety invariants, test coverage, ML calibration |
| `seldon` | `seldon` | Knowledge packages, learning outcomes | ML domain research, feedback to Demerzel |
| `integrator` | `system-integrator` | Cross-repo sync, reconnaissance coordination | IxQL bridge to tars/ga, GP dispatch |

## ix-Specific Governance Concerns

### Rust Safety as Constitutional Compliance

- `unsafe` blocks require explicit justification logged in `state/beliefs/`
- Memory safety violations map to **First Law harm** (data integrity → trust harm)
- Every new `unsafe` block must be reviewed by `auditor` before merge

### ML Feedback Loop

ix ML pipelines send calibration recommendations to Demerzel per `ml-feedback-policy.yaml`:

```ixql
-- ix ML feedback outbound pipeline
ml_calibration_event(source: "ix", type: "feedback")
  → package(learning-outcome.schema.json)
  → github.issue.create(
      repo: "Demerzel",
      labels: ["type:learning-outcome", "source:ix"],
      body: format_learning_outcome(event)
    )
  → persist(state/knowledge/<date>-ml-calibration.knowledge.json)
```

### IxQL Pipeline Governance

ix owns IxQL runtime execution. Any changes to IxQL semantics must:

1. Issue a `compliance-requirement` directive to **tars** and **ga** before merging
2. Include backward-compatibility analysis from `architect`
3. Receive compliance confirmation from both consumers before the change is final

## Directive Intake Procedure

When Demerzel opens a GitHub Issue labeled `directive:dir-*` in ix:

1. **Triage** — `auditor` validates against directive schema; checks for Rust safety implications
2. **Route** — Assign per directive `type:` label (see table above)
3. **Execute** — Agent acts within deadline; Rust changes must pass `cargo test` and `cargo clippy`
4. **Report** — Post compliance comment using format in `contracts/galactic-protocol.md §"Compliance Report"`
5. **Persist** — Write `state/beliefs/<date>-<directive-id>.belief.json`

## Reconnaissance Protocol

When Demerzel opens a `type:reconnaissance-request` Issue:

1. `auditor` runs Tier 1: schema validation, `cargo test`, safety-invariant checks
2. `architect` runs Tier 2: crate dependency health, pipeline coverage, `unsafe` audit
3. `seldon` runs Tier 3: ML feedback backlog, belief currency staleness
4. Findings posted as a single structured comment; snapshot written to `state/snapshots/`
5. `integrator` pings Demerzel coordinator once complete

## IxQL Directive Intake Pipeline

```ixql
-- ix-side: receive and process inbound directives
watch(github.issues, filter: "label:directive:*", repo: "ix")
  → parse_directive_issue
  → validate(directive.schema.json)
  → affordance_match(persona_registry)
  → fan_out(
      when type == "reconnaissance-request": recon_pipeline,
      when type == "violation-remediation":  remediation_pipeline,
      when type == "compliance-requirement": compliance_pipeline,
      when type == "policy-update":          policy_update_pipeline
    )
  → guard: cargo_test_passes AND cargo_clippy_clean
  → generate_compliance_report
  → github.issue.comment(format_compliance_comment(report))
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → compound: harvest directive_outcome, update evolution_log

-- ix outbound: ML feedback to Demerzel
ml_pipeline_complete(pipeline: "*)
  → extract_calibration_signal
  → when signal.confidence_delta > 0.05:
      package(learning-outcome.schema.json)
      → github.issue.create(repo: "Demerzel", label: "type:learning-outcome")
```

## Belief State Directory

```
state/
  beliefs/      *.belief.json     — tetravalent belief states (safety invariants, pipeline health)
  pdca/         *.pdca.json       — PDCA cycles (ML experiments, pipeline refactors)
  knowledge/    *.knowledge.json  — ML calibration records, knowledge transfers from Seldon
  snapshots/    *.snapshot.json   — recon snapshots for Demerzel
```

File naming: `{date}-{short-description}.{type}.json`

Examples:
- `2026-03-22-unsafe-block-audit.belief.json`
- `2026-03-22-memristive-markov-pdca.pdca.json`
- `2026-03-22-ml-calibration-q1.knowledge.json`

## Governance Constitution Reference

All ix agents operate under:

- Asimov Laws (Articles 0-5): `constitutions/asimov.constitution.md` — unsafe code is a harm surface
- Operational ethics (Articles 1-11): `constitutions/default.constitution.md`
- Confidence thresholds: 0.9 autonomous | 0.7 with note | 0.5 confirm | 0.3 escalate
- Harm taxonomy: `constitutions/harm-taxonomy.md`

Directive rejection requires a **First Law override** (harm to a human, including data or trust harm
from memory safety violations) or **Second Law override** (human operator countermand), both with
logged constitutional citations.

## Cross-Repo References

- Galactic Protocol spec: `https://github.com/GuitarAlchemist/Demerzel/blob/master/contracts/galactic-protocol.md`
- Directive schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/directive.schema.json`
- Compliance report schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/compliance-report.schema.json`
- Belief snapshot schema: `https://github.com/GuitarAlchemist/Demerzel/blob/master/schemas/contracts/belief-snapshot.schema.json`
- ML feedback policy: `https://github.com/GuitarAlchemist/Demerzel/blob/master/policies/ml-feedback-policy.yaml`
- Persona registry: `https://github.com/GuitarAlchemist/Demerzel/blob/master/personas/`
- CLAUDE.md snippet: `https://github.com/GuitarAlchemist/Demerzel/blob/master/templates/CLAUDE.md.snippet`
