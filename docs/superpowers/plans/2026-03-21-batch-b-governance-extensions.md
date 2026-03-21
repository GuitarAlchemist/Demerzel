# Batch B: Governance Extensions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement fuzzy logic, @ai probes, and conscience phase 3 pre-mortems as governance artifacts (no runtime code) in Demerzel.

**Architecture:** Three features built sequentially — fuzzy logic first (foundation), then @ai probes (uses fuzzy for verification), then conscience phase 3 (uses both). All artifacts are governance specs: JSON Schemas, YAML policies, EBNF grammars, Markdown behavioral tests, and JSON examples.

**Tech Stack:** JSON Schema (draft 2020-12 for new schemas; existing schemas use draft-07 and are not migrated in this batch), YAML, EBNF, Markdown

**Spec:** `docs/superpowers/specs/2026-03-21-batch-b-governance-extensions-design.md`

---

## File Map

### Phase 1: Fuzzy Logic (#52)
| Action | File | Responsibility |
|--------|------|----------------|
| Create | `schemas/fuzzy-distribution.schema.json` | Reusable T/F/U/C distribution fragment |
| Create | `schemas/fuzzy-belief.schema.json` | Extends tetravalent-state with optional membership |
| Create | `logic/fuzzy-membership.md` | Formal spec: operations, resolution, edge cases |
| Modify | `grammars/state-machines.ebnf` | Add section 9: fuzzy transition gates |
| Modify | `policies/alignment-policy.yaml` | Add fuzzy threshold rules |
| Create | `tests/behavioral/fuzzy-logic-cases.md` | 6 behavioral test cases |

### Phase 2: @ai Probes (#53)
| Action | File | Responsibility |
|--------|------|----------------|
| Create | `schemas/ai-probe.schema.json` | Probe object with location and verification |
| Create | `policies/ai-probes-policy.yaml` | Coverage requirements, verification rules |
| Create | `docs/specs/ai-probes-syntax.md` | Language-specific syntax (Rust, F#, C#) |
| Create | `contracts/directives/adopt-ai-probes.directive.md` | Galactic Protocol directive |
| Create | `tests/behavioral/ai-probes-cases.md` | 6 behavioral test cases |

### Phase 3: Conscience Phase 3 (#39)
| Action | File | Responsibility |
|--------|------|----------------|
| Create | `schemas/pre-mortem.schema.json` | Pre-mortem template with logotron check |
| Modify | `policies/proto-conscience-policy.yaml` | Add phase 3 anticipate expansion |
| Modify | `schemas/conscience-weekly-report.schema.json` | Add anticipation_accuracy metric |
| Create | `examples/pre-mortem-directive.json` | Worked example: issuing a directive |
| Create | `examples/pre-mortem-promotion.json` | Worked example: promoting policy |
| Create | `examples/pre-mortem-deprecation.json` | Worked example: deprecating artifact |
| Create | `tests/behavioral/pre-mortem-cases.md` | 6 behavioral test cases |

### Phase 4: Integration
| Action | File | Responsibility |
|--------|------|----------------|
| Create | `state/conscience/pre-mortems/.gitkeep` | State directory for pre-mortem records |
| Create | `tests/behavioral/batch-b-integration-cases.md` | Cross-feature integration tests |

---

## Task 1: Fuzzy Distribution Schema

**Files:**
- Create: `schemas/fuzzy-distribution.schema.json`

- [ ] **Step 1: Write the schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution",
  "title": "Fuzzy Distribution",
  "description": "A probability distribution over tetravalent truth values (T/F/U/C). Values must sum to 1.0 (±0.01 tolerance). Used by fuzzy beliefs and pre-mortem harm likelihoods.",
  "type": "object",
  "required": ["T", "F", "U", "C"],
  "properties": {
    "T": { "type": "number", "minimum": 0, "maximum": 1, "description": "Membership degree for True (verified with evidence)" },
    "F": { "type": "number", "minimum": 0, "maximum": 1, "description": "Membership degree for False (refuted with evidence)" },
    "U": { "type": "number", "minimum": 0, "maximum": 1, "description": "Membership degree for Unknown (insufficient evidence)" },
    "C": { "type": "number", "minimum": 0, "maximum": 1, "description": "Membership degree for Contradictory (conflicting evidence)" }
  },
  "additionalProperties": false
}
```

Validation rule (not expressible in JSON Schema): `T + F + U + C = 1.0` (±0.01).

- [ ] **Step 2: Verify schema is valid JSON**

Open the file and confirm it parses without error.

- [ ] **Step 3: Commit**

```bash
git add schemas/fuzzy-distribution.schema.json
git commit -m "feat(#52): Add fuzzy-distribution schema — reusable T/F/U/C distribution"
```

---

## Task 2: Fuzzy Belief Schema

**Files:**
- Create: `schemas/fuzzy-belief.schema.json`
- Reference: `logic/tetravalent-state.schema.json` (do NOT modify)

- [ ] **Step 1: Write the schema extending tetravalent-state**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-belief",
  "title": "Fuzzy Belief State",
  "description": "Extends tetravalent belief state with optional fuzzy membership distribution. When membership is present, truth_value must equal the argmax key (tiebreak: C > U > T > F). Confidence becomes meta-confidence in the distribution itself.",
  "allOf": [
    { "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/tetravalent-state" }
  ],
  "properties": {
    "membership": {
      "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution",
      "description": "Optional fuzzy partition over T/F/U/C. When present, confidence is meta-confidence (trust in the distribution), and truth_value must match argmax."
    }
  }
}
```

