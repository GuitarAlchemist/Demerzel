---
module_id: mus-022-grothendieck-deltas-icv-distance
department: music
course: Grothendieck Deltas — What Interval-Content Distance Measures
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Grothendieck Deltas — What Interval-Content Distance Measures, and What It Cannot

> **Department of Music** | Stage: Citrinitas (Intermediate to Advanced) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Treat interval-class vectors as elements of a commutative monoid, and build the group in which they can be subtracted
- Compute the delta and the L1 distance between two sets, and bound the distance from the sizes of the sets alone
- Prove which sets lie at distance 0, and why sets of one size lie an even distance apart
- Say what the distance cannot see: voice leading, major against minor, keys, the notes a chord contains, and the Z-relation
- Trace what GA computes for each of these, and where a heuristic, a comment or a test says something else

---

## 1. Interval Content as a Count

A guitarist asks for "a chord close to this one". One answer compares interval content. The interval-class vector of MUS-020 §2 counts, for each interval class from 1 to 6, the pairs of notes the set holds at that distance. C major has <001110>: one minor third, one major third and one fifth.

A vector is a list of six natural numbers, an element of N^6, and two such lists add component by component. With <000000> as identity, N^6 is a **commutative monoid**: its addition is associative and commutative and has an identity. No element but <000000> has an inverse: no list of natural numbers added to <001110> gives <000000>.

The sum of two vectors counts pairs; it does not combine chords. Add B to C E G. The new set, Cmaj7, keeps the three pairs of C major and gains the three pairs between B and C, E and G, at 11, 7 and 4 semitones: interval classes 1, 5 and 4. So ICV(Cmaj7) = <001110> + <100110> = <101220>. In general, when two sets A and B share no note, ICV(A ∪ B) = ICV(A) + ICV(B) + X(A, B), where X(A, B) counts the pairs made of one note from each set, class by class: the interval function of Lewin (1987), folded into interval classes. The single note B has the vector <000000>; everything it adds comes from X.

Not every list is the vector of a set. The six counts of an n-note set add up to n(n − 1)/2, its number of pairs. The 4,096 sets have 200 distinct vectors: <000000> for the empty set and the single notes, then 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 and 1 vectors for the sizes 2 to 12. That is the 224 set classes of MUS-020 §4, minus 23 because each Z-related pair shares a vector, minus 1 because the empty set and a single note share <000000>.

### Practice Exercise

Find the vector of C7, C E G B♭, from that of C major.

> *Solution:* B♭ lies 10, 6 and 3 semitones above C, E and G: interval classes 2, 6 and 3. So X = <011001>, and <001110> + <011001> = <012111>, the vector MUS-020 §2 gives for C7.

---

## 2. Subtracting Counts: the Grothendieck Group

To compare two sets, we want a difference: how many more pairs of each class the second set holds than the first. N^6 has no negative elements, so we enlarge it to the smallest group in which any two of its elements can be subtracted.

The **Grothendieck construction** does this for any commutative monoid M. Take pairs (a, b) of elements of M, to be read as "a − b". Call (a, b) and (c, d) equivalent when a + d + k = b + c + k for some k in M. The classes form an abelian group K(M): (a, b) + (c, d) = (a + c, b + d), the identity is the class of (0, 0), and the inverse of (a, b) is the class of (b, a). The map a ↦ (a, 0) sends M into K(M), and every homomorphism from M to a group extends to K(M) in exactly one way: that is the sense of "smallest". When M is **cancellative**, that is, when a + k = b + k implies a = b, the k can be dropped and the map is one-to-one. N^6 is cancellative, and K(N^6) is Z^6: the class of (a, b) is the list of integers a − b.

The **Grothendieck delta** from a set A to a set B is δ(A, B) = ICV(B) − ICV(A), an element of Z^6. From C major to Cmaj7 it is <+1, 0, 0, +1, +1, 0>: one more semitone, one more major third and one more fifth. Three laws make it a difference, and they hold because subtraction in a group obeys them:
- δ(A, A) = 0;
- δ(B, A) = −δ(A, B);
- δ(A, B) + δ(B, C) = δ(A, C).

The delta depends on the two vectors only, not on the notes. Going from C major to Fmaj7, F A C E, keeps C and E, drops G and adds F and A, yet gives the same delta as going to Cmaj7, because Fmaj7 and Cmaj7 share the vector <101220>.

