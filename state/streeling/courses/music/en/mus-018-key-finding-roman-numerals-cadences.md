---
module_id: mus-018-key-finding-roman-numerals-cadences
department: music
course: Key Finding, Roman Numerals and Cadences
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-003-functional-harmony]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Key Finding, Roman Numerals and Cadences — What a Count of Chords Can and Cannot Decide

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- List the triads of a major key and of its relative minor, and explain why chords alone cannot tell the two keys apart
- Score a progression against the 30 major and minor keys by counting its diatonic triads, and break the ties with the cadence, the opening chord and the mode
- Explain why the major V of a minor key is not in its natural minor, and what that does to a count
- Label a progression with Roman numerals once its key is chosen, including secondary dominants and half-diminished chords
- Tell enharmonic keys apart by their spelling, and name the relative key of each of the 30 keys
- Say how key-profile algorithms differ from chord counting, and what each can and cannot hear
- Trace what GA's key identification computes, which of its tools shows what, and where its answers and its documentation disagree

---

## 1. Keys, Diatonic Triads and the Relative Pair

A major key builds a triad on each degree of its scale: I, ii, iii, IV, V, vi and vii°. In C major they are C, Dm, Em, F, G, Am and B°. The **natural minor** on A uses the same seven notes, so its triads are the same seven chords in another order: i, ii°, III, iv, v, VI and VII, that is Am, B°, C, Dm, Em, F and G. A major key and the minor key on its sixth degree form a **relative pair**: they share a key signature, every note and every diatonic triad. Going the other way, the relative major sits on the minor key's third degree.

Minor-key harmony does not stay in the natural minor. To lead back to its tonic, it raises the seventh degree, G to G♯ in A minor. That is the **harmonic minor**. The triad on the fifth degree becomes major, E G♯ B, and the dominant seventh E7 (E G♯ B D) carries the tritone G♯–D whose resolution MUS-003 §3 described. The triad on the seventh degree becomes vii°, G♯ B D. A minor key thus has two dominants on its fifth degree, v from the natural minor and V from the harmonic minor, and its cadences use V.

With at most seven sharps or flats there are 15 major keys and 15 minor keys, 30 names in all. Their scales make only 12 different sets of notes, one for each transposition of the diatonic scale. Nine of these sets carry two names, a major key and its relative minor. The other three carry four, because each of their keys can be spelled two ways: B and C♭ major with G♯ and A♭ minor, F♯ and G♭ major with D♯ and E♭ minor, and C♯ and D♭ major with A♯ and B♭ minor. That makes 9 × 2 + 3 × 4 = 30.

### Practice Exercise

Why can't the chords alone separate C major from A minor in Am F C G?

> *Solution:* The two keys share every diatonic triad, so all four chords belong to both, and so does every note. Only emphasis can decide: which chord opens and which closes, which lasts longest or falls on the strong beats, and above all a cadence, G to C or E to Am. Here Am opens the progression, which leans toward A minor, but nothing in the list of chords proves it.

---

## 2. Counting Diatonic Triads

The simplest key finder reduces each chord to its root and the quality of its triad: major, minor or diminished. A seventh chord counts as its triad, so Dm7 is Dm and G7 is G. For each of the 30 keys, it counts how many of the progression's distinct chords are among the key's seven triads, and it keeps the keys with the highest count.

For Am F C G, C major and A minor both count 4 of 4. Four keys count 3 of 4. F major contains F, C and Am, but its ii is Gm, not G. G major contains C, G and Am, but not F. D minor contains F, C and Am, and E minor contains G, Am and C. Every other key counts at most 1.

