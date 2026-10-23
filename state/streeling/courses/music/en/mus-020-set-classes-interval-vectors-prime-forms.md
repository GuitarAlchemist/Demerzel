---
module_id: mus-020-set-classes-interval-vectors-prime-forms
department: music
course: Set Classes, Interval Vectors, the Z-Relation and Prime Forms
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-002-beyond-tonality]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Set Classes, Interval Vectors, the Z-Relation and Prime Forms — Two Packings, One Catalogue

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Group pitch-class sets by transposition alone and by transposition and inversion, and tell from a set's symmetry how many sets its class contains
- Compute an interval-class vector, show that a whole set class shares it, and say what multiplying by 5 does to it
- Find a normal order and a prime form with Forte's rule and with Rahn's rule, and name the six set classes on which they disagree
- Explain why the smallest 12-bit number among a set's 24 forms is its prime form under Rahn's rule
- Count set classes with Burnside's lemma
- State the complement theorem and the hexachord theorem, and use them with the M-relation to explain how the 23 Z-related pairs are distributed and how some of them are related
- Read a Forte number, and tell it apart from an ordinal that only looks like one
- Trace what GA computes for each of these, and where its names, documentation and tests say something else

---

## 1. Pitch-Class Sets and Their Symmetries

Number the pitch classes from C = 0 to B = 11, as MUS-002 does. A chord, a scale or the notes of a melody then become a **pitch-class set**, a subset of the 12 pitch classes. There are 2¹² = 4,096 of them, from the empty set to the full aggregate.

Two kinds of operation move a set without changing its shape. **Transposition** Tn adds n to every pitch class, mod 12. **Inversion followed by transposition**, TnI (In for short), sends every x to n − x. Together they make 24 operations. T2 turns C major {0, 4, 7} into D major {2, 6, 9}. I0 turns it into {0, 8, 5}, F minor, and I7 into {7, 3, 0}, C minor: a mirror that exchanges C and G and turns E into E♭.

Sets related by a transposition form a **Tn-type**; sets related by a transposition or an inversion form a **set class**. The 4,096 sets fall into 352 Tn-types and 224 set classes. A major and a minor triad are two Tn-types of one set class, which Forte's catalogue (§6) labels 3-11.

How many sets a class contains depends on how symmetric its members are. If k of the 24 operations map a set onto itself, its class contains 24 / k sets. Only T0 maps a major triad onto itself, so its class holds 24 sets: the 12 major and the 12 minor triads. The augmented triad C E G♯ is mapped onto itself by T0, T4, T8 and three inversions, so its class holds 24 / 6 = 4 sets. The class of the diminished seventh chord holds 3, that of the whole-tone scale 2, and that of the aggregate 1.

### Practice Exercise

The class of C7, C E G B♭, contains 24 sets; the class of Cmaj7, C E G B, only 12. Why?

> *Solution:* Only T0 maps C7 onto itself, so its class holds 24 sets: the 12 dominant sevenths and their 12 inversions, the half-diminished sevenths (I0 turns {0, 4, 7, 10} into {0, 8, 5, 2}, D F A♭ C, Dø7). Cmaj7 is its own inversion: I11 swaps C with B and E with G. Two of the 24 operations map it onto itself, so its class holds 24 / 2 = 12 sets, the major sevenths.

---

## 2. Interval-Class Vectors

Take every pair of notes in a set, measure the interval between them in semitones, and fold it into an **interval class** from 1 to 6: an interval and its inversion, such as a fourth and a fifth, make one class. The six counts form the set's **interval-class vector**. A set of n notes has n(n − 1)/2 pairs, and the counts add up to that number. C major has one minor third (E–G), one major third (C–E) and one fifth (C–G): <001110>. C7 has <012111>, Cmaj7 <101220>, the diminished seventh chord <004002> and the major scale <254361>.

Every set of a set class has the same vector. A transposition keeps the difference between any two notes. An inversion turns a difference d into −d, which is the same interval class. So C major and C minor share <001110>, and C7 and Cø7 share <012111>. The converse fails: two sets can share a vector without sharing a class (§5).

