# Department of IX Research — Course Catalog

**Head:** skeptical-auditor
**Established:** 2026-10-16
**Subject:** experiments on [IX](https://github.com/GuitarAlchemist/ix), the GuitarAlchemist Rust workspace

Every number in this department comes from a receipt: a pinned commit, a result file or a test run, named beside the number. A result whose receipt was lost is reported as lost. Code links are pinned to full commit hashes, so they keep pointing at the code that produced the result.

## Courses

| Code | Title | Level | Duration | Languages |
|------|-------|-------|----------|-----------|
| IXR-001 | Streams Under Budgets: Back-Pressure, a Learned Gate and a Petri Check | Intermediate | 40 min | en, fr, es |

IXR-001 is in `en/ixr-001-streams-under-budgets.md`, with its translations under `fr/` and `es/`. It has no research-cycle record: it was written from a tracer slice run in a Claude Code session, and it waits for a human review.

## Research index

Five studies of 2026-09-22 to 2026-10-16. The first is taught in IXR-001; the others are planned as IXR-002 to IXR-005.

### 1. ix-stream: streams under budgets

- **Code:** [`crates/ix-stream`](https://github.com/GuitarAlchemist/ix/tree/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream) at commit [`14dccd0`](https://github.com/GuitarAlchemist/ix/commit/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab), branch `exp/loop-nodes`. SQL nodes followed in [`944f42c`](https://github.com/GuitarAlchemist/ix/commit/944f42ccae4d996b0432d2211dfa9b0f2022cc31).
- **What it is:** JSON values flow through a graph of threads joined by bounded channels, with back-pressure up to a `duckdb -jsonlines` source and cancellation upstream; a lossy algedonic bus carries feedback; a gate routes each item to one expert with a per-context UCB1 bandit minus a shadow price paced on each budget, under a hard cap; an SSE feed with event ids, `Last-Event-ID` resumption and replay draws an ECharts page; and the graph is checked as a Petri net before it runs.
- **Result:** 663 router questions (221, three passes), Jev answers replayed from recorded receipts, Jev budget $0.0320792472 (265.2 recorded calls). Waiting on the chosen lane, the learned gate scores a mean 0.833 over seeds 1 to 5 against 0.791 for "Jev until spent", 4.1 points higher on every seed, with 265 Jev calls each; the local router alone scores 0.688. Without waiting, Jev's capacity binds: 84 calls happen and both policies land between 0.71 and 0.73. A retry loop of waiting links deadlocks (1728 markings explored); a lossy link frees it.
- **Taught in:** IXR-001.

### 2. ix-wasm: pipeline stages in any WASI language

- **Code:** [`crates/ix-wasm`](https://github.com/GuitarAlchemist/ix/tree/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-wasm), built in four commits on `exp/loop-nodes`: [`dfaaef6`](https://github.com/GuitarAlchemist/ix/commit/dfaaef6b551cac904d651bf79e96b318fd76d468) (the sandbox, Go builds), [`6229c60`](https://github.com/GuitarAlchemist/ix/commit/6229c6060d0716331d3aa1e5fcf652d841005de7) (the `wasm.run` pipeline skill), [`8ce2a29`](https://github.com/GuitarAlchemist/ix/commit/8ce2a29f541b00f05090be7211d79098af905a08) (all of WASI preview 1 linked, files and sockets closed), [`4cf71df`](https://github.com/GuitarAlchemist/ix/commit/4cf71dfc57e9ca66d14726a0d659177c4e0f325b) (Zig beside Go, one content-addressed builder).
- **What it is:** a stage is a WASI command module, JSON in on stdin and JSON out on stdout, run in the wasmi interpreter. Every preview 1 function is linked, so modules from any toolchain load, but no directory is preopened: path and descriptor functions answer `EBADF`, sockets and signals `ENOSYS`, and imports outside preview 1 are refused. Each run is bounded by fuel, memory and output caps; the clock moves 1 µs per reading and the random source is seeded, so two runs on one input give the same output and spend the same fuel. Builds are cached under a BLAKE3 hash of the language, the toolchain version and the source; Go builds with `GOPROXY=off` and cgo off, Zig runs `build-exe` on one file and never a `build.zig`.
- **Measured (commit messages):** a Zig 0.17 ReleaseSmall stage with 3 imports runs correctly in 0.2 ms on 116,370 fuel; Zig's `std.Io` (30 imports, 14 closed) and V 0.5.2 through C and `zig cc` now load and run correctly; V's own wasm backend still produces an invalid module; a Zig program that opens a file gets `EBADF` and exits 1. Zig's default 16 MiB stack made each run start by zeroing it (10 ms instead of 1 ms), so Zig stages are built with a 64 KiB stack.
- **A trap worth keeping:** without wasmi's `auto-dispatch` feature, an unoptimized build dispatches through tail calls that LLVM does not make at opt-level 0, and the host stack overflows on the first long wasm loop.
- **Planned:** IXR-002.

### 3. ix-loop: loops that write loops

- **Code:** [pull request 383](https://github.com/GuitarAlchemist/ix/pull/383) on GuitarAlchemist/ix, open, head [`dd6a42a`](https://github.com/GuitarAlchemist/ix/commit/dd6a42a48f93f4e8db0ad44b379bdce4a56b1c00) (ADR-0011).
- **What it is:** agentic loops written in sandboxed Lua 5.4 (only `table`, `string`, `math`, `coroutine` and `utf8`; `load` takes text only; 64 MB per state; only JSON crosses between loops) that run, judge and write other loops. A budget counts fuel, calls, a deadline and depth (at most 3); a child's share is carved out of its parent's and the unspent part is refunded, so the root's budget bounds the whole tree. The semantic node runs `claude -p` headless with no tools on the person's plan. `tasks.judge` runs a draft on instances that no loop in the run has seen, which closes the Goodhart trick of the experiment's first run, where the writer returned the shown instance's answer instead of a loop. Loops can only propose; a person accepts.
- **Evidence (PR body):** one test per line of the slice's "done when" list, 14 tests in all; six fuel-escape routes closed and tested, including two `xpcall` handler routes found by a probe during review. Known limit: one long call into C, such as a backtracking `string.find`, runs to its end before the hook can stop it.
- **Planned:** IXR-003.

### 4. The Jev router study, pre-registered

- **Data and results:** [`state/router-spike/RESULTS.md`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/RESULTS.md), [`jev/full/stage3-comparison.json`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/jev/full/stage3-comparison.json) and [`jev/musicse/stage4-comparison.json`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/jev/musicse/stage4-comparison.json), at ix commit `7c37c8c` on `main`.
- **What it is:** TypeSafe's hosted zero-shot classifier `jev-1.13.0` against GA's local embedding router, each stage pre-registered with its decision rule before any call, scored with exact McNemar tests.
- **Stage 3, all 32 skills (221 model-written prompts):** Jev 209 right, the arena router `c2-merge` 152, production 145; Jev is right where `c2-merge` is wrong on 64 prompts and the reverse on 7 (p ≈ 1.3e-12). Escalating to Jev on a decline or a margin below 0.05 gives 211 but sends 133 of 221 prompts (60%) to Jev.
- **Stage 4, human-written questions (87 scored Music Stack Exchange titles):** Jev 82, `c2-merge` 54, production 42. Production routes 45 of the 86 questions no skill can answer to a skill; Jev routes 5.
- **Spend:** 970 calls in all experiments, about $0.060 computed from reported tokens at the rate card, not an invoice.
- **Planned:** IXR-004.

### 5. Node design: a family times a verb

- **Source:** a French design draft of 2026-10-16 (*Flux, experts et nœuds Claude Code : le tri*), written in the session that built ix-stream. It is not in a repository; this entry is its summary.
- **The rule:** a node is one family times one verb. A family is one resource, for example `claude`, `jev`, `wasm`, `artifact`, `skill`, `mcp`, `gh`, `voice` or `ga`; its verbs are `read`, `write`, `run` and `manage`; every node is off by default and has its own budget.
- **What follows:** writing is `claude.ask` with an output schema, not a new node; reviewing is a host oracle (validation, tests, a tool's schema), with any LLM judge panel used only to refuse by default; managing is the existing store, where a loop proposes and only a person accepts; running needs two nodes because it touches two resources, `skill.run` (headless Claude Code with one skill) and `mcp.call` (one tool of a named MCP server).
- **Agentic roles are skills, not node kinds:** a review, a proposal or a web search is `skill.run` with an existing skill, and each call declares the tools it grants: none by default, the web only when granted, never personal data. A new role is a new skill, written and reviewed through the `artifact` family.
- **Status:** a proposal. `claude`, `wasm` and the proposal store exist in ix-loop and ix-wasm; `skill.run` and `mcp.call` do not.
- **Planned:** IXR-005.

## Related departments

Computer Science (agentic loops, CS-002), Cybernetics (the algedonic channel, CYB-001), MetaQA (oracles and held-out tests), Systems Engineering (interfaces between stages), Psychohistory (preregistration, PSY-025).
