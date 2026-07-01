# Review Mode Router and Human Attention Budget

## Purpose

Demerzel should route each work item into the lightest review mode that still preserves meaningful human control.

The system should not ask for explicit human confirmation by default. It should classify the situation, expose evidence, and choose the appropriate review mode.

## Review modes

```text
silent-classify
batch-digest
fast-review
focused-review
decision-gate
escalate-review
```

## Routing signals

Demerzel should consider:

```text
impact
reversibility
scope_class
changed_file_class
review_friction
uncertainty
known_pattern
human_decision_required
verification_horizon
conflicting_evidence
value_sensitive_tradeoff
```

## Mode definitions

### silent-classify

Use when the item is low-impact and does not trigger an external action.

Examples:

- classify a PR as docs-only;
- mark an evidence packet complete;
- update a dashboard row;
- record a retrospective candidate;
- detect that an item has not changed state.

Human prompt: none.

Safe default: record state only.

### batch-digest

Use when the human should be informed but not interrupted.

Examples:

- daily summary of low-risk PRs;
- repeated known-safe pattern usage;
- scorecard trend without required action;
- queue health summary;
- retrospective candidates awaiting later scan.

Human prompt: grouped summary.

Safe default: continue observing.

### fast-review

Use for safe, reversible, low-risk changes that need a quick human glance.

Examples:

- docs-only PR;
- template PR;
- example JSON artifact;
- retrospective example;
- known-safe Jules docs-state-artifact pattern.

Human prompt: concise evidence and merge/hold choice.

Safe default: hold if not reviewed.

### focused-review

Use when one specific human judgment is needed.

Examples:

- choose between two priorities;
- confirm whether an issue is actually satisfied;
- decide whether a PR should be split;
- decide whether evidence is sufficient;
- resolve a product/architecture ambiguity.

Human prompt: one clear question, alternatives, recommendation, and evidence.

Safe default: defer.

### decision-gate

Use for decisions with architectural, responsibility, priority, hard-to-reverse, or value-sensitive consequences.

Examples:

- change repo boundaries;
- change governance model;
- modify critical workflow policy;
- accept significant technical debt;
- make a value-sensitive tradeoff;
- change ownership or responsibility.

Human prompt: structured decision brief.

Safe default: no action.

### escalate-review

Use when evidence conflicts, uncertainty is high, or the item exceeds the verification horizon.

Examples:

- checks pass but intent is unclear;
- scorecard improves but qualitative evidence disagrees;
- PR is broad and touches multiple concerns;
- agent output is non-mergeable or hard to inspect;
- repeated pattern failure appears.

Human prompt: evidence conflict summary and escalation recommendation.

Safe default: hold and request deeper review.

## Mode selection table

| Situation | Review mode | Reason |
|---|---|---|
| Low-impact classification only | silent-classify | No action requires confirmation |
| Many low-risk updates | batch-digest | Preserve attention by grouping |
| Docs-only known-safe PR | fast-review | Human glance is enough |
| Issue satisfaction unclear | focused-review | Needs one human judgment |
| Architecture boundary change | decision-gate | Human decision required |
| Conflicting evidence | escalate-review | Needs deeper critique |
| Hard-to-reverse change | decision-gate | Safe default is no action |
| Value-sensitive tradeoff | decision-gate | Metrics cannot decide values |
| PR exceeds verification horizon | escalate-review | Human cannot verify from summary |

## Prompt usefulness score

Every human prompt should be retrospectively classifiable:

```text
useful_changed_outcome
useful_confirmed_high_value_decision
useful_added_context
unnecessary_low_value
unclear
```

A high rate of `unnecessary_low_value` means Demerzel is causing rubber-stamp pressure.

A high rate of missed escalations means Demerzel is under-routing important work.

## Interaction with TARS

TARS should produce a review-mode verdict that includes:

```text
review_mode
reason
confidence
human_question
alternatives
reversibility_note
evidence_links
safe_default
```

Demerzel may accept, downgrade, or escalate the TARS verdict, but should record why.

## Interaction with IX

IX should measure the human-attention budget:

- prompts per week;
- prompts by mode;
- approval without change;
- decisions that changed outcome;
- fast-review time-to-confidence;
- batch digest usefulness;
- decision-gate quality;
- rubber-stamp warnings.

## Non-goals

- No hidden approval.
- No auto-merge.
- No automatic priority change.
- No metric-only escalation.
- No constant prompting for low-impact state changes.
