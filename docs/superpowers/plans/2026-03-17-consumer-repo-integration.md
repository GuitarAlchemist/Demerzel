# Consumer Repo Integration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire ix, tars, and ga consumer repos to Demerzel governance via CLAUDE.md snippets, state directories, and Galactic Protocol directives.

**Architecture:** Issue governance directives from Demerzel, then execute integration checklists in each consumer repo (ix → ga → tars). Integration is additive — markers for CLAUDE.md, empty state directories, submodule update.

**Tech Stack:** Git submodules, Markdown, YAML, JSON, Bash (GitHub Actions)

---

## Chunk 1: Create Governance Directives in Demerzel

### Task 1.1: Create directive for ix

**Files:**
- Create: `examples/sample-data/directive-integration-ix.json`

- [ ] **Step 1: Write the ix integration directive**

Create `examples/sample-data/directive-integration-ix.json`:

```json
{
  "id": "dir-integration-ix-2026-03-17",
  "type": "compliance-requirement",
  "priority": "high",
  "source_article": "demerzel-mandate.md",
  "target_repo": "ix",
  "directive_content": "Adopt full Demerzel governance integration: (1) Append templates/CLAUDE.md.snippet to CLAUDE.md with section markers <!-- BEGIN DEMERZEL GOVERNANCE --> and <!-- END DEMERZEL GOVERNANCE -->, replacing [Demerzel repo] with governance/demerzel. (2) Create full state/ directory structure with beliefs/, pdca/, knowledge/, snapshots/ subdirectories and .gitkeep files. (3) Update governance/demerzel submodule to latest master.",
  "issued_by": "demerzel",
  "issued_at": "2026-03-17T00:00:00Z",
  "channel": "crisp"
}
```

- [ ] **Step 2: Validate directive against schema**

Run:
```bash
cd C:/Users/spare/source/repos/Demerzel
npx ajv validate -s schemas/contracts/directive.schema.json -d examples/sample-data/directive-integration-ix.json --spec=draft2020
```

If `npx ajv` is not available, manually verify: all required fields (`id`, `type`, `priority`, `source_article`, `target_repo`, `directive_content`, `issued_by`, `issued_at`) are present, `id` matches `^dir-[a-z0-9-]+$`, `type` is `compliance-requirement`, `priority` is `high`, `target_repo` is `ix`.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/Demerzel
git add examples/sample-data/directive-integration-ix.json
git commit -m "feat: Add governance integration directive for ix (#12)"
```

### Task 1.2: Create directive for ga

**Files:**
- Create: `examples/sample-data/directive-integration-ga.json`

- [ ] **Step 1: Write the ga integration directive**

Create `examples/sample-data/directive-integration-ga.json`:

```json
{
  "id": "dir-integration-ga-2026-03-17",
  "type": "compliance-requirement",
  "priority": "high",
  "source_article": "demerzel-mandate.md",
  "target_repo": "ga",
  "directive_content": "Adopt full Demerzel governance integration: (1) Append templates/CLAUDE.md.snippet to CLAUDE.md with section markers <!-- BEGIN DEMERZEL GOVERNANCE --> and <!-- END DEMERZEL GOVERNANCE -->, replacing [Demerzel repo] with governance/demerzel. (2) Create full state/ directory structure with beliefs/, pdca/, knowledge/, snapshots/ subdirectories and .gitkeep files. (3) Update governance/demerzel submodule to latest master.",
  "issued_by": "demerzel",
  "issued_at": "2026-03-17T00:00:00Z",
  "channel": "crisp"
}
```

- [ ] **Step 2: Validate directive against schema**

Same validation as Task 1.1 Step 2, substituting the ga directive file path.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/Demerzel
git add examples/sample-data/directive-integration-ga.json
git commit -m "feat: Add governance integration directive for ga (#12)"
```

### Task 1.3: Create directive for tars

**Files:**
- Create: `examples/sample-data/directive-integration-tars.json`

- [ ] **Step 1: Write the tars integration directive**

Create `examples/sample-data/directive-integration-tars.json`:

