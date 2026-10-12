# FUT-003 learner transfer task

Do not show the learner the FUT-003 answer blocks or `fut-003-review-brief.md` while they work. This is an **invented** adapter record, not evidence of a deployed agent, reviewer, or page.

The proposed `nova` adapter has three runs. Every run must preserve equal input, output, and review-target source labels; have an approved independent review; and record `build`, `targeted_test`, and `public_readback`. Treat each label here as a synthetic stand-in, not as an authenticated receipt.

| Case | Input/output/review target | Verdict label | Recorded checks | Minutes |
|---|---|---|---|---:|
| D | `fixture-D-v1` / `fixture-D-v1` / `fixture-D-v1` | `pending` | build, targeted_test, public_readback | 12 |
| E | `fixture-E-v1` / `fixture-E-v1` / `fixture-E-v1` | `approved` | build, public_readback | 10 |
| F | `fixture-F-v1` / `fixture-F-v1` / `fixture-F-v1` | `approved` | build, targeted_test, public_readback | 17 |

Write a short decision that answers all five prompts:

1. Which cases are admissible, and which exact gate fails for every rejected case?
2. Should a three-case median be used to promote `nova`? Explain why or why not.
3. What evidence would replace the synthetic source and verdict labels in a real GA/Streeling run?
4. State one predeclared trigger for a limited real trial and one result that would falsify a production switch.
5. State one conclusion that these invented rows cannot establish.

The reviewer will retain your unedited response and score it against the five criteria in the review brief. There is no recorded learner result yet.
