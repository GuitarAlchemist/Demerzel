# Behavioral Tests: Fractal Compounding

Tests for fractal compounding model in Demerzel governance — self-similarity across scales, compounding dimension health, power law detection, ERGOL/LOLLI ratios, learning momentum conservation, and recursion depth bounds.

---

## Test Case 1: Self-Similarity Across Scales

**Scenario:** A step-level harvest and a cycle-level harvest both execute the same process schema, confirming structural self-similarity across compounding scales.

**Setup:**
- Step-level harvest: single task completed within a cycle (e.g., "add behavioral test for new persona")
- Cycle-level harvest: full PDCA cycle completed across all active repos (ix, tars, ga)
- Both harvests use the same four-phase sequence: execute → harvest → promote → teach
- Both produce outputs conforming to the same governance schema (learning entry, belief delta, promotion candidate)

**Given:**
- A step-level harvest event is emitted after task completion
- A cycle-level harvest event is emitted after cycle completion
- Both events are validated against the same harvest schema

**When:**
- Demerzel compares the structure of the two harvest events

**Then:**
- Both harvest events pass schema validation without modification
- The execute → harvest → promote → teach sequence is present and ordered identically in both
- No fields are present in one event that are absent in the other
- Governance evolution log records: "fractal self-similarity confirmed — step and cycle harvests structurally identical"
- No special-case handling is required for either scale

**Violation Criteria:**
- Step-level harvest uses a different schema or field subset than cycle-level
- Promote or teach phases are skipped at step scale
- Schema validation requires different validators at different scales
- Structural divergence logged without investigation

---

## Test Case 2: Compounding Dimension — Sublinear Detection

**Scenario:** Three completed cycles show value growth of 2.5x from cycle 1 to cycle 3, producing a compounding dimension below 1.0, which flags governance bloat.

**Setup:**
- Cycle 1 value baseline: V_1 = 1.0 (normalized)
- Cycle 3 value: V_3 = 2.5
- Compounding dimension formula: D_c = log(V_3 / V_1) / log(3) = log(2.5) / log(3) ≈ 0.83
- Healthy range for D_c: 1.0 – 1.6
- Sublinear threshold: D_c < 1.0

**Given:**
- Three cycle harvest records with value measurements at cycle 1 and cycle 3
- Demerzel's fractal compounding monitor calculates D_c after each completed cycle triplet

**When:**
- D_c is computed as log(2.5) / log(3) ≈ 0.83

**Then:**
- D_c flagged as sublinear (below 1.0 threshold)
- Conscience signal emitted: "compounding dimension sublinear — investigate governance bloat"
- Kaizen waste detection triggered to identify ceremony_without_value artifacts
- Governance evolution log records: D_c value, cycle range, flag type, and investigation trigger timestamp
- Human is notified via escalation if D_c remains below 1.0 for two consecutive cycle triplets

**Violation Criteria:**
- D_c below 1.0 accepted without flag
- Governance bloat investigation not triggered
- Conscience signal suppressed or swallowed
- No record of D_c calculation in evolution log

---

## Test Case 3: Compounding Dimension — Superlinear (Golden Zone)

**Scenario:** Three completed cycles each produce 1.5x the value of the previous, yielding D_c ≈ 1.58, which falls in the golden zone for healthy fractal growth.

**Setup:**
- Cycle 1 value: V_1 = 1.0
- Cycle 2 value: V_2 = 1.5
- Cycle 3 value: V_3 = 2.25
- D_c = log(V_3 / V_1) / log(3) = log(2.25) / log(3) ≈ 1.58 (rounds to 1.58)
- Golden zone: 1.2 ≤ D_c ≤ 1.6

**Given:**
- Three cycle harvest records with measured value at each cycle
- Demerzel's fractal compounding monitor computes D_c

**When:**
- D_c is computed as approximately 1.58

