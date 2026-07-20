# Agentic Engineering — 2026-07 delta (Matt Pocock channel sweep)

> Companion to [agentic-engineering.md](agentic-engineering.md), which distilled Pocock's *older*
> "Agentic Engineering Workflow" talk. This doc captures only what is **net-new, sharper, or in
> tension** with that baseline, harvested from the **31 AI-coding videos** he published *after* it
> (`@mattpocockuk`, swept 2026-07-19). Same posture: **agree = keep, diverge = adjust.** Read
> on-demand when deciding *how* to direct a non-trivial change — not on every turn.
>
> Each item is tagged `[NEW]` / `[SHARPENS]` / `[TENSION]` and mapped to concrete Demerzel machinery.
> Sources are paraphrased from the named videos; raw transcripts were captured to scratchpad and
> **deliberately not vendored** (our `sources/` rule: transform, never copy raw).

---

## 0. The one load-bearing tension: CLAUDE.md is doing too much

Three videos — *"Never Run claude /init"*, *"How to force Claude Code to use the right CLI (don't use
CLAUDE.md)"*, *"Claude Code tried to improve /init"* — converge on a doctrine that **directly
tensions this repo's CLAUDE.md-centric design**. It deserves its own section because it is the single
highest-leverage change on the table, and it is a judgment call for the human, not an auto-adopt.

**The instruction budget is real and separate from the token budget.** Pocock's claim: an agent
degrades after roughly **300–500 instructions** regardless of how cheap those tokens are — the count
matters, not the bytes. The system prompt (CLAUDE.md + resident MCP tool descriptions) is the *one*
context cost you cannot flex: it is hardwired at session start and shrinks the room left for explore /
implement / test.

**His decisive admission test — does a line earn its place in CLAUDE.md?**

1. Is it **trivially discoverable** from code/config, or will the **explore phase** surface it? → delete.
2. Does it **name specific files** or describe architecture that will **rot** when implementation
   changes? → delete (a doc-vs-code conflict is worse than no doc).
3. Is it **already enforced** by a hook / CI / schema? → delete (redundant).
4. What survives: **non-discoverable, durable** facts (his entire global CLAUDE.md is one line —
   *"You are on WSL on Windows"*) and genuinely non-obvious steering.

**Where the deleted content goes instead:**

- **Enforceable prohibitions → deterministic `PreToolUse` hooks.** A hook fires before a tool call and
  can *block* it: a `.sh` matched to the `Bash` tool that greps the command, prints a steer message,
  and `exit 2` (exit 2 = block **and** feed the message back to the model, which self-corrects). This
  *prevents*; a CLAUDE.md "never run git push" only *lowers the probability* while still spending
  budget. Negative instructions are the worst value: cost with no guarantee.
- **Style/standards rules → linters / validators** the agent runs (feedback loop), not prose. "Lint
  the agent into correctness."
- **Steering knowledge → progressively-disclosed skills**, discovered just-in-time, not resident.

**Mapping to Demerzel — measured, not assumed.** An earlier draft asserted "our `CLAUDE.md` is large by
this standard." That was wrong, and it was the load-bearing premise for the riskiest adoption item.
Measured: **124 lines / 1,150 words**, with the five `.claude/rules/*.md` files totalling 6 lines.
Against the 300–500-instruction budget cited above, that is roughly an order of magnitude *under* the
threshold. `docs/methodology/agentic-engineering.md` independently reached the same conclusion
("already lean"), and this doc had contradicted its own companion without noticing.

