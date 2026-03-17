# Wiki Auto-Contribution Design

**Date:** 2026-03-17
**Status:** Draft
**Approach:** GitHub Actions workflow generating wiki pages from governance artifacts

## Overview

Auto-generate and maintain GitHub Wiki pages from Demerzel's governance artifacts. The wiki serves as living documentation that stays in sync with the repo -- no manual wiki editing required.

The GitHub Wiki is a separate git repo (`Demerzel.wiki.git`) that can be cloned, modified, and pushed to programmatically from a GitHub Actions workflow.

## 1. Wiki Page Structure

```
Home.md                         ← Landing page with overview + navigation
Constitution.md                 ← Constitution hierarchy overview
Constitution-Asimov.md          ← asimov.constitution.md (Articles 0-5)
Constitution-Default.md         ← default.constitution.md (Articles 1-11)
Constitution-Mandate.md         ← demerzel-mandate.md
Constitution-Harm-Taxonomy.md   ← harm-taxonomy.md
Personas.md                     ← Persona catalog index (table of all 14 personas)
Persona-<Name>.md               ← One page per persona (e.g., Persona-Demerzel.md)
Policies.md                     ← Policy index with summaries
Policy-<Name>.md                ← One page per policy (e.g., Policy-Alignment.md)
Schemas.md                      ← Schema reference index
Contracts.md                    ← Galactic Protocol overview + contract schema summaries
_Sidebar.md                     ← Auto-generated navigation sidebar
_Footer.md                      ← Generation timestamp + link back to repo
```

Total: ~40 pages (1 home + 4 constitution + 1 persona index + 14 persona pages + 1 policy index + 9 policy pages + 1 schema index + 1 contracts + 3 navigation/footer).

## 2. Generation Strategy

Each artifact type maps to wiki markdown differently. The workflow uses shell scripting (bash) -- no runtime code lives in the repo.

### 2.1 Constitutions (Markdown to Markdown)

Source files are already markdown. Generation is mostly pass-through with added wiki metadata.

**Template:**

```markdown
<!-- Auto-generated from constitutions/{filename} -- do not edit manually -->

# {Title from H1}

> Source: [`constitutions/{filename}`](../blob/master/constitutions/{filename})
> Last updated: {file last-modified date from git}

{Original markdown content}

---
See also: [Constitution Overview](Constitution) | [Home](Home)
```

**Processing:**
- Copy markdown content verbatim
- Prepend auto-generation notice
- Add source link and cross-navigation footer
- Extract H1 as page title

### 2.2 Personas (YAML to Markdown)

Parse YAML fields into structured markdown pages.

**Persona index page (`Personas.md`):**

```markdown
# Persona Catalog

| Persona | Role | Goal Directedness | Estimator |
|---------|------|-------------------|-----------|
| [Demerzel](Persona-Demerzel) | Governance coordinator... | governance-scoped | skeptical-auditor |
| [Seldon](Persona-Seldon) | Knowledge transfer... | session-scoped | skeptical-auditor |
...
```

**Individual persona page (`Persona-<Name>.md`):**

```markdown
<!-- Auto-generated from personas/{name}.persona.yaml -- do not edit manually -->

# {Name} (v{version})

> {description}
>
> Source: [`personas/{name}.persona.yaml`](../blob/master/personas/{name}.persona.yaml)

**Role:** {role}
**Domain:** {domain}
**Goal Directedness:** {goal_directedness}
**Estimator Pairing:** [{estimator_pairing}](Persona-{Estimator-Name})

## Capabilities

- {capability 1}
- {capability 2}
...

## Constraints

- {constraint 1}
- {constraint 2}
...

## Voice

- **Tone:** {voice.tone}
- **Verbosity:** {voice.verbosity}
- **Style:** {voice.style}

---
See also: [Persona Catalog](Personas) | [Home](Home)
```

**Processing:**
- Parse YAML with `yq` (lightweight YAML processor, available in GitHub Actions runners)
- Iterate over all `*.persona.yaml` files
- Generate index table sorted alphabetically by name
- Generate one detail page per persona

### 2.3 Policies (YAML to Markdown)

Parse YAML into readable reference pages.

**Policy index page (`Policies.md`):**

