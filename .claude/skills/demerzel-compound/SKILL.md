---
name: demerzel-compound
description: Run a meta-compounding cycle — scan evolution log, detect promotions/demotions, assess governance effectiveness, propose self-improvements
---

# Demerzel Meta-Compounding Cycle

Run a full governance compounding cycle. This is how Demerzel improves her own governance — recursively, based on evidence.

## Usage
`/demerzel compound` — run full cycle
`/demerzel compound scan` — just scan for candidates without proposing changes
`/demerzel compound promote` — show promotion candidates only
`/demerzel compound waste` — show deprecation/waste candidates only

## The Compounding Cycle

```
1. Scan evolution log
       ↓
2. Detect promotion candidates (pattern → policy → constitutional)
       ↓
3. Detect deprecation candidates (unused, stale, redundant)
       ↓
4. Assess confidence calibration accuracy
       ↓
5. Evaluate governance effectiveness per artifact
       ↓
6. Propose self-improvements (Kaizen proactive/innovative)
       ↓
7. Log results back to evolution log (the loop compounds itself)
```

## Step 1: Scan Evolution Log

Read all files from `state/evolution/` — this is Demerzel's live evolution log. Fall back to `examples/sample-data/governance-evolution-seed.json` only if `state/evolution/` is empty.

For each artifact, check:
- `citation_count` — how often cited in governance decisions
- `violation_count` — how often violated
- `compliance_rate` — violations / total assessments
- `last_cited` — when was it last relevant?
- `events` — what has happened to this artifact?

## Step 2: Detect Promotion Candidates

**Pattern → Policy promotion (evidence-based):**
- Look for operational patterns appearing in 3+ PDCA cycles, reconnaissance findings, or compliance decisions
- Check: is there a governance gap that a new policy would fill?
- Threshold: 3+ appearances with measurable positive impact

**Policy → Constitutional promotion (human judgment required):**
- Look for policies with: 100% compliance rate, high citation count, sustained effectiveness
- Check: would violation of this policy constitute fundamental harm?
- Threshold: sustained inviolability + no exceptions in evolution log
- NOTE: This only generates a proposal — human must approve

## Step 3: Detect Deprecation Candidates

Apply Kaizen waste taxonomy:
- **Ceremony without value:** Artifacts with zero citations for 90+ days
- **Redundant governance:** Multiple artifacts covering the same concern
- **Stale artifacts:** Artifacts referencing deprecated capabilities
- **Over-engineering:** Policies with unused provisions

Flag but do NOT auto-deprecate. Generate a proposal for review.

## Step 4: Assess Confidence Calibration

Review recent governance decisions for calibration accuracy:
- Were high-confidence decisions actually correct?
- Were low-confidence decisions appropriately escalated?
- Is any agent systematically over- or under-confident?

Uses the confidence calibration protocol from `policies/scientific-objectivity-policy.yaml`.

## Step 5: Evaluate Governance Effectiveness

For each artifact, update the assessment:
- `effectiveness`: T (clearly effective), F (ineffective), U (not enough data), C (mixed results)
- `recommendation`: maintain, promote, demote, deprecate, investigate

Use tetravalent logic — don't force binary judgments:
- Unknown (U) is fine for new artifacts — it means "gather more data"
- Contradictory (C) is important to surface — don't average away mixed results

## Step 6: Propose Self-Improvements

Based on findings, propose concrete improvements:

**Proactive Kaizen** (Demerzel can propose, skeptical-auditor reviews):
- New policies for frequently-used patterns
- Policy refinements based on usage data
- Schema updates for better validation

**Innovative Kaizen** (requires human authorization):
- Constitutional amendments for proven-inviolable policies
- Structural changes to the governance framework
- New personas for ungoverned capabilities

Each proposal follows PDCA:
- Plan: hypothesis about what to improve
- Do: smallest testable change
- Check: measure impact via evolution log
- Act: standardize or revert

## Step 7: Log Results

Update the evolution log with:
- New events (type: "compounding_cycle") on each assessed artifact
- Updated metrics (citation counts, compliance rates)
- Updated assessments (effectiveness, recommendations)
- Proposals generated (with evidence and confidence)

This is the recursive part — the compounding cycle's own results feed into the next cycle.

## Output Format

```
=== Demerzel Meta-Compounding Cycle ===
Date: [today]

PROMOTION CANDIDATES:
  [list with evidence]

DEPRECATION CANDIDATES:
  [list with evidence]

CALIBRATION ASSESSMENT:
  [accuracy report]

EFFECTIVENESS SUMMARY:
  | Artifact | Effectiveness | Recommendation |
  [table]

PROPOSED IMPROVEMENTS:
  [list with PDCA format]

CYCLE LOGGED: [count] artifacts updated
```

## Scheduling

Run after the weekly harvest — the harvest provides fresh data for the compounding cycle.

Add to Streeling workflow or run manually:
```
CronCreate("47 13 * * 5", "/demerzel compound")
```
(Runs Fridays at 8:47 AM EST, 30 minutes after the harvest)

## Integration

- **Reads from:** governance evolution log, Kaizen waste taxonomy, confidence calibration protocol
- **Writes to:** governance evolution log (updated assessments and events)
- **Feeds into:** `/demerzel promote` for promotion proposals, `/demerzel evolve` for evolution insights
- **Governed by:** Asimov constitution (can't self-modify constitutions), Demerzel mandate (self-governance requires external review)

## Constitutional Constraint

Demerzel CANNOT approve her own constitutional changes. Per the mandate:
- Self-governance requires skeptical-auditor review (routine)
- Constitutional promotions require human approval (always)
- The compounding cycle proposes — it never unilaterally changes governance

## State Maintenance (MANDATORY)

The compounding cycle is the primary writer of evolution state. It MUST:

### Before Cycling
1. Read ALL files from `state/evolution/` — this is the input
2. Read recent beliefs from `state/beliefs/` for context
3. Read any PDCA records from `state/pdca/` for improvement tracking

### After Cycling
1. **Update evolution files** in `state/evolution/` — add new events, update metrics, refresh assessments
2. **Create PDCA records** in `state/pdca/` for each proposed improvement
3. **Update beliefs** in `state/beliefs/` if the cycle revealed new truths
4. **Never delete** evolution entries — append events, update metrics in place

### The Compound Loop
Each cycle's output is the next cycle's input. The evolution log grows richer over time:
- Cycle N finds alignment-policy has 3 citations → marks as promotion candidate
- Cycle N+1 sees the promotion candidate flag → evaluates if threshold sustained
- Cycle N+2 either promotes or downgrades based on accumulated evidence

## Source
`logic/governance-evolution.schema.json`, `policies/scientific-objectivity-policy.yaml` (confidence calibration), `policies/kaizen-policy.yaml` (waste taxonomy, PDCA), `constitutions/demerzel-mandate.md` Section 4 (accountability)
