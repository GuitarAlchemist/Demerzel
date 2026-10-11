---
module_id: sem-002-chord-symbols-and-canonicalization
department: semiotics
course: "Chord Symbols, Canonicalization, and Meaning in GA DSL"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-11-002
version: "0.1.0"
---

# Chord Symbols, Canonicalization, and Meaning in GA DSL

> **Department of Semiotics** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to identify the entered sign, parsed chord structure, canonical rendering, and pitch-class projection in Guitar Alchemist (GA). You will trace five fixed examples through pinned source or tests, distinguish lexical equivalence from musical interpretation, and design labels that tell a GA user which transformation produced each value.

## The project question

Suppose a guitarist enters `Cmi7` into a GA tool. A downstream result displays `Cm7`. Did GA hear a performance, change the chord, or normalize a written symbol? The pinned [chord parser](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.DSL/Parsers/ChordParser.fs), [renderer](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.DSL/Generators/ChordRenderer.fs), and [service](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.DSL/Services/ChordDslService.fs) answer a narrower, useful question: **Which distinctions in entered chord notation survive parsing and canonical rendering, and which are projected away?** All GA links in this lesson pin commit `dc2e74cbd992a298f67efb928b5b3754615e1924`.

[SEM-001](sem-001-signs-in-governance.md) used signs to inspect governance documents. Here a **signifier** is the string a musician types, such as `Cmi7`; the parser produces a structured **interpretation** in an abstract syntax tree (AST); and the renderer emits a preferred written symbol. This is a computational account of the code's behavior, not proof of what a player hears or intends. The spelling can matter in a key or score even when a machine calculation groups notes by pitch class. Treat those as separate statements with separate evidence.

## 1. Entered text and canonical text

The service defines `Normalize` as `Parse` followed by `Render` when parsing succeeds. The parser accepts several notational signs for minor quality, including `min`, `mi`, and `-`; the renderer writes the minor quality as `m`. The pinned [normalization test cases](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.DSL.Tests/ChordDslTests.cs) include `Cmi7 → Cm7` and `D-7 → Dm7`. The source explains why: the root and components survive in an AST, while the particular characters used to express minor quality are replaced by the renderer's convention.

This is a many-to-one transformation at the text level. Given only the resulting `Cm7`, one cannot recover whether the user typed `Cmi7` or `Cm7`. The transformation is useful for search, deduplication, and consistent display, provided the screen tells users that they are seeing a canonical symbol. If exact user notation matters for editing or provenance, retain it in a separate entered-text field. A canonical value should not silently overwrite the only copy of the entered text.

The evidence here is a checked-in test **declaration** and the implementation. This lesson has not rerun the test suite. The named cases are verifiable against the test source, but they do not prove that every notation a guitarist might use parses, that a UI calls this service, or that the rendered string captures every harmonic intention.

### Exercise 1 — Trace two spellings

What canonical strings do the pinned tests expect for `Cmi7` and `D-7`? Which part of each written sign changes, and what would be lost if GA stored only the canonical output?

> **Answer:** The expected outputs are `Cm7` and `Dm7`. The entered minor markers `mi` and `-` become `m`; the root letters and `7` remain. If only the output is stored, the original minor-marker spelling cannot be reconstructed.

## 2. A symbol is made of parser fields

A chord symbol is not parsed as one indivisible label. The [AST type](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.DSL/Types/ChordAst.fs) has `Root`, `RootAccidental`, optional `Quality`, a list of `Components`, and optional `Bass`. The parser tries an initial note letter, optional accidental, optional quality, zero or more extensions or alterations, and optional slash bass. The renderer then writes each field in a fixed order. This field separation lets a tool ask what a token denotes inside this implementation instead of guessing from typography alone.

For `EbΔ9`, the flat belongs to root `E`, `Δ` selects `Major` quality, and `9` is an extension. The renderer spells the root `Eb`, major quality `maj`, and extension `9`, yielding `Ebmaj9`. That exact input-output pair is also in the pinned tests. The `Δ` sign is a convention within the DSL's accepted grammar; its change to `maj` is a rendering decision. It does not say how the chord is voiced, what key surrounds it, or how a performer articulates it. A UI might display both “entered: EbΔ9” and “canonical: Ebmaj9” to preserve the distinction.

The parser's ordering matters. It tests certain multi-character extensions before shorter components. This prevents `13` from being split into `1` and `3`, and its comment says `maj7` should be consumed as a whole extension rather than a bare `maj` quality followed by `7`. These are code-level tokenization rules. They should not be converted into claims about a universal chord-notation standard; a different notation system could tokenize the same surface differently.

### Exercise 2 — Explain a glyph substitution

Using the pinned parser, renderer, and test case, what fields account for `EbΔ9 → Ebmaj9`? Does the test establish a particular guitar fingering?

> **Answer:** Root `E` with flat accidental produces `Eb`; `Δ` gives `Major` quality; `9` is an extension. The renderer outputs `Ebmaj9`. No fingering is encoded in that input-output assertion, so the test does not establish a voicing or a sounded performance.

## 3. Do not confuse an AST field with the displayed word

`Fmaj7/A` is a useful trap for a reader who expects `Major` in the AST's `Quality` field. In the pinned parser, bare `maj` is blocked when followed by a digit; `maj7` is then consumed as a whole `Extension "maj7"` token. Consequently, the source-derived AST for this input has root `F`, no explicit quality value (`Quality=None`), one `maj7` extension, and bass `A`. The renderer writes root `F`, no separate quality marker, component `maj7`, and slash bass `/A`, producing `Fmaj7/A`. The pinned normalization tests give that output.

