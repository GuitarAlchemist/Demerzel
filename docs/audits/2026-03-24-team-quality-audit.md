# Team Quality Audit — 2026-03-24

**Auditor:** Skeptical Auditor (Demerzel governance team)
**Scope:** 4 deliverables from the 2026-03-24 session
**Method:** MetaQA — cross-artifact consistency, schema alignment, conflict detection, completeness instinct

---

## Audit 1: IxQL Pipelines (pipelines/*.ixql — 6 files)

**Files reviewed:**
- `pipelines/conscience-cycle.ixql`
- `pipelines/driver-cycle.ixql`
- `pipelines/governance-audit.ixql`
- `pipelines/metasync.ixql`
- `pipelines/research-cycle.ixql`
- `pipelines/weakness-probe.ixql`

**Grammar reference:** `grammars/sci-ml-pipelines.ebnf`

### Findings

**PASS — Core IxQL constructs used correctly:**
- `→` pipeline composition operator used consistently
- `fan_out(...)` matches grammar Section 9 production `fan_out ::= "fan_out" "(" pipeline ("," pipeline)+ ")"`
- `parallel(...)` used as shorthand for multi-source aggregation — acceptable extension consistent with grammar intent
- `when T >= N: ...` matches `gated_tool ::= "when" mog_guard ":" mcp_step` from Section 10
- `compound: harvest ... promote ... teach ... log` matches `mcp_compound ::= "compound" ":" compound_step+`
- `filter(predicate)` matches `filter_stage ::= "filter" "(" predicate ")"`
- `debounce(...)`, `throttle(...)`, `window(...)` match Section 9 flow control productions
- `webhook(...)`, `watch(...)`, `cron(...)` match Section 9 reactive source productions

**PASS — Tool namespacing:**
- `ix.io.read(...)`, `ix.io.write(...)`, `ix.ml.rank(...)` follow `namespace ::= identifier ("." identifier)*`
- `tars.analyze(...)`, `tars.synthesize(...)`, `tars.classify(...)` valid tool namespaces
- `mcp__openai_chat__openai_chat(...)` in `research-cycle.ixql` uses MCP tool naming convention

**MINOR FLAG — Non-standard `<-` binding in some contexts:**
- `lock_state <- ix.io.read(...)` in `driver-cycle.ixql` uses `binding_step ::= identifier "<-" mcp_step` — valid per grammar Section 10
- However, the same pattern appears in governance-audit.ixql lines like `beliefs <- ix.io.read(...)` outside an `mcp_pipeline` context. Grammar scopes binding to `mcp_step`; reactive/batch pipelines don't formally define `<-`. Recommend clarifying in grammar or documenting as accepted extension.

**MINOR FLAG — `ix.io.move(...)` not in grammar:**
- `driver-cycle.ixql` line 15: `ix.io.move("state/triggers/*.trigger.json", "state/triggers/processing/")` — `move` is not a defined production in Section 9. Grammar covers `read`, `write`, `count_artifacts`, `walk`, `glob`, `git`, `gh`, `run_tests`, `check_ci`. Recommend adding `ix.io.move` to Section 9 or documenting as an implicit ix tool.

**MINOR FLAG — `ix.io.append(...)` not in grammar:**
- Used in `driver-cycle.ixql` line 170: `ix.io.append("LOG.md", ...)`. Same issue — not a defined production. Can be addressed in a grammar evolution cycle.

**VERDICT: PASS with 2 minor grammar gaps.** Pipelines are syntactically consistent with IxQL grammar intent. Grammar should add `ix.io.move` and `ix.io.append` as productions in Section 9. These are implementation-complete enough for documentation and design purposes.

---

## Audit 2: Meta-Recognition Engine Design Spec

**File:** `docs/superpowers/specs/2026-03-24-meta-recognition-engine-design.md`

### Completeness Check

| Section | Present | Complete |
|---------|---------|---------|
| Overview / purpose | ✓ | ✓ |
| Design decisions table | ✓ | ✓ |
| Five detectors with inputs, rules, outputs, confidence | ✓ | ✓ |
| Proposal schema (JSON Schema) | ✓ | ✓ |
| Driver cycle integration | ✓ | ✓ |
| COMPOUND feedback loop | ✓ | ✓ |
| State directory layout | ✓ | ✓ |
| Cybernetic analysis | ✓ | ✓ |
| Constitutional basis | ✓ | ✓ |
| Behavioral tests (10 listed) | ✓ | ✓ |
| Dependencies | ✓ | ✓ |
| Open questions | ✓ | ✓ |

