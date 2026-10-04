---
module_id: cs-003-chord-parser-uncertainty
department: computer-science
course: Return Uncertainty at the Chord-Parser Boundary
level: intermediate
prerequisites: ["basic chord symbols", "result types"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-003
version: "0.1.0"
---

# Return Uncertainty at the Chord-Parser Boundary

> **Department of Computer Science** | Intermediate | 45 minutes | Draft: runtime and subject review pending

## Objectives

You will trace a musician's input from GA's chord parser to a fretboard response; distinguish a recognized chord from a partially interpreted one; model unknown notation as an explicit result; and write a regression corpus that checks musical meaning, not merely whether a `Chord` object exists.

## 1. The user's problem: a plausible wrong answer

A guitarist asks GA for voicings of `C7b5`. A response labelled `C7b5` is useful only if the internal formula preserves both the dominant seventh and the lowered fifth. Returning attractive diagrams for some other pitch-class set is worse than saying the notation is unsupported: the error looks credible and may enter practice or teaching material.

The inspected GA checkout has several chord parsers. This lesson follows the one actually used by `VoicingFilterService`: `Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs`. Its root regex captures a note followed by **any** suffix (lines 11–12). `ParseChordSuffix` matches familiar forms exactly, then `ParseComplexSuffix` checks whether the suffix *contains* an alteration (lines 103–133). If nothing matches, it returns a major formula (lines 138–139). `TryParse` catches every exception and reports only `true` or `false` (lines 42–53). None of these choices tells the caller that part of the input was ignored.

The user path matters. `VoicingFilterService.cs:28` calls this `TryParse`. If it succeeds, the service builds voicings from `chord.PitchClassSet`. `ContextualChordsController.cs:56–63` returns `200 OK` for the result and a generic `400` for an argument error. Thus a wrong but successfully constructed chord can pass through the endpoint. This is a source trace, not a claim that a live endpoint was exercised.

### Practice exercise 1

What should the endpoint do with `Cnope`? Trace root, suffix, formula, service, and response under the current code; then state the desired behavior.

> **Answer:** The root is C; `nope` is not an exact suffix and contains no recognized alteration, so the parser falls back to a major formula. `TryParse` succeeds, and the service can return C-major voicings under the original text with `200 OK`. Desired: a typed unsupported-suffix result, mapped to a user-facing invalid or unsupported response. Do not guess that `nope` means major.

## 2. Check the meaning, not the parse count

The [CS-003 corpus](../../../fixtures/computer-science/cs-003/README.md) has eight inputs. `C`, `Am`, and `G7` are supported controls; `Hmaj7` tests an invalid root. The remaining four expose different failure modes:

| Input | Source-traced current interpretation | Required contract |
|---|---|---|
| `Cnope` | unknown suffix becomes major | reject unknown suffix |
| `Galtxyz` | substring `alt` wins despite trailing `xyz` | consume all input or reject |
| `C7b5` | `b5` branch builds a flat-fifth formula from semitones 4 and 6; the seventh is lost | preserve both alterations or reject |
| `C/E` | unknown suffix becomes major; original symbol survives, but `Chord.Bass` is `Notes[0]`, the root | represent E bass or reject |

The existing `ChordSymbolParserTests.cs` checks that accepted cases produce a non-null root and symbol. It even lists `C/E` as valid, but does not assert its bass. That is a useful test of *construction* but not of interpretation. A regression must assert the resulting pitch classes, quality, extension, and bass that the feature promises. For an unsupported form, it must assert a rejection with a reason.

GA also has `Chord.TryFromSymbol` in `Common/GA.Domain.Core/Theory/Harmony/Chord.cs`. Its unknown-suffix path returns `false` (lines 161–166), but it accepts a narrower set of exact suffixes. Replacing the service parser with it without a compatibility corpus could reject currently supported notation. The lesson is to define the contract and measure compatibility before selecting a single parser.

### Practice exercise 2

Why does a passing `Parse_ReturnsValidChord_On_ValidSymbols` test for `C7b5` fail to protect the guitarist? Name two additional assertions.

> **Answer:** The test only asserts an object, root, and symbol. Assert a dominant seventh pitch class and a lowered fifth in the formula or pitch-class set; also assert that no unconsumed suffix remains. A formatted symbol alone does not prove the intervals.

### Practice exercise 3

`C/E` is syntactically familiar but the current consumer cannot represent its bass. Is it an invalid input?

> **Answer:** The text is not intrinsically invalid. It is **unsupported semantics in this path**. Either implement an explicit slash-bass representation and test E as bass, or return a specific unsupported-result. Calling it C major while retaining `C/E` loses the user's intent.

## 3. Compose a boundary that can say “I do not know”

Start from the consumer's needed meaning, not a permissive regex. One possible design is:

```text
tokenize(input)                      -> Result<Tokens, SyntaxError>
consumeAll(tokens)                   -> Result<ChordSyntax, TrailingInput>
interpret(ChordSyntax, vocabulary)   -> Result<ChordMeaning, UnsupportedForm>
construct(ChordMeaning)              -> Result<Chord, DomainError>
mapForUser(error)                    -> documented client response
```

The first four operations can be pure when the vocabulary is an explicit input. The endpoint and logging are effects. Preserve the original input and normalized form for diagnosis, but never put the original label on a different formula. `UnsupportedForm` is distinct from a malformed root: it tells the user that the music notation might be valid even though this GA path does not implement it. The decision to expose a new HTTP status or response shape is a public API choice requiring compatibility review; this course does not make it.

### Practice exercise 4

An agent proposes “fixing” `C7b5` by changing only the parser's `b5` branch. What must its test prove before the change is accepted?

> **Answer:** The test must assert the intended intervals, including the dominant seventh and flat fifth, and show that `C`, `Am`, `G7`, and other already supported forms retain their meanings. It must reject a trailing token such as `Galtxyz`. The service-to-response path must then be checked so an unsupported form cannot return plausible voicings.

## 4. Dogfood the error path

Run the corpus first as a test against a pinned GA revision. Ask a guitarist to enter one supported chord, one typo, and one valid but unsupported slash chord in the actual voicing UI. Record the exact text shown, whether a correction was obvious, and whether a wrong diagram looked trustworthy. A code test can prove the parser contract; only product use reveals whether the message helps a player recover. Compare the old and proposed behavior using the same inputs and record any notation that a stricter parser unexpectedly rejects.

The acceptance rule is set before editing: no unknown suffix can produce a successful chord; no supported input may silently change pitch classes; and a user can distinguish a typo from unsupported notation. A failing test or confusing error is evidence to revise the design, not a reason to let the agent invent a chord. Keep the fixture's source-traced predictions separate from runtime observations until the test is executed.

### Practice exercise 5

A stricter parser rejects `C/E` and eliminates a wrong C-major diagram, but musicians still cannot request slash chords. Is the task finished?

> **Answer:** The safety defect is contained, but the product need remains. Record the rejection as a partial improvement, keep the missing slash-chord capability in the backlog, and test whether the displayed message guides the guitarist. Claim complete support only after E-bass semantics and a user-visible path are implemented and verified.

## Evidence and limits

The code paths, tests, and [corpus](../../../fixtures/computer-science/cs-003/chord-symbol-corpus.json) were inspected in a local GA checkout on 2026-10-04. The examples above are source-traced predictions. An executable regression, a pinned GA commit, actual endpoint responses, and musician feedback are still required before this lesson can be published as a verified behavior report.
