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
  (`<constitution>#<article>`, `policy:<name>`, `persona:<name>`) followed by a prose gloss
  after `—`. Lives in YAML fields (`constitutional_basis`, `references`) and in a new
  `validates:` frontmatter block on behavioral tests (making persona↔test bidirectional,
  not filename-only). The manifest harvests these into resolvable edges; dangling ones fail CI.
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

## Conventions

See `CLAUDE.md` / `AGENTS.md` for authoritative validation rules, the constitutional
hierarchy, and cross-repo contract handling.
