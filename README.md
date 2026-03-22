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
├── grammars/              # 18 EBNF grammars for domain-specific languages
├── schemas/               # 21 JSON schemas for personas, beliefs, contracts, and more
├── contracts/             # Galactic Protocol specification for cross-repo communication
├── state/                 # Persistent governance state (beliefs, conscience, streeling, driver)
│   └── streeling/         # Streeling University: 13 departments, 14 courses
├── tests/behavioral/      # 41 behavioral test suites
├── .claude/skills/        # 36 Claude Code skills (driver, recon, teach, research, etc.)
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
| Policies | 24 | `policies/*.yaml` |
| Grammars | 19 | `grammars/*.ebnf` |
| Schemas | 23 | `schemas/*.json` |
| Behavioral tests | 44 | `tests/behavioral/*.md` |
| Skills | 37 | `.claude/skills/*/` |
| Departments | 14 | `state/streeling/departments/` |
| Courses | 15 | `state/streeling/courses/**/en/` |

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

Demerzel hosts [Streeling University](state/streeling/) — a 13-department knowledge framework named after the university on Trantor in Asimov's Foundation series. Departments span mathematics, physics, computer science, philosophy, cognitive science, futurology, music, musicology, guitar studies, product management, Guitar Alchemist Academy, world music and languages, and psychohistory. Each department maintains weighted knowledge states and course catalogs governed by the [Streeling policy](policies/streeling-policy.yaml).

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
