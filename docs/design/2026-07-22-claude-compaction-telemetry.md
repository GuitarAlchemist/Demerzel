# Claude Fleet Compaction Telemetry — Tracer Slice

## Outcome

Every local Claude Code repo inherits the supported 40% auto-compaction
threshold. `PreCompact`, `PostCompact`, and compact-driven `SessionStart`
events append privacy-safe metadata to `~/.agents/compaction-events.jsonl`.

The slice closes one real feedback loop:

1. Claude Code emits lifecycle evidence.
2. IX/DuckDB queries compaction and recovery rates by repo.
3. TARS retains task meaning in the existing per-repo session digest.
4. Demerzel flags obsolete project settings and governs threshold changes.
5. The fleet Project carries the verified remediation work.

## Privacy boundary

Transcript paths and compact summaries are never stored. The event contains
only their SHA-256 hashes and summary character count. This supports replay,
deduplication, and trend analysis without turning the fleet ledger into a
second transcript store.

## Gate

- The user setting must use `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`.
- Repo-local use of `CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE` is reported as
  `obsolete-key`.
- Hook failures never block a Claude session.
- DuckDB must query a synthetic event end to end before installation is
  considered complete.

## Installation

Run `pwsh scripts/install-claude-compaction-hook.ps1`. The idempotent installer
backs up the user settings, removes the obsolete environment key, installs the
hook and DuckDB reader under `~/.claude/hooks`, and merges the three lifecycle
events without replacing unrelated hooks.
