---
module_id: phi-003-what-does-the-same-chord-mean
department: philosophy
course: What Does the Same Chord Mean in GA Search?
level: early-intermediate
prerequisites: [phi-001-how-to-argue-well]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: philosophy-2026-10-12-003
version: "0.1.0"
---

# What Does “the Same Chord” Mean in GA Search?

> **Department of Philosophy** | Early intermediate | 40 minutes | English draft; subject and learner review pending

## Objectives and project question

You will distinguish three meanings of sameness for guitar chords, calculate a small pitch-class and interval-class example, and choose evidence for a search claim. **Project question:** when GA tells a guitarist that two voicings are “the same” or “similar,” which musical relation did it actually test? Without an explicit relation, a correct algorithm can still answer the wrong musical question.

[PHI-001](phi-001-how-to-argue-well.md) separates a conclusion from its supporting premises. [PHI-002](phi-002-when-is-an-advisory-decision-justified.md) separates a valid decision record from warranted action. Here we apply that discipline to a product word. “Same” is a conclusion; MIDI notes, pitch classes, interval classes, and a search score are different possible premises. The relevant GA [domain schema](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/architecture/DOMAIN_SCHEMA.md) distinguishes a literal `PitchClassSet`, an `IntervalClassVector` (ICV), and a set class related by transposition or inversion. We must name which relation a guitarist is asking for before choosing a retrieval method.

## 1. Four lenses on one chord comparison

