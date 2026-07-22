# Slice A verdict: the embed IS delivery — three broken hops, all identified

**Date:** 2026-07-21 (deadline was 2026-07-28)
**Plan:** `docs/superpowers/plans/2026-07-21-galactic-protocol-followups.md` Slice A
**Method:** zero-code investigation via GitHub API — dispatch handlers, issue disposition, run logs, branch/PR inventory per consumer.

## Verdict

**The submodule embed is a real delivery channel and should keep its spec claim.** A full remediation pipeline exists and fires: Demerzel's `submodule-notify.yml` (green, 4 runs today) → `demerzel-updated` repository_dispatch → each consumer's `submodule-auto-update.yml` (exists in all three; triggered by dispatch AND cron ~3×/day) → bump branch + PR. Consumers are months stale not because the signal is missing but because the **last hop fails differently in each repo, red for months, unwatched**.

## Per-consumer evidence

| Consumer | Pin age | Handler | Failure | Evidence |
|---|---|---|---|---|
| ix | 2026-05-17 (515 commits behind per today's run) | runs 4×/day, fails every run | **SIGPIPE exit 141** after force-pushing the bump branch, at/before `gh pr create` | 28 orphan `chore/update-demerzel-*` branches; last bump PR April (#26, closed unmerged); staleness issue #52 open since 05-24 |
| tars | 2026-05-16 | runs 3×/day, fails (same workflow shape) | same exit-141 flakiness; occasionally completes | 23 orphan branches; PR #201 **merged 07-13** (the one success — closed issue #51); issue #205 open since 07-18 |
| ga | 2026-04-04 (most stale) | runs 4×/day, fails every run | **exit 128 at recursive checkout**: `mcp-servers/meshy-ai` pinned to nonexistent commit `0efc525…` ("not our ref") — dies before any Demerzel step | zero bump branches, zero PRs ever since failure began; **also** no staleness issues since 03-29 (see finding 4) |

## Findings

1. **ix/tars hop:** exit 141 = SIGPIPE under `pipefail`, almost certainly the `$CHANGES` cosmetic pipe (`git log … | head`-style) in the PR-body heredoc, executed after the force-push succeeds. One-line fix in each consumer's `submodule-auto-update.yml`; then prune the orphan branch pileup (28 + 23) and let the next run open a real PR.
2. **ga hop:** unrelated broken submodule pin (`mcp-servers/meshy-ai` → force-pushed/rewritten upstream history). Fix or unpin that submodule, or scope the workflow's checkout to `governance/demerzel` only (non-recursive), which also decouples the governance bump from every other submodule's health.
3. **Demerzel-side defect (our repo):** `submodule-notify.yml` line ~95 swallows issue-creation failures (`2>/dev/null … || echo "Failed"`). The exact swallowed-exit-code pattern from `docs/solutions/harness/2026-07-20-powershell-native-exit-codes.md`. Fail-loud fix, one line, `.github/` = human-gated PR.
4. **ga issue silence since 03-29 — SOLVED (follow-up probe):** the notifier's existing-issue guard uses *full-text* search (`--search "Demerzel submodule"`), and ga's open issue #47 ("Prime Radiant: integrate ix governance.graph…") mentions the submodule in its body — so `EXISTING=1` and ga's staleness alerts have been muted since #47 opened. Fixed alongside finding 3 by scoping the search `in:title` (PR #814).
5. **Meta:** every hop that failed did so *visibly* in its own repo's Actions tab and *invisibly* to the ecosystem — red runs 3-4×/day for months with no consumer of the failure signal. The loop-health registry pattern (proof-of-success, not absence-of-alarm) is the general cure; consumers don't have it yet.

## Named next actions (one per lane, coordination via ~/.agents/claims.jsonl)

- **ix session:** fix SIGPIPE in `submodule-auto-update.yml`, prune 28 orphan branches, merge the resulting bump PR (515 commits of governance including PR #808/#813 once merged).
- **tars session:** same fix, prune 23 branches, action issue #205.
- **ga session:** repair/unpin `mcp-servers/meshy-ai` or make the bump checkout non-recursive; then bump a 3.5-month-stale pin.
- **Demerzel (this session):** fail-loud fix to `submodule-notify.yml` (separate small PR, human-gated).
- **Spec:** no change needed — the delivery claim stands; the v1.3.0 status table needs no edit for this.

## Consumer of this verdict

Repo owner, next governance review (per plan Slice A acceptance). This doc is the plan's Slice A deliverable, complete 7 days ahead of deadline.
