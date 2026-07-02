# AIW Budget-Aware Delegation Router

Related: #455, #457, #459, #461, #465, #467.

## Purpose

The AIW router chooses the cheapest worker that can produce the next required evidence artifact without violating Demerzel governance.

It prevents every task from being sent to the strongest remote coding agent by default, and it records the budget decision behind each escalation.

## Router principle

Use the cheapest adequate worker for the next evidence step.

Escalate only when the current evidence says a stronger, larger-context, or remote worker is justified.

## Routing stages

| Stage | Goal | Default worker | Output |
|---|---|---|---|
| intake | classify task, lane, risk, rough context size | `ollama-local` or cheap small model | intake estimate |
| grounding | gather source-grounded context | `notebooklm`, `ollama-local`, or `gemini-cli` | research pack |
| shaping | make the issue Matt-ready | Pocock-style shaping skills or cheap model | allowed paths, non-goals, tests, stop conditions |
| implementation | produce patch or PR only after readiness gates | `claude-code-local`, `codex`, `jules`, or similar | branch, diff, PR, logs |
| verification | validate and collect evidence | static checks, CI, model review, human review | test log, risk notes, decision |

## Budget fields

Every AIW job should carry an explicit budget block before any paid or remote provider invocation.

```yaml
budget:
  tier: free-local|cheap-hosted|paid-agent|manual-approval
  max_input_tokens: 150000
  max_output_tokens: 30000
  max_total_tokens: 200000
  max_model_calls: 6
  max_retries: 1
  max_runner_minutes: 30
  max_cost_usd: 2.00
  approval_required_above_usd: 5.00
  context_bundle_sha: "sha256:..."
  cache_policy: reuse-summaries-first
  stop_on:
    - repeated_test_failure
    - context_missing
    - risk_escalation
    - budget_exceeded
```

## Provider selection matrix

| Worker | Prefer when | Avoid when |
|---|---|---|
| `ollama-local` | classification, summarization, mechanical docs, cheap pre-review | high-stakes reasoning or large missing context |
| `notebooklm` | source-heavy reading, cross-document synthesis, research notes | canonical repo writes, merge decisions, secret-bearing material |
| `gemini-cli` | large-context inspection or Google ecosystem workflows | small local tasks where cache/local model is enough |
| `claude-code-local` | local repo edits with a human nearby | unavailable local machine or broad unshaped work |
| `codex` | strong patch generation, cloud worktrees, code review feedback | vague work that has not passed Matt readiness |
| `jules` | GitHub-native issue-to-PR tasks | missing repo secret, missing human label, or governance-heavy work |
| `augment-code` | IDE-assisted targeted patching | fully unattended AFK work without harness evidence |

## Escalation rules

The router may escalate when:

- the issue is classified as `loop`;
- Matt readiness has `afk_ready: true`;
- budget cap is present;
- allowed paths and non-goals are present;
- a lower-cost worker produced insufficient evidence;
- the expected value justifies the next worker.

The router must stop or ask for approval when:

- the budget cap would be exceeded;
- risk becomes high or critical;
- policy, secrets, HALT, or merge authority is involved;
- required context is missing;
- repeated retries do not add new evidence;
- two agents would duplicate the same context burn.

## NotebookLM adapter boundary

NotebookLM is a research/read/write adapter, not a governance authority.

Allowed:

- read issue bundles, repo docs, architecture notes, prior PR summaries, and exported CI logs;
- produce research memos, Q&A notes, decision tables, comparison matrices, checklists, and source-grounded summaries;
- export results back to GitHub, Drive, or committed docs.

Not allowed by default:

- direct repository branch writes;
- direct merge decisions;
- use of secret-bearing logs or credentials as sources;
- serving as the only copy of a risk, HALT, authorization, or merge decision.

## MVP NotebookLM path

Until NotebookLM has a stable official API, the MVP path is manual-assisted:

1. Demerzel creates a source bundle.
2. A human imports or updates a NotebookLM notebook.
3. NotebookLM produces notes or tables.
4. The human exports or copies results back to GitHub, Drive, or repo docs.
5. Demerzel treats the exported artifact as evidence, not as authority.

Avoid brittle browser automation as the default integration path.

## Ledger requirement

Each routed job should emit a budget ledger artifact with:

- providers considered;
- providers used;
- estimated and actual token/cost fields where available;
- runner minutes;
- cache hits;
- escalations;
- stop reason;
- value artifacts produced.

See `examples/aiw-budget-ledger.example.json`.

## Non-goals

- This router does not own Demerzel policy.
- This router does not approve merges.
- This router does not override HALT.
- This router does not make paid or cloud workers the default.
- This router does not treat NotebookLM as the canonical source of truth.
