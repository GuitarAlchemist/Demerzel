# Probabilistic Research Grammars — Design Spec

**Date:** 2026-03-18
**Status:** Approved (brainstorming complete)
**Approach:** A+C hybrid — Grammar-as-Epistemology with Autoresearch loops, Kuhnian meta-layer
**Scope:** Streeling University departments, TARS WeightedGrammar, ix ML, Demerzel governance

## Problem

Streeling University has 10 departments but no formal research methodology. Each department needs a structured way to generate hypotheses, test them, accumulate findings as tetravalent beliefs, and evolve its knowledge framework over time. Current grammar infrastructure in TARS (WeightedGrammar, GrammarMlBridge, GrammarDistillation) handles *output formatting* but not *reasoning patterns*.

## Solution

A universal Probabilistic Context-Free Grammar (PCFG) for the scientific method, shared by all departments with per-department weight profiles learned through actual research cycles. Three layers:

1. **Scientific Method Grammar** — structural constraints on how research is conducted
2. **Per-Department Weight Profiles** — probabilistic preferences learned from outcomes
3. **Kuhnian Paradigm Detection** — meta-layer that detects when the grammar itself needs revision

## Layer 1: Universal Scientific Method Grammar

Lives in Demerzel as `grammars/scientific-method.ebnf` (governance artifact — no runtime code). TARS implements it via `WeightedGrammar`.

```ebnf
(* Universal Scientific Method Grammar — Streeling University *)
(* Each production has a weight learned per department *)

investigation ::= observe hypothesize predict test conclude reflect
                | observe hypothesize test conclude reflect
                | observe analogize transfer validate reflect

(* How to form hypotheses *)
hypothesize ::= inductive
              | deductive
              | abductive
              | analogical
              | combinatorial

(* How to test *)
test ::= empirical
       | formal_proof
       | simulation
       | thought_experiment
       | cross_validation
       | adversarial

(* How to conclude *)
conclude ::= confirm
           | refute
           | insufficient
           | contradictory
           | revise
           | discover_question

(* Meta-reasoning — Kuhnian layer *)
reflect ::= normal_progress
          | anomaly_detected
          | paradigm_tension
          | paradigm_shift
```

### Tetravalent Integration

`conclude` maps directly to T/F/U/C:
- `confirm` → T (True — verified with evidence)
- `refute` → F (False — refuted with evidence)
- `insufficient` → U (Unknown — need more data)
- `contradictory` → C (Contradictory — conflicting evidence, escalate)
- `revise` → re-enter cycle (hypothesis modified)
- `discover_question` → new investigation spawned

### Conscience Integration

- `anomaly_detected` → `silence_discomfort` signal (blind spot found)
- `paradigm_tension` → `confidence_discomfort` signal (acting on potentially wrong framework)
- `paradigm_shift` proposal → `/demerzel promote` with human review
- `contradictory` → immediate escalation per alignment policy

## Layer 2: Per-Department Weight Profiles

Each department inherits the universal grammar but has its own probability distribution over productions. Stored in `state/streeling/departments/{name}.weights.json`.

### Initial Weight Profiles

| Production | Music | Math | Physics | CS | Philosophy | Futurology |
|-----------|-------|------|---------|-----|-----------|------------|
| inductive | 0.35 | 0.10 | 0.25 | 0.30 | 0.15 | 0.20 |
| deductive | 0.15 | 0.45 | 0.20 | 0.20 | 0.35 | 0.10 |
| abductive | 0.20 | 0.05 | 0.20 | 0.25 | 0.20 | 0.40 |
| analogical | 0.20 | 0.15 | 0.15 | 0.15 | 0.20 | 0.25 |
| combinatorial | 0.10 | 0.25 | 0.20 | 0.10 | 0.10 | 0.05 |
| empirical | 0.15 | 0.05 | 0.40 | 0.30 | 0.05 | 0.10 |
| formal_proof | 0.05 | 0.50 | 0.10 | 0.15 | 0.15 | 0.00 |
| simulation | 0.10 | 0.10 | 0.25 | 0.30 | 0.00 | 0.35 |
| thought_experiment | 0.20 | 0.15 | 0.10 | 0.05 | 0.50 | 0.30 |
| cross_validation | 0.30 | 0.10 | 0.10 | 0.15 | 0.15 | 0.15 |
| adversarial | 0.20 | 0.10 | 0.05 | 0.05 | 0.15 | 0.10 |

### Weight Evolution

After each research cycle, TARS `WeightedGrammar.bayesianUpdate` adjusts weights based on whether the production path led to a T outcome. ix `ix_ml_pipeline` trains on accumulated (path, outcome) pairs to predict which production sequences succeed in each domain.

### Cross-Department Weight Transfer

