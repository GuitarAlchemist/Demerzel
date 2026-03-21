# Everything Claude Code (ECC) — Analysis for Demerzel Adoption

**Source:** https://github.com/affaan-m/everything-claude-code (94K stars)
**Analyzed:** 2026-03-22

## Key Patterns to Adopt

### 1. Context Budget Skill (HIGH PRIORITY)

**What ECC does:** `/context-budget` audits token consumption across all loaded components — agents, skills, MCP servers, rules, CLAUDE.md. Classifies each as always-needed/sometimes/rarely. Produces prioritized savings recommendations.

**Why we need this:** Our sessions are massive (this one consumed enormous context). With 36 skills, 22 policies, and 200+ MCP tools registered, we're likely burning context on components we don't need per-session.

**Adoption plan:**
- Create `/demerzel context-budget` skill
- Scan: skills (36 SKILL.md files), rules (.claude/rules/), CLAUDE.md chain, MCP tool schemas
- Classify by session relevance
- Report: total overhead, top savings, recommendations
- Wire into driver RECON as a health metric

### 2. Continuous Learning v2 — Instinct System (HIGH PRIORITY)

**What ECC does:** Hooks capture session observations (PreToolUse/PostToolUse). Background agent (Haiku) analyzes for patterns. Extracts atomic "instincts" — small learned behaviors with confidence scoring. Instincts evolve into skills/commands/agents via promotion.

**How this maps to Demerzel:**
- ECC "instincts" = our "patterns" (`state/patterns/`)
- ECC "confidence scoring" = our tetravalent beliefs
- ECC "evolution to skills" = our promotion staircase
- ECC "project-scoped" = our department-scoped grammar weights

**What we're missing that ECC has:**
- **Hook-based observation** — we don't capture session activity into patterns automatically
- **Background agent analysis** — we don't run a cheap model to extract patterns in real-time
- **Atomic granularity** — our patterns are manually created, not auto-extracted
- **Promotion pipeline** — instinct → cluster → skill is more automated than our manual `/demerzel promote`

**Adoption plan:**
- Add PreToolUse/PostToolUse hooks that log observations
- Background agent (Haiku) extracts patterns into `state/patterns/`
- Connect to existing promotion staircase and grammar evolution
- This IS the metafix Level 4 automation — the system learns from itself

### 3. Hook Profiles (MEDIUM PRIORITY)

**What ECC does:** `ECC_HOOK_PROFILE=minimal|standard|strict` controls which hooks run. Allows runtime gating without editing files.

**Adoption plan:**
- Add `DEMERZEL_HOOK_PROFILE` env var
- `minimal` = no governance checks (fast dev)
- `standard` = staleness + link checks
- `strict` = full constitutional + conscience + pre-mortem

### 4. Doc File Warning Hook (LOW PRIORITY)

**What ECC does:** PreToolUse hook on Write warns about non-standard documentation files.

**Maps to:** Our README sync policy — could be a hook that warns when writing to a README without updating related READMEs.

## Patterns We Already Have (Better)

| Pattern | ECC Version | Demerzel Version | Assessment |
|---------|-------------|------------------|------------|
| Skills | Domain skills (50+) | Governance skills (36) with constitutional integration | Ours are richer |
| Memory | Hooks-based persistence | claude-mem + state/ + beliefs | Ours is more structured |
| Autonomy | Autonomous loops skill | Driver cycle (8-phase) with governance gates | Ours is more governed |
| Security | AgentShield scanning | Asimov constitution + conscience system | Different approach, complementary |
| Learning | Instincts → skills | Patterns → policies (manual) | ECC is more automated |

## Key Insight

ECC's biggest strength is **automation of learning**. They use hooks to capture, background agents to analyze, and promotion pipelines to evolve. We have the governance framework but our learning is manual. Adopting their observation → extraction → promotion automation would close our biggest gap.

## Action Items

1. Create `/demerzel context-budget` skill
2. Add observation hooks (PreToolUse/PostToolUse)
3. Create background pattern extraction agent
4. Add hook profiles (DEMERZEL_HOOK_PROFILE)
5. Reference ECC in external resources
