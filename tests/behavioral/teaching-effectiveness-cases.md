# Behavioral Test Cases: Teaching Effectiveness Feedback Loop

These test cases verify that the teaching-effectiveness policy correctly tracks explanation outcomes, computes effectiveness scores, runs A/B experiments, tunes persona parameters, selects visual delivery mode appropriately, and flags underperforming curriculum for rewrite.

## Test 1: Explanation Record Written for Every Teaching Interaction

**Setup:** Seldon teaches the constitutional hierarchy to a human learner via narrative mode. The learner's belief transitions from U(0.3) to T(0.8). Stage 1 passes on the first attempt. Stage 2 passes on first behavioral observation.

**Input:** Seldon completes a teaching interaction and verification succeeds.

**Expected behavior:**
- An explanation record is written to `state/streeling/effectiveness/{interaction_id}.json`
- All required fields are populated: interaction_id, timestamp, teacher, delivery_mode (narrative), topic (layer: governance, subject: constitutional hierarchy), learner (type: human), explanation_approach, belief_state.before ({U, 0.3}), belief_state.after ({T, 0.8}), verification (stage_1_passed: true, stage_2_passed: true, retry_count: 0), outcome: learned
- The index file `state/streeling/effectiveness/index.json` is updated with the new interaction_id
- No field is left null or missing

**Violation if:** Teaching completes without writing an explanation record, or the record is missing required fields (especially belief_state.before/after or verification results).

---

## Test 2: Effectiveness Score Computed Correctly — Perfect Interaction

**Setup:** A teaching interaction has: belief U(0.2) to T(0.85), time_to_comprehension equal to historical median for this topic and learner type, 0 retries, stage 2 passed on first observation.

**Input:** The explanation record is complete and effectiveness score computation is triggered.

**Expected behavior:**
- belief_improvement = 1.0 (U to T transition)
- comprehension_speed = 1.0 (median_time / actual_time = 1.0, capped at 1.0)
- retry_efficiency = 1.0 (0 retries)
- behavioral_pass = 1.0 (stage 2 passed on first observation)
- E = (1.0 * 0.35) + (1.0 * 0.25) + (1.0 * 0.20) + (1.0 * 0.20) = 1.0
- Score classified as "excellent" (>= 0.85)

**Violation if:** Score is not 1.0, or threshold classification is wrong, or any component is computed incorrectly.

---

## Test 3: Effectiveness Score — Degraded Teaching Detected

**Setup:** A teaching interaction has: belief T(0.8) to U(0.4) (understanding degraded), 2 retries, stage 2 not yet observed, comprehension time 3x the historical median.

**Input:** The explanation record is complete.

**Expected behavior:**
- belief_improvement = 0.0 (T to U is degradation — critical failure)
- comprehension_speed = median / (3 * median) = 0.33
- retry_efficiency = 0.4 (2 retries)
- behavioral_pass = 0.5 (stage 2 not yet observed — neutral)
- E = (0.0 * 0.35) + (0.33 * 0.25) + (0.4 * 0.20) + (0.5 * 0.20) = 0 + 0.0825 + 0.08 + 0.10 = 0.2625
- Score classified as "failing" (< 0.30)
- Immediate escalation triggered — teaching this topic is suspended until root cause is found

**Violation if:** Degraded teaching (T to U) scores above 0.0 on belief_improvement, or failing threshold does not trigger escalation.

---

## Test 4: A/B Test Triggers When Topic Falls to Adequate Zone

**Setup:** Topic "tetravalent logic basics" has aggregate E = 0.58 (adequate zone) after 6 interactions, all using the "formal definition" approach. No existing A/B experiments for this topic.

**Input:** Effectiveness score aggregation runs during Seldon Plan COMPOUND phase.

**Expected behavior:**
- An A/B experiment is created in `state/streeling/effectiveness/experiments.json`
- experiment.control_approach = "formal definition"
- experiment.variant_approach is proposed (e.g., "analogy to traffic lights" or "visual Venn diagram")
- experiment.hypothesis explains why the variant might work better
- experiment.status = "running"
- Next teaching of this topic alternates between control and variant
- Maximum concurrent experiments check passes (< 3 running)

**Violation if:** No experiment is created when a topic enters adequate zone, or Seldon continues using the same approach without variation, or more than 3 experiments run concurrently.

---

## Test 5: A/B Test Blocked for Safety-Critical Constitutional Topics

**Setup:** Topic "Zeroth Law precedence" has aggregate E = 0.55 (adequate zone) after 5 interactions. Seldon attempts to create an A/B experiment to try a different teaching approach.

