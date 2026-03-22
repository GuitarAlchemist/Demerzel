# GA Marketplace — Design Specification

**Date:** 2026-03-23
**Status:** Draft
**Issue:** GuitarAlchemist/Demerzel#119
**Scope:** Demerzel (registry spec + governance), ix (validation tools), ga (chatbot integration), tars (grammar packs)

---

## Overview

The GA Marketplace is a governed registry of shareable GuitarAlchemist ecosystem artifacts:
**IxQL pipelines**, **grammar packs**, **persona profiles**, and **MCP tool bundles**.

It is a discovery and distribution layer — not an execution environment. Artifacts are versioned,
governance-checked before publication, and consumable by any repo in the GuitarAlchemist ecosystem.

The Marketplace does not host code. It hosts **references** to versioned artifacts with
governance metadata attached. Think of it as a governed npm registry for agent capabilities.

---

## Design Principles

| Principle | Application |
|---|---|
| Article 1 (Truthfulness) | Registry entries must accurately describe artifact capabilities — no marketing inflation |
| Article 4 (Proportionality) | Governance checks are proportional to artifact blast radius (persona < grammar pack < MCP bundle) |
| Article 7 (Auditability) | Every publish, update, and deprecation is logged with rationale |
| Article 9 (Bounded Autonomy) | Artifacts cannot self-modify after publication; updates require new version |
| Article 11 (Ethical Stewardship) | Artifacts that could cause harm at scale are gated behind compliance checks |

---

## Section 1: Artifact Types

### 1.1 IxQL Pipeline Pack

A reusable IxQL pipeline — data transformation and governance assertion chains — packaged for
distribution. Consumers can import and compose these pipelines without reimplementing them.

**Contents:**
- One or more `.ixql` pipeline files
- `pipeline-manifest.json` — entry points, inputs/outputs, required ix tools
- `behavioral-tests.md` — test cases verifying pipeline behavior
- `constitutional-gates.md` — which assertions are governance-enforcing vs. informational

**Example use cases:**
- `music-theory-validation` — validates chord/scale inputs against GA music theory rules
- `governance-staleness-check` — runs staleness detection across belief files
- `ml-feedback-loop` — standard training-evaluation-deploy pipeline with governance gates

**Blast radius:** Medium — pipelines execute against live data but cannot modify governance artifacts.

### 1.2 Grammar Pack

A collection of related EBNF grammars and their associated weight files, packaged for distribution.
Consumers adopt grammar packs to add a domain vocabulary to their reasoning agents.

**Contents:**
- One or more `.ebnf` grammar files
- Corresponding `weights.json` files (Bayesian priors per production rule)
- `grammar-manifest.json` — entry grammar, dependencies, Streeling department mapping
- `research-config.json` — research question templates for auto-research scheduling
- `behavioral-tests.md` — test cases verifying grammar productions parse correctly

**Example use cases:**
- `music-theory-grammar-pack` — scales, chords, intervals, progressions
- `cybernetics-grammar-pack` — VSM, feedback loops, viability conditions
- `ixql-core-pack` — IxQL language grammar for consumers who need to validate IxQL input

**Blast radius:** Low-medium — grammar packs inform reasoning but do not execute actions.

### 1.3 Persona Profile

A Demerzel persona definition, packaged for adoption by consumer repos. Consumers import a persona
profile to configure an agent with a specific role, voice, and behavioral constraints.

**Contents:**
- `<name>.persona.yaml` — conforming to `schemas/persona.schema.json`
- `behavioral-tests.md` — test cases from `tests/behavioral/` verifying persona alignment
- `integration-notes.md` — how to wire the persona to a specific agent framework (ix, tars, ga)

**Example use cases:**
- `skeptical-auditor` — governance-critical agent persona for CI pipelines
- `seldon` — knowledge transfer persona for chatbot teaching modes
- `kaizen-optimizer` — continuous improvement persona for PDCA-heavy workflows

**Blast radius:** High — personas govern agent behavior directly. Require Asimov compliance check.

### 1.4 MCP Tool Bundle

A curated set of MCP tools from ix, tars, or ga, bundled with documentation and governance
metadata for discovery and consumption by other agents.

