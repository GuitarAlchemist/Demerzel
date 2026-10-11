# Learn sync and build preflight at Demerzel 54d68c2 — 2026-10-11

This is an isolated local preflight, not a public release, anonymous readback, human review, or localization approval.

- Source: Demerzel `54d68c284c139102e11d6703bd67748b5bb0eaba`. Learn isolated worktree `C:\tmp\learn-pr165-review` is based on merged Learn commit `bdc660f29d888db007204d80ea2bf660dfd2a78b`; the primary Learn checkout was not edited.
- `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` exited 0. `streeling.lock.json` recorded 21 departments, 96 EN / 73 FR / 73 ES source modules and the full source commit. The sync rewrote 51 links to site pages and pointed 99 to GitHub. Hand-written EN/FR/ES journals still warn that new modules are missing from their lists.
- `npm run build` exited 0: 1,555 pages built and 1,577 HTML files indexed. The FUT-002, GTR-004, and WML-002 English `dist/streeling/` routes exist. FR/ES fallback routes do not add translations to the 73/73 source counts.
- [Governance Validate run 38179576310](https://github.com/GuitarAlchemist/Demerzel/actions/runs/38179576310) passed all seven jobs on source commit `54d68c2`, including unit tests and BAML drift. [Cross-Model Code Review run 38179576312](https://github.com/GuitarAlchemist/Demerzel/actions/runs/38179576312) failed before reviewing content because `llm_call` reported `API error: invalid x-api-key` (exit 3); it supplies no review verdict.

The source PR is still draft. Human subject/learner/language checks, public Learn deployment, and anonymous readback remain open.