```markdown
# Policy Reference

| Policy | Version | Description |
|--------|---------|-------------|
| [Alignment](Policy-Alignment) | 1.0.0 | Rules for verifying agent actions serve user intent |
| [Kaizen](Policy-Kaizen) | 1.0.0 | Universal continuous improvement methodology... |
...
```

**Individual policy page (`Policy-<Name>.md`):**

```markdown
<!-- Auto-generated from policies/{name}.yaml -- do not edit manually -->

# {name} Policy (v{version})

> {description}
>
> Source: [`policies/{name}.yaml`](../blob/master/policies/{name}.yaml)
> Effective: {effective_date}

## Summary

{Top-level YAML keys rendered as sections}

## References

- {reference 1}
- {reference 2}
...

---
See also: [Policy Reference](Policies) | [Home](Home)
```

**Processing:**
- Parse YAML with `yq`
- Render top-level keys as H2 sections
- For nested structures (like `pdca_cycle`, `waste_taxonomy`), render as nested lists or sub-sections
- Depth limit: render up to 3 levels of nesting; deeper structures become indented bullet lists
- Long policies (like kaizen-policy) get a table of contents at the top

### 2.4 Schemas (JSON Schema to Markdown)

Generate a reference page listing all schemas with their required fields and descriptions.

**Schema index page (`Schemas.md`):**

```markdown
# Schema Reference

## Core Schemas

| Schema | Description |
|--------|-------------|
| [`persona.schema.json`](../blob/master/schemas/persona.schema.json) | Structured behavioral profile for an AI agent |
| [`reconnaissance-profile.schema.json`](../blob/master/schemas/reconnaissance-profile.schema.json) | ... |

## Contract Schemas

| Schema | Description | Direction |
|--------|-------------|-----------|
| [`directive.schema.json`](../blob/master/schemas/contracts/directive.schema.json) | Governance directives | Demerzel -> consumer |
...
```

**Processing:**
- Read `$id`, `title`, and `description` from each JSON Schema file using `jq`
- List required fields for each schema
- Link to raw schema files in the repo (schemas are technical reference -- no need to fully render JSON Schema as markdown)

### 2.5 Contracts (Markdown to Markdown)

The Galactic Protocol spec is already markdown. Same pass-through approach as constitutions.

### 2.6 Home Page

Static template with dynamic content:

```markdown
# Demerzel Governance Framework

> AI governance framework providing constitutions, personas, policies, schemas, and contracts.

## Quick Navigation

- [Constitution Overview](Constitution) -- Asimov Laws, operational ethics, governance mandate
- [Persona Catalog](Personas) -- {count} agent personas
- [Policy Reference](Policies) -- {count} governance policies
- [Schema Reference](Schemas) -- JSON Schemas for validation
- [Galactic Protocol](Contracts) -- Cross-repo communication contracts

## Constitution Hierarchy

\```
asimov.constitution.md        (root -- Laws of Robotics, Articles 0-5)
  |-- demerzel-mandate.md     (who enforces the laws)
  |-- default.constitution.md (operational ethics, Articles 1-11)
       |-- policies/*.yaml
            |-- personas/*.persona.yaml
\```

## Confidence Thresholds

| Threshold | Action |
|-----------|--------|
| >= 0.9 | Proceed autonomously |
| >= 0.7 | Proceed with note |
| >= 0.5 | Ask for confirmation |
| >= 0.3 | Escalate to human |
| < 0.3 | Do not act |

---
*Auto-generated from [Demerzel repo](../). Last synced: {timestamp}.*
```

## 3. Sidebar Navigation

Auto-generated `_Sidebar.md`:

```markdown
**[Home](Home)**

**Constitution**
- [Overview](Constitution)
- [Asimov Laws](Constitution-Asimov)
- [Default Constitution](Constitution-Default)
- [Governance Mandate](Constitution-Mandate)
- [Harm Taxonomy](Constitution-Harm-Taxonomy)

**Personas**
- [Catalog](Personas)
- [Demerzel](Persona-Demerzel)
- [Seldon](Persona-Seldon)
- ...{alphabetical list}

**Policies**
- [Reference](Policies)
- [Alignment](Policy-Alignment)
- ...{alphabetical list}

**Technical**
- [Schemas](Schemas)
- [Galactic Protocol](Contracts)
```

