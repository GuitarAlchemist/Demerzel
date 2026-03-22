# ix micro/ — Karpathy Micro Implementations — Design Specification

**Date:** 2026-03-23
**Status:** Draft
**Issue:** GuitarAlchemist/Demerzel#121
**Scope:** ix repo — new `crates/micro/` directory + `crates/kernels/` WGPU directory
**Inspired by:** Andrej Karpathy's micrograd, nanoGPT, and minBPE projects

---

## Overview

The `micro/` directory is a curated set of minimal, readable ML implementations in Rust — each
fitting in a single file with a tight line-count budget. The goal is educational clarity combined
with governance integration: every implementation is an `@ai probe`-annotated reference for
Demerzel governance verification.

Unlike ix's production ML crates (ix-nn, ix-supervised, ix-pipeline), `micro/` implementations:
- Have **zero external ML dependencies** (only `std` + optional `rand`)
- Are **single-file** — the entire implementation in one `.rs` file
- Have **explicit line budgets** per implementation
- Are **governance-annotated** — `@ai probe` on every major component
- Serve as **ground truth** for testing ix's heavier ML crates

---

## Design Principles

| Principle | Application |
|---|---|
| Article 1 (Truthfulness) | Comments must accurately describe what the code does — no aspirational documentation |
| Article 7 (Auditability) | Every impl has `@ai probe` annotations making its semantics verifiable |
| Article 4 (Proportionality) | Line budgets enforced — implementations that grow beyond budget are refactored, not extended |
| Article 8 (Observability) | Each impl exposes a `health_check()` fn returning a governance-readable status |

---

## Section 1: micro/ Directory Layout

```
crates/micro/
  src/
    lib.rs              # Re-exports all micro implementations
    micrograd.rs        # Autograd engine (~100 lines)
    nanogpt.rs          # Transformer language model (~300 lines)
    minbpe.rs           # Byte-pair encoding tokenizer (~100 lines)
    health.rs           # governance health_check() for all three
  tests/
    micrograd_tests.rs  # Unit tests — gradient correctness
    nanogpt_tests.rs    # Unit tests — forward pass shape, causal mask
    minbpe_tests.rs     # Unit tests — encode/decode roundtrip
  examples/
    micrograd_xor.rs    # XOR problem solved with micrograd
    nanogpt_tiny.rs     # Character-level language model on tiny corpus
    minbpe_wiki.rs      # BPE tokenization of a sample text
  Cargo.toml
  README.md
```

---

## Section 2: micrograd.rs (~100 lines)

### 2.1 Purpose

A scalar-valued autograd engine. Implements a computation graph where each `Value` node stores
its data, gradient, and the backward closure that propagates gradients to its inputs.

This is the minimal foundation for understanding backpropagation — the same idea that powers
all deep learning frameworks, in ~100 lines.

### 2.2 API

```rust
// @ai probe: "Scalar value node in the computation graph — stores data, grad, and backward closure"
pub struct Value {
    pub data: f64,
    pub grad: f64,
    // internal: children, op, backward closure
}

impl Value {
    pub fn new(data: f64) -> Rc<RefCell<Value>>;

    // Arithmetic — each returns a new Value node recording the operation
    pub fn add(a: &Rc<RefCell<Value>>, b: &Rc<RefCell<Value>>) -> Rc<RefCell<Value>>;
    pub fn mul(a: &Rc<RefCell<Value>>, b: &Rc<RefCell<Value>>) -> Rc<RefCell<Value>>;
    pub fn pow(base: &Rc<RefCell<Value>>, exp: f64) -> Rc<RefCell<Value>>;
    pub fn relu(x: &Rc<RefCell<Value>>) -> Rc<RefCell<Value>>;
    pub fn tanh(x: &Rc<RefCell<Value>>) -> Rc<RefCell<Value>>;

    // Backpropagation — topological sort + chain rule application
    // @ai invariant: after backward(), every node's .grad == ∂output/∂node
    pub fn backward(root: &Rc<RefCell<Value>>);
}

// @ai probe: "Multi-layer perceptron built from Value nodes — forward pass only"
pub struct MLP {
    layers: Vec<Layer>,
}

impl MLP {
    pub fn new(input_size: usize, layer_sizes: &[usize]) -> MLP;
    pub fn forward(&self, inputs: &[f64]) -> Vec<Rc<RefCell<Value>>>;
    pub fn parameters(&self) -> Vec<Rc<RefCell<Value>>>;
    pub fn zero_grad(&self);
}
```

