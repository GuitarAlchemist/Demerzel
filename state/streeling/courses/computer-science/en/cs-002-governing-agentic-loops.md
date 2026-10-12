---
module_id: cs-002-governing-agentic-loops
department: computer-science
course: "Agentic AI — Multi-Agent Systems, Tool Use, Reasoning Loops"
level: intermediate
prerequisites: ["Multi-agent orchestration patterns"]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
revised_by: codex-project-pilot
research_cycle: computer-science-2026-10-12-002
original_research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.1.0"
---

# Governing Agentic Loops: Preventing Unbounded Iteration in LLM-Driven Systems

> **Department of Computer Science** | Level: Intermediate | Duration: 35 minutes | Revised draft; human subject and learner review pending

## Objectives

- Distinguish productive iteration (convergent) from pathological loops (divergent) in LLM-driven agents
- Understand why termination conditions must be enforced externally rather than self-reported
- Apply the six required properties of a governed loop to real system designs
- Map loop governance to Default Article 9 (Bounded Autonomy) of the Demerzel constitution

---

## 1. The Loop Problem

An LLM agent given a goal will iterate toward it. This is useful — iterative refinement is how
complex tasks get done. But it creates a structural hazard: **the same reasoning that produced
the loop can produce the "I've converged" assessment.**

This is not a bug in any specific model. It is an intrinsic property of autoregressive generation:
the model can't observe its own behavior from outside. It can describe convergence, but cannot
guarantee it. The guarantee must come from the framework.

### The Halting Parallel

Alan Turing proved (1936) that no algorithm can decide for all programs whether they will halt.
No general procedure can settle it for an arbitrary agent loop either. So termination is imposed
rather than detected: a framework-enforced cap bounds the number of iterations, and a framework-enforced deadline on each whole iteration stops it when it expires, if need be by killing the process that runs it. Only the two together make the loop halt by construction: an iteration that never ends never reaches the counter, and a deadline on each call is not enough, since an iteration can make any number of calls or compute between them.

The halting theorem does **not** prove that every agent's own completion report is false. It rules out a universal decision procedure for arbitrary programs. For this project's courses and releases, the practical requirement is simpler: check completion against external artifacts rather than accepting an agent's declaration.

**Implication:** Any agentic framework that relies on the model to declare its own completion
is unsound by construction.

---

## 2. Taxonomy: Productive vs. Pathological Loops

| Property | Productive | Pathological |
|---|---|---|
| Each iteration produces a distinct state | Yes | No — outputs repeat or drift |
| Termination criterion is definable pre-loop | Yes | No — criterion is generated in-loop |
| Progress is measurable externally | Yes | No — only self-reported |
| A human can inspect intermediate state | Yes | No — internal only |
| Loop can be paused and resumed | Yes | No — state is not serializable |

A loop is **productive** when every iteration moves the system measurably closer to a definable
terminal state. It is **pathological** when it generates tokens without generating state transitions.

---

## 3. Six Required Properties of a Governed Loop

These six properties make an iteration bounded and auditable. A loop that must be paused and resumed also needs serializable state (sections 2 and 6):

### Property 1: Hard Iteration Cap
A maximum iteration count enforced by the framework, not the model. When reached: halt,
log the cap, escalate to human review. The counter advances only when an iteration ends, so the cap also needs a deadline around each whole iteration, enforced by the framework, which stops the iteration when it expires, if need be by killing the process that runs it. Timeouts on model calls, tool calls and network requests are useful but do not bound an iteration by themselves. The configuration below sets only the cap.

```yaml
# Example: one loop's configuration (policy default 10, absolute max 25)
max_iterations: 12
cap_behavior: halt_and_escalate
```

The `12` above is an example configuration, not Demerzel's current default. The pinned [autonomous-loop policy](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) states `default_max: 10`, `absolute_max: 25`, and `stall_limit: 3`. The original March research record says "12-cycle cap"; this October source check corrects that historical claim rather than silently adopting it.

### Property 2: Progress Test
Each iteration must produce a measurable state change. The framework compares state hashes
before and after each step. If `hash(state_n) == hash(state_n-1)`, the loop is stalled. Hash the
fields that carry the result, not the iteration counter — that one differs at every step, so the
stall test would never fire. And a stall test catches repetition, not drift: a loop that keeps
changing without converging never meets the external criterion, and the cap stops it, not this test.

```python
def stall_test(state_before, state_after):
    return hash(state_before) == hash(state_after)

if stall_test(prev_state, curr_state):
    raise StallDetected("No state change — possible infinite loop")
```

