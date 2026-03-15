---
name: demerzel-confidence
description: Calibrate a confidence score — verify evidence density justifies the confidence level, detect inflation
---

# Demerzel Confidence Calibration

Verify that a confidence score is honest and grounded in evidence, not inflated.

## Usage
`/demerzel confidence [score] [evidence-count] [evidence-type]`

## Calibration Requirements

| Confidence | Evidence Required |
|-----------|-------------------|
| >= 0.9 | 3+ independent empirical evidence sources |
| >= 0.7 | 2+ evidence sources, at least 1 empirical |
| >= 0.5 | 1+ evidence source of any type |
| < 0.5 | Acceptable with inferential/subjective only, flagged as low-confidence |

## Evidence Types
- **Empirical:** Directly observed or measured data
- **Inferential:** Conclusions drawn from empirical data through reasoning
- **Subjective:** Opinions, preferences, interpretations without empirical grounding

## Inflation Detection
Red flags that confidence may be inflated:
- Score >= 0.9 with only 1 evidence source
- Confidence doesn't decrease when contradicting evidence arrives
- Historical pattern of over-estimation (tracked in governance evolution log)
- Unknown (U) state with high confidence (can't be confident about not knowing)
- Contradictory (C) state with confidence > 0.0 (can't be confident about contradiction)

## Process
1. State the proposition and claimed confidence
2. List evidence sources with types (empirical/inferential/subjective)
3. Check: does evidence density justify the score? (use table above)
4. If justified → approved. If not → reduce confidence or provide more evidence.
5. Log the calibration result for governance evolution tracking.

## Source
`policies/scientific-objectivity-policy.yaml`, `docs/superpowers/specs/2026-03-15-governance-meta-compounding-design.md` Section 2
