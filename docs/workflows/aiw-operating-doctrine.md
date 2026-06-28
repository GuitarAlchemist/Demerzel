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
```

## Exploration Output Canonization

Exploration output is not canonical until shaped (Pocock lane) and validated (Cherny lane with Demerzel gates).

## Follow-up Implementation

The following implementation issues are required to turn this doctrine into executable workflow rules:
- Lane classification: automate the identification of which lane a task belongs to.
- Matt-before-AFK gating: implement the requirement that Pocock-style shaping occurs before AFK autonomy is granted.
- Loop/budget routing: implement Cherny-style budget-aware agent loops and routing.
