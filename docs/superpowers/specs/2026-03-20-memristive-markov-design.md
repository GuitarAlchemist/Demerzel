# Memristive Markov Engine — Design Spec (SP1)

**Date:** 2026-03-20
**Status:** Approved
**Version:** 1.1.0
**Sub-project:** 1 of 3 (SP1: math engine, SP2: ix-music, SP3: ga migration)

## Summary

A Rust crate (`memristive-markov`) in the ix ecosystem that provides non-linear, history-dependent Markov chain computation. Combines sparse higher-order transition tensors with memristive conductance (biological memory model), variable-length Markov models (VLMM), and optional reservoir computing — all GPU-acceleratable via ix-gpu/WGPU.

This is the pure math foundation. It knows nothing about music, governance, or any domain. Domain-specific crates (ix-music in SP2) wrap it with semantic types.

## Inspirations

- **Memristors** — resistance depends on history of current flow (non-Markovian)
- **Variable-Length Markov Models (VLMM)** — dynamically choose optimal context length
- **Reservoir Computing** — random sparse networks for temporal pattern recognition
- **Karpathy's autoresearch** — mechanical metrics, iterative improvement
- **Tymoczko's OPTIC** — quotient spaces reduce state dimensionality (consumed by SP2)

## Requirements

- **Pure math** — no domain knowledge, operates on abstract integer states
- **Sparse** — real-world transition tensors are extremely sparse; dense storage is infeasible
- **GPU-accelerated** — hot paths (normalization, conductance decay, reservoir multiply, batch prediction) dispatch to WGPU when available
- **Variable order** — dynamically selects optimal Markov order k per context (VLMM)
- **Memristive memory** — two-layer: volatile session conductance + persistent long-term conductance
- **Serializable** — all state can be exported/imported as JSON for persistence
- **FFI-compatible** — expose a C API for consumption by non-Rust consumers (.NET, Python, etc.)
- **Well-tested** — unit tests, property-based tests (proptest), benchmarks

## Architecture

### Crate Structure

```
ix/crates/memristive-markov/
├── Cargo.toml
├── src/
│   ├── lib.rs              — public API surface
│   ├── tensor.rs           — MarkovTensor<K> sparse tensor
│   ├── conductance.rs      — ConductanceMatrix + memristor update rules
│   ├── vlmm.rs             — VariableOrderSelector (prediction suffix tree)
│   ├── consolidator.rs     — MemoryConsolidator (session → long-term)
│   ├── reservoir.rs        — ReservoirNetwork (optional, feature-gated)
│   ├── engine.rs           — MemristiveEngine (orchestrates all components)
│   ├── sampler.rs          — Sampling strategies (greedy, top-k, nucleus, temperature)
│   ├── gpu/
│   │   ├── mod.rs          — GPU dispatch layer
│   │   ├── normalize.wgsl  — row-wise softmax shader
│   │   ├── decay.wgsl      — bulk conductance decay shader
│   │   ├── reservoir.wgsl  — sparse matrix-vector multiply shader
│   │   └── batch.wgsl      — batch prediction shader
│   ├── ffi.rs              — C-compatible API surface
│   └── serde_state.rs      — JSON serialization for all state
├── benches/
│   ├── tensor_bench.rs
│   ├── conductance_bench.rs
│   └── reservoir_bench.rs
└── tests/
    ├── tensor_tests.rs
    ├── conductance_tests.rs
    ├── vlmm_tests.rs
    ├── consolidator_tests.rs
    ├── engine_integration.rs
    └── proptest_tensor.rs
```

### Feature Flags

```toml
[features]
default = []
gpu = ["ix-gpu", "wgpu"]
reservoir = []
ffi = []
full = ["gpu", "reservoir", "ffi"]
```

## Error Handling

```rust
#[derive(Debug, thiserror::Error)]
pub enum MemristiveError {
    #[error("deserialization failed: {0}")]
    Deserialize(#[from] serde_json::Error),
    #[error("invalid config: {0}")]
    InvalidConfig(String),  // e.g., alpha > 1.0, max_order = 0
    #[error("GPU initialization failed: {0}")]
    GpuInit(String),
    #[error("invalid state index {0}: exceeds state_count {1}")]
    InvalidState(usize, usize),
    #[error("reservoir dimension mismatch: expected {expected}, got {got}")]
    ReservoirDimension { expected: usize, got: usize },
    #[error("engine not warmed up: need at least {needed} observations, have {have}")]
    ColdEngine { needed: usize, have: usize },
}
```

