# Harness Engineering as a Governance Direction

**Status:** Governance direction, version 1.0, 2026-04-11.
**Scope:** Establishes harness engineering across repos as a
first-class architectural direction for the Demerzel governance
framework.
**Inspiration:** Martin Fowler's "Harness Engineering" article
(harness = the infrastructure surrounding code that keeps it
trustworthy at scale).
**Companion artifacts:**
- `logic/hex-merge.md` — the CRDT merge rules
- `logic/harness-tars.md` — the first projection spec
- `schemas/session-event.schema.json` — the canonical wire format
- `docs/brainstorms/2026-04-11-path-c-and-memory-spaces.md` — the
  multi-AI brainstorm that produced the substrate
- `ix/docs/brainstorms/2026-04-11-harness-adapter-pattern.md` — the
  implementation-layer design doc
- `ix/crates/ix-harness-tars/` — the reference adapter

## Thesis

The substrate Demerzel governs — SessionLog coordination, Belnap-
extended hexavalent merge, blast-radius approval middleware, trace
flywheel, MCP sampling — was initially built for AI agent action
governance. It turns out to be **structurally identical to what
harness engineering needs** for CI runs, code deployments, and
cross-repo observation flows.

Fowler's framing asks: how do we surround production code with
infrastructure that keeps it trustworthy at scale? Our framing
asked: how do we surround LLM tool calls with middleware that
keeps them trustworthy at scale? Same problem, different producer.
Same substrate answers both.

**The governance direction:** we treat Demerzel-governed harness
infrastructure as a first-class offering, not an incidental
byproduct of the agent-governance work. Future work explicitly
extends the substrate to harness external repos and CI systems.

## Why this works

Three structural properties make the substrate generalize:

### 1. The coordination format is producer-agnostic

`SessionEvent::ObservationAdded` carries:

```
source:       any trusted identifier (tars, ix, github-actions, ...)
diagnosis_id: content hash of the native input
round:        monotone integer
ordinal:      position within (source, diagnosis_id, round)
claim_key:    action_key::aspect grammar
variant:      T/P/U/D/F/C
weight:       (0, 1]
evidence:     optional audit string
```

Nothing in this schema assumes the producer is an LLM, an agent,
a CI system, or a human. It's just "someone observed something
about a specific claim with a specific confidence." Any producer
that can content-hash its input can emit observations.

### 2. The merge function is producer-agnostic

The G-Set CRDT defined in `hex-merge.md` treats all sources
symmetrically. Two observations from different sources on the
same claim synthesize a contradiction per the Belnap-extended
table. It doesn't matter whether the sources are:

- tars diagnosis vs ix execution (the original Path C case)
- GitHub Actions vs semgrep (a CI-scoped case)
- Prometheus alert vs Sentry incident (an observability case)
- Human code review vs static analysis (a governance case)

The math is the same. The contradictions fire the same way.
Cross-source escalation emerges from the same threshold.

### 3. The governance layer is authoritative

`hex-merge.md` owns the merge semantics. `harness-<source>.md`
owns the per-source projection rules. `schemas/session-event.schema.json`
owns the wire format. Every implementation — in any language —
defers to these Demerzel artifacts.

This is the critical governance property: **schema and semantic
authority live in Demerzel, not in implementation crates.**
Changing a projection rule is a Demerzel PR with rationale,
not a silent code edit. Changing the merge table is a Demerzel
PR with rationale. Adding a new aspect is a Demerzel PR with
rationale. Implementations are downstream.

## Per-agent / per-system mathematical space assignment

From the Path C brainstorm synthesis, each governed producer has
an **epistemological shape** that matches a natural mathematical
space. The SessionLog wire format is flat; each producer's
internal index can be curved.

| Producer role | Natural space | Rationale |
|---|---|---|
| **Diagnostician** (tars, monitoring systems) | Euclidean ℝⁿ | Sensor data, time series, linear metrics |
| **Executor** (ix, deploy systems, CI runners) | Hyperbolic Hⁿ | Action tree, tool hierarchy, branching search — needs exponential volume growth |
| **Governor** (Demerzel itself, policy engines) | Category / morphism | Constitutional transformations, policy composition — structure over state |
| **Observer** (Prometheus, DataDog, SIEM) | Euclidean + Fourier | Time-domain signals, frequency analysis for periodic patterns |
| **Reviewer** (human code review, audit tooling) | Combinatorial | Discrete bundles (PRs, issues, postmortems) |
| **Forecaster** (capacity planning, SLO prediction) | Hyperbolic + stochastic | Branching futures with probability weighting |

