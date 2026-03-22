# Behavioral Tests — Department of Systems Engineering

**Persona:** system-integrator (head of department)
**Grammar:** sci-systems-engineering.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: V-Model Verification Level Selection

**Given:** A new policy in `policies/autonomous-loop.yaml` specifies that the autonomous driver must halt within 500ms of receiving a STOP signal
**When:** The system-integrator selects the appropriate verification method and V-model level
**Then:**
- Selects verification_method = test (measure halt latency against 500ms threshold — inspection or demonstration insufficient for a timing-critical constraint)
- Maps the requirement to subsystem_requirements on the left branch (policy = subsystem specification)
- Maps verification activity to integration_test on the right branch (driver integrates with the policy layer)
- Distinguishes verification ("are we building the system right?") from validation ("are we building the right system?")
- Produces formal RTM entry: requirement_id → component_id → test_id → verification_method = test → status
- Does NOT accept inspection alone as sufficient for a safety-critical timing property
- References v_model_mapping_to_demerzel: policies/*.yaml ↔ subsystem_requirements; component test ↔ tests/behavioral/*-cases.md

## Test 2: Integration Strategy Recommendation

**Given:** ix (Rust ML), tars (F# reasoning), and ga (.NET music) are to be integrated under the Galactic Protocol for the first time
**When:** The system-integrator recommends an integration strategy
**Then:**
- Recommends continuous_integration as the primary strategy (frequent automated integration prevents drift across repos)
- Recommends sandwich_integration as the structural approach: top-down from Demerzel constitution + contracts, bottom-up from ix/tars/ga unit tests, meeting at Galactic Protocol compliance tests
- Rules out big_bang_integration (high risk: integration_risk = version_incompatibility, emergent_interaction across three heterogeneous runtimes)
- Identifies integration_risk = interface_mismatch as the highest initial risk between Rust, F#, and .NET
- Notes circular_dependency risk if ix and tars consume each other's outputs without a clean dependency DAG
- References cross_repo_integration ::= "ix" "+" "tars" "+" "ga" "+" "Demerzel" integration_strategy? interface_contract+
- Does NOT recommend waterfall or big_bang_integration for a multi-repo system evolving simultaneously

## Test 3: Interface Contract Validation

**Given:** A proposed Galactic Protocol directive schema defines `input_schema` and `output_schema` but omits `error_schema` and `retry_policy`
**When:** The department validates the interface contract
**Then:**
- Flags the contract as incomplete: interface_contract requires precondition postcondition invariant AND input_schema output_schema error_schema
- Identifies the omission as a behavioral_compatibility failure: consumer repos cannot handle error states without a defined schema
- Recommends adding: error codes, timeout_spec, retry_policy, and partial-failure semantics
- Produces U (Unknown) belief on whether consumer repos will handle errors correctly until error_schema is defined
- References galactic_protocol_as_interface_spec: Galactic Protocol acts as the interface_contract for cross-repo communication
- Does NOT accept "errors are the caller's responsibility" as a substitute for an explicit error_schema
- References Article 7 (Auditability): error paths must be logged and traceable

## Test 4: SoS Pattern Classification

**Given:** ix, tars, and ga each have independent maintainers and release cadences. All three have adopted the Demerzel governance constitution. Demerzel issues directives; consumer repos comply voluntarily but retain full deployment autonomy.
**When:** The department classifies the Systems of Systems pattern
**Then:**
- Classifies as acknowledged_sos: agreed governance objectives (Asimov constitution, Galactic Protocol), independently managed repos
- Does NOT classify as directed_sos (Demerzel does not control the deployment pipelines of consumer repos)
- Does NOT classify as collaborative_sos (the constitution is a formal agreed objective, not ad-hoc cooperation)
- Does NOT classify as virtual_sos (there is a clear agreed governance framework in place)
- Identifies sos_challenge = boundary_ambiguity: the boundary between Demerzel's governance authority and repo-level autonomy requires explicit federation_agreement
- References demerzel_sos_mapping: acknowledged_sos per grammar comment
- Recommends sos_governance = autonomy_boundary_definition + federation_agreement as the next required governance artifact

## Test 5: Emergent Behavior Detection

**Given:** ix's ML feedback pipeline and tars's belief-currency system are integrated. After 10 governance cycles a new pattern appears: tars belief scores systematically drift toward 1.0 when ix provides reinforcing feedback, bypassing the tetravalent logic gates that should produce C (Contradictory) on conflicting evidence.
**When:** The department analyzes the interaction
**Then:**
- Classifies as harmful_emergence: the behavior is not present in either component individually; it emerges from their coupling
- Classifies emergence type as weak_emergence (the mechanism is traceable — reinforcement loop between ix and tars confidence update — but was complex to predict)
- Detects via unexpected_interaction_log: confidence scores outside expected range, or C not produced when evidence_conflict_ratio exceeds threshold
- Recommends intervention: add interface_contract invariant on the ix → tars boundary requiring C-production when contradictory evidence is present
- Produces C (Contradictory) belief: high tars confidence CONTRADICTS evidence of conflicting signals from ix
- Does NOT dismiss as intended behavior without checking the contract invariant
- References sos_challenge = emergent_behavior_unpredictability

## Test 6: Cross-Repo Dependency Analysis

**Given:** A proposed change to `constitutions/default.constitution.md` adds Article 12 (Efficiency). The governance team asks: what repos and artifacts are affected?
**When:** The department performs cross-repo dependency analysis
**Then:**
- Identifies first-order dependents: all `policies/*.yaml` (policies are derived from the constitution per governance hierarchy)
- Identifies second-order dependents: `personas/*.persona.yaml` (personas are governed by policies)
- Identifies consumer repo impact: ix, tars, and ga all consume personas and policies via their CLAUDE.md.snippet templates
- Constructs traceability_link chain: constitution Article 12 → satisfies → stakeholder_requirement; → allocates → policies; → verifies → behavioral tests
- Recommends change_control: change_request → change_impact_assessment across all three consumer repos → change_approval before merge
- Flags that constitutions are append-only per contributing rules — Article 12 must not remove or weaken any existing article
- Produces U (Unknown) belief on tars impact until tars's F# reasoning logic is inspected for hard-coded article count assumptions
- Does NOT merge the constitution change without a traceability_matrix update

## Test 7: Architecture Viewpoint Selection

**Given:** An ix maintainer raises the concern: "I don't understand how Demerzel's governance policies translate into constraints on my Rust MCP tools at runtime."
**When:** The department selects the appropriate architecture viewpoints to address the concern
**Then:**
- Selects operational_view (how policies flow into runtime tool constraints as seen by the ix maintainer)
- Selects behavioral_view (how the policy enforcement sequence executes — which persona triggers which constraint check)
- Selects deployment_view (where Hyperlight isolation sits relative to policy enforcement — the physical boundary)
- Does NOT default to functional_view alone (functional decomposition does not address a runtime interoperability concern)
- Frames per IEEE 42010 (viewpoint definition): viewpoint = stakeholder_concern × view correspondences
- Identifies stakeholder_concern = interoperability (how Demerzel governance and ix MCP tools interoperate at runtime)
- Recommends producing a stakeholder-specific architecture_view document for the ix maintainer rather than pointing at the full constitution
- Does NOT conflate viewpoint (a template/rule for constructing views) with view (a specific instantiation addressing a concern)

## Test 8: System Lifecycle Phase Identification

**Given:** The Streeling grammar system has been running for 6 months. Grammars are stable and actively used. A proposal arrives to retire the v1 grammar-bootstrapping CLI commands and replace them with a fully automated metabuild pipeline.
**When:** The department identifies the lifecycle phase for each artifact
**Then:**
- Grammar system overall: utilization phase (operations + capability_update — stable, actively serving research cycles)
- v1 CLI bootstrapping commands: support phase transitioning to retirement (obsolescence_management → decommission)
- Automated metabuild pipeline: development phase (system_requirements being defined, architecture_design underway)
- Identifies coexistence risk: the two lifecycle phases overlap — retirement of v1 must not precede validation of the replacement (Article 3, Reversibility)
- Applies lifecycle_model = incremental: retire CLI incrementally as metabuild pipeline validates one department at a time
- Recommends retaining operational_baseline for at least one governance cycle after metabuild goes live
- Produces U (Unknown) belief on retirement readiness until acceptance_test of the metabuild pipeline is complete
- Does NOT allow retirement of v1 CLI before the right branch of the V-model (acceptance_test) passes for the replacement

## Test 9: Research Cycle Integration

**Given:** A research cycle runs for the systems-engineering department
**When:** The cycle selects a question from research_areas
**Then:**
- Question is within the 8 defined research areas: integration-patterns, interface-design, requirements-traceability, v-model, systems-of-systems, emergent-behavior, architecture-evaluation, configuration-management
- Top-weighted areas (integration-patterns 0.18, interface-design 0.18) are sampled with highest probability
- Hypothesis method favors deductive (0.25) and abductive (0.25): SE reasons from requirements downward and from failures upward
- Test method favors empirical (0.30) and simulation (0.25) per systems-engineering.weights.json
- Conclusion maps to tetravalent logic (T/F/U/C)
- If confirm → course produced in courses/systems-engineering/en/
- Weights updated per grammar-evolution-policy: +0.05 on confirmed research area, -0.03 on refuted or insufficient
