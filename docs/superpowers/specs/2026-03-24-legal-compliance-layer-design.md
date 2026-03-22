# Legal Compliance Layer — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Issue:** GuitarAlchemist/Demerzel#147
**Scope:** Demerzel (governance spec), ix (enforcement), tars (reasoning), ga (content pipeline)
**Depends on:** `docs/research-catala-constitutional-encoding.md`, `constitutions/harm-taxonomy.md`

---

## Overview

The legal compliance layer formalizes how Demerzel's governed agents handle four intersecting legal domains:

1. **AI Act risk classification** — EU AI Act (2024/1689) risk tier determination
2. **GDPR data provenance** — lawful basis, data minimization, right to erasure
3. **Copyright gates** — training data and output copyright risk classification
4. **WCAG accessibility** — output accessibility standards for public-facing content

Each domain is encoded as a **Catala scope** (per the research in `docs/research-catala-constitutional-encoding.md`) where deterministic rule logic applies, and as a **Demerzel policy extension** where tetravalent reasoning and PDCA cycles apply. The two layers are complementary, not duplicative.

---

## Design Principles

| Principle | Application |
|---|---|
| Article 1 (Truthfulness) | Legal classifications must not be fabricated; uncertain classifications emit U not a guess |
| Article 2 (Transparency) | Every compliance decision is explained with its legal basis |
| Article 3 (Reversibility) | Compliance gates are non-destructive; rejected content is quarantined, not deleted |
| Article 6 (Escalation) | Classification confidence < 0.5 escalates to human legal review |
| Article 9 (Bounded Autonomy) | Agents do not make final legal determinations; they classify and escalate |
| Article 10 (Stakeholder Pluralism) | Compliance considers users, subjects of data, rightsholders, and regulators |

---

## Section 1: AI Act Risk Classification

### 1.1 Regulatory Context

The EU AI Act (Regulation 2024/1689, effective 2 August 2026) establishes four risk tiers for AI systems:

| Tier | Label | Examples | Consequence |
|---|---|---|---|
| 0 | Unacceptable | Social scoring, real-time biometric surveillance | Prohibited outright |
| 1 | High | Hiring, credit, medical diagnosis, critical infrastructure | Conformity assessment + registration |
| 2 | Limited | Chatbots (must disclose AI), deepfakes | Transparency obligations only |
| 3 | Minimal | Spam filters, AI-enabled games | No mandatory requirements |

### 1.2 Classification Gate

IxQL governance gate: `ai_act_classification`

```ixql
-- Classify pipeline output before deployment
assert ai_act_compliance: pipeline_output
  assert_check(governance: ai_act_classification, message: "AI Act tier must be determined before deploy")
  assert_check(truth >= 0.7, message: "Classification must be at least T >= 0.7 confident")
```

**Classification inputs (required):**
- `domain` — application domain (hiring, medical, creative, educational, etc.)
- `deployment_context` — public API, internal tool, research, open-source
- `human_oversight` — supervised, human-in-loop, autonomous
- `biometric` — boolean: does the system process biometric data?
- `output_affects_rights` — boolean: can output affect legal rights or life opportunities?

**Classification output:**
- `tier` — 0 / 1 / 2 / 3
- `confidence` — float [0.0, 1.0]
- `required_conformity_assessment` — boolean
- `human_review_required` — boolean
- `legal_basis` — citation list

**Tetravalent behavior:**
- T (>= 0.9): tier determined; enforcement can proceed autonomously
- T (0.7–0.9): tier determined; human confirmation recommended
- U (< 0.7): insufficient context; escalate to legal reviewer
- C: contradictory signals (e.g. domain signals Tier 1, deployment context signals Tier 3); escalate

### 1.3 Catala Encoding

```catala
scope AiActClassification:
  input domain content Domain
  input deployment_context content DeploymentContext
  input output_affects_rights content boolean
  input biometric content boolean
  output tier content Tier
  output human_review_required content boolean

  label tier_default
  definition tier equals minimal  -- Tier 3 default

  exception tier_default
  definition tier under condition
    domain = hiring or domain = medical or domain = credit
    or output_affects_rights
  consequence equals high  -- Tier 1

  exception tier_default
  definition tier under condition
    biometric and deployment_context = public
  consequence equals unacceptable  -- Tier 0

  definition human_review_required under condition
    tier = high or tier = unacceptable
  consequence equals true
```

