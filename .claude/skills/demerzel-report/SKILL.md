---
name: demerzel-report
description: Post daily governance reports and knowledge digests to GitHub Discussions and Discord across all repos
---

# Demerzel Daily Report

Post governance reports (Demerzel) and knowledge digests (Seldon) to GitHub Discussions and Discord.

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

## Discord Posting

In addition to GitHub Discussions, post a rich embed summary to Discord.

**Channel:** `#general` on Stephane Pareilleux's server
- Guild ID: `1484806750682218700`
- Channel ID: `1484806751554506854`

### How to Post to Discord

1. Read the bot token from `~/.claude/channels/discord/.env` (DISCORD_BOT_TOKEN)
2. Write the embed JSON to a temp file (avoids shell escaping issues)
3. POST to `https://discord.com/api/v10/channels/1484806751554506854/messages`
4. Clean up the temp file

```bash
TOKEN=$(grep DISCORD_BOT_TOKEN ~/.claude/channels/discord/.env | cut -d= -f2)
curl -s -X POST "https://discord.com/api/v10/channels/1484806751554506854/messages" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d @tmp-discord-msg.json
rm tmp-discord-msg.json
```

### Embed Templates

**Cycle Report:** Title with cycle number, color `5025616` (teal), fields for tasks/duration/health scores/highlights/next steps.

**Seldon/Streeling Report:** Three embeds — Department Overview (color `7506394` purple), Research Programs (color `15844367` gold), Curriculum (color `3066993` green). Use inline fields for department grid.

**Governance Alert:** Color `15158332` (red) for urgent, `16776960` (yellow) for warnings. Include constitutional article reference and recommended action.

### When to Post

- After every driver cycle completes (cycle report)
- After `/demerzel harvest` (knowledge digest)
- On governance alerts (constitutional concerns, paradigm shifts)
- On Seldon teaching events (knowledge transfer summaries)

## Source
`constitutions/demerzel-mandate.md` Section 4 (Accountability), `policies/streeling-policy.yaml`