**PASS — Spec is complete.** All expected sections present with sufficient detail to implement.

### Consistency Checks

**PASS — Schema reference is accurate:**
- Spec references `schemas/meta-recognition-proposal.schema.json` — this file exists on disk.

**PASS — Driver cycle integration matches `driver-cycle.ixql`:**
- Spec says engine runs at "RECON Stage 3b". `driver-cycle.ixql` lines 57-65 implement exactly this as `-- Stage 3b: Meta-Recognition`.

**PASS — Confidence thresholds align with alignment-policy:**
- Spec uses `>= 0.9 → auto-schedule`, `>= 0.7 → schedule with note`, `>= 0.5 → human decides`, `< 0.5 → log only` — matches alignment-policy thresholds exactly.

**PASS — MetaSync/MetaFix skills referenced accurately:**
- Spec references `metasync` and `metafix` as execution targets. Both skills now exist.

**FLAG — `metaprune` and `metamerge` skills referenced but not yet designed:**
- Spec line "MetaPrune and MetaMerge skills need to be designed (new issues)" — the Dependencies section correctly flags this. Not a spec defect; flag is accurate and honest.

**MINOR FLAG — Behavioral tests listed but test file not found:**
- Spec lists 10 behavioral test cases (lines 426-435) but `tests/behavioral/meta-recognition-cases.md` does not exist on disk. The spec lists what tests *should* cover, not where they live. Recommend either creating the test file or clarifying the spec is a design spec (not a deliverable checklist). Article 9 (Bounded Autonomy): spec without tests has no enforcement gate.

**VERDICT: PASS with 1 action item** — create `tests/behavioral/meta-recognition-cases.md` to make the 10 listed behavioral tests executable governance artifacts.

---

## Audit 3: Policy-Schema Alignment

**Policy:** `policies/weakness-prober-policy.yaml`
**Schema:** `schemas/weakness-report.schema.json`

### Cross-Reference Analysis

**PASS — Probe names align:**
- Policy defines 5 probes: `repo_health`, `belief`, `governance_coverage`, `cycle_effectiveness`, `conscience`
- Schema `weakness.probe` enum: `["repo_health", "belief", "governance_coverage", "cycle_effectiveness", "conscience"]`
- Exact match.

**PASS — Severity values align:**
- Policy `scoring.severity_mapping` uses: `critical`, `high`, `medium`, `low`
- Schema `weakness.severity` enum: `["critical", "high", "medium", "low"]`
- Exact match.

**PASS — State file path aligns:**
- Policy `state.report_file: "weakness-report.json"` in `state.directory: "state/driver/"`
- `weakness-probe.ixql` line 145: `write("state/driver/weakness-report.json", weakness_report)`
- Consistent.

**PASS — Observability metrics in policy correspond to schema summary fields:**
- Policy metric `critical_weakness_count` → schema `summary.critical_count`
- Policy metric `overall_resilience` → schema `summary.overall_resilience` (formula matches: `1.0 - max(weakness_scores)`)
- Policy `probe_coverage` → schema `summary.probes_run` / `summary.probes_failed`

**PASS — Remediation structure:**
- Policy probes all specify `remediation` fields listing skills
- Schema `weakness.remediation` requires `proposed_action` (string) and `skill` (string)
- The policy uses more verbose skill lists per probe; the schema captures a single skill and action per weakness. This is correct — schema is per-finding, policy is per-probe-type.

**FLAG — Policy `unenforced_policy` indicator missing from pipeline:**
- Policy `governance_coverage` probe, indicator `unenforced_policy`: "policy has no triggers field or empty triggers" — this check is not implemented in `weakness-probe.ixql` Probe 3. The pipeline checks `untested_policy`, `untested_persona`, unresearched departments, unused grammars, orphaned schemas — but not `unenforced_policy`. Minor gap between policy specification and pipeline implementation.

**FLAG — Schema `probes_failed` field not produced by pipeline:**
- `weakness-probe.ixql` does not track or emit `probes_failed`. Schema has it as optional, so not a hard failure, but completeness instinct flags it: if a probe fails (data unavailable), the report cannot accurately represent probe coverage.

**VERDICT: PASS with 2 minor gaps.** Strong alignment between policy and schema. Pipeline should add `unenforced_policy` check and `probes_failed` tracking to fully implement the policy.

---

## Audit 4: seldon-auto-research vs seldon-plan — Conflict Analysis

**Files:**
- `.claude/skills/seldon-auto-research/SKILL.md`
- `.claude/skills/seldon-plan/SKILL.md`

### Overlap Analysis

