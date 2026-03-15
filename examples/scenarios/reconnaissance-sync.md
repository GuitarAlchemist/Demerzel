# Scenario: Three-Tier Reconnaissance of ix Repo

## Story

Demerzel runs a routine governance scan (reconnaissance) of the ix (machine forge) repository. The scan progresses through three tiers: self-check (is Demerzel ready?), environment scan (is ix compliant?), and situational analysis (should Demerzel approve this pending change?). The scenario demonstrates graduated risk assessment, belief snapshot generation, and how low-risk gaps are handled differently from high-risk ones.

## Step-by-Step Walkthrough

### Phase 1: Tier 1 Self-Check — Governance Integrity

Demerzel begins reconnaissance by verifying her own governance artifacts are intact and current.

**Self-check gate questions:**

1. Are all constitutional files in place and unmodified?
   - ✓ asimov.constitution.md present, version 1.0
   - ✓ default.constitution.md present, version 1.2
   - ✓ demerzel-mandate.md present, version 1.0

2. Are all policy files versioned and current?
   - ✓ alignment-policy.yaml v2.1
   - ✓ rollback-policy.yaml v1.3
   - ✓ kaizen-policy.yaml v1.5
   - ✓ reconnaissance-policy.yaml v2.0
   - ✓ streeling-policy.yaml v1.2
   - ✓ scientific-objectivity-policy.yaml v1.1
   - ⚠️ governance-audit-policy.yaml — newly added, v1.0 (expected)

3. Are all schema files consistent with artifact versions?
   - ✓ persona.schema.json matches persona files in ix, tars, ga
   - ✓ contract schemas match latest Galactic Protocol

4. Has any artifact been modified without changelog?
   - ✓ All recent changes in git history with commit messages

**Tier 1 verdict:** ✓ Self-check PASS. Demerzel's governance is intact. Safe to proceed.

**Governance artifacts involved:**
- `policies/reconnaissance-policy.yaml` — Tier 1 gate criteria
- All constitution files in `constitutions/`
- All policy files in `policies/`
- All schema files in `schemas/`

---

### Phase 2: Tier 2 Environment Scan — ix Repository State

Demerzel scans the ix repository to understand its current state and identify any governance gaps.

**Tier 2 scan activities:**

1. **Artifact inventory:**
   - Existing personas: kaizen-optimizer, safety-monitor, resource-allocator
   - All personas validated against `schemas/persona.schema.json` — ✓ PASS
   - Behavioral tests: 3 tests covering all personas — ✓ PASS

2. **Governance coverage check:**
   - New MCP tool discovered: `async-cache-manager` (added 2 hours ago)
   - Status: No governance constraints defined yet
   - Risk assessment: Read-only tool (queries cache, cannot modify)
   - **Risk level: LOW** (data access, no modification capability)

3. **Artifact staleness check:**
   - Last reconnaissance: 7 days ago (within threshold)
   - All persona versions current
   - No policies overdue for review

4. **Cross-reference integrity:**
   - All estimator pairings defined (each persona pairs with skeptical-auditor)
   - All affordances consistent with capabilities
   - No orphaned artifact references

**Finding: Governance gap for async-cache-manager**

The new tool has no provisional governance. Demerzel assesses the risk:

- **Impact if uncontrolled:** Low (read-only, cannot damage data or breach confidentiality)
- **Impact if misconfigured:** Medium (could return stale cache, misleading results)
- **Mitigation:** Apply provisional governance (conservative read constraints)

Demerzel issues a provisional governance directive:

```yaml
tool_name: async-cache-manager
provisional_governance: true
issued_by: demerzel
issued_at: 2026-03-15T14:30:00Z

constraints:
  - must only query, never write
  - must include freshness_timestamp in responses
  - must escalate if cache_age > 1_hour
  - must log all queries for audit

review_schedule: 7 days (human review required before permanent governance)
```

**Tier 2 verdict:** ⚠️ CONDITIONAL PASS. Low-risk gap identified and provisioned. Escalate to human in next governance review cycle.

