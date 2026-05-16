---
name: demerzel-halt
description: Pause every /auto-optimize loop across the GuitarAlchemist ecosystem (GA, ix, Demerzel, tars) by writing the cross-repo HALT-ALL marker per the contract in ga/docs/contracts/2026-05-16-overseer-halt-marker.contract.md. Use halt/resume/status subcommands. Implementation is scripts/demerzel_halt.py.
---

# /demerzel-halt

Operator skill for halting every autonomous loop in every sibling repo at once. Wraps `scripts/demerzel_halt.py` which writes `~/.demerzel/HALT-ALL` per the cross-repo contract.

## Subcommands

| Subcommand | What | Example |
|---|---|---|
| `halt` | Write the marker. Required: `--reason`. Optional: `--scope`, `--expires-at`, `--exempt-agents`, `--halted-by`, `--issue-ref`. | `python scripts/demerzel_halt.py halt --reason "Investigating cost burn"` |
| `resume` | Remove the marker. Archives the prior marker to `~/.demerzel/halts/<stamp>-resumed.json`. | `python scripts/demerzel_halt.py resume` |
| `status` | Report whether HALT-ALL is in effect. Honors `expires_at`. | `python scripts/demerzel_halt.py status` |

## When to use

- A loop is producing unexpected output across multiple repos and you want one button to pause everything while you investigate
- Cloud-cost burn is climbing faster than expected
- You're cutting a release branch and want zero autonomous churn during the freeze
- An operator on another machine pushed something you need to investigate before agents react

## Effect

Consumers (per-repo `/auto-optimize` Step 0, GA's `Scripts/dev-process-overseer.ps1`, ix's loop runner, tars's loop runner — as they each adopt the contract) read `~/.demerzel/HALT-ALL` before every cycle. If present and valid:

- The cycle prints the halt reason and exits 0
- No commits, no PRs, no cost-bearing tool calls happen until the marker is removed

If the file is unreadable / missing / expired / the agent is in `exempt_agents`, consumers fall through to their per-repo `state/.loop-halted` killswitch.

## Contract reference

Schema: `ga/docs/contracts/overseer-halt-marker.schema.json`
Doc: `ga/docs/contracts/2026-05-16-overseer-halt-marker.contract.md`
Operator runbook: `ga/docs/runbooks/halt-resume.md`

## Time-limited halts

Use `--expires-at` to schedule an automatic unhalt:

```
python scripts/demerzel_halt.py halt \
  --reason "Mobile release branch cut — freeze through Sunday" \
  --expires-at 2026-05-19T00:00:00Z
```

Consumers check `expires_at` and treat the marker as absent after that time. No human intervention needed to lift the halt.

## Exempting specific agents

Halt everyone EXCEPT one debugging session:

```
python scripts/demerzel_halt.py halt \
  --reason "Debugging chatbot-qa loop in isolation" \
  --exempt-agents auto-optimize/chatbot-qa-debug
```

The named agent ignores the marker; everyone else pauses.

## What this skill does NOT do (yet)

- **No HTTP / ACP endpoint** — Demerzel does not currently ship an HTTP server. The CLI fills the role of the planned `POST /halt` endpoint until the ACP server lands.
- **No audit-log append** — Phase 2 of the strategic plan adds `~/.demerzel/audit.jsonl` with every halt event recorded. This skill will be updated to write that event when Phase 2 lands.
- **No trust-score interaction** — Phase 3.

## Future phases

- Phase 2: every halt writes an audit event (`~/.demerzel/audit.jsonl`).
- Phase 3: halts contributed by agents with low trust scores get a confirmation prompt.
- Phase 4: CI-side enforcement so a halted ecosystem can't accept auto-loop merges.

Tracked in `ga/docs/plans/2026-05-16-arch-demerzel-overseer-extension-plan.md`.

## Related

- `ga/docs/contracts/2026-05-16-overseer-halt-marker.contract.md` — the wire format this skill produces.
- `ga/.claude/skills/auto-optimize/SKILL.md` Step 0 — the canonical consumer.
- `ga/docs/runbooks/halt-resume.md` — operator one-pager covering both this Demerzel CLI and the hand-edit fallback for when this script is unavailable.
- `ga/Scripts/dev-process-overseer.ps1` — per-repo policy engine that should also consult the marker (added in a follow-up).
