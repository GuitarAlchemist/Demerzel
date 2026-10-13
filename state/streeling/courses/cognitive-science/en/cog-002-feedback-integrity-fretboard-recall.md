---
module_id: cog-002-feedback-integrity-fretboard-recall
department: cognitive-science
course: Feedback Integrity for Fretboard Recall
level: early-intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-11-002
version: "0.1.0"
---

# Feedback Integrity for Fretboard Recall

> **Department of Cognitive Science** | Level: Early intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Check a displayed fretboard answer against a stated string order, tuning, and fret calculation.
- Separate a visible cue, a learner's prediction, a verified answer, and a later attempt in a practice record.
- Explain exactly what GA's pinned SVG fretboard displays and what its click callback records.
- Identify a wrong answer key without turning a source-code observation into an unsupported claim about learning outcomes.

## The project question

A guitarist looking at GA's SVG fretboard demo sees a set of positions called a C-major chord. Could the displayed note labels serve as the answer key for a **predict the note, then check** exercise? This is a practical cognitive-science problem: feedback can only correct a prediction if its answer key is trustworthy. If the key is wrong, a learner's correct response can be marked wrong, while an incorrect response can look correct. That is a risk to investigate, not evidence that any particular user has already learned the wrong note.

Use one fixed source revision throughout this lesson: GA commit [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). The [demo page's six position objects](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) are the exercise fixture. The [SVG component's type and default tuning](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) define how to read the positions. The page is explicitly a **test page for the SVG legacy component**; its name is not evidence of an automated test or a deployed learning flow.

[COG-001](cog-001-your-brain-lies-to-you.md) surveys general cognitive biases. [GTR-001](../../guitar-studies/en/gtr-001-the-fretboard-map.md) teaches the fretboard map. Here the task is narrower: make a particular GA practice prompt checkable, and specify what an observed learner response would have to contain. There is no experiment about memory or skill improvement in the pinned sources. The idea that an unaided prediction followed by verified feedback might help this task remains a teaching hypothesis until tested with learners.

## 1. Fix the orientation before checking the key

The component states that `string: 0` is the **high E** string and uses zero-based strings `0–5`. Its default tuning array is `['E', 'B', 'G', 'D', 'A', 'E']`, explicitly high to low. This differs from the common spoken list “E A D G B E” given low to high; reversing the order while keeping the same string index will produce confident but wrong answers. The demo passes six strings and leaves the default tuning in place.

For this fixed standard-tuning fixture, advance one semitone per fret. Equivalently, assign pitch classes `C=0, C#=1, ..., B=11`, add the fret number to the open string's pitch class, and reduce modulo 12. Spell the resulting pitch class as a note name. For example, the low E is `E=4`; at fret 3, `(4+3) mod 12 = 7`, which is **G**. This arithmetic checks the label at a position; it does not tell us whether the whole chord shape is comfortable, correctly fingered, or audible.

| String index | Open string | Fret | Calculated note | Demo label | Match? |
|---:|---|---:|---|---|---|
| 0 | high E | 0 | E | E | yes |
| 1 | B | 1 | C | C | yes |
| 2 | G | 0 | G | G | yes |
| 3 | D | 2 | E | E | yes |
| 4 | A | 3 | C | C | yes |
| 5 | low E | 3 | **G** | **C** | **no** |

Five of six displayed labels match the calculated notes. The sixth position is still a C-major **chord tone** because G belongs to the C–E–G triad. The defect is more precise: its individual note label is wrong. The demo also marks that position with `emphasized: true` and the same red color used for its other C-labeled positions. Since the component documents `emphasized` as an optional emphasis such as a root note, the visual cue could reinforce the wrong label in a root-finding task. The source does not establish how a user interprets that color.

### Practice exercise 1: read the coordinate system

The demo includes `{ string: 5, fret: 3, label: 'C' }`. Which open string does index 5 name, and what note does the fret calculate under the component's default tuning? Show the pitch-class arithmetic.

> **Answer:** Index 5 is the low E, because the array runs from high E at index 0 to low E at index 5. E has pitch class 4; `4 + 3 = 7`, and pitch class 7 is G. The calculated note is G, so the displayed C is inconsistent with this fixed tuning and fret.

### Practice exercise 2: audit all six answers

List the calculated notes in demo-array order, count matching labels, and say whether the name “C-major chord positions” is itself disproved by the mismatched label.

> **Answer:** The calculated sequence is `E, C, G, E, C, G`; the displayed sequence is `E, C, G, E, C, C`, giving five matching labels out of six. G is a note in a C-major triad, so this calculation does not disprove the chord-tone collection. It identifies one incorrect **marker label**, at string 5 fret 3.

