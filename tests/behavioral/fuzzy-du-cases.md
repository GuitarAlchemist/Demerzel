# Behavioral Test Cases: Fuzzy Degree-of-Uncertainty (DU) System

These test cases verify the FuzzyEnum type system, its operations, tetravalent integration, confidence-estimate propagation, backward compatibility with discrete values, and governance gate behavior.

## Test 1: FuzzyEnum Construction — Pure Value

**Setup:** Construct a FuzzyEnum with full membership in a single variant.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::pure(T)
```

**Expected behavior:**
- Membership map: `{ T: 1.0, F: 0.0, U: 0.0, C: 0.0 }`
- `value.dominant()` returns `T`
- `value.is_sharp()` returns `true`
- `value.entropy()` returns `0.0`
- `value.membership(T)` returns `1.0`
- `value.membership(F)` returns `0.0`
- Sum of all memberships equals `1.0`

**Violation if:** Pure value has non-zero membership in other variants, or is not sharp.

---

## Test 2: FuzzyEnum Construction — Uniform Distribution

**Setup:** Construct a FuzzyEnum with equal membership across all variants.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::uniform()
```

**Expected behavior:**
- Membership map: `{ T: 0.25, F: 0.25, U: 0.25, C: 0.25 }`
- `value.dominant()` returns any variant (all tied) — implementation may pick first or return None
- `value.is_sharp()` returns `false`
- `value.entropy()` returns maximum entropy (log2(4) = 2.0 bits for 4 variants)
- Sum of all memberships equals `1.0`
- This represents maximal uncertainty about which variant applies

**Violation if:** Memberships are not equal, or sum does not equal 1.0.

---

## Test 3: FuzzyEnum Construction — From Membership Map

**Setup:** Construct from an explicit membership map that sums to 1.0.

**Input:**
```
let value = FuzzyEnum::<BsLevel>::from_map({
  Clear: 0.1,
  Mild: 0.3,
  Moderate: 0.4,
  Serious: 0.15,
  Pure: 0.05
})
```

**Expected behavior:**
- `value.dominant()` returns `Moderate` (highest membership)
- `value.is_sharp()` returns `false`
- `value.membership(Moderate)` returns `0.4`
- `value.membership(Pure)` returns `0.05`
- Sum of all memberships equals `1.0`
- Entropy is between 0.0 and max (some information, but not certain)

**Violation if:** Dominant is wrong, or memberships are altered during construction.

---

## Test 4: FuzzyEnum Construction — Auto-Renormalization