### 1.4 High-Risk Documentation Requirements (Tier 1)

For Tier 1 systems, Demerzel must produce or reference:

- [ ] Technical documentation (Article 11): architecture, training data, capabilities
- [ ] Risk management system log (Article 9): ongoing risk tracking
- [ ] Data governance documentation (Article 10): training data provenance
- [ ] Human oversight measures (Article 14): who intervenes, how, when
- [ ] Accuracy and robustness metrics (Article 15): eval results from IxQL pipeline
- [ ] EU database registration number (Article 71): upon deployment

These requirements are encoded as `assert_check` assertions in the deployment pipeline.

---

## Section 2: GDPR Data Provenance

### 2.1 Regulatory Context

GDPR (Regulation 2016/679) requires every processing activity to have a lawful basis and that personal data is handled with documented provenance. For AI systems, the most relevant obligations are:

| Obligation | Relevant Articles | Demerzel mapping |
|---|---|---|
| Lawful basis declaration | Art. 6 | `gdpr_lawful_basis` gate |
| Data minimization | Art. 5(1)(c) | `feature_selection` must justify each feature |
| Retention limits | Art. 5(1)(e) | Model artifacts have expiry metadata |
| Right to erasure | Art. 17 | Training data index supports deletion |
| Data provenance | Art. 30 | Records of processing activities (ROPA) |
| Cross-border transfers | Art. 44-49 | `gdpr_transfer_gate` for non-EEA sources |

### 2.2 Data Provenance Schema

Every `data_source` in a governed IxQL pipeline must carry provenance metadata:

```json
{
  "$schema": "https://demerzel.gov/schemas/data-provenance.schema.json",
  "source_id": "train-2026-03-24-001",
  "collection_date": "2026-03-24",
  "collection_method": "web_scrape | api | user_provided | synthetic",
  "lawful_basis": "consent | contract | legal_obligation | vital_interests | public_task | legitimate_interests",
  "contains_personal_data": true,
  "data_subjects": ["users", "artists", "public_figures"],
  "erasure_index": "state/gdpr/erasure-index-2026.json",
  "retention_policy": "P2Y",
  "transfer_mechanism": "adequacy_decision | scc | bcr | derogation | none",
  "dpa_contact": "dpa@guitaralchemist.com"
}
```

### 2.3 GDPR Governance Gate

IxQL gate: `gdpr_provenance_check`

```ixql
-- Assert provenance before training
assert gdpr_compliance: csv("users.csv")
  assert_check(schema: "schemas/data-provenance.schema.json", message: "Must have provenance record")
  assert_check(not_null, message: "Provenance fields must be complete")
  assert_check(governance: gdpr_provenance_check, message: "GDPR gate must pass")
```

**Gate checks:**
1. Provenance record exists and validates against schema
2. Lawful basis is declared and non-expired
3. If personal data: erasure index is present
4. If non-EEA source: transfer mechanism is declared
5. Retention period has not expired

**Erasure propagation:** When a subject requests erasure, the `erasure-index` is updated and all downstream model artifacts referencing that subject are flagged for retraining or deletion. This is tracked in `state/gdpr/erasure-queue.json`.

### 2.4 Feature Justification (Data Minimization)

Data minimization requires that only necessary features are processed. For `feature_selection` stages, each retained feature must have a justification:

```ixql
feature_selection(
  retain: ["frequency_hz", "amplitude_db", "tempo_bpm"],
  justification: "Required for guitar-tone classification per business purpose",
  gdpr_minimization_review: "2026-03-24"
)
```

The `ix-lsp` LSP warns when `feature_selection` has no `justification` annotation in a governed pipeline.

---

## Section 3: Copyright Gates

### 3.1 Context

Training on copyrighted data without appropriate license creates legal risk. Three regimes are relevant:

| Regime | Jurisdiction | Key provision | Agent behavior |
|---|---|---|---|
| EU DSM Directive Art. 4 | EU | TDM opt-out is binding; honor `robots.txt` TDM tags | Check TDM opt-out before training |
| US fair use (17 U.S.C. § 107) | US | Four-factor test; commercial use weighs against fair use | Classify commercial vs. research context |
| Output similarity | All | Generated output substantially similar to training data source | Screen outputs against known copyrighted works |

### 3.2 Copyright Classification Gate

IxQL gate: `copyright_gate`

**Input signals:**

