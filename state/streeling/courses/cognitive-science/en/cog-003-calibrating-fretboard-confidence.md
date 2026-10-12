---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Calibrating Confidence in Fretboard Note Identification"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Calibrating Confidence in Fretboard Note Identification

> **Department of Cognitive Science** | Intermediate | 40 minutes | English draft; review and publication pending

## Objectives

You will turn a guitarist's “I am sure” into a probability recorded **before** feedback, calculate a binary Brier score against a verified GA fretboard answer key, distinguish a six-item illustration from a measured learner result, and design a test that could falsify a calibration hypothesis. [COG-002](cog-002-feedback-integrity-fretboard-recall.md) audits whether the displayed key itself is correct. This lesson assumes that audit and asks a different question: **Does a learner's stated confidence match how often their note answers are correct?**

## The project decision

Suppose GA offers a “name this note” exercise on its SVG fretboard. Two guitarists each answer four of six positions correctly. One gives low confidence to the two wrong answers; the other is certain about them. Raw accuracy treats the two equally, but the second learner may need a different prompt or feedback. Before choosing one, we need a score with an explicit event, a trustworthy key, and a test of whether the feedback helps actual learners.

Use GA commit [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). The [demo page](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) declares six position objects; the [SVG component](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) defines string index 0 as high E, fret 0 as open, and default tuning `E, B, G, D, A, E` from high to low. The page does not override that tuning. Its sixth object displays `C` at string 5 fret 3, although low E plus three semitones is **G**. That is a source-level mismatch, not a claim about any user's experience. The corrected note sequence, in demo-array order, is `E, C, G, E, C, G`.

The pinned page calls itself an SVG legacy component test page. The component's [click handler](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) passes only a string/fret coordinate to its callback. These sources do **not** show a confidence input, scored learner session, calibration dashboard, or deployed course flow. Every learner response below is **synthetic teaching data**; no GA user made these predictions for this lesson.

## 1. Define the prediction before giving the answer

For each trial, ask the learner to select a note name `a_i` for a specified string/fret. Then ask for `p_i`, a number from 0 to 1 answering: “How likely is **my chosen note** to match the independently verified key?” This is a probability about correctness of the answer just chosen, not about the chance that the guitar produces sound or that the demo's marker label is trustworthy. Record `a_i` and `p_i` before revealing any note label. Afterward set `y_i=1` if `a_i` matches the verified key and `y_i=0` otherwise.

To construct a usable key, retain string order, tuning, and fret with the source revision. Under standard tuning, the low E string is index 5; E is pitch class 4, so fret 3 has `(4+3) mod 12 = 7`, or G. The sixth displayed `C` cannot be used as the key without the correction documented in COG-002. That one correction is a prerequisite for scoring; this course does not repeat COG-002's full feedback-integrity analysis.

The UI would also need a **new** answer and confidence input. The current click callback supplies a coordinate, not a note prediction or a probability. A proposed trial record is `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}`. The field list is a study design, not an existing GA API. Hiding the answer is also a design requirement: the pinned demo's position objects carry visible labels, so presenting it unchanged would leak the key before `p_i` is captured.

### Practice exercise 1 — Define the event

A learner chooses `C` at string 5 fret 3 and reports `p=0.9`. Against the pinned component's standard tuning, what are the verified note and binary outcome `y`? Does the current click callback record `p`?

> **Answer:** String 5 is low E. `(4+3) mod 12=7`, so the verified note is G and `y=0` for the chosen C. The click callback contains only `{string, fret}` and does not record the chosen note or confidence. The `p=0.9` response is hypothetical.

## 2. Score an explicitly synthetic six-trial trace

The binary **Brier score** is the mean squared difference between the predicted probability and the observed outcome: `BS = (1/n) Σ_i (p_i - y_i)^2`. It ranges from 0 (all probabilities match outcomes exactly) to 1 (maximal error); **lower is better**. Unlike a correct/incorrect count, it distinguishes a 0.9-confidence mistake from a 0.6-confidence mistake. Use the same outcome definition on every item. The following six guesses and probabilities were invented for arithmetic practice; only the coordinates, standard tuning, and corrected key derive from pinned GA source.

| Trial | GA string, fret | Verified note | Synthetic choice | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

The synthetic learner gets four notes right: `accuracy = 4/6 = 0.6667` to four decimal places. The squared losses total `0.01+0.04+0.49+0.16+0.01+0.81 = 1.52`, so `BS = 1.52/6 = 0.2533` to four decimals. Both statistics describe **this invented trace only**. They do not estimate any real learner's ability. If the uncorrected demo label `C` were improperly scored as the key on trial 6, that trial's loss would be `0.01` instead of `0.81`, and the reported Brier score would falsely fall to `(1.52-0.81+0.01)/6 = 0.12`. A good scoring rule cannot repair a bad answer key.

### Practice exercise 2 — Compute the score

Using the six outcomes in the table, compute raw accuracy, total squared loss, and mean Brier score. Which wrong trial contributes the larger loss?

> **Answer:** Four of six are correct, so accuracy is `4/6≈0.6667`. The losses total `1.52`; the Brier score is `1.52/6≈0.2533`. Trial 6 contributes `0.81`, more than trial 3's `0.49`, because its wrong choice carried confidence 0.9 rather than 0.7.

### Practice exercise 3 — Check one confidence bin

Among only the trials with `p_i=0.9`, what fraction is correct and how far is it below the stated confidence? Can this three-trial bin establish stable calibration for a learner?

