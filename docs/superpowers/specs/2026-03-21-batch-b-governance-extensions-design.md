# Batch B: Governance Extensions Design

**Date:** 2026-03-21
**Issues:** #52 (Fuzzy Logic), #53 (@ai Probes), #39 (Conscience Phase 3)
**Scope:** Demerzel governance artifacts only (schemas, policies, grammars, behavioral tests). Consumer repo implementation via Galactic Protocol directives.

---

## Foundational Inspiration: The Logotron

Jean-Pierre Petit's *Logotron* comic establishes key ideas that underpin all three features:

1. **Four-fold proposition classification** — Petit shows that formal systems classify propositions as *axioms* (foundational), *demonstrable* (provably true), *refutable* (provably false), or *undecidable* (neither). This maps directly to Demerzel's tetravalent logic: T (demonstrable), F (refutable), U (undecidable), C (contradictory — Petit's paradoxes). Fuzzy membership extends this by adding *degrees* within each category.

2. **Gödel numbering** — The Logotron encodes entire propositions and proofs as whole numbers via prime factorization, making them mechanically verifiable. This is the intellectual ancestor of `@ai probes` — encoding semantic meaning as machine-readable annotations that governance can scan and verify without reading the code itself.

3. **Incompleteness as feature** — Gödel's theorem proves no consistent formal system can be complete. Conscience phase 3 embraces this: pre-mortems acknowledge that governance cannot anticipate all consequences. The anticipatory step is not about achieving certainty but about *reducing the radius of the unknown*.

4. **Metalanguage recursion** — Languages contain their own metalanguages, creating self-referential loops. This is why conscience must monitor itself (observability policy) and why probes need a governance layer above them (the probes policy governs how probes are used).

---

## Feature 1: Fuzzy Membership for Tetravalent Logic (#52)

### Concept

Extend tetravalent truth values with continuous membership degrees. A fuzzy value preserves the discrete T/F/U/C classification while adding a `membership` field (0.0–1.0) expressing the degree of belief.

From the Logotron: Petit observes that not all truths are equally accessible — some follow directly from axioms, others require long chains of evidence. Membership degree is analogous: it captures how much evidential weight supports each truth value, not proof complexity but evidential density.

### Design: Layered Extension (Backward Compatible)

Fuzzy membership **layers on top of** existing tetravalent logic. A standard belief `{truth_value: "T", confidence: 0.85}` remains valid. A fuzzy belief adds `membership`:

```json
{
  "proposition": "Consumer repos adopt governance probes",
  "truth_value": "U",
  "confidence": 0.6,
  "membership": {
    "T": 0.3,
    "F": 0.1,
    "U": 0.5,
    "C": 0.1
  }
}
```

The `membership` object distributes belief across all four truth values. The `truth_value` field reflects the argmax (highest membership). This is a **fuzzy partition** — memberships sum to 1.0.

### Semantic Clarification: confidence vs. membership

- **`membership`** — Distribution of belief across T/F/U/C. Expresses *what* you believe.
- **`confidence`** — Meta-confidence in the membership distribution itself. Expresses *how much you trust your own assessment*. A confidence of 0.9 with membership `{T:0.5, U:0.5}` means "I'm quite sure it's genuinely ambiguous." A confidence of 0.3 means "I'm not even sure about my uncertainty distribution."
- **`truth_value`** — Argmax of membership. Must match; enforced as a validation rule (not schema-expressible).

When `membership` is absent (legacy beliefs), `confidence` retains its original meaning from `tetravalent-state.schema.json`.

### Schema Design: Reusable fuzzy-distribution fragment

To avoid duplication between fuzzy beliefs and pre-mortem harm likelihoods, define a shared schema fragment:

```json
{
  "$id": "fuzzy-distribution",
  "type": "object",
  "properties": {
    "T": { "type": "number", "minimum": 0, "maximum": 1 },
    "F": { "type": "number", "minimum": 0, "maximum": 1 },
    "U": { "type": "number", "minimum": 0, "maximum": 1 },
    "C": { "type": "number", "minimum": 0, "maximum": 1 }
  },
  "required": ["T", "F", "U", "C"]
}
```

**Validation rules** (enforced by governance, not JSON Schema):
- `T + F + U + C = 1.0` (±0.01 tolerance for floating point)
- `truth_value` must equal argmax key. On tie, prefer in order: C > U > T > F (conservative — contradictions and unknowns surface first)

The fuzzy belief schema (`schemas/fuzzy-belief.schema.json`) extends existing `tetravalent-state.schema.json` via `allOf` + `$ref`, adding the optional `membership` property.

### Fuzzy Transition Gates

For state machine transitions (grammars/state-machines.ebnf), add gates that fire based on membership thresholds:

```ebnf
fuzzy_transition ::= state "->" state "when" fuzzy_guard
fuzzy_guard      ::= membership_test | semantic_predicate | fuzzy_guard "&&" fuzzy_guard
membership_test  ::= "T(" threshold ")" | "F(" threshold ")" | "U(" threshold ")" | "C(" threshold ")"
semantic_predicate ::= "?" natural_language_description
threshold        ::= float  (* 0.0 to 1.0 *)
```

Example: `RECON -> PLAN when T(0.7) && ?"all repos scanned"` — transition fires when T-membership exceeds 0.7 AND the semantic predicate evaluates to true.

### Semantic Predicates

Semantic predicates are natural-language guards evaluated by the reasoning engine (tars). They bridge formal logic with contextual judgment — the Logotron's "metalanguage" level. The predicate `?"all repos scanned"` is not mechanically checkable in Demerzel; it requires an agent to assess and return a fuzzy truth value.

### Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Spec | `logic/fuzzy-membership.md` | Formal spec: fuzzy partitions, operations, resolution rules |
| Schema | `schemas/fuzzy-belief.schema.json` | JSON Schema extending tetravalent-state with membership |
| Grammar | `grammars/state-machines.ebnf` (update) | Add fuzzy_transition and fuzzy_guard productions |
| Policy | `policies/alignment-policy.yaml` (update) | Add fuzzy threshold rules to confidence bands |
| Tests | `tests/behavioral/fuzzy-logic-cases.md` | 6+ test cases |

### Fuzzy Operations (from Logotron truth tables, extended)

| Operation | Definition |
|-----------|-----------|
| Fuzzy AND | `min(a.T, b.T)` for T, `max(a.C, b.C)` for C |
| Fuzzy OR | `max(a.T, b.T)` for T, `max(a.C, b.C)` for C |
| Fuzzy NOT | Swap T↔F memberships, preserve U and C |
| Resolution | When C > 0.3, trigger escalation (contradictory evidence) |
| Sharpening | Collapse fuzzy to discrete when argmax membership > 0.8 |

### Edge Cases

- **Tied argmax** (e.g., `{T:0.25, F:0.25, U:0.25, C:0.25}`): Use conservative tiebreak order C > U > T > F. Result: truth_value = C, triggering escalation.
- **NOT on pure-U** (`{T:0, F:0, U:1.0, C:0}`): NOT swaps T↔F but leaves U and C unchanged. Result is identical to input — correct, because negating pure uncertainty yields uncertainty.
- **AND/OR with C > 0.3**: Escalation fires *after* the operation completes. The operation result is computed, then the resolution rule checks if result.C > 0.3.
- **All-zero membership**: Invalid — memberships must sum to 1.0.

### Grammar Backward Compatibility

Existing non-fuzzy transitions (`state -> state`) remain valid. `fuzzy_transition` is a **new production** used alongside, not replacing, existing transitions. Non-fuzzy transitions are implicitly `when T(0.0)` (always fire).

---

## Feature 2: @ai Probes — Semantic Code Annotations (#53)

### Concept