All public methods that can fail return `Result<T, MemristiveError>`.

## Thread Safety

`MemristiveEngine` is **not** `Sync`. It is designed for single-threaded use within a session. Consumers that need concurrent access should use `Arc<Mutex<MemristiveEngine>>`.

The `predict` and `sample` methods take `&mut self` (not `&self`) because they update the VLMM order histogram diagnostic counters. This is intentional — prediction has observable side effects on diagnostics.

For lock-free read-only prediction (e.g., UI displaying probabilities while another thread observes), consumers can clone `EngineDiagnostics` or snapshot the prediction distribution.

## Warm-Up Behavior

The first `max_order` observations will have incomplete context (e.g., after only 2 observations, the context buffer holds `[s1, s2]` but max_order may be 4). These partial-context observations are **recorded normally** — the VLMM handles variable-length contexts, so a 2-state context at order k=2 is valid even when max_order=4. The engine does not discard or special-case early observations.

Consumers can check `diagnostics.total_observations` to determine warm-up status.

## Core Components

### 1. MarkovTensor

Sparse k-order transition tensor.

```rust
pub struct MarkovTensor {
    /// Maximum order supported
    max_order: usize,
    /// Sparse storage: context (Vec<usize>) → next_state → count
    /// Context length determines the order for that entry
    transitions: HashMap<Vec<usize>, HashMap<usize, f64>>,
    /// Number of distinct states observed
    state_count: usize,
    /// Total observations per context (for normalization)
    context_totals: HashMap<Vec<usize>, f64>,
}
```

**Key operations:**
- `observe(context: &[usize], next: usize)` — record a transition (increments count)
- `predict(context: &[usize]) -> Vec<(usize, f64)>` — get probability distribution for next state
- `normalize(context: &[usize])` — ensure probabilities sum to 1.0 (GPU-accelerable for batch)
- `merge(other: &MarkovTensor)` — combine two tensors (for corpus training)
- `sparsity() -> f64` — fraction of zero entries (diagnostic)

**Multi-order storage:** A single MarkovTensor stores all orders simultaneously. An observation of `[A, B, C] → D` also records `[B, C] → D` and `[C] → D`. This enables the VLMM to fall back gracefully.

**GPU acceleration:** Batch normalization dispatches to `normalize.wgsl` — converts sparse rows to dense buffers, runs parallel softmax, writes back.

### 2. ConductanceMatrix

Memristive state that modulates base tensor probabilities.

```rust
pub struct ConductanceMatrix {
    /// Conductance values: (context, next_state) → g ∈ (0, 1]
    /// Uses Vec<usize> as key (not hash) to avoid collision risk.
    /// For large state spaces, consider switching to 128-bit ahash.
    conductances: HashMap<(Vec<usize>, usize), f64>,
    /// Learning rate — how fast conductance strengthens on use
    alpha: f64,  // default 0.1 for session, 0.01 for long-term
    /// Decay rate — how fast conductance weakens on non-use
    beta: f64,   // default 0.01 for session, 0.001 for long-term
    /// Minimum conductance (never reaches zero — biological realism)
    g_min: f64,  // default 0.01
}
```

**Update rules:**
- **On use (Hebbian):** `g = g + α * (1.0 - g)` — asymptotically approaches 1.0
- **On decay (time step):** `g = max(g_min, g - β * g)` — exponential decay toward g_min
- **Bulk decay:** apply decay to all conductances simultaneously (GPU: `decay.wgsl`)

**Effective probability:**
```
effective[context → next] = normalize(base_prob[context → next] * g[context → next])
```

If no conductance entry exists for a transition, default `g = g_min` (minimal but non-zero — allows discovery of new transitions).

### 3. VariableOrderSelector (VLMM)

Dynamically picks the best Markov order for each prediction.