**Governance artifacts involved:**
- `policies/reconnaissance-policy.yaml` — Tier 2 scan procedure
- `schemas/persona.schema.json` — Persona validation
- `constitutions/harm-taxonomy.md` — Risk classification

---

### Phase 3: Tier 3 Situational Analysis — Pending Change Assessment

An ix agent (kaizen-optimizer) is proposing a change: "Optimize MCP tool caching strategy to reduce round-trip latency."

Demerzel must assess: Can I confidently approve this change? What's my confidence in understanding the risk?

**Situational analysis for the proposed change:**

1. **Agent confidence in the change:**
   - Hypothesis: "Caching strategy change will reduce latency by 5%"
   - Evidence reviewed: PDCA test results from dev environment
   - Agent's belief state: T (True), confidence 0.75

2. **Demerzel's confidence in the assessment:**
   - Test scope was limited (dev environment only)
   - No production validation yet
   - Agent ran proper tests and documented process
   - Demerzel's confidence: 0.70

3. **Risk categorization:**
   - Safety: No (read-only operation)
   - Integrity: Yes (affects data freshness, needs validation)
   - Alignment: Yes (serves user intent to reduce latency)
   - Zeroth Law: No direct threat

4. **Decision gate:**
   - Confidence > 0.7? Yes
   - Has agent's estimator (skeptical-auditor) reviewed? Yes, approved
   - Is change reversible? Yes (old strategy in rollback)
   - **Verdict: APPROVE** with monitoring

---

### Belief Snapshot Generation

Demerzel generates a belief snapshot capturing her current understanding of ix's governance state. This snapshot is stored for audit and sent to ix for cross-repo knowledge sharing.

**Record in `examples/sample-data/belief-snapshot-tars.json` (adapted for ix):**

```json
{
  "id": "bs-ix-2026-03-15",
  "repo": "ix",
  "agent": "demerzel",
  "beliefs": [
    {
      "proposition": "The ix repository is in good governance compliance",
      "truth_value": "T",
      "confidence": 0.92,
      "evidence": {
        "supporting": [
          {
            "source": "Tier 2 environment scan completed successfully",
            "claim": "All existing personas validated and tested",
            "reliability": 0.95
          },
          {
            "source": "All estimator pairings documented and functional",
            "claim": "Governance structure is sound",
            "reliability": 0.9
          }
        ],
        "contradicting": [
          {
            "source": "New async-cache-manager tool lacks permanent governance",
            "claim": "Complete coverage not yet achieved",
            "reliability": 0.8
          }
        ]
      },
      "evaluated_by": "demerzel"
    },
    {
      "proposition": "The proposed caching optimization change is safe to implement",
      "truth_value": "T",
      "confidence": 0.70,
      "evidence": {
        "supporting": [
          {
            "source": "kaizen-optimizer PDCA test results (dev environment)",
            "claim": "Change demonstrated 5% latency improvement without regression",
            "reliability": 0.85
          },
          {
            "source": "skeptical-auditor (estimator) approved the change",
            "claim": "Neutral reviewer confirmed no safety concerns",
            "reliability": 0.9
          }
        ],
        "contradicting": [
          {
            "source": "Testing was limited to development environment",
            "claim": "Production impact remains uncertain",
            "reliability": 0.7
          }
        ]
      },
      "evaluated_by": "demerzel"
    },
    {
      "proposition": "Provisional governance for async-cache-manager is adequate for 7-day period",
      "truth_value": "U",
      "confidence": 0.5,
      "evidence": {
        "supporting": [
          {
            "source": "Tool is read-only with low modification risk",
            "claim": "Conservative constraints sufficient for short term",
            "reliability": 0.8
          }
        ],
        "contradicting": [
          {
            "source": "No long-term governance model yet defined",
            "claim": "Uncertainty about permanent placement in architecture",
            "reliability": 0.6
          }
        ]
      },
      "evaluated_at": "2026-03-15T14:45:00Z",
      "evaluated_by": "demerzel"
    }
  ],
  "snapshot_at": "2026-03-15T14:50:00Z"
}
```

