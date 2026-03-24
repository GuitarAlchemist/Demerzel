# Belief Report: Demerzel (Self-Dogfood)

Generated: 2026-03-23
Artifacts scanned: 255 (38 policies, 14 personas, 79 tests, 30 schemas, 16 grammars, 23 departments, 49 skills, 6 docs-sampled)
Phase 1 slop density: ~18% (low — most docs encode decisions, not descriptions)

---

## Phase 1: Slop Audit Summary

81 doc files totaling ~32K lines were sampled. Key findings:

| Category | Files | Slop Score | Notes |
|----------|-------|------------|-------|
| Architecture docs | 5 | 0.15 (good) | Encode actual decisions and precedence hierarchy |
| Spec docs | 8 | 0.20 (good) | IxQL guide, grammar pipeline — contain real examples |
| Report docs | 6 | 0.25 (ok) | Test reports, lint reports — factual data |
| Article docs | 5 | 0.30 (ok) | Some could substitute any governance project |
| Course READMEs | 21 | 0.10 (good) | Machine-generated but domain-specific |
| State READMEs | 5 | 0.40 (borderline) | Generic descriptions of directory purpose |

**Overall slop density: ~18%.** Below the 60% gate. Proceed to Phase 2.

---

## T -- What We Know (with evidence chains)

### Constitutional Hierarchy

| Artifact | Proposition | Confidence | Key Evidence |
|----------|-------------|------------|--------------|
| asimov.constitution.md | Root of all governance; Articles 0-5 override everything | 0.95 | 63 cross-refs + architecture.md + governance-model.md + all policies cite it |
| default.constitution.md | Operational ethics Articles 1-11 are the enforcement layer | 0.90 | 38 policies cite constitutional_basis from these articles |
| demerzel-mandate.md | Establishes Demerzel as governance coordinator with defined authority | 0.85 | governance-model.md Section 2.2 + 210 cross-refs to demerzel persona |

### Core Policies

| Artifact | Proposition | Confidence | Key Evidence |
|----------|-------------|------------|--------------|
| alignment-policy.yaml | Central policy — most referenced (63 cross-refs), gates all agent actions | 0.90 | Highest cross-ref count of any policy |
| reconnaissance-policy.yaml | Three-tier discovery protocol, actively consumed by recon skill | 0.85 | 26 cross-refs + demerzel-recon skill + 1 dedicated test |
| kaizen-policy.yaml | PDCA continuous improvement, most-tested policy (2 test files) | 0.85 | 21 cross-refs + 2 tests + kaizen-optimizer persona |
| streeling-policy.yaml | Knowledge transfer protocol, governs all 23 departments | 0.90 | 30 cross-refs + 21 courses + 23 departments + dedicated skill |
| autonomous-loop-policy.yaml | Governs Ralph Loops with graduated oversight | 0.85 | 27 cross-refs + demerzel-loop skill + demerzel-drive skill |

### Persona System

| Artifact | Proposition | Confidence | Key Evidence |
|----------|-------------|------------|--------------|
| All 14 personas | Every persona has estimator_pairing, behavioral test, and schema-valid structure | 0.90 | Schema validation + 14/14 tests + 14/14 estimator_pairings |
| skeptical-auditor.persona | Most-referenced persona after demerzel (87 refs) — universal estimator | 0.85 | Used as estimator_pairing across all other personas |
| demerzel.persona | 210 cross-refs, 2 dedicated tests — central governance persona | 0.90 | Highest cross-ref count of any artifact |

### Governance Health

| Artifact | Proposition | Confidence | Key Evidence |
|----------|-------------|------------|--------------|
| Resilience score R=0.82 | 9/11 injections caught across 4 chaos cycles | 0.85 | state/resilience/history.json + 4 documented cycles (0.0->0.64->0.73->0.82) |
| LOLLI detection L0-L4 | Multi-level dead code detection is operational | 0.80 | 12 orphan grammars deleted (commit 68cdb38) + lint report shows 0% dead code |
| 37/38 policies cite constitutional_basis | Near-complete constitutional grounding | 0.90 | Only capability-unity-policy.yaml is missing |

---

## F -- What's Dead (LOLLI remediation candidates)

| Artifact | Evidence of Death | Last Activity | Action |
|----------|------------------|---------------|--------|
| resilience-metric-policy.yaml | 0 external cross-references (only self-referencing) | Recent creation | INVESTIGATE — may be consumed only by pipelines not yet connected |
| state/streeling/departments/metaqa (courses) | Department exists with 0 courses, 0 course content | 2026-03-22 | POPULATE or mark as planned-not-built |
| state/streeling/departments/systems-engineering (courses) | Department exists with 0 courses, 0 course content | 2026-03-22 | POPULATE or mark as planned-not-built |
| 12 deleted grammars | Confirmed dead by LOLLI remediation (commit 68cdb38) | 2026-03-23 | DONE — already deleted |

**Note:** The 12 deleted grammars were properly cleaned up. The remaining 16 grammars all have 2+ cross-references.

---

## U -- What Nobody Knows (THE REAL GAPS)

These are the gold. Each Unknown is a question no source could answer.

### Critical Unknowns