The **L1 norm** of a delta adds the absolute values of its six components, and the **distance** d(A, B) is the L1 norm of δ(A, B). On vectors, this is a metric. On sets, it is only a pseudometric: d(A, B) = 0 does not force A = B (§3).

### Practice Exercise

Give the vectors of a major triad and of a minor triad, and their distance.

> *Solution:* Both are <001110>. A minor triad is an inversion of a major triad, and an inversion keeps every interval class (MUS-020 §2). The delta is 0, and so is the distance. GA reports 1 (§5).

---

## 3. What the Distance Measures

Write T(n) = n(n − 1)/2 for the number of pairs in an n-note set. The six components of δ(A, B) add up to T(|B|) − T(|A|).

**Theorem 1 (size bound and parity).** d(A, B) ≥ |T(|B|) − T(|A|)|, and d(A, B) − (T(|B|) − T(|A|)) is even.

*Proof.* The sum of the absolute values of the components is at least the absolute value of their sum. And for every integer x, |x| − x is 0 or 2|x|, an even number, so the norm and the sum differ by an even number. ∎

Three consequences follow:
- Two sets of one size lie an even distance apart, so two sets of one size with different vectors lie at least 2 apart.
- A triad and a four-note set lie at least T(4) − T(3) = 3 apart.
- A distance of exactly 1 needs T(|B|) − T(|A|) = ±1, which happens only between a set of two notes and a set of at most one note. From a set of three notes or more, every set lies at distance 0 or at least 2.

**Theorem 2 (one added note).** If A has n notes and x is not one of them, adding x adds the n pairs between x and the notes of A and changes no other pair. So δ(A, A ∪ {x}) has non-negative components that add up to n, and d(A, A ∪ {x}) = n, whichever note is added.

So Cmaj7, C7, C6 and Cadd9 all lie at distance 3 from C major, the smallest distance a four-note set can have from a triad. Of the 29 tetrachord classes, 13 lie at distance 3 from C major. Four of them contain no major or minor triad: (0125), (0135), (0145) and (0146).

**Theorem 3 (distance zero).** d(A, B) = 0 exactly when A and B have the same vector. Since T(0) = T(1) = 0 and T increases from n = 1 on, two sets of different sizes share a vector only when one is empty and the other is a single note. Two sets of one size share a vector exactly when they lie in the same set class or in two Z-related classes (MUS-020 §5). So every transposition and every inversion of a set lies at distance 0 from it, and so does every member of its Z partner.

The distance counts how many pairs of each interval class appear or disappear, and nothing else. Theorem 2 says what one added note costs; Theorem 3 says what costs nothing.

### Practice Exercise

Which distances occur between two distinct trichord classes?

> *Solution:* Two trichords both have 3 pairs, so by Theorem 1 their distance is even, and it is not 0, because no two trichord classes are Z-related. The values that occur are 2, 4 and 6: (037) lies at 2 from (025), at 4 from (048) and at 6 from (012).

---

## 4. What It Cannot See

Each limit below follows from §3: the distance is a function of two vectors, so an operation that keeps the vector is invisible to it.

**Voice leading.** Move one note of C E G by a semitone, up or down. The six results are E G B (E minor) and C E♭ G (C minor) at distance 0, and C♯ E G (C♯ diminished), C F G (Csus4), C E F♯ and C E G♯ (C augmented) at distance 4. The three trichord classes closest to C major in interval content, at distance 2, are (014), (015) and (025), and none of them is one semitone away: their nearest members, such as E♭ E G, C E F and D E G, need three, two and two semitones of motion, adding up how far each voice moves. A distance on vectors cannot rank chords by how far the hand moves. MAT-022 §6 shows IX's path search failing, for this reason, to join the augmented triad and C major, and GA's search fails in the same way (§5).

**Major and minor, keys and modes.** C major and C minor lie at distance 0, since an inversion keeps the vector. So do all twelve major scales, C major and F♯ major included: a transposition keeps the vector, so a distance on vectors cannot count accidentals. A mode of a scale is the same set of pitch classes, and C natural minor holds the notes of E♭ major, so both lie at distance 0 from every major scale.

