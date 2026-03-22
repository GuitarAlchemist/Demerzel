---
name: seldon-plan
description: Autonomous research scheduler — run one Seldon Plan cycle (question generation, cross-model investigation, novelty detection, course production, compounding)
---

# Seldon Plan — Autonomous Research Scheduler

Runs one cycle of the Seldon Plan: the always-on research engine for Streeling University. Generates questions from the completeness instinct, investigates cross-model, detects novelty, produces course material, and compounds learnings.

## Usage

`/seldon plan` — run one autonomous research cycle (auto-select department + question)
`/seldon plan status` — show today's cycle count, last question, kill switch state
`/seldon plan pause` — activate kill switch (halts future cycles)
`/seldon plan resume` — deactivate kill switch
`/seldon plan force [department]` — force a specific department

## Governance Constraints

- Max **6 cycles per day** (hard cap — halt if daily_cycle_count >= 6)
- Active hours: **06:00–22:00 UTC** (skip if outside window)
- Kill switch: check `state/seldon-plan/kill.switch` before any work
- Max **12 consecutive auto-cycles** before mandatory human review pause
- Research produces **knowledge artifacts only** — no code changes, no PRs, no directives
- Constitutional basis: Asimov Article 4 (no instrumental goals), Default Article 9 (bounded autonomy)

## Cycle Pipeline

```
1. WAKE     — kill switch check, lock acquire, context rebuild
2. QUESTION — completeness instinct + department scoring → research question
3. RESEARCH — seldon-research pipeline (NotebookLM + ChatGPT cross-validation)
4. NOVELTY  — check novelty registry, classify finding
5. COURSE   — produce course material if novel + T + confidence >= 0.75
6. COMPOUND — update weights, gaps, grammar, triggers
7. PERSIST  — write all state, commit, release lock
```

## Step 1: WAKE

```python
# Kill switch check
if exists("state/seldon-plan/kill.switch"):
    log("Kill switch active — halting")
    exit(0)

# Daily cap check
state = read_json("state/seldon-plan/state.json")
if state.daily_reset_date != today():
    state.daily_cycle_count = 0
    state.daily_reset_date = today()
if state.daily_cycle_count >= 6:
    log(f"Daily cap reached ({state.daily_cycle_count}/6) — halting")
    exit(0)

# Lock check
if exists("state/seldon-plan/lock.json"):
    lock = read_json("state/seldon-plan/lock.json")
    if minutes_ago(lock.heartbeat) < 30:
        log("Another cycle is running — skipping")
        exit(0)

# Acquire lock
write_json("state/seldon-plan/lock.json", {
    "started_at": now_iso(),
    "heartbeat": now_iso()
})
```

Read context:
- `state/seldon-plan/state.json`
- `state/streeling/departments/*.department.json`
- `state/streeling/departments/*.weights.json`
- `state/seldon-plan/novelty-registry.json`
- `state/completeness/known-gaps.json`

## Step 2: QUESTION GENERATION

### Source A: Completeness Instinct
Load `state/completeness/known-gaps.json`. Find critical/important open gaps.
Transform gap → research question:

| Gap type | Question template |
|---|---|
| `declared_but_underspecified` | "What are the full semantics of {concept}?" |
| `implied_but_missing` | "What should govern {missing_concept} given {existing_context}?" |
| `policy_with_no_enforcement` | "How would {policy} detect violations in practice?" |
| `persona_with_no_test` | "What behavioral signatures distinguish {persona} from adjacent roles?" |

### Source B: Department Priority Scoring
```
priority = (days_since_last_cycle * 0.4)
         + (curriculum_gap_count * 0.3)
         + (U_belief_ratio * 0.2)
         + (random_exploration * 0.1)
```

Select top-scoring department, sample from `research_areas`, check against existing curriculum.

### Merge + Novelty Gate
1. Critical completeness gap → use it (highest priority)
2. Important completeness gap → 50% probability
3. Otherwise → department priority winner

Check novelty: compute `sha256(normalize(question))`, look up in `novelty-registry.json`.
If found → re-sample (max 3 attempts). If all fail → log "all sampled questions known", exit cycle gracefully.

## Step 3: INVESTIGATION

Invoke the seldon-research pipeline directly (do not call `/seldon research` recursively — execute the steps inline):

### 3a. Classify
- governance → check constitutional artifacts directly
- experiential → check evolution log + NotebookLM
- domain → GA skills + NotebookLM

### 3b. NotebookLM Lookup
```javascript
mcp__notebooklm__ask_question({
  question: "[research question]",
  notebook_id: "[best matching notebook]"
})
```