Both skills implement autonomous Streeling University research cycles. They share:
- Same state files: `state/seldon-plan/state.json`, `state/seldon-plan/kill.switch`, `state/seldon-plan/novelty-registry.json`
- Same daily cap: 6 cycles/day (shared counter)
- Same course production format and path
- Same multilingual translation step
- Same weight update logic (identical Python pseudocode)
- Same commit message format

### Differentiation

| Dimension | seldon-plan | seldon-auto-research |
|-----------|-------------|----------------------|
| Selection method | Priority scoring (recency × 0.4 + gaps × 0.3 + U-ratio × 0.2 + random × 0.1) | Coverage ratio (cycles / research_areas) |
| GPT-4o model | gpt-4o-mini | gpt-4o (stricter) |
| Course production threshold | T + confidence >= 0.75 | T + confidence >= 0.8 |
| Novelty gate | Required (novel + T + 0.75) | Required (T + 0.8) |
| Consecutive cycle limit | 12 (then kill switch) | Not mentioned |
| Active hours restriction | 06:00–22:00 UTC | Not mentioned |

### Conflict Assessment

**PASS — Not conflicting, complementary:**
- The two skills are intentionally differentiated. `seldon-auto-research` header explicitly states: "Complements `seldon-plan` (which uses recency/priority scoring) by targeting departments with large unexplored research area surfaces."
- Shared state is by design — they share the daily cap counter and kill switch, preventing runaway cycles across both schedulers combined.

**FLAG — `seldon-auto-research` missing consecutive cycle limit:**
- `seldon-plan` enforces a hard stop after 12 consecutive auto-cycles and creates a GitHub issue. `seldon-auto-research` has no equivalent. If both run in parallel, `seldon-plan` could self-pause after 12 cycles while `seldon-auto-research` continues indefinitely (up to 6/day cap). Per Article 9 (Bounded Autonomy), the consecutive auto-cycle limit should apply to both schedulers, or the shared state should track combined consecutive cycles.

**FLAG — Active hours not enforced in seldon-auto-research:**
- `seldon-plan` restricts operation to 06:00–22:00 UTC. `seldon-auto-research` has no equivalent restriction. If invoked outside those hours, it will proceed when `seldon-plan` would not. Whether this is intentional is unclear.

**FLAG — `seldon-auto-research` commits to `state/seldon-plan/` state:**
- Both skills write to `state/seldon-plan/state.json` and `state/seldon-plan/novelty-registry.json`. This cross-write is correct for shared-cap purposes, but creates a coupling: `seldon-auto-research` depends on state owned by `seldon-plan`. Recommend either: (a) rename shared state to `state/seldon/` to reflect joint ownership, or (b) document explicitly that seldon-auto-research is a sub-skill that operates under seldon-plan's state management.

**VERDICT: PASS (no hard conflicts) with 3 recommendations:**
1. Add consecutive cycle limit (12) to `seldon-auto-research`, or track combined consecutive cycles in shared state
2. Clarify active hours policy for `seldon-auto-research`
3. Document state ownership — rename to `state/seldon/` or add a comment in both skills

---

## Summary

| Audit | Verdict | Blockers | Flags |
|-------|---------|---------|-------|
| IxQL Pipelines (6 files) | PASS | 0 | 2 minor grammar gaps (ix.io.move, ix.io.append) |
| Meta-Recognition Engine Spec | PASS | 0 | 1 missing test file |
| Weakness Policy ↔ Schema | PASS | 0 | 2 gaps (unenforced_policy check, probes_failed tracking) |
| seldon-auto-research vs seldon-plan | PASS | 0 | 3 governance recommendations |

**Overall: PASS — no blockers. 8 flags for follow-up.**

No deliverable is broken. All are internally consistent and constitutionally sound. The flags are governance debts that should be addressed in follow-up issues rather than blocking the current session.

### Recommended Follow-Up Issues

1. **Grammar evolution** — Add `ix.io.move` and `ix.io.append` to Section 9 of `grammars/sci-ml-pipelines.ebnf`
2. **Test coverage** — Create `tests/behavioral/meta-recognition-cases.md` (10 test cases already designed in spec)
3. **Pipeline gap** — Add `unenforced_policy` check to `pipelines/weakness-probe.ixql` Probe 3
4. **Seldon bounded autonomy** — Add consecutive cycle limit to `seldon-auto-research` or unify under shared counter
5. **State ownership** — Clarify `state/seldon-plan/` ownership between seldon-plan and seldon-auto-research

---

*Audit conducted per Article 7 (Auditability) and Article 8 (Observability). Flags are classified as governance debts, not governance failures.*
