# DV-001 Learn publication preflight — 2026-10-11

This is a local build preflight, **not** public publication or a course review verdict.

## Inputs and isolation

- Demerzel source: pilot branch commit `a0b30010b3aaff320486016d83fb971850314828`, rebased onto `origin/master` at `260226f`.
- Learn: isolated worktree `C:\tmp\learn-streeling-preview-20261011`, based on `origin/main` at `fe8e38444d882c28691dce9f12c21ac2ad404ec0` plus the duration-localization generator fix `1d6e30b` ([draft PR #165](https://github.com/spareilleux/learn/pull/165)). The user's dirty Learn checkout was not edited.
- Command: `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot`, followed by `npm run build`.

## Observed result

- Synchronization succeeded and `streeling.lock.json` pinned Demerzel commit `a0b30010b3aaff320486016d83fb971850314828`: 21 departments and 77 EN / 73 FR / 73 ES generated module pages.
- Astro build exited 0 and reported 1,498 pages built. The three DV-001 HTML files exist under `dist/streeling/`, `dist/fr/streeling/`, and `dist/es/streeling/` with the expected Data Visualization slug. Each contains the June 8 and July 19 exercise dates and the pinned source commit link. The ES page has `35 minutos` in its generated banner.
- The sync reported 11 new module IDs missing from each hand-written Streeling journal, including DV-001 through DV-004. Journals were preserved by the generator.

## Remaining before publication

1. Complete the human subject, fluent-language, and learner gates in `dv-001-review-brief.md` and record their actual results.
2. Make the Demerzel source commit reachable on GitHub; the local preview's source links use that commit SHA.
3. Integrate the Learn generator fix, update the hand-written EN/FR/ES journals, synchronize the reviewed source into Learn, and run its build again.
4. After deployment, perform anonymous public readback of the EN/FR/ES lesson and index pages. Local `dist/` files cannot prove that public gate.

The current production record remains `review_pending`; this preflight does not change it.
