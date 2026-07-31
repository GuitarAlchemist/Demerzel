# Gaia — Local Semantic Bus for Cross-Session AI Coordination

**Date:** 2026-07-30
**Status:** Design approved; slice 1 not yet implemented
**Scope:** Desktop-only. All local AI harnesses (Claude Code, Codex, Antigravity,
Junie, any MCP-capable tool) on one machine.
**Supersedes nothing.** Extends `docs/design/2026-07-21-galactic-live-session-bridge.md`
and reuses `~/.agents/claims.jsonl` unchanged.

Named for Foundation's shared planetary consciousness: many minds, one substrate,
each still itself.

## Why

Concurrent AI sessions on this machine collide, and the existing channels do not
stop them. One measured case, from `~/.agents/claims.jsonl`:

> "another lane is mid-refactor on `scripts/run_afk_cycle.py` in the SHARED tree
> building #873; my edits were backed out of it to avoid collision."

Work was written and thrown away. The claim ledger did not prevent it because the
two lanes carried different slugs — `issue-873-governor` and
`issue-863-spend-attribution` — and nothing compared what they were *touching*.

### What already exists, and why it did not solve this

| artifact | state | why it falls short |
|---|---|---|
| `~/.agents/claims.jsonl` | live, 131 claims | advisory, exact-match on `(repo, lane)`; nothing keys on files |
| `scripts/galactic_bridge.py` | on master, 813 lines | MCP + CLI for presence/claims/messages — but see below |
| `%LOCALAPPDATA%/Demerzel/galactic-protocol/events.jsonl` | live, 363 events | **361 of 363 from one origin (`codex-desktop`); 354 are heartbeats; 6 messages ever** |

The bridge is not broken. It is unused, and the reason is structural rather than
technical: **it requires a session to remember to send.** Coordination that
depends on an agent choosing to cooperate decays to zero, and the ledger records
exactly that decay — a pulse with no traffic.

The same decay appears in the claims ledger. Of 44 lanes opened, **5 were never
closed** (11%): sessions reliably claim and unreliably release.

Both are the failure `docs/methodology` already names — infrastructure built
ahead of a proven consumer. Gaia is only worth building if it does not repeat it.

## The one idea this rests on

**Nothing is published by hand.**

`PostToolUse` on Edit/Write emits a touch event automatically. `PreToolUse` on
Edit/Write asks whether anyone else holds that path. Neither requires a session
to decide to cooperate — coordination becomes a side effect of working.

If that idea is wrong, Gaia becomes a third dead ledger and should not be built.
Everything below is downstream of it.

## Architecture

```
  Claude Code        Codex         Antigravity
  (hooks + MCP)   (hooks + MCP)   (MCP only)
       |                |                |
       +-------- named pipe -------------+
                \\.\pipe\gaia          (no TCP port, no listener)
                        v
        +-------------------------------+
        |          gaia daemon          |
        |  facet exchange   (exact)     |  <- slice 1
        |  semantic exchange (kNN)      |  <- deferred, slice 2
        |  claim liveness / expiry      |
        +-------------------------------+
                        |
          SQLite (WAL)  — working store
                        |
          ~/.agents/claims.jsonl — mirrored, contract unchanged
```

A named pipe rather than a localhost port keeps the existing safety boundary from
the Galactic bridge: local stdio only, nothing bindable from off-machine.

SQLite is the working store because it gives multi-process concurrency for free.
`claims.jsonl` keeps its current schema and keeps being appended, so every
existing reader — including the `SessionStart` hook — continues to work untouched.
**Gaia mirrors; it does not migrate.**

### Two exchanges, because the jobs want opposite guarantees

**Facet exchange (slice 1, deterministic).** Routes on typed facets: repo, path,
issue, symbol. Set overlap, no model, fully explainable and replayable. Collision
detection must fire *every* time — a miss costs thrown-away work, and a matcher
trusted to catch collisions that silently misses one is worse than no matcher.

**Semantic exchange (slice 2, fuzzy).** Routes on embedding similarity for
findings, corrections and dead ends, where the value is surfacing a connection
nobody knew to query for. A deterministic matcher there is just grep.

Splitting them means **slice 1 has no model dependency**: if Ollama is down or the
GPU is saturated, collision detection runs at full strength and only future fuzzy
discovery degrades. The failure asymmetry falls out of the design rather than
needing machinery.

## Identity and path normalization

This machine has **47 git worktrees**. The same logical file has dozens of
absolute paths — `scripts/run_afk_cycle.py` currently exists under
`.claude/worktrees/agent-*`, `C:/tmp/dz-*`, and the primary clone.

Keying on absolute path means the detector **never fires once**, while passing any
unit test written against a single directory. This is the highest-risk detail in
the design.

Identity is therefore `(repo, repo_relative_path)` where `repo` derives from
`git config remote.origin.url` and the path is relative to
`git rev-parse --show-toplevel`.

### Hits are graded

Normalizing across worktrees creates the opposite risk: parallel worktree work is
*normal*, and warning on all of it produces a noise floor that trains the reader
to ignore it — the cry-wolf failure of #850.

| situation | verdict | rationale |
|---|---|---|
| same worktree, same file | **hard** | literally the same bytes; one session will clobber the other |
| different worktree, same file, both targeting master | **soft** | a merge conflict is coming; worth knowing, not alarming |
| different repo | no hit | — |

## Claim liveness

Measured 2026-07-30 over the 44 lanes then present in `~/.agents/claims.jsonl`:

| percentile | duration |
|---|---|
| median | 30.5 min |
| p75 | 45.0 min |
| p90 | 864 min (14.4 h) |
| p95 | 1324 min (22 h) |
| never closed | 5 of 44 (11%) |