### 2.3 Implementation Notes

**Computation graph construction:**
Each arithmetic operation creates a new `Value` that stores closures over its input `Value`s.
The backward pass does a topological sort of the graph, then calls each node's backward closure
in reverse order (chain rule).

**Why `Rc<RefCell<Value>>`:**
Multiple nodes can share the same input (e.g., `x * x`). `Rc` enables shared ownership;
`RefCell` enables interior mutability for gradient accumulation during backward.

**Line budget breakdown (target: 100 lines):**
- `Value` struct + `new` + arithmetic ops: ~50 lines
- `backward` (topological sort): ~15 lines
- `Neuron` + `Layer`: ~15 lines
- `MLP`: ~20 lines

### 2.4 Tests

```rust
// micrograd_tests.rs

#[test]
fn test_gradient_add() {
    // d(a + b)/da == 1.0
}

#[test]
fn test_gradient_mul() {
    // d(a * b)/da == b
}

#[test]
fn test_gradient_chain_rule() {
    // d(relu(a * b + c))/da == b (when a*b+c > 0)
}

#[test]
fn test_mlp_forward_shape() {
    // MLP(2, [4, 1]) forward pass returns 1 output Value
}

#[test]
fn test_mlp_backward_no_nan() {
    // After one backward pass, no gradient is NaN or inf
}

#[test]
fn test_xor_convergence() {
    // MLP(2, [4, 1]) trained for 100 steps on XOR achieves loss < 0.1
}
```

---

## Section 3: nanogpt.rs (~300 lines)

### 3.1 Purpose

A minimal transformer language model — GPT-style decoder-only architecture. Supports forward pass,
causal self-attention, and autoregressive generation. Uses `ndarray` (or pure Vec<Vec<f64>>) for
tensors, with no deep learning framework dependencies.

This is the minimal implementation needed to understand transformer internals — attention heads,
positional encoding, residual connections, layer norm.

### 3.2 Configuration

```rust
// @ai probe: "Transformer hyperparameters — all architecture decisions in one struct"
pub struct GPTConfig {
    pub vocab_size: usize,       // Number of tokens in vocabulary
    pub block_size: usize,       // Maximum sequence length (context window)
    pub n_embd: usize,           // Embedding dimension
    pub n_head: usize,           // Number of attention heads (n_embd must be divisible by n_head)
    pub n_layer: usize,          // Number of transformer blocks
    pub dropout: f64,            // Dropout rate (0.0 = disabled for inference)
}

impl GPTConfig {
    // @ai probe: "Nano configuration — fits on a CPU, trains in seconds"
    pub fn nano() -> GPTConfig {
        GPTConfig { vocab_size: 65, block_size: 64, n_embd: 64, n_head: 4, n_layer: 2, dropout: 0.0 }
    }
    // @ai probe: "Small configuration — character-level models, fast iteration"
    pub fn small() -> GPTConfig {
        GPTConfig { vocab_size: 256, block_size: 128, n_embd: 128, n_head: 4, n_layer: 4, dropout: 0.1 }
    }
}
```

### 3.3 Architecture

