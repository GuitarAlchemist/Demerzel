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

`PreToolUse` on Edit/Write **atomically checks and claims** the path in one SQLite
transaction. `PostToolUse` confirms and `SessionEnd` releases. Neither requires a
session to decide to cooperate — coordination becomes a side effect of working.

The claim must be taken at `PreToolUse`, not `PostToolUse`. Check-at-Pre and
publish-at-Post leaves a race: A checks clear, B checks clear, both edit, and
neither has published yet — precisely the simultaneous case the bus exists to
catch, sailing through green. Test-and-set in one transaction closes it, and a
concurrent test is mandatory rather than optional (see Guards).

### Where this claim is weaker than it looks

Automatic publication removes the discipline of *calling send*. It does not
remove discipline; it relocates it, and the honest list is:

- Hooks must stay installed, enabled and fast in every harness.
- **Every mutation must pass through a recognised Edit/Write tool.** Shell
  redirection, `sed`, formatters, patch tools, IDE saves and build steps all
  bypass it. This is not theoretical: the session that wrote this spec appended
  test code with `cat >>` and wrote files from inline Python, neither of which
  any Edit/Write hook would have seen.
- Sessions must actually heed `additionalContext`.
- A flaky 100 ms tax must get repaired rather than disabled.

So the third-dead-ledger risk is not "nobody writes events" — publication is now
automatic and will look healthy indefinitely. It is that **events stop predicting
danger**: missed mutation paths and stale sessions produce false negatives,
over-broad matching produces false positives, warnings become ambient text, and
consumption decays to zero while the ledger stays busy. That is the predecessor's
354-heartbeat failure wearing a different mask, and it is the thing to watch for.

## Architecture

```
  Claude Code                 Codex / Antigravity / other harnesses
  lifecycle hooks             dependency-free CLI verbs
       |                                  |
       +---------- gaia_bus.py -----------+  <- slice 1, brokerless
                          |
                    SQLite (WAL)            working file-claim store
                          |
            ~/.agents/claims.jsonl          lane lifecycle mirror

  named pipe + gaia daemon + MCP           <- deferred, slice 2
  semantic exchange (kNN)                  <- deferred, slice 2
```

Slice 1 exposes no listener at all. Claude gets automatic publication through
hooks; any harness that can launch a process can call the same `check`, `confirm`,
`heartbeat`, `release`, and `status` CLI verbs. A named pipe rather than a
localhost port remains the intended slice-2 boundary when a resident process has
work to do.

**The daemon is deferred to slice 2.** Reviewing what it actually buys slice 1:
the vector index needs a resident process, but slice 1 has no embeddings; TTL
expiry can sweep on read; fan-out bookkeeping only matters for messages, which
slice 1 does not carry. Nothing in deterministic collision detection needs a
long-lived process that SQLite's WAL and the hooks do not already provide — while
the daemon contributes the one failure mode this codebase is repeatedly burned by,
a process that dies quietly and reads green. Slice 1 therefore ships
**brokerless**: hooks write to SQLite directly. The daemon arrives with the
semantic exchange, when there is something resident for it to hold.

SQLite is the working store because it gives multi-process concurrency for free.
`claims.jsonl` keeps its current schema and keeps being appended, so every
existing reader — including the `SessionStart` hook — continues to work untouched.
**Gaia mirrors; it does not migrate.** The mirror remains lane-level: the first
file claim appends `claimed`, the first confirmed dirty edit appends `in-progress`,
and `SessionEnd` appends `released`, with the repo-relative path carried as
evidence. File-level exclusion stays in SQLite; the legacy `(repo, lane)` fold is
not reinterpreted as a file lock.

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

### What counts as a collision — settled by measurement, 2026-07-30

An earlier draft of this spec graded hits as *hard* (same worktree) and *soft*
(different worktree, same file). Measuring the live machine refuted the soft tier
outright.

| signal | files | overlapping | rate |
|---|---|---|---|
| touched vs master, all 31 worktrees with a diff | 159 | 77 | **48%** |
| touched vs master, 16 worktrees active in last 48 h | 114 | 66 | **58%** |
| **uncommitted simultaneously**, 7 dirty worktrees | 29 | **0** | **0%** |

Two conclusions, and they point the same way.

**Branch-level overlap is not a signal.** At 48% — rising to 58% when restricted
to *live* work, so this is not stale-branch noise — a warning on shared branch
paths fires on the majority of edits. That is a noise floor that trains the reader
to ignore it, which is the cry-wolf death of #850 arriving on day one. It is also
redundant: divergent committed branches touching one file is the case git already
handles, loudly, at merge.