**The notes a chord contains.** 4-Z15, C C♯ E F♯, and 4-Z29, C C♯ E♭ G, both lie at distance 3 from C major, with the same delta <+1, +1, 0, 0, 0, +1>. 4-Z29 contains a minor triad, C E♭ G; 4-Z15 contains no major or minor triad at all. Distance 3 from C major does not mean "C major plus one note": three other tetrachord classes lie at distance 3 with no major or minor triad, as 4-Z15 does (§3).

**The Z-relation.** Those two sets share the vector <111111> and lie at distance 0 from each other, although no transposition or inversion maps one onto the other.

### Practice Exercise

A user asks for "a four-note chord close to C major" and receives the tetrachord classes at distance 3, the closest any four-note set can be. Which of them contain a major or minor triad?

> *Solution:* 9 of the 13. (0125), (0135), (0145) and (0146) contain none. The distance ranks all 13 alike.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), GA's `main` on 2026-10-06; this lesson documents that code and does not change it, and it has not run GA or its tests. Learn's ga-ai course ran some of the same code, compiled at two earlier GA commits where the code concerned is the same as at `40d3374`, and its outputs are quoted where they apply. The other numbers come from a line-by-line Python transcription of the GA code named.

**The delta.** [`GrothendieckDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L8-L11) is "a signed delta in the Grothendieck group", with an addition and a negation that obey the group laws ([lines 139-167](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L139-L167)). [`FromIcVs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L113) subtracts the two vectors component by component, then:

```csharp
        // Heuristic: When two distinct sets share the same ICV (e.g., diatonic modes/keys),
        // L1 difference is zero. To preserve musical differentiation expected by callers/tests,
        // emit a minimal non-zero delta focused on ic1. This keeps related keys close but not identical.
        if (delta.L1Norm == 0)
        {
            delta = delta with { Ic1 = 1 };
        }
```

The comment speaks of "two distinct sets", but the method only sees two vectors, so it also gives <+1, 0, 0, 0, 0, 0> for a set compared with itself: for all 200 vectors, by the transcription. The map therefore breaks the three laws of §2. δ(A, A) is not 0. From C minor back to C major, it gives <+1, 0, 0, 0, 0, 0> again, not the negative of the forward delta. And C major → C minor → C major adds up to <+2, 0, 0, 0, 0, 0>. Between two different vectors, the transcription finds it equal to the true delta. The +1 lands on interval class 1, where no pair of notes changed, and [`Explain`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L172) reads it as "+1 ic1 (semitone)" and, since [a gain in ic1 or ic2](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L229-L232) is tested first, as "more chromatic color". GA issue [#776](https://github.com/GuitarAlchemist/ga/issues/776) reports the heuristic and asks for `ComputeDelta(v, v).L1Norm` to be 0. Learn's [ga-ai lesson 14](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/14-what-the-substitution-skill-answers.md) printed `ComputeDelta(...).L1Norm = 1` for C against C, against Am and against F♯, and for G7 against D♭7 ([output](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l14.txt#L64-L67)), compiling GA at `a826864`, where `GrothendieckDelta.cs` is the same as at `40d3374`.

GA has a second delta. [`IcvDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.DSL/Generators/OptickGrothendieck.fs#L77-L93), in the DSL's `OptickGrothendieck.fs`, represents "elements of the Grothendieck group Z^6" and subtracts with no heuristic, so GA's two deltas disagree exactly on equal vectors. Its test, [`Grothendieck_IcvDelta_IsAbelianGroupAndCancellative`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L143-L155), checks the identity and the inverse on one delta; it checks neither commutativity, nor associativity, nor cancellation, and it does not touch `GrothendieckDelta`.

**The tests' scales.** GA's tests write sets as strings of digits, read one character at a time ([`PitchClassSet.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L728-L748)), through [`PitchClass.TryParseSetNotation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L275-L294), which reads A and B as 10 and 11 and passes everything else to [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L244-L267): digits, T for 10, E for 11, and note names, which these strings do not use. [`ShouldComputeDelta_FromCMajorToGMajor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L73-L90) parses G major as ["02479E1"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L77), with the comment "G A B C D E F#", and `OptickGrothendieckTests` [repeats it](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L27). The digits give C C♯ D E G A B: a 1 where G major needs a 6. That set has the vector <354351>, not the diatonic <254361>, and its true delta from C major is <+1, 0, 0, 0, −1, 0>, at distance 2. The "C minor" of [`ShouldComputeDelta_FromCMajorToCMinor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L62-L70), "0235789", is C D E♭ F G A♭ A, with the vector <344352>, at distance 4; C natural minor would be "023578T". By the transcription:
- `FromCMajorToCMinor` asserts an L1 above 0 and an explanation containing "ic", and [`ShouldComputeDelta_WithExplanation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L93-L108), on the same "02479E1" as `FromCMajorToGMajor`, asserts that the explanation contains "ic1". Both pass on the true delta. With C natural minor in the first test, the mode its comment ("Moves between modes") points to, and the real G major in the second, both true deltas would be 0, and both tests would pass only through the heuristic: without it, `Explain` would return "No change". #776 reads the first test as a comparison of C major with C natural minor, which share a vector, and concludes that it passes "only because of the rule above". At `40d3374`, as at the commit #776 cites, the test's set is not C natural minor, and the test passes on the true delta of 4.
- `FromCMajorToGMajor` asserts an L1 below 5: 2 for the set it uses; 1, through the heuristic, for the real G major.
- [`ShouldFindShortestPath_BetweenRelatedKeys`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L267-L279) checks only the two ends of the path, which has one step whether the target is "02479E1" or the real G major.
- The `IcvDelta` test above runs on the same "G major": its delta is non-zero only because of the wrong digit.