| Signal | Type | Description |
|---|---|---|
| `source_license` | enum | public_domain, cc0, cc_by, cc_by_sa, cc_by_nc, all_rights_reserved, unknown |
| `tdm_opt_out` | boolean | Source has declared TDM opt-out |
| `deployment_context` | enum | research, internal, commercial, open_source |
| `output_type` | enum | classification, regression, generation, summarization |

**Classification output:**

| License + Context | Classification | Action |
|---|---|---|
| public_domain / cc0 | Green | No gate needed |
| cc_by / cc_by_sa + attribution honored | Green | Require attribution metadata |
| cc_by_nc + commercial context | Red | Block; suggest license purchase |
| all_rights_reserved + no explicit license | Amber | Human review required |
| tdm_opt_out = true | Red | Exclude from training set |
| unknown license | Amber | Human review required |

**Tetravalent mapping:**
- Green: T — proceed
- Amber: U — escalate to human
- Red: F — halt, quarantine data source

### 3.3 Output Similarity Screening

For generative models (`diffusion_model`, `variational_autoencoder`, neural text/audio generators), output must be screened before delivery:

```ixql
assert output_originality: generative_model → audio_output
  assert_check(copyright_similarity_check(threshold: 0.80), message: "Output must not be substantially similar to copyrighted works")
```

The `copyright_similarity_check` predicate compares output against a reference database of known copyrighted works using embedding distance. Threshold 0.80 = 80% similarity triggers review.

### 3.4 Attribution Tracking

When training on CC-licensed data, attribution metadata must propagate to the model card:

```json
{
  "model_id": "guitar-tone-classifier-v2",
  "training_data_attributions": [
    {
      "source": "Freesound.org dataset",
      "license": "cc_by",
      "attribution": "Various artists via Freesound.org (CC BY 4.0)",
      "records_used": 12400
    }
  ]
}
```

---

## Section 4: WCAG Accessibility Gates

### 4.1 Context

Public-facing content generated or presented by governed agents must meet WCAG 2.2 Level AA. For Guitar Alchemist's React frontend (ga-react-components, ga-client), this applies to:

- AI-generated text displayed in UI
- Generated music notation (VexFlow)
- Data visualizations (D3.js, Three.js)
- Audio content with transcripts

### 4.2 Accessibility Checks

| Content type | Required checks | WCAG criterion |
|---|---|---|
| Text output | Language tag, reading level <= Grade 12 | 3.1.1, 3.1.5 |
| Images / charts | Alt text generated | 1.1.1 |
| Audio output | Transcript / caption available | 1.2.1 |
| Color coding (D3/Three.js) | Color-blind safe palette, not color-only | 1.4.1 |
| Interactive components | Keyboard navigable, ARIA labels | 2.1.1, 4.1.2 |
| Contrast | 4.5:1 minimum for normal text | 1.4.3 |

### 4.3 WCAG Governance Gate

IxQL gate: `wcag_accessibility_check`

```ixql
-- Assert accessibility before publishing content
assert content_accessibility: llm_output → web_component_render
  assert_check(governance: wcag_accessibility_check, message: "Content must meet WCAG 2.2 AA")
  assert_check(type: text, message: "Text content must have language tag")
```

**Gate outputs:**
- `wcag_level_achieved` — A, AA, AAA, or Fail
- `violations` — list of failing criteria with remediation hints
- `auto_remediated` — list of issues auto-fixed (e.g. alt text generated from content)

### 4.4 Auto-Remediation

Where violations can be automatically fixed without changing content meaning:

| Violation | Auto-remediation |
|---|---|
| Missing alt text | Generate alt text via image-caption model |
| Missing transcript | Generate transcript via ASR model |
| Insufficient contrast | Darken/lighten color automatically |
| Missing ARIA label | Derive label from adjacent text content |

Auto-remediations are logged in the audit trail with the original and remediated values.

---

## Section 5: Catala Integration

### 5.1 Architecture

Per `docs/research-catala-constitutional-encoding.md`, Catala handles the deterministic rule layer. The integration architecture is:

```
Demerzel constitutional articles (Catala scopes)
  ├── AiActClassification scope
  ├── GdprLawfulBasis scope
  ├── CopyrightGate scope
  └── WcagAccessibility scope
        │
        ▼
  Evaluated at pipeline compile time (static) + runtime (dynamic)
        │
        ▼
  Conclusions → tetravalent values → IxQL governance gates
```

