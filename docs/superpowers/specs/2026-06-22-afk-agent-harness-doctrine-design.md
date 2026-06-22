# AFK Agent + Harness Doctrine — Design

**Date:** 2026-06-22
**Status:** Approved for planning
**Author:** Demerzel (Claude Opus 4.8) with Stephane Pareilleux
**Source material:** `sources/chats/matt-pocock-david-ondrej-agentic-workflow.md`
(Matt Pocock × David Ondrej, YouTube, 2026-06-18)

---

## 1. Purpose

Absorb Matt Pocock's agentic-engineering philosophy and apply it to the
GuitarAlchemist ecosystem in two concrete deliverables:

1. **Absorb & reconcile doctrine** — capture the transcript's reusable lessons and
   *adjust* the existing `CLAUDE.md` operating doctrine where Matt diverges from
   the Karpathy 4 Rules and the Cherny continuity patterns already encoded there.
2. **AFK agent (tracer bullet)** — close the one missing link in the ecosystem's
   existing autonomous machinery: an *away-from-keyboard implement step* that takes
   a triaged, labelled GitHub issue and produces a reviewed pull request, running
   the agent inside a Docker sandbox via `sandcastle`.

The governing insight from recon: **~70% of an AFK system already exists** in
Demerzel. This work is a thin vertical slice connecting two halves we already
built, not a greenfield system.

## 2. Background — what already exists (do not rebuild)

| Existing artifact | Role in Matt's queue model |
|---|---|
| `.github/workflows/demerzel-driver-triggers.yml` | Commits `state/triggers/*.trigger.json` — **the queue** |
| `.github/workflows/demerzel-autofix.yml` | Claude-API triage (classification/priority/auto_fixable/verdict) — **explore → structured verdict** |
| `.github/workflows/agent-blackbox.yml` | PR risk report + verdict enforcement w/ `agent-blackbox-reviewed` human override — **review gate** |
| `.github/workflows/cross-model-review.yml` | Cross-model PR review — **second review lens** |
| `policies/autonomous-loop-policy.yaml` | Risk classification, self-merge authority, HITL thresholds — **the rules the AFK agent obeys** |
| `scripts/run_ml_feedback_cycle.py` | Working, scheduled, HALT-honored governor — **the pattern the AFK governor copies** |
| `scripts/demerzel_halt.py` | Cross-repo HALT kill-switch — **must be honored** |

**The gap:** `demerzel-autofix.yml` stops at *commenting* "run `/demerzel fix #N`
in a Claude Code session" — i.e. the implementation step is still human-in-the-loop.
The AFK agent fills exactly that gap.

## 3. Deliverable 1 — Absorb & reconcile doctrine

### 3.1 Capture

Run `/learnings` to record the non-obvious takeaways (harness ≈ model,
queue-not-loop, procedures-vs-abilities, context-bloat, DX≈AX) under
`docs/solutions/`.

### 3.2 Reconcile `CLAUDE.md` (surgical — add one section, leave others in place)

Add a new section **"Harness doctrine (Pocock delta, 2026-06-22)"** that states
each principle and its relationship to the doctrine already present:

| Matt's principle | Relationship | Action |
|---|---|---|
| Harness ≈ model (50/50), **agent-agnostic** | New | Add; cross-reference `project_harness_engineering_direction` memory |
| **Queue, not loop** (HITL pushed right) | Adjusts Ralph-loop framing | Reframe loops as a special case of a task-queue; cite `demerzel-driver-triggers` as the existing queue |
| **Procedures vs abilities** (abilities leak descriptions into context) | Tensions with superpowers "model-in-control" | Add skill-authoring rule: prefer procedures; mark user-only ability-skills `disable model invocation` |
| **Delete everything → observe → layer back** | Adjusts (heavy skill/MCP inventory) | Add as periodic practice; `demerzel-context-budget` is the consumer |
| **DX ≈ AX** (optimize codebase for the agent) | New | Add one line |
| Review the *system*, not just code | Reinforces metafix + ml-feedback | Cite convergence, no change |
| Strategic > tactical (Ousterhout) | ≈ Karpathy "think before coding" + goal-driven | Cite convergence, keep |

Constitutions and policies are **not** touched (this is operating doctrine, not
constitutional change). The section explicitly marks agree=keep vs diverge=adjust
so future readers see the reconciliation, not a silent overwrite.

## 4. Deliverable 2 — AFK agent

### 4.1 Components and placement

`no-runtime-code.md` keeps Demerzel spec-only. Therefore:

1. **Harness — `../afk-harness/` (sibling repo dir, agent-agnostic).**
   A `sandcastle` (`@ai-hero/sandcastle`, TypeScript) project with the **Docker**
   bind-mount provider (Docker 29.2.1 already installed). Entry point takes
   `(repo, issue#, prompt)`, runs Claude Code **headless** inside a Docker
   sandbox against a checkout of the target repo, produces a branch + commits,
   pushes, and opens a PR. Reusable later by ga/ix/tars (Matt: keep the harness
   agent-agnostic).