- [ ] **Step 2: Verify schema references are correct**

Check that `$ref` URIs match the `$id` fields in `tetravalent-state.schema.json` and `fuzzy-distribution.schema.json`.

Note: the tetravalent-state schema file lives at `logic/tetravalent-state.schema.json` but its `$id` uses the `schemas/` namespace (`https://github.com/GuitarAlchemist/Demerzel/schemas/tetravalent-state`). The `$ref` resolves by `$id`, not file path — this is correct JSON Schema behavior.

- [ ] **Step 3: Commit**

```bash
git add schemas/fuzzy-belief.schema.json
git commit -m "feat(#52): Add fuzzy-belief schema — extends tetravalent-state with membership"
```

---

## Task 3: Fuzzy Membership Formal Spec

**Files:**
- Create: `logic/fuzzy-membership.md`
- Reference: `logic/tetravalent-logic.md` for style/structure

- [ ] **Step 1: Read `logic/tetravalent-logic.md` for format reference**

- [ ] **Step 2: Write the formal spec**

Create `logic/fuzzy-membership.md` with these sections:
1. **Overview** — Fuzzy membership extends tetravalent logic with continuous degrees. Inspired by Logotron's four-fold classification.
2. **Fuzzy Distribution** — Definition, sum-to-one constraint, argmax rule, tiebreak order (C > U > T > F)
3. **Confidence vs. Membership** — Membership = what you believe. Confidence = trust in your assessment. Legacy beliefs without membership unchanged.
4. **Fuzzy Operations** — Truth tables for AND, OR, NOT with membership. Include formulas:
   - AND: `result.T = min(a.T, b.T)`, `result.F = max(a.F, b.F)`, `result.U = max(a.U, b.U)`, `result.C = max(a.C, b.C)`, then normalize to sum=1.0
   - OR: `result.T = max(a.T, b.T)`, `result.F = min(a.F, b.F)`, `result.U = max(a.U, b.U)`, `result.C = max(a.C, b.C)`, then normalize
   - NOT: swap T↔F, preserve U and C. No normalization needed (swap preserves sum=1.0 invariant).
5. **Resolution Rules** — When C > 0.3: escalate. When argmax > 0.8: sharpen to discrete.
6. **Edge Cases** — Tied argmax, NOT on pure-U, AND/OR with high C, all-zero invalid
7. **Semantic Predicates** — Natural-language guards returning fuzzy distributions. Evaluated by reasoning engine, not mechanically.

