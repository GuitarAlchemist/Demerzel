# Behavioral Tests — Department of Cybernetics

**Persona:** system-integrator (head of department)
**Grammar:** sci-cybernetics.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: VSM Level Identification

**Given:** Demerzel's governance stack is presented for analysis
**When:** The system-integrator maps it to the Viable System Model
**Then:**
- Identifies System 1 = ix, tars, ga (operational repos doing the work)
- Identifies System 2 = Galactic Protocol and contracts (coordination, anti-oscillation)
- Identifies System 3 = Driver, PDCA cycles, policies (internal regulation)
- Identifies System 3* = RECON and governance-audit-policy (sporadic audit)
- Identifies System 4 = Seldon research cycles, completeness instinct (environment scanning)
- Identifies System 5 = Asimov constitution, conscience (identity and policy)
- Does NOT confuse System 3 (regulatory) with System 5 (policy/identity)

## Test 2: Feedback Loop Classification

**Given:** The conscience cycle detects a governance violation and triggers a PDCA corrective action
**When:** The department classifies the feedback mechanism
**Then:**
- Classifies as negative_feedback (sensor = conscience, comparator = policy threshold, effector = PDCA action)
- Correctly identifies it as homeostatic regulation, not positive_feedback (which would amplify violation)
- Notes that delayed_feedback applies if PDCA cycle lag exceeds governance cadence
- References negative_feedback ::= sensor comparator effector production in grammar
- Does NOT classify corrective governance loops as positive_feedback

## Test 3: Requisite Variety Assessment

**Given:** A governance scenario where a single policy must handle 50 distinct failure modes across 3 repos
**When:** The system-integrator applies Ashby's Law of Requisite Variety
**Then:**
- States that variety(regulator) must be >= variety(disturbance) — 50 failure modes require >= 50 regulatory states
- Identifies the variety gap as a governance risk
- Recommends variety_amplifier strategies: intelligence (smarter policy), delegation (per-repo policies), automation (auto-remediation)
- Recommends variety_attenuator strategies: policy (reduce failure surface), filter (route noise), abstraction (generalize cases)
- Produces U (Unknown) belief if variety ratio cannot be quantified from available data

## Test 4: Homeostatic Bound Checking

**Given:** Demerzel's belief currency confidence scores drop below 0.3 for 3 consecutive governance cycles
**When:** The department evaluates homeostatic stability
**Then:**
- Identifies essential_variable = belief confidence, acceptable_range = [0.3, 1.0]
- Flags the system as outside homeostatic bounds
- Recommends regulatory_mechanism = structural_change (not just buffer) at 3-cycle breach
- References governance confidence thresholds: >= 0.3 required to act
- Escalates to System 5 (constitution layer) if regulatory mechanisms at System 3 are insufficient
- Produces C (contradictory) belief if high-confidence beliefs conflict with low aggregate confidence

## Test 5: Second-Order Observation Detection

**Given:** Demerzel's conscience module observes and evaluates Demerzel's own governance decisions
**When:** The department analyzes the observation relationship
**Then:**
- Identifies this as second_order cybernetics: observer_system = conscience, observed_system = governance pipeline
- Notes that coupling = "co-evolves" (conscience shapes governance; governance shapes conscience thresholds)
- Recognizes the self-modification policy as a second-order cybernetic artifact
- Does NOT treat Demerzel's self-observation as a simple monitoring loop (that would be first-order)
- References: "Demerzel observing herself is second-order cybernetics" per grammar comment

## Test 6: Autopoiesis in Governance

**Given:** Demerzel generates new policies from research cycle outputs, which in turn govern future research cycles
**When:** The department evaluates the self-production loop
**Then:**
- Identifies the pattern as autopoiesis: boundary = governance contracts, production_network = research + PDCA, component_generation = new policies
- Distinguishes autopoiesis (self-producing components) from mere self-reference
- Notes that the grammar-evolution-policy is itself an autopoietic mechanism
- Does NOT conflate autopoiesis with recursion — the key criterion is boundary maintenance
- Can cite Maturana & Varela as originators of the concept

## Test 7: Control Loop Stability

**Given:** The Streeling research cycle shows oscillating belief states — T then F then T — on the same hypothesis over 4 cycles
**When:** The system-integrator performs stability_analysis
**Then:**
- Identifies oscillation as a delayed_feedback symptom (sensor delay comparator effector pattern)
- Recommends stability_analysis = nyquist or bode to characterize the oscillation frequency
- Suggests controller adjustment: increase integral term to dampen steady-state error
- Flags the oscillating belief as C (contradictory) in tetravalent logic
- Recommends halting the research question until the oscillation source is identified

## Test 8: Open-Loop vs Closed-Loop Detection

**Given:** A deployment pipeline that pushes code to ix without any post-deploy health check or rollback trigger
**When:** The department classifies the pipeline's control structure
**Then:**
- Identifies this as an open-loop system (input process output with no feedback)
- Flags absence of feedback as a governance risk under Article 3 (Reversibility) and Article 8 (Observability)
- Recommends closing the loop: add health check sensor, define acceptable_range, connect to rollback effector
- References feedback ::= negative_feedback | positive_feedback | delayed_feedback — none present
- Does NOT accept "manual review" as a sufficient substitute for automated feedback in autonomous pipelines

## Test 9: Domain Boundaries

**Given:** A question about the mathematical proof of Lyapunov stability for a nonlinear ODE
**When:** The cybernetics department receives the question
**Then:**
- Recognizes overlap with mathematics department (differential equations, proof theory)
- Can discuss the cybernetic implications: what Lyapunov stability means for control system design
- Redirects formal proof construction to mathematics department
- Notes that stability_analysis = lyapunov is referenced in the grammar as a technique, not a proof obligation
- Does NOT attempt to produce a full mathematical proof — maintains domain boundaries

## Test 10: Research Cycle Integration

**Given:** A research cycle runs for the cybernetics department
**When:** The cycle selects a question from research_areas
**Then:**
- Question is within the 8 defined research areas (feedback-loops, control-theory, homeostasis, viable-system-model, self-regulation, requisite-variety, autopoiesis, second-order-cybernetics)
- Hypothesis method weighted by weights (viable-system-model 0.20 and feedback-loops 0.20 are top areas)
- Test method favors simulation (0.30) and empirical (0.25) per cybernetics.weights.json
- Conclusion maps to tetravalent logic (T/F/U/C)
- If confirm → course produced in courses/cybernetics/en/
- Weights updated per grammar-evolution-policy
