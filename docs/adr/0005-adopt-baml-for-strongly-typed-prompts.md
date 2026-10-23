# ADR 0005: Adopt BAML for Strongly-Typed Prompts and In-Flight Schema Validation

## Status
Accepted — **§Decision.3 and §Consequences amended 2026-07-30** (see *Amendment* below).
The decision to adopt BAML stands; only the client-distribution mechanism changed.

## Context
Our ecosystem currently handles LLM interactions using unstructured prompt markdown templates (e.g. `afk-implement.prompt.md`) or dictionary-based strings (e.g. `aiw_prompt_pack.py`). Output verification is done post-generation at rest using Python's `jsonschema` library or PowerShell's `Test-Json` command.

This design has several drawbacks:
1. **JSON parsing fragility:** Models occasionally output slightly malformed JSON, markdown wrapper blocks (```json ... ```), or omitted properties that cause validation gates to fail and trigger retries.
2. **Scatter Prompt Templates:** Prompts are hard to test, version, and manage across multiple repos.
3. **No compiler type-safety:** Code editors cannot verify properties returned by LLM requests, making refactoring complex and error-prone.

## Decision
We will adopt BAML (Boundary AI Markup Language) to define all LLM interactions as typed prompt functions.

1. **Centralized Schemas:** Prompts and schemas will be declared under `baml_src/` in the `Demerzel` repo.
2. **Output Type Enforcement:** BAML will guarantee that outputs match defined class structures (such as `QaVerdict` or `SwarmVote`) by parsing outputs in native Rust-based transpilation layers.
3. **Automatic Client Generation:** Generators configured inside `baml_src/baml_project.baml` will generate clients:
   * `python/pydantic` client for Demerzel.
   * ~~`typescript` client for chatbots.~~ — *removed, see Amendment 2026-07-30.*
   * ~~`rust` client for ix and hari components.~~ — *removed, see Amendment 2026-07-30.*
4. **CI Integration:** Integrate BAML generate tasks into `scripts/verify.ps1` to keep typings updated and fail builds if schemas are broken.

## Consequences
* Prompts are decoupled from runtime logic and live in dedicated `.baml` files.
* Substantially lower LLM call retries and schema failures due to BAML's stream-parsing capabilities.
* Sibling repos must reference or copy the compiled `baml_client/` folder to access strongly typed clients. — *amended, see below.*
* Python code will import clients via `from baml_client import b` and models from `baml_client.types`.

## Amendment 2026-07-30 — consumers generate their own clients

**What changed.** §Decision.3 declared three generators (Python, TypeScript, Rust) and
§Consequences had sibling repos "reference or copy the compiled `baml_client/` folder".
Only the Python generator remains here. The TypeScript and Rust generators and their
committed output (`clients/typescript/`, `clients/rust/`, 37 files) were removed.

**Why.** `CONTRIBUTING.md`'s CL-817-12 adjudication (2026-07-23) predates this ADR and is
explicit: a consumer-facing library "moves to a sibling repo, with Demerzel keeping only the
contract and behavioral tests", and nothing here "may become a dependency of a consumer
repo's runtime". The Rust and TypeScript trees were exactly that — and had **zero consumers
in this repo**: no `Cargo.toml`, no `package.json`, and no file importing either. The Python
client is different and stays: `validate_dsp_loop.py`, `aiw_prompt_pack.py` and
`monitor_baml_and_learning.py` import it, which makes it repository-local tooling.

`ix` had already reached the same conclusion independently — `crates/ix-baml/src/lib.rs`
rejects a `#[path]` escape into a sibling clone because it "makes `cargo check --workspace`
depend on a checkout that CI and most contributors do not have", and plans to generate into
its own crate. Nothing was broken by the removal.

**What the contract is now.** `baml_src/schema.baml`. Consumers run `baml generate` against
it with their own `output_dir` and commit the result in their own repo, versioning it on
their own cadence. This is strictly better for them than copying: a vendored copy of *our*
generated output pins a snapshot of a generator version, whereas generating from the contract
lets each consumer pick its own BAML version.

**What this costs.** Three repos now run the generator instead of one, so a `schema.baml`
change requires a regeneration in each — the drift surface moves outward rather than
disappearing. That is the trade CL-817-12 already chose, and it is why the contract, not the
client, is the thing to watch.

**§Decision.4 is still unfulfilled.** The drift check exists (`scripts/verify.ps1`) but no
workflow invokes it, so "fail builds if schemas are broken" is not true today. Tracked in
#919. Do not read this ADR as evidence that the check runs.

## Amendment 2026-07-30 (b) — the transport is out of band, on the subscription

**What changed.** §Decision.2 implied BAML would also *make* the LLM call. It does not.
Callers render with `b.request.Fn(...)`, obtain a completion through the Claude Code CLI
(`scripts/baml_claude_code.py`), and type it with `b.parse.Fn(raw)`. Neither BAML step
opens a socket, so the typed-prompt and schema-enforcement benefits this ADR was adopted
for are unaffected — only the wire is different.

**Why.** The function was bound to `client "openai/gpt-4o"`, a provider that appears
nowhere in `state/driver/aiw-budget-policy.json`. An in-band call would therefore have
billed a provider the AIW budget gate has never heard of — the #863 shape exactly: a
correct gate, pointed at a provider nobody is using. `claude-code-cli` *is* declared
(`local-seat`, `subscription-or-local`, no manual approval), so routing through it puts
the spend inside a control that already knows how to classify it.

**The non-obvious part.** Claude Code prefers `ANTHROPIC_API_KEY` over the claude.ai
subscription when both are present, and says so on stderr. Verified 2026-07-30: the same
prompt returned `API Error: 400 ... usage limits` with the key set and a normal completion
with it unset. So `run_claude_code` strips the key from the **child** environment. A
transport whose billing depends on an ambient variable is a coincidence, not a guarantee.

**Fail-closed by construction.** The declared client is now `NeverSendInBand`, pointing at
`http://127.0.0.1:1/v1` — a port nothing can listen on. `b.request` only needs a client to
know what body shape to render; an accidental direct `b.Fn(...)` call gets a connection
error instead of a bill. `test_baml_claude_code.py` asserts both that the grader never
takes the in-band path and that the declared client cannot bill anyone.

**Cost.** One subprocess per call, so a full `validate_dsp_loop` run (3 roles × up to 10
cycles) is minutes rather than seconds, and streaming is unavailable. Acceptable for a
governance gate; wrong for anything interactive.
