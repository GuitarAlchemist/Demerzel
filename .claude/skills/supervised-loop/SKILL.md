---
name: supervised-loop
description: Run one bounded supervised autonomous cycle on the Demerzel governance repo. Picks the smallest unchecked governance slice inside allow_edit, implements it, runs the oracle (`pwsh scripts/verify.ps1`), emits cycle evidence, and stops. Refuses to run unless dev-process-overseer reports loop-eligible and the preflight passes. Use when asked to "run one supervised loop", "advance governance autonomously", or "do one cycle and stop".
metadata:
  type: skill
  scope: demerzel
  version: 0.1.0
  emits: state/governance/supervised-loop-cycle.json
---

# Supervised Autonomous Loop (Demerzel)

Operationalises the supervised-loop pattern from agent-blackbox on the
Demerzel governance repo. The cycle is intentionally short: one slice,
one verify, one evidence file, then stop.

## Demerzel-specific scope

Demerzel is the **governance authority** for the GA / ix / tars / Seldon
ecosystem. Its contracts (`policies/`, `constitutions/`, `personas/`,
`schemas/contracts/`) are load-bearing for every sibling repo via the
Galactic Protocol. The supervised loop **only operates within
documentation, scripts, state, and `.claude/`** on the initial rollout.
The four canonical protected surfaces (`policies/`, `constitutions/`,
`personas/`, `.github/workflows/`) are protected_paths because a
regression there fans out across every consumer immediately.

The Asimov Zeroth Law is a hard one-way door and is enforced by the
preflight refusal list below.

## When to use

- The user asked for one bounded autonomous improvement on Demerzel.
- You are running a scheduled `/loop` and need to make one safe slice of
  progress before yielding.
- You are dogfooding the supervised pattern that sibling repos copy
  from agent-blackbox (`scripts/supervised-loop-preflight.ps1`).

## Hard refusals (never bypass)

- `state/governance/dev-process-overseer.json` missing, stale (>24h),
  or `workflowMode != "loop-eligible"` -> abort with reason.
- `.STOP` file at repo root -> abort.
- `HALT-ALL` marker present at `$HOME/.demerzel/HALT-ALL` and active
  (scope covers Demerzel) -> abort. See
  [`scripts/demerzel_halt.py`](../../../scripts/demerzel_halt.py).
- The diff touches `policies/**`, `constitutions/**`, `personas/**`,
  or `.github/workflows/**` -> abort and route to the operator.
- The diff exceeds the **rewrite budget** (default 200 lines / 10 files
  per cycle, 600 lines absolute cap) -> abort with reason
  `budget-exceeded`. See [`docs/review-independence.md`](../../../docs/review-independence.md).

## Operating model

Demerzel's loop runs as a **producer-reviewer** pair (see
[`docs/review-independence.md`](../../../docs/review-independence.md)):

1. **Producer**: this skill plans and writes the diff.
2. **Reviewer**: a **fresh sub-agent** (different context window) reads
   the diff + oracle output + policy, and votes pass/warn/fail. The
   reviewer **cannot self-certify** — it is never the same agent that
   produced the diff.
3. **Cross-vendor verdict**: for one-way-door slices the verdict step
   adds a sibling vendor (Gemini, Codex peer, or Mistral) so at least
   two independent vendors agree before merge-drive.

The supervised loop will refuse to merge-drive when any of the four
review-independence dimensions is unreachable for the slice in
question.

## Cycle steps

1. **Preflight**: `pwsh scripts/supervised-loop-preflight.ps1`. Refuses
   on dirty worktree, missing overseer, halt markers, or
   protected-path dirt.
2. **Pick a slice**: the smallest unchecked entry in `BACKLOG.md`
   (when present) or `docs/roadmap-poincare.png`'s next checkbox.
3. **Implement**: scoped to `allow_edit`. Stay inside the rewrite
   budget.
4. **Oracle**: `pwsh scripts/verify.ps1` MUST exit zero. The oracle
   gates on the validate_governance.py script + schema validation.
5. **Cycle evidence**: write
   `state/governance/supervised-loop-cycle.json` with the slice id,
   diff stats, oracle exit, and reviewer verdict.
6. **Yield**: commit one Conventional commit, push the branch, and
   stop. Do **not** chain into another cycle in the same session.

## Loop policy

Loop scope lives in the harness baseline at
[`state/quality/demerzel-harness/baseline.json`](../../../state/quality/demerzel-harness/baseline.json)
under `_harness` and `scope_boundary`:

- `allow_edit`: documents, scripts, state, `.claude/`.
- `protected_paths`: `policies/**`, `constitutions/**`,
  `personas/**`, `.env*`.
- Kill-switches: `state/.loop-halted` (global),
  `state/quality/demerzel-harness/.STOP` (per-domain).

## Related

- [`scripts/supervised-loop-preflight.ps1`](../../../scripts/supervised-loop-preflight.ps1) — deterministic preflight.
- [`scripts/verify.ps1`](../../../scripts/verify.ps1) — repo oracle.
- [`scripts/dev-process-overseer.ps1`](../../../scripts/dev-process-overseer.ps1) — workflowMode emitter.
- [`docs/review-independence.md`](../../../docs/review-independence.md) — the four independence dimensions.
- [`docs/harness-observability.md`](../../../docs/harness-observability.md) — producer-reviewer evidence chain.
- [`.claude/skills/demerzel-loop/SKILL.md`](../demerzel-loop/SKILL.md) — the legacy Demerzel review loop.
