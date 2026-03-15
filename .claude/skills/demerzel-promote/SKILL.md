---
name: demerzel-promote
description: Propose a governance promotion — elevate operational patterns to policies, or policies to constitutional articles
---

# Demerzel Governance Promotion

Propose elevating a governance pattern through the precedence hierarchy.

## Usage
`/demerzel promote [stage]` — stage is `pattern-to-policy` or `policy-to-constitutional`

## Stage 1: Pattern → Policy (evidence-based)
- **Trigger:** Pattern appears in 3+ PDCA cycles, reconnaissance findings, or compliance decisions
- **Evidence required:** Usage frequency, measurable impact, consistency across repos
- **Process:** Demerzel proposes. Skeptical-auditor reviews evidence. If approved, draft new policy YAML.
- **Authorization:** Demerzel + skeptical-auditor (no human required)

## Stage 2: Policy → Constitutional (human judgment)
- **Trigger:** Policy has been inviolable in practice for sustained period — violations always cause harm
- **Evidence required:** Stage 1 evidence + no exceptions in governance evolution log + consensus that violation = fundamental harm
- **Process:** Demerzel proposes with full evidence package. Human reviews. Constitutional amendment process applies.
- **Authorization:** Human required

## Demotion Path
Unused or counterproductive artifacts can be demoted/deprecated with same evidence requirements and approval levels.

## Evidence Package Format
1. Usage data (citation count, compliance rate from evolution log)
2. Impact assessment (what improves with this governance, what breaks without it)
3. Cross-repo consistency (does the pattern hold across ix, tars, ga?)
4. Counter-evidence (any cases where the pattern was wrong or unhelpful?)

## Source
`docs/superpowers/specs/2026-03-15-governance-meta-compounding-design.md` Section 1
