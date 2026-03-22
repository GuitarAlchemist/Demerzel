---
name: demerzel-bs-decode
description: Decode BS — run text through structural, content, and rhetorical analysis to produce a FuzzyEnum<BsLevel> score with tetravalent mapping
---

# Demerzel BS Decoder

Analyze text for bullshit density using the BS detection grammar (`grammars/gov-bs-generators.ebnf`). Produces a quantified BS score, per-test breakdowns, rhetorical device inventory, tetravalent mapping, and a clear-speech rewrite when warranted.

## Usage

`/demerzel bs-decode [text or URL]`
`/demerzel bs-decode --file [path]` — decode a file
`/demerzel bs-decode --url [url]` — fetch and decode a URL
`/demerzel bs-decode --self [artifact-path]` — self-check a Demerzel governance artifact

## Pipeline

```
INPUT
  │
  ▼
STRUCTURAL ANALYSIS
  ├─ Specificity Test    → FuzzyEnum<Low|Medium|High>
  ├─ Falsifiability Test → FuzzyEnum<Zero|Low|Medium|High>
  └─ Commitment Test     → FuzzyEnum<Low|Medium|High>
  │
  ▼
CONTENT ANALYSIS
  ├─ Density Test        → FuzzyEnum<Fluff|Mixed|Substance>
  ├─ Factual Density     → FuzzyEnum<None|Sparse|Dense>
  └─ Actionability Test  → FuzzyEnum<None|Vague|Actionable>
  │
  ▼
RHETORICAL ANALYSIS
  ├─ Device Scan         → List of devices from gov-bs-generators.ebnf §11
  └─ Evasion Scan        → List of tactics from gov-bs-generators.ebnf §12
  │
  ▼
SCORING
  │  Weighted combination of all tests
  │  Weights: specificity 0.20, falsifiability 0.15, commitment 0.20,
  │           content_density 0.15, factual_density 0.15, actionability 0.15
  │
  ▼
CLASSIFICATION → FuzzyEnum<BsLevel>
  │  Clear    (score > 0.8)  — real content
  │  Mild     (score 0.6-0.8) — some fluff, substance present
  │  Moderate (score 0.4-0.6) — more style than substance
  │  Serious  (score 0.2-0.4) — almost entirely empty rhetoric
  │  Pure     (score < 0.2)  — could be randomly generated
  │
  ▼
TETRAVALENT MAPPING
  │  Clear/Mild   → T (verified real content)
  │  Moderate     → U (substance unclear, investigate)
  │  Serious/Pure → C (contradictory — sounds meaningful, says nothing)
  │
  ▼
REWRITE (if score ≤ Moderate)
  │  Generate clear-speech alternative using antidote pattern:
  │  claim + evidence + specifics + commitment
  │
  ▼
OUTPUT
```

## Structural Analysis Details

### Specificity Test

Replace the subject with any other subject. If the sentence still makes sense, specificity is LOW.

| Result | Criterion |
|--------|-----------|
| High (1.0) | Statement only applies to the specific subject named |
| Medium (0.5) | Partially specific — some generic, some concrete |
| Low (0.0) | Could apply to any company, product, or person |

### Falsifiability Test

Ask: "What evidence would DISPROVE this claim?" If no evidence could disprove it, falsifiability is ZERO.

| Result | Criterion |
|--------|-----------|
| High (1.0) | Clear criteria for disproof exist |
| Medium (0.5) | Partially testable — some aspects verifiable |
| Low (0.2) | Very difficult to test |
| Zero (0.0) | Unfalsifiable — no evidence could disprove it |

### Commitment Test

Ask: "WHO will do WHAT by WHEN?" Missing any element reduces the score.

| Result | Criterion |
|--------|-----------|
| High (1.0) | All three present: who, what, when |
| Medium (0.5) | Two of three present |
| Low (0.0) | Vague aspiration with no specifics |

## Content Analysis Details

### Density Test

Remove all adjectives, adverbs, and buzzwords. Ratio of remaining content words to total words.

### Factual Density

Count verifiable facts per sentence: numbers, dates, names, measurements, citations.

### Actionability Test

Could someone act on this statement without asking clarifying questions?

## Rhetorical Analysis Details

Scan for devices defined in `grammars/gov-bs-generators.ebnf`:

**Devices (§11):** weasel_words, false_precision, appeal_to_authority, false_dichotomy, circular_reasoning, loaded_language, appeal_to_novelty, appeal_to_tradition, bandwagon, thought_terminating_cliche, strategic_ambiguity

**Evasion Tactics (§12):** deflection, flooding, reframing, credentialism, complexity_shield, future_promise, whataboutism

Report: devices per sentence (rhetorical density) and specific instances found.

## Domain Detection

Match input against BS domain productions in the grammar:

