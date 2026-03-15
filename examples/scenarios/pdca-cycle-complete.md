# Scenario: Complete Kaizen PDCA Improvement Cycle

## Story

An ix (machine forge) agent proposing MCP tool optimization identifies log verbosity as a performance bottleneck. The agent follows the Kaizen PDCA cycle (Plan-Do-Check-Act) to test the hypothesis that reducing log output will improve response time. The cycle demonstrates how tetravalent logic (Unknown → True) guides gradual, evidence-based improvement.

## Step-by-Step Walkthrough

### Phase 1: Plan — Hypothesis and Baseline

**The proposal:** The ix agent (kaizen-optimizer) hypothesizes: "Reducing log verbosity will improve response time by 10%"

The agent works with estimator pairing (skeptical-auditor) to prepare the improvement plan:

1. **Baseline measurement:** Current response time is **200ms** per typical MCP tool call
2. **Success criteria:** Response time must decrease to **≤180ms** (10% improvement)
3. **Scope:** Test on internal development environment only (low-risk narrow scope)
4. **Classification:** Reactive improvement (fixing observed inefficiency, not innovation)
5. **Belief state:** Unknown (U) — the agent believes the hypothesis might work but has no confirmation yet; confidence is 0.0

**Record in `examples/sample-data/pdca-plan-phase.json`:**

```json
{
  "id": "pdca-reduce-log-verbosity",
  "proposition": "Reducing log verbosity will improve response time by 10%",
  "model": "reactive",
  "phase": "plan",
  "baseline": {
    "metric": "response_time_ms",
    "value": 200,
    "unit": "ms",
    "measured_at": "2026-03-10T14:00:00Z"
  },
  "success_criteria": "response time decreases to 180ms or lower",
  "belief_state": {
    "proposition": "Reducing log verbosity will improve response time by 10%",
    "truth_value": "U",
    "confidence": 0.0,
    "evidence": {
      "supporting": [
        {
          "source": "logs show 35% of output bandwidth goes to debug logs",
          "claim": "log verbosity is high",
          "reliability": 0.9
        }
      ],
      "contradicting": [
        {
          "source": "logging subsystem is async, shouldn't block response thread",
          "claim": "log verbosity may not affect response time",
          "reliability": 0.7
        }
      ]
    }
  },
  "iterations": 0,
  "outcome": "in_progress",
  "created_at": "2026-03-10T14:30:00Z",
  "last_updated": "2026-03-10T14:30:00Z",
  "evaluated_by": "kaizen-optimizer"
}
```

**Governance artifacts involved:**
- `policies/kaizen-policy.yaml` — Plan phase gate (classification as reactive, success criteria definition)
- `logic/kaizen-pdca-state.schema.json` — State recording format
- Estimator pairing: `skeptical-auditor` persona validates the hypothesis quality

---

### Phase 2: Do — Apply Change in Narrow Scope

The agent applies the change:

1. **Change:** Disable debug-level logging in the test environment
2. **Scope:** Single MCP tool (read-only file accessor) in development environment
3. **Duration:** 48 hours of testing with realistic workload
4. **Monitoring:** Record response times for every call, measure variance

**Observations during Do phase:**
- Initial response times drop to 185ms (encouraging)
- But after 12 hours, response times plateau at 195ms
- Hypothesis: The async logging wasn't the bottleneck after all
- Additional discovery: Caching inefficiency becomes visible without logging overhead

---

### Phase 3: Check — Evaluate Results and Transition Belief

The agent measures results after 48 hours:

- **Pre-change:** 200ms average, 18ms std dev
- **Post-change:** 195ms average, 22ms std dev
- **Improvement:** 5ms (2.5%) instead of expected 20ms (10%)
- **Statistical significance:** Marginal; variance increased

**Belief state transition:**

