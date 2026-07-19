# Core identifiers (v1)

Streeling observes, Seldon learns, Demerzel decides, IX optimizes, TARS executes.
They can only agree on *what happened* if they name the same entity the same way.
This document fixes that vocabulary: the ten identifiers every repo uses to point
at a worker, a capability, a pipeline, and so on.

It is a **naming contract**, not a schema — it says how an id is *spelled* and what
it *means to stay stable*, so a `worker_id` emitted by Streeling resolves to the
same worker in a Demerzel decision and an IX metric. Companion: the
[engineering ontology](engineering-ontology.md), which defines the *entities* these
ids point at and how they relate.

## Conventions

These generalize what the schemas and registries already do (`pipeline_id`,
`artifact_id`, `worker_id`; workers spelled `claude` / `jules` / `github-actions`):

- **Field name** — `snake_case` with an `_id` suffix (`worker_id`, not `workerId`
  or `worker`). JSON keys and schema properties use this form.
- **Value** — a lowercase **kebab-case slug**, optionally namespaced with `:` when
  a bare slug would collide across producers (`worker_id: "jules"`,
  `capability_id: "review"`, `metric_id: "ix:token-cost"`). No spaces, no camelCase,
  no opaque UUIDs where a human-stable slug will do.
- **Stability** — ids are **append-only**: once emitted and referenced, a slug is
  not renamed in place. A supersede is a *new* slug plus a `supersedes` note (the
  same non-breaking pattern the cross-repo contracts use), never a silent rename —
  a renamed id orphans every belief, metric, and decision that referenced the old
  one.
- **Ownership** — each id has one *authoritative producer* (below). Others reference
  it; they do not mint new spellings for the same entity.

## The ten identifiers

| Id | Field | Value format | Authoritative producer | Example (grounded) |
|---|---|---|---|---|
| **WorkerId** | `worker_id` | agent/runner slug | Demerzel worker registry | `claude`, `codex`, `jules`, `github-actions` |
| **CapabilityId** | `capability_id` | domain-verb slug | Demerzel capability registry | `implementation`, `observability`, `review` |
| **RepositoryId** | `repository_id` | ecosystem repo key | `schemas/capability-registry.json` `.repos` | `demerzel`, `ix`, `tars`, `ga` |
| **PipelineId** | `pipeline_id` | pipeline slug | pipeline registry | `qa-architect-cycle`, `ml-feedback` |
| **PolicyId** | `policy_id` | policy file stem | `policies/` | `alignment-policy`, `autonomous-loop-policy` |
| **DecisionId** | `decision_id` | `<producer>:<verb>:<seq-or-hash>` | Demerzel advisory decisions | `demerzel:escalate:2026-07-19-001` |
| **MetricId** | `metric_id` | `<repo>:<measure>` | IX / emitters | `ix:token-cost`, `demerzel:artifact-effectiveness` |
| **EvidenceId** | `evidence_id` | `<kind>:<ref>` | any producer | `pr:GuitarAlchemist/Demerzel#767`, `test:discovery-267` |
| **KnowledgeId** | `knowledge_id` | knowledge-package slug | Seldon | `seldon:planner-mvp`, `harvest:2026-07-19` |
| **ArtifactId** | `artifact_id` | governance-artifact path stem | `governance-manifest.json` | `skeptical-auditor`, `execution-graph` |

Notes:

- **WorkerId vs provider** — a `worker_id` is the agent identity (`claude`); a
  *provider* is a concrete execution channel for that worker (`claude-code-local`,
  `claude-code-cli`, an `ANTHROPIC_API_KEY` fallback). One worker, many providers;
  budget/routing lives at the provider level (see
  [cost-aware routing](cost-aware-routing.md)).
- **EvidenceId** is the join key between an action and its proof — a Demerzel
  decision cites `evidence_id`s; Streeling emits them; Seldon distills over them.
- **ArtifactId** reuses the manifest's `name` (a file stem), so the governance
  graph and the ontology share one key space rather than two.

## How other sprint packs reference this

- Streeling events (`docs/architecture/streeling-event-store.md`) carry
  `worker_id` / `repository_id` / `evidence_id` on every envelope.
- Demerzel advisory decisions (`demerzel-advisory-decisions.md`) key on
  `decision_id` and cite `evidence_id`s.
- The registry factory (#525) is the authoritative producer for `worker_id`,
  `capability_id`, `pipeline_id`, `policy_id`, `metric_id`.
- IX/Seldon control models (#594, #596) consume `metric_id` / `evidence_id`.

## Status

v1 — the starting vocabulary. Additions are append-only; changes to an existing
id's semantics require a supersede note and cross-repo coordination per the
Galactic Protocol.
