# IxQL Language Server — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** ix repo (new `ix-lsp` crate), VS Code extension, Claude Code integration
**Issue:** #117
**Depends on:** #103 (ix CLI — provides `ix-ixql` parser crate)

## Overview

A Language Server Protocol (LSP) implementation for IxQL that provides grammar-aware autocomplete, real-time pipeline validation, governance gate suggestions, and completeness instinct feedback. Built on the `ix-ixql` parser crate designed in #103.

Primary consumer: Claude Code (MCP tool integration). Secondary: VS Code extension.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LSP framework | tower-lsp | Async Rust, well-maintained, used by rust-analyzer |
| Parser reuse | `ix-ixql` crate | Single parser, shared AST — no desync between CLI and LSP |
| Transport | stdio (VS Code) + MCP (Claude Code) | stdio is LSP standard; MCP enables Claude Code native integration |
| Incremental parsing | tree-sitter adapter (future) | pest for correctness now; tree-sitter for incremental perf later |
| Governance awareness | Read Demerzel artifacts at startup | LSP loads constitutions/policies for gate suggestions |

## Section 1: Crate Architecture

```
crates/ix-lsp/
  src/
    lib.rs                # LSP server setup
    main.rs               # Binary entry point (stdio transport)
    server.rs             # tower-lsp LanguageServer implementation
    capabilities/
      completion.rs       # Autocomplete
      diagnostics.rs      # Real-time error/warning reporting
      hover.rs            # Hover documentation
      goto.rs             # Go to definition (source → stage definition)
      code_action.rs      # Quick fixes and governance gate insertion
      semantic_tokens.rs  # Syntax highlighting tokens
      inlay_hints.rs      # Inline type annotations and confidence hints
    governance/
      loader.rs           # Load Demerzel governance artifacts
      suggestions.rs      # Suggest governance gates based on pipeline context
      completeness.rs     # Completeness instinct: what's missing?
    state.rs              # Document state management
    config.rs             # LSP configuration
  Cargo.toml
```

### Dependencies

```toml
[dependencies]
ix-ixql = { path = "../ix-ixql" }
tower-lsp = "0.20"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
dashmap = "6"           # Concurrent document store
```

## Section 2: LSP Capabilities

### 2.1 Diagnostics (Real-Time Validation)

Triggered on every document change. Uses `ix-ixql::parse()` + `ix-ixql::validate()`.

**Error categories:**

| Severity | Category | Example |
|----------|----------|---------|
| Error | Parse error | `csv → → random_forest` (double arrow) |
| Error | Unknown stage | `csv → frobnicate → rf` (no such stage) |
| Error | Type mismatch | `csv → kmeans → f1_score` (unsupervised → classification metric) |
| Error | Unresolved binding | `when T >= 0.8: deploy(result)` where `result` not bound |
| Warning | Missing evaluation | Pipeline has model but no evaluation stage |
| Warning | Ungoverned deploy | Deploy stage without any governance gate |
| Warning | Fan-out without merge | Fan-out branches never converge |
| Info | Governance suggestion | "Consider adding bias_assessment before deploy" |
| Info | Completeness hint | "Pipeline has no compound phase — learnings will be lost" |

### 2.2 Autocomplete

Context-aware completions at cursor position. Uses `ix-ixql::completions()`.

**Completion triggers:**

| Context | Completions Offered |
|---------|-------------------|
| After `→` | Valid next stages based on current output type |
| After `(` | Parameters for the current stage |
| After `when` | `T`, `F`, `U`, `C` + comparison operators |
| After `--governed` keyword | Governance gate names |
| Start of line | `csv`, `json`, `parquet`, `watch`, `webhook`, `cron`, data source names |
| Inside `fan_out(` | Pipeline starters |
| After `compound:` | `harvest`, `promote`, `teach`, `update_evolution_log` |
| Inside string `"..."` | File paths (relative), department names, model names |
| After `mcp.` | Known MCP tool names from catalog |

**Completion detail:**

Each completion includes:
- `label` — stage name
- `detail` — input/output types
- `documentation` — description from grammar + governance implications
- `insertText` — full snippet with parameter placeholders

