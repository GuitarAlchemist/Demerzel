# CONTEXT — Demerzel domain glossary

> The shared language of the Demerzel governance repo. `/grill-with-docs` grows
> this lazily as terms get resolved; `/improve-codebase-architecture`, `/qa`, and
> the other engineering skills read it so their output uses **our** words. This is
> a **seed** — add terms when a real ambiguity is resolved, not speculatively.

## What Demerzel is

AI governance for the GuitarAlchemist ecosystem: reusable **constitutions**,
**personas**, alignment **policies**, hexavalent logic, behavioral tests, and
cross-repo loop control. Named after R. Daneel Olivaw (Asimov's Foundation) — it
defines *how agents should behave*, not *how they compute*, and is deliberately
separate from runtime code. Consumed by sibling repos **ga** (.NET/music+RAG),
**ix** (Rust ML), and **tars** (F# theory) as a submodule (`governance/demerzel/`)
or sibling clone, plus the `demerzel-bot` Discord agent.

## Architecture invariant

**Constitutional hierarchy** — Asimov root (precedence: ROOT) overrides the
Default + Demerzel-mandate + epistemic constitutions, which override operational
**policies**, which override **persona** preferences. The Zeroth Law (do not harm
humanity) overrides everything. Constitutions are **append-only**.

## Core terms (seed)

- **Constitution / Persona / Policy** — the three artifact tiers. Constitutions are
  hard boundaries (append-only); personas are structured behavioral profiles
  (role/capabilities/constraints/voice), each requiring a behavioral test; policies
  are versioned, auditable alignment/rollback rules.
- **Hexavalent logic (T/P/U/D/F/C)** — truth values: True, Probable, Unknown,
  Doubtful, False, Contradictory. `U` triggers investigation; `C` triggers
  escalation. (The README's older "tetravalent" T/F/U/C is the same lattice's
  4-value subset.) The probability-distribution shape over these values lives in
  **one** schema, `schemas/fuzzy-distribution.schema.json` — the byte-identical
  `hexavalent-distribution` duplicate was collapsed into it 2026-06-21 (its
  `$id`, `https://github.com/GuitarAlchemist/Demerzel/schemas/fuzzy-distribution`,
  is the cross-repo-stable reference target).
- **IxQL** — the declarative EBNF-grammared language (`grammars/`) for composing
  governed ML pipelines (`pipelines/*.ixql`); every step maps to a hexavalent
  conclusion + constitutional gates. Executed by the **ix** forge.
- **HALT-ALL marker** — the single cross-repo overseer signal: `~/.demerzel/HALT-ALL`,
  written by `scripts/demerzel_halt.py`, read by every `/auto-optimize` consumer at
  Step 0. The **only mandatory** cross-repo signal; everything else is advisory.
- **QA Architect Tribunal** — cross-repo PR-quality governance: repo-dispatch events
  emit verdicts validated against `schemas/contracts/qa-verdict.schema.json`. v0.1
  contract — **do not freeze** until the owning plan's Phase 4.
- **LOLLI / Resilience score (R)** — `R = injections_caught / injections_total`; the
  chaos-engineering metric for how well governance detects injected poison (dead
  bindings, orphaned branches, BS descriptions, unconsumed artifacts).
- **BAML (Boundary AI Markup Language)** — the DSL (`baml_src/`) that declares prompts as
  strongly-typed functions, enforcing LLM output schemas *in flight* rather than validating
  them at rest ([ADR-0005](docs/adr/0005-adopt-baml-for-strongly-typed-prompts.md), which
  supersedes the earlier **defer** recommendation in
  [`docs/research/2026-07-28-baml-adoption-assessment.md`](docs/research/2026-07-28-baml-adoption-assessment.md);
  adoption is tracked in #890). `baml_src/schema.baml` is **the contract**; Demerzel generates
  exactly one client from it — Python/Pydantic at the repo root (`baml_client/`, so
  `from baml_client import b` resolves), because this repo's own scripts import it. Consumers
  generate their own from the same contract: a client library built here for a sibling to
  compile would be that sibling's runtime living in the governance repo, which
  `CONTRIBUTING.md`'s CL-817-12 adjudication sends to the sibling. If you do add a generator,
  give it a distinct `output_dir` — BAML writes `<output_dir>/baml_client`, so two generators
  sharing a directory silently clobber each other.
  Because the client is derived-but-tracked, `baml_src/` and `baml_client/` can disagree;
  `scripts/verify.ps1` regenerates and diffs to catch that, but **no workflow invokes it**
  (#919), so treat a matching pair as unverified rather than guaranteed.
- **validate_dsp_loop** — the self-correcting parameter gate (`scripts/validate_dsp_loop.py`):
  binary-searches a DSP distortion parameter until a hexavalent swarm consensus clears the
  bounds in [`logic/dsp-safety-bounds.yaml`](logic/dsp-safety-bounds.yaml). Two interchangeable
  graders — deterministic threshold comparisons (default) and the typed BAML
  `EvaluateSignalSwarm` function (`--use-baml`) — read the *same* bounds file, so the code
  gate and the model gate cannot drift apart. The BAML grader's transport is **out of
  band**: BAML renders the prompt and types the answer locally, and the completion comes
  from `claude -p` on the subscription via `scripts/baml_claude_code.py`, which strips
  `ANTHROPIC_API_KEY` from the child environment because Claude Code otherwise prefers it
  over the claude.ai login. No BAML call bills a metered provider. Emits an audited record per run to
  `state/dsp-validation/`. Only a cycle that passes in **this** run may report a value, so an
  aborted or non-converging run exits non-zero rather than re-proposing a cached one.
  `--use-cached-bounds` authorizes a *warm start* — narrowing the search space to a prior
  value, which cycle 1 then re-validates — and nothing more. A validated parameter remains a
  **proposal**; enacting it as a control input is a separate explicit human authorization,
  per Article 9.

## Architecture seams (designed 2026-06-20 via `/improve-codebase-architecture`; built 2026-06-21, PR #357)

A single deepening that collapses today's hand-synced indices and scattered validators
into a few deep modules. The unifying discipline: **harvest, don't declare** — every
fact lives in one place and is read out, never restated.

- **Governance manifest** — `governance-manifest.json`, *derived* by `scripts/build_manifest.py`
  from the filesystem. Exposes one small interface over three harvested concerns:
  *inventory* (artifacts on disk), *edges* (read from artifacts' own reference fields),
  and *health snapshots* (resilience/effectiveness values pulled from their emitters with
  `computed_at` provenance — never recomputed). Committed and CI-diffed; the README-SYNC
  counts and the constitutional-precedence prose are populated from it. Replaced the
  hand-maintained `context-map.yaml` (removed 2026-06-21).
- **Canonical reference syntax** — every cross-artifact citation is a parseable token
  (`<constitution>#<article>`, `policy:<name>`, `persona:<name>`, and `ref:confidence#<key>`
  for the confidence ladder — added 2026-06-21, Candidate 6) followed by a prose gloss
  after `—`. Lives in YAML fields (`constitutional_basis`, `references`, threshold values)
  and in a new `validates:` frontmatter block on behavioral tests (making persona↔test
  bidirectional, not filename-only). The manifest harvests these into resolvable edges;
  dangling ones fail CI. The confidence rungs are single-sourced in
  `logic/confidence-thresholds.yaml`; policies reference a rung
  (`proceed_autonomously: ref:confidence#autonomous`) instead of restating `0.9`.
- **Schema-as-single-source validation** — structural rules live once in `*.schema.json`,
  read by two thin adapters: `jsonschema` (Python) and `Test-Json -Schema` (PowerShell).
  Kills the halt-marker and digest duplication; `persona.schema.json` finally gets used.
  *Relational* checks (citations resolve) fold into the manifest; *temporal* checks
  (`expires_at` in the future, freshness) stay at point-of-use.
- **`Get-DomainGateState`** — a dot-sourced PowerShell deep module that reads loop state
  once (HALT-ALL + schema-validate + expiry, protected paths, lock age, git dirty) and
  returns *facts*. `dev-process-overseer.ps1` and `supervised-loop-preflight.ps1` become
  thin deciders that weigh those facts themselves.
- **Precedence declaration** — `precedence.yaml` authors the constitutional hierarchy once;
  the manifest validates that each constitution's `Precedence:` / `Subordinate to:` header
  *agrees* with it. Makes the append-only + precedence [Architecture invariant](#architecture-invariant)
  machine-checkable without generating the headers' human rationale.

## Architecture seams (designed + built 2026-06-21, Candidate 1)

- **`DigestState`** — `.claude/hooks/DigestState.psm1`, a dot-sourced PowerShell deep
  module mirroring [`Get-DomainGateState`](#architecture-seams-designed-2026-06-20-via-improve-codebase-architecture-built-2026-06-21-pr-357).
  The eight session-digest hooks were each re-deriving the same primitives — the
  `state/digests` path, YAML escaping, git facts, counter I/O, and a late-bound
  validation call. Those now live here once, behind a small interface
  (`Write-Digest`/`Get-DigestPaths`/`Format-Yaml`/`Get-RepoFacts`/`{Get,Step,Reset}-Counter`/`Test-Digest`);
  the hooks became thin *deciders*. `Write-Digest -Kind digest|rationale` resolves
  paths, fetches/accepts repo facts, rotates `latest`→`archive`, **validates the
  constructed object against the schema** (`docs/contracts/{digest,pr-rationale}-schema.json`),
  writes, and auto-resets counters by trigger. `Test-Digest` replaced
  `digest-validate.ps1`'s hand-coded rules with a schema read (ADR-0003). First
  unit-testable seam in the hook layer (`tests/powershell/DigestState.Tests.ps1`, Pester).

## Architecture seams (designed + built 2026-06-21, Candidate 2)

- **Ecosystem facts action** — `.github/actions/ecosystem`, a composite action that is
  the single parse point for the GuitarAlchemist ecosystem's GitHub plumbing. It reads
  `schemas/capability-registry.json` (new `github` block: `repo_node_id`,
  `discussion_categories` name→id) and `governance-manifest.json` (`.counts`) once and
  exposes them as step outputs (`repo_node_id`, `cat_*`, `count_*`, `consumer_repos` from
  `.repos | keys`). Workflows stop restating the repo id / category ids (was duplicated
  ~22× across 9 files) and stop re-deriving counts with `ls | wc -l` (was ~4 workflows) —
  the latter is **harvest, don't declare** (ADR-0002) finally reaching the CI surface.
  Every discussion-creating workflow now resolves ids from the action and posts via
  `post_discussion.sh` (Candidate 3).

## Architecture seams (designed + built 2026-06-21, Candidate 3)

- **`llm_call.sh` / `post_discussion.sh`** — two deep, unit-tested scripts under
  `.github/scripts/` that replace inline `run:` ceremony duplicated across workflows.
  `llm_call.sh <provider> <prompt>` hides per-provider auth/payload/extraction
  (`.content[0].text` vs `.candidates[]..` vs `.choices[]..`) behind one interface
  with an explicit error contract (stdout=text · stderr=diagnostic · exit 0/2/3/4).
  `post_discussion.sh` owns the createDiscussion GraphQL and **raises on failure**
  instead of the `|| echo "Failed"` swallow (9 workflows). The network call is the single
  overridable function (`_http_post` / `_graphql`); bats tests (`tests/bats/`)
  override it with fixtures so the logic is tested without a live API — the first
  unit-tested seam for the shell layer (`.github/workflows/script-tests.yml`:
  bats + shellcheck). `post_discussion.sh` takes the category id as an arg, composing
  with the ecosystem action's `cat_*` outputs.

## Architecture seams (designed + built 2026-06-25 via `/improve-codebase-architecture`, Python emitter kit)

- **`demerzel_kit`** — `scripts/demerzel_kit.py`, the Python sibling of
  `DigestState.psm1` and the `llm_call.sh` shell seams: one small interface the
  `scripts/` **emitters** share, owning the four primitives each was re-deriving
  (`now_iso` — copy-pasted ×7; `atomic_write` — ×6; schema `validate`; and the `gh`
  subprocess wrapper — ×3, with three different error contracts). `write_artifact(
  path, data, schema=…)` validates **then** atomic-writes, so an invalid governance
  artifact never reaches disk for a read-time consumer to choke on — the gap that
  let `council_emit._write_verdict` write unvalidated verdicts despite its docstring.
  `gh_json` / `gh_text` take an injectable `run=` seam, which is what finally makes
  the emitters testable through their interface: `council_emit.convene()` now runs
  end-to-end offline in `scripts/test_council_emit.py`, the test the un-seamed `gh`
  calls used to make impossible. `validate` lazily imports `jsonschema` and degrades
  when absent (matching `demerzel_halt`), so an emitter still runs stdlib-only. Wired
  into CI via `governance-validate.yml` (`python -m unittest discover -s scripts`).
  `council_emit` is the first migrated emitter (tracer bullet); the other six
  (`qa_tribunal_emit`, `run_afk_cycle`, `apply_ml_feedback`, `compliance_report`,
  `run_ml_feedback_cycle`, `demerzel_halt`) follow. Does **not** auto-stamp a
  timestamp — domain artifacts carry their own (`timestamp`, `halted_at`) and several
  schemas set `additionalProperties: false`, so callers stamp with `now_iso()`.

## Conventions

This file **is** the authority on the constitutional hierarchy and the domain
glossary; `CLAUDE.md` points here for both. For validation and contribution rules
see `CONTRIBUTING.md`; for cross-repo contract handling see
`docs/architecture/cross-repo-contracts.md`. `CLAUDE.md` is a short index, not a
reference — don't send readers there for detail.