Multiplying every pitch class by 5, the operation **M5**, is not one of the 24 operations of §1, but its effect on the vector is simple. It multiplies every interval by 5: 1 becomes 5; 2 becomes 10, interval class 2; 3 becomes 15, which is 3; 4 becomes 20, which is 8, interval class 4; 5 becomes 25, which is 1; and 6 becomes 30, which is 6. So M5 swaps the counts of interval classes 1 and 5 and keeps the others. The chromatic pentachord C C♯ D E♭ E, <432100>, becomes C F B♭ E♭ A♭, <032140>: a stack of fourths, the pentatonic scale. M5 moves 132 of the 224 set classes to another class: it sends C major to C A♭ B, a member of the class written (014) in §3. M7 is M5 followed by I0, since 7 = −5 mod 12.

### Practice Exercise

Compute the vector of C E G A, which is both C6 and Am7.

> *Solution:* Six pairs, by interval class: C–E (4), C–G (5), C–A (3), E–G (3), E–A (5) and G–A (2). One interval class 2, two 3s, one 4 and two 5s: <012120>.

---

## 3. Normal Order and Prime Form: Two Ways to Pack

To name a set class, theorists choose one member and write it in a standard order. The **normal order** of a set is the rotation of its notes, in ascending order around the octave, with the smallest span from first to last note. When rotations tie, they are compared by their intervals from the first note, and the tie can be broken from either end:

- **Forte (1973)** packs to the left: the smaller interval from the first note to the second, then to the third, and so on.
- **Rahn (1980)** packs from the right: the smaller interval from the first note to the next-to-last, then to the one before it, and so on.

The **prime form** compares the normal orders of the set and of its inversion, both transposed to start on 0, by the same rule, and keeps the more packed one. Prime forms are written in parentheses without commas, with T and E for 10 and 11: (037) for both triads.

The two rules can differ only when candidates tie on the span. Take 5-20, C C♯ F F♯ A♭, {0, 1, 5, 6, 8}. Two rotations span 8: 0 1 5 6 8 and, from F, 0 1 3 7 8. The inversion gives two more of span 8, 0 1 5 7 8 and 0 2 3 7 8. From the left, the second intervals are 1, 1, 1 and 2; among the first three, the third intervals are 5, 3 and 5, so Forte's prime form is (01378). From the right, the next-to-last intervals are 6, 7, 7 and 7, so Rahn's prime form is (01568). Over all 224 set classes, the two rules disagree on six:

| Set class | Rahn | Forte |
|---|---|---|
| 5-20 | (01568) | (01378) |
| 6-Z29 | (023679) | (013689) |
| 6-31 | (014579) | (013589) |
| 7-Z18 | (0145679) | (0123589) |
| 7-20 | (0125679) | (0124789) |
| 8-26 | (0134578T) | (0124579T) |

These six classes hold 120 of the 4,096 sets. Every other set gets the same prime form from both rules.

**Why a computer can skip the rules.** Write a set as a 12-bit number, with bit p set when pitch class p is present: C major {0, 4, 7} is 1 + 16 + 128 = 145. Comparing two such numbers compares their highest pitch classes first, since 2^p is larger than the sum of all lower powers of 2. Among the 24 forms of a set, the smallest number contains 0, because transposing a set down lowers every bit. Then it has the smallest last note, which is the smallest span, then the smallest next-to-last note, and so on. That is Rahn's rule. For 5-20, (01568) is 1 + 2 + 32 + 64 + 256 = 355, and (01378) is 395.

### Practice Exercise

C C♯ E F G A, {0, 1, 4, 5, 7, 9}, belongs to 6-31. Give its prime form under each rule, and the 12-bit number of each.

> *Solution:* Four forms span 9: 0 1 4 5 7 9 and, from E, 0 1 3 5 8 9, then 0 2 4 5 8 9 and 0 1 4 6 8 9 from the inversion. From the left, the second intervals are 1, 1, 2 and 1, and the third intervals of the three left are 4, 3 and 4: Forte's (013589), 1 + 2 + 8 + 32 + 256 + 512 = 811. From the right, the next-to-last intervals are 7, 8, 8 and 8: Rahn's (014579), 1 + 2 + 16 + 32 + 128 + 512 = 691. The smaller number is Rahn's.

---

## 4. Counting Set Classes

**Burnside's lemma** counts classes without listing them: the number of classes is the average, over the operations, of the number of sets each operation leaves unchanged.

