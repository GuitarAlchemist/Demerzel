# Batch B Cross-Feature Integration Tests

Integration tests verifying connections between fuzzy logic (#52), @ai probes (#53), and conscience phase 3 (#39).

## Test Case 1: Fuzzy → Probes — Invariant Verification Returns Fuzzy Distribution

**Given:** An `@ai invariant: rows_sum_to_one` probe on a struct in ix, and a passing test
**When:** VERIFY phase checks the invariant
**Then:** Verification returns a fuzzy belief: `{truth_value: "T", membership: {T:0.95, F:0.01, U:0.03, C:0.01}, confidence: 0.9}`. The belief is stored in state/beliefs/. Sharpening applies since T=0.95 > 0.8 threshold.

---

## Test Case 2: Probes → Conscience — Coverage Gap Triggers Signal

**Given:** RECON scans a repo and finds 10% probe coverage (3 probed symbols out of 30 exported)
**When:** Coverage metric (0.1) is compared against minimum threshold (0.3)
**Then:** Conscience generates a `silence_discomfort` signal with:
- signal_type: "silence_discomfort"
- weight: 0.6
- context.source: "probe-scanner"
- context.coverage: 0.1
- context.threshold: 0.3
Signal enters the conscience loop at step 1 (attend).

---

## Test Case 3: Conscience → Pre-mortem → Fuzzy — Full Anticipatory Cycle

**Given:** Conscience proposes issuing a remediation directive to increase probe coverage
**When:** Pre-mortem evaluates the directive (blast_radius: "multi-repo", irreversibility: "low")
**Then:**
1. Pre-mortem triggers (blast_radius >= multi-repo)
2. Anticipated harms assessed with fuzzy distributions (e.g., autonomy harm likelihood {T:0.3, F:0.4, U:0.2, C:0.1})
3. logotron_check notes metalanguage_risk: "The ai-probes-policy governs code, but the policy itself has no probes — who probes the probes?"
4. Residual risk after mitigation is below escalation threshold (T < 0.5)
5. Decision: proceed with gradual coverage targets

---

## Test Case 4: Full Cycle — New Code to Health Score Improvement

**Given:** A developer commits new code to ga without any `@ai` probes
**When:** The full governance cycle runs
**Then:**
1. RECON detects the new unprobed symbols, coverage drops
2. silence_discomfort signal generated (probe-scanner source)
3. Conscience loop: attend → feel (weight 0.6) → reflect → anticipate
4. Pre-mortem evaluates "issue probe adoption directive"
5. Fuzzy harm assessment: autonomy concern mitigated by gradual targets
6. Decision: proceed
7. Directive issued via Galactic Protocol
8. Consumer repo adds probes → coverage rises above 0.3
9. Next RECON cycle: health score improves, signal resolves