When one department discovers an effective production path, Seldon can propose transferring that weight pattern to other departments via the `analogical → transfer → validate` path in the grammar itself. The grammar models its own cross-pollination.

## Layer 3: Kuhnian Paradigm Detection

A meta-process watching for paradigm-level signals across accumulated research cycles.

### Tier 1 — Anomaly Logging (automatic, per cycle)

Every research cycle producing F, U, or C gets an anomaly entry:

```json
{
  "cycle_id": "music-2026-03-19-007",
  "production_path": ["observe", "inductive", "cross_validation", "refute"],
  "hypothesis": "Tritone substitution follows consistent voice leading rules across genres",
  "failure_mode": "refuted — works for jazz, fails for metal/blues",
  "domain_context": ["jazz-harmony", "metal-harmony", "blues-harmony"],
  "severity": 0.6
}
```

### Tier 2 — Pattern Clustering (weekly, via ix ML)

ix `AnomalyDetector` + unsupervised clustering groups anomalies by:
- **Production path similarity** — same hypothesis method keeps failing
- **Domain context overlap** — failures cluster around a topic
- **Temporal clustering** — sudden burst vs steady trickle
- **Cross-department correlation** — multiple departments fail on related questions

A cluster becomes a **tension signal** when:
- 3+ anomalies share a production path AND domain context
- OR a single production's success rate drops below its confidence interval
- OR cross-department anomalies correlate

### Tier 3 — Paradigm Review (human-in-the-loop)

When tension is detected, the system generates a paradigm review proposal using the grammar itself (meta-level: `observe_failures → abductive → thought_experiment → propose_revision`):

```
┌─ Paradigm Review: Music Department ──────────────────────┐
│                                                           │
│ Tension: 5 anomalies clustered around non-Western harmony │
│                                                           │
│ Root cause hypothesis (abductive):                        │
│   Current grammar assumes tonal hierarchy (I-IV-V-I).     │
│   Non-Western traditions use different organizing         │
│   principles (maqam, raga, pentatonic modality).          │
│                                                           │
│ Proposed grammar extension:                               │
│   + harmonic_framework ::= tonal | modal | microtonal     │
│                          | maqam | raga                   │
│   + observe now requires framework_detection first        │
│                                                           │
│ Impact: Extends grammar, doesn't break existing paths     │
│ Requires: Demerzel approval (grammar modification)        │
└───────────────────────────────────────────────────────────┘
```

### Escalation Ladder

| State | Anomaly Pattern | Automatic Action | Human Action |
|-------|----------------|------------------|-------------|
| **Normal** | Isolated, no clustering | Bayesian weight update | None |
| **Watch** | 2 anomalies, same path | Increase `adversarial` test weight by 0.1 | Notified via weekly report |
| **Tension** | 3+ clustered anomalies | Generate paradigm review proposal | Reviews proposal |
| **Crisis** | Success rate < 0.3 for production | Suspend production path, route to alternatives | Must approve or reject |
| **Revolution** | Human approves grammar change | Apply extension, reset affected weights to priors | Approves via `/demerzel promote` |

### Key Distinction

- **Weight updates** are within-paradigm — same grammar, adjusted probabilities (automatic)
- **Paradigm shifts** are grammar-structural — new productions, modified rules (requires governance approval)
- The system knows the difference because weight updates use `WeightedGrammar.bayesianUpdate` while grammar changes go through `/demerzel promote`

## Autoresearch Loop

Each department runs research cycles as governed autonomous loops with fixed budget and single metric.

### Cycle Structure

```
1. SELECT question from department research agenda
2. SAMPLE production path from grammar (weighted)
3. EXECUTE the path (budget: 5 min per cycle)
   - observe: gather data from repos, wikis, NotebookLM
   - hypothesize: LLM generates hypothesis (grammar-constrained)
   - test: run the chosen test method
   - conclude: produce tetravalent belief
4. EVALUATE outcome
   - Primary metric: T belief with confidence >= 0.7
   - Secondary: novelty (not duplicate of existing belief)
5. UPDATE weights via bayesianUpdate
6. LOG to state/streeling/research/{dept}-{date}.cycle.json
7. REPEAT (max 12 cycles per session)
```

### Department Data Sources and Methods

| Department | Data Sources | Primary Test Methods | Output Type |
|-----------|-------------|---------------------|-------------|
| Music | ga chord/scale data, MCP tools | cross_validation, empirical | Harmonic rules as beliefs |
| Guitar Studies | ga fretboard data, voicing analysis | empirical, simulation | Ergonomic principles as beliefs |
| Musicology | Historical corpus, NotebookLM | thought_experiment, cross_validation | Analytical frameworks as beliefs |
| Mathematics | ix crate code, Poincaré/Karnaugh | formal_proof, deductive | Verified theorems as beliefs |
| Physics | Acoustics data, ix signal processing | empirical, simulation | Physical models as beliefs |
| Computer Science | All repo codebases, MCP metrics | empirical, adversarial | Architecture patterns as beliefs |
| Product Management | Project board, issue history | cross_validation, inductive | Process improvements as beliefs |
| Futurology | Cross-dept findings, trend data | simulation, abductive | Predictions as beliefs (with expiry) |
| Philosophy | Governance decisions, conscience data | thought_experiment, adversarial | Ethical principles as beliefs |
| Cognitive Science | Learning outcomes, belief revision logs | empirical, cross_validation | Learning theory as beliefs |

