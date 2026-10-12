# NET-003 learner transfer task

Give this sheet without NET-003's answers or reviewer brief. This is a **static advisory policy graph**, not a report of live wmux sessions. A worker-to-class edge means the pinned policy declares at least one primary or secondary role in that class after DRAINING mode blocks are applied. The five-class denominator remains `fix`, `groom`, `navigate`, `net_new_feature`, `review`.

| Worker | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 0 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

Answer in your own words:

1. How many worker-class edges survive DRAINING, which classes are covered, and what is coverage using the five-class denominator?
2. Delete **both** `claude` and `codex` from this matrix. How many edges and covered classes remain? Which class is newly lost?
3. A request asks `codex` to perform `autonomous_merge_actor`, a role marked forbidden in the policy. What selector decision should it receive, and why cannot the projected graph alone decide that request?
4. A dry-run selector process exits 0 and returns JSON `decision: "recommend"` for an unblocked secondary role. Does 0 mean the task was authorized or completed? Explain what the two observations actually say.
5. What independent evidence would you collect before claiming that a surviving route can perform a real task now? Name at least a presence or permission check and a result artifact.

The reviewer will retain the unedited response and score it against the five criteria in the review brief. There is no recorded learner result.