| Domain | Grammar Section |
|--------|----------------|
| Consulting | §1: consulting_bs |
| AI/Tech | §2: ai_bs |
| Academic | §3: academic_bs |
| Motivational | §4: motivational_bs |
| Governance | §5: governance_bs |
| Corporate | §6: corporate_bs |
| Startup/VC | §7: startup_bs |
| Political | §8: political_bs |
| HR/People | §9: hr_bs |
| Marketing | §10: marketing_bs |

## Self-Check Mode

`/demerzel bs-decode --self` runs the decoder against Demerzel's own governance artifacts. This is critical — the grammar itself warns:

> *Self-check: Is Demerzel creating governance artifacts to govern governance artifacts that govern governance? If yes, this IS the BS.*

## FuzzyEnum Output

All test results are FuzzyEnum values, not discrete. A statement might be:

```
specificity: { High: 0.3, Medium: 0.6, Low: 0.1 }
```

This means 60% medium specificity, 30% high, 10% low. The weighted combination produces a FuzzyEnum<BsLevel> with membership across all five levels.

## Example Output

```json
{
  "input": "We are leveraging our next-generation AI platform to deliver unprecedented insights and drive transformative outcomes across the enterprise.",
  "domain_match": "ai_bs (§2), corporate_bs (§6)",
  "structural_analysis": {
    "specificity": {
      "result": { "Low": 0.85, "Medium": 0.15 },
      "reasoning": "Replace 'our platform' with any company — sentence unchanged"
    },
    "falsifiability": {
      "result": { "Zero": 0.7, "Low": 0.3 },
      "reasoning": "No criteria for 'unprecedented' or 'transformative' — unfalsifiable"
    },
    "commitment": {
      "result": { "Low": 0.9, "Medium": 0.1 },
      "reasoning": "No who, no what specifically, no when"
    }
  },
  "content_analysis": {
    "density": {
      "result": { "Fluff": 0.8, "Mixed": 0.2 },
      "reasoning": "Remove 'next-generation', 'unprecedented', 'transformative', 'across the enterprise' — almost nothing remains"
    },
    "factual_density": {
      "result": { "None": 0.95, "Sparse": 0.05 },
      "reasoning": "Zero numbers, dates, names, or verifiable facts"
    },
    "actionability": {
      "result": { "None": 0.9, "Vague": 0.1 },
      "reasoning": "No one could act on this statement"
    }
  },
  "rhetorical_analysis": {
    "devices_found": [
      { "type": "loaded_language", "instances": ["next-generation", "unprecedented", "transformative"] },
      { "type": "strategic_ambiguity", "instances": ["across the enterprise"] },
      { "type": "weasel_words", "instances": ["drive...outcomes"] }
    ],
    "evasion_tactics_found": [],
    "rhetorical_density": 3.0
  },
  "bs_score": {
    "weighted_raw": 0.12,
    "classification": {
      "Pure": 0.65,
      "Serious": 0.30,
      "Moderate": 0.05
    },
    "dominant": "Pure"
  },
  "tetravalent_mapping": "C",
  "tetravalent_reasoning": "Statement sounds meaningful but conveys zero information — contradictory signal",
  "rewrite": "We built [product name]. It [does X] for [Y users]. [Metric] improved by [N%]. Limitations: [list].",
  "clear_speech_template": "claim + evidence + specifics + commitment"
}
```

## Process

1. **Receive input** — text, URL, or file path
2. **Detect domain** — match against 10 BS domain grammars
3. **Run structural analysis** — specificity, falsifiability, commitment (3 FuzzyEnum results)
4. **Run content analysis** — density, factual density, actionability (3 FuzzyEnum results)
5. **Run rhetorical analysis** — device scan, evasion scan (counts + instances)
6. **Compute weighted score** — combine 6 test scores using defined weights
7. **Classify** — map score to FuzzyEnum<BsLevel>
8. **Map to tetravalent** — Clear/Mild→T, Moderate→U, Serious/Pure→C
9. **Rewrite if needed** — if score ≤ Moderate, generate clear-speech alternative
10. **Output** — structured JSON with all results

## Governance

- **Article 1 (Truthfulness)** — the decoder exists to distinguish truth from rhetoric; it must itself be truthful about what it finds
- **Article 5 (Non-Deception)** — BS is institutionalized deception; detecting it upholds non-deception
- **Article 2 (Transparency)** — all scoring weights, test criteria, and reasoning are exposed; the decoder is fully transparent about how it reaches its conclusion
- **Governance self-check** — the decoder can and should be run against Demerzel's own artifacts (governance BS detection, §5)

## Source

`grammars/gov-bs-generators.ebnf` (Universal BS Generator & Detector Grammar v2), `policies/scientific-objectivity-policy.yaml`, `constitutions/default.constitution.md` Articles 1, 2, 5