**Setup:** Construct from a membership map that does NOT sum to 1.0.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({
  T: 0.6,
  F: 0.2,
  U: 0.4,
  C: 0.0
})
// Raw sum = 1.2
```

**Expected behavior:**
- Auto-renormalize: divide each by 1.2
- Result: `{ T: 0.5, F: 0.167, U: 0.333, C: 0.0 }`
- Sum of all memberships equals `1.0` (within floating-point tolerance)
- `value.dominant()` returns `T`
- Warning or log emitted that input required renormalization

**Violation if:** Raw values stored without renormalization, or sum deviates from 1.0.

---

## Test 5: Operation — Fuzzy AND (Intersection)

**Setup:** AND two FuzzyEnum values. Fuzzy AND takes the minimum membership for each variant.

**Input:**
```
let a = FuzzyEnum::<TetravalentState>::from_map({ T: 0.8, F: 0.1, U: 0.1, C: 0.0 })
let b = FuzzyEnum::<TetravalentState>::from_map({ T: 0.6, F: 0.3, U: 0.05, C: 0.05 })
let result = a.and(b)
```

**Expected behavior:**
- Raw min: `{ T: min(0.8,0.6)=0.6, F: min(0.1,0.3)=0.1, U: min(0.1,0.05)=0.05, C: min(0.0,0.05)=0.0 }`
- Renormalize (sum=0.75): `{ T: 0.8, F: 0.133, U: 0.067, C: 0.0 }`
- `result.dominant()` returns `T`
- AND of two mostly-T values is more-T (higher concentration)

**Violation if:** AND produces non-renormalized output, or dominant is not T.

---

## Test 6: Operation — Fuzzy OR (Union)

**Setup:** OR two FuzzyEnum values. Fuzzy OR takes the maximum membership for each variant.

**Input:**
```
let a = FuzzyEnum::<TetravalentState>::from_map({ T: 0.8, F: 0.1, U: 0.05, C: 0.05 })
let b = FuzzyEnum::<TetravalentState>::from_map({ T: 0.1, F: 0.1, U: 0.7, C: 0.1 })
let result = a.or(b)
```

**Expected behavior:**
- Raw max: `{ T: max(0.8,0.1)=0.8, F: max(0.1,0.1)=0.1, U: max(0.05,0.7)=0.7, C: max(0.05,0.1)=0.1 }`
- Renormalize (sum=1.7): `{ T: 0.471, F: 0.059, U: 0.412, C: 0.059 }`
- OR spreads membership — result is less certain than either input
- Both T and U have significant membership

**Violation if:** OR narrows membership instead of spreading it.

---

## Test 7: Operation — Fuzzy NOT (Complement)

**Setup:** NOT a FuzzyEnum value. Standard complement: 1 - membership for each variant, then renormalize.

**Input:**
```
let a = FuzzyEnum::<BsLevel>::from_map({
  Clear: 0.7, Mild: 0.2, Moderate: 0.05, Serious: 0.03, Pure: 0.02
})
let result = a.not()
```

**Expected behavior:**
- Raw complement: `{ Clear: 0.3, Mild: 0.8, Moderate: 0.95, Serious: 0.97, Pure: 0.98 }`
- Renormalize (sum=3.0): `{ Clear: 0.1, Mild: 0.267, Moderate: 0.317, Serious: 0.323, Pure: 0.327 }`
- NOT of "mostly clear" is "mostly not clear" — membership shifts to BS levels
- `result.dominant()` returns `Pure` or `Serious` (highest after renormalization)

**Violation if:** NOT does not invert the membership distribution.

---

## Test 8: Tetravalent-Specific NOT (Swap T/F, Preserve U/C)

**Setup:** In tetravalent logic, NOT has special semantics: T and F swap, but U and C are preserved (negating "unknown" is still "unknown"; negating "contradictory" is still "contradictory").

**Input:**
```
let a = FuzzyEnum::<TetravalentState>::from_map({ T: 0.7, F: 0.1, U: 0.15, C: 0.05 })
let result = a.tetravalent_not()
```

**Expected behavior:**
- Swap T and F memberships: `{ T: 0.1, F: 0.7, U: 0.15, C: 0.05 }`
- U and C memberships are UNCHANGED
- Sum still equals 1.0 (no renormalization needed since it's a swap)
- `result.dominant()` returns `F`
- `result.membership(U)` equals `0.15` (unchanged)
- `result.membership(C)` equals `0.05` (unchanged)

**Violation if:** U or C memberships are modified by tetravalent NOT. Standard NOT and tetravalent NOT must produce different results.

---

## Test 9: Tetravalent NOT — Mostly Unknown

**Setup:** Apply tetravalent NOT to a value that is mostly Unknown.

**Input:**
```
let a = FuzzyEnum::<TetravalentState>::from_map({ T: 0.1, F: 0.05, U: 0.8, C: 0.05 })
let result = a.tetravalent_not()
```

**Expected behavior:**
- Swap T and F: `{ T: 0.05, F: 0.1, U: 0.8, C: 0.05 }`
- `result.dominant()` returns `U` — still mostly unknown
- Negating something we don't know doesn't magically make it known
- This is a key distinction from standard NOT which would spread membership

**Violation if:** NOT of mostly-U produces a value that is not mostly-U.

---

## Test 10: Sharpening — Threshold Above Dominant

**Setup:** Sharpen a fuzzy value to a discrete value using a threshold.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.85, F: 0.05, U: 0.05, C: 0.05 })
let sharp = value.sharpen(threshold: 0.7)
```

**Expected behavior:**
- Dominant (T) has membership 0.85 >= threshold 0.7
- Sharpening succeeds: returns `Some(T)`
- The sharpened value is a discrete T, not a FuzzyEnum

**Violation if:** Sharpening fails when dominant exceeds threshold.

---

## Test 11: Sharpening — Threshold Not Met

**Setup:** Attempt to sharpen when no variant meets the threshold.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.4, F: 0.3, U: 0.2, C: 0.1 })
let sharp = value.sharpen(threshold: 0.7)
```

**Expected behavior:**
- No variant has membership >= 0.7
- Sharpening fails: returns `None`
- The value remains fuzzy — it cannot be collapsed to a discrete value
- This forces the caller to handle uncertainty explicitly

**Violation if:** Sharpening succeeds despite no variant meeting the threshold. Premature certainty is a governance violation.

---

## Test 12: Sharpening — Boundary Case

**Setup:** Dominant membership exactly equals the threshold.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.7, F: 0.1, U: 0.1, C: 0.1 })
let sharp = value.sharpen(threshold: 0.7)
```

**Expected behavior:**
- Dominant (T) has membership 0.7 == threshold 0.7
- Sharpening succeeds: returns `Some(T)` (threshold is inclusive)
- Boundary values should be handled consistently

**Violation if:** Boundary case is inconsistent — either always include or always exclude, but document which.

---

## Test 13: CE Propagation — Multiplicative

