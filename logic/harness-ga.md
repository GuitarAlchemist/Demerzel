# Harness Adapter Projection — Guitar Alchemist (ga)

**Status:** Version 0.1 SCOPING DOC, 2026-04-11.
**Scope:** Projection rules for Guitar Alchemist governance
events into `HexObservation` records.
**Implementation:** `ix/crates/ix-harness-ga` (stub — see
"Current state" below).
**Tier:** Tier 0 for first-party invocation. Becomes Tier 1
when ga operates as a cross-repo governance peer (once the
signature layer ships).
**Companion:** `harness-tars.md`, `harness-cargo.md`.

## Why this document exists as a stub

The brainstorm around harness engineering across repos named
`ix-harness-ga` as the natural next adapter after tars and
cargo. ga is already Demerzel-aware (it consumes the Demerzel
submodule for governance policies) and has the richest
governance-event output of any repo we've built — it emits
grammar evolution events, belief updates, constitutional
compliance signals, music-domain decisions, and more.

**But the specific wire format ga should emit is still being
designed.** ga is a large .NET + React + TypeScript codebase
with governance events scattered across multiple services:

- `GaApi` (.NET backend) — GovernanceHub (SignalR), AlgedonicSignalService,
  SeldonPlanService, ConstitutionalComplianceTracker
- `GuitarAlchemist` web client — user interaction signals,
  component mount/unmount telemetry
- `Prime Radiant` visualization — governance graph updates,
  belief-state transitions
- MCP servers in the ga repo — policy invocations, rule triggers

Rather than commit to a premature projection spec, this document
**scopes what an eventual ga adapter would cover** and serves
as the entry point for future work.

## Proposed input shape

ga's governance events are already structured (SignalR messages,
typed C# events, JSON log streams). For the adapter MVP, we
propose a canonical intermediate shape: a NDJSON file where
each line is a `GaGovernanceEvent`:

```json
{
  "kind": "algedonic" | "constitutional" | "grammar" | "belief" | "seldon" | "compliance",
  "severity": "info" | "warning" | "error" | "critical",
  "subject": "<claim identifier>",
  "source_component": "<ga subsystem name>",
  "evidence": { /* kind-specific payload */ },
  "timestamp": "<ISO 8601, ignored by adapter>"
}
```

**Who emits this:** a thin ga-side shim reads ga's native event
streams (SignalR hub, event logs, MCP server output) and writes
the canonical NDJSON. The shim is **out of scope for this
adapter** — it lives in ga's repo, not ix's.

**Why this split:** we don't want the Rust adapter to care
about SignalR wire format, .NET serialization quirks, or
React component lifecycle. The shim handles all that on the
ga side. The adapter handles the canonical NDJSON → HexObservation
projection, which is the part that benefits from Rust's
type safety and ix's CRDT substrate.

## Proposed projection rules

Once the shim produces canonical NDJSON, the projection rules
by event kind:

### algedonic events
ga emits these when the algedonic signal service detects
governance pain or pleasure. Severity maps directly:

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga:<subject>::reliable` | T | 0.7 |
| warning | `ga:<subject>::reliable` | D | 0.6 |
| error | `ga:<subject>::reliable` | F | 0.8 |
| critical | `ga:<subject>::reliable` | F | 1.0 |

### constitutional events
ga emits these when a governance article is consulted or
potentially violated:

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga_constitution:<article>::valuable` | T | 0.8 |
| warning | `ga_constitution:<article>::safe` | D | 0.7 |
| error/critical | `ga_constitution:<article>::safe` | F | 1.0 |

### grammar events
ga's grammar system evolves based on observation. Grammar
evolution is typically positive signal (the system learned
something):

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga_grammar:<rule>::valuable` | P | 0.6 |
| warning | `ga_grammar:<rule>::reliable` | D | 0.5 |

### belief events
Belief changes in ga's tetravalent/hexavalent state:

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga_belief:<proposition>::reliable` | P | 0.5 |
| warning | `ga_belief:<proposition>::reliable` | U | 0.4 |

### seldon events
ga's Seldon planning service emits progress/blocked signals:

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga_seldon:<plan_id>::timely` | T | 0.7 |
| warning | `ga_seldon:<plan_id>::timely` | D | 0.6 |
| error | `ga_seldon:<plan_id>::valuable` | F | 0.8 |

### compliance events
Constitutional compliance tracker outputs:

| severity | claim_key | Variant | Weight |
|---|---|---|---|
| info | `ga_compliance:<check_id>::reliable` | T | 0.9 |
| warning | `ga_compliance:<check_id>::reliable` | D | 0.7 |
| critical | `ga_compliance:<check_id>::reliable` | F | 1.0 |

## What the adapter would NOT project

- **No UI telemetry.** Component mount/unmount events, user
  clicks, render times — all out of scope. Those are UX
  metrics, not governance signals.
- **No raw log lines.** Unstructured log messages don't have
  a claim_key. The shim must pre-classify into the canonical
  event kind.
- **No music-domain data.** Notes, chords, tunings — these are
  domain content, not governance.
- **No cross-reference to tars/ix/cargo observations.** The ga
  adapter emits; the merge function (ix-fuzzy) combines sources.

## Current state — stub crate

`ix/crates/ix-harness-ga/` contains a minimal reference
implementation that:

1. Parses the canonical NDJSON shape into `GaGovernanceEvent`
   records
2. Applies the projection rules above for all six event kinds
3. Emits `SessionEvent::ObservationAdded` records matching the
   Demerzel schema
4. Has enough tests (6) to prove the projection rules behave
   as documented

**The stub is intentionally simple.** It doesn't try to parse
ga's native formats; it assumes the canonical NDJSON already
exists. When the ga-side shim is built, the adapter is already
waiting for it.

## Why stub now rather than defer entirely

1. **The rules are the important part.** Projection rules are
   governance decisions. Writing them down now — while the
   harness-engineering context is fresh — captures the design
   before it gets lost.
2. **The adapter is ~200 LoC.** Cheap to maintain as a stub.
   Reviewing later is much easier than starting from scratch.
3. **Future ga sessions can pick it up immediately.** No need
   to re-derive the rules or the canonical format.

## Open questions (deferred to the ga-side shim design)

1. **Should ga emit events directly to a SessionLog file**, or
   produce a separate NDJSON stream that an adapter invocation
   reads? File-based is simpler; direct emission is faster.
2. **How are round numbers allocated?** Per-request? Per-
   governance-cycle? Per-minute? Depends on ga's existing
   governance-loop structure.
3. **Which ga services emit which events?** Needs a catalog of
   ga subsystems → event kinds they produce.
4. **Can the shim be written in F# / C#** (matching ga's stack)
   or TypeScript, or does it need to be its own language? TS
   is probably easiest — it can run from node and parse SignalR
   messages.

These questions are out of scope for this document; they belong
in a future ga-side design session.

## Version

0.1 — 2026-04-11 — stub/scoping document. Six event kinds with
projection rules, canonical NDJSON input shape, minimal Rust
stub in ix-harness-ga. Full implementation deferred pending
the ga-side shim design session.
