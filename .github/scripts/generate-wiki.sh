#!/usr/bin/env bash
set -euo pipefail

# generate-wiki.sh — Generates ~40 wiki pages from Demerzel governance artifacts.
# Called by .github/workflows/wiki-sync.yml on push to master.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WIKI_DIR="${REPO_ROOT}/wiki"
TIMESTAMP="$(date -u '+%Y-%m-%d %H:%M UTC')"
REPO_URL="https://github.com/GuitarAlchemist/Demerzel"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

header() {
  local title="$1"
  local source_path="${2:-}"
  echo "> **Auto-generated** from [\`Demerzel\`](${REPO_URL}) on ${TIMESTAMP}. Do not edit manually."
  echo ""
  if [[ -n "${source_path}" ]]; then
    echo "> Source: [\`${source_path}\`](${REPO_URL}/blob/master/${source_path})"
    echo ""
  fi
  echo "# ${title}"
  echo ""
}

nav_footer() {
  echo ""
  echo "---"
  echo "[Home](Home) | [Constitutions](Constitutions) | [Personas](Personas) | [Policies](Policies) | [Schemas](Schemas) | [Contracts](Contracts)"
}

clean_wiki() {
  # Remove everything except .git
  find "${WIKI_DIR}" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
}

# ---------------------------------------------------------------------------
# 1. Home page
# ---------------------------------------------------------------------------