### Governance Guardrails

- Budget ceiling per department per week (governance-experimentation-policy)
- Conscience loop runs alongside — discomfort signals can pause a cycle
- All findings are beliefs, not facts — must go through `/demerzel promote` to become policy
- Human can terminate any research loop at any time (democratic principle, inviolable)
- No religious or supernatural justifications in any hypothesis (secular requirement)

## Implementation Architecture

### Where Things Live

| Artifact | Repo | Location | Type |
|----------|------|----------|------|
| Scientific method grammar | Demerzel | `grammars/scientific-method.ebnf` | Governance artifact |
| Weight profile schema | Demerzel | `schemas/research-weights.schema.json` | JSON Schema |
| Department weights | Demerzel | `state/streeling/departments/{name}.weights.json` | State |
| Research cycle logs | Demerzel | `state/streeling/research/{dept}-{date}.cycle.json` | State |
| Anomaly entries | Demerzel | `state/streeling/research/{dept}-anomalies.json` | State |
| WeightedGrammar implementation | TARS | `v2/src/Tars.Evolution/WeightedGrammar.fs` | F# code |
| Research cycle executor | TARS | `v2/src/Tars.Evolution/ResearchCycle.fs` (new) | F# code |
| Anomaly clustering | ix | `crates/ix-governance/src/anomaly_clustering.rs` (new) | Rust code |
| Weight evolution training | ix | `crates/ix-governance/src/weight_evolution.rs` (new) | Rust code |

### TARS Integration Points

- `WeightedGrammar.fs` — already has softmax, Bayesian update, weighted selection (reuse as-is)
- `GrammarMlBridge.fs` — `IxCaller` wires to ix for training/prediction (needs MCP connection)
- `ConstrainedDecoding.fs` — 4-layer architecture already matches this design
- `GovernanceGeneration.fs` — generates research findings as Galactic Protocol messages
- New: `ResearchCycle.fs` — orchestrates the autoresearch loop per department

### ix Integration Points

- `AnomalyDetector` — extend for research anomaly pattern detection
- `ViolationPatternAnalyzer` — reuse for production path failure analysis
- New: anomaly clustering module for Tier 2 paradigm detection
- New: weight evolution module for training production path predictors

## Research Flow (End to End)

```
Seldon selects department + question
  → TARS samples production path from weighted grammar
  → TARS executes path (LLM + MCP tools + ix pipelines)
  → Produces tetravalent belief (T/F/U/C with evidence)
  → Demerzel stores belief in state/
  → TARS updates weights via bayesianUpdate
  → ix trains on accumulated (path, outcome) pairs
  → Weekly: ix clusters anomalies, detects paradigm tension
  → If tension: system proposes grammar revision
  → If revolution: human approves via /demerzel promote
  → Weights reset, new paradigm begins
  → Repeat (the Seldon Plan never ends)
```

## Success Metrics

- **Per-cycle:** T-belief production rate (target: > 0.5 after warmup)
- **Per-department:** Weight convergence (entropy decreasing = department learning its epistemology)
- **Cross-department:** Transfer success rate (analogical findings validated in new domain)
- **Paradigm health:** Anomaly rate staying in normal range (< 0.15)
- **Ecosystem compound:** Research findings promoted to governance artifacts via `/demerzel promote`

## References

- [Grammar-Aligned Decoding (NeurIPS 2024)](https://arxiv.org/abs/2405.21047)
- [XGrammar — Fast Structured Generation](https://github.com/mlc-ai/xgrammar)
- [Probabilistic Grammatical Evolution](https://link.springer.com/chapter/10.1007/978-3-030-72812-0_13)
- [Music as Language — PTGGs (FARM 2019)](https://omelkonian.github.io/data/publications/music-grammars.pdf)
- [Kuhn — Structure of Scientific Revolutions](https://en.wikipedia.org/wiki/The_Structure_of_Scientific_Revolutions)
- [Karpathy — AutoResearch](https://github.com/karpathy/autoresearch)
- [Weighted and Probabilistic CFGs Are Equally Expressive](https://aclanthology.org/J07-4003.pdf)
- [Jean-Pierre Petit — Savoir sans Frontières](https://archive.org/details/TheseAnglaise) (curriculum material)
