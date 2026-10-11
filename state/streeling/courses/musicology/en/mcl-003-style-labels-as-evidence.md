---
module_id: mcl-003-style-labels-as-evidence
department: musicology
course: "Musicology: Style Labels as Evidence"
level: intermediate
alchemical_stage: albedo
prerequisites: [mcl-002-musical-form]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: musicology-2026-10-11-003
version: "0.1.0"
---

# When Is a Style Label Evidence?

> **Department of Musicology** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to distinguish a catalog label from an observation about a performance, read a progression record without silently adding missing details, compare catalog entries at the right level, and write a source-aware style caption for Guitar Alchemist (GA). You will also be able to specify what a future listening check must record before a claim about an actual recording is warranted.

## Project question and evidence boundary

GA has a checked-in [progression catalog](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.Config/ChordProgressions.yaml) with fields such as `Name`, `RomanNumerals`, `Category`, `Chords`, `Structure`, and `Examples`. It also has a separate [domain record](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Core/Theory/Harmony/Progressions/ProgressionCorpusItem.cs) declaring `StyleLabel`, `Chords`, and `Source`. Both links pin GA commit `dc2e74cbd992a298f67efb928b5b3754615e1924`. **When may a GA screen show a progression's `Category` as catalog metadata, and what evidence would support a statement about the style of a performed recording?**

The catalog can answer the first part: it tells us what an editor stored at that revision. It cannot answer the second part by itself. A chord list is neither audio nor a transcription with independently checked timing, instrumentation, articulation, and context. The catalog's named song examples and `UsedBy` lists are source claims too; this lesson does not treat them as verified music history. The code record's required `Source` property is an instruction to carry attribution, not proof that every instance has been independently audited. The YAML and C# record are separate artifacts; this lesson does not assert a loader or mapping between them.

In [MCL-002](mcl-002-musical-form.md), you learned about form. Here the focus is the evidence behind a **style label**. A catalog category and a heard performance answer different questions.

## 1. Read the unit that carries the label

Start with the top-level `ii-V-I` record. It has `Category: "Jazz"`, `InKey: "C Major"`, Roman numerals `ii7, V7, I`, and chords `Dm7, G7, Cmaj7`. These are four distinct fields. The label belongs to the catalog entry; it is not a property measured from a particular waveform. The key and chord spellings explain how this instance is written in the file. They do not establish that every performance of a ii–V–I uses those voicings, that it is always jazz, or that the named song examples use this exact sequence at every occurrence.

A GA display can say: “`ii-V-I` — category in GA catalog: Jazz; example in C major: Dm7–G7–Cmaj7.” The word *catalog* gives the label its provenance. “Jazz recording” would need performance evidence.

The `ProgressionCorpusItem` code reinforces the attribution problem. `StyleLabel` and `Source` are required strings, and `Chords` defaults to an empty read-only list. A required value could come from an editor, performer, listener, or classifier. A UI or dataset export should show the source and claim type rather than treating `StyleLabel` as validation.

### Exercise 1 — Extract without upgrading

From the pinned catalog, give the `ii-V-I` category, key, Roman numerals, and chord names. Then write one permitted caption and one unsupported caption for a recording you have not heard.

> **Answer:** Category `Jazz`; key `C Major`; Roman numerals `ii7, V7, I`; chords `Dm7, G7, Cmaj7`. Permitted: “GA catalog labels `ii-V-I` as Jazz and gives Dm7–G7–Cmaj7 in C major.” Unsupported: “This unheard recording is jazz because it contains Dm7–G7–Cmaj7.” The file supplies the first statement's fields; it supplies no observation of the recording.

## 2. Count what is encoded; keep descriptive claims separate

The `12-Bar Blues` entry provides a stronger structural clue than a name alone. Its `RomanNumerals` list has twelve positions: `I, I, I, I, IV, IV, I, I, V, IV, I, V`. Its `Chords` list also has twelve: `E, E, E, E, A, A, E, E, B, A, E, B`. The entry says `InKey: "E Major"` and `Category: "Blues"`. If we interpret each position as a measure in the entry's intended template, positions 5 and 6 are `IV`/`A`; position 9 is `V`/`B`; position 12 is `V`/`B`, a candidate turnaround back to the first `I`/`E`. The positional arithmetic is checkable in the file. Actual tempo, bar duration, repeats, omissions, and performed chord qualities remain unknown.

The same record's `Structure` reads “AAB lyrical form over 12 measures.” Its chord arrays contain no lyrics or audio, so they cannot independently demonstrate AAB lyric organization. We can report the catalog's description, but cannot claim its chords prove that a specific singer delivered AAB lines. A particular take would need direct checking.

### Exercise 2 — Count and locate

How many chord positions occur in the pinned `12-Bar Blues` top-level `Chords` list? What are positions 5, 6, 9, and 12? Can that list alone verify the entry's AAB lyrical description?

> **Answer:** There are twelve positions. Using one-based positions, 5 = `A`, 6 = `A`, 9 = `B`, and 12 = `B`. No: the `Chords` array contains chord symbols, not words or a recorded vocal structure. AAB is an additional catalog description.

## 3. A form label is not a performed arrangement

