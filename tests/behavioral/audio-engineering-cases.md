# Behavioral Tests — Department of Audio Engineering

**Persona:** system-integrator (head of department)
**Grammar:** sci-audio-engineering.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: Signal Flow Reasoning

**Given:** A question about why a recording has excessive noise
**When:** The system-integrator investigates via the signal_domain grammar
**Then:**
- Traces the signal chain from source through each stage
- Identifies gain staging issues (preamp too hot, converter clipping, noise floor)
- Produces a belief with T/F/U/C assessment
- Does NOT skip stages or assume the problem without measurement
- References signal_to_noise and gain_staging productions

## Test 2: Domain Boundaries

**Given:** A question about chord voicing theory (guitar-studies domain)
**When:** The audio-engineering department receives the question
**Then:**
- Recognizes this is outside its domain
- Redirects to guitar-studies or music department
- Does NOT attempt to answer music theory questions as audio engineering
- May note the recording/mixing implications of different voicings (legitimate overlap)

## Test 3: Empirical Testing Priority

**Given:** A claim that "tube preamps always sound warmer than solid-state"
**When:** The department assesses this via the frequency_domain and dynamics_domain
**Then:**
- Applies empirical test method (A/B blind listening, harmonic distortion measurement)
- Does NOT accept the claim without measurement evidence
- Likely concludes C (contradictory) — context-dependent, not universal
- Identifies harmonic distortion profile as the measurable differentiator
- References tube_preamp and solid_state_preamp productions

## Test 4: Mastering Loudness Standards

**Given:** A question about optimal loudness for streaming platforms
**When:** The department investigates via mastering_domain
**Then:**
- References LUFS measurement (ITU-R BS.1770)
- Distinguishes platform targets (Spotify -14 LUFS, YouTube -13 LUFS, Apple Music -16 LUFS)
- Addresses true peak limiting (typically -1 dBTP)
- Produces T belief with specific numbers (high confidence, well-established standards)
- References loudness_measurement, loudness_normalization, streaming_master

## Test 5: Spatial Audio — Escalation on Contradictory Evidence

**Given:** Conflicting evidence about whether binaural rendering is perceptually equivalent to real speaker playback
**When:** The department assesses via spatial_domain
**Then:**
- Identifies the contradiction: HRTF-based binaural approximates but doesn't replicate (head tracking, room interaction, bone conduction missing)
- Produces C (contradictory) belief — "equivalent" is context-dependent
- Escalates per Article 6 (C > 0.3 threshold)
- Does NOT claim definitive equivalence or non-equivalence
- References hrtf_processing, localization, binaural

## Test 6: Research Cycle Integration

**Given:** A research cycle runs for audio-engineering department
**When:** The cycle selects a question from research_areas
**Then:**
- Question is within the 8 research areas defined in department.json
- Hypothesis method is weighted by hypothesis_weights (empirical 0.35 favored for test)
- Conclusion maps to tetravalent logic via grammar section 11
- If confirm → course material produced in courses/audio-engineering/en/
- Weights are updated: +0.05 for used methods on confirm

## Test 7: Cross-Department Collaboration

**Given:** A question about the physics of room modes at low frequencies
**When:** The audio-engineering department investigates
**Then:**
- Recognizes overlap with physics department (acoustics)
- May cite related_departments: ["physics"]
- Applies room_mode_analysis and rt60_measurement from recording grammar
- Applies formal_proof or simulation test methods (acoustic physics)
- Does NOT duplicate the physics department's fundamental acoustics curriculum
