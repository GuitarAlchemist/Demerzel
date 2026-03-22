---
name: seldon-auto-research
description: Autonomous research scheduler — selects the most under-researched department by coverage ratio, generates questions from completeness gaps, cross-model validates, auto-produces courses at T>=0.8, rate-limited to 6 cycles/day with kill switch
---

# Seldon Auto-Research — Coverage-Driven Autonomous Scheduler

Selects the Streeling University department with the **lowest research coverage ratio**
(`research_cycle_count / research_area_count`), generates a research question from
completeness gaps, investigates via cross-model validation (Claude + GPT-4o + NotebookLM),
and auto-produces course material when T-belief confidence >= 0.8.

Complements `seldon-plan` (which uses recency/priority scoring) by targeting departments
with large unexplored research area surfaces rather than stale ones.

## Usage

`/seldon auto-research` — run one coverage-driven research cycle
`/seldon auto-research status` — show coverage ratios for all departments
`/seldon auto-research force [department]` — force a specific department
`/demerzel research pause` — activate kill switch (halts all future cycles)
`/demerzel research resume` — deactivate kill switch

## Governance Constraints

- Max **6 cycles per day** — halt if `state/seldon-plan/state.json`.`daily_cycle_count >= 6`
- Kill switch: check `state/seldon-plan/kill.switch` before any work
- Knowledge artifacts only — no code changes, no PRs, no directives
- Course production threshold: **T + confidence >= 0.8** (stricter than seldon-plan's 0.75)
- Constitutional basis: Asimov Article 4 (no instrumental goals), Default Article 9 (bounded autonomy)

---

## Pipeline

```
1. WAKE        — kill switch + daily cap check
2. SELECT      — lowest coverage ratio department
3. GAPS        — completeness instinct → research questions
4. VALIDATE    — Claude + GPT-4o + NotebookLM cross-model
5. ASSESS      — agreement matrix → tetravalent belief
6. PRODUCE     — course if T >= 0.8
7. COMPOUND    — weights, gaps, novelty registry, IxQL fragment
8. PERSIST     — state update, commit, LOG.md entry
```

---

## Step 1: WAKE

```python
# Kill switch
if exists("state/seldon-plan/kill.switch"):
    log("Kill switch active — halting auto-research")
    exit(0)

# Daily cap (shared with seldon-plan — same counter)
state = read_json("state/seldon-plan/state.json")
today = date.today().isoformat()
if state.daily_reset_date != today:
    state.daily_cycle_count = 0
    state.daily_reset_date = today
if state.daily_cycle_count >= 6:
    log(f"Daily cap reached ({state.daily_cycle_count}/6) — skipping")
    exit(0)
```

---

## Step 2: SELECT Department (Coverage Ratio)

Load all department files from `state/streeling/departments/*.department.json`.
Load corresponding weights files for `metadata.cycle_count`.

Compute **coverage ratio** for each department:

```python
def coverage_ratio(dept):
    research_area_count = len(dept.get("research_areas", []))
    if research_area_count == 0:
        return 1.0  # No research areas declared — skip
    research_cycle_count = weights.metadata.get("cycle_count", 0)
    return research_cycle_count / research_area_count
```

Select the department with the **lowest coverage ratio** (most under-researched relative
to its declared scope). Ties broken by department name (alphabetical — deterministic).

If `force [department]` was specified, skip scoring and use that department directly.

**Status display** (`/seldon auto-research status`):

```
Department Coverage Ratios — {ISO_DATE}
────────────────────────────────────────────
Department              Areas  Cycles  Ratio
──────────────────────────────────────────
guitar-studies            12      3    0.25  ← selected
music-theory               8      3    0.37
world-music               10      4    0.40
philosophy                 7      3    0.43
data-visualization         9      4    0.44
...
Kill switch: inactive | Cycles today: {n}/6
```

---

## Step 3: GAPS — Completeness Instinct Question Generation

Load `state/completeness/known-gaps.json` filtered to the selected department.
Also load `state/streeling/departments/{dept}.department.json` for `research_areas`
and `curriculum` (to avoid generating duplicate questions).

### Priority Order for Question Selection

1. **Critical gap** (`severity: critical`, `status: open`) — use immediately
2. **Important gap** (`severity: important`, `status: open`) — use if no critical
3. **Uncovered research area** — a `research_areas` entry with no matching curriculum item
4. **Completeness dimension** — apply policy dimensions to existing curriculum:

| Dimension | Question template |
|---|---|
| `declared_but_underspecified` | "What are the complete semantics and constraints of {concept}?" |
| `implied_but_missing` | "Given that {A} exists in {dept}, what is its dual/complement {B}?" |
| `dual_analysis` | "If {X} process exists, what governs the inverse {Y} process?" |
| `scale_projection` | "How does {approach} break down at 10x current scale in {dept}?" |
| `adjacency_needs` | "What does {consumer_repo} need from {dept} that isn't yet provided?" |

### Novelty Gate

Compute `sha256(normalize(question))` and check `state/seldon-plan/novelty-registry.json`.
If found → re-sample (max 3 attempts). If all 3 fail → log "coverage frontier reached for {dept}", exit gracefully.

---

## Step 4: CROSS-MODEL VALIDATION

Three-model pipeline. All three queried; agreement matrix determines belief.

### 4a. Claude (Primary)

Answer the research question from domain knowledge and available governance artifacts.
Produce:
- A direct answer
- Supporting evidence (citations to policies, grammars, courses, external sources)
- An initial confidence estimate (0.0–1.0)

### 4b. NotebookLM (Institutional Memory)

```javascript
mcp__notebooklm__ask_question({
  question: "[research question]",
  notebook_id: "[most relevant notebook — Streeling, Demerzel, or GA domain]"
})
```

Extract: does NotebookLM confirm, contradict, or have no data on Claude's answer?

### 4c. GPT-4o (Independent Validation)

```javascript
mcp__openai-chat__openai_chat({
  model: "gpt-4o",  // Note: GPT-4o (not mini) for stricter threshold T>=0.8
  messages: [
    {
      role: "system",
      content: "You are an independent expert reviewer. Assess the following research finding. State: agree/disagree/uncertain and a confidence score 0.0–1.0. Be concise and critical — do not simply affirm."
    },
    {
      role: "user",
      content: "Research question: {question}\n\nProposed finding: {claude_answer}\n\nDo you agree? Confidence?"
    }
  ]
})
```

---

## Step 5: AGREEMENT MATRIX → TETRAVALENT BELIEF

| Claude | GPT-4o | NotebookLM | Belief | Confidence |
|--------|--------|------------|--------|------------|
| Confident answer | Agrees (conf>=0.7) | Confirms | **T** | >= 0.85 |
| Confident answer | Agrees (conf>=0.7) | Silent/absent | **T** | 0.75–0.84 |
| Confident answer | Agrees (conf>=0.7) | Contradicts | **C** | 0.60–0.74 |
| Confident answer | Uncertain (<0.5) | Any | **U** | 0.50–0.65 |
| Confident answer | Disagrees | Any | **C** | <= 0.55 |
| Uncertain | Any | Any | **U** | <= 0.50 |
| All uncertain/absent | — | — | **U** | < 0.40 |

**Course production gate: T AND confidence >= 0.8** (requires row 1 or high-end row 2).

---

## Step 6: COURSE PRODUCTION

Produce course material **only if** `belief_value == "T"` AND `confidence >= 0.8`.

### Course File

Save to `state/streeling/courses/{department}/en/{module_id}.md`.

`module_id` format: `{dept-code}-{NNN}-{slug}` — NNN is the next sequence number for the department.

Use the standard course format (same frontmatter and section structure as `seldon-research-cycle`):

```markdown
---
module_id: {dept-code}-{NNN}-{slug}
department: {department}
course: "{curriculum area}"
level: {beginner|intermediate|advanced}
prerequisites: []
estimated_duration: "{N} minutes"
produced_by: seldon-auto-research
research_cycle: {cycle_id}
cross_model_agreement: {claude: "T", gpt4o: "{verdict}", notebooklm: "{verdict}"}
version: "1.0.0"
---

# {Title}

> **{Department Full Name}** | Level: {level} | Duration: {duration}

## Objectives
- [3-5 learning objectives from research findings]

---

## 1. {Section 1}
[Content from confirmed findings]

### Practice Exercise
[Hands-on exercise if applicable]

---

## Key Takeaways
- [Summary of main points]

## Further Reading
- [Related courses, NotebookLM notebooks, external references]

---
*Produced by Seldon Auto-Research {cycle_id} on {date}.*
*Research question: {question}*
*Belief: {value} (confidence: {confidence}) — Claude + GPT-4o agreement*
```

### Multilingual Translation

Per `policies/multilingual-policy.yaml` — produce es/pt/fr/it/de variants if department is in scope.

### IxQL Pipeline Fragment

Emit research finding as an IxQL expression (per `docs/ixql-guide.md` Section 11 — Evolution Hooks):

```ixql
-- Seldon Auto-Research Finding
-- Cycle: {cycle_id} | Department: {department}
-- Coverage ratio at selection: {ratio}
department_state("{department}")
  → question_generation("{gap_source}", coverage_ratio: {ratio})
  → cross_model_validation(
       claude.research("{question}"),
       gpt4o.research("{question}"),
       notebooklm.lookup("{question}")
     )
  → evaluation(agreement_score, evidence_density)
  → when T >= 0.8: course_production("{module_id}", languages: ["{lang_list}"])
  → compound:
      update_weights(department: "{department}", conclusion: "{conclusion}")
      register_finding(hash: "{sha256}", belief: {value: "{T/F/U/C}", confidence: {number}})
      promote if confidence >= 0.9
```

Save to `state/seldon-plan/ixql-findings/{cycle_id}.ixql`.

---

## Step 7: COMPOUND

### Weight Update

```python
weights = read_json(f"state/streeling/departments/{dept}.weights.json")

if belief_value == "T":
    weights.hypothesis_weights[used_strategy] += 0.05
    weights.test_weights[used_method] += 0.05
elif belief_value in ("F", "U"):
    weights.hypothesis_weights[used_strategy] -= 0.03
    weights.test_weights[used_method] -= 0.03
elif belief_value == "C":
    weights.test_weights["adversarial"] += 0.05

normalize_to_sum_1(weights.hypothesis_weights)
normalize_to_sum_1(weights.test_weights)

weights.metadata.cycle_count += 1
weights.metadata[f"total_{belief_value}"] += 1
weights.metadata.last_updated = today()

write_json(f"state/streeling/departments/{dept}.weights.json", weights)
```

### Gap Status Update

- If question addressed a gap from `known-gaps.json` → mark gap `status: researched`
- If finding reveals a new uncovered research area → add to department `curriculum_gaps`
- 3+ new gaps in one cycle → write trigger file for main driver

### Novelty Registry

Append entry to `state/seldon-plan/novelty-registry.json`:

```json
{
  "question_hash": "{sha256(normalize(question))}",
  "question": "{question}",
  "belief_value": "{T/F/U/C}",
  "belief_confidence": {number},
  "cycle_id": "{cycle_id}",
  "department": "{department}",
  "date": "{ISO_DATE}",
  "source": "seldon-auto-research",
  "coverage_ratio_at_selection": {number}
}
```

---

## Step 8: PERSIST

### State Update

```python
state = read_json("state/seldon-plan/state.json")
state.daily_cycle_count += 1
state.last_question = question
state.last_department = department
state.last_cycle_id = cycle_id
state.total_cycles_all_time += 1
if course_produced:
    state.total_courses_produced += 1
state.total_novelty_registry_entries += 1
write_json("state/seldon-plan/state.json", state)
```

### Cycle Log

Write `state/streeling/research-cycles/{cycle_id}.json`:

```json
{
  "cycle_id": "{cycle_id}",
  "scheduler": "seldon-auto-research",
  "department": "{department}",
  "coverage_ratio_at_selection": {number},
  "gap_source": "{completeness_dimension_or_gap_id}",
  "question": "{question}",
  "belief_value": "{T/F/U/C}",
  "belief_confidence": {number},
  "cross_model_agreement": {
    "claude_verdict": "{answer_summary}",
    "gpt4o_verdict": "{verdict}",
    "gpt4o_confidence": {number},
    "notebooklm_verdict": "{confirm|contradict|silent}"
  },
  "course_produced": {true|false},
  "module_id": "{module_id_or_null}",
  "timestamp": "{ISO_DATETIME}"
}
```

### Commit

```bash
git add state/
git commit -m "feat(seldon-auto-research): cycle {cycle_id} — {conclusion} ({belief_value}, conf:{confidence:.2f})"
```

### LOG.md Entry

Append to `LOG.md`:
```
[{ISO_DATE}] Seldon Auto-Research {cycle_id}: {dept}(ratio:{ratio:.2f}) | "{question[:60]}..." | {belief_value}({confidence:.2f}) | course:{yes/no}
```

---

## Kill Switch: `/demerzel research pause`

When `/demerzel research pause` is received:

```bash
echo "Manual pause via /demerzel research pause — {ISO_DATETIME}" > state/seldon-plan/kill.switch
git add state/seldon-plan/kill.switch
git commit -m "feat(seldon-plan): activate kill switch — manual pause via /demerzel research pause"
```

When `/demerzel research resume` is received:

```bash
rm state/seldon-plan/kill.switch
git rm state/seldon-plan/kill.switch
git commit -m "feat(seldon-plan): deactivate kill switch — resuming"
```

---

## Error Handling

| Failure | Response |
|---|---|
| GPT-4o unavailable | Fall back to GPT-4o-mini. If both unavailable, cap confidence at 0.70 (T becomes U at threshold) |
| NotebookLM unavailable | Proceed without; note absence in cycle log; confidence reduced by 0.05 |
| All 3 question re-samples in novelty registry | Log "coverage frontier reached for {dept}", skip cycle, try next-lowest-ratio department |
| Department has zero research areas | Skip (coverage ratio = 1.0 by convention) |
| Kill switch active | Halt immediately, do not log cycle |
| Daily cap reached | Skip cycle, log |
| GPT-4o disagrees with Claude | Set belief to C, log, do NOT produce course, write conscience signal |

---

## Source

`policies/seldon-plan-policy.yaml` v1.0.0,
`policies/completeness-instinct-policy.yaml` v1.0.0,
`policies/streeling-policy.yaml`,
`policies/autonomous-loop-policy.yaml`,
`docs/ixql-guide.md`,
`personas/seldon.persona.yaml` v2.0.0,
`.claude/skills/seldon-research-cycle/SKILL.md`,
`.claude/skills/seldon-plan/SKILL.md`
