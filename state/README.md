# Demerzel Governance State

Demerzel's own persistent state — what she knows, believes, and tracks about the ecosystem she governs.

## Directory Structure

- `beliefs/` — Tetravalent belief states about governance propositions (schema: `tetravalent-state.schema.json`)
- `evolution/` — Governance artifact effectiveness tracking (schema: `governance-evolution.schema.json`)
- `pdca/` — Demerzel's own improvement cycles (schema: `kaizen-pdca-state.schema.json`)
- `knowledge/` — Knowledge transfer records from Seldon (schema: `knowledge-state.schema.json`)
- `snapshots/` — Reconnaissance snapshots per repo (schema: `belief-snapshot.schema.json`)
- `oversight/` — Cross-repo governance tracking (compliance reports, directive status)

## Why Demerzel Has State

Demerzel governs ix, tars, and ga. A stateless coordinator cannot:
- Track what she knows vs. what she assumes about each repo
- Detect belief staleness (> 7 days without update)
- Measure governance artifact effectiveness over time
- Know which directives have been acknowledged vs. ignored

Consumer repos also maintain their own `state/` directories for local beliefs. Demerzel's state is the **ecosystem-wide view** — the governor's perspective.

## File Naming Convention

`{date}-{short-description}.{type}.json`

Examples:
- `2026-03-17-ix-governance-readiness.belief.json`
- `2026-03-17-default-constitution.evolution.json`
- `2026-03-17-behavioral-test-gap.pdca.json`

## Staleness

Default threshold: 7 days. Beliefs older than threshold are flagged during Tier 1 reconnaissance self-check.
