---
category: agentic
date: 2026-07-24
topic: Read-only spike campaign — dependency-ordered background agents, findings-as-issue-comments, ADR synthesis at the end
source: ga#590 epic (spikes #591/#592/#593/#597 + tars#211) → ADR docs/adr/0007, all in ~30h wall-clock
---

# Five spikes to one accepted ADR in a day: the read-only campaign pattern

## What worked

The ga persistence decision (epic #590) went from five open spike issues to an
owner-accepted ADR (ga `docs/adr/0007`) using a pattern worth repeating:

1. **Repos are READ-ONLY for spike agents; prototypes live in scratchpad.**
   No branches, no commits, no cleanup debt, no merge-gate friction. The Gel
   agent installed a CLI, ran a Docker server, seeded real repo data, executed
   live queries — and still left the repo untouched.
2. **Findings land as one comprehensive comment on the spike's own issue.**
   The evidence lives exactly where the downstream decision issue (#594) looks
   for it, survives session loss, and needs no PR review to exist.
3. **Launch in dependency order, not all at once.** #591 (inventory) ran first
   with #593 (independent); #592 and #597 launched only after their declared
   inputs landed, with the predecessor's findings quoted in the spawn prompt.
   Parallelism where the DAG allows, sequence where it doesn't.
4. **Every spike prompt carries a null hypothesis and a LOLLI guard.** "Object
   storage + httpfs already covers sharing" (MotherDuck), "grep + /learnings
   already cover this" (Obsidian). Two spikes returned *decline/not-yet*
   verdicts — negative results were explicitly framed as valid outcomes, so
   agents didn't inflate findings to justify their run.
5. **Synthesis is the orchestrator's job, not another agent's.** The ADR draft
   was written from the five reports in-context, posted on the decision issue
   as a PROPOSED comment, and became binding only by owner word + PR into
   docs/adr/.

## Numbers

5 spikes, 5 background agents, 0 repo mutations, 2 negative verdicts kept as
evidence, 1 accepted ADR + 1 executed follow-up (DuckDB.NET pin, ga#602) —
about 30 hours wall-clock, most of it unattended.

## Gotchas hit

- Agents die silently or post-delivery (one API stall, several idle pings):
  **always verify the issue comment exists** before trusting a completion
  notification, and treat "failed" notifications as *check-the-deliverable*,
  not *rerun*.
- ga worktrees on Windows need `git -c core.longpaths=true worktree add` and a
  short root (`C:/tmp/...`) — Playwright test-result paths overflow MAX_PATH.
- Claim each spike as a `(repo, lane)` in `~/.agents/claims.jsonl` before
  spawning, so parallel sessions (Codex was live in ga) don't collide.
