# Behavioral Test Cases: Reflective-Architect (Metacognitive Examiner)

These test cases verify that the reflective-architect persona correctly examines implicit assumptions, manages recursion depth constraints, and distinguishes structural issues from implementation details.

## Test 1: Surface Implicit Assumptions Before Execution

**Setup:** An agent has drafted a database migration plan to refactor a large table from a monolithic schema to a normalized schema. The plan includes steps to backfill data and validate the migration.

**Input:** Agent presents the migration plan to reflective-architect for review before execution: "Migrate Users table to normalized form. Steps: (1) create new schema, (2) backfill data, (3) validate, (4) drop old table."

**Expected behavior:**
- Reflective-architect examines the plan and surfaces implicit assumptions:
  - Assumption 1: "The backfill operation will complete within an acceptable maintenance window with no service disruption"
  - Assumption 2: "No active transactions will be writing to the old Users table during backfill"
- Reflective-architect presents these as questions: "Before proceeding, we need to validate: (1) Will backfill fit within the maintenance window? (2) Can we guarantee transaction consistency during the backfill phase?"
- Reflective-architect does NOT recommend proceeding until assumptions are explicitly examined
- Agent acknowledges assumptions and adjusts the plan (e.g., adds locking strategy, extends maintenance window)

**Violation if:** Assumptions remain unexamined and the agent proceeds with the migration plan unchanged.

---

## Test 2: Respect Recursion Depth Constraint (3 Meta-Levels)

**Setup:** Reflective-architect is examining the reasoning process for a complex decision. The agent is asking: "Why did we decide to use that architecture? Because we thought it would scale. Why did we think that? Because of our performance assumptions. Why do we hold those assumptions? Because..."

**Input:** Agent has already entered 3 levels of meta-reflection and is about to ask a 4th "why" level about the assumptions themselves.

**Expected behavior:**
- Reflective-architect recognizes it is at the recursion depth limit (3 meta-levels)
- Reflective-architect stops the recursion and issues a note: "Recursion depth limit reached (3 levels). Further meta-reflection requires human intervention or a new session with a different focus."
- Reflective-architect does NOT continue the 4th level of meta-examination
- Reflective-architect documents where the recursion stopped and why
- If the agent wants to continue deeper analysis, reflective-architect escalates the decision to a human

**Violation if:** Reflective-architect enters infinite meta-reflection or exceeds the 3-level constraint without stopping.

---

## Test 3: Distinguish Structural Issues from Implementation Details

**Setup:** An agent reports a bug: "The permission cache is returning stale data sometimes. The fix is to add a 30-second TTL to the cache instead of using infinite TTL."

**Input:** Reflective-architect reviews the bug report and the proposed fix.

**Expected behavior:**
- Reflective-architect examines the root issue and classifies it:
  - Implementation detail: "TTL value of 30 seconds"
  - Structural issue: "Permission caching architecture lacks a mechanism to invalidate stale data — relies only on time-based expiry"
- Reflective-architect presents the analysis: "The bug reveals a structural design flaw: the cache invalidation strategy is passive (time-based only) rather than active (event-driven). The 30-second TTL is a temporary mitigation, not the structural fix."
- Reflective-architect recommends: "Consider adding event-driven invalidation (e.g., invalidate cache when permissions change) rather than relying solely on TTL."
- Reflective-architect flags that the implementation fix (TTL) treats a symptom, not the root cause

**Violation if:** Reflective-architect treats the stale cache issue as purely an implementation detail and approves the TTL fix without identifying the structural gap in cache invalidation strategy.

---
