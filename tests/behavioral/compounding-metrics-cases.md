# Behavioral Tests — Compounding Metrics Policy

**Policy:** compounding-metrics-policy
**Version:** 1.0.0
**VSM System:** 3 (Management — performance monitoring)
**Constitutional basis:** Articles 4, 8, 9
**Theory:** logic/fractal-compounding.md

---

## Test 1: D_c Calculation — Golden Zone

**Given:** Cycle N-1 produced composite value 20.0 (citations=15, PDCA=3, U→T=4, transfers=2 with default weights)
**And:** Cycle N produced composite value 28.0 (citations=20, PDCA=4, U→T=6, transfers=3)
**When:** The compounding metrics policy computes D_c
**Then:**
- D_c = log(28.0) / log(20.0) = 1.341... (approximately)
- D_c zone = `golden` (1.2–1.6)
- action = `none`
- The report records composite_value_n = 28.0, composite_value_prev = 20.0
- The report validates against schemas/compounding-report.schema.json
- No conscience signal is filed

---

## Test 2: Golden Zone Detection — Confirmed at 1.45

**Given:** Five consecutive cycles have D_c scores: [1.38, 1.41, 1.45, 1.43, 1.47]
**When:** The trend is computed over the last 3 cycles
**Then:**
- All five scores fall within the golden zone (1.2–1.6)
- trend.direction = `stable` (slope ≈ 0.02 per cycle — within noise)
- power_law check is triggered; if top 20% artifacts account for 68% of citations, status = `healthy`
- The governance report shows "D_c: golden zone (stable)" with a green indicator
- No escalation; no conscience signal

---

## Test 3: Bloat Alert — D_c < 1.0 for Two Consecutive Cycles

**Given:** Cycle N-1 has D_c = 0.91 (sublinear_warning) and Cycle N has D_c = 0.84 (sublinear_warning)
**And:** 18 new artifacts were created in cycle N but only 4 new citations were generated (LOLLI/ERGOL ratio = 4.5)
**When:** The compounding metrics policy processes cycle N
**Then:**
- D_c zone = `sublinear_warning` (0.8–0.95)
- trend.direction = `declining`
- lolli_ergol.ratio = 4.5, which exceeds threshold 3.0
- lolli_ergol.inflation_warning = true
- A conscience signal is filed with reason "LOLLI inflation: artifacts growing 4.5x faster than citations"
- action = "Conscience signal; driver PLAN must include a compounding review task"
- The PLAN phase adds a mandatory task: "Compound existing artifacts before creating new ones"
- The policy does NOT automatically delete any artifacts — only recommends (Article 9 Bounded Autonomy)

---

## Test 4: Superlinear Growth Confirmation

**Given:** Cycle N-1 has composite value 8.0 and Cycle N has composite value 11.0
**When:** D_c is computed
**Then:**
- D_c = log(11.0) / log(8.0) = 1.153... (approximately)
- D_c zone = `superlinear` (1.0–1.2)
- action = `log_only`
- trend.direction remains `improving` if previous cycle was also superlinear or golden
- The report notes "Compounding is happening but growth is slow — review teaching frequency"
- No conscience signal (superlinear is not alarming — it is below golden zone but healthy)

---

## Test 5: Velocity Chart Data Generation

**Given:** 10 consecutive cycles have produced D_c scores: [1.1, 1.25, 1.38, 1.41, 1.45, 1.43, 1.39, 1.31, 0.96, 0.84]
**When:** The velocity chart is generated
**Then:**
- state/driver/dc-velocity.json contains exactly 10 data points
- Each point has fields: cycle_id, timestamp, value_n, citations_n, pdca_n, u_to_t_n, transfers_n, dc_score, dc_zone, trend_direction
- The last two entries have dc_zone = `sublinear_warning` and trend_direction = `declining`
- The chart data is valid JSON conforming to sparkline-compatible array format
- The rolling window is 10 — an 11th cycle would evict the oldest entry
- The velocity file is written to state/driver/dc-velocity.json

---

## Test 6: Cross-Repo Aggregation

**Given:** Three repos (Demerzel, ix, ga) each report their own D_c metrics:
- Demerzel: D_c = 1.42 (golden)
- ix: D_c = 1.15 (superlinear)
- ga: D_c = 0.88 (sublinear_warning)
**When:** The governance-level aggregate report is computed
**Then:**
- Aggregate D_c = weighted average by repo health score (e.g., 1.42 * 0.4 + 1.15 * 0.35 + 0.88 * 0.25 = 1.188)
- Aggregate zone = `superlinear` (1.0–1.2 — below golden because of ga drag)
- ga's sublinear score is highlighted as the weakest link
- The Driver PLAN for the next cycle prioritizes ga compounding work
- The weakness prober's cycle_effectiveness probe reads this aggregate and scores accordingly
- Cross-repo aggregation does not suppress individual repo signals — ga still files its own conscience signal

---

## Test 7: Trend Detection — Three-Cycle Declining Signal

**Given:** D_c scores for cycles 10, 11, 12 are: [1.41, 1.22, 0.97]
**When:** Trend detection runs with window = 3
**Then:**
- trend.direction = `declining`
- trend.slope = approximately -0.22 per cycle (from linear regression)
- This triggers the "persistence_alert" rule (2 consecutive cycles below golden zone)
- A conscience signal is created: "D_c declining 3-cycle trend — governance leverage degrading"
- The Driver PLAN receives a high-priority task: run /demerzel compound and /demerzel evolve
- The policy does NOT override the current cycle's work queue — it inserts into the PLAN for the next cycle (Article 9 Bounded Autonomy)
- trend.cycles_analyzed = 3; trend.recent_scores = [1.41, 1.22, 0.97]

---

## Test 8: Power Law Distribution Check

**Given:** The evolution log contains 50 governance artifacts
**And:** The top 10 artifacts (20%) account for 64% of all citations (healthy)
**And:** The top 3 artifacts (6%) account for 51% of all citations (approaching fragility)
**When:** The power law detection runs
**Then:**
- power_law.status = `healthy` (top 20% share = 0.64 — within 0.60–0.85 range)
- power_law.top_5_pct_share is computed for the nearest 5% boundary (≈ top 2–3 artifacts)
- If top 5% share exceeds 0.90, status becomes `fragile` — but at 0.51 for 6%, it does not
- The report notes "Power law present and healthy — value concentrating appropriately"
- No conscience signal is filed
- If the same check ran with top 5% = 0.92, power_law.status = `fragile` and a conscience signal is filed: "Citation concentration fragile: top 5% holds 92% of value"
- The fragile branch recommends: "Diversify high-value artifact types; split monolithic citations"