Define a standardized annotation syntax for code across all repos (ix/Rust, tars/F#, ga/C#) that encodes semantic meaning, invariants, dependencies, and governance links in machine-readable form.

From the Logotron: Gödel numbering assigns unique integers to propositions, making proof-checking mechanical. Probes are Gödel numbers for code — they encode what the code *means* so governance can verify without parsing implementation.

### Probe Types

| Probe | Syntax | Purpose |
|-------|--------|---------|
| Semantic | `@ai probe: "description"` | What this code means in domain terms |
| Invariant | `@ai invariant: expression` | Mechanically verifiable property |
| Dependency | `@ai depends: Module::function` | Semantic dependency (not import graph) |
| Governance | `@ai governs: policy-name` | Links code to governance artifact |
| Domain | `@ai domain: category/subcategory` | Streeling department classification |
| Test link | `@ai tested-by: path#test-name` | Links to behavioral test |

### Language-Specific Syntax

```rust
// ix (Rust)
/// @ai probe: "Markov tensor storing transition probabilities"
/// @ai invariant: rows_sum_to_one
/// @ai domain: mathematics/probability
/// @ai governs: ml-governance-feedback-policy
pub struct MarkovTensor { ... }
```

```fsharp
// tars (F#)
/// @ai probe: "Weighted grammar production selector"
/// @ai invariant: weights_sum_to_one
/// @ai depends: ResearchWeights::loadDepartmentWeights
/// @ai domain: computer-science/grammar-theory
let selectProduction weights rng = ...
```

```csharp
// ga (C#)
/// @ai probe: "Chord voicing optimizer for guitar fretboard"
/// @ai invariant: max_fret_span <= 4
/// @ai domain: guitar-studies/voicing
/// @ai tested-by: tests/VoicingTests.cs#OptimalVoicing
public Voicing Optimize(Chord chord) { ... }
```

### Probe Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AI Probe",
  "type": "object",
  "required": ["probe_type", "value", "location"],
  "properties": {
    "probe_type": {
      "enum": ["probe", "invariant", "depends", "governs", "domain", "tested-by"]
    },
    "value": { "type": "string" },
    "location": {
      "type": "object",
      "required": ["repo", "file"],
      "properties": {
        "repo": { "type": "string" },
        "file": { "type": "string" },
        "line": { "type": "integer" },
        "symbol": { "type": "string" }
      }
    },
    "verified": {
      "type": "object",
      "required": ["truth_value", "last_verified"],
      "properties": {
        "truth_value": { "enum": ["T", "F", "U", "C"] },
        "membership": { "$ref": "fuzzy-distribution" },
        "last_verified": { "type": "string", "format": "date-time" },
        "verifier": { "type": "string" }
      }
    }
  }
}
```

### Governance Integration

**RECON phase:** The driver scans all repos for `@ai` probes, builds a semantic code map. Code without probes = ungoverned territory = conscience blind spot signal.

**VERIFY phase:** Check `@ai invariant` probes mechanically where possible. Mark invariant verification results as fuzzy beliefs (T(0.95) if test passes, U(0.5) if no test exists).

**Coverage metric:** `probed_symbols / total_exported_symbols` per repo — tracked in health scores.

**Incompleteness acknowledgment** (from Logotron): Not all code semantics can be captured by probes, just as not all propositions are decidable. The policy explicitly states that 100% coverage is not the goal — the goal is to reduce the *radius of the ungoverned*.

### Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Schema | `schemas/ai-probe.schema.json` | Probe object schema |
| Policy | `policies/ai-probes-policy.yaml` | Coverage requirements, verification rules |
| Syntax spec | `docs/specs/ai-probes-syntax.md` | Language-specific syntax guide |
| Directive template | `contracts/directives/adopt-ai-probes.directive.md` | Galactic Protocol directive for consumer repos |
| Tests | `tests/behavioral/ai-probes-cases.md` | 6+ test cases |

### Probe Verification Levels

Inspired by Petit's hierarchy (axiom → demonstrable → refutable → undecidable):

| Level | Name | Description | Tetravalent |
|-------|------|-------------|-------------|
| 0 | Axiomatic | Probe asserts a definition — verified by existence | T |
| 1 | Demonstrable | Invariant has a passing test | T (high confidence) |
| 2 | Refutable | Invariant has a failing test | F |
| 3 | Undecidable | Semantic probe — cannot be mechanically verified | U |
| 4 | Contradictory | Probe conflicts with another probe or test | C |

---

## Feature 3: Conscience Phase 3 — Anticipatory Ethics Pre-mortems (#39)

### Concept

Add an ANTICIPATE step to the conscience loop that performs structured pre-mortems before significant governance actions. The pre-mortem asks: "If this action causes harm, what would it look like and how would we know?"

From the Logotron: Gödel proved that no system can fully verify itself. Pre-mortems internalize this — they don't claim to foresee all consequences but systematically explore the *foreseeable* failure modes, accepting that some are undecidable.

### Pre-mortem Template

```json
{
  "pre_mortem_id": "pm-2026-03-21-001",
  "action": {
    "type": "directive",
    "type_enum": ["directive", "promotion", "deprecation", "self-modification", "deployment"],
    "description": "Issue directive requiring @ai probes in all consumer repos",
    "irreversibility": "low",
    "irreversibility_enum": ["low", "medium", "high"],
    "blast_radius": "multi-repo",
    "blast_radius_enum": ["self", "single-repo", "multi-repo", "ecosystem"]
  },
  "stakeholders": [
    {
      "name": "Consumer repo developers",
      "relationship": "affected",
      "relationship_enum": ["affected", "responsible", "consulted", "informed"],
      "voice_heard": true
    }
  ],
  "anticipated_harms": [
    {
      "harm_category": "autonomy",
      "harm_category_note": "Values from constitutions/harm-taxonomy.md",
      "description": "Developers feel surveilled by mandatory probe annotations",
      "likelihood": { "T": 0.3, "F": 0.4, "U": 0.2, "C": 0.1 },
      "likelihood_note": "Uses $ref fuzzy-distribution schema",
      "severity": "medium",
      "severity_enum": ["negligible", "low", "medium", "high", "critical"],
      "constitutional_article": 6,
      "mitigation": "Frame probes as documentation, not surveillance. Make coverage targets gradual.",
      "residual_risk": { "T": 0.1, "F": 0.6, "U": 0.2, "C": 0.1 }
    }
  ],
  "logotron_check": {
    "self_referential": false,
    "undecidable_aspects": ["Whether probe coverage improves code quality long-term"],
    "metalanguage_risk": "Probes describe code, but who probes the probes?"
  },
  "decision": "proceed",
  "decision_enum": ["proceed", "modify", "defer", "escalate"],
  "decided_at": "2026-03-21T00:00:00Z",
  "accuracy_tracking": {
    "predicted_harms": 1,
    "actual_harms_at_review": null,
    "review_date": null
  }
}
```

### The Logotron Check

Every pre-mortem includes a `logotron_check` section inspired by Petit's incompleteness insights:

- **self_referential** — Does this action govern its own governance? (e.g., modifying the constitution that authorizes modifications). If true, escalate to human.
- **undecidable_aspects** — What aspects of this action's consequences cannot be determined in advance? Acknowledging unknowns prevents false confidence.
- **metalanguage_risk** — Does this action create a new layer of governance that itself needs governing? (The infinite regress problem from the Logotron.)

### Conscience Loop Update

Current 8-step loop: attend → feel → reflect → anticipate → decide → act → monitor → learn

Phase 3 expands **step 4 (anticipate):**

```
anticipate:
  trigger: action.irreversibility >= "medium" OR action.blast_radius >= "multi-repo"
  steps:
    1. Identify action type and blast radius
    2. Enumerate stakeholders (who is affected?)
    3. For each harm category in harm-taxonomy.md:
       - Estimate likelihood as fuzzy membership (T/F/U/C distribution)
       - If likelihood.T > 0.3 OR likelihood.C > 0.1: propose mitigation
    4. Run logotron_check (self-reference, undecidability, metalanguage)
    5. Calculate residual risk after mitigations
    6. If any residual_risk.T > 0.5: escalate to human
    7. Record pre-mortem in state/conscience/pre-mortems/
  skip_when: action.irreversibility == "low" AND action.blast_radius == "self"