```json
{
  "id": "dir-integration-tars-2026-03-17",
  "type": "compliance-requirement",
  "priority": "high",
  "source_article": "demerzel-mandate.md",
  "target_repo": "tars",
  "directive_content": "Adopt full Demerzel governance integration: (1) Append templates/CLAUDE.md.snippet to CLAUDE.md with section markers <!-- BEGIN DEMERZEL GOVERNANCE --> and <!-- END DEMERZEL GOVERNANCE -->, replacing [Demerzel repo] with governance/demerzel. (2) Create missing state/ subdirectories (pdca/, knowledge/, snapshots/) — beliefs/ may already exist, preserve it. (3) Update governance/demerzel submodule to latest master.",
  "issued_by": "demerzel",
  "issued_at": "2026-03-17T00:00:00Z",
  "channel": "crisp"
}
```

- [ ] **Step 2: Validate directive against schema**

Same validation as Task 1.1 Step 2, substituting the tars directive file path.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/Demerzel
git add examples/sample-data/directive-integration-tars.json
git commit -m "feat: Add governance integration directive for tars (#12)"
```

---

## Chunk 2: Execute Integration in ix

**Working directory:** `C:/Users/spare/source/repos/ix`

### Task 2.1: Update the governance/demerzel submodule

- [ ] **Step 1: Verify submodule exists**

```bash
cd C:/Users/spare/source/repos/ix
ls governance/demerzel/constitutions/
```

Should list constitutional files. If it fails, run `git submodule update --init --recursive` first.

- [ ] **Step 2: Update submodule to latest master**

```bash
cd C:/Users/spare/source/repos/ix/governance/demerzel
git fetch origin
git checkout origin/master
```

### Task 2.2: Append CLAUDE.md governance section

**Files:**
- Modify: `C:/Users/spare/source/repos/ix/CLAUDE.md`

- [ ] **Step 1: Check for existing markers**

Search `C:/Users/spare/source/repos/ix/CLAUDE.md` for `<!-- BEGIN DEMERZEL GOVERNANCE -->`. If found, replace content between markers. If not found, proceed to Step 2.

- [ ] **Step 2: Append governance section**

Append the following to the end of `C:/Users/spare/source/repos/ix/CLAUDE.md`:

```markdown

<!-- BEGIN DEMERZEL GOVERNANCE -->
# Demerzel Governance Integration

This repo participates in the Demerzel governance framework.

## Governance Framework

All agents in this repo are governed by the Demerzel constitutional hierarchy:

- **Root constitution:** governance/demerzel/constitutions/asimov.constitution.md (Articles 0-5: Laws of Robotics + LawZero principles)
- **Governance coordinator:** Demerzel (see governance/demerzel/constitutions/demerzel-mandate.md)
- **Operational ethics:** governance/demerzel/constitutions/default.constitution.md (Articles 1-7)
- **Harm taxonomy:** governance/demerzel/constitutions/harm-taxonomy.md

## Policy Compliance

Agents must comply with all Demerzel policies:

- **Alignment:** Verify actions serve user intent (confidence thresholds: 0.9 autonomous, 0.7 with note, 0.5 confirm, 0.3 escalate)
- **Rollback:** Revert failed changes automatically; pause autonomous changes after automatic rollback
- **Self-modification:** Never modify constitutional articles, disable audit logging, or remove safety checks
- **Kaizen:** Follow PDCA cycle for improvements; classify as reactive/proactive/innovative before acting
- **Reconnaissance:** Respond to Demerzel's reconnaissance requests with belief snapshots and compliance reports
- **Scientific objectivity:** Tag evidence as empirical/inferential/subjective; generator/estimator accountability
- **Streeling:** Accept knowledge transfers from Seldon; report comprehension via belief state assessment

## Galactic Protocol

This repo communicates with Demerzel via the Galactic Protocol:

- **Inbound (from Demerzel):** Governance directives, knowledge packages
- **Outbound (to Demerzel):** Compliance reports, belief snapshots, learning outcomes
- **Message formats:** See governance/demerzel/schemas/contracts/

## Belief State Persistence

This repo maintains a `state/` directory for belief persistence:

- `state/beliefs/` — Tetravalent belief states (*.belief.json)
- `state/pdca/` — PDCA cycle tracking (*.pdca.json)
- `state/knowledge/` — Knowledge transfer records (*.knowledge.json)
- `state/snapshots/` — Belief snapshots for reconnaissance (*.snapshot.json)

File naming: `{date}-{short-description}.{type}.json`

## Agent Requirements

Every persona in this repo must include:

- `affordances` — Explicit list of permitted actions
- `goal_directedness` — One of: none, task-scoped, session-scoped
- `estimator_pairing` — Neutral evaluator persona (typically skeptical-auditor)
- All fields required by governance/demerzel/schemas/persona.schema.json
<!-- END DEMERZEL GOVERNANCE -->
```

### Task 2.3: Create state directory structure

- [ ] **Step 1: Create directories with .gitkeep**

```bash
cd C:/Users/spare/source/repos/ix
mkdir -p state/beliefs state/pdca state/knowledge state/snapshots
touch state/beliefs/.gitkeep state/pdca/.gitkeep state/knowledge/.gitkeep state/snapshots/.gitkeep
```

### Task 2.4: Commit integration

- [ ] **Step 1: Stage and commit all integration changes**

```bash
cd C:/Users/spare/source/repos/ix
git add CLAUDE.md state/ governance/demerzel
git commit -m "feat: Adopt Demerzel governance integration (#12)"
```

---

## Chunk 3: Execute Integration in ga

**Working directory:** `C:/Users/spare/source/repos/ga`

### Task 3.1: Update the governance/demerzel submodule

- [ ] **Step 1: Verify submodule exists**

```bash
cd C:/Users/spare/source/repos/ga
ls governance/demerzel/constitutions/
```

If it fails, run `git submodule update --init --recursive` first.

- [ ] **Step 2: Update submodule to latest master**

```bash
cd C:/Users/spare/source/repos/ga/governance/demerzel
git fetch origin
git checkout origin/master
```

### Task 3.2: Append CLAUDE.md governance section

**Files:**
- Modify: `C:/Users/spare/source/repos/ga/CLAUDE.md`

- [ ] **Step 1: Check for existing markers**

Search `C:/Users/spare/source/repos/ga/CLAUDE.md` for `<!-- BEGIN DEMERZEL GOVERNANCE -->`. If found, replace content between markers. If not found, proceed to Step 2.

- [ ] **Step 2: Append governance section**

Append the same governance section as Task 2.2 Step 2 to `C:/Users/spare/source/repos/ga/CLAUDE.md`. All instances of `[Demerzel repo]` are already replaced with `governance/demerzel` in the template text above.

### Task 3.3: Create state directory structure

- [ ] **Step 1: Create directories with .gitkeep**

```bash
cd C:/Users/spare/source/repos/ga
mkdir -p state/beliefs state/pdca state/knowledge state/snapshots
touch state/beliefs/.gitkeep state/pdca/.gitkeep state/knowledge/.gitkeep state/snapshots/.gitkeep
```

### Task 3.4: Commit integration

- [ ] **Step 1: Stage and commit all integration changes**

```bash
cd C:/Users/spare/source/repos/ga
git add CLAUDE.md state/ governance/demerzel
git commit -m "feat: Adopt Demerzel governance integration (#12)"
```

---

## Chunk 4: Execute Integration in tars

**Working directory:** `C:/Users/spare/source/repos/tars`

### Task 4.1: Update the governance/demerzel submodule

- [ ] **Step 1: Verify submodule exists**

```bash
cd C:/Users/spare/source/repos/tars
ls governance/demerzel/constitutions/
```

If it fails, run `git submodule update --init --recursive` first.

- [ ] **Step 2: Update submodule to latest master**

```bash
cd C:/Users/spare/source/repos/tars/governance/demerzel
git fetch origin
git checkout origin/master
```

### Task 4.2: Append CLAUDE.md governance section

**Files:**
- Modify: `C:/Users/spare/source/repos/tars/CLAUDE.md`

- [ ] **Step 1: Check for existing markers**

Search `C:/Users/spare/source/repos/tars/CLAUDE.md` for `<!-- BEGIN DEMERZEL GOVERNANCE -->`. If found, replace content between markers. If not found, proceed to Step 2.

- [ ] **Step 2: Append governance section**

Append the same governance section as Task 2.2 Step 2 to `C:/Users/spare/source/repos/tars/CLAUDE.md`. All instances of `[Demerzel repo]` are already replaced with `governance/demerzel` in the template text above.

### Task 4.3: Create state directory structure (idempotent — tars may have partial state/)

- [ ] **Step 1: Check existing state directories**

```bash
cd C:/Users/spare/source/repos/tars
ls -la state/ 2>/dev/null
ls -la state/beliefs/ 2>/dev/null
```

Note which directories already exist. Do NOT delete or overwrite existing files.

- [ ] **Step 2: Create only missing directories**

```bash
cd C:/Users/spare/source/repos/tars
mkdir -p state/beliefs state/pdca state/knowledge state/snapshots
```

- [ ] **Step 3: Add .gitkeep only to empty directories**

For each subdirectory, add `.gitkeep` only if the directory is empty:

```bash
cd C:/Users/spare/source/repos/tars
for dir in state/beliefs state/pdca state/knowledge state/snapshots; do
  if [ -z "$(ls -A $dir 2>/dev/null)" ]; then
    touch "$dir/.gitkeep"
  fi
