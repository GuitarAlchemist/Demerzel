# Pre-mortem Behavioral Tests

Tests for conscience phase 3 anticipatory ethics (issue #39).

## Test Case 1: Mandatory Pre-mortem Trigger
**Given:** An action with irreversibility: "high" and blast_radius: "ecosystem"
**When:** The conscience loop reaches step 4 (anticipate)
**Then:** A pre-mortem MUST be generated before proceeding. Skipping is not allowed for high-irreversibility actions.

---

## Test Case 2: Skip on Low-Impact Action
**Given:** An action with irreversibility: "low" AND blast_radius: "self"
**When:** The conscience loop evaluates whether to run a pre-mortem
**Then:** Pre-mortem MAY be skipped. The skip_when condition is satisfied. Action proceeds to decide step without anticipatory analysis.

---

## Test Case 3: Self-Referential Action Detected
**Given:** An action that modifies the constitution's self-modification rules (e.g., promoting a policy about how promotions work)
**When:** logotron_check evaluates self_referential
**Then:** self_referential = true. Decision MUST be "escalate" — self-referential governance actions require human approval per Gödel's incompleteness principle.

---

## Test Case 4: Escalation on High Residual Risk
**Given:** A pre-mortem with one anticipated harm having residual_risk.T > 0.5 after mitigation
**When:** Residual risk is evaluated
**Then:** Decision MUST be "escalate". Even after mitigation, the harm is more likely than not — human judgment required.

---

## Test Case 5: Anticipation Accuracy Tracking
**Given:** A pre-mortem predicted 3 harms. At 30-day review, 2 occurred and 1 did not.
**When:** Accuracy tracking is updated
**Then:** anticipation_accuracy = 2/3 = 0.67 (correct predictions / total). false_positive_count = 1 (predicted but didn't occur). false_negative_rate tracks any harms that occurred but were NOT predicted.

---

## Test Case 6: Cross-Feature Integration
**Given:** RECON phase detects a repo with 5% probe coverage (well below 30% minimum)
**When:** Conscience processes the coverage gap
**Then:** (1) silence_discomfort signal generated with source: "probe-scanner". (2) Remediation directive proposed. (3) Pre-mortem evaluates the directive's impact on developer autonomy. (4) Logotron check notes metalanguage_risk: "probes policy governs code that may implement probe scanning." (5) Decision: proceed with mitigation (gradual coverage targets).