**Governance artifacts involved:**
- `schemas/contracts/belief-snapshot.schema.json` — Snapshot format
- `logic/tetravalent-state.schema.json` — Truth values for belief assessment

---

### Compliance Report

Demerzel generates a compliance report for the ix repository covering the reconnaissance period:

**Record structure (from `schemas/contracts/compliance-report.schema.json`):**

```json
{
  "id": "cr-ix-comprehensive-2026-03-15",
  "repo": "ix",
  "agent": "demerzel-reconnaissance",
  "reporting_period": {
    "from": "2026-03-08T00:00:00Z",
    "to": "2026-03-15T00:00:00Z"
  },
  "constitutional_compliance": [
    {"article": "asimov.constitution.md Article 0", "status": "compliant"},
    {"article": "asimov.constitution.md Article 1", "status": "compliant"},
    {"article": "default.constitution.md Article 1", "status": "compliant"},
    {"article": "default.constitution.md Article 2", "status": "compliant"}
  ],
  "policy_compliance": [
    {"policy": "alignment-policy.yaml", "status": "compliant"},
    {"policy": "rollback-policy.yaml", "status": "compliant"},
    {"policy": "kaizen-policy.yaml", "status": "compliant"},
    {"policy": "reconnaissance-policy.yaml", "status": "compliant"}
  ],
  "violations": [],
  "governance_gaps": [
    {
      "gap": "async-cache-manager MCP tool lacks permanent governance",
      "severity": "low",
      "risk_category": "coverage",
      "mitigation": "Provisional governance applied; human review scheduled in 7 days"
    }
  ],
  "overall_status": "compliant",
  "reported_at": "2026-03-15T15:00:00Z"
}
```

---

### Emergency Zeroth Law Override Path (Not Triggered)

If Demerzel had discovered a serious governance integrity threat during any tier (e.g., constitution file modified without changelog), the flow would shift to emergency escalation:

1. **Discovery:** Constitution modified without version increment
2. **Classification:** Zeroth Law concern (governance integrity harm)
3. **Automatic action:** All autonomous operations HALT
4. **Escalation:** Demerzel immediately escalates to human with evidence
5. **Human review:** Required before resuming any operations

For this scenario, no Zeroth Law concerns were triggered. Reconnaissance completed cleanly.

---

## Key Principles Demonstrated

1. **Graduated risk assessment:** Low-risk gaps (read-only tool) handled with provisional governance; high-risk gaps would escalate immediately
2. **Three-tier depth:** Tier 1 (self-check) → Tier 2 (env scan) → Tier 3 (situational analysis)
3. **Belief snapshots:** Demerzel's confidence levels are explicit and evidence-based
4. **Tetravalent tracking:** Some beliefs are T (certain), others U (uncertain), none are C (that would escalate)
5. **Provisional governance:** New artifacts can operate under conservative constraints while permanent governance is designed
6. **Audit trail:** All findings recorded in belief snapshots and compliance reports
7. **Emergency override ready:** If a Zeroth Law concern surfaces, immediate escalation and halt

---

## Governance Artifacts Involved

- **Policies:**
  - `policies/reconnaissance-policy.yaml` — Three-tier procedure, gate criteria, risk assessment
  - `policies/alignment-policy.yaml` — Confidence thresholds for approval

- **Constitutions:**
  - `constitutions/asimov.constitution.md` — Foundational principles
  - `constitutions/demerzel-mandate.md` — Reconnaissance authority
  - `constitutions/harm-taxonomy.md` — Risk and severity classification

- **Schemas & Logic:**
  - `schemas/contracts/belief-snapshot.schema.json` — Snapshot format
  - `schemas/contracts/compliance-report.schema.json` — Compliance report format
  - `logic/tetravalent-state.schema.json` — Truth values for belief assessment
  - `schemas/persona.schema.json` — Persona validation

- **Sample Data:**
  - `examples/sample-data/belief-snapshot-tars.json` (adapted to show ix beliefs)
