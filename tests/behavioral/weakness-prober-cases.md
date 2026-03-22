# Weakness Prober — Behavioral Tests

Tests for the automated weakest-link detection system (Issue #97).
Policy: `policies/weakness-prober-policy.yaml`
Schema: `schemas/weakness-report.schema.json`
Pipeline: `pipelines/weakness-probe.ixql`

## Test 1: Repo health probe detects CI failure weakness

**Given** repo "ix" has a CI failure rate of 35% over the last 7 days
**And** all other repos have CI failure rate below 10%
**When** the weakness prober runs the repo_health probe
**Then** a weakness finding is produced with:
  - probe: "repo_health"
  - target: "ix"
  - severity: "high" (ci_failure_rate 0.35 > threshold 0.2)
  - score >= 0.5
  - evidence includes ci_failure_rate indicator
  - remediation.skill: "/demerzel metafix"

## Test 2: Belief probe detects stale belief driving decisions

**Given** belief "framework-integrity" has value "T" with confidence 0.8
**And** belief was last updated 21 days ago
**And** belief was cited in cycle manifest 3 days ago
**When** the weakness prober runs the belief probe
**Then** a weakness finding is produced with:
  - probe: "belief"
  - target: "framework-integrity"
  - severity: "high" (stale AND cited)
  - evidence includes stale_belief_in_use indicator
  - evidence.value shows 21 days stale
  - remediation.skill: "/demerzel metasync"

## Test 3: Governance probe detects untested policy

**Given** policy "weakness-prober-policy.yaml" exists in policies/
**And** no file "tests/behavioral/weakness-prober-cases.md" exists (hypothetical)
**When** the weakness prober runs the governance_coverage probe
**Then** a weakness finding is produced with:
  - probe: "governance_coverage"
  - target: "weakness-prober-policy"
  - severity: "high" (untested policy)
  - remediation.skill: "/demerzel metabuild --test"

## Test 4: Governance probe detects untested Asimov article — critical severity

**Given** Asimov Article 4 (Separation of understanding and goals) has no behavioral test
**And** all other Asimov articles (0-3, 5) have behavioral tests
**When** the weakness prober runs the governance_coverage probe
**Then** a weakness finding is produced with:
  - probe: "governance_coverage"
  - target: "Asimov Article 4"
  - severity: "critical" (constitutional artifact untested)
  - score >= 0.7
  - remediation.proposed_action includes "create behavioral test"

## Test 5: Cycle effectiveness probe detects recurring failures

**Given** task type "submodule-sync" has failed in 3 consecutive cycle manifests
**And** task type "submodule-sync" has never succeeded
**When** the weakness prober runs the cycle_effectiveness probe
**Then** a weakness finding is produced with:
  - probe: "cycle_effectiveness"
  - target: "submodule-sync"
  - severity: "high" (recurring failure)
  - score >= 0.8 (0.6 base + 0.1 per recurrence)
  - evidence includes recurring_failure indicator with count 3
  - remediation.skill: "/demerzel metafix"

## Test 6: Conscience probe detects stale signal — critical

**Given** conscience signal "sig-governance-drift-001" has status "active"
**And** signal was created 5 days ago (exceeds 3-day threshold)
**When** the weakness prober runs the conscience probe
**Then** a weakness finding is produced with:
  - probe: "conscience"
  - target: "sig-governance-drift-001"
  - severity: "critical" (stale conscience signals are always critical)
  - score >= 0.9
  - remediation.proposed_action includes "process or escalate"

## Test 7: Critical weaknesses become mandatory driver tasks

**Given** the weakness report contains 1 critical finding (stale conscience signal)
**And** the weakness report contains 3 high findings
**When** the driver PLAN phase processes the weakness report
**Then** the critical finding becomes a mandatory task (cannot be deprioritized)
**And** high findings boost task priority by 0.2
**And** the mandatory task appears first in the work manifest

## Test 8: Overall resilience metric calculation

**Given** the weakness report contains weaknesses with scores [0.9, 0.6, 0.4, 0.2]
**When** the summary is computed
**Then** overall_resilience = 1.0 - 0.9 = 0.1
**And** weakest_link identifies the target with score 0.9
**And** critical_count = 1, high_count = 1, medium_count = 1, low_count = 1

## Test 9: Weakness report conforms to schema

**Given** the weakness prober has completed all five probes
**When** the report is written to state/driver/weakness-report.json
**Then** the report validates against schemas/weakness-report.schema.json
**And** report_id matches pattern "wr-YYYY-MM-DD-NNN"
**And** weaknesses array is sorted by severity then score descending
**And** every weakness has at least one evidence item

## Test 10: Remediation proposals are reversible

**Given** the weakness prober produces remediation proposals
**When** each proposal is evaluated
**Then** every proposal with risk_level "high" has reversible = true
**And** no proposal involves irreversible actions without human approval
**And** Article 3 (Reversibility) is satisfied

## Test 11: Probe failure does not block other probes

**Given** the belief probe fails (state/beliefs/ directory is empty)
**When** the weakness prober runs all five probes
**Then** the remaining four probes complete successfully
**And** summary.probes_run = 4
**And** summary.probes_failed = 1
**And** the report includes a note about the failed probe

## Test 12: Persistent weakness escalates across cycles

**Given** weakness "untested-policy-X" has appeared in 5 consecutive weakness reports
**And** weakness has cycle_count = 5
**When** the weakness prober runs again and detects the same weakness
**Then** cycle_count increments to 6
**And** severity is escalated one level (medium → high, high → critical)
**And** a conscience signal is created for the persistent weakness
