# Streeling revision-bound review display

Status: draft implementation plan. Related: [Learn #169](https://github.com/spareilleux/learn/issues/169), Demerzel PR #1207.

## User problem and success condition

Streeling needs a trustworthy path from AI-authored source to a human-reviewed course. The current production record has a boolean review phase, while Learn renders one hardcoded unreviewed warning for every imported module. When a reviewer approves AUD-001, the site must show exactly which source and language were reviewed and must stop showing that verdict if the course changes. This work prepares that path; it does not create a human verdict.

## Assumptions and counterargument

- A human subject reviewer, a fluent language reviewer, and a learner can supply different evidence. Their verdicts should not collapse into one boolean.
- The strongest simpler option is to keep every page labeled unreviewed and publish a human-maintained journal. That avoids a new contract, but cannot accurately display mixed review status across 525 courses or invalidate a stale approval after editing.
- Hidden costs are reviewer identity and evidence verification, Git-blob handling across line endings, translations whose English source changes, and maintenance of stale receipts. A JSON receipt cannot authenticate a human by itself; repository review and linked evidence remain necessary.

## Reversible tracer bullet

1. Add a draft JSON schema and a receipt directory in Demerzel. A receipt covers one module, one locale, one review kind, one exact Git blob, one verdict, one named or pseudonymous reviewer, and one evidence path or URL. A language receipt also binds the English source blob used for comparison. No approval files are added before an actual review.
2. In Learn, read receipts from the pinned clean Demerzel source and compare each receipt's blob to the imported course file's Git tree object. Ignore `not_assessed` and `changes_requested` for approval display. Fail closed on malformed, duplicate, or conflicting receipts rather than guessing.
3. Render separate per-page subject, fluent-language, and learner states. Show an approved status only for a matching locale and source blob. Keep the site-owner's personal journal status separate. On the overview, report mixed counts instead of “all unreviewed” or “all reviewed.”
4. Test missing, matching, stale, wrong-locale, and duplicate receipts using a tiny Git fixture. Confirm source SHA links and normal link rewriting remain intact. Run an isolated Demerzel-to-Learn sync. Do not deploy an unreviewed course merely to exercise the display.

This is additive and reversible: the draft receipt files can be ignored by older Learn versions, and no existing production fields are changed. Do not freeze the schema until an actual AUD-001 human review and a Learn pilot expose its missing fields.

## Rejection and revisit

Reject this approach if a reviewer cannot produce evidence tied to a stable source blob, if the generator displays an approval after any source edit or locale change, or if the interface implies that a language review also proves learner success. Revisit after the named AUD-001 reviewer completes the brief and a learner task has a recorded outcome. A production flag alone never proves approval.
