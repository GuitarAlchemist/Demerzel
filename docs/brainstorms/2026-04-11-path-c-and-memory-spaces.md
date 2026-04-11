# 2026-04-11 — Path C Synthesis + Compact Memory Formats Over Math Spaces

**Status:** Brainstorm record. Multi-AI team session (Codex / Gemini / Claude) followed by Claude-led deep dives and a creative expansion into compact memory file formats using mathematical spaces.

**Scope:** Captures the whole arc from "how do we extend `ix_triage_session` across a process boundary" to "what if ix/tars/Demerzel each had their own memory format grounded in a different mathematical space."

**Reading order:** Read Part 1 first for the coordination substrate decision, then Part 2 for the memory-format exploration. Part 2 only makes sense if Part 1's SessionLog-as-protocol decision is accepted.

---

# Part 1 — Path C (cross-repo governed remediation loop)

## The problem

`ix_triage_session` is live as of `2f8be46`. It exercises every shipped harness primitive in one MCP call: read SessionLog → sample LLM for structured plan → rank via HexavalentDistribution → dispatch through middleware chain → optionally export trace via flywheel → re-ingest.

Path C extends this across the ix ↔ tars process boundary so:
- tars's `diagnose_and_remediate` produces a governed remediation plan
- That plan flows into ix's middleware chain for execution
- Execution results flow back to tars as prior-state context for the next diagnosis round

Constraints:
- ix is Rust, tars is TypeScript, both expose MCP over stdio
- The only shared bus today is the Claude Code client
- Demerzel governance (blast-radius, constitutional boundaries) must apply
- No new ix primitives — compose what's shipped

## Multi-AI brainstorm outputs

### 🔴 Codex (technical feasibility)

Key contributions:
- **The host IS the trust boundary**, not either server. Naive dispatch loses approval and sampling provenance across process hops.
- **Delegation envelope pattern:** every cross-hop request carries `caller`, `diagnosis_id`, `remediation_round`, `plan_hash`, `blast_radius_declared`, `max_steps_remaining`. Mandatory for audit.
- **Provenance killer:** diagnose → govern → execute → re-diagnose without persisting the exact diagnosis snapshot + plan hash makes the feedback loop silently non-reproducible. Audit and rollback break.
- **5 implementation paths, ranked:** loopback HTTP, main-agent shuttle, outbox queue, single-action governor, delegation-scoped token minting.
- **Recommended Phase 1:** main-agent shuttle — zero new cross-server auth, preserves host approval semantics.

### 🟡 Gemini (lateral / ecosystem)

Key contributions:
- **Stigmergy via `ix-cache`:** treat filesystem as shared blackboard. tars writes Intent Manifest, ix middleware auto-injects on sampling.
- **Hexavalent-as-BGP:** use T/P/U/D/F/C labels as routing protocol state. tars marks Provisional (P), ix symbolically executes + upgrades to Decided (D) or halts at Contradictory (C).
- **Sampling-parasitism:** tag sampling requests with `persona: tars-debugger` so the client routes through tars toolset.
- **Contrarian move:** don't build a bridge — build a *shared gravity well* (Kubernetes reconciliation pattern, `ix-cache` = etcd).
- **6-12 month forecast:** MCP-to-MCP emerges as **service-mesh sidecar pattern**. ix becomes Envoy sidecar, tars is microservice.

### 🔵 Claude (pattern / paradox)

