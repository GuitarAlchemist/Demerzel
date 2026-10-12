# Batch 13 verification — 2026-10-12

Source head `bd4c1328373181daf5e28e9ab62d448d997b32a2` on draft Demerzel PR #1207 adds COG-003 (confidence calibration with the GA fretboard demo) and GAS-003 (a proposed open-E decay calibration trial). Each has an English source, FR/ES/PT/IT/DE AI-drafted localizations, a research cycle, a production record, and answered exercises. The source inventory is **108 EN drafts, 23 packages with all six active-language source files, zero approved pipeline reviews** across 21 course directories. On that denominator, 417 EN drafts remain for the 525-course target; 23 department records still exist.

## Evidence and review limits

- COG-003 uses pinned GA fretboard code to correct the demo's string-5-fret-3 label and compute an explicitly synthetic six-prediction Brier example. An independent AI subject check and a separate EN-to-five-locale semantic-parity check found no actionable issue. No real learner calibration or next-day intervention was tested. See `cog-003-subject-preflight-2026-10-12.md`.
- GAS-003 uses saved GAS-001 selected-window RMS measurements and pinned GA Rust decay code. Its `0.9978` to `0.9976` comparison, feedback coefficients, and proposed ≤1.8 dB classroom gate are calculations and a trial design, not a candidate render or product standard. Independent AI subject and EN-to-five-locale semantic-parity checks found no actionable issue. See `gas-003-subject-preflight-2026-10-12.md`.
- These are bounded static AI checks. Human subject, fluent-language, learner, final editorial, and public-deployment gates remain open. Both production records keep `review.completed=false` and `publish.completed=false`.

## Source and local Learn checks

- `python scripts/streeling_course_preflight.py cp-cognitive-science-2026-10-12-003` and the same command for `cp-guitar-acoustics-2026-10-12-003` passed schemas, source metadata, declared languages, word counts, answered exercises, and status consistency.
- `python -m unittest scripts.test_streeling_course_preflight scripts.test_streeling_course_progress` passed 10 tests. `python scripts/backlog_facts.py` left `BACKLOG.md` unchanged. `git diff --cached --check` passed before the source commit.
- In isolated Learn worktree `C:\tmp\learn-pr165-review`, `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` reported source `bd4c132`, 21 departments, **108 EN / 80 FR / 80 ES** modules. `npm run build` exited 0, built **1,591 pages**, and indexed **1,613 HTML files**. COG-003 and GAS-003 EN/FR/ES static routes exist with the source SHA and answer text. Sync warns that hand-written journals omit these and many other new modules. The current Learn sync does not render PT/IT/DE; generated pages were not committed or deployed.

## Public readback

Anonymous GET requests to `https://spareilleux.github.io/learn/streeling/cognitive-science/cog-003-calibrating-fretboard-confidence/` and `https://spareilleux.github.io/learn/streeling/guitar-acoustics/gas-003-decay-calibration-open-e/` returned HTTP **404** on 2026-10-12. These source drafts are **not publicly published**. The isolated local build is a preflight, not a publication receipt.