```

### Anticipation Accuracy Metric

Track predictive quality over time:

```
anticipation_accuracy = correct_predictions / total_predictions
```

Where:
- A predicted harm that occurred = correct positive
- A predicted harm that didn't occur = false positive (overcautious)
- An unpredicted harm that occurred = false negative (blind spot — triggers conscience signal)

Target: accuracy > 0.5 (better than random), false negative rate < 0.2 (catching most real harms).

Added to weekly conscience reports as a growth indicator alongside moral sensitivity, resolution velocity, etc.

### Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Schema | `schemas/pre-mortem.schema.json` | Pre-mortem template with logotron check |
| Policy update | `policies/proto-conscience-policy.yaml` | Add phase 3 anticipate expansion |
| Report update | `schemas/conscience-weekly-report.schema.json` | Add anticipation_accuracy metric |
| Example 1 | `examples/pre-mortem-directive.json` | Pre-mortem for issuing a directive |
| Example 2 | `examples/pre-mortem-promotion.json` | Pre-mortem for promoting policy to constitution |
| Example 3 | `examples/pre-mortem-deprecation.json` | Pre-mortem for deprecating an artifact |
| Tests | `tests/behavioral/pre-mortem-cases.md` | 6+ test cases |

---

## Cross-Cutting Connections

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Fuzzy Logic     │     │   @ai Probes     │     │  Conscience Ph.3    │
│  (#52)           │     │   (#53)          │     │  (#39)              │
│                  │     │                  │     │                     │
│ Fuzzy membership │────>│ Invariant verify │────>│ Pre-mortem harms    │
│ distributions    │     │ returns fuzzy    │     │ expressed as fuzzy  │
│                  │     │ truth values     │     │ membership          │
│                  │     │                  │     │                     │
│ Transition gates │     │ Coverage gaps  ──┼────>│ Blind spot signals  │
│ use membership   │     │ = ungoverned     │     │ trigger anticipation│
│ thresholds       │     │                  │     │                     │
│                  │     │ @ai governs:   ──┼────>│ Logotron check      │
│                  │     │ creates audit    │     │ traces governance   │
│                  │     │ trail            │     │ self-reference      │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
         │                       │                        │
         └───────────┬───────────┘                        │
                     │                                    │
              Logotron Foundation                         │
         ┌───────────┴───────────┐                        │
         │ Four-fold classif.    │                        │
         │ T/F/U/C = axiom/      │◄───────────────────────┘
         │ demonstrable/refutable│  Incompleteness:
         │ /undecidable          │  pre-mortems accept
         │                       │  undecidable aspects
         │ Gödel numbering       │
         │ = probes encode       │
         │ meaning mechanically  │
         └───────────────────────┘
```

