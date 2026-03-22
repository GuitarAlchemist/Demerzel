# tree-sitter-ixql

tree-sitter grammar for **IxQL** — the governed ML pipeline & reactive data flow language.

## Source

- Grammar EBNF: `../grammars/sci-ml-pipelines.ebnf`
- LSP spec: `../docs/superpowers/specs/2026-03-24-ixql-lsp-design.md`
- Issue: GuitarAlchemist/Demerzel#145

## Files

| File | Purpose |
|------|---------|
| `grammar.js` | tree-sitter grammar definition (all 12 sections) |
| `queries/highlights.scm` | Syntax highlighting queries for Neovim, Helix, VS Code |
| `package.json` | npm package + tree-sitter config |

## Grammar Sections

The grammar mirrors the EBNF sections:

1. Pipeline Architecture — `source_file`, `pipeline_statement`, `ensemble_pipeline`
2. Data Sources — `file_source`, `streaming_source_expr`, `governance_state_source`
3. Preprocessing — `cleaning_expr`, `transformation_expr`, `splitting_expr`
4. Models — `model_stage` (supervised, unsupervised, probabilistic, neural, RL)
5. Evaluation — `evaluation_stage` (classification, regression, clustering metrics)
6. Deployment — `serialization_expr`, `serving_expr`, `monitoring_expr`
7. Governance Integration — `governance_gate`, `governance_annotation`, `conclude_expr`
8. ix-Specific Patterns — `karnaugh_optimization`, `memristive_markov`, etc.
9. I/O & Reactive — `reactive_pipeline_statement`, `flow_control_expr`, `output_sink_expr`
10. MCP Orchestration — `mcp_pipeline_statement`, `tool_invocation`, `compound_phase`
12. Assertions — `assertion_statement`, `assertion_pipeline`, `assertion_check`

## Building

```bash
npm install
npm run generate   # runs tree-sitter generate → emits src/parser.c
npm run build      # compiles native binding
npm test           # runs grammar tests in test/corpus/
```

Requires: `tree-sitter-cli` >= 0.23, Node.js >= 18, a C compiler.

## Usage

### Neovim (nvim-treesitter)

```lua
-- In your nvim-treesitter config:
require("nvim-treesitter.parsers").get_parser_configs().ixql = {
  install_info = {
    url = "https://github.com/GuitarAlchemist/tree-sitter-ixql",
    files = { "src/parser.c" },
    branch = "main",
  },
  filetype = "ixql",
}
```

### Helix

Add to `~/.config/helix/languages.toml`:

```toml
[[language]]
name = "ixql"
scope = "source.ixql"
file-types = ["ixql"]
roots = []
comment-token = "--"
grammar = "ixql"

[[grammar]]
name = "ixql"
source = { git = "https://github.com/GuitarAlchemist/tree-sitter-ixql", rev = "main" }
```

## Governance

This grammar is a Demerzel governance artifact.

- **Article 2 (Transparency):** syntax highlighting makes pipeline structure visible
- **Article 7 (Auditability):** governance gates (`bias_assessment`, `reversibility_check`) are first-class highlighted nodes
- **Article 9 (Bounded Autonomy):** governance annotations (`--governed`, `--governed strict`) are parseable and checkable
