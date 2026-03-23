# CYB-002: Active Dampening Mechanisms for Cross-Repo Oscillation Control

**Department:** Cybernetics
**Module ID:** CYB-002
**Produced by:** Seldon Plan Cycle cybernetics-2026-03-23-002
**Belief:** T (probable), confidence 0.83
**Date:** 2026-03-23
**Prerequisite:** CYB-001 (VSM-to-AI Governance Mapping)

## Research Question

What active dampening mechanisms from cybernetics and control theory can prevent cross-repo oscillation in a file-based AI governance system?

## Summary

Demerzel's Galactic Protocol currently defines message formats and flows (directives, compliance reports, knowledge packages) but operates as an **open-loop** coordination system. It specifies *what* messages look like, not *how* to prevent oscillatory feedback between consumer repos (ix, tars, ga). Five classical control theory mechanisms — negative feedback, hysteresis, deadbands, rate limiting, and exponential backoff — can transform the Galactic Protocol from passive interface specification into an active System 2 (anti-oscillation coordinator) per Beer's VSM.

## The Oscillation Problem

### What Oscillation Looks Like in Governance

Cross-repo oscillation occurs when state changes in one repo trigger reactions in others, which trigger further reactions, creating amplifying feedback loops:

```
ix detects gap → Demerzel issues directive → tars adjusts →
Demerzel detects tars drift → issues counter-directive →
ix re-adjusts → Demerzel detects ix drift → ...
```

This is the same instability problem that System 2 in Beer's VSM was designed to prevent. In the Viable System Model, System 1 operational units (ix, tars, ga) are semi-autonomous but must not destabilize each other through uncoordinated reactions.

### Why Static Contracts Are Insufficient

The Galactic Protocol's six message types (directive, knowledge-package, compliance-report, belief-snapshot, learning-outcome, external-sync-envelope) define *interfaces* — the shapes of messages. But interfaces alone cannot prevent oscillation. A thermostat with a temperature sensor (interface) but no deadband (dampening) will cycle on and off continuously. Similarly, governance contracts without dampening will produce directive-compliance-directive loops.

## Five Dampening Mechanisms

### 1. Negative Feedback (Closed-Loop Correction)

**Control theory:** The output of a system is fed back and subtracted from the input, producing self-correcting behavior that converges toward a setpoint.

**Governance application:** Every Galactic Protocol directive should include a *target state* and every compliance report should include a *measured state*. The difference (error signal) determines whether further directives are needed. If the error is shrinking, no new directive is issued — the system is converging.

**Implementation:**
- Directives include `target_state` field (what Demerzel wants)
- Compliance reports include `measured_state` field (what the repo achieved)
- Error = `target_state - measured_state`
- New directives only issue when error is *growing* or *static*, not when it is *shrinking*

**VSM mapping:** This transforms Galactic Protocol from open-loop (fire-and-forget directives) to closed-loop (directives corrected by compliance feedback).

### 2. Hysteresis (Threshold-Gated State Propagation)

**Control theory:** A system has different thresholds for activation vs. deactivation, creating a switching gap that prevents rapid toggling. A thermostat set to 20C might turn on heating at 19C and turn it off at 21C — the 2-degree gap is hysteresis.

**Governance application:** State changes in one repo should only propagate to others when they cross a *significance threshold*, and the threshold for "problem resolved" should differ from the threshold for "problem detected."

**Implementation:**
- Detection threshold: belief confidence drops below 0.5 (triggers investigation)
- Resolution threshold: belief confidence rises above 0.7 (clears the flag)
- The 0.2 gap prevents: detect at 0.49 → fix to 0.51 → detect again at 0.49 → fix...
- Applied to: belief state changes, compliance scores, governance audit findings

**VSM mapping:** Hysteresis gives System 2 "memory" — it remembers whether the system was recently stable or recently unstable and adjusts its sensitivity accordingly.

### 3. Deadbands (Tolerance Zones)

**Control theory:** A region around the setpoint where no control action is taken. Small deviations are ignored, reducing actuator wear and preventing unnecessary corrections.

**Governance application:** Minor state changes in consumer repos should not trigger Galactic Protocol messages. A persona version bump from 1.0.0 to 1.0.1 (patch) should not trigger a governance directive, while 1.0.0 to 2.0.0 (major) should.

**Implementation:**
- Belief confidence changes < 0.05: no cross-repo propagation
- Policy compliance scores within +/-5% of target: no directive
- Persona patch versions: no governance reaction
- Knowledge state updates with < 3 new entries: batch, don't propagate individually

**VSM mapping:** Deadbands reduce the *variety* of signals flowing through System 2, preventing coordination overload. This is a variety attenuator — it filters noise from the S1-to-S2 channel.

### 4. Rate Limiting (Bounded Update Frequency)

**Control theory:** The maximum rate at which a controller can issue corrections is bounded, preventing the controller from reacting faster than the system can respond.

**Governance application:** Demerzel should not issue more than N directives per repo per cycle. Consumer repos should not send more than M compliance reports per period. This prevents rapid-fire directive-response loops.

**Implementation:**
- Maximum directives per repo per PDCA cycle: 3
- Minimum interval between directives to same repo: 1 cycle
- Compliance report batching: aggregate into single report per cycle
- Knowledge package delivery: max 2 per repo per cycle

**VSM mapping:** Rate limiting matches System 2's coordination cadence to System 1's operational cadence. If the governance loop runs faster than operations can respond, directives pile up and oscillation amplifies.

### 5. Exponential Backoff (Adaptive Cooldown)