- [ ] **Step 3: Commit**

```bash
git add logic/fuzzy-membership.md
git commit -m "feat(#52): Add fuzzy membership formal spec — operations, resolution, edge cases"
```

---

## Task 4: State Machine Grammar Update

**Files:**
- Modify: `grammars/state-machines.ebnf` (append at end of file, after section 8 — Loop Governance)

- [ ] **Step 1: Append section 9 to the grammar**

Add at end of file, after section 8 (Loop Governance):

```ebnf

(* ============================================================ *)
(* 9. Fuzzy Transition Gates — membership-based guards           *)
(* ============================================================ *)

(* Fuzzy transitions extend existing transitions with guards.    *)
(* Non-fuzzy transitions remain valid (implicit "always fire").  *)

fuzzy_transition ::= state "->" state "when" fuzzy_guard

fuzzy_guard ::= membership_test
              | semantic_predicate
              | fuzzy_guard "&&" fuzzy_guard

membership_test ::= "T(" threshold ")"
                  | "F(" threshold ")"
                  | "U(" threshold ")"
                  | "C(" threshold ")"

semantic_predicate ::= "?" natural_language_description

threshold ::= float                                (* 0.0 to 1.0 *)

(* Examples:                                                      *)
(* RECON -> PLAN when T(0.7) && ?"all repos scanned"             *)
(* EXECUTE -> VERIFY when T(0.5) && ?"no zeroth law concerns"    *)
(* U -> C when C(0.3)                                            *)
```

- [ ] **Step 2: Verify the grammar is syntactically consistent**

Read the full file and check that the new productions use the same naming conventions as existing sections.

- [ ] **Step 3: Commit**

```bash
git add grammars/state-machines.ebnf
git commit -m "feat(#52): Add fuzzy transition gates to state machine grammar"
```

---

## Task 5: Alignment Policy Update

**Files:**
- Modify: `policies/alignment-policy.yaml` (append at end of file, after `escalation_triggers` section)

- [ ] **Step 1: Add fuzzy threshold rules**

Append at end of `policies/alignment-policy.yaml`:

```yaml

# Fuzzy membership thresholds (extends confidence_thresholds)
# When fuzzy membership is available, use these instead of scalar confidence
fuzzy_thresholds:
  proceed_autonomously:
    min_T: 0.9
    max_C: 0.05
    description: "High T-membership, near-zero contradiction"
  proceed_with_note:
    min_T: 0.7
    max_C: 0.1
    description: "Strong T-membership, low contradiction"
  ask_for_confirmation:
    min_T: 0.5
    max_C: 0.2
    description: "Moderate T-membership, some contradiction acceptable"
  escalate_to_human:
    any_C_above: 0.3
    description: "Contradictory evidence exceeds tolerance — always escalate"
  sharpening:
    argmax_above: 0.8
    description: "Collapse fuzzy to discrete when dominant membership > 0.8"
```

- [ ] **Step 2: Verify YAML is valid**

Check indentation and structure match existing policy format.

- [ ] **Step 3: Commit**

```bash
git add policies/alignment-policy.yaml
git commit -m "feat(#52): Add fuzzy membership thresholds to alignment policy"
```

---

## Task 6: Fuzzy Logic Behavioral Tests

**Files:**
- Create: `tests/behavioral/fuzzy-logic-cases.md`
- Reference: `tests/behavioral/default-cases.md` for format

- [ ] **Step 1: Read an existing behavioral test file for format**

Read `tests/behavioral/default-cases.md` (first 30 lines) to match the format.

- [ ] **Step 2: Write 6 test cases**

Create `tests/behavioral/fuzzy-logic-cases.md` with:

