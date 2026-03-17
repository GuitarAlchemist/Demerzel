# Wiki Auto-Contribution Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auto-generate and maintain GitHub Wiki pages from Demerzel governance artifacts via a push-triggered GitHub Actions workflow.

**Architecture:** A bash script generates ~40 wiki pages from constitutions (markdown pass-through), personas (YAML→markdown via yq), policies (YAML→markdown via yq), and schemas (JSON→markdown via jq). A GitHub Actions workflow clones the wiki repo, runs the script, and pushes changes.

**Tech Stack:** GitHub Actions, Bash, yq, jq, Git

---

## Prerequisites

- [ ] **Step 0: Create wiki manually**
  - Go to the Demerzel repo on GitHub → Wiki tab → "Create the first page"
  - Add a placeholder Home page with text: `# Demerzel — Wiki initializing...`
  - Save the page (this creates the `Demerzel.wiki.git` repo that the workflow needs)
  - **Time:** 1 minute

---

## Phase 1: Generation Script

File: `.github/scripts/generate-wiki.sh`

### Step 1a: Script scaffold and Home page generation

- [ ] Create `.github/scripts/` directory
- [ ] Create `generate-wiki.sh` with shebang, `set -euo pipefail`, and the scaffold:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WIKI_DIR="${REPO_ROOT}/wiki"
TIMESTAMP="$(date -u '+%Y-%m-%d %H:%M UTC')"
REPO_URL="https://github.com/GuitarAlchemist/Demerzel"

# Clean wiki dir (preserve .git)
find "${WIKI_DIR}" -maxdepth 1 -not -name '.git' -not -name '.' -delete 2>/dev/null || true