```rust
// @ai probe: "Causal self-attention — attends only to past tokens (lower triangular mask)"
pub struct CausalSelfAttention {
    n_head: usize,
    n_embd: usize,
    // Weight matrices: Q, K, V projections + output projection
    c_attn: Linear,   // [n_embd, 3 * n_embd] — fused Q, K, V
    c_proj: Linear,   // [n_embd, n_embd]
}

// @ai probe: "Transformer block — attention + MLP with residual connections and layer norm"
pub struct Block {
    ln_1: LayerNorm,
    attn: CausalSelfAttention,
    ln_2: LayerNorm,
    mlp: MLP,         // 4x expansion: n_embd -> 4*n_embd -> n_embd with GELU
}

// @ai probe: "GPT model — token embedding + position embedding + N transformer blocks + LM head"
pub struct GPT {
    config: GPTConfig,
    wte: Embedding,   // Token embeddings [vocab_size, n_embd]
    wpe: Embedding,   // Position embeddings [block_size, n_embd]
    blocks: Vec<Block>,
    ln_f: LayerNorm,
    lm_head: Linear,  // [n_embd, vocab_size] — tied to wte weights
}

impl GPT {
    pub fn new(config: GPTConfig) -> GPT;

    // @ai invariant: output shape == [batch_size, seq_len, vocab_size]
    pub fn forward(&self, idx: &[Vec<usize>]) -> Vec<Vec<Vec<f64>>>;

    // Autoregressive generation — appends tokens one at a time
    // @ai probe: "Greedy or temperature-sampled generation — no beam search"
    pub fn generate(&self, context: &[usize], max_new_tokens: usize, temperature: f64) -> Vec<usize>;
}
```

### 3.4 Key Implementation Details

**Scaled dot-product attention:**
```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```
The causal mask zeros out the upper triangle of `QK^T / sqrt(d_k)` (set to -inf before softmax),
ensuring each position only attends to itself and prior positions.

**Multi-head splitting:**
`Q`, `K`, `V` are computed from the same projection, then split into `n_head` heads each of
dimension `n_embd / n_head`. Heads are computed in parallel, then concatenated.

**Residual connections:**
Every sub-layer output is added to its input: `x = x + sublayer(layer_norm(x))`.
Pre-norm (layer norm before the sub-layer) matches modern GPT implementations.

**Line budget breakdown (target: 300 lines):**
- Config + embedding structs: ~30 lines
- Linear + LayerNorm helpers: ~30 lines
- CausalSelfAttention: ~60 lines
- Block: ~40 lines
- GPT struct + forward: ~80 lines
- GPT generate: ~30 lines
- Softmax, GELU helpers: ~30 lines

### 3.5 Tests

```rust
#[test]
fn test_forward_output_shape() {
    // GPT::nano() forward on batch of 2, seq_len 8 → shape [2, 8, 65]
}

#[test]
fn test_causal_mask_respected() {
    // Attention at position i has zero weight on positions j > i
}

#[test]
fn test_generate_length() {
    // generate(context, max_new_tokens=10) returns exactly 10 new tokens
}

#[test]
fn test_generate_within_vocab() {
    // All generated token IDs are in [0, vocab_size)
}

#[test]
fn test_residual_gradient_flow() {
    // In a 2-layer GPT, gradients reach layer 0 from the output
    // (verifies residual connections, not dead by vanishing gradients)
}
```

---

## Section 4: minbpe.rs (~100 lines)

### 4.1 Purpose

A minimal byte-pair encoding (BPE) tokenizer. Takes a text corpus, learns a vocabulary of
`n_vocab` merge rules by iteratively merging the most frequent byte pair, and encodes/decodes
text using the learned vocabulary.

BPE is the tokenization algorithm behind GPT-2/3/4, LLaMA, and most modern LLMs.

### 4.2 API

