# IxQL Cookbook Pipeline — Behavioral Tests

Tests for the seven cookbook pipelines in `examples/ixql/`.

## Structural Validity Tests

### IXQL-COOK-001: Pipeline files use valid IxQL syntax

**Given** each `.ixql` file in `examples/ixql/`
**When** parsed against `grammars/sci-ml-pipelines.ebnf`
**Then** all pipeline stages, governance gates, and compound phases parse without error

### IXQL-COOK-002: All pipelines include governance gates

**Given** each `.ixql` file in `examples/ixql/`
**When** scanned for governance gate keywords
**Then** each pipeline contains at least one of: `reversibility_check`, `explanation_requirement`, `bias_assessment`, `confidence_calibration`

### IXQL-COOK-003: All pipelines include compound phase

**Given** each `.ixql` file in `examples/ixql/`
**When** scanned for the `compound:` section
**Then** each pipeline contains a compound phase with at least `harvest` and either `promote` or `teach`

### IXQL-COOK-004: All artifact references point to real paths

**Given** each `.ixql` file in `examples/ixql/`
**When** file paths referenced in `ix.io.read()`, `ix.io.glob()`, or `write()` are extracted
**Then** each referenced directory or glob pattern matches at least one real artifact in the repo

### IXQL-COOK-005: All pipelines use binding syntax correctly

**Given** each `.ixql` file in `examples/ixql/`
**When** scanned for binding syntax (`identifier <-`)
**Then** every bound variable is referenced at least once after its binding

## Skill to Code Pipeline Tests

### IXQL-COOK-010: Skill invocation uses valid handle syntax

**Given** `examples/ixql/skill-to-code.ixql`
**When** the `invoke` statement is parsed
**Then** the handle follows `@identifier` format and references `@gov-audit-001`

### IXQL-COOK-011: Generated code passes schema validation before write

**Given** the skill-to-code pipeline
**When** code artifacts are generated
**Then** `tars.validate_schema()` is called before any `write()` operation

### IXQL-COOK-012: Cross-model validation used for code generation

**Given** the skill-to-code pipeline
**When** test generation occurs
**Then** both `tars.generate_code()` and `mcp__openai_chat__openai_chat()` are invoked in parallel with `tars.cross_validate()`

## MCP to Data Pipeline Tests

### IXQL-COOK-020: Three MCP sources invoked in parallel

**Given** `examples/ixql/mcp-to-data.ixql`
**When** the data gathering step executes
**Then** Discord, NotebookLM, and context7 are all invoked within a single `parallel()` block

### IXQL-COOK-021: Heterogeneous outputs normalized to common schema

**Given** MCP outputs from three different sources
**When** normalization step executes
**Then** each source is mapped to a schema in `schemas/`

### IXQL-COOK-022: Belief updates require confidence calibration

**Given** the mcp-to-data pipeline
**When** belief updates are proposed
**Then** `confidence_calibration` gate is applied before persistence

## Governance to Test Pipeline Tests

### IXQL-COOK-030: Coverage gap detection scans all policies

**Given** `examples/ixql/governance-to-test.ixql`
**When** the coverage check runs
**Then** `ix.io.glob("policies/*.yaml")` and `ix.io.glob("tests/behavioral/*-cases.md")` are both queried

### IXQL-COOK-031: Generated tests follow Given/When/Then format

**Given** the governance-to-test pipeline
**When** test cases are generated
**Then** `tars.extract_requirements(format: "given_when_then")` is used

### IXQL-COOK-032: Generated tests are re-validated by audit

**Given** the governance-to-test pipeline
**When** test files are written
**Then** `invoke @gov-audit-001(level: 2)` is called to verify the generated tests

## Research to Course Pipeline Tests

### IXQL-COOK-040: Department selection uses weighted scoring

**Given** `examples/ixql/research-to-course.ixql`
**When** department selection runs
**Then** `ix.ml.score()` with weights summing to 1.0 is followed by `ix.ml.argmax()`

### IXQL-COOK-041: Research uses three independent sources

**Given** the research-to-course pipeline
**When** investigation runs
**Then** `tars.research()`, `mcp__openai_chat__openai_chat()`, and `mcp__notebooklm__search_notebooks()` are all invoked in `fan_out()`

### IXQL-COOK-042: Tetravalent conclusion covers all four states

