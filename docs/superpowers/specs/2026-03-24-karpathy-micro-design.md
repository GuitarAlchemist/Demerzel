# Karpathy Micro Implementations — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Issue:** GuitarAlchemist/Demerzel#121
**Scope:** ix repo (new `ix-micro` crate family), Demerzel (behavioral specifications)
**Inspiration:** Andrej Karpathy — micrograd, minGPT, nanoGPT, llm.c

---

## Overview

A family of minimal, pedagogically-clear Rust implementations of foundational ML primitives, built in the spirit of Karpathy's micro-implementations: every operation is visible, every gradient is explicit, every abstraction earns its place.

**Philosophy:** "The best way to understand a thing is to build it from scratch." — Karpathy

These are not production ML libraries. They are governance artifacts: behavioral specifications expressed as working Rust code. They serve as:

1. **Reference implementations** — ground truth for what IxQL stages do
2. **Teaching materials** — used in Streeling University computer-science department
3. **Test fixtures** — small, inspectable models for ix integration tests
4. **Grammar validators** — each ix_pattern production in the EBNF maps to one micro crate

---

## Design Principles

| Principle | Application |
|---|---|
| Minimal dependencies | No ML framework dependencies (no tch, no candle, no ort). Pure Rust + ndarray. |
| All gradients explicit | No autograd magic. Gradient computations are written out and documented. |
| Readable over fast | No SIMD intrinsics, no unsafe blocks, no loop unrolling in the core path. |
| Governed by design | Every crate includes a `governance.rs` module exposing IxQL governance gates. |
| Tested to spec | Each crate has property-based tests (proptest) plus reference output tests. |
| No black boxes | Every hyperparameter is exposed; every intermediate state is inspectable. |

---

## Section 1: Crate Family

```
ix/crates/
  ix-micro-autograd/       -- Scalar-valued reverse-mode autograd (micrograd port)
  ix-micro-nn/             -- Neural network layers built on ix-micro-autograd
  ix-micro-transformer/    -- Decoder-only transformer (nanoGPT-style)
  ix-micro-tokenizer/      -- BPE tokenizer (no external tokenizer libraries)
  ix-micro-optim/          -- SGD, Adam, AdamW — all gradients explicit
  ix-micro-governance/     -- Governance gates for micro model training pipelines
```

Each crate is:
- Independent (no crate depends on a sibling unless specified)
- `no_std`-compatible (except `ix-micro-transformer`)
- Fully documented with examples
- Tested against known-good numerical reference outputs

---

## Section 2: ix-micro-autograd

### Overview

Scalar-value reverse-mode automatic differentiation. Direct Rust port of Karpathy's `micrograd` (Python, 2023). Operates on a dynamically-built computation graph of `Value` nodes.

### Core types

```rust
/// A scalar value in a computation graph.
/// Carries: value, gradient, and a backward closure.
pub struct Value {
    pub data: f64,
    pub grad: f64,
    pub(crate) _backward: Box<dyn Fn()>,
    pub(crate) _prev: Vec<Rc<RefCell<Value>>>,
    pub(crate) _op: &'static str,
}

impl Value {
    pub fn new(data: f64) -> Rc<RefCell<Self>>;
    pub fn backward(&self);          // trigger reverse-mode gradient accumulation

    // Arithmetic — all build the computation graph
    pub fn add(a: &Rc<RefCell<Self>>, b: &Rc<RefCell<Self>>) -> Rc<RefCell<Self>>;
    pub fn mul(a: &Rc<RefCell<Self>>, b: &Rc<RefCell<Self>>) -> Rc<RefCell<Self>>;
    pub fn pow(base: &Rc<RefCell<Self>>, exp: f64) -> Rc<RefCell<Self>>;
    pub fn relu(x: &Rc<RefCell<Self>>) -> Rc<RefCell<Self>>;
    pub fn tanh(x: &Rc<RefCell<Self>>) -> Rc<RefCell<Self>>;
    pub fn exp(x: &Rc<RefCell<Self>>) -> Rc<RefCell<Self>>;
}
```

### Governance hook

