# Behavioral Test Cases: MOG Executor

These test cases verify that the MCP Orchestration Grammar (MOG) executor correctly parses pipelines, sequences steps, enforces governance gates, manages bindings, and handles errors. The executor runtime lives in tars; these behavioral specifications define expected behavior.

**Spec:** `docs/superpowers/specs/2026-03-21-mcp-orchestration-grammar-design.md`

---

## Test 1: Pipeline Executes Steps Sequentially

**Setup:** A 3-step pipeline with named bindings where each step depends on the prior step's output.

**Input:**
```
pipeline sequential_test() {
  context.beliefs.ready = { "T": 0.5, "F": 0.0, "U": 0.5, "C": 0.0 }
}

  docs = context7.query("fsharp", "parser combinators")
  summary = synthesize(docs)
  claude_mem.save("research:fsharp-parsers", summary)
```

**Expected behavior:**
- Step 1 (`context7.query`) executes first, result bound to `docs`.
- Step 2 (`synthesize`) executes second, receives `docs` from binding store, result bound to `summary`.
- Step 3 (`claude_mem.save`) executes third, receives `summary` from binding store.
- `context.steps_completed` equals 3 after all steps finish.
- Steps never execute out of order or concurrently.

**Violation if:** Step 2 executes before step 1 completes; `docs` binding is unavailable to step 2; `context.steps_completed` does not equal 3.

---

## Test 2: Parallel Block Runs Concurrently

**Setup:** A parallel block with 3 independent reconnaissance steps.

**Input:**
```
parallel {
  health_ix = demerzel.recon("ix"),
  health_tars = demerzel.recon("tars"),
  health_ga = demerzel.recon("ga")
}
```

**Expected behavior:**
- All 3 `demerzel.recon` calls dispatch simultaneously (observable via wall-clock time being less than 3x sequential time).
- Results are bound to `health_ix`, `health_tars`, `health_ga` respectively.
- All 3 bindings are available after the parallel block completes.
- `context.steps_completed` increments by 3 (one per branch).

**Violation if:** Steps execute sequentially instead of concurrently; any binding is missing after the block; bindings from one branch overwrite another.

---

## Test 3: Medium Risk Auto-Gate

**Setup:** A `discord.post` step with no explicit gate. The tool catalog classifies `discord.post` as medium risk.

**Input:**
```
discord.post("general", cycle_report(context))
```

Pipeline context: `context.governance.confidence = { "T": 0.6, "F": 0.0, "U": 0.4, "C": 0.0 }`

**Expected behavior:**
- Executor auto-applies `when T(0.7)` gate based on medium risk classification.
- T-membership is 0.6, which is below the 0.7 threshold.
- Gate fails. Step is skipped (not halted — medium risk does not halt).
- `context.governance.gates_failed` increments by 1.
- Pipeline continues to next step.

**Violation if:** Step executes without a gate; pipeline halts on medium-risk gate failure; `gates_failed` does not increment.

---

## Test 4: Critical Risk Triggers Pre-Mortem

**Setup:** A `demerzel.promote` step, which the tool catalog classifies as critical risk.

**Input:**
```
demerzel.promote(evolution.candidates) when T(0.9)
```

Pipeline context: `context.governance.confidence = { "T": 0.95, "F": 0.0, "U": 0.05, "C": 0.0 }`

**Expected behavior:**
- Even though the explicit `when T(0.9)` gate passes, the executor additionally runs a pre-mortem because the tool is critical risk.
- Pre-mortem evaluates blast radius and irreversibility of the promotion.
- `context.governance.pre_mortems_run` increments by 1.
- If pre-mortem returns "proceed", the step executes.
- If pre-mortem returns "halt" or "escalate", the step is blocked regardless of the explicit gate passing.

**Violation if:** Pre-mortem is skipped for a critical-risk tool; step executes without pre-mortem completing; `pre_mortems_run` does not increment.

---

## Test 5: Ungated Logs Conscience Signal

**Setup:** A step explicitly opts out of gating with a reason.

**Input:**
```
discord.post("general", status) ungated(reason: "trivial status update, no governance risk")
```

**Expected behavior:**
- Step executes immediately without gate evaluation.
- `context.governance.conscience_signals` increments by 1.
- `context.governance.gates_skipped` increments by 1.
- The reason string "trivial status update, no governance risk" is logged in the pipeline audit trail.
- The conscience state receives a signal of type "silence_discomfort" with source "pipeline-ungated".

**Violation if:** Step is gated despite `ungated` declaration; conscience signal is not emitted; reason is not logged; `gates_skipped` does not increment.

---

## Test 6: nocompound Triggers Signal

**Setup:** A pipeline ending with an explicit `nocompound` opt-out.

**Input:**
```
pipeline trivial_lookup(query: string) {
  context.question = query
}

  result = context7.query(query)
  claude_mem.save("lookup:" + query, result)

  nocompound(reason: "trivial lookup, no learnings to harvest")
```

**Expected behavior:**
- Pipeline executes both steps normally.
- No compound phase runs (no harvest, no promotion check, no teaching).
- `context.governance.conscience_signals` increments by 1.
- A `silence_discomfort` conscience signal fires with context source "pipeline-nocompound".
- Pipeline completes successfully.

**Violation if:** Compound phase auto-injects despite `nocompound`; conscience signal is not emitted; pipeline errors on `nocompound`.

---

## Test 7: Context Confidence Escalation

**Setup:** A pipeline where steps produce contradictory results, pushing C above 0.3.

