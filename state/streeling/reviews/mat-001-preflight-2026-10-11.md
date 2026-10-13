# MAT-001 source and Learn preflight — 2026-10-11

## Source revision and scope

- Demerzel source commit: `0faf880cb115585d8644cb70718267ec31ac396a` on `codex/streeling-project-pilot`.
- Six MAT-001 active-language drafts contain the same pinned GA case and answered direct-proof exercise. This is AI-drafted localization, not fluent human review.
- The new research-cycle and production records validate against `schemas/research-cycle.schema.json` and `schemas/course-production.schema.json`. The production record remains `in_progress`, with review and publish both incomplete.

## Checks performed

- `python -m unittest scripts.test_streeling_course_progress`: 3 tests passed.
- JSON Schema validation with `jsonschema.validate`: both new records passed.
- A focused six-language comparison found the same six pinned GA URLs and matching `SqrtWeight`, `SimilarityWeight`, `double.Epsilon`, `NaN`, `1e-6`, and proof-expression markers in every draft.
- `git diff --cached --check` passed before the source commit.
- In isolated Learn worktree `C:\tmp\learn-pr165-review`, `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` imported source commit `0faf880`: 21 departments, 99 English modules, 73 French, 73 Spanish. The generated EN/FR/ES MAT-001 pages contain the pinned case, exercise identifiers, and that source provenance.
- `npm run build` in the isolated Learn worktree completed: 1,564 pages; Pagefind indexed 1,586 HTML files. The build emitted existing unsupported-code-language and content warnings, but exited 0.

## Limits and next gates

The GA source and test were inspected at their pinned revision; the GA contract test was not rerun for this cycle. This preflight is not a mathematical subject approval, fluent-language review, human learner trial, merged Learn change, live public deployment, or anonymous public readback. The full Demerzel `scripts/verify.ps1` was not rerun in this cycle; the draft PR's CI is the next repository-wide verification gate.