```rust
pub mod governance {
    /// Assert gradient norms are finite and below threshold.
    /// Tetravalent: T (finite, < threshold) | F (NaN or Inf) | U (empty graph) | C (threshold conflicte)
    pub fn assert_gradient_health(graph: &Value, threshold: f64) -> TruthValue;
}
```

### Reference tests

Each operation tested against known-good Python micrograd output (stored as JSON fixtures):

```
tests/
  fixtures/
    autograd-add.json       { "a": 2.0, "b": -3.0, "result": -1.0, "grad_a": 1.0, "grad_b": 1.0 }
    autograd-tanh.json
    autograd-backprop.json  { "inputs": [...], "expected_grads": [...] }
```

---

## Section 3: ix-micro-nn

### Overview

Neural network layers built on `ix-micro-autograd`. Corresponds to the `neural_model` productions in the IxQL EBNF (mlp, lstm, rnn). Pure Rust, weights stored as `Vec<Rc<RefCell<Value>>>`.

### Layers

```rust
/// A single neuron: dot(weights, inputs) + bias, then activation
pub struct Neuron {
    weights: Vec<Rc<RefCell<Value>>>,
    bias: Rc<RefCell<Value>>,
    activation: Activation,
}

/// A fully-connected layer of N neurons
pub struct Layer {
    neurons: Vec<Neuron>,
}

/// A multi-layer perceptron
pub struct MLP {
    layers: Vec<Layer>,
}

impl MLP {
    pub fn new(nin: usize, nouts: Vec<usize>) -> Self;
    pub fn forward(&self, inputs: &[f64]) -> Vec<Rc<RefCell<Value>>>;
    pub fn parameters(&self) -> Vec<Rc<RefCell<Value>>>;
    pub fn zero_grad(&self);
}
```

### Activations

```rust
pub enum Activation {
    ReLU,
    Tanh,
    Sigmoid,
    Linear,    // no activation — for output layers
}
```

### Training loop (explicit, no magic)

```rust
// The training loop is a first-class concept, not hidden in a Trainer struct.
// Every step is a method call the user can see and modify.
for step in 0..steps {
    let ypred: Vec<_> = xs.iter().map(|x| model.forward(x)).collect();
    let loss = mse_loss(&ypred, &ys);

    model.zero_grad();          // reset all gradients
    loss.borrow().backward();   // compute all gradients via reverse mode

    for p in model.parameters() {
        let grad = p.borrow().grad;
        p.borrow_mut().data -= learning_rate * grad;
    }
}
```

---

## Section 4: ix-micro-transformer

### Overview

A decoder-only transformer (nanoGPT-style) for sequence modeling over integer tokens. This is the most complex micro crate — it introduces tensor operations. Uses `ndarray` (no framework) for 2D/3D tensor operations. Gradients are computed analytically (hand-written backward passes), not via autograd.

### Architecture

```
Embedding → N × (LayerNorm → MultiHeadAttention → LayerNorm → FFN) → LM Head
```

All components are explicit Rust structs with named weight matrices.

### Configuration

```rust
pub struct TransformerConfig {
    pub vocab_size: usize,
    pub context_length: usize,    // max sequence length
    pub n_embed: usize,           // embedding dimension
    pub n_head: usize,            // attention heads
    pub n_layer: usize,           // transformer blocks
    pub dropout: f64,
    pub bias: bool,               // use bias in attention + FFN?
}
```

### Guitar Alchemist–specific defaults

A default config tuned for guitar tablature tokenization:

```rust
pub const GUITAR_TAB_CONFIG: TransformerConfig = TransformerConfig {
    vocab_size: 512,        // string × fret × technique token space
    context_length: 256,    // ~16 bars of tab
    n_embed: 128,
    n_head: 4,
    n_layer: 4,
    dropout: 0.1,
    bias: true,
};
```

### IxQL mapping

The `transformer` production in the IxQL EBNF maps to this crate:

```ixql
csv("guitar_tabs.csv") → tfidf → transformer → cross_validation
  --governed standard
```

---

## Section 5: ix-micro-tokenizer

### Overview

A Byte-Pair Encoding (BPE) tokenizer trained from scratch. No dependency on HuggingFace tokenizers. Implements the same algorithm as GPT-2's tokenizer, expressed explicitly.

### Algorithm (visible, not abstracted)

