# BAML adoption assessment

**Date:** 2026-07-28  
**Scope:** Demerzel, `ga`, `tars`, `ix`, and `demerzel-bot`  
**Decision:** **Defer ecosystem adoption. Permit one isolated, time-boxed
evaluation in `demerzel-bot`; do not put BAML on a production path or make it a
cross-repo contract yet.**

## Executive judgment

BAML has a real technical advantage where an application makes many
schema-shaped LLM calls: prompts become typed functions, its schema-aligned
parser repairs common malformed-model output, generated clients expose typed
results and partial streams, and provider fallback/retry plus prompt tests live
beside the prompt. Those capabilities are substantially better than hand-built
JSON extraction.

They do not justify fleet-wide adoption today:

1. **The product is between generations.** The latest conventional framework
   release is [`0.222.0` (2026-04-27)](https://github.com/BoundaryML/baml/releases/tag/0.222.0),
   while the repository's current branch describes a much broader
   ["programming language for agents"](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/README.md)
   and publishes a separate `0.15.1-nightly` language toolchain
   ([example release](https://github.com/BoundaryML/baml/releases/tag/baml-language-0.15.1-nightly.20260728.e)).
   Boundary's current adoption page explicitly says this new line is pre-1.0
   and says some agent/runtime features are still under development
   ([current adoption status](https://boundaryml.com/explore#part-4--adopting-baml),
   [developing agent features](https://boundaryml.com/explore#part-5--building-agents)).
   Its checked-in SDK support matrix labels Python and TypeScript beta, Go and
   Rust alpha, and C# “coming soon”
   ([SDK support matrix](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/baml_language/sdks/README.md)).
   This is active development, not abandonment, but it is an unstable point at
   which to standardize five repositories.
2. **Its strongest interoperability story does not match this fleet.** Python
   and TypeScript are the best-supported hosts. The core runtime paths in `ga`
   and `tars` are .NET/C#/F#, and `ix` is Rust. The repository contains a
   substantial C# bridge and release pipeline, but its own architecture notes
   show a CFFI/native-library boundary and generated runtime
   ([C# bridge source](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/baml_language/sdks/csharp/README.md));
   the checked-in support matrix still lists C# as “coming soon.” F# has no
   first-class target.
3. **BAML types would be a second schema authority.** Demerzel and its consumers
   already treat committed JSON Schema as the structural source of truth.
   BAML's current TypeBuilder documentation lists JSON Schema integration as a
   future feature, and its tracker records gaps in expressing general JSON
   Schema validation constraints
   ([TypeBuilder limitations](https://docs.boundaryml.com/ref/baml_client/type-builder),
   [issue #765](https://github.com/BoundaryML/baml/issues/765)). Re-declaring
   governance verdicts in BAML would violate Demerzel's “harvest, don't
   declare” architecture unless code generation has one unambiguous direction.
4. **Most repositories already own the adjacent abstraction.** Demerzel has a
   small, fixture-tested provider seam; `ga` and `tars` use
   `Microsoft.Extensions.AI`-style interfaces; `ix` has direct, testable Rust
   calls; and the bot has explicit routing, health, latency-budget, and
   local-first semantics. BAML could replace prompt rendering and parsing for
   selected calls, but replacing these routing boundaries would discard
   domain-specific behavior for a generic client strategy.

The appropriate rung is therefore **defer**, not decline: preserve BAML as a
candidate for typed LLM-boundary calls, gather local evidence in the one
JavaScript runtime where reversal is cheap, and revisit after a stable language
release and a clear schema-import story.

## Evidence boundary: two BAML surfaces

The official sources currently expose two overlapping surfaces:

- The established prompt framework documented at `docs.boundaryml.com`:
  `.baml` prompt functions, generated clients, schema-aligned parsing,
  provider strategies, typed streaming, and IDE/CLI prompt tests. Its generated
  client performs the endpoint call, malformed-JSON repair, typed conversion,
  and error handling
  ([generated-client contract](https://docs.boundaryml.com/guide/introduction/baml_client)).
- The new general-purpose agent language on the repository's default branch:
  runtime types, typed errors, green threads, built-in tests/evals, standalone
  execution, binary packaging, and generated host SDKs
  ([current README](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/README.md),
  [current product overview](https://boundaryml.com/explore)).

Claims below about fallbacks, the client registry, React hooks, and Boundary
Studio are established-framework capabilities. They should not be assumed to
have identical compatibility or lifecycle guarantees in the new language line
until Boundary publishes a stable migration contract.

## Capability assessment

| Concern | Benefit | Cost or gap for this ecosystem | Judgment |
|---|---|---|---|
| Typed structured outputs | Function return types generate host-language models; SAP parses model output even when provider-native structured output is weak. Checks can be non-fatal and assertions can reject invalid values ([checks and asserts](https://docs.boundaryml.com/guide/baml-advanced/checks-and-asserts)). | BAML's type system is not the fleet's existing JSON Schema authority. Complex schema constraints and JSON Schema import remain gaps. A repaired parse is also not equivalent to a governance-valid verdict; canonical schema validation must remain after parsing. | **Strongest reason to pilot**, but only for a new leaf-shaped output, not an existing cross-repo artifact. |
| Multi-provider routing | Declarative retry, ordered fallback, nested fallback, round-robin, and runtime client selection are built in ([fallback strategy](https://docs.boundaryml.com/ref/llm-client-strategies/fallback), [client registry](https://docs.boundaryml.com/ref/baml_client/client-registry)). It supports OpenAI, Anthropic, Google, Bedrock, Azure, and OpenAI-compatible endpoints including Ollama. | Strategy failure is transport/client-oriented; ecosystem routing also encodes constitutional escalation, domain classification, model availability, budget, and readiness. BAML would be a lower-level executor, not the fleet router. Moving those policies into `.baml` would split governance from existing policy artifacts. | Use behind, never instead of, an existing domain router. |
| Prompt versioning | Prompts are local text files, diffable and versioned by Git; this matches the ecosystem's preference for committed artifacts ([BAML's versioning philosophy](https://github.com/BoundaryML/baml/tree/v0.222.0#bamls-design-philosophy)). | There is no independent prompt registry or release contract in the open-source core. Generated clients and runtime/CLI versions must match ([upgrade guidance](https://docs.boundaryml.com/guide/development/upgrade-baml-versions)), so a prompt-only change can also create generated-code churn. | Compatible philosophy; little net gain by itself. |
| Streaming | Typed partial results and final results are exposed by generated clients; TypeScript/React hooks distinguish stream and final callbacks ([client streaming](https://docs.boundaryml.com/ref/baml_client/client), [React hook contract](https://docs.boundaryml.com/ref/baml_client/react-next-js/hook-input)). | Partial structured values have different validity semantics from final values. Discord bot replies and current governance workflows are non-streaming; only a `ga` web experience has an obvious UX benefit, while its LLM backend is C#. | Valuable later for a TS-owned UI path, not an adoption driver now. |
| Testing and evals | Tests are colocated with functions, runnable in parallel from CLI/CI, and support checks/asserts ([CLI test reference](https://docs.boundaryml.com/ref/baml-cli/test)). The new language advertises dynamic test sets, statistical runners, and LLM-as-judge evals ([current test/eval direction](https://boundaryml.com/explore#3-write-tests-anywhere-or-load-them-at-runtime)). | Model-backed tests remain nondeterministic and incur provider cost. They complement rather than replace deterministic fixture tests, JSON Schema validation, adversarial corpora, and behavioral tests. The richer new-language eval surface is itself pre-1.0. | Good authoring ergonomics; require recorded fixtures and deterministic outer assertions. |
| Observability | Local terminal logging, collectors, a workflow view/profiler, and optional hosted Boundary Studio traces are available. Studio traces typed function inputs/outputs when `BOUNDARY_API_KEY` is configured ([Studio tracing](https://docs.boundaryml.com/guide/boundary-cloud/observability/tracking-usage)). | `BAML_LOG=info` includes prompt, raw response, and parsed response ([terminal logs](https://docs.boundaryml.com/guide/development/terminal-logs)); governance prompts and Discord content therefore require redaction and conservative log levels. Hosted traces add another data processor and must be separately approved. CLI usage telemetry is enabled unless disabled; it excludes prompts/responses but records command, version, machine characteristics, a machine ID, and a salted project-root hash ([telemetry policy](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/TELEMETRY.md)). | Local-only for a pilot; set `DO_NOT_TRACK=1`, do not set `BOUNDARY_API_KEY`, and keep logs at `warn` or `off`. |
| Deployment and runtime | Generated SDKs can embed the runtime, and the new CLI can package selected functions as a standalone binary ([SDK model](https://boundaryml.com/explore#1-drops-into-your-existing-stack), [binary packaging](https://boundaryml.com/explore#5-baml-pack--ship-a-function-as-a-tiny-binary)). | Adds a compiler/codegen step, generated artifacts, native Rust/CFFI assets, exact-version coupling, and platform/RID testing. “Any language” in the established line uses a BAML HTTP sidecar plus generated OpenAPI client, which official docs still call preview ([REST/OpenAPI deployment](https://docs.boundaryml.com/guide/development/deploying/docker-rest-api)). | Acceptable in one service after proof; disproportionate for shell CI or a small direct call. |
| Licensing and privacy | Repository and runtime are Apache-2.0 ([license](https://github.com/BoundaryML/baml/blob/8c8af4154e174218a24c9b6e88cc52be9310d47e/LICENSE)); prompts remain local unless an explicitly configured provider or Studio receives them. | Apache notice obligations are ordinary. Telemetry opt-out and trace configuration must be made explicit in CI/container policy rather than assumed. | No licensing blocker. |
| Maturity | Active project, frequent releases, extensive CI, several native clients, and a production-oriented established framework. | Both release families remain below 1.0, the default branch has changed product scope, current public pages and older docs describe different support matrices, and several advertised agent primitives are explicitly “coming soon.” | Mature enough to evaluate; not stable enough to govern the fleet. |

## Repository fit

### Demerzel — decline runtime adoption; allow research artifacts only

Demerzel is explicitly governance rather than product runtime. Its sanctioned
scripts must serve governance tooling and must not become consumer runtime
dependencies
([contribution boundary](https://github.com/GuitarAlchemist/Demerzel/blob/1617bd2060c82cc8274f96424b18a18d6a6fb471/CONTRIBUTING.md#what-demerzel-is-and-is-not)).
Its existing [`llm_call.sh`](https://github.com/GuitarAlchemist/Demerzel/blob/1617bd2060c82cc8274f96424b18a18d6a6fb471/.github/scripts/llm_call.sh)
already centralizes Claude, Gemini, and OpenAI request/response differences
behind a stable stdout/stderr/exit-code contract and is fixture-testable.

BAML would improve structured parsing for emitters, but those emitters must
continue validating canonical JSON Schema. Introducing a BAML schema for the
same verdict would create dual authority. Replacing a small shell seam with a
compiler/runtime and generated SDK would also make GitHub workflows heavier
without improving their current plain-text contract.

**Fit:** low. Do not add BAML as a Demerzel dependency or encode constitutions,
policies, IxQL, or cross-repo schemas in BAML.

### `ga` — defer server adoption; reconsider after C# SDK stabilization

`ga` already isolates providers behind `Microsoft.Extensions.AI.IChatClient`.
Its Anthropic project deliberately prevents provider SDK types from escaping
the adapter
([provider project](https://github.com/GuitarAlchemist/ga/blob/10e29d29ea874e0369ccc546de5470966577b963/Common/GA.Providers.Anthropic/GA.Providers.Anthropic.csproj)),
and its chatbot uses Microsoft Ollama/OpenAI packages
([chatbot project](https://github.com/GuitarAlchemist/ga/blob/10e29d29ea874e0369ccc546de5470966577b963/Apps/GaChatbot/GaChatbot.csproj)).
That is already a deep, ecosystem-native interface.

BAML could help a specific extraction/classification call and eventually a
React streaming UI. Today, however, adopting it in the C# server means taking a
new generated client plus native bridge or running the preview HTTP sidecar.
Using BAML only in React would move model credentials and orchestration toward
the browser, which is the wrong boundary.

**Fit:** medium potential, low present readiness. Re-evaluate when Boundary
publishes a stable C# package and cancellation/streaming/RID contract, and only
for one typed LLM leaf behind `IChatClient`-level application interfaces.

### `tars` — defer

The active v2 code already has distinct Ollama, OpenAI-compatible, and Anthropic
F# clients plus `Microsoft.Extensions.AI`
([LLM project](https://github.com/GuitarAlchemist/tars/blob/0004239b05c8fcc1aab0a3055a97071e221dd563/v2/src/Tars.Llm/Tars.Llm.fsproj),
[Cortex project](https://github.com/GuitarAlchemist/tars/blob/0004239b05c8fcc1aab0a3055a97071e221dd563/v2/src/Tars.Cortex/Tars.Cortex.fsproj)).
There is no native F# target. Consuming a developing C# bridge from F# would add
generated C# types, CFFI assets, and interop ergonomics that BAML does not
document; the preview REST route would introduce a sidecar into an already
complex system.

**Fit:** low until the C# SDK is stable and a small F# interop spike proves
discriminated-union, option/null, async, cancellation, and streaming behavior.

### `ix` — defer

`ix` has a native Rust dependency graph and direct Anthropic call in the skill
compiler, with explicit timeouts and JSON handling
([current call site](https://github.com/GuitarAlchemist/ix/blob/6a2850df4ac6b1085348f9a05359a53b776cdba5/crates/ix-skill/src/verbs/compile.rs#L484)).
The established BAML line added a native Rust SDK in `0.218.0`
([changelog](https://docs.boundaryml.com/changelog/changelog#02180---2026-01-22)),
but the current new-language SDK matrix labels Rust support alpha. This makes a
long-lived Rust integration especially sensitive to which BAML generation is
selected.

**Fit:** medium technical potential for typed proposer outputs, but defer until
the new Rust SDK is stable and the project publishes migration guidance from
the `0.22x` framework runtime.

### `demerzel-bot` — best pilot host, not yet an adoption target

The bot is Node/CommonJS and directly depends on the Anthropic and OpenAI SDKs
([manifest](https://github.com/GuitarAlchemist/demerzel-bot/blob/0755dd1eafcae70ba42f17a8b50ce51b31de6339/package.json)).
Its router owns local Ollama tiering, cloud escalation, availability caching,
and latency-budget telemetry
([router](https://github.com/GuitarAlchemist/demerzel-bot/blob/0755dd1eafcae70ba42f17a8b50ce51b31de6339/src/llm-router.js)).
TypeScript is BAML's strongest host language, and this is a deployable service
where robust structured outputs could create value.

The bot is still plain JavaScript/CommonJS, so BAML's generated TypeScript
client adds a build step or a small TS island. BAML must remain *behind*
`llm-router.js`: its generic fallback must not replace the bot's constitutional
cloud escalation, local availability behavior, or budget accounting.

**Fit:** highest, but only as an isolated experiment.

## Smallest reversible pilot

Create a short-lived branch in `demerzel-bot`; do not change production imports
or deployment manifests.

1. Add `experiments/baml-route-decision/` with a separately pinned
   `@boundaryml/baml@0.222.0` dev dependency and committed lockfile. Do not use a
   nightly. Keep all generated output inside that directory.
2. Define one new, non-authoritative output type such as:
   `RouteExplanation { route: "local" | "cloud", confidence: float,
   reasons: string[] }`. It may *explain* the existing router's decision but
   must not make or override that decision.
3. Run it against 20–30 existing safe routing fixtures using local Ollama.
   Include malformed JSON, markdown-wrapped JSON, missing fields, an unknown
   enum, timeout, provider failure, and cancellation. Compare:
   - schema-valid final-result rate;
   - false repair/semantic corruption rate;
   - cold and warm latency;
   - package/install size and Windows/Linux build success;
   - clarity of errors and generated diffs.
4. Add one opt-in Anthropic fallback test, excluded from normal CI. Keep routing
   external: the existing router selects a client; BAML renders/parses only.
5. Set `DO_NOT_TRACK=1`, leave `BOUNDARY_API_KEY` unset, and set
   `BAML_LOG=warn`. Never send Discord production content to Studio.
6. Delete the experiment after recording results unless all exit criteria pass.
   Reversal must be removal of one directory with no production call-site or
   package-manifest change.

**Exit criteria for considering a real pilot:**

- at least 95% of expected-valid fixture outputs parse to the intended semantic
  value, with **zero** cases where repair changes an invalid semantic answer
  into a plausible but wrong one;
- deterministic outer validation remains in place;
- Windows and Linux builds are reproducible from the lockfile;
- added warm-call overhead is measured and acceptable for the bot;
- no hosted telemetry/traces or secrets appear in logs;
- the team can state which BAML product line it is pinning and Boundary has
  published a credible migration path for that line.

If the experiment succeeds, the first production use should be a new
leaf-shaped extraction function in `demerzel-bot`, feature-flagged with the
existing direct-SDK path as rollback. It should **not** be a fleet package,
shared schema source, `ga`/`tars`/`ix` migration, or replacement for
`llm-router.js`.

## Revisit triggers

Re-open the decision when all of the following are true:

- the new language line has a stable non-nightly release and a documented
  migration path from the `0.22x` framework;
- TypeScript, Python, Rust, and C# SDK support have published stability and
  deployment matrices; F# interop has a supported or demonstrated path;
- BAML can consume canonical JSON Schema, or the ecosystem has approved a
  one-way generator that prevents BAML/JSON-Schema drift;
- the bot pilot demonstrates a material reliability gain over direct SDK plus
  canonical validation;
- local-only tracing, redaction, and telemetry settings are encoded in the
  deployment contract.

Until then, use BAML as a research candidate, not an ecosystem standard.
