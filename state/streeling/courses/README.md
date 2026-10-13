# Streeling University — Course Catalog

## Structure

```
courses/
  {department}/           # One directory per department
    en/                   # English (primary)
    es/                   # Spanish
    pt/                   # Portuguese
    fr/                   # French
    it/                   # Italian
    de/                   # German
```

**Naming convention:** `{DEPT-CODE}-{SEQ}-{slug}.{lang}.md` (e.g., `gaa-001-your-first-chord.es.md`)

## Available Courses

### Guitar Alchemist Academy

| Code | Title | Level | Duration | Languages |
|------|-------|-------|----------|-----------|
| [GAA-001](guitar-alchemist-academy/en/gaa-001-your-first-chord.md) | Your First Chord — E Minor | Beginner | 20 min | en, es, pt, fr, it, de |

**Curriculum path:** Nigredo (Beginner) → Albedo (Intermediate) → Citrinitas (Advanced) → Rubedo (Master)

### Psychohistory

| Code | Title | Level | Duration | Languages |
|------|-------|-------|----------|-----------|
| [PSY-001](psychohistory/en/psy-001-intro-fractal-compounding.md) | Introduction to Fractal Compounding | Intermediate | 30 min | en, es, pt, fr, it, de |

**Curriculum path:** Foundations → Statistical Mechanics → Power Laws → Phase Transitions → Crisis Prediction

## Current inventory

The sample rows above do not enumerate all modules. Run
`python scripts/streeling_course_progress.py` from the Demerzel repository root
for current counts and per-department gaps. Source files, language coverage,
review verdicts, and public Learn readback are separate measures. The 25-course
target currently uses the 21 course directories; the university registry and
department records disagree about the department set. See
[`docs/specs/streeling-project-curriculum-2026-10-04.md`](../../../docs/specs/streeling-project-curriculum-2026-10-04.md)
for the counting rule and open scope decision.

## How Courses Are Produced

```
/seldon research-cycle [dept]     # Generate research question, investigate, assess
        ↓
/seldon course-pipeline [dept]    # Outline → content → translate → review → publish
        ↓
courses/{dept}/{lang}/{code}.md   # Published course in 6 languages
```

See: [`seldon-research-cycle`](../../.claude/skills/seldon-research-cycle/SKILL.md) and [`seldon-course-pipeline`](../../.claude/skills/seldon-course-pipeline/SKILL.md)

## Quality Standards

- Courses require research cycle with `belief_confidence >= 0.5`
- Auto-publish at `>= 0.7` confidence; human review for `0.5-0.7`
- Each course must have practice exercises
- Translations follow [multilingual policy](../../policies/multilingual-policy.yaml) with cultural adaptation
- All courses reference their source research cycle for traceability
