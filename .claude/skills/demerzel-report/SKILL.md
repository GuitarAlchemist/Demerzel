---
name: demerzel-report
description: Post daily governance reports and knowledge digests to GitHub Discussions across all repos
---

# Demerzel Daily Report

Post governance reports (Demerzel) and knowledge digests (Seldon) to GitHub Discussions.

## Usage
`/demerzel report` — post today's report to all repos
`/demerzel report [repo]` — post to a specific repo only

## Report Types

### Demerzel Governance Report (Announcements category)
Posted to: **Demerzel** repo Discussions

Contents:
- Date, governance status summary
- Active directives and their status
- Reconnaissance findings (if harvest ran)
- Compliance status across repos
- Governance evolution highlights (promotion/deprecation candidates)
- Active Ralph Loops and their progress
- Any Zeroth Law concerns flagged

### Seldon Knowledge Digest (General category)
Posted to: **ga**, **tars**, **ix** repo Discussions (repo-specific content)

Contents:
- New experiential knowledge from PDCA cycles
- Cross-repo learnings available for teaching
- Domain-specific knowledge updates for that repo
- Knowledge transfer outcomes (what was taught, comprehension status)
- Recommended learning paths for agents in that repo

## How to Post

Uses `gh api graphql` to create discussions. Category IDs:

| Repo | Announcements | General |
|------|--------------|---------|
| Demerzel | `DIC_kwDORnMyyc4C4eDS` | `DIC_kwDORnMyyc4C4eDT` |
| ga | `DIC_kwDOGhMFHs4C4NRa` | `DIC_kwDOGhMFHs4C4NRb` |
| tars | `DIC_kwDOOB9ph84C4NRs` | `DIC_kwDOOB9ph84C4NRt` |
| ix | `DIC_kwDORk4dlc4C4eDe` | `DIC_kwDORk4dlc4C4eDf` |

Repository node IDs:

| Repo | Node ID |
|------|---------|
| Demerzel | `R_kgDORnMyyQ` |
| ga | `R_kgDOGhMFHg` |
| tars | `R_kgDOOB9phw` |
| ix | `R_kgDORk4dlQ` |

### GraphQL Mutation Template
```graphql
mutation {
  createDiscussion(input: {
    repositoryId: "<REPO_NODE_ID>",
    categoryId: "<CATEGORY_ID>",
    title: "🤖 <Reporter> Report — <DATE>",
    body: "<MARKDOWN_CONTENT>"
  }) {
    discussion { url }
  }
}
```

## Scheduling

**In-session (ephemeral):**
```
CronCreate("23 8 * * *", "/demerzel report")
```
Run after the harvest (scheduled at 8:17) so the report includes fresh data.

**Persistent:**
```bash
claude --print "Run /demerzel report" --cwd /path/to/Demerzel
```

## Integration
- Runs AFTER `/demerzel harvest` — uses harvest results as report content
- References governance evolution log for trends
- References active loop states for progress updates
- Seldon's digest references knowledge-state files for teaching status

## Source
`constitutions/demerzel-mandate.md` Section 4 (Accountability), `policies/streeling-policy.yaml`