A MIDI note number includes register: C3 is 48 and C4 is 60. A **pitch class** takes the note number modulo 12, so both map to C (`0`). An unordered pitch-class set forgets octave, doubling, and note order. An ICV counts the unordered interval classes between distinct pitch classes; it forgets even more. The [GA schema at `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs) places literal 12-bin pitch-class chroma, cardinality, and a six-bin ICV inside `STRUCTURE`, then carries the declared root pitch class in a separate `ROOT` partition. The schema explicitly cautions that **the whole `STRUCTURE` partition is not transposition-invariant**. Its ICV/cardinality sub-dimensions have a different invariance from its chroma.

| Question a guitarist might mean | Operational relation | What it forgets |
|---|---|---|
| “Are these the identical played notes?” | Same MIDI-note multiset | Performance timing and timbre, but not octave |
| “Are these the same pitch classes in another position?” | Same pitch-class set | Octave, doublings, order, and register |
| “Is this a transposed or inverted version?” | An explicit transposition or inversion maps one set to the other | Absolute pitch-class location |
| “Do they have the same interval content?” | Same six-component ICV | Absolute pitch classes, root, and possibly distinctions between different set classes |

These relations answer different questions. Equal pitch-class sets have equal ICVs, but the converse need not hold. An ICV match should not silently become “the same chord name” or “the same physical shape.” A similarity threshold is weaker still: it may rank candidates but does not by itself define a mathematical equivalence class.

The pinned [teaching fixture at Demerzel `50c0d2f`](https://github.com/GuitarAlchemist/Demerzel/tree/50c0d2f5eb6684499c3bcf95d77f0481af2cc136/state/streeling/fixtures/philosophy/phi-003) supplies five short MIDI-note lists and explicit root labels. Its dependency-free script computes pitch-class sets, six interval-class counts, a **toy binary-chroma cosine**, and whether an exact transposition or inversion exists. Run `python state/streeling/fixtures/philosophy/phi-003/compare_voicings.py` from the Demerzel root. The fixture is not a GA embedding, live search trace, or test of fingering comfort.

### Practice Exercise 1

The fixture compares `c_major_low = [48,52,55]` with `c_major_high = [60,64,67]`. Are the MIDI-note multisets equal? Are the pitch-class sets and ICVs equal? What remains unproven about two guitar fingerings?

> **Answer:** The MIDI-note multisets differ by an octave. Both map to pitch-class set `{0,4,7}` and therefore share the ICV `[0,0,1,1,1,0]`; their toy binary chroma cosine is `1`. The fixture says nothing about string choice, hand stretch, timbre, playability, or whether GA's *whole* 240-dimensional embeddings and rankings are equal.

## 2. A transposition is not literal pitch-class identity

`c_major_low` has pitch classes `{0,4,7}`. Moving each class two semitones yields `d_major = {2,6,9}`. The fixture confirms an exact `+2` transposition and the same ICV `[0,0,1,1,1,0]`. Its binary-chroma sets do not overlap, so their **toy chroma-only cosine is zero**. That zero is not the cosine of GA's full `STRUCTURE` partition. GA's [TheoryVectorService](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/Services/TheoryVectorService.cs) combines chroma with ICV, cardinality, and other values; its own comment reports a nonzero major-triad `STRUCTURE` cosine under transposition. The pinned [invariance export tool](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tools/GaStructureInvariance/Program.cs) exists specifically to test that partition on set classes and all 12 transpositions.

The distinction affects an actual user workflow. “Show this chord in another register” suggests retaining pitch classes while looking at fingering and register. “Play this shape in D” calls for transposition. “Find harmonically related material” may call for an ICV-based search. GA's pinned [IcvNeighborsSkill](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs) uses ICV distance for nearby pitch-class sets; that is a different operation from promising that the entire OPTIC-K embedding is transposition-invariant. A product label should expose enough of the relation for a guitarist to judge the result.

### Practice Exercise 2

For `c_major_low` and `d_major`, name one relation that holds and two that do not. Why would the fixture's chroma cosine of zero be the wrong numeric answer to “What is GA's full STRUCTURE cosine?”

> **Answer:** Exact transposition and ICV equality hold. Literal MIDI-note multiset equality and pitch-class-set equality do not. The fixture computes cosine only over equal-weight binary chroma bits, while GA's `STRUCTURE` contains additional ICV, cardinality, and tonal components. A zero in this toy projection cannot be substituted for GA's full partition or final weighted search score.

## 3. Even root plus interval content can be insufficient

Compare `c_major_low = {0,4,7}` with `c_minor = {0,3,7}`. Both have declared root C (`0`) and ICV `[0,0,1,1,1,0]`; the fixture finds that inversion plus transposition relates their pitch-class sets. Yet the sets differ, and their toy chroma cosine is `2/3` because only C and G overlap. The declared root and ICV together do not identify whether the third is E or E-flat. A root label in the fixture is **supplied input**, not a root inferred by the script. That matters when a chord has several plausible interpretations.

For `c_diminished = {0,3,6}`, the ICV is `[0,0,2,0,0,1]`; it differs from the major triad despite the shared C root. These small comparisons make a useful counterexample to the claim “one representation captures every notion of sameness.” They do not imply that the full GA system confuses these chords. GA's embedding contains more than the two fields examined here, and a real retrieval claim needs a query, index revision, scoring path, and observed ranked output.

### Practice Exercise 3

Someone proposes a key `(root_pc, ICV)` as a unique chord identifier. Use `c_major_low` and `c_minor` to test it. What additional field in GA's `STRUCTURE` helps distinguish the examples?

> **Answer:** Both examples have supplied root `0` and the same six-component ICV, so the proposed key collides even though `{0,4,7} != {0,3,7}`. Literal pitch-class chroma distinguishes the E from E-flat. This counterexample rejects uniqueness of that two-field key; it does not measure the reliability of GA's complete vector.

## 4. Decide what a similarity claim may say

Equality of exact pitch-class sets is reflexive, symmetric, and transitive. A thresholded similarity can fail transitivity: a synthetic score table might have `sim(A,B)=0.8`, `sim(B,C)=0.8`, and `sim(A,C)=0.5`. At threshold `0.75`, A is “similar” to B and B to C, while A is not “similar” to C. Calling these threshold-connected items “the same” would create a misleading equivalence class. A practical search UI can rank by score, but it should state the score's scope and avoid a universal identity claim.

A small **advisory** design candidate is to ask which comparison the user wants: exact pitch-class set, explicit transposition, ICV neighborhood, or voicing ranking. The strongest counterargument is extra interface complexity: many guitarists simply want a playable alternative and do not want four technical controls. A simpler alternative is one ordinary search with a clear explanation on each result, such as “same pitch classes; different register” or “same interval content after transposition.” The criterion for rejecting the extra control is a learner test where it adds friction without improving task success or reducing mistaken choices. No such user test has been run here.

### Practice Exercise 4

At a synthetic threshold `0.75`, the similarities are A–B `0.8`, B–C `0.8`, and A–C `0.5`. Can “score at least 0.75” be an equivalence relation? Name the violated property.

> **Answer:** No. A is related to B and B to C, but A is not related to C, so transitivity fails. A ranking or neighborhood can still be useful; it must not be described as a mathematical class of identical chords on this rule alone.

### Practice Exercise 5

A guitarist asks “show the same notes higher on the neck,” then asks “transpose this to D.” Which relation should a prototype test for each request, and what observation would falsify a claim that one generic search handles both well?

> **Answer:** For the first request, retain the pitch-class set and evaluate playable octave/register alternatives; for the second, apply an explicit transposition to the target key and verify the resulting classes. A controlled learner task in which users repeatedly choose results with the wrong pitch classes, key, or fingering purpose would falsify a claim that the generic result label is sufficient. Test against actual GA queries and ranked outputs before claiming product behavior; the fixture alone cannot establish it.

## Sources, limits, and next check

The source-bound implementation references are GA [EmbeddingSchema](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs), [TheoryVectorService](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/Services/TheoryVectorService.cs), [invariance export tool](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tools/GaStructureInvariance/Program.cs), [ICV neighbor skill](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs), and [domain schema](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/architecture/DOMAIN_SCHEMA.md), all at `dc2e74cbd992a298f67efb928b5b3754615e1924`. The [deterministic teaching fixture](https://github.com/GuitarAlchemist/Demerzel/tree/50c0d2f5eb6684499c3bcf95d77f0481af2cc136/state/streeling/fixtures/philosophy/phi-003) computes only the stated simple relations. It does not instantiate the GA vector service, query a current OPTIC-K index, test physical fingering, or interview a guitarist. Human subject review, a blinded learner attempt, localization, and public readback remain pending.
