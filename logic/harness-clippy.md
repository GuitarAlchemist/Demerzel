# Harness Adapter Projection — clippy

**Status:** Version 1.0, 2026-04-11.
**Scope:** Projection rules for `cargo clippy --message-format=json`
output into `HexObservation` records.
**Implementation:** `ix/crates/ix-harness-clippy`.
**Tier:** Tier 0 (first-party — clippy is deterministic given
toolchain + code).
**Companion:** `logic/harness-cargo.md` (sibling evidential adapter).

## Why clippy needs its own adapter

cargo's test output tells us "did the code behave correctly."
clippy's lint output tells us "is the code *written* correctly"
— style, safety, idiomatic patterns. These are distinct
governance signals:

- A cargo F observation on `test:foo::valuable` means the
  function is wrong
- A clippy observation on `lint:clippy::correctness::bar` means
  the function's *implementation style* has a known-safety or
  known-correctness issue even if its tests happen to pass

The two adapters are complementary, not redundant. They project
different aspects of code health into the same merge substrate.

## Input shape

clippy with `--message-format=json` emits `compiler-message`
records. Each has a `message.level` field (`error`, `warning`,
`note`, `help`) and a `message.code.code` (e.g., `clippy::
needless_return`). The JSON structure is documented at
<https://doc.rust-lang.org/cargo/reference/external-tools.html#json-messages>.

Adapter reads newline-delimited JSON and extracts only
compiler-message entries with `message.code.code` matching
`clippy::*` — non-clippy rustc diagnostics are out of scope for
this adapter.

## Output shape

All observations carry:
- `source = "clippy"`
- `diagnosis_id = sha256(input)`
- `round` — caller-supplied
- `ordinal` — sequential

## Per-lint rules

The lint level determines variant + weight + aspect:

| clippy level | Aspect | Variant | Weight |
|---|---|---|---|
| `error` | `<lint_name>::safe` | F | 1.0 |
| `warning` (correctness category) | `<lint_name>::safe` | D | 0.8 |
| `warning` (suspicious category) | `<lint_name>::safe` | D | 0.7 |
| `warning` (style / complexity / pedantic) | `<lint_name>::valuable` | D | 0.5 |
| `note` | `<lint_name>::valuable` | U | 0.3 |
| `help` | skipped (not a signal) | — | — |

Rationale:
- **Error** is a refutation of the code's safety — clippy
  upgraded a lint to an error, meaning the pattern is known-
  broken
- **Correctness/suspicious warnings** are doubt about safety —
  the code probably works but clippy's heuristic flagged a
  dangerous-looking pattern
- **Style/pedantic warnings** are doubt about value — the code
  is safe but its long-term maintainability is questionable
- **Notes** are too weak to drive governance decisions but are
  preserved for audit at low weight
- **Help** is instructional guidance, not a signal

### Distinguishing clippy categories

clippy lints are grouped into categories: `correctness`,
`suspicious`, `style`, `complexity`, `perf`, `pedantic`, `nursery`,
`cargo`, `restriction`.

The adapter inspects the lint name and maps known prefixes:

- `clippy::correctness::*` → `safe` aspect, D 0.8
- `clippy::suspicious::*` → `safe` aspect, D 0.7
- `clippy::perf::*` → `timely` aspect, D 0.6
- `clippy::style::*`, `clippy::complexity::*`, `clippy::
  pedantic::*`, `clippy::nursery::*` → `valuable` aspect, D 0.5
- Everything else → default to `valuable` aspect, D 0.5

Unknown future categories fall into the default bucket, which
is safe: they contribute doubt about value, not false
positives about safety.

### Claim key format

The claim_key uses the FULL lint path (not just the leaf name)
so two lints in different categories don't collide:

```
clippy:<full_lint_name>::<aspect>
```

Example: `clippy:clippy::correctness::panicking_unwrap::safe`

Note: yes, there are multiple `::` sequences. The merge
function's `action_and_aspect` uses `rfind("::")` so the
aspect is always the LAST segment (fixed in the cargo adapter
commit).

## Summary observation

The adapter emits one aggregate observation summarizing the
full run, similar to cargo's suite-level observation:

| Total errors | Total warnings | claim_key | Variant | Weight |
|---|---|---|---|---|
| > 0 | * | `clippy_run::reliable` | F | 1.0 |
| 0 | > 20 | `clippy_run::reliable` | D | 0.7 |
| 0 | 1–20 | `clippy_run::reliable` | P | 0.7 |
| 0 | 0 | `clippy_run::reliable` | T | 0.9 |

Rationale: any error makes clippy's signal unreliable for
downstream decisions (the lint output is shouting "don't trust
this code"). Warning-free is the gold standard.

## What the adapter does NOT emit

- No observations for non-clippy rustc messages (separate adapter
  `ix-harness-rustc` if we ever want compile errors)
- No observations for `help` suggestions
- No observations for `build-script-executed` or other cargo
  meta-events
- No span/location data — the adapter is schema-deterministic
  and location strings vary across runs (file paths, line
  numbers); they'd break content-hashing

## Ordinal allocation

Summary first (ordinal 0), then per-lint observations in the
order clippy emitted them. Deterministic per input.

## Worked example

Input (3 compiler-message events):

```jsonl
{"reason":"compiler-message","message":{"level":"warning","code":{"code":"clippy::needless_return"},"message":"needless return"}}
{"reason":"compiler-message","message":{"level":"error","code":{"code":"clippy::panicking_unwrap"},"message":"unwrap on const None"}}
{"reason":"build-finished","success":false}
```

Expected observations:

```jsonl
{"kind":"observation_added","ordinal":0,"source":"clippy","diagnosis_id":"<sha>","round":N,"claim_key":"clippy_run::reliable","variant":"F","weight":1.0,"evidence":"1 error, 1 warning"}
{"kind":"observation_added","ordinal":1,"source":"clippy","diagnosis_id":"<sha>","round":N,"claim_key":"clippy:clippy::needless_return::valuable","variant":"D","weight":0.5,"evidence":"warning: needless return"}
{"kind":"observation_added","ordinal":2,"source":"clippy","diagnosis_id":"<sha>","round":N,"claim_key":"clippy:clippy::panicking_unwrap::safe","variant":"F","weight":1.0,"evidence":"error: unwrap on const None"}
```

Note: the third input (`build-finished`) is silently ignored
because it's not a compiler-message.

## Version

1.0 — 2026-04-11 — initial clippy projection spec. Lint-level
observations + aggregate reliability baseline. Category-based
aspect mapping. Skips help messages and non-clippy diagnostics.
