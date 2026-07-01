# Anti-Rubber-Stamp Human Review Policy

## Purpose

Demerzel must preserve meaningful human judgment without turning the human maintainer into a constant approval button.

The goal is not to ask the human to approve every small action. The goal is to route work so that human attention is used where it materially changes the outcome: architecture, priority, responsibility, uncertainty, reversibility, and value-sensitive tradeoffs.

## Core principle

```text
Do not ask the human to approve what the system can safely classify, summarize, defer, or batch.

Ask the human only when the decision is meaningful.
```

## Operating model

```text
Agents execute.
IX measures.
TARS reasons.
Demerzel governs.
Humans decide.
```

Demerzel should distinguish between:

- an agent proposal;
- an analytical signal;
- a TARS reasoning verdict;
- a Demerzel recommendation;
- a human decision.

A recommendation is not a decision. A score is not a decision. A green check is not a decision.

## Human attention budget

Human attention is a scarce governance resource.

Demerzel should ask for explicit human confirmation when one or more are true:

- architectural direction changes;
- priority changes;
- responsibility or accountability changes;
- large or hard-to-reverse changes;
- conflicting evidence;
- high uncertainty;
- value-sensitive tradeoff;
- agent recommendation exceeds the verification horizon;
- repeated pattern failure;
- scorecard suggests improvement but qualitative evidence disagrees.

Demerzel should avoid explicit human confirmation for:

- trivial docs or examples updates;
- known-safe patterns;
- low-impact reversible changes;
- purely informational reports;
- already-approved template application;
- classification that does not trigger external action.

## Rubber-stamp smell tests

A review request is probably rubber-stamping if:

- the human is not shown alternatives;
- the human is not shown uncertainty;
- the human is not shown consequences;
- the human has no realistic ability to change the result;
- the same confirmation repeats many times;
- the approval wording is broader than the evidence;
- the prompt asks for approval of a metric rather than a decision;
- the safe default is unclear;
- approval is requested before the relevant evidence is visible.

## Meaningful review prompt requirements

When Demerzel asks for human confirmation, the prompt should include:

- the decision to make;
- why human judgment is required;
- available options;
- recommended option;
- reason for recommendation;
- uncertainty;
- cost of being wrong;
- reversibility;
- affected repos or components;
- evidence links;
- default safe action if the human does nothing.

## Default safe actions

```text
Low impact, known-safe, reversible -> classify or batch
Ambiguous or medium impact -> defer or focused-review
High impact -> decision-gate
Value-sensitive -> decision-gate with argumentation
Hard to reverse -> decision-gate
Evidence conflict -> escalate-review
```

## Metrics

Demerzel should track, or delegate to IX to track:

- human prompts per week;
- prompts by review mode;
- approval-without-change rate;
- outcome-changed-by-human rate;
- prompts later judged unnecessary;
- batch digest success rate;
- fast-review time-to-confidence;
- focused-review resolution rate;
- decision-gate quality notes;
- escalations due to missing evidence.

If most prompts are approved without change, the review design is probably too noisy.

If prompts decrease while missed important decisions increase, the review design is too quiet.

The goal is not fewer prompts. The goal is better prompts.

## Relationship to other governance artifacts

- Decision gates define when human confirmation is required.
- Review mode routing defines how work reaches the human.
- TARS review-mode verdicts explain which mode is justified.
- IX attention metrics measure whether prompts are useful.
- Retrospectives capture corrections and update future routing.

## Non-goals

- No automatic merge approval.
- No automatic priority change.
- No replacement of human architectural judgment.
- No hidden escalation based only on a metric.
- No prompt spam for low-impact events.