```rust
// @ai probe: "BPE tokenizer — learns merge rules from a corpus, encodes/decodes text"
pub struct BPETokenizer {
    vocab: HashMap<Vec<u8>, usize>,       // token bytes → token ID
    merges: Vec<(Vec<u8>, Vec<u8>)>,      // merge rules in application order
    id_to_token: Vec<Vec<u8>>,            // token ID → token bytes
}

impl BPETokenizer {
    // Initialize with single-byte vocabulary (256 tokens for all byte values)
    pub fn new() -> BPETokenizer;

    // Train: learn n_merges merge rules from the corpus
    // @ai invariant: after train(corpus, n_merges), vocab.len() == 256 + n_merges
    pub fn train(&mut self, corpus: &str, n_merges: usize);

    // Encode text to token IDs
    // @ai invariant: decode(encode(text)) == text for any text
    pub fn encode(&self, text: &str) -> Vec<usize>;

    // Decode token IDs to text
    pub fn decode(&self, ids: &[usize]) -> Result<String, std::string::FromUtf8Error>;

    // Vocabulary size
    pub fn vocab_size(&self) -> usize;
}
```

### 4.3 Algorithm

**Training:**
1. Start with all 256 single-byte tokens
2. Find the most frequent consecutive pair in the corpus encoding
3. Add the merged pair as a new token; add to merge rules list
4. Reapply: encode the corpus with the new vocabulary, repeat

**Encoding:**
1. Start with byte-level encoding of the text
2. Apply merge rules in training order: whenever the next two tokens match a merge rule, merge them
3. Return final token ID sequence

**Decoding:**
1. Map each token ID to its byte sequence using `id_to_token`
2. Concatenate all byte sequences
3. Decode UTF-8 (may fail if the encoding is mid-character)

**Line budget breakdown (target: 100 lines):**
- `BPETokenizer` struct + `new`: ~10 lines
- `train` (find pairs + apply merge): ~40 lines
- `encode`: ~25 lines
- `decode`: ~10 lines
- Helper: `get_stats` (count pairs), `merge_ids`: ~15 lines

### 4.4 Tests

```rust
#[test]
fn test_encode_decode_roundtrip() {
    // decode(encode(text)) == text for ASCII text
}

#[test]
fn test_vocab_size_after_training() {
    // After train(corpus, 100), vocab_size() == 356
}

#[test]
fn test_frequent_pair_merged_first() {
    // In corpus "aaabdaaabac", 'aa' should be the first merge
}

#[test]
fn test_encode_empty_string() {
    // encode("") == []
}

#[test]
fn test_encode_single_byte() {
    // encode("a") == [97]  (byte value of 'a')
}
```

---

## Section 5: kernels/ Directory (WGPU)

### 5.1 Purpose

GPU compute kernels written in WGSL (WebGPU Shading Language) for accelerating the micro
implementations and ix's production ML crates. Uses `wgpu` (cross-platform GPU abstraction).

The kernels are intentionally minimal — each kernel does one thing and does it clearly.

### 5.2 Directory Layout

```
crates/kernels/
  src/
    lib.rs              # WgpuContext + kernel dispatch
    context.rs          # GPU device/queue initialization
    matmul.rs           # Matrix multiplication kernel dispatch
    softmax.rs          # Row-wise softmax kernel dispatch
    gelu.rs             # GELU activation kernel dispatch
    layer_norm.rs       # Layer normalization kernel dispatch
    embedding.rs        # Embedding lookup kernel dispatch
  shaders/
    matmul.wgsl         # Tiled matrix multiplication
    softmax.wgsl        # Row-wise softmax (numerically stable)
    gelu.wgsl           # GELU approximation (tanh variant)
    layer_norm.wgsl     # Layer norm (mean + variance per row)
    embedding.wgsl      # Embedding gather
  tests/
    matmul_tests.rs     # Compare GPU vs CPU matmul output
    softmax_tests.rs    # Numerical correctness + stability
    gelu_tests.rs       # Compare against precise GELU
  Cargo.toml
  README.md
```

### 5.3 WgpuContext

