---
name: seldon-course-pipeline
description: End-to-end university course production — research findings to published multilingual course material with review gates
---

# Seldon Course Pipeline — Automated Course Production

Chains research findings into published course material through a governed pipeline with quality gates.

## Usage

`/seldon course-pipeline [department]` — run full pipeline for department (triggers research-cycle first)
`/seldon course-pipeline --from-cycle [cycle_id]` — produce course from an existing research cycle
`/seldon course-pipeline batch [department]` — produce courses for all confirmed findings lacking courses

## Pipeline

```
RESEARCH ──→ OUTLINE ──→ CONTENT ──→ TRANSLATE ──→ REVIEW ──→ PUBLISH
   │            │           │            │            │          │
   └─ /seldon   └─ structure └─ write    └─ ES/PT/FR  └─ quality  └─ commit
     research-     sections     full       cultural      gate       + log
     cycle         + duration   module     adaptation    (>0.7)
```

## Phase 1: RESEARCH

If `--from-cycle` is provided, load the existing cycle from `state/streeling/research-cycles/{cycle_id}.json`.

Otherwise, invoke `/seldon research-cycle [department]` to run a fresh research cycle.

**Gate:** Research must produce `confirm` or `discover_question` conclusion with confidence >= 0.5. If not, pipeline stops with status `rejected` and logs the reason.

## Phase 2: OUTLINE

Generate a course outline from research findings:

1. Read department curriculum (`state/streeling/departments/{dept}.department.json`)
2. Check existing courses to avoid duplication (`state/streeling/courses/{dept}/en/`)
3. Determine level (beginner/intermediate/advanced) based on:
   - If finding extends a beginner topic → intermediate
   - If finding is foundational → beginner
   - If finding requires prior courses → advanced
4. Structure into sections (3-6 sections, 15-45 min total)
5. Plan practice exercises (at least 1 per main section)

**Output:** Outline object with section titles, estimated durations, exercise sketches.

## Phase 3: CONTENT

Write the full course module in English following the standard format:

```markdown
---
module_id: {dept-code}-{sequence}-{slug}
department: {department}
course: "{curriculum area}"
level: {level}
prerequisites: [{list}]
estimated_duration: "{N} minutes"
produced_by: seldon-course-pipeline
research_cycle: {cycle_id}
pipeline_id: {pipeline_id}
version: "1.0.0"
---

# {Title}

> **{Department Full Name}** | Level: {level} | Duration: {duration}

## Objectives
[3-5 learning objectives]

---

## {Sections with content}

### Practice Exercise
[Hands-on exercises]

---

## Key Takeaways

## Further Reading

---
*Produced by Seldon Course Pipeline {pipeline_id}.*
*Research: {cycle_id} | Belief: {value} ({confidence})*
```

**Content quality requirements:**
- Factual claims must trace to research evidence
- Examples must be concrete, not abstract
- Practice exercises must be doable without special tools (for music: just a guitar)
- Tone matches department persona's voice settings
- No unexplained jargon — define terms on first use

Save to: `state/streeling/courses/{department}/en/{module_id}.md`

## Phase 4: TRANSLATE

Check `policies/multilingual-policy.yaml` for translation requirements.

For each required language (currently: es, pt, fr):

1. Translate content preserving structure and frontmatter
2. Apply cultural adaptation:
   - **Spanish (es):** Use Latin American music examples where relevant, formal "usted" for technical content
   - **Portuguese (pt):** Brazilian Portuguese with bossa nova / MPB examples for music
   - **French (fr):** Metropolitan French, reference chanson tradition for music
3. Preserve all Markdown formatting, code blocks, and frontmatter fields
4. Add language suffix to module_id in frontmatter

Save to: `state/streeling/courses/{department}/{lang}/{module_id}.{lang}.md`

**Gate:** Translation must preserve all sections, exercises, and key terms. Quick verification: section count must match English version.

## Phase 5: REVIEW

Quality gate before publishing:

1. **Accuracy check:** Do claims match research evidence? (belief_confidence >= 0.7 to auto-approve)
2. **Completeness check:** All sections present? At least 1 exercise?
3. **Curriculum alignment:** Does module fit the department's curriculum progression?
4. **Duplication check:** No significant overlap with existing courses?
5. **Format check:** Frontmatter valid? Module ID follows convention?

**Verdicts:**
- `approved` — proceed to publish
- `revise` — return to CONTENT phase with specific feedback (max 2 revisions)
- `reject` — pipeline ends, log reason, flag for human review

If confidence < 0.7 but >= 0.5: flag for human review instead of auto-approving.
If confidence < 0.5: auto-reject (should have been caught at Phase 1 gate).

## Phase 6: PUBLISH

1. Verify all files are written to correct paths
2. Log pipeline run to `state/streeling/course-productions/{pipeline_id}.json` conforming to `schemas/course-production.schema.json`
3. Update department weights if research cycle was fresh (delegate to research-cycle compound step)
4. Commit all course files with conventional commit:
   ```
   feat: {DEPT-CODE}-{SEQ} — {course title}
   ```
5. Print summary:

```
Course Published: {module_id}
Department: {department}
Title: {title}
Level: {level} | Duration: {duration}
Languages: en, es, pt, fr
Research: {cycle_id} (belief: {value}, confidence: {confidence})
Files: {count} files across {language_count} languages
```

## Batch Mode

When invoked with `batch`, scan `state/streeling/research-cycles/` for cycles with:
- `conclusion` = `confirm` or `discover_question`
- `belief_confidence` >= 0.5
- No corresponding course in `state/streeling/courses/{dept}/en/`

Run the pipeline (phases 2-6) for each qualifying cycle. Print batch summary.

## Pipeline State

Pipeline runs are logged to `state/streeling/course-productions/{pipeline_id}.json`.

This allows:
- Resuming interrupted pipelines
- Tracking production metrics (duration, token usage, revision count)
- Identifying bottleneck phases
- Measuring course production velocity per department

## Governance

- **Article 2 (Transparency):** All production steps are logged with evidence trails
- **Article 9 (Bounded Autonomy):** Course scope bounded by department curriculum
- **Article 11 (Ethical Stewardship):** Content reviewed before publication
- **Multilingual Policy:** Translation required for departments in policy scope
- **Streeling Policy:** Knowledge transfer quality standards
- **Confidence thresholds:** Auto-publish >= 0.7, human review 0.5-0.7, reject < 0.5
