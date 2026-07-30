# ADR 0005: Adopt BAML for Strongly-Typed Prompts and In-Flight Schema Validation

## Status
Accepted

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
   * `typescript` client for chatbots.
   * `rust` client for ix and hari components.
4. **CI Integration:** Integrate BAML generate tasks into `scripts/verify.ps1` to keep typings updated and fail builds if schemas are broken.

## Consequences
* Prompts are decoupled from runtime logic and live in dedicated `.baml` files.
* Substantially lower LLM call retries and schema failures due to BAML's stream-parsing capabilities.
* Sibling repos must reference or copy the compiled `baml_client/` folder to access strongly typed clients.
* Python code will import clients via `from baml_client import b` and models from `baml_client.types`.
