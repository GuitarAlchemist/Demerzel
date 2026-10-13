# COG-003 learner transfer task

Give this sheet without COG-003's answer blocks or reviewer brief. These choices and probabilities are **invented for teaching**; they are not learner observations from GA. Use standard tuning with string index 0 as high E and index 5 as low E. A probability is the learner's pre-feedback confidence that **the note they chose** matches the independently checked key.

| Trial | String, fret | Synthetic chosen note | Pre-feedback `p` |
|---:|---|---|---:|
| 1 | 0, 0 | E | 0.8 |
| 2 | 1, 1 | D | 0.6 |
| 3 | 5, 3 | C | 0.9 |
| 4 | 4, 2 | B | 0.7 |

Answer in your own words:

1. Derive the verified note for each coordinate and mark each outcome `y=1` for correct or `0` for incorrect. Do not copy the pinned demo's mistaken low-E fret-3 label.
2. Compute each `(p-y)^2`, the total, the four-trial mean Brier score, and raw accuracy.
3. If trial 3 were scored against a displayed `C` instead of the verified note, what would its loss and the reported mean become? Did any learner become better?
4. Why must the answer and confidence be captured before feedback, and why does the existing GA coordinate click alone not provide this study record?
5. Name one held-out comparison that could test confidence feedback with real learners and one accuracy guardrail or result that would reject the proposed benefit.

The reviewer will retain your unedited response and score it against the five criteria in the review brief. No learner result is recorded.