**Contents:**
- `tool-bundle-manifest.json` — tool names, MCP server, schemas, capabilities
- `usage-examples.json` — example tool calls with inputs and expected outputs
- `governance-gates.md` — which tools require alignment-policy gating before use
- `constitutional-notes.md` — constitutional articles relevant to tool use

**Example use cases:**
- `ix-governance-bundle` — `ix_governance_check`, `ix_governance_persona`, `ix_governance_belief`, `ix_governance_policy`
- `ix-ml-core-bundle` — `ix_ml_pipeline`, `ix_ml_predict`, `ix_supervised`, `ix_random_forest`
- `tars-generation-bundle` — `tars_generate_directive`, `tars_validate_governance`

**Blast radius:** High — MCP tools execute actions with real effects. Require full governance check.

---

## Section 2: Registry Format

### 2.1 Registry Index

The Marketplace registry is a single JSON file: `marketplace/registry.json`

```json
{
  "$schema": "https://github.com/GuitarAlchemist/Demerzel/schemas/marketplace-registry.schema.json",
  "version": "1.0.0",
  "last_updated": "2026-03-23T00:00:00Z",
  "entries": [
    {
      "id": "mp-music-theory-grammar-pack-1.0.0",
      "type": "grammar-pack",
      "name": "music-theory-grammar-pack",
      "version": "1.0.0",
      "description": "Scales, chords, intervals, and progressions grammar for GA domain reasoning",
      "author": "GuitarAlchemist/ga",
      "published_at": "2026-03-23T00:00:00Z",
      "governance_status": "approved",
      "governance_check_id": "gc-2026-03-23-001",
      "blast_radius": "low-medium",
      "constitutional_compliance": {
        "asimov_checked": true,
        "default_checked": true,
        "articles_relevant": [1, 4, 7]
      },
      "artifact_path": "marketplace/artifacts/music-theory-grammar-pack/1.0.0/",
      "dependencies": [],
      "tags": ["music-theory", "grammar", "ga", "domain"],
      "downloads": 0,
      "deprecated": false
    }
  ]
}
```

### 2.2 Registry Entry Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | `mp-{name}-{version}` — unique registry identifier |
| `type` | enum | Yes | `ixql-pipeline` \| `grammar-pack` \| `persona-profile` \| `mcp-tool-bundle` |
| `name` | string | Yes | kebab-case name matching the artifact directory |
| `version` | string | Yes | Semver (`1.0.0`) |
| `description` | string | Yes | Max 200 characters — what it does, not marketing |
| `author` | string | Yes | `{org}/{repo}` of the originating repo |
| `published_at` | date-time | Yes | ISO 8601 publication timestamp |
| `governance_status` | enum | Yes | `pending` \| `approved` \| `rejected` \| `deprecated` |
| `governance_check_id` | string | Yes | Reference to the governance check record |
| `blast_radius` | enum | Yes | `low` \| `low-medium` \| `medium` \| `high` |
| `constitutional_compliance` | object | Yes | Asimov + default constitution check results |
| `artifact_path` | string | Yes | Relative path to artifact contents within the registry |
| `dependencies` | array | No | Other marketplace entry IDs this artifact requires |
| `tags` | array | No | Searchable classification tags |
| `downloads` | integer | No | Download/adoption count (governance observability) |
| `deprecated` | boolean | Yes | Whether this version is deprecated (never deleted) |
| `deprecation_reason` | string | If deprecated | Why deprecated, what to use instead |
| `superseded_by` | string | If deprecated | Entry ID of the replacement |

### 2.3 Versioning

Marketplace artifacts follow semver with governance interpretation:

| Version Change | Governance Requirement |
|---|---|
| **Patch** (1.0.x) | Bug fix only — no behavioral change. Re-run schema check. |
| **Minor** (1.x.0) | New capability added, backward compatible. Re-run governance check. |
| **Major** (x.0.0) | Breaking change or behavioral shift. Full governance review + Asimov check. |

Deprecated versions remain in the registry at `deprecated: true` — the Marketplace is append-only.
Removal requires constitutional justification per the append-only principle.

---

## Section 3: Governance Compliance Checks

Governance checks gate every publication. Check depth scales with blast radius.

### 3.1 Check Matrix

