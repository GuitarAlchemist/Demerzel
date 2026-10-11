---
module_id: vc-002-godot-react-bridge-evidence
department: visual-computing
course: Evidence for a Godot and React Observatory Bridge
level: intermediate
prerequisites: [vc-001-accessible-fretboard-paths]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-11-002
version: "0.1.0"
---

# Evidence for a Godot and React Observatory Bridge

> **Department of Visual Computing** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Separate a React iframe host, a planned Godot scene, and a verified running 3D observatory.
- Trace `godot:ready` and `godot:node-clicked` messages through the host's source check and callbacks.
- Write a measurable readiness and click-source contract with a fixed fixture and a future live check.
- State exactly what a source read can and cannot prove about a web export or rendering technology.

## The project question

An observatory card in GA offers a Godot 3D view. A teammate says, “The React bridge is checked in, so the Godot scene is ready; the 3D click path works.” What evidence would justify that claim?

At GA revision [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), [`GodotScene.tsx`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/GodotScene.tsx) implements a React host with panel and fullscreen iframe views. Its default `src` is `/godot/index.html`. It declares TypeScript message types, listens for browser `message` events, handles `godot:ready` and `godot:node-clicked`, and exposes callbacks. The checked-in [Godot integration plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md) checks Phase 1's bridge/embed work but leaves the constitutional-gravity Godot scene and WASM web export unchecked. The plan is stored under `docs/plans/parked/` despite its older “active” header; neither label is runtime proof.

A tracked-path scan of this pinned GA tree found no `.gd` or `.tscn` scene, `godot/index.html`, `.wasm` export, or file named for DLSS. That is a bounded repository finding, not proof about other branches, a developer's machine, deployed assets, or every possible implementation name. A forked DLSS rendering path is outside the inspected bridge and remains unverified. The component's iframe and fallback text do not establish that a Godot export exists or runs.

### Practice exercise 1: sort the evidence

Classify each claim as **source-supported**, **planned or unverified**, or **requires a live run**: (a) React declares an iframe defaulting to `/godot/index.html`; (b) the Godot gravity scene renders policy nodes; (c) clicking a real Godot node selects the corresponding React record; (d) forked DLSS improves the observatory image.

> **Answer:** (a) is source-supported by the pinned React component. (b) is a planned scene with unchecked work in the pinned plan. (c) requires a real scene/export and an observed callback trace; the host declaration alone cannot prove it. (d) is unverified in the inspected tree and requires a separately identified implementation and measurement.

## 1. Define a small bridge contract

The host's outbound TypeScript union includes `{ type: 'godot:ready' }` and `{ type: 'godot:node-clicked', nodeId: string }`. Its message handler checks `ev.source` against the mounted iframe's `contentWindow` **when the iframe ref exists**. It then checks that `ev.data.type` is a string and branches on the two message types. A matching-source `godot:ready` sets an internal ready ref, clears the loading state, and invokes `onReady`. A matching-source `godot:node-clicked` invokes `onNodeClick` with `msg.nodeId`.

These are source-level behaviors, not a full trust or readiness contract. The handler does not compare `ev.origin`, does not validate `nodeId` at runtime, and does not require ready before accepting a click. If the iframe ref is absent, the source comparison is skipped. The TypeScript `as GodotOutboundMessage` assertion does not validate an incoming browser event. Outbound messages use `postMessage(msg, '*')`; a future cross-origin deployment needs an explicit target-origin decision. For this lesson's fixture, assume the iframe is mounted and both callbacks are installed, so the source comparison applies.

### Practice exercise 2: check the sender

A window other than the mounted iframe posts `{ type: 'godot:ready' }`. The mounted iframe then posts the same message. Which one invokes `onReady` under the fixture assumptions? Does a matching `ev.source` alone establish that the payload is valid or the scene rendered?

> **Answer:** The foreign window's message is rejected by the handler's source comparison. The mounted iframe's message sets the ready ref and invokes `onReady`. Source equality is only one check: the handler does not inspect origin or validate payload fields at runtime, and a ready message does not prove that the scene rendered a frame.

## 2. Trace a fixed synthetic message fixture

This is a **reasoning fixture**, not a browser test or an observed Godot run. Let `F` be the mounted iframe's `contentWindow`, and `X` another window. Begin with `readyRef = false`, `loading = true`, and callback counters at zero. Deliver these events to the host handler in order:

| Step | Source | Event or clock | What the pinned handler does |
|---|---|---|---|
| 1 | X | `{ type: 'godot:ready' }` | Ignores it because source differs from F |
| 2 | F | `{ type: 'godot:node-clicked', nodeId: 'belief-7' }` | Calls `onNodeClick('belief-7')` even before ready |
| 3 | F | `{ type: 'godot:ready' }` | Sets ready, clears loading, calls `onReady` |
| 4 | F | `{ type: 'godot:ready' }` again | Calls `onReady` again; no deduplication is coded |
| 5 | F | `{ type: 'godot:node-clicked', nodeId: 'belief-8' }` | Calls `onNodeClick('belief-8')` |
| 6 | clock | Fifteen-second timeout fires | Finds ready true and makes no fallback change |