Take the 220 sets of three notes. Among the 12 transpositions, T0 leaves all 220 unchanged, T4 and T8 leave the 4 augmented triads unchanged, and the others leave none: (220 + 4 + 4) / 12 = 19 Tn-types. Now add the 12 inversions. When n is even, TnI mirrors the pitch-class circle across an axis through two pitch classes, n/2 and n/2 + 6. It leaves a set of three notes unchanged when the set holds one of those two and one of the five pairs that the mirror swaps: 2 × 5 = 10 sets. When n is odd, the axis passes between pitch classes, every note is swapped with another, and no set of three notes is left unchanged. So (228 + 6 × 10) / 24 = 12 set classes.

| Notes | Set classes | Tn-types |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 6 | 6 |
| 3 | 12 | 19 |
| 4 | 29 | 43 |
| 5 | 38 | 66 |
| 6 | 50 | 80 |
| 7 | 38 | 66 |
| 8 | 29 | 43 |
| 9 | 12 | 19 |
| 10 | 6 | 6 |
| 11 | 1 | 1 |
| 12 | 1 | 1 |
| Total | 224 | 352 |

The columns are symmetric, because complementation pairs the sets of n notes with those of 12 − n. A class holds one Tn-type when an inversion maps its members onto themselves, and two otherwise, such as 3-11A, the minor triads, and 3-11B, the major triads. So 352 − 224 = 128 classes hold two Tn-types, and the other 96 are inversionally symmetric. The totals are the numbers of binary bracelets and binary necklaces with 12 beads (OEIS A000029 and A000031).

### Practice Exercise

Which of the 12 trichord classes are their own inversion? Check that the count agrees with 19 Tn-types.

> *Solution:* (012), (024), (027), (036) and (048), the classes of C C♯ D, C D E, C D G, C E♭ G♭ and C E G♯: inverting any of them gives a transposition of the same set. The other 7 classes hold two Tn-types each, so 5 + 2 × 7 = 19.

---

## 5. Complements and the Z-Relation

The **complement** of a set holds the pitch classes it lacks, and its vector follows from the set's. Fix an interval class k from 1 to 5. The aggregate holds 12 pairs at interval class k, and each note has two partners at that distance. If a set of n notes holds a_k such pairs, its notes take part in 2n pairs counted from their side, 2a_k of them inside the set, so 2n − 2a_k pairs cross to the complement. The complement keeps the rest: 12 − a_k − (2n − 2a_k) = a_k + 12 − 2n. For the tritone, with 6 pairs in all and one partner per note, the same count gives a_6 + 6 − n. This is the **complement theorem**: every count but the tritone's changes by 12 − 2n, and the tritone's by 6 − n.

For a hexachord, n = 6, so a hexachord and its complement have the same vector. This is the **hexachord theorem**, often called Babbitt's.

Two set classes with the same number of notes and the same vector are **Z-related**. There are 23 such pairs. One is among tetrachords, 4-Z15 (0146) and 4-Z29 (0137), both <111111>. Three are among pentachords, 15 among hexachords, 3 among heptachords and 1 among octachords. The complement theorem explains the symmetry: the complements of two Z-related sets also share a vector, so the pairs of 4 and 8 notes, and of 5 and 7, come together. Of the 50 hexachord classes, 20 contain their own complements. Each of the other 30 has its complements in its Z partner, which accounts for all 15 pairs of hexachords.

M5 accounts for some pairs in another way. It swaps the counts of interval classes 1 and 5 (§2), so a set whose two counts are equal keeps its vector under M5: the image lies in the same class or in its Z partner. 4-Z15 is such a case: 0 1 4 6 times 5 is 0 5 8 6, whose normal order 5 6 8 0 gives (0137), 4-Z29. Nine of the 23 pairs are related this way: 4-Z15/4-Z29, 5-Z17/5-Z37, 5-Z18/5-Z38, 6-Z6/6-Z38, 6-Z11/6-Z40, 6-Z19/6-Z44, 7-Z17/7-Z37, 7-Z18/7-Z38 and 8-Z15/8-Z29.

### Practice Exercise

Show that 5-Z17 (01348) and 5-Z37 (03458) have the same vector, and that M5 maps one onto the other.

> *Solution:* Both have <212320>. Multiplying 0 1 3 4 8 by 5 gives 0 5 3 8 4, that is {0, 3, 4, 5, 8}. Its only rotation of span 8 starts on 0, and its inversion gives the same, so its prime form is (03458).

---

## 6. Forte Numbers

