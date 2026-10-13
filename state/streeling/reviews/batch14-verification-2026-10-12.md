# Batch 14 verification — 2026-10-12

Source head `53ae114af72b26aebc254eb969487696874d31d9` on draft Demerzel PR #1207 resolves a prospective course-code collision with open PR #1195. The Gaia lane-admission draft is now optional `CYB-026`; its pinned substantive evidence and five answers are unchanged. The core `CYB-004` number remains available for the proposed foundational feedback course that CYB-005/006 require. PR #1195 and its Learn import PR #161 remain unmerged and unapproved; `cybernetics-identity-reconciliation-2026-10-12.md` records the evidence and remaining findings.

The reporter counts **108 English source drafts but 107 distinct codes within the 001–025 core target**, so 418 core slots remain across the 21 course directories. The 23 department records and zero approved pipeline reviews are unchanged. A new collision field reports zero collisions in this checkout and will expose a duplicate numbered code if source candidates are combined. This is source inventory, not reviewed or published-course progress.

## Verification

- `python -m unittest scripts.test_streeling_course_progress scripts.test_streeling_course_preflight` passed 12 focused tests, including a two-slug/one-code collision fixture and an optional `026` fixture.
- `python scripts/streeling_course_preflight.py cp-cybernetics-2026-10-11-004` passed source metadata, word count, five answered exercises, language declaration, and status checks after renumbering. `git diff --cached --check` passed before commit.
- `pwsh scripts/verify.ps1` exited 0 during the edit sequence. It ran the full Python suite, IXQL grammar tests, and BAML drift check; the final code-count and course-identity edits were followed by the targeted checks above rather than a second full local run. The verifier regenerated `baml_client` line endings; those tool-only changes were restored before commit.
- A fresh Learn sync to isolated output `C:\tmp\streeling-batch14-sync` from clean committed source head `53ae114` reported 21 departments and 108 EN / 80 FR / 80 ES modules. Its lock pins the same full source SHA. The generated English CYB-026 page contains that SHA and answer text; the old CYB-004 Gaia page is absent. This preview was not committed, built, or deployed.
- An anonymous GET to the public CYB-026 route returned HTTP 404 on 2026-10-12. Human subject, learner, fluent-language, final editorial, and public readback gates remain open; the production record keeps review and publish false.

GitHub unit tests, Validate, backlog-facts, CodeQL, risk-report, and most other checks passed on this head when inspected. The automated Claude review failed before content review with `llm_call: API error: invalid x-api-key`; the remaining CodeQL actions job was still pending at that inspection. Neither the failed job nor this static review counts as subject approval.
