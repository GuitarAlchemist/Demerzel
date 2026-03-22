---
name: demerzel-report
description: Generate governance dashboard reports with stories, drill-downs, and multi-format output — terminal, Discord, or markdown file
---

# Demerzel Governance Dashboard Report

Generate comprehensive governance reports covering beliefs, conscience, Streeling University, cross-repo health, evolution activity, and open issues. Supports narrative "stories" for notable events and drill-down sub-commands for focused views.

## Usage

```
/demerzel report                    — full dashboard to terminal
/demerzel report --format=discord   — post dashboard embed to Discord
/demerzel report --format=markdown  — write dashboard to state/reports/{date}-dashboard.md
/demerzel report beliefs            — drill-down: belief state detail
/demerzel report conscience         — drill-down: conscience health detail
/demerzel report streeling          — drill-down: Streeling University detail
/demerzel report health             — drill-down: cross-repo integration health
```

## Full Dashboard Sections

The full dashboard aggregates all sections into a single view. Each section can also be accessed individually via drill-down commands.

### 1. Belief State Summary

**Source:** `state/beliefs/*.belief.json`

Collect and summarize:
- **Truth value distribution:** count of T, F, U, C across all active beliefs
- **Staleness check:** beliefs whose `last_updated` is older than 7 days — flag as potentially stale
- **Confidence distribution:** histogram buckets [0.0-0.3), [0.3-0.5), [0.5-0.7), [0.7-0.9), [0.9-1.0]
- **Average confidence:** weighted mean across all beliefs
- **Archived count:** number of beliefs in `state/beliefs/archived/`

Output format:
```
BELIEFS                          T:3  F:0  U:1  C:0
  Confidence: avg 0.87 | [>=0.9]: 2  [0.7-0.9]: 1  [0.5-0.7]: 1  [<0.5]: 0
  Staleness:  0 stale (>7d)  |  1 archived
```

### 2. Conscience Health

**Source:** `state/conscience/signals/*.signal.json`, `state/conscience/regrets/*.regret.json`, `state/conscience/patterns/*.pattern.json`, `state/conscience/digests/*.digest.json`

Collect and summarize:
- **Signals:** total count, count by type (constitutional, stale-action, confidence, harm-proximity, silence, delegation, remediation)
- **Resolved vs unresolved signals:** signals with `resolved: true` vs open
- **Regrets:** total count, resolved vs unresolved
- **Patterns detected:** count, statuses (detected/investigating/addressed/monitoring)
- **Moral sensitivity score:** if available in latest digest, report it; otherwise mark U
- **Latest digest date:** when was the last daily self-reflection?

Output format:
```
CONSCIENCE                       signals: 5 (3 resolved, 2 open)
  Types: stale-action:2  harm-proximity:1  silence:1  remediation:1
  Regrets: 1 (0 resolved)  |  Patterns: 0 detected
  Moral sensitivity: 0.72  |  Last digest: 2026-03-23
```

### 3. Streeling University Status

**Source:** `state/streeling/university.json`, `state/streeling/departments/`, `state/streeling/research-cycles/`, `state/streeling/courses/`, `state/streeling/course-productions/`, `state/streeling/research/`

Collect and summarize:
- **Department count:** from `university.json` departments array
- **Department list:** names of all departments
- **Research cycles run:** count of files in `state/streeling/research-cycles/`
- **Courses produced:** count of files in `state/streeling/courses/`
- **Course productions:** count of files in `state/streeling/course-productions/`
- **Research papers:** count of files in `state/streeling/research/`
- **Weight evolution:** if department weight files exist, show latest weights; otherwise note "weights not yet tracked"

Output format:
```
STREELING UNIVERSITY             13 departments | chancellor: seldon
  Research cycles: 4  |  Courses: 23  |  Productions: 12
  Research papers: 8  |  Founded: 2026-03-18
  Departments: music, guitar-studies, musicology, mathematics, physics,
               computer-science, product-management, futurology, philosophy,
               cognitive-science, guitar-alchemist-academy, world-music-languages,
               psychohistory
```

### 4. Cross-Repo Health

**Source:** `state/beliefs/*consumer-repo*.belief.json`, `state/beliefs/*integration*.belief.json`

Collect and summarize:
- **Per repo (ix, tars, ga):** integration status belief truth value and confidence
- **Submodule freshness:** if belief mentions submodule commit counts, surface them
- **Governance adoption:** which repos have state/ directories, CLAUDE.md governance sections, persona definitions
- **Overall health:** GREEN (all T, confidence >= 0.7), YELLOW (any U or confidence < 0.7), RED (any F or C)