Forte (1973) gave every class of 3 to 9 notes, 208 in all, a name of the form cardinality-index: 3-11 is the eleventh trichord class. A Z before the index marks a Z-related class. Two conventions make the catalogue easier to use. Except for the Z-related hexachords, whose complements lie in the Z partner, a class of n notes and the class of its complements carry the same index: 4-Z15 and 8-Z15, or 5-35, the pentatonic scale, and 7-35, the diatonic collection that its complement forms. And of each Z-related pair of hexachords, one carries an index from 3 to 29 and the other an index from 36 to 50.

The labels are Forte's; the forms printed next to them depend on the packing. A table that follows Rahn prints (01568) next to 5-20, one that follows Forte prints (01378). An ordinal that counts through some other ordering is not a Forte number, even when it has the same shape (§7).

### Practice Exercise

The black keys of a piano, C♯ D♯ F♯ G♯ A♯, form a pentatonic scale. Name its class and the class of the white keys.

> *Solution:* 5-35, (02479), and 7-35, (013568T), for the seven white keys, its complement. The index is the same, as for every pair of complementary classes except the Z-related hexachords.

---

## 7. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); this lesson documents that code and does not change it, and it has not run GA or its tests. The files it cites are unchanged on GA's `main` at `6d5ff22`. Learn's [music-theory-ga lesson 4](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/04-set-classes.mdx) compiles an earlier version of GA, `a826864`, and checks its set classes against the textbook definitions. The other numbers below come from a line-by-line Python transcription of the GA code named.

**Prime forms are Rahn's, by number.** [`PitchClassSetId.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L137) keeps the smallest id among the 24 forms, and [`PitchClassSet.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L161) and [`SetClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L53) are built on it. By §3, that is Rahn's rule, and Learn's program, compiled at `a826864`, found it for [4,096 of 4,096 sets](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L45). GA's own test compares the prime form with what it calls an [independent oracle](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L32), which also takes the smallest of the 24 ids. It pins the definition rather than checking it against a packing rule, and none of its [three anchors](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L89) is among the six classes of §3.

**The normal form is not the textbook's.** [`ToNormalForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L420) keeps the rotation whose gaps between successive notes, around the circle, are the most even: the smallest difference between the largest and the smallest gap, then the lexicographically smaller sequence of gaps. Its remarks say so, ["This is not the textbook normal form"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L415), and the code calls that difference of gaps the [span](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L671). The table that `ToNormalForm` reads is built by [this loop](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L631):

```csharp
                var rotation = Rotr12(set, member);
                Gaps(rotation, count, gaps);
                var span = Span(gaps[..count]);
                if (span > bestSpan || (span == bestSpan && !MoreCompact(gaps[..count], bestGaps[..count])))
                {
                    continue;
                }
```

On the 4,095 non-empty sets, its answer differs on 1,998 from the normal order of Rahn's rule transposed to 0. The method's own example still describes the textbook rule: for G B D, it calls the result 0 3 8 the most compact, with a span [from 0 to 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L402), although 0 4 7, from G, spans 7. The prime form does not use this method, but GA's [closest-key search](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L559) does: it expects a minor key when the normal form contains pitch class 3. Every major triad gets 0 3 8, so for C E G, which three major and three minor keys contain, the search picks a minor key.

**The Z-relation and the M-relation.** [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L199) looks in the set's [modal family](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114), the sets containing 0 that share its vector, for a member that is not among the 24 forms of the family's first member. The transcription agrees with the vector on all 4,096 sets, and [a test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82) checks it against the Z of every stored label. [`SetClass.MRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L80) applies M5 to a class, and 92 of the 224 classes are their own M5 image.

**Two catalogues.** [`CanonicalForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L25) stores Forte's labels for 1 to 6 notes and derives those of 7 to 11 notes from [the complement](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L227). Its remarks say that ["the stored prime forms are Rahn's"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L16) and name the six classes of §3. [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) numbers the classes of each size by the id of their vector, then by prime id:

```csharp
            var ordered = group
                .OrderBy(sc => sc.IntervalClassVector.Id)
                .ThenBy(sc => sc.PrimeForm.Id.Value)
                .ToList();

            for (var i = 0; i < ordered.Count; i++)
            {
                var setClass = ordered[i];
                var forte = new ForteNumber(cardinality, i + 1);
                result[setClass.PrimeForm.Id] = forte;
            }
```

