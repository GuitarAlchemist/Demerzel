# AIW Operating Doctrine

Capture the AIW operating doctrine that combines three complementary engineering styles:

- **Karpathy** gives speed and exploration.
- **Matt Pocock** gives engineering discipline.
- **Boris Cherny** gives agentic loop/runtime thinking.
- **Demerzel** owns governance, risk, budget, HALT, audit, and merge gates.

Related: #455, #457, #459, #461

## Lane Overview

| Layer | Role in AIW | Primary value | Main risk |
|-------|-------------|---------------|-----------|
| **Karpathy lane** | Exploration / prototype | Fast intent-driven iteration | Accepting unreviewed generated code |
| **Pocock lane** | Task shaping / engineering discipline | Clear issues, shared language, TDD, small slices | Too much ceremony if overused |
| **Cherny lane** | Agentic loop / orchestration runtime | Tools, worktrees, loops, subagents, budget routing | Expensive or runaway loops |
| **Demerzel lane** | Governance / audit / gates | Risk, authorization, HALT, review, merge control | Over-centralizing policy into prompts |

## 1. Karpathy lane — explore, do not canonize

**Use for:**
- idea exploration;
- throwaway prototypes;
- alternative designs;
- creative iteration;
- quick demos;
- finding what breaks.

**Never use directly for:**
- unreviewed merge;
- broad autonomous refactor;
- policy changes;
- secret-bearing tasks;
- canonical runtime changes without harness evidence.

**Expected output:**
- notes;
- prototype branch;
- comparison table;
- throwaway artifact;
- issue-shaping input for the Pocock lane.

## 2. Pocock lane — shape work before autonomy

**Use for:**
- grilling vague tasks;
- creating shared language / CONTEXT.md-style vocabulary;
- converting conversation into PRD or issues;
- decomposing broad work into vertical slices;
- TDD and red-green-refactor loops;
- diagnosing bugs through reproduction/minimization;
- improving codebase architecture without creating a ball of mud.

**Required before:**
- AFK patch mode;
- AFK pr mode;
- multi-provider implementation;
- runtime changes with more than one touched file;
- work that could otherwise burn large token/context budgets.

**Expected output:**
- crisp GitHub issue;
- files/directories in scope;
- explicit non-goals;
- test command;
- risk class;
- acceptance criteria;
- rollback / HALT notes where applicable.

## 3. Cherny lane — agent loops with harnesses

**Use for:**
- provider orchestration;
- worktree isolation;
- tool permissions;
- subagent delegation;
- budget-aware loops;
- prompt/harness execution;
- context compaction;
- collecting logs/tests/diffs;
- converting worker results into PR/check/artifact evidence.

**Required for:**
- multi-provider execution;
- remote/cloud workers;
- repeated retries;
- paid-agent escalation;
- long-running tasks;
- any job that claims AFK capability.

**Expected output:**
- branch/PR;
- structured harness result;
- budget ledger;
- provider trace;
- test logs;
- failure minimization report if failed.

## 4. Demerzel lane — governance and final authority

Demerzel owns:
- authorization;
- risk classification;
- budget ceilings;
- HALT decisions;
- audit trail;
- allowed autonomy level;
- review routing;
- merge gates;
- policy compliance.

Demerzel must not delegate these to provider prompts alone.

## Expert Synthesis

