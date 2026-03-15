# State Directory Convention

This directory stores file-based belief state persistence as defined by the Galactic Protocol.

## Directory Structure

- `beliefs/` — Tetravalent belief states conforming to `tetravalent-state.schema.json`
- `pdca/` — PDCA cycle tracking conforming to `kaizen-pdca-state.schema.json`
- `knowledge/` — Knowledge transfer records conforming to `knowledge-state.schema.json`
- `snapshots/` — Belief snapshots conforming to `belief-snapshot.schema.json`

## File Naming Convention

`{date}-{short-description}.{type}.json`

Examples:
- `2026-03-15-cache-invalidation-fix.pdca.json`
- `2026-03-15-constitutional-hierarchy.belief.json`
- `2026-03-15-recon-tier2-scan.snapshot.json`

## Lifecycle

- **Beliefs:** Created when formed, updated in place on truth value change
- **PDCA:** Created at Plan phase, updated through cycle, retained after completion
- **Knowledge:** Created when Seldon teaches, updated with assessment results
- **Snapshots:** Generated on-demand for reconnaissance sync, retained for audit

## Staleness

Default threshold: 7 days. Beliefs with `last_updated` older than threshold are flagged during Demerzel's reconnaissance Tier 1 self-check.