Each producer reads and writes the flat SessionEvent substrate
but may index its private memory using its natural math space.
The brainstorm doc proposed this as a design principle; this
governance doc adopts it as a direction.

**What this means concretely:** when designing a new harness
adapter, start by asking "what is this producer's epistemological
shape?" That answer tells you what claim_key vocabulary to use,
what weights to assign, and what aspects to observe. The projection
spec (`logic/harness-<source>.md`) flows naturally from the
epistemological diagnosis.

## The four tiers of harness governance

We adopt a tiered model for how producers join the governed substrate:

### Tier 0 — First-party (fully trusted)

ix, tars, Demerzel itself. Observation sources are our own code
under our own version control. Trust by construction.

**Signing:** not required.
**Adapter shape:** direct Rust library or colocated CLI binary.
**Review:** standard PR review of the producer code.
**Example:** `ix-harness-tars` (shipped in `9a5d3ab`).

### Tier 1 — Second-party (trusted with attestation)

ga (Guitar Alchemist), employer-adjacent repos, other repos we
own but that run in environments we don't fully control.

**Signing:** future work; once the signature layer exists, Tier 1
adapters must sign their observations.
**Adapter shape:** CLI binary or foreign-language library.
**Review:** PR review + integration test on canonical fixtures.
**Example:** *none yet*. `ix-harness-ga` is planned but not started.

### Tier 2 — Third-party (trusted within scope)

Open-source tools we consume: semgrep, cargo-audit, clippy,
rustfmt, tree-sitter. We don't author them but we trust their
output.

**Signing:** observations are signed by the adapter (which is
first-party) after validating the upstream tool's output against
a pinned schema.
**Adapter shape:** CLI binary.
**Review:** adapter code is first-party; projection spec lives in
`logic/harness-<tool>.md`.
**Example:** *none yet*. Candidates: semgrep, cargo-audit.

### Tier 3 — External (untrusted until verified)

Signals from producers we don't control and can't vouch for:
community contributions, external webhooks, third-party incident
feeds.

**Signing:** required end-to-end; the source must prove its
identity via a signature verifiable against a known public key
registry.
**Adapter shape:** CLI binary with mandatory signature verification
step before emitting observations.
**Review:** adapter code AND signature registry are first-party
artifacts.
**Example:** *none yet*. Requires the signature layer to ship
first.

**Current state:** we have one Tier 0 adapter. Tiers 1-3 are
scoped but not implemented. The governance direction commits to
treating Tier 0 → Tier 3 as a natural progression; each tier
unlocks as the supporting infrastructure ships.

## What Demerzel owns vs what ix owns

The boundary is clearer once harness engineering becomes a
first-class direction:

**Demerzel owns:**
- `schemas/session-event.schema.json` — the canonical wire format
- `logic/hex-merge.md` — merge semantics
- `logic/harness-<source>.md` — per-source projection rules
- `logic/hex-observation-trust.md` — *future*, the trust-tier
  specification
- `schemas/harness-adapter-catalog.json` — *future*, an index of
  all approved adapters and their Demerzel governance docs
- `docs/governance/harness-engineering.md` — this document

**ix owns:**
- `ix-agent-core::SessionEvent` — Rust implementation of the schema
- `ix-fuzzy::observations::merge` — Rust implementation of the
  merge semantics
- `ix-agent::projection` — SessionEvent → HexObservation projection
- `ix-agent::triage` — the triage session consumer
- `ix-harness-<source>` crates — one per first-party source
- `ix-mcp-triage` binary — the main-agent orchestration entry point

**Changes affecting the boundary:** any change that affects
schema, projection rules, merge table, or trust tiers MUST go
through a Demerzel PR first. The ix-side implementation then
tracks the Demerzel change in a follow-up commit.

This is analogous to how RFCs work: IETF publishes the standard;
BIND, djbdns, Unbound implement it. The standard has one owner;
the implementations are many.

