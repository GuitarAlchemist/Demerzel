// Client generation — ADR-0005 §Decision.3 (amended 2026-07-30, see the ADR).
//
// ONE generator lives here: the Python client, which is this repo's own tooling —
// `scripts/validate_dsp_loop.py`, `scripts/aiw_prompt_pack.py` and
// `scripts/monitor_baml_and_learning.py` import it. It stays at the repo root so
// `from baml_client import b` resolves, as ADR-0005 §Consequences specifies.
//
// The TypeScript and Rust generators were REMOVED. Their output was a consumer-facing
// library with zero consumers in this repo — no `package.json`, no `Cargo.toml`, nothing
// here that imports either — and CONTRIBUTING.md's CL-817-12 adjudication is explicit
// that such a library "moves to a sibling repo, with Demerzel keeping only the contract".
// The contract is `schema.baml`; each consumer generates its own client from it.
//
// Do not re-add a generator whose output this repo does not itself consume. Generating a
// client is not the same as owning its runtime, and a client generated here would be a
// consumer's runtime dependency living in the governance repo.
//
// If you do add one, give it a DISTINCT output_dir: BAML creates
// `<output_dir>/baml_client`, so two generators sharing a directory silently clobber
// each other.

generator python_client {
  output_type "python/pydantic"
  output_dir "../"
  version "0.223.0"
}
