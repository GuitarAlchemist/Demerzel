# 4. Single-sourced confidence thresholds via ref:confidence tokens

- Status: Accepted
- Date: 2026-06-21
- Deciders: Stephane Pareilleux
- Source: `/improve-codebase-architecture` review + `/grilling` session (2026-06-21), Candidate 6

## Context

The confidence ladder — `≥0.9 autonomous · ≥0.7 with-note · ≥0.5 ask-confirmation ·
≥0.3 escalate · <0.3 do-not-act` (stated in `CLAUDE.md`) — was restated across 8+
policies. `auto-remediation-policy.yaml` even carried `reference: "alignment-policy.yaml
confidence_thresholds"` beside its own copy of `0.9 / 0.7 / 0.5`. Retuning a rung meant a
multi-file hunt, and the copies could drift.

This is the same disease as ADR-0002 (harvest, don't declare), one tier down: a value
**declared** in many places instead of read from one home.

## Decision

Author the ladder once in `logic/confidence-thresholds.yaml` (`thresholds.<key>` →
`{value, operator, meaning}`), and introduce a new **canonical citation token**,
`ref:confidence#<key>`, alongside the existing `<constitution>#<article>` / `policy:<name>`
/ `persona:<name>` syntax. Policies reference a rung instead of restating the number:

```yaml
confidence_thresholds:
  proceed_autonomously: ref:confidence#autonomous
```

`scripts/build_manifest.py` (`check_confidence_refs`) harvests every token, emits a
`confidence_ref` edge, and **fails CI on a dangling key** — the same gate `precedence.yaml`
and the canonical reference syntax already use. The values live only in the canonical file.

Only genuine **ladder** restatements are migrated. Thresholds that merely share a number
but mean something policy-specific (e.g. `autonomous-loop-policy.yaml`'s single-model
self-merge cap at `0.8`, its bump/halt triggers) stay where they are — they are not the
ladder. Prose that *describes* the ladder ("confidence below 0.5 → ask") stays prose.

## Consequences

- **Locality**: retune a rung in one file; every referencing policy follows.
- **Leverage**: dangling references fail CI, so a renamed/removed rung can't rot silently.
- **Trade-off (accepted)**: the consumer of a policy here is an LLM reading the YAML, and
  it now sees `ref:confidence#autonomous` instead of the literal `0.9` — an indirection it
  must dereference. We accept this for the single-source guarantee; the canonical file is
  small and self-describing. (The alternative — keep the inline number and only *assert*
  agreement, the precedence.yaml pattern — was considered and not chosen here.)
- A new token kind joins the canonical reference syntax; future schemes resolve it.

## Alternatives considered

- **Keep inline values, assert agreement in the manifest** (the `precedence.yaml` pattern:
  values stay readable, CI fails on divergence). Rejected in favour of true single-sourcing
  with reference tokens — though it remains the better fit if the LLM-reader indirection
  proves costly, and this ADR is the place to revisit that.
- **Leave the restatement, document it as accepted.** Rejected: the drift risk is real
  (`auto-remediation` already carried a hand-synced copy with a "reference" note).
