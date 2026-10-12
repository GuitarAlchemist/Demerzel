# Streeling human review receipts

This directory holds **human** review evidence for exact course file revisions. It currently contains no approval receipt. Automated preflight notes under `state/streeling/reviews/` are not human verdicts.

For each completed review, create one JSON file named `<module-id>.<locale>.<kind>.json` and validate it against `schemas/streeling-review-receipt.schema.json`. The file records a named or pseudonymous reviewer, the exact course file Git blob, the source commit, the review time and scope, an evidence link, and one verdict. Use `git rev-parse <reviewed-commit>:state/streeling/courses/<department>/<locale>/<filename>` to obtain the blob. The review brief for AUD-001 pins all six initial blobs.

One receipt covers one locale and one kind: `subject`, `language`, or `learner`. A `language` receipt also records `source_english_blob`, the English course blob against which the translation was checked. Reviewing English audio content does not approve translations. A learner task result does not establish subject correctness. An approval becomes stale when the reviewed locale blob changes, or when the English source changes for a language receipt. Do not copy it to a new blob without a fresh reviewer decision. The Git history preserves replaced receipts.

The schema and directory are a draft v0.1 contract. Shape validation does not authenticate a human or establish that the linked evidence is sufficient. Review the evidence and source diff in the PR before setting `verdict` to `approved`. Until then, keep the production pipeline's review and publication flags false.