**Simultaneous uncommitted overlap is the signal.** It is the case git *cannot*
help with — no merge, no conflict marker, just one session's working tree
overwritten — and it is exactly what #873 was: two sessions with uncommitted edits
"in the SHARED tree". Its measured base rate is **zero**, which is what a
high-signal alarm needs. Every fire is real by construction.

So slice 1 keys on **dirty-state overlap**, not branch overlap:

| situation | verdict | rationale |
|---|---|---|
| two live sessions, uncommitted edits, same path, **same physical worktree** | **collision** | one working tree, one copy of the file; the loser is overwritten with no trace |
| same path dirty in *different* worktrees | **not a collision** | different physical files; git reconciles at merge |
| same path, committed on divergent branches | **not a collision** | git's job, at merge, with markers |
| different repo | not a collision | — |

The worktree axis was itself a correction. An earlier revision keyed on
`(repo, rel_path)` across all worktrees, which over-claims: two dirty copies in
separate trees cannot silently overwrite each other. Only a shared physical tree
can, and that is exactly what #873 recorded — *"in the SHARED tree"*. Note the
measurement above cannot see this case at all: it keys on worktree, so it counts
overlap *between* trees and is blind to two sessions inside one. **The zero is
real but off-axis.** The same-worktree rate is unmeasured and should be
instrumented before slice 1 is called done.

The measurement also validates the problem. Two of the 66 live branch-level
overlaps were this session's own lanes — `scripts/aiw_budget_gate.py`
(`agent-ac5e6c441797d4c0b` vs `demerzel-fixall`) and `scripts/ecosystem_freshness.py`
(`agent-a48ee49061d2bb40c` vs `agent-a6225e88fd138f984`) — neither noticed while
the work was happening. The collision risk is real and continuous. Only the
*discriminator* needed correcting.

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

So liveness is **heartbeat-primary for session presence**, with ordinary tool
traffic refreshing the heartbeat for free. `SessionEnd` releases the session's
claims. Heartbeat expiry removes the session-presence row, but never proves that
dirty work disappeared: a dirty claim remains protective until Git positively
shows the path clean (committed or reverted). A pending claim whose edit never
landed may self-heal after a short grace period, again only after positive clean
Git state. Timeout, command failure, and malformed Git output are UNKNOWN and may
not delete a holder.

The measurement chose the mechanism, not merely the number. There is no fixed
dirty-claim TTL: elapsed wall time cannot safely distinguish an overnight live
lane from a crashed lane whose uncommitted work still needs protection.

## Data flow — the collision path

```
Session A                         SQLite                       Session B
    |                               |                              |
    | PreToolUse(Edit, path)        |                              |
    |-- atomic check-and-claim ---->|                              |
    |<------------- clear ----------|                              |
    | edit; PostToolUse confirms    |                              |
    |                               |<-- atomic check-and-claim ----|
    |                               |--- A holds path, lane, age -->|
    |                               |        additionalContext      |
    |                               |        before B edits         |
```

## Behavioural decisions

**It warns; it does not block.** `~/.agents/README.md` states outright: *"this is
NOT a task queue or a lock server."* That holds. `PreToolUse` surfaces a collision
as context, never a denial. A false positive that halts real work costs more than
a warning that is read and overruled, and starting with hard blocks would poison
adoption before the signal quality is known. Escalation stays available later.

**Publish fails loudly, or the bus is worthless.** The lethal failure is sessions
publishing into an unusable store and believing they coordinated. Liveness is
therefore on the call path, not in a monitor: the CLI errors and `SessionStart`
reports the bus as down. Green must be unreachable while dead. A scheduled guard
is defense-in-depth on top, never the primary detector.

**A hook must never block editing.** These pull in opposite directions and the
split resolves it: the CLI/library call errors loudly so a calling agent knows; the
*hook* catches, emits `gaia: bus unreachable` into context, and lets the edit
proceed. Loud, not obstructive.

**100 ms hard timeout** on the PreToolUse round trip. Past that the edit proceeds
unblocked but explicitly **unguarded**; an overrun is UNKNOWN and never a clear
verdict. A coordination nicety must not add latency to every edit, and a dropped
claim must not read green.

Desktop-only buys a real simplification: one machine, one clock. No skew, no
distributed consensus, no partition semantics.

## Safety boundaries

- Slice 1 uses local files and subprocess stdio only; no listener or network surface.
- Runtime state contains no credentials and never copies environment secrets.
- Cross-session message bodies surface as **untrusted context**, never as
  instructions with elevated priority.
