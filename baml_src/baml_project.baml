// Client generation — ADR-0005 §Decision.3.
//
// One generator per consumer language. Each needs a DISTINCT output_dir: BAML
// creates `<output_dir>/baml_client`, so pointing two generators at the same
// directory makes the last one silently clobber the others.
//
// Python stays at the repo root so `from baml_client import b` resolves as
// ADR-0005 §Consequences specifies. The other two live under `clients/` and are
// copied/referenced by sibling repos (policy `recursive-learning-eval`
// applies_to: demerzel, tars, ix — each needs a client to consume the contract).

generator python_client {
  output_type "python/pydantic"
  output_dir "../"
  version "0.223.0"
}

// Consumed by the chatbot front-ends (ga).
generator typescript_client {
  output_type "typescript"
  output_dir "../clients/typescript"
  version "0.223.0"
}

// Consumed by ix and hari. Emits a module tree (mod.rs + types/ + functions/)
generator rust_client {
  output_type "rust"
  output_dir "../clients/rust"
  version "0.223.0"
}
