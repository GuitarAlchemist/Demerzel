# IxQL Executor Integration Plan

## Goal
Implement a minimal, deterministic Rust IxQL executor inside the `ix` repository that compiles and runs pipelines, routes dynamic values via `serde_json`, integrates BAML for LLM steps, and gates state mutations with JSON Schemas.

## Tasks
- [x] Task 1: Create wrapper crate `crates/ix-baml` in `C:/Users/spare/source/repos/ix/` and add it to workspace members in `ix/Cargo.toml` → Verify: `cargo check -p ix-baml` compiles.
- [~] Task 2: ~~Configure `crates/ix-baml/src/lib.rs` to path-include the generated client from the sibling `Demerzel-baml` workspace~~ → **changed, see Deviations §2.** `ix-baml` now owns the dynamic seam (`BamlOperation` / `BamlRegistry` / offline stand-ins); the generated client is vendored into it once Demerzel PR #908 merges.
- [x] Task 3: Implement AST type definitions ~~inside `crates/ix-agent/src/ast.rs`~~ → `crates/ix-ixql/src/ast.rs` (see Deviations §1). Matches design-spec §2.
- [x] Task 4: Create the `serde_json`-based evaluator loop → `crates/ix-ixql/src/eval.rs`.
- [x] Task 5: Integrate `jsonschema` to intercept `ix.io.write` calls and validate payloads at-rest → `crates/ix-ixql/src/schema.rs`.
- [x] Task 6: Add the BAML function handler registry mapping `→ baml.<Fn>()` steps to `BamlOperation` invocations.
- [x] Task 7: Offline test running the real `qa-architect-cycle.ixql` with a stand-in LLM client → `crates/ix-ixql/tests/ixql_exec_tests.rs`.
- [x] Task 8 (added): Write the parser. The plan assumed one existed; it did not — see Deviations §3.

## Done When
- [x] The `ix` workspace compiles with `ix-baml` and `ix-ixql` included (`cargo clippy --workspace --all-targets` clean; the crate-maturity reconciliation test passes).
- [x] The local test parses and executes the real `qa-architect-cycle.ixql` pipeline offline (54 tests green across both crates).
- [ ] All 412 existing unit tests in `Demerzel` still pass — **not run**: nothing in Demerzel was modified by this work.

## Deviations from the original plan

**§1 — the executor lives in `crates/ix-ixql`, not `crates/ix-agent`.**
`crates/ix-agent/src/eval/` already exists as a module *directory*
(`mod.rs`, `permutation_importance.rs`, `silhouette.rs`), so
`crates/ix-agent/src/eval.rs` could not have been created at all. Beyond that
collision, `ix-agent` is the MCP server; a language runtime does not belong in
it. `ix-agent` can depend on `ix-ixql` later to expose the executor as a tool.

**§2 — no `#[path]` include of Demerzel's generated client.**
Design-spec §5 proposes
`#[path = "../../../../Demerzel-baml/clients/rust/baml_client/mod.rs"]`. Three
problems: the directory `Demerzel-baml` does not exist (the client is at
`Demerzel/clients/rust/baml_client`); that tree is untracked and lives only on
the unmerged `feat/baml-adoption` branch (PR #908); and a `#[path]` escape into
a sibling clone makes `cargo check --workspace` fail for CI and for every
contributor without Demerzel checked out. `ix-baml` instead owns the dynamic
boundary, which is what the executor actually dispatches through, so vendoring
the generated client later changes nothing outside that crate.

**§3 — a parser had to be written.**
The plan and the design spec both assumed parsing was solved by
`tree-sitter-ixql`. It is not, for this input: that grammar describes the
*ML-pipeline* dialect from `grammars/sci-ml-pipelines.ebnf` (`csv(…) →
train(…)`), while `pipelines/*.ixql` — including the tracer target — are written
in the binding/record dialect the design spec's own AST models. A hand-rolled
recursive-descent parser for that second dialect is in
`crates/ix-ixql/src/{lexer,parser}.rs`.

**§4 — `CompoundOp` (AST) and `CompoundRecord` (runtime) are separate types.**
Design-spec §3 puts `compound_stash: Vec<CompoundOp>` on the execution context,
but `CompoundOp` holds *unevaluated* expressions; a stash of those tells a
consumer nothing. The runtime records evaluated operands instead.

**§5 — `when` blocks parse to an explicit error.**
`Statement::When` exists in the AST per the spec, but no pipeline in
`Demerzel/pipelines` uses one, so the block-delimiting rule (IXQL has no
statement terminator and no braces) is still undecided. The parser refuses
`when` with a message saying so rather than guessing a rule that would later
have to change.

## What is deliberately not done

- **The `ix.io.write` gate is empty until a caller registers schemas.** There is
  no path→schema autodiscovery; `Executor::schema_gate()` is part of the setup
  surface. A gate that guessed its own bindings would create a false sense of
  coverage.
- **`qa-verdict.schema.json` is not vendored into ix.** The canonical copy is in
  `ga`, already vendored once into Demerzel under a no-drift policy. The test
  uses a deliberately partial subset schema instead — enough to prove the gate
  admits a conforming write and refuses a non-conforming one.
- **No MCP tool exposure.** Wiring `ix-ixql` into `ix-agent` is a separate,
  reversible step.
- **Only the tracer pipeline is covered — 1 of 23.** Every file in
  `Demerzel/pipelines` was run through the parser as a coverage probe:
  `qa-architect-cycle.ixql` parses, the other 22 do not. The blockers, in
  descending frequency, are the language features this slice does not
  implement. Counts are of *first* error per file, so a file may need more than
  the one feature it tripped on:
  - **lambdas** — `→ map(b => { … })` (10 files). `Expr::Lambda` is in the
    design spec's AST and was dropped from this slice along with the rest of
    the surface the tracer target never reaches.
  - **a nested pipeline inside an argument list** — a `→` appearing between
    `(` and `)` (3 files).
  - **arithmetic** — `current_params.brightness + 0.05`, and `*` / `/`
    (4 files).
  - **null-coalescing** — `sweep_config.seed ?? 42` (2 files).
  - **`name = value` argument syntax** alongside the `name: value` this parser
    accepts, and slice indexing `window[:-1]` (2 files).
  - **bare step references** — `→ bias_assessment` with no argument list
    (1 file); the parser currently requires a `→` step to be a call.

  This is the honest scope line: the tracer bullet goes end to end through one
  real pipeline, and extending to the corpus is a second, separately-sized
  piece of work rather than a finishing touch.
