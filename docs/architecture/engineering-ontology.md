# Engineering ontology (v1)

The shared model of *what exists* in the GuitarAlchemist software organization:
twelve entities and the edges between them. Streeling emits instances, Seldon
learns over them, Demerzel decides against them, IX measures them, TARS executes
them. Their identifiers are fixed in [core identifiers](core-identifiers.md); this
document fixes what they *are* and how they *connect*.

It exists so the eventual knowledge graph (Wave 3) has a spine agreed up front,
rather than each repo inventing an incompatible half of it.

## The twelve entities

| Entity | Id | Is | Owned by |
|---|---|---|---|
| **Worker** | `worker_id` | An agent identity that can be assigned work (`claude`, `jules`, `github-actions`). Executes through one or more providers. | Demerzel |
| **Capability** | `capability_id` | A thing a worker can do (`implementation`, `review`, `observability`). The unit routing matches work against. | Demerzel |
| **Repository** | `repository_id` | An ecosystem repo (`demerzel`, `ix`, `tars`, `ga`) — the boundary for collisions and ownership. | shared |
| **Pipeline** | `pipeline_id` | A declarative multi-step process (`qa-architect-cycle`, `ml-feedback`) a worker runs. | Demerzel / IX / TARS |
| **Policy** | `policy_id` | A governance rule that constrains decisions and workers. Overrides personas. | Demerzel |
| **Decision** | `decision_id` | A recorded choice (`escalate`, `proceed`, `standardize`) with evidence and a confidence. Advisory by default. | Demerzel |
| **Evidence** | `evidence_id` | A verifiable fact backing a decision or metric (a PR, a test log, a receipt). The join key between action and proof. | any producer |
| **Metric** | `metric_id` | A measured quantity over time (`ix:token-cost`, effectiveness deltas). | IX / emitters |
| **Artifact** | `artifact_id` | A governance object on disk (persona, schema, skill, constitution) — a node in `governance-manifest.json`. | Demerzel |
| **Review** | — | An assessment stage applied to a change before merge (council, adversarial, human). Produces Evidence. | Demerzel |
| **Workflow** | — | An automated GitHub Actions process; a Workflow may *run* a Pipeline and *emit* Evidence/Metrics. | shared |
| **Knowledge** | `knowledge_id` | A distilled, transferable package (a Seldon course, a harvested learning). | Seldon |

(Review and Workflow are addressed by their GitHub-native ids — a run url, a
workflow file — rather than a minted slug; they still appear in the graph as first
-class nodes.)

## Core relationships

The edges that make the model a graph rather than a glossary:

```text
Worker      --has-->        Capability
Worker      --assigned-->   WorkPackage        (Planner, #529)
Capability  --matches-->    WorkPackage
Pipeline    --runs-in-->    Repository
Workflow    --runs-->       Pipeline
Workflow    --emits-->      Evidence, Metric
Review      --produces-->   Evidence
Decision    --cites-->      Evidence
Decision    --governed-by-->Policy
Metric      --measures-->   Worker | Capability | Pipeline | Artifact
Knowledge   --distills-->   Evidence, Metric
Artifact    --references--> Artifact            (the governance manifest edges)
```

### Reading the roles onto the model

- **Streeling (observe)** emits `Evidence` and `Metric` instances tagged with
  `worker_id` / `repository_id`.
- **Seldon (learn)** turns streams of Evidence/Metric into `Knowledge`.
- **Demerzel (decide)** produces `Decision`s that cite Evidence and are governed by
  `Policy`, and owns the `Worker` / `Capability` registries that routing consumes.
- **IX (optimize)** produces `Metric`s and control models over them.
- **TARS (execute)** runs `Pipeline`s declared against `Repository`s.

## Alignment with existing artifacts

This is a naming-and-relationship layer over things that already exist — it does
not replace them:

- `Worker`/`Capability`/`Pipeline`/`Policy`/`Metric` are materialized by the
  registry factory (#525);
- `Evidence` and its envelope are the [Streeling event store](streeling-event-store.md);
- `Decision` is [Demerzel advisory decisions](demerzel-advisory-decisions.md);
- `Artifact` + its edges are `governance-manifest.json` (ADR-0002, harvested not
  declared);
- `Knowledge` is the Seldon delivery / harvest output.

## Status

v1 — a spine to build the knowledge graph on, deliberately small. Adding an entity
or edge kind is append-only; changing the meaning of an existing one requires a
supersede note and cross-repo coordination. No runtime types are mandated here;
consumers (e.g. the registry factory) may implement types once this stabilizes.
