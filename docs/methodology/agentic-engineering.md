# Agentic Engineering — the harness is the work

> A read-on-demand reference, **not** an always-loaded instruction block. Distilled from Matt
> Pocock's "Agentic Engineering Workflow" (aihero.dev) + Ousterhout's *A Philosophy of Software
> Design*, and mapped to **this repo's** existing machinery. Read it when you're deciding *how* to
> direct AI on a non-trivial change — not on every turn. (Mirrors `ga/docs/methodology/agentic-engineering.md`,
> adapted to Demerzel.)

## The one idea

**Optimise the harness, not the model.** The model is the engine; the *harness* — prompts, skills,
the codebase itself, the environment the agent runs in — is roughly half the system and the half you
fully control. The load-bearing consequence:

> *"How do you optimise token spend? Have a codebase that's easier to make changes in."*

Demerzel is the ecosystem's **governance harness made explicit**: the constitutions, the 45 versioned
policies, the hexavalent logic (T/P/U/D/F/C), the personas, and the IXQL pipelines *are* the rules the
agents run inside — governance shapes behaviour without living in runtime code. A clearer, lower-
duplication governance corpus lets a cheaper model behave correctly with fewer tokens.

## Strategic over tactical

AI ate **tactical** programming (writing syntax, chasing bugs, making commits) — it's cheaper and
faster than you at it. Your leverage is **strategic** programming (Ousterhout):

- **Design the hard parts up front.** Decide the consequential things before delegating — for Demerzel,
  that's constitutional/policy changes (one-way doors needing sign-off) and the Galactic Protocol
  message contracts.
- **Scope tasks tightly.** A well-scoped task is one an AFK agent can finish with no further context.
- **Own the interfaces / seams between modules.** This is where bugs and rework concentrate.
- **Keep just-enough docs that point agents to the right place** — not exhaustive, navigational.

"Your skills are the ceiling on what AI can do." Delegate the tactical; keep the strategic mindset.

## DX ≈ AX

Agent experience ≈ developer experience. What makes a corpus pleasant for a senior human makes it
tractable for an agent: **deep modules** (a lot of behaviour behind a small interface), **low
duplication**, **clear seams**, **guardrails**. The `/improve-codebase-architecture` vocabulary
(module / interface / depth / seam / **deletion test**) is the shared language for this across the
ecosystem (it ships with the aihero skill set being wired in via `setup-matt-pocock-skills`). Real deep
seams already in Demerzel: the **constitutional hierarchy** (`constitutions/{asimov,default,epistemic}.constitution.md`
+ `harm-taxonomy.md` — the Zeroth-Law-overrides-all interface), the **policy engine** (`policies/*.yaml`,
e.g. `alignment-policy.yaml` with the confidence-threshold ladder), and the **Galactic Protocol + IXQL**
(`contracts/galactic-protocol.md` + `pipelines/*.ixql` — one DSL behind all cross-repo orchestration).
The domain backbone is `context-map.yaml` (the Tier 0–3 artifact loader); architectural decisions live
in `docs/superpowers/{plans,specs}/` and `docs/governance/` rather than a `docs/adr/`.

## Procedures vs abilities (and context hygiene)

- **Procedure** — a skill *you* invoke to stay in the driver's seat. Demerzel ships ~60 governance
  skills (`/demerzel-*`, `/seldon-*`); the aihero procedures (`/grill-me`, `/to-prd`, `/to-issues`,
  `/improve-codebase-architecture`) install via `setup-matt-pocock-skills` (the branch this doc may land
  alongside). Prefer procedures; keep the thinking in the human.
- **Ability** — a skill the *model* self-invokes. Every ability leaks its description into the context
  window. With 60 skills, this is the live risk here — mark deliberate procedures
  `disable-model-invocation: true` and lean on `context-map.yaml`'s tiered loading.

Matt's blank-slate test: periodically strip skills / MCP / CLAUDE.md back toward nothing, watch what
the agent does unaided, then **layer back only the procedures you deliberately choose**. Demerzel's
always-loaded surface is already lean (`CLAUDE.md` ~85 lines, `AGENTS.md` ~72) — the discipline is to
keep skill descriptions from leaking; that's what `context-map.yaml` tiers are for.

## Queues, not loops

The unit of AFK work is a **queue** of well-scoped tasks, not an infinite prompt loop. Tasks flow
**triage → explore → implement → review → merge**, pulled off by labelled agents. Demerzel already
speaks this: GitHub Issues + canonical triage labels (see
[docs/agents/triage-labels.md](../agents/triage-labels.md)), the `/demerzel drive` 8-phase autonomous
cycle (WAKE → RECON → PLAN → EXECUTE → VERIFY → COMPOUND → PERSIST → SLEEP), `demerzel-team` dispatch,
and the cross-repo `~/.demerzel/HALT-ALL` marker that gates every loop. The Ralph Loop (`ga-ralph`,
bounded 15 iterations, boundary-only governance) is the canonical *bounded* loop. Keep
**human-in-the-loop checkpoints**, but push them as far toward the final output as the work safely allows.

## Build self-improving systems

When a model finds a deep bug, the lesson is **not** "the model is great" — it's *"I should have a
system that catches this."* Demerzel *is* a self-improving system: `/demerzel quality-trend` (nightly,
zero-judgment per-artifact deltas → `state/quality-trend/*.jsonl`) feeds `/demerzel compound` (scan
`state/evolution/` → detect promotions/demotions → propose self-improvements). Crucially, both run a
**liveness check first** — measuring freshness before reading, the explicit guard against the
green-but-dead trap (a scheduler that's green for weeks while producing nothing). CI backs this:
`demerzel-self-improvement.yml`, `demerzel-autofix.yml`, `governance-validate.yml`,
`karpathy-cherny-discipline.yml`. Extend these loops rather than one-shotting fixes.

## Make review seamless

The bottleneck is human review, so spend the harness on making review *fast*. Demerzel is where the
ecosystem's review machinery *lives*: `demerzel-cross-review` enforces the **reviewer ≠ author**
invariant (Gemini→Claude, Claude→Codex, …, author detected from PR label / `Model-Author:` trailer),
`cross-model-review.yml` automates it, and the **QA Tribunal** (`qa-tribunal.yml` →
`state/quality/verdicts/<repo>/<pr>/*.json`) renders multi-LLM verdicts. `/demerzel-consult` pulls
second opinions. You stay the gate on security and on "did the system do a good job," but you make that
gate one click. (Caveat from this ecosystem: multi-LLM judge panels confirm well but catch invalidity
poorly — use them as a *fail-closed asymmetric* gate, not a truth oracle.)

## You own the product

AI is weak at original ideas and at deciding *what* to build. Choose the features; ask "what can I
**remove**, how do I make this **simpler**." The classic product-design fundamentals still hold — AI
just implements them faster.

## The two action steps Matt actually recommends

1. **Strip to a blank slate, then layer deliberately.** Remove the bloat; re-add only procedures you
   choose and can customise.
2. **Move work AFK.** Scope a task tightly, hand it to a sandboxed agent (a git worktree off the default
   branch), review the result. Two of you, then three, then five — then you review.

---

*Pointer, not gospel: this doc is read when you're deciding how to direct a non-trivial change. It is
deliberately **not** wired into the always-loaded instruction set — that would contradict its own
context-hygiene advice.*
