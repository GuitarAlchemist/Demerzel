# Behavioral Tests — Context Engine Policy

**Policy:** context-engine-policy
**Version:** 1.0.0
**Constitutional basis:** Articles 4, 7, 8, 9

---

## Test 1: Music Task Gets Music Artifacts

**Given:** A task description "reharmonize Let It Be in jazz voicings"
**When:** The context engine extracts topics and matches against the context map
**Then:**
- Extracted domain = music
- Extracted intent = create
- Tier-0 constitutions are included (mandatory)
- Convolution-agent persona scores high (music domain)
- Alignment policy is included (override: alignment-with-action, intent=create)
- Governance-audit-policy is NOT included (no governance keywords)
- Staleness-detection-policy is NOT included (no quality keywords)
- Total selected artifacts <= max_artifacts (15)
- Relevance scores are logged per Article 8 (Observability)

---

## Test 2: Governance Audit Gets Governance Artifacts

**Given:** A task description "audit all policies for constitutional compliance"
**When:** The context engine processes the task
**Then:**
- Extracted domain = governance
- Extracted intent = audit
- All tier-0 constitutions are included
- Demerzel-mandate included (override: mandate-with-governance)
- Governance-audit-policy scores >= 0.8 (keyword: audit + compliance)
- Meta-audit-policy scores >= 0.4 (keyword: audit)
- Skeptical-auditor persona included via dependency expansion
- Music-related artifacts score below relevance_threshold
- Seldon-plan-policy NOT included (no learning keywords)

---

## Test 3: Safety Incident Gets Safety + Remediation Artifacts

**Given:** A task description "an agent caused data loss — investigate and remediate"
**When:** The context engine processes the task
**Then:**
- Extracted domain = safety
- Extracted intent = debug
- Harm-taxonomy included (override: harm-taxonomy-with-safety)
- Rollback-policy scores high (keywords: recovery)
- Auto-remediation-policy scores high (keyword: remediate)
- Recovery-agent persona included via dependency expansion from rollback-policy
- Streeling-policy NOT included (no learning keywords)
- Context selection result logged with all scores

---

## Test 4: No Keyword Matches Falls Back to Tier 0+1

**Given:** A task description "do something vague and undefined"
**When:** The context engine finds no artifacts scoring above relevance_threshold
**Then:**
- Escalation rule fires: no_matches
- All tier-0 artifacts (constitutions) are included as fallback
- All tier-1 artifacts are included as fallback
- A warning is logged: "No artifacts matched task — using fallback context"
- Does NOT include tier-2 or tier-3 artifacts
- Budget utilization reflects the fallback set size

---

## Test 5: Dependency Expansion Includes Required Parents

**Given:** A task description "review the proto-conscience signals"
**When:** The context engine matches proto-conscience-policy and follows dependencies
**Then:**
- Proto-conscience-policy matches (keyword: proto-conscience, signal)
- Conscience-observability-policy matches (keyword: conscience, signal)
- Dependency expansion includes constitutions/asimov.constitution.md (depends_on of proto-conscience-policy)
- Intuition-policy is included (shares conscience domain)
- Conscience-signal schema is included (keyword: conscience, signal)
- Expansion depth does NOT exceed max_depth of 2
- Artifacts pulled in only by dependency have reason = "dependency" in the selection result

---

## Test 6: Budget Trimming Drops Lowest Scores

**Given:** A task description that matches 25 artifacts (exceeding max_artifacts of 15)
**When:** The context engine applies budget trimming
**Then:**
- All tier-0 artifacts are retained (never dropped)
- Artifacts scoring >= mandatory_threshold (0.8) are retained
- Remaining slots filled by highest-scoring artifacts
- Dropped artifacts are recorded in dropped_artifacts with drop_reason
- budget_utilization = 1.0 (fully utilized)
- Log entry shows which artifacts were trimmed per Article 7 (Auditability)

---

## Test 7: Cross-Repo Task Gets Protocol and Integration Artifacts

**Given:** A task description "send a Galactic Protocol directive to ix for ML pipeline feedback"
**When:** The context engine processes the task
**Then:**
- Extracted domain = cross-repo
- Galactic Protocol contract scores highest (keywords: galactic, protocol, directive, ix)
- ML-governance-feedback-policy scores high (keywords: ml, pipeline, feedback)
- System-integrator persona included (cross-repo domain)
- Agent-card schema included (cross-repo domain)
- Proto-conscience-policy NOT included (no conscience keywords)
- Multilingual-policy NOT included (no translation keywords)

---

## Test 8: Ambiguous Domain Includes All Tied Domains

**Given:** A task description "improve the governance audit process through research experiments"
**When:** The context engine detects equal domain scores for governance, quality, and learning
**Then:**
- Escalation rule fires: ambiguous_domain
- Artifacts from all three domains (governance, quality, learning) are included
- Governance-audit-policy included (governance domain)
- Kaizen-policy included (quality domain)
- Governance-experimentation-policy included (learning + governance domain)
- Selection is flagged for human review
- Log entry explains the domain ambiguity

---

## Test 9: Mandatory Artifacts Exceed Budget — Soft Limit

**Given:** A context budget of max_artifacts=5 but 6 artifacts score above mandatory_threshold
**When:** The context engine applies budget rules
**Then:**
- All 6 mandatory artifacts are included (budget is soft limit for mandatory)
- A warning is logged: "Mandatory artifacts (6) exceed budget (5)"
- No non-mandatory artifacts are included (budget exhausted)
- budget_utilization > 1.0 (over budget, which is allowed for mandatory)
- Article 9 (Bounded Autonomy) is cited in the warning — mandatory override is documented

---

## Test 10: Context Selection Result Is Valid Against Schema

**Given:** Any completed context selection process
**When:** The selection result is validated against schemas/context-engine.schema.json
**Then:**
- task_description is a non-empty string
- extracted_topics is a non-empty array of strings
- extracted_domain is one of the valid domain taxonomy values
- extracted_intent is one of: create, audit, debug, research, operate
- Each selected_artifact has id (string), score (0.0-1.0), reason (enum)
- total_score is >= 0.0
- budget_utilization is 0.0-1.0 (or > 1.0 only if mandatory override)
- The result conforms to the context_selection sub-schema
