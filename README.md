# Demerzel

Agent governance for the GuitarAlchemist ecosystem — reusable constitutions, personas, alignment policies, tetravalent logic, behavioral tests, and cross-repo loop control. Part of a four-repo ecosystem (`Demerzel` + [`ga`](https://github.com/GuitarAlchemist/ga) .NET + [`ix`](https://github.com/GuitarAlchemist/ix) Rust ML + [`tars`](https://github.com/GuitarAlchemist/tars) F# theory validator).

> Named after [Eto Demerzel](https://asimov.fandom.com/wiki/R._Daneel_Olivaw) — the guardian who shapes policy without wielding direct power. This repo is deliberately separate from runtime code: it defines *how agents should behave*, not *how they compute*.

> **Agent-facing canonical docs:** [`CLAUDE.md`](./CLAUDE.md) (breadcrumb-style) and [`AGENTS.md`](./AGENTS.md) (full development guidelines).

## Quick start

```bash
# Consume as a submodule (ga / ix / tars do this)
git submodule add https://github.com/GuitarAlchemist/Demerzel governance/demerzel

# Or use directly as a sibling clone (demerzel-bot does this)
git clone https://github.com/GuitarAlchemist/Demerzel ../Demerzel

# Halt every /auto-optimize loop across the ecosystem
python scripts/demerzel_halt.py halt --reason "Investigating cost burn"
python scripts/demerzel_halt.py status
python scripts/demerzel_halt.py resume
```

## Cross-repo loop control (HALT-ALL)

Demerzel owns the **cross-repo overseer**: a single marker file at `~/.demerzel/HALT-ALL` that every `/auto-optimize` consumer in the ecosystem reads at Step 0 of each cycle. If present, valid, and unexpired, consumers pause until the marker is removed or expires.

- **Producer:** [`scripts/demerzel_halt.py`](./scripts/demerzel_halt.py) — `halt` / `resume` / `status` subcommands; atomic write; schema-validated; archives prior markers to `~/.demerzel/halts/` on resume.
- **Operator skill:** [`.claude/skills/demerzel-halt/SKILL.md`](./.claude/skills/demerzel-halt/SKILL.md) — Claude Code skill wrapping the CLI.
- **Marker schema (v0.1):** `schema_version`, `halted_at`, `halted_by`, `reason`, `scope` (`loops-only` default), `exempt_agents`, `expires_at`.
- **Contract source of truth:** [`ga/docs/contracts/2026-05-16-overseer-halt-marker.contract.md`](https://github.com/GuitarAlchemist/ga/blob/main/docs/contracts/2026-05-16-overseer-halt-marker.contract.md) (consumer side: GA `/auto-optimize` Step 0 reader + operator runbook).

There is **no HTTP / ACP server** in this repo today; the CLI plus operator runbook fill the role of a `POST /halt` endpoint. An ACP server is a Phase 2/3 option, not a shipped surface.

## QA Architect Tribunal

Cross-repo PR-quality governance. Repository-dispatch events from `ga` / `ix` / `tars` land in [`scripts/qa_tribunal_emit.py`](./scripts/qa_tribunal_emit.py), which validates against the vendored [`schemas/contracts/qa-verdict.schema.json`](./schemas/contracts/qa-verdict.schema.json) and emits verdicts to `state/quality/verdicts/<repo>/<pr>/<verdict_id>.json`. The IXQL pipeline [`pipelines/qa-architect-cycle.ixql`](./pipelines/qa-architect-cycle.ixql) is the governed equivalent (Phase 0 skeleton, six stages). Workflow: [`.github/workflows/qa-tribunal.yml`](./.github/workflows/qa-tribunal.yml).

- **Phase 0** (shipped 2026-05-14 — 16): emitter + workflow + schema vendoring.
- **Phase 1** (scheduled 2026-05-18): real `qa_assess_blast_radius` MCP call + `fan_out` over reviewer roles (semantic_judge, regression_replay, gap_analysis, contract_audit), aggregated via `SemanticRouter.AggregateAsync` in GA.

Contract is **v0.1 draft — do not freeze** until Phase 4 of the owning plan.

## Structure

```text
Demerzel/
├── constitutions/         # 5 constitutions — Asimov root + default (14 articles) + Demerzel mandate + epistemic (10 articles) + harm taxonomy
├── personas/              # 17 persona archetypes (YAML) defining agent roles and voices
├── policies/              # 45 governance policies (alignment, rollback, kaizen, conscience, …)
├── logic/                 # Tetravalent logic (T/F/U/C), PDCA state, knowledge state schemas
├── grammars/              # 20 EBNF grammars including IxQL (ML pipelines + MCP orchestration)
├── schemas/               # 38 JSON schemas + 9 contract schemas (incl. qa-verdict, halt-marker)
├── contracts/             # Galactic Protocol + voicing-handle URI + MCP routing
├── pipelines/             # 23 IxQL pipelines (qa-architect-cycle, governance-shake-test, …)
├── state/
│   ├── streeling/         # Streeling University — 23 departments, 21 course tracks
│   └── governance/        # Beliefs, conscience, driver, halt audit
├── scripts/               # demerzel_halt.py, qa_tribunal_emit.py, validate_governance.py
├── tests/behavioral/      # 114 behavioral test suites
├── .claude/skills/        # 60 Claude Code skills (incl. demerzel-halt)
├── templates/             # Integration templates for consumer repos
├── examples/              # Scenario walkthroughs and sample data
├── sources/               # Extraction material (TARS v1 chats, etc.)
└── docs/                  # Architecture docs, design specs, implementation plans, contracts/
```

## Artifact counts

<!-- README-SYNC: These counts are verified by the driver cycle. Do not edit manually. -->

| Artifact | Count | Source |
|----------|-------|--------|
| Constitutions | 5 (incl. epistemic + harm taxonomy) | `constitutions/` |
| Constitutional articles | 14 (default) + 10 (epistemic) + 3 (Asimov root) | `constitutions/*.md` |
| Personas | 17 | `personas/*.persona.yaml` |
| Policies | 45 | `policies/*.yaml` |
| Grammars | 20 | `grammars/*.ebnf` |
| Schemas | 45 + 9 contracts | `schemas/*.json` + `schemas/seldon/*.json` + `schemas/contracts/` |
| Behavioral tests | 114 | `tests/behavioral/*.md` |
| Skills | 69 | `.claude/skills/*/` |
| Streeling departments | 23 | `state/streeling/departments/*.department.json` |
| Course tracks | 21 | `state/streeling/courses/*/` |
| IxQL pipelines | 23 | `pipelines/*.ixql` |
| GitHub workflows | 24 | `.github/workflows/*.yml` |

## Key concepts

- **Personas** are not personality theater — they are structured behavioral profiles with capabilities, constraints, and interaction patterns.
- **Constitutions** define hard boundaries that override persona preferences. Asimov root (precedence: ROOT) overrides everything.
- **Policies** are versioned, auditable rules for alignment, rollback, and self-modification.
- **Tetravalent logic** extends boolean True/False with Unknown and Contradictory. Conclusions in PDCA cycles are typed `T | F | U | C`.
- **Epistemic Constitution** (10 articles) encodes braiding, contradictory ground, teaching-as-validation, viscosity, the Epistemic Tensor, and federated epistemology — drafted via 4-provider brainstorm (2026-03-29).
- **HALT-ALL marker** is the only mandatory cross-repo signal `/auto-optimize` consumers must respect; everything else is advisory.

## Cross-repo connection points

| Consumer | Integration | What it loads |
|---|---|---|
| **ga** | Submodule at `governance/demerzel/` | Schemas + grammars (Loaded). Reads `~/.demerzel/HALT-ALL` at `/auto-optimize` Step 0. |
| **tars** | Submodule at `governance/demerzel/` | Governance schemas → EBNF generation in `v2/grammars/governance/`. |
| **ix** | Submodule at `governance/demerzel/` | `crates/ix-governance/` parses + **enforces** the 11-article constitution; `crates/ix-agent/` exposes 3 governance MCP tools. |
| **demerzel-bot** | Sibling path `../Demerzel/` | 3 constitutions + streeling-policy + gov-bs-generators injected as system prompts; multi-model-orchestration-policy drives LLM routing. |

Most artifacts today are **Defined** or **Loaded**. Full **Enforcement** (constitution actively blocking actions) is shipped only in `ix-governance` — closing the gap in ga / tars requires runtime validation hooks in each consumer, not more Demerzel artifacts.

## Governance health

<!-- README-SYNC: Resilience score is updated by the resilience-dashboard pipeline. -->

| Resilience score | LOLLI detection | Policies | Personas | Tests |
|:---:|:---:|:---:|:---:|:---:|
| 82% (2 gaps) | L0–L4 + Policy + Schema | 45 | 17 | 114 |

**Governance Resilience Score (R)** measures how well the system detects injected poisons — dead bindings, orphaned branches, BS descriptions, unconsumed artifacts, dead computations. Inspired by [Netflix's Chaos Monkey](https://netflix.github.io/chaosmonkey/) (2011) and [Chaos Engineering](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/) (Rosenthal et al., O'Reilly 2020): if Demerzel can't catch deliberate poison, she can't catch accidental LOLLI.

```
R = injections_caught / injections_total
```

| Level | What it detects | Detector |
|-------|----------------|----------|
| L0 file | Files with no consumer | File consumer check |
| L1 pipeline | Cross-pipeline unconsumed outputs | Cross-pipeline scan |
| L2 binding | Dead `let` bindings | `analyzeLolli()` (F# parser) |
| L3 branch | Orphaned fan-out branches | LOLLI lint |
| L4 expression | Dead computations | Transitive closure |
| Policy | BS descriptions, missing consumers | BS decoder, anti-LOLLI policy |
| Schema | Unreferenced schemas | Cross-reference scan |

**Current status:** R = 0.82 (9/11 injections caught). Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles. Remaining gaps: L0/L1 cross-file analysis (requires F# multi-file scanner in TARS). Full history: [`state/resilience/history.json`](state/resilience/history.json). Dashboard: [`pipelines/resilience-dashboard.ixql`](pipelines/resilience-dashboard.ixql).

## Usage

Artifacts are consumed by agents via:

1. **Submodule** — ga, tars, ix include `governance/demerzel/` as a git submodule.
2. **Sibling path** — demerzel-bot reads `../Demerzel/` directly at runtime.
3. **MCP tools** — ix-agent exposes 3 governance tools via JSON-RPC.
4. **Claude Code skills** — 60 skills reference governance artifacts for agent operations.
5. **Claude Code hooks** — enforce constitutional constraints at tool-call time.
6. **Cross-repo halt marker** — `~/.demerzel/HALT-ALL` paused via `demerzel_halt.py` and respected by every `/auto-optimize` consumer.

## CI workflows

24 GitHub workflows under [`.github/workflows/`](./.github/workflows/). Notable:

- [`qa-tribunal.yml`](./.github/workflows/qa-tribunal.yml) — repository-dispatch emitter (Phase 0).
- [`governance-validate.yml`](./.github/workflows/governance-validate.yml) — schema + grammar validation.
- [`agent-blackbox.yml`](./.github/workflows/agent-blackbox.yml) — risk-report cross-model review.
- [`streeling-daily.yml`](./.github/workflows/streeling-daily.yml) — hexavalent course-state evolution.
- [`karpathy-cherny-discipline.yml`](./.github/workflows/karpathy-cherny-discipline.yml) — session-digest + `/correct` discipline enforcement.
- [`demerzel-discussion-responder.yml`](./.github/workflows/demerzel-discussion-responder.yml) — auto-responder for GitHub Discussions across the ecosystem.

## Contributing

When adding governance artifacts:

1. Use the schemas in `schemas/` for validation.
2. Every persona must have a behavioral test in `tests/behavioral/`.
3. Constitutions are append-only by default — removal requires explicit justification.
4. TARS v1 chats are extraction sources, never direct artifacts.
5. Contracts marked `v0.1` are **draft** — only freeze at the explicit Phase 4 milestone of the owning plan.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the full guide and [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## Streeling University

Demerzel hosts [Streeling University](state/streeling/) — a 23-department knowledge framework named after the university on Trantor in Asimov's Foundation series. Departments span mathematics, physics, computer science, cybernetics, audio engineering, data visualization, philosophy, cognitive science, futurology, psychohistory, music, musicology, guitar studies, semiotics, visual computing, network science, information theory, product management, Guitar Alchemist Academy, and world music. Each department maintains weighted knowledge states; 21 course tracks (multilingual: en/de/es/fr/it/…) are governed by the [Streeling policy](policies/streeling-policy.yaml) and evolved daily via [`streeling-daily.yml`](./.github/workflows/streeling-daily.yml).

## IxQL — ML pipeline language

IxQL is a declarative language for composing ML pipelines, defined as an [EBNF grammar](grammars/sci-ml-pipelines.ebnf) and executed by the [ix](https://github.com/GuitarAlchemist/ix) forge. Pipelines are governed artifacts — every step maps to tetravalent conclusions (T/F/U/C) and constitutional checks.

```ixql
(* Research pipeline: governance health scoring *)
governance_state → cleaning → gradient_boosting → f1_score → shap_values

(* Ensemble: combine classifiers with stacking *)
(csv → normalize → random_forest → accuracy)
  + (csv → embedding → transformer → auc_roc)
  => stacking

(* Governed pipeline with constitutional gates *)
data_source → bias_assessment → model → confidence_calibration → explanation_requirement → deployment
```

**17 sections** — pipeline architecture, data sources, preprocessing, models, evaluation, deployment, governance gates, ix-specific patterns, I/O & reactive patterns, MCP orchestration, pipeline identity & routing, evolution hooks, assertions, traceability, auto-distillation & type providers, literate comments, algedonic signals, fractal compound operators. See the [full grammar](grammars/sci-ml-pipelines.ebnf) and the [IxQL Guide](docs/ixql-guide.md).

## Manifesto for AI-age development

The original [Agile Manifesto](https://agilemanifesto.org/) (2001) was written for human teams building software. Demerzel operates in a world where AI agents build software alongside humans. This demands new principles. We value:

1. **Governance over heroics** — guardrails over brilliant operators.
2. **Compounding over sprinting** — `D_c > 1.0`; a sprint that doesn't compound is waste.
3. **Bounded autonomy over full delegation** — calibrated confidence thresholds (≥0.9 proceed, ≥0.7 note, ≥0.5 confirm, <0.3 stop).
4. **Tetravalent truth over binary status** — Unknown triggers investigation; Contradictory triggers escalation.
5. **Observable conscience over hidden judgment** — visible regrets, learnable patterns.
6. **Reactive governance over periodic review** — watch → detect → act → compound in real time.
7. **Constitutional hierarchy over flat rules** — Asimov Laws override operational policies override persona preferences.
8. **Completeness instinct over gap tolerance** — proactively ask what's declared but underspecified.
9. **Factory of factories over manual creation** — [MetaBuild](.claude/skills/demerzel-metabuild/SKILL.md) bootstraps departments; [MetaFix](.claude/skills/demerzel-metafix/SKILL.md) fixes the system that allowed the problem.
10. **Human–AI collaboration over human-or-AI** — HITL pattern defines when to escalate, proceed, or ask.

> *While there is value in the items on the right of the original manifesto, we value the items above as essential for the age of AI agents.*

## Prime Radiant

The [Prime Radiant](https://github.com/GuitarAlchemist/ga/tree/master/ReactComponents/ga-react-components/src/components/PrimeRadiant) is Demerzel's 3D governance visualization — named after [Hari Seldon's device](https://foundation.fandom.com/wiki/Prime_Radiant) for viewing the equations of psychohistory. Built with Three.js + WebGPU, it renders the governance ecosystem as a force-directed graph: 8 node types (constitutions / policies / personas / pipelines / departments / schemas / tests / IxQL), animated particle streams, pulsing health aura, LOLLI decay particles, bloom + starfield. Route: [`/test/prime-radiant`](https://demos.guitaralchemist.com/test/prime-radiant) on the public demo site.

## Ecosystem

| Repo | Description |
|------|-------------|
| [Demerzel](https://github.com/GuitarAlchemist/Demerzel) | AI governance framework (this repo) |
| [ix](https://github.com/GuitarAlchemist/ix) | Rust ML forge with 40+ MCP tools |
| [tars](https://github.com/GuitarAlchemist/tars) | F# Grammar × ML bridge with 150+ MCP tools |
| [ga](https://github.com/GuitarAlchemist/ga) | .NET Guitar Alchemist platform + chatbot |
| [demerzel-bot](https://github.com/GuitarAlchemist/demerzel-bot) | Discord bot for governance + teaching |

- [GuitarAlchemist Project Board](https://github.com/orgs/GuitarAlchemist/projects/2) — ecosystem roadmap.
- [Discussions](https://github.com/orgs/GuitarAlchemist/discussions) — community, governance reports, ideation.

## License

MIT — see [`LICENSE`](./LICENSE). Copyright (c) 2026 GuitarAlchemist.

## Acknowledgements

- [Isaac Asimov](https://en.wikipedia.org/wiki/Isaac_Asimov) — Foundation series, Laws of Robotics, R. Daneel Olivaw (Demerzel's namesake).
- [Jean-Pierre Petit](https://en.wikipedia.org/wiki/Jean-Pierre_Petit) — *Logotron* (four-fold logic), *Economicon* (ERGOL/LOLLI), *Bourbakof* (Noether's theorem) — scientific comics that inspired tetravalent logic, governance economics, and learning momentum.
- [Frederik Pohl](https://en.wikipedia.org/wiki/Frederik_Pohl) — Heechee saga — persona architecture inspiration.
- [Anthropic](https://www.anthropic.com/) — Claude AI powering the governance framework.
- [Claude Code](https://claude.com/claude-code) — CLI tool used for development.
- [Superpowers](https://github.com/anthropics/claude-code-superpowers) — Development methodology skills.
