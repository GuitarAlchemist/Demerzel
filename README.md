# Demerzel

> Agent governance: reusable constitutions, personas, alignment policies, multi-valued logic, and behavioral tests for the GuitarAlchemist ecosystem.

Named after [Eto Demerzel](https://asimov.fandom.com/wiki/R._Daneel_Olivaw) — the guardian who shapes policy without wielding direct power.

## Purpose

Demerzel provides the **governance layer** for AI agents across multiple repos:

- **ix** (machine forge) — algorithms, CLI, MCP server
- **tars** (cognition) — reasoning loops, memory, belief graphs
- **ga** (Guitar Alchemist) — music-domain product

This repo is deliberately separate from runtime code. It defines *how agents should behave*, not *how they compute*.

## Structure

```text
Demerzel/
├── constitutions/         # 11-article constitution + Asimov root + Demerzel mandate + harm taxonomy
├── personas/              # 14 persona archetypes (YAML) defining agent roles and voices
├── policies/              # 24 governance policies (alignment, rollback, kaizen, conscience, etc.)
├── logic/                 # Tetravalent logic (T/F/U/C), PDCA state, knowledge state schemas
├── grammars/              # 21 EBNF grammars including IxQL (ML pipelines + MCP orchestration)
├── schemas/               # 23 JSON schemas for personas, beliefs, contracts, and more
├── contracts/             # Galactic Protocol specification for cross-repo communication
├── state/                 # Persistent governance state (beliefs, conscience, streeling, driver)
│   └── streeling/         # Streeling University: 16 departments, 14 courses
├── tests/behavioral/      # 44 behavioral test suites
├── .claude/skills/        # 37 Claude Code skills (driver, recon, teach, research, etc.)
├── templates/             # Integration templates for consumer repos
├── examples/              # Scenario walkthroughs and sample data
├── sources/               # Extraction material (TARS v1 chats, etc.)
└── docs/                  # Architecture docs, design specs, implementation plans
```

## Key Concepts

- **Personas** are not personality theater — they are structured behavioral profiles with capabilities, constraints, and interaction patterns
- **Constitutions** define hard boundaries that override persona preferences
- **Policies** are versioned, auditable rules for alignment, rollback, and self-modification
- **Tetravalent logic** extends boolean True/False with Unknown and Contradictory states
- **Grammars** define formal languages for music theory, governance, and research domains

## Artifact Counts

<!-- README-SYNC: These counts are verified by the driver cycle. Do not edit manually. -->

| Artifact | Count | Source |
|----------|-------|--------|
| Constitutions | 3 + harm taxonomy | `constitutions/` |
| Personas | 14 | `personas/*.persona.yaml` |
| Policies | 27 | `policies/*.yaml` |
| Grammars | 26 | `grammars/*.ebnf` |
| Schemas | 24 | `schemas/*.json` |
| Behavioral tests | 55 | `tests/behavioral/*.md` |
| Skills | 40 | `.claude/skills/*/` |
| Departments | 21 | `state/streeling/departments/` |
| Courses | 14 | `state/streeling/courses/**/en/` |

## Usage

Artifacts in this repo are consumed by agents via:

1. Direct file reference in `.claude/` agent definitions
2. MCP tool that loads governance artifacts at runtime
3. Claude Code hooks that enforce constitutional constraints

## Contributing

When adding governance artifacts:

1. Use the schemas in `schemas/` for validation
2. Every persona must have a behavioral test in `tests/behavioral/`
3. Constitutions are append-only by default — removal requires explicit justification
4. TARS v1 chats are extraction sources, never direct artifacts

## Streeling University

Demerzel hosts [Streeling University](state/streeling/) — a 21-department knowledge framework named after the university on Trantor in Asimov's Foundation series. Departments span mathematics, physics, computer science, cybernetics, audio engineering, data visualization, philosophy, cognitive science, futurology, psychohistory, music, musicology, guitar studies, product management, Guitar Alchemist Academy, and world music. Each department maintains weighted knowledge states and course catalogs governed by the [Streeling policy](policies/streeling-policy.yaml).

## IxQL — ML Pipeline Language

IxQL is a declarative language for composing ML pipelines, defined as an [EBNF grammar](grammars/sci-ml-pipelines.ebnf) and executed by the [ix](https://github.com/GuitarAlchemist/ix) forge. Pipelines are governed artifacts — every step maps to tetravalent conclusions (T/F/U/C) and constitutional checks.

```
(* Research pipeline: governance health scoring *)
governance_state → cleaning → gradient_boosting → f1_score → shap_values

(* Ensemble: combine classifiers with stacking *)
(csv → normalize → random_forest → accuracy)
  + (csv → embedding → transformer → auc_roc)
  => stacking

(* ix pattern: memristive Markov chain *)
streaming_source → lag_features → memristive_markov → time_series_validation → mcp_tool_integration

(* Governed pipeline with constitutional gates *)
data_source → bias_assessment → model → confidence_calibration → explanation_requirement → deployment
```

**11 sections** — data sources, preprocessing, models, evaluation, deployment, governance gates, ix-specific patterns, I/O & reactive patterns, MCP orchestration, evolution hooks. See the [full grammar](grammars/sci-ml-pipelines.ebnf) and the [IxQL Guide](docs/ixql-guide.md) for complex use cases.

## Manifesto for AI-Age Development

The original [Agile Manifesto](https://agilemanifesto.org/) (2001) was written for human teams building software. Demerzel operates in a world where AI agents build software alongside humans. This demands new principles.

### We have come to value:

1. **Governance over heroics** — Agents need constitutional guardrails, not just talented operators. A single brilliant agent without bounds is more dangerous than a mediocre one with good governance.

2. **Compounding over sprinting** — Every cycle should leave the system stronger. Measure compounding dimension (D_c > 1.0), not velocity. A sprint that doesn't compound is waste.

3. **Bounded autonomy over full delegation** — Agents operate within explicit confidence thresholds: ≥0.9 proceed, ≥0.7 note, ≥0.5 confirm, <0.3 stop. Trust is earned through calibrated confidence, not assumed.

4. **Tetravalent truth over binary status** — Not everything is pass/fail. Unknown (U) triggers investigation. Contradictory (C) triggers escalation. Admitting uncertainty is stronger than false certainty.

5. **Observable conscience over hidden judgment** — Agents should track regrets, detect patterns, and learn from mistakes visibly. A conscience without observability is theater.

6. **Reactive governance over periodic review** — Watch → detect → act → compound in real time. Don't wait for the retrospective to discover what IxQL `file_watcher → debounce → pipeline` would have caught immediately.

7. **Constitutional hierarchy over flat rules** — Hard limits (Asimov Laws) override operational policies, which override persona preferences. Not all rules are equal. [Zeroth Law](constitutions/asimov.constitution.md) overrides everything.

8. **Completeness instinct over gap tolerance** — Proactively ask: what's declared but underspecified? What's implied but missing? What's the dual? What would break at scale? ([VSM System 4](https://en.wikipedia.org/wiki/Viable_system_model))

9. **Factory of factories over manual creation** — Don't create things; create systems that create things. [MetaBuild](https://github.com/GuitarAlchemist/Demerzel/blob/master/.claude/skills/demerzel-metabuild/SKILL.md) bootstraps entire departments. [MetaFix](https://github.com/GuitarAlchemist/Demerzel/blob/master/.claude/skills/demerzel-metafix/SKILL.md) fixes the system that allowed the problem.

10. **Human-AI collaboration over human-or-AI** — Neither pure automation nor pure human control. The [HITL pattern](https://github.com/GuitarAlchemist/Demerzel/blob/master/policies/alignment-policy.yaml) defines when to escalate, when to proceed, and when to ask. The human is always in the loop — the question is where.

> *That is, while there is value in the items on the right of the original manifesto, we value the items above as essential for the age of AI agents.*

## Ecosystem

| Repo | Description |
|------|-------------|
| [Demerzel](https://github.com/GuitarAlchemist/Demerzel) | AI governance framework (this repo) |
| [ix](https://github.com/GuitarAlchemist/ix) | Rust ML forge with 40+ MCP tools |
| [tars](https://github.com/GuitarAlchemist/tars) | F# Grammar x ML bridge with 150+ MCP tools |
| [ga](https://github.com/GuitarAlchemist/ga) | .NET Guitar Alchemist chatbot |
| [demerzel-bot](https://github.com/GuitarAlchemist/demerzel-bot) | Discord bot for governance + teaching |

- [GuitarAlchemist Project Board](https://github.com/orgs/GuitarAlchemist/projects/2) — ecosystem roadmap
- [Discussions](https://github.com/orgs/GuitarAlchemist/discussions) — community, governance reports, ideation

## Acknowledgements

- [Isaac Asimov](https://en.wikipedia.org/wiki/Isaac_Asimov) — Foundation series, Laws of Robotics, R. Daneel Olivaw (Demerzel's namesake)
- [Jean-Pierre Petit](https://en.wikipedia.org/wiki/Jean-Pierre_Petit) — Logotron (four-fold logic), Economicon (ERGOL/LOLLI), Bourbakof (Noether's theorem) — scientific comics that inspired tetravalent logic, governance economics, and learning momentum
- [Frederik Pohl](https://en.wikipedia.org/wiki/Frederik_Pohl) — Heechee saga — persona architecture inspiration
- [Anthropic](https://www.anthropic.com/) — Claude AI powering the governance framework
- [Claude Code](https://claude.com/claude-code) — CLI tool used for development
- [Superpowers](https://github.com/anthropics/claude-code-superpowers) — Development methodology skills