Its summary calls the result a ["Forte-style catalog"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L6), and its remarks call the differences from Forte's numbering ["minor"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L18). Of the 208 classes in Forte's table, it gives the same index as Forte to 3: 5-Z18, 6-21 and 8-Z15. The major triad comes out 3-2, and the diatonic collection 7-1. [`ForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ForteCatalog.cs#L11) says the ordinal "diverges for most set classes" and must not be shown to users. GA's issue [#544](https://github.com/GuitarAlchemist/ga/issues/544), now closed, found {4, 5, 10, 11} tagged 4-21 instead of 4-9, and the chord recognizer cites it where it [names a chord by Forte's catalogue](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L327). [`SetClassLabelFormatter`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClassLabelFormatter.cs#L32) still offers the ordinal as the "Rahn" notation, although Rahn's name belongs to a packing rule, not to a numbering.

**What the catalogue tests check.** The [catalogue's tests](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L7) prove it "against GA's own atonal engine" with four constraints: every stored form is a GA set class, the counts per size match, the labels match GA's classes one to one, and the Z markers agree with `IsZRelated`. Three tests enforce them: [the counts](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L32), [the one-to-one match](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L47), which also covers membership, and [the Z markers](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82). A fourth checks [the round trip](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L145) from form to label and back. They show that the table agrees with GA and with itself, not that it is Forte's: exchanging the forms of two stored labels of the same size and Z status, such as 5-1 and 5-2, would keep all of them true. The file's other tests name nine labels, and none of 5-1, 5-2, 7-1 or 7-2 is among them (§8, step 5).

**The vector's id.** [`IntervalClassVectorId`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L17) packs the six counts as base-12 digits. The aggregate's counts of 12 do not fit a digit, and its id is now [decoded as a special case](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L49). Learn's lesson 4, compiled at `a826864`, still shows the earlier answer, [<1 1 1 1 0 6>](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L18).

**What the chatbot reads.** The chatbot's [`IntervalClassVectorSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L31) builds a chord from its own table of qualities. It lowercases the quality [before comparing](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L199), so "CM7" becomes "m7" and gets the vector of a minor seventh, <012120>, instead of the major seventh's <101220>, although [its table lists "M7"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L206). A quality outside the table, such as C7♯9, C13 or Cadd9, falls back to [the major triad](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L216), and the answer still carries [confidence 1.0](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L226). Its [chord pattern](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L66) also takes the article in "ICV of a major scale" for the chord A.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

GA's `ToNormalForm` returns 0 3 8 for G B D. What does the textbook normal order give, and why does GA's prime form still come out right?

> *Solution:* The rotations are G B D (0 4 7, span 7), B D G (0 3 8, span 8) and D G B (0 5 9, span 9). Both Forte's and Rahn's rule keep G B D, 0 4 7, since its span is the only smallest one. GA's prime form never calls `ToNormalForm`: it takes the smallest id of the 24 forms, which gives (037).

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `5c3a52a`. Nothing in it is a measurement. The predictions come from the transcription of §7 and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Prime forms.** For all 4,096 sets, compare `PitchClassSet.PrimeForm` with Rahn's and Forte's rules. Prediction: Rahn's on all 4,096 sets; Forte's on all but the 120 sets of the six classes of §3.
2. **Normal forms.** Compare `ToNormalForm` with Rahn's normal order transposed to 0. Prediction: 1,998 differences among the 4,095 non-empty sets, among them G B D, given as 0 3 8.
3. **Complements and Z.** Over the 224 classes, count the classes for which `IsZRelated` is true, and compare each hexachord class with the class of its complement. Prediction: 46; the complement lies in the same class for 20 hexachord classes and in the Z partner for the other 30; and the complement theorem of §5 holds for all 4,096 sets.
4. **The M-relation.** Apply `SetClass.MRelated` to every class. Prediction: 92 classes are their own image, and 9 of the 23 Z pairs are each other's image.
5. **The catalogue tests under a swap.** In a copy of `CanonicalForteCatalog` inside the lab, never in GA itself, exchange the forms of 5-1 and 5-2 and run the same four tests against the copy. Prediction: all four pass.
6. **Two numberings.** Compare `ProgrammaticForteCatalog` with `CanonicalForteCatalog`, ignoring the Z. Prediction: the same index for 7 of the 224 classes: the four classes of 0, 1, 11 and 12 notes, and 5-Z18, 6-21 and 8-Z15.
7. **The chatbot's vectors.** Call `IntervalClassVectorSkill.ExecuteAsync` with "ICV of CM7", "ICV of C7#9" and "ICV of a major scale". Prediction: <012120>; <001110> at confidence 1.0; and <001110> again.

