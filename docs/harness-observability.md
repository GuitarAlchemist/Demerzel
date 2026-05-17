---
title: Harness & Response-Quality Observability (Demerzel)
status: living
date: 2026-05-17
related:
  - docs/review-independence.md
  - .claude/skills/supervised-loop/SKILL.md
  - state/governance/dev-process-overseer.json
  - state/quality/demerzel-harness/baseline.json
  - agent-blackbox.policy.json
---

# Harness & Response-Quality Observability (Demerzel)

This doc records the loop-driven observability artifacts that Demerzel
emits so the agent-blackbox install audit and the supervised-loop kit
can treat the governance harness as **durably reviewed**, not just
*"the validator passed on my box"*.

It is the Demerzel-side companion to the install-audit `observability`
check, which expects four pieces of evidence:

1. **harness-audit** — repo harness readiness report.
2. **response-quality** — agent response verbosity, readability, claim
   density, grounding markers.
3. **overseer** — dev-process-overseer JSON capturing workflowMode,
   warnings, and gate signals.
4. **quality baselines** — `state/quality/<domain>/baseline.json` plus
   the matching `last.json` produced each cycle.

Demerzel already produces overseer + baseline + per-domain oracle
output. The two that the install audit still flags (`harness-audit`
and `response-quality`) live as **workflow step strings** inside
`.github/workflows/agent-blackbox.yml`; that workflow file is in the
protected-paths list and cannot be edited by the supervised loop, so
those two evidence credits stay as a follow-up tracked in `BACKLOG.md`
(see *agent-blackbox install-audit follow-ups*).

## Loop-driven evidence chain

```text
producer  -> scripts/dev-process-overseer.ps1
          -> state/governance/dev-process-overseer.json    (overseer)

producer  -> pwsh scripts/verify.ps1
          -> state/quality/demerzel-harness/last.json      (oracle output)

producer  -> scripts/qa_tribunal_emit.py                   (QA Architect)
          -> state/quality/verdicts/<repo>/<pr>/...        (cross-vendor)

reviewer  -> python -m cli.agent_blackbox harness-audit    (harness-audit)
          -> dist/harness-audit.json

reviewer  -> python -m cli.agent_blackbox response-quality (response-quality)
          -> dist/response-quality.json

verdict   -> python -m cli.agent_blackbox install-audit
          -> dist/install-audit.json
```

The pattern is *producer-reviewer with disk handoff*: each producer
writes to a stable JSON path, each reviewer reads that path in a
**fresh sub-agent** / **different context**, and the verdict is a
third party reading both producer and reviewer outputs. This is the
same review independence the QA Architect tribunal pattern uses (see
`docs/review-independence.md`).

## Why on-disk artifacts

JSON-on-disk is the canonical Demerzel cross-agent handoff. It:

- survives session boundaries (auto-compact, restart, surface
  hand-off),
- can be inspected by a human reviewer without rehydrating the agent,
- is the input shape `python -m cli.agent_blackbox harness-audit` and
  `python -m cli.agent_blackbox response-quality` already accept,
- is the same shape `state/quality/<domain>/baseline.json` and
  `state/governance/dev-process-overseer.json` already publish.

## Pre-existing Demerzel evidence

| Path | Producer | What it proves |
| --- | --- | --- |
| `state/governance/dev-process-overseer.json` | `scripts/dev-process-overseer.ps1` | workflowMode, gate warnings, halt markers |
| `state/quality/demerzel-harness/baseline.json` | (committed baseline) | what "green" means for the Demerzel harness oracle |
| `state/quality/demerzel-harness/last.json` | `pwsh scripts/verify.ps1` | latest harness oracle result |
| `state/quality/governance-validation/baseline.json` | committed baseline | schema-validation pass-rate baseline (Phase 1 follow-up) |

These artifacts + overseer are already published, and the install
audit already credits them. The remaining install-audit deductions
for `harness-audit` and `response-quality` are
*workflow-step-string* checks (the audit greps the agent-blackbox
GitHub Actions workflow text for those literal strings); they do not
relax to docs alone, so closing them requires either an operator
workflow edit or a follow-up audit-rule relaxation in agent-blackbox
itself. Both are tracked in `BACKLOG.md`.

## How a loop session uses this

A supervised-loop cycle ends with:

1. The producer writes `state/quality/<domain>/last.json` and
   `state/governance/supervised-loop-cycle.json`.
2. A reviewer (fresh sub-agent, different context) reads both, and
   votes by writing `dist/harness-audit.json` and
   `dist/response-quality.json` when applicable.
3. The verdict step runs `python -m cli.agent_blackbox install-audit`
   and `python -m cli.agent_blackbox enforce --report …` against the
   above to decide whether the cycle is mergeable.

No producer is ever its own reviewer (see
`docs/review-independence.md`).

## Hard limits

The observability chain never bypasses the supervised-loop hard
gates (see `.claude/skills/supervised-loop/SKILL.md`):

- No service restarts.
- No edits to `policies/**`, `constitutions/**`, or `personas/**`
  without explicit human approval.
- No `.github/workflows/**` edits without explicit human approval —
  even if it would close the remaining install-audit observability
  deduction.
- No `agent-blackbox-reviewed` label without explicit human approval.

## Related

- `docs/review-independence.md` — independence dimensions the
  verdict step relies on.
- `.claude/skills/supervised-loop/SKILL.md` — the bounded-cycle skill.
- `scripts/supervised-loop-preflight.ps1` — deterministic preflight.
- `scripts/verify.ps1` — the Demerzel oracle.
