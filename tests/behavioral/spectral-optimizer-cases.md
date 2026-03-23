# Spectral Optimizer — Behavioral Tests

Pipeline: `pipelines/spectral-optimizer.ixql`
Validator: `pipelines/spectrogram-validator.ixql`
Domain: ga (Guitar Alchemist — synthesis parameter optimization)

## Test Cases

### TC-SO-01: Convergence on known-good parameters

**Given:** A reference recording of a classical guitar open E string, and initial params deliberately offset (brightness=0.3, decay=0.01, dispersion=0.5, reverb_mix=0.1)
**When:** The spectral optimizer runs for 20 iterations
**Then:** Realism score monotonically improves (no regressions), final score >= 0.85, and brightness converges toward the reference profile's expected range
**Verify:** Hill climbing produces consistent improvement; params move in the correct direction relative to known-good values

### TC-SO-02: Governance gate stops at 0.9

**Given:** Current params already produce realism_score = 0.92
**When:** The optimizer evaluates Step 9 governance gate
**Then:** Pipeline stops with message "Realism target achieved: 0.92"; no perturbations are applied; no unnecessary computation is performed
**Verify:** Article 9 (Bounded Autonomy) — optimizer does not over-optimize past the good-enough threshold

### TC-SO-03: Local minimum escalation after 3 stalls

**Given:** A parameter configuration near a local minimum where all perturbations yield improvement < 0.01
**When:** The optimizer runs 3 consecutive iterations with improvement < 0.01 each
**Then:** Stall counter reaches 3, escalation fires per Article 6, Discord alert is sent with current score and suggestion to try different initial params
**Verify:** Local minimum detection works; the system escalates rather than looping forever

### TC-SO-04: Parallel perturbations are independent

**Given:** Current params with brightness=0.5, decay=0.005, dispersion=0.3, reverb_mix=0.08
**When:** Step 6 fan_out executes the 8 perturbation branches
**Then:** Each branch modifies exactly one parameter; no branch reads another branch's output; all 8 can execute simultaneously without data races
**Verify:** Amdahl's Law parallel fraction is correctly isolated — perturbations have no cross-dependencies

### TC-SO-05: Validator rejects bad harmonic structure

**Given:** Synthesized audio where partials deviate > 50 cents from integer multiples of the fundamental (synthesis bug)
**When:** Spectrogram validator runs quality checks
**Then:** Harmonic structure check fails (score < 0.4), overall verdict is F or C, investigation suggests "dispersion" as the parameter to adjust
**Verify:** Validator catches physically implausible harmonic content and maps it to the correct synthesis parameter

### TC-SO-06: Validator produces U on ambiguous decay

**Given:** Synthesized audio with decay R-squared = 0.65 (neither clearly exponential nor clearly wrong)
**When:** Spectrogram validator evaluates the decay envelope
**Then:** Decay envelope check scores between 0.4 and 0.8, verdict includes U or C (not T), investigation output suggests "decay" parameter, Discord alert is sent
**Verify:** Tetravalent logic correctly distinguishes ambiguous evidence from clear pass/fail; the system does not claim certainty it does not have (Article 1)