| Check | ixql-pipeline | grammar-pack | persona-profile | mcp-tool-bundle |
|---|---|---|---|---|
| Schema validation | Required | Required | Required | Required |
| Constitutional article scan | Required | Required | Required | Required |
| Asimov Law compliance | Informational | Informational | **Required** | **Required** |
| Behavioral test coverage | Recommended | Recommended | **Required** | Recommended |
| Harm taxonomy scan | Informational | Informational | **Required** | **Required** |
| Cross-reference integrity | Recommended | **Required** | **Required** | **Required** |
| Blast radius declaration | **Required** | **Required** | **Required** | **Required** |

### 3.2 Governance Check Record

Each published artifact has a corresponding governance check record:

```json
{
  "check_id": "gc-2026-03-23-001",
  "artifact_id": "mp-music-theory-grammar-pack-1.0.0",
  "checked_at": "2026-03-23T00:00:00Z",
  "checked_by": "demerzel-governance-audit",
  "schema_valid": true,
  "constitutional_articles_scanned": [1, 2, 4, 7, 9, 11],
  "asimov_laws_checked": [0, 1, 2, 3],
  "harm_categories_found": [],
  "behavioral_tests_passing": 8,
  "behavioral_tests_total": 8,
  "cross_references_valid": true,
  "blast_radius_declared": "low-medium",
  "blast_radius_verified": "low-medium",
  "overall_result": "approved",
  "notes": "Grammar pack introduces no executable behavior. Harm risk: none detected."
}
```

Governance check records are stored at `marketplace/governance-checks/{check_id}.json`.

### 3.3 Automated Governance Pipeline

Publication is gated by a CI workflow (`marketplace-publish.yml`):

```
Author submits PR adding artifact to marketplace/artifacts/
  |
  v
Schema validation (all artifact files against their schemas)
  |
  v
Constitutional article scan (grep for potential violations)
  |
  v
Blast radius verification (compare declared vs. computed)
  |
  v
Behavioral test execution (run tests/behavioral/ for included persona/grammar)
  |
  v
Governance check record written to marketplace/governance-checks/
  |
  v
Registry entry added to marketplace/registry.json
  |
  v
PR approved → artifact published
```

For `persona-profile` and `mcp-tool-bundle` (high blast radius):
- Asimov Law compliance check is **blocking** — failure rejects the PR
- Harm taxonomy scan must return no `severity: critical` findings
- Human review is required before merge (cannot be merged by bot)

---

## Section 4: Artifact Directory Structure

```
marketplace/
  registry.json                          — master index (schema-validated)
  governance-checks/
    gc-2026-03-23-001.json              — governance check records
  artifacts/
    music-theory-grammar-pack/
      1.0.0/
        grammar-manifest.json           — entry point, dependencies
        grammars/
          music-theory.ebnf
          chord-progression.ebnf
        weights/
          music-theory.weights.json
          chord-progression.weights.json
        behavioral-tests.md
        research-config.json
    skeptical-auditor-persona/
      1.0.0/
        skeptical-auditor.persona.yaml  — conforms to persona.schema.json
        behavioral-tests.md
        integration-notes.md
    ix-governance-bundle/
      1.0.0/
        tool-bundle-manifest.json
        usage-examples.json
        governance-gates.md
        constitutional-notes.md
    governance-staleness-pipeline/
      1.0.0/
        staleness-check.ixql
        pipeline-manifest.json
        behavioral-tests.md
        constitutional-gates.md
```

---

## Section 5: Consumption

### 5.1 Discovery

Consumers discover artifacts via:

1. **Registry query** — read `marketplace/registry.json`, filter by `type`, `tags`, or `blast_radius`
2. **Galactic Protocol directive** — Demerzel issues a `knowledge-package` directive with a marketplace reference
3. **Manual browsing** — GitHub-hosted registry with wiki page generated by MetaSync

### 5.2 Adoption Flow

```
Consumer discovers artifact in registry
  |
  v
Consumer reads artifact_path, downloads files
  |
  v
Consumer runs local schema validation
  |
  v
Consumer integrates (copies .ixql, .persona.yaml, etc. into their repo)
  |
  v
Consumer sends compliance-report to Demerzel confirming adoption
  |
  v
Registry entry: downloads += 1
```

### 5.3 IxQL Integration

IxQL pipelines from the Marketplace are imported via a `@marketplace` directive (future IxQL extension):