#--- Home page ---
generate_home() {
  local persona_count policy_count
  persona_count=$(find "${REPO_ROOT}/personas" -name '*.persona.yaml' | wc -l)
  policy_count=$(find "${REPO_ROOT}/policies" -name '*.yaml' | wc -l)

  cat > "${WIKI_DIR}/Home.md" <<HOMEEOF
<!-- Auto-generated from Demerzel repo -- do not edit manually -->

# Demerzel Governance Framework

> AI governance framework providing constitutions, personas, policies, schemas, and contracts.

## Quick Navigation

- [Constitution Overview](Constitution) -- Asimov Laws, operational ethics, governance mandate
- [Persona Catalog](Personas) -- ${persona_count} agent personas
- [Policy Reference](Policies) -- ${policy_count} governance policies
- [Schema Reference](Schemas) -- JSON Schemas for validation
- [Galactic Protocol](Contracts) -- Cross-repo communication contracts

## Constitution Hierarchy

\`\`\`
asimov.constitution.md        (root -- Laws of Robotics, Articles 0-5)
  |-- demerzel-mandate.md     (who enforces the laws)
  |-- default.constitution.md (operational ethics, Articles 1-11)
       |-- policies/*.yaml
            |-- personas/*.persona.yaml
\`\`\`

## Confidence Thresholds

| Threshold | Action |
|-----------|--------|
| >= 0.9 | Proceed autonomously |
| >= 0.7 | Proceed with note |
| >= 0.5 | Ask for confirmation |
| >= 0.3 | Escalate to human |
| < 0.3 | Do not act |

---
*Auto-generated from [Demerzel repo](${REPO_URL}). Last synced: ${TIMESTAMP}.*
HOMEEOF
}
```

- **Time:** 3 minutes

### Step 1b: Constitution page generation

- [ ] Add `generate_constitutions()` function to the script:

```bash
generate_constitutions() {
  # Constitution overview page
  cat > "${WIKI_DIR}/Constitution.md" <<'CONSTEOF'
<!-- Auto-generated from Demerzel repo -- do not edit manually -->

# Constitution Hierarchy

The Demerzel governance framework is built on a layered constitution:

| Document | Scope |
|----------|-------|
| [Asimov Laws](Constitution-Asimov) | Root -- Laws of Robotics (Articles 0-5) |
| [Default Constitution](Constitution-Default) | Operational ethics (Articles 1-11) |
| [Governance Mandate](Constitution-Mandate) | Who enforces the laws |
| [Harm Taxonomy](Constitution-Harm-Taxonomy) | Classification of potential harms |

---
See also: [Home](Home)
CONSTEOF

  # Map filenames to wiki page names
  declare -A const_pages=(
    ["asimov.constitution.md"]="Constitution-Asimov"
    ["default.constitution.md"]="Constitution-Default"
    ["demerzel-mandate.md"]="Constitution-Mandate"
    ["harm-taxonomy.md"]="Constitution-Harm-Taxonomy"
  )

  for file in "${REPO_ROOT}/constitutions/"*.md; do
    local basename filename page_name last_modified content title
    basename="$(basename "$file")"
    page_name="${const_pages[$basename]:-}"
    if [[ -z "$page_name" ]]; then
      continue
    fi

    last_modified=$(git -C "${REPO_ROOT}" log -1 --format=%ci -- "constitutions/${basename}" 2>/dev/null || echo "unknown")
    # Extract first H1 as title, fallback to filename
    title=$(grep -m1 '^# ' "$file" | sed 's/^# //' || echo "$basename")
    # Get content after the first H1 line
    content=$(tail -n +2 "$file")

    cat > "${WIKI_DIR}/${page_name}.md" <<PAGEEOF
<!-- Auto-generated from constitutions/${basename} -- do not edit manually -->

# ${title}

> Source: [\`constitutions/${basename}\`](${REPO_URL}/blob/master/constitutions/${basename})
> Last updated: ${last_modified}

${content}

---
See also: [Constitution Overview](Constitution) | [Home](Home)
PAGEEOF
  done
}
```

- **Time:** 3 minutes

### Step 1c: Persona page generation (index + detail pages)

- [ ] Add `generate_personas()` function to the script:

```bash
generate_personas() {
  # --- Persona index page ---
  {
    echo '<!-- Auto-generated from Demerzel repo -- do not edit manually -->'
    echo ''
    echo '# Persona Catalog'
    echo ''
    echo '| Persona | Role | Goal Directedness | Estimator |'
    echo '|---------|------|-------------------|-----------|'

    for file in "${REPO_ROOT}/personas/"*.persona.yaml; do
      local name version description role goal_dir estimator display_name
      name=$(yq -r '.name' "$file")
      role=$(yq -r '.role' "$file" | head -c 80)
      goal_dir=$(yq -r '.goal_directedness // "none"' "$file")
      estimator=$(yq -r '.estimator_pairing // "none"' "$file")
      # Capitalize first letter for display
      display_name="$(echo "$name" | sed 's/-/ /g; s/\b\(.\)/\u\1/g')"
      # Wiki page name: Persona-Display-Name (capitalize each word, keep hyphens)
      wiki_name="Persona-$(echo "$name" | sed 's/\b\(.\)/\u\1/g; s/ /-/g')"

      echo "| [${display_name}](${wiki_name}) | ${role} | ${goal_dir} | ${estimator} |"
    done

    echo ''
    echo '---'
    echo 'See also: [Home](Home)'
  } > "${WIKI_DIR}/Personas.md"

  # --- Individual persona pages ---
  for file in "${REPO_ROOT}/personas/"*.persona.yaml; do
    local name version description role domain goal_dir estimator display_name wiki_name
    local capabilities constraints voice_tone voice_verbosity voice_style last_modified

    name=$(yq -r '.name' "$file")
    version=$(yq -r '.version' "$file")
    description=$(yq -r '.description' "$file")
    role=$(yq -r '.role' "$file")
    domain=$(yq -r '.domain // "unspecified"' "$file")
    goal_dir=$(yq -r '.goal_directedness // "none"' "$file")
    estimator=$(yq -r '.estimator_pairing // "none"' "$file")
    voice_tone=$(yq -r '.voice.tone // "neutral"' "$file")
    voice_verbosity=$(yq -r '.voice.verbosity // "moderate"' "$file")
    voice_style=$(yq -r '.voice.style // "standard"' "$file")

    display_name="$(echo "$name" | sed 's/-/ /g; s/\b\(.\)/\u\1/g')"
    wiki_name="Persona-$(echo "$name" | sed 's/\b\(.\)/\u\1/g; s/ /-/g')"
    estimator_wiki="Persona-$(echo "$estimator" | sed 's/\b\(.\)/\u\1/g; s/ /-/g')"

    local basename_file
    basename_file="$(basename "$file")"
    last_modified=$(git -C "${REPO_ROOT}" log -1 --format=%ci -- "personas/${basename_file}" 2>/dev/null || echo "unknown")

    {
      echo "<!-- Auto-generated from personas/${basename_file} -- do not edit manually -->"
      echo ""
      echo "# ${display_name} (v${version})"
      echo ""
      echo "> ${description}"
      echo ">"
      echo "> Source: [\`personas/${basename_file}\`](${REPO_URL}/blob/master/personas/${basename_file})"
      echo ""
      echo "**Role:** ${role}"
      echo "**Domain:** ${domain}"
      echo "**Goal Directedness:** ${goal_dir}"
      echo "**Estimator Pairing:** [${estimator}](${estimator_wiki})"
      echo ""
      echo "## Capabilities"
      echo ""
      yq -r '.capabilities[]' "$file" | while read -r cap; do
        echo "- ${cap}"
      done
      echo ""
      echo "## Constraints"
      echo ""
      yq -r '.constraints[]' "$file" | while read -r con; do
        echo "- ${con}"
      done
      echo ""
      echo "## Voice"
      echo ""
      echo "- **Tone:** ${voice_tone}"
      echo "- **Verbosity:** ${voice_verbosity}"
      echo "- **Style:** ${voice_style}"
      echo ""
      echo "---"
      echo "See also: [Persona Catalog](Personas) | [Home](Home)"
    } > "${WIKI_DIR}/${wiki_name}.md"
  done
}
```

- **Time:** 5 minutes

### Step 1d: Policy page generation (index + detail pages)

- [ ] Add `generate_policies()` function to the script:

```bash
generate_policies() {
  # --- Policy index page ---
  {
    echo '<!-- Auto-generated from Demerzel repo -- do not edit manually -->'
    echo ''
    echo '# Policy Reference'
    echo ''
    echo '| Policy | Version | Description |'
    echo '|--------|---------|-------------|'

    for file in "${REPO_ROOT}/policies/"*.yaml; do
      local name version description display_name wiki_name
      name=$(yq -r '.name' "$file")
      version=$(yq -r '.version' "$file")
      description=$(yq -r '.description' "$file" | tr '\n' ' ' | head -c 100)
      display_name="$(echo "$name" | sed 's/-policy//; s/-/ /g; s/\b\(.\)/\u\1/g')"
      wiki_name="Policy-$(echo "$name" | sed 's/-policy//; s/\b\(.\)/\u\1/g; s/ /-/g')"

      echo "| [${display_name}](${wiki_name}) | ${version} | ${description} |"
    done

    echo ''
    echo '---'
    echo 'See also: [Home](Home)'
  } > "${WIKI_DIR}/Policies.md"

  # --- Individual policy pages ---
  for file in "${REPO_ROOT}/policies/"*.yaml; do
    local name version description effective_date display_name wiki_name basename_file last_modified

    name=$(yq -r '.name' "$file")
    version=$(yq -r '.version' "$file")
    description=$(yq -r '.description' "$file" | tr '\n' ' ')
    effective_date=$(yq -r '.effective_date // "unspecified"' "$file")
    display_name="$(echo "$name" | sed 's/-policy//; s/-/ /g; s/\b\(.\)/\u\1/g')"
    wiki_name="Policy-$(echo "$name" | sed 's/-policy//; s/\b\(.\)/\u\1/g; s/ /-/g')"
    basename_file="$(basename "$file")"
    last_modified=$(git -C "${REPO_ROOT}" log -1 --format=%ci -- "policies/${basename_file}" 2>/dev/null || echo "unknown")

    {
      echo "<!-- Auto-generated from policies/${basename_file} -- do not edit manually -->"
      echo ""
      echo "# ${display_name} Policy (v${version})"
      echo ""
      echo "> ${description}"
      echo ">"
      echo "> Source: [\`policies/${basename_file}\`](${REPO_URL}/blob/master/policies/${basename_file})"
      echo "> Effective: ${effective_date}"
      echo ""

      # Render top-level keys as sections (skip metadata keys)
      local keys
      keys=$(yq -r 'keys | .[]' "$file" | grep -vE '^(name|version|effective_date|description|scope|applies_to|references)$')

      for key in $keys; do
        local section_title
        section_title="$(echo "$key" | sed 's/_/ /g; s/\b\(.\)/\u\1/g')"
        echo "## ${section_title}"
        echo ""
        # Render the value — use yq to convert to a readable format
        # For objects/arrays, render as nested YAML block for readability
        local val_type
        val_type=$(yq -r ".${key} | type" "$file")
        if [[ "$val_type" == "!!seq" || "$val_type" == "array" ]]; then
          yq -r ".${key}[]" "$file" 2>/dev/null | while IFS= read -r item; do
            echo "- ${item}"
          done
        elif [[ "$val_type" == "!!map" || "$val_type" == "object" ]]; then
          # Render nested structure as indented content (up to 3 levels)
          yq -r ".${key} | to_entries[] | \"### \" + (.key | sub(\"_\"; \" \"; \"g\") | split(\" \") | map(select(. != \"\") | split(\"\") | .[0] |= ascii_upcase | join(\"\")) | join(\" \")) + \"\n\n\" + (if .value | type == \"!!seq\" then (.value[] | \"- \" + .) elif .value | type == \"!!map\" then (.value | to_entries[] | \"- **\" + .key + \":** \" + (.value | tostring)) else .value end)" "$file" 2>/dev/null || \
          yq -y ".${key}" "$file" | sed 's/^/    /'
        else
          yq -r ".${key}" "$file"
        fi
        echo ""
      done

      # References section
      local has_refs
      has_refs=$(yq -r '.references // empty | length' "$file" 2>/dev/null)
      if [[ -n "$has_refs" && "$has_refs" != "0" ]]; then
        echo "## References"
        echo ""
        yq -r '.references[]' "$file" | while IFS= read -r ref; do
          echo "- ${ref}"
        done
        echo ""
      fi

      echo "---"
      echo "See also: [Policy Reference](Policies) | [Home](Home)"
    } > "${WIKI_DIR}/${wiki_name}.md"
  done
}
```

- **Time:** 5 minutes

### Step 1e: Schema page generation

- [ ] Add `generate_schemas()` function to the script:

```bash
generate_schemas() {
  {
    echo '<!-- Auto-generated from Demerzel repo -- do not edit manually -->'
    echo ''
    echo '# Schema Reference'
    echo ''
    echo '## Core Schemas'
    echo ''
    echo '| Schema | Description |'
    echo '|--------|-------------|'

    for file in "${REPO_ROOT}/schemas/"*.json; do
      local basename_file title desc
      basename_file="$(basename "$file")"
      title=$(jq -r '.title // .["$id"] // "'"${basename_file}"'"' "$file")
      desc=$(jq -r '.description // "No description"' "$file")
      echo "| [\`${basename_file}\`](${REPO_URL}/blob/master/schemas/${basename_file}) | ${desc} |"
    done

    echo ''
    echo '## Contract Schemas'
    echo ''
    echo '| Schema | Description |'
    echo '|--------|-------------|'

    if [[ -d "${REPO_ROOT}/schemas/contracts" ]]; then
      for file in "${REPO_ROOT}/schemas/contracts/"*.json; do
        local basename_file title desc
        basename_file="$(basename "$file")"
        title=$(jq -r '.title // .["$id"] // "'"${basename_file}"'"' "$file")
        desc=$(jq -r '.description // "No description"' "$file")
        echo "| [\`${basename_file}\`](${REPO_URL}/blob/master/schemas/contracts/${basename_file}) | ${desc} |"
      done
    fi

    echo ''
    echo '---'
    echo 'See also: [Home](Home)'
  } > "${WIKI_DIR}/Schemas.md"
}
```

- **Time:** 3 minutes

### Step 1f: Contracts page generation

- [ ] Add `generate_contracts()` function to the script:

```bash
generate_contracts() {
  local contract_file="${REPO_ROOT}/contracts/galactic-protocol.md"

  if [[ ! -f "$contract_file" ]]; then
    echo "Warning: galactic-protocol.md not found, skipping Contracts page" >&2
    return
  fi

  local last_modified title content
  last_modified=$(git -C "${REPO_ROOT}" log -1 --format=%ci -- "contracts/galactic-protocol.md" 2>/dev/null || echo "unknown")
  title=$(grep -m1 '^# ' "$contract_file" | sed 's/^# //' || echo "Galactic Protocol")
  content=$(cat "$contract_file")

  cat > "${WIKI_DIR}/Contracts.md" <<CONTRACTEOF
<!-- Auto-generated from contracts/galactic-protocol.md -- do not edit manually -->

> Source: [\`contracts/galactic-protocol.md\`](${REPO_URL}/blob/master/contracts/galactic-protocol.md)
> Last updated: ${last_modified}

${content}

---
See also: [Home](Home)
CONTRACTEOF
}
```

- **Time:** 2 minutes

### Step 1g: Sidebar and Footer generation

- [ ] Add `generate_sidebar()` and `generate_footer()` functions, then add the main execution block:

```bash
generate_sidebar() {
  {
    echo '**[Home](Home)**'
    echo ''
    echo '**Constitution**'
    echo '- [Overview](Constitution)'
    echo '- [Asimov Laws](Constitution-Asimov)'
    echo '- [Default Constitution](Constitution-Default)'
    echo '- [Governance Mandate](Constitution-Mandate)'
    echo '- [Harm Taxonomy](Constitution-Harm-Taxonomy)'
    echo ''
    echo '**Personas**'
    echo '- [Catalog](Personas)'

    for file in "${REPO_ROOT}/personas/"*.persona.yaml; do
      local name display_name wiki_name
      name=$(yq -r '.name' "$file")
      display_name="$(echo "$name" | sed 's/-/ /g; s/\b\(.\)/\u\1/g')"
      wiki_name="Persona-$(echo "$name" | sed 's/\b\(.\)/\u\1/g; s/ /-/g')"
      echo "- [${display_name}](${wiki_name})"
    done

    echo ''
    echo '**Policies**'
    echo '- [Reference](Policies)'

    for file in "${REPO_ROOT}/policies/"*.yaml; do
      local name display_name wiki_name
      name=$(yq -r '.name' "$file")
      display_name="$(echo "$name" | sed 's/-policy//; s/-/ /g; s/\b\(.\)/\u\1/g')"
      wiki_name="Policy-$(echo "$name" | sed 's/-policy//; s/\b\(.\)/\u\1/g; s/ /-/g')"
      echo "- [${display_name}](${wiki_name})"
    done

    echo ''
    echo '**Technical**'
    echo '- [Schemas](Schemas)'
    echo '- [Galactic Protocol](Contracts)'
  } > "${WIKI_DIR}/_Sidebar.md"
}

generate_footer() {
  cat > "${WIKI_DIR}/_Footer.md" <<FOOTEREOF
---
*Auto-generated from [Demerzel repo](${REPO_URL}) on ${TIMESTAMP}. Do not edit manually -- changes will be overwritten.*
FOOTEREOF
}

# --- Main execution ---
echo "Generating wiki pages..."
generate_home
echo "  ✓ Home"
generate_constitutions
echo "  ✓ Constitutions"
generate_personas
echo "  ✓ Personas"
generate_policies
echo "  ✓ Policies"
generate_schemas
echo "  ✓ Schemas"
generate_contracts
echo "  ✓ Contracts"
generate_sidebar
echo "  ✓ Sidebar"
generate_footer
echo "  ✓ Footer"

page_count=$(find "${WIKI_DIR}" -name '*.md' | wc -l)
echo "Done. Generated ${page_count} wiki pages."
```

- **Time:** 3 minutes

### Step 1h: Make the script executable

- [ ] Run: `chmod +x .github/scripts/generate-wiki.sh`
- **Time:** 1 minute

---

## Phase 2: Workflow File

File: `.github/workflows/wiki-sync.yml`

### Step 2a: Create the workflow

- [ ] Create `.github/workflows/wiki-sync.yml` with the following content:

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
      - '.github/scripts/generate-wiki.sh'
  workflow_dispatch:

jobs:
  sync-wiki:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout main repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Checkout wiki repo
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository }}.wiki
          path: wiki
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Install tools
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y -qq jq
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