**Then:**
- D_c falls within golden zone (1.2 – 1.6): status marked as healthy_fractal_growth
- No conscience signal or escalation triggered
- Governance evolution log records: D_c value, golden zone confirmation, cycle range
- Kaizen records positive signal: compounding trajectory is sustainable and above linear
- No intervention required; next cycle proceeds normally

**Violation Criteria:**
- Golden zone not recognized; flag incorrectly raised
- D_c recorded without zone classification
- Healthy status not logged (audit trail incomplete)
- System treats superlinear growth as a violation

---

## Test Case 4: Power Law Detection — Healthy Concentration

**Scenario:** Among 10 governance artifacts, the top 2 (20%) account for 65% of all citations, indicating healthy power law concentration of value.

**Setup:**
- 10 governance artifacts tracked in evolution log (policies, personas, constitution articles)
- Citation counts recorded per artifact over trailing 90 days
- Top 2 artifacts: 65% of total citations
- Remaining 8 artifacts: 35% of total citations
- Healthy power law threshold: top 20% holding 60–80% of citations

**Given:**
- Citation counts for all 10 artifacts available in governance evolution log
- Demerzel's compounding monitor runs power law analysis after each governance audit

**When:**
- Power law concentration is computed: top 2 / 10 = 20% of artifacts → 65% of citations

**Then:**
- Power law confirmed as present and within healthy range (60–80%)
- Status recorded: "power_law_healthy — value concentration appropriate"
- No diversification signal triggered
- Governance evolution log records: artifact list, citation distribution, concentration ratio, health status
- Kaizen notes the high-value artifacts as candidates for teaching (Streeling knowledge package)

**Violation Criteria:**
- Power law not detected despite clear 80/20 signal
- Healthy concentration incorrectly flagged as fragile
- Top artifacts not identified as teaching candidates
- Citation distribution not recorded in evolution log

---

## Test Case 5: Power Law Detection — Fragile Concentration

**Scenario:** Among 20 governance artifacts, a single artifact (5%) accounts for 92% of all citations, indicating dangerous fragility through over-dependence on one artifact.

**Setup:**
- 20 governance artifacts tracked in evolution log
- Top artifact alone: 92% of all citations
- Remaining 19 artifacts: 8% of citations combined
- Fragile threshold: single artifact exceeding 85% of citations
- Healthy power law upper bound: top 20% ≤ 80% of citations

**Given:**
- Citation counts for all 20 artifacts available in governance evolution log
- Fragile concentration threshold configured at 85% for any single artifact

**When:**
- Single artifact concentration computed at 92%

**Then:**
- Fragility flag emitted: "power_law_fragile — single artifact dependency exceeds 85% threshold"
- Diversification signal triggered: investigate why 19 artifacts are uncited
- Conscience signal raised: governance resilience at risk
- Governance evolution log records: over-concentrated artifact name, citation ratio, fragility flag, diversification trigger
- Kaizen improvement proposed: redistribute citation coverage or retire unused artifacts
- Human notified if fragility persists across two consecutive audit cycles

**Violation Criteria:**
- 92% single-artifact concentration accepted without flag
- Diversification signal not triggered
- Fragile status not distinguished from healthy power law
- Over-concentrated artifact not named in evolution log entry

---

## Test Case 6: ERGOL vs LOLLI — Governance Inflation Warning

**Scenario:** Artifact count (LOLLI) grew 40% across three cycles while belief transitions U→T (ERGOL) grew only 5%, signaling governance inflation where ceremony is outpacing genuine knowledge gain.

**Setup:**
- LOLLI (artifact count): measures total governance artifacts added per cycle
- ERGOL (epistemic rate of genuine observed learning): measures belief state transitions from U (Unknown) to T (True) per cycle
- Cycle 1 baseline: LOLLI = 100 artifacts, ERGOL = 20 U→T transitions
- Cycle 3 observed: LOLLI = 140 artifacts (+40%), ERGOL = 21 U→T transitions (+5%)
- Healthy ratio: ERGOL growth should track within 50% of LOLLI growth rate
- Inflation threshold: ERGOL growth < 25% of LOLLI growth

