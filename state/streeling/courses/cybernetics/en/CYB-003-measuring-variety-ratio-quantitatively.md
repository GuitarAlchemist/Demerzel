# CYB-003: Measuring the Variety Ratio Quantitatively

**Department:** Cybernetics
**Module ID:** CYB-003
**Produced by:** Seldon Plan Cycle cybernetics-2026-03-23-003
**Belief:** T (verified), confidence 0.85
**Date:** 2026-03-23
**Prerequisites:** CYB-001 (VSM Mapping), CYB-002 (Active Dampening)

## Research Question

How can Demerzel measure its variety ratio quantitatively? (Carried from Cycle 001 follow-up questions)

## Summary

Ashby's Law of Requisite Variety states that a regulator must have at least as much variety as the disturbances it faces. This course defines a quantitative framework for measuring Demerzel's variety ratio across three dimensions: behavioral variety (personas), structural variety (grammars), and regulatory variety (policies, constitutions, thresholds). The key formula is V = log2(N) applied per dimension, with the variety ratio R = V_amplifiers / V_attenuators tracked over time to detect governance drift toward over-constraint or under-regulation.

## Ashby's Variety: The Formal Definition

### What Is Variety?

Variety is the number of distinguishable states a system can exhibit. Ashby defined it in *An Introduction to Cybernetics* (1956, Chapter 7) as:

> The variety of a set of elements is the logarithm (base 2) of the number of distinct elements.

**Formula:**

```
V = log2(N)
```

where N is the count of distinguishable states. This is measured in bits — the same unit as Shannon entropy. A system with 8 possible states has variety 3 (bits). A system with 1024 possible states has variety 10 (bits).

### Why Logarithmic?

The log scale matters because variety combines multiplicatively, not additively. If system A has 4 states and system B has 8 states, the combined system has 4 x 8 = 32 states, and log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. This is why we can sum log-varieties across independent dimensions.

### Ashby's Law

```
V(regulator) >= V(disturbance)
```

"Only variety can absorb variety." A governance system that can produce fewer distinct responses than the distinct disturbances it faces will necessarily fail to regulate some of those disturbances.

## Three Dimensions of Variety in Demerzel

Variety in a governance framework is not a single number. Demerzel's variety operates across three independent dimensions:

### Dimension 1: Behavioral Variety (V_B)

**What it measures:** The range of distinct agent behaviors the system can produce.

**Amplifiers:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Goal directedness levels | 4 | 2.00 bits |
| Voice configurations (tone x verbosity x style) | ~27 | 4.75 bits |

**Total behavioral amplification:** V_B_amp = 3.81 + 2.00 + 4.75 = **10.56 bits**

This means Demerzel can produce approximately 2^10.56 = 1,506 distinguishable behavioral configurations.

**Attenuators:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Persona constraints (avg 4 per persona) | 56 | 5.81 bits |
| Estimator pairings (fixed to skeptical-auditor) | 1 | 0 bits |

**Total behavioral attenuation:** V_B_att = 5.81 bits

**Behavioral variety ratio:** R_B = V_B_amp / V_B_att = 10.56 / 5.81 = **1.82**

Interpretation: Behavioral amplification exceeds attenuation by a factor of 1.82. This is healthy — the system has more response capacity than constraint.

### Dimension 2: Structural Variety (V_S)

**What it measures:** The range of distinct structures (question forms, investigation patterns, output formats) the system can generate.

**Amplifiers:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Grammars | 27 | 4.75 bits |
| Grammar productions (avg 12 per grammar) | ~324 | 8.34 bits |
| Streeling departments | 15 | 3.91 bits |

**Total structural amplification:** V_S_amp = 4.75 + 8.34 + 3.91 = **17.00 bits**

**Attenuators:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Grammar evolution gates (T >= 0.7, C < 0.1) | 2 | 1.00 bit |
| Staleness detection (30-day window) | 1 | 0 bits |

**Total structural attenuation:** V_S_att = 1.00 bit

**Structural variety ratio:** R_S = V_S_amp / V_S_att = 17.00 / 1.00 = **17.00**

Interpretation: Structural variety is very high relative to attenuation. This reflects the generative nature of grammars — they are variety amplifiers by design. However, this high ratio also signals a potential concern: insufficient structural constraint could lead to grammar sprawl without quality control.

### Dimension 3: Regulatory Variety (V_R)

**What it measures:** The range of distinct governance decisions the system can make.

**Amplifiers:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Tetravalent logic states | 4 | 2.00 bits |
| Confidence thresholds | 5 | 2.32 bits |
| PDCA states | 4 | 2.00 bits |