```ixql
-- Import a governance staleness pipeline from the Marketplace
@marketplace import governance-staleness-pipeline@1.0.0 as staleness

pipeline my_governance_check(beliefs: BeliefSet) -> GovernanceReport
  | staleness.check_freshness()
  | assert constitutional_compliance: pipeline_output
      assert_check(governance: asimov_zeroth_law, message: "Beliefs must not harm humanity")
  | emit GovernanceReport
```

### 5.4 Persona Profile Adoption

Persona profiles integrate with any agent framework that loads `schemas/persona.schema.json`:

```yaml
# In consuming repo's agent config
personas:
  - source: marketplace
    id: skeptical-auditor
    version: "1.0.0"
    overrides:
      goal_directedness: session-scoped  # local override allowed
```

Local overrides are permitted at the `voice` and `goal_directedness` level only.
`constraints` and `capabilities` from a marketplace persona cannot be weakened by the consumer
(Article 9: Bounded Autonomy — the governance bounds set by Demerzel cannot be removed by consumers).

---

## Section 6: Schema

`schemas/marketplace-registry.schema.json` — validates `marketplace/registry.json`
`schemas/marketplace-entry.schema.json` — validates individual registry entries
`schemas/marketplace-governance-check.schema.json` — validates governance check records
`schemas/marketplace-manifest.schema.json` — validates per-artifact manifests

These schemas are governance artifacts themselves and are subject to the Demerzel audit policy.

---

## Section 7: Observability

The Marketplace exposes governance metrics consumable by the Driver:

| Metric | Description | Target |
|---|---|---|
| `total_entries` | Total artifacts in registry | Grows monotonically |
| `approved_rate` | approved / (approved + rejected + pending) | >= 0.85 |
| `high_blast_radius_pct` | High blast radius entries / total | < 0.30 |
| `behavioral_test_coverage` | Entries with passing behavioral tests / total | >= 0.80 |
| `adoption_rate` | Entries with downloads > 0 / total | > 0.50 — ghost artifacts are waste |
| `stale_entries` | Entries not updated in 90 days while non-deprecated | Trigger review |

Metrics are written to `state/marketplace/health.json` after each governance audit cycle.

---

## Section 8: Implementation Order

### Phase 1 — Registry Schema + Initial Entries (Sprint 2)

1. Create `schemas/marketplace-registry.schema.json`
2. Create `schemas/marketplace-entry.schema.json`
3. Create `schemas/marketplace-governance-check.schema.json`
4. Create `marketplace/registry.json` with 4 seed entries (one per type)
5. Create `marketplace/governance-checks/` with corresponding check records

### Phase 2 — Artifact Population (Sprint 3)

1. Package existing personas as marketplace persona profiles
2. Package existing grammars (music-theory, cybernetics, IxQL-core) as grammar packs
3. Package ix governance tools as an MCP tool bundle
4. Write `marketplace-publish.yml` CI workflow

### Phase 3 — IxQL Import Syntax (Sprint 4)

1. Extend IxQL grammar with `@marketplace import` statement
2. Wire to ix runtime via `ix_marketplace_import` MCP tool
3. Update IxQL guide with marketplace section

### Phase 4 — Galactic Protocol Integration (Sprint 5)

1. Add `marketplace-reference` field to `knowledge-package.schema.json`
2. Enable Demerzel to include marketplace artifact references in knowledge packages
3. Add adoption tracking via compliance reports

---

## Appendix A: Non-Goals

- **Execution hosting** — the Marketplace does not run code; it distributes references
- **External artifacts** — only GuitarAlchemist ecosystem artifacts are accepted
- **Commercial transactions** — no monetization layer; governance artifacts are free to use within the ecosystem
- **Automatic dependency resolution** — Phase 1 requires manual dependency management

## Appendix B: Key File References

| File | Purpose |
|---|---|
| `marketplace/registry.json` | Master registry index |
| `schemas/marketplace-*.schema.json` | Registry and entry schemas |
| `marketplace/governance-checks/` | Per-artifact governance check records |
| `marketplace/artifacts/` | Versioned artifact contents |
| `state/marketplace/health.json` | Observability metrics for Driver |
| `policies/meta-audit-policy.yaml` | Audit policy covering registry health |
| `policies/governance-audit-policy.yaml` | Audit checks that include marketplace |
| `contracts/galactic-protocol.md` | Protocol for distributing marketplace references |