**Neighbourhoods and paths.** The cost is the L1 norm times 0.6 ([lines 39-42](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L39-L42)), which [`ShouldComputeHarmonicCost_AsL1Norm`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L115) checks at 5.4 for a norm of 9. [`FindNearby`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L45) scans all 4,096 sets, [puts the source first, at cost 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L58-L62), [skips the source by value](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L72-L77) and keeps every set whose heuristic delta lies within the radius, sorted by cost. Every other set with the source's vector comes back at 1, never at 0. By the transcription, from C major (the triad), radius 0 returns C alone; radius 1 returns C and the other 23 major and minor triads, and nothing else; radius 2 adds 108 dyads and trichords at true distance 2, 132 sets in all. From the C major scale, radius 1 returns its 12 transpositions, itself included, and radius 2 returns 36 sets.

[`FindShortestPath`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L118) searches breadth first through `FindNearby(current, 2)`, among sets of the current size ([lines 148-151](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L148-L151)). Its comment says that radius 2 ["connects closely related diatonic collections (e.g., C major → G major)"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L146-L147), which "typically differ by one accidental yet may exceed radius=1". By §4, any two major scales lie at distance 0, and at 1 through the heuristic: the metric does not see the accidental, and every key lies one step from every other. The transcription goes from C major to F♯ major in one step, as from C major to G major; from C to C minor and from C to F♯, the triads, in one step each; and finds no path from C major to C E G♯, since no other trichord class lies within 2 of (048). MAT-022 §6 finds the same gap in IX, and GA issue [#802](https://github.com/GuitarAlchemist/ga/issues/802) reports it, with the one-step triad paths, in the chatbot's `IcvShortestPathSkill`.

**The chatbot's two skills.** Learn's [ga-ai lesson 23](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/23-harmonic-distance-and-path.md) called [`GrothendieckDeltaSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L97-L131) directly, compiling GA's `main` at `f4f5b4a`, where the skill, the delta and the service are the same as at `40d3374`. Five of the skill's ten [example prompts](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L46-L58) name two chords of one set class. The skill declines one of them, "how different are C major and F major harmonically", because "major" stands between the first chord and "and", as lesson 23 notes. It answers the other four: C to G, Am and Em, Cmaj7 and Fmaj7, C to F. For each, in both directions, the run printed the delta [+1, 0, 0, 0, 0, 0], L1 1, cost 0.60, then "+1 ic1 (semitone)" and "more chromatic color" ([output, lines 58-63](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L58-L63) and [66-67](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L66-L67)). The skill then [explains](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L123-L128) that each component "says how many more occurrences of that interval-class the target has than the source": G major would hold one more semitone than C major, while both hold none. #802 reports this, and the garbled arrow `Explain` prints between the two parts. Learn's [ga-ai lesson 22](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/22-similar-chords.md) ran [`IcvNeighborsSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L120-L140), which recomputes the true delta because of the heuristic ([its comment](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L122-L129)). By Theorem 1, every set at distance 1 or 2 from a triad lies at 2, so the skill keeps the first eight in `FindNearby`'s order, which is the order of the sets' bitmasks. For C: {0,3}, {0,4}, {1,4}, {0,1,4}, {0,3,4}, {0,5}, {1,5} and {0,1,5}, five set classes, announced as the ["top 8 by harmonic cost"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L146) ([output](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l22-main.txt#L90-L98)). GA issue [#798](https://github.com/GuitarAlchemist/ga/issues/798) reports it. The skill's filter [drops distance 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L136) as "exact ICV-identical (same set class)", which would also drop a Z partner; none of the chords the skill builds has one.

**The MCP tool.** GaMcpServer's [`GaIcvNeighbors`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L325) gets the distance right. It [recomputes the true L1](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L337-L348), and its comment names the heuristic; it skips the chord's own set class and lists each class once. By the transcription, `GaIcvNeighbors("C", 2)` lists (03), (04), (014), (05), (015) and (025), all at Δ=2. [Its two tests](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L72-L94) check that the distance-1 answer for C does not name Forte 3-11, and that at distance 2 every line is at Δ=2, no line repeats or names Forte 3-11, and Forte 3-7 appears. With the default distance 1, it lists nothing for C. By Theorem 1, for a set of three notes or more, distance 1 can only add a Z partner at distance 0, as the tool's [description](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L327-L328) says: "distance 0 is a Z-related set".

GA issues #776, #798 and #802 cover the heuristic and the two skills. As this lesson is written, no GA issue covers the tests' scales, the path comment or the `IcvDelta` test. Fixing any of these is for GA's owners; this lesson only describes them.

### Practice Exercise

Would `ShouldComputeDelta_WithExplanation` pass with the real G major scale, "024679E", if `FromIcVs` returned the true delta?

> *Solution:* No. The real G major scale is a transposition of C major, so the true delta is 0, and `Explain` returns "No change", which does not contain "ic1". With the heuristic, it passes on <+1, 0, 0, 0, 0, 0>. With the set the test uses, it passes either way, on <+1, 0, 0, 0, −1, 0>.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `40d3374`. Nothing in it is a measurement. The predictions come from §3 and from the transcription of §5, and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types in the lab's own process, never a running MCP server or a language model. The chatbot's skills are left out, since Learn's ga-ai lessons 22 and 23 already ran them.

1. **Deltas.** Call `GrothendieckService.ComputeDelta` and `IcvDelta.Between` on the vectors of C major and C minor ("047", "037"), C major and D major ("047", "269"), 4-Z15 and 4-Z29 ("0146", "0137"), the C major scale and the real G major scale ("024579E", "024679E"), and the C major scale and "02479E1". Prediction: for the first four pairs, `IcvDelta` is zero and `ComputeDelta` is <+1, 0, 0, 0, 0, 0>; for the last, both give +1 at interval class 1 and −1 at interval class 5.
2. **The laws.** Over the 200 distinct vectors of the 4,096 sets, test the three laws of §2 on `ComputeDelta` and on `IcvDelta`. Prediction: `IcvDelta` keeps every law on every pair and triple. `ComputeDelta(v, v)` is <+1, 0, 0, 0, 0, 0> for all 200 vectors; antisymmetry fails on the 200 equal pairs only; additivity fails on the 119,600 triples whose three vectors are not all different, and only there.
3. **Neighbourhoods.** Count what `FindNearby` returns from C major ("047") at radius 0, 1 and 2, and from the C major scale at radius 1 and 2. Prediction: 1, 24 and 132; 12 and 36.
4. **Paths.** Call `FindShortestPath` from the C major scale to F♯ major ("13568TE") and to the real G major, and from the C major triad ("047") to the C minor triad ("037") and to C E G♯ ("048"). Prediction: two sets each for the first three; an empty path for the last.
5. **The tests' scales.** Print the members and vectors of "02479E1" and "0235789". Prediction: {0, 1, 2, 4, 7, 9, 11} with <354351>, and {0, 2, 3, 5, 7, 8, 9} with <344352>.
6. **The MCP tool.** Call `GaClosureBootstrap.init()`, as GA's tests do, then `GaIcvNeighbors("C", 1)` and `GaIcvNeighbors("C", 2)`. Prediction: the message "No other set class within distance 1 of C", then six classes at Δ=2, among them Forte 3-7.

### Practice Exercise

Where does the 119,600 of step 2 come from?

> *Solution:* The heuristic fires only on equal vectors. When a, b and c are all different, each leg is a true difference and the law holds. When a = b ≠ c, the left side carries the +1 of the first leg; when b = c ≠ a, that of the second. When a = c ≠ b, the left side is 0 and the right side <+1, 0, 0, 0, 0, 0>. When a = b = c, the left side is <+2, 0, 0, 0, 0, 0> and the right side <+1, 0, 0, 0, 0, 0>. So the law fails exactly on the 200³ − 200 × 199 × 198 = 8,000,000 − 7,880,400 = 119,600 triples that are not all different.

---

## 7. Common Pitfalls

- **Reading distance 0 as "the same chord".** It means the same vector: a transposition, an inversion or a Z partner.
- **Reading a small distance as a small move.** Moving one note of C major by a semitone gives distance 0 or 4; the trichord classes at distance 2 need two or three semitones of motion.
- **Expecting the distance to count accidentals.** Every major key lies at distance 0 from every other.
- **Reading a delta as a recipe.** A delta says how many pairs of each class appear or disappear, not which notes change: C major to Cmaj7 and C major to Fmaj7 have one delta.
- **Patching a zero.** Replacing a zero delta with a "minimal non-zero" one breaks δ(A, A) = 0, antisymmetry and additivity, and reports a change in an interval class where no pair changed.
- **Trusting a test's comment.** A test checks the set its code builds, not the one its comment names: "02479E1" is not G major.
- **Comparing sets of different sizes.** The size bound holds whatever the notes: a triad and a four-note chord are never closer than 3.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Commutative monoid** | A set with an associative, commutative addition and an identity, such as N^6 under addition component by component |
| **Cancellative** | Having a + k = b + k only when a = b |
| **Grothendieck group** | K(M), the classes of pairs (a, b) read as a − b: every homomorphism from M to a group extends to it in exactly one way; K(N^6) = Z^6 |
| **Grothendieck delta** | δ(A, B) = ICV(B) − ICV(A), an element of Z^6 |
| **L1 norm** | The sum of the absolute values of a delta's six components |
| **Interval-content distance** | d(A, B), the L1 norm of δ(A, B): a metric on vectors, a pseudometric on sets |
| **Size bound** | The distance is at least the absolute difference between the two sets' numbers of pairs, T(n) = n(n − 1)/2, and has the same parity |

---

## Self-Check Assessment

**1. What is the delta from C major to C7, and the distance?**
> <0, +1, +1, 0, 0, +1>, at distance 3. C7 adds B♭ to C major, and by Theorem 2 one note added to a three-note set always costs 3.

**2. Why can no four-note chord lie at distance 1 or 2 from a triad?**
> The components of the delta add up to T(4) − T(3) = 3, so its L1 norm is at least 3 (Theorem 1).

**3. GA's `FindNearby` returns 24 sets within radius 1 of the C major triad. Which, and what is their true distance from it?**
> C major itself and the other 23 major and minor triads. All share the vector <001110>, so their true distance is 0; the heuristic puts the 23 at 1.

**4. Can `GaIcvNeighbors` with distance 1 list anything for a dominant seventh chord?**
> Only a Z partner, at distance 0: a distance of exactly 1 occurs only between a set of two notes and a set of at most one. The dominant seventh chord's class, 4-27, has no Z partner, so the tool lists nothing.

**Pass criteria:** Build K(M) and explain why K(N^6) = Z^6; compute deltas and distances; prove the size bound, the one-note rule and the distance-zero theorem; name what the distance cannot see; and say where GA's heuristic, comments and tests depart from the mathematics.

---

## Research Basis

- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987: the interval function of two sets
- S. Lang, *Algebra*, revised third edition, Springer, 2002: the Grothendieck group of a commutative monoid
- Streeling MUS-020 for interval-class vectors and the Z-relation, and MAT-022 for groups, invariants and IX's path search
- GA source at commit `40d337479af36d987df3f06c8c638ffd35f13458`, and GA issues #776, #798 and #802: every code fact in §5 links to its line
- Learn's ga-ai course, lessons 14, 22 and 23, at Learn commit `1190ee33650a5637414e73a455b69f3914f44fd6`: the run outputs quoted in §5
- Python checks over all 4,096 sets: every other number in §§1–5 comes from them or from the transcription of GA's code
- Experiment: proposed in §6, not run; this lesson reports no new measurement of GA
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
