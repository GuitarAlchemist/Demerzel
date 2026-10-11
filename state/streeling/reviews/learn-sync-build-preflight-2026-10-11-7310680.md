# Learn sync and build preflight at Demerzel 7310680 — 2026-10-11

This is a local, isolated Learn worktree check. It is **not** a public release, anonymous readback, translation approval, or course review verdict.

- Source: Demerzel commit `7310680da6c1b3fce5bca50847e164977414a10a` on `codex/streeling-project-pilot`. Learn worktree: `C:\tmp\learn-pr165-review`, based on merged Learn commit `bdc660f29d888db007204d80ea2bf660dfd2a78b`; the user's primary Learn checkout was not edited.
- `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` exited 0. The lock recorded the full Demerzel commit, 21 departments, and 90 EN / 73 FR / 73 ES source modules. It rewrote 43 links to site pages and pointed 99 to GitHub. The generator warned that the hand-written EN/FR/ES journals omit newer modules; it preserved those journals.
- `npm run build` exited 0: 1,537 pages built and 1,559 HTML files indexed by Pagefind. The six English output routes for AUD-002, PHY-002, VC-002, INF-002, NET-002, and MCL-003 exist under `dist/streeling/<department>/<module-id>/index.html`.
- Starlight also builds FR/ES fallback routes for an English-only module. Inspection of the INF-002 French HTML found its French-language fallback notice before the English lesson. Those routes do not count as French or Spanish source translations; the lock's 73/73 counts remain the language-coverage measure.
- AUD-002's WAV references were rewritten to GitHub blob links pinned at the synced Demerzel commit. This preflight did not test download, playback, listening quality, accessibility in a browser, or public hosting.

Publication still requires the source PR review gate, localizations and human checks as applicable, a Learn publication change, and anonymous route readback.
