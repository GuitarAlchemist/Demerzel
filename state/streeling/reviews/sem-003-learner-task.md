# SEM-003 learner transfer task

Give this sheet without SEM-003's answer blocks or reviewer brief. The case below is **invented**. Revisions `A` and `B` are labels for two different source blobs, not real Git SHAs.

An agent reports: “EXAMPLE-001 is ready, reviewed, and published; the tests are green.” The available records actually say:

- English source revision `A` exists. A bounded **automated source and answer-key check** at A reported no findings.
- The production record says `in_progress`, `review.completed=false`, and `publish.completed=false`. There is no authenticated human subject or learner receipt.
- Learn generated a local page linking to A. An anonymous GET of the intended public route returned 404 on the observation date.
- After those checks, the author edited the course to revision `B`. No check or reviewer verdict is tied to B.

Answer in your own words:

1. Which parts of the agent's sentence have supporting evidence, and which words are too broad? State what “ready” could mean if qualified.
2. Does the automated “no findings” result establish that a human reviewed the course? Explain its actual scope.
3. What does the local generated page prove, and what does the anonymous 404 show at the observation time? What would you inspect after a later deploy?
4. May the check at source A automatically cover edited source B? What identity and diff check is needed next?
5. Write a three-sentence handoff to a second agent that names a revision, one completed bounded check, the missing gates, and one concrete next action without inventing a publication result.

The reviewer will retain the unedited response and score it against the five criteria in the review brief. No learner result is recorded.