---

## Implementation Order

1. **Fuzzy Logic first** — foundation for the other two (both reference fuzzy membership)
2. **@ai Probes second** — depends on fuzzy for verification results
3. **Conscience Phase 3 third** — depends on both (fuzzy harms, probe coverage as conscience input)

---

## Summary of All New Artifacts

| # | Artifact | Type | Path |
|---|----------|------|------|
| 1 | Fuzzy membership spec | Logic doc | `logic/fuzzy-membership.md` |
| 2 | Fuzzy belief schema | JSON Schema | `schemas/fuzzy-belief.schema.json` |
| 3 | State machine grammar update | EBNF | `grammars/state-machines.ebnf` |
| 4 | Alignment policy update | YAML | `policies/alignment-policy.yaml` |
| 5 | Fuzzy logic tests | Behavioral | `tests/behavioral/fuzzy-logic-cases.md` |
| 6 | AI probe schema | JSON Schema | `schemas/ai-probe.schema.json` |
| 7 | AI probes policy | YAML | `policies/ai-probes-policy.yaml` |
| 8 | Probe syntax spec | Markdown | `docs/specs/ai-probes-syntax.md` |
| 9 | Adopt probes directive | Contract | `contracts/directives/adopt-ai-probes.directive.md` |
| 10 | Probe tests | Behavioral | `tests/behavioral/ai-probes-cases.md` |
| 11 | Pre-mortem schema | JSON Schema | `schemas/pre-mortem.schema.json` |
| 12 | Proto-conscience policy update | YAML | `policies/proto-conscience-policy.yaml` |
| 13 | Weekly report schema update | JSON Schema | `schemas/conscience-weekly-report.schema.json` |
| 14 | Pre-mortem example: directive | JSON | `examples/pre-mortem-directive.json` |
| 15 | Pre-mortem example: promotion | JSON | `examples/pre-mortem-promotion.json` |
| 16 | Pre-mortem example: deprecation | JSON | `examples/pre-mortem-deprecation.json` |
| 17 | Pre-mortem tests | Behavioral | `tests/behavioral/pre-mortem-cases.md` |
| 18 | Fuzzy distribution fragment | JSON Schema | `schemas/fuzzy-distribution.schema.json` |
| 19 | Conscience signal schema update | JSON Schema | `schemas/conscience-signal.schema.json` |
| 20 | Pre-mortem state directory | Directory | `state/conscience/pre-mortems/` |
| 21 | Directives directory | Directory | `contracts/directives/` |
| 22 | Cross-feature integration test | Behavioral | `tests/behavioral/batch-b-integration-cases.md` |

