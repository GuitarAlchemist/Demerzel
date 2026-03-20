# Memristive Markov Engine Implementation Plan (SP1)

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `memristive-markov`, a Rust crate in the ix ecosystem providing sparse higher-order Markov tensors with memristive conductance, variable-length Markov models, and GPU acceleration.

**Architecture:** Sparse transition tensors store multi-order state probabilities. A conductance matrix modulates probabilities via Hebbian learning + exponential decay (memristor model). A VLMM selector dynamically picks optimal context length. Optional reservoir computing for long-range temporal patterns. GPU shaders accelerate hot paths via ix-gpu.

**Tech Stack:** Rust, ndarray 0.17, wgpu 28 (via ix-gpu), serde, ahash, proptest, criterion

**Spec:** `docs/superpowers/specs/2026-03-20-memristive-markov-design.md` v1.1.0

**Repo:** `C:\Users\spare\source\repos\ix` — workspace member at `crates/memristive-markov`

**Conventions:** ix crates use inline `#[cfg(test)]` modules (not separate test dirs), workspace dependency versions, and `version.workspace = true` in Cargo.toml.

---

## File Map

| File | Purpose |
|------|---------|
| `crates/memristive-markov/Cargo.toml` | Crate manifest with feature flags |
| `crates/memristive-markov/src/lib.rs` | Public API re-exports |
| `crates/memristive-markov/src/error.rs` | `MemristiveError` enum |
| `crates/memristive-markov/src/tensor.rs` | `MarkovTensor` — sparse k-order transitions |
| `crates/memristive-markov/src/conductance.rs` | `ConductanceMatrix` — memristive state |
| `crates/memristive-markov/src/vlmm.rs` | `VariableOrderSelector` — prediction suffix tree |
| `crates/memristive-markov/src/sampler.rs` | `SamplingStrategy` — greedy, top-k, nucleus, temperature |
| `crates/memristive-markov/src/consolidator.rs` | `MemoryConsolidator` — session → long-term |
| `crates/memristive-markov/src/engine.rs` | `MemristiveEngine` — top-level orchestrator |
| `crates/memristive-markov/src/serde_state.rs` | JSON serialization for all state |
| `crates/memristive-markov/src/reservoir.rs` | `ReservoirNetwork` (feature-gated: `reservoir`) |
| `crates/memristive-markov/src/ffi.rs` | C-compatible API (feature-gated: `ffi`) |
| `crates/memristive-markov/src/gpu/mod.rs` | GPU dispatch (feature-gated: `gpu`) |
| `crates/memristive-markov/src/gpu/normalize.wgsl` | L1 normalization shader |
| `crates/memristive-markov/src/gpu/decay.wgsl` | Bulk conductance decay shader |
| `crates/memristive-markov/benches/engine_bench.rs` | Criterion benchmarks |
| `Cargo.toml` (workspace root) | Add `crates/memristive-markov` to members |

---

## Task 1: Crate Scaffolding + Error Type

Set up the crate, workspace registration, and foundational error type.

**Files:**
- Create: `crates/memristive-markov/Cargo.toml`
- Create: `crates/memristive-markov/src/lib.rs`
- Create: `crates/memristive-markov/src/error.rs`
- Modify: `Cargo.toml` (workspace root)

- [ ] **Step 1: Create crate directory**

```bash
mkdir -p crates/memristive-markov/src
```

- [ ] **Step 2: Write Cargo.toml**

Write `crates/memristive-markov/Cargo.toml`:

```toml
[package]
name = "memristive-markov"
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true
rust-version.workspace = true
categories = ["algorithms", "mathematics", "science"]
keywords = ["markov-chain", "memristor", "probabilistic", "machine-learning"]
description = "Non-linear Markov chains with memristive conductance, VLMM, and GPU acceleration"

[features]
default = []
gpu = ["dep:ix-gpu"]
reservoir = []
ffi = []
full = ["gpu", "reservoir", "ffi"]

[dependencies]
serde = { workspace = true }
serde_json = { workspace = true }
rand = { workspace = true }
ndarray = { workspace = true }
thiserror = { workspace = true }
ahash = "0.8"

[dependencies.ix-gpu]
path = "../ix-gpu"
optional = true

[dev-dependencies]
proptest = "1"
criterion = "0.5"

[[bench]]
name = "engine_bench"
harness = false
```

- [ ] **Step 3: Write error.rs**

