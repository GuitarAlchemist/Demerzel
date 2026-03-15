# Demerzel Architecture

## Design Principles

1. **Separation of concerns** — Governance artifacts are independent of runtime code
2. **Reusability** — Any agent in any repo can consume these artifacts
3. **Auditability** — All policies are versioned with explicit rationale
4. **No runtime** — Demerzel defines behavior specifications, not execution engines
5. **Extraction over import** — Source material is transformed into canonical formats, never copied raw

## Artifact Types

### Precedence Hierarchy

```text
asimov.constitution.md        (root — Laws of Robotics + LawZero principles)
  ├─ demerzel-mandate.md      (who enforces the laws)
  └─ default.constitution.md  (operational ethics)
       └─ policies/*.yaml     (operational rules)
            └─ personas/*.persona.yaml  (behavioral profiles, advisory)
```

The Asimov constitution is the root of all governance. The Demerzel mandate establishes who enforces the laws. The default constitution provides operational ethics. Both the mandate and default constitution are subordinate to Asimov. Policies provide operational rules. Personas are advisory.

### Personas (`personas/*.persona.yaml`)

Structured behavioral profiles for AI agents. Each persona defines:

- **Role**: What the agent is responsible for
- **Capabilities**: What the agent can do
- **Constraints**: What the agent must not do
- **Voice**: Communication style and tone
- **Interaction patterns**: How the agent collaborates with humans and other agents

Personas are advisory — they can be overridden by constitutions and policies.

### Constitutions (`constitutions/*.constitution.md`)

Hard behavioral boundaries. A constitution:

- Defines inviolable principles
- Takes precedence over persona preferences
- Cannot be overridden by the agent itself
- Requires explicit human authorization to modify

The Demerzel mandate (`constitutions/demerzel-mandate.md`) is a special constitutional document that establishes Demerzel as the governance coordinator. It defines her authority, jurisdiction, accountability, and succession rules.

### Policies (`policies/*.yaml`)

Operational rules for specific scenarios:

- **Alignment policy**: How the agent verifies its actions serve user intent
- **Rollback policy**: When and how the agent reverts its own changes
- **Self-modification policy**: Rules for when an agent modifies its own behavior
- **Kaizen policy**: Universal continuous improvement methodology — PDCA cycle, waste taxonomy, 5 Whys, three improvement models
- **Reconnaissance policy**: Three-tier mandatory discovery protocol
- **Scientific objectivity policy**: LawZero principles — fact/opinion separation, generator/estimator accountability
- **Streeling policy**: Knowledge transfer protocol — three-layer curriculum (governance/experiential/domain), adaptive delivery, two-stage verification
- **Governance audit policy**: Three-level validation checklist — schema validation, cross-reference integrity, full governance audit

### Logic (`logic/`)

Multi-valued reasoning frameworks:

- **Tetravalent logic**: True, False, Unknown, Contradictory
- Used for belief state management in TARS reasoning loops
- Provides a formal framework for handling uncertainty and contradiction
- **Kaizen PDCA state**: Extends tetravalent logic for Plan-Do-Check-Act improvement cycles
- **Knowledge state**: Tracks knowledge transfer events with tetravalent belief state assessment for the Streeling framework

### Schemas (`schemas/`)

JSON Schema definitions for all artifact types, enabling:

- Validation of persona/constitution/policy files
- IDE auto-completion
- Programmatic consumption by agents

### Harm Taxonomy (`constitutions/harm-taxonomy.md`)

Shared reference defining categories of harm recognized by the constitutional framework:

- **Zeroth Law tier**: Ecosystem harm (governance integrity, collective trust, cascading harm)
- **First Law tier**: Human-directed harm (data, trust, autonomy)
- **Third Law tier**: System harm (operational degradation, self-preservation)

Each category includes definitions, examples, detection signals, and severity criteria.

### Contracts (`schemas/contracts/` + `contracts/`)

Cross-repo communication protocol (Galactic Protocol) defining how Demerzel communicates with consumer repos:

- **Outbound:** Governance directives, knowledge packages (Demerzel → consumers)
- **Inbound:** Compliance reports, belief snapshots, learning outcomes (consumers → Demerzel)
- **Bidirectional:** External sync envelopes for integration with external systems (Confluence, knowledge graphs, etc.)

Contract schemas in `schemas/contracts/` define message formats. The protocol specification in `contracts/galactic-protocol.md` defines behavioral semantics — flows, error handling, and message ordering.

### State Convention (`state/` in consumer repos)

File-based belief state persistence. Each consumer repo maintains a `state/` directory with JSON files conforming to existing schemas:

- `state/beliefs/` — tetravalent belief states
- `state/pdca/` — PDCA cycle tracking
- `state/knowledge/` — knowledge transfer records
- `state/snapshots/` — belief snapshots for reconnaissance sync

Files follow the naming convention: `{date}-{short-description}.{type}.json`. Staleness detection flags beliefs older than 7 days during reconnaissance.

### Examples (`examples/`)

Operational examples demonstrating governance frameworks in action:

- **Scenarios** (`examples/scenarios/`): Step-by-step walkthroughs of governance flows — constitutional violations, PDCA cycles, knowledge transfer, reconnaissance, Zeroth Law escalation
- **Sample data** (`examples/sample-data/`): Valid JSON instances of all contract and state schemas, suitable for testing and reference

### Templates (`templates/`)

Ready-to-copy artifacts for consumer repos adopting Demerzel governance:

- **CLAUDE.md snippet**: Template governance text for consumer repo instructions
- **State directory**: Pre-structured `state/` directory with convention guide
- **Agent config**: Template persona file with all required governance fields

### Reconnaissance (`policies/reconnaissance-policy.yaml`)

Three-tier mandatory discovery protocol:

- **Tier 1 — Self-Check**: Are governance artifacts intact and current?
- **Tier 2 — Environment Scan**: Is the target repo state understood?
- **Tier 3 — Situational Analysis**: Is Demerzel ready for this specific action?

Each tier has a gate that can halt operations based on graduated risk assessment. Zeroth Law concerns trigger an emergency override at any tier.

Per-repo discovery profiles extend the universal checklist for ix, tars, and ga.

### Scientific Objectivity (`policies/scientific-objectivity-policy.yaml`)

Operationalizes LawZero principles:

- **Fact/opinion separation**: Evidence tagged as empirical, inferential, or subjective
- **Generator/estimator accountability**: Creative output reviewed by neutral evaluator
- **No instrumental goals**: Agents cannot acquire unauthorized capabilities or persistent goals

## Relationship to Other Repos

```text
Demerzel (governance)
    │
    ├──→ ix (machine forge)
    │       Uses: personas for agent skill behavior
    │       Uses: constitutions (Asimov + default) for MCP tool constraints
    │       Uses: reconnaissance profiles for self-governance
    │
    ├──→ tars (cognition)
    │       Uses: personas for reasoning agent profiles
    │       Uses: tetravalent logic for belief management
    │       Uses: policies for self-modification rules
    │       Uses: reconnaissance profiles for belief state monitoring
    │
    └──→ ga (Guitar Alchemist)
            Uses: personas for music-domain agent behavior
            Uses: constitutions for safe experimentation
            Uses: reconnaissance profiles for capability boundary checks
```

## Versioning Strategy

- Personas: semver, breaking changes require new version
- Constitutions: append-only with dated amendments
- Policies: semver, with rollback provisions documented
- Schemas: semver, backward-compatible additions preferred
- Harm taxonomy: versioned alongside the Asimov constitution it supports
- Reconnaissance profiles: per-repo profiles versioned with the reconnaissance policy