---

## Conscience Signal Type Extension

The existing `conscience-signal.schema.json` defines 6 signal types. Probe coverage gaps trigger conscience signals via the existing `silence_discomfort` type (detecting absence/blind spots). If experience shows this is insufficient, a dedicated `probe_coverage_discomfort` type can be added later. For now, `silence_discomfort` with `context.source = "probe-scanner"` is adequate.

---

## Directive Format Note

The `contracts/directives/` directory is new. The directive format follows the Galactic Protocol contract structure defined in `contracts/galactic-protocol.md`, with additional fields for compliance deadline, verification criteria, and remediation guidance. The adopt-ai-probes directive will be the first concrete example.

---

## Example Test Case Titles

### Fuzzy Logic Tests
1. Fuzzy AND with both operands having high T-membership
2. Fuzzy NOT on pure-U distribution (should return identical distribution)
3. Tied argmax resolution — C > U > T > F tiebreak
4. Sharpening trigger at membership > 0.8
5. Escalation on C > 0.3 after fuzzy OR operation
6. Backward compatibility — belief without membership field validates normally

### @ai Probe Tests
1. Probe scanner finds all `@ai` annotations in a Rust file
2. Invariant probe with passing test returns T with high membership
3. Coverage metric calculation — probed vs total exported symbols
4. Ungoverned code (no probes) triggers silence_discomfort signal
5. Conflicting probes on same symbol detected as Contradictory
6. Probe with `@ai governs: nonexistent-policy` flagged as error

### Pre-mortem Tests
1. High-irreversibility action triggers mandatory pre-mortem
2. Low-irreversibility, self-scope action skips pre-mortem
3. Self-referential action detected by logotron_check
4. Anticipated harm with residual_risk.T > 0.5 triggers escalation
5. Anticipation accuracy tracking updates after review
6. Cross-feature: probe coverage gap → conscience signal → pre-mortem on remediation directive