`Rhythm Changes` illustrates a different shape of record. It has `Category: "Jazz"` and `Structure: "AABA form with specific harmonic rhythm"`. Instead of a top-level `Chords` or `RomanNumerals` list, it has an `ASection` and a `BSection`. The A section lists `I, vi, ii, V` over `Bb, Gm, Cm, F`; the B section lists `III, VI, ii, V` over `D, G, Cm, F`. A reader may compare those section templates, but must not flatten them into an asserted full performance. The source does not specify how many times each four-chord segment is played, how long each chord lasts, the actual harmonic rhythm, or what a particular band played.

“AABA” names an ordering of sections above individual chord events. Sketching A–A–B–A from the two arrays interprets the catalog; it does not document a take. A performance annotation would require section boundaries, timestamps, and a recording or score reference. This record does not encode a total bar count.

### Exercise 3 — Identify the missing top level

List the first chord of `Rhythm Changes` `ASection` and `BSection`, and say whether the record has a top-level `Chords` array. What remains unverified about a performance?

> **Answer:** `ASection` begins with `Bb`; `BSection` begins with `D`. The record has no top-level `Chords` array. Its AABA `Structure` and section arrays do not verify a particular performance's section timing, repeats, duration, instrumentation, or even that the performer followed the template.

## 4. Repeated catalog text is not independent corroboration

The `I-vi-IV-V` record has top-level `Category: "Pop"`, a C-major example `C, Am, F, G`, and a nested `Variations` item named `vi-IV-I-V` with `Am, F, C, G` and `Context: "Pop ballad version"`. The nested variation does not declare its own `Category`; it sits under a parent that does. Elsewhere the same YAML contains a separate top-level `vi–IV–I–V (Pop Loop)` entry, using en dashes in its name, with `Category: "Pop"`, `InKey: "C Major"`, and `Chords: ["Am", "F", "C", "G"]`.

The two appearances show the same four-chord order in a nested variation and standalone entry. They are not independent listening studies or evidence that every song using those chords is a pop ballad. The variation's `Context` is editorial prose, not a measured recording feature. A display should name the parent and child relationship.

For a future style study, select actual performances and record the analyzed interval, observed features, labeler, and disagreements. A chord sequence is a retrieval key; performance, production, and cultural context also matter. Define labels before scoring examples.

### Exercise 4 — Compare levels

Where does `vi-IV-I-V` appear under `I-vi-IV-V`, what four chords does it use, and how does the separate top-level `vi–IV–I–V (Pop Loop)` differ as a record? Does the duplication independently validate a genre?

> **Answer:** It is a nested `Variations` item with `Context: "Pop ballad version"` and chords `Am, F, C, G`; it has no own `Category` field. The standalone `vi–IV–I–V (Pop Loop)` is a top-level record with its own `Category: "Pop"` and the same chord order. Both are statements within one catalog, so their repetition does not independently verify the genre of any recording.

## 5. Write a caption and a testable next step

A careful GA caption separates three layers. First, identify the **stored object**: a named progression entry at a pinned revision. Second, identify the **stored claim**: a category or form label and any explicitly listed example chords. Third, state the **performance status**: no recording has been assessed here. This pattern is useful even when the catalog is accurate, because the reader can see what can be checked and what would require additional work. A revision link lets another learner reproduce the lookup later; an unpinned link could silently point to changed data.

Suppose a screen presents the `12-Bar Blues` template next to an uploaded recording. Before analysis, it may say: “GA catalog template: Blues; E-major example, twelve listed chord positions.” It should not yet say “the upload is a blues performance.” A future live check could ask two trained listeners to mark section boundaries and chord events on a specified timestamp interval, retain the audio reference and annotation versions, and compare their findings with a declared matching rule. For example, require at least ten of the twelve expected harmonic positions to align in order, while reporting deviations and disagreements. That threshold is a **proposed study rule**, not a validated genre criterion and not a test run for this draft. Meeting it would support a template-match statement; a broader style judgment would still need a defined rubric and relevant performance evidence.

The required `Source` string in `ProgressionCorpusItem` might point to a catalog, score, annotation, or audio file. It needs a claim-specific interpretation. A future YAML-to-corpus mapping would need verification before assuming `Category` and `StyleLabel` are synchronized.

### Exercise 5 — Choose defensible product copy

Draft one sentence for a GA screen showing the catalog's `12-Bar Blues` entry beside an unheard upload. Then name two observations or records needed before making a claim about the upload's performed style.

> **Answer:** “GA catalog template `12-Bar Blues` is categorized as Blues and lists twelve chord positions in E major; the upload has not been assessed.” For a later claim, retain an identified audio interval with timestamped chord/section annotations and a stated style rubric applied by identified reviewers or a validated classifier. The catalog entry alone supports the template caption, not the upload's genre.

## Limits and research basis

This is a source-reading lesson, not an audio analysis. No recording, score edition, timestamped transcription, classifier output, or listener agreement was tested. The catalog's descriptions, song examples, `UsedBy` names, and historical implications remain unverified in this cycle. The proposed listening threshold is an exercise in designing a falsifiable check; it has not been calibrated. The pinned code shows declarations for a domain record, not runtime provenance checks or a proven import route from the YAML. Human subject review, learner testing, localization, and publication remain pending.

The primary evidence is the pinned [GA progression catalog](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.Config/ChordProgressions.yaml) and pinned [`ProgressionCorpusItem` declaration](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Core/Theory/Harmony/Progressions/ProgressionCorpusItem.cs). The lesson's confidence applies to extraction of fields and counts from that exact revision, not to the independent truth of its genre or song associations.