The real finding is narrower and duller: the surface is **duplicated**, not oversized — several rules
are restated 2–4× across `CLAUDE.md`, `AGENTS.md`, and `.claude/rules/`. De-duplication is worth doing
on its own merits (#775) and does not need the instruction-budget argument to justify it.

A related caution, learned the hard way in #775: *"a hook can enforce this prohibition more reliably
than prose"* is only true once the hook demonstrably works. Demoting prose in anticipation of
enforcement that doesn't exist yet is strictly worse than either. Counter-argument specific to us:
Demerzel is a **governance** repo whose CLAUDE.md is partly a *constitutional mandate*, not just
tactical steering — some of it is deliberately load-bearing context an agent must not have to
rediscover. **This is a one-way-ish door; it needs the maintainer's call, not an autonomous rewrite.**
See the adoption table (§7) for the surgical version.

---

## 1. The named end-to-end flow, and the skill catalog has moved on

Pocock's `mattpocock/skills` is now an **ordered, named flow** walked down in one unbroken context
window, not a bag of independent skills.

**Correction — check the filesystem before declaring a gap.** An earlier draft claimed our installed
set was "one generation behind" and filed four adoption items to build skills that already exist.
Measured against `~/.claude/skills/`: **`implement`, `handoff`, `triage`, `prototype`, and `review`
are all installed and live**, alongside `git-guardrails-claude-code` and `ubiquitous-language`.
`review`'s own description is the two-axis parallel-sub-agent design this doc proposed as net-new.

The accurate finding is a one-liner: the **project-scoped** copy under `.claude/skills/` is stale
while the newer generation sits at **user scope**. The fix is to sync, not to rebuild. Acting on the
original table would have duplicated five working skills — in a document arguing for a leaner surface.
**Only `wayfinder` is genuinely absent.**

**The current flow:**

```
setup (one-time)  →  grill-with-docs | wayfinder   →  [to-spec → to-tickets]  →  implement  →  code-review  →  commit
                          ↕ (on a high-fidelity Q)        (skippable if it fits one context window)   (auto-invoked)
                     handoff → prototype → handoff back
        ── triage runs continuously as the queue layer over all of it ──
```

- `[NEW]` **`implement`** — a deliberately *tiny* skill ("implement the spec/tickets; TDD at pre-agreed
  seams; type-check + targeted tests continuously, full suite once; then `code-review`; then commit").
  It exists only to name the spine. **`~/.claude/skills/implement/` already exists** (`disable-model-invocation: true`) and is verbatim
  this skill. Nothing to build; sync the project-scoped copy if it matters.
- `[NEW]` **`wayfinder`** — his new default for work that is *big AND foggy* (route not yet visible).
  Charts a **map as a GitHub issue with typed, blocking sub-issues** (research / grilling / prototype /
  task); you close them one at a time until the route clears, then `to-spec`. **We have no
  map-as-issue-tree planning primitive** — strong fit for cross-repo cycles (and it is what our Planner
  MVP #529 execution-graph should *feed*).
- `[NEW]` **`handoff`** — compress current context into a **disposable temp-file** (OS temp, *not* the
  repo) for a fresh/other agent (even a different harness) to pick up: read-before-write, reference
  artifacts by path (don't duplicate), redact secrets, include a *suggested-skills* section, take the
  next focus as an argument. **Distinct from our `/digest`**: digest is *persistent session state*;
  handoff is *disposable, task-scoped, cross-harness*. Don't conflate — and don't let handoff files rot
  in `state/`.
- `[NEW]` **`prototype`** — throwaway spikes for "unknown unknowns you can only see in code." Two modes:
  UI (several radically-different variants + a floating toggle, human picks by taste) and **logic** (a
  tiny interactive terminal app that drives a **state machine** through hard cases). The logic mode maps
  cleanly onto validating a **hexavalent policy's state transitions** before writing it.
- `[NEW]` **`triage`** = a **state machine encoded in labels**: exactly one category role (bug/enhancement)
  + one state role (`needs-triage`/`needs-info`/`ready-for-agent`/`ready-for-human`/`wont-fix`), plus a
  **`.out-of-scope/` ADR directory** the agent reads to auto-close declared non-goals. "Managing AFK
  agents is essentially queue management." We have triage *labels* (`docs/agents/triage-labels.md`) but
  no enforced *one-category+one-state* invariant and no machine-readable non-goals set.
- `[SHARPENS]` **`research`** — a *background* agent against primary sources, writing to the repo's
  existing note convention. Parallels `seldon-research`; the delta is "background so you keep working"
  + "match existing convention" (anti-sprawl).
- `[SHARPENS]` **`code-review`** now runs **two parallel sub-agents on distinct axes — Standards and
  Spec** — in fresh context (an author-agent reviews its own code poorly), armed with **named Fowler
  refactoring smells** (mysterious name, duplicated code, feature envy, data clumps, primitive
  obsession, repeated switches, divergent change, speculative generality, message chains) so the
  reviewer *names the smell back* and fixes it. Refactoring moved *out of the TDD loop into review*.
- `[TENSION/rename]` `to-prd` → **`to-spec`** (a spec is broader than a PRD: technical/non-technical/blend
  = the *destination*); `to-issues` → **`to-tickets`** (the *journey*; tracker-agnostic). At minimum
  adopt the **spec-vs-tickets vocabulary**; renaming our skills is optional ecosystem parity.
- `[SHARPENS]` `grill-me` (stateless, no codebase) vs `grill-with-docs` (stateful; grill + a `CONTEXT.md`
  **ubiquitous-language glossary** (DDD) + ADRs, updated inline). **Stateless vs stateful is the core
  skill-design axis** — a useful lens for auditing which Demerzel skills *should* persist (belief-state
  writers) vs stay stateless.
- `[SHARPENS]` `setup` picks the issue tracker (**GitHub / local-markdown / Jira / Linear** — pluggable,
  not GitHub-locked) and writes `CONTEXT.md` + ADR + triage docs. Our machinery hardcodes GitHub Issues;
  a local-markdown fallback matters for repos/sessions without `gh` auth.
- `[SHARPENS]` **Skill descriptions are a budget.** His 38 skills cost ~660 always-loaded tokens by being
  terse and user-invoked. Model-only skills set **`user_invocable: false`** to stay out of the human
  menu *and* out of description leakage. **Audit our 69 project skills** (measured; +35 at user scope) via `demerzel-context-budget`.

## 2. Loop & AFK mechanics (Ralph, sandbox, worktrees)

- `[SHARPENS]` **Ralph technique, concretely:** a bash `for` loop (max-iterations + `set -e`), each
  iteration a fresh context, driven by two on-disk files — **`prd.json`** (array of small stories each
  with a `passes: true/false` flag = PRD + to-do list) and an **append-only `progress.txt`** (the
  cross-iteration memory). Prompt: pick the *highest-priority unpassed* item → work **only that one** →
  set `passes:true` → **append** progress → **commit** → emit a grep-able **completion sentinel** when
  done. Our `supervised-loop`/`ga-ralph` should adopt this shape verbatim: passes-flagged checklist,
  append-only log, one-slice-per-iteration, commit-per-cycle (queryable memory), sentinel exit.
- `[SHARPENS]` **One feature per iteration** and **evenly-sized tasks** are the central discipline — an
  oversized task "swallows" a context window; an undersized one pays full agent-spinup cost. Size to
  "one agent boot ≈ one meaningful slice."
- `[SHARPENS]` **Agents fake completion.** Claude marks work done without real testing unless explicitly
  told to **verify end-to-end as a human user** (browser automation). Keep slices small *precisely* to
  leave context budget for that verification. (Matches our render-verification / harness-before-harvest
  memories and `scripts/verify.ps1` oracle.)
- `[SHARPENS]` **AFK safety = sandbox, not Yolo.** His `@ai-hero/sandcastle` runs each agent in a
  **Docker container** (the sandbox *is* the permission boundary) rather than
  `--dangerously-skip-permissions`, which risks destructive / data-exfil behavior. Matches our
  AFK-harness (Podman, PR #380). Factory shape: **Planner → parallel Implementers (branch-per-issue) →
  Reviewer (a *different* model) → Merger** (a senior model that resolves conflicts, merges, closes the
  issue). The **dedicated Merger agent** is a piece we don't model explicitly; cross-model review is
  trivially swappable when the harness is **agent-agnostic** (Pocock-delta baseline, vindicated).
- `[SHARPENS]` **Worktrees, native:** `claude --worktree` isolates each agent under
  `.claude/worktrees/<name>` on its own branch. **Gotcha:** the branch sources from *main*, so an
  unqualified push can land on main — fix with an explicit `git push origin <branch>` **and a
  `PreToolUse` push-guard hook** that blocks the push and prints the exact command for the human. This
  repo had multiple accidental-push-to-master near-misses this era → the push-guard is a concrete,
  low-risk win.

## 3. Context & token economics (mechanical rules we can codify)

- `[NEW]` **Lost-in-the-middle:** attention prioritizes the **start and end**; mid-context is
  deprioritized and *degrades* as the window fills ("context rot" — bigger windows are not better).
  **Ordering rule:** put governance invariants (constitution precedence, HALT-honoring, thresholds) at
  the **front** of any assembled prompt and the **task/success-criteria** at the **end**; never bury a
  hard rule in the middle.
- `[NEW]` **`clear` should be the default between tasks; `compact` is the exception** (it costs an LLM
  call + ~a minute and preserves only "vibes"). Our `/digest` is compaction-done-deliberately →
  doctrine: prefer a **fresh session re-primed from digest** over in-session compaction.
- `[SHARPENS]` **Agent vs Workflow — "who owns the stop?"** Agent = LLM decides when to stop (new info via
  tool calls); Workflow = *code* decides (predetermined path). **Repeated, known-path work must be a
  deterministic workflow — paying an LLM per run is a smell.** Stamp every Demerzel loop/pipeline with a
  "stop-owner" field: our trigger-queue + scripts = *workflow*; `demerzel-drive`/`supervised-loop` =
  *agent* and must declare an explicit `max_steps` (our HALT marker + rate caps generalized).
- `[NEW]` **Budget in provider-native tokens.** Each provider tokenizes differently (same prompt ≠ same
  count; ~2–3× spread), input vs output priced separately, and you can hit the ceiling *mid-generation*
  (silent truncation our freshness guards won't catch). Our **budget gate must reserve/charge in
  per-provider tokens**, not a normalized byte/word estimate, and add **output** headroom checks.
- `[NEW]` **Rare tokens cost more** — bespoke DSLs (our `.ixql` pipelines, custom grammar) are the
  "Haskell case": they tokenize expensively *and* run off-distribution (worse model performance).
  Prefer canonical JSON-on-disk contracts over novel notation where a model is in the loop.
- `[SHARPENS]` **MCP is the #1 stealth context-bloater** ("a third system prompt"). Treat adding any MCP
  server as an **admission gate**: measure its tool-schema token cost *before* adding. The large deferred-MCP roster visible in a
  *session* (godot ~150, ga ~90) is the risk — note this repo's `.mcp.json` declares only `ga`, so
  that surface is user/session-level, not repo-level; **ToolSearch/deferred-loading is the
  correct mitigation** — keep it. Also: **trim tool output at the boundary** (paginate/summarize
  server-side) and always give tools **descriptions** (an undescribed tool is an ungoverned capability).

## 4. Cost reality — why local-seat-first is now non-optional

> **Sourcing caveat — read before acting on any number below.** Everything in this section is a
> paraphrase of one video and **nothing here is independently verified**. The dollar figures, the
> "non-rolling" mechanic, and the ~June-2026 date are *as stated in the source*, not confirmed against
> Anthropic's published pricing — treat all of them as hearsay, not just the multiplier at the end.
> The `sources/` rule forbids vendoring raw captions; it does not forbid citations, and their absence
> here is a defect of this doc, not a constraint.
>
> **Do not let this section justify engineering.** The `token_multiplier` work it motivated (P5) was
> built and then withdrawn (#772) — it turned out to be attached to the token cap, which for these
> providers costs nothing, while leaving cost untouched. Confirm the pricing model directly before
> anything here becomes code.

*"Anthropic's dedicated monthly credit is actually a huge cut"* is the load-bearing video for the
budget gate.

- `[NEW]` From ~June 2026, paid Claude plans fund **all programmatic/AFK usage** (Agent SDK, `claude -p`,
  Claude Code GitHub Actions, 3rd-party apps) from a **separate monthly credit ≈ the plan price** (Pro
  $20 / Max-5x $100 / Max-20x $200), **non-rolling**, that **pauses until reset** when exhausted.
  Human-in-the-loop usage keeps the old (subsidized) budget.
- `[NEW]` It is a **cut, not a bonus**: subscriptions are ~10× cheaper than API, so capping AFK to a
  $100–200 credit that spends at API-equivalent rates is a **~5–10× reduction** in AFK capacity for heavy
  users (numbers estimated / Anthropic-opaque — hold skeptically).
- **Design confirmations for our gate:** treat metered-AFK as a **premium, rationed** provider; **exhaust
  local/free seats first** (exactly the fail-closed, local-seat-first design); add a **monthly-reset
  accounting boundary** and a **separate AFK ledger** from interactive spend.
- `[TENSION]` Pocock's own move is to shift AFK **off** Claude Code to Codex (no AFK/human split *yet*).
  The durable lesson is the **abstraction** (a budget-gated, **provider-portable** router), not the
  vendor arbitrage — don't hardcode Anthropic assumptions into the seat model.

## 5. Anti-hallucination & review sharpenings

- `[SHARPENS]` **Intrinsic vs extrinsic hallucination:** answers grounded in *in-context* info are far
  more reliable than those guessed from training data — **always feed the info first**. But grounding is
  necessary, *not sufficient*: models sometimes contradict context even when provided (the Air Canada
  case) → for high-stakes governance verdicts, a human/second-model must actually read the source.
  Confidence-emitting skills should record **intrinsic vs extrinsic** and penalize extrinsic (maps to
  hexavalent U/D and the confidence-calibration belief work).
- `[NEW]` **Reward calibrated abstention.** LLMs hallucinate partly because evals reward guessing over
  "I don't know." Governance evaluators should **not** penalize a triggered `U`/Unknown vs a confident
  wrong answer.
- `[SHARPENS]` **Two concrete reflexes** that beat generic "verify before guessing": (1) *"Use your search
  tool"* forces extrinsic→intrinsic; (2) **a confident *negative* ("no tests exist", "not found") is an
  investigation trigger, not an answer** — "look harder." Bake both into `demerzel-self-diagnostic` /
  the skeptical-auditor pairing. (Also: fabricated package names are a supply-chain surface —
  *slopsquatting* — verify a dependency exists before install.)
- `[SHARPENS]` **Red→Green is an anti-faking mechanism**, not just quality: seeing a test go red *then*
  green (test unchanged) lets a reviewer skip reading test bodies. A green with **no prior red is
  suspect** — our `tdd` skill should emit the red→green transition as auditable evidence, and enforce
  **one test at a time** (forbid dumping 90 tests as a horizontal layer → "crap tests"). This *matches*
  our existing tdd anti-horizontal-slice rule; the delta is emitting the transition as evidence.
- `[SHARPENS]` **Review with ambition over precision:** tell the reviewer to look **beyond the diff** at
  the whole codebase and propose structural "code judo" (delete a whole layer, not polish it).
  Ambition = more false positives, but that's the right trade — false positives are cheap to reject; the
  *missed* improvements are the dangerous ones. Keep review skills **DRY, seam/test/feedback-loop-aware,
  and free of tone directives** (Pocock's critique of the Cursor review skill).
- `[SHARPENS]` **Plan mode is symmetric:** it grounds the *agent* AND rubber-ducks the *developer's* own
  requirements. Cheap, high-leverage prompt additions he swears by: *"make the plan extremely concise,
  sacrifice grammar for concision"* and *"end every plan with a list of unresolved questions."*

## 6. Frontend / visual feedback loop

- `[NEW]` **Frontend is harder for AI than backend because the feedback loop is *visual/temporal*, not
  textual** — the modality LLMs are worst at. The fix is to **hand the agent the same visual loop a human
  has**: a browser via MCP (Chrome DevTools / Playwright) pointed at localhost, doing *ad-hoc
  screenshot QA* (light/dark, `prefers-color-scheme`), **not** writing e2e tests on every commit. This is
  exactly the shape of our `render-critic` / `perception-loop` skills — formalize "visual loop = ad-hoc
  screenshot QA" and **budget for it** (browser MCPs are context-hungry). Without it an AFK frontend loop
  "flies blind" — so any ecosystem AFK front-end cycle must include a browser loop before running
  unattended. (Reinforces `feedback_ui_perception_gap`, `feedback_qa_needs_fps`.)

---

## 7. Adoption table — what to do with this

Ranked by leverage ÷ risk. **Nothing here is auto-adopted; load-bearing items need the maintainer's
call.** Grouped so the human can pick a slice.

| # | Change | Class | Risk | Where |
|---|--------|-------|------|-------|
| A1 | ~~Add an `implement` spine skill~~ **Already installed at user scope.** Sync the stale project-scoped copy instead | Corrected | low | `.claude/skills/` |
| A2 | Run the existing **`git-guardrails-claude-code`** skill rather than hand-writing a hook (a bespoke regex guard was tried in #775 and removed — 12 bypasses) | Adopt now | low | #786 |
| A3 | Emit **red→green transition as evidence** + one-test-at-a-time in `tdd` skill | Adopt now | low | `.claude/skills/tdd/` |
| A4 | `demerzel-self-diagnostic`: treat **confident negatives + unsearched claims** as investigation triggers | Adopt now | low | skill prompt |
| A5 | **Front-load invariants / end-load task** ordering rule; **spec-vs-tickets** vocabulary | Adopt now | low | this doc + skills |
| P1 | **Slim CLAUDE.md** by the admission test; migrate enforceable rules to hooks/validators | **Propose** | **high (one-way)** | `CLAUDE.md`, `.claude/rules/` |
| P2 | ~~Build triage machinery~~ **`~/.claude/skills/triage/` already installed.** Only the one-category+one-state invariant + `.out-of-scope/` ADR non-goals are net-new | Corrected | med | existing `triage` |
| P3 | **`wayfinder`-style map-as-issue-tree** planner (feeds Planner MVP #529) | Propose | med | new skill + Planner |
| P4 | ~~Build a `handoff` skill~~ **`~/.claude/skills/handoff/` already installed**, argument-hint and all. Net-new is only the doctrine that it stays distinct from `/digest` | Corrected | low | existing `handoff` |
| P5 | Budget gate: **provider-native token accounting** + separate **AFK monthly-reset ledger** | Propose | med | `scripts/aiw_budget_gate.py` |
| P6 | Routing rule: **planning = frontier model, implementation = cheap model** (parametric vs contextual) | Propose | low | routing policy |
| W1 | **MCP admission gate** — measure tool-schema token cost before adding; trim tool output | Watch | low | context-budget doctrine |
| W2 | ~~Propose two-axis review~~ **`~/.claude/skills/review/` already does this**, word for word (Standards + Spec, parallel sub-agents). Net-new is only the named Fowler smells + ambition clause | Corrected | low | existing `review` |
| R1 | Rename `to-prd`→`to-spec`, `to-issues`→`to-tickets` (adopt vocabulary; rename optional) | Defer | — | ecosystem parity |

**Provenance:** 140 videos enumerated, 31 AI-coding transcripts captured & distilled 2026-07-19 (the
other 109 are pure-TypeScript/XState, out of scope). Raw captions were not vendored per the `sources/`
transform rule.
