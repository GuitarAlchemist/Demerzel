# Design Spec: Rust-based IxQL Pipeline Executor (with BAML)

**Status:** Proposed  
**Host Workspace:** `ix` (Rust)  
**Tracer Target:** `qa-architect-cycle.ixql` and `ml-feedback-loop.ixql`  
**Core Abstraction:** **BAML** for in-flight LLM parsing + **JSON Schema** for at-rest governance validation.

---

## 1. High-Level Architecture

The executor lives as a module/crate within the `ix` workspace. It bridges the dynamic dataflow of IxQL with the strongly-typed schema validation of BAML at the LLM boundary.

```text
       [ Natural Language Prompt ]
                   │
                   ▼
    +-----------------------------+
    |   BAML Frontend Compiler    | (LLM translation)
    +-----------------------------+
                   │ (Produces)
                   ▼
    [ Validated IxQL AST / Intent ]
                   │
                   ▼
    +-----------------------------+
    |   tree-sitter-ixql Parser   | (Syntax Validation)
    +-----------------------------+
                   │
                   ▼
+=======================================+
|       Rust 'ix' IxQL Executor         |
|                                       |
|  [ Step 1: Standard IxQL Compute ]    |
|                  │                    |
|                  ▼                    |
|  [ Step 2: BAML Action Step ]         |
|       │                               |
|       ├─► Map IxQL Value to JSON      |
|       ├─► Call Generated BAML Client  | ──► (LLM Validation/Reasoning)
|       └─► Map BAML Struct to Value    | 
|                  │                    |
|                  ▼                    |
|  [ Step 3: Conditional Branching ]    |
+=======================================+
                   │
                   ▼
        [ Compound State Updates ]
```

---

## 2. Abstract Syntax Tree (AST) in Rust

The AST is represented using Rust's enums and `Box` pointers to handle recursive definitions.

```rust
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp {
    Eq, Neq, Gt, Gte, Lt, Lte,
    And, Or, In, NotIn, IsEmpty, IsNotEmpty
}

#[derive(Debug, Clone, PartialEq)]
pub enum Literal {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
}

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Lit(Literal),
    Var(String),
    Member(Box<Expr>, String),
    Array(Vec<Expr>),
    Record(HashMap<String, Expr>),
    Interpolation(Vec<Expr>),
    BinOp(Box<Expr>, BinaryOp, Box<Expr>),
    Call {
        target: Box<Expr>,
        positional: Vec<Expr>,
        named: HashMap<String, Expr>,
    },
    Lambda(Vec<String>, Box<Block>),
    Pipeline(Box<Expr>, Vec<PipeStep>),
}

#[derive(Debug, Clone, PartialEq)]
pub enum PipeStep {
    CallStep {
        target: Box<Expr>,
        positional: Vec<Expr>,
        named: HashMap<String, Expr>,
    },
    FanOut(Vec<Block>),
    Parallel(Vec<Block>),
    Compound(Vec<CompoundOp>),
}

#[derive(Debug, Clone, PartialEq)]
pub enum CompoundOp {
    Harvest(Box<Expr>),
    Promote { id: String, condition: Option<Box<Expr>> },
    Log { id: String, destination: Box<Expr> },
    Teach { id: String, target: String },
}

#[derive(Debug, Clone, PartialEq)]
pub enum Statement {
    Assign(String, Box<Expr>),
    Do(Box<Expr>),
    When(Box<Expr>, Box<Block>),
}

pub type Block = Vec<Statement>;
```

---

## 3. Dynamic Value Mapping via Serde

To handle data flow natively and interoperate with BAML's generated serde structs, the runtime standardizes on `serde_json::Value` for its dynamic types:

```rust
use serde_json::Value;

pub struct ExecutionContext {
    pub env: HashMap<String, Value>,
    pub compound_stash: Vec<CompoundOp>,
}

pub trait BamlOperation: Send + Sync {
    /// Takes the dynamic input Value, deserializes it to the BAML input,
    /// calls the generated BAML client, and serializes the result back to Value.
    fn invoke(&self, input: &Value) -> Result<Value, String>;
}
```

### Example Mapping Workflow:
1. **Input Map:** `let baml_input: BamlGeneratedInput = serde_json::from_value(input_value)?;`
2. **LLM Query:** `let baml_output = baml_client::b.MyFunction(baml_input).await?;`
3. **Output Map:** `let output_value: Value = serde_json::to_value(&baml_output)?;`

---

## 4. Preserving JSON Schema Authority

While BAML handles prompt rendering, streams, and in-flight LLM extraction correctness:
1. **At-Rest Validation:** Every file-write action (e.g. `ix.io.write`) intercepts the payload.
2. **Schema Engine:** The executor loads the canonical JSON Schema (e.g., `qa-verdict.schema.json`) and runs it against the `serde_json::Value` using the Rust `jsonschema` crate.
3. **Execution Gate:** If the schema validation fails, the write is aborted, and the pipeline terminates with a validation error.

---

## 5. Linking BAML Client into `ix` Crate

We introduce a dedicated wrapper crate `crates/ix-baml` within `ix`'s Cargo workspace.

* **Workspace Cargo.toml:**
  ```toml
  [workspace]
  members = [
      # ...
      "crates/ix-baml"
  ]
  ```
* **Crate Cargo.toml:**
  ```toml
  [dependencies]
  baml = "0.223.0"
  serde = { version = "1", features = ["derive"] }
  serde_json = "1"
  ```
* **Src include (`crates/ix-baml/src/lib.rs`):**
  ```rust
  #[path = "../../../../Demerzel-baml/clients/rust/baml_client/mod.rs"]
  pub mod baml_client;
  ```

  > **Superseded 2026-07-30.** This proposal was rejected — see the plan's Deviations §2
  > for `ix`'s reasons — and the target no longer exists: Demerzel removed
  > `clients/rust/` under CL-817-12 (ADR-0005 Amendment). `ix` generates its own client
  > from Demerzel's `baml_src/schema.baml` into `ix-baml`, so there is no path to escape
  > into and `cargo check --workspace` stays self-contained.