A count over the natural minor misses the minor key's own cadence. In Am Dm E7 Am, the triad of E7 is E major, which is not in natural A minor, where the fifth degree carries Em. A minor counts 2 of the 3 distinct chords, no more than C major, F major and D minor. Counting the harmonic V as well gives A minor 3 of 3, alone at the top. That fix has a price in major keys. A **secondary dominant** (MUS-003 §5) borrows the V of a minor key's harmonic form: in C E7 Am F, E7 is V7/vi of C major. With the harmonic V counted, A minor gets all 4 chords and C major 3, so the count names the relative minor of a progression that stays in C major. Without it, C major, A minor, F major and D minor all count 3. Neither way of counting gets both progressions right: the count needs help from the order of the chords.

### Practice Exercise

Score Dm G C against C major, A minor, D minor and G major.

> *Solution:* C major counts 3 of 3 (ii, V, I), and so does A minor (iv, VII, III). D minor counts 2: Dm and C, its i and VII, but G is a major triad, not its natural iv. G major counts 2: G and C, its I and IV, but its V is D major, not Dm.

---

## 3. Breaking the Tie: Cadence, Opening Chord and Mode

A count leaves a key and its relative minor tied whenever every chord is diatonic, and it can leave other keys tied as well. Three kinds of evidence break the tie, in decreasing order of strength.

- **The cadence.** A progression that ends V–I, or V7–I, confirms the key of that I. In a minor key the V of the cadence is the major V of the harmonic minor. A half cadence ends on V, and a plagal cadence ends IV–I. Neither confirms a key in the same way, and a deceptive cadence, V–vi, avoids the tonic altogether.
- **The opening chord.** A progression that opens on a tied key's tonic triad leans toward that key.
- **Convention.** When nothing else decides, a finder has to pick, for instance the major key.

These rules settle the earlier examples. Am F C G opens on Am and goes to A minor, while C G Am F goes to C major. Dm G C ends G–C, V–I of C major, so C major comes first, although A minor has the same count. In Am Dm E7 Am, E7–Am is V7–i of A minor, which decides between the four keys that count 2. C D G C shows that a cadence can matter more than the count. G major and E minor contain all three distinct chords and C major only two, since D is V/V, a secondary dominant. Yet the progression ends G–C and is in C major. A finder that gives the cadence the weight of two chords, as GA does (§7), puts C major first.

Some music has no major or minor key to find. G F C G is in G Mixolydian, the mode of the major scale with a lowered seventh, so its F chord is ♭VII. Its count gives C major and A minor 3 of 3 and G major 2, and its ending C–G is plagal, so no cadence speaks for G. C B♭ F C is in C major with a ♭VII borrowed from C minor; the count prefers F major and D minor, which contain all three distinct chords, to C major, which contains two. A Dorian vamp, Dm7 Em7 repeated, counts 2 of 2 for C major and A minor. A finder whose answers are the 30 major and minor keys can only name the key whose notes these progressions use.

### Practice Exercise

D C♯7 F♯m opens on D. Which key is it in?

> *Solution:* F♯ minor. D and F♯m are both in D major, A major, B minor and F♯ minor, each counting 2 of 3, while the triad of C♯7 is in none of their natural forms. C♯7–F♯m is V7–i of F♯ minor, the harmonic-minor cadence, and it outweighs the opening on D.

---

## 4. Roman Numerals

Once a key is chosen, each chord gets a **Roman numeral**: the degree of its root in the key's scale, written upper case for a major triad, lower case for a minor one, with ° for a diminished triad, ø for a half-diminished seventh, + for an augmented triad, and the figure of the seventh where there is one. In C major, Dm7 G7 Cmaj7 is ii7 V7 Imaj7. In A minor, Bø7 E7 Am is iiø7 V7 i. The triad of Bø7, B D F, is diminished: Bø7 is the same chord as Bm7♭5, a minor seventh with a lowered fifth, not a minor triad. E7 is V7, from the harmonic minor, and Am is i.

Numerals carry function as well as degree. In C E7 Am F G7 C, E7 is **V7/vi**, the dominant of Am, and not a "III7" chord of C major: the numeral names the chord it leads to (MUS-003 §5). A chord whose root is outside the scale gets an accidental: B♭ in C major is ♭VII.

