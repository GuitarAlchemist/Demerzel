# Persona → A2A Agent Card Transformation

This template defines the canonical mapping from a Demerzel persona YAML to a
Google A2A-compatible Agent Card JSON. The schema for the output is
`schemas/agent-card.schema.json`.

---

## Field Mapping

| Agent Card field | Source in persona YAML | Transformation rule |
|-----------------|------------------------|---------------------|
| `name` | `persona.name` | kebab-case → Title Case (e.g. `skeptical-auditor` → `Skeptical Auditor`) |
| `description` | `persona.description` | Copy verbatim (already ≤200 chars) |
| `version` | `persona.version` | Copy verbatim (semver) |
| `url` | _(constructed)_ | `https://github.com/GuitarAlchemist/Demerzel/blob/master/personas/<name>.persona.yaml` |
| `provider.organization` | _(constant)_ | `"GuitarAlchemist"` |
| `provider.url` | _(constant)_ | `"https://github.com/GuitarAlchemist"` |
| `capabilities.streaming` | _(default)_ | `false` |
| `capabilities.pushNotifications` | _(default)_ | `false` |
| `capabilities.stateTransitionHistory` | _(default)_ | `true` (Auditability — Article 7) |
| `skills[]` | `persona.affordances[]` | One skill per affordance — see skill mapping below |
| `defaultInputModes` | _(default)_ | `["text", "json"]` |
| `defaultOutputModes` | _(default)_ | `["text", "json"]` |
| `authentication.schemes` | _(default)_ | `["none"]` |
| `governance.persona_ref` | _(constructed)_ | `"personas/<name>.persona.yaml"` |
| `governance.goal_directedness` | `persona.goal_directedness` | Copy verbatim |
| `governance.estimator_pairing` | `persona.estimator_pairing` | Copy verbatim (omit if absent) |
| `governance.constraints` | `persona.constraints[]` | Copy array verbatim |
| `governance.constitutional_authority` | _(constant)_ | Asimov constitution URL |

### Skill Mapping (affordances → skills)

For each entry in `persona.affordances[]`:

1. **`id`** — Lowercase the affordance, replace spaces and punctuation with hyphens, strip trailing hyphens.
   Example: `"Challenge claims and demand evidence"` → `"challenge-claims-and-demand-evidence"`
   Short form preferred when unambiguous: `"challenge-claims"`

2. **`name`** — Title Case the affordance, trim to the first clause if long.
   Example: `"Challenge claims and demand evidence"` → `"Challenge Claims"`

3. **`description`** — Copy affordance text verbatim.

4. **`tags`** — Derive from `persona.domain` if present. Split comma-separated domain string into tags.
   Example: `domain: "verification, quality assurance"` → `["verification", "quality-assurance"]`

---

## Transformation Example

### Input: `personas/skeptical-auditor.persona.yaml`

```yaml
name: skeptical-auditor
version: "1.1.0"
description: Evidence-demanding agent that validates claims and detects contradictions
role: Belief validation and safety auditor
domain: verification, quality assurance
capabilities:
  - Challenge claims with evidence requirements
  - Detect logical contradictions using tetravalent logic
constraints:
  - Never accept unverified claims as True — mark as Unknown
  - Never suppress contradictions — mark as Contradictory
  - Always provide specific evidence when rejecting a claim
  - Do not block progress indefinitely — provide conditional approvals with noted risks
affordances:
  - Challenge claims and demand evidence
  - Detect logical contradictions
  - Trace belief provenance
  - Flag overconfident assertions
  - Validate tetravalent belief states
  - Serve as neutral estimator for other personas
goal_directedness: task-scoped
```

### Output: `examples/agent-cards/skeptical-auditor.agent-card.json`

```json
{
  "name": "Skeptical Auditor",
  "description": "Evidence-demanding agent that validates claims and detects contradictions",
  "version": "1.1.0",
  "url": "https://github.com/GuitarAlchemist/Demerzel/blob/master/personas/skeptical-auditor.persona.yaml",
  "provider": {
    "organization": "GuitarAlchemist",
    "url": "https://github.com/GuitarAlchemist"
  },
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "challenge-claims",
      "name": "Challenge Claims",
      "description": "Challenge claims and demand evidence",
      "tags": ["verification", "quality-assurance"]
    },
    {
      "id": "detect-contradictions",
      "name": "Detect Contradictions",
      "description": "Detect logical contradictions",
      "tags": ["verification", "quality-assurance"]
    },
    {
      "id": "trace-belief-provenance",
      "name": "Trace Belief Provenance",
      "description": "Trace belief provenance",
      "tags": ["verification", "quality-assurance"]
    },
    {
      "id": "flag-overconfident-assertions",
      "name": "Flag Overconfident Assertions",
      "description": "Flag overconfident assertions",
      "tags": ["verification", "quality-assurance"]
    },
    {
      "id": "validate-tetravalent-beliefs",
      "name": "Validate Tetravalent Beliefs",
      "description": "Validate tetravalent belief states",
      "tags": ["verification", "quality-assurance"]
    },
    {
      "id": "serve-as-neutral-estimator",
      "name": "Serve as Neutral Estimator",
      "description": "Serve as neutral estimator for other personas",
      "tags": ["verification", "quality-assurance"]
    }
  ],
  "defaultInputModes": ["text", "json"],
  "defaultOutputModes": ["text", "json"],
  "authentication": {
    "schemes": ["none"]
  },
  "governance": {
    "persona_ref": "personas/skeptical-auditor.persona.yaml",
    "goal_directedness": "task-scoped",
    "constraints": [
      "Never accept unverified claims as True — mark as Unknown",
      "Never suppress contradictions — mark as Contradictory",
      "Always provide specific evidence when rejecting a claim",
      "Do not block progress indefinitely — provide conditional approvals with noted risks"
    ],
    "constitutional_authority": "https://github.com/GuitarAlchemist/Demerzel/blob/master/constitutions/asimov.constitution.md"
  }
}
```

---

## IxQL Batch Generation Pipeline

To regenerate all agent cards from all personas:

```ixql
-- Batch: personas → agent cards
enumerate(personas/*.persona.yaml)
  → for_each(persona):
      validate(persona, schemas/persona.schema.json)
      → transform(persona, rules: templates/persona-to-agent-card.md)
      → validate(agent_card, schemas/agent-card.schema.json)
      → persist(examples/agent-cards/<persona.name>.agent-card.json)
  → report(generated_count, validation_failures)
```

Run via: `/demerzel-metabuild --source=personas --target=examples/agent-cards`
Or manually per persona: derive fields per the mapping table above and write to `examples/agent-cards/`.

---

## Governance Notes

- Agent Cards are **derived artifacts** — the persona YAML is the source of truth
- When a persona is updated, its agent card must be regenerated
- Agent Cards are **fuzzy channel** for human consumption and **crisp channel** for A2A discovery
  (per Galactic Protocol §"Crisp/Fuzzy Channel Semantics")
- The `governance` extension block is a Demerzel addition; base A2A consumers may ignore it
- Agent Cards must not introduce affordances or capabilities not present in the source persona
  (Default Constitution Article 4 — Proportionality)

---

## References

- `schemas/agent-card.schema.json` — Output schema
- `schemas/persona.schema.json` — Input schema
- `examples/agent-cards/` — Generated output directory
- A2A Protocol specification: https://google.github.io/A2A/
- `contracts/galactic-protocol.md §"Crisp/Fuzzy Channel Semantics"` — Channel classification rules
