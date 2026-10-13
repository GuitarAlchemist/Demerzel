# Learn sync preflight for Demerzel `0220ca8` — 2026-10-11

## Inputs and command

- Demerzel source commit: `0220ca84a25f59973bd6b9236cc00b7f68631a50` (`codex/streeling-project-pilot`).
- Learn generator commit: `1d6e30bc1c174786ef3eedfa44424d4b4d483bcf` from [Learn PR #165](https://github.com/spareilleux/learn/pull/165), subsequently merged as `bdc660f29d888db007204d80ea2bf660dfd2a78b`.
- Command in an isolated Learn worktree: `node scripts/sync-streeling.mjs --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot --out C:\tmp\learn-streeling-preflight-20261011-0220ca8`.
- The output root was a temporary preflight directory, not the Learn publication branch.

## Observed output

The command exited 0 and reported 21 departments, 81 English modules, 73 French modules, and 73 Spanish modules. It rewrote 32 links to site pages and pointed 71 links at GitHub. The generated `streeling.lock.json` recorded the full Demerzel source commit above. English pages for DV-006, PM-002, and CS-005 were present under `src/content/docs/streeling/` in the temporary output.

This proves only a local generator run for that source snapshot. The earlier Learn PR #165 build passed independently, before this source sync. The combined generated tree has not been built or deployed, and no anonymous readback or review approval is claimed for these three drafts.