Write `crates/memristive-markov/src/error.rs`:

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum MemristiveError {
    #[error("deserialization failed: {0}")]
    Deserialize(#[from] serde_json::Error),

    #[error("invalid config: {0}")]
    InvalidConfig(String),

    #[error("invalid state index {index}: exceeds state_count {state_count}")]
    InvalidState { index: usize, state_count: usize },

    #[error("reservoir dimension mismatch: expected {expected}, got {got}")]
    ReservoirDimension { expected: usize, got: usize },

    #[error("engine not warmed up: need at least {needed} observations, have {have}")]
    ColdEngine { needed: usize, have: usize },

    #[cfg(feature = "gpu")]
    #[error("GPU initialization failed: {0}")]
    GpuInit(String),
}

pub type Result<T> = std::result::Result<T, MemristiveError>;
```

- [ ] **Step 4: Write lib.rs with module declarations**

Write `crates/memristive-markov/src/lib.rs`:

```rust
pub mod error;
pub mod tensor;
pub mod conductance;
pub mod vlmm;
pub mod sampler;
pub mod consolidator;
pub mod engine;
pub mod serde_state;

#[cfg(feature = "reservoir")]
pub mod reservoir;

#[cfg(feature = "ffi")]
pub mod ffi;

#[cfg(feature = "gpu")]
pub mod gpu;

pub use error::{MemristiveError, Result};
pub use tensor::MarkovTensor;
pub use conductance::ConductanceMatrix;
pub use vlmm::VariableOrderSelector;
pub use sampler::SamplingStrategy;
pub use consolidator::MemoryConsolidator;
pub use engine::MemristiveEngine;
```

- [ ] **Step 5: Add workspace member**

Add to `Cargo.toml` (workspace root) in the `[workspace] members` list:

```toml
    "crates/memristive-markov",
```

- [ ] **Step 6: Create stub modules so it compiles**

Create minimal stub files for each module so `cargo check` passes:

`crates/memristive-markov/src/tensor.rs`:
```rust
pub struct MarkovTensor;
```

`crates/memristive-markov/src/conductance.rs`:
```rust
pub struct ConductanceMatrix;
```

`crates/memristive-markov/src/vlmm.rs`:
```rust
pub struct VariableOrderSelector;
```

`crates/memristive-markov/src/sampler.rs`:
```rust
pub enum SamplingStrategy { Greedy }
```

`crates/memristive-markov/src/consolidator.rs`:
```rust
pub struct MemoryConsolidator;
```

`crates/memristive-markov/src/engine.rs`:
```rust
pub struct MemristiveEngine;
```

`crates/memristive-markov/src/serde_state.rs`:
```rust
// Serialization types — implemented in Task 7
```

`crates/memristive-markov/benches/engine_bench.rs`:
```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_placeholder(c: &mut Criterion) {
    c.bench_function("placeholder", |b| b.iter(|| 1 + 1));
}

criterion_group!(benches, bench_placeholder);
criterion_main!(benches);
```

- [ ] **Step 7: Verify it compiles**

```bash
cd C:/Users/spare/source/repos/ix && cargo check -p memristive-markov
```

Expected: compiles with no errors.

- [ ] **Step 8: Commit**

```bash
git add crates/memristive-markov/ Cargo.toml
git commit -m "feat: scaffold memristive-markov crate — error type, stubs, workspace registration"
```

---

## Task 2: MarkovTensor — Sparse Multi-Order Transitions

The core data structure. TDD: write tests first, then implement.

**Files:**
- Modify: `crates/memristive-markov/src/tensor.rs`

- [ ] **Step 1: Write tests**

Replace `tensor.rs` with tests at the bottom:

```rust
use std::collections::HashMap;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MarkovTensor {
    max_order: usize,
    /// context → (next_state → count)
    transitions: HashMap<Vec<usize>, HashMap<usize, f64>>,
    context_totals: HashMap<Vec<usize>, f64>,
    state_count: usize,
}

// Implementation will go here

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_tensor_is_empty() {
        let t = MarkovTensor::new(3);
        assert_eq!(t.max_order(), 3);
        assert_eq!(t.state_count(), 0);
        assert!(t.sparsity() == 1.0 || t.sparsity().is_nan());
    }

    #[test]
    fn test_observe_single_transition() {
        let mut t = MarkovTensor::new(2);
        t.observe(&[0, 1], 2);
        let dist = t.predict(&[0, 1]);
        assert_eq!(dist.len(), 1);
        assert_eq!(dist[0], (2, 1.0));
    }

    #[test]
    fn test_observe_multi_order_storage() {
        let mut t = MarkovTensor::new(3);
        // Observing [A,B,C]→D should also store [B,C]→D and [C]→D
        t.observe(&[0, 1, 2], 3);
        assert!(!t.predict(&[0, 1, 2]).is_empty());
        assert!(!t.predict(&[1, 2]).is_empty());
        assert!(!t.predict(&[2]).is_empty());
    }

    #[test]
    fn test_probabilities_sum_to_one() {
        let mut t = MarkovTensor::new(2);
        t.observe(&[0, 1], 2);
        t.observe(&[0, 1], 3);
        t.observe(&[0, 1], 2);
        let dist = t.predict(&[0, 1]);
        let total: f64 = dist.iter().map(|(_, p)| p).sum();
        assert!((total - 1.0).abs() < 1e-10);
        // state 2 should have 2/3, state 3 should have 1/3
        let p2 = dist.iter().find(|(s, _)| *s == 2).unwrap().1;
        let p3 = dist.iter().find(|(s, _)| *s == 3).unwrap().1;
        assert!((p2 - 2.0 / 3.0).abs() < 1e-10);
        assert!((p3 - 1.0 / 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_predict_unknown_context_returns_empty() {
        let t = MarkovTensor::new(2);
        let dist = t.predict(&[99, 100]);
        assert!(dist.is_empty());
    }

    #[test]
    fn test_merge_tensors() {
        let mut t1 = MarkovTensor::new(2);
        t1.observe(&[0, 1], 2);
        let mut t2 = MarkovTensor::new(2);
        t2.observe(&[0, 1], 3);
        t1.merge(&t2);
        let dist = t1.predict(&[0, 1]);
        assert_eq!(dist.len(), 2);
    }

    #[test]
    fn test_state_count_tracks_unique_states() {
        let mut t = MarkovTensor::new(2);
        t.observe(&[0, 1], 2);
        t.observe(&[0, 1], 2); // duplicate
        t.observe(&[3, 4], 5);
        assert_eq!(t.state_count(), 6); // states 0,1,2,3,4,5
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cargo test -p memristive-markov -- tensor::tests
```

Expected: FAIL — methods not implemented.

- [ ] **Step 3: Implement MarkovTensor**

Add implementation between the struct and tests:

```rust
impl MarkovTensor {
    pub fn new(max_order: usize) -> Self {
        Self {
            max_order,
            transitions: HashMap::new(),
            context_totals: HashMap::new(),
            state_count: 0,
        }
    }

    pub fn max_order(&self) -> usize {
        self.max_order
    }

    pub fn state_count(&self) -> usize {
        self.state_count
    }

    pub fn sparsity(&self) -> f64 {
        if self.state_count == 0 {
            return 1.0;
        }
        let total_possible: f64 = self.context_totals.len() as f64 * self.state_count as f64;
        if total_possible == 0.0 {
            return 1.0;
        }
        let total_nonzero: f64 = self.transitions.values().map(|m| m.len() as f64).sum();
        1.0 - (total_nonzero / total_possible)
    }

    /// Observe a transition: given context, next state occurred.
    /// Also records at all lower orders for VLMM fallback.
    pub fn observe(&mut self, context: &[usize], next: usize) {
        // Track unique states
        for &s in context.iter().chain(std::iter::once(&next)) {
            if s >= self.state_count {
                self.state_count = s + 1;
            }
        }

        // Record at all orders from full context down to order 1
        let len = context.len().min(self.max_order);
        for start in 0..len {
            let ctx = context[start..].to_vec();
            *self.transitions.entry(ctx.clone()).or_default().entry(next).or_insert(0.0) += 1.0;
            *self.context_totals.entry(ctx).or_insert(0.0) += 1.0;
        }

        // Also record order-0 (marginal distribution) with empty context
        *self.transitions.entry(vec![]).or_default().entry(next).or_insert(0.0) += 1.0;
        *self.context_totals.entry(vec![]).or_insert(0.0) += 1.0;
    }

    /// Get probability distribution for next state given context.
    /// Returns empty vec if context has never been seen.
    pub fn predict(&self, context: &[usize]) -> Vec<(usize, f64)> {
        let ctx = context.to_vec();
        match (self.transitions.get(&ctx), self.context_totals.get(&ctx)) {
            (Some(next_map), Some(&total)) if total > 0.0 => {
                next_map.iter().map(|(&state, &count)| (state, count / total)).collect()
            }
            _ => Vec::new(),
        }
    }

    /// Get raw observation count for a context
    pub fn context_count(&self, context: &[usize]) -> f64 {
        self.context_totals.get(context.as_ref() as &Vec<usize>).copied().unwrap_or(0.0)
    }

    /// Merge another tensor into this one (additive counts)
    pub fn merge(&mut self, other: &MarkovTensor) {
        for (ctx, next_map) in &other.transitions {
            for (&state, &count) in next_map {
                *self.transitions.entry(ctx.clone()).or_default().entry(state).or_insert(0.0) += count;
            }
        }
        for (ctx, &total) in &other.context_totals {
            *self.context_totals.entry(ctx.clone()).or_insert(0.0) += total;
        }
        self.state_count = self.state_count.max(other.state_count);
    }
}
```

- [ ] **Step 4: Run tests**

```bash
cargo test -p memristive-markov -- tensor::tests
```

Expected: all 7 tests pass.

- [ ] **Step 5: Commit**

```bash
git add crates/memristive-markov/src/tensor.rs
git commit -m "feat: MarkovTensor — sparse multi-order transition storage with TDD"
```

---

## Task 3: ConductanceMatrix — Memristive State

**Files:**
- Modify: `crates/memristive-markov/src/conductance.rs`

- [ ] **Step 1: Write tests and struct**

Replace `conductance.rs`:

```rust
use std::collections::HashMap;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConductanceMatrix {
    conductances: HashMap<(Vec<usize>, usize), f64>,
    alpha: f64,
    beta: f64,
    g_min: f64,
}

// Implementation will go here

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_conductance_is_g_min() {
        let cm = ConductanceMatrix::new(0.1, 0.01, 0.01);
        assert_eq!(cm.get(&[0, 1], 2), 0.01);
    }

    #[test]
    fn test_hebbian_strengthens() {
        let mut cm = ConductanceMatrix::new(0.1, 0.01, 0.01);
        cm.strengthen(&[0, 1], 2);
        let g = cm.get(&[0, 1], 2);
        assert!(g > 0.01, "Should strengthen above g_min: {}", g);
    }

    #[test]
    fn test_hebbian_asymptotes_at_one() {
        let mut cm = ConductanceMatrix::new(0.5, 0.01, 0.01);
        for _ in 0..100 {
            cm.strengthen(&[0], 1);
        }
        let g = cm.get(&[0], 1);
        assert!(g > 0.99 && g <= 1.0, "Should approach 1.0: {}", g);
    }

    #[test]
    fn test_decay_weakens() {
        let mut cm = ConductanceMatrix::new(0.1, 0.1, 0.01);
        cm.strengthen(&[0], 1);
        let before = cm.get(&[0], 1);
        cm.decay_all();
        let after = cm.get(&[0], 1);
        assert!(after < before, "Decay should weaken: {} -> {}", before, after);
    }

    #[test]
    fn test_decay_floors_at_g_min() {
        let mut cm = ConductanceMatrix::new(0.1, 0.99, 0.05);
        cm.strengthen(&[0], 1);
        for _ in 0..100 {
            cm.decay_all();
        }
        let g = cm.get(&[0], 1);
        assert!(g >= 0.05, "Should not go below g_min: {}", g);
    }

    #[test]
    fn test_modulate_probabilities() {
        let mut cm = ConductanceMatrix::new(0.5, 0.01, 0.01);
        // Strengthen transition to state 2 heavily
        for _ in 0..20 {
            cm.strengthen(&[0], 2);
        }
        let base_probs = vec![(1, 0.5), (2, 0.5)];
        let modulated = cm.modulate(&[0], &base_probs);
        // State 2 should now have higher probability
        let p2 = modulated.iter().find(|(s, _)| *s == 2).unwrap().1;
        let p1 = modulated.iter().find(|(s, _)| *s == 1).unwrap().1;
        assert!(p2 > p1, "Strengthened state should dominate: p1={}, p2={}", p1, p2);
        // Should still sum to 1.0
        let total: f64 = modulated.iter().map(|(_, p)| p).sum();
        assert!((total - 1.0).abs() < 1e-10);
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cargo test -p memristive-markov -- conductance::tests
```

- [ ] **Step 3: Implement ConductanceMatrix**

```rust
impl ConductanceMatrix {
    pub fn new(alpha: f64, beta: f64, g_min: f64) -> Self {
        Self {
            conductances: HashMap::new(),
            alpha,
            beta,
            g_min,
        }
    }

    /// Get conductance for a transition. Returns g_min if not seen.
    pub fn get(&self, context: &[usize], next: usize) -> f64 {
        self.conductances
            .get(&(context.to_vec(), next))
            .copied()
            .unwrap_or(self.g_min)
    }

    /// Hebbian strengthening: g += alpha * (1 - g)
    pub fn strengthen(&mut self, context: &[usize], next: usize) {
        let key = (context.to_vec(), next);
        let g = self.conductances.entry(key).or_insert(self.g_min);
        *g += self.alpha * (1.0 - *g);
    }

    /// Decay all conductances: g = max(g_min, g * (1 - beta))
    pub fn decay_all(&mut self) {
        let g_min = self.g_min;
        let beta = self.beta;
        self.conductances.values_mut().for_each(|g| {
            *g = (*g * (1.0 - beta)).max(g_min);
        });
    }

    /// Modulate base probabilities by conductance, re-normalize.
    pub fn modulate(&self, context: &[usize], base_probs: &[(usize, f64)]) -> Vec<(usize, f64)> {
        let weighted: Vec<(usize, f64)> = base_probs
            .iter()
            .map(|&(state, prob)| {
                let g = self.get(context, state);
                (state, prob * g)
            })
            .collect();

        let total: f64 = weighted.iter().map(|(_, w)| w).sum();
        if total == 0.0 {
            return base_probs.to_vec();
        }
        weighted.into_iter().map(|(s, w)| (s, w / total)).collect()
    }

    pub fn alpha(&self) -> f64 { self.alpha }
    pub fn beta(&self) -> f64 { self.beta }
    pub fn g_min(&self) -> f64 { self.g_min }
    pub fn len(&self) -> usize { self.conductances.len() }
    pub fn is_empty(&self) -> bool { self.conductances.is_empty() }
}
```

- [ ] **Step 4: Run tests**

```bash
cargo test -p memristive-markov -- conductance::tests
```

Expected: all 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add crates/memristive-markov/src/conductance.rs
git commit -m "feat: ConductanceMatrix — Hebbian strengthening + exponential decay with TDD"
```

---

## Task 4: VLMM + Sampler

**Files:**
- Modify: `crates/memristive-markov/src/vlmm.rs`
- Modify: `crates/memristive-markov/src/sampler.rs`

- [ ] **Step 1: Write VLMM with tests**

Replace `vlmm.rs`:

```rust
use serde::{Serialize, Deserialize};
use crate::tensor::MarkovTensor;

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum FallbackStrategy {
    Uniform,
    MarginalDistribution,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VariableOrderSelector {
    min_observations: usize,
    max_order: usize,
    fallback: FallbackStrategy,
    order_counts: Vec<u64>,
}

impl VariableOrderSelector {
    pub fn new(max_order: usize, min_observations: usize, fallback: FallbackStrategy) -> Self {
        Self {
            min_observations,
            max_order,
            fallback,
            order_counts: vec![0; max_order + 1],
        }
    }

    /// Select best order and return prediction from tensor.
    /// Tries highest order first, falls back to lower if insufficient data.
    pub fn predict(&mut self, tensor: &MarkovTensor, context: &[usize]) -> Vec<(usize, f64)> {
        let max_k = context.len().min(self.max_order);

        for k in (1..=max_k).rev() {
            let ctx = &context[context.len() - k..];
            let count = tensor.context_count(ctx);
            if count >= self.min_observations as f64 {
                self.order_counts[k] += 1;
                return tensor.predict(ctx);
            }
        }

        // Fallback: try marginal (order 0) or uniform
        self.order_counts[0] += 1;
        match self.fallback {
            FallbackStrategy::MarginalDistribution => tensor.predict(&[]),
            FallbackStrategy::Uniform => {
                let n = tensor.state_count();
                if n == 0 { return vec![]; }
                let p = 1.0 / n as f64;
                (0..n).map(|s| (s, p)).collect()
            }
        }
    }

    pub fn effective_order(&self, tensor: &MarkovTensor, context: &[usize]) -> usize {
        let max_k = context.len().min(self.max_order);
        for k in (1..=max_k).rev() {
            let ctx = &context[context.len() - k..];
            if tensor.context_count(ctx) >= self.min_observations as f64 {
                return k;
            }
        }
        0
    }

    pub fn order_histogram(&self) -> &[u64] {
        &self.order_counts
    }

    pub fn reset_counts(&mut self) {
        self.order_counts.fill(0);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vlmm_uses_highest_order_with_data() {
        let mut t = MarkovTensor::new(3);
        // Add enough data at order 2
        for _ in 0..10 {
            t.observe(&[0, 1], 2);
        }
        let mut vlmm = VariableOrderSelector::new(3, 5, FallbackStrategy::Uniform);
        let dist = vlmm.predict(&t, &[0, 1]);
        assert!(!dist.is_empty());
        assert_eq!(vlmm.effective_order(&t, &[0, 1]), 2);
    }

    #[test]
    fn test_vlmm_falls_back_on_sparse_data() {
        let mut t = MarkovTensor::new(3);
        // Only 2 observations at order 2 (below threshold of 5)
        t.observe(&[0, 1], 2);
        t.observe(&[0, 1], 3);
        // But 10 at order 1
        for _ in 0..8 {
            t.observe(&[1], 2);
        }
        let mut vlmm = VariableOrderSelector::new(3, 5, FallbackStrategy::MarginalDistribution);
        let _dist = vlmm.predict(&t, &[0, 1]);
        assert_eq!(vlmm.effective_order(&t, &[0, 1]), 1);
    }

    #[test]
    fn test_vlmm_uniform_fallback() {
        let mut t = MarkovTensor::new(2);
        t.observe(&[0], 1); // only 1 observation, below threshold
        let mut vlmm = VariableOrderSelector::new(2, 5, FallbackStrategy::Uniform);
        let dist = vlmm.predict(&t, &[99]);
        // Should fall back to uniform over 2 known states
        assert!(dist.len() >= 2);
    }

    #[test]
    fn test_order_histogram_tracks_usage() {
        let mut t = MarkovTensor::new(2);
        for _ in 0..10 {
            t.observe(&[0, 1], 2);
        }
        let mut vlmm = VariableOrderSelector::new(2, 5, FallbackStrategy::Uniform);
        vlmm.predict(&t, &[0, 1]);
        vlmm.predict(&t, &[0, 1]);
        assert_eq!(vlmm.order_histogram()[2], 2);
    }
}
```

- [ ] **Step 2: Write Sampler**

Replace `sampler.rs`:

```rust
use rand::Rng;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SamplingStrategy {
    Greedy,
    TopK { k: usize },
    Nucleus { p: f64 },
    Temperature { t: f64 },
    TemperatureTopK { t: f64, k: usize },
}

impl SamplingStrategy {
    /// Sample from a probability distribution using this strategy.
    /// `dist` must be non-empty and sum to ~1.0.
    pub fn sample(&self, dist: &[(usize, f64)], rng: &mut impl Rng) -> Option<usize> {
        if dist.is_empty() {
            return None;
        }

        match self {
            SamplingStrategy::Greedy => {
                dist.iter().max_by(|a, b| a.1.partial_cmp(&b.1).unwrap()).map(|&(s, _)| s)
            }
            SamplingStrategy::TopK { k } => {
                let mut sorted: Vec<_> = dist.to_vec();
                sorted.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
                sorted.truncate(*k);
                Self::weighted_sample(&sorted, rng)
            }
            SamplingStrategy::Nucleus { p } => {
                let mut sorted: Vec<_> = dist.to_vec();
                sorted.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
                let mut cumulative = 0.0;
                let truncated: Vec<_> = sorted
                    .into_iter()
                    .take_while(|&(_, prob)| {
                        let include = cumulative < *p;
                        cumulative += prob;
                        include
                    })
                    .collect();
                Self::weighted_sample(&truncated, rng)
            }
            SamplingStrategy::Temperature { t } => {
                let scaled = Self::apply_temperature(dist, *t);
                Self::weighted_sample(&scaled, rng)
            }
            SamplingStrategy::TemperatureTopK { t, k } => {
                let scaled = Self::apply_temperature(dist, *t);
                let mut sorted = scaled;
                sorted.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
                sorted.truncate(*k);
                Self::weighted_sample(&sorted, rng)
            }
        }
    }

    fn apply_temperature(dist: &[(usize, f64)], t: f64) -> Vec<(usize, f64)> {
        let t = t.max(1e-10);
        let scaled: Vec<f64> = dist.iter().map(|(_, p)| (p.ln() / t).exp()).collect();
        let total: f64 = scaled.iter().sum();
        dist.iter()
            .zip(scaled.iter())
            .map(|(&(s, _), &w)| (s, w / total))
            .collect()
    }

    fn weighted_sample(dist: &[(usize, f64)], rng: &mut impl Rng) -> Option<usize> {
        if dist.is_empty() {
            return None;
        }
        let total: f64 = dist.iter().map(|(_, p)| p).sum();
        let mut r: f64 = rng.random::<f64>() * total;
        for &(state, prob) in dist {
            r -= prob;
            if r <= 0.0 {
                return Some(state);
            }
        }
        Some(dist.last().unwrap().0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;

    fn test_rng() -> rand::rngs::StdRng {
        rand::rngs::StdRng::seed_from_u64(42)
    }

    #[test]
    fn test_greedy_picks_highest() {
        let dist = vec![(0, 0.1), (1, 0.7), (2, 0.2)];
        let result = SamplingStrategy::Greedy.sample(&dist, &mut test_rng());
        assert_eq!(result, Some(1));
    }

    #[test]
    fn test_top_k_limits_candidates() {
        let dist = vec![(0, 0.5), (1, 0.3), (2, 0.15), (3, 0.05)];
        let mut rng = test_rng();
        // Sample many times with top-2, should never get states 2 or 3
        for _ in 0..100 {
            let s = SamplingStrategy::TopK { k: 2 }.sample(&dist, &mut rng).unwrap();
            assert!(s <= 1, "TopK(2) should only produce states 0 or 1, got {}", s);
        }
    }

    #[test]
    fn test_empty_dist_returns_none() {
        let result = SamplingStrategy::Greedy.sample(&[], &mut test_rng());
        assert_eq!(result, None);
    }

    #[test]
    fn test_temperature_low_concentrates() {
        let dist = vec![(0, 0.5), (1, 0.3), (2, 0.2)];
        let scaled = SamplingStrategy::apply_temperature(&dist, 0.1);
        // Low temperature should make highest prob dominate
        assert!(scaled[0].1 > 0.9, "Low temp should concentrate: {:?}", scaled);
    }
}
```

- [ ] **Step 3: Run all tests**

```bash
cargo test -p memristive-markov -- vlmm::tests sampler::tests
```

Expected: all 8 tests pass.

- [ ] **Step 4: Commit**

```bash
git add crates/memristive-markov/src/vlmm.rs crates/memristive-markov/src/sampler.rs
git commit -m "feat: VLMM variable-order selector + sampling strategies with TDD"
```

---

## Task 5: MemoryConsolidator + Serialization

**Files:**
- Modify: `crates/memristive-markov/src/consolidator.rs`
- Modify: `crates/memristive-markov/src/serde_state.rs`

- [ ] **Step 1: Write MemoryConsolidator with tests**

Replace `consolidator.rs`:

```rust
use serde::{Serialize, Deserialize};
use crate::conductance::ConductanceMatrix;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryConsolidator {
    gamma: f64,
    min_session_observations: usize,
    decay_on_consolidate: bool,
}

impl MemoryConsolidator {
    pub fn new(gamma: f64, min_session_observations: usize) -> Self {
        Self {
            gamma,
            min_session_observations,
            decay_on_consolidate: true,
        }
    }

    /// Transfer session conductance into long-term.
    /// long_term_g = (1 - gamma) * long_term_g + gamma * session_g
    pub fn consolidate(
        &self,
        session: &ConductanceMatrix,
        long_term: &mut ConductanceMatrix,
        session_observations: usize,
    ) -> bool {
        if session_observations < self.min_session_observations {
            return false;
        }

        // For each conductance in session, blend into long-term
        // This requires iterating session's entries
        // We'll use the merge approach: for each key in session, update long_term
        session.for_each(|context, next, session_g| {
            let lt_g = long_term.get(context, next);
            let blended = (1.0 - self.gamma) * lt_g + self.gamma * session_g;
            long_term.set(context, next, blended);
        });

        if self.decay_on_consolidate {
            long_term.decay_all();
        }

        true
    }

    pub fn gamma(&self) -> f64 { self.gamma }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_consolidation_blends() {
        let mut session = ConductanceMatrix::new(0.5, 0.01, 0.01);
        for _ in 0..10 {
            session.strengthen(&[0], 1);
        }
        let session_g = session.get(&[0], 1);

        let mut long_term = ConductanceMatrix::new(0.01, 0.001, 0.01);
        let consolidator = MemoryConsolidator::new(0.1, 5);
        let did = consolidator.consolidate(&session, &mut long_term, 10);
        assert!(did);

        let lt_g = long_term.get(&[0], 1);
        // Should be between g_min and session_g
        assert!(lt_g > 0.01 && lt_g < session_g, "Blended: {}", lt_g);
    }

    #[test]
    fn test_consolidation_skips_below_threshold() {
        let session = ConductanceMatrix::new(0.5, 0.01, 0.01);
        let mut long_term = ConductanceMatrix::new(0.01, 0.001, 0.01);
        let consolidator = MemoryConsolidator::new(0.1, 20);
        let did = consolidator.consolidate(&session, &mut long_term, 5);
        assert!(!did);
    }
}
```

- [ ] **Step 2: Add iteration methods to ConductanceMatrix**

Add to `conductance.rs`:

```rust
    /// Iterate over all conductance entries
    pub fn for_each(&self, mut f: impl FnMut(&[usize], usize, f64)) {
        for ((context, next), &g) in &self.conductances {
            f(context, *next, g);
        }
    }

    /// Set conductance directly (used by consolidator)
    pub fn set(&mut self, context: &[usize], next: usize, g: f64) {
        self.conductances.insert((context.to_vec(), next), g.max(self.g_min));
    }
```

- [ ] **Step 3: Write serde_state.rs**

Replace `serde_state.rs`:

```rust
use serde::{Serialize, Deserialize};
use crate::tensor::MarkovTensor;
use crate::conductance::ConductanceMatrix;
use crate::vlmm::{VariableOrderSelector, FallbackStrategy};
use crate::consolidator::MemoryConsolidator;
use crate::sampler::SamplingStrategy;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineConfig {
    pub max_order: usize,
    pub session_alpha: f64,
    pub session_beta: f64,
    pub long_term_alpha: f64,
    pub long_term_beta: f64,
    pub g_min: f64,
    pub min_observations: usize,
    pub fallback: FallbackStrategy,
    pub consolidation_gamma: f64,
    pub min_session_observations: usize,
    pub default_sampling: SamplingStrategy,
}

impl Default for EngineConfig {
    fn default() -> Self {
        Self {
            max_order: 4,
            session_alpha: 0.1,
            session_beta: 0.01,
            long_term_alpha: 0.01,
            long_term_beta: 0.001,
            g_min: 0.01,
            min_observations: 5,
            fallback: FallbackStrategy::MarginalDistribution,
            consolidation_gamma: 0.1,
            min_session_observations: 20,
            default_sampling: SamplingStrategy::Temperature { t: 1.0 },
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EngineState {
    pub config: EngineConfig,
    pub tensor: MarkovTensor,
    pub session_conductance: ConductanceMatrix,
    pub long_term_conductance: Option<ConductanceMatrix>,
    pub vlmm: VariableOrderSelector,
    pub consolidator: MemoryConsolidator,
    pub context_buffer: Vec<usize>,
    pub total_observations: u64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_serializes_roundtrip() {
        let config = EngineConfig::default();
        let json = serde_json::to_string(&config).unwrap();
        let back: EngineConfig = serde_json::from_str(&json).unwrap();
        assert_eq!(back.max_order, config.max_order);
    }
}
```

- [ ] **Step 4: Run all tests**

```bash
cargo test -p memristive-markov
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add crates/memristive-markov/src/consolidator.rs crates/memristive-markov/src/conductance.rs crates/memristive-markov/src/serde_state.rs
git commit -m "feat: MemoryConsolidator + EngineConfig serialization with TDD"
```

---

## Task 6: MemristiveEngine — The Orchestrator

**Files:**
- Modify: `crates/memristive-markov/src/engine.rs`

- [ ] **Step 1: Write engine with tests**

Replace `engine.rs`:

```rust
use std::collections::VecDeque;
use rand::Rng;
use serde::{Serialize, Deserialize};
use crate::error::Result;
use crate::tensor::MarkovTensor;
use crate::conductance::ConductanceMatrix;
use crate::vlmm::VariableOrderSelector;
use crate::consolidator::MemoryConsolidator;
use crate::sampler::SamplingStrategy;
use crate::serde_state::{EngineConfig, EngineState};

#[derive(Debug, Serialize, Deserialize)]
pub struct EngineDiagnostics {
    pub total_observations: u64,
    pub unique_states: usize,
    pub tensor_sparsity: f64,
    pub order_histogram: Vec<u64>,
    pub avg_conductance: f64,
    pub session_observations: u64,
}

pub struct MemristiveEngine {
    tensor: MarkovTensor,
    session_conductance: ConductanceMatrix,
    long_term_conductance: Option<ConductanceMatrix>,
    vlmm: VariableOrderSelector,
    consolidator: MemoryConsolidator,
    context_buffer: VecDeque<usize>,
    config: EngineConfig,
    total_observations: u64,
    session_observations: u64,
}

impl MemristiveEngine {
    pub fn new(config: EngineConfig) -> Self {
        let tensor = MarkovTensor::new(config.max_order);
        let session_conductance = ConductanceMatrix::new(
            config.session_alpha, config.session_beta, config.g_min,
        );
        let long_term_conductance = Some(ConductanceMatrix::new(
            config.long_term_alpha, config.long_term_beta, config.g_min,
        ));
        let vlmm = VariableOrderSelector::new(
            config.max_order, config.min_observations, config.fallback,
        );
        let consolidator = MemoryConsolidator::new(
            config.consolidation_gamma, config.min_session_observations,
        );

        Self {
            tensor,
            session_conductance,
            long_term_conductance,
            vlmm,
            consolidator,
            context_buffer: VecDeque::with_capacity(config.max_order),
            config,
            total_observations: 0,
            session_observations: 0,
        }
    }

    pub fn from_state(json: &str) -> Result<Self> {
        let state: EngineState = serde_json::from_str(json)?;
        Ok(Self {
            tensor: state.tensor,
            session_conductance: state.session_conductance,
            long_term_conductance: state.long_term_conductance,
            vlmm: state.vlmm,
            consolidator: state.consolidator,
            context_buffer: VecDeque::from(state.context_buffer),
            config: state.config,
            total_observations: state.total_observations,
            session_observations: 0,
        })
    }

    /// Observe a state transition
    pub fn observe(&mut self, state: usize) {
        if !self.context_buffer.is_empty() {
            let context: Vec<usize> = self.context_buffer.iter().copied().collect();
            self.tensor.observe(&context, state);
            self.session_conductance.strengthen(&context, state);
        }

        // Maintain context buffer
        self.context_buffer.push_back(state);
        if self.context_buffer.len() > self.config.max_order {
            self.context_buffer.pop_front();
        }

        self.total_observations += 1;
        self.session_observations += 1;
    }

    /// Observe a full sequence
    pub fn observe_sequence(&mut self, states: &[usize]) {
        for &s in states {
            self.observe(s);
        }
    }

    /// Predict next state distribution (modulated by conductance)
    pub fn predict(&mut self) -> Vec<(usize, f64)> {
        let context: Vec<usize> = self.context_buffer.iter().copied().collect();
        let base = self.vlmm.predict(&self.tensor, &context);

        // Modulate by session conductance
        let modulated = self.session_conductance.modulate(&context, &base);

        // If long-term conductance exists, blend
        if let Some(lt) = &self.long_term_conductance {
            let lt_modulated = lt.modulate(&context, &base);
            // Blend: 70% session, 30% long-term
            let blended: Vec<(usize, f64)> = modulated.iter().map(|&(s, sp)| {
                let lp = lt_modulated.iter().find(|(ls, _)| *ls == s).map(|(_, p)| *p).unwrap_or(0.0);
                (s, 0.7 * sp + 0.3 * lp)
            }).collect();
            let total: f64 = blended.iter().map(|(_, p)| p).sum();
            if total > 0.0 {
                return blended.into_iter().map(|(s, p)| (s, p / total)).collect();
            }
        }

        modulated
    }

    /// Sample next state
    pub fn sample(&mut self, rng: &mut impl Rng) -> Option<usize> {
        let dist = self.predict();
        self.config.default_sampling.sample(&dist, rng)
    }

    /// Consolidate session → long-term
    pub fn consolidate(&mut self) {
        if let Some(lt) = &mut self.long_term_conductance {
            self.consolidator.consolidate(
                &self.session_conductance, lt, self.session_observations as usize,
            );
        }
        self.session_conductance = ConductanceMatrix::new(
            self.config.session_alpha, self.config.session_beta, self.config.g_min,
        );
        self.session_observations = 0;
    }

    /// Discard session without consolidating
    pub fn reset_session(&mut self) {
        self.session_conductance = ConductanceMatrix::new(
            self.config.session_alpha, self.config.session_beta, self.config.g_min,
        );
        self.context_buffer.clear();
        self.session_observations = 0;
    }

    /// Export full state as JSON
    pub fn export_state(&self) -> String {
        let state = EngineState {
            config: self.config.clone(),
            tensor: self.tensor.clone(),
            session_conductance: self.session_conductance.clone(),
            long_term_conductance: self.long_term_conductance.clone(),
            vlmm: self.vlmm.clone(),
            consolidator: self.consolidator.clone(),
            context_buffer: self.context_buffer.iter().copied().collect(),
            total_observations: self.total_observations,
        };
        serde_json::to_string_pretty(&state).unwrap_or_default()
    }

    pub fn diagnostics(&self) -> EngineDiagnostics {
        EngineDiagnostics {
            total_observations: self.total_observations,
            unique_states: self.tensor.state_count(),
            tensor_sparsity: self.tensor.sparsity(),
            order_histogram: self.vlmm.order_histogram().to_vec(),
            avg_conductance: 0.0, // TODO: compute from conductance
            session_observations: self.session_observations,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;

    fn test_rng() -> rand::rngs::StdRng {
        rand::rngs::StdRng::seed_from_u64(42)
    }

    #[test]
    fn test_engine_observe_and_predict() {
        let mut engine = MemristiveEngine::new(EngineConfig::default());
        // Feed a simple repeating pattern: 0 → 1 → 2 → 0 → 1 → 2 ...
        for _ in 0..20 {
            engine.observe(0);
            engine.observe(1);
            engine.observe(2);
        }
        // After seeing ...→2, next should likely be 0
        let dist = engine.predict();
        assert!(!dist.is_empty());
        let p0 = dist.iter().find(|(s, _)| *s == 0).map(|(_, p)| *p).unwrap_or(0.0);
        assert!(p0 > 0.5, "After 2, should predict 0 with high prob: {}", p0);
    }

    #[test]
    fn test_engine_sample_returns_valid_state() {
        let mut engine = MemristiveEngine::new(EngineConfig::default());
        engine.observe_sequence(&[0, 1, 2, 0, 1, 2, 0, 1, 2]);
        let mut rng = test_rng();
        let s = engine.sample(&mut rng);
        assert!(s.is_some());
        assert!(s.unwrap() <= 2);
    }

    #[test]
    fn test_engine_state_roundtrip() {
        let mut engine = MemristiveEngine::new(EngineConfig::default());
        engine.observe_sequence(&[0, 1, 2, 3, 4]);
        let json = engine.export_state();
        let restored = MemristiveEngine::from_state(&json).unwrap();
        assert_eq!(restored.diagnostics().total_observations, 5);
    }

    #[test]
    fn test_consolidation_resets_session() {
        let mut engine = MemristiveEngine::new(EngineConfig {
            min_session_observations: 5,
            ..EngineConfig::default()
        });
        engine.observe_sequence(&[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
        assert_eq!(engine.diagnostics().session_observations, 10);
        engine.consolidate();
        assert_eq!(engine.diagnostics().session_observations, 0);
    }

    #[test]
    fn test_reset_session_discards() {
        let mut engine = MemristiveEngine::new(EngineConfig::default());
        engine.observe_sequence(&[0, 1, 2, 3, 4]);
        engine.reset_session();
        assert_eq!(engine.diagnostics().session_observations, 0);
    }

    #[test]
    fn test_conductance_biases_prediction() {
        let mut engine = MemristiveEngine::new(EngineConfig {
            session_alpha: 0.5,
            min_observations: 1,
            ..EngineConfig::default()
        });
        // Equal base probabilities: after [0], both 1 and 2 are equally likely
        engine.observe(0); engine.observe(1);
        engine.observe(0); engine.observe(2);
        // Now heavily observe [0]→1 to strengthen conductance
        for _ in 0..20 {
            engine.observe(0); engine.observe(1);
        }
        let dist = engine.predict();
        let p1 = dist.iter().find(|(s, _)| *s == 1).map(|(_, p)| *p).unwrap_or(0.0);
        let p2 = dist.iter().find(|(s, _)| *s == 2).map(|(_, p)| *p).unwrap_or(0.0);
        assert!(p1 > p2, "Conductance should bias toward 1: p1={}, p2={}", p1, p2);
    }
}
```

- [ ] **Step 2: Run all tests**

```bash
cargo test -p memristive-markov
```

Expected: all tests pass (7 tensor + 6 conductance + 4 vlmm + 4 sampler + 2 consolidator + 1 serde + 6 engine = ~30 tests).

- [ ] **Step 3: Commit**

```bash
git add crates/memristive-markov/src/engine.rs
git commit -m "feat: MemristiveEngine — full orchestrator with observe/predict/consolidate, TDD"
```

---

## Task 7: Reservoir Network (Feature-Gated)

**Files:**
- Modify: `crates/memristive-markov/src/reservoir.rs`

- [ ] **Step 1: Write reservoir with tests**

Create `crates/memristive-markov/src/reservoir.rs` (only compiled with `--features reservoir`):

```rust
use ndarray::{Array1, Array2};
use rand::Rng;
use rand_distr::Uniform;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReservoirNetwork {
    size: usize,
    weights: Array2<f64>,
    input_weights: Array2<f64>,
    state: Array1<f64>,
    spectral_radius: f64,
    sparsity: f64,
    leak_rate: f64,
    readout: Option<Array2<f64>>,
}

impl ReservoirNetwork {
    pub fn new(size: usize, input_dim: usize, spectral_radius: f64, sparsity: f64, leak_rate: f64, rng: &mut impl Rng) -> Self {
        let dist = Uniform::new(-1.0, 1.0).unwrap();

        // Generate sparse random weight matrix
        let mut weights = Array2::zeros((size, size));
        for w in weights.iter_mut() {
            if rng.random::<f64>() > sparsity {
                *w = rng.sample(dist);
            }
        }

        // Scale to desired spectral radius (approximate via max singular value)
        let max_val = weights.iter().map(|x| x.abs()).fold(0.0_f64, f64::max);
        if max_val > 0.0 {
            weights.mapv_inplace(|x| x * spectral_radius / max_val);
        }

        // Input weights (dense, random)
        let input_weights = Array2::from_shape_fn((input_dim, size), |_| rng.sample(dist) * 0.1);

        Self {
            size,
            weights,
            input_weights,
            state: Array1::zeros(size),
            spectral_radius,
            sparsity,
            leak_rate,
            readout: None,
        }
    }

    /// Update reservoir state with new input
    pub fn step(&mut self, input: &Array1<f64>) -> &Array1<f64> {
        let pre_activation = input.dot(&self.input_weights) + self.state.dot(&self.weights);
        self.state = (1.0 - self.leak_rate) * &self.state
            + self.leak_rate * pre_activation.mapv(f64::tanh);
        &self.state
    }

    /// Get current state
    pub fn state(&self) -> &Array1<f64> {
        &self.state
    }

    /// Reset state to zeros
    pub fn reset(&mut self) {
        self.state.fill(0.0);
    }

    pub fn size(&self) -> usize {
        self.size
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;

    #[test]
    fn test_reservoir_creation() {
        let mut rng = rand::rngs::StdRng::seed_from_u64(42);
        let r = ReservoirNetwork::new(64, 4, 0.9, 0.9, 0.3, &mut rng);
        assert_eq!(r.size(), 64);
        assert_eq!(r.state().len(), 64);
    }

    #[test]
    fn test_reservoir_step_changes_state() {
        let mut rng = rand::rngs::StdRng::seed_from_u64(42);
        let mut r = ReservoirNetwork::new(32, 4, 0.9, 0.9, 0.3, &mut rng);
        let input = Array1::from_vec(vec![1.0, 0.0, 0.5, -0.5]);
        let initial_norm: f64 = r.state().iter().map(|x| x * x).sum();
        r.step(&input);
        let after_norm: f64 = r.state().iter().map(|x| x * x).sum();
        assert!(after_norm > initial_norm, "State should change after step");
    }

    #[test]
    fn test_reservoir_state_bounded() {
        let mut rng = rand::rngs::StdRng::seed_from_u64(42);
        let mut r = ReservoirNetwork::new(32, 4, 0.9, 0.9, 0.3, &mut rng);
        let input = Array1::from_vec(vec![100.0, -100.0, 50.0, -50.0]);
        for _ in 0..100 {
            r.step(&input);
        }
        // tanh keeps values in (-1, 1), so state should be bounded
        for &v in r.state().iter() {
            assert!(v.abs() <= 1.0, "Reservoir state should be bounded: {}", v);
        }
    }

    #[test]
    fn test_reservoir_reset() {
        let mut rng = rand::rngs::StdRng::seed_from_u64(42);
        let mut r = ReservoirNetwork::new(32, 4, 0.9, 0.9, 0.3, &mut rng);
        r.step(&Array1::ones(4));
        r.reset();
        assert!(r.state().iter().all(|&v| v == 0.0));
    }
}
```

- [ ] **Step 2: Add rand_distr dependency**

Add to `crates/memristive-markov/Cargo.toml` under `[dependencies]`:

```toml
rand_distr = { workspace = true }
ndarray-rand = { workspace = true }
```

- [ ] **Step 3: Run tests with reservoir feature**

```bash
cargo test -p memristive-markov --features reservoir
```

Expected: all tests pass including 4 reservoir tests.

- [ ] **Step 4: Commit**

```bash
git add crates/memristive-markov/
git commit -m "feat: ReservoirNetwork — echo state network for temporal patterns, feature-gated"
```

---

## Task 8: Benchmarks + Full Test Suite

**Files:**
- Modify: `crates/memristive-markov/benches/engine_bench.rs`

- [ ] **Step 1: Write benchmarks**

Replace `benches/engine_bench.rs`:

```rust
use criterion::{criterion_group, criterion_main, Criterion, black_box};
use memristive_markov::{MemristiveEngine, SamplingStrategy};
use memristive_markov::serde_state::EngineConfig;
use rand::SeedableRng;

fn bench_observe(c: &mut Criterion) {
    let mut engine = MemristiveEngine::new(EngineConfig::default());
    let mut state = 0usize;
    c.bench_function("observe_1000_states", |b| {
        b.iter(|| {
            for _ in 0..1000 {
                engine.observe(black_box(state % 64));
                state += 1;
            }
        })
    });
}

fn bench_predict(c: &mut Criterion) {
    let mut engine = MemristiveEngine::new(EngineConfig {
        min_observations: 1,
        ..EngineConfig::default()
    });
    for i in 0..1000 {
        engine.observe(i % 32);
    }
    c.bench_function("predict", |b| {
        b.iter(|| {
            let _ = black_box(engine.predict());
        })
    });
}

fn bench_sample(c: &mut Criterion) {
    let mut engine = MemristiveEngine::new(EngineConfig {
        min_observations: 1,
        ..EngineConfig::default()
    });
    for i in 0..1000 {
        engine.observe(i % 32);
    }
    let mut rng = rand::rngs::StdRng::seed_from_u64(42);
    c.bench_function("sample", |b| {
        b.iter(|| {
            let _ = black_box(engine.sample(&mut rng));
        })
    });
}

fn bench_state_roundtrip(c: &mut Criterion) {
    let mut engine = MemristiveEngine::new(EngineConfig::default());
    for i in 0..500 {
        engine.observe(i % 16);
    }
    let json = engine.export_state();
    c.bench_function("state_roundtrip", |b| {
        b.iter(|| {
            let _ = black_box(MemristiveEngine::from_state(&json));
        })
    });
}

criterion_group!(benches, bench_observe, bench_predict, bench_sample, bench_state_roundtrip);
criterion_main!(benches);
```

- [ ] **Step 2: Run full test suite**

```bash
cargo test -p memristive-markov --features reservoir
```

Expected: ~34 tests pass.

- [ ] **Step 3: Run benchmarks**

```bash
cargo bench -p memristive-markov
```

Expected: benchmarks run and report timing.

- [ ] **Step 4: Commit**

```bash
git add crates/memristive-markov/benches/
git commit -m "feat: Criterion benchmarks for observe, predict, sample, state roundtrip"
```

---

## Task 9: Property-Based Tests

**Files:**
- Create: `crates/memristive-markov/tests/proptest_tensor.rs`

- [ ] **Step 1: Write property tests**

```rust
use proptest::prelude::*;
use memristive_markov::tensor::MarkovTensor;
use memristive_markov::conductance::ConductanceMatrix;

proptest! {
    #[test]
    fn tensor_probabilities_sum_to_one(
        transitions in prop::collection::vec((0..20usize, 0..20usize, 0..20usize), 10..100)
    ) {
        let mut t = MarkovTensor::new(2);
        for (a, b, next) in &transitions {
            t.observe(&[*a, *b], *next);
        }
        // Check all contexts produce valid distributions
        for (a, b, _) in &transitions {
            let dist = t.predict(&[*a, *b]);
            if !dist.is_empty() {
                let total: f64 = dist.iter().map(|(_, p)| p).sum();
                prop_assert!((total - 1.0).abs() < 1e-9, "Sum was {}", total);
                for (_, p) in &dist {
                    prop_assert!(*p >= 0.0 && *p <= 1.0, "Invalid prob {}", p);
                }
            }
        }
    }

    #[test]
    fn conductance_stays_bounded(
        observations in prop::collection::vec(0..10usize, 1..50),
        alpha in 0.01..1.0_f64,
        beta in 0.001..0.5_f64,
    ) {
        let mut cm = ConductanceMatrix::new(alpha, beta, 0.01);
        for &s in &observations {
            cm.strengthen(&[0], s);
        }
        cm.decay_all();
        cm.for_each(|_, _, g| {
            prop_assert!(g >= 0.01, "Below g_min: {}", g);
            prop_assert!(g <= 1.0, "Above 1.0: {}", g);
            Ok(())
        }.unwrap_or(()));
    }
}
```

- [ ] **Step 2: Run property tests**

```bash
cargo test -p memristive-markov --test proptest_tensor
```

Expected: property tests pass (runs many random cases).

- [ ] **Step 3: Commit**

```bash
git add crates/memristive-markov/tests/
git commit -m "test: Property-based tests — tensor normalization + conductance bounds"
```

---

## Task 10: Final Verification + Push

- [ ] **Step 1: Run full test suite with all features**

```bash
cargo test -p memristive-markov --features full
```

Expected: all tests pass.

- [ ] **Step 2: Run clippy**

```bash
cargo clippy -p memristive-markov --features full -- -D warnings
```

Expected: no warnings.

- [ ] **Step 3: Verify file count**

```bash
find crates/memristive-markov/src -name "*.rs" | wc -l
```

Expected: 12 source files (lib, error, tensor, conductance, vlmm, sampler, consolidator, engine, serde_state, reservoir, ffi stub, gpu stub).

- [ ] **Step 4: Push**

```bash
git push origin main
```
