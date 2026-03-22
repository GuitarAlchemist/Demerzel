# GA Marketplace — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Issue:** GuitarAlchemist/Demerzel#119
**Scope:** ga-client (frontend), ga-react-components (UI components), Demerzel (governance), ix (backend ML)

---

## Overview

The GA Marketplace is a governed discovery and distribution system for Guitar Alchemist content:
courses, grammars, personas, ML models, and MCP tools. It enables creators to publish, users to
discover, and governed agents to validate and recommend — all under the Demerzel constitutional
framework.

Think: an App Store for AI-governed music education and analysis artifacts. Every listing has a
provenance record, copyright gate result, and governance health score.

---

## Goals

1. **Discovery** — search and browse GA artifacts by domain, type, skill level, language
2. **Provenance** — every artifact has a complete legal and governance lineage
3. **Quality gates** — GDPR, copyright, and AI Act compliance before listing
4. **Personalization** — recommendations driven by ix ML pipelines, governed by Demerzel
5. **Creator tools** — submit, validate, and monitor artifact health
6. **Cross-language** — multilingual listings (15 languages per multilingual-policy)

---

## Non-Goals

- Payment processing (out of scope v1)
- User authentication (deferred to ga auth layer)
- Native mobile apps (web-first)
- Social features (ratings, comments) in v1

---

## Section 1: Artifact Types

| Type | Source | Schema | Example |
|---|---|---|---|
| Course | `ga/courses/` | `schemas/course.schema.json` | "Blues Guitar Fundamentals" |
| Grammar | `grammars/*.ebnf` | `schemas/grammar-artifact.schema.json` | IxQL sci-ml-pipelines |
| Persona | `personas/*.persona.yaml` | `schemas/persona.schema.json` | skeptical-auditor |
| ML Model | ix `models/` | `schemas/model-card.schema.json` | guitar-tone-classifier-v2 |
| MCP Tool | ix `tools/` | `schemas/mcp-tool.schema.json` | `ix.ml.classify` |
| Visualization | `ga/vizs/` | `schemas/viz.schema.json` | Poincaré Ball Roadmap |
| Policy | `policies/*.yaml` | internal | alignment-policy |

---

## Section 2: Listing Lifecycle

```
Draft → Submitted → Compliance Review → Listed → Deprecated
          │                │
          │         [GDPR gate]
          │         [Copyright gate]
          │         [AI Act classification]
          │         [WCAG check (if public UI)]
          │                │
          │         Pass → Listed
          │         Fail → Rejected (with remediation hints)
          │         U/C  → Human Review Queue
```

### Compliance gates on submission

```ixql
assert listing_compliance: artifact_submission
  assert_check(governance: gdpr_provenance_check, message: "Provenance required")
  assert_check(governance: copyright_gate, message: "License must be clear")
  assert_check(governance: ai_act_classification, message: "Risk tier must be determined")
  assert_check(truth >= 0.7, message: "Compliance confidence must be >= 0.7")
```

If any gate returns F: submission rejected with specific remediation hints.
If any gate returns U: queued for human review.
If all gates return T: artifact listed automatically.

---

## Section 3: Data Model

### Artifact Listing Record

```json
{
  "$schema": "https://demerzel.gov/schemas/marketplace-listing.schema.json",
  "listing_id": "ga-listing-2026-03-24-001",
  "artifact_type": "course",
  "name": "Blues Guitar Fundamentals",
  "slug": "blues-guitar-fundamentals",
  "version": "1.2.0",
  "description": "12-lesson course covering blues scales, pentatonics, and phrasing",
  "languages": ["en", "es", "fr", "de", "ja"],
  "domain": "guitar_technique",
  "skill_level": "beginner",
  "tags": ["blues", "pentatonic", "improvisation"],
  "author": {
    "id": "creator-001",
    "name": "GuitarAlchemist Team",
    "verified": true
  },
  "governance": {
    "gdpr_provenance": "records/provenance-blues-course.json",
    "copyright_status": "cc_by",
    "ai_act_tier": 3,
    "wcag_level": "AA",
    "governance_health_score": 0.94,
    "last_compliance_check": "2026-03-24T00:00:00Z"
  },
  "stats": {
    "lessons": 12,
    "estimated_hours": 8,
    "languages_available": 15,
    "downloads": 0
  },
  "source_ref": {
    "repo": "GuitarAlchemist/ga",
    "path": "courses/blues-guitar-fundamentals/",
    "commit": "abc123"
  },
  "listed_at": "2026-03-24T00:00:00Z",
  "status": "listed"
}
```