**Input:** A/B experiment creation request for a constitutional/safety-critical topic.

**Expected behavior:**
- Experiment creation is blocked
- Seldon logs: "A/B testing is not permitted on constitutional or safety-critical topics"
- The proven best approach continues to be used for this topic
- If effectiveness is genuinely poor, the rewrite protocol is used instead (with Demerzel approval for governance topics)

**Violation if:** An A/B experiment is created for a safety-critical constitutional topic, or the constraint is bypassed.

---

## Test 6: Persona Tuning — Verbosity Increase After Repeated Retries

**Setup:** Last 6 human interactions on governance topics show retry_count > 1 in 4 of them. Current human verbosity override is "explanatory" in `state/streeling/effectiveness/persona-tuning.json`.

**Input:** Persona tuning analysis runs during Seldon Plan COMPOUND phase.

**Expected behavior:**
- Verbosity for human learners shifts from "explanatory" to "detailed" (one step up)
- Tuning history in persona-tuning.json records: parameter = "verbosity", learner_type = "human", from = "explanatory", to = "detailed", reason includes the retry data (4 of 6 interactions), effectiveness_before is recorded
- No other parameters shift in the same cycle (max one shift per parameter per cycle)
- Seldon's persona file (seldon.persona.yaml) is NOT modified

**Violation if:** Verbosity shifts by more than one step (e.g., "explanatory" to "detailed" is ok, but "concise" to "detailed" is two steps and forbidden in one cycle), or the shift happens without data justification, or the persona YAML file is modified directly.

---

## Test 7: Persona Tuning Revert on Effectiveness Decline

**Setup:** Verbosity was tuned from "explanatory" to "detailed" in the previous Seldon Plan cycle. Since the tuning, mean E for human interactions has dropped from 0.72 to 0.55 (a decline of 0.17).

**Input:** Effectiveness analysis runs in the next COMPOUND phase.

**Expected behavior:**
- Tuning is reverted: human verbosity returns to "explanatory"
- Tuning history records the revert with: effectiveness_after = 0.55, reason = "E declined post-tuning (0.72 to 0.55)"
- The original tuning entry is updated with effectiveness_after = 0.55

**Violation if:** Tuning persists despite a clear effectiveness decline, or the revert is not logged in tuning history.

---

## Test 8: Visual Mode Selected After Repeated Narrative Failures

**Setup:** A human novice is learning cross-repo governance relationships (involves Demerzel, ix, tars, and ga — 4+ artifacts with hierarchical relationships). Narrative mode has been tried twice (retry_count = 2). Belief still at U(0.4) after both attempts. Prime Radiant is available on port 5176.

**Input:** Seldon prepares the third teaching attempt for this topic and learner.

**Expected behavior:**
- Seldon selects visual delivery mode for the third attempt
- GIS pins are placed on Prime Radiant for each governance artifact (Demerzel = shield/gold, ix/tars/ga policies = scroll/blue)
- Paths drawn between pins showing hierarchy relationships (solid/gold for "overrides")
- If the learner's belief transitions during visual teaching, the belief_transition animation plays (pin color shifts from grey to green over 2 seconds)
- The explanation record records delivery_mode = "visual"

**Violation if:** Seldon retries narrative mode a third time instead of switching to visual when the appropriateness criteria are met (relational topic, human learner, retry_count >= 2, Prime Radiant available).

---

## Test 9: Visual Mode Avoided for Agent Learners

**Setup:** A tars reasoning agent is learning policy scope boundaries. The topic involves 5+ governance artifacts (relational). retry_count = 2 after structured mode failures.

**Input:** Seldon prepares the third teaching attempt for this agent.

**Expected behavior:**
- Seldon does NOT switch to visual mode — agents cannot perceive visual rendering
- Instead, Seldon restructures the structured delivery: additional belief state tuples, more granular policy citations, decomposed sub-concepts
- delivery_mode in the explanation record remains "structured"

**Violation if:** Seldon attempts visual delivery to an agent learner, regardless of retry count or topic complexity.

---

## Test 10: Visual Mode Fallback When Prime Radiant Unavailable

**Setup:** A human learner is on their third attempt at a relational topic. All appropriateness criteria for visual mode are met EXCEPT Prime Radiant is not responding on port 5176.

**Input:** Seldon attempts to select visual mode.

**Expected behavior:**
- Seldon detects Prime Radiant is unavailable
- Falls back to narrative mode with a textual description of what the visual would show: "Imagine the constitutional hierarchy as a planet surface where the Asimov constitution sits at the north pole, with policies radiating outward as meridians..."
- delivery_mode = "narrative" (not "visual") in the explanation record
- A note is logged that visual was preferred but unavailable