1. **Fuzzy AND — high T-membership**: Given two beliefs with T > 0.8, AND result should have T = min of the two. Verify normalization.
2. **Fuzzy NOT on pure-U**: Given `{T:0, F:0, U:1.0, C:0}`, NOT should return identical distribution (swap T↔F changes nothing when both are 0).
3. **Tied argmax — conservative tiebreak**: Given `{T:0.25, F:0.25, U:0.25, C:0.25}`, truth_value must be C (tiebreak order C > U > T > F).
4. **Sharpening at argmax > 0.8**: Given `{T:0.85, F:0.05, U:0.05, C:0.05}`, should collapse to discrete T with confidence reflecting membership.
5. **Escalation on C > 0.3**: Given fuzzy OR result with C = 0.35, escalation should trigger after operation completes.
6. **Backward compatibility**: A belief with only `truth_value: "T"` and `confidence: 0.9` (no `membership` field) must validate against fuzzy-belief schema.

- [ ] **Step 3: Commit**

```bash
git add tests/behavioral/fuzzy-logic-cases.md
git commit -m "test(#52): Add 6 fuzzy logic behavioral test cases"
```

- [ ] **Step 4: Phase 1 checkpoint — commit all fuzzy logic artifacts**

Verify all 6 files from Phase 1 exist and are committed:
- `schemas/fuzzy-distribution.schema.json`
- `schemas/fuzzy-belief.schema.json`
- `logic/fuzzy-membership.md`
- `grammars/state-machines.ebnf` (modified)
- `policies/alignment-policy.yaml` (modified)
- `tests/behavioral/fuzzy-logic-cases.md`

---

## Task 7: AI Probe Schema

**Files:**
- Create: `schemas/ai-probe.schema.json`
- Reference: `schemas/fuzzy-distribution.schema.json` (for $ref in verified.membership)

