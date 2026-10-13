# Batch 8 source and Learn verification — 2026-10-11

## Source scope

At Demerzel source commit `497a299`, this batch adds English drafts AUD-003, CS-007, and VC-004, with one research-cycle record, one in-progress production record, and five answered exercises each. Their independent AI subject preflights are recorded in `aud-003-subject-preflight-2026-10-11.md`, `cs-007-subject-preflight-2026-10-11.md`, and `vc-004-subject-preflight-2026-10-11.md`. CS-007's first review found a draft-versus-wire-schema contradiction; the source was corrected and the same independent reviewer confirmed the fix. MAT-001's independent English math preflight is also recorded in this commit. These are bounded AI reviews, not pipeline or human approvals.

## Checks performed

- Both JSON records for each of the three new lessons validated against the repository's research-cycle and course-production schemas. All three production records remain `in_progress` with translation, review, and publish incomplete.
- Recorded whitespace word counts and answer blocks matched source: AUD-003 2,148 words and five answers; CS-007 1,899 and five; VC-004 2,120 and five.
- `python -m unittest scripts.test_streeling_course_progress`: three tests passed. `git diff --cached --check` passed before the source commit.
- `python scripts/streeling_course_progress.py` reported 21 course directories, 23 department records, 102 English drafts, 16 six-language complete modules, and zero approved pipeline reviews. The provisional 21-directory target leaves 423 English drafts to reach 25 each; issue #1209 still asks which department set is canonical.
- In isolated Learn worktree `C:\tmp\learn-pr165-review`, `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` imported commit `497a299`: 102 EN / 73 FR / 73 ES modules across 21 directories. `npm run build` exited 0 with 1,573 pages and a Pagefind index of 1,595 HTML files. Each new EN lesson has a generated source page and static HTML route with `497a299` provenance.

## Limits and next gates

The Learn worktree is a local, generated preview; it was not committed, merged, deployed, or read anonymously on the public site. The new lessons have no French, Spanish, Portuguese, Italian, or German drafts. Their proposed audio, IXQL, Godot, and human-task experiments were not run. Human subject review, fluent localization, learner trials, formal pipeline review, publication decision, and public readback remain open. The full Demerzel `scripts/verify.ps1` was not rerun for this batch; the draft PR's CI is the next repository-wide verification gate.