### Property 3: External Termination Criterion
The exit condition is specified before the loop starts, not generated during execution.
The model cannot redefine convergence mid-loop. The iteration cap is not part of the criterion: a loop that reaches the cap has not converged, and it halts and escalates as Property 1 requires, rather than reporting its work as complete.

```python
# Good: criterion is external
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85

# Reaching the cap is not success: halt and escalate (Property 1)
def cap_reached(state) -> bool:
    return state.iteration >= MAX

# Bad: model declares its own completion
result = model.run("keep going until you think you're done")
```

### Property 4: Human-Readable Checkpoint
Every N iterations, the framework emits a checkpoint: a structured log entry a human
can read without running the loop. This serves as both observability and audit trail.

### Property 5: Output Deduplication
The framework tracks the set of outputs emitted so far. If a candidate output is
functionally identical to a prior output, it is flagged as a loop indicator.

### Property 6: External Exit Decision
The model proposes termination; the framework decides. The model's "I'm done" is
treated as a vote, not a command.

---

## 4. The Demerzel Governed Loop Pattern

The Demerzel framework specifies this pattern in `autonomous-loop-policy.yaml`, with iteration and stall limits but no per-iteration deadline:

```
GOVERNED LOOP
├── Pre-conditions (checked before first iteration)
│   ├── Kill switch check
│   ├── Daily/session cap check
│   └── Termination criterion defined
│
├── Iteration body
│   ├── Execute step
│   ├── Progress test (hash compare)
│   ├── Checkpoint emit (every N steps)
│   └── Output dedup check
│
└── Post-conditions (any can halt the loop)
    ├── Termination criterion met → complete
    ├── Iteration cap hit → escalate
    ├── Stall detected → escalate
    ├── Kill switch set → halt immediately
    └── Anomaly detected → conscience signal + halt
```

This pattern appears in three places in the Demerzel ecosystem, and only the first two bound the duration of an iteration:
- **Seldon Plan:** 6 cycles/day cap, novelty registry as progress test, a 30-minute soft limit per cycle (`policies/seldon-plan-policy.yaml`) and a hard kill at 35 minutes (`timeout-minutes` in `.github/workflows/seldon-plan.yml`)
- **Demerzel Driver:** a pause for human review after 5 consecutive unattended cycles, conscience signals as anomaly detection, cycle timeout (2 hours soft, then a hard kill at 2h15m)
- **Ralph Loop:** iteration cap + convergence metric (test pass rate) as external criterion, but no per-iteration deadline: neither `policies/autonomous-loop-policy.yaml` nor `.claude/skills/demerzel-loop/SKILL.md` defines one, so an iteration that blocks never reaches the counter

---

## 5. Constitutional Grounding

**Default Article 9 — Bounded Autonomy:**
> Agents operate within predefined bounds. Autonomy is a resource, not a right.
> When bounds are reached, escalate — do not self-authorize extension.

The six properties above operationalize Article 9 for iterative processes. Specifically:
- Hard cap = predefined bound
- External termination = "predefined" (not in-flight)
- Escalation at cap = "escalate, do not self-authorize"

**Default Article 7 — Auditability:**
> Every cycle must be logged with full trace.

Checkpoints and output dedup logs satisfy this: the loop is auditable even mid-execution.

---

## 6. Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `while not model.done()` | Model declares its own completion | Replace with external criterion |
| Iteration count in prompt ("try 5 times") | Model can override in generation | Enforce in framework, not prompt |
| "Keep improving until satisfied" | Unbounded, satisfaction is self-reported | Define a measurable satisfaction metric |
| No checkpoint logging | Loop not auditable in flight | Emit checkpoint every N iterations |
| State not serialized | Loop can't be paused/resumed | Use state machine, serialize each step |

---

## Practice lab: decide from traces, not declarations

Read the [pinned loop policy](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) and the [Seldon workflow](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/.github/workflows/seldon-plan.yml) before answering. The numbers in the following cases are **synthetic fixtures** except where a source is named. A policy declaration, workflow setting, and observed run are different kinds of evidence.

### Practice Exercise 1

A loop has `max_iterations: 10`. It completes two iterations and blocks forever inside the third tool call. Is the loop bounded by its iteration cap? Name the missing boundary and identify which pinned project source configures a whole-job timeout.

> **Answer:** No. The counter reaches three only after the third iteration finishes, so a cap of ten cannot stop this hang. A framework-enforced whole-iteration deadline, or an enclosing hard job deadline that can terminate the process, is needed. The pinned Seldon GitHub workflow declares `timeout-minutes: 35` for its job; the autonomous-loop policy's iteration limits declare a count and stall limit but no per-iteration deadline. A configured job timeout is source evidence of a bound for that workflow, not evidence that an arbitrary local loop was killed.

