# Learn sync and build preflight for Demerzel `ec66c45` — 2026-10-11

## Inputs

- Demerzel source commit: `ec66c454dff3e8603f14123526a2c2862062a102` on `codex/streeling-project-pilot`.
- Learn generator and site commit: `bdc660f29d888db007204d80ea2bf660dfd2a78b`, the merge of [Learn PR #165](https://github.com/spareilleux/learn/pull/165).
- Isolated Learn worktree: `C:\tmp\learn-pr165-review`; generated output stayed in that worktree and was not committed to Learn.

## Commands and observations

1. `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` exited 0. It reported 21 departments, 84 EN modules, 73 FR modules, and 73 ES modules. The generated `streeling.lock.json` contains the full Demerzel source commit above. The sync rewrote 36 links to site pages and pointed 81 at GitHub.
2. The generator warned that the preserved EN/FR/ES journals do not list several newer modules, including the six new EN lessons. No journal entries were added automatically.
3. `npm run build` exited 0. Astro reported 1,519 pages built, and Pagefind indexed 1,541 HTML files. The `dist/streeling/` routes for DV-006, DV-007, PM-002, PM-003, CS-005, and CS-006 each contained an `index.html` whose content included the expected lesson title.

This is a local integration preflight for draft source. It is not a human review, deployment, or anonymous public readback. The new lessons remain English-only and the Demerzel PR remains a draft.
