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

## Executable preflight

The policy is executable before a provider is invoked. `state/driver/aiw-budget-policy.json`
allowlists the worker tiers and keeps local-seat tools first. The policy, ledgers,
approval artifact, and receipt are pinned to canonical repository paths; a caller
may pass them explicitly but cannot redirect them to a caller-controlled file. Run
the gate with a job request that contains the estimated tokens, calls, retries,
runner minutes, and estimated cost:

```powershell
python scripts/aiw_budget_gate.py `
  --policy state/driver/aiw-budget-policy.json `
  --request .octo/aiw-request.json `
  --ledger .octo/aiw-budget-ledger.json `
  --cycle-ledger .octo/aiw-cycle-ledger.json
```

Exit `0` is the only allowed path to invocation. Exit `1` blocks the job before
the provider call; exit `2` means the request or policy is invalid. Metered cloud
workers (`gemini-cli`, `jules`, `notebooklm`) require explicit approval even when
their estimate is below the per-job cap. Approval is **not** a self-attested flag
in the request: it is a separate `.octo/aiw-approval.json` artifact bound to the
job id, provider, and exact request SHA-256; a `manual_approval` key inside the
request is rejected. Claude Code CLI and Codex CLI are the preferred first workers
for local-seat work; an `ANTHROPIC_API_KEY` fallback must carry the same budget
block and approval rules.

The cycle ledger is authoritative and reserved atomically before invocation;
callers cannot supply their own aggregate spend or concurrency values. A
reservation is bound to its provider and request SHA-256, so a reused job id
cannot inherit an old grant under a changed request. On terminal completion,
release the reservation. Metered providers must supply a trusted
`.octo/aiw-receipt.json` receipt whose issuer matches the policy's
`trusted_receipt_issuer` and whose actual cost matches the released amount;
spend over the reservation's admitted cap is recorded truthfully but returned as a
blocking `over_budget` decision:

```powershell
python scripts/aiw_budget_gate.py --release-job aiw-0001 `
  --actual-cost-usd 0.00 --cycle-ledger .octo/aiw-cycle-ledger.json `
  --policy state/driver/aiw-budget-policy.json `
  --request .octo/aiw-request.json --ledger .octo/aiw-budget-ledger.json `
  --receipt .octo/aiw-receipt.json
```

### Live consumer

`.github/workflows/jules-auto-delegate.yml` is the first live consumer of the gate.
Jules is a `metered-cloud` provider, so the delegation job runs the reserve
preflight before invoking `google-labs-code/jules-action`:

- **allow (exit 0)** → delegation proceeds;
- **block (exit 1)** → the job comments on the issue that a committed
  `.octo/aiw-approval.json` (bound to the job id, provider, and request SHA-256)
  is required, keeps the labels, writes no delegation marker, and stays green so
  the issue remains re-runnable after approval;
- **invalid (exit 2)** → the job fails closed.

`scripts/test_aiw_budget_consumer.py` guards this wiring so the gate cannot be
silently unwired back into a declared-but-unconsumed artifact.

## Trust boundary

The gate validates the approval (`.octo/aiw-approval.json`) and the receipt
(`.octo/aiw-receipt.json`) by **field equality** — the approval must match the
job id, provider, and request SHA-256; the receipt's `issuer` must equal the
policy's `trusted_receipt_issuer` and its actual cost must match the released
amount. This is an **integrity** check, not an **authenticity** one: there is no
cryptographic signature, so the gate cannot itself tell a genuine receipt from a
forged JSON file with the right fields.

Authenticity therefore comes from **git-commit provenance, not from the gate**:

- **Approval and receipt artifacts must be committed** to the repository (a
  human-reviewed PR / an orchestrator step running under separate credentials),
  never written at runtime by the worker they authorize. Committing requires
  review, and review — not the string comparison — is what makes the artifact
  trustworthy. **The requesting job must not be able to write or commit these**;
  that separation is enforced by ordinary PR review and branch protection, and it
  is the property the whole metered-spend guarantee rests on.
- **Runtime ledgers are the opposite** — `.octo/aiw-budget-ledger.json`,
  `.octo/aiw-cycle-ledger.json`, and `*.lock` are per-run state, are gitignored,
  and must never be committed. A committed ledger would be stale, caller-authored
  authority — exactly what the boundary excludes.

**Decision (accepted for the current threat model):** where `.octo/` approval and
receipt artifacts originate from committed, reviewed sources and the worker cannot
commit them, the git + filesystem boundary is sufficient. Cryptographically signed
receipts / approvals (e.g. an HMAC or Sigstore attestation the gate verifies) are
a **future hardening, not a requirement today** — see Non-goals. A consumer must
not read the gate's field-equality checks as cryptographic trust.

## Non-goals

- This router does not own Demerzel policy.
- This router does not approve merges.
- This router does not override HALT.
- This router does not make paid or cloud workers the default.
- This router does not treat NotebookLM as the canonical source of truth.
- This router does not cryptographically sign approvals or receipts today —
  their authenticity comes from git-commit provenance, not the gate (see
  [Trust boundary](#trust-boundary)); signed attestations are a future option.
