# Batch 12 verification — 2026-10-12

Source head `c7e932e` on draft Demerzel PR #1207 adds PHY-003 (sampling/aliasing at the GA guitar-engine boundary) and SEM-003 (agentic status signs and their evidence). Each has an English source, FR/ES/PT/IT/DE AI-drafted localizations, a research cycle, a production record, five answered exercises, and an independent AI subject plus cross-language semantic preflight. The source inventory is **106 EN drafts, 21 packages with all six active-language source files, zero approved pipeline reviews** across 21 course directories. On that denominator, 419 EN drafts remain for the 525-course target; 23 department records still exist.

## Evidence and review limits

- PHY-003 computes exact sample counts, Nyquist limits, theoretical E2 partial boundaries, and synthetic single-sine folds using pinned GA audio-engine code and the GAS-001 fixture. No high-frequency alias measurement, browser capture, or listening result was performed for this course. The independent subject review found no issue. Independent localization review found one stale EN sentence about translation/review status; it was corrected and retested. See `phy-003-subject-preflight-2026-10-12.md`.
- SEM-003 checks a pinned SEM-002 production record, bounded AI review, schema, reporter, preflight, and dated public baseline. Independent subject review found a research-record P2 overclaim that evidence-scoped handoffs *prevent* overclaiming without an experiment. The hypothesis and evidence were narrowed to confirmed pinned-file facts; a focused retest found the issue resolved. Independent localization review found no actionable semantic discrepancy. The handoff benefit remains untested. See `sem-003-subject-preflight-2026-10-12.md`.
- These are bounded AI checks. Human subject, fluent-language, learner, final editorial, and public-deployment gates remain open. Both production records keep `review.completed=false` and `publish.completed=false`.

## Source and local Learn checks

- `python scripts/streeling_course_preflight.py cp-physics-2026-10-12-003 cp-semiotics-2026-10-12-003 cp-audio-engineering-2026-10-12-004` passed schemas, identity, declared language files, English word counts, answered-exercise counts, and status consistency.
- `python -m unittest scripts.test_streeling_course_preflight scripts.test_streeling_course_progress` passed 10 tests. `python scripts/backlog_facts.py` left `BACKLOG.md` unchanged. `git diff --cached --check` passed before the source commit.
- In isolated Learn worktree `C:\tmp\learn-pr165-review`, `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` reported source `c7e932e`, 21 departments, **106 EN / 78 FR / 78 ES** modules. `npm run build` exited 0, built **1,585 pages**, and indexed **1,607 HTML files**. PHY-003 and SEM-003 EN/FR/ES static routes exist with the source SHA and answer text. Sync still warns that hand-written journals omit many new modules. The current Learn sync does not render PT/IT/DE; generated pages were not committed or deployed.

## Public readback

Anonymous GET requests to `https://spareilleux.github.io/learn/streeling/physics/phy-003-sampling-aliasing-guitar-engine/` and `https://spareilleux.github.io/learn/streeling/semiotics/sem-003-status-signs-and-evidence/` returned HTTP **404** on 2026-10-12. These source drafts are **not publicly published**. The isolated local build is a preflight, not a publication receipt.