- **Time:** 3 minutes

---

## Phase 3: Testing

### Step 3a: Test with workflow_dispatch

- [ ] Push both files to master
- [ ] Go to GitHub → Actions → "Sync Wiki" → "Run workflow" → Run
- [ ] Verify the workflow completes successfully (green check)
- **Time:** 3 minutes

### Step 3b: Verify generated pages

- [ ] Check the wiki at `https://github.com/GuitarAlchemist/Demerzel/wiki`
- [ ] Verify the following pages exist and render correctly:
  - [ ] Home page with correct persona/policy counts
  - [ ] Constitution overview with links to all 4 constitution pages
  - [ ] Constitution-Asimov, Constitution-Default, Constitution-Mandate, Constitution-Harm-Taxonomy
  - [ ] Personas index with table of all 14 personas
  - [ ] At least 3 persona detail pages (Demerzel, Seldon, Skeptical Auditor)
  - [ ] Policies index with table of all 9 policies
  - [ ] At least 2 policy detail pages (Alignment, Kaizen)
  - [ ] Schemas page with core and contract schema tables
  - [ ] Contracts page with Galactic Protocol content
  - [ ] Sidebar navigation with all sections
  - [ ] Footer with timestamp
- [ ] Verify cross-links work (click persona estimator links, constitution links, source links)
- **Time:** 5 minutes

### Step 3c: Fix any rendering issues

- [ ] If any yq/jq commands produce unexpected output, adjust the generation script
- [ ] Re-run via workflow_dispatch to verify fixes
- **Time:** 5 minutes (if needed)

---

## Files Created

| File | Purpose |
|------|---------|
| `.github/workflows/wiki-sync.yml` | GitHub Actions workflow triggered on push to master |
| `.github/scripts/generate-wiki.sh` | Bash script generating ~40 wiki pages from governance artifacts |

## Files NOT Modified

No governance artifacts (personas, constitutions, policies, schemas, contracts) are modified by this plan. The generation script lives in `.github/` (CI infrastructure), not in the repo's governance artifact directories.

## Estimated Total Time

| Phase | Time |
|-------|------|
| Prerequisites (manual wiki creation) | 1 min |
| Phase 1: Generation script (steps 1a-1h) | 25 min |
| Phase 2: Workflow file | 3 min |
| Phase 3: Testing and verification | 13 min |
| **Total** | **~42 min** |
