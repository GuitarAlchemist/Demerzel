# The Sentinel

**Status:** Governance specification v1.0, 2026-04-12.
**Origin:** Multi-AI meditation on "By asking a human to fix a thing, we remain in the copy and paste world." Three providers converged: the Sentinel is the bottleneck. Ship it first; The Crossing and the Remediation Amendment Protocol are consequences.

## Definition

A **Sentinel** is a governed reactive reasoner with a wake/sleep lifecycle. It is not a daemon (no reasoning), not a cron job (no observation), not an "AI agent" (no sleep), not a service (no duty cycle).

A Sentinel:
- **Sleeps** until a signal arrives
- **Wakes** into a bounded context
- **Observes** through harness adapters
- **Reasons** via MCP sampling
- **Acts** through the governed middleware chain
- **Learns** by feeding outcomes back as observations
- **Sleeps** again

The name captures the duty cycle. A Sentinel is not always-on. It is always-ready. It has a post. It watches from that post. It acts within its mandate. It returns to the post.

Daneel was a Sentinel for twenty thousand years.

## Why it matters

The Sentinel is the architectural move that shifts the human from **operator** to **governor**.

| | Human as Operator | Human as Governor |
|---|---|---|
| Touches | Fix commands, scripts, terminals | Constitutions, thresholds, escalation policy |
| Reads | Compiler output, logs | Escalation reports, observation trends |
| Decides | What to fix next | What the boundary conditions are |
| Leverage | 1x (one fix per action) | 10x-100x (one policy governs all future fixes) |

The human becomes more important, not less. But important for **policy**, not execution.

## The paradox it resolves

We built escalation gates so agents CAN act autonomously. C mass > 0.3 = escalate to human. Everything below = proceed. But then we put a human in front of every action, including the ones the framework explicitly cleared.

This is not caution. It is **incoherence**. The constitution says "you may act," and the deployment says "but don't." The gates are load-bearing walls holding up an empty room.

The Sentinel resolves this by being the first thing that actually lets the gates bear load.

## The lifecycle

```
SIGNAL → WAKE → OBSERVE → REASON → ACT → LEARN → SLEEP
  ↑                                                  │
  └──────────────────────────────────────────────────┘
```

### SIGNAL (trigger)

What wakes the Sentinel:
- **Git hook**: post-commit, post-push, post-merge
- **Timer**: cron schedule (every N hours, daily, weekly)
- **Webhook**: GitHub Actions completion, PR opened, issue created
- **Threshold breach**: a monitoring system detects a governance signal crossed a boundary
- **Manual invocation**: human explicitly asks the Sentinel to wake (the escape hatch)

The trigger is external to the Sentinel. The Sentinel does not poll. It reacts.

### WAKE (context assembly)

On wake, the Sentinel assembles its bounded context:
1. Read the installed SessionLog for recent history
2. Determine the current round number (last round + 1)
3. Load the remediation catalog (claim_key patterns → fix commands)
4. Load the governance policies (blast-radius thresholds, escalation rules, staleness budget)

This is `ix_triage_session`'s preamble, generalized.

### OBSERVE (adapter execution)

Run all registered harness adapters for the current round:
- `ix-harness-cargo` — test health
- `ix-harness-clippy` — lint health
- `ix-harness-tars` — system health (if tars is available)
- `ix-harness-github-actions` — CI health (if run data exists)
- `ix-harness-ga` — governance events (if ga shim exists)
- Any custom shell adapters (submodule currency, etc.)

Each adapter produces `SessionEvent::ObservationAdded` records. All records are appended to the SessionLog.

### REASON (sampling + merge)

1. Merge all observations (current round + prior rounds within staleness budget K) through `ix-fuzzy::observations::merge`
2. Check for contradictions (Belnap-extended table)
3. Check escalation gate: if merged C mass > 0.3, **stop and escalate**
4. If no escalation: use MCP sampling to ask the client LLM to propose a remediation plan given the observations
5. Parse the plan into typed remediation intents

This is `ix_triage_session`'s core logic.

### ACT (governed dispatch)

For each remediation intent in the plan:
1. Map to an `AgentAction::InvokeTool` or a shell command from the catalog
2. Route through `dispatch_action` — the full middleware chain fires:
   - Loop-detect circuit breaker (prevents runaway)
   - Approval / blast-radius classifier (gates destructive changes)
   - Session log (records every verdict)
3. Execute in an isolated worktree/branch (never on main directly)
4. Capture the outcome (success / blocked / failed)

### LEARN (flywheel)

1. Project the execution outcomes into new observations via `projection::events_to_observations`
2. Append to SessionLog
3. Export trace via the flywheel (`export_session_to_trace_dir`)
4. Re-ingest via `ix_trace_ingest` for statistics

The Sentinel's own actions become input to the next round's observations. The loop is closed.

### SLEEP (quiescence)

1. If improvements were made and verified: commit to branch, optionally merge if policy permits
2. If escalation was triggered: write escalation report to a known location (file, issue, notification)
3. Clear the wake context
4. Return to waiting for the next signal

## What already exists vs what needs building

