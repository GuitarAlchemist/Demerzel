---
name: demerzel-cross-review
description: Use when a pull request needs review by a different AI model than the one that authored it, or when configuring cross-model code review pipelines in CI/CD.
---

# Cross-Model Code Review

No model reviews its own work. When one AI generates code, a different model reviews the PR — exploiting divergent training biases to catch what self-review misses.

## Usage

```
/demerzel cross-review                          # Review current PR with auto-detected reviewer
/demerzel cross-review --author claude          # Explicitly set author model
/demerzel cross-review --reviewer gemini        # Force specific reviewer
/demerzel cross-review --focus security         # Narrow review focus
/demerzel cross-review --dry-run                # Show what would happen without posting
/demerzel cross-review --configure              # Edit review matrix for this repo
```

## Review Matrix

The core invariant: `reviewer != author`. The matrix encodes which model reviews which and why.

| Author | Primary Reviewer | Fallback Reviewer | Rationale |
|--------|-----------------|-------------------|-----------|
| Gemini | Claude | Codex | Catches Gemini's confident-but-wrong patterns |
| Claude | Codex | Gemini | Catches Claude's over-engineering and verbosity |
| Codex | Claude | Gemini | Catches Codex's terse/incomplete implementations |
| Human | Claude | Gemini | Standard AI-assisted review |
| Unknown | Claude | Gemini | Default when author model cannot be detected |

## Author Detection

The Action detects the author model from (in priority order):

1. **PR label**: `model:claude`, `model:gemini`, `model:codex`
2. **Commit message trailer**: `Model-Author: claude` (conventional trailer)
3. **Commit message body**: Patterns like "Generated with Claude Code", "Gemini CLI", "OpenAI Codex"
4. **PR body**: Same pattern matching as commit messages
5. **Fallback**: `unknown` — triggers default reviewer (Claude)

Detection patterns:

```yaml
claude:
  - "Claude Code"
  - "claude-opus"
  - "claude-sonnet"
  - "Co-Authored-By:.*Claude"
  - "Anthropic"

gemini:
  - "Gemini CLI"
  - "gemini-"
  - "Jules"
  - "Google AI"

codex:
  - "Codex"
  - "codex-"
  - "OpenAI"
  - "GitHub Copilot"
```

## Review Focus Areas

Every cross-model review checks five dimensions, each mapped to a governance article:

### 1. Correctness (Article 1 — Truthfulness)
- Logic errors, off-by-ones, edge cases
- Type mismatches, null safety gaps
- Incorrect algorithm choice for the data shape

### 2. Security (Article 3 — Reversibility)
- OWASP top 10: injection, auth gaps, XSS, CSRF
- Secrets in code, hardcoded credentials
- Unsafe deserialization, path traversal

### 3. Anti-Slop (Article 5 — Non-Deception)
Integrates with `/demerzel anti-slop-docs`:
- Comments that restate what code already says
- Documentation that passes the substitution test (could describe any class)
- Verbose implementations where concise ones exist

### 4. LOLLI Detection (Article 4 — Proportionality)
Integrates with `/demerzel lolli-remediate`:
- Dead code, unused exports, unreachable branches
- Ahead-of-demand abstractions (interfaces with one implementation, unused)
- Over-engineering: feature flags for hypothetical futures

### 5. Constitutional Compliance (Article 9 — Bounded Autonomy)
- Reversibility: does the change prefer reversible actions?
- Proportionality: is the scope matched to the request?
- Auditability: are decisions logged and traceable?

## Review Output Format

The reviewer posts a structured PR review comment:

```markdown
## Cross-Model Review

**Author model:** {detected_model}
**Reviewer model:** {reviewer_model}
**Files reviewed:** {count} ({lines_changed} lines changed)

### Findings

#### Correctness
- [ ] {finding with file:line reference}

#### Security
- (none found)

#### Anti-Slop
- [ ] {finding}

#### LOLLI
- [ ] {finding}

#### Constitutional Compliance
- (compliant)

### Verdict: {APPROVE | REQUEST_CHANGES | COMMENT}

**Confidence:** {0.0-1.0}
**Rationale:** {one sentence}
```

## Cost Control

The Action skips review when the PR is unlikely to benefit:

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Lines changed < 10 | Skip | Too small to warrant API cost |
| Only `.md` files changed | Skip | Docs-only, no logic to review |
| Only `.yml`/`.yaml` config | Skip | Config-only unless in `policies/` |
| Label `skip-cross-review` | Skip | Explicit opt-out |
| Draft PR | Skip | Not ready for review |
| Lines changed > 2000 | Chunk | Split into batches of 500 lines |

## Configuration

Consumer repos configure the review matrix in `.github/cross-review-config.yml`:

```yaml
# .github/cross-review-config.yml
review_matrix:
  gemini: claude      # gemini PRs reviewed by claude
  claude: codex       # claude PRs reviewed by codex
  codex: claude       # codex PRs reviewed by claude
  human: claude       # human PRs reviewed by claude
  unknown: claude     # fallback

skip_conditions:
  min_lines: 10
  docs_only: true
  draft: true
  max_lines_per_chunk: 500

focus_areas:
  - correctness
  - security
  - anti-slop
  - lolli
  - constitutional-compliance

# API keys stored as GitHub Secrets:
#   ANTHROPIC_API_KEY — for Claude reviews
#   OPENAI_API_KEY   — for Codex reviews
#   GEMINI_API_KEY   — for Gemini reviews
```

## GitHub Action Template

The workflow template lives at `templates/cross-model-review.yml`. Consumer repos copy it to `.github/workflows/cross-model-review.yml`.

See that template for the full Action implementation with:
- PR trigger configuration
- Author model detection logic
- Reviewer selection from matrix
- API call to reviewer model
- Review comment posting via `gh pr review`
- Cost control skip conditions

## Governance Integration

Review results feed back into Demerzel's governance state:

- **Belief states**: cross-model agreement increases confidence (two_model_agreement: 0.9 per multi-model-orchestration-policy)
- **Evolution log**: disagreements between models are recorded as contradictory (C) evidence
- **Confidence calibration**: single_model review caps at 0.8; cross-model agreement reaches 0.9

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Model reviews its own code | The matrix enforces `reviewer != author`. If detection fails, fallback is always a different model. |
| Reviewing trivial PRs | Cost control skips PRs under 10 lines or docs-only changes. |
| Ignoring reviewer disagreement | Disagreements are C (contradictory) in tetravalent logic — they trigger human escalation, not silent resolution. |
| Hardcoding API keys in workflow | Keys must be GitHub Secrets, never in workflow YAML. |
| Skipping review on large PRs | Large PRs are chunked, not skipped — every chunk gets reviewed. |
