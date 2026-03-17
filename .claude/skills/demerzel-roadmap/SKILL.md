---
name: demerzel-roadmap
description: Manage the GuitarAlchemist ecosystem roadmap — create/prioritize/assign/track work items across all repos via GitHub Projects and Issues
---

# Demerzel Roadmap — Product & Project Management

Demerzel manages the ecosystem roadmap through GitHub Projects and Issues. She creates work items, prioritizes them, assigns to repos, tracks progress, and closes completed work.

## Usage
`/demerzel roadmap` — show current roadmap status
`/demerzel roadmap create [title] [repo]` — create a new work item
`/demerzel roadmap prioritize` — re-prioritize based on governance evolution
`/demerzel roadmap scan` — scan all repos for untracked work
`/demerzel roadmap close [issue]` — close with evidence

## Project Board
**https://github.com/orgs/GuitarAlchemist/projects/2** (Demerzel Governance)

## How to Create Issues

### On any repo:
```bash
TOKEN="$GITHUB_PAT"
GH_TOKEN=$TOKEN gh issue create --repo GuitarAlchemist/<repo> \
  --title "Issue title" \
  --body "Description with governance references"
```

### Add to project board:
```bash
# Get issue node ID
ISSUE_ID=$(GH_TOKEN=$TOKEN gh api graphql -f query='query {
  repository(owner:"GuitarAlchemist", name:"<repo>") {
    issue(number: <num>) { id }
  }
}' --jq '.data.repository.issue.id')

# Add to project
GH_TOKEN=$TOKEN gh api graphql -f query="mutation {
  addProjectV2ItemById(input: {
    projectId: \"PVT_kwDOBbiyps4BR3QU\",
    contentId: \"$ISSUE_ID\"
  }) { item { id } }
}"
```

## Prioritization Criteria

Based on governance evolution and meta-compounding:

1. **Critical:** Constitutional violations, Zeroth Law concerns, security gaps
2. **High:** Governance gaps (uncovered repos, missing tests), active Ralph Loops
3. **Medium:** Framework improvements, knowledge expansion, new features
4. **Low:** Nice-to-have enhancements, cleanup, documentation

## Roadmap Scan Protocol

When scanning for untracked work:
1. Check git logs across ix/tars/ga for recent significant commits
2. Cross-reference with open issues — any completed work without closure?
3. Check governance evolution log — any promotion/deprecation candidates?
4. Review meta-compounding proposals — any with high confidence?
5. Create issues for anything untracked

## Cross-Repo Issue Management

| Repo | Issues URL | Focus |
|------|-----------|-------|
| Demerzel | https://github.com/GuitarAlchemist/Demerzel/issues | Governance framework |
| ix | https://github.com/GuitarAlchemist/ix/issues | ML tools, MCP servers |
| tars | https://github.com/GuitarAlchemist/tars/issues | Reasoning, grammars, AI functions |
| ga | https://github.com/GuitarAlchemist/ga/issues | Music chatbot, domain logic |

## Automated Workflows

| Workflow | Schedule | What it does |
|----------|----------|-------------|
| `streeling-daily.yml` | Mon-Fri 8:17 AM | Harvest + compounding + reports |
| `demerzel-autofix.yml` | Mon-Fri 9:17 AM | Scan/close Demerzel issues |
| `demerzel-cross-repo-issues.yml` | Mon-Fri 9:47 AM | Scan/create cross-repo issues |
| `project-automation.yml` | On new issues | Auto-add to project board |
| `ga-chatbot-discussions.yml` | On new discussions | Answer music theory questions |

## Token Reference
Project ID: `PVT_kwDOBbiyps4BR3QU`
PAT secret: `PAT_TOKEN` (in repo secrets)

## Source
`constitutions/demerzel-mandate.md` (governance authority), `policies/autonomous-loop-policy.yaml` (work execution)
