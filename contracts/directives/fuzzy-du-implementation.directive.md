# Directive: Fuzzy DU System Implementation

**Directive ID:** DIR-2026-03-23-001
**Type:** implementation
**From:** Demerzel (Governance)
**To:** tars (F# implementation)
**Priority:** P1
**Issued:** 2026-03-23
**Compliance Deadline:** 2026-04-06

## Context

The Fuzzy DU system extends F#'s discriminated unions with fuzzy membership vectors, enabling governance decisions to operate on probability distributions rather than crisp values. This is foundational for tetravalent logic integration — every governance gate, belief state, and confidence threshold benefits from expressing uncertainty as a first-class type rather than a scalar.

**Design spec:** `docs/superpowers/specs/2026-03-22-fuzzy-enum-du-design.md`
**Schemas:** `schemas/fuzzy-enum.schema.json`, `schemas/fuzzy-du.schema.json`

## Directive

tars SHALL implement the Fuzzy DU system as a new `Tars.Fuzzy` project with the following phased components:

### Phase 1 — Core Types (Week 1)

- Create `src/Tars.Fuzzy/` project and namespace.
- **FuzzyEnum<'T>**: A membership vector mapping each case of a union to a probability in [0,1]. MUST support:
  - `ArgMax` — returns the case with highest membership
  - `IsSharp` — returns true iff exactly one case has membership 1.0, all others 0.0
  - `Pure(case)` — constructs a sharp (crisp) distribution with 1.0 on the given case
  - `Uniform` — constructs equal membership across all cases
- **FuzzyOps**: Combinators for fuzzy algebra. MUST implement:
  - `AND` — element-wise minimum of two membership vectors
  - `OR` — element-wise maximum of two membership vectors
  - `NOT` — complement (1 - membership) for each case
  - `Renormalize` — scale memberships so they sum to 1.0
  - `Sharpen(threshold)` — zero out memberships below threshold, renormalize remainder
  - `NOT_tetravalent` — tetravalent-aware negation: T<->F, U->U, C->C
- **FuzzyDU<'T,'P>**: A fuzzy enum paired with per-case payload storage. MUST support:
  - `ToEnum` — project away payloads, yielding FuzzyEnum<'T>
  - `Payloads` — access typed payloads keyed by case
- **PropagationStrategy**: Discriminated union defining how fuzzy memberships combine through pipelines:
  - `Multiplicative` — element-wise product (default)
  - `Zadeh` — min/max propagation
  - `Bayesian` — Bayesian update with prior
  - `Custom of (float[] -> float[] -> float[])` — user-defined combinator
- **FuzzyResult<'T>**: A fuzzy enum with an execution trace. MUST support:
  - `Trace` — ordered list of operations that produced this result
  - `ScaleBy(factor)` — multiply all memberships by a scalar, renormalize
  - `Merge(other, strategy)` — combine with another FuzzyResult using the given PropagationStrategy
- **Unit tests** for all operations in `tests/Tars.Fuzzy.Tests/`. At minimum:
  - Pure/Uniform construction
  - AND/OR/NOT algebra laws
  - Sharpen threshold behavior
  - NOT_tetravalent mapping correctness
  - Renormalize sum-to-one invariant
  - Merge with each PropagationStrategy

### Phase 2 — Computation Expression (Week 1-2)

- **FuzzyBuilder**: F# computation expression for composing fuzzy operations. MUST implement:
  - `Bind` — propagate fuzzy context through sequential operations
  - `Return` — lift a crisp value into a FuzzyResult
  - `Combine` — merge parallel fuzzy branches using the builder's PropagationStrategy
- **Convenience instances**:
  - `fuzzy` — default builder using Multiplicative strategy
  - `fuzzyZadeh` — builder using Zadeh (min/max) strategy
  - `fuzzyBayes` — builder using Bayesian strategy
- **Threshold gates**: Support `when T(threshold)` syntax within the CE to filter branches where T-membership falls below the threshold. Gates that reject MUST record the rejection in the trace.
- **Integration test**: Implement the governance gate example from the design spec — a pipeline that evaluates a belief state through fuzzy confidence, applies a governance threshold, and produces a gated decision with full trace.

### Phase 3 — Integration (Week 2)

- **BeliefState extension**: Extend the existing `BeliefState` type with an optional `fuzzy_membership` field of type `FuzzyEnum<TetravalentValue>`. This enables belief states to carry T/F/U/C as a distribution rather than a single value.
- **BS decode MCP tool** (`bs_decode`): Create or extend an MCP tool that:
  - Accepts a serialized belief state (JSON conforming to `schemas/belief-state.schema.json`)
  - Decodes fuzzy membership if present
  - Returns the ArgMax classification and full distribution
- **Grammar system connection**: Wire fuzzy types into the existing grammar system so that grammar productions can reference fuzzy enums as terminal/nonterminal types.

### Phase 4 — Auto-Production (Future, Non-Blocking)

This phase is informational and NOT required for compliance. It describes the envisioned future direction:

- **Type provider extension**: F# type provider that reads Demerzel JSON schemas (`schemas/fuzzy-enum.schema.json`, `schemas/fuzzy-du.schema.json`) and generates corresponding F# types at compile time.
- **File watcher extension**: Watches schema files for changes and triggers type regeneration.
- **Runtime variant discovery**: Dynamically discovers new union cases from schema updates without recompilation.

## Compliance Requirements

1. **Unit tests:** Phases 1 and 2 MUST include unit tests in `tests/Tars.Fuzzy.Tests/`.
2. **Schema conformance:** Serialized fuzzy enums MUST conform to `schemas/fuzzy-enum.schema.json`. Serialized fuzzy DUs MUST conform to `schemas/fuzzy-du.schema.json`.
3. **Constitution compliance:** Fuzzy governance gates MUST enforce Article 6 (Escalation) — C > 0.3 triggers escalation. Threshold gates MUST enforce Article 7 (Auditability) — all gate decisions are traced.
4. **Conscience signals:** Governance gates that are bypassed or overridden MUST emit signals per `policies/proto-conscience-policy.yaml`.
5. **Tetravalent compatibility:** FuzzyEnum<TetravalentValue> MUST be the canonical representation for fuzzy belief states. NOT_tetravalent MUST preserve tetravalent semantics (U and C are not simple complements).

## Compliance Report

Upon completion of each phase, tars SHALL submit a compliance report to Demerzel via:
```
contracts/compliance/tars-fuzzy-du-phase-{N}.compliance.md
```

Each report MUST include:
- Phase number and name
- Files created/modified
- Test results (pass/fail counts)
- Any deviations from the design spec with justification
- Remaining blockers for the next phase

## Rejection Grounds

Per Galactic Protocol, valid rejection requires:
- **First Law override:** Implementation would cause harm to humans (data harm, trust harm, or autonomy harm)
- **Second Law override:** A human operator has explicitly countermanded this directive

Both require logged reasoning with constitutional citations.

## Reference

- Design spec: `docs/superpowers/specs/2026-03-22-fuzzy-enum-du-design.md`
- Fuzzy enum schema: `schemas/fuzzy-enum.schema.json`
- Fuzzy DU schema: `schemas/fuzzy-du.schema.json`
- Belief state schema: `schemas/belief-state.schema.json`
- Alignment policy: `policies/alignment-policy.yaml`
- Proto-conscience policy: `policies/proto-conscience-policy.yaml`
- Tetravalent logic: `logic/tetravalent.yaml`
