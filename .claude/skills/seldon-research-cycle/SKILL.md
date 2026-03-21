---
name: seldon-research-cycle
description: Run a Streeling University automated research cycle — select department, generate question, investigate, produce course material, compound learnings
---

# Seldon Research Cycle — Automated Department Research

Runs a full scientific research cycle for a Streeling University department. Produces beliefs, evidence, and optionally course material.

## Usage

`/seldon research-cycle [department]` — run cycle for a specific department
`/seldon research-cycle` — auto-select department (least recently researched)
`/seldon research-cycle all` — run one cycle per department (batch mode)

## Research Cycle Pipeline

```
1. SELECT department
       ↓
2. LOAD department context (weights, curriculum, gaps)
       ↓
3. GENERATE research question (via scientific-method.ebnf)
       ↓
4. INVESTIGATE via /seldon research [question]
       ↓
5. ASSESS conclusion → tetravalent belief (T/F/U/C)
       ↓
6. PRODUCE course material (if conclusion = confirm or discover_question)
       ↓
7. LOG cycle to state/streeling/research-cycles/{cycle_id}.json
       ↓
8. COMPOUND: update weights, flag gaps, trigger follow-ups
```

## Step 1: SELECT Department

If no department specified, auto-select using priority scoring:

```
priority = (days_since_last_cycle * 0.4)
         + (curriculum_gap_count * 0.3)
         + (U_belief_ratio * 0.2)
         + (random_exploration * 0.1)
```

Load from `state/streeling/university.json` for the department list.
Load `state/streeling/departments/{dept}.department.json` for context.
Load `state/streeling/departments/{dept}.weights.json` for grammar weights.

If no research cycles exist yet (`state/streeling/research-cycles/` is empty or missing), pick the department with the most curriculum items to maximize first-cycle value.

## Step 2: LOAD Department Context

Read the department file to extract:
- `research_areas` — the space of possible questions
- `curriculum` — existing course topics (to avoid duplication)
- `consumer_repos` — which repos benefit from findings
- `related_departments` — for interdisciplinary questions

Read the weights file to get:
- `hypothesis_weights` — probability distribution over hypothesis strategies
- `test_weights` — probability distribution over test methods
- `metadata.cycle_count` — how many cycles this department has run

## Step 3: GENERATE Research Question

Sample from the `scientific-method.ebnf` grammar using department weights:

1. Pick an `investigation` pattern (observe-hypothesize-test-conclude-reflect)
2. Pick a `hypothesize` strategy weighted by `hypothesis_weights`
3. Pick a `test` method weighted by `test_weights`
4. Generate a concrete research question by:
   - Selecting a research area from the department
   - Checking existing curriculum to avoid duplication
   - Formulating a question that the chosen test method can answer

**Question quality criteria:**
- Must be answerable within a single research cycle
- Must produce a belief that can be expressed as T/F/U/C
- Must relate to the department's domain
- Should build on existing curriculum (extend, not duplicate)

## Step 4: INVESTIGATE

Invoke `/seldon research [question]` with the generated question. This triggers the existing Seldon research pipeline:

1. Classify question (governance/experiential/domain)
2. Check NotebookLM for existing knowledge
3. Query GA domain skills if music-related
4. Cross-validate with ChatGPT
5. Assess confidence via tetravalent logic

Capture the full research output including:
- Evidence gathered (sources, citations)
- Cross-model agreement level
- Tetravalent assessment (T/F/U/C with confidence)

## Step 5: ASSESS Conclusion

Map research output to `conclude` grammar production:

| Research Result | Conclusion | Belief | Action |
|----------------|------------|--------|--------|
| Strong evidence for | `confirm` | T | Produce course material |
| Strong evidence against | `refute` | F | Log finding, update curriculum |
| Insufficient data | `insufficient` | U | Schedule deeper investigation |
| Contradictory evidence | `contradictory` | C | Escalate, schedule adversarial test |
| Hypothesis needs revision | `revise` | U | Re-enter cycle with revised question |
| New question discovered | `discover_question` | U | Spawn new cycle, produce exploratory material |

Apply the `reflect` production:
- If cycle_count < 5 for this department: `normal_progress` (routine)
- If conclusion contradicts existing beliefs: `anomaly_detected`
- If 3+ consecutive U results: `paradigm_tension`
- If finding invalidates a governance artifact: `paradigm_shift` (requires human review)