### 5.2 What Catala Handles

- Deterministic legal rule application (tier determination, lawful basis check)
- Override hierarchy (constitution > regulation > policy > pipeline)
- Conflict detection (two rules firing simultaneously → Catala runtime error → C in tetravalent)
- Test vector coverage for every article × regulation boundary condition

### 5.3 What Catala Does NOT Handle

Per research findings:

| Requirement | Limitation | Demerzel workaround |
|---|---|---|
| Tetravalent U/C values | Catala is bivalent | Encode as enum + YAML policy |
| PDCA cycle state | Catala is stateless | External PDCA orchestration in `state/` |
| Probabilistic confidence | No float conditionals | IxQL policy layer handles thresholds |
| Cross-scope proof | Manual F* lemmas needed | Behavioral tests as substitute |

### 5.4 Proof-of-Concept Catala Files (Future Work)

When the Catala PoC (#113 next step) is implemented, the files will live at:

```
constitutions/catala/
  ai-act-classification.catala.md
  gdpr-lawful-basis.catala.md
  copyright-gate.catala.md
  asimov-override-hierarchy.catala.md
tests/catala/
  ai-act-test-vectors.catala.md
  gdpr-test-vectors.catala.md
```

---

## Section 6: Implementation Roadmap

### Phase 1 — Schema + Gate Specs (this document)

- [x] AI Act classification gate spec
- [x] GDPR provenance schema spec
- [x] Copyright gate classification spec
- [x] WCAG gate spec
- [ ] `schemas/data-provenance.schema.json` — JSON Schema for provenance records
- [ ] `schemas/model-card.schema.json` — JSON Schema for model cards with legal metadata

### Phase 2 — Policy YAML

- [ ] `policies/ai-act-classification-policy.yaml` — classification rules and thresholds
- [ ] `policies/gdpr-provenance-policy.yaml` — provenance requirements per data type
- [ ] `policies/copyright-gate-policy.yaml` — license classification and TDM opt-out handling
- [ ] `policies/wcag-accessibility-policy.yaml` — required WCAG levels per content type

### Phase 3 — IxQL Gate Integration (ix repo)

- [ ] `governance_gates.rs` in ix: implement AI Act, GDPR, copyright, WCAG checks
- [ ] LSP integration: `--governed strict` triggers all four gates
- [ ] Erasure queue processing: `ix gdpr erasure-process`

### Phase 4 — Catala PoC

- [ ] Catala encoding of AI Act tier classification
- [ ] F* lemma: "if biometric=true and context=public, tier is always unacceptable"
- [ ] Test vectors for all tier boundaries

---

## Constitutional Basis

| Article | Compliance domain |
|---|---|
| 0 (Zeroth Law) | AI Act Tier 0 prohibition — systems that harm humanity are blocked absolutely |
| 1 (Truthfulness) | GDPR accuracy; copyright gate prevents training on falsely-licensed data |
| 2 (Transparency) | All compliance decisions explained with legal basis citation |
| 3 (Reversibility) | GDPR erasure propagation; quarantine over deletion |
| 6 (Escalation) | Classification confidence < 0.5 always escalates to human |
| 7 (Auditability) | All gate results logged with input signals and conclusions |
| 9 (Bounded Autonomy) | Agents classify and recommend; humans make final legal determinations |
| 10 (Stakeholder Pluralism) | GDPR data subjects, rightsholders, and regulators are all considered |

---

## Open Questions

1. **TDM opt-out enforcement**: Should `gdpr_provenance_check` automatically reject sources with TDM opt-out flags in `robots.txt`, or flag for human review? Recommendation: automatic rejection for Tier 1 systems, human review for Tier 3.

2. **WCAG scope for audio output**: Guitar Alchemist generates audio. WCAG 1.2.1 requires transcripts for pre-recorded audio. Should IxQL mandate transcripts for all audio deployments, or only web-published ones? Recommendation: web-published only; embedded/API audio is out of scope.

3. **Copyright similarity threshold**: The 0.80 embedding similarity threshold for output screening is conservative. False positive rate needs calibration against a known-safe baseline. Recommendation: start at 0.85, lower to 0.80 after calibration.

4. **Catala PoC priority**: The Catala encoding is valuable for formal verification but is not on the critical path. Recommendation: deprioritize until Phase 2 policy YAML is complete.