```rust
pub struct VariableOrderSelector {
    /// Minimum observations required to trust a context
    min_observations: usize,  // default 5
    /// Maximum order to attempt
    max_order: usize,         // default 4
    /// Fallback behavior when no context has enough data
    fallback: FallbackStrategy,  // Uniform | MarginalDistribution
}
```

**Selection algorithm (prediction suffix tree):**
1. Start with full context `[s1, s2, ..., sk]` at `k = max_order`
2. Look up `context_totals[context]` in the tensor
3. If total >= `min_observations` → use this order, return prediction
4. If not → drop oldest state: `context = [s2, ..., sk]`, try k-1
5. Continue until k=1 or sufficient data found
6. If k=0 (no context has enough data) → use `fallback` strategy

**Diagnostics:**
- `order_histogram() -> Vec<(usize, usize)>` — how often each order was selected (useful for tuning)
- `effective_order(context: &[usize]) -> usize` — what order would be used for this context

### 4. MemoryConsolidator

Transfers session (volatile) conductance to long-term (persistent) storage.

```rust
pub struct MemoryConsolidator {
    /// Blend rate: how much session influence transfers to long-term
    gamma: f64,  // default 0.1
    /// Minimum session observations before consolidation is worthwhile
    min_session_observations: usize,  // default 20
    /// Whether to decay long-term conductances during consolidation
    decay_on_consolidate: bool,  // default true
}
```

**Consolidation rule:**
```
long_term_g[t → s] = (1 - γ) * long_term_g[t → s] + γ * session_g[t → s]
```

**When to consolidate:** called explicitly by the consumer (e.g., at end of session). Not automatic — the consumer controls lifecycle.

**Export/import:** both session and long-term conductance serialize to JSON for persistence.

### 5. ReservoirNetwork (feature-gated: `reservoir`)

Random sparse network for capturing long-range temporal dependencies.

```rust
pub struct ReservoirNetwork {
    /// Number of reservoir nodes
    size: usize,              // default 256
    /// Sparse weight matrix (reservoir × reservoir), CSR format via ndarray
    weights: ndarray::Array2<f64>,  // sparse via mostly-zero dense; CSR for GPU dispatch
    /// Input weight matrix (input_dim × reservoir)
    input_weights: ndarray::Array2<f64>,
    /// Current reservoir state vector
    state: Vec<f64>,
    /// Spectral radius (controls stability, < 1.0 for echo state property)
    spectral_radius: f64,     // default 0.9
    /// Sparsity of weight matrix (fraction of zero entries)
    sparsity: f64,            // default 0.9
    /// Leaking rate (how much old state persists)
    leak_rate: f64,           // default 0.3
    /// Readout weights (trained via ridge regression), ndarray for linear algebra
    readout: Option<ndarray::Array2<f64>>,
}
```

**Update equation:**
```
state[t] = (1 - leak) * state[t-1] + leak * tanh(W_in * input + W * state[t-1])
output = readout * state[t]
```

**Training:** collect (state, target) pairs during observation, then train readout via ridge regression (closed-form, no gradient descent needed).

**GPU acceleration:** the sparse matrix-vector multiply (`W * state`) dispatches to `reservoir.wgsl`. This is the computational bottleneck.

### 6. MemristiveEngine

Top-level orchestrator that combines all components.

```rust
pub struct MemristiveEngine {
    tensor: MarkovTensor,
    session_conductance: ConductanceMatrix,
    long_term_conductance: Option<ConductanceMatrix>,
    vlmm: VariableOrderSelector,
    consolidator: MemoryConsolidator,
    reservoir: Option<ReservoirNetwork>,
    /// Recent context buffer (last K observed states)
    context_buffer: VecDeque<usize>,
    /// Configuration
    config: EngineConfig,
}
```