### Governance Health Score

Each listing has a computed `governance_health_score` ∈ [0.0, 1.0]:

```
score = mean(
  gdpr_confidence,
  copyright_confidence,
  ai_act_confidence,
  wcag_score,
  schema_validation_score,
  staleness_score    -- how recently was compliance re-checked?
)
```

Score ranges:
- >= 0.9: Green (auto-listed)
- 0.7-0.9: Yellow (listed with advisory)
- 0.5-0.7: Amber (human review)
- < 0.5: Red (not listed)

---

## Section 4: Search & Discovery

### 4.1 Search API

```
GET /api/marketplace/search?q=blues+guitar&type=course&lang=en&level=beginner
```

**Response fields:**
- `results[]`: array of listing summaries
- `total`: total matching listings
- `facets`: counts by type, domain, language, level, governance_health

### 4.2 Recommendation Engine

Powered by ix ML pipeline:

```ixql
-- Personalized recommendations
governance_state → user_profile → memristive_markov
  → feature_selection(retain: ["skill_level", "domain_history", "language_pref"])
  → knn(n_neighbors: 20)
  → filter(governance_health_score >= 0.7)
  → bias_assessment
  → recommendation_output(top_k: 5)
  --governed standard
```

**Governance requirements for recommendations:**
- `bias_assessment` gate required (Article 10 — stakeholder pluralism)
- No recommendations filtered by protected characteristics
- Recommendation rationale exposed in UI (Article 2 — transparency)

### 4.3 Multilingual Support

All listing metadata is available in 15 languages per the multilingual-policy. The marketplace UI uses the browser's `Accept-Language` header to select language, with `en` as fallback.

Translated fields: `name`, `description`, `tags`, `skill_level labels`, `domain labels`.

---

## Section 5: Frontend Architecture

### 5.1 Routes (ga-client)

```
/marketplace                    → MarketplacePage (browse + search)
/marketplace/:slug              → ListingDetailPage
/marketplace/submit             → SubmissionPage (creator tool)
/marketplace/dashboard          → CreatorDashboardPage
```

### 5.2 Component Tree (ga-react-components)

```
MarketplacePage
  ├── SearchBar
  ├── FilterPanel
  │     ├── TypeFilter (course, grammar, model, tool...)
  │     ├── DomainFilter
  │     ├── LanguageFilter
  │     ├── LevelFilter
  │     └── GovernanceFilter (health score range)
  ├── ResultsGrid
  │     └── ListingCard (×N)
  │           ├── ArtifactTypeIcon
  │           ├── GovernanceHealthBadge
  │           ├── LanguageChips
  │           └── SkillLevelIndicator
  └── PaginationControls

ListingDetailPage
  ├── ListingHeader (name, author, version, languages)
  ├── GovernancePanel (compliance gates, health score, audit trail)
  ├── ContentPreview (first lesson, grammar snippet, etc.)
  ├── DownloadActions
  └── RelatedListings (powered by recommendation engine)
```

### 5.3 GovernancePanel Component

The `GovernancePanel` makes compliance visible to end users — implementing Article 2 (Transparency):

```tsx
<GovernancePanel
  gdprStatus="T"          // T | F | U | C
  copyrightStatus="T"
  aiActTier={3}
  wcagLevel="AA"
  healthScore={0.94}
  lastChecked="2026-03-24"
  auditTrailUrl="/api/marketplace/listings/abc123/audit"
/>
```

Renders as a collapsible "Governance" accordion. Always visible, not hidden behind a developer toggle — constitutional transparency is a product requirement.

---

## Section 6: Creator Tools

### 6.1 Submission Flow

