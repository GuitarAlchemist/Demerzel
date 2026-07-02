# Seldon Engineering Intelligence Platform

**Status:** Draft / Phase 0
**Component:** Seldon
**Role:** Learn
**Precedence:** Advisory

## Overview

Seldon is the engineering intelligence platform for the Harness. While **Streeling** observes events and **Demerzel** decides on policy, **Seldon**'s job is to **learn** from the ecosystem's operation.

Seldon consumes normalized events (via Streeling), analyzes them for patterns, computes engineering KPIs, and emits advisory recommendations to Demerzel.

### Responsibility Split

| Component | Role | Action |
|---|---|---|
| **Streeling** | Observe | Emit normalized event stream |
| **Seldon** | Learn | Turn events into metrics, patterns, and recommendations |
| **Demerzel** | Decide | Policy enforcement and routing decisions |
| **IX** | Optimize | Implementation and forge execution |
| **Human** | Architect | Final authority and system design |

## Core Principles

1. **Advisory, not Authoritative:** Seldon recommends; Demerzel decides. Seldon does not mutate GitHub state or dispatch work.
2. **Outcome-Oriented:** Metrics are derived from observed outcomes (merges, reverts, CI failures), not just activity.
3. **Multi-Model Neutrality:** Seldon evaluates all workers (Claude, Jules, Gemini, Human, etc.) using the same objective criteria.
4. **Harness-Driven:** All intelligence is grounded in the Harness substrate (SessionEvents, Streeling records).

## Intelligence Domains

1. **Engineering KPI Catalog:** Continuous tracking of delivery speed, quality, and cost.
2. **Capability Scoring:** Mathematical modeling of worker effectiveness per capability.
3. **Worker Reliability:** Tracking completion rates and failure frequencies.
4. **Review Effectiveness:** Measuring the impact and accuracy of peer reviews.
5. **Routing Recommendations:** Proposing the best worker for a given task based on historical data.
6. **Policy Suggestions:** Periodic recommendations to adjust governance weights and thresholds.

## Artifacts

- [Metric Catalog](./metric-catalog.md)
- [Capability Scoring Design](./capability-scoring-design.md)
- [Worker Reliability Metrics](./worker-reliability-metrics.md)
- [Review Effectiveness Metrics](./review-effectiveness-metrics.md)
- [Routing Recommendation Contract](../schemas/routing-recommendation.schema.json)
- [Policy Improvement Loop](./policy-improvement-loop.md)