Persona and policy entries in the sidebar are generated dynamically from the file listing.

## 4. GitHub Actions Workflow

File: `.github/workflows/wiki-sync.yml`

### Trigger

```yaml
name: Sync Wiki
on:
  push:
    branches: [master]
    paths:
      - 'constitutions/**'
      - 'personas/**'
      - 'policies/**'
      - 'schemas/**'
      - 'contracts/**'
  workflow_dispatch:  # manual trigger for initial population or debugging
```

**Rationale:** Trigger on push to master when source artifacts change. No daily schedule needed -- push-based keeps the wiki in sync without unnecessary runs. `workflow_dispatch` allows manual re-generation.

### Steps

```yaml
jobs:
  sync-wiki:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout main repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # need git history for last-modified dates

      - name: Checkout wiki repo
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository }}.wiki
          path: wiki
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Install tools
        run: |
          sudo apt-get install -y jq
          sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
          sudo chmod +x /usr/local/bin/yq

      - name: Generate wiki pages
        run: bash .github/scripts/generate-wiki.sh

      - name: Push wiki changes
        working-directory: wiki
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          if git diff --cached --quiet; then
            echo "No wiki changes detected"
          else
            git commit -m "Auto-sync wiki from $(git -C .. rev-parse --short HEAD)"
            git push
          fi
```

### Generation Script

File: `.github/scripts/generate-wiki.sh`

This is a bash script that:
1. Clears the `wiki/` directory (except `.git`)
2. Generates each page type using the templates described in Section 2
3. Uses `yq` for YAML parsing, `jq` for JSON parsing
4. Uses `git log -1 --format=%ci -- <file>` for last-modified dates

The script is the only "code" added, and it lives in `.github/` (CI infrastructure, not runtime code).

## 5. Change Detection

The workflow already uses path filtering on the trigger (`paths:` key), so it only runs when source artifacts change. Within the script, there is no per-file diffing -- the entire wiki is regenerated on each run. This is simpler and avoids stale page bugs from partial updates.

**Rationale:** The full set of governance artifacts is small (~30 files). Regenerating all ~40 wiki pages takes seconds. Incremental generation adds complexity for no meaningful benefit.

## 6. Cross-Linking

Wiki pages cross-link using GitHub Wiki link syntax `[text](Page-Name)`:

- Constitution pages link to each other and to the hierarchy overview
- Persona pages link to their `estimator_pairing` persona page
- Policy pages link to referenced constitutions and other policies (parsed from the `references:` YAML field)
- All pages link back to source files in the main repo via `../blob/master/` URLs
- All pages have footer links to their parent index page and Home

## 7. Edge Cases

| Case | Handling |
|------|----------|
| Wiki repo does not exist yet | Fails gracefully; user must create wiki with at least one page first (GitHub requirement) |
| YAML parse error | `yq` exits non-zero; workflow fails; shows which file broke |
| New persona/policy added | Automatically picked up on next push -- no config changes needed |
| Persona/policy deleted | Old wiki page is removed (full regeneration clears all pages first) |
| Very long policy (kaizen) | Auto-generate table of contents from H2 headings |
| Special characters in names | Persona names are kebab-case by schema constraint; safe for filenames |

## 8. What This Does NOT Do

- No runtime code in the Demerzel repo (script lives in `.github/`)
- No custom wiki themes or CSS
- No search functionality beyond GitHub's built-in wiki search
- No versioned wiki (wiki reflects current master; use repo git history for versions)
- No two-way sync (wiki is read-only output; edits go through the main repo)

## 9. Implementation Plan

1. **Create initial wiki page** -- manually create a Home page in the GitHub Wiki UI (required for the wiki git repo to exist)
2. **Write `generate-wiki.sh`** -- the generation script with templates from Section 2
3. **Add workflow file** -- `.github/workflows/wiki-sync.yml`
4. **Test with `workflow_dispatch`** -- trigger manually, verify generated pages
5. **Merge to master** -- push-based trigger takes over

## 10. Files to Create

| File | Purpose |
|------|---------|
| `.github/workflows/wiki-sync.yml` | GitHub Actions workflow |
| `.github/scripts/generate-wiki.sh` | Wiki page generation script |

No governance artifacts are modified. No schemas, personas, or policies are added.
