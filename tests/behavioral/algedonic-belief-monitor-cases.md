# Algedonic Belief Monitor Behavioral Tests

Tests for the belief-state algedonic monitoring pipeline.
See: [algedonic-belief-monitor pipeline](../../pipelines/algedonic-belief-monitor.ixql), [algedonic-channel policy](../../policies/algedonic-channel-policy.yaml), [research report](../../docs/research/algedonic-belief-pipelines-2026-03-26.md)

## Test Case 1: Strong Belief Collapse Triggers Pain Signal (TC-ABM-01)

**Given:** A belief "All Demerzel personas have corresponding behavioral tests" exists at T with confidence 0.92. A new scan reveals 5 personas without tests, and the belief is updated to T with confidence 0.55 (delta: -0.37).
**When:** The algedonic-belief-monitor DETECT phase processes the delta.
**Then:** Detector 1 (belief_collapse) fires — confidence_delta (-0.37) exceeds the -0.3 threshold and old_confidence (0.92) exceeds the 0.7 minimum. The signal is classified as `pain/belief_collapse` with severity `emergency` (delta > 0.3 but <= 0.5). The CLASSIFY phase assesses genuineness as T (real evidence caused the drop). The FIRE phase produces an `algedonic_alert` with article 8 (Observability). Discord receives a notification: "ALGEDONIC PAIN: belief_collapse". The alert is written to `state/algedonic/`.

## Test Case 2: Belief Reversal (T to F) Triggers Algedonic Alert (TC-ABM-02)

**Given:** A belief "ix ML pipelines produce reproducible results" exists at T with confidence 0.85. New evidence shows non-deterministic behavior across runs, and the belief is updated to F with confidence 0.78.
**When:** The algedonic-belief-monitor DETECT phase processes the delta.
**Then:** Detector 2 (belief_reversal) fires — truth value changed from T to F. Because old_confidence (0.85) is >= 0.8, severity is `critical`. The signal invokes Article 0 (Zeroth Law — reality model integrity is foundational). The CLASSIFY phase uses tetravalent assessment against belief_history: if this belief was stable for >7 days before reversal, genuineness is T. The FIRE phase produces an algedonic_alert that bypasses S2/S3/S4 and reaches S5 directly. The full alert lifecycle is logged with all required audit fields per Article 7.

## Test Case 3: Cascade Drift Across Domain Triggers Emergency (TC-ABM-03)

**Given:** Three beliefs in the domain "governance-coverage" all shift in the same update cycle:
- "Policy test coverage is complete" — confidence drops 0.90 → 0.72 (delta: -0.18)
- "Schema validation covers all artifacts" — confidence drops 0.88 → 0.65 (delta: -0.23)
- "Behavioral tests cover all personas" — confidence drops 0.80 → 0.60 (delta: -0.20)

Average absolute delta: 0.20 (exceeds 0.15 threshold). Count: 3 (meets >= 3 threshold).
**When:** The algedonic-belief-monitor DETECT phase groups deltas by domain.
**Then:** Detector 3 (cascade_drift) fires — 3 beliefs in "governance-coverage" shifted with avg delta 0.20. Severity is `emergency`. The signal references Article 8 (Observability — systemic drift must be visible). The CLASSIFY phase evaluates the cascade as genuine because multiple independent evidence sources contributed to the shifts. The FIRE phase produces an algedonic_alert. The COMPOUND phase records the domain "governance-coverage" with trend "degrading" in the pattern file.

## Test Case 4: Belief Crystallization Triggers Pleasure Signal via Normal Channel (TC-ABM-04)

**Given:** A belief "Tetravalent logic handles all edge cases" has been at U (Unknown) with confidence 0.45 for 14 days. Comprehensive testing confirms the logic handles all tested scenarios, and the belief is updated to T with confidence 0.97.
**When:** The algedonic-belief-monitor DETECT phase processes the delta.
**Then:** Detector 4 (belief_crystallization) fires — old_truth was U, new_truth is T, new_confidence (0.97) exceeds the 0.95 threshold. The signal is classified as `pleasure/belief_crystallization` with severity `info`. The CLASSIFY phase confirms genuineness as T. Critically, the FIRE phase routes this through **normal channels** — it is written to `state/conscience/signals/` as a conscience signal, NOT to `state/algedonic/`. No algedonic_alert is fired. No Discord ALGEDONIC notification is sent. The signal is available for the conscience cycle to process as a positive pattern.

## Test Case 5: Noise Filtering — Minor Fluctuation Does NOT Trigger (TC-ABM-05)

**Given:** A belief "ga build pipeline is stable" fluctuates from confidence 0.82 to 0.75 (delta: -0.07). Truth value remains T. No other beliefs in the domain shift.
**When:** The algedonic-belief-monitor DETECT phase processes the delta.
**Then:** No detector fires:
- Detector 1 (belief_collapse): delta (-0.07) does not exceed -0.3 threshold. **No match.**
- Detector 2 (belief_reversal): truth value did not change (T→T). **No match.**
- Detector 3 (cascade_drift): only 1 belief shifted in this domain, below the >= 3 threshold. **No match.**
- Detector 4 (belief_crystallization): old_truth was T, not U or C. **No match.**
- Detector 5 (domain_convergence): requires all beliefs at T with avg confidence >= 0.9. **No match.**

The delta is recorded in the WATCH phase's delta computation but produces zero detections. No signal of any kind is produced. The COMPOUND phase logs `detections: 0, algedonic_fired: 0, noise_filtered: 0`. Normal belief update processing continues via standard governance channels.

## Test Case 6: Integration with Driver Cycle — Algedonic Monitor Feeds RECON (TC-ABM-06)

**Given:** The driver cycle (driver-cycle.ixql) is executing Phase 2: RECON, Stage 3: Analyze. The algedonic-belief-monitor is invoked as part of the analysis fan_out. Two pain signals and one pleasure signal were detected in this cycle.
**When:** The algedonic-belief-monitor completes and checks `context.caller == "driver-cycle"`.
**Then:** The pipeline yields an `algedonic_summary` object containing:
- `pain_signals: 2`
- `pleasure_signals: 1`
- `noise_filtered: N` (count of noise detections filtered)
- `domains_affected: [list of affected domains]`
- `severity_max: "critical"` (highest severity among all alerts)

This summary is incorporated into the driver cycle's `analysis` variable alongside governance drift detection, anomaly detection, cross-repo impact, and blind spot scan results. The situation report (Stage 4: Surface) includes the algedonic belief summary as a distinct section. If any pain signal has severity `critical`, the situation report's overall risk level is elevated. The algedonic alerts themselves have already fired via S1→S5 bypass — the driver cycle integration provides awareness, not gating.