done
```

### Task 4.4: Commit integration

- [ ] **Step 1: Stage and commit all integration changes**

```bash
cd C:/Users/spare/source/repos/tars
git add CLAUDE.md state/ governance/demerzel
git commit -m "feat: Adopt Demerzel governance integration (#12)"
```

---

## Chunk 5: Generate Compliance Reports

### Task 5.1: Generate compliance report for ix

**Files:**
- Create: `C:/Users/spare/source/repos/ix/state/snapshots/2026-03-17-integration-compliance.snapshot.json`

- [ ] **Step 1: Write the compliance report**

Create `C:/Users/spare/source/repos/ix/state/snapshots/2026-03-17-integration-compliance.snapshot.json`:

```json
{
  "id": "cr-integration-ix-2026-03-17",
  "repo": "ix",
  "agent": "ix-forge",
  "reporting_period": {
    "from": "2026-03-17T00:00:00Z",
    "to": "2026-03-17T23:59:59Z"
  },
  "constitutional_compliance": [
    { "article": "demerzel-mandate.md", "status": "compliant" }
  ],
  "policy_compliance": [
    { "policy": "reconnaissance-policy.yaml", "status": "compliant" },
    { "policy": "streeling-policy.yaml", "status": "compliant" }
  ],
  "violations": [],
  "overall_status": "compliant",
  "reported_at": "2026-03-17T23:59:59Z",
  "channel": "crisp"
}
```

- [ ] **Step 2: Validate against compliance-report schema**

Verify all required fields are present and values match the enum constraints in `schemas/contracts/compliance-report.schema.json`: `id` matches `^cr-[a-z0-9-]+$`, `repo` is `ix`, `overall_status` is `compliant`.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/ix
git add state/snapshots/2026-03-17-integration-compliance.snapshot.json
git commit -m "feat: Add integration compliance report (#12)"
```

### Task 5.2: Generate compliance report for ga

**Files:**
- Create: `C:/Users/spare/source/repos/ga/state/snapshots/2026-03-17-integration-compliance.snapshot.json`

- [ ] **Step 1: Write the compliance report**

Create `C:/Users/spare/source/repos/ga/state/snapshots/2026-03-17-integration-compliance.snapshot.json`:

```json
{
  "id": "cr-integration-ga-2026-03-17",
  "repo": "ga",
  "agent": "guitar-alchemist",
  "reporting_period": {
    "from": "2026-03-17T00:00:00Z",
    "to": "2026-03-17T23:59:59Z"
  },
  "constitutional_compliance": [
    { "article": "demerzel-mandate.md", "status": "compliant" }
  ],
  "policy_compliance": [
    { "policy": "reconnaissance-policy.yaml", "status": "compliant" },
    { "policy": "streeling-policy.yaml", "status": "compliant" }
  ],
  "violations": [],
  "overall_status": "compliant",
  "reported_at": "2026-03-17T23:59:59Z",
  "channel": "crisp"
}
```

- [ ] **Step 2: Validate against compliance-report schema**