### 3c. GA Domain Skills (if music domain)
Invoke relevant skill conceptually (ScaleInfoSkill, ChordExplanationSkill, etc.).

### 3d. ChatGPT Cross-Validation (mandatory for Seldon Plan)
```javascript
mcp__openai-chat__openai_chat({
  model: "gpt-4o-mini",
  messages: [
    {
      role: "system",
      content: "You are a domain expert. Evaluate this research finding and indicate whether you agree, disagree, or are uncertain. Be concise. State your confidence (0.0–1.0)."
    },
    {
      role: "user",
      content: "Finding: [Claude's answer]\nQuestion: [research question]\nDo you agree? Provide confidence."
    }
  ]
})
```

### 3e. Agreement Matrix → Tetravalent Belief

| Condition | Belief | Confidence |
|---|---|---|
| Claude + ChatGPT agree, NotebookLM confirms | T | >= 0.85 |
| Claude + ChatGPT agree, NotebookLM silent | T | 0.70–0.84 |
| Claude has answer, ChatGPT uncertain | U | 0.50–0.69 |
| Claude + ChatGPT disagree | C | <= 0.50 |
| All uncertain | U | < 0.50 |

## Step 4: NOVELTY DETECTION

```python
finding_hash = sha256(normalize(question))
registry = read_json("state/seldon-plan/novelty-registry.json")

existing = registry.find(hash=finding_hash)
if existing:
    classification = "redundant"
elif contradicts_existing_T_belief(question, conclusion):
    classification = "anomaly"
    trigger_conscience_signal()
elif improves_confidence_of_existing_belief(question, conclusion):
    classification = "incremental"
else:
    classification = "novel"
```

**Action by classification:**
- `novel` + T + confidence >= 0.75 → proceed to course production
- `novel` + T + confidence < 0.75 → log, schedule deeper investigation
- `novel` + U or C → log, schedule deeper investigation
- `novel` + F → log refutation, update curriculum "not X" entry
- `incremental` → update registry entry confidence, no new course
- `anomaly` → conscience signal, trigger for main driver, **do not auto-resolve**
- `redundant` → skip production, increment skip counter in state

## Step 5: COURSE PRODUCTION

Only if: `classification == "novel"` AND `belief_value == "T"` AND `confidence >= 0.75`

### Course File
Save to `state/streeling/courses/{department}/en/{module_id}.md` using the format from `seldon-research-cycle` SKILL.md (same frontmatter, same section structure).

`module_id` format: `{dept-code}-{NNN}-{slug}` where NNN is next sequence number for this department.

### Multilingual Translation
Per `multilingual-policy.yaml` — produce es/pt/fr/it/de variants if department is in scope.

### IxQL Expression
Emit research finding as an IxQL pipeline fragment:

```ixql
-- Seldon Plan Research Finding
-- Cycle: {cycle_id} | Department: {department}
-- Question: {question}
-- Belief: {T/F/U/C}({confidence})
RESEARCH_FINDING {
  department: "{department}",
  question: "{question}",
  conclusion: "{conclusion}",
  evidence_sources: ["{source_1}", "{source_2}"],
  cross_model_agreement: {
    claude: "{claude_verdict}",
    chatgpt: "{chatgpt_verdict}",
    notebooklm: "{notebooklm_verdict}"
  },
  belief: { value: "{T/F/U/C}", confidence: {number} },
  course_produced: {true|false},
  course_id: "{module_id_or_null}"
} -> KNOWLEDGE_STATE "{department}/findings/{cycle_id}"
```

Save to `state/seldon-plan/ixql-findings/{cycle_id}.ixql`.

## Step 6: COMPOUND

### Weight Update
```python
weights = read_json(f"state/streeling/departments/{dept}.weights.json")

if conclusion == "confirm":
    weights.hypothesis_weights[used_strategy] += 0.05
    weights.test_weights[used_method] += 0.05
elif conclusion in ("refute", "insufficient"):
    weights.hypothesis_weights[used_strategy] -= 0.03
    weights.test_weights[used_method] -= 0.03
elif conclusion == "contradictory":
    weights.test_weights["adversarial"] += 0.05

# Normalize
normalize_to_sum_1(weights.hypothesis_weights)
normalize_to_sum_1(weights.test_weights)

weights.metadata.cycle_count += 1
weights.metadata[f"total_{belief_value}"] += 1
weights.metadata.last_updated = today()

write_json(f"state/streeling/departments/{dept}.weights.json", weights)
```