**Total regulatory amplification:** V_R_amp = 2.00 + 2.32 + 2.00 = **6.32 bits**

**Attenuators:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Policies | 37 | 5.21 bits |
| Constitutional articles (Asimov + Default) | 17 | 4.09 bits |
| Harm taxonomy categories | 4 | 2.00 bits |

**Total regulatory attenuation:** V_R_att = 5.21 + 4.09 + 2.00 = **11.30 bits**

**Regulatory variety ratio:** R_R = V_R_amp / V_R_att = 6.32 / 11.30 = **0.56**

Interpretation: Regulatory attenuation significantly exceeds amplification. This is **by design** — governance should constrain more than it amplifies. A regulatory ratio below 1.0 means the system is conservative, which aligns with Asimov's Laws (prefer safety over capability).

## The Composite Variety Dashboard

### Summary Table

| Dimension | V_amplifiers | V_attenuators | Ratio R | Assessment |
|-----------|-------------|---------------|---------|------------|
| Behavioral (V_B) | 10.56 bits | 5.81 bits | 1.82 | Healthy — more response capacity than constraint |
| Structural (V_S) | 17.00 bits | 1.00 bit | 17.00 | Caution — high generativity, low constraint |
| Regulatory (V_R) | 6.32 bits | 11.30 bits | 0.56 | By design — governance is conservative |

### Healthy Ranges

Based on Ashby's Law and VSM principles (CYB-001), healthy variety ratios differ by dimension:

| Dimension | Healthy Range | Rationale |
|-----------|---------------|-----------|
| Behavioral | 1.2 -- 3.0 | System needs more behavioral options than constraints, but not unbounded |
| Structural | 2.0 -- 10.0 | Grammars should be generative but gated by quality controls |
| Regulatory | 0.3 -- 0.8 | Governance SHOULD be over-attenuated — this is the conservative principle |

### Current Assessment

- **Behavioral (1.82):** Within healthy range. No action needed.
- **Structural (17.00):** Above healthy range. The 27 grammars with ~324 productions are weakly constrained. Recommendation: add structural quality gates (e.g., grammar test coverage requirements, production usage tracking).
- **Regulatory (0.56):** Within healthy range. The system is conservative but not paralyzed.

## The Disturbance Side: What Must Be Regulated?

The variety ratio only tells half the story. We must also measure the variety of disturbances the system faces:

### External Disturbances (V_D_ext)
| Source | Estimate (N) | Variety V |
|--------|-------------|-----------|
| Consumer repos (ix, tars, ga) | 3 | 1.58 bits |
| Repo state combinations (3 repos x ~10 states each) | 30 | 4.91 bits |
| External environment changes (libraries, APIs, models) | ~100 | 6.64 bits |

**Total external disturbance variety:** V_D_ext = **6.64 bits** (dominated by environment changes)

### Internal Disturbances (V_D_int)
| Source | Estimate (N) | Variety V |
|--------|-------------|-----------|
| Belief state changes per cycle | ~20 | 4.32 bits |
| Policy interactions (37 policies, pairwise) | 666 | 9.38 bits |
| Grammar evolution proposals | ~5 per cycle | 2.32 bits |

**Total internal disturbance variety:** V_D_int = **9.38 bits** (dominated by policy interactions)

### Ashby's Law Check

For governance to be viable:

```
V(regulatory response) >= V(disturbance)
```

- V_R_amp = 6.32 bits
- V_D = max(V_D_ext, V_D_int) = 9.38 bits
- **Gap: 9.38 - 6.32 = 3.06 bits**

This means the regulatory system faces approximately 2^3.06 = 8x more disturbance variety than it can produce response variety. The gap is absorbed by:

1. **Human escalation** — the confidence threshold system routes difficult decisions to humans, borrowing their variety
2. **Constitutional override** — the Asimov Laws collapse complex decisions to binary (safe/unsafe), reducing required variety
3. **PDCA cycling** — sequential processing converts parallel disturbances into manageable queues

These are legitimate variety absorption mechanisms, but the 3-bit gap suggests Demerzel should monitor whether policy-interaction complexity is growing faster than regulatory capacity.

## Measurement Protocol

To track the variety ratio over time, Demerzel should compute the following metrics at each governance cycle:

### Metric 1: Component Counts

```json
{
  "variety_snapshot": {
    "timestamp": "2026-03-23T00:00:00Z",
    "amplifiers": {
      "personas": 14,
      "grammars": 27,
      "grammar_productions": 324,
      "departments": 15,
      "tetravalent_states": 4,
      "confidence_levels": 5,
      "pdca_states": 4
    },
    "attenuators": {
      "policies": 37,
      "constitutional_articles": 17,
      "harm_categories": 4,
      "persona_constraints": 56,
      "evolution_gates": 2
    }
  }
}
```