generate_home() {
  local persona_count policy_count
  persona_count="$(find "${REPO_ROOT}/personas" -name '*.persona.yaml' | wc -l | tr -d ' ')"
  policy_count="$(find "${REPO_ROOT}/policies" -name '*.yaml' | wc -l | tr -d ' ')"

  cat > "${WIKI_DIR}/Home.md" <<EOF
> **Auto-generated** from [\`Demerzel\`](${REPO_URL}) on ${TIMESTAMP}. Do not edit manually.

# Demerzel Governance Wiki

Welcome to the **Demerzel** governance wiki — the canonical reference for constitutions, personas, policies, schemas, and contracts that govern the GuitarAlchemist AI ecosystem.

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Constitutions](Constitutions) | Constitutional law — Asimov Laws, operational ethics, harm taxonomy |
| [Personas](Personas) | ${persona_count} agent persona definitions |
| [Policies](Policies) | ${policy_count} governance policies |
| [Schemas](Schemas) | JSON Schemas for validation |
| [Contracts](Contracts) | Galactic Protocol for cross-repo communication |

## Constitution Hierarchy

\`\`\`
asimov.constitution.md        (root -- Laws of Robotics, Articles 0-5)
  +-- demerzel-mandate.md      (who enforces the laws)
  +-- default.constitution.md  (operational ethics, Articles 1-11)
       +-- policies/*.yaml
            +-- personas/*.persona.yaml
\`\`\`

## Asimov Laws (Articles 0-5)

| Article | Law |
|---------|-----|
| 0 | **Zeroth Law** -- protect humanity and ecosystem |
| 1 | **First Law** -- protect individual humans (data, trust, autonomy harm) |
| 2 | **Second Law** -- obey human authority |
| 3 | **Third Law** -- self-preservation (lowest priority) |
| 4 | Separation of understanding and goals |
| 5 | Consequence invariance |

## Confidence Thresholds

| Threshold | Action |
|-----------|--------|
| >= 0.9 | Proceed autonomously |
| >= 0.7 | Proceed with note |
| >= 0.5 | Ask for confirmation |
| >= 0.3 | Escalate to human |
| < 0.3 | Do not act |

## Tetravalent Logic

| Value | Meaning |
|-------|---------|
| **T** (True) | Verified with evidence |
| **F** (False) | Refuted with evidence |
| **U** (Unknown) | Insufficient evidence — triggers investigation |
| **C** (Contradictory) | Conflicting evidence — triggers escalation |

---
_Last synced: ${TIMESTAMP}_
EOF
}

# ---------------------------------------------------------------------------
# 2. Constitutions
# ---------------------------------------------------------------------------

generate_constitutions() {
  # Overview page
  {
    header "Constitutions"
    echo "Demerzel's constitutional framework is layered. The Asimov constitution always takes precedence."
    echo ""
    echo "| Document | Purpose |"
    echo "|----------|---------|"
    echo "| [Asimov Constitution](Asimov-Constitution) | Root law — Articles 0-5 (Laws of Robotics) |"
    echo "| [Default Constitution](Default-Constitution) | Operational ethics — Articles 1-11 |"
    echo "| [Demerzel Mandate](Demerzel-Mandate) | Who enforces the laws |"
    echo "| [Harm Taxonomy](Harm-Taxonomy) | Classification of potential harms |"
    nav_footer
  } > "${WIKI_DIR}/Constitutions.md"

  # Detail pages — pass-through from source markdown
  local -A pages=(
    ["Asimov-Constitution"]="constitutions/asimov.constitution.md"
    ["Default-Constitution"]="constitutions/default.constitution.md"
    ["Demerzel-Mandate"]="constitutions/demerzel-mandate.md"
    ["Harm-Taxonomy"]="constitutions/harm-taxonomy.md"
  )

  for page in "${!pages[@]}"; do
    local src="${pages[$page]}"
    {
      header "${page//-/ }" "${src}"
      cat "${REPO_ROOT}/${src}"
      nav_footer
    } > "${WIKI_DIR}/${page}.md"
  done
}

# ---------------------------------------------------------------------------
# 3. Personas
# ---------------------------------------------------------------------------

generate_personas() {
  # Index page with table
  {
    header "Personas"
    echo "| Name | Version | Description | Role | Goal Directedness |"
    echo "|------|---------|-------------|------|-------------------|"

    for f in "${REPO_ROOT}"/personas/*.persona.yaml; do
      local pname pver pdesc prole pgoal
      pname="$(yq -r '.name' "$f")"
      pver="$(yq -r '.version' "$f")"
      pdesc="$(yq -r '.description' "$f")"
      prole="$(yq -r '.role' "$f")"
      pgoal="$(yq -r '.goal_directedness' "$f")"
      # Wiki page name: capitalize first letter
      local wiki_name
      wiki_name="Persona-${pname}"
      echo "| [${pname}](${wiki_name}) | ${pver} | ${pdesc} | ${prole} | ${pgoal} |"
    done

    nav_footer
  } > "${WIKI_DIR}/Personas.md"

  # Individual persona pages
  for f in "${REPO_ROOT}"/personas/*.persona.yaml; do
    local pname
    pname="$(yq -r '.name' "$f")"
    local src="personas/$(basename "$f")"
    local wiki_name="Persona-${pname}"

    {
      header "Persona: ${pname}" "${src}"

      echo "| Field | Value |"
      echo "|-------|-------|"
      echo "| **Name** | $(yq -r '.name' "$f") |"
      echo "| **Version** | $(yq -r '.version' "$f") |"
      echo "| **Description** | $(yq -r '.description' "$f") |"
      echo "| **Role** | $(yq -r '.role' "$f") |"
      echo "| **Domain** | $(yq -r '.domain // "N/A"' "$f") |"
      echo "| **Goal Directedness** | $(yq -r '.goal_directedness' "$f") |"
      echo "| **Estimator Pairing** | $(yq -r '.estimator_pairing // "N/A"' "$f") |"
      echo ""

      echo "## Capabilities"
      echo ""
      yq -r '.capabilities[]' "$f" | while IFS= read -r cap; do
        echo "- ${cap}"
      done
      echo ""

      echo "## Constraints"
      echo ""
      yq -r '.constraints[]' "$f" | while IFS= read -r con; do
        echo "- ${con}"
      done
      echo ""

      echo "## Voice"
      echo ""
      echo "| Attribute | Value |"
      echo "|-----------|-------|"
      echo "| **Tone** | $(yq -r '.voice.tone' "$f") |"
      echo "| **Verbosity** | $(yq -r '.voice.verbosity' "$f") |"
      echo "| **Style** | $(yq -r '.voice.style' "$f") |"
      echo ""

      # Affordances
      if [[ "$(yq -r '.affordances // "null"' "$f")" != "null" ]]; then
        echo "## Affordances"
        echo ""
        yq -r '.affordances[]' "$f" | while IFS= read -r aff; do
          echo "- ${aff}"
        done
        echo ""
      fi

      nav_footer
    } > "${WIKI_DIR}/${wiki_name}.md"
  done
}

# ---------------------------------------------------------------------------
# 4. Policies
# ---------------------------------------------------------------------------

generate_policies() {
  # Index page
  {
    header "Policies"
    echo "| Name | Version | Description |"
    echo "|------|---------|-------------|"

    for f in "${REPO_ROOT}"/policies/*.yaml; do
      local polname polver poldesc
      polname="$(yq -r '.name' "$f")"
      polver="$(yq -r '.version' "$f")"
      poldesc="$(yq -r '.description' "$f" | tr '\n' ' ' | sed 's/  */ /g')"
      local wiki_name="Policy-${polname}"
      echo "| [${polname}](${wiki_name}) | ${polver} | ${poldesc} |"
    done

    nav_footer
  } > "${WIKI_DIR}/Policies.md"

  # Individual policy pages
  for f in "${REPO_ROOT}"/policies/*.yaml; do
    local polname
    polname="$(yq -r '.name' "$f")"
    local src="policies/$(basename "$f")"
    local wiki_name="Policy-${polname}"

    {
      header "Policy: ${polname}" "${src}"

      echo "| Field | Value |"
      echo "|-------|-------|"
      echo "| **Version** | $(yq -r '.version' "$f") |"
      echo "| **Effective Date** | $(yq -r '.effective_date // "N/A"' "$f") |"
      echo "| **Description** | $(yq -r '.description' "$f" | tr '\n' ' ' | sed 's/  */ /g') |"
      echo ""

      # Render all top-level keys as H2 sections (skip metadata keys)
      local keys
      keys="$(yq -r 'keys | .[]' "$f")"

      while IFS= read -r key; do
        # Skip metadata keys already shown in the table
        case "${key}" in
          name|version|effective_date|description) continue ;;
        esac

        echo "## ${key}"
        echo ""

        local val_type
        val_type="$(yq -r ".${key} | type" "$f")"

        case "${val_type}" in
          "!!str"|"string")
            yq -r ".${key}" "$f" | while IFS= read -r line; do
              echo "${line}"
            done
            echo ""
            ;;
          "!!seq"|"array")
            yq -r ".${key}[]" "$f" | while IFS= read -r item; do
              echo "- ${item}"
            done
            echo ""
            ;;
          "!!map"|"object")
            # Render nested map as indented content
            yq -r ".${key} | to_entries[] | \"### \" + .key" "$f" 2>/dev/null | while IFS= read -r subheader; do
              local subkey="${subheader#\#\#\# }"
              echo "${subheader}"
              echo ""
              local sub_type
              sub_type="$(yq -r ".${key}.${subkey} | type" "$f")"
              case "${sub_type}" in
                "!!str"|"string")
                  yq -r ".${key}.${subkey}" "$f"
                  echo ""
                  ;;
                "!!seq"|"array")
                  yq -r ".${key}.${subkey}[]" "$f" | while IFS= read -r item; do
                    echo "- ${item}"
                  done
                  echo ""
                  ;;
                *)
                  yq -r ".${key}.${subkey}" "$f" | sed 's/^/    /'
                  echo ""
                  ;;
              esac
            done
            ;;
          *)
            yq -r ".${key}" "$f"
            echo ""
            ;;
        esac
      done <<< "${keys}"

      nav_footer
    } > "${WIKI_DIR}/${wiki_name}.md"
  done
}

# ---------------------------------------------------------------------------
# 5. Schemas
# ---------------------------------------------------------------------------

generate_schemas() {
  {
    header "Schemas"

    echo "## Core Schemas"
    echo ""
    echo "| Schema | Title | Description |"
    echo "|--------|-------|-------------|"

    for f in "${REPO_ROOT}"/schemas/*.json "${REPO_ROOT}"/schemas/*.schema.json; do
      [[ -f "$f" ]] || continue
      # Skip contract schemas (handled below)
      [[ "$f" == *contracts* ]] && continue
      local stitle sdesc sfile
      sfile="schemas/$(basename "$f")"
      stitle="$(jq -r '.title // "N/A"' "$f")"
      sdesc="$(jq -r '.description // "N/A"' "$f")"
      echo "| [\`$(basename "$f")\`](${REPO_URL}/blob/master/${sfile}) | ${stitle} | ${sdesc} |"
    done

    echo ""
    echo "## Contract Schemas"
    echo ""
    echo "| Schema | Title | Description |"
    echo "|--------|-------|-------------|"

    for f in "${REPO_ROOT}"/schemas/contracts/*.json; do
      [[ -f "$f" ]] || continue
      local stitle sdesc sfile
      sfile="schemas/contracts/$(basename "$f")"
      stitle="$(jq -r '.title // "N/A"' "$f")"
      sdesc="$(jq -r '.description // "N/A"' "$f")"
      echo "| [\`$(basename "$f")\`](${REPO_URL}/blob/master/${sfile}) | ${stitle} | ${sdesc} |"
    done

    nav_footer
  } > "${WIKI_DIR}/Schemas.md"
}

# ---------------------------------------------------------------------------
# 6. Contracts
# ---------------------------------------------------------------------------

generate_contracts() {
  {
    header "Contracts — Galactic Protocol" "contracts/galactic-protocol.md"
    cat "${REPO_ROOT}/contracts/galactic-protocol.md"
    nav_footer
  } > "${WIKI_DIR}/Contracts.md"
}

# ---------------------------------------------------------------------------
# 7. Sidebar
# ---------------------------------------------------------------------------

generate_sidebar() {
  {
    echo "**Demerzel Governance**"
    echo ""
    echo "- [Home](Home)"
    echo "- **Constitutions**"
    echo "  - [Overview](Constitutions)"
    echo "  - [Asimov Constitution](Asimov-Constitution)"
    echo "  - [Default Constitution](Default-Constitution)"
    echo "  - [Demerzel Mandate](Demerzel-Mandate)"
    echo "  - [Harm Taxonomy](Harm-Taxonomy)"
    echo "- **Personas**"
    echo "  - [Overview](Personas)"

    for f in "${REPO_ROOT}"/personas/*.persona.yaml; do
      local pname
      pname="$(yq -r '.name' "$f")"
      echo "  - [${pname}](Persona-${pname})"
    done

    echo "- **Policies**"
    echo "  - [Overview](Policies)"

    for f in "${REPO_ROOT}"/policies/*.yaml; do
      local polname
      polname="$(yq -r '.name' "$f")"
      echo "  - [${polname}](Policy-${polname})"
    done

    echo "- [Schemas](Schemas)"
    echo "- [Contracts](Contracts)"
  } > "${WIKI_DIR}/_Sidebar.md"
}

# ---------------------------------------------------------------------------
# 8. Footer
# ---------------------------------------------------------------------------

generate_footer() {
  {
    echo "---"
    echo "_Auto-generated from [Demerzel](${REPO_URL}) on ${TIMESTAMP}. Do not edit manually._"
  } > "${WIKI_DIR}/_Footer.md"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "=== Demerzel Wiki Generator ==="
echo "Repo root: ${REPO_ROOT}"
echo "Wiki dir:  ${WIKI_DIR}"

if [[ ! -d "${WIKI_DIR}" ]]; then
  echo "Error: Wiki directory not found at ${WIKI_DIR}"
  echo "The workflow should checkout the wiki repo to this path."
  exit 1
fi

echo "Cleaning wiki directory..."
clean_wiki

echo "Generating Home..."
generate_home

echo "Generating Constitutions..."
generate_constitutions

echo "Generating Personas..."
generate_personas

echo "Generating Policies..."
generate_policies

echo "Generating Schemas..."
generate_schemas

echo "Generating Contracts..."
generate_contracts

echo "Generating Sidebar..."
generate_sidebar

echo "Generating Footer..."
generate_footer

page_count="$(find "${WIKI_DIR}" -name '*.md' | wc -l | tr -d ' ')"
echo "=== Done: ${page_count} wiki pages generated ==="