## Onboarding checklist for a new harness adapter

When proposing a new adapter:

1. **Epistemological shape.** Which tier? Which math space? What
   does this producer fundamentally observe?

2. **Demerzel PR: projection spec.** Create `logic/harness-<source>.md`
   specifying which native signals map to which HexObservation
   shapes. Include a worked canonical example.

3. **Grammar extension.** If the adapter needs a new aspect (like
   `reliable`), extend `hex-merge.md §Claim Key Grammar` in the
   same PR.

4. **Schema validation.** Update `session-event.schema.json` if
   needed (description updates only — the JSON Schema regex is
   deliberately permissive).

5. **Catalog entry.** Add to `schemas/harness-adapter-catalog.json`
   (once that artifact exists).

6. **Implementation PR in ix.** Create `crates/ix-harness-<source>`
   following the reference implementation at `ix-harness-tars`.
   Library + CLI binary + canonical fixture tests.

7. **End-to-end integration.** Demonstrate the adapter fed into
   `ix_triage_session` via the `prior_observations` parameter,
   with at least one test case showing the escalation gate firing
   correctly on a cross-source contradiction.

8. **Documentation.** Add a walkthrough to
   `ix/docs/walkthroughs/harness-<source>.md` showing real usage.

Each step commits independently. The Demerzel-side artifacts ship
before the ix implementation so there's never a period where code
exists without governance authority.

## The trust-model gap

**This document does not solve the external-source trust problem.**
It names the gap and scopes the path forward.

Current state:
- Observations are trusted by `source` field at face value.
- Tier 0 (first-party) is fine under this model.
- Tier 1, 2, 3 are unsafe until signatures exist.

Required to unlock higher tiers:
1. A public key registry (`schemas/harness-source-keys.json`)
2. A canonical serialization rule for observation payloads
3. A signature verification step in `ix-fuzzy::observations::merge`
   that drops unsigned observations from sources that require
   signing
4. A key rotation policy (`logic/harness-key-rotation.md`)
5. A compromise-response playbook (what to do if a source's
   private key leaks)

Each is substantial. None are blocked. The governance direction
commits to shipping them before any Tier 1+ adapter goes live.

**Near-term implication:** we can harness as many first-party
(Tier 0) sources as we like — tars is the first, ga can be next,
future work in ix-observatory also qualifies. External sources
wait until the signature layer is built.

## What this is NOT

To keep the governance direction honest:

- **Not a replacement for GitHub Actions, Jenkins, or Kubernetes.**
  Those systems execute builds and deploys. The Demerzel substrate
  *governs* their output, merging observations across systems into
  a single escalation-gated decision surface.
- **Not a new DSL.** The adapter contract is in Markdown + JSON
  Schema + Rust. Nothing new to learn beyond what already exists.
- **Not yet horizontally scalable.** The in-process CRDT merge is
  fine for governance-scale decision loads (N observations where
  N is in the hundreds per round). If we ever need millions of
  observations per second, re-architect.
- **Not a product.** It's infrastructure. The value is in what it
  governs, not in the governance itself.

## Why commit to this direction now

Three reasons, in order of increasing strategic weight:

1. **The substrate already exists.** Phase 1 Path C shipped the
   merge, the schema, the projection infrastructure, and the first
   adapter. The marginal cost of the second adapter is low. We'd
   be leaving value on the table by not generalizing.

2. **The trust-model gap is bounded.** First-party harness
   engineering is unblocked today. Second-party and beyond wait
   for the signature layer — which is 2-3 weeks of design+prototype
   work, not months. We're not committing to an infinite-timeline
   project.

3. **The architectural pattern generalizes beyond our repos.** If
   harness-adapter works for tars and ga, it works for any
   producer that can content-hash its output. That's a huge class
   of systems. Adopting this direction positions Demerzel's
   governance model as applicable to AI agent governance AND CI
   harness engineering AND cross-system observation merging — all
   with one substrate.

## Version

1.0 — 2026-04-11 — initial governance direction. Committed to
harness engineering as a first-class architectural direction.
Tier 0 unblocked today via `ix-harness-tars`. Tiers 1-3 gated on
the signature layer (future work).