### Practice Exercise

Step 5 predicts that the four tests still pass after the swap. What kind of test would fail?

> *Solution:* One that compares every stored form with a copy of Forte's table made independently of GA's file, entered from another source. Membership, counts, a one-to-one match, Z markers and a round trip cannot tell apart two labels of the same size and Z status.

---

## 9. Common Pitfalls

- **Calling the major and minor triads two set classes.** They are two Tn-types of one class, 3-11.
- **Reading a prime form without its rule.** Six classes have two prime forms; check whether a table packs to the left or from the right.
- **Taking a shared vector for a shared class.** 23 pairs of classes share their vector.
- **Assuming M5 keeps a set's class or its vector.** It sends C major to (014); it keeps the vector only when the counts of interval classes 1 and 5 are equal.
- **Taking an ordinal for a Forte number.** A label of the form n-k is Forte's only if it comes from Forte's table.
- **Trusting the name of a method.** A library's "normal form" or "span" may not be the textbook's; read the definition.
- **Reading a consistency test as a correctness test.** A table can agree with itself everywhere and still carry a wrong label.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Pitch-class set** | A subset of the 12 pitch classes, numbered from C = 0 to B = 11 |
| **Tn-type** | The sets related to one another by transposition |
| **Set class** | The sets related to one another by transposition or by inversion followed by transposition |
| **Interval-class vector** | The counts of the six interval classes among all pairs of notes in a set |
| **Normal order** | The rotation of a set with the smallest span, ties broken by Forte's or Rahn's rule |
| **Prime form** | The more packed of the normal orders of a set and of its inversion, transposed to start on 0 |
| **Complement** | The pitch classes that a set does not contain |
| **Z-relation** | The relation between two set classes of the same size with the same interval-class vector |
| **M5** | Multiplication of every pitch class by 5, which swaps the counts of interval classes 1 and 5 |
| **Forte number** | Forte's label cardinality-index, with a Z for a Z-related class |

---

## Self-Check Assessment

**1. How many sets does the class of the diminished seventh chord contain, and why?**
> 3. C E♭ G♭ A is mapped onto itself by T0, T3, T6, T9 and four inversions, 8 of the 24 operations, so its class holds 24 / 8 = 3 sets: the three diminished seventh chords.

**2. A set of five notes has the vector <212320>. What is the vector of its complement?**
> <434541>. With n = 5, the complement theorem adds 12 − 2n = 2 to the first five counts and 6 − n = 1 to the tritone's.

**3. Which prime form does a table that follows Forte print for 6-Z29, and which does one that follows Rahn print?**
> Forte's (013689) and Rahn's (023679). 6-Z29 is one of the six classes on which the rules disagree.

**4. GA's [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) labels the major triad 3-2. Is that its Forte number?**
> No. The major triad is 3-11 in Forte's catalogue, and 3-2 there is (013). The programmatic ordinal follows the vector's id, and it gives the same index as Forte to only 3 of the 208 classes in his table.

**Pass criteria:** Group sets into Tn-types and set classes and size a class from its symmetry; compute an interval-class vector and its complement's; find the prime form by both rules and name the six classes on which they differ; count classes with Burnside's lemma; explain the Z-relation with the complement theorem and M5; and tell a Forte number from an ordinal.

---

## Research Basis

- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973: the catalogue of set classes, normal order packed to the left, Forte numbers and the Z-relation
- J. Rahn, *Basic Atonal Theory*, Longman, 1980: normal order packed from the right
- J. N. Straus, *Introduction to Post-Tonal Theory*, 4th edition, W. W. Norton, 2016: normal order, prime form, interval-class vectors, complements and the Z-relation
- OEIS A000029 and A000031: the numbers of binary bracelets and binary necklaces, 224 and 352 for 12 beads
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §7 links to its line; GA issue #544
- Learn, music-theory-ga lesson 4 and its expected output at commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: the compiled check of GA's prime forms quoted in §7
- Experiment: proposed in §8, not run; this lesson contains no measurement of its own
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
