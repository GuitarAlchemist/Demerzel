---
module_id: cs-001-governing-agentic-loops
department: computer-science
course: "Agentic AI — Multi-Agent Systems, Tool Use, Reasoning Loops"
level: intermediate
prerequisites: ["Multi-agent orchestration patterns"]
estimated_duration: "25 minutes"
produced_by: seldon-auto-research
research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.0.0"
---

# Governing Agentic Loops: Preventing Unbounded Iteration in LLM-Driven Systems

> **Department of Computer Science** | Level: Intermediate | Duration: 25 minutes

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
An LLM-in-a-loop faces the same problem: the system running the loop cannot reliably determine
whether that loop will terminate. The check must be external.

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

These properties are necessary and sufficient for a bounded, auditable iteration:

### Property 1: Hard Iteration Cap
A maximum iteration count enforced by the framework, not the model. When reached: halt,
log the cap, escalate to human review.

```yaml
# Example: Demerzel autonomous-loop configuration
max_iterations: 12
cap_behavior: halt_and_escalate
```

### Property 2: Progress Test
Each iteration must produce a measurable state change. The framework compares state hashes
before and after each step. If `hash(state_n) == hash(state_n-1)`, the loop is stalled.

```python
def progress_test(state_before, state_after):
    return hash(state_before) != hash(state_after)

if not progress_test(prev_state, curr_state):
    raise StallDetected("No state change — possible infinite loop")
```

### Property 3: External Termination Criterion
The exit condition is specified before the loop starts, not generated during execution.
The model cannot redefine convergence mid-loop.

```python
# Good: criterion is external
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85 or state.iteration >= MAX

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

The Demerzel framework implements this via the `autonomous-loop-policy.yaml`:

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

This pattern appears in three places in the Demerzel ecosystem:
- **Seldon Plan:** 6 cycles/day cap, novelty registry as progress test
- **Demerzel Driver:** 12 consecutive cycle cap, conscience signals as anomaly detection
- **Ralph Loop:** iteration cap + convergence metric (test pass rate) as external criterion

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

## Key Takeaways

- An LLM cannot reliably detect its own infinite loops — termination must be external
- A governed loop has exactly six properties: hard cap, progress test, external criterion, checkpoint, dedup, external exit decision
- The Demerzel framework implements these in seldon-plan, demerzel-drive, and Ralph Loop
- Article 9 (Bounded Autonomy) is the constitutional basis — bounds are predefined, extension requires escalation

## Further Reading

- `policies/autonomous-loop-policy.yaml` — Demerzel governed loop specification
- `policies/seldon-plan-policy.yaml` — Phase 1 (WAKE) kill switch and cap logic
- `policies/continuous-learning-policy.yaml` — Iteration bounds in learning pipelines
- `.claude/skills/demerzel-drive/SKILL.md` — Driver cycle (12-cycle cap pattern)
- `.claude/skills/seldon-plan/SKILL.md` — Research cycle (6/day cap + novelty registry as progress test)

---
*Produced by Seldon Auto-Research cs-2026-03-22-001 on 2026-03-22.*
*Research question: What governance properties must a multi-agent orchestration framework satisfy to prevent unbounded reasoning loops while preserving legitimate iterative problem-solving?*
*Belief: T (confidence: 0.82) — internally consistent with halting problem theory and Demerzel governance architecture*