A labeller that only reads the root's degree and the chord's quality will write III for E7 in C major. That describes the chord, but it hides the function, and the two conventions should not be mixed up.

### Practice Exercise

Label C E7 Am F G7 C in C major.

> *Solution:* I, V7/vi, vi, IV, V7, I. The progression tonicizes vi for one chord, then returns through IV and V7 to I.

---

## 5. Enharmonic Keys and the Relative Key

D♭ major and C♯ major sound the same on a guitar and contain the same pitch classes, but they are different keys on paper. D♭ major has five flats; C♯ major has seven sharps, and its chords are spelled C♯, F♯ and G♯. A lead sheet that reads D♭ G♭ A♭ D♭ is in D♭ major, and the spelling is the evidence. A key finder that turns every chord into a pitch class before scoring gives both keys the same score, so it cannot use that evidence.

The relative key is a spelling too. The relative minor of B major is G♯ minor, on B major's sixth degree, and both have five sharps. A♭ minor contains the same pitch classes, but it has seven flats and is the relative minor of C♭ major. The 12 key names of the three sets that carry four names form six enharmonic pairs of the same mode: B and C♭ major, F♯ and G♭ major, C♯ and D♭ major, and G♯ and A♭, D♯ and E♭, A♯ and B♭ minor.

### Practice Exercise

Name the relative keys of F♯ major and of D♯ minor.

> *Solution:* D♯ minor and F♯ major, each with six sharps. E♭ minor and G♭ major have the same notes, but with six flats.

---

## 6. Key Profiles: Weighing Notes Instead of Counting Chords

Chord counting is one family of key finders. Another weighs the notes themselves. Longuet-Higgins and Steedman (1971) found the key of the 48 fugue subjects of Bach's *Well-Tempered Clavier* by eliminating, note by note, the keys whose scale does not contain the note heard, with a rule that favours the key whose tonic, or else dominant, is the first note when elimination does not settle it. Krumhansl and Kessler (1982) asked listeners how well each of the 12 pitch classes fitted a key context. The answers gave a **key profile** for major keys and one for minor keys, highest for the tonic and lowest for the notes outside the scale. In the **Krumhansl–Schmuckler algorithm** (Krumhansl, 1990, ch. 4), the total duration of each pitch class in a passage is correlated with the 24 rotations of the two profiles, and the key with the highest correlation wins. Temperley (1999) reconsidered that algorithm and proposed revisions. His book (Temperley, 2001) treats key finding with preference rules alongside meter, harmony and pitch spelling, and lets the key change during a piece.

The difference with a chord count is weight. A profile method hears that a chord lasts four bars and that the tonic note keeps returning, so it can separate a key from its relative minor where a count of distinct chords cannot. A chord list without durations gives it nothing to weigh, and neither family hears the bass line, the meter or the phrase unless they are added to its input. Both also choose among major and minor keys only, so a Dorian or Mixolydian passage gets the major or minor key whose notes it uses.

### Practice Exercise

C lasts four bars, then Am, F and G one bar each. Why can a duration-weighted profile separate C major from A minor here, when a count of distinct chords cannot?

> *Solution:* Both keys contain the four chords, so the count ties. In the durations, C, E and G weigh far more than A, and C weighs most. The C major profile is highest on C, so its correlation with the passage beats A minor's, whose profile is highest on A.

---

## 7. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); this lesson documents that code and does not change it, and it has not run GA or its tests. The service and its callers are unchanged on GA's `main` today. The numbers come from two places. Learn's [ga-ai lesson 11](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/ga-ai/11-the-chords-the-key-skill-reads.md) compiles GA's service and prints its answers, under the label `6baf32e`, the last commit that changed the service. The other numbers come from a line-by-line Python transcription of the service, the chatbot tool and the array tool, which reproduces every answer that Learn prints for this version of the service, on 53 lines.