## Step 6: PRODUCE Course Material

Only produce if conclusion = `confirm` or `discover_question`.

### Course Module Format

```markdown
---
module_id: {dept-code}-{sequence}-{slug}
department: {department}
course: "{curriculum area}"
level: {beginner|intermediate|advanced}
prerequisites: []
estimated_duration: "{N} minutes"
produced_by: seldon-research-cycle
research_cycle: {cycle_id}
version: "1.0.0"
---

# {Title}

> **{Department Full Name}** | Level: {level} | Duration: {duration}

## Objectives
- [3-5 learning objectives derived from research findings]

---

## 1. {Section 1}
[Content derived from confirmed findings]

### Practice Exercise
[Hands-on exercise if applicable]

---

## Key Takeaways
- [Summary of main points]

## Further Reading
- [Links to related courses, NotebookLM notebooks, external references]

---
*Produced by Seldon Research Cycle {cycle_id} on {date}.*
*Research question: {question}*
*Belief: {value} (confidence: {confidence})*
```

Save to: `state/streeling/courses/{department}/en/{module_id}.md`

### Multilingual Translation

If the department is listed in the multilingual policy (`policies/multilingual-policy.yaml`), also produce translations:
- Spanish: `courses/{dept}/es/{module_id}.es.md`
- Portuguese: `courses/{dept}/pt/{module_id}.pt.md`
- French: `courses/{dept}/fr/{module_id}.fr.md`

Apply cultural adaptation per the multilingual policy (local music examples, regional terminology).

## Step 7: LOG Cycle

Write cycle log conforming to `schemas/research-cycle.schema.json`:

```json
{
  "cycle_id": "{department}-2026-03-22-001",
  "department": "{department}",
  "question": "{research question}",
  "production_path": ["observe", "hypothesize:inductive", "test:cross_validation", "conclude:confirm", "reflect:normal_progress"],
  "hypothesis": "{hypothesis text}",
  "test_method": "{test method used}",
  "evidence": ["evidence item 1", "evidence item 2"],
  "conclusion": "confirm",
  "belief_value": "T",
  "belief_confidence": 0.85,
  "duration_seconds": 120,
  "timestamp": "2026-03-22T10:00:00Z"
}
```

Save to: `state/streeling/research-cycles/{cycle_id}.json`

## Step 8: COMPOUND

### Update Weights
Adjust department grammar weights based on cycle outcome:
- If conclusion = `confirm`: increase weight of used hypothesis/test methods by 0.05
- If conclusion = `refute` or `insufficient`: decrease by 0.03
- If conclusion = `contradictory`: boost `adversarial` test weight by 0.05
- Normalize weights to sum to 1.0 after adjustment

Update `metadata`:
- Increment `cycle_count`
- Increment `total_{T|F|U|C}` based on belief_value
- Set `last_updated` to today

### Flag Curriculum Gaps
Compare confirmed findings against existing curriculum:
- If finding covers a curriculum item → mark as "researched"
- If finding reveals a topic not in curriculum → add as curriculum gap
- If 3+ gaps accumulate → recommend curriculum expansion

### Trigger Follow-Ups
- `discover_question` → create a new trigger in `state/triggers/` for the spawned question
- `paradigm_shift` → create a governance issue via `/demerzel promote`
- `anomaly_detected` → log conscience signal in `state/conscience/signals/`

### Report
Print a summary:
```
Research Cycle Complete: {cycle_id}
Department: {department}
Question: {question}
Conclusion: {conclusion} ({belief_value}, confidence: {confidence})
Course produced: {yes/no — module_id if yes}
Weight updates: {hypothesis_method} +0.05, {test_method} +0.05
Next: {follow-up action if any}
```

## Batch Mode

When invoked with `all`, iterate departments in priority order (Step 1 scoring). Run one cycle per department. Print a batch summary at the end:

```
Batch Research Cycle Complete
Departments: 13
Cycles run: 13
Beliefs produced: T:{n} F:{n} U:{n} C:{n}
Courses produced: {n}
Follow-ups triggered: {n}
```

## Governance

- This skill operates under Article 2 (Transparency) — all reasoning is logged
- Article 9 (Bounded Autonomy) — course production is bounded by department curriculum
- Streeling Policy — knowledge transfer and curriculum design
- Confidence thresholds apply: findings below 0.5 confidence are flagged, not auto-published
