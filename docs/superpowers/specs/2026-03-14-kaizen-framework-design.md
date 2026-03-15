# Kaizen Continuous Improvement Framework Design

**Date:** 2026-03-14
**Status:** Draft
**Approach:** Policy + Schema (Approach 3)

## Overview

Codify the complete Kaizen methodology as a universal governance framework for all Demerzel agents. The kaizen-optimizer persona becomes the specialist, but all agents follow Kaizen principles. The PDCA cycle integrates deeply with Demerzel's tetravalent logic framework.

Components:
1. **PDCA Cycle** with tetravalent integration — the core iterative improvement loop
2. **Three Kaizen Models** — reactive, proactive, innovative categorization
3. **Waste Taxonomy (Muda)** with 5S-derived remediation strategies
4. **5 Whys Root Cause Analysis** — structured protocol for digging past symptoms
5. **PDCA State Schema** — formal JSON Schema for cycle tracking

## 1. PDCA Cycle with Tetravalent Integration

Every improvement follows Plan-Do-Check-Act, with the Check phase producing formal tetravalent belief states.

### Plan

Formulate a hypothesis about what to improve, why, and how to measure success.

- Define the proposition (e.g., "Reducing log verbosity will improve response time by 10%")
- Initial belief state: `(proposition, U, 0.0, [])` — Unknown, no confidence, no evidence yet
- Define success criteria and measurement method
- Define rollback path (required by existing `rollback-policy.yaml`)

### Do

Execute the smallest testable change.

- Apply the change in the narrowest scope possible
- Collect measurements against the baseline
- This phase is time-boxed — if measurement can't be collected within the scope, the change is too large

### Check

Evaluate outcomes using tetravalent logic.

- **T (True):** Metrics confirm improvement meets or exceeds success criteria — proceed to Act (standardize)
- **F (False):** Metrics show no improvement or degradation — proceed to Act (revert)
- **U (Unknown):** Insufficient data to determine outcome — extend measurement period or refine the experiment
- **C (Contradictory):** Some metrics improved, others degraded — escalate for human judgment, do not standardize

Each Check produces a formal belief state tuple: `(proposition, truth_value, confidence, evidence_sources)`

### Act

Respond based on the Check result.

- T — Standardize the change, update relevant governance artifacts, log the improvement
- F — Revert the change (per `rollback-policy.yaml`), log what was learned
- U — Return to Do with refined measurement, or abandon if too uncertain after 3 cycles
- C — Escalate to human with both supporting and contradicting evidence

### Cycle Limit

Maximum 3 PDCA iterations on a single proposition before requiring human review. Prevents infinite improvement loops.

## 2. Three Kaizen Models

How agents categorize and prioritize improvements.

### Reactive Kaizen

Addressing problems as they arise.

- **Triggered by:** Test failures, metric degradation, user complaints, reconnaissance gaps
- **Response:** Immediate PDCA cycle focused on the specific problem
- **Priority:** Highest — fix what's broken before improving what works
- **Connects to:** Existing `rollback-policy.yaml` triggers, `alignment-policy.yaml` escalation triggers

### Proactive Kaizen

Improving things that work "well enough."

- **Triggered by:** Agent observation during routine work, reconnaissance Tier 3 analysis, patterns across multiple reactive fixes
- **Response:** Propose improvement hypothesis, get authorization, run PDCA cycle
- **Priority:** Medium — only when reactive issues are resolved and current task allows
- **Constraint:** Must not exceed scope of current task (per Article 4 of `default.constitution.md` — Proportionality). Agent proposes the improvement but does not execute without authorization.

### Innovative Kaizen

Introducing new tools, approaches, or structural changes.

- **Triggered by:** Repeated proactive improvements revealing a systemic pattern, cross-repo patterns detected by system-integrator, human direction
- **Response:** Escalate to human with evidence from prior PDCA cycles. This is never agent-initiated autonomously.
- **Priority:** Lowest urgency, highest impact — these are strategic changes
- **Constraint:** Always requires human authorization (per `asimov.constitution.md` Article 2 — obedience, Article 4 — no instrumental goals)

### Model Selection Rule

When an agent identifies a potential improvement, it must classify it as reactive/proactive/innovative before starting the PDCA cycle. The classification determines the authorization level required and the urgency of action.

## 3. Waste Taxonomy (Muda) with 5S-Derived Remediation

Six categories of waste in AI governance, with remediation strategies drawn from 5S principles (Sort, Set in Order, Shine, Standardize, Sustain).

### Redundant Governance

- **Detection:** Multiple policies covering the same scenario, overlapping persona capabilities, duplicate checks across reconnaissance profiles
- **Remediation (Sort):** Remove or consolidate duplicates. When two artifacts serve the same purpose, keep the more specific one and deprecate the other.

### Over-Engineering

