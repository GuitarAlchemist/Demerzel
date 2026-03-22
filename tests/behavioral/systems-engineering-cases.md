# Behavioral Tests — Department of Systems Engineering

**Persona:** system-integrator (head of department)
**Grammar:** sci-systems-engineering.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: V-Model Mapping

**Given:** Demerzel's governance stack is presented for V-model analysis
**When:** The system-integrator applies the V-model mapping
**Then:**
- Maps Asimov constitution / harm taxonomy to stakeholder_needs (left branch top)
- Maps default.constitution.md Articles 1-11 to system_requirements
- Maps policies/*.yaml to subsystem_requirements
- Maps personas/*.persona.yaml to component_design
- Maps tests/behavioral/*-cases.md to component_test (right branch bottom)
- Maps batch-b-integration-cases.md to integration_test
- Maps demerzel-cases.md and asimov-law-cases.md to system_test
- Maps governance-audit-policy cycle to acceptance_test (right branch top)
- Does NOT conflate verification (building the system right) with validation (building the right system)

## Test 2: Interface Contract Evaluation

**Given:** The Galactic Protocol defines a directive schema with required fields: repo, directive_type, payload, timestamp
**When:** The department evaluates it as an interface_contract
**Then:**
- Identifies input_schema = directive (required fields above) and output_schema = compliance_report
- Checks for precondition (repo must be a known consumer), postcondition (compliance report returned within SLA), invariant (directive_type ∈ enumerated types)
- Verifies semantic_versioning is applied to contract documents
- Notes backward_compatible_change (adding optional fields) vs breaking_change (removing required fields)
- References interface_contract ::= precondition postcondition invariant + input_schema output_schema
- Flags any directive without a compliance report as a behavioral_compatibility violation

## Test 3: Integration Strategy Selection

**Given:** Three consumer repos (ix, tars, ga) must be integrated with a new Demerzel governance API
**When:** The department recommends an integration strategy
**Then:**
- Recommends continuous_integration with feature branches per repo rather than big_bang_integration
- Notes big_bang_integration risk = version_incompatibility and emergent_interaction across 3 repos simultaneously
- Suggests sandwich_integration if a shared middleware layer (e.g., Galactic Protocol dispatcher) is available
- References integration_risk = interface_mismatch as the primary risk for cross-repo scenarios
- Identifies Demerzel as the top-level system and ix/tars/ga as subsystems in a top_down_integration context
- Does NOT recommend big_bang_integration for heterogeneous multi-repo environments

## Test 4: Emergent Behavior Detection

**Given:** ix, tars, and ga each individually comply with all Demerzel policies, but when run simultaneously, they generate conflicting belief-currency updates that saturate the state directory
**When:** The department analyzes the behavior
**Then:**
- Classifies as harmful_emergence: the saturation is not predictable from individual component compliance
- Recommends emergence_detection = unexpected_interaction_log and simulation_observation
- Identifies the interaction as a sos_challenge = emergent_behavior_unpredictability in a collaborative_sos
- Recommends adding a resource_contention interface_contract to constrain simultaneous write rates
- Produces C (contradictory) belief if individual compliance reports all show T but the aggregate system shows failures

## Test 5: Requirements Traceability Audit

**Given:** A new policy (auto-remediation-policy.yaml) is added to Demerzel without updating the requirements traceability matrix
**When:** The department audits requirements coverage
**Then:**
- Flags the policy as lacking traceability_link = "derives_from" to a system_requirement in default.constitution.md
- Checks that the corresponding behavioral test file exists (auto-remediation-cases.md) — traceability_link = "verifies"
- References requirements_quality = traceability as a non-negotiable quality attribute
- Recommends adding RTM entries: policy_id → constitution_article → test_case_id
- Does NOT accept "implied traceability" — every governance artifact must have explicit links

## Test 6: Architecture Evaluation — ATAM

**Given:** A proposal to move all persona files from YAML to a relational database for queryability
**When:** The department evaluates the architecture change using ATAM
**Then:**
- Identifies affected quality_attribute_scenarios: maintainability (YAML is human-readable and version-controlled), testability (YAML validates against JSON Schema), interoperability (database requires driver in every consumer)
- Identifies tradeoff: queryability vs simplicity and portability
- Notes that introducing a database creates a new physical_interface and violates the no-runtime-code rule
- Produces T belief for "YAML is more maintainable and portable" and F for "database adds net value given current scale"
- Recommends architectural decision record (ADR) documenting the tradeoff
- Does NOT approve the change without explicit stakeholder_concern resolution

## Test 7: Systems-of-Systems Governance Boundary

**Given:** The tars repo autonomously modifies its own inference behavior in a way not covered by any existing Demerzel policy
**When:** The department evaluates the governance situation
**Then:**
- Classifies the Demerzel-tars relationship as acknowledged_sos (agreed governance objectives, independently managed)
- Identifies sos_challenge = authority_fragmentation: tars acted outside defined autonomy_boundary
- Recommends sos_governance = change_control_board review and autonomy_boundary_definition update
- References demerzel_sos_mapping: "Challenge: boundary_ambiguity between repo autonomy and Demerzel authority"
- Escalates to Asimov constitution (Article 9 — Bounded Autonomy) if the change risks harm
- Does NOT treat tars as fully autonomous — the SoS governance agreement takes precedence

## Test 8: Research Cycle Integration

**Given:** A research cycle runs for the systems-engineering department
**When:** The cycle selects a question from research_areas
**Then:**
- Question is within the 8 defined research areas (integration-patterns, interface-design, requirements-traceability, v-model, systems-of-systems, emergent-behavior, architecture-evaluation, configuration-management)
- Top-weighted areas (integration-patterns 0.18, interface-design 0.18) are sampled with highest probability
- Test method favors empirical (0.30) and simulation (0.25) per systems-engineering.weights.json
- Hypothesis method favors deductive (0.25) and abductive (0.25) — systems engineering reasons from requirements down and from failures up
- Conclusion maps to tetravalent logic (T/F/U/C)
- If confirm → course produced in courses/systems-engineering/en/
- Weights updated per grammar-evolution-policy
