# IxQL Cookbook — Universal Connector Pipelines

IxQL connects every component in the Demerzel ecosystem: skills, code, MCP tools, data, docs, governance, and research. These eight cookbook pipelines demonstrate IxQL as the universal connector language.

Each pipeline is a working `.ixql` file in `examples/ixql/` using syntax from the [IxQL grammar](../grammars/sci-ml-pipelines.ebnf) and the conventions established in `pipelines/`.

## Pipelines

### 1. Skill to Code (`skill-to-code.ixql`)

**Connector:** Governance Skill --> Code Generation

Invokes the governance audit skill (`@gov-audit-001`), identifies coverage gaps (untested policies, orphaned schemas), then generates code artifacts (behavioral tests, schema patches, policy stubs) via cross-model validation. Generated artifacts are schema-validated before being written.

Key IxQL patterns:
- `invoke @handle(args)` — skill invocation via pipeline routing
- `parallel(tars.generate_code(...), mcp__openai_chat__openai_chat(...))` — cross-model code generation
- `tars.validate_schema()` — schema gate before write
- `reversibility_check` + `explanation_requirement` — constitutional gates

**When to use:** After audit reveals gaps that have mechanical fixes.

---

### 2. MCP to Data (`mcp-to-data.ixql`)

**Connector:** MCP Tools --> Structured Data

Orchestrates three real MCP servers (Discord, NotebookLM, context7) in parallel, normalizes their heterogeneous outputs into a common schema, cross-references for themes, and produces beliefs, courses, and research triggers.

Key IxQL patterns:
- `parallel(mcp__plugin_discord_discord__fetch_messages(...), mcp__notebooklm__search_notebooks(...), mcp__plugin_context7_context7__query_docs(...))` — multi-MCP fanout
- `tars.normalize(schema: ...)` — heterogeneous data normalization
- `tars.cross_reference(method: "semantic_similarity")` — cross-source enrichment
- `tars.propose_belief_update(...)` — data-driven belief updates

**When to use:** To gather intelligence from external sources and convert it into actionable governance state.

---

### 3. Governance to Test (`governance-to-test.ixql`)

**Connector:** Policy --> Behavioral Test

Scans all policies for missing or partial behavioral test coverage, extracts testable requirements in Given/When/Then format, generates test suites via cross-model validation, validates them against schemas, and runs a dry audit to verify.

Key IxQL patterns:
- `ix.io.glob("policies/*.yaml")` + `ix.io.glob("tests/behavioral/*-cases.md")` — coverage gap detection
- `tars.extract_requirements(format: "given_when_then")` — requirement extraction
- `tars.check_requirement_coverage(...)` — coverage validation
- `invoke @gov-audit-001(level: 2, focus: ...)` — recursive pipeline invocation for verification

**When to use:** To close the governance loop — every policy should have tests, and this pipeline enforces that.

---

### 4. Research to Course (`research-to-course.ixql`)

**Connector:** Research Question --> Published Course

The full Seldon research cycle: selects a department by weighted scoring, samples a grammar-weighted research question, investigates via three sources (Claude, ChatGPT, NotebookLM), assesses with tetravalent logic, produces a course module, translates to 5 languages, and evolves the grammar if gaps are found.

Key IxQL patterns:
- `ix.ml.score(days_since: 0.4, gaps: 0.3, ...)` + `ix.ml.argmax()` — weighted department selection
- `tars.grammar.sample(grammar, weights, pattern: "investigation")` — grammar-constrained question generation
- `tars.cross_validate(agreement_threshold: 0.7)` — multi-model validation
- Kuhnian reflection: `when conclusion.contradicts(beliefs): { reflect: "anomaly_detected" }`
- Grammar evolution: `ix.io.append("grammars/...", new_production)`

**When to use:** For scheduled or on-demand research cycles that produce durable knowledge.

---

### 5. Cross-Repo Directive (`cross-repo-directive.ixql`)

**Connector:** Demerzel --> ix/tars/ga --> Compliance Report

Detects governance changes via git diff, drafts Galactic Protocol directives (mandate/recommendation/advisory), delivers via GitHub issues, monitors compliance by checking submodule status and issue resolution, and updates cross-repo health beliefs.

Key IxQL patterns:
- `ix.io.git("diff", ref: "HEAD~1..HEAD")` — change detection trigger
- `tars.draft_directive(type: "mandate", from: "Demerzel", to: repo)` — protocol message drafting
- `ix.io.gh("issue create", repo: ...)` — cross-repo GitHub integration
- `tars.synthesize(template: "compliance-report")` — compliance assessment
- `bias_assessment` — Article 10: ensure all repos are checked equally

**When to use:** When governance artifacts change and consumer repos need to update.

---

### 6. Context Budget (`context-budget.ixql`)

**Connector:** Task --> Relevant Artifacts (within token budget)