Output format:
```
CROSS-REPO HEALTH                overall: GREEN
  ix:   T (0.90) — submodule current, 83 governance tests
  tars: T (0.90) — submodule current, grammar-constrained generation
  ga:   T (0.90) — submodule current, 7 agent personas
```

### 5. Evolution Activity

**Source:** `state/evolution/*.evolution.json`

Collect and summarize:
- **Total tracked artifacts:** count of evolution files
- **Recent events:** events from the last 7 days across all evolution files
- **Promotion candidates:** artifacts with promotion-related events or recommendations
- **Deprecation candidates:** artifacts flagged for deprecation
- **Citation leaders:** top 3 artifacts by citation count

Output format:
```
EVOLUTION                        6 artifacts tracked
  Recent events (7d): 3 events across 2 artifacts
  Promotions pending: 0  |  Deprecations pending: 0
  Top cited: alignment-policy (12), asimov-constitution (8), default-constitution (6)
```

### 6. Open Issues Summary

**Source:** GitHub API via `gh issue list`

Run: `gh issue list --repo GuitarAlchemist/Demerzel --state open --limit 10 --json number,title,labels,createdAt`

Collect and summarize:
- **Total open issues:** count
- **By label:** group by label if present
- **Recent (last 7 days):** highlight newly opened issues
- **Stale (>30 days):** flag old issues with no recent activity

Output format:
```
GITHUB ISSUES                    12 open
  Recent (7d): #73 Dashboard reports, #71 Staleness policy
  Stale (>30d): none
  Labels: enhancement:5  governance:3  bug:1  unlabeled:3
```

## Stories — Narrative Summaries

After the dashboard sections, generate a "Stories" section highlighting notable events. Stories are short narrative paragraphs (2-3 sentences) describing significant changes. Scan for:

1. **New courses published** — check `state/streeling/courses/` for files created in the last 7 days
2. **Conscience signals resolved** — signals that moved to `resolved: true` recently
3. **Belief state changes** — beliefs whose `truth_value` changed (especially F->T or T->F)
4. **Weight shifts** — department weights that changed significantly (>10%)
5. **Evolution milestones** — artifacts that crossed citation thresholds or changed recommendation
6. **Regrets logged** — new regrets are always story-worthy (lessons learned)
7. **Cross-repo events** — new directives sent or compliance reports received
8. **Research cycle completions** — research cycles that produced findings

Story format:
```
STORIES

  [Conscience] Stale-action signal sig-stale-action-2026-03-17-002 was resolved
  after submodule updates brought all three consumer repos current. The original
  signal flagged 142-commit drift in ix — now addressed.

  [Streeling] 5 new courses published across guitar-studies and world-music-languages
  departments, expanding the curriculum to 23 total courses. Research cycle RC-004
  produced findings on modal interchange patterns.

  [Evolution] The autonomous-driver artifact logged its first compounding cycle
  event, marking the transition from experimental to monitored status.
```

If no notable events are found, output: `STORIES: No notable events in the last 7 days.`

## Drill-Down Commands

### `/demerzel report beliefs`

Expanded belief detail:
- List every active belief with: proposition (truncated to 80 chars), truth_value, confidence, last_updated, staleness flag
- Show archived beliefs count and reasons
- Show belief change history (previous_value -> current value)
- Confidence calibration assessment: are high-confidence beliefs verified? Are low-confidence beliefs being investigated?

### `/demerzel report conscience`

Expanded conscience detail:
- List every signal with: id, type, severity, date, resolved status, article reference
- List every regret with: id, summary, resolved status, lessons learned
- List every pattern with: id, status, signal count
- Show latest digest summary
- Show pre-mortem records if any exist in `state/conscience/pre-mortems/`
- Trend: signal frequency over time (increasing/decreasing/stable)

### `/demerzel report streeling`

Expanded Streeling detail:
- Per-department breakdown: research cycles run, courses produced, research papers, current weight
- Curriculum reference status from `state/streeling/curriculum-references.json`
- Recent course list with titles and production dates
- Research cycle results summary
- Department creation timeline

### `/demerzel report health`

Expanded cross-repo health:
- Per-repo detail: submodule commit hash, governance test count, persona count, state directory contents
- Galactic Protocol status: recent directives and compliance reports
- Belief evidence detail for each repo's integration status
- Recommendations for repos needing attention

## Output Formats

### Terminal (default)

Plain text with section headers, aligned columns, and box-drawing characters for visual structure. Use the output formats shown above in each section.

