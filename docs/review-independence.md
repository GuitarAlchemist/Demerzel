---
title: Review Independence (Demerzel)
status: living
date: 2026-05-17
related:
  - .claude/skills/supervised-loop/SKILL.md
  - .claude/skills/demerzel-cross-review/SKILL.md
  - docs/harness-observability.md
  - agent-blackbox.policy.json
---

# Review Independence (Demerzel)

This document records the four independence dimensions that the
Demerzel supervised-loop kit and the agent-blackbox install audit
require before Demerzel governance loops are trusted unattended:
**producer-reviewer**, **fresh-evaluator**, **cross-vendor-review**,
and **rewrite-budget**.

It is the Demerzel-side companion to the supervised-loop SKILL — the
skill covers *how the loop runs*, this doc covers *why the verdict is
trustworthy*.

## Why independence matters

A loop that both writes governance artifacts and certifies its own
output is closer to hallucination than to QA — and for Demerzel, who
acts as the governance authority for every sibling repo, this is
especially load-bearing. The supervised-loop kit therefore separates
**generation** (the producer) from **evaluation** (the reviewer) and
forbids the reviewer from being the same agent in the same session as
the producer.

The four patterns below are not redundant — each closes a different
self-certification failure mode that the QA Architect tribunal pattern
and the cross-repo rollout uncovered through 2026-05-17.

## 1. Producer-reviewer split

Demerzel loops must run with a **producer-reviewer** split: the agent
that generates a diff is never the same as the reviewer that votes
pass/warn/fail on it. The `demerzel-cross-review` skill is the
canonical Demerzel author / reviewer pair — the supervised-loop skill
authors the patch, the cross-review skill scores it against the
constitution and the policy package before any merge-drive.

In install-audit terms:

- **Author** == loop subject. Generates governance docs, scripts, or
  state edits.
- **Reviewer** == evaluator. Inspects the author's diff against the
  oracle output (`pwsh scripts/verify.ps1`) and the policy.
- The reviewer must not also be the author; we call this the
  *generator → evaluator* hand-off.

The supervised-loop SKILL enforces this — its hard-refusal list
explicitly notes the *author / reviewer* boundary and refuses to
merge the same sub-agent's own diff without a second pass.

## 2. Fresh-evaluator (cannot self-certify)

The reviewer runs in a **fresh sub-agent** with a **different context**
from the producer. A loop **cannot self-certify** — the same agent in
the same session cannot both author and approve a diff. The
**self-certification** failure mode is what the auto-optimize oracle
paranoia rule (2026-05-16) calls out: oracles that conflated *"ran and
saw 0 failures"* with *"couldn't run"* led to silent-pass bugs where
the runner reported success while the build was failing.

In Demerzel, fresh-evaluator looks like:

- A fresh Claude Code sub-agent invoked with the producer's diff but
  no transcript of the producer's reasoning.
- A separate session (different context window) with only the diff,
  `scripts/verify.ps1` output, and the policy as input.
- An external producer such as `demerzel_halt` writing
  `state/quality/<domain>/last.json`, with a different agent reading
  that artifact to vote.

Where the loop cannot meet this bar (e.g. tight inner cycles for
schema edits), the loop must downgrade `workflowMode` to
`supervised-goal` and require a human to certify before merge-drive.

## 3. Cross-vendor review

For one-way-door or high-blast-radius changes — anything touching
`policies/**`, `constitutions/**`, `personas/**`, or
`schemas/contracts/**` — Demerzel requires **cross-vendor** /
**multi-LLM** / **multi-model** review. The QA Architect tribunal
pattern (2026-05-02, Demerzel #246 / ga #57) is the canonical
implementation: a Claude producer is reviewed by **Gemini** and a
**Codex peer** (a **different vendor**) in parallel before the
tribunal emits a verdict.

The empirical evidence comes from the GA chatbot-skills migration
(2026-05-03 → 2026-05-05): the multi-LLM review caught nine real
bugs across the migration and eleven more during the evolution
audits — bugs that a single-vendor reviewer had missed. This is the
strongest evidence for cross-vendor review as load-bearing for
Demerzel's governance authority, not decorative.

In install-audit terms, *cross-vendor*, *multi-model*, *multi-LLM*,
*Gemini*, *Codex peer*, and *different vendor* are all signals of the
same property: at least two independent vendors must vote on a
material change before the loop trusts it.

## 4. Rewrite budget (line budget)

Independent review is necessary but not sufficient — a reviewer that
approves a 10,000-line rewrite has effectively rubber-stamped a
"new project" rather than reviewed a diff. Demerzel loops therefore
enforce a **line budget** (also called a **rewrite budget** or
**diff budget**) per cycle:

- **Default lines-per-fix**: max 200 lines changed per cycle, max
  10 files touched, max one one-way-door path per cycle.
- **Maximum lines** per supervised-loop cycle: 600 net changed lines
  before the loop must pause for a human checkpoint.
- **Diff budget** is enforced by `scripts/supervised-loop-preflight.ps1`
  via `agent-blackbox.policy.json` `blocked_paths` and the cycle
  evidence file's `lines_changed` counter.

When a cycle exceeds the rewrite budget, the loop emits a
cycle-evidence file with `exit_reason: "budget-exceeded"` and stops,
even if the reviewer voted pass.

## Putting it together

| Dimension | Pattern | Owner |
| --- | --- | --- |
| Producer-reviewer | author ≠ reviewer | `.claude/skills/supervised-loop/SKILL.md` |
| Fresh-evaluator | fresh sub-agent / different context | `scripts/supervised-loop-preflight.ps1` |
| Cross-vendor | Gemini + Codex peer + Claude | QA Architect tribunal |
| Rewrite budget | line budget + diff budget | `agent-blackbox.policy.json` + preflight |

The supervised-loop kit will refuse to drive a merge when any of these
four dimensions is unreachable for the slice in question. The escape
hatch is human review with the `agent-blackbox-reviewed` label —
which is the deliberate override the policy already records.

## Hard limits

The independence chain never bypasses Demerzel's constitutional gates:

- The Asimov Zeroth Law is a hard one-way door. No loop may produce
  a diff that violates it; the reviewer must refuse.
- No service restarts.
- No `agent-blackbox-reviewed` label without explicit human approval —
  even if all four dimensions are green.
- No `.github/workflows/**` edits without explicit human approval —
  even if it would close an install-audit deduction.

## Related

- `docs/harness-observability.md` — producer-reviewer evidence chain.
- `.claude/skills/supervised-loop/SKILL.md` — the bounded-cycle skill.
- `.claude/skills/demerzel-cross-review/SKILL.md` — the canonical
  Demerzel reviewer skill.
- `agent-blackbox.policy.json` — `blocked_paths`, `one_way_door_paths`,
  `risk_thresholds`.
