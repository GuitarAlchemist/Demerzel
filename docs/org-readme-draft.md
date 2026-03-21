# Guitar Alchemist

**AI-native tools for music, machine learning, and agent governance.**

We build composable systems where AI agents operate under principled governance — combining music theory, ML algorithms, neuro-symbolic reasoning, and constitutional alignment into a federated ecosystem.

**7 repos** | **200+ MCP tools** | **14 personas** | **22 policies** | **18 grammars** | **13 departments** | **6 languages** | **41 behavioral tests**

---

## Zero to Hero — Learning Paths

### Path 1: Music Theory (for guitarists)

| Step | What You Learn | Where |
|------|---------------|-------|
| 1 | Play your first chord (Em) | [GAA-001](https://github.com/GuitarAlchemist/Demerzel/blob/master/state/streeling/courses/guitar-alchemist-academy/en/gaa-001-your-first-chord.md) |
| 2 | Chord construction from intervals | [ga](https://github.com/GuitarAlchemist/ga) `ChordExplanationSkill` |
| 3 | Scales and modes | ga `ScaleInfoSkill`, `ModeExplorationSkill` |
| 4 | Voice leading and progressions | ga `HarmonicAnalysisSkill` |
| 5 | Ask the AI chatbot anything | [Discussions Q&A](https://github.com/orgs/GuitarAlchemist/discussions) |

**Concepts:** intervals, chord qualities, scale formulas, modes, voice leading, functional harmony.
**Grammar:** [`music-theory.ebnf`](https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/music-theory.ebnf) | [`music-satriani-advanced.ebnf`](https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/music-satriani-advanced.ebnf)

### Path 2: ML Engineering (for developers)

| Step | What You Learn | Where |
|------|---------------|-------|
| 1 | ML pipeline anatomy | [`sci-ml-pipelines.ebnf`](https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/sci-ml-pipelines.ebnf) |
| 2 | Build pipelines with ix MCP | [ix](https://github.com/GuitarAlchemist/ix) `ix-ml-builder` |
| 3 | Composable Rust ML crates | ix: optimization, search, neural nets, chaos, topology |
| 4 | Grammar-driven ML | tars `WeightedGrammar` + `GrammarDistillation` |
| 5 | Governed deployment | Demerzel governance gates |

**Math:** linear algebra (PCA, neural nets), calculus (backprop), probability (Bayes), information theory (entropy, KL divergence).

### Path 3: Agent Governance (for AI researchers)

| Step | What You Learn | Where |
|------|---------------|-------|
| 1 | Asimov's Laws (Articles 0-5) | [`asimov.constitution.md`](https://github.com/GuitarAlchemist/Demerzel/blob/master/constitutions/asimov.constitution.md) |
| 2 | Operational ethics (Articles 1-11) | [`default.constitution.md`](https://github.com/GuitarAlchemist/Demerzel/blob/master/constitutions/default.constitution.md) |
| 3 | Tetravalent logic (T/F/U/C) | [`logic/`](https://github.com/GuitarAlchemist/Demerzel/tree/master/logic) |
| 4 | 21 governance policies | [`policies/`](https://github.com/GuitarAlchemist/Demerzel/tree/master/policies) |
| 5 | Conscience + meta-compounding | `state/conscience/`, `/demerzel compound` |

### Path 4: Grammar Engineering (for language nerds)

| Step | What You Learn | Where |
|------|---------------|-------|
| 1 | EBNF basics | [`core-scientific-method.ebnf`](https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/core-scientific-method.ebnf) |
| 2 | Weighted productions | `*.weights.json` files |
| 3 | Distillation (traces to rules) | tars `GrammarDistillation` |
| 4 | WoT DSL compilation | tars `WotParser` + `WotCompiler` |
| 5 | Meta-grammar | [`core-meta-grammar.ebnf`](https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/core-meta-grammar.ebnf) |

**Pipeline:** `Demerzel EBNF -> tars WeightedGrammar -> WoT DSL -> MCP execution -> GrammarDistillation -> Evolution`

---

## Most Impactful Features

### 1. Probabilistic Grammar Engine

Every production has a learned weight. Bayesian updates after each use: `P(rule|outcome) = P(outcome|rule) x P(rule) / P(outcome)`. [18 grammars](https://github.com/GuitarAlchemist/Demerzel/tree/master/grammars) evolve through research cycles and tars distillation.

### 2. Tetravalent Logic

Beliefs are T/F/U/C with fuzzy membership `{T:0.7, F:0.0, U:0.2, C:0.1}`. Unknown triggers investigation. Contradictory triggers escalation. `C > 0.3` = escalate. `argmax > 0.8` = sharpen.

### 3. Constitutional Hierarchy

`Asimov Laws (immutable) -> Constitution (11 articles) -> 22 Policies -> 14 Personas`. Higher layers override lower. Every action traces to constitutional basis.

### 4. MCP Federation (200+ Tools)

| Repo | Lang | Tools | Domain |
|------|------|-------|--------|
| [ix](https://github.com/GuitarAlchemist/ix) | Rust | 40+ | ML, math, optimization, GPU |
| [tars](https://github.com/GuitarAlchemist/tars) | F# | 151 | Reasoning, grammars, agents |
| [ga](https://github.com/GuitarAlchemist/ga) | C#/.NET | 50+ | Music theory, chords, scales |

### 5. Streeling University (13 Departments)

| Dept | Grammar | Domain |
|------|---------|--------|
| Music | music-theory.ebnf | Harmony, composition |
| Guitar Studies | music-guitar-technique.ebnf | Technique, fretboard |
| Musicology | music-musicology-analysis.ebnf | History, culture |
| Mathematics | sci-mathematical-proof.ebnf | Proofs, algebra |
| Physics | sci-acoustics-physics.ebnf | Acoustics, vibration |
| Computer Science | sci-algorithms.ebnf | Algorithms, complexity |
| Product Management | gov-product-management.ebnf | Communication + BS detection |
| Futurology | human-futurology.ebnf | Scenarios, horizons |
| Philosophy | human-philosophy.ebnf | Ethics, dialectic |
| Cognitive Science | human-cognitive-science.ebnf | Biases, agent cognition |
| GA Academy | music-satriani-advanced.ebnf | Beginner to Satriani |
| World Music | music-guitar-technique.ebnf | 12 languages, traditions |
| Psychohistory | human-psychohistory.ebnf | Prediction, crisis |

Courses in 6 languages: EN, ES, PT, FR, IT, DE

### 6. BS Detection

Grammar that generates AND detects empty rhetoric across 10 domains. Quantified BS scoring maps to tetravalent logic.

### 7. Grammar Library (18 grammars)

All grammars are [living artifacts](https://github.com/GuitarAlchemist/Demerzel/blob/master/policies/grammar-evolution-policy.yaml) — evolved by research cycles, Bayesian weight updates, and tars distillation.

```
grammars/
├── core-                          # Universal foundations
│   ├── core-meta-grammar.ebnf         # Grammar of grammars (self-governing)
│   ├── core-scientific-method.ebnf    # Research investigation
│   └── core-state-machines.ebnf       # Governance state transitions
├── music-                         # Music domain
│   ├── music-theory.ebnf              # Chords, scales, progressions, voice leading
│   ├── music-guitar-technique.ebnf    # CAGED, fingerpicking, practice routines
│   ├── music-musicology-analysis.ebnf # Periods, styles, comparative study
│   └── music-satriani-advanced.ebnf   # Advanced technique, phrasing, composition
├── sci-                           # Science & engineering
│   ├── sci-mathematical-proof.ebnf    # Proof strategies, reasoning chains
│   ├── sci-acoustics-physics.ebnf     # Vibration, harmonics, resonance
│   ├── sci-algorithms.ebnf            # Paradigms, data structures, complexity
│   └── sci-ml-pipelines.ebnf          # ML pipeline vocabulary, ix patterns
├── gov-                           # Governance & detection
│   ├── gov-blind-spot-detection.ebnf  # Staleness, coverage gaps, meta blind spots
│   ├── gov-bs-generators.ebnf         # 10-domain BS generator + detector v2
│   └── gov-product-management.ebnf    # PM communication + buzzword engine
└── human-                         # Human sciences
    ├── human-philosophy.ebnf          # Ethics, dialectic, thought experiments
    ├── human-cognitive-science.ebnf   # Biases, agent architectures, paradigms
    ├── human-futurology.ebnf          # Scenario planning, signal detection
    └── human-psychohistory.ebnf       # Crisis prediction, power laws, Seldon Plan
```

---

## Community

- [Discussions](https://github.com/orgs/GuitarAlchemist/discussions) — governance reports, ideation, Q&A
- [Project Board](https://github.com/orgs/GuitarAlchemist/projects/2) — ecosystem roadmap
- [Discord](https://github.com/GuitarAlchemist/demerzel-bot) — Demerzel + Seldon bots

## Acknowledgements

- [Isaac Asimov](https://en.wikipedia.org/wiki/Isaac_Asimov) — Foundation, Laws of Robotics, R. Daneel Olivaw
- [Jean-Pierre Petit](https://en.wikipedia.org/wiki/Jean-Pierre_Petit) — Logotron, Economicon, Bourbakof
- [Frederik Pohl](https://en.wikipedia.org/wiki/Frederik_Pohl) — Heechee saga
- [Anthropic](https://www.anthropic.com/) / [Claude Code](https://claude.com/claude-code) / [Superpowers](https://github.com/anthropics/claude-code-superpowers)

**Built With:** Rust | F# | .NET 10 | React | Node.js | WGPU | Claude Code | MCP | NotebookLM | discord.js
