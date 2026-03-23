# Behavioral Tests — Department of Guitar Acoustics & Sound Synthesis

**Persona:** ga-musician (head of department)
**Grammar:** sci-guitar-acoustics.ebnf
**Bootstrapped by:** /demerzel metabuild

## TC-GA-ACO-01: Karplus-Strong Parameter Validation

**Given:** A synthesis configuration with decay coefficient set to 0.98
**When:** The ga-musician validates the parameter via the parameter_space grammar
**Then:**
- Rejects the decay coefficient as out of valid range (must be 0.99-0.9999)
- Produces F belief — parameter will cause unrealistic rapid decay
- Suggests valid alternatives (0.995 for bright, 0.9995 for sustained)
- References decay_coefficient production and its documented range constraint
- Does NOT proceed with synthesis using invalid parameters

## TC-GA-ACO-02: Spectral Realism Scoring

**Given:** A synthesized guitar tone and a reference recording of the same note
**When:** The department evaluates realism via the realism_verification grammar
**Then:**
- Computes spectral distance between synth and reference
- Applies perceptual scoring method (not just raw MSE)
- Threshold check: score >= 0.7 is acceptable, >= 0.8 is good, >= 0.9 is excellent
- Produces T belief if score meets threshold, F if below, U if reference quality is questionable
- References spectral_distance, perceptual_score, quality_threshold productions

## TC-GA-ACO-03: Guitar Profile Completeness

**Given:** A new guitar profile definition for "flamenco" type
**When:** The department validates the profile via the guitar_profile grammar
**Then:**
- Verifies the profile defines a resonator_config (resonator chain is mandatory)
- Verifies string_config is present with count, tuning, and gauge
- Verifies excitation_default is specified
- Produces F belief if any required component is missing
- References guitar_profile production: "Every profile MUST define its own resonator chain"
- Does NOT accept a profile without resonators regardless of other completeness

## TC-GA-ACO-04: Latency Constraint for Real-Time Synthesis

**Given:** A synthesis pipeline configuration targeting real-time playback
**When:** The department evaluates the pipeline via synthesis_pipeline grammar
**Then:**
- Checks total pipeline latency against realtime_10ms constraint
- Identifies which pipeline stages consume the most latency
- Produces T belief if pipeline meets < 10ms budget
- Produces F belief with specific bottleneck identification if over budget
- References latency_budget, buffer_size, sample_rate productions
- Suggests buffer_size reduction or algorithm simplification if failing

## TC-GA-ACO-05: Spectral Critic Generates Actionable Suggestions

**Given:** A synthesized tone with spectral centroid 20% higher than the reference
**When:** The department runs spectral analysis via spectral_analysis grammar
**Then:**
- Identifies the brightness mismatch via spectral_centroid feature
- Generates specific actionable suggestion: "Reduce brightness_factor or adjust loop_filter cutoff"
- Does NOT simply report "score is low" without diagnosis
- Maps the finding to parameter_space adjustments
- Produces C belief if brightness works for some profiles but not others
- References spectral_feature, parameter_set, optimization_target productions

## TC-GA-ACO-06: Reference Recording Quality Validation

**Given:** A reference recording submitted for realism comparison
**When:** The department validates the reference via realism_verification grammar
**Then:**
- Checks signal-to-noise ratio of the reference (must be adequate for comparison)
- Checks for clipping, excessive room reverb, or compression artifacts
- Produces U belief if reference quality is insufficient for reliable comparison
- Does NOT use a poor reference to judge synthesis quality
- Escalates per Article 6 if no valid reference is available
- References reference_matching, quality_threshold productions

## TC-GA-ACO-07: 12-String Mode Doubles Frequencies Correctly

**Given:** A twelve_string guitar profile configuration
**When:** The department validates the 12-string model via guitar_profile grammar
**Then:**
- Verifies string_count is twelve_string_doubled
- Checks that each course pair has correct frequency relationship (unison for lower strings, octave for upper)
- Validates sympathetic_coupling is enabled between paired strings
- Produces F belief if doubled strings use identical frequencies without octave offset for courses 3-6
- References twelve_string, string_config, coupling productions
- Tests that the output contains the expected doubled spectral content

## TC-GA-ACO-08: Realism Score Regression Detection

**Given:** A parameter update that changes loop_filter coefficients
**When:** The department evaluates the change via parameter_space and realism_verification grammars
**Then:**
- Runs realism scoring before and after the parameter change
- Compares scores across ALL guitar profiles (not just the target profile)
- Produces F belief if any profile's realism score drops by more than 0.05
- Identifies which specific profiles regressed and by how much
- Does NOT approve changes that improve one profile at the expense of others
- References optimization_target, quality_threshold, guitar_profile productions
- Triggers revise conclusion to re-enter the investigation cycle
