# INF-004 learner transfer task

Give this sheet without the INF-004 course answer blocks or reviewer brief. This is a synthetic handoff decision, not an observed GA agent session.

An agent receives three notes, each saying `ready`. For this classroom decision, integration requires `tests_passed`, `single_writer`, and `review_approved` to be true. A false accept costs 6 invented units; a false reject costs 2.

| Note | Tests passed | Single writer | Review approved |
|---|---|---|---|
| E | true | true | false |
| F | true | true | true |
| G | false | true | true |

Answer in your own words:

1. Which notes satisfy the toy rule? Why can the headline alone not determine the answer?
2. Calculate the mean cost over these three cases if the receiver accepts every `ready` note. Calculate it if the receiver rejects every note.
3. Name the information the receiver needs for this specific decision. Explain why a free-form `tests pass` sentence is weaker than a checkable test receipt.
4. The note has a short Git head and zero dirty lines. Does that prove that the review saw the same source or that a test passed? State what you would check.
5. Give one concrete observation that would falsify a claim that F is currently ready for integration, even though all three booleans in the table are true.

The reviewer should preserve the unedited response, relevant experience, elapsed time, sources consulted, confusion, corrections, and any retest. No learner result is recorded in this file.