**Primary API:**
```rust
impl MemristiveEngine {
    /// Create a new engine with configuration
    fn new(config: EngineConfig) -> Self;

    /// Load from persisted state (JSON)
    fn from_state(json: &str) -> Result<Self>;

    /// Observe a state transition (updates tensor + conductance)
    fn observe(&mut self, state: usize);

    /// Predict next state distribution (tensor * conductance, order selected by VLMM)
    fn predict(&self) -> Vec<(usize, f64)>;

    /// Sample next state using configured strategy (greedy, top-k, nucleus, temperature)
    fn sample(&self, strategy: SamplingStrategy) -> usize;

    /// Batch observe a sequence
    fn observe_sequence(&mut self, states: &[usize]);

    /// Batch predict for multiple contexts (GPU-accelerable)
    fn predict_batch(&self, contexts: &[Vec<usize>]) -> Vec<Vec<(usize, f64)>>;

    /// Consolidate session → long-term memory
    fn consolidate(&mut self);

    /// Discard session conductance without consolidating (start fresh)
    fn reset_session(&mut self);

    /// Export full state as JSON
    fn export_state(&self) -> String;

    /// Get engine diagnostics
    fn diagnostics(&self) -> EngineDiagnostics;
}
```

### 7. Sampler

Sampling strategies for converting probability distributions to concrete predictions.

```rust
pub enum SamplingStrategy {
    /// Always pick highest probability
    Greedy,
    /// Sample from top K candidates
    TopK { k: usize },
    /// Sample from candidates whose cumulative probability <= p
    Nucleus { p: f64 },
    /// Scale probabilities by temperature before sampling
    Temperature { t: f64 },
    /// Combined: temperature + top-k
    TemperatureTopK { t: f64, k: usize },
}
```

### 8. FFI Surface (feature-gated: `ffi`)

C-compatible API for consumption by .NET, Python, etc.

All FFI functions accept non-null pointers only. Null input returns -1 or NULL and sets the last error. All `void*` engine pointers carry an internal type tag to prevent misuse. Errors are retrieved via `mm_last_error`.

```c
// Lifecycle
void* mm_engine_create(const char* config_json);
void* mm_engine_from_state(const char* state_json);
void  mm_engine_destroy(void* engine);

// Observation
void mm_engine_observe(void* engine, uint32_t state);
void mm_engine_observe_sequence(void* engine, const uint32_t* states, size_t len);

// Prediction
uint32_t mm_engine_sample(void* engine, const char* strategy_json);
char*    mm_engine_predict(void* engine);  // returns JSON array of (state, prob)

// Memory
void  mm_engine_consolidate(void* engine);
char* mm_engine_export_state(void* engine);

// Diagnostics
char* mm_engine_diagnostics(void* engine);

// Error reporting
int32_t mm_last_error(char* buf, size_t buf_len);  // copies last error message into buf, returns length

// Memory management
void mm_free_string(char* ptr);
```

## GPU Architecture

### Feature-gated: `gpu`

When the `gpu` feature is enabled, hot paths dispatch to WGPU compute shaders. The CPU implementation is always available as fallback.

```rust
pub trait GpuAccelerable {
    fn cpu_execute(&self, data: &mut [f64]);
    #[cfg(feature = "gpu")]
    fn gpu_execute(&self, gpu: &GpuContext, data: &mut [f64]);

    fn execute(&self, gpu: Option<&GpuContext>, data: &mut [f64]) {
        match gpu {
            #[cfg(feature = "gpu")]
            Some(ctx) => self.gpu_execute(ctx, data),
            _ => self.cpu_execute(data),
        }
    }
}
```

### Shader Operations

| Shader | Operation | Parallelism |
|--------|-----------|-------------|
| `normalize.wgsl` | Row-wise L1 normalization (divide by sum, NOT softmax) on sparse tensor slices | One workgroup per row |
| `decay.wgsl` | Apply conductance decay to all entries | One thread per entry |
| `reservoir.wgsl` | Sparse matrix-vector multiply | One thread per output element |
| `batch.wgsl` | Predict for N contexts simultaneously | One workgroup per context |

### GPU Context

Depends on `ix-gpu` crate. Accepts a reference to `ix_gpu::GpuContext` (which owns `device` and `queue`). The memristive crate manages its own pre-compiled pipelines:

```rust
pub struct MemristivePipelines {
    normalize_pipeline: wgpu::ComputePipeline,
    decay_pipeline: wgpu::ComputePipeline,
    reservoir_pipeline: wgpu::ComputePipeline,
    batch_pipeline: wgpu::ComputePipeline,
}

impl MemristivePipelines {
    /// Compile shaders using the existing ix-gpu context
    pub fn new(gpu: &ix_gpu::GpuContext) -> Self;
}
```

