---
name: demerzel-metafix
description: Meta-fix — don't just fix the problem, fix the system that allowed the problem. Generalize fixes into patterns, policies, and prevention.
---

# Demerzel Meta-Fix — Fix the System, Not Just the Symptom

When you fix a bug, you fixed one instance. When you meta-fix, you prevent the entire class of bugs. This skill escalates every fix through 5 levels until the root cause is addressed systemically.

## Usage

`/demerzel metafix [description of what just broke]`
`/demerzel metafix --from-pattern [pattern-id]` — meta-fix a known anti-pattern
`/demerzel metafix --scan` — scan for fixable patterns across all state

## The 5 Levels of Fixing

```
Level 0: FIX THE INSTANCE
    "The meta-grammar link is broken"
    → Fix the link

Level 1: FIX THE BATCH
    "Are there other broken links?"
    → Scan and fix all broken links

Level 2: FIX THE DETECTION
    "Why didn't we catch this before it was visible?"
    → Add link verification to driver RECON phase

Level 3: FIX THE PREVENTION
    "Why did the link break in the first place?"
    → Add rename-tracking to the grammar prefix refactor process

Level 4: FIX THE SYSTEM
    "Why is this class of problem possible at all?"
    → Create readme-sync-policy + blind-spot-detection grammar
    → Wire into driver cycle so it's automated
```

**The meta-fix is not complete until you've reached Level 4.**

## Process

### Step 1: IDENTIFY the instance

What broke? Describe the specific problem.

```
Instance: [what happened]
Impact: [who was affected, what was wrong]
How discovered: [user noticed, audit caught, driver flagged]
```

### Step 2: FIX the instance (Level 0)

Fix the immediate problem. Commit with conventional style.

### Step 3: SCAN for siblings (Level 1)

Ask: "Is this the only instance, or are there others?"

- Search for the same pattern across all repos
- Check state/ for similar staleness patterns
- Check all READMEs for similar broken links
- Check all grammars/policies/schemas for similar inconsistencies

Fix all siblings found. Commit.

### Step 4: ADD detection (Level 2)

Ask: "How should we have caught this automatically?"

Options (pick the most appropriate):
- **Blind spot grammar production** — add a detection rule to `gov-blind-spot-detection.ebnf`
- **Staleness policy category** — add a new artifact category to `staleness-detection-policy.yaml`
- **Behavioral test** — add a test case that would catch this regression
- **Driver RECON check** — add a scan step to the driver skill
- **GitHub workflow** — add an automated check on push/PR

Implement the detection. Commit.

### Step 5: ADD prevention (Level 3)

Ask: "Why did this happen, and how do we prevent it?"

Common root causes and their preventions:

| Root Cause | Prevention |
|-----------|------------|
| Rename without link update | README sync policy — link check after refactors |
| New artifact without README | Coverage check — directories need READMEs |
| Stats drift from reality | Auto-count in COMPOUND phase |
| Cross-repo inconsistency | Galactic Protocol sync directives |
| Manual process skipped | Automate in driver cycle or GitHub workflow |
| Grammar gap | Research cycle grammar evolution (Step 6b) |
| No test coverage | Behavioral test for the scenario |

Implement prevention. Commit.

### Step 6: SYSTEMIZE (Level 4)

Ask: "What policy, grammar, or skill change ensures this entire class of problem is handled?"

Options:
- **New policy** — if this pattern recurs and needs formal rules
- **Grammar evolution** — add productions to detection grammars
- **Skill update** — update driver, audit, or report skills
- **Pattern catalog** — log in `state/patterns/` for future reference
- **Promotion candidate** — if the fix reveals something constitutional

Implement. Commit.

### Step 7: LOG the meta-fix

Create a meta-fix record in `state/patterns/`:

```json
{
  "pattern_id": "metafix-NNN-slug",
  "category": "metafix",
  "name": "Description of what was meta-fixed",
  "levels_completed": [0, 1, 2, 3, 4],
  "instance_fixed": "what broke",
  "siblings_found": N,
  "detection_added": "where detection was added",
  "prevention_added": "what prevention was added",
  "system_change": "what policy/grammar/skill was created or updated",
  "timestamp": "2026-03-22T00:00:00Z"
}
```

### Step 8: REPORT

Print meta-fix summary:

```
Meta-Fix Complete: [name]
Level 0 (instance): [what was fixed]
Level 1 (batch): [N siblings found and fixed]
Level 2 (detection): [what detection was added]
Level 3 (prevention): [what prevention was added]
Level 4 (system): [what system change was made]
Artifacts modified: [list]
Commits: [count]
```

## Scan Mode

`/demerzel metafix --scan` walks through known anti-patterns and checks:

1. Read all `state/patterns/anti-pattern-*.json`
2. For each, check if Levels 2-4 have been addressed
3. Report which anti-patterns still lack detection, prevention, or systemization
4. Prioritize by occurrence_count and recency

## Examples

### Example 1: Broken Grammar Link

```
Level 0: Fix meta-grammar.ebnf → core-meta-grammar.ebnf link in org README
Level 1: Scan all READMEs — found 5 more broken links from prefix rename
Level 2: Added link verification to driver RECON phase (readme-sync-policy)
Level 3: Added rename-tracking rule: "after git mv, grep for old name in all .md files"
Level 4: Created readme-sync-policy.yaml with automated sync fields + link check
```

### Example 2: Stale Conscience Signals

```
Level 0: Process 5 stale signals from 2026-03-17
Level 1: Found 30+ stale artifacts across state/
Level 2: Created staleness-detection-policy.yaml with per-category thresholds
Level 3: Added staleness scan to driver RECON phase
Level 4: Created gov-blind-spot-detection.ebnf grammar + patterns catalog
```

### Example 3: Empty Departments

```
Level 0: Produce course for music department
Level 1: Found 11 of 13 departments had no courses
Level 2: Added coverage check to blind-spot-detection grammar
Level 3: Created /seldon course-pipeline for automated production
Level 4: Created grammar-evolution-policy ensuring grammars drive course production
```

## Meta-Meta-Fix

If you find yourself repeatedly meta-fixing the same class of problem, that's a signal that the meta-fix system itself needs improvement:

- Are Level 4 changes actually preventing recurrence?
- Are patterns being logged but not acted on?
- Is the driver cycle actually running the detection checks?

This is the fixed-point question: does the meta-fix process meta-fix itself?

## Governance

- Article 7 (Auditability) — every meta-fix is logged with full 5-level trace
- Article 8 (Observability) — meta-fix count and level distribution are governance metrics
- Article 11 (Ethical Stewardship) — systemic fixes demonstrate care for long-term quality
- Staleness detection policy — meta-fix records have 30-day freshness threshold
- Grammar evolution policy — detection grammars evolve through meta-fix discoveries
