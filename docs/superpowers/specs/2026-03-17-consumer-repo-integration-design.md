# Consumer Repo Integration Design Spec

**Issue:** #12 — Consumer Repo Integration
**Date:** 2026-03-17
**Status:** Approved
**Author:** Demerzel governance framework

## Problem

Three consumer repos (ix, tars, ga) have the Demerzel submodule at `governance/demerzel/` but lack full governance integration:

- None have adopted `templates/CLAUDE.md.snippet` into their CLAUDE.md
- None have the full `state/` directory structure (tars has partial — only `beliefs/`)
- Submodules may not point to latest Demerzel

Without these, agents in consumer repos lack governance context in their CLAUDE.md instructions, have no standardized persistence directories, and cannot participate in Galactic Protocol flows (reconnaissance, compliance reporting, knowledge transfer).

## Solution

Issue a governance directive to each consumer repo that triggers a repeatable integration workflow. The workflow is manual (no runtime code in Demerzel) but follows a documented checklist that can be executed by a human or agent session.

## What Gets Added to Each Consumer Repo

### 1. CLAUDE.md Governance Section

Append the contents of `templates/CLAUDE.md.snippet` to each consumer repo's `CLAUDE.md` using section markers for idempotency:

```markdown
<!-- BEGIN DEMERZEL GOVERNANCE -->
{contents of templates/CLAUDE.md.snippet}
<!-- END DEMERZEL GOVERNANCE -->
```

**Integration rules:**
- If markers already exist, replace content between them (update path)
- If markers do not exist, append to end of CLAUDE.md
- Replace `[Demerzel repo]` placeholder with `governance/demerzel` (the submodule path)
- Never modify content outside the markers

### 2. State Directory Structure

Create the full `state/` directory at repo root:

```
state/
  beliefs/.gitkeep
  pdca/.gitkeep
  knowledge/.gitkeep
  snapshots/.gitkeep
```

**Rules:**
- If `state/` partially exists (e.g., tars has `beliefs/`), create only missing subdirectories
- Never overwrite existing state files
- Add `.gitkeep` only to empty directories
- Add `state/` to the repo's `.gitignore` exceptions if needed (state files should be tracked)

### 3. Submodule Update

Update the `governance/demerzel` submodule to latest `master`:

```
cd governance/demerzel && git fetch origin && git checkout origin/master
```

Then commit the submodule pointer update in the consumer repo.

## Integration Directive Format

Each consumer repo receives a directive conforming to `schemas/contracts/directive.schema.json`:

```json
{
  "id": "dir-integration-{repo}-2026-03-17",
  "type": "compliance-requirement",
  "priority": "high",
  "source_article": "demerzel-mandate.md",
  "target_repo": "{repo}",
  "directive_content": "Adopt full Demerzel governance integration: (1) Append templates/CLAUDE.md.snippet to CLAUDE.md with section markers, (2) Create full state/ directory structure with beliefs/, pdca/, knowledge/, snapshots/ subdirectories, (3) Update governance/demerzel submodule to latest master.",
  "issued_by": "demerzel",
  "issued_at": "2026-03-17T00:00:00Z",
  "channel": "crisp"
}
```

## Compliance Report Format

Each consumer repo responds with a compliance report conforming to `schemas/contracts/compliance-report.schema.json`:

```json
{
  "id": "cr-integration-{repo}-2026-03-17",
  "repo": "{repo}",
  "agent": "{repo-primary-agent}",
  "reporting_period": {
    "from": "2026-03-17T00:00:00Z",
    "to": "{completion-timestamp}"
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
  "reported_at": "{completion-timestamp}",
  "channel": "crisp"
}
```

If integration is partial, `overall_status` should be `"partial"` with details in `violations` describing what was not completed and why.

## Integration Checklist (Per Repo)

This checklist is executed manually in a Claude Code session within the consumer repo:

1. **Verify submodule exists:** `ls governance/demerzel/constitutions/` should list files
2. **Update submodule:** `cd governance/demerzel && git fetch origin && git checkout origin/master && cd ../..`
3. **Check CLAUDE.md for existing markers:** Search for `<!-- BEGIN DEMERZEL GOVERNANCE -->`
4. **Append snippet:** If no markers found, append marker-wrapped snippet to CLAUDE.md
5. **Create state directories:** `mkdir -p state/{beliefs,pdca,knowledge,snapshots}` and add `.gitkeep` to each
6. **Commit:** Single commit with message `feat: Adopt Demerzel governance integration (#12)`
7. **Generate compliance report:** Save to `state/snapshots/{date}-integration-compliance.snapshot.json`

## Execution Order

1. **ix** first — simplest repo, validates the process
2. **ga** second — moderately complex
3. **tars** third — has partial state, tests the idempotent merge path

## Rollback Plan

If integration causes issues in a consumer repo:

1. **CLAUDE.md:** Remove everything between `<!-- BEGIN DEMERZEL GOVERNANCE -->` and `<!-- END DEMERZEL GOVERNANCE -->` markers (inclusive). Original content outside markers is untouched.
2. **State directory:** Remove only `.gitkeep` files from empty subdirectories. Never delete directories containing state files. If no state files exist, `rm -rf state/` is safe.
3. **Submodule:** `cd governance/demerzel && git checkout {previous-commit-sha}` to revert to prior version.
4. **Commit:** `fix: Rollback Demerzel governance integration` with reference to the issue.

Rollback is safe because the integration is purely additive — it appends to CLAUDE.md (with markers for clean removal) and creates empty directories.

## Verification

After integration, verify each repo by checking:

- `grep "BEGIN DEMERZEL GOVERNANCE" CLAUDE.md` returns a match
- `ls state/beliefs/ state/pdca/ state/knowledge/ state/snapshots/` succeeds
- `git -C governance/demerzel log -1 --oneline` shows latest Demerzel commit
- A compliance report exists in `state/snapshots/`

## References

- `templates/CLAUDE.md.snippet` — Governance section content
- `templates/state/README.md` — State directory conventions
- `contracts/galactic-protocol.md` — Directive and compliance report flows
- `schemas/contracts/directive.schema.json` — Directive format
- `schemas/contracts/compliance-report.schema.json` — Compliance report format