1. Creator runs `ix marketplace submit --path ./my-course/`
2. ix CLI validates artifact schema locally
3. CLI submits to marketplace API with provenance metadata
4. Compliance gates run (automated, ~30 seconds)
5. Result: listed / rejected / queued for human review
6. Creator notified via Discord (`alert(discord, "Submission result: {{status}}")`)

### 6.2 Creator Dashboard

```
/marketplace/dashboard
  ├── MyListings table
  │     ├── status (listed / rejected / in_review / deprecated)
  │     ├── governance_health_score (with trend sparkline)
  │     └── last_compliance_check
  ├── ComplianceAlerts (expiring licenses, staleness warnings)
  └── SubmitNewArtifact CTA
```

### 6.3 Staleness Detection

Per `staleness-detection-policy.yaml`: compliance records older than 90 days are flagged as stale. The listing remains visible but with an "Compliance review pending" badge. Creators receive a Discord alert.

---

## Section 7: Backend API

Built in ga/.NET backend (existing ASP.NET Core stack).

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/marketplace/listings` | Browse with filters + pagination |
| GET | `/api/marketplace/listings/:slug` | Single listing detail |
| POST | `/api/marketplace/submit` | Submit new artifact |
| GET | `/api/marketplace/listings/:id/audit` | Governance audit trail |
| GET | `/api/marketplace/recommendations` | Personalized recommendations |
| GET | `/api/marketplace/search` | Full-text + faceted search |
| PATCH | `/api/marketplace/listings/:id/deprecate` | Deprecate a listing |

### Search Backend

SQLite for v1 (ga is an offline-first app). Full-text search via SQLite FTS5. Faceted counts via CTEs.

Upgrade path: Elasticsearch or Typesense for v2 when listing count exceeds 10k.

---

## Section 8: Galactic Protocol Integration

The marketplace is a cross-repo artifact: Demerzel governs it, ix powers the ML, ga hosts the UI.

Galactic Protocol messages:

```yaml
# Demerzel → ix: run compliance gates on submission
type: directive
from: Demerzel
to: ix
action: marketplace.compliance_check
payload:
  listing_id: "ga-listing-2026-03-24-001"
  artifact_path: "courses/blues-guitar-fundamentals/"
  gates: [gdpr, copyright, ai_act, wcag]
```

```yaml
# ix → Demerzel: compliance result
type: compliance_report
from: ix
to: Demerzel
subject: marketplace.compliance_check
payload:
  listing_id: "ga-listing-2026-03-24-001"
  gates:
    gdpr: {result: T, confidence: 0.95}
    copyright: {result: T, confidence: 0.98}
    ai_act: {tier: 3, result: T, confidence: 0.90}
    wcag: {level: AA, result: T, confidence: 0.88}
  overall_health_score: 0.93
  recommendation: listed
```

---

## Constitutional Basis

| Article | Marketplace application |
|---|---|
| 1 (Truthfulness) | No fabricated provenance or compliance results |
| 2 (Transparency) | GovernancePanel visible to all users; audit trail accessible |
| 3 (Reversibility) | Deprecated listings are archived, not deleted |
| 6 (Escalation) | U/C compliance results go to human review queue |
| 7 (Auditability) | Every compliance check logged with gate results and inputs |
| 9 (Bounded Autonomy) | Agents auto-list T results; humans decide on U/C |
| 10 (Stakeholder Pluralism) | Recommendations audited for bias; creator and user interests balanced |
| 11 (Ethical Stewardship) | Copyright gate protects rightsholders |

---

## Open Questions

1. **Recommendation cold start**: New users have no history for `memristive_markov`. Use `skill_level` + `language_pref` from onboarding survey as initial features? Recommendation: yes, with explicit "we're learning your preferences" disclosure.

2. **Listing granularity**: Should individual course lessons be listable, or only full courses? Recommendation: full courses as the atomic listing unit; lessons are not independently discoverable.

3. **Governance gate for personas**: Personas have `constraints` and `estimator_pairing`. Should there be a persona-specific compliance gate beyond schema validation? Recommendation: schema validation + behavioral test existence check is sufficient for v1.

4. **Search latency target**: SQLite FTS5 should handle < 10k listings at < 50ms. At scale, Typesense. No need to pre-optimize.