### Metric 2: Dimensional Ratios

```json
{
  "variety_ratios": {
    "behavioral": 1.82,
    "structural": 17.00,
    "regulatory": 0.56,
    "timestamp": "2026-03-23T00:00:00Z"
  }
}
```

### Metric 3: Trend Detection

Track ratios over consecutive cycles. Alert when:
- Any ratio crosses its healthy range boundary
- The regulatory ratio drops below 0.3 (system paralysis risk)
- The structural ratio exceeds 20.0 (grammar sprawl risk)
- The behavioral ratio drops below 1.0 (under-responsive system)

### Metric 4: Disturbance Growth Rate

Track V_disturbance over time. If disturbance variety grows faster than response variety, Ashby's Law will eventually be violated. This is the governance equivalent of technical debt.

## GPT-4o Cross-Validation

Cross-validation with GPT-4o confirmed:

1. **V = log2(N) is the correct formula** for Ashby variety. Both models agree.
2. **The additive model (summing log-varieties) is valid** for independent dimensions but overly simplistic when components interact. The dimensional separation (behavioral, structural, regulatory) addresses this by treating each dimension independently.
3. **GPT-4o computed a naive composite ratio of -2.8**, treating amplifiers and attenuators as a single additive sum. This is incorrect — negative variety is meaningless (you cannot have fewer than zero distinguishable states). The dimensional model avoids this error.
4. **Both models agree R_regulatory < 1.0 is expected** for a governance system. Governance is inherently attenuating.
5. **The 3-bit regulatory gap** is a novel finding not present in GPT-4o's analysis. It emerges from separately computing disturbance variety, which GPT-4o did not do.

**Cross-validation confidence: 0.85** (T — both models agree on fundamentals; dimensional refinement adds value beyond GPT-4o's analysis)

## Implications for Demerzel

1. **Track variety ratios per cycle** — Add variety snapshot to `state/governance/variety-metrics.json` (or equivalent state file). Monitor dimensional ratios for drift.
2. **Add structural quality gates** — The structural ratio (17.00) is above healthy range. Introduce grammar test coverage requirements and production usage tracking to increase attenuation without reducing generativity.
3. **Monitor the 3-bit regulatory gap** — Policy-interaction complexity (666 pairwise combinations from 37 policies) is the largest source of internal disturbance. As policies grow, this gap will widen quadratically. Consider policy grouping or hierarchical policy organization.
4. **Human escalation is a variety bridge** — The confidence threshold system (Article 6: Escalation) is Demerzel's primary mechanism for absorbing variety that exceeds her regulatory capacity. This is a feature, not a limitation.
5. **Evolve grammar Section 6** — The `sci-cybernetics.ebnf` grammar's requisite variety section (lines 78-82) should be expanded with quantitative measurement productions.

## Connection to CYB-001 and CYB-002

- **CYB-001** identified that Ashby's Law applies to Demerzel and listed variety amplifiers/attenuators qualitatively. CYB-003 makes this quantitative.
- **CYB-001 Recommendation 5** ("Monitor variety ratio") is now operationalized with specific formulas, healthy ranges, and a measurement protocol.
- **CYB-002** addressed System 2 dampening. The deadband and hysteresis mechanisms from CYB-002 are themselves variety attenuators — they reduce the variety of signals flowing through coordination channels. CYB-003's structural attenuation metric should include these when implemented.

## Sources

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Chapter 7: Quantity of Variety; Chapter 11: Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Chapter 6: Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.
- Fathom (2025). Ashby Workshops — AI governance and requisite variety, Independent Verification Organizations (IVO) model.

## Follow-Up Questions for Cycle 004

1. Can the 3-bit regulatory gap be closed by hierarchical policy grouping (reducing pairwise interactions from O(n^2) to O(n log n))?
2. How should grammar production usage be tracked to detect dead productions and inform structural attenuation?
3. What is the information-theoretic relationship between Demerzel's tetravalent logic (T/F/U/C) and Shannon entropy — does U (Unknown) carry more bits than T (True)?

## Cross-References

- Prerequisite: `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Prerequisite: `state/streeling/courses/cybernetics/en/CYB-002-active-dampening-cross-repo-oscillation.md`
- Grammar: `grammars/sci-cybernetics.ebnf` (Section 6, Requisite Variety)
- Department: `state/streeling/departments/cybernetics.department.json`
- Policy: `policies/seldon-plan-policy.yaml`
