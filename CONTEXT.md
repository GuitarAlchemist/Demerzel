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
  4-value subset.)
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

## Conventions

See `CLAUDE.md` / `AGENTS.md` for authoritative validation rules, the constitutional
hierarchy, and cross-repo contract handling.
