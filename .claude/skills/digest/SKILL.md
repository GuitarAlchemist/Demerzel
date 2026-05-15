---
name: digest
description: Capture meaningful session state (current cursor, in-flight work, live hypotheses, open questions, do-NOT-carry-forward, success criteria) to state/digests/latest.md so the next session — including one after auto-compaction — can re-enter without re-discovering context cold. Distinct from /learnings (which captures surprises). Validates against docs/contracts/digest-schema.json.
allowed-tools: Bash, Read, Write, Edit
last_verified: 2026-05-14
karpathy_rules: [R1-think-before-coding, R4-goal-driven-execution]
---

# /digest

Captures the **meaningful state of the current session** to
`state/digests/latest.md`. The `.claude/hooks/sessionstart-digest.ps1` hook
reads it on the next session start and emits it as `additionalContext` for
the model. Pairs with `.claude/hooks/precompact-digest.ps1` which provides
a metadata-only fallback when /digest isn't invoked before auto-compaction.

## When to run

- **Before compaction is imminent** (context feels >60% full).
- **At a natural breakpoint** — after finishing a feature, before a risky
  operation, before handing off to another agent.
- **Before launching long-running background work.**

**Do NOT** invoke on every message or tool call.

## What it captures

```yaml
---
schema_version: 1
session_id: <session_id>
written_at: <RFC3339 UTC>
trigger: digest-skill
branch: <git branch>
head_sha: <short SHA>
head_subject: <commit subject>
open_pr: <"#N" or null>
last_model_update: <RFC3339 UTC>
success_criteria:
  - criterion: "<testable assertion for the Next action>"
    status: pending | in-progress | achieved | abandoned
    evidence: "<file:line | PR# | metric path | null>"
---

# Session digest — <branch> @ <sha>

## Next action

ONE imperative sentence. Must map 1:1 to `success_criteria` entries.

## In-flight

Work currently mid-execution. file/feature, step N of total, next sub-step.

## Live hypotheses

Working hypotheses to inherit. *Unconfirmed*; don't promote to MEMORY.md yet.

## Open questions

Numbered. Questions you would ask the user if they walked in now.

## Do NOT carry forward

**Highest-leverage field.** Things the next session must NOT re-propose.

## Prior success criteria status (Karpathy R4)

When a prior digest exists, this section reports the status delta:

- ✅ achieved: <prior criterion> — evidence: <file:line | commit | PR>
- ⏳ in-progress: <prior criterion> — last touched: <where>
- ⛔ abandoned: <prior criterion> — reason: <one sentence>
```

## How to run

1. Read existing `state/digests/latest.md` if present — preserve current sections.
2. Karpathy R4 — review/mark prior success criteria.
3. Capture git state via Bash (`git rev-parse`, `git log -1`, `gh pr view`).
4. Synthesize content; derive 1–3 testable `success_criteria` from Next action.
5. Write to `state/digests/latest.md`. Set `trigger: digest-skill` + `last_model_update`.
6. `rm -f state/digests/.activity-counter` to reset the staleness nudge.
7. Validate: `pwsh -NoProfile -File .claude/hooks/digest-validate.ps1`. Non-zero = fix.
8. Report: `Digest updated: <branch>@<sha> · next: <one-line> · criteria: <N>`.

## Driving criteria autonomously with `/goal`

After writing the digest, **consider `/goal <condition>` (native Claude
Code v2.1.139+) for substantial autonomous work**. `/goal` mechanizes
Karpathy R4: a small fast model evaluates after every turn whether the
condition holds and either fires another turn or clears the goal.

Use `/goal` when the Next action has:

- A verifiable end state (build green, tests pass, file count under budget)
- 5+ minutes of expected autonomous work
- An evaluator-checkable result (checked against the transcript — no
  tool calls)

Skip `/goal` for short tasks, visual/UX judgement, or ambiguous specs.

When `/goal` lands a "yes," the next `/digest` should mark the
corresponding `success_criteria` entry as `achieved` with the `/goal`
evidence.

## Anti-patterns

- Transcript capture — git log is the transcript.
- Empty digest — if nothing changed, prior digest still applies.
- Forgetting "Do NOT carry forward".

## Related

- `/learnings` — captures surprises into `docs/solutions/`.
- `/correct` — captures user corrections as permanent `CLAUDE.md` rules.
- `.claude/hooks/{precompact,sessionstart}-digest.ps1` — auto-fallback + read-back.
- `state/digests/README.md` — directory layout.