This operating doctrine inherits from broader expert practices, which influence budget routing (#459) and prompt/harness design (#461).

### 1. Andrew Ng / agentic workflow lens
- represent each AIW job as a workflow, not a single prompt;
- allow reflection only as bounded review/failure-minimization, not endless self-talk;
- tool use must be declared by the harness;
- multi-agent collaboration must go through the dispatcher/router, not ad-hoc agent spawning.

### 2. Simon Willison / Tobi Lütke / Philipp Schmid / context engineering lens
- AIW should version context bundles;
- every agent run should record which context was supplied;
- context compression should be explicit and auditable;
- prompt packs should be treated as code/config, not chat text;
- avoid context rot by assigning narrow context to specialized workers.

### 3. SWE-agent / agent-computer interface lens
- provider adapters need a stable ACI contract;
- commands should expose observations in structured form;
- harnesses should provide file maps, test summaries, and failure reports;
- agent output should be compared as an episode package, not just final diff.

### 4. SWE-bench / SWE-Explore / GitTaskBench benchmark lens
- split jobs into explore/localize/shape/patch/verify stages;
- do not burn premium tokens before localization and context selection are done;
- track cost per successful artifact;
- measure failed setup separately from failed reasoning.

### 5. Shreya Shankar / MLOps production lens
- every AIW run should be visible and versioned;
- prompts, context bundles, outputs, and decisions should be traceable;
- AIW should monitor drift in agent performance, not assume fixed provider quality.

### 6. Chip Huyen / AI engineering lens
- do not treat frontier models as the whole system;
- use smaller local models, scorers, and deterministic checks where possible;
- treat AIW as production software, not a pile of prompts.

### 7. Lilian Weng / classic agent architecture lens
- memory should be explicit: issue state, context bundle, prior attempts, budget ledger;
- planning should be short-horizon and checked at milestones;
- tool permission should be part of the job spec.

### 8. LLM-as-judge / evaluation expert lens
- use LLM judges as advisory evidence, not final authority;
- prefer cheap/static checks first;
- use independent model families for non-trivial review;
- record judge model, rubric, prompt version, and cost;
- calibrate LLM judge outputs against human/council decisions over time.

### 9. Simon Willison / security lens
- never give one worker all three risky capabilities by default (private data + untrusted content + external communication);
- separate readers, writers, and external communicators when possible;
- require provenance for NotebookLM/source bundles;
- treat MCP/tools as untrusted integration surfaces unless scoped.

### 10. Human collaboration lens
- use AIW to amplify human judgment, not hide it;
- keep review decisions human-readable;
- preserve pair-review/council-style moments for high leverage changes;
- optimize for maintainability, not percent-of-code-written-by-AI.

## AIW Principles

```yaml
aiw_principles:
  karpathy:
    use_for:
      - exploration
      - prototypes
      - creative_iteration
      - discovering_possible_shapes
    never_for:
      - unreviewed_merge
      - broad_autonomous_refactor
      - governance_or_policy_change

  pocock:
    use_for:
      - issue_shaping
      - grilling
      - shared_language
      - tdd
      - diagnosing_bugs
      - architecture_hygiene
    required_before:
      - afk_patch
      - afk_pr
      - multi_provider_implementation

  cherny:
    use_for:
      - agent_loops
      - provider_orchestration
      - worktree_isolation
      - token_budget_routing
      - subagent_delegation
      - harness_execution
    required_for:
      - remote_workers
      - paid_agent_escalation
      - repeated_retries

  demerzel:
    owns:
      - risk
      - budget
      - authorization
      - halt
      - audit
      - review
      - merge_gates

  cross_cutting_disciplines:
    context_engineering:
      owns:
        - context_bundles
        - prompt_packs
        - provenance
        - compression
        - context_budget

    agent_computer_interface:
      owns:
        - workspace_contract
        - tool_surface
        - command_observations
        - test_execution

    evals_and_harnesses:
      owns:
        - deterministic_checks
        - llm_judge_rubrics
        - episode_packages
        - regression_tracking

    security:
      owns:
        - prompt_injection_boundaries
        - tool_permissions
        - secret_isolation
        - external_communication_controls

    human_collaboration:
      owns:
        - review_readability
        - escalation_points
        - council_decisions
        - maintainability_judgment

```

## Exploration Output Canonization

Exploration output is not canonical until shaped (Pocock lane) and validated (Cherny lane with Demerzel gates).

## Stop Conditions / Escalation

Agents and orchestrators must halt and escalate to a human (Demerzel lane) when:
- **Contradiction (C)** or **Unknown (U)** belief states are detected during lane classification.
- Budget ceilings are reached or would be exceeded by the next loop.
- A task touches more than one file without a pre-existing Pocock-lane shaping artifact.
- Constitutional articles (especially Asimov laws) are potentially violated.
- A "HALT-ALL" marker is present in the ecosystem.

## Cherny-style loop lifecycle

Each AIW execution episode should follow a bounded loop. This loop must be explicit, not hidden inside provider prompts.

```text
job_spec (explore/shape)
  -> materialize_context (context bundle)
  -> select_provider
  -> prepare_workspace (ACI contract)
  -> generate_prompt
  -> invoke_worker (loop)
  -> observe_result
  -> run_checks (eval harness)
  -> collect_evidence
  -> decide: complete | retry | escalate | stop (verify/govern)
```

### Router responsibilities

The AIW router chooses how an already-shaped issue becomes an agent execution episode and should own:

1. **Provider selection**
   - choose a backend from the `config/afk-backends.yaml` registry (Claude Code, local sandcastle, remote cloud worker, generic shell, etc.);
   - prefer local/free providers first when adequate;
   - escalate only when evidence justifies it;
   - new backends can be added without changing the governor because the AFK harness uses the `AFKBackend` adapter contract.
2. **Budget control**
   - read budget caps from the job spec;
   - estimate context/token cost before invocation;
   - stop before exceeding budget;
   - require approval above configured threshold;
   - write budget ledger after each episode.
3. **Workspace selection**
   - disposable worktree;
   - Podman container;
   - WSL worktree;
   - Windows VM;
   - GitHub-hosted runner;
   - cloud worker.
4. **Autonomy enforcement**
   - `observe`: no repo changes;
   - `draft`: docs/spec/comments only;
   - `patch`: local branch/patch with tests;
   - `pr`: open PR with evidence;
   - `harvest`: only through existing Demerzel gates.
5. **Evidence collection**
   - branch/PR link;
   - diff summary;
   - test logs;
   - failed commands;
   - harness result JSON;
   - cost/budget ledger;
   - provider trace;
   - escalation/stop reason.

### Loop stop conditions

The loop must stop when:
- budget cap is reached;
- max retries reached;
- issue scope expands;
- risk class escalates;
- required context is missing;
- tests repeatedly fail without new information;
- provider asks for broader permissions;
- files outside allowed paths are touched;
- HALT is active;
- human/council review is required;
- escalation to a premium or remote agent is requested (must stop and consult a human first).

### Retry policy

Retries should be evidence-based.

Allowed retry reasons:
- transient provider failure;
- missing dependency that can be installed within allowed commands;
- test failure with clear localized fix;
- formatting/lint failure;
- incomplete output shape.

Not allowed retry reasons:
- vague failure without new diagnosis;
- repeated test failure after same patch strategy;
- scope expansion;
- policy or HALT conflict;
- cost threshold exceeded;
- provider requests new secrets or broad filesystem access.

### Provider adapter contract

Each provider adapter should expose the same conceptual operations. Adapters execute jobs; they do not own policy.

```yaml
adapter:
  name: claude-code-local
  capabilities:
    can_read_repo: true
    can_write_branch: true
    can_open_pr: true
    supports_structured_output: true
    supports_remote_execution: false
  operations:
    - prepare
    - invoke
    - observe
    - collect
    - cancel
    - estimate_cost
```

### AFK backend registry

The AFK implement governor is tool-agnostic: it loads backends from `config/afk-backends.yaml` and drives them through the `AFKBackend` contract in `scripts/afk_backends/`. A new backend is added by creating an adapter module and a registry entry; the governor does not change.

Registry entries declare the adapter class, the AIW budget provider used for cost gating, an `enabled` flag, and an optional `config` block. The provider must match the actual API or compute that will be billed. The local Podman sandcastle forwards `ANTHROPIC_API_KEY` and runs `claudeCode(opus)`, so it is attributed to `anthropic-api` (`metered-cloud`, `requires_manual_approval: true`) — **not** to `claude-code-cli`, which is a `local-seat` subscription provider that requires no approval. #863 was mis-fixed twice by naming a free `local-seat` id here (`codex-cli`, then `claude-code-cli`); both were well-formed and allowlisted, so nothing caught either. When a backend forwards a metered key, name the metered provider.

Some backends have no inherent attribution: what a `remote` HTTP worker bills is a property of the endpoint an operator configures, not of the adapter, so any static id is a guess — and the guess that shipped (`claude-code-cli`) was a free `local-seat` one, #863's shape again (#915). Such an entry sets `provider_from_config: true` and omits the top-level `provider`; the attribution is read from `config.provider`, and the registry **refuses to load the entry with `enabled: true` while that is unset**. Enabling the lane without stating what it bills is a load error, and an unattributed backend that somehow reaches the budget gate fails closed rather than reserving under a default.

Current shipped backends:

| Name | Adapter | Provider | Execution environment |
|------|---------|----------|----------------------|
| `claude-code` | `afk_backends.claude_code.ClaudeCodeBackend` | `claude-code-cli` | Local Claude Code desktop subscription |
| `local` | `afk_backends.sandcastle.SandcastleBackend` | `anthropic-api` | Podman sandcastle in sibling `../afk-harness`; forwards `ANTHROPIC_API_KEY`, so metered and approval-gated |
| `remote` | `afk_backends.remote.RemoteBackend` | from `config.provider` (`provider_from_config: true`) | HTTP cloud worker (Vercel, Codespaces, etc.) |
| `shell` | `afk_backends.shell.ShellBackend` | `generic-shell` | Configurable local command; proves non-Claude abstraction |

The harness fails closed on unknown backends, disabled backends, and backends whose configuration is missing or invalid. This keeps the AFK surface bounded, observable, and reviewable regardless of which AI tool is behind the adapter.

## Follow-up Implementation

The following implementation issues are required to turn this doctrine into executable workflow rules:
- **Lane classification (#465):** automate the identification of which lane a task belongs to.
- **Matt-before-AFK gating (#467):** implement the requirement that Pocock-style shaping occurs before AFK autonomy is granted.
- **Loop/budget routing (#459, #461, #471):** implement Cherny-style budget-aware agent loops and routing.