The distribution is sharply bimodal — most lanes are half an hour, a tail runs
overnight. **A fixed TTL therefore cannot work.** 45 minutes expires the tail and
misses real collisions; 24 hours keeps dead claims warm all day and cries wolf.

So liveness is **heartbeat-primary**: a claim is live iff its owning session has
heartbeated recently. Sessions heartbeat for free on ordinary hook traffic, so
this costs no discipline. `SessionEnd` releases the session's claims. A generous
TTL (> p95) remains only as a crash backstop for sessions that die without
releasing — the 11% case.

The measurement chose the mechanism, not merely the number. A single TTL constant
would have been a judgement presented as a threshold.

## Data flow — the collision path

```
Session A                          gaia daemon                    Session B
    |                                   |                             |
    | PreToolUse(Edit, run_afk_cycle.py)|                             |
    |---- check(repo, rel_path) ------->|                             |
    |<--- clear ------------------------|                             |
    | (edit proceeds)                   |                             |
    | PostToolUse(Edit)                 |                             |
    |---- touch(repo, rel_path, lane) ->| claim recorded, live        |
    |                                   |                             |
    |                                   |<-- check(same repo+path) ---|
    |                                   |--- HARD hit: A holds it, ---|
    |                                   |    lane issue-873-governor, |
    |                                   |    14m ago                  |
    |                                   |    -> additionalContext     |
    |                                   |       before B's edit runs  |
```

## Behavioural decisions

**It warns; it does not block.** `~/.agents/README.md` states outright: *"this is
NOT a task queue or a lock server."* That holds. `PreToolUse` surfaces a collision
as context, never a denial. A false positive that halts real work costs more than
a warning that is read and overruled, and starting with hard blocks would poison
adoption before the signal quality is known. Escalation stays available later.

**Publish fails loudly, or the bus is worthless.** The lethal failure is sessions
publishing into a dead daemon and believing they coordinated. Liveness is
therefore on the call path, not in a monitor: if the daemon is unreachable the MCP
tool **errors**, and `SessionStart` reports the bus as down. Green must be
unreachable while dead. A scheduled guard is defense-in-depth on top, never the
primary detector.

**A hook must never block editing.** These pull in opposite directions and the
split resolves it: the MCP *tool* errors loudly so a calling agent knows; the
*hook* catches, emits `gaia: bus unreachable` into context, and lets the edit
proceed. Loud, not obstructive.

**100 ms hard timeout** on the PreToolUse round trip. Past that the edit proceeds
unwarned. A coordination nicety must not add latency to every edit.

Desktop-only buys a real simplification: one machine, one clock. No skew, no
distributed consensus, no partition semantics.

## Safety boundaries

- Local named pipe only; no TCP listener, no network surface.
- Runtime state contains no credentials and never copies environment secrets.
- Cross-session message bodies surface as **untrusted context**, never as
  instructions with elevated priority.
- Gaia never rewrites another session's claim history; releases are appends.
- A session may release only its own claims.
- `claims.jsonl` remains append-only and schema-compatible.

## Tracer bullet

Slice 1 is complete when this passes as an automated test, and not before:

```
GIVEN  session A has touched scripts/run_afk_cycle.py
         (lane issue-873-governor, worktree W1)
WHEN   session B, on lane issue-863-spend-attribution in worktree W2,
         is about to edit the same repo-relative path
THEN   B's PreToolUse hook receives a SOFT collision naming A, its lane,
         and the claim age
AND    the same scenario within one worktree yields a HARD collision
FAILS IF the warning arrives after the edit, or not at all.
```

This is the #873 collision replayed. It was chosen because it already cost real
work, so passing it proves the bus catches something that actually happens.

### Guards, because a green test that has never been seen red is not coverage

1. **Mutation — disable path normalization.** The collision must be missed and the
   test must fail. This proves worktree handling is load-bearing rather than
   decorative, and is the guard for the highest-risk detail in the design.
2. **Daemon stopped.** The bus must report DEAD and publish must error.
   Green-while-dead must be unreachable.
3. **Grading.** A different-worktree hit must not report as HARD. Without this the
   noise floor eats the signal and the warning stops being read.

## Deliberately not in slice 1

Each is architecturally provided for and none is built:

- **Semantic exchange / embeddings.** `mxbai-embed-large` via local Ollama is the
  intended model. Deferred because building fuzzy discovery before the
  deterministic half has a proven consumer repeats precisely the mistake the
  363-event ledger documents.
- **Presence UI / tray notification.** No idle-session push exists to surface.
- **Shared world-model and belief sync.** Wants the semantic exchange first.
- **Hard blocking on collision.** Requires trust in the signal that slice 1 exists
  to establish.
- **Migration off `claims.jsonl`.** The existing contract stays.

## Known limits

**No push to idle sessions.** There is no supported API for injecting a turn into
a running Claude Code or Codex desktop session. Consumers are reachable only at
hook boundaries — `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`,
`PreCompact`. RabbitMQ's push-to-consumer model degrades here to durable queue
plus poll at hook points. The broker's value is durability, routing and fan-out —
not push. During active work hooks fire often enough that delivery feels
near-live; an idle session hears nothing until its next interaction.

**Non-MCP tools are out of reach** unless they expose lifecycle hooks or can call
the CLI verbs. The dependency-free CLI surface from the Galactic bridge is the
intended fallback.

**Advisory, not authoritative.** Two sessions determined to edit the same file
still can. Gaia removes the excuse of not knowing; it does not remove the ability.

## Open question for the owner

**Hard-block escalation.** Slice 1 warns only. Whether a HARD same-worktree
collision should eventually *deny* the tool call is a judgement about how much
autonomy to hand a detector, and it should be made with slice 1's measured false
positive rate in hand rather than now.
