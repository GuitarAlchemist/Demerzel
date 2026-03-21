# Demerzel Patterns & Anti-Patterns

Living catalog of operational patterns discovered through governance cycles. Patterns are promoted from observations; anti-patterns are learned from failures.

## How Patterns Are Collected

```
Observation (driver cycle, audit, research)
    ↓ occurs 3+ times
Pattern Candidate (logged here with evidence)
    ↓ validated by /demerzel evolve
Confirmed Pattern (cited in policies)
    ↓ if critical enough
Policy Amendment or Constitutional Reference
```

## Pattern Format

Each pattern file follows: `{category}-{number}-{slug}.pattern.json`

```json
{
  "pattern_id": "category-NNN-slug",
  "category": "operational|governance|development|anti-pattern",
  "name": "Human-readable name",
  "description": "What this pattern is",
  "detection": "How to spot it",
  "action": "What to do when detected",
  "evidence": ["list of occurrences with dates"],
  "occurrence_count": 5,
  "first_seen": "2026-03-17",
  "last_seen": "2026-03-22",
  "status": "candidate|confirmed|promoted|deprecated",
  "belief_value": "T|F|U|C",
  "belief_confidence": 0.85
}
```

## Active Patterns

See individual files in this directory.

## Anti-Pattern Categories

- **Staleness:** artifacts that exist but are never updated
- **Coverage gaps:** things that should exist but don't
- **Ceremony:** governance artifacts that add process without value
- **Drift:** consumer repos diverging from governance standards
- **Meta-governance bloat:** governance about governance about governance