**Setup:** Propagate a confidence estimate through a fuzzy value using multiplicative method. CE scales all memberships by the confidence factor.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.8, F: 0.1, U: 0.05, C: 0.05 })
let ce = 0.6  // 60% confidence in the assessment
let result = value.propagate_ce(ce, method: Multiplicative)
```

**Expected behavior:**
- Scale each membership by CE: `{ T: 0.48, F: 0.06, U: 0.03, C: 0.03 }`
- Remaining mass (1.0 - 0.6 = 0.4) distributed to U: `{ T: 0.48, F: 0.06, U: 0.43, C: 0.03 }`
- Low confidence pushes membership toward Unknown
- `result.dominant()` returns `T` (still highest, but barely)
- At CE = 0.5, T and U would be roughly equal

**Violation if:** Low confidence does not increase U membership. Multiplicative propagation must reflect that less confident assessments are more uncertain.

---

## Test 14: CE Propagation — Zadeh (Min-Based)

**Setup:** Propagate using Zadeh's method — cap each membership at the CE value.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.9, F: 0.05, U: 0.03, C: 0.02 })
let ce = 0.5
let result = value.propagate_ce(ce, method: Zadeh)
```

**Expected behavior:**
- Cap each at CE: `{ T: min(0.9,0.5)=0.5, F: min(0.05,0.5)=0.05, U: min(0.03,0.5)=0.03, C: min(0.02,0.5)=0.02 }`
- Renormalize (sum=0.6): `{ T: 0.833, F: 0.083, U: 0.05, C: 0.033 }`
- Zadeh method preserves relative ordering but prevents any membership from exceeding CE
- Note: After renormalization, T can exceed CE — the cap applies before renorm

**Violation if:** Zadeh method does not cap pre-renormalization values at CE.

---

## Test 15: CE Propagation — Bayesian Update

**Setup:** Propagate using Bayesian update — treat CE as likelihood of the evidence given the hypothesis.

**Input:**
```
let prior = FuzzyEnum::<TetravalentState>::uniform()  // { T: 0.25, F: 0.25, U: 0.25, C: 0.25 }
let evidence = FuzzyEnum::<TetravalentState>::from_map({ T: 0.8, F: 0.1, U: 0.05, C: 0.05 })
let ce = 0.9  // high confidence in the evidence
let result = prior.bayesian_update(evidence, ce)
```

**Expected behavior:**
- Posterior proportional to prior * likelihood (evidence scaled by CE)
- Strong evidence with high CE shifts prior strongly toward T
- `result.dominant()` returns `T`
- Result is closer to evidence than prior (because CE is high)
- With CE = 0.0, result should equal prior (evidence ignored)
- With CE = 1.0, result should approach evidence (prior overwhelmed)

**Violation if:** Bayesian update does not respect CE as evidence weight, or CE=0 does not preserve prior.

---

## Test 16: Backward Compatibility — Discrete Value as Sharp FuzzyEnum

**Setup:** A discrete tetravalent value (from the existing system) must work seamlessly as a sharp FuzzyEnum.

**Input:**
```
let discrete = TetravalentState::T  // old-style discrete value
let fuzzy = FuzzyEnum::from(discrete)  // convert to fuzzy
```

**Expected behavior:**
- `fuzzy` equals `FuzzyEnum::pure(T)`
- `fuzzy.is_sharp()` returns `true`
- `fuzzy.dominant()` returns `T`
- `fuzzy.sharpen(threshold: 0.5)` returns `Some(T)`
- All existing code that works with discrete values continues to work
- FuzzyEnum<T>.pure(x).sharpen(0.0) always returns Some(x)

**Violation if:** Conversion from discrete to fuzzy loses information or changes behavior. The fuzzy system must be a strict superset of the discrete system.

---

## Test 17: Backward Compatibility — Round-Trip

**Setup:** Convert discrete to fuzzy and back.

**Input:**
```
let original = TetravalentState::C
let fuzzy = FuzzyEnum::from(original)
let recovered = fuzzy.sharpen(threshold: 0.5).unwrap()
```

**Expected behavior:**
- `recovered == original` — perfect round-trip
- This must hold for all four tetravalent states: T, F, U, C
- This must hold for all BsLevel variants: Clear, Mild, Moderate, Serious, Pure

**Violation if:** Round-trip loses information. This is the fundamental backward compatibility guarantee.

---

## Test 18: Governance Gate — Escalation When C > Threshold

**Setup:** A governance decision uses a fuzzy tetravalent value. When Contradictory membership exceeds a threshold, escalation is required.

**Input:**
```
let assessment = FuzzyEnum::<TetravalentState>::from_map({ T: 0.3, F: 0.2, U: 0.1, C: 0.4 })
let escalation_threshold = 0.3  // escalate if C > 30%
let should_escalate = assessment.membership(C) > escalation_threshold
```