2. **Governor — `Demerzel/scripts/run_afk_cycle.py`.**
   Modeled on `run_ml_feedback_cycle.py`. Responsibilities:
   - Check the HALT marker first (no-op if halted).
   - `gh issue list --label agent-implement --state open` → candidate queue.
   - Classify risk per `autonomous-loop-policy.yaml` (low/medium/high/critical).
   - Verify authorization trace (the issue itself = pre-authorized domain work;
     governance edits = always-pre-authorized governance work).
   - Invoke `../afk-harness` for each eligible issue.
   - Persist `state/loops/<id>.loop.json` (schema reuse) and an audit record
     under `state/oversight/` (NOT `state/evolution/` — that schema rejects
     run-logs; learned the hard way in #373/#375).

3. **Procedure skill — `Demerzel/.claude/skills/afk-implement/` (`disable model invocation: true`).**
   The operating instructions the sandboxed Claude Code runs with: scope-check the
   issue → minimal implementation (Karpathy simplicity) → run the oracle
   (`python scripts/validate_governance.py`) → commit → write a rich PR description
   (what/why/evidence). User-invoked / governor-invoked only; description does not
   leak into normal context.

4. **Governance spec — `Demerzel`.**
   A short behavioral spec for the AFK agent + `agent-implement` label semantics
   (extends `docs/agents/triage-labels.md`). Reuses `schemas/loop-state.schema.json`.

5. **Review gate — EXISTING.** `agent-blackbox.yml` + `cross-model-review.yml`.
   Self-merge governed by EXISTING `autonomous-loop-policy.yaml`.

### 4.2 Data flow

```
GitHub issue [label: agent-implement]
  → scripts/run_afk_cycle.py        (HALT check · risk classify · auth trace)
  → ../afk-harness  sandcastle.run() (Claude Code headless + afk-implement skill, in Docker)
  → branch + commits + PR
  → agent-blackbox.yml + cross-model-review.yml   (existing gates)
  → self-merge  (governance work, low/medium risk, CI pass, confidence ≥ 0.7)
       OR ping human  (high/critical, low confidence, conscience signal)
  → audit: state/loops/<id>.loop.json + state/oversight/afk-audit.json
```

### 4.3 Safety & policy compliance (all from `autonomous-loop-policy.yaml`)

- **Sandbox isolation:** Docker — agent cannot delete host files or exfiltrate env
  vars (Matt's stated reason for sandboxing).
- **HALT:** honored as the first action of every cycle.
- **Risk gates:** constitution/policy edits = critical → never self-merged, human
  pre-approval required. Schema migrations / cross-repo = high → per-iteration.
- **Confidence thresholds:** <0.5 bump risk one level; <0.3 escalate to human.
- **Self-merge:** CI pass + confidence ≥0.7 + no conscience signal ≥0.8 + auth
  trace. Single-model confidence capped at 0.8.
- **Halt conditions:** 2 consecutive failures; drift/regression/convergence-stall;
  any Zeroth Law concern.
- **Auditability:** every action traces to the issue number (Default Art. 7).

### 4.4 Testing / proof of done (tracer bullet)

1. **Dry-run mode:** governor classifies + plans + writes loop-state, *without*
   invoking the sandbox. Verifies queue read, risk classification, HALT, audit.
2. **One real low-risk issue:** a genuine Demerzel governance issue labelled
   `agent-implement` flows end-to-end to a PR that passes `agent-blackbox` and is
   self-merged (or human-pinged). Oracle: `validate_governance.py`.
3. **Done = that run is green.** Until then the harness is not "done"
   (harness-before-harvest rule).

### 4.5 Explicitly deferred (YAGNI — graduation steps, not built now)

- Approach A: self-hosted GitHub Actions runner (`agent-implement.yml`,
  `runs-on: [self-hosted]`) for event-driven triggering.
- Parallel multi-sandbox fan-out.
- Rollout to ga / ix / tars (the harness is built agent-agnostic to enable this).
- Video + TTS PR walkthroughs (Matt's "make review seamless" idea).
- Podman / WSL backends (Docker only for the tracer bullet).

## 5. Out of scope

- No changes to constitutions or policies.
- No new MCP servers or model changes (agent-agnostic; Opus 4.8 medium, as today).
- No rewrite of existing workflows; the AFK agent plugs into them.

## 6. Open risks

- **Headless Claude Code in Docker:** running the agent non-interactively with a
  bounded, allow-listed tool set inside the container needs validation; this is the
  riskiest unknown and is surfaced first by the tracer bullet.
- **Secrets in the sandbox:** the container needs a scoped token to push + open PRs;
  must be least-privilege and never the user's full PAT.
- **`no-runtime-code` perception:** the harness lives outside Demerzel to avoid the
  conflict; the governor (`run_afk_cycle.py`) follows the established
  governance-automation carve-out already used by `run_ml_feedback_cycle.py`.