```rust
// @ai probe: "GPU context — device + queue + shader compilation cache"
pub struct WgpuContext {
    device: wgpu::Device,
    queue: wgpu::Queue,
    shader_cache: HashMap<&'static str, wgpu::ShaderModule>,
}

impl WgpuContext {
    // @ai invariant: new() succeeds on any platform with a Vulkan/Metal/DX12/WebGPU adapter
    pub async fn new() -> Result<WgpuContext, WgpuError>;

    // Graceful fallback: returns None if no GPU available (use CPU path instead)
    pub async fn try_new() -> Option<WgpuContext>;
}
```

### 5.4 matmul.wgsl — Tiled Matrix Multiplication

```wgsl
// @ai probe: "Tiled matmul kernel — workgroup tiles reduce global memory access"
// @ai invariant: C[i][j] = sum_k(A[i][k] * B[k][j]) for all valid i, j

struct MatMulDims {
    M: u32,   // rows of A (and C)
    K: u32,   // cols of A (rows of B)
    N: u32,   // cols of B (and C)
}

@group(0) @binding(0) var<uniform> dims: MatMulDims;
@group(0) @binding(1) var<storage, read> A: array<f32>;
@group(0) @binding(2) var<storage, read> B: array<f32>;
@group(0) @binding(3) var<storage, read_write> C: array<f32>;

const TILE_SIZE: u32 = 16u;

var<workgroup> tileA: array<array<f32, TILE_SIZE>, TILE_SIZE>;
var<workgroup> tileB: array<array<f32, TILE_SIZE>, TILE_SIZE>;

@compute @workgroup_size(TILE_SIZE, TILE_SIZE)
fn main(@builtin(global_invocation_id) gid: vec3<u32>,
        @builtin(local_invocation_id) lid: vec3<u32>,
        @builtin(workgroup_id) wid: vec3<u32>) {
    // Load tiles, compute partial sums, accumulate
}
```

**Design decisions:**
- Tile size of 16×16 balances register pressure and memory bandwidth on most GPUs
- Shared memory (`var<workgroup>`) reduces global memory accesses by TILE_SIZE×
- Handles non-tile-aligned dimensions with boundary checks

### 5.5 softmax.wgsl — Numerically Stable Row Softmax

```wgsl
// @ai probe: "Numerically stable softmax — three-pass: max, sum, normalize"
// @ai invariant: output[i][j] >= 0 and sum(output[i]) == 1.0 for all rows i

// Three-pass algorithm:
// Pass 1: Find row maximum (avoids overflow in exp())
// Pass 2: Compute sum(exp(x - max)) per row
// Pass 3: Divide each element by the sum
```

### 5.6 Cargo.toml Dependencies

```toml
[dependencies]
wgpu = { version = "0.19", optional = true }
pollster = { version = "0.3", optional = true }  # Block on async GPU init in tests

[features]
default = []
gpu = ["wgpu", "pollster"]

# micro/ uses kernels with:
[dependencies]
ix-kernels = { path = "../kernels", optional = true, features = ["gpu"] }
```

GPU acceleration is opt-in — `micro/` implementations work without a GPU. When `gpu` feature
is enabled, `nanogpt.rs` dispatches matmul and attention operations to kernels.

---

## Section 6: Governance Annotations

### 6.1 @ai Probe Coverage Requirements

Per `policies/ai-probes-policy.yaml`, exported symbols need 30% minimum probe coverage.
The `micro/` crate targets 80% coverage — every public function and struct gets a probe.

Required probe types per implementation:

| Symbol | Probe Type | Example |
|---|---|---|
| `Value` struct | `@ai probe:` | "Scalar value node in computation graph" |
| `backward()` | `@ai invariant:` | "after backward(), .grad == ∂output/∂node" |
| `GPT::forward()` | `@ai invariant:` | "output shape == [batch, seq_len, vocab_size]" |
| `BPETokenizer::train()` | `@ai invariant:` | "vocab.len() == 256 + n_merges after training" |
| WGSL kernels | `@ai probe:` | "numerically stable softmax — three-pass" |

### 6.2 health.rs

