# Demerzel — AI Governance Framework

Governance framework for AI agents: constitutions, personas, hexavalent logic, alignment policies, and behavioral tests. Named after R. Daneel Olivaw from Asimov's Foundation. Consumed by **ix**, **tars**, **ga** via the Galactic Protocol.

Full directory listing: see `README.md`. Source of truth for Asimov laws, Default constitution articles, and all 45 policies: `constitutions/` and `policies/`.

## Key Principle

The Asimov constitution always takes precedence. Zeroth Law (do not harm humanity) overrides everything. Demerzel enforces governance through her constitutional mandate.

## Hexavalent Logic (T/P/U/D/F/C)

- **T** True — verified with evidence
- **P** Probable — evidence leans true, not yet verified
- **U** Unknown — insufficient evidence, triggers investigation
- **D** Doubtful — evidence leans false, not yet refuted
- **F** False — refuted with evidence
- **C** Contradictory — conflicting evidence, triggers escalation

## Confidence Thresholds

`≥0.9` autonomous · `≥0.7` with note · `≥0.5` ask confirmation · `≥0.3` escalate · `<0.3` do not act.

## Validation

- Persona files must conform to `schemas/persona.schema.json`: `name` (kebab-case), `version` (semver), `description` (≤200 chars), required `role`, `capabilities`, `constraints`, `voice`, `affordances`, `goal_directedness`.
- Use schemas in `schemas/` to validate new artifacts.

## Contributing Rules

- Every persona needs a behavioral test in `tests/behavioral/`.
- Constitutions are **append-only** — removals need explicit justification.
- Source material in `sources/` must be transformed into canonical formats, never copied raw.
- All policies include versioning with explicit rationale.

## Cross-repo contracts

Demerzel orchestrates cycles across sibling repos via JSON-on-disk contracts (the canonical handoff pattern across the GuitarAlchemist ecosystem). Sibling clones are typically peers under the same parent directory:

- **ga** (`../ga/`, .NET / C# / F# / React, music theory + RAG): defines `docs/contracts/2026-05-02-qa-verdict.contract.md` (schema: `docs/contracts/qa-verdict.schema.json`) — the QA Architect verdict shape Demerzel emits via `pipelines/qa-architect-cycle.ixql`. Also owns `docs/contracts/2026-05-02-optick-sae-artifact.contract.md` consumed by `qa_score_quality_drift`.
- **ix** (`../ix/`, Rust ML algorithms): the `ix-optick-sae` crate is intended to produce `state/voicings/optick.index` and SAE artifacts under `state/quality/optick-sae/` for cross-cycle quality drift evidence. **Not yet emitted as of 2026-06-21** — the crate exists but these runtime artifacts have not been generated, so `qa_score_quality_drift` has no live input. Treat this seam as declared-but-unfulfilled: any consumer must degrade explicitly when the artifacts are absent.
- **tars** (`../tars/`, F# grammar + metacognition): cross-model theory validator.

Locked-field changes need cross-repo coordination; the Galactic Protocol and `governance/demerzel/schemas/capability-registry.json` are Demerzel's own equivalents. The `links.supersedes` pattern in `optick-sae-artifact` is how to introduce a non-breaking baseline shift without freezing a schema. Contracts marked v0.1.x in their headers remain drafts until their Phase 4 freeze milestones.

## Karpathy 4 Rules — AI coding discipline

These rules apply to every Claude proposal that touches code:

1. **Think before coding.** State your interpretation of the request + assumptions; ask one clarifying question if anything is ambiguous; wait for confirmation before writing code.
2. **Simplicity first.** Write minimum code that solves the exact problem. No speculative features, no future-proofing.
3. **Surgical changes only.** Only modify code directly related to the request. Don't refactor adjacent code, don't fix unrelated style issues.
4. **Goal-driven execution.** Transform every task into verifiable success criteria. Loop until each is demonstrably met. "Task completed" ≠ "goal achieved." Use native `/goal <condition>` (Claude Code v2.1.139+) to mechanize this — Claude keeps working across turns until an evaluator confirms the condition holds. `/digest`'s `success_criteria` field is the **declared** form; `/goal` is the **operational** driver.

Self-improvement reflex: when the user corrects you, invoke `/correct` so the rule lands in this file's **Session-learned rules** section — Cherny's "most important loop" from the 2026 Sequoia talk.

## Session continuity (Cherny pattern)

- `/digest` — captures meaningful session state (cursor, in-flight, hypotheses, success criteria) to `state/digests/latest.md`. Auto-fallback via `.claude/hooks/precompact-digest.ps1`; auto-injected on next session via `.claude/hooks/sessionstart-digest.ps1`. See `.claude/skills/digest/SKILL.md`.
- `/learnings` — captures surprises (non-obvious facts worth grep-finding later) into `docs/solutions/<category>/<date>-<topic>.md`.
- `/correct` — turns user corrections into permanent rules in this CLAUDE.md.

The hooks are validated in CI by `.github/workflows/karpathy-cherny-discipline.yml`.

## Session-learned rules

_Appended by `/correct` when the user corrects an approach. Persists across sessions._

(none yet)

## Tracer-bullets + vertical slices (aihero delta, 2026-06-14)

Adopted ecosystem-wide from aihero.dev. Counters AI's "build the whole thing at
once" failure mode:

- **Tracer-bullet first.** For any non-trivial feature, build the smallest
  **end-to-end** slice that touches *every* layer, test it, get feedback, then
  expand — never build layers in isolation. "Context-window constraints make the
  discipline non-negotiable."
- **Vertical, not horizontal, decomposition.** Each task/PR is a thin slice
  cutting through all integration layers (surfacing unknowns early), not a
  horizontal layer.

Prefer existing planning/review/quality tooling over adding new skills — aihero's
`/grill-me`, `/to-prd`, `/to-issues`, `/tdd`, `/improve-codebase-architecture`
are already covered by this ecosystem's brainstorming, planning-doc, test, and
structural-quality machinery. (The `/teach` skill IS adopted — see
`.claude/skills/teach`.)

## Agent skills

Per-repo config for the installed aihero/mattpocock engineering skills (`grill-with-docs`, `grill-me`, `to-prd`, `to-issues`, `tdd`, `improve-codebase-architecture`, `teach`), installed project-scoped into `.claude/skills/` via `npx skills@latest add mattpocock/skills --copy` (MIT; Socket/Snyk clean). Configured 2026-06-14 via `/setup-matt-pocock-skills`.

### Issue tracker

GitHub Issues on `GuitarAlchemist/Demerzel`, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical defaults (`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the repo root. `/grill-with-docs` grows them lazily. See `docs/agents/domain.md`.

## AI-coding vocabulary (shared ecosystem reference)

<https://github.com/mattpocock/dictionary-of-ai-coding> — the plain-English
glossary behind the aihero methodology adopted across the GuitarAlchemist
ecosystem (smart-zone, tracer-bullets, context windows, handoffs, failure
modes). Referenced, not vendored, so it tracks upstream.
