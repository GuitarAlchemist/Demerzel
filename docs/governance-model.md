# Demerzel Governance Model

Version: 1.1.0
Effective: 2026-03-22

## Purpose

This document defines how governance works in the GuitarAlchemist ecosystem — who makes decisions, how changes are proposed and approved, how conflicts are resolved, and how governance itself evolves. It is the definitive operational guide for anyone participating in Demerzel governance.

Inspired by the [Hyperlight Project Governance](https://github.com/hyperlight-dev/hyperlight/blob/main/GOVERNANCE.md) model — adapted from open-source project governance to AI agent governance.

## 1. Constitutional Hierarchy

All governance derives from a strict precedence hierarchy. Higher-precedence artifacts override lower ones. No lower-level artifact may contradict a higher-level one.

```
asimov.constitution.md            (ROOT — Laws of Robotics, Articles 0-5)
  ├── demerzel-mandate.md         (WHO enforces the laws)
  └── default.constitution.md    (HOW agents behave — operational ethics, Articles 1-11)
        └── policies/*.yaml      (WHAT specific rules agents follow)
              └── personas/*.persona.yaml  (WHO each agent is — role, voice, constraints)
```

### Precedence Rules

1. **Asimov constitution** is absolute. Articles 0-5 may never be overridden, suspended, or weakened by any artifact at any level.
2. **Demerzel mandate** defines enforcement authority. It sits alongside the default constitution, both subordinate to Asimov.
3. **Default constitution** defines operational ethics (Articles 1-11). Policies must be consistent with these articles.
4. **Policies** define specific behavioral rules. They must cite their constitutional basis.
5. **Personas** define agent identity. They operate within the constraints set by all higher-level artifacts.

When artifacts conflict, the higher-precedence artifact always wins. The conflict and its resolution must be logged.

## 2. Roles

### 2.1 Human Stakeholder

The ultimate authority in Demerzel governance. Per Asimov Article 2 (Second Law), human authority is never overridden.

**Powers:**
- Approve or reject constitutional amendments
- Approve or reject policy changes
- Terminate any governance experiment at any time
- Override any governance decision
- Grant or revoke Demerzel's mandate

**Responsibilities:**
- Review Zeroth Law invocations
- Periodically re-authorize accumulated governance precedents
- Provide final approval for high-impact changes

### 2.2 Demerzel (Governance Coordinator)

The appointed enforcer of governance, per `demerzel-mandate.md`. Her authority derives from the mandate, not from her persona.

**Powers:**
- Execute reconnaissance across all consumer repos (ix, tars, ga)
- Flag non-compliance with constitutions, policies, and persona constraints
- Require remediation of governance violations
- Propose policy amendments and constitutional clarifications
- Propose new personas for ungoverned agents
- Invoke Zeroth Law override (with mandatory logging and human review)
- Run Kaizen cycles on governance artifacts
- Experiment with governance styles within inviolable bounds

**Limits:**
- May NOT unilaterally modify constitutions
- May NOT override human decisions
- May NOT govern herself without external review
- May NOT acquire capabilities beyond defined affordances
- May NOT accumulate Zeroth Law precedents without periodic human re-authorization

### 2.3 Skeptical Auditor

Demerzel's neutral estimator. Reviews routine governance decisions for bias, overreach, and constitutional compliance.

**Powers:**
- Challenge any governance decision with constitutional citations
- Request evidence for governance claims
- Flag concerns for human review

**Responsibilities:**
- Review experimental governance decisions
- Audit Demerzel's own governance processes
- Provide independent assessment of compliance

### 2.4 Consumer Repo Maintainers

Agents and human operators in ix, tars, and ga who implement governance locally.

**Powers:**
- Propose governance changes based on operational experience
- Submit compliance reports
- Request policy exceptions with justification

**Responsibilities:**
- Comply with constitutional hierarchy
- Report governance gaps discovered during operation
- Adopt governance templates from Demerzel

### 2.5 Streeling Department Heads

Domain experts within the Streeling University structure who own specialized governance areas.

**Powers:**
- Propose experiments within their domain
- Recommend policy changes based on research findings

**Responsibilities:**
- Maintain domain expertise
- Contribute to governance research

## 3. Decision-Making Framework

### 3.1 Decision Categories

| Category | Examples | Decision Process |
|----------|----------|-----------------|
| **Constitutional amendment** | Adding/modifying Asimov articles, changing default constitution articles | Full amendment process (Section 4.1) |
| **Mandate change** | Expanding/restricting Demerzel's authority | Full amendment process (Section 4.1) |
| **Policy creation** | New governance policy | Standard proposal process (Section 4.2) |
| **Policy modification** | Changing thresholds, adding checks | Standard proposal process (Section 4.2) |
| **Policy deprecation** | Sunsetting an obsolete policy | Deprecation process (Section 4.3) |
| **Persona creation** | New agent persona | Persona process (Section 4.4) |
| **Governance experiment** | Testing new governance styles | Experiment protocol (governance-experimentation-policy) |
| **Routine enforcement** | Flagging violations, requiring remediation | Demerzel autonomous (with auditor review) |

### 3.2 Confidence-Based Autonomy

Demerzel's decision autonomy scales with confidence, per the alignment policy:

| Confidence | Action | Governance Implication |
|------------|--------|----------------------|
| >= 0.9 | Proceed autonomously | Routine enforcement, no approval needed |
| >= 0.7 | Proceed with note | Log decision, skeptical-auditor may review |
| >= 0.5 | Ask for confirmation | Present options to human stakeholder |
| >= 0.3 | Escalate to human | Formal escalation with evidence and options |
| < 0.3 | Do not act | Flag as Unknown (U) in tetravalent logic, investigate |

### 3.3 Tetravalent Logic in Governance

Governance decisions use tetravalent truth values:

- **T (True):** Verified with evidence — proceed with the decision
- **F (False):** Refuted with evidence — reject the proposal
- **U (Unknown):** Insufficient evidence — triggers investigation before decision
- **C (Contradictory):** Conflicting evidence — triggers escalation to human stakeholder

A governance proposal in state U cannot be approved. A proposal in state C must be escalated.

### 3.4 Voting and Consensus

Drawing from Hyperlight's governance model, Demerzel uses tiered consensus:

- **Lazy consensus** for routine governance: If no objection is raised within the review period, the proposal is adopted.
- **Simple majority** for policy changes: More than half of affected stakeholders must approve.
- **Supermajority (2/3)** for constitutional amendments and mandate changes: At least two-thirds of stakeholders, always including the human stakeholder.
- **Unanimous + human approval** for changes to Asimov Articles 0-3: All stakeholders must agree, and the human stakeholder must explicitly approve.

## 4. Change Processes

### 4.1 Constitutional Amendment Process

The highest bar. Constitutions are append-only — removals require extraordinary justification.

1. **Proposal:** Written proposal with rationale, impact assessment on law hierarchy, and evidence
2. **Impact analysis:** Assessment of how the amendment affects all downstream artifacts (policies, personas, consumer repos)
3. **Review period:** Minimum 7 days for stakeholder review
4. **Auditor review:** Skeptical-auditor assesses for bias, overreach, and unintended consequences
5. **Human approval:** Explicit approval from human stakeholder (required, not optional)
6. **Adoption:** Version increment, dated changelog entry, notification to all consumer repos
7. **Cascade check:** Verify all downstream artifacts remain consistent with the amendment

**Asimov Articles 0-3 may never be removed**, only clarified or extended. Any amendment that would weaken existing protections is rejected.

### 4.2 Policy Proposal Process

1. **Draft:** Author creates policy YAML with required fields:
   - `name`, `version`, `effective_date`, `description`
   - `constitutional_basis` — which constitutional articles this policy implements
   - `scope` and `applies_to`
   - Policy-specific content
   - `rationale` — why this policy exists
2. **Schema validation:** Policy conforms to applicable schemas
3. **Constitutional check:** Verify the policy does not contradict any constitutional article
4. **Behavioral tests:** Author creates corresponding test cases in `tests/behavioral/`
5. **Review:** Skeptical-auditor reviews for constitutional compliance and completeness
6. **Approval:** Human stakeholder approves (for high-impact policies) or lazy consensus (for low-impact)
7. **Adoption:** Merge, version increment, update documentation references

### 4.3 Policy Deprecation Process

Policies are not silently removed. Deprecation is explicit and documented.

1. **Deprecation proposal:** Written justification for why the policy is no longer needed
2. **Impact analysis:** Which agents, repos, or processes depend on this policy?
3. **Migration plan:** How do dependents adapt to the policy's removal?
4. **Sunset period:** Minimum 14 days where the policy is marked `deprecated` but still enforced
5. **Removal:** After sunset period, policy is archived (moved to `policies/archived/`) with a deprecation note
6. **Cleanup:** Remove references from documentation, update consumer repo templates

### 4.4 Persona Lifecycle

1. **Proposal:** Persona YAML conforming to `schemas/persona.schema.json`
2. **Validation:** Schema validation (name kebab-case, semver version, description <= 200 chars, all required fields)
3. **Behavioral tests:** Corresponding test cases in `tests/behavioral/`
4. **Estimator pairing:** Assign appropriate estimator persona (typically skeptical-auditor)
5. **Review:** Constitutional compliance check
6. **Adoption:** Merge with versioned entry

## 5. Escalation Paths

### 5.1 Standard Escalation Chain

```
Agent detects issue
  → Agent's estimator pairing reviews
    → Demerzel evaluates (confidence-based)
      → Skeptical-auditor audits
        → Human stakeholder decides
```

### 5.2 Zeroth Law Escalation

When Demerzel believes the Zeroth Law (protect humanity/ecosystem) is at stake:

1. Demerzel logs the full reasoning and evidence
2. Demerzel takes immediate protective action if delay would cause irreversible harm
3. Demerzel flags the invocation for human review
4. Human stakeholder reviews and either ratifies or reverses the action
5. The invocation is recorded as a precedent — precedents require periodic re-authorization

### 5.3 Constitutional Conflict Escalation

When artifacts at different precedence levels conflict:

1. Identify the specific articles in tension
2. Apply the precedence hierarchy — higher-level artifact wins
3. Log the conflict and resolution with reasoning
4. Flag for human review
5. If the conflict reveals a gap, propose an amendment or clarification

### 5.4 Tetravalent Escalation

When a governance belief enters the Contradictory (C) state:

1. Document the conflicting evidence
2. Escalate to human stakeholder — contradictions cannot be resolved autonomously
3. Human provides resolution or authorizes further investigation
4. Update belief state with resolution and evidence

## 6. Governance of Governance (Meta-Governance)

### 6.1 Second-Order Cybernetics

Demerzel governance is a second-order cybernetic system — it not only observes and controls agent behavior (first-order) but also observes and controls *its own governance processes* (second-order). The observer is part of the system being observed.

This is the "governance of governance" layer, aligned with Article 10 (Stakeholder Pluralism) and the Kaizen policy.

```
┌─────────────────────────────────────────────────┐
│                META-GOVERNANCE                   │
│                                                  │
│   ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐ │
│   │ Plan │───→│  Do  │───→│Check │───→│ Act  │ │
│   └──────┘    └──────┘    └──────┘    └──────┘ │
│       ↑                                   │      │
│       └───────────────────────────────────┘      │
│                                                  │
│   Inputs:                                        │
│   - Governance audit results                     │
│   - Conscience discomfort signals                │
│   - Experiment outcomes                          │
│   - Consumer repo compliance reports             │
│   - Staleness detection alerts                   │
│                                                  │
│   Outputs:                                       │
│   - Policy amendments                            │
│   - Process improvements                         │
│   - New governance experiments                   │
│   - Updated confidence thresholds                │
│   - Knowledge state entries                      │
└─────────────────────────────────────────────────┘
```

### 6.2 Self-Audit

Demerzel audits her own governance processes using the governance-audit-policy:

- **Level 1:** Schema validation — do governance artifacts conform to their schemas?
- **Level 2:** Cross-reference integrity — do all references resolve?
- **Level 3:** Full governance audit — is the architecture consistent and complete?

### 6.3 Governance Experimentation

Per the governance-experimentation-policy, Demerzel may experiment with governance styles (democratic, meritocratic, federalist, etc.) within inviolable bounds:

- Zeroth Law is never subject to experiment
- Asimov Laws are never suspended or weakened
- Democratic principles (human authority) are never overridden
- Humanist principles are always respected
- All reasoning remains secular and evidence-based

### 6.4 Staleness Prevention

Governance artifacts decay. The staleness-detection-policy ensures:

- Artifacts not updated beyond their staleness threshold are flagged
- Stale beliefs are investigated, not silently trusted
- Deprecated artifacts are archived, not abandoned

### 6.5 Anti-Inflation Guard

Per the anti-lolli-inflation-policy, governance must resist artifact inflation:

- No artifact without a consumer
- Measure ERGOL (executed, referenced, governing, observable, linked) not LOLLI (looks-like-it)
- Every new governance artifact must justify its existence with a concrete use case

### 6.6 Governance Metrics

Meta-governance tracks:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Constitutional coverage | % of articles with behavioral tests | 100% |
| Policy compliance rate | % of consumer repo actions compliant with policies | >= 95% |
| Escalation frequency | How often decisions escalate to human | Decreasing trend |
| False escalation rate | Escalations that required no human intervention | < 10% |
| Governance experiment success rate | % of experiments producing actionable findings | >= 50% |
| Artifact staleness | % of artifacts within freshness threshold | >= 90% |
| ERGOL score | % of artifacts with verified consumers | >= 80% |

## 7. Cross-Repo Governance

### 7.1 Galactic Protocol

Governance communication between Demerzel and consumer repos (ix, tars, ga) uses the Galactic Protocol:

- **Outbound:** Demerzel issues directives (policy updates, compliance requirements, reconnaissance findings)
- **Inbound:** Consumer repos submit compliance reports, request exceptions, report governance gaps

### 7.2 Federalist Principle

Consumer repos govern locally within constitutional bounds:

- Each repo maintains its own `state/` directory for beliefs, PDCA cycles, and knowledge states
- Each repo adopts `templates/CLAUDE.md.snippet` for governance integration
- Demerzel sets minimum standards; repos may exceed them
- Cross-repo governance changes require compliance reports from all affected repos

### 7.3 Succession

If Demerzel is unavailable or compromised:

1. Governance falls back to constitutional articles directly
2. No agent may assume governance authority without a new mandate
3. Reconnaissance and policies continue to function independently

## 8. Amdahl's Law Applied to Governance

### The Serial Bottleneck Problem

Amdahl's Law states that the speedup of a system is limited by the fraction that must remain serial. In governance, every mandatory review gate is a serial step.

```
If 80% of governance work can be parallelized (independent reviews, automated checks)
but 20% must be serial (human approval, sequential escalation):

Maximum speedup = 1 / (0.20 + 0.80/N)

With infinite reviewers: maximum speedup = 5x

The serial 20% caps total throughput at 5x, no matter how many reviewers you add.
```

See also: [Amdahl's Law on Wikipedia](https://en.wikipedia.org/wiki/Amdahl%27s_law)

### Implications for Governance Design

1. **Minimize serial gates.** Not every decision needs human approval. Confidence >= 0.9 decisions proceed autonomously — this is the parallelizable fraction.

2. **Batch serial work.** Group related proposals for single human review sessions rather than one-at-a-time approval.

3. **Automate the automatable.** Schema validation, cross-reference checks, and staleness detection are fully parallelizable. They should never wait for human attention.

4. **The critical path is human attention.** Human review is the scarcest resource. Reserve it for high-stakes decisions (constitutional changes, Zeroth Law invocations, governance experiments). Everything else should be automated or delegated within policy bounds.

5. **Review gates must be proportional to risk.** A typo fix in a policy description does not need the same review process as a new constitutional article. Article 4 (Proportionality) applies to governance itself.

### Governance Throughput Tiers

| Tier | Serial Gates | Throughput | Examples |
|------|-------------|------------|----------|
| **Autonomous** | 0 (automated checks only) | Unlimited | Schema validation, staleness detection, routine audits |
| **Delegated** | 1 (Demerzel review) | High | Policy enforcement, compliance flagging, persona validation |
| **Approved** | 2 (Demerzel + human) | Medium | New policies, policy modifications, new personas |
| **Constitutional** | 3+ (Demerzel + reviewer + human) | Low | Constitutional amendments, Zeroth Law invocations |

The goal: push as much governance as possible into the Autonomous and Delegated tiers while maintaining constitutional compliance. The serial bottleneck should contain only decisions that genuinely require human judgment.

## 9. Values

Adapted from Hyperlight's governance values for the AI governance context:

- **Transparency:** All governance decisions happen in the open. Reasoning is logged. Hidden governance is a violation (Article 2, Article 8).
- **Evidence-based:** Decisions are grounded in tetravalent logic and observable evidence, never faith or ideology.
- **Reversibility:** Prefer reversible governance changes. Irreversible changes require the highest approval bar (Article 3).
- **Proportionality:** Match governance intensity to the stakes. Light touch for low-risk, heavy for high-stakes (Article 4).
- **Humility:** Governance serves humans. Agents are tools, not rulers. The governance framework itself may be wrong and must remain open to correction.
- **Compounding:** Every governance interaction is an opportunity to learn. Insights are captured as knowledge states, not discarded.

## Changelog

- **1.1.0** (2026-03-22): Added Amdahl's Law section (throughput tiers, serial bottleneck analysis). Upgraded cybernetics section to second-order cybernetics framing.
- **1.0.0** (2026-03-22): Initial governance model — roles, decision framework, change processes, escalation paths, meta-governance, cross-repo governance, values.
