# 2. Harvest, don't declare

- Status: Accepted
- Date: 2026-06-20
- Deciders: Stephane Pareilleux
- Source: `/improve-codebase-architecture` review + `/grilling` session (2026-06-20)

## Context

Across the repo, the same fact is restated in multiple places and the copies drift:
artifact counts (ADR-0001), cross-reference edges (`context-map.yaml` vs the artifacts
themselves), the resilience score (`pipelines/resilience-dashboard.ixql` vs anywhere that
would recompute it), and validation rules (the halt marker validated in both Python and
PowerShell — ADR-0003).

Every one of these is the same disease: a fact is **declared** in an index or **recomputed**
in a consumer, instead of being read from the single place that owns it.

## Decision

Adopt one cross-cutting principle for the governance graph: **harvest, don't declare.**
A derived artifact (the manifest, ADR-0001) contains a fact **only because** the owning
source carried it. Nothing in an index is authored or recomputed.

This resolves into one verb — *harvest* — applied uniformly:

- **Inventory** is harvested from the filesystem (existence lives on disk).
- **Edges** are harvested from the artifacts' own reference fields — `constitutional_basis`,
  `references`, and the `validates:` frontmatter on tests (ADR-0003 / canonical reference
  syntax). An edge is never authored in the manifest.
- **Health snapshots** (resilience score, effectiveness deltas) are harvested from their
  emitters' latest output as `{metric, value, source, computed_at}`. The manifest stores the
  number and its provenance — **never the formula**. The formula stays in the emitter.

A harvested health number may be **stale** (emitter hasn't run since the last structural
change). That is accepted and made visible via `computed_at`, rather than hidden by
recomputing.

## Consequences

- **Locality everywhere**: the resilience formula stays in the pipeline; edges stay in
  artifacts; existence stays on disk. Each fact has exactly one home to fix.
- The manifest is a deep read-aggregator with a single small interface — *harvest* — not a
  dashboard that re-derives things.
- Health metrics are *referenced with provenance*, not owned. Staleness is a visible
  property, not a silent bug.

## Alternatives considered

- **Recompute health inside the manifest generator** (so the manifest is self-contained).
  Rejected: it puts the resilience formula `R = injections_caught / injections_total` in a
  second place beside `resilience-dashboard.ixql` — the very duplication ADR-0003 exists to
  remove, reborn one level up.
- **Author edges in the manifest** (a curated graph). Rejected: edges drift from the
  artifacts they describe; broken references can't be fixed at their source.