This does **not** mean a musician would call the written chord “quality-less.” It means the implementation stores the `maj7` marker under `Components` rather than under `Quality` for this parse. Treating internal field names as a complete theory of musical meaning would confuse a code representation with its object. A diagnostic view can show “parsed quality field: none” while a musician-facing view shows the canonical chord symbol. The bass field records slash notation, not a measured bass note in any particular take.

The same distinction affects generated explanations. If an assistant sees `Quality=None`, it should not confidently tell the learner “there is no major quality here” without considering the `maj7` component. A good explanation can cite both fields and the canonical rendering. This is where semiotics becomes a product-quality tool: the program's internal sign structure is useful, but its labels need interpretation before they reach a musician.

### Exercise 3 — Inspect a non-obvious parse

For `Fmaj7/A`, identify the source-derived root, `Quality` field, component, bass, and canonical output. Why is “no major implication” an unsound conclusion from `Quality=None` alone?

> **Answer:** Root `F`; `Quality=None`; component `Extension "maj7"`; bass `A`; canonical output `Fmaj7/A`. The parser represents `maj7` as a component, so the empty quality field alone does not describe the complete symbol.

## 4. Token boundaries and structured alterations

The pinned test for `C13#11b9` checks that parsing succeeds, the root is `C`, and the AST contains **three** components. The parser explains the expected decomposition: `13` is an extension, `#11` an alteration, and `b9` another alteration. This is a source-derived interpretation of the exact string; the test itself asserts the count but does not independently assert the three component names. Distinguishing those two kinds of evidence makes the exercise reproducible without inflating the test's coverage.

The characters `#` and `b` here modify numbered degrees inside the symbol; they are not the root accidental. The parser handles an optional root accidental immediately after the note letter, then reads later components. A system that reports only “contains sharp and flat” would erase this syntax and likely mislead the reader. A structured display could instead say “root C; extension 13; altered 11 sharp; altered 9 flat,” while retaining the original `C13#11b9` for comparison.

This example does not establish an actual voicing, a chord-tone inventory on a specific instrument, or whether a particular guitarist would prefer that notation. It demonstrates the parser's decomposition and the shape of the checked-in assertion. An actual runtime check would call the pinned build with this input and compare its AST, while a listening claim would require a separate recorded performance.

### Exercise 4 — Count components precisely

How many components does the pinned `C13#11b9` test require? Name the source-derived component categories and explain why the root is still `C`.

> **Answer:** The test requires three components. The parser's alternatives yield `Extension "13"`, `Alteration(Sharp, "11")`, and `Alteration(Flat, "9")`. The root is `C` because the root parser consumes the first letter and there is no accidental immediately after it; the later `#` and `b` belong to components.

## 5. Projection is a different claim from spelling

The pinned [`domain.projectChord` closure](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L424-L486) accepts a `symbol` and requested `fields`. Among other fields, it can emit `root` from the parsed letter and accidental and `pc` from a semitone calculation modulo twelve. In the source's note mapping, C is zero, D is two, sharp adds one, and flat subtracts one. Therefore the source predicts `root=C#`, `pc=1` for `C#`, and `root=Db`, `pc=1` for `Db`. Those are derived outcomes for this fixed input pair, **not** an executed closure result in this lesson.

The two root strings differ while their projected pitch-class numbers agree. Projecting both to `1` deliberately removes spelling. That can be useful for chromatic comparison, but it is not a license to replace the entered root in a score or assert identical harmonic function. C sharp and D flat can carry different spelling implications in context. Neither `root` nor `pc` alone tells us the key, the guitarist's intention, the instrument's tuning, or a sounding note's octave. A useful UI labels the values “entered symbol,” “canonical symbol,” “parsed root,” and “root pitch class” so that equality in one field does not masquerade as equality everywhere.

The parser ends with `run pChord` and shows no explicit end-of-input requirement. That is a source-level reason to test how trailing text behaves before advertising strict full-string validation. This lesson does not claim that a malformed example is accepted or rejected at runtime. It also does not infer that any particular GA screen currently displays the closure's projected fields. The product recommendation is to present provenance clearly when a screen does use them.

### Exercise 5 — Compare signs and a numeric projection

For inputs `C#` and `Db`, predict `root` and `pc` from the pinned `domain.projectChord` source. Which equality is established, and which stronger conclusion would need musical context?

> **Answer:** The source predicts `C#`: `root=C#`, `pc=1`; `Db`: `root=Db`, `pc=1`. Their root pitch-class projections are equal, while their root spellings differ. Equal `pc` does not prove identical notation, key function, voicing, or heard performance.

## Limits and next check

This lesson reads a pinned implementation and checked-in tests; it does not claim a fresh test run, a live UI observation, or a listening study. The tests cover named examples, not all user spellings. The parser's lack of an explicit end-of-input check is a prompt for a dedicated boundary test, not a measured runtime result. The proposed UI labels are a design application, not a claim about current product behavior. Future validation should run the named cases on a pinned build, inspect a real UI call path, and ask learners whether they can distinguish entered, canonical, parsed, and projected values. Human subject review, learner testing, localization, and publication remain pending.