**Given** the research-to-course pipeline
**When** the conclusion step runs
**Then** all four outcomes are handled: T (confirm), F (refute), C (contradictory), U (insufficient)

### IXQL-COOK-043: Course production only triggers on confirmation

**Given** conclusion with `conclude: "refute"` or `conclude: "insufficient"`
**When** the course production step is reached
**Then** no course is produced (guarded by `when conclusion.conclude == "confirm"`)

### IXQL-COOK-044: Translation targets five languages per multilingual policy

**Given** a confirmed research conclusion
**When** the translation step runs
**Then** translations are produced for es, fr, pt, it, de

## Cross-Repo Directive Pipeline Tests

### IXQL-COOK-050: Directive type matches change severity

**Given** `examples/ixql/cross-repo-directive.ixql`
**When** a breaking change is detected
**Then** directive type is "mandate" with a 7-day deadline

### IXQL-COOK-051: Directives validated against contract schema

**Given** a drafted directive
**When** before delivery
**Then** `tars.validate_schema(schema: "schemas/contracts/directive-contract.schema.json")` is called

### IXQL-COOK-052: Compliance check uses bias assessment

**Given** the compliance monitoring phase
**When** repos are checked
**Then** `bias_assessment` gate ensures all repos are checked equally (Article 10)

### IXQL-COOK-053: Overdue mandates escalate to human

**Given** a mandate directive past its deadline
**When** compliance check shows `verdict: "F"`
**Then** `tars.escalate(to: "human")` is called with Article 6 reference

## Context Budget Pipeline Tests

### IXQL-COOK-060: Four-dimension scoring applied to all candidates

**Given** `examples/ixql/context-budget.ixql`
**When** candidate artifacts are scored
**Then** semantic (0.40), recency (0.20), citation (0.20), and constitutional (0.20) dimensions are all computed

### IXQL-COOK-061: Knapsack respects token budget constraints

**Given** the context budget pipeline
**When** artifact selection runs
**Then** `ix.ml.knapsack()` enforces `max_per_item` (30%) and `response_reserve` (20%) constraints

### IXQL-COOK-062: Constitutional articles always included

**Given** a task referencing specific constitution articles
**When** artifact selection runs
**Then** `must_include` constraint ensures referenced articles are selected regardless of other scores

## Meta-Pipeline Tests

### IXQL-COOK-070: Generated pipeline validated against grammar

**Given** `examples/ixql/meta-pipeline.ixql`
**When** a new pipeline is generated
**Then** `tars.grammar.validate(content, grammar)` is called before registration

### IXQL-COOK-071: Artifact reference validation catches invalid paths

**Given** a generated pipeline referencing `state/nonexistent/path.json`
**When** validation runs
**Then** `ix.io.exists(p)` returns F and the path is flagged

### IXQL-COOK-072: Generated pipeline registered in pipeline registry

**Given** a valid generated pipeline
**When** registration runs
**Then** `state/pipeline-registry.json` is updated with the new handle

### IXQL-COOK-073: Behavioral test stub auto-generated

**Given** a valid generated pipeline
**When** registration completes
**Then** a test file is written to `tests/behavioral/{handle}-pipeline-cases.md`

### IXQL-COOK-074: Self-modification proposal follows Article 9

**Given** the meta-pipeline detects an improvement signal
**When** `tars.propose_self_modification()` is called
**Then** it references Article 9 (Bounded Autonomy) as its gate

## Cross-Cutting Tests

### IXQL-COOK-080: All pipelines log to evolution state

**Given** each cookbook pipeline
**When** the compound phase executes
**Then** a `log ... to "state/evolution/"` entry is present

### IXQL-COOK-081: All pipelines teach findings to Seldon

**Given** each cookbook pipeline
**When** the compound phase executes
**Then** a `teach ... to seldon` entry is present

### IXQL-COOK-082: No pipeline writes to constitutions

**Given** each cookbook pipeline
**When** all `write()` targets are extracted
**Then** no path matches `constitutions/*.md` (constitutions are append-only per policy)

### IXQL-COOK-083: Cookbook docs match pipeline count

**Given** `docs/ixql-cookbook.md`
**When** pipeline sections are counted
**Then** the count matches the number of `.ixql` files in `examples/ixql/`
