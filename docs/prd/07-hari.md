# PRD: hari -- Belief-Substrate Research Sandbox

**Version:** 2.0 | **Last Updated:** 2026-05-02 | **Status:** Active research, library-stable

---

## Executive Summary

Project Hari is a Rust workspace of four library crates exploring a typed, contradiction-preserving epistemic substrate for autoresearch systems. Named after Hari Seldon from Asimov's *Foundation* series, it is the most experimental repo in the ecosystem -- a research sandbox whose differentiated primitives (trust-weighted multi-agent consensus, forward reasoning with derivation provenance, action recommendations) are candidates for graduation into ix-side production crates.

**Relationship to ix-fuzzy.** The Demerzel hex-merge specification (`governance/demerzel/logic/hex-merge.md`) is implemented in `ix-fuzzy::observations` as a CRDT-correct G-Set merge over `Hexavalent` observations. Hari's `hari-lattice::BeliefNetwork` is a parallel implementation of the same hexavalent vocabulary (T/P/U/D/F/C, single-letter wire format compatible with `hexavalent-state.schema.json`) plus features that ix-fuzzy does not currently have: trust-weighted swarm consensus, forward reasoning over typed relations, and derivation provenance. The graduation path: prove these features under research replay, then propose the proven ones for adoption into `ix-fuzzy` or a sibling crate.

## Problem Statement

Autoresearch systems need to track uncertain claims, preserve contradictory evidence, coordinate agent beliefs under explicit trust, derive downstream beliefs from declared logical relations, and recommend what needs more investigation. The original Hari hypothesis -- that Lie-algebra cognitive dynamics would beat simpler baselines -- was tested in Phase 5 and **does not survive comparison against a Subjective Logic baseline** on the fixture suite. SL beats Lie on `false_acceptance_count` 3/6 fixtures, ties 3/6, never loses (`docs/research/phase5-results.md` §6 in the hari repo). The defensible value claim is the substrate (typed claim layer + reasoning + trust-aware consensus + audit trail), not the Lie dynamics that motivated the original hypothesis.

## Goals & Success Metrics

### P0 (Must-Have) -- shipped

- **Build clean**: `cargo build --workspace --all-targets` + `cargo clippy --all-targets --all-features -- -D warnings` pass on stable. Enforced in CI (`.github/workflows/ci.yml`).
- **Test coverage**: `cargo test --all` passes 159 tests across 11 suites at HEAD.
- **Hexavalent vocabulary parity**: `HexValue::{True, Probable, Unknown, Doubtful, False, Contradictory}` matches `ix-types::Hexavalent` semantically. Wire-format compatibility with Demerzel's `hexavalent-state.schema.json` is a follow-up.

### P1 (Should-Have) -- shipped

- **Streaming protocol** (Phase 6): stdio JSONL `serve` mode with deterministic replay parity (`replay --session`). One subprocess per session.
- **Trust-aware swarm consensus** (Phase 4): `TrustModel::RoleWeighted` with self-trust-weighted consensus and message-trust filtering. `AgentVote` events bridge into `Swarm::consensus_with`. `InboxStats::filtered` surfaces dropped low-trust messages.
- **Forward reasoning** (Phase 8): `Implies` / `Supports` / `Contradicts` relations with belief propagation. Derivation provenance (`Derivation { proposition, previous_value, new_value, contributions, round }`) is preserved per event.
- **Substrate decision** (Phase 5 follow-up): default `PriorityModel::RecencyDecay`. `SubjectiveLogic` available as an opt-in `PriorityModel` variant; `Lie` retained as research knob; `Flat` retained for ablation.

### P2 (Nice-to-Have) -- graduation candidates

- **Hex-merge conformance with ix-fuzzy.** Implement the Demerzel hex-merge spec (Belnap-extended table, meta-conflict synthesis, staleness budget K=5) inside Hari and assert byte-equal output against `ix-fuzzy::observations::merge` on a shared fixture set.
- **Trust-weighted observations as an ix-fuzzy candidate.** Propose a `TrustedHexObservation` (observation + per-source trust) extension to ix-fuzzy. Hari's `TrustModel::RoleWeighted` is the reference behavior; the graduation question is whether weight-by-source belongs in the merge layer or stays in a downstream consumer.
- **Forward reasoning over claim_keys.** Hari's `Implies`/`Supports`/`Contradicts` relations operate on propositions; ix-fuzzy's claim_keys carry `action_key::aspect` semantics. The graduation question is whether typed semantic relations between claim_keys belong in ix-fuzzy or in a higher-layer crate.
- **Real IX integration with benchmarks.** Wire is solid (subprocess-tested + Python reference client smoke-tested), but data informing the substrate choice on real autoresearch tasks needs IX itself, not fixtures.