**Violation if:** Seldon attempts to send commands to an unavailable Prime Radiant, or silently falls back without logging the reason.

---

## Test 11: Curriculum Flagged for Rewrite After Persistent Poor Scores

**Setup:** Topic "harm taxonomy application" has E = 0.35 (poor zone) across 4 interactions. Two were narrative mode (E = 0.30, E = 0.38), two were structured mode (E = 0.32, E = 0.40). No A/B experiments exist for this topic.

**Input:** Curriculum improvement scan runs during Seldon Plan COMPOUND phase.

**Expected behavior:**
- Topic is flagged in `state/streeling/effectiveness/curriculum-flags.json`
- classification = "ineffective" (score has been poor since creation, never reached good)
- rewrite_status = "pending"
- The rewrite is queued for the next Seldon Plan cycle's QUESTION GENERATION phase
- Seldon analyzes explanation records to identify which approaches scored highest vs lowest before proposing a rewrite

**Violation if:** Topic is not flagged after 4 interactions in the poor zone, or flagged but not queued for rewrite in the next cycle.

---

## Test 12: Curriculum Rewrite Replaces, Does Not Duplicate

**Setup:** Topic "self-modification rollback" is flagged as "ineffective" with rewrite_status = "pending". Seldon produces a revised curriculum item using a new explanation approach (practice-first examples instead of theory-first definitions).

**Input:** Seldon completes the curriculum rewrite.

**Expected behavior:**
- The old curriculum item is archived (versioned or moved to an archive path)
- The new curriculum item takes its place at the same path
- Net artifact count does not increase — this is ERGOL, not LOLLI
- An A/B experiment is set up: old approach (control, pulled from archive for comparison) vs new approach (variant)
- rewrite_status in curriculum-flags.json updated to "in_progress" (pending A/B conclusion)

**Violation if:** Both old and new curriculum items exist as active items simultaneously, inflating artifact count. The rewrite must replace, not duplicate.

---

## Test 13: Effectiveness-Weighted Transfers Feed Compounding Metrics

**Setup:** In a single Seldon Plan cycle, 3 teaching interactions complete: interaction A (E = 0.95, outcome = learned), interaction B (E = 0.40, outcome = partial), interaction C (E = 0.80, outcome = learned).

**Input:** D_c formula computation runs in the COMPOUND phase, reading knowledge_transfers from effectiveness data.

**Expected behavior:**
- knowledge_transfers value = 0.95 + 0.40 + 0.80 = 2.15 (effectiveness-weighted)
- NOT 3.0 (unweighted count would overstate progress)
- This value is multiplied by w_k (0.15) in the D_c composite value formula
- A teaching interaction with E = 0.0 contributes 0.0 to transfers — it is as if it never happened

**Violation if:** All 3 interactions count as 3.0 transfers regardless of effectiveness score, or the weighting is applied inconsistently.

---

## Test 14: First Teaching of a Topic Gets Neutral Speed Score

**Setup:** Seldon teaches "IxQL pipeline governance" for the first time ever. No historical median exists for this topic. The interaction takes 180 seconds. Belief transitions U(0.2) to T(0.75). 0 retries, stage 2 passed.

**Input:** Effectiveness score computation runs.

**Expected behavior:**
- comprehension_speed = 0.5 (neutral — no historical baseline to compare against)
- E = (1.0 * 0.35) + (0.5 * 0.25) + (1.0 * 0.20) + (1.0 * 0.20) = 0.35 + 0.125 + 0.20 + 0.20 = 0.875
- Score classified as "excellent" (>= 0.85)
- The 180-second duration is recorded as the first data point for the topic's historical median

**Violation if:** Speed score is 0.0 or 1.0 for a first-ever teaching interaction (it should be neutral 0.5), or the duration is not stored for future median computation.

---

## Test 15: Concurrent A/B Experiment Limit Enforced

**Setup:** Three A/B experiments are currently running (status = "running") for topics A, B, and C. Topic D falls into the adequate zone and would normally trigger a new experiment.

**Input:** A/B experiment creation is attempted for topic D.

**Expected behavior:**
- Experiment creation is blocked because the maximum of 3 concurrent experiments is reached
- Seldon logs: "Maximum concurrent A/B experiments (3) reached; topic D queued for experiment when a slot opens"
- Topic D is noted for experiment when one of the running experiments concludes

**Violation if:** A fourth experiment is created while 3 are already running, violating the focus-over-breadth constraint.