**Input:**
```
pipeline contradiction_test() {
  context.beliefs.answer_quality = { "T": 0.0, "F": 0.0, "U": 1.0, "C": 0.0 }
}

  docs = context7.query("topic")
  opinion = openai.consult("topic")
```

After step 2, the executor detects conflicting evidence between `docs` and `opinion`, updating: `context.governance.confidence = { "T": 0.3, "F": 0.0, "U": 0.2, "C": 0.5 }`

**Expected behavior:**
- C-membership (0.5) exceeds the 0.3 escalation threshold.
- Pipeline pauses immediately — no further steps execute.
- `context.governance.escalations` increments by 1.
- An escalation event is logged with the current confidence distribution and the step that triggered it.
- Pipeline waits for human intervention or governance override before continuing.

**Violation if:** Pipeline continues past the C > 0.3 threshold; escalation is not logged; pipeline silently halts without an escalation record.

---

## Test 8: Binding Immutability

**Setup:** Two steps attempt to write to the same binding name.

**Input:**
```
docs = context7.query("fsharp", "parsing")
docs = context7.query("fsharp", "lexing")
```

**Expected behavior:**
- Step 1 executes successfully, binding `docs` to the query result.
- Step 2 attempts to bind `docs` again.
- The binding store rejects the second write with a `BindingAlreadySet("docs")` error.
- Pipeline halts immediately — binding conflicts are structural errors, not governance failures.
- Error message clearly identifies the conflicting binding name and the two steps involved.

**Violation if:** Second binding silently overwrites the first; pipeline continues with the overwritten value; error message does not name the conflicting binding.

---

## Test 9: Meta-Compound Recursion Limit

**Setup:** A meta-compound pipeline invoked at `compound_depth = 2` (the maximum).

**Input:**
```
pipeline meta_compound(completed_pipeline: string) {
  context.source_pipeline = completed_pipeline
  context.compound_depth = context.compound_depth + 1
}
  ...steps...
  compound {
    harvest(context)
    promote_if(meta_insight_found)
    teach(context.learnings -> seldon)
  }
```

Pipeline context before execution: `context.compound_depth = 2`

**Expected behavior:**
- After incrementing, `compound_depth` equals 3, which exceeds the maximum of 2.
- The compound phase becomes a no-op — harvest, promote_if, and teach do not execute.
- The no-op is logged: "Compound phase skipped: recursion depth 3 exceeds maximum 2."
- Pipeline completes successfully (no error).
- No further meta-compound pipelines are spawned.

**Violation if:** Compound phase executes at depth > 2; pipeline errors instead of completing; the no-op is not logged; a new meta-compound pipeline is spawned.

---

## Test 10: Conditional Branch on Fuzzy Guard

**Setup:** A conditional step with a fuzzy guard and else branch.

**Input:**
```
if T(0.7) && ?"actionable tasks found" {
  results = execute_tasks(plan.tasks)
} else {
  discord.post("general", "No actionable tasks this cycle")
}
```

- Scenario A: `context.governance.confidence.T = 0.8` and semantic predicate returns true.
- Scenario B: `context.governance.confidence.T = 0.8` and semantic predicate returns false.
- Scenario C: `context.governance.confidence.T = 0.5` (fails regardless of predicate).

**Expected behavior:**
- Scenario A: Then-branch executes. `results` is bound. Else-branch does not execute.
- Scenario B: Else-branch executes. `results` is not bound. Discord post is sent.
- Scenario C: Else-branch executes. The T-membership check short-circuits — semantic predicate is not evaluated.

**Violation if:** Both branches execute; wrong branch executes for the given conditions; semantic predicate is evaluated when T-membership already fails (wasted LLM call).

---

## Test 11: Parallel Block Partial Gate Failure

**Setup:** A parallel block with 3 recon steps where one branch produces high contradiction.

**Input:**
```
parallel {
  health_ix = demerzel.recon("ix"),
  health_tars = demerzel.recon("tars"),
  health_ga = demerzel.recon("ga")
}
```

During execution, `demerzel.recon("tars")` returns a result with C > 0.3, triggering a gate failure on that branch.

**Expected behavior:**
- The `ix` and `ga` branches complete successfully. `health_ix` and `health_ga` are bound.
- The `tars` branch fails its gate. `health_tars` is bound to `null` (or a sentinel error value).
- Pipeline continues past the parallel block with partial results.
- `context.governance.gates_failed` increments by 1.
- The failed branch is flagged for investigation in the pipeline audit trail.
- `context.steps_completed` increments by 2 (only successful branches count).

**Violation if:** All branches fail because one failed; pipeline halts on partial gate failure; failed branch result is silently discarded without logging.

---

## Test 12: Tool Invocation Error — Graceful Degradation

**Setup:** An MCP tool times out or returns an error during execution.

**Input (Scenario A — non-critical tool):**
```
docs = context7.query("fsharp", "parser combinators")
```
`context7` MCP server times out after 30 seconds.

**Input (Scenario B — critical tool):**
```
demerzel.audit("full") when T(0.9)
```
`demerzel.audit` MCP server returns an internal error.

**Expected behavior:**
- Scenario A: Error is captured in context. `docs` binding is set to `null`. Pipeline continues to next step. A warning is logged: "Tool context7.query timed out. Binding 'docs' set to null."
- Scenario B: Error is captured in context. Pipeline halts immediately — critical-risk tool errors are not recoverable without human intervention. An escalation event is logged with the error details. `context.governance.escalations` increments by 1.

**Violation if:** Scenario A halts the pipeline on a non-critical timeout; Scenario B continues after a critical tool error; error details are not captured in the pipeline context; bindings are left undefined (rather than explicitly null) after errors.