## Key Features (What Exists)

| Crate | Purpose | Internal deps |
|-------|---------|--------------|
| hari-lattice | 6-valued logic + `BeliefNetwork` + propagation with provenance | (leaf) |
| hari-cognition | Lie algebra dynamics, `SymmetryGroup`, `Evolution` (research knob) | nalgebra |
| hari-swarm | `Agent` / `Message` / `Swarm`, `TrustModel`, weighted consensus | hari-lattice + hari-cognition |
| hari-core | `CognitiveLoop`, `ResearchEvent` boundary, SL pipeline, streaming binary | all three |

`hari-swarm` is library-only by design; capabilities reach the IX boundary through `hari-core` via `SessionConfig.{trust_model, use_swarm_consensus, initial_agents}`.

The four `PriorityModel` variants are routable via `SessionConfig.priority_model`:

- **Flat** -- `priority = 1.0`. Pre-Phase-5 default; ablation only.
- **RecencyDecay** -- `priority = exp(-lambda * age)`. **Default since the substrate decision.**
- **Lie** -- `priority = base * (1 + alpha * proj(attention, axis))`. Opt-in research knob.
- **SubjectiveLogic** -- short-circuits to Opinion-fusion pipeline (Jøsang 2016 prior art). Data-best non-Lie option per Phase 5; default change is an explicit owner call.

## Architecture

```
Crate Dependency Flow:
  hari-lattice ──► hari-cognition ──► hari-swarm ──► hari-core
                                                       │
                                                       ▼
                                          (binary: serve | replay | demo)

Streaming Protocol (Phase 6):
  IX (stdin) ──Request JSONL──► hari-core serve ──Response JSONL──► IX (stdout)
                                       │
                                       └── deterministic replay parity:
                                           replay --session traces/recorded.jsonl

Runtime: Rust 1.85+, ndarray-free; nalgebra for Lie path only
CI: GitHub Actions on stable, fmt + clippy + build + test enforced
```

## Current Status

- **Library-stable**: 159 tests across 11 suites. Substrate, reasoning, provenance, swarm bridge, streaming all shipped. Defaults pinned by tests so they cannot drift silently.
- **Active research**: Lie algebra remains as an opt-in `PriorityModel`. Subjective Logic remains as an opt-in `PriorityModel`. New variants must coexist with existing ones.
- **No production consumers yet**: The wire is solid (stdio JSONL streaming, Python reference client at `clients/ix_reference/`), but real IX integration is external work.

## Next Steps

1. **Implement Demerzel hex-merge inside Hari** with byte-equal conformance against `ix-fuzzy::observations::merge`. This gives Hari a clean spec-compliance story and lets differentiated features layer cleanly above the standard merge.
2. **Propose `TrustedHexObservation` to ix-fuzzy.** Cross-repo design conversation; whichever way the layering decision goes, Hari's existing `TrustModel::RoleWeighted` is the reference implementation.
3. **Update the IX-side cross-repo plan** with explicit graduation criteria for each Hari-differentiated primitive (trust-weighting, forward reasoning, derivation provenance).
4. **Real IX integration with benchmarks** (external-blocked).

## Cross-Repo Dependencies

- **Depends on**: Nothing internal to the GuitarAlchemist ecosystem. (External: nalgebra, serde, etc.)
- **Consumed by**: None directly. Streaming protocol designed for IX; not yet wired.
- **Aligned with**: Demerzel's `logic/hex-merge.md` (parallel implementation, conformance pending) and `logic/hexavalent-logic.md` (vocabulary match).
- **Parallel to**: `ix-fuzzy::observations` (CRDT merge) and `ix-types::Hexavalent` (vocabulary). Hari's differentiated features are graduation candidates per the path this PRD describes.
