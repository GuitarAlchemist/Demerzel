# Cross-repo contracts

> Moved out of `CLAUDE.md` (2026-07-19). It was resident on every turn while being
> both **discoverable** (the contracts live in the named repos) and **rot-prone** —
> it carries a dated liveness claim that silently ages. Read this when you are
> changing a cross-repo seam, not on every turn.

Demerzel orchestrates cycles across sibling repos via **JSON-on-disk contracts** —
the canonical handoff pattern across the GuitarAlchemist ecosystem. Sibling clones
are typically peers under the same parent directory.

## The seams

- **ga** (`../ga/`, .NET / C# / F# / React, music theory + RAG) — defines
  `docs/contracts/2026-05-02-qa-verdict.contract.md` (schema:
  `docs/contracts/qa-verdict.schema.json`), the QA Architect verdict shape Demerzel
  emits via `pipelines/qa-architect-cycle.ixql`. Also owns
  `docs/contracts/2026-05-02-optick-sae-artifact.contract.md`, consumed by
  `qa_score_quality_drift`.
- **ix** (`../ix/`, Rust ML algorithms) — the `ix-optick-sae` crate is *intended* to
  produce `state/voicings/optick.index` and SAE artifacts under
  `state/quality/optick-sae/` for cross-cycle quality-drift evidence.
  **Declared-but-unfulfilled:** as recorded on 2026-06-21 the crate existed but
  these runtime artifacts had not been generated, so `qa_score_quality_drift` had
  no live input. Any consumer must degrade explicitly when the artifacts are absent.
  ⚠️ *This liveness claim is dated — re-verify against `../ix/` before relying on it.*
- **tars** (`../tars/`, F# grammar + metacognition) — cross-model theory validator.

## Rules of change

- **Locked-field changes need cross-repo coordination.** The Galactic Protocol and
  `governance/demerzel/schemas/capability-registry.json` are Demerzel's own
  equivalents.
- **Introducing a non-breaking baseline shift:** use the `links.supersedes` pattern
  from `optick-sae-artifact` rather than freezing a schema.
- **Draft status:** contracts marked `v0.1.x` in their headers remain drafts until
  their Phase 4 freeze milestones.