Same validation as Task 5.1 Step 2, with `repo` = `ga`.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/ga
git add state/snapshots/2026-03-17-integration-compliance.snapshot.json
git commit -m "feat: Add integration compliance report (#12)"
```

### Task 5.3: Generate compliance report for tars

**Files:**
- Create: `C:/Users/spare/source/repos/tars/state/snapshots/2026-03-17-integration-compliance.snapshot.json`

- [ ] **Step 1: Write the compliance report**

Create `C:/Users/spare/source/repos/tars/state/snapshots/2026-03-17-integration-compliance.snapshot.json`:

```json
{
  "id": "cr-integration-tars-2026-03-17",
  "repo": "tars",
  "agent": "tars-cognition",
  "reporting_period": {
    "from": "2026-03-17T00:00:00Z",
    "to": "2026-03-17T23:59:59Z"
  },
  "constitutional_compliance": [
    { "article": "demerzel-mandate.md", "status": "compliant" }
  ],
  "policy_compliance": [
    { "policy": "reconnaissance-policy.yaml", "status": "compliant" },
    { "policy": "streeling-policy.yaml", "status": "compliant" }
  ],
  "violations": [],
  "overall_status": "compliant",
  "reported_at": "2026-03-17T23:59:59Z",
  "channel": "crisp"
}
```

Note: If tars integration was partial (e.g., beliefs/ already existed with files), set `overall_status` to `"compliant"` since existing state was preserved and all new artifacts were added. Only use `"partial"` if some step could not be completed.

- [ ] **Step 2: Validate against compliance-report schema**

Same validation as Task 5.1 Step 2, with `repo` = `tars`.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/spare/source/repos/tars
git add state/snapshots/2026-03-17-integration-compliance.snapshot.json
git commit -m "feat: Add integration compliance report (#12)"
```

---

## Chunk 6: Verify All Integrations

### Task 6.1: Verify ix integration

- [ ] **Step 1: Check CLAUDE.md markers**

```bash
cd C:/Users/spare/source/repos/ix
grep "BEGIN DEMERZEL GOVERNANCE" CLAUDE.md
```

Should return one match.

- [ ] **Step 2: Check state directories**

```bash
cd C:/Users/spare/source/repos/ix
ls state/beliefs/ state/pdca/ state/knowledge/ state/snapshots/
```

Should list `.gitkeep` and/or compliance report.

- [ ] **Step 3: Check submodule version**

```bash
git -C C:/Users/spare/source/repos/ix/governance/demerzel log -1 --oneline
```

Should show the latest Demerzel commit.

- [ ] **Step 4: Check compliance report exists**

```bash
ls C:/Users/spare/source/repos/ix/state/snapshots/2026-03-17-integration-compliance.snapshot.json
```

### Task 6.2: Verify ga integration

- [ ] **Step 1-4: Same checks as Task 6.1**

Repeat all four verification steps for `C:/Users/spare/source/repos/ga`.

### Task 6.3: Verify tars integration

- [ ] **Step 1-4: Same checks as Task 6.1**

Repeat all four verification steps for `C:/Users/spare/source/repos/tars`.

Additionally for tars, verify that any pre-existing state files in `state/beliefs/` were preserved (not overwritten or deleted).

### Task 6.4: Final summary commit in Demerzel

- [ ] **Step 1: Commit all three directives together if not already committed individually**

If directives were committed individually in Chunk 1, this step is a no-op. Otherwise:

```bash
cd C:/Users/spare/source/repos/Demerzel
git add examples/sample-data/directive-integration-*.json
git commit -m "feat: Add governance integration directives for ix, ga, tars (#12)"
```

---

## Rollback Procedure

If integration causes issues in any consumer repo, follow this procedure per the design spec:

1. **CLAUDE.md:** Remove everything between `<!-- BEGIN DEMERZEL GOVERNANCE -->` and `<!-- END DEMERZEL GOVERNANCE -->` markers (inclusive)
2. **State directory:** Remove only `.gitkeep` files from empty subdirectories. If no state files exist, `rm -rf state/` is safe
3. **Submodule:** `cd governance/demerzel && git checkout {previous-commit-sha}`
4. **Commit:** `fix: Rollback Demerzel governance integration` with reference to #12

---

## Summary

| Chunk | Repo | Tasks | Estimated Time |
|-------|------|-------|---------------|
| 1 | Demerzel | 3 directives (ix, ga, tars) | 5-10 min |
| 2 | ix | Submodule + CLAUDE.md + state dirs + commit | 3-5 min |
| 3 | ga | Submodule + CLAUDE.md + state dirs + commit | 3-5 min |
| 4 | tars | Submodule + CLAUDE.md + state dirs (idempotent) + commit | 5-8 min |
| 5 | All three | Compliance reports + validation + commit | 5-10 min |
| 6 | All three + Demerzel | Verification checks | 3-5 min |
| **Total** | | | **24-43 min** |
