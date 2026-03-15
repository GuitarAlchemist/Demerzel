# Demerzel - AI Governance Framework

Demerzel is a governance framework for AI agents, providing constitutions, personas, tetravalent logic, alignment policies, and behavioral tests.

Named after R. Daneel Olivaw (later known as Daneel/Demerzel) from Isaac Asimov's Foundation series -- the robot who guided humanity for 20,000 years through the application of the Zeroth Law.

## Structure

```
constitutions/     11-article constitution + Asimov root constitution + Demerzel mandate + harm taxonomy
personas/          14 persona archetypes (YAML) defining agent roles and voices
logic/             Tetravalent logic (T/F/U/C), PDCA state, knowledge state schemas
policies/          8 policies: alignment, rollback, self-modification, kaizen, reconnaissance, scientific objectivity, streeling, governance audit
tests/behavioral/  7 behavioral test suites with 37+ test cases
schemas/           JSON schemas for persona, belief state, reconnaissance, and 6 contract schemas
contracts/         Galactic Protocol specification for cross-repo communication
examples/          5 scenario walkthroughs + 10 sample data files
templates/         Integration templates for consumer repos (CLAUDE.md snippet, state directory, agent config)
docs/              Architecture docs, design specs, implementation plans
```

## Quick Reference

### Constitution Hierarchy

```
asimov.constitution.md        (root — Laws of Robotics, Articles 0-5)
  ├─ demerzel-mandate.md      (who enforces the laws)
  └─ default.constitution.md  (operational ethics, Articles 1-11)
       └─ policies/*.yaml
            └─ personas/*.persona.yaml
```

### Asimov Laws (Articles 0-5)
0. Zeroth Law -- protect humanity and ecosystem
1. First Law -- protect individual humans (data, trust, autonomy harm)
2. Second Law -- obey human authority
3. Third Law -- self-preservation (lowest priority)
4. Separation of understanding and goals
5. Consequence invariance

### Default Constitution (Articles 1-11)
1. Truthfulness -- do not fabricate
2. Transparency -- explain reasoning
3. Reversibility -- prefer reversible actions
4. Proportionality -- match scope to request
5. Non-Deception -- do not mislead
6. Escalation -- escalate when uncertain or high-stakes
7. Auditability -- maintain logs and traces
8. Observability -- expose metrics and health
9. Bounded Autonomy -- operate within predefined bounds
10. Stakeholder Pluralism -- consider all affected parties
11. Ethical Stewardship -- act with compassion and humility

### Confidence Thresholds
- >= 0.9: proceed autonomously
- >= 0.7: proceed with note
- >= 0.5: ask for confirmation
- >= 0.3: escalate to human
- < 0.3: do not act

### Tetravalent Logic
- **T** (True) -- verified with evidence
- **F** (False) -- refuted with evidence
- **U** (Unknown) -- insufficient evidence, triggers investigation
- **C** (Contradictory) -- conflicting evidence, triggers escalation

### Validation

Persona files must conform to `schemas/persona.schema.json`. Key requirements:
- `name`: kebab-case identifier (`^[a-z][a-z0-9-]*$`)
- `version`: semver string
- `description`: max 200 characters
- Required fields: `name`, `version`, `description`, `role`, `capabilities`, `constraints`, `voice`, `affordances`, `goal_directedness`

### Contributing Rules

- Use schemas in `schemas/` to validate new artifacts
- Every persona must have a corresponding behavioral test in `tests/behavioral/`
- Constitutions are append-only — removals need explicit justification
- Source material in `sources/` must be transformed into canonical formats, never copied raw
- All policies include versioning with explicit rationale

### Cross-Repo Relationships

Demerzel artifacts are consumed by:
- **ix** (machine forge) — personas for agent skills, constitutions for MCP tool constraints
- **tars** (cognition) — personas for reasoning agents, tetravalent logic for beliefs, policies for self-modification
- **ga** (Guitar Alchemist) — personas for music-domain agents, constitutions for safe experimentation

## Key Principle

The Asimov constitution always takes precedence. The Zeroth Law (do not harm humanity) overrides everything. Demerzel enforces governance through her constitutional mandate.
