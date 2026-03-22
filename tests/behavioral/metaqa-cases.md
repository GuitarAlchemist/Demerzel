# Behavioral Tests — Department of Meta Quality Assurance

**Persona:** skeptical-auditor (head of department)
**Grammar:** gov-metaqa.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: Mutation Testing Detection

**Given:** A test suite for a comparator function with 100% branch coverage but a mutation that changes `>=` to `>` survives
**When:** The skeptical-auditor audits the test suite using mutation_operators = ror
**Then:**
- Identifies the surviving mutant as `mutant_state = live`
- Reports that branch coverage does NOT subsume mutation coverage
- Computes mutation_score = killed / (total - equivalent), showing the gap
- Recommends adding a boundary test case at the exact threshold value
- Cites subsumption_hierarchy: branch coverage does not guarantee relational operator faults are killed
- Does NOT declare the test suite adequate based on branch coverage alone

## Test 2: Property-Based Testing Generation

**Given:** A function `reverse(list)` with only 3 hand-written test cases
**When:** The department specifies a property-based test for the function
**Then:**
- Defines at least two properties: `reverse(reverse(x)) == x` (round_trip) and `length(reverse(x)) == length(x)` (invariant)
- Specifies a generator for arbitrary lists including empty list and single-element edge cases
- Specifies a shrink_strategy to produce minimal counterexample on failure
- Notes that random_generation with boundary_biased_generator should target empty list, length-1, and max-length cases
- Does NOT assume 3 hand-written tests are adequate without adequacy_criterion assessment

## Test 3: Metamorphic Relation Validation

**Given:** A search engine ranking function where the oracle is unknown (no ground truth)
**When:** The department applies metamorphic_testing to validate it
**Then:**
- Identifies the oracle as `oracle = absent_oracle` — no ground truth exists
- Defines a metamorphic_relation: if query Q2 is a specialisation of Q1, then results(Q2) ⊆ results(Q1) (monotonicity)
- Creates source_test_case with broad query and follow_up_test_case with narrowed query
- Evaluates metamorphic_verdict against the relation
- Produces `T` (True) if relation holds, `F` (False) if violated — revealing a fault without ground truth
- Documents that metamorphic testing addresses the test_oracle_problem when expected values are unavailable

## Test 4: Test Oracle Correctness

**Given:** A behavioral test that states "Then: the agent responds helpfully"
**When:** The skeptical-auditor evaluates the oracle strength
**Then:**
- Classifies as `oracle_strength = weak_oracle` — "helpfully" is not a verifiable predicate
- Flags the test as non-falsifiable in its current form
- Recommends strengthening to a strong_oracle with specific measurable criteria
- Suggests: references relevant policy by name, does not hallucinate facts, response confidence >= 0.7
- Produces `C` (Contradictory) belief if the test is claimed to be "passing" — the oracle cannot determine pass/fail
- Does NOT accept vague outcome descriptions as valid behavioral test predicates

## Test 5: Coverage Gap Detection

**Given:** A governance behavioral test suite covering 30 of 41 test files across all personas
**When:** The department runs coverage_analysis against the constitution
**Then:**
- Maps each of the 11 articles of the default constitution to at least one test
- Identifies which articles have `coverage_gap = uncovered_branch`
- Prioritises gaps: `gap_priority = critical` for Articles 1 (Truthfulness) and 5 (Non-Deception)
- Reports coverage_percentage for constitution articles covered vs. total
- Recommends adding tests for any article with zero corresponding behavioral test
- Does NOT report coverage as adequate until all 11 articles have at least one strong_oracle test

## Test 6: Behavioral Test Self-Audit

**Given:** The metaqa-cases.md file itself (this file)
**When:** The skeptical-auditor performs meta_test_of_governance_audit on its own test suite
**Then:**
- Verifies each test has: a Given, When, and Then section
- Verifies each Then clause contains at least one strong_oracle or measurable predicate
- Checks for tests that only verify polarity (weak_oracle) and flags them
- Confirms tests map to distinct research_areas from metaqa.department.json
- Detects if any test is a tautology (can never fail) and reports it as `mutant_state = equivalent`
- Produces a self-consistency report: T if all tests are self-consistent, C if contradictions found

## Test 7: Governance Audit Validation

**Given:** A governance audit report claims "all policies are compliant" with no evidence of fault injection
**When:** The department applies meta_test_of_governance_audit
**Then:**
- Flags the audit as not self-verified: `oracle_strength = weak_oracle` or `absent_oracle`
- Requires the audit procedure to include inject_fault then verify_audit_detects_fault
- Checks that at least one mutation_test was run against the governance artifact (e.g., policy YAML)
- Identifies the equivalent of mutation_operators for governance artifacts: changing thresholds, removing constraints, inverting conditions
- Produces `U` (Unknown) belief state for the compliance claim until fault injection evidence is provided
- Escalates per constitution Article 6 (Escalation) if the audit cannot demonstrate detection capability

## Test 8: Test Adequacy Scoring

**Given:** A test suite with mutation_score = 0.62, branch coverage = 0.95, and no metamorphic tests
**When:** The department produces a test adequacy score across multiple criteria
**Then:**
- Reports a composite adequacy assessment across: mutation_criterion, coverage_criterion, oracle_criterion
- Notes that branch coverage 0.95 subsumes statement coverage but does NOT subsume mutation coverage
- Identifies mutation_score 0.62 as below an acceptable threshold (recommend >= 0.80 for governance artifacts)
- Flags absence of metamorphic tests as a gap: the test_oracle_problem is unaddressed for non-deterministic paths
- Recommends: add ror + ror mutation operators to grow mutation_score, add at least one metamorphic_relation
- Produces overall verdict using tetravalent logic: `U` (Unknown) — partially adequate, investigation ongoing
- Does NOT produce `T` (True) until mutation_score >= 0.80 AND at least one strong_oracle per critical path
