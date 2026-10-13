# Batch 11 verification — 2026-10-12

Source head: Demerzel `9f15c4776b0837040b195f33636e35c62738f1d5` on draft PR #1207. This batch repairs AUD-001 in EN, FR, ES, PT, IT, and DE. It changes no course-count denominator: 104 English source drafts, 19 source packages with all six active-language files, and zero approved pipeline reviews across 21 course directories. The 23 department records remain unresolved as to target scope.

## Source and review gates

- `python scripts/streeling_course_preflight.py cp-audio-engineering-2026-10-12-004` passed schemas, source metadata, declared languages, English word count, answered exercises, and status consistency.
- `python -m unittest scripts.test_streeling_course_preflight scripts.test_streeling_course_progress` passed 10 tests.
- `python scripts/backlog_facts.py` left `BACKLOG.md` unchanged; `git diff --cached --check` passed before the source commit.
- Independent AI subject and cross-language static review findings and corrections are documented in `aud-001-subject-preflight-2026-10-12.md`. Human subject, fluent-language, learner, and final editorial review remain pending. The synthetic operator example is not an executed compressor or guitar processing comparison.

## Isolated Learn build

In `C:\tmp\learn-pr165-review`, `npm run sync:streeling -- --source C:\Users\spare\source\repos\Demerzel-streeling-project-pilot` reported source `9f15c47`, 21 departments, 104 EN / 76 FR / 76 ES modules. The EN, FR, and ES generated AUD-001 pages cite the full source SHA. `npm run build` exited 0, building 1,579 pages and indexing 1,601 HTML files. The three AUD-001 static HTML routes exist and contain the guitar-focused text, `0.25` synthetic delta, and full source SHA. Sync warned that journals are missing many new modules. Learn currently renders EN/FR/ES, not PT/IT/DE; no Learn commit or deployment was made.

## Public readback

The public [AUD-001 route](https://spareilleux.github.io/learn/streeling/audio-engineering/aud-001-eq-compression-order/) still serves the older vocal-centered version, titled “EQ and Compression Order: Why Signal Chain Matters,” with open-ended vocal exercises and historical research cycle `audio-engineering-2026-03-23-001`. The revised guitar draft is therefore **not published**. A successful local build does not satisfy the public-readback gate.