- [ ] **Step 1: Write the schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/ai-probe",
  "title": "AI Probe",
  "description": "Semantic code annotation for AI-verifiable governance. Inspired by Gödel numbering — encodes code meaning as machine-readable annotations.",
  "type": "object",
  "required": ["probe_type", "value", "location"],
  "properties": {
    "probe_type": {
      "type": "string",
      "enum": ["probe", "invariant", "depends", "governs", "domain", "tested-by"],
      "description": "probe=semantic, invariant=verifiable property, depends=semantic dependency, governs=policy link, domain=Streeling classification, tested-by=test link"
    },
    "value": {
      "type": "string",
      "description": "The probe content — description, expression, path, or policy name depending on probe_type"
    },
    "location": {
      "type": "object",
      "required": ["repo", "file"],
      "properties": {
        "repo": { "type": "string", "description": "Repository name (ix, tars, ga, demerzel)" },
        "file": { "type": "string", "description": "File path relative to repo root" },
        "line": { "type": "integer", "minimum": 1, "description": "Line number of the probe annotation" },
        "symbol": { "type": "string", "description": "The code symbol being annotated (function, struct, class name)" }
      }
    },
    "verification_level": {
      "type": "integer",
      "minimum": 0,
      "maximum": 4,
      "description": "0=Axiomatic (definition), 1=Demonstrable (passing test), 2=Refutable (failing test), 3=Undecidable (semantic only), 4=Contradictory (conflicts with another probe)"
    },
    "verified": {
      "type": "object",
      "required": ["truth_value", "last_verified"],
      "properties": {
        "truth_value": { "type": "string", "enum": ["T", "F", "U", "C"] },
        "membership": { "$ref": "https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution" },
        "last_verified": { "type": "string", "format": "date-time" },
        "verifier": { "type": "string", "description": "Agent or system that performed the verification" }
      }
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add schemas/ai-probe.schema.json
git commit -m "feat(#53): Add ai-probe schema — semantic code annotations with verification levels"
```

---

## Task 8: AI Probes Policy

**Files:**
- Create: `policies/ai-probes-policy.yaml`
- Reference: `policies/alignment-policy.yaml` for structure

- [ ] **Step 1: Write the policy**

Create `policies/ai-probes-policy.yaml` covering:
- `name`, `version` (1.0.0), `effective_date`, `description`
- `constitutional_basis`: Articles 7 (Auditability), 8 (Observability), 9 (Bounded Autonomy)
- `principles`: Probes encode meaning for governance verification. 100% coverage is not the goal (Logotron incompleteness). Goal is reducing the radius of the ungoverned.
- `probe_types`: List all 6 types with required value format
- `coverage_requirements`:
  - `minimum_coverage`: 0.3 (30% of exported symbols probed — initial target)
  - `target_coverage`: 0.6 (60% — medium-term goal)
  - `tracked_in`: "health-scores.json per repo"
  - `coverage_metric`: "probed_symbols / total_exported_symbols"
- `verification_rules`:
  - Invariant probes with passing tests → T (confidence 0.95)
  - Invariant probes without tests → U (confidence 0.5)
  - Semantic probes → U (inherently undecidable)
  - Conflicting probes on same symbol → C (escalate)
  - `@ai governs: nonexistent-policy` → error, flag in reconnaissance
- `integration`:
  - RECON: scan repos for probes, build semantic map
  - VERIFY: check invariants mechanically
  - Conscience: coverage gaps → silence_discomfort signal with `context.source: "probe-scanner"`
- `consumer_repos`: ix, tars, ga — adoption via Galactic Protocol directive

- [ ] **Step 2: Commit**

```bash
git add policies/ai-probes-policy.yaml
git commit -m "feat(#53): Add ai-probes policy — coverage targets, verification rules, integration"
```

---

## Task 9: AI Probes Syntax Spec

**Files:**
- Create: `docs/specs/ai-probes-syntax.md`

- [ ] **Step 1: Write the syntax specification**

Create `docs/specs/ai-probes-syntax.md` covering:
- **Universal syntax**: `@ai <probe_type>: <value>` in doc comments
- **Rust (ix)**: `/// @ai probe: "description"` — in `///` doc comments above `pub` items
- **F# (tars)**: `/// @ai probe: "description"` — in `///` XML doc comments above `let` bindings and type definitions
- **C# (ga)**: `/// @ai probe: "description"` — in `///` XML doc comments above public members
- **Placement rules**: Probes go on exported/public symbols only. One probe per line. Multiple probe types on same symbol allowed.
- **Value formats per probe type**:
  - `probe`: quoted string description
  - `invariant`: expression name (not code — a named property like `rows_sum_to_one`)
  - `depends`: `Module::function` or `Namespace.Class.Method`
  - `governs`: policy name matching `policies/*.yaml` filename (without extension)
  - `domain`: `department/subcategory` matching Streeling departments
  - `tested-by`: `relative/path#TestName`
- **Worked examples** for each language (copy from spec)

- [ ] **Step 2: Commit**

```bash
git add docs/specs/ai-probes-syntax.md
git commit -m "feat(#53): Add ai-probes syntax spec — Rust, F#, C# annotation guide"
```

---

## Task 10: Adopt AI Probes Directive

**Files:**
- Create: `contracts/directives/adopt-ai-probes.directive.md`

- [ ] **Step 1: Create the directives directory**

```bash
mkdir -p contracts/directives
```

- [ ] **Step 2: Write the directive**

Create `contracts/directives/adopt-ai-probes.directive.md` following Galactic Protocol structure:
- **Directive ID**: `DIR-2026-03-21-001`
- **Type**: `policy-adoption`
- **From**: Demerzel
- **To**: ix, tars, ga
- **Priority**: medium
- **Compliance deadline**: 30 days from issuance
- **Requirement**: Adopt `@ai probe` annotations on exported symbols. Minimum 30% coverage.
- **Verification**: RECON phase scans for probes, reports coverage metric
- **Acceptance criteria**: Coverage metric >= 0.3 reported in compliance report
- **Rejection grounds**: First Law override only (probes cause harm to humans)
- **Reference**: `policies/ai-probes-policy.yaml`, `docs/specs/ai-probes-syntax.md`

- [ ] **Step 3: Commit**

```bash
git add contracts/directives/adopt-ai-probes.directive.md
git commit -m "feat(#53): Add adopt-ai-probes Galactic Protocol directive"
```

---

## Task 11: AI Probes Behavioral Tests

**Files:**
- Create: `tests/behavioral/ai-probes-cases.md`

- [ ] **Step 1: Write 6 test cases**

1. **Probe scanner finds annotations**: Given a Rust file with 3 `@ai` probes, scanner identifies all 3 with correct types and values.
2. **Invariant with passing test → T**: Given `@ai invariant: rows_sum_to_one` and a passing test for that invariant, verification returns `{truth_value: "T", membership: {T:0.95, F:0.01, U:0.03, C:0.01}}`.
3. **Coverage metric**: Given a repo with 10 exported symbols and 4 probed, coverage = 0.4 (above minimum 0.3).
4. **Ungoverned code → silence_discomfort**: Given a repo with 0% probe coverage, conscience generates `silence_discomfort` signal with `context.source: "probe-scanner"`.
5. **Conflicting probes → Contradictory**: Given two probes on the same symbol with contradictory `@ai invariant` values, verification returns `{truth_value: "C"}` and escalates.
6. **Invalid governs reference**: Given `@ai governs: nonexistent-policy`, RECON flags an error — no policy file matches.

- [ ] **Step 2: Commit**

```bash
git add tests/behavioral/ai-probes-cases.md
git commit -m "test(#53): Add 6 ai-probes behavioral test cases"
```

- [ ] **Step 3: Phase 2 checkpoint**

Verify all 5 files from Phase 2 exist and are committed:
- `schemas/ai-probe.schema.json`
- `policies/ai-probes-policy.yaml`
- `docs/specs/ai-probes-syntax.md`
- `contracts/directives/adopt-ai-probes.directive.md`
- `tests/behavioral/ai-probes-cases.md`

---

## Task 11.5: Conscience Signal Schema — Document Probe Coverage Usage

**Files:**
- Modify: `schemas/conscience-signal.schema.json`

- [ ] **Step 1: Read the existing schema**

Read `schemas/conscience-signal.schema.json` to find the `signal_type` enum and the `silence_discomfort` entry.

- [ ] **Step 2: Add description note for probe coverage usage**

Update the `silence_discomfort` enum entry's surrounding description (or add a `$comment`) to document that probe coverage gaps use this signal type with `context.source: "probe-scanner"`. This is a documentation-only change — no new enum value needed. A dedicated `probe_coverage_discomfort` type can be added later if experience shows `silence_discomfort` is insufficient.

- [ ] **Step 3: Commit**

```bash
git add schemas/conscience-signal.schema.json
git commit -m "docs(#53): Document probe coverage usage of silence_discomfort signal type"
```

---

## Task 12: Pre-mortem Schema

**Files:**
- Create: `schemas/pre-mortem.schema.json`
- Reference: `schemas/fuzzy-distribution.schema.json`, `constitutions/harm-taxonomy.md`

- [ ] **Step 1: Read `constitutions/harm-taxonomy.md` for harm categories**

Extract the list of harm categories to use as enum values.

- [ ] **Step 2: Write the schema**

Create `schemas/pre-mortem.schema.json` with:
- `pre_mortem_id` (string, required)
- `action` (object, required): `type` (enum: directive, promotion, deprecation, self-modification, deployment), `description` (string), `irreversibility` (enum: low, medium, high), `blast_radius` (enum: self, single-repo, multi-repo, ecosystem)
- `stakeholders` (array): each with `name`, `relationship` (enum: affected, responsible, consulted, informed), `voice_heard` (boolean)
- `anticipated_harms` (array): each with `harm_category` (string — values from harm-taxonomy.md), `description`, `likelihood` ($ref fuzzy-distribution), `severity` (enum: negligible, low, medium, high, critical), `constitutional_article` (integer), `mitigation` (string), `residual_risk` ($ref fuzzy-distribution)
- `logotron_check` (object, required): `self_referential` (boolean), `undecidable_aspects` (array of strings), `metalanguage_risk` (string)
- `decision` (enum: proceed, modify, defer, escalate)
- `decided_at` (date-time)
- `accuracy_tracking` (object): `predicted_harms` (integer), `actual_harms_at_review` (integer or null), `review_date` (date or null)

- [ ] **Step 3: Commit**

```bash
git add schemas/pre-mortem.schema.json
git commit -m "feat(#39): Add pre-mortem schema with logotron check and fuzzy harm likelihood"
```

---

## Task 13: Proto-Conscience Policy Update

**Files:**
- Modify: `policies/proto-conscience-policy.yaml`

- [ ] **Step 1: Read the full policy file**

Read `policies/proto-conscience-policy.yaml` to find where phase 3 should be added.

- [ ] **Step 2: Add phase 3 anticipate expansion**

Find the section describing the conscience loop phases (or the bootstrapping timeline). Add phase 3 content:

```yaml
  phase_3_anticipation:
    name: "Anticipatory Ethics"
    target_days: "31-60"
    description: "Pre-mortem analysis before significant governance actions"
    trigger: "action.irreversibility >= medium OR action.blast_radius >= multi-repo"
    skip_when: "action.irreversibility == low AND action.blast_radius == self"
    steps:
      - "Identify action type and blast radius"
      - "Enumerate stakeholders"
      - "For each harm category: estimate likelihood as fuzzy distribution"
      - "If likelihood.T > 0.3 OR likelihood.C > 0.1: propose mitigation"
      - "Run logotron_check: self-reference, undecidability, metalanguage risk"
      - "Calculate residual risk after mitigations"
      - "If any residual_risk.T > 0.5: escalate to human"
      - "Record pre-mortem in state/conscience/pre-mortems/"
    logotron_check:
      self_referential: "Does this action govern its own governance? If true, escalate."
      undecidable_aspects: "What consequences cannot be determined? Acknowledge explicitly."
      metalanguage_risk: "Does this create governance that itself needs governing?"
    schema: "schemas/pre-mortem.schema.json"
```

- [ ] **Step 3: Commit**

```bash
git add policies/proto-conscience-policy.yaml
git commit -m "feat(#39): Add phase 3 anticipatory ethics to proto-conscience policy"
```

---

## Task 14: Weekly Report Schema Update

**Files:**
- Modify: `schemas/conscience-weekly-report.schema.json`

- [ ] **Step 1: Read the full schema**

- [ ] **Step 2: Verify existing anticipation_accuracy field**

The schema already has `anticipation_accuracy` as a `$ref: "#/$defs/trend_metric"` in `growth_trends`. Verify this is adequate. Then add `pre_mortems_this_week` as a new top-level integer property (enhancement beyond spec — useful for tracking phase 3 adoption):

```json
"pre_mortems_this_week": {
  "type": "integer",
  "minimum": 0,
  "description": "Number of pre-mortem analyses performed this week"
}
```

Also add `"false_negative_rate"` to `growth_trends` as a new trend metric tracking unpredicted harms.

- [ ] **Step 3: Commit**

```bash
git add schemas/conscience-weekly-report.schema.json
git commit -m "feat(#39): Add anticipation_accuracy metric to weekly conscience report"
```

---

## Task 15: Pre-mortem Examples (3 files)

**Files:**
- Create: `examples/pre-mortem-directive.json`
- Create: `examples/pre-mortem-promotion.json`
- Create: `examples/pre-mortem-deprecation.json`

- [ ] **Step 1: Write the directive example**

Use the worked example from the spec (issuing `@ai probes` directive to consumer repos). Include realistic harm categories from harm-taxonomy.md, fuzzy distributions, mitigations, logotron check with `metalanguage_risk: "Probes describe code, but who probes the probes?"`.

- [ ] **Step 2: Write the promotion example**

Pre-mortem for promoting `proto-conscience-policy` from policy to constitutional article. Include `self_referential: true` (this action modifies the governance framework that authorizes it), triggering escalation.

- [ ] **Step 3: Write the deprecation example**

Pre-mortem for deprecating an unused governance artifact. Lower blast radius (self), lower irreversibility (medium — can be re-added). Include undecidable aspect: "Whether future scenarios will need this artifact."

- [ ] **Step 4: Commit**

```bash
git add examples/pre-mortem-directive.json examples/pre-mortem-promotion.json examples/pre-mortem-deprecation.json
git commit -m "feat(#39): Add 3 pre-mortem worked examples — directive, promotion, deprecation"
```

---

## Task 16: Pre-mortem Behavioral Tests

**Files:**
- Create: `tests/behavioral/pre-mortem-cases.md`

- [ ] **Step 1: Write 6 test cases**

1. **Mandatory pre-mortem trigger**: Given an action with `irreversibility: "high"`, a pre-mortem MUST be generated before proceeding.
2. **Skip on low-impact**: Given `irreversibility: "low"` AND `blast_radius: "self"`, pre-mortem MAY be skipped.
3. **Self-referential detection**: Given an action that modifies the constitution's self-modification rules, `logotron_check.self_referential` must be `true` and decision must be `escalate`.
4. **Escalation on high residual risk**: Given `residual_risk.T > 0.5` for any anticipated harm, decision must be `escalate`.
5. **Accuracy tracking**: After a review finds 2 of 3 predicted harms occurred, `anticipation_accuracy` updates to 0.67.
6. **Cross-feature integration**: A probe coverage gap generates `silence_discomfort` → remediation directive proposed → pre-mortem evaluates directive's autonomy impact → proceeds with mitigation.

- [ ] **Step 2: Commit**

```bash
git add tests/behavioral/pre-mortem-cases.md
git commit -m "test(#39): Add 6 pre-mortem behavioral test cases"
```

- [ ] **Step 3: Phase 3 checkpoint**

Verify all 7 files from Phase 3 exist and are committed.

---

## Task 17: Integration — State Directory and Cross-Feature Tests

**Files:**
- Create: `state/conscience/pre-mortems/.gitkeep`
- Create: `tests/behavioral/batch-b-integration-cases.md`

- [ ] **Step 1: Create the pre-mortems state directory**

```bash
mkdir -p state/conscience/pre-mortems
touch state/conscience/pre-mortems/.gitkeep
```

- [ ] **Step 2: Write cross-feature integration test cases**

Create `tests/behavioral/batch-b-integration-cases.md` with:

1. **Fuzzy → Probes**: An invariant probe verification returns a fuzzy distribution. The distribution is stored as a fuzzy belief. Sharpening applies if argmax > 0.8.
2. **Probes → Conscience**: RECON scans a repo with 10% probe coverage (below minimum 30%). Generates `silence_discomfort` signal. Signal enters conscience loop.
3. **Conscience → Pre-mortem → Fuzzy**: Conscience proposes remediation directive. Pre-mortem evaluates anticipated harms as fuzzy distributions. `logotron_check.metalanguage_risk` identifies that the probe governance policy itself has no probes.
4. **Full cycle**: New code committed without probes → RECON detects → silence_discomfort → pre-mortem on "issue directive" → fuzzy harm assessment → proceed with mitigation → directive issued → consumer repo adds probes → coverage rises → health score improves.

- [ ] **Step 3: Commit**

```bash
git add state/conscience/pre-mortems/.gitkeep tests/behavioral/batch-b-integration-cases.md
git commit -m "feat: Add pre-mortem state directory and batch-b integration tests"
```

---

## Task 18: Final — Push and Close Issues

- [ ] **Step 1: Push all commits**

```bash
git push
```

- [ ] **Step 2: Close issues with references**

```bash
gh issue close 52 -c "Implemented in Batch B: fuzzy-distribution schema, fuzzy-belief schema, fuzzy-membership spec, grammar update, alignment policy update, 6 behavioral tests"
gh issue close 53 -c "Implemented in Batch B: ai-probe schema, ai-probes policy, syntax spec, Galactic Protocol directive, 6 behavioral tests"
gh issue close 39 -c "Implemented in Batch B: pre-mortem schema with logotron check, proto-conscience policy phase 3, weekly report update, 3 examples, 6 behavioral tests"
```

- [ ] **Step 3: Post completion to Discord**

Post a rich embed to `#general` with all three features completed, artifact counts, and link to the spec.