Example:
```
Label: random_forest
Detail: (tabular) → (predictions)
Documentation: Supervised classifier. Section 4 of IxQL grammar.
  Governance: consider bias_assessment after this stage.
Insert: random_forest(n_estimators: ${1:100}, max_depth: ${2:10})
```

### 2.3 Hover

Shows documentation and governance context when hovering over a stage or keyword.

**Hover content structure:**

```markdown
### random_forest
**Type:** Model (Supervised / Classification)
**Input:** tabular data
**Output:** predictions + probabilities
**Grammar:** Section 4, classification_model production

**Governance:**
- Article 10: Consider bias_assessment for fairness
- Article 2: explanation_requirement available (SHAP)

**Parameters:**
- `n_estimators` (int, default: 100)
- `max_depth` (int, default: 10)
- `min_samples_split` (int, default: 2)
```

### 2.4 Code Actions

Quick fixes and governance insertions.

| Action | Trigger | Effect |
|--------|---------|--------|
| Insert governance gate | Warning: ungoverned deploy | Insert `→ bias_assessment → reversibility_check` before deploy |
| Add compound phase | Warning: no compound | Append `→ compound: harvest findings` |
| Fix type mismatch | Error: wrong metric | Replace metric with compatible one |
| Add evaluation | Warning: model without eval | Insert `→ evaluation(f1_score)` after model |
| Wrap in fan-out | Select 2+ stages | Wrap selection in `fan_out(...)` |
| Add when gate | Cursor on stage | Wrap stage in `when T >= 0.7:` |

### 2.5 Semantic Tokens

Syntax highlighting token types:

| Token Type | Maps To |
|-----------|---------|
| `keyword` | `when`, `compound`, `fan_out`, `fan_in`, `parallel` |
| `function` | Stage names: `csv`, `normalize`, `random_forest` |
| `operator` | `→`, `->`, `=>`, `+`, `<-`, `>=`, `<=` |
| `variable` | Binding names: `result`, `features` |
| `string` | `"quoted strings"` |
| `number` | Numeric literals |
| `comment` | `-- line comments` |
| `type` | `T`, `F`, `U`, `C` (tetravalent values) |
| `namespace` | MCP tool namespaces: `tars.`, `ix.`, `context7.` |

### 2.6 Inlay Hints

Inline annotations shown between stages:

```
csv("data.csv") → normalize → random_forest → f1_score
                 ^tabular     ^tabular        ^predictions  ^metric:0.87
```

- Type annotations after each `→` showing the data shape
- Confidence annotations on `when` clauses
- Gate count annotations on `--governed` pipelines

## Section 3: Governance Awareness

### Governance Artifact Loading

At startup, the LSP loads Demerzel governance artifacts:

```rust
pub struct GovernanceContext {
    pub articles: Vec<Article>,         // From constitutions/
    pub policies: Vec<Policy>,          // From policies/
    pub confidence_thresholds: Thresholds, // From alignment-policy.yaml
    pub gate_definitions: Vec<GateDef>,   // Available governance gates
}
```

Configuration in LSP settings:
```json
{
  "ixql.governance.demerzelPath": "../Demerzel",
  "ixql.governance.autoSuggest": true,
  "ixql.governance.level": "standard"
}
```

### Completeness Instinct

The LSP implements a "completeness instinct" — proactive suggestions for what's missing in a pipeline, based on the completeness-instinct-policy:

1. **No evaluation after model** — "Add evaluation to measure model quality"
2. **No governance before deploy** — "Add governance gates for constitutional compliance"
3. **No compound phase** — "Add compound to capture learnings"
4. **Model without preprocessing** — "Consider data cleaning before training"
5. **Fan-out without strategy** — "Branches need a merge strategy"
6. **MCP call without error handling** — "Add retry or circuit_breaker for resilience"
7. **Reactive source without debounce** — "Add debounce to prevent event storms"

These appear as blue info diagnostics, not errors.

## Section 4: Claude Code Integration

### MCP Tool Registration

The LSP exposes itself as an MCP tool for Claude Code:

```json
{
  "name": "ixql",
  "description": "IxQL pipeline authoring assistant",
  "tools": [
    {
      "name": "ixql.validate",
      "description": "Validate IxQL source and return diagnostics",
      "inputSchema": {
        "type": "object",
        "properties": {
          "source": { "type": "string", "description": "IxQL source code" }
        }
      }
    },
    {
      "name": "ixql.complete",
      "description": "Get completions at a position in IxQL source",
      "inputSchema": {
        "type": "object",
        "properties": {
          "source": { "type": "string" },
          "line": { "type": "integer" },
          "character": { "type": "integer" }
        }
      }
    },
    {
      "name": "ixql.explain",
      "description": "Explain an IxQL pipeline execution plan",
      "inputSchema": {
        "type": "object",
        "properties": {
          "source": { "type": "string" },
          "governed": { "type": "boolean", "default": false }
        }
      }
    },
    {
      "name": "ixql.suggest_governance",
      "description": "Suggest governance improvements for a pipeline",
      "inputSchema": {
        "type": "object",
        "properties": {
          "source": { "type": "string" }
        }
      }
    }
  ]
}
```

This allows Claude Code agents to programmatically validate and improve IxQL pipelines during authoring.

### Dual Transport

```
┌─────────────┐     stdio      ┌──────────┐
│  VS Code    │◄──────────────►│          │
│  Extension  │                │  ix-lsp  │
└─────────────┘                │  server  │
                               │          │
┌─────────────┐     MCP/HTTP   │          │
│ Claude Code │◄──────────────►│          │
│   Agent     │                └──────────┘
└─────────────┘
```

The server listens on stdio by default (for VS Code) and optionally on HTTP for MCP tool calls:

```bash
# VS Code mode (default)
ix-lsp

# MCP mode (for Claude Code)
ix-lsp --transport mcp --port 3100

# Both
ix-lsp --also-listen mcp:3100
```

## Section 5: VS Code Extension

Minimal VS Code extension that wraps the LSP:

```
ixql-vscode/
  package.json          # Extension manifest
  src/
    extension.ts        # Activation, LSP client setup
  language-configuration.json
  syntaxes/
    ixql.tmLanguage.json  # TextMate grammar for basic highlighting
```

**package.json highlights:**

```json
{
  "name": "ixql",
  "displayName": "IxQL — ML Pipeline Language",
  "description": "Language support for IxQL governed ML pipelines",
  "categories": ["Programming Languages"],
  "contributes": {
    "languages": [{
      "id": "ixql",
      "extensions": [".ixql"],
      "aliases": ["IxQL"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "ixql",
      "scopeName": "source.ixql",
      "path": "./syntaxes/ixql.tmLanguage.json"
    }],
    "configuration": {
      "title": "IxQL",
      "properties": {
        "ixql.governance.demerzelPath": {
          "type": "string",
          "default": "",
          "description": "Path to Demerzel governance repo"
        },
        "ixql.governance.autoSuggest": {
          "type": "boolean",
          "default": true,
          "description": "Suggest governance gates automatically"
        },
        "ixql.governance.level": {
          "type": "string",
          "enum": ["minimal", "standard", "strict"],
          "default": "standard"
        }
      }
    }
  }
}
```

## Section 6: Performance Considerations

| Concern | Mitigation |
|---------|-----------|
| Parse on every keystroke | Debounce 100ms; only re-parse changed region |
| Large .ixql files | pest is fast enough for files <10K lines; tree-sitter migration if needed |
| Governance artifact loading | Load once at startup, file-watch for changes |
| MCP tool catalog | Cache catalog, refresh on `ixql.refreshToolCatalog` command |
| Completion latency | Target <50ms; pre-compute completion sets per context type |

## Constitutional Basis

- **Article 2 (Transparency)** — LSP makes pipeline behavior visible before execution
- **Article 7 (Auditability)** — governance suggestions create auditable pipeline designs
- **Article 8 (Observability)** — real-time diagnostics expose pipeline health
- **Article 9 (Bounded Autonomy)** — governance gate suggestions keep pipelines within constitutional bounds

## Open Questions

1. **tree-sitter for incremental parsing?** pest re-parses the full file. For large files, tree-sitter would give incremental updates. Recommendation: start with pest (shared with CLI), add tree-sitter adapter if performance requires it.
2. **Snippet library?** Should the LSP include a library of common pipeline snippets? Recommendation: yes, bundled from `examples/` in Demerzel.
3. **Live execution preview?** Should the LSP execute pipelines in a sandbox and show preview results? Recommendation: out of scope for v1; add as `ix-lsp --preview` in v2.