```rust
// @ai probe: "Governance health check for all micro implementations"
pub struct MicroHealth {
    pub micrograd_ok: bool,
    pub nanogpt_ok: bool,
    pub minbpe_ok: bool,
    pub gpu_available: bool,
    pub probe_coverage: f64,   // fraction of exported symbols with @ai probes
}

pub fn health_check() -> MicroHealth {
    // Run a minimal smoke test for each implementation
    // Check @ai probe coverage via compile-time macro counting
    // Return structured health report
}
```

---

## Section 7: Implementation Order

### Phase 1 — micrograd.rs (Sprint 2)

1. Implement `Value` struct with `Rc<RefCell<>>` interior mutability
2. Implement `add`, `mul`, `pow`, `relu`, `tanh` with backward closures
3. Implement `backward()` with topological sort
4. Implement `Neuron`, `Layer`, `MLP`
5. Add `@ai probe` and `@ai invariant` annotations throughout
6. Write all 6 tests
7. Write `micrograd_xor.rs` example

**Why first:** Smallest scope. Validates the `crates/micro/` structure and Cargo workspace integration.

### Phase 2 — minbpe.rs (Sprint 2)

1. Implement `BPETokenizer::new()` with 256-token byte vocabulary
2. Implement `get_stats` (pair counting) and `merge_ids` (apply one merge)
3. Implement `train` iterating over `n_merges` rounds
4. Implement `encode` and `decode`
5. Add `@ai invariant` on encode/decode roundtrip
6. Write all 5 tests

**Why second:** Standalone (no tensor ops). Validates the tokenization path needed for nanogpt.

### Phase 3 — nanogpt.rs (Sprint 3)

1. Implement `GPTConfig` with `nano()` and `small()` presets
2. Implement `Linear`, `LayerNorm`, `Embedding` helpers
3. Implement `CausalSelfAttention` with tiled softmax
4. Implement `Block` with pre-norm residual connections
5. Implement `GPT::forward()` and `GPT::generate()`
6. Add all `@ai probe` annotations
7. Write all 5 tests
8. Write `nanogpt_tiny.rs` example (character-level LM)

**Why third:** Depends on BPE tokenizer. Largest scope — warrants its own sprint slot.

### Phase 4 — kernels/ WGPU (Sprint 4)

1. Set up `crates/kernels/` with `WgpuContext`
2. Implement `matmul.wgsl` with 16×16 tiling
3. Implement `softmax.wgsl` (three-pass numerically stable)
4. Implement `gelu.wgsl` and `layer_norm.wgsl`
5. Wire `nanogpt.rs` to use kernels when `features = ["gpu"]`
6. Add CPU vs. GPU comparison tests

---

## Appendix A: Line Budget Summary

| File | Target Lines | Tolerance | Notes |
|---|---|---|---|
| `micrograd.rs` | 100 | ±20 | Rust verbosity (Rc/RefCell) may push toward 120 |
| `nanogpt.rs` | 300 | ±50 | Attention mechanism requires clarity over brevity |
| `minbpe.rs` | 100 | ±15 | Straightforward — target is firm |
| `matmul.wgsl` | 60 | ±10 | WGSL is verbose; tiling adds boilerplate |
| `softmax.wgsl` | 30 | ±5 | Three passes, clearly separated |

## Appendix B: Key References

| Reference | Relevance |
|---|---|
| Karpathy/micrograd (Python) | Original autograd inspiration |
| Karpathy/nanoGPT (Python) | Original transformer inspiration |
| Karpathy/minbpe (Python) | Original BPE inspiration |
| `crates/ix-nn/` | Production neural net crate that micro/ validates |
| `crates/ix-supervised/` | Production training crate — micro/ is its ground truth |
| `policies/ai-probes-policy.yaml` | @ai probe coverage requirements |
| `docs/specs/ix-governance-integration-map.md` | How ix ML integrates with Demerzel governance |
| `grammars/sci-ml-pipelines.ebnf` | IxQL grammar covering ML pipeline constructs |