Implements context engineering (#163) as IxQL: parses a task's intent, discovers candidate artifacts across the ecosystem, scores each on four dimensions (semantic relevance, recency, citation frequency, constitutional weight), then uses a knapsack algorithm to select the best artifacts that fit within the token budget.

Key IxQL patterns:
- `tars.score_relevance(artifact, task_description)` — semantic scoring
- `ix.ml.weighted_sum(semantic: 0.40, recency: 0.20, ...)` — multi-dimensional scoring
- `ix.ml.knapsack(items, capacity, constraints)` — budget-constrained selection
- `tars.summarize(max_tokens: allocated, preserve: [...])` — token-aware summarization
- Feedback loop: `selected -> filter(was_useful) -> weights.boost(0.05)` — learn from outcomes

**When to use:** Before every significant task to assemble the optimal context window.

---

### 7. Meta-Pipeline (`meta-pipeline.ixql`)

**Connector:** Intent --> New Pipeline (factory of factories)

Accepts a pipeline generation request, analyzes existing pipelines for structural patterns, selects the best template, generates a new pipeline via grammar-constrained cross-model generation, validates syntax and artifact references, auto-fixes common issues, registers the pipeline in the registry, and generates a behavioral test stub.

Key IxQL patterns:
- `tars.cluster(method: "structural_similarity")` — pattern discovery across existing pipelines
- `tars.generate_pipeline(request, template, grammar, constraints)` — grammar-constrained generation
- `tars.grammar.validate(content, grammar)` — syntax validation
- `tars.register_pipeline(...)` — pipeline registry update
- `tars.propose_self_modification(target: "pipelines/meta-pipeline.ixql")` — recursive self-improvement

**When to use:** When a new governance or research workflow needs to be formalized as an IxQL pipeline.

---

### 8. Amdahl Optimizer (`amdahl-optimizer.ixql`)

**Connector:** Pipeline --> Optimized Pipeline (via Amdahl's Law)

Applies Amdahl's Law — `Speedup = 1 / (s + (1-s)/N)` — to IxQL pipelines themselves. Parses a target pipeline into a dependency graph, classifies each stage as serial or parallelizable, computes the serial fraction, identifies bottlenecks, generates optimization suggestions (parallel grouping, fan_out conversion, speculative execution), and produces an optimized pipeline variant.

Key IxQL patterns:
- `tars.extract_dependency_graph(nodes: "stages", edges: "data_dependencies")` — structural analysis
- `tars.classify_side_effects(serial_indicators: ["write(", "ix.io.git("])` — side-effect detection
- `ix.ml.knapsack()` — optimization selection under constraints
- `tars.compute_amdahl(serial_cost, total_cost)` — Amdahl's Law computation
- `tars.apply_optimization(pipeline, stage, strategy)` — automated refactoring

**When to use:** To analyze and optimize any IxQL pipeline's parallelism. Amdahl's Law is fundamental — the serial fraction is always the bottleneck.

---

## The Universal Connector Pattern

All eight pipelines share a common structure:

```
Source(s) → Transform → Governance Gate → Output → Compound
```

What makes IxQL universal is that **Source** can be anything (skill, MCP tool, git, file, webhook), **Transform** can be anything (ML model, grammar sampling, cross-model validation), and **Output** can be anything (file, GitHub issue, Discord alert, belief update, new pipeline).

The governance gates (`reversibility_check`, `explanation_requirement`, `bias_assessment`, `confidence_calibration`) and the `compound` phase are the invariant backbone that ensures every pipeline, regardless of its domain, operates within constitutional bounds and learns from its own execution.

## Relationship to Existing Pipelines

| Existing Pipeline | Cookbook Pipeline | Connection |
|---|---|---|
| `driver-cycle.ixql` | `context-budget.ixql` | Driver uses context budget during PLAN phase |
| `conscience-cycle.ixql` | `governance-to-test.ixql` | Conscience signals can trigger test generation |
| `research-cycle.ixql` | `research-to-course.ixql` | Same flow, cookbook version adds MCP data sources |
| `governance-audit.ixql` | `skill-to-code.ixql` | Audit findings feed code generation |
| `metasync.ixql` | `cross-repo-directive.ixql` | MetaSync detects drift, directives fix it |
| `ml-feedback-loop.ixql` | `mcp-to-data.ixql` | ML feedback is one type of MCP data flow |
| `weakness-probe.ixql` | `meta-pipeline.ixql` | Weakness findings can trigger meta-pipeline generation |
| All pipelines | `amdahl-optimizer.ixql` | Any pipeline can be analyzed for parallelization opportunities |

## References

- [IxQL Guide](ixql-guide.md) — Language overview and syntax reference
- [IxQL Grammar](../grammars/sci-ml-pipelines.ebnf) — Full EBNF (14 sections)
- [Existing Pipelines](../pipelines/) — Production governance pipelines
- [Galactic Protocol](../contracts/galactic-protocol.md) — Cross-repo communication spec
- [Context Management Policy](../policies/context-management-policy.yaml) — Context budget rules
- [Seldon Plan Policy](../policies/seldon-plan-policy.yaml) — Research cycle rules