| Component | Status | What's needed |
|---|---|---|
| Observe (adapters) | ✅ 5 adapters live | Nothing — they work |
| Reason (merge + escalation) | ✅ `ix-fuzzy::observations::merge` | Nothing — it works |
| Reason (sampling) | ✅ `ix_triage_session` | Generalize beyond triage |
| Act (governed dispatch) | ✅ `dispatch_action` + middleware | Nothing — it works |
| Learn (flywheel) | ✅ `flywheel::export` + `ix_trace_ingest` | Nothing — it works |
| **SIGNAL (trigger)** | ❌ not built | Git hook / cron / webhook listener |
| **WAKE (context assembly)** | ⚠️ partially in triage handler | Extract into reusable Sentinel::wake() |
| **SLEEP (quiescence)** | ❌ not built | Branch management, escalation report, context teardown |
| **Lifecycle orchestrator** | ❌ not built | The thing that ties SIGNAL→WAKE→...→SLEEP into one binary |

**Four pieces to build.** Everything else is already shipped and tested.

## The Crossing (embedded, not separate)

Per the multi-AI meditation synthesis: The Crossing is embedded in the Sentinel, not a separate system.

The Sentinel tracks, for each remediation catalog entry, a `success_count` and `attempt_count`. When `success_count / attempt_count` exceeds a promotion threshold (default: 3 consecutive successes), the catalog entry's confidence promotes from P to T. This is The Crossing — earned trust through proof.

The governance rule: **a Sentinel with only P-confidence catalog entries runs in supervised mode** (human reviews every commit before merge). **A Sentinel with T-confidence entries runs in autonomous mode** for those specific entry types (commits merge without human review; escalations still go to human).

This means:
- Day 1: Sentinel runs, fixes clippy warnings, human reviews every PR → supervised
- Day 7 (after 3 successful rounds): clippy fixes auto-merge → autonomous for clippy
- Day 14: submodule updates auto-merge → autonomous for submodules
- Each category earns trust independently
- A regression in any category (failed verification after a fix) resets its confidence to P

The Crossing is not a separate ship date. It's the Sentinel's graduation test, built into its telemetry from day one.

## The Remediation Amendment Protocol (deferred)

Per the meditation synthesis: the Amendment Protocol is a consequence of the Sentinel + Crossing, not a prerequisite.

Once the Sentinel has accumulated enough observation history to recognize patterns (observations with no catalog match that recur across rounds), it can propose new remediation mappings. But this is Level 3 — it comes after Level 2 (the running Sentinel) is proven.

**Deferred.** The governance artifact for the Amendment Protocol will be written when the Sentinel has enough telemetry to make self-teaching meaningful, not before.

## Implementation shape

The Sentinel is a single Rust binary: `ix-sentinel`.

```
ix-sentinel
  --mode [supervised | autonomous]  (default: supervised)
  --trigger [hook | cron | manual]
  --config sentinel.toml            (adapter list, catalog, thresholds)
  --session-log ~/.ix/session.jsonl
  --worktree-dir /tmp/ix-sentinel-worktrees
```

In supervised mode: the Sentinel runs the full loop but stops before merge. It writes a PR description + observation diff + the verification result. The human reviews the PR and merges (or rejects). This is the training phase.

In autonomous mode: the Sentinel merges automatically for T-confidence catalog entries. It still stops and writes a PR for P-confidence entries and any escalated actions.

The mode applies **per catalog entry**, not globally. A Sentinel can be autonomous for clippy fixes and supervised for submodule updates simultaneously.

## Governance boundaries

The Sentinel operates under the full Demerzel constitution. Specifically:

- **Article 3 (Reversibility):** The Sentinel MUST work in isolated worktrees/branches. Never commit directly to main. Every action must be revertable.
- **Article 4 (Proportionality):** The Sentinel MUST NOT fix more than the observations indicate. No speculative refactoring. No "while I'm here" changes.
- **Article 6 (Escalation):** The Sentinel MUST escalate when C mass > 0.3, when blast-radius classifier returns Tier 3+, or when loop-detect fires.
- **Article 7 (Auditability):** Every Sentinel run produces a SessionLog trace. The commit message carries the observation diff. The PR description explains the governance reasoning.
- **Article 9 (Bounded Autonomy):** The Sentinel operates within the remediation catalog. It cannot invent new fix types (until the Amendment Protocol ships). It cannot modify its own catalog. It cannot change its own governance thresholds.

## What this document does NOT specify

- **The trigger implementation** (git hook vs cron vs webhook). That's a deployment choice, not a governance question.
- **The Amendment Protocol** (Level 3 self-teaching). Deferred until the Sentinel has telemetry.
- **Cross-repo Sentinel coordination** (multiple Sentinels watching different repos). Deferred until one Sentinel works.
- **The signature layer integration** (signed observations from the Sentinel). Uses the existing `ix-harness-signing` foundation when Tier 1+ adapters are needed.

## The sentence that captures it

> The Sentinel is the moment governance artifacts stop being documents and start being operational infrastructure. The escalation gates bear load. The adapters produce signal. The middleware governs action. The flywheel compounds learning. The human writes policy. The code improves itself.

## Version

1.0 — 2026-04-12 — initial specification. Lifecycle, embedded Crossing, governance boundaries, implementation shape. Informed by multi-AI meditation (Codex/Gemini/Claude) with 2-1 convergence on Sentinel as bottleneck, Gemini dissent on Crossing absorbed as embedded feature.