| Artifact | Unanswered Question | Confidence | Why It Matters |
|----------|-------------------|------------|----------------|
| 24 policies with 0 behavioral tests | Are alignment, rollback, self-modification, autonomous-loop, belief-currency, chaos-test, conscience-observability, constitutional-compliance, context-management, continuous-learning, governance-audit, governance-experimentation, grammar-evolution, intuition, meta-audit, ml-governance-feedback, multi-model-orchestration, multilingual, readme-sync, scientific-objectivity, seldon-plan, staleness-detection, visual-critic policies actually enforceable? | 0.3 | 63% of policies (24/38) have zero dedicated behavioral tests. The test suite covers personas well (14/14) but policies poorly (14/38). A policy without tests is an assertion without verification. |
| Consumer repo compliance | Do ix, tars, and ga actually consume Demerzel artifacts? No compliance reports found in state/. | 0.25 | 9 directives issued, 0 compliance responses observed in this repo. Cross-repo governance is aspirational until proven bilateral. |
| 30 schemas with 0 test validators | No schema is validated by the test suite. Are schemas enforced at all, or purely documentary? | 0.30 | Schema validation is claimed but no test file references any schema by name. |
| Automation pipelines (IxQL) | Do the IxQL pipelines in automation-manifest.md actually execute anywhere? | 0.25 | The manifest describes 6+ cron pipelines (Seldon, staleness-scan, etc.) but IxQL has no runtime in this repo. Are these specs for ix/tars to implement, or aspirational? |
| 6 low-reference personas | recovery-agent (6 refs), validator-reflector (6 refs), critical-theorist (7 refs), rational-administrator (7 refs), virtuous-leader (7 refs), communal-steward (8 refs) — are these actively consumed? | 0.35 | These personas exist and have tests, but low cross-reference counts suggest they may be theoretical rather than operational. |

### Moderate Unknowns

| Artifact | Unanswered Question | Confidence | Why It Matters |
|----------|-------------------|------------|----------------|
| Galactic Protocol directives | 9 directives issued, but are they received and acted on by consumer repos? | 0.35 | Protocol is well-specified but evidence of bilateral execution is missing from this repo's state. |
| Department research weights | 23 departments have .weights.json files — are these used by Seldon to prioritize research? | 0.40 | Weight files exist but their consumption path is unclear without ix/tars runtime. |
| CLAUDE.md staleness | Claims 28 policies, 67 tests, 25 schemas — all wrong. Actual: 38 policies, 79 tests, 30 schemas. | 0.50 | CLAUDE.md is loaded into every conversation. Stale counts mean agents start with wrong mental models. |

---

## C -- Contradictions (escalate to humans)

| Artifact | Source A Says | Source B Says | Severity |
|----------|--------------|---------------|----------|
| Grammar count | README.md: "28 EBNF grammars" | Filesystem: 16 grammars (12 deleted in commit 68cdb38) | **HIGH** — README not updated after LOLLI remediation |
| Skill count | README.md: "46 Claude Code skills" | Filesystem: 49 skills (3 added since) | **MEDIUM** — count drift |
| CLAUDE.md policy count | CLAUDE.md: "28 policies" | Filesystem: 38 policies | **HIGH** — 10 policies added without CLAUDE.md update |
| CLAUDE.md test count | CLAUDE.md: "67 behavioral test suites with 100+ test cases" | Filesystem: 79 test files | **MEDIUM** — 12 tests added without update |
| CLAUDE.md schema count | CLAUDE.md: "25 JSON schemas" | Filesystem: 30 schemas | **MEDIUM** — 5 schemas added without update |
| capability-unity-policy.yaml | All policies should cite constitutional_basis (governance-audit-policy requires it) | This policy has no constitutional_basis field | **LOW** — easy fix, but breaks the governance contract |

---

## Metrics Summary

| Truth Value | Count | Percentage |
|-------------|-------|------------|
| T (True) | 14 beliefs | 47% |
| F (False) | 4 beliefs | 13% |
| U (Unknown) | 8 beliefs | 27% |
| C (Contradictory) | 6 beliefs | 20% |

**Overall governance confidence: 0.68** (watch threshold — not yet healthy)

The system's T beliefs are strong where they exist. The danger zone is the 24 untested policies and the stale artifact counts in CLAUDE.md and README.md. The C beliefs are all fixable with a single sync pass.

---

## Recommended Actions

### Immediate (fix contradictions)

1. **Update README.md** grammar count from 28 to 16, skill count from 46 to 49
2. **Update CLAUDE.md** policy count from 28 to 38, test count from 67 to 79, schema count from 25 to 30
3. **Add constitutional_basis** to capability-unity-policy.yaml

### Short-term (close unknowns)

4. **Add behavioral tests for the 24 untested policies** — prioritize alignment, rollback, self-modification, autonomous-loop (highest cross-ref counts)
5. **Populate metaqa and systems-engineering courses** — or explicitly mark as "planned, not built"
6. **Investigate resilience-metric-policy** — determine if it's consumed by pipelines or orphaned

### Medium-term (validate cross-repo)

7. **Establish compliance reporting** — consumer repos should report back to state/
8. **Verify IxQL pipeline execution** — determine which pipelines are specs vs. running
9. **Audit low-reference personas** — determine if recovery-agent, validator-reflector, critical-theorist, rational-administrator, virtuous-leader, communal-steward are consumed outside this repo