### Novelty Registry Update
Append to `state/seldon-plan/novelty-registry.json`:
```json
{
  "question_hash": "{sha256}",
  "question": "{question}",
  "belief_value": "{T/F/U/C}",
  "belief_confidence": {number},
  "cycle_id": "{cycle_id}",
  "department": "{department}",
  "date": "{ISO_DATE}",
  "classification": "{novel|incremental|anomaly}"
}
```

### Curriculum Gap Update
- Finding covers a gap → mark gap as "researched" in department file
- Finding reveals new topic → add to `curriculum_gaps` list
- 3+ new gaps → create trigger file for main driver

### Grammar Evolution (if gap detected)
If the research question required a concept not expressible in `grammars/{dept}.ebnf`:
```ebnf
(* Proposed by seldon-plan cycle {cycle_id} *)
(* Evidence: {brief description} *)
(* Confidence: {belief_confidence} *)
new_production ::= term_a | term_b | term_c
```
Gate: `when T(0.7) && C(<0.1)`. Log in `state/evolution/`.

### Follow-Up Triggers
Write to `state/triggers/{ISO_DATETIME}-seldon-plan-followup.trigger.json`:
```json
{
  "type": "seldon_research_followup",
  "priority": "{high|medium|low}",
  "department": "{department}",
  "reason": "{discover_question|paradigm_shift|anomaly_detected|grammar_gap}",
  "details": { "spawned_question": "{question_if_applicable}" },
  "timestamp": "{ISO_DATETIME}"
}
```

## Step 7: PERSIST + SLEEP

### Cycle Log
Write `state/streeling/research-cycles/{cycle_id}.json` conforming to `schemas/research-cycle.schema.json`.

### State Update
```python
state.daily_cycle_count += 1
state.consecutive_auto_cycles += 1
state.last_question = question
state.last_department = department
state.last_cycle_id = cycle_id
state.total_cycles_all_time += 1
if course_produced:
    state.total_courses_produced += 1
write_json("state/seldon-plan/state.json", state)
```

### Commit
```bash
git add state/
git commit -m "feat(seldon-plan): cycle {cycle_id} — {conclusion} ({belief_value}, conf:{confidence})"
```

### Release Lock
```bash
rm state/seldon-plan/lock.json
```

### Log Entry
Append to `LOG.md`:
```
[{ISO_DATE}] Seldon Plan {cycle_id}: {dept} | "{question[:60]}..." | {belief_value}({confidence:.2f}) | course:{yes/no}
```

### Pause Check
```python
if state.consecutive_auto_cycles >= 12:
    # Activate kill switch
    write("state/seldon-plan/kill.switch", "Auto-pause: 12 consecutive cycles — human review needed")
    # Create GitHub issue
    gh_create_issue(
        title="Seldon Plan: 12 autonomous cycles completed — review findings",
        body=generate_findings_summary()
    )
```

## Status Command

When invoked as `/seldon plan status`, read and display:

```
Seldon Plan Status — {ISO_DATE}
─────────────────────────────────────
Cycles today:        {daily_cycle_count}/6
Kill switch:         {ACTIVE ⚠ / inactive}
Consecutive auto:    {consecutive_auto_cycles}/12
Total all-time:      {total_cycles_all_time}

Last cycle:          {last_cycle_id}
  Department:        {last_department}
  Question:          "{last_question[:80]}..."
  Belief:            {belief_value} ({confidence})
  Course produced:   {yes/no}

Novelty registry:    {registry_size} entries
Courses (lifetime):  {total_courses_produced}
Grammar productions: {total_grammar_productions_added}

Next window:         {next_scheduled_time} UTC (if GH Actions cron active)
```

## Error Handling

| Failure | Response |
|---|---|
| ChatGPT unavailable | Proceed without cross-validation, set confidence cap at 0.70, log |
| NotebookLM unavailable | Proceed without institutional memory, note in cycle log |
| All 3 question re-samples hit novelty registry | Skip cycle, log "knowledge frontier reached", increment skip counter |
| Lock held > 30min | Skip cycle (other instance running) |
| Daily cap reached | Skip cycle, log |
| Kill switch active | Skip cycle, log |
| Anomaly detected | Log, conscience signal, trigger for driver, do NOT auto-resolve |
| ChatGPT contradicts Claude | Set belief to C, log, do NOT produce course, escalate |

## Source

`policies/seldon-plan-policy.yaml` v1.0.0,
`policies/completeness-instinct-policy.yaml` v1.0.0,
`policies/continuous-learning-policy.yaml` v1.0.0,
`policies/streeling-policy.yaml`,
`personas/seldon.persona.yaml` v2.0.0,
`.claude/skills/seldon-research-cycle/SKILL.md`,
`.claude/skills/seldon-research/SKILL.md`