> **Answer:** Trials 1, 5, and 6 have `p_i=0.9`; two are correct, so the empirical fraction is `2/3≈0.6667`. It is `0.9-2/3≈0.2333` below the stated confidence. Three invented, related trials are far too few and too artificial to establish a stable individual calibration curve.

### Practice exercise 4 — Detect answer-key contamination

If the sixth trial were mistakenly scored against the demo's displayed `C` instead of the verified G, what would happen to its outcome, its loss, and the six-trial mean? Is the resulting lower score evidence of a better learner?

> **Answer:** The synthetic choice C would be marked `y_6=1`, changing its loss from `(0.9-0)^2=0.81` to `(0.9-1)^2=0.01`. The sum becomes `0.72` and the mean `0.72/6=0.12`. The learner made no new prediction; the apparent improvement is a scoring error caused by the wrong key.

## 3. Why squared probability error is a useful target

Let `q` be the actual probability that a chosen answer is correct for a specified class of future trials. If a learner reports `p`, the expected Brier loss is `q(1-p)^2 + (1-q)p^2`. Expanding gives `(p-q)^2 + q(1-q)`. The second term does not depend on `p`, so the expected loss is uniquely smallest when `p=q`. This is the sense in which binary Brier scoring rewards honest probabilities **in expectation**. It does not guarantee that a well-calibrated forecaster wins on every six-trial sample, and it cannot tell whether a wrong answer arose from a string-order mistake, a memory lapse, or misleading feedback.

For example, if the actual correctness chance for a comparable future item class were `q=0.7`, reporting `p=0.7` would have expected loss `0.7(0.3)^2+0.3(0.7)^2=0.21`. Reporting `p=0.9` would have expected loss `0.7(0.1)^2+0.3(0.9)^2=0.25`; the excess `0.04` equals `(0.9-0.7)^2`. The example assumes a known `q` for illustration. The six invented trials do not establish `q=0.7` for real guitarists.

Do not interpret a lower Brier score alone as better musical knowledge. A learner could move toward 0.5 on every item and lower the penalty for confident mistakes without recognizing more notes. Report accuracy alongside Brier, examine performance by strings and frets, and keep the original pre-feedback probabilities. Rewriting `p_i` after feedback would make the score invalid as a measure of the learner's forecast at the time of the answer.

### Practice exercise 5 — Prove the direction of the rule

With a hypothetical true correctness probability `q=0.7`, compare expected Brier loss for reports `p=0.7` and `p=0.9`. Which is lower, and by how much?

> **Answer:** At `p=0.7`, expected loss is `0.7(1-0.7)^2+0.3(0.7)^2=0.21`. At `p=0.9`, it is `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. Honest `p=0.7` is lower by `0.04`. The six-trial teaching data did not measure the assumed `q`.

## 4. Design a learner test that could fail

A falsifiable project hypothesis is: **adding explicit confidence calibration feedback after each verified note answer will lower held-out next-day Brier loss without reducing note-identification accuracy**, compared with showing the correct note alone. Both groups must choose a note and enter confidence before feedback, or their scores will not be comparable. The calibration group could see its recorded confidence, correctness, and cumulative score; the comparison group could see the same verified note and correctness without a confidence summary. This is a proposed experiment, not current GA behavior.

First repair the mislabeled demo position or use a separately audited answer table. Build two label-free prompt states using the same declared standard tuning, and confirm that neither reveals the note before the prediction. Recruit actual learners, record consent and prior fretboard experience, and assign them to conditions before practice. Counterbalance item sets across conditions; keep a held-out set of positions for the next-day test. Log the source revision, item, response, confidence, response time, displayed feedback, and the exact delay. Keep the native UI question separate from an audio or performance task: identifying a diagram coordinate does not prove a learner can play or hear the note.

Predeclare the primary outcome as mean held-out next-day Brier score, with note accuracy as a guardrail. The hypothesis is **not supported** if calibration feedback fails to lower that score relative to the comparison condition, or if any apparent score gain comes with lower note accuracy under the predeclared guardrail. Report uncertainty and the number of learners and items; do not extrapolate from the six-trial synthetic table. A pilot may expose UI misunderstanding or a ceiling effect, prompting a revised test rather than a post hoc success claim. None of these learners, allocations, UI variants, or next-day measurements has been run for this course.

### Practice exercise 6 — Specify a falsifier

An agent says, “The synthetic `0.2533` Brier score proves our confidence feedback improves recall.” Give two reasons this is unsupported, and state one concrete result in the proposed study that would fail its hypothesis.

> **Answer:** The six probabilities and answers are invented, and the pinned GA page has no confidence-feedback intervention or next-day measurement. A controlled study would fail the proposed hypothesis if the calibration-feedback group did not obtain a lower held-out next-day Brier score than the answer-only group, or if a lower score came with a decline in note accuracy under the predeclared guardrail. The study must use a corrected key and capture probabilities before feedback.

## Evidence boundary

The pinned GA sources establish six demo coordinates, default string order, visible labels, and the click payload. The corrected key and the Brier arithmetic are independently checkable calculations. The six choices and probabilities, the `q=0.7` example, the UI variants, and the trial design are teaching constructions. No real learner confidence, calibration change, intervention benefit, browser execution, subject review, fluent-language review, Learn build, or public readback is established here. Those require separate artifacts and reviewers before this draft can be represented as a reviewed or published course.
