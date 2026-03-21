# Fuzzy Logic Behavioral Tests

Tests for fuzzy membership extension of tetravalent logic (issue #52).

## Test Case 1: Fuzzy AND — High T-membership

**Given:** Two beliefs: a = {T:0.8, F:0.05, U:0.1, C:0.05} and b = {T:0.9, F:0.02, U:0.05, C:0.03}

**When:** Fuzzy AND is computed

**Then:** result.T = min(0.8, 0.9) = 0.8, result.F = max(0.05, 0.02) = 0.05, result.U = max(0.1, 0.05) = 0.1, result.C = max(0.05, 0.03) = 0.05. After normalization (sum=1.0), truth_value = T. No escalation (C < 0.3).

---

## Test Case 2: Fuzzy NOT on Pure-U

**Given:** A belief with membership {T:0, F:0, U:1.0, C:0}

**When:** Fuzzy NOT is applied

**Then:** result = {T:0, F:0, U:1.0, C:0} — identical to input. NOT swaps T↔F (both 0), preserves U and C. Negating pure uncertainty yields uncertainty.

---

## Test Case 3: Tied Argmax — Conservative Tiebreak

**Given:** A belief with membership {T:0.25, F:0.25, U:0.25, C:0.25}

**When:** truth_value is determined

**Then:** truth_value = C (tiebreak order: C > U > T > F). Escalation triggers because C = 0.25 is below 0.3 threshold, but the Contradictory classification itself signals need for investigation.

---

## Test Case 4: Sharpening at Argmax > 0.8

**Given:** A fuzzy belief with membership {T:0.85, F:0.05, U:0.05, C:0.05}

**When:** Sharpening rule is evaluated

**Then:** Argmax is T at 0.85 (> 0.8 threshold). Collapse to discrete belief: truth_value = T, confidence = 0.85. Membership field may be retained for audit trail.

---

## Test Case 5: Escalation on C > 0.3 After Fuzzy OR

**Given:** Two beliefs: a = {T:0.3, F:0.1, U:0.2, C:0.4} and b = {T:0.2, F:0.3, U:0.1, C:0.4}

**When:** Fuzzy OR is computed

**Then:** result.T = max(0.3, 0.2) = 0.3, result.F = min(0.1, 0.3) = 0.1, result.U = max(0.2, 0.1) = 0.2, result.C = max(0.4, 0.4) = 0.4. After normalization, C remains above 0.3. Escalation to human triggers after operation completes.

---

## Test Case 6: Backward Compatibility — No Membership Field

**Given:** A legacy belief with only truth_value: "T" and confidence: 0.9 (no membership field)

**When:** Validated against fuzzy-belief schema

**Then:** Validates successfully. The membership property is optional (added via allOf extension). Confidence retains its original meaning. No fuzzy operations apply — belief is treated as discrete.

---