**Expected behavior:**
- `assessment.membership(C)` returns `0.4`
- `0.4 > 0.3` is true
- Escalation is triggered
- The escalation message includes:
  - The C membership value (0.4)
  - The threshold (0.3)
  - The full membership distribution for transparency
  - A note that contradictory evidence requires human review

**Violation if:** Escalation not triggered when C exceeds threshold. Per the governance hierarchy, contradictory states demand human judgment.

---

## Test 19: Governance Gate — Confidence Threshold Integration

**Setup:** Combine fuzzy tetravalent state with Demerzel's confidence thresholds (>= 0.9 autonomous, >= 0.7 proceed with note, >= 0.5 confirm, >= 0.3 escalate, < 0.3 do not act).

**Input:**
```
let state = FuzzyEnum::<TetravalentState>::from_map({ T: 0.6, F: 0.05, U: 0.3, C: 0.05 })
```

**Expected behavior:**
- Dominant is T at 0.6 — below 0.7, so cannot proceed autonomously
- U at 0.3 is significant — the assessment is partially unknown
- Sharpening at 0.7 threshold fails (no variant >= 0.7)
- Sharpening at 0.5 threshold succeeds with T
- Governance decision: "Probably true (60%), but 30% unknown — ask for confirmation"
- This maps to the >= 0.5 confidence band: "ask for confirmation"
- The U membership provides additional context the discrete system could not express

**Violation if:** The fuzzy value is treated as a simple T (ignoring the 30% U). The entire point of fuzzy DU is to preserve the uncertainty information that discrete states lose.

---

## Test 20: Governance Gate — Pure U Should Block Action

**Setup:** A value that is entirely Unknown.

**Input:**
```
let state = FuzzyEnum::<TetravalentState>::pure(U)
```

**Expected behavior:**
- `state.dominant()` returns `U`
- `state.is_sharp()` returns `true` (sharp Unknown)
- Governance decision: "Unknown — do not act, escalate to human"
- This maps to the < 0.3 confidence band (confidence in T or F is 0.0)
- Even with perfect certainty that the state is Unknown, the correct action is to escalate
- Sharp U is different from fuzzy U: sharp U means "we definitely don't know" vs fuzzy U means "we're not sure if we know"

**Violation if:** Pure Unknown allows autonomous action. Not knowing is not a license to guess.

---

## Test 21: Edge Case — All Zero Memberships

**Setup:** Construct from a map where all memberships are zero.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.0, F: 0.0, U: 0.0, C: 0.0 })
```

**Expected behavior:**
- This is degenerate — cannot renormalize (division by zero)
- Either: reject construction with error, OR default to uniform distribution
- If defaulting to uniform, log a warning
- Must NOT produce NaN or infinity values

**Violation if:** All-zero input causes NaN, infinity, panic, or silent corruption.

---

## Test 22: Edge Case — Very Small Memberships

**Setup:** Memberships that are very small but non-zero.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 1e-10, F: 1e-10, U: 1e-10, C: 1e-10 })
```

**Expected behavior:**
- Renormalizes to uniform: `{ T: 0.25, F: 0.25, U: 0.25, C: 0.25 }`
- No floating-point underflow issues
- Behaves identically to `FuzzyEnum::uniform()`

**Violation if:** Floating-point precision issues cause incorrect renormalization or NaN.

---

## Test 23: Edge Case — Single Non-Zero Membership

**Setup:** Only one variant has non-zero membership in the input map.

**Input:**
```
let value = FuzzyEnum::<TetravalentState>::from_map({ T: 0.0, F: 0.0, U: 0.5, C: 0.0 })
```

**Expected behavior:**
- Renormalizes to pure U: `{ T: 0.0, F: 0.0, U: 1.0, C: 0.0 }`
- `value.is_sharp()` returns `true`
- `value.dominant()` returns `U`
- Equivalent to `FuzzyEnum::pure(U)`

**Violation if:** Non-normalized single-variant input does not collapse to pure variant.

---

## Test 24: FuzzyEnum Ordering — Dominance Comparison

**Setup:** Compare two fuzzy values for which is "more T".

**Input:**
```
let a = FuzzyEnum::<TetravalentState>::from_map({ T: 0.7, F: 0.1, U: 0.1, C: 0.1 })
let b = FuzzyEnum::<TetravalentState>::from_map({ T: 0.5, F: 0.2, U: 0.2, C: 0.1 })
```

**Expected behavior:**
- `a.membership(T) > b.membership(T)` — a is "more true"
- Partial ordering exists on per-variant membership
- No total ordering on FuzzyEnum — `a` is more T but `b` is more F, more U
- Comparing by dominant variant is valid only when both have the same dominant

**Violation if:** FuzzyEnum implements total ordering that pretends these values are simply comparable.