Key contributions:
- **Compiler pipeline frame:** tars is frontend (diagnosis AST), ix is backend (dispatch_action IR). SessionLog IS the IR.
- **HexavalentDistribution is already a CRDT semilattice.** (Corrected later: distributions under mixture aren't CRDT, but the *observation set* that derives them IS a G-Set CRDT.)
- **The paradox:** "we need a shared bus" — but both are stdio leaves of the same Claude Code process. The bus exists. It's the conversation.
- **Unnamed concepts:**
  - **Prompt-as-IR**: JSON schema carried in sampling prompts, client-as-translator
  - **Algedonic echo**: loop-detect / blast-radius signals must flow back to tars next round, not die in SessionLog
  - **Constitutional drift budget**: how much hex mass shift per iteration before freezing the loop
- **Three counterintuitive moves:**
  1. tars emits a SessionLog fragment, not a remediation — skip protocol, reuse existing schema
  2. Demerzel as merge function, not referee — CRDT G-counter merge
  3. Flywheel re-ingest IS the feedback channel — loop closes through existing artifact

## Cross-perspective synthesis

**Convergence (multiple providers surfaced independently):**

1. **Main-agent-as-shuttle is the right Phase 1.** Codex arrived from audit safety; Claude from the paradox. Two independent derivations → strong signal.
2. **Structured state is the real protocol.** Codex's delegation envelope ≈ Gemini's convergent state file ≈ Claude's SessionLog fragment. Three framings of the same idea: agree on a schema, skip the wire protocol.
3. **The loop closes through existing artifacts, not new channels.** Gemini's stigmergy, Claude's flywheel re-ingest, Codex's mailbox outbox all reject synchronous RPC.

**Divergence (unique per provider):**
- **Only Codex** surfaced the provenance-killer constraint — losing diagnosis snapshot + plan hash across the hop breaks audit.
- **Only Gemini** named the service-mesh sidecar pattern as the MCP ecosystem's 6-12 month trajectory.
- **Only Claude** saw the CRDT structure + the SessionLog-as-protocol collapse.

## Three deep dives

### Deep dive 1: CRDT HexavalentDistribution merge

Original framing: "HexavalentDistribution is already a CRDT."

**Math check:** distributions under *mixture* (average) fail CRDT laws — mixing is not associative. Pattern-spotter intuition was right but on the wrong level.

**Corrected structure:** G-Set of observations, where each observation is:

```typescript
interface HexObservation {
  source: "tars" | "ix" | "demerzel-merge",
  diagnosis_id: string,        // correlation key
  remediation_round: number,
  ordinal: number,             // monotone within source
  claim_key: string,           // what this observation is ABOUT
  variant: "T"|"P"|"U"|"D"|"F"|"C",
  weight: number,              // (0, 1]
  evidence?: string,
}
```

State = `Set<HexObservation>` deduplicated by `(source, diagnosis_id, round, ordinal)`. Merge = set union. This IS a state-based CRDT:

| Law | Why |
|---|---|
| Commutative | `A ∪ B = B ∪ A` |
| Associative | `(A ∪ B) ∪ C = A ∪ (B ∪ C)` |
| Idempotent | `A ∪ A = A` |
| Monotone | State only grows |

**Key synthesis:** Codex's delegation envelope and the CRDT dedup key are the same fields. Provenance and mergeability are the same requirement.

**Contradiction derivation:** when source A says positive-side (T/P) and source B says negative-side (D/F) on the same claim_key, synthesize a new `C` observation with weight scaled to disagreement strength. Pushes distribution past escalation threshold automatically.

### Deep dive 2: Claim-key design + Belnap-extended contradiction table

**Claim grammar:**
```
claim_key   := action_key "::" aspect
action_key  := tool_name (":" target_hint)?
aspect      := "valuable" | "safe" | "reversible" | "timely" | "reproducible"
```

Default aspect: `valuable`. Reuses loop-detector's `tool_name:target_hint` convention.

**Why aspects matter:** tars says "restart_gpu_service is T valuable" and ix blocks via approval — "restart_gpu_service is F safe". These aren't a direct contradiction (different aspects). But a governance system needs to catch it.

**Meta-conflict rule:** when any action_key has positive-side observations on one aspect AND negative-side observations on another aspect, synthesize `<action>::meta_conflict = C`. Catches the cross-aspect case.

**Belnap table (weights for C synthesis on same claim_key):**

| | T | P | U | D | F | C |
|---|---|---|---|---|---|---|
| **T** | — | — | — | C 0.8 | **C 1.0** | — |
| **P** | — | — | — | C 0.5 | C 0.8 | — |
| **U** | — | — | — | — | — | — |
| **D** | C 0.8 | C 0.5 | — | — | — | — |
| **F** | **C 1.0** | C 0.8 | — | — | — | — |
| **C** | — | — | — | — | — | — |

Rationale:
- T+F = full contradiction (1.0)
- T+D or P+F = strong (0.8) — definite vs evidence-leaning
- P+D = soft (0.5) — both sides only leaning
- U + anything = no synthesis (unknowns don't contradict)
- C preserved, never re-derived

**Same-side pairs (T+P, D+F) are agreement with different confidence, NOT contradiction.**

### Deep dive 3: SessionLog-as-protocol

**The move:** instead of inventing a protocol for cross-repo coordination, extend the SessionLog schema that ix-session already has. tars emits SessionEvents directly; ix reads them.

**Vocabulary analysis:**

| SessionEvent variant | Owner |
|---|---|
| `ActionProposed` | tars + ix (both propose) |
| `BeliefChanged` | tars (observes state), ix (post-execution) |
| `MetadataMounted` | tars (diagnosis facts), ix (middleware verdicts) |
| `ActionBlocked` | ix (middleware) |
| `ActionCompleted` / `ActionFailed` | ix only (executor) |
| `ActionReplaced` | ix only (middleware rewrites) |
| `ObservationAdded` (NEW) | tars + ix + Demerzel merge |

The schema **already** splits naturally along the producer/consumer line. Not designed — discovered.

**Four consequences that reshape the architecture:**

1. **`diagnosis_id` becomes a content hash for free.** `sha256(tars_emit_jsonl)` IS the correlation key. No UUID generation.
2. **Replay is trivial.** `SessionLog::events()` already iterates events from JSONL. Loading historical tars fragments into an empty log IS the replay tool.
3. **The CRDT work absorbs into SessionEvent.** HexObservation becomes `SessionEvent::ObservationAdded`. Two schemas collapse to one. G-Set = set of ObservationAdded events in the log.
4. **Schema ownership moves to Demerzel.** `ix-agent-core` owns the Rust enum; Demerzel owns the canonical JSON Schema and the governance doc for which variants which producers are allowed to emit.

**DNS AXFR analogy (exact):** nobody designed a DNS replication protocol. They reused zone files as the wire format. SessionLog-as-protocol is the same move.

**The insight that sticks:** the SessionLog was an audit trail. It's about to become a coordination protocol. Those are the same thing seen from different angles.

## Unified Path C Phase 1

| Layer | Decision |
|---|---|
| Coordination substrate | SessionLog (JSONL SessionEvents). One format. |
| Schema authority | Demerzel owns `schemas/session-event.schema.json` + governance docs |
| Belief/observation representation | New `SessionEvent::ObservationAdded` variant |
| Merge semantics | G-Set of ObservationAdded events, CRDT-correct by construction |
| Contradiction derivation | Belnap-extended table in `demerzel/logic/hex-merge.md`, runs client-side |
| Feedback channel | Flywheel trace → `trace_to_observations` → append to next round's log |
| tars output format | JSONL fragments, append-ready to any SessionLog |
| `diagnosis_id` | `sha256(tars_fragment_jsonl)` — content-addressable |
| Phase 1 deliverable | SessionLog becomes cross-repo wire format |
| Phase 2 deliverable | `ix_dispatch_action` MCP tool for synchronous cross-process calls |

**Estimated new code:** ~650 LoC unified (vs ~780 CRDT-only, ~300 SessionLog-only, ~400 bespoke JSON).

---

# Part 2 — Compact memory formats over mathematical spaces

## The question

Can ix, tars, and Demerzel each have their own compact file-based memory format grounded in a different mathematical space? Specifically: Euclidean, hyperbolic, and other spaces already implemented in ix's crate ecosystem. Optionally including DNA-inspired or convolutional encodings.

## What ix has in-tree

| Crate | Mathematical content | Memory format potential |
|---|---|---|
| `ix-math` | Linear algebra, statistics | Euclidean embeddings, covariances |
| `ix-topo` | Topological data analysis (persistent homology) | Shape-of-session invariants |
| `ix-fractal` | IFS, fractal dimension | Self-similar replay structures |
| `ix-sedenion` | 16-D hypercomplex (non-associative!) | Order-dependent session products |
| `ix-category` | Category theory / morphisms | State transformations as arrows |
| `ix-rotation` | SO(n), quaternions | Cumulative state as rotation product |
| `ix-graph` | Graph algorithms | Causal DAGs of events |
| `ix-signal` | FFT / signal processing | Frequency-domain session patterns |
| `ix-probabilistic` | Bloom, HyperLogLog, HMM | Approximate membership / cardinality |
| `ix-fuzzy` | HexavalentDistribution | Truth-space belief |
| `ix-chaos` | Lyapunov, dynamical systems | Session sensitivity / attractors |
| `ix-nn` | Neural networks | Learned compression |

This is an unusually rich substrate. Most projects would pull in external libraries; ix has the math in-tree. Therefore memory formats can compose math spaces rather than pick one.

## 10 format ideas (with feasibility flags)

### 1. Poincaré-ball hyperbolic memory (✅ feasible, high impact)

Hyperbolic space H^n has exponential volume growth. Trees embed with bounded distortion. The governance hierarchy IS a tree. Each event gets a Poincaré-ball coordinate; distance = hierarchical distance. O(log N) nearest-neighbor queries.

**Precedent:** Facebook's Poincaré embeddings for WordNet (2017). Real research.

### 2. DNA-codon SessionEvent encoding (✅ feasible, medium impact)

64-codon space, 2 bits per base. Map SessionEvent variants to codons with redundancy. A minimal `ObservationAdded` → ~4 codons = 24 bits = 3 bytes vs ~180 bytes JSON. 60x compression on the tag and provenance; payload needs separate encoding.

**Bonus:** DNA alignment algorithms (Smith-Waterman) find similar event sequences even with insertions/deletions.

### 3. Holographic Reduced Representations (✅ feasible, high impact)

Tony Plate's HRRs: circular convolution binds role + filler into a single vector. Multiple bindings SUM into one fixed-size vector. Retrieval by correlation with a probe.

**Compactness:** O(1) regardless of event count. 10 events or 10 million — same file size.

**Tradeoff:** noisy retrieval, storage capacity ~D/4 distinct bindings with reliable recall.

**Precedent:** Kanerva's Vector Symbolic Architectures (VSA), IBM's brain-inspired computing work. Real literature.

### 4. Sedenion session-product signature (🟡 speculative, beautiful)

Sedenions S^16: 16-dimensional hypercomplex, **non-associative**, contain zero divisors. `(a*b)*c ≠ a*(b*c)` — order of operations matters at the algebra level.

**Proposal:** each SessionEvent variant maps to a sedenion basis element. A session = the sedenion product of its events in order. The sedenion value IS the session signature — can't reorder without changing the product.

**Use case:** cryptographic-grade audit signature derived from math the session already lives in. Replay-proof, reorder-detecting, tamper-evident by algebra.

**Risk:** nobody else uses sedenions for this. ix-sedenion exists. Basis-element assignment is a design choice.

### 5. Fractal IFS regenerative memory (🔴 speculative, high ceiling)

Barnsley's fractal compression: find an IFS whose attractor IS the data. Store the IFS (~60 bytes) instead of the data (KB).

**Problem:** finding the IFS is an inverse problem, hard in general.

**Refinement:** detect self-similar chunks (repetitive triage loops, diagnosis cycles), encode as local IFS, keep non-repeating chunks verbatim. Hybrid adaptive compression.

### 6. Persistent homology as memory summary (🟡 feasible, weird)

Reduce SessionLog to a persistence diagram: bounded set of (birth, death) pairs representing topological features that survive across scales.

- **H_0** = connected components = investigation clusters
- **H_1** = loops = disagreements that persisted then closed

**Use case:** "show me the shape of this 10K-event session" = ~20 persistent features. Lossy executive summary.

### 7. Rotation-group cumulative state (✅ feasible, elegant)

Each event is a rotation in SO(n). Current state = product of all rotations. `n²` floats for the current state regardless of N events. Event generators stored separately for replay.

**Use case:** "what's the current governance posture?" = read one matrix.

### 8. Bloom filter + HyperLogLog side indices (✅ trivial)

Not a format by themselves — perfect side indices for any format. Bloom = "has this tool been called?" in O(1). HLL = "how many distinct targets walked?" in constant memory.

### 9. FFT of event signal (✅ feasible, niche)

Treat event stream as a signal. FFT gives frequency decomposition. Top-k Fourier coefficients = tiny spectral summary. Useful for detecting cron-like or reactive-loop patterns; limited for non-periodic sessions.

### 10. Category-theoretic generator presentation (🔴 speculative, Grothendieck-grade)

A category = generators and relations. Small presentation, large unfolding. Model SessionEvents as morphisms in a state category. Store only generators + sequence of generator indices.

**Bonus:** functors between categories = principled cross-repo translation. Math forces coherence.

**Risk:** requires designing the category. ix-category may or may not expose the right primitives. Months-long exercise.

## Per-agent space assignment

| Agent | Natural space | Why | Primary format |
|---|---|---|---|
| **tars** (diagnostician) | **Euclidean** ℝⁿ | Sensor data, time series, linear metrics — classical metric space | `.sess` + Euclidean side index |
| **ix** (executor) | **Hyperbolic** Hⁿ | Action tree, tool hierarchy, branching search — needs exponential volume growth | `.sess` + Poincaré index |
| **Demerzel** (governance) | **Category / morphism** | Constitutional transformations, policy composition | `.cat` generator presentation (long-term) |

This is not arbitrary. It matches the **epistemological shape** of each agent's work:

- tars *measures* → Euclidean is the home of measurements
- ix *searches and dispatches* → hyperbolic is the home of tree search
- Demerzel *transforms policy* → category theory is the home of structure-preserving transformation

The SessionLog-as-protocol layer becomes the translation substrate between spaces. Each agent reads and writes SessionEvents (flat) but indexes its own memory using its natural math (curved). **Schema is flat; indices are curved.**

## Three-tier proposal

### Tier 1 — ships next (feasible, measurable)

`.sess` binary compact SessionLog format:
- Variable-width integer encoding
- String interning for tool_name, claim_key, source
- Hyperbolic index sidecar (Idea 1)
- Bloom + HLL sidecars (Idea 8)
- SHA-256 integrity trailer

Expected: 10-20x compression vs JSONL, O(log N) hierarchical queries.

### Tier 2 — experimental (feasible, research-grade)

`.hrr` fuzzy memory vector sidecar — single fixed-size HRR vector, all events bound. Purpose: fuzzy long-term memory the agent can correlate against.

### Tier 3 — research experiments (speculative, high ceiling)

One experimental format per math space, each as a tiny module with benchmarks:
- `.hhf` — Hyperbolic + Holographic combined (Tier 1 + 2 flagship)
- `.sdn` — Sedenion session signature
- `.tda` — Persistence diagram summary
- `.ifs` — Fractal regenerative
- `.cat` — Category-theoretic generator presentation

## Counterintuitive moves

### Move A: Different spaces for storage vs index

Storage is always flat (JSONL or binary). The *index* is curved. Math space is a view on flat storage, not a replacement. Best of both: auditable linear record + efficient curved query.

### Move B: DNA codons for tags, not payloads

Everyone thinks "store payload in DNA." Wrong level. Payload is arbitrary JSON; compress with entropy coding. Tags have tiny entropy — 64-codon space is huge. Use biology where biology wins (discrete tag encoding with redundancy).

### Move C: Sedenions as tamper-evident signature, not storage

Don't store session in sedenion algebra. Store in `.sess`. Compute `signature = e_1 * e_2 * ... * e_n` as trailer. Non-associativity makes this a *structural* fingerprint — rearrangement changes the product.

### Move D: Fractal compression for self-similar chunks only

Adaptive to session character. Detect repetitive parts, encode as local IFS. Keep the rest verbatim.

### Move E: Persistent homology as executive summary

Not replacement for detail storage — overview metadata. ~20 features characterizing session shape. Read the diagram first, drill into `.sess` only if needed.

## Dark sides to name

1. **Most of this is over-engineering** for a system currently storing kilobytes per session. Justification must be *structure*, not size — queries that wouldn't work on flat logs.
2. **Every new math space is a new abstraction** requiring maintenance, documentation, audit.
3. **Translation layer is where bugs hide.** Euclidean ↔ hyperbolic ↔ categorical translations must be mathematically correct or indices lie. Test coverage must be extreme.
4. **Fractal and persistent-homology encoders are heavy compute.** Fine for cold storage, wrong for hot path.

## Recommendation

**Tier 1 only, initially.** Build `.sess` with hyperbolic side index. Measure. If compression ratio + query speedup meet a threshold, proceed to Tier 2. Treat Tier 3 as research with one weekend per format, benchmarked against real session data.

**Per-agent space assignment** should be a **Demerzel governance doc first, not code.** Specify the epistemological justification. Let the code follow.

## What's implemented alongside this doc

A minimal experimental crate `ix-memory` with three proof-of-concept modules:

1. **`hrr`** — Holographic Reduced Representations with circular convolution binding and correlation retrieval
2. **`dna`** — DNA-codon encoding for SessionEvent variant tags
3. **`sedenion_sig`** — Sedenion session signature using ix-sedenion multiplication

Plus an `.mem` binary wrapper format that can carry any of the three payload types with magic header + kind tag + SHA-256 integrity.

See `ix/crates/ix-memory/` for the code and `ix/docs/brainstorms/2026-04-11-compact-memory-formats.md` for the Rust-level details.

---

# Appendix — Follow-on threads not taken

Ideas surfaced during the brainstorm that are recorded but not pursued here:

- **Flywheel re-ingest as feedback channel** — already partially addressed via trace_to_observations pattern; the SessionLog-as-protocol absorption makes the separate channel unnecessary
- **Stigmergy via ix-cache as blackboard** — Gemini's idea; judged less elegant than SessionLog-as-protocol but could be a fallback if the SessionLog schema move meets resistance
- **Sampling-parasitism via persona headers** — Gemini's idea; flagged as unsafe (confused-deputy risk)
- **BGP-style remediation routing** — Gemini's idea; interesting analogy but no clear implementation path
- **Kubernetes reconciliation loop** — Gemini's idea; premature, revisit at Phase 3

These are preserved here so future sessions can reconsider them if the primary path hits a wall.
