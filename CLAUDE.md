# Demerzel — AI Governance Framework

Governance framework for AI agents: constitutions, personas, hexavalent logic, alignment policies, and behavioral tests. Named after R. Daneel Olivaw from Asimov's Foundation. Consumed by **ix**, **tars**, **ga** via the Galactic Protocol.

Full directory listing: see `README.md`. Source of truth for Asimov laws, Default constitution articles, and all 44 policies: `constitutions/` and `policies/`.

## Key Principle

The Asimov constitution always takes precedence. Zeroth Law (do not harm humanity) overrides everything. Demerzel enforces governance through her constitutional mandate.

## Hexavalent Logic (T/P/U/D/F/C)

- **T** True — verified with evidence
- **P** Probable — evidence leans true, not yet verified
- **U** Unknown — insufficient evidence, triggers investigation
- **D** Doubtful — evidence leans false, not yet refuted
- **F** False — refuted with evidence
- **C** Contradictory — conflicting evidence, triggers escalation

## Confidence Thresholds

`≥0.9` autonomous · `≥0.7` with note · `≥0.5` ask confirmation · `≥0.3` escalate · `<0.3` do not act.

## Validation

- Persona files must conform to `schemas/persona.schema.json`: `name` (kebab-case), `version` (semver), `description` (≤200 chars), required `role`, `capabilities`, `constraints`, `voice`, `affordances`, `goal_directedness`.
- Use schemas in `schemas/` to validate new artifacts.

## Contributing Rules

- Every persona needs a behavioral test in `tests/behavioral/`.
- Constitutions are **append-only** — removals need explicit justification.
- Source material in `sources/` must be transformed into canonical formats, never copied raw.
- All policies include versioning with explicit rationale.