Full terminal output structure:
```
╔══════════════════════════════════════════════════════════════╗
║  DEMERZEL GOVERNANCE DASHBOARD — 2026-03-22                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [Beliefs section]                                           ║
║  [Conscience section]                                        ║
║  [Streeling section]                                         ║
║  [Cross-Repo section]                                        ║
║  [Evolution section]                                         ║
║  [GitHub Issues section]                                     ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  STORIES                                                     ║
║  [narrative paragraphs]                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Discord (`--format=discord`)

Post a rich embed to Discord channel `1484806751554506854` (guild `1484806750682218700`).

**Embed structure:** Multiple embeds in a single message:

1. **Dashboard Header** — color `5025616` (teal)
   - Title: "Demerzel Governance Dashboard — {date}"
   - Fields: one inline field per dashboard section with key metrics

2. **Stories** — color `7506394` (purple)
   - Title: "Notable Events"
   - Description: narrative story paragraphs

3. **Action Items** — color `15844367` (gold), only if there are stale beliefs, open signals, or stale issues
   - Title: "Needs Attention"
   - Fields: items requiring action

**Discord posting method:**
1. Read bot token from `~/.claude/channels/discord/.env` (DISCORD_BOT_TOKEN)
2. Write embed JSON to a temp file
3. POST to `https://discord.com/api/v10/channels/1484806751554506854/messages`
4. Clean up temp file
5. Include clickable GitHub links for every referenced artifact (issue, PR, discussion)

```bash
TOKEN=$(grep DISCORD_BOT_TOKEN ~/.claude/channels/discord/.env | cut -d= -f2)
curl -s -X POST "https://discord.com/api/v10/channels/1484806751554506854/messages" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/demerzel-dashboard-embed.json
rm /tmp/demerzel-dashboard-embed.json
```

**Link requirements:** Every artifact mentioned in Discord must include a clickable link:
- Issues: `https://github.com/GuitarAlchemist/Demerzel/issues/{N}`
- Files: `https://github.com/GuitarAlchemist/Demerzel/blob/master/{path}`
- Discussions: link from `gh api` response

### Markdown (`--format=markdown`)

Write a full markdown report to `state/reports/{date}-dashboard.md`. Create the `state/reports/` directory if it does not exist.

Use proper markdown headers, tables, and code blocks. Include all dashboard sections, stories, and a metadata footer with generation timestamp and data sources read.

## State Maintenance (MANDATORY)

### Before Reporting
1. Read ALL files from `state/beliefs/` (excluding `archived/` subdirectory for main counts)
2. Read ALL files from `state/conscience/signals/`, `state/conscience/regrets/`, `state/conscience/patterns/`, `state/conscience/digests/`
3. Read `state/streeling/university.json` and list `state/streeling/courses/`, `state/streeling/research-cycles/`, `state/streeling/course-productions/`, `state/streeling/research/`
4. Read ALL files from `state/evolution/`
5. Read integration beliefs for cross-repo health
6. Run `gh issue list` for GitHub issues

### After Reporting
1. If `--format=markdown`, write report to `state/reports/{date}-dashboard.md`
2. Do NOT modify any state files — this is a read-only operation
3. Log the report generation as an event if a compounding cycle follows

## Scheduling

**In-session:**
```
CronCreate("30 8 * * *", "/demerzel report --format=discord")
```
Run after harvest (8:17) and before compound cycle. Discord post provides the team a daily governance snapshot.

**Persistent:**
```bash
claude --print "Run /demerzel report --format=markdown" --cwd /path/to/Demerzel
```

## Integration

- **Reads from:** `state/beliefs/`, `state/conscience/`, `state/streeling/`, `state/evolution/`, GitHub Issues API
- **Writes to:** Discord channel (if `--format=discord`), `state/reports/` (if `--format=markdown`), terminal (default)
- **Feeds into:** `/demerzel compound` (dashboard highlights inform compounding priorities), `/demerzel drive` (health scores inform driver task selection)
- **Triggered by:** `/demerzel harvest` completion, manual invocation, scheduled cron
- **Governed by:** `policies/governance-audit-policy.yaml` (reporting requirements), `policies/conscience-observability-policy.yaml` (conscience metrics exposure)

## GitHub Discussion Posting

For weekly or milestone reports, also post to GitHub Discussions using the existing infrastructure:

| Repo | Announcements Category | Node ID |
|------|----------------------|---------|
| Demerzel | `DIC_kwDORnMyyc4C4eDS` | `R_kgDORnMyyQ` |

```graphql
mutation {
  createDiscussion(input: {
    repositoryId: "R_kgDORnMyyQ",
    categoryId: "DIC_kwDORnMyyc4C4eDS",
    title: "Governance Dashboard — {date}",
    body: "{MARKDOWN_CONTENT}"
  }) {
    discussion { url }
  }
}
```

## Source

`policies/governance-audit-policy.yaml` (audit reporting requirements), `policies/conscience-observability-policy.yaml` (conscience metrics), `policies/streeling-policy.yaml` (university reporting), `constitutions/demerzel-mandate.md` Section 4 (Accountability)