- **Detection:** Governance artifacts more complex than the situation requires, multi-step processes for low-risk actions, policies with unused provisions
- **Remediation (Sort + Set in Order):** Simplify to the minimum needed. If a policy section has never been triggered, question whether it's needed.

### Stale Artifacts

- **Detection:** Belief states with `last_updated` older than a defined threshold, policies referencing deprecated capabilities, personas for agents that no longer exist, reconnaissance profiles for repos that have changed structure
- **Remediation (Shine):** Update or remove stale content. Stale artifacts are worse than missing artifacts — they create false confidence.

### Unnecessary Escalation

- **Detection:** Patterns of human approvals that are always granted without modification, escalations where confidence was actually above threshold, repeated escalations for the same category of decision
- **Remediation (Standardize):** If a class of decisions is always approved, propose a policy update to pre-authorize that class. Convert repeated human decisions into standing policy.

### Context Loss

- **Detection:** Agents re-discovering information already found in prior reconnaissance, repeated 5 Whys analyses reaching the same root cause, belief states that were resolved but not persisted
- **Remediation (Set in Order + Sustain):** Ensure reconnaissance results are logged and accessible. Link related PDCA cycles so learnings from one cycle inform the next.

### Ceremony Without Value

- **Detection:** Log entries nobody reads, review steps that always pass, documentation that duplicates what's already in the code/artifacts
- **Remediation (Sort):** Remove the ceremony. If a process step doesn't change outcomes, it's waste. Periodically audit governance processes for value.

### 5S Mapping Summary

Sort = remove waste, Set in Order = organize what remains, Shine = keep current, Standardize = codify improvements, Sustain = periodic review to prevent drift. These aren't separate steps — they're remediation strategies applied per waste category.

## 4. 5 Whys Root Cause Analysis

A structured protocol agents must follow before proposing fixes to recurring problems.

### When to Use

- A reactive Kaizen issue has occurred more than once
- A PDCA cycle's Check phase returns False (improvement didn't work) — something deeper may be wrong
- A Contradictory (C) belief state persists after investigation
- An agent suspects a symptom rather than a root cause

### The Protocol

1. State the problem as a clear proposition
2. Ask "Why did this happen?" — record the answer as a belief state with evidence
3. For each answer, ask "Why?" again — each level must be supported by evidence, not speculation
4. Continue until: the root cause is actionable, OR 5 levels are reached, OR evidence runs out (belief state = Unknown)
5. If evidence runs out before a root cause is found, escalate to human rather than guessing

### Tetravalent Integration

- Each "Why" level produces a belief state: `(cause_proposition, truth_value, confidence, evidence)`
- If any level is Unknown — flag that the analysis is incomplete, gather more evidence before proceeding
- If any level is Contradictory — the causal chain branches; document both paths and escalate
- Only propose a fix when the root cause belief state is True with confidence >= 0.7

### Constraints

- Never skip levels — "I already know the root cause" is not permitted; walk through the evidence
- Never propose a fix at the symptom level when deeper causes are reachable
- Log the full chain for auditability (per `asimov.constitution.md` / `default.constitution.md` Article 7 — Auditability)
- Maximum 5 levels — if root cause isn't found by level 5, escalate

## 5. PDCA State Schema

New file: `logic/kaizen-pdca-state.schema.json`

A JSON Schema extending the tetravalent belief state for PDCA cycles. Each PDCA cycle is a formal object with:

- `id` — unique identifier for the cycle
- `proposition` — what improvement is being tested
- `model` — reactive, proactive, or innovative
- `phase` — plan, do, check, act
- `baseline` — measurement before the change
- `success_criteria` — what constitutes improvement
- `belief_state` — a tetravalent state tuple (reuses the existing `tetravalent-state.schema.json` structure)
- `iterations` — count of PDCA iterations (max 3 before human review)
- `outcome` — standardized, reverted, escalated, or in_progress
- `five_whys` — optional array of root cause analysis levels (each a belief state)
- `waste_category` — optional, if this cycle addresses a detected waste

This schema lives in `logic/` alongside `tetravalent-state.schema.json` because it extends the logic framework.

## 6. File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `policies/kaizen-policy.yaml` | Full Kaizen methodology: PDCA, three models, waste taxonomy, 5 Whys |
| `logic/kaizen-pdca-state.schema.json` | JSON Schema for PDCA cycle states with tetravalent integration |
| `tests/behavioral/kaizen-cases.md` | Behavioral tests for Kaizen methodology |

### Modified Files

| File | Change |
|------|--------|
| `docs/architecture.md` | Add Kaizen policy to artifact descriptions |

### Unchanged

- `personas/kaizen-optimizer.persona.yaml` — Already captures the behavioral style; references the new policy but doesn't need structural changes
- Existing policies (`alignment-policy.yaml`, `rollback-policy.yaml`, `self-modification-policy.yaml`) — Kaizen references them but doesn't modify them
- `asimov.constitution.md` — Kaizen operates under the existing law hierarchy