The `MemristiveEngine` optionally holds `(Arc<ix_gpu::GpuContext>, MemristivePipelines)`. It does NOT redefine the GPU context.

## Serialization

All state serializes to JSON via serde:

```rust
#[derive(Serialize, Deserialize)]
pub struct EngineState {
    pub config: EngineConfig,
    pub tensor: MarkovTensorState,
    pub session_conductance: ConductanceState,
    pub long_term_conductance: Option<ConductanceState>,
    pub vlmm_config: VlmmConfig,
    pub consolidator_config: ConsolidatorConfig,
    pub reservoir_state: Option<ReservoirState>,
    pub context_buffer: Vec<usize>,
    pub diagnostics: EngineDiagnostics,
}
```

Consumers persist this JSON however they choose (file system, database, Demerzel state directory, etc.).

## Diagnostics

```rust
pub struct EngineDiagnostics {
    pub total_observations: u64,
    pub unique_states: usize,
    pub tensor_sparsity: f64,
    pub order_histogram: Vec<(usize, u64)>,  // how often each k was used
    pub avg_conductance: f64,
    pub session_observations: u64,
    pub long_term_observations: u64,
    pub reservoir_active: bool,
    pub gpu_available: bool,
}
```

## Testing Strategy

| Test Type | What | Location |
|-----------|------|----------|
| Unit tests | Each component in isolation | `tests/*.rs` |
| Property-based | Tensor normalization always sums to 1.0, conductance bounds [g_min, 1.0] | `tests/proptest_tensor.rs` |
| Integration | Full engine: observe → predict → consolidate cycle | `tests/engine_integration.rs` |
| Benchmarks | Tensor ops, conductance updates, reservoir multiply (CPU vs GPU) | `benches/*.rs` |
| Convergence | Feed known Markov chain, verify stationary distribution recovered | `tests/engine_integration.rs` |

## Dependencies

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
rand = "0.9"                # aligned with ix workspace
ahash = "0.8"               # fast hashing for context keys
ndarray = "0.17"            # aligned with ix-math; used for reservoir state/readout
thiserror = "2"             # error type derivation

[dev-dependencies]
proptest = "1"
criterion = "0.5"

[dependencies.ix-gpu]
path = "../ix-gpu"
optional = true
# wgpu version inherited from ix-gpu (currently v28) — do NOT add separate wgpu dep
```

**Note:** The crate must be added to `[workspace.members]` in `ix/Cargo.toml`.

## Scope Boundaries

**In scope (SP1):**
- `memristive-markov` crate with all 8 components
- GPU shaders (4 compute shaders)
- FFI C API surface
- JSON serialization for all state
- Unit tests, property tests, benchmarks
- Cargo feature flags (gpu, reservoir, ffi)

**Out of scope (SP2: ix-music):**
- Musical types (PitchClass, ChordState, etc.)
- OPTIC quotient spaces and orbifold distance
- HarmonicDistance and style profiles
- MCP tool exposure
- Genre seed profiles

**Out of scope (SP3: ga integration):**
- MemristiveAdapter.fs
- .NET P/Invoke bindings
- ga chatbot integration
- NOTE: ga's core C# domain classes (music theory, scales, chords, intervals) are **preserved** — they are the user's original work. SP3 adds ix as a computation backend alongside ga's domain model, not a replacement. ga's C# classes remain the canonical domain representation; ix-music provides Rust-native equivalents for performance-critical computation paths.

## Future: How SP2 and SP3 Consume This

SP2 (`ix-music`) will:
- Define `TensorIndex` trait mapping musical types → `usize`
- Use OPTIC quotient spaces to reduce state count before indexing
- Wrap `MemristiveEngine` with musical semantics
- Add MCP tools that construct/manage engines

SP3 (ga migration) will:
- Call ix-music via MCP (batch) and FFI (real-time)
- Merge memristive probabilities with remaining grammar weights
- Persist style profiles using engine state export