**One service, six callers.** [`KeyIdentificationService.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L175) scores the 30 keys of §1 with the major pattern and the [natural-minor pattern](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L40), and counts [distinct chords](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L182). The chatbot's [`KeyIdentificationSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L47) and [`ProgressionCompletionSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ProgressionCompletionSkill.cs#L51), and the MCP tool [`ga_key_identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L62), call it on chords read out of a sentence. The MCP tool [`ga_key_from_progression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L177) and the DSL closures [`domain.analyzeProgression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L405) and [`domain.progressionCompletion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L739) call it on a list of chords.

**The minor V: in the order, not in the count.** The natural-minor pattern puts a minor triad on the fifth degree, and a dominant seventh counts in a minor key only on the [seventh degree](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L207), as VII7, so neither E nor E7 counts in A minor. GA chose the natural count of §2, under which C E7 Am F ties four keys and C major comes first by its opening chord. The cadence comes back in the order of the candidates:

```csharp
            .Where(s => s.Candidate.MatchCount > 0)
            .OrderByDescending(s => s.Candidate.MatchCount + s.Cadence)
            .ThenByDescending(s => s.OpensOnTonic)
            .ThenByDescending(s => s.Candidate.Key.EndsWith("major", StringComparison.OrdinalIgnoreCase))
            .ThenBy(s => s.Candidate.Key)
            .Select(s => s.Candidate)];
```

[`CadenceWeight`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L233) adds 2 when the last two chords are the key's V, as a major triad or a dominant seventh, and its tonic triad. Then come the opening chord and the major key, as in §3, and last the key's name. Am Dm E7 Am therefore puts A minor first, at 2 of 3. The service's remark about C E7 Am F G7 C says that A minor [matches more chords](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L165). That was true of the harmonic count, not of this code: C major and A minor both count 4 of 5, and the cadence G7–C puts C major first, as [the test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L104) requires.

**Two counts for one progression.** [`IsChordDiatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L251) does [accept the harmonic V](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L265) in a minor key, and the array tool's confidence counts every chord of the list, repeats included, [with it](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L187). The chatbot shows the count of `Identify` instead, as ["N/M chords diatonic"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L105). For Am Dm E7 Am the array tool reports A minor at 4/4 (100%), as the [closure's test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L97) asserts for its confidence, while `Identify` counts 2 of 3. The array tool keeps the order of `Identify` but [computes its own score](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L204), so its first key can show the lower confidence. For C E7 Am F G7 C, its best guess is C major at 5/6 (83%), followed by A minor at 6/6 (100%). For C D G C, it is C major at 3/4 (75%), followed by G major and E minor at 4/4 (100%).

**What the chatbot reads.** The chords of a sentence are read with [one regular expression](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L325) whose final `\b` drops a sharp before a space. In "What key is F# B C# F# in?", F♯ is read as F and C♯ as C. The signs ♭ and ♯ are not read, C° is read as C major, and CM7, CΔ7 and Cø7 are skipped. Repeated chords are [removed](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L299) before `Identify` sees them. "What key is C D G C in?" is read as C D G, whose last two chords are V–I of G major, and the answer is [G major](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L92). The chord parser turns min into m, then keeps the triad by deleting [everything from the first digit](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L319) on, with a maj, aug, sus or add just before it. Bm7♭5, written Bm7b5, becomes Bm, a minor triad, so a iiø7 never matches ii°. AM7 becomes A minor, and a [test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L149) asserts that AM7, read as a minor chord, is diatonic to C major. In standard chord symbols CM7 is Cmaj7, a major seventh. Learn asked the six textbook progressions of its lesson in the 15 keys of their mode, 90 questions. On [this version](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L84), 50 put the textbook key first, 13 tied it at the top but not first, 11 left it out of the top, and 16 lost or misread a chord.

**The top the model is shown.** The tool hands the model the keys tied at the top, then up to three more from the ordered list:

```csharp
        var topScore = candidates[0].MatchCount;
        var topTied  = candidates
            .Where(c => c.MatchCount == topScore)
            .Select(ToCandidate)
            .ToArray();
        var partial  = candidates
            .Skip(topTied.Length)
            .Take(MaxPartialCandidates)
            .Select(ToCandidate)
            .ToArray();
```

The top is cut by the first key's count, while the order uses the count plus the cadence, so the two disagree whenever the cadence lifts a key with a lower count. For C♯m7b5 F♯7 Bm, iiø7 V7 i of B minor, B minor comes first at 1 of 3 through its cadence. The top is then the [six keys at 1 of 3](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L103), and G♯ minor, at 2 of 3, comes among the partial matches. Five other keys count 2 of 3, A major, B major, C♭ major, A♭ minor and F♯ minor, and appear in neither list. For Bm7b5 E7 Am, the minor ii–V–i of [GA's own corpus](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/Progressions/README.md#L37), the top is six keys at 1 of 3. The partial matches repeat three of them, C major, D major and F major, and the four keys at 2 of 3, A major, E minor, F♯ minor and G major, are left out. The skill's prompt calls the top ["all tied at the highest score"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L102), which it is not here. The corpus test uses a second definition, the [highest count](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/ProgressionCorpusMatrixTests.cs#L440) among all keys, which leaves A minor out of the top for Bm7b5 E7 Am.

**Enharmonic keys and relative keys.** Chord roots become [pitch classes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L106) before scoring, so the enharmonic twins of §5 always get the same score, and the [key's name](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L227) decides between them. D♭ G♭ A♭ D♭ puts [C♯ major first](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L88), and the 13 questions of Learn's grid that tie the textbook key without putting it first are all such ties. Each key's relative is the [first key of the other mode](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L98) with the same pitch classes, so [6 of the 30](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L107) are spelled from the twin: B major's relative is given as A♭ minor, and G♯ minor's as C♭ major.

**Roman numerals.** [`romanFor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L355) takes the degree from the position of the root in the major or natural-minor scale, and the case and sign from the chord. Am Dm E7 Am is labelled [i iv V i](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L99), and C Bdim Bm7b5 Caug in C major [I vii° viiø I+](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L110). A root outside the scale gets [a question mark](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L374), so B♭ in C major is "?", not ♭VII. There is no secondary-dominant notation: E7 in C major is labelled by its degree, as the III chord of §4.

**What the documentation says.** The skill's instructions give a [single-candidate example](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L60), Dm G C in C major at 3/3, but the tool returns C major and A minor [tied](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L9), as relative keys always are. The instructions expect ["almost always 2"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L64) tied keys, and the tool's documentation ["often 1 element"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L131); enharmonic sets give four, and the examples above six. The instructions also point to the service at [a path](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L88) where it no longer is. A test comment says that [B minor lacks A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L86) as a major triad. In fact A is VII of natural B minor, and E major's relative is C♯ minor; the assertion itself holds.

GA's issues [#771](https://github.com/GuitarAlchemist/ga/issues/771) and [#772](https://github.com/GuitarAlchemist/ga/issues/772), both open, report how the chatbot reads chords, how it groups the top, the enharmonic ties, the relative keys and the single-candidate example. Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

`ga_key_identify` answers G major for "What key is C D G C in?", while `ga_key_from_progression`, given ["C", "D", "G", "C"], answers C major. Explain both answers.

> *Solution:* The chatbot tool reads C D G, because it drops the repeated C. Its last two chords, D and G, are V–I of G major, so G major gets the cadence weight on top of its count of 3. The array tool keeps the list as it is, so the ending is G–C, V–I of C major. C major's count of 2 plus the cadence weight of 2 then beats G major's 3. C major is the textbook answer: D is V/V. The array tool still lists it first with the lower confidence, 3/4 (75%), against G major's 4/4 (100%).

---

## 8. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's ga-ai lab, which compiles GA's service. Nothing in it is a measurement. The predictions come from the transcription of §7 and are written down before any run; a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server or a language model.

1. **Identify on a fixed corpus.** Call `Identify` on Am F C G, C G Am F, C E7 Am F G7 C, Am Dm E7 Am, D C♯7 F♯m, C D G C, Dm7 G7, G F C G, C B♭ F C (written C Bb F C) and Dm7 Em7 Dm7 Em7. Prediction, first key and its count: A minor 4/4, C major 4/4, C major 4/5, A minor 2/3, F♯ minor 2/3, C major 2/3, C major 2/2, C major 3/3, F major 3/3 and C major 2/2.
2. **The chatbot tool on the same progressions.** Ask `KeyIdentificationMcpTools.IdentifyKey` "What key is … in?" for each. Prediction: C D G C is read as C D G and answered G major, with E minor tied; Am Dm E7 Am is read as Am Dm E7, with A minor, C major, F major and D minor tied at 2/3, A minor first.
3. **The array tool.** Call `GaKeyFromProgression` on C E7 Am F G7 C and C D G C. Prediction: C major at 5/6 (83%) ahead of A minor at 6/6 (100%), and C major at 3/4 (75%) ahead of G major and E minor at 4/4 (100%).
4. **Two definitions of the top.** For Bm7b5 E7 Am, compute the tool's top and its partial matches, and the corpus test's top. Prediction: six keys at 1/3 with A minor first; partial matches C major, D major and F major, already in the top; the corpus's top A major, E minor, F♯ minor and G major, without A minor.
5. **The harmonic V counted.** In a copy of the service inside the lab, never in GA itself, count a major triad or a dominant seventh on the fifth degree of a minor key. Prediction: Am Dm E7 Am gives A minor 3/3, alone; C E7 Am F gives A minor 4/4 ahead of C major 3/4; C E7 Am F G7 C still puts C major first, at 4/5 plus the cadence, ahead of A minor at 5/5.
6. **Enharmonic spelling.** Call `Identify` on D♭ G♭ A♭ D♭ and on C♯ F♯ G♯ C♯, both as lists. Prediction: the same answer for both, C♯ major first, then D♭ major.

### Practice Exercise

Step 5 changes the count. Which result would show that the change is worth making, and which that it is not?

> *Solution:* It is worth making if minor-key cadences such as Am Dm E7 Am are found without help from the order, while progressions in major keys with a secondary dominant keep their key. C E7 Am F shows it is not: the relative minor wins, since there is no final cadence to correct the count. A fair test needs a corpus that holds both kinds, with the keys written down before the run.

---

## 9. Common Pitfalls

- **Taking a tie for an answer.** A key and its relative minor always tie on their chords; emphasis decides between them.
- **Counting the harmonic V everywhere.** It finds minor-key cadences, and it pulls major-key secondary dominants toward the relative minor.
- **Reading a chord list without its order or its repeats.** The cadence is in the order, and a repeated tonic is emphasis.
- **Reducing chords to pitch classes before choosing between enharmonic keys.** The spelling is the evidence.
- **Reading "N/M chords diatonic" as confidence.** Two of GA's tools compute different N for the same chords, and the first key can show the lower one.
- **Naming a mode with a major and minor key finder.** Dorian and Mixolydian vamps come out as the key whose notes they use.
- **Trusting a top without asking how it was cut.** Cut by the first key's count or by the highest count of all keys, the same candidates give different lists, and neither follows the order by count plus cadence.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Diatonic triad** | A triad built from the notes of a key's scale on one of its seven degrees |
| **Relative pair** | A major key and the minor key on its sixth degree, with the same key signature and the same triads |
| **Natural minor** | The minor scale with the key signature's notes; its triad on the fifth degree is minor |
| **Harmonic minor** | The minor scale with a raised seventh degree, which makes the fifth degree's triad major |
| **Authentic cadence** | V or V7 to I (or i), the ending that confirms a key |
| **Secondary dominant** | The V or V7 of a chord other than I, written V7/vi for the dominant seventh of vi |
| **Roman numeral** | A chord's degree in the key, with case and signs for its quality |
| **Enharmonic keys** | Keys of the same mode whose tonics are one pitch spelled two ways, such as D♭ major and C♯ major |
| **Key profile** | The weight of each of the 12 pitch classes in a major or minor key context |
| **Krumhansl–Schmuckler algorithm** | Correlate a passage's durations per pitch class with the 24 rotated key profiles |

---

## Self-Check Assessment

**1. Which keys tie for Em C G D, and which does the opening decide?**
> G major and E minor count 4 of 4. The progression opens on Em, the tonic triad of E minor, so a finder that weighs the opening chord picks E minor, as GA's [test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L122) requires.

**2. Why does a natural-minor count leave Am Dm E7 Am at 2 of 3 for A minor?**
> The triad of E7 is E major, the V of the harmonic minor. The natural minor's fifth degree carries Em, so E7 is not counted.

**3. A lead sheet reads D♭ G♭ A♭ D♭, and a key finder answers C♯ major. What went wrong?**
> The finder turned the chords into pitch classes, which D♭ major and C♯ major share, and then chose by name. The spelling, with five flats rather than seven sharps, says D♭ major.

**4. For C♯m7b5 F♯7 Bm, `ga_key_identify` returns six keys as its top candidates, ["tied at the highest match count"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L140), at 1 of 3. What key is it in, and what is missing?**
> B minor: iiø7 V7 i. The top is cut by the first key's count, while the order adds the cadence. Keys that count 2 of 3 are missing from the top: G♯ minor appears among the partial matches, and five others appear nowhere.

**Pass criteria:** Name the triads of a key and of its relative; score a progression by counting diatonic triads and break the tie with the cadence and the opening chord; explain the natural-minor count's blind spot and the price of counting the harmonic V; label a progression with Roman numerals, secondary dominants included; tell enharmonic keys and relative keys apart by spelling; and say which of GA's tools shows which count.

---

## Research Basis

- M. Gotham, K. Gullings, C. Hamm, B. Hughes, B. Jarvis, M. Lavengood and J. Peterson, *Open Music Theory*, version 2, VIVA Open Publishing, 2021 (CC BY-SA 4.0): diatonic triads, the natural and harmonic minor, and Roman numerals
- S. Kostka, D. Payne and B. Almén, *Tonal Harmony*, 7th edition, McGraw-Hill, 2013: Roman numerals, cadences and secondary dominants
- H. C. Longuet-Higgins and M. J. Steedman, "On interpreting Bach", *Machine Intelligence* 6, 1971, pp. 221–241: key finding by eliminating keys note by note
- C. L. Krumhansl and E. J. Kessler, "Tracing the dynamic changes in perceived tonal organization in a spatial representation of musical keys", *Psychological Review* 89(4), 1982, pp. 334–368: the probe-tone key profiles
- C. L. Krumhansl, *Cognitive Foundations of Musical Pitch*, Oxford University Press, 1990, chapter 4, "A key-finding algorithm based on tonal hierarchies": the Krumhansl–Schmuckler algorithm
- D. Temperley, "What's key for key? The Krumhansl-Schmuckler key-finding algorithm reconsidered", *Music Perception* 17(1), 1999, pp. 65–100
- D. Temperley, *The Cognition of Basic Musical Structures*, MIT Press, 2001: key finding with preference rules
- Wikipedia, "Chord names and symbols (popular music)": CM7, CΔ7 and Cmaj7 as names of the major seventh
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §7 links to its line; GA issues #771 and #772
- Learn, ga-ai lesson 11 and its expected output at commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: the compiled answers of GA's service quoted in §7
- Experiment: proposed in §8, not run; this lesson contains no measurement of its own
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
