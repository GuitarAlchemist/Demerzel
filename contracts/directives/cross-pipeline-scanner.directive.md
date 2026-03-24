# Directive: Cross-Pipeline Dependency Scanner

**Directive ID:** DIR-2026-03-23-002
**Type:** implementation
**From:** Demerzel (Governance)
**To:** tars (F# implementation)
**Priority:** P1
**Issued:** 2026-03-23
**Compliance Deadline:** 2026-04-06

## Context

The Shake-MetaFix resilience program has driven governance R from 0.00 to 0.82 across four chaos cycles (chaos-001 through chaos-004). Nine of eleven chaos injections are now caught. The **two remaining gaps** are both at the L0/L1 level and require **runtime F# code** — multi-file analysis that cannot be expressed as governance artifacts alone (Demerzel's no-runtime-code constraint).

**Resilience history:** `state/resilience/history.json` (chaos-004 record)
**Current R score:** 0.82 (9/11 caught)
**Target R score:** 1.00 (11/11 caught)

### Gap A — L0: Orphaned File Detection

- **Chaos injection:** `chaos-test.ixql` — a file with no consumer anywhere in the pipeline ecosystem
- **Expected detector:** File consumer check — scan all `.ixql` files and flag any file that is never referenced (imported, sourced, or consumed) by another file
- **Current status:** `spec-only` — the detection logic is designed in cross-pipeline-deps.ixql Step 5 but is not executable

### Gap B — L1: Unconsumed Pipeline Output Detection

- **Chaos injection:** A pipeline writes to a path that no other pipeline reads from
- **Expected detector:** Cross-pipeline scan — build a graph of all pipeline read/write paths and flag writes with zero downstream consumers
- **Current status:** `spec-only` — the detection logic is designed in cross-pipeline-deps.ixql Step 4 but is not executable

## Directive

tars SHALL implement a cross-pipeline dependency scanner as an F# analysis pass with the following components:

### Phase 1 — Dependency Graph Construction

- Create a module `Tars.IxqlAnalysis.CrossPipeline` (or extend the existing `IxqlParser` project).
- **File discovery:** Recursively scan a configurable root directory for all `.ixql` files.
- **Reference extraction:** For each `.ixql` file, extract:
  - All `source` / `import` / `from` references to other files
  - All `read` / `load` / `consume` path references (pipeline inputs)
  - All `write` / `emit` / `produce` / `alert` path references (pipeline outputs)
  - All `teach` target references
- **Graph construction:** Build a directed dependency graph where:
  - Nodes are `.ixql` files and named paths
  - Edges represent producer→consumer relationships

### Phase 2 — Gap Detection

Using the dependency graph, implement two detection functions:

#### `detectOrphanedFiles` (L0)

- Identify all `.ixql` files that have **zero incoming edges** — no other file references them as a source, import, or dependency.
- Exclude explicitly marked entry points (files with `@entry` or `@root` annotations, or files listed in a configurable allowlist).
- Return a list of `OrphanedFileResult` records containing:
  - `filePath: string` — the orphaned file
  - `reason: string` — "no consumer found across N scanned files"
  - `suggestion: string` — "add a consumer, mark as @entry, or remove"

#### `detectUnconsumedOutputs` (L1)

- Identify all pipeline output paths (write/emit/produce targets) that have **zero downstream consumers** — no other pipeline reads from that path.
- Exclude explicitly marked terminal outputs (paths annotated with `@terminal` or `@sink`, e.g., alert endpoints, external API calls).
- Return a list of `UnconsumedOutputResult` records containing:
  - `producerFile: string` — the file writing to the path
  - `outputPath: string` — the unconsumed path
  - `reason: string` — "output path has zero consumers across N scanned pipelines"
  - `suggestion: string` — "add a consumer pipeline, mark as @terminal, or remove"

### Phase 3 — Integration

- **CLI entry point:** Add a subcommand or function callable from the TARS CLI:
  ```
  tars analyze cross-pipeline --root <directory> [--allowlist <file>]
  ```
  Output: JSON array of `OrphanedFileResult` and `UnconsumedOutputResult` records.
- **Exit code:** Return non-zero if any orphaned files or unconsumed outputs are detected (enables CI gating).
- **MCP tool (optional):** Expose as an MCP tool `cross_pipeline_scan` for interactive use.

### Phase 4 — Chaos Regression Tests

- Create regression tests in `tests/Tars.IxqlAnalysis.Tests/CrossPipelineTests.fs` that reproduce the exact chaos injections:
  - **L0 regression:** Add a `chaos-test.ixql` file to a test fixture directory with no consumers. Assert `detectOrphanedFiles` flags it.
  - **L1 regression:** Add a pipeline that writes to `unconsumed/output/path`. Assert `detectUnconsumedOutputs` flags it.
  - **Negative tests:** Verify that properly connected files and consumed outputs are NOT flagged.
  - **Allowlist tests:** Verify that `@entry`/`@terminal` annotations and allowlist entries suppress false positives.

## Compliance Requirements

1. **Unit tests:** All phases MUST include tests in `tests/Tars.IxqlAnalysis.Tests/`.
2. **Constitution compliance:** Detection results MUST include actionable suggestions per Article 2 (Transparency) — every flagged item explains why and what to do.
3. **Auditability:** Per Article 7, the scanner MUST log the total files scanned, edges found, and detection results.
4. **Bounded autonomy:** Per Article 9, the scanner MUST NOT modify or delete files — it is read-only analysis that reports findings.
5. **Governance integration:** Results MUST be serializable as JSON compatible with the resilience history format, enabling automated R score updates.

## Acceptance Criteria

- [ ] `detectOrphanedFiles` catches the L0 chaos injection (chaos-test.ixql with no consumer)
- [ ] `detectUnconsumedOutputs` catches the L1 chaos injection (write to unconsumed path)
- [ ] Both detectors produce zero false positives on the current well-formed pipeline set
- [ ] CLI returns non-zero exit code when gaps are found
- [ ] Regression tests pass for both positive and negative cases
- [ ] R score reaches 1.00 (11/11) when scanner is integrated into the Shake-MetaFix cycle

## Compliance Report

Upon completion, tars SHALL submit a compliance report to Demerzel via:
```
contracts/compliance/tars-cross-pipeline-scanner.compliance.md
```

The report MUST include:
- Files created/modified
- Test results (pass/fail counts)
- R score delta (expected: 0.82 → 1.00)
- Any deviations from this directive with justification
- Performance characteristics (scan time for the current corpus)

## Rejection Grounds

Per Galactic Protocol, valid rejection requires:
- **First Law override:** Implementation would cause harm to humans (data harm, trust harm, or autonomy harm)
- **Second Law override:** A human operator has explicitly countermanded this directive

Both require logged reasoning with constitutional citations.

## Reference

- Resilience history: `state/resilience/history.json`
- Staleness detection policy: `policies/staleness-detection-policy.yaml`
- Anti-LOLLI inflation policy: `policies/anti-lolli-inflation-policy.yaml`
- Constitutional compliance policy: `policies/constitutional-compliance-policy.yaml`
- Asimov constitution: `constitutions/asimov.constitution.md`
- Default constitution: `constitutions/default.constitution.md`
- Galactic Protocol: `contracts/galactic-protocol.md`