## 2. Separate the prompt from the feedback

The component has three different kinds of text cue. `showFretNumbers` controls numeric fret labels along the bottom. `showStringLabels` controls the six open-string tuning labels. Each position object's optional `label` controls the text inside that individual position marker; the [render branch checks `pos.label`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L239-L318). Hiding string labels does **not** hide the note names inside populated position markers. Conversely, leaving fret and string labels visible does not require a note label inside a marker.

For a proposed prediction task, a designer could render one fixed set of marker coordinates without their optional `label` fields, ask the learner to state a note, and then render a verified answer separately. That describes **two prepared states**, not an implemented reveal feature. The pinned test page supplies labels immediately; it has no answer input, correctness check, delayed reveal control, or learner history. This boundary matters because reading the current code cannot establish how people behave in a flow that does not yet exist.

The safe answer key must be derived from the same declared tuning and coordinates as the prompt, then audited independently. Do not copy the demo's sixth `label` into both the prompt and the validator: the duplicated error would make a failing lesson look internally consistent. A minimal record for an actual study would include the pinned source revision, string and fret, tuning, cue state, the learner's answer before feedback, the verified key, when feedback appeared, and any later answer. Without those fields, “the user clicked G” is not a trace of recall.

### Practice exercise 3: identify the visible cue

Suppose a render sets `showStringLabels: false` and `showFretNumbers: true`, but passes the original six position objects unchanged. Which texts disappear, and is the incorrect `C` inside the sixth marker hidden?

> **Answer:** The six open-string tuning labels disappear; fret numbers remain. Every supplied position `label` still renders inside its marker, so the incorrect sixth `C` remains visible. A prediction-before-answer state would need to omit or otherwise withhold position labels; the existing page does not provide a tested reveal toggle.

## 3. What an interaction can and cannot measure

The component's [`handlePositionClick`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) creates a new object containing `{ string, fret }` and passes it to the optional `onPositionClick` callback. Marker circles call that handler when clicked. The callback does not include the original position's `label`, a typed note guess, correctness, or feedback time. A click can show which coordinate was selected, if a parent records the callback; it cannot by itself say what note the learner believed was there.

Here is a deliberately **synthetic** two-attempt trace for the same item. It is not an observed GA user session: before correction, a learner says `C` for string 5 fret 3; after a verified `G` answer is shown, the learner says `G` on an immediate retry. Scored against the corrected key, this is `0/1` then `1/1` on that item. It shows a changed answer in the fixture. It does not establish independent recall tomorrow, transfer to another fret, or a benefit of one cue design over another. Those questions need an appropriate learner test with a stated interval, comparison, and actual recorded answers.

### Practice exercise 4: inspect the evidence from a click

If a parent listens to `onPositionClick` and receives `{ string: 5, fret: 3 }`, can it score whether the learner predicted G? Name two missing observations.

> **Answer:** No. The callback sends the selected coordinate only. At minimum the parent would need the learner's stated note **before** feedback and a verified answer key tied to the current tuning; it would also need cue/feedback timing to evaluate a predict-then-check flow. The callback's lack of `label` is especially important because the source demo's label for this coordinate is wrong.

### Practice exercise 5: limit a learning claim

Using the synthetic trace above, calculate both item scores against the verified G key. Which narrower claim is supported, and which larger claim is unsupported?

> **Answer:** The first answer C scores `0/1`; the immediate second answer G scores `1/1`. The synthetic record supports only that the fixture's response changed after the supplied correction and that its immediate score improved. It cannot show that any real GA user improved, retained G later, or benefited from delayed reveal; no such user measurement appears in the pinned artifacts.

## Project evidence and next check

The source-level finding is concrete: at the pinned GA revision, one of six displayed note labels disagrees with the component's string order and standard tuning. A small independent pitch-class calculation of the six fixed entries produced `E, C, G, E, C, G` and a `5/6` label match. That calculation did not run a browser, an automated UI test, or a learner study. The source code shows available props and rendering branches; it does not prove the page is deployed or used for education.

Before using this demo as feedback, correct and test the answer key at the same revision as the rendered component. For any proposed predict-then-check experience, test the two visible states and record a real pre-feedback response before making claims about recall. This course remains an English draft. It has not received subject review, a learner attempt, localization review, Learn sync/build, or publication verification.

## Pinned sources

- [GA `GuitarFretboardTest.tsx` at `dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx): the six labeled demo positions and page configuration.
- [GA `GuitarFretboard.tsx` at the same commit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx): string indexing, default tuning, optional labels, click payload, and SVG rendering.