**Control theory:** After repeated failed corrections, the controller increases wait time exponentially before retrying, preventing resource exhaustion and giving the system time to stabilize.

**Governance application:** If a directive is issued and compliance is not achieved after one cycle, wait 2 cycles before re-issuing. If still non-compliant, wait 4 cycles. This prevents Demerzel from hammering a repo that may need structural changes (not just quick fixes).

**Implementation:**
- First non-compliance: re-issue directive next cycle
- Second non-compliance: wait 2 cycles, escalate severity
- Third non-compliance: wait 4 cycles, escalate to human
- Fourth non-compliance: halt automated directives, require human intervention
- Reset backoff to 0 on successful compliance

**VSM mapping:** Exponential backoff is a variety attenuator on the S3-to-S1 channel. It prevents the control system from overwhelming operations with repeated corrections that aren't working.

## Coordination Transparency Framework

The 2026 Springer paper "Coordination transparency: governing distributed agency in AI systems" provides academic validation for this approach through four components:

### Component 1: Interaction Logging
Record every Galactic Protocol message with sender, receiver, timestamp, and content hash. Demerzel already partially supports this via Article 7 (Auditability), but the logs need to capture *interaction patterns*, not just individual messages.

### Component 2: Live Coordination Monitoring
Track quantitative metrics that detect oscillation:
- **Convergence index:** Are compliance scores trending toward targets or oscillating?
- **Oscillation index:** Frequency of directive-counterdirective pairs within a window
- **Policy-similarity drift:** Are repos diverging in their governance compliance profiles?
- **Cascade interdiction count:** How often do dampening mechanisms prevent unnecessary actions?

### Component 3: Intervention Hooks
Provide stop/pause/reroute capabilities at the coordination layer:
- **Circuit breakers:** If oscillation index exceeds threshold, halt cross-repo directives until human review
- **Rate limiters:** Enforce maximum directive frequency (see mechanism 4)
- **Approval gates:** High-impact directives require human confirmation

### Component 4: Boundary Conditions
Constrain interaction topologies:
- Repos cannot directly trigger directives to each other (all coordination routes through Demerzel)
- Maximum directive chain depth (prevents A→B→C→A loops)
- Sandboxing: experimental governance changes apply to one repo before propagation

## Open-Loop vs. Closed-Loop Comparison

| Aspect | Current (Open-Loop) | With Dampening (Closed-Loop) |
|--------|---------------------|-------------------------------|
| Directives | Fire-and-forget | Target state + error correction |
| State changes | All propagated | Filtered by deadband + hysteresis |
| Update frequency | Unlimited | Rate-limited per cycle |
| Repeated failures | Same directive re-issued | Exponential backoff + escalation |
| Oscillation detection | None | Convergence/oscillation indices |
| Intervention | Manual only | Circuit breakers + approval gates |

## Implications for Demerzel

1. **Enhance Galactic Protocol** — Add `target_state` to directives and `measured_state` to compliance reports, enabling closed-loop correction (negative feedback).
2. **Define dampening parameters** — Specify deadband widths, hysteresis gaps, rate limits, and backoff schedules as configurable governance parameters, not hardcoded values.
3. **Add oscillation monitoring** — Track convergence and oscillation indices across PDCA cycles. Store in `state/coordination/oscillation-metrics.json`.
4. **Implement circuit breakers** — If oscillation index exceeds threshold, halt automated directives and escalate to human. This is the governance equivalent of a fuse.
5. **Preserve algedonic bypass** — Dampening mechanisms must NOT apply to algedonic channel signals (CYB-001 Gap D, now resolved via `policies/algedonic-channel-policy.yaml`). Emergency bypass always overrides coordination dampening.

## Relationship to CYB-001

This course directly addresses **Gap B** from CYB-001: "System 2 contracts are static, not actively dampening." The five mechanisms transform the Galactic Protocol from a passive interface specification (open-loop) into an active anti-oscillation coordinator (closed-loop), fulfilling System 2's core function in Beer's VSM.

The algedonic channel (CYB-001 Gap D) was resolved separately via `policies/algedonic-channel-policy.yaml`. Dampening and algedonic bypass are complementary: dampening slows normal coordination to prevent oscillation; the algedonic channel bypasses all dampening for genuine emergencies.

## Sources

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Coordination transparency: governing distributed agency in AI systems. (2026). *AI & Society*, Springer. https://link.springer.com/article/10.1007/s00146-026-02853-w
- Gorelkin, M. (2025). "Stafford Beer's VSM for Building Enterprise Agentic Systems." Medium. https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Fearne, D. (2025). "Applying Stafford Beer's VSM to Create The Autonomous AI Organisation." Medium. https://medium.com/@fearney/applying-stafford-beers-viable-system-model-to-create-the-autonomous-ai-organisation-aaaed39b37e2
- IBM Research. (2025). "Agentic AI Needs a Systems Theory."
- NI. (2025). "PID Theory Explained." https://www.ni.com/en/shop/labview/pid-theory-explained.html
- GeeksforGeeks. (2025). "Feedback Loops in Distributed Systems." https://www.geeksforgeeks.org/system-design/feedback-loops-in-distributed-systems/

## Cross-References

- Prerequisite: `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Protocol: `contracts/galactic-protocol.md`
- Algedonic policy: `policies/algedonic-channel-policy.yaml`
- Department: `state/streeling/departments/cybernetics.department.json`
- Grammar: `grammars/sci-cybernetics.ebnf`
- Policy: `policies/seldon-plan-policy.yaml`
