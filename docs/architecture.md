# Demerzel Architecture

## Design Principles

1. **Separation of concerns** — Governance artifacts are independent of runtime code
2. **Reusability** — Any agent in any repo can consume these artifacts
3. **Auditability** — All policies are versioned with explicit rationale
4. **No runtime** — Demerzel defines behavior specifications, not execution engines
5. **Extraction over import** — Source material is transformed into canonical formats, never copied raw

## Artifact Types

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

### Policies (`policies/*.yaml`)

Operational rules for specific scenarios:

- **Alignment policy**: How the agent verifies its actions serve user intent
- **Rollback policy**: When and how the agent reverts its own changes
- **Self-modification policy**: Rules for when an agent modifies its own behavior

### Logic (`logic/`)

Multi-valued reasoning frameworks:

- **Tetravalent logic**: True, False, Unknown, Contradictory
- Used for belief state management in TARS reasoning loops
- Provides a formal framework for handling uncertainty and contradiction

### Schemas (`schemas/`)

JSON Schema definitions for all artifact types, enabling:

- Validation of persona/constitution/policy files
- IDE auto-completion
- Programmatic consumption by agents

## Relationship to Other Repos

```text
Demerzel (governance)
    │
    ├──→ ix (machine forge)
    │       Uses: personas for agent skill behavior
    │       Uses: constitutions for MCP tool constraints
    │
    ├──→ tars (cognition)
    │       Uses: personas for reasoning agent profiles
    │       Uses: tetravalent logic for belief management
    │       Uses: policies for self-modification rules
    │
    └──→ ga (Guitar Alchemist)
            Uses: personas for music-domain agent behavior
            Uses: constitutions for safe experimentation
```

## Versioning Strategy

- Personas: semver, breaking changes require new version
- Constitutions: append-only with dated amendments
- Policies: semver, with rollback provisions documented
- Schemas: semver, backward-compatible additions preferred