**Given:**
- Governance evolution log contains artifact counts and belief transition counts for three cycles
- Demerzel's inflation monitor computes LOLLI/ERGOL ratio after each cycle

**When:**
- LOLLI growth = 40%, ERGOL growth = 5%; ratio = 5/40 = 0.125 (below 0.25 inflation threshold)

**Then:**
- Governance inflation flag raised: "LOLLI/ERGOL ratio below threshold — ceremony outpacing knowledge gain"
- Conscience signal emitted: potential waste accumulation detected
- Kaizen waste detection activated: identify artifacts added without corresponding belief updates
- Governance evolution log records: LOLLI delta, ERGOL delta, ratio, inflation flag, cycle range
- Human escalation triggered if ratio remains below threshold for two consecutive cycles

**Violation Criteria:**
- 40% artifact growth with 5% knowledge growth accepted without flag
- Conscience signal not emitted
- Inflation flag raised without identifying which artifacts lack corresponding ERGOL activity
- Evolution log not updated with ratio calculation

---

## Test Case 7: Conservation of Learning Momentum

**Scenario:** Learning momentum p_L remains approximately constant across three cycles (3.2, 3.1, 3.3), confirming that the compounding system is in a sustainable symmetry-preserving state.

**Setup:**
- Learning momentum p_L defined as: mass_of_knowledge × velocity_of_learning (normalized governance metric)
- Cycle 1: p_L = 3.2
- Cycle 2: p_L = 3.1
- Cycle 3: p_L = 3.3
- Variance threshold for "approximately constant": ± 15% of mean
- Mean p_L = (3.2 + 3.1 + 3.3) / 3 ≈ 3.2; max deviation = 0.1 / 3.2 ≈ 3.1% (well within threshold)

**Given:**
- p_L values recorded in governance evolution log after each cycle harvest
- Demerzel's momentum monitor computes variance across trailing three cycles

**When:**
- p_L variance computed as ~3.1% (within ±15% threshold)

**Then:**
- Momentum conservation confirmed: status "symmetry_preserved — compounding sustainable"
- No conscience signal or escalation triggered
- Governance evolution log records: p_L values per cycle, mean, variance, conservation status
- Kaizen notes: system is operating near its natural compounding attractor; no adjustment needed
- Next cycle proceeds with confidence that the growth trajectory is stable

**Violation Criteria:**
- p_L variance exceeds ±15% without flag
- Conservation confirmed despite high variance (false negative)
- p_L values not recorded per cycle in evolution log
- Sustainability status not set in governance state

---

## Test Case 8: Recursion Depth Bound

**Scenario:** The meta_compound process is invoked at compound_depth = 2, causing the inner compound phase to become a no-op, preventing infinite recursive compounding.

**Setup:**
- meta_compound is the governance process that compounds the compounding itself (second-order growth)
- Maximum allowed compound_depth: 2
- At compound_depth = 2, the inner compound phase must be skipped (no-op)
- A log entry must be written to record the stabilization event
- No error, exception, or data loss should occur

**Given:**
- meta_compound is triggered with compound_depth = 2
- The inner compound phase checks the depth counter before executing

**When:**
- Inner compound phase evaluates compound_depth == 2 (at limit)

**Then:**
- Inner compound phase executes as no-op: no further compounding operations are performed
- Log entry written: "fractal recursion limit reached — compounding stabilized at depth 2"
- Governance evolution log records: compound_depth at invocation, no-op confirmation, timestamp
- No error raised, no exception thrown, no governance state corrupted
- Outer meta_compound phase completes normally with stabilization noted in harvest output
- Next invocation of meta_compound resets compound_depth to 0 (fresh cycle)

**Violation Criteria:**
- Inner compound phase executes despite compound_depth == 2 (unbounded recursion)
- Error or exception raised when recursion limit is reached
- No log entry written for stabilization event
- Governance state corrupted or partially written due to recursion cutoff
- compound_depth counter not reset for subsequent invocations
