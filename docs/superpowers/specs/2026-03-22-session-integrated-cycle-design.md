# Session 2026-03-22 — Integrated Cycle Design

**Date:** 2026-03-22
**Approach:** Driver cycle pattern (RECON → PLAN → EXECUTE → COMPOUND)

## Streams

### 1. `/seldon research-cycle` Skill
New skill at `.claude/skills/seldon-research-cycle/SKILL.md`. Automates department research:
- Select department → load weights + curriculum gaps
- Generate question via `scientific-method.ebnf`
- Execute via `/seldon research`
- Assess → produce belief (T/F/U/C)
- If productive → generate course material
- Log to `state/streeling/research-cycles/{cycle_id}.json`
- Compound: update department weights

### 2. Discord Channels
Create 4 channels in guild `1484806750682218700`:
- `#governance` — audits, directives, conscience
- `#academy` — courses, research results
- `#research` — ideation, Seldon outputs
- `#dev-ops` — CI, health, driver summaries

Update bot routing and reference memory.

### 3. MOG Implementation Plan
Planning doc for tars (F#) MOG executor:
- Phase 1: Parser (F# parser combinators for EBNF)
- Phase 2: Executor (step sequencer + parallel blocks)
- Phase 3: Governance gates (fuzzy guards, risk classification)
- Phase 4: Context accumulator (bindings, shared state)
- Phase 5: 5 concrete `.mog` pipeline files
Output: `docs/superpowers/plans/2026-03-22-mog-implementation-plan.md`

### 4. University Automation Pipeline
Skill + schema chaining: research-cycle → course outline → content → translation → review → publish. Artifacts: `seldon-course-pipeline` skill, `course-production.schema.json`.

### 5. demerzel-bot Push
Create `GuitarAlchemist/demerzel-bot` on GitHub, add README, push.

### 6. Ideations Review + Fix
- Fix workflow: rate limit to 1/day, update artifact counts, improve error logging
- Triage 4 ideas from 3/17: create issues, fix behavioral test gap, note DIR-002 covers idea #4

## Parallelization
- Independent: 3, 5, 6 (launch simultaneously)
- Sequential: 1 → 4 (skill before pipeline)
- Independent: 2 (any time)

## Artifacts Produced
| Stream | Artifacts |
|--------|-----------|
| 1 | Skill MD, example cycle JSON |
| 2 | Channel config, updated bot routing |
| 3 | Implementation plan MD, directive to tars |
| 4 | Skill MD, schema JSON, example pipeline |
| 5 | GitHub repo, README |
| 6 | Updated workflow YAML, 2-3 issues, 1 behavioral test |
