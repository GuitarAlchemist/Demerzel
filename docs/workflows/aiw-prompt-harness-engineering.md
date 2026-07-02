# AIW Prompt and Harness Engineering

Related: #455, #457, #459, #461, #465, #467, #471.

## Purpose

AIW agents should not run from vague prompts. Every AFK-capable task needs a job contract and a harness that makes the work observable, bounded, repeatable, and reviewable.

This document defines the prompt and harness discipline for AIW provider tasks.

## Core principle

A prompt is not enough. The harness owns the execution boundary.

The prompt describes the job. The harness materializes context, restricts scope, runs checks, collects evidence, caps retries, records budget, and stops when governance requires it.

## Minimum provider prompt sections

Every provider task prompt should contain:

1. **Role** — which provider role is being used.
2. **Task** — one bounded task.
3. **Source of truth** — issue, PR, doc, or job spec.
4. **Context bundle** — relevant files, summaries, links, prior attempts (must record which versioned bundle was supplied).
5. **Allowed scope** — paths and operations allowed (defines the strict security boundaries).
6. **Non-goals** — explicit exclusions.
7. **Constraints** — budget, sandbox (ACI contract), secrets, network, style, risk.
8. **Required process** — small steps, tests first where applicable, no broad rewrites.
9. **Required outputs** — patch, branch, PR, summary, tests, risk notes, ledger (packaged for the eval harness).
10. **Stop conditions** — missing context, failing tests, budget exceeded, risk escalation, HALT (explicit human escalation points).

See `prompts/aiw/provider-task.prompt.md`.

## Harness responsibilities

The harness should provide:

- input materialization: issue body, source bundle, prompt pack, linked docs;
- workspace isolation: worktree, container, WSL, VM, GitHub runner, or cloud worker;
- command allowlist: exact commands or approved command classes;
- output collection: diff, logs, checks, structured JSON result;
- failure capture: failed command, stderr excerpt, minimized repro, next action;
- retry policy: max retries, allowed retry causes, escalation rules;
- budget ledger: estimated and actual tokens, calls, runner minutes, cost;
- trace links: issue, branch, PR, workflow runs, artifacts.

## Autonomy modes

```yaml
autonomy:
  mode: observe|draft|patch|pr|harvest
  max_steps: 5
  requires_human_before:
    - broad_scope_change
    - new_secret
    - policy_change
    - cost_over_budget
    - risk_high_or_critical
  allowed_without_human:
    - create_context_bundle
    - classify_issue
    - produce_design_draft
    - make_small_doc_patch
    - make_low_risk_tested_code_patch
```

| Mode | Meaning |
|---|---|
| `observe` | summarize, classify, inspect; no repo changes |
| `draft` | create docs, specs, comments, examples; no runtime code |
| `patch` | create local branch or patch with validation evidence |
| `pr` | open PR only when checks and evidence are present |
| `harvest` | review and merge path only through Demerzel gates |

## Matt-readiness integration

Before `patch` or `pr` mode, the task must pass the Matt-before-AFK readiness gate from `docs/workflows/aiw-matt-readiness-gate.md`.

The generated job must include:

- single vertical slice;
- shared language or links to context;
- allowed paths;
- explicit non-goals;
- test or validation commands;
- evidence requirements;
- stop conditions;
- budget cap;
- no high or critical governance risk.

## Budget-router integration

Before a remote, paid, or large-context provider is invoked, the job must include a budget block compatible with `docs/workflows/aiw-budget-router.md`.

The harness must stop before exceeding the cap or request human approval when the configured approval threshold is crossed.

## Harness result shape

Each execution episode should produce a structured result with:

- job id and issue;
- lane and autonomy mode;
- provider and workspace;
- context bundle hash;
- prompt pack version;
- budget summary;
- commands run;
- changed files;
- outputs;
- observations;
- decision;
- stop reason;
- risk notes.

See `examples/aiw-harness-result.example.json`.

## Retry policy

Allowed retry reasons:

- transient provider failure;
- formatting or lint failure;
- localized test failure with a clear diagnosis;
- incomplete structured output;
- missing dependency that can be installed with allowed commands.

Blocked retry reasons:

- vague failure without new diagnosis;
- repeated same strategy after a failed test;
- scope expansion;
- policy, HALT, or secret conflict;
- budget threshold exceeded;
- provider asks for broader permissions.

## Human-required gates

Human review is required before:

- policy or governance changes;
- new or changed secrets;
- high or critical risk work;
- broad refactors;
- merge authority changes;
- budget increases beyond the approval threshold;
- changes outside allowed paths;
- any action while HALT is active.

## Non-goals

- Do not make prompts the source of truth.
- Do not let provider instructions override Demerzel governance.
- Do not claim safety from prompt text alone.
- Do not give AFK agents broad filesystem or secret access.
- Do not auto-merge based on model confidence.
- Do not create giant prompt templates that encourage broad unreviewable changes.