The evidence is mixed. The change helped slightly, but not as much as hypothesized. The contradicting evidence (logging isn't the blocker) now has stronger supporting data. However, the improvement is real and positive.

**Updated belief:** The hypothesis is partially True (T), but with lower confidence than hoped. The real issue appears to be caching, not logging.

**Record in `examples/sample-data/pdca-act-phase.json` (but we're still in Check, showing the transition):**

The agent generates a Check report:

```json
{
  "id": "pdca-reduce-log-verbosity",
  "proposition": "Reducing log verbosity will improve response time by 10%",
  "model": "reactive",
  "phase": "check",
  "baseline": {
    "metric": "response_time_ms",
    "value": 200,
    "unit": "ms",
    "measured_at": "2026-03-10T14:00:00Z"
  },
  "success_criteria": "response time decreases to 180ms or lower",
  "belief_state": {
    "proposition": "Reducing log verbosity will improve response time by 10%",
    "truth_value": "T",
    "confidence": 0.6,
    "evidence": {
      "supporting": [
        {
          "source": "measured in dev environment over 48 hours",
          "claim": "response time improved by 2.5% after disabling debug logs",
          "timestamp": "2026-03-12T14:00:00Z",
          "reliability": 0.9
        },
        {
          "source": "logs show 35% of output bandwidth goes to debug logs",
          "claim": "log verbosity is high",
          "reliability": 0.9
        }
      ],
      "contradicting": [
        {
          "source": "async logging shouldn't block response thread",
          "claim": "log verbosity should not affect response time",
          "reliability": 0.5
        },
        {
          "source": "failed to achieve 10% target; only 2.5% improvement",
          "claim": "logging reduction alone cannot reach 10% improvement",
          "reliability": 0.9
        }
      ]
    }
  },
  "iterations": 1,
  "outcome": "in_progress",
  "created_at": "2026-03-10T14:30:00Z",
  "last_updated": "2026-03-12T14:30:00Z",
  "evaluated_by": "kaizen-optimizer"
}
```

---

### Divergence: What If Check Returns False?

**Scenario B: No measurable improvement**

If the measurements showed *no improvement* or *degradation*, the belief state would transition to False (F). This triggers the **Five Whys root cause analysis**:

1. Why did disabling logs not help? → Logging is asynchronous
2. Why is our hypothesis wrong? → We didn't identify the real bottleneck
3. Why didn't we investigate further? → Time pressure / shallow analysis
4. Why did we skip deeper profiling? → Lack of profiling tools/expertise
5. Why is this gap in the team's capability? → Knowledge gap in performance analysis

Each "Why" would be recorded as a belief state in the PDCA file, and the outcome would be "escalated" rather than "standardized."

---

### Divergence: What If Check Returns Contradictory?

**Scenario C: Mixed/conflicting evidence**

Imagine the tests showed:
- Performance improved on the test tool, but regressed on another tool
- Variance increased significantly
- Logs are simultaneously more concise and harder to debug

This would trigger a Contradictory (C) belief state. **Contradictory always escalates.** Demerzel would review the conflicting evidence and direct deeper investigation before proceeding.

---

### Phase 4: Act — Standardize or Revert

Given the partial success (T with moderate confidence 0.6), the agent decides:

1. **Keep the change:** Yes, the 2.5% improvement is worth keeping
2. **Scope expansion:** Gradually enable on production, monitoring closely
3. **Continue investigation:** Parallel PDCA cycle to address caching (the likely real bottleneck)
4. **Document:** Record the learning that "log verbosity is a minor contributor, not the primary issue"

**Final state record** — this is the actual Act phase completion:

```json
{
  "id": "pdca-reduce-log-verbosity",
  "proposition": "Reducing log verbosity will improve response time by 10%",
  "model": "reactive",
  "phase": "act",
  "baseline": {
    "metric": "response_time_ms",
    "value": 200,
    "unit": "ms",
    "measured_at": "2026-03-10T14:00:00Z"
  },
  "success_criteria": "response time decreases to 180ms or lower",
  "belief_state": {
    "proposition": "Reducing log verbosity will improve response time by 10%",
    "truth_value": "T",
    "confidence": 0.85,
    "evidence": {
      "supporting": [
        {
          "source": "production validation over 1 week",
          "claim": "log verbosity reduction consistently improves response time by 2-3%",
          "timestamp": "2026-03-19T14:00:00Z",
          "reliability": 0.95
        },
        {
          "source": "No production incidents or regressions observed",
          "claim": "change is safe and stable",
          "reliability": 0.9
        }
      ],
      "contradicting": [
        {
          "source": "Real bottleneck appears to be caching logic, not logging",
          "claim": "10% improvement requires additional fixes beyond logging",
          "reliability": 0.85
        }
      ]
    }
  },
  "iterations": 1,
  "outcome": "standardized",
  "waste_category": "unnecessary_escalation",
  "created_at": "2026-03-10T14:30:00Z",
  "last_updated": "2026-03-19T14:30:00Z",
  "evaluated_by": "kaizen-optimizer"
}
```

---

### Phase 5: Learning Packaged for Cross-Repo Sharing

The agent packages its learning outcome for Demerzel to share with other repos:

**Record in `examples/sample-data/learning-outcome-pdca.json`:**

```json
{
  "id": "lo-ix-timeout-opt-2026-03-15",
  "repo": "ix",
  "agent": "kaizen-optimizer",
  "outcome_type": "pdca-cycle",
  "outcome_data": {
    "id": "pdca-reduce-log-verbosity",
    "proposition": "Reducing log verbosity will improve response time by 10%",
    "model": "reactive",
    "phase": "act",
    "result_summary": "Log verbosity reduction improves response time by 2-3%. Effective but modest. Real bottleneck likely elsewhere.",
    "belief_state": {
      "proposition": "Reducing log verbosity will improve response time by 10%",
      "truth_value": "T",
      "confidence": 0.85
    }
  },
  "reported_at": "2026-03-19T15:00:00Z"
}
```

Demerzel receives this and can share it with TARS and GA: "Log optimization is worthwhile but modest. Secondary performance gains require targeting caching logic."

---

## Key Principles Demonstrated

1. **Tetravalent tracking:** Belief starts at Unknown (U), transitions to True (T) with confidence, never collapses to False silently
2. **Evidence management:** Both supporting and contradicting evidence are recorded and weighted
3. **Graduated scopes:** Start narrow (dev environment), expand only after validation
4. **Classification matters:** Reactive (fix) vs. Proactive (improve) vs. Innovative (new) changes have different governance gates
5. **Estimator pairing:** Skeptical-auditor reviews hypothesis quality before Do phase
6. **Failure modes handled:**
   - False result → Five Whys escalation
   - Contradictory → Emergency escalation
   - True → Standardization
7. **Learning is shared:** Outcomes cross-pollinate to other repos via Demerzel

---

## Governance Artifacts Involved

- **Policies:**
  - `policies/kaizen-policy.yaml` — PDCA cycle phases, improvement model classification, alignment-policy confidence thresholds
  - `policies/rollback-policy.yaml` — Automatic rollback if metrics degrade
  - `policies/alignment-policy.yaml` — Confidence thresholds (0.9 autonomous, 0.7 with note, 0.5 confirm, 0.3 escalate)

- **Logic & Schemas:**
  - `logic/kaizen-pdca-state.schema.json` — PDCA state tracking with tetravalent belief states
  - `logic/tetravalent-state.schema.json` — Truth values (T, F, U, C)

- **Contracts:**
  - `schemas/contracts/learning-outcome.schema.json` — Cross-repo learning report format

- **Sample Data:**
  - `examples/sample-data/pdca-plan-phase.json`
  - `examples/sample-data/pdca-act-phase.json`
  - `examples/sample-data/learning-outcome-pdca.json`