The fixture predicts **two ready callbacks and two click callbacks**, including one click before ready. It does not claim that Godot actually emitted any of these messages. If no ready message arrives, the timeout hides the loading indicator after 15 seconds without setting the ready ref or an error; “spinner gone” is not “scene ready.” The host's panel mode initially shows the Builder tab, so an iframe may not be mounted until the Viewer tab is selected.

### Practice exercise 3: count callbacks

Using only the table and the pinned handler, list the callback sequence. What should an observatory dashboard avoid inferring from step 6?

> **Answer:** The callbacks are `onNodeClick('belief-7')`, `onReady()`, `onReady()`, then `onNodeClick('belief-8')`. Step 1 produces none. The timeout in step 6 produces none because ready is already true. In a run with no ready event, the timeout can still remove the spinner, so a dashboard must not infer readiness from the spinner disappearing.

## 3. Make the desired behavior measurable

A future product contract can be stricter than today's handler. For one mounted iframe and one load generation, propose: accept ready only from the expected source and allowed origin with a valid payload; count **one** readiness transition; accept a click only after that transition, from the same source and origin, with a nonempty known `nodeId`; deliver each intentional click to React **exactly once**. A reload begins a new generation and resets the counters. This is a proposed acceptance rule, not a description of current code. Steps 2 and 4 in the synthetic fixture would fail its pre-ready and duplicate-ready conditions.

After a real Godot scene and web export exist, a live bridge check could use a **dedicated test host that keeps the iframe mounted for one load generation**. Record the build SHA and browser, wait for one ready event, perform **20 known node clicks**, and compare the 20 expected IDs to 20 callback IDs in order with no duplicates. The pinned [Prime Radiant parent](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/ForceRadiant.tsx) switches to detail after a recognized panel click and closes the fullscreen view after its click callback; a 20-click run in that product host would need a reopen and fresh-ready step for each click. Inject foreign-source and pre-ready synthetic messages in the dedicated harness and require **zero foreign-source callbacks** and **zero pre-ready click callbacks**; resend ready and require no second transition. Record the message source, origin, payload validation result, callback count, and a frame-render or screenshot observation. A screenshot alone cannot prove click routing; a callback trace alone cannot prove the Godot scene rendered correctly. Until those observations exist, the contract is a test proposal.

### Practice exercise 4: test readiness

A live trial reports that the loading spinner disappeared after 15 seconds but records no `godot:ready` message. May the trial count the scene as ready? Name one further observation needed.

> **Answer:** No. The host's timeout clears loading without setting readiness. Record a valid ready event from the mounted iframe under the chosen origin and payload rules, and observe a rendered frame or another explicit scene-ready signal before claiming that the 3D view works.

### Practice exercise 5: set a pass condition

An eventual dedicated-host test sends 20 known clicks after ready, receives 19 matching React callbacks, and gets one callback from a foreign window. Does it pass the proposed contract? State the expected and observed counts, and name one artifact needed before running it.

> **Answer:** No. The contract requires 20/20 ordered, exactly-once callbacks and zero foreign-source callbacks; the trial has 19/20 known callbacks and one foreign-source callback. A versioned Godot scene and web export served at the iframe URL are needed before this can be a live scene test. Preserve the build SHA and event trace to diagnose the missing and foreign callbacks.

## Key takeaways

- A checked-in React host is evidence of a host and handler, not evidence of a running Godot scene.
- Ready messages, loading indicators, rendered frames, and click callbacks are separate observations.
- Source, origin, payload shape, load generation, and callback counts belong in a measurable bridge contract.
- The current handler accepts pre-ready clicks and repeated ready messages in the fixed reasoning fixture; a stricter product rule needs implementation and live testing.
- An unchecked plan phase or an absent file in one pinned tree is a limit on the claim, not a universal statement about all environments.

## Project evidence and limits

- Pinned GA [`GodotScene.tsx`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/GodotScene.tsx), [Prime Radiant parent](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/ForceRadiant.tsx), and [parked Godot integration plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md). The source check covered this pinned tree; it did not execute the scene or audit a deployment.
- [VC-001](vc-001-accessible-fretboard-paths.md) addresses a separate requirement: a 3D view must preserve useful information and available actions for pointer, keyboard, and screen-reader paths. The bridge contract here does not complete that accessibility check.
- The six-step fixture and 20-click acceptance threshold are teaching and proposed-test artifacts. No Godot runtime, WASM export, forked DLSS implementation, subject review, learner attempt, localization, or public readback has been verified for this lesson.

*Research: `visual-computing-2026-10-11-002`. English draft only; review and publication pending.*
