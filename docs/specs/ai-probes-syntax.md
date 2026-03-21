# @ai Probe Syntax Specification

**Version:** 1.0.0
**Effective:** 2026-03-21
**Policy:** `policies/ai-probes-policy.yaml`

## Overview

`@ai` probes are semantic code anchors — structured annotations in doc comments that
make code meaning legible to the governance layer. They are the bridge between runtime
behavior and the Demerzel constitution. Each probe encodes a claim about what a symbol
means, what it guarantees, what it depends on, or which policy governs it.

The metaphor: probes are Gödel numbers for code. They do not replace tests or types;
they express the *meaning* behind them in terms the governance driver can reason about.

## Universal Syntax

```
@ai <probe_type>: <value>
```

- Must appear inside a doc comment on an exported/public symbol.
- One probe per line. Multiple probe types on the same symbol are allowed and encouraged.
- Order within the comment block does not matter.
- Values are case-sensitive.

### Probe Types

| Type | Syntax | Value format |
|------|--------|--------------|
| `probe` | `@ai probe: "description"` | Quoted string — domain meaning of the symbol |
| `invariant` | `@ai invariant: property_name` | Named semantic property (not code) |
| `depends` | `@ai depends: Module::function` | Semantic dependency reference |
| `governs` | `@ai governs: policy-name` | Policy filename without `.yaml` extension |
| `domain` | `@ai domain: department/subcategory` | Streeling department / research area |
| `tested-by` | `@ai tested-by: path#test-name` | Relative file path `#` test function or case |

---

## Language-Specific Placement

### Rust (ix)

Use `///` doc comment lines above `pub` items (structs, enums, functions, traits, modules).
Probes go inside the doc comment block, one per line, before or after prose.

```rust
/// @ai probe: "Markov tensor storing transition probabilities"
/// @ai invariant: rows_sum_to_one
/// @ai domain: mathematics/probability
/// @ai governs: ml-governance-feedback-policy
pub struct MarkovTensor { /* ... */ }
```

Rules:
- Apply only to `pub` or `pub(crate)` items.
- Place probes at the top of the doc comment block for scannability.
- `@ai governs:` value must match a filename in `policies/*.yaml` (without extension).
- `@ai invariant:` names should be `snake_case` semantic properties, not Rust expressions.
- `@ai depends:` uses `Module::function` or `Crate::Module::Type` format.

### F# (tars)

Use `///` XML doc comment lines above `let` bindings, type definitions, and module signatures.

```fsharp
/// @ai probe: "Weighted grammar production selector"
/// @ai invariant: weights_sum_to_one
/// @ai depends: ResearchWeights::loadDepartmentWeights
/// @ai domain: computer-science/grammar-theory
let selectProduction weights rng = (* ... *)
```

Rules:
- Apply to top-level `let` bindings, discriminated unions, record types, and module definitions.
- F# uses `///` (triple slash) for XML docs — probes go on `///` lines, not `//`.
- `@ai depends:` uses `Module::functionName` (PascalCase module, camelCase function).
- Internal `let` bindings inside a function body are not probed (not exported symbols).

### C# (ga)

Use `///` XML doc comment lines above `public` members (classes, methods, properties, interfaces).

```csharp
/// @ai probe: "Chord voicing optimizer for guitar fretboard"
/// @ai invariant: max_fret_span_lte_4
/// @ai domain: guitar-studies/voicing
/// @ai tested-by: tests/VoicingTests.cs#OptimalVoicing
public Voicing Optimize(Chord chord) { /* ... */ }
```

Rules:
- Apply to `public` and `internal` members. Skip `private` members.
- Probes may coexist with `<summary>`, `<param>`, and `<returns>` XML tags.
- Place probe lines before or after XML tags — do not embed inside XML tags.
- `@ai tested-by:` path is relative to the repo root.
- `@ai depends:` uses `Namespace.Class.Method` format.

---

## Placement Rules Summary

| Rule | Detail |
|------|--------|
| Exported symbols only | `pub` in Rust, top-level `let`/type in F#, `public`/`internal` in C# |
| One probe per line | Never combine two probe types on one line |
| Multiple types allowed | A symbol may have `probe`, `invariant`, `domain`, etc. simultaneously |
| Not in inline comments | Probes must be in doc comments (`///`), never `//` inline comments |
| Not on private symbols | Private/internal implementation details are intentionally ungoverned |

---

## Value Format Reference

### `@ai probe: "..."`

A quoted natural-language string describing what the symbol *means* in domain terms.
Write for a reader who knows the domain but not this specific codebase.

- Good: `"Markov tensor storing transition probabilities between grammar states"`
- Avoid: `"This struct holds the data"` (too generic)
- Avoid: `"See MarkovTensor::new for construction"` (procedural, not semantic)

### `@ai invariant: property_name`

A named semantic property that the symbol maintains. Use `snake_case`. This is not code —
it is the *name* of a property that may or may not be mechanically verifiable.

Examples: `rows_sum_to_one`, `weights_normalized`, `max_fret_span_lte_4`, `acyclic_dependency_graph`

