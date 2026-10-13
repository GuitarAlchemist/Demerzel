# COG-002 bounded AI subject review — 2026-10-11

## Scope and provenance

- Reviewer: independent Codex AI subagent `pm002_course`, read-only.
- Material: English COG-002 draft and GA `GuitarFretboardTest.tsx` and `GuitarFretboard.tsx` at commit `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- Verdict: **no findings in this bounded source and answer-key review**. The reviewer recalculated the six expected notes as E, C, G, E, C, G against displayed labels E, C, G, E, C, C; five of six match. The sixth marker is low E string, fret 3, so G, while the demo labels it C. G is still a C-major triad tone.
- The reviewer checked the separate string/fret cue controls and optional marker labels, the click callback's `{string,fret}` payload, five answers, local and pinned links, and the 1,804-word count. No browser session or learner outcome was assessed.
- The source finding was reported as [GA issue #832](https://github.com/GuitarAlchemist/ga/issues/832). [Draft GA PR #833](https://github.com/GuitarAlchemist/ga/pull/833) corrects the copied marker in five demos; the course remains a historical exercise against the pinned pre-fix GA revision. The draft PR is not evidence of a deployed fix or learner validation.

This is preliminary AI evidence only. Human cognitive-science and guitar subject, learner, fluent-language, and public Learn reviews remain open. The production record keeps review and publication incomplete.