- Gaia never rewrites another session's claim history; releases are appends.
- A session may release only its own claims.
- `claims.jsonl` remains append-only and schema-compatible.

## Tracer bullet

Slice 1 is complete when this passes as an automated test, and not before:

```
GIVEN  session A holds UNCOMMITTED edits to scripts/run_afk_cycle.py
         (lane issue-873-governor)
WHEN   session B, on lane issue-863-spend-attribution, is about to edit
         the same (repo, repo-relative path) while A's edits are still
         uncommitted and A is still live
THEN   B's PreToolUse hook receives a collision naming A, its lane,
         and the claim age — before B's edit runs
FAILS IF the warning arrives after the edit, or not at all.

AND, equally required:
GIVEN  A's edits to that path are COMMITTED on a divergent branch
WHEN   B edits the same path
THEN   NO collision is reported — that is git's job, at merge
FAILS IF this warns, because at a 58% branch-overlap rate the signal
         is destroyed on day one.
```

This is the #873 collision replayed. It was chosen because it already cost real
work, so passing it proves the bus catches something that actually happens. The
second clause is not optional politeness: it is what keeps the first clause
readable.

### Guards, because a green test that has never been seen red is not coverage

1. **Mutation — disable path normalization.** The collision must be missed and the
   test must fail. This proves worktree handling is load-bearing rather than
   decorative, and is the guard for the highest-risk detail in the design.
2. **Store unreachable.** The bus must report DEAD and publish must error.
   Green-while-dead must be unreachable. (Slice 1 is brokerless, so this is an
   unwritable/locked SQLite file rather than a stopped daemon; the requirement is
   identical and carries forward when the daemon lands in slice 2.)
3. **Committed-divergence must stay silent.** A path committed on two branches
   must produce NO collision. Measured branch-level overlap is 58%, so a
   regression here does not degrade the signal — it deletes it. This guard is the
   reason the first guard's warnings remain readable.
4. **Base-rate regression.** Re-run the dirty-overlap measurement against the live
   machine and assert the alarm's fire rate stays near its measured zero. A
   detector whose base rate has silently climbed is one nobody reads, and no unit
   test would show it.
5. **Concurrency — the race.** Two sessions must call `PreToolUse` on the same
   path with **no serialisation between them**, and exactly one must win. A test
   that claims sequentially passes against a broken check-then-publish
   implementation, so this must exercise genuine concurrency. This is the guard
   for the failure the tracer bullet cannot see.
6. **Bypass honesty.** A file mutated *outside* Edit/Write — shell redirection or
   an inline script — must be shown to produce **no** claim, asserted rather than
   assumed. The coverage gap is real and permanent; a spec that lets it stay
   implicit invites the false confidence that the bus sees everything.

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

**Tools without hooks are not automatic.** They can call Gaia's dependency-free
CLI verbs directly, but mutations made without either lifecycle hooks or those
calls remain invisible. Slice 1 deliberately does not claim automatic coverage
for every desktop harness.

**Advisory, not authoritative.** Two sessions determined to edit the same file
still can. Gaia removes the excuse of not knowing; it does not remove the ability.

## Open question for the owner

**Hard-block escalation.** Slice 1 warns only, and the measurement makes that
worth revisiting sooner than planned. Warn-only was chosen against an assumed
false-positive rate; the measured base rate for simultaneous uncommitted overlap
is **zero**. A detector that fires approximately never can afford to block, and
the cost asymmetry favours it — a false block costs seconds, a missed collision
cost an hour of thrown-away work in #873.

The conservative form I first proposed — **deny once, then allow** — does not
survive review. An autonomous agent that hits a denial simply retries, and a
retry is indistinguishable from an override, so the block degrades to a warning
with extra latency. **If it blocks, the override must be a distinct act** — a
different call carrying an explicit acknowledgement of the holder — not the same
call issued twice.

Warn-only is also weaker than it sounds against this particular failure. It
proves information was *emitted*, not that destruction was *prevented*: an agent
can summarise the warning away, judge its own task more urgent, or never surface
it. Across enough edits, recurrence is the default outcome.

Against that, the narrow condition — same repo, same relative path, same physical
worktree, another live session holding uncommitted edits — has close to no
legitimate concurrent-write reading. That is a strong case for denial, and the
cost asymmetry agrees: a false block costs one coordination step, a false allow
destroyed an hour of work in #873.

Slice 1 still ships warn-only, because the same-worktree base rate is **not yet
measured** (the existing zero is off-axis, see above) and warn-only is the
reversible choice. But this is now a live decision with an argued case against it,
not a default to inherit. Instrument the rate during slice 1, then decide.