```rust
pub struct BpeTokenizer {
    vocab: HashMap<Vec<u8>, usize>,    // byte sequence → token id
    merges: Vec<(Vec<u8>, Vec<u8>)>,   // merge rules in priority order
    special_tokens: HashMap<String, usize>,
}

impl BpeTokenizer {
    /// Train BPE from a corpus. Returns Self with learned merges.
    /// Steps (all logged):
    ///   1. Initialize vocab from byte-level character inventory
    ///   2. Count all adjacent pair frequencies
    ///   3. Merge most frequent pair → new token
    ///   4. Repeat until vocab_size reached
    pub fn train(corpus: &str, vocab_size: usize) -> Self;

    pub fn encode(&self, text: &str) -> Vec<usize>;
    pub fn decode(&self, tokens: &[usize]) -> String;
    pub fn vocab_size(&self) -> usize;
}
```

### Domain vocabulary

Guitar Alchemist uses a specialized tokenizer for guitar tab notation, extending the base BPE with domain-specific special tokens:

```
<|fret_0|> .. <|fret_24|>    -- fret positions
<|string_1|> .. <|string_6|> -- string numbers
<|bend|> <|slide|> <|hammer|> <|pull|> <|vibrato|>  -- techniques
<|bar_start|> <|bar_end|>    -- rhythmic structure
<|chord|> <|arpeggio|>       -- harmonic structure
```

---

## Section 6: ix-micro-optim

### Overview

Explicit optimizer implementations. Every gradient update formula is written out with comments referencing the original paper.

### Implemented optimizers

```rust
pub trait Optimizer {
    fn step(&mut self, params: &[Rc<RefCell<Value>>]);
    fn zero_grad(&self, params: &[Rc<RefCell<Value>>]);
}

/// Stochastic Gradient Descent with momentum
/// update: v = momentum * v - lr * grad
///         param += v
pub struct SGD { pub lr: f64, pub momentum: f64 }

/// Adam (Kingma & Ba, 2015)
/// m = beta1 * m + (1 - beta1) * grad
/// v = beta2 * v + (1 - beta2) * grad²
/// m_hat = m / (1 - beta1^t)
/// v_hat = v / (1 - beta2^t)
/// param -= lr * m_hat / (sqrt(v_hat) + eps)
pub struct Adam { pub lr: f64, pub beta1: f64, pub beta2: f64, pub eps: f64 }

/// AdamW — Adam with decoupled weight decay
/// Same as Adam but: param -= lr * weight_decay * param  (before Adam update)
pub struct AdamW { pub lr: f64, pub beta1: f64, pub beta2: f64,
                   pub eps: f64, pub weight_decay: f64 }
```

---

## Section 7: ix-micro-governance

### Overview

The governance crate wires all micro implementations into IxQL-compatible governance gates. This crate is the bridge between the pure-math micro crates and the Demerzel constitutional framework.

### Governance gates exposed

```rust
/// gradient_health — Article 8 (Observability): gradient norms must be finite
pub fn gradient_health(model: &MLP) -> GovernanceGateResult;

/// training_convergence — Article 1 (Truthfulness): training must not be fabricated
pub fn training_convergence(loss_history: &[f64], window: usize) -> GovernanceGateResult;

/// model_card — Article 2 (Transparency): model must have complete metadata
pub fn model_card_complete(card: &ModelCard) -> GovernanceGateResult;

/// bias_detection — Article 10 (Stakeholder Pluralism): model outputs checked for bias
pub fn bias_detection(predictions: &[f64], protected_groups: &GroupLabels) -> GovernanceGateResult;

/// reversibility_check — Article 3 (Reversibility): model weights can be checkpointed
pub fn reversibility_check(model: &MLP, checkpoint_path: &Path) -> GovernanceGateResult;
```

### GovernanceGateResult

```rust
pub struct GovernanceGateResult {
    pub truth: TruthValue,        // T | F | U | C
    pub confidence: f64,
    pub message: String,
    pub article_citations: Vec<String>,
    pub remediation: Option<String>,
}
```

---

## Section 8: IxQL Integration

Each micro crate maps to one or more IxQL productions:

| Crate | IxQL production | ix_pattern |
|---|---|---|
| ix-micro-autograd | `neural_model` (backprop) | — |
| ix-micro-nn | `mlp`, `rnn` | — |
| ix-micro-transformer | `transformer` | — |
| ix-micro-tokenizer | `tfidf`, `word2vec` | — |
| ix-micro-optim | (implicit in training loop) | — |
| ix-micro-governance | `governance_gate` | `grammar_weight_learning` |

The `grammar_weight_learning` ix_pattern uses `ix-micro-autograd` to update Bayesian grammar weights via a gradient signal computed from prediction error:

```ixql
governance_state → grammar_weight_learning(
  grammar: "grammars/sci-ml-pipelines.ebnf",
  signal: prediction_error,
  optimizer: adamw(lr: 0.001)
) --governed standard
```

---

## Section 9: Streeling University Integration

The micro crates are primary teaching materials for the computer-science department:

| Course | Micro crate used | Learning objective |
|---|---|---|
| "Neural Networks from Scratch" | ix-micro-autograd + ix-micro-nn | Understand backpropagation through explicit code |
| "Transformers: No Magic" | ix-micro-transformer | Attention mechanism from first principles |
| "How Tokenizers Work" | ix-micro-tokenizer | BPE algorithm hands-on |
| "Governed ML Pipelines" | ix-micro-governance | Constitutional gates in practice |

Each course links to the crate source as the primary reference implementation. The code is the curriculum.

---

## Section 10: Testing Strategy

### Reference output tests

Each crate ships JSON fixture files (`tests/fixtures/`) with known-good input/output pairs generated from:
- Karpathy's original Python implementations (for autograd, transformer)
- sklearn reference outputs (for optimizers)
- Manual calculation (for small test cases)

Tests assert `abs(actual - expected) < 1e-6`.

### Property-based tests (proptest)

```rust
proptest! {
    // Gradient of sum is 1.0 for all inputs
    #[test]
    fn test_add_gradient(a in -1000.0f64..1000.0f64, b in -1000.0f64..1000.0f64) {
        let va = Value::new(a);
        let vb = Value::new(b);
        let vc = Value::add(&va, &vb);
        vc.borrow().backward();
        prop_assert!((va.borrow().grad - 1.0).abs() < 1e-9);
        prop_assert!((vb.borrow().grad - 1.0).abs() < 1e-9);
    }
}
```

### Governance gate tests

Every governance gate tested with:
- Happy path (T)
- Failure path (F)
- Insufficient data path (U)
- Contradiction path (C — two gates give opposite verdicts)

---

## Constitutional Basis

| Article | Karpathy micro application |
|---|---|
| 1 (Truthfulness) | Gradient health gate catches NaN/Inf before results are reported |
| 2 (Transparency) | Every computation is readable; no black boxes; model card required |
| 7 (Auditability) | Training loss logged at every step; weights checkpointed |
| 8 (Observability) | Gradient norms, loss curves, convergence metrics all exposed |
| 9 (Bounded Autonomy) | Micro models are bounded-scope: they do not self-modify |
| 11 (Ethical Stewardship) | Bias detection gate required before any predictions affect users |

---

## Open Questions

1. **Float precision**: `ix-micro-autograd` uses `f64` for clarity. Should `ix-micro-transformer` support `f32` as well for performance? Recommendation: `f64` only in v1 (pedagogy over speed); `f32` option in v2.

2. **GPU acceleration**: The micro crates deliberately avoid WGPU to stay readable. If `ix-micro-transformer` becomes too slow for useful guitar tab generation, should we add a `--fast` feature that delegates to candle? Recommendation: out of scope; users who need speed should use the production pipeline (memristive-markov, etc.).

3. **Tokenizer domain specialization**: Should the guitar tab tokenizer vocabulary be committed to Demerzel as a governance artifact, or live entirely in ix? Recommendation: vocabulary definition lives in Demerzel (it's a behavioral specification); implementation lives in ix.

4. **Relationship to memristive-markov**: The `grammar_weight_learning` ix_pattern uses both `ix-micro-autograd` (gradient signal) and `memristive-markov` (conductance weights). Should they be coupled or remain independent? Recommendation: independent; `grammar_weight_learning` orchestrates both as a pipeline stage.
