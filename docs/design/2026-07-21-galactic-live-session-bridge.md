# Galactic Live Session Bridge — Tracer-Bullet Design

**Date:** 2026-07-21  
**Status:** Approved for tracer-bullet implementation  
**Architect:** Reflective Architect lane  
**Scope:** Local Codex desktop/CLI sessions across the ecosystem repos

## Why

The Galactic Protocol has durable cross-repo messages, but no live fleet layer.
Top-level Codex sessions cannot use their subagent messaging APIs to reach other
top-level sessions. Git branches reduce collisions, but they do not identify who
owns a repo or lane, expose current presence, or carry handoffs.

The missing capability is therefore not another belief store. It is a small
coordination plane with four primitives:

1. session presence and heartbeat;
2. shared repo/lane claims;
3. addressed messages;
4. delivery and acknowledgement.

## Hidden assumptions surfaced

- "Live" cannot mean unsolicited model turns in an idle Codex desktop chat.
  Codex does not document a supported API for injecting a turn into another
  already-running top-level desktop session.
- Codex lifecycle hooks can surface messages at session start, prompt submit,
  and after local tool calls. That provides near-live delivery while a session
  is active and immediate delivery on its next interaction.
- A project-only file is insufficient because ix, tars, ga, hari, and Demerzel
  run in different workspace sandboxes. The state root must be shared and the
  bridge must be installed in Codex's user-level MCP and hook configuration.
- Runtime traffic must not dirty the governance repository. Presence and inbox
  events belong under the user's local application-data directory. Claims must
  interoperate with the fleet's existing `~/.agents/claims.jsonl` authority.

## Tracer bullet

```text
Codex session A                         Codex session B
      |                                      |
 SessionStart hook                       SessionStart hook
      | register + heartbeat                 | register + heartbeat
      +-------------+            +-----------+
                    v            v
              local append-only ledger
                    ^            ^
      +-------------+            +-----------+
 MCP send/claim/status                 prompt/tool hook poll
      |                                      |
      +------ integrity-checked message ---->+ additional context
                                             |
                                          MCP ack
```

The smallest end-to-end slice will:

- expose a dependency-free stdio MCP server named `galactic`;
- append integrity-protected presence/message events under
  `%LOCALAPPDATA%/Demerzel/galactic-protocol` (or
  `GALACTIC_STATE_ROOT` when set);
- read and write claims using the schema in `~/.agents/README.md` (or
  `GALACTIC_CLAIMS_PATH` when set);
- inject identity and newly delivered messages with Codex hooks;
- support `status`, `claim`, `claim_update`, `send`, `inbox`, and `ack` tools;
- expose the same shared claim operations as dependency-free CLI verbs for
  non-Codex harnesses;
- install the MCP server and hooks into the user-level Codex configuration;
- verify two simulated sessions can claim, send, receive, and acknowledge.

## Event model

Every ledger row is one JSON object with the Galactic Protocol integrity fields:
`message_id`, `origin_repo`, `origin_agent`, `timestamp`, `content_hash`, and
`hash_algorithm`. The content hash is SHA-256 over canonical JSON excluding
those six integrity fields.

Initial event types:

- `session.started`, `session.heartbeat`
- `message.sent`, `message.delivered`, `message.acknowledged`

State is reconstructed by folding the ledger. This keeps writes append-only,
auditable, and recoverable after a process crash. Claims remain deliberately
advisory: their separate fleet ledger is append-only and the latest line per
`(repo, lane)` wins. The bridge checks for a sequential conflict but does not
misrepresent that convention as a distributed lock server.

## Safety boundaries

- Local stdio only; no listener or network port.
- Runtime state contains no credentials and must never copy environment secrets.
- Message bodies are capped and surfaced as **untrusted cross-session context**,
  never as higher-priority instructions.
- Claims are completed or released by appending a new row with evidence; the
  bridge never rewrites another session's history.
- A session may acknowledge only messages addressed to it or its repo.
- Corrupt or hash-mismatched ledger rows are ignored and reported by `status`.
- Installation merges a named Galactic hook into existing user hooks and leaves
  unrelated configuration intact.

## Trade-offs and deferred work

This slice deliberately avoids a Tauri shell, WebSocket service, cloud relay,
and unsupported desktop app-server injection. Those would add transport and UI
layers before the fleet semantics are proven. A later vertical slice may add a
Windows tray watcher/toast for truly idle-session notification while continuing
to use the same ledger and MCP tools.

## Desktop development roadmap

Official Codex capabilities change the build order. We should use the native
desktop control and Remote surfaces before funding a parallel shell:

1. **Coordination substrate (this slice).** Shared `~/.agents` claims plus the
   local Galactic MCP event ledger and lifecycle-hook delivery.
2. **Native GUI actuation.** Install/enable the Codex Computer Use plugin and
   invoke it with `@Computer` or `@AppName` only for GUI-dependent verification,
   settings, and multi-app flows. On Windows the target stays visible and the
   desktop is foreground-controlled.
3. **Remote supervision.** Use Codex Remote from the official mobile/desktop
   clients to steer active work, approve actions, and review screenshots/diffs.
   Do not build a competing phone-to-PC WebSocket relay.
4. **Claim-aware visual QA.** Before Computer Use edits or tests a repo-owned
   app, read/claim its lane; after verification, append `done` with the commit,
   screenshot, or test evidence. Computer Use is an actuator, never the claim
   authority.
5. **Prime Radiant only on evidence.** Build a custom Tauri dashboard/tray
   watcher only if native Codex notifications, Remote, hooks, and MCP status do
   not provide adequate fleet presence or idle notification.

Safety invariants: one target app/flow at a time; preserve app-by-app approvals;
no unattended credentials, payments, account, security, or privacy settings;
and no Computer Use action may bypass Galactic claims or Codex approvals.

Official references:

- https://developers.openai.com/codex/app/computer-use
- https://learn.chatgpt.com/docs/remote-connections

## Acceptance tests

1. Two sessions register and appear as active with distinct repo/branch/lane.
2. A current claim blocks a sequential conflicting claim; `done` or `released`
   permits the next claimant and every update matches `~/.agents/README.md`.
3. A message to a repo is delivered once by the recipient hook and remains in
   the inbox until acknowledged.
4. Tampered ledger content fails integrity validation.
5. The stdio server completes MCP initialize, tool listing, and a tool call.
6. `pwsh scripts/verify.ps1` passes.

The claim row shape is committed as
`schemas/contracts/session-claim.schema.json`; the implementation also validates
the live fleet ledger without rewriting it.

## Architect decision

Approved for a tracer bullet. The design improves the solution by adding the
missing fleet feedback loop; it improves the process by making ownership and
handoffs observable. The boundary is intentionally modest: near-live at Codex
lifecycle points now, idle-desktop push later if evidence shows it is needed.