When a test exists that validates this property, the governance driver maps it to
tetravalent `T (confidence 0.95)`. Without a test, it is `U (confidence 0.5)`.

### `@ai depends: Reference`

A semantic dependency — a symbol this code relies on for its correctness. Format varies by language:

| Language | Format | Example |
|----------|--------|---------|
| Rust | `Crate::Module::Symbol` | `MarkovCore::transition::normalize` |
| F# | `Module::functionName` | `ResearchWeights::loadDepartmentWeights` |
| C# | `Namespace.Class.Method` | `GuitarAlchemist.Theory.Interval.Semitones` |

### `@ai governs: policy-name`

The policy file (without `.yaml`) that this symbol implements or is constrained by.
Must match a file in `policies/*.yaml`. A missing match is flagged as an error in
the reconnaissance report.

Examples: `ml-governance-feedback-policy`, `autonomous-loop-policy`, `ai-probes-policy`

### `@ai domain: department/subcategory`

Streeling University department and research subcategory. See `policies/streeling-policy.yaml`
for the canonical department list.

Examples: `mathematics/probability`, `computer-science/grammar-theory`, `guitar-studies/voicing`

### `@ai tested-by: path#test-name`

Relative path from repo root to the test file, followed by `#` and the test function or
case name. Used by the governance driver to cross-reference coverage.

Examples:
- `tests/markov_tests.rs#test_rows_sum_to_one`
- `tests/VoicingTests.cs#OptimalVoicing`
- `TarsTests/GrammarTests.fs#selectProduction_weightsNormalized`

---

## Coverage Metric

```
probe_coverage = probed_symbols / total_exported_symbols
```

Tracked per-repo in `health-scores.json`. Thresholds:

| Level | Coverage | Status |
|-------|----------|--------|
| Minimum | 30% | Initial adoption target |
| Target | 60% | Medium-term goal |
| Full | 100% | Not required (Logotron incompleteness principle) |

Coverage gaps below the minimum threshold trigger a `silence_discomfort` conscience signal
with `context.source: probe-scanner`.

---

## Verification and Tetravalent Logic

Probes produce tetravalent truth values during the governance driver's verify phase:

| Condition | Result |
|-----------|--------|
| `@ai invariant` with passing test | T (confidence 0.95) |
| `@ai invariant` without test | U (confidence 0.5) |
| `@ai probe` (semantic, no test possible) | U (inherently undecidable) |
| Conflicting probes on same symbol | C (escalate) |
| `@ai governs` referencing missing policy | Error — flagged in recon report |

Axiomatic probes (`@ai probe:`) assert meaning by existence. They cannot be
mechanically falsified — their truth value is `U` until a test or contradiction
emerges. This is by design: the goal is not mechanical proof, but reducing the
radius of the ungoverned.

---

## Worked Examples

### Rust — Full example (ix repo)

```rust
/// @ai probe: "Markov tensor storing transition probabilities"
/// @ai invariant: rows_sum_to_one
/// @ai domain: mathematics/probability
/// @ai governs: ml-governance-feedback-policy
pub struct MarkovTensor { /* ... */ }

/// @ai probe: "Normalizes a probability row to sum to 1.0"
/// @ai invariant: output_rows_sum_to_one
/// @ai depends: MarkovCore::tensor::MarkovTensor
/// @ai tested-by: tests/markov_tests.rs#test_normalize_row
pub fn normalize_row(row: &mut Vec<f64>) { /* ... */ }
```

### F# — Full example (tars repo)

```fsharp
/// @ai probe: "Weighted grammar production selector"
/// @ai invariant: weights_sum_to_one
/// @ai depends: ResearchWeights::loadDepartmentWeights
/// @ai domain: computer-science/grammar-theory
let selectProduction weights rng = (* ... *)

/// @ai probe: "Seldon Plan research grammar — probabilistic sentence generator"
/// @ai governs: streeling-policy
/// @ai domain: computer-science/grammar-theory
type ResearchGrammar = { Productions: Production list; Weights: float list }
```

### C# — Full example (ga repo)

```csharp
/// @ai probe: "Chord voicing optimizer for guitar fretboard"
/// @ai invariant: max_fret_span_lte_4
/// @ai domain: guitar-studies/voicing
/// @ai tested-by: tests/VoicingTests.cs#OptimalVoicing
public Voicing Optimize(Chord chord) { /* ... */ }

/// <summary>Maps a chord to its interval structure.</summary>
/// @ai probe: "Interval set for a named chord quality"
/// @ai invariant: intervals_distinct
/// @ai depends: GuitarAlchemist.Theory.Interval.Semitones
/// @ai domain: guitar-studies/theory
public IReadOnlyList<Interval> GetIntervals(ChordQuality quality) { /* ... */ }
```

---

## Adoption

Consumer repos (ix, tars, ga) adopt probe annotations via Galactic Protocol directive.
See `contracts/directives/adopt-ai-probes.directive.md` for the adoption contract.

The governance driver (demerzel-bot) scans for `@ai` probes during the recon phase of
each driver cycle, building a semantic code map across all governed repositories.