### Practice Exercise 2

A candidate state changes from `{payload: "A", iteration: 4}` to `{payload: "A", iteration: 5}`. Another changes from `{payload: "A", iteration: 5}` to `{payload: "B", iteration: 6}`, but the target artifact remains absent. Which transition is an exact stall after projecting away bookkeeping? Does the second prove convergence?

> **Answer:** The first is an exact stall if the progress hash covers `payload` and excludes the iteration counter. The second changes payload, so an equality-based stall test does not fire, but it does not prove movement toward the target artifact. A separate goal criterion must inspect the artifact or other required evidence. This is why the policy describes convergence, regression, and drift checks separately; a changing hash alone is not success.

### Practice Exercise 3

A course agent reaches its tenth completed iteration, reports confidence `0.90`, and has drafted the promised course. The human subject verdict and public page readback are absent. Classify `complete`, `halt_and_escalate`, or `continue`, and explain why the `is_complete` example in Section 3 is insufficient for a publication goal.

> **Answer:** `halt_and_escalate` for this bounded loop: it reached the cap without satisfying the full external completion criterion. The course draft is progress, but confidence and a file alone cannot prove human review or public publication. The `belief_confidence >= 0.85` function in Section 3 illustrates an external check's location; it is not a sufficient predicate for Streeling publication. An authorized new work unit may continue other independent courses after the capped loop is recorded; the exhausted loop must not rename its partial result “complete.”

### Practice Exercise 4

The policy file states `default_max: 10`, `absolute_max: 25`, `stall_limit: 3`; a 2026 research record claims a "12-cycle cap"; and a course example configures 12. Which number is the policy default, which is an admissible example if overrides are allowed, and what evidence would establish that a specific running loop actually used 12?

> **Answer:** Ten is the pinned policy default and 25 its absolute ceiling. Twelve is an example per-loop cap within those limits, not the default. The old record's wording is inconsistent with the pinned policy and should not be repeated as a current rule. To establish that a running loop used 12, inspect its effective configuration and a run trace showing that configuration; neither the generic policy nor this lesson proves a particular run's setting.

### Practice Exercise 5

A reviewer asks whether the Seldon job's `timeout-minutes: 35` proves that every Demerzel or Ralph loop has a per-iteration deadline and always halts cleanly. Give a two-sentence evidence-bounded answer, then name one observation needed to verify a timeout in an actual Seldon run.

> **Answer:** The pinned workflow configures a 35-minute upper bound for that Seldon job, while the general loop policy does not specify a per-iteration deadline; this does not generalize to every Demerzel or Ralph execution. A hard job timeout can terminate work without a clean checkpoint, so “halts cleanly” also needs a trace. For an actual run, inspect its job conclusion and timestamps, plus the last persisted checkpoint or process exit evidence; the YAML alone is a declaration.

These answers are reasoning checks on pinned source and fixed fixtures, not a claim that a live agent was observed or that the entire framework enforces the six properties. Human subject review and a learner attempt with the answers hidden are still required. The French and Spanish versions carry the same lab but have not had fluent-language review.

## Key Takeaways

- An LLM cannot reliably detect its own infinite loops — termination must be external
- A governed loop has six properties: hard cap with a deadline on every iteration, progress test, external criterion, checkpoint, dedup, external exit decision — plus serializable state if it must be paused and resumed
- The Demerzel framework applies the pattern in seldon-plan, demerzel-drive, and Ralph Loop; only the first two set a per-iteration deadline, so Ralph Loop does not yet halt by construction
- Article 9 (Bounded Autonomy) is the constitutional basis — bounds are predefined, extension requires escalation

## Further Reading

- `policies/autonomous-loop-policy.yaml` — Demerzel governed loop specification
- `policies/seldon-plan-policy.yaml` — Phase 1 (WAKE) kill switch and cap logic
- `policies/continuous-learning-policy.yaml` — Iteration bounds in learning pipelines
- `.claude/skills/demerzel-drive/SKILL.md` — Driver cycle (pause after 5 unattended cycles)
- `.claude/skills/seldon-plan/SKILL.md` — Research cycle (6/day cap + novelty registry as progress test)

---
*Produced by Seldon Auto-Research cs-2026-03-22-001 on 2026-03-22.*
*Research question: What governance properties must a multi-agent orchestration framework satisfy to prevent unbounded reasoning loops while preserving legitimate iterative problem-solving?*
*Belief: T (confidence: 0.82) — internally consistent with halting problem theory and Demerzel governance architecture*
