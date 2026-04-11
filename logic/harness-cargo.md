# Harness Adapter Projection — cargo

**Status:** Version 1.0, 2026-04-11.
**Scope:** Projection rules for `cargo test --format=json
--report-time` output into `HexObservation` records.
**Implementation:** `ix/crates/ix-harness-cargo`.
**Consumed by:** `ix_triage_session` via `prior_observations`, or
any other governance consumer that reads the SessionEvent stream.
**Producer tier:** Tier 0 (first-party — cargo is a trusted tool
we don't author but whose output is deterministic and reviewable).

## Purpose

cargo's `--format=json` output is a stable, machine-readable
stream of test events. This adapter projects those events into
the hexavalent observation substrate so **test outcomes in any
Rust repo become first-class signals in the Demerzel governance
layer**.

Unlike the tars adapter (which is diagnostic — "what does the
system look like right now"), this adapter is **evidential** —
"what did the code just prove about itself." The epistemological
shape matches cargo's role: it's a **reviewer**, combinatorial
by nature (a run is a bundle of discrete pass/fail events).

## Input shape

cargo emits newline-delimited JSON events with a `type` tag:

```json
{"type":"suite","event":"started","test_count":42}
{"type":"test","event":"started","name":"my_module::test_name"}
{"type":"test","event":"ok","name":"my_module::test_name","exec_time":0.001}
{"type":"test","event":"failed","name":"my_module::broken","exec_time":0.005,"stdout":"..."}
{"type":"test","event":"ignored","name":"my_module::flaky"}
{"type":"suite","event":"ok","passed":41,"failed":1,"ignored":0,"measured":0,"filtered_out":0,"exec_time":2.34}
```

The adapter is permissive: unknown fields are ignored, malformed
lines are skipped (not errors), and the adapter can produce
useful output from a partial stream.

## Output shape

All observations carry:

- `source = "cargo"` — fixed
- `diagnosis_id = sha256(canonical input bytes)` — content-addressable
- `round` — caller-supplied via `--round`
- `ordinal` — monotonically incremented across the full run

## Rules

### Rule 1 — per-test outcome

For each `{"type":"test","event":<event>,"name":<name>,...}` line:

| Event | claim_key | Variant | Weight |
|---|---|---|---|
| `ok` | `test:<name>::valuable` | T | 0.9 |
| `failed` | `test:<name>::valuable` | F | 1.0 |
| `ignored` | `test:<name>::valuable` | U | 0.3 |
| `bench` (allocation-only) | `test:<name>::valuable` | P | 0.6 |
| `started` | none (not a terminal event) | — | — |

Rationale: a passing test is verified value (T, high weight). A
failing test is a refutation of value (F, full weight — cargo is
authoritative on its own test results). An ignored test carries
almost no information (U, low weight). A `bench` event is a
probable signal — the benchmark ran but we don't know whether
the number was good.

The claim_key uses `test:` as the `tool_name` and the full test
path as `target_hint`, so two tests with the same module prefix
don't collide on loop-detector semantics.

### Rule 2 — suite-level summary

For each `{"type":"suite","event":"ok"|"failed",...}` line, emit
one observation on `cargo_suite::reliable`:

| Suite event | passed / total ratio | Variant | Weight |
|---|---|---|---|
| `ok` | — | T | 0.9 |
| `failed` | passed == 0 | F | 1.0 |
| `failed` | passed / total > 0.9 | D | 0.7 |
| `failed` | passed / total > 0.5 | D | 0.8 |
| `failed` | passed / total <= 0.5 | F | 0.9 |

"reliable" (source credibility) is the right aspect here: a
suite that mostly passes is a reliable source; a catastrophic
failure refutes that source's reliability for this round.

### Rule 3 — slow tests (optional performance signal)

For each test event with `exec_time > 5.0` seconds:

Emit `test:<name>::timely = D, weight 0.6`

Rationale: slow tests aren't *wrong*, but they drag the feedback
loop and suggest the test's value is time-discounted. Timely
aspect catches this without contaminating the `::valuable`
signal.

### What this adapter does NOT emit

- No observations for `started` events (intermediate state, not
  outcome)
- No observations for compiler warnings (separate adapter: clippy)
- No observations for build errors (separate adapter: cargo-build)
- No observations for test output text (privacy-adjacent; also
  not mergeable without NLP)
- No observations when `passed == 0 && failed == 0` (no signal)

## Ordinal allocation

Ordinals start at 0 and increment for every emitted observation.
The order is:

1. Suite-level summary first (so consumers see the bottom line
   before drilling into individual tests)
2. Per-test observations in the order cargo emitted them

This ordering is deterministic per input, so two runs on the
same cargo output produce identical ordinals.

## Worked example

Input (3 lines of cargo JSON):

```jsonl
{"type":"test","event":"ok","name":"foo::test_a","exec_time":0.01}
{"type":"test","event":"failed","name":"foo::test_b","exec_time":0.02}
{"type":"suite","event":"failed","passed":1,"failed":1,"ignored":0,"exec_time":0.5}
```

Expected observations:

```jsonl
{"kind":"observation_added","ordinal":0,"source":"cargo","diagnosis_id":"<sha>","round":N,"claim_key":"cargo_suite::reliable","variant":"D","weight":0.7,"evidence":"passed 1 of 2"}
{"kind":"observation_added","ordinal":1,"source":"cargo","diagnosis_id":"<sha>","round":N,"claim_key":"test:foo::test_a::valuable","variant":"T","weight":0.9,"evidence":"ok"}
{"kind":"observation_added","ordinal":2,"source":"cargo","diagnosis_id":"<sha>","round":N,"claim_key":"test:foo::test_b::valuable","variant":"F","weight":1.0,"evidence":"failed"}
```

Note: `test:foo::test_b::valuable` contains four `::` sequences
in the claim_key. The merge function's `action_and_aspect` helper
splits on the **first** `::`, so `action_key = "test:foo"` and
`aspect = "test_b::valuable"`. This is a known limitation: the
claim_key grammar doesn't round-trip cleanly when the test name
itself contains `::`.

**Mitigation:** the adapter uses `:` (single colon) as the
separator between `test` and the test name, so the first `::` in
the claim_key is always the aspect separator. The test name
itself may contain `::` (module paths do), but the aspect is
always the text after the LAST `::`. The merge function should
use `rfind("::")` instead of `find("::")` to handle this.

**Action item:** `hex-merge.md §Claim Key Grammar` should
specify that claim_key splitting uses `rfind("::")` not `find`.
This change is documented here and committed alongside the
cargo adapter so the grammar stays consistent with real-world
test names.

## Example: cross-source contradiction

Suppose ix runs the triage session and dispatches `ix_stats`,
which succeeds (completed with value). Then cargo runs the test
suite, and `test:ix_math::stats_tests::basic_stats::valuable`
fails.

- ix observation: `ix_stats::valuable = T` (from Completed event)
- cargo observation: `test:ix_math::stats_tests::basic_stats::valuable = F`

These have DIFFERENT claim_keys — ix_stats is the tool; the
failing test is a specific test name. So no direct contradiction
fires. **But** meta-conflict detection on `action_key="ix_stats"`
vs `action_key="test"` (different actions) doesn't fire either.

The test failure is a real signal but it's about a different
"thing" than ix_stats running. The adapter's rule of using
`test:<name>` as the action_key is correct: tests are their own
namespace, not tied to the tool name they exercise.

**What would fire:** if ix dispatches `ix_stats` and the cargo
adapter also sees `test:ix_stats::valuable = F` (someone added a
test named `ix_stats`), then the two DO contradict. The grammar
chose "tests are their own namespace" to avoid accidental
contradictions.

## Content hashing

The `diagnosis_id` is `sha256(canonical_input_bytes)` — the full
cargo JSON stream, byte-for-byte. This means:

- Two adapter runs on the same cargo output produce identical IDs
- A re-run of the same test suite (even with identical pass/fail
  status) produces a NEW diagnosis_id because cargo includes
  per-run metadata (timing) that varies
- This is correct: each test run is a distinct observation event
  even if it reports the same outcomes

## Trust considerations

cargo is **Tier 0 trusted** because:

1. cargo is authored by the Rust Foundation and is deterministic
   given the same code and toolchain
2. The JSON output schema is stable and documented
3. cargo's test runner has no network access by default
4. We control the invocation (we run cargo ourselves)

cargo's output is **not** signed today because Tier 0 doesn't
require signatures. If we ever run external-author tests in a
harness context (e.g., consuming cargo output from a third-party
CI service), that becomes a Tier 2+ scenario and needs the
signature layer.

## Version

1.0 — 2026-04-11 — initial cargo projection spec. Per-test
valuable observations, suite-level reliability baseline, optional
slow-test timely flag. Claim-key grammar clarification: use
`rfind("::")` for aspect splitting.
