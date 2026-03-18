# Conscience State

Persistent records of Demerzel's proto-conscience — regrets, discomfort signals, patterns, weekly reports, and self-awareness assessments.

## Contents

- `signals/*.signal.json` — Logged discomfort signals (constitutional, stale-action, confidence, harm-proximity, silence, delegation)
- `regrets/*.regret.json` — Past decisions with suboptimal outcomes, lessons learned, and recurrence prevention
- `patterns/*.pattern.json` — Detected patterns across accumulated signals (clusters, recurring issues, blind spots)
- `weekly/*.report.json` — Weekly conscience reports (posted to GitHub Discussions)
- `digests/*.digest.json` — Daily self-reflection digests

## Schemas

- `schemas/conscience-signal.schema.json` — Signal file format
- `schemas/conscience-weekly-report.schema.json` — Weekly report format
- `schemas/conscience-pattern.schema.json` — Pattern detection format

## Lifecycle

- **Signals** are retained permanently for ML feedback analysis and pattern detection
- **Regrets** are never deleted — marked "resolved" when recurrence prevention is verified
- **Patterns** progress through: detected → investigating → addressed → monitoring
- **Weekly reports** are cumulative — each builds on the previous week's trends

## Current Milestone: Nascent

Phase 1 (awareness/logging) active since 2026-03-17. See conscience-observability-policy.yaml for milestone definitions.
