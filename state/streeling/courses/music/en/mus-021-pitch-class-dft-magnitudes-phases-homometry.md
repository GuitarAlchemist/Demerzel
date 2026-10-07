---
module_id: mus-021-pitch-class-dft-magnitudes-phases-homometry
department: music
course: The Pitch-Class DFT — Magnitudes, Phases and Homometry
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-021-fourier-analysis-signals]
estimated_duration: "75 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# The Pitch-Class DFT — What the Magnitudes Keep, and What the Phases Add

> **Department of Music** | Stage: Citrinitas (Intermediate to Advanced) | Estimated duration: 75 minutes

## Objectives

After this lesson, you will be able to:
- Compute the Fourier coefficients of a pitch-class set and read them as sums of points on a circle
- Prove that transposition and inversion keep the magnitudes, say what they do to the phases, and say what M5 does to the magnitudes
- Derive Lewin's lemma, and use it to explain why Z-related sets share every magnitude
- Name the sets that maximise each of the six magnitudes, and predict from a set's symmetry which coefficients vanish
- Compare two sets by their phases, and say exactly what a phase similarity of 1 does and does not show
- Trace what GA computes for each of these, and where its names, documentation and tests say something else

---

## 1. A Set as a Signal

Number the pitch classes from C = 0 to B = 11, as MUS-020 does, and write a pitch-class set A as a signal of 12 samples: 1 at each pitch class in A, 0 elsewhere. MAT-021 defines the discrete Fourier transform of such a signal. For a set, the sum runs over its notes:

X_k(A) = Σ_(x ∈ A) e^(−2πikx/12), for k = 0, 1, …, 11.

Each note contributes one point of the unit circle, at an angle of −30k·x degrees, and X_k adds the points. For k = 1, the notes keep their places on the chromatic circle. For k = 5, note x moves to the place of 5x, and the circle becomes the circle of fourths: C, F, B♭, E♭ and so on. X_0 is the number of notes, n. The signal is real, so X_(12−k) is the complex conjugate of X_k (MAT-021 §1), and the coefficients for k = 0 to 6 carry all the information. This lesson uses only those.

A coefficient is large when its points bunch together and small when they spread around the circle. Its **magnitude** |X_k| measures how much they bunch, and its **phase**, the angle φ_k of X_k, says where. For C major {0, 4, 7} and k = 5, the three points sit at 0°, 120° and 30° (C, E and G, since −600° and −1050° are 120° and 30° around the circle), and they add up to X_5 = 1.366 + 1.366i, of magnitude 1.932 and phase 45°.

### Practice Exercise

Compute every coefficient of the tritone C F♯, {0, 6}.

> *Solution:* X_k = 1 + e^(−2πi·6k/12) = 1 + e^(−πik) = 1 + (−1)^k. The coefficients are 2 for even k and 0 for odd k.

---

## 2. Transposition, Inversion and M5

Transposing A by t moves each note x to x + t, and its term becomes e^(−2πik(x+t)/12) = e^(−2πikt/12) e^(−2πikx/12). Every term is multiplied by the same factor, so

X_k(T_t A) = e^(−2πikt/12) X_k(A).

This is the **shift theorem**. The magnitude stays the same, and the phase turns by −30kt degrees: each coefficient turns at its own speed, k times as fast as the first. Inversion I0 sends x to −x, which replaces every term by its conjugate, so X_k(I0 A) is the conjugate of X_k(A): the magnitude stays, and the phase changes sign. Every set of a set class is reached from any other by these operations, so the six magnitudes |X_1| to |X_6| are the same for all the sets of a class.

M5, which multiplies every pitch class by 5, is not one of those operations, but its effect is simple. It sends the term of note x to e^(−2πik·5x/12), which is the term of x in X_5k. So X_k(M5 A) = X_(5k mod 12)(A). For k = 1 to 6, 5k mod 12 is 5, 10, 3, 8, 1 and 6, and |X_10| = |X_2|, |X_8| = |X_4|. M5 swaps |X_1| and |X_5| and keeps the other magnitudes. This is the spectral side of MUS-020 §2, where M5 swaps the counts of interval classes 1 and 5. The chromatic pentachord C C♯ D E♭ E has |X_1| = 3.732 and |X_5| = 0.268. Its image under M5, the pentatonic scale, has the reverse.

A Python check over all 4,096 sets and the 12 transpositions finds the shift theorem, the conjugation and the M5 rule exact up to rounding, with differences below 10⁻¹³.

### Practice Exercise

For C major, X_5 has phase 45°. Without adding any terms, find the phase of X_5 for D major and for C minor.

> *Solution:* D major is T2 of C major, so the phase turns by −30 × 5 × 2 = −300°, which is +60°: 105°. C minor {0, 3, 7} is I7 of C major, since 7 − {0, 4, 7} = {7, 3, 0}, and I7 is I0 followed by T7. I0 turns 45° into −45°, and T7 turns it by −30 × 5 × 7 = −1050°, which is +30°: −15°. The magnitude stays 1.932 in both.

---

## 3. Lewin's Lemma and Homometry

Multiply X_k by its conjugate:

|X_k|² = Σ_(x ∈ A) Σ_(y ∈ A) e^(−2πik(x−y)/12).

The n terms with x = y give n. Every pair of distinct notes appears twice, as x − y and as y − x, and the two terms add up to 2 cos(2πk(x − y)/12). That cosine depends only on the pair's interval class d, as cos(πkd/6). Grouping the pairs by interval class:

|X_k|² = n + 2 Σ_(d=1..6) ICV_d cos(πkd/6),

where ICV_d is the count of interval class d in the interval-class vector of MUS-020 §2. This is **Lewin's lemma**, after Lewin (1959). For C major, n = 3 and the vector is <001110>. For k = 3, the cosines for d = 3, 4 and 5 are cos 270° = 0, cos 360° = 1 and cos 450° = 0, so |X_3|² = 3 + 2 = 5 and |X_3| = 2.236.

The formula also runs backwards. Its seven equations, for k = 0 to 6, form a cosine transform, and they can be solved for n and the six counts. So the seven magnitudes |X_0| to |X_6| and the pair (n, vector) carry the same information: the 4,096 sets have 201 distinct profiles of seven magnitudes and 201 distinct pairs, matched one to one. n matters on both sides: the empty set and a single note share the vector <000000> but not n, and without |X_0| the six magnitudes |X_1| to |X_6| give only 118 profiles, and cannot even tell a set from its complement, whose coefficients are −X_k for every k other than 0, since those of the aggregate are 0.

Two sets are **homometric** when they have the same seven magnitudes |X_0| to |X_6|, that is, the same size and the same |X_1| to |X_6|. Z-related set classes (MUS-020 §5) have the same size and the same vector, so by Lewin's lemma they share all seven. The all-interval tetrachords 4-Z15 (0146) and 4-Z29 (0137) cannot be told apart by any function of the magnitudes, and the same holds for all 23 Z-related pairs.

### Practice Exercise

Compute |X_5| of C major from its vector, and check it against §1.

> *Solution:* For k = 5, the cosines for d = 3, 4 and 5 are cos 450° = 0, cos 600° = −0.5 and cos 750° = 0.866. So |X_5|² = 3 + 2(−0.5 + 0.866) = 3.732, and |X_5| = 1.932, as in §1.

---

## 4. Six Qualities

Each magnitude measures one kind of regularity. Quinn (2006–07) read the six magnitudes as six harmonic qualities, each judged by how close a set comes to the sets that maximise it. A Python search through all sets of each size finds those sets:

- **k = 1**, chromatic clusters: C C♯ D among three notes, with 2.732, and the chromatic hexachord among six, with 3.864.
- **k = 2**, two clusters a tritone apart: C F♯ with 2, the only two-note set up to transposition to reach it, C C♯ F♯ G with 3.464, and C C♯ D F♯ G A♭ with 4.
- **k = 3**, the cycle of major thirds: the augmented triad with 3, and the hexatonic scale C C♯ E F G♯ A with 4.243.
- **k = 4**, the cycle of minor thirds: the diminished seventh chord and the octatonic scale, both with 4.
- **k = 5**, chains of fifths: C D G with 2.732, the pentatonic scale with 3.732, C D E F G A among six, with 3.864, and among seven notes the diatonic collection, with 3.732 as well.
- **k = 6**, the whole-tone scale, with 6. The even and the odd pitch classes form the two whole-tone scales, and X_6 = Σ_(x ∈ A) (−1)^x counts a set's even notes minus its odd ones.

The magnitudes of some familiar sets show the qualities side by side:

| Set | n | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | k = 6 |
|---|---|---|---|---|---|---|---|
| Major triad C E G | 3 | 0.518 | 1 | 2.236 | 1.732 | 1.932 | 1 |
| Augmented triad C E G♯ | 3 | 0 | 0 | 3 | 0 | 0 | 3 |
| Chromatic cluster C C♯ D | 3 | 2.732 | 2 | 1 | 0 | 0.732 | 1 |
| Tritone C F♯ | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| Dominant seventh C E G B♭ | 4 | 0.518 | 1 | 1.414 | 2.646 | 1.932 | 2 |
| Major seventh C E G B | 4 | 0.518 | 1.732 | 2.828 | 1 | 1.932 | 0 |
| Diminished seventh C E♭ G♭ A | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| Pentatonic C D E G A | 5 | 0.268 | 1 | 1 | 1 | 3.732 | 1 |
| Whole-tone scale | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| Hexatonic C C♯ E F G♯ A | 6 | 0 | 0 | 4.243 | 0 | 0 | 0 |
| Diatonic C major scale | 7 | 0.268 | 1 | 1 | 1 | 3.732 | 1 |
| Octatonic C C♯ E♭ E F♯ G A B♭ | 8 | 0 | 0 | 0 | 4 | 0 | 0 |

So no single number says whether a chord sounds whole-tone or fifthy, but one number per quality does. C7 and Cmaj7 are equally fifthy, with 1.932 at k = 5, but C7 leans to the whole-tone scale, with 2 at k = 6, against 0 for Cmaj7, which leans to the augmented triad, with 2.828 at k = 3.

The zeros follow from symmetry. If T_p maps A onto itself, the shift theorem gives X_k(A) = e^(−2πikp/12) X_k(A), so X_k = 0 unless kp is a multiple of 12. Among k = 1 to 6, the augmented triad and the hexatonic scale, fixed by T4, can be non-zero only at k = 3 and 6. The diminished seventh and the octatonic scale, fixed by T3, only at k = 4. The whole-tone scale, fixed by T2, only at k = 6, and the tritone, fixed by T6, only at the even k. The Python check finds no exception among the 4,096 sets. The converse fails: Cmaj7 is fixed by no transposition, yet X_6 = 0, since it has two even and two odd notes.

### Practice Exercise

Why is |X_6| of the whole-tone scale C D E F♯ G♯ B♭ the largest value any set can reach?

> *Solution:* Its notes are the even pitch classes, so each term e^(−2πi·6x/12) = (−1)^x is +1. The six terms add in phase, and |X_6| = 6. No set can do better: X_6 is the number of even notes minus the number of odd ones, at most 6 in size.

---

## 5. What the Phases Add

The magnitudes cannot tell a set from its transpositions and inversions, nor one class of a Z-related pair from the other. The phases can. By §2, transposing by t turns the phase of X_k by −30kt degrees, every coefficient at once, each at its own speed. To compare B with A up to transposition, turn the phases of B for each t and measure how well they line up with those of A, weighting each coefficient by the two magnitudes:

S(A, B) = max over t of Σ_(k=1..6) |X_k(A)| |X_k(B)| cos(φ_k(A) − φ_k(B) + 30°·kt) / Σ_(k=1..6) |X_k(A)| |X_k(B)|.

The values of t that reach the maximum are written t*. If B = T_u A, every cosine equals 1 at t = −u, so S = 1. C major against D major gives S = 1 at t = 10, the transposition that takes D major back to C major. S does not change when either set is transposed. C major against C minor gives S = 0.5714, because an inversion negates the phases instead of turning them. Comparing A also with the inversion of B, whose coefficients are the conjugates of those of B, gives S_TnI(A, B), the larger of the two values. It is 1 for C major and C minor. On the 23 Z-related pairs, S_TnI stays below 1, at most 0.6667: the phases separate the sets that the magnitudes cannot.

**S = 1 does not mean a transposition.** Every term of S, in the sum and in the denominator, is zero unless both sets have a non-zero coefficient at that k, and the magnitudes only weight the cosines. S reaches 1 as soon as, for one t, every phase difference on the shared coefficients vanishes. Take C D E and the augmented triad C E G♯. For k = 1 to 6, the coefficients of the augmented triad are 0, 0, 3, 0, 0 and 3, and those of C D E are 1 − 1.732i, 0, 1, 0, 1 + 1.732i and 3. Only k = 3 and k = 6 count, and there both sets have phase 0. At t = 0 both cosines are 1, and S = (1 × 3 + 3 × 3) / (1 × 3 + 3 × 3) = 1, at t = 4 and t = 8 as well, since T4 and T8 fix the augmented triad. Yet C D E, (024), and C E G♯, (048), are different set classes. When no k has both coefficients non-zero, as for the augmented triad against the diminished seventh, S is 0/0. GA then sets S to 0, and to 1 only when each set is the empty set or the aggregate. The counts in the next paragraph follow that convention: among the pairs they range over, 268 are of this kind and get S = 0.

Zeros are not even needed. The chromatic pentachord C C♯ D E♭ E and the pentatonic scale C D E G A have no zero coefficient, and their magnitudes differ (§2), but their phases agree at t = 0, and S = 1. Over all pairs of distinct Tn-types, leaving aside the empty set and the aggregate, 270 pairs of the same size and 1,230 pairs of different sizes reach S = 1. Among chords: Csus2 and C9 at t = 0, and Cmaj7 and Cdim7 at t = 1, 4, 7 and 10.

S = 1 does give a transposition when the two sets also have the same size and the same magnitudes. Then the phases agree on every non-zero coefficient, so the coefficients of A equal those of a transposition of B for k = 0 to 6, and by conjugation for every k. The inverse DFT turns equal coefficients back into equal sets.

### Practice Exercise

Show that S = 1 between the single note C and the tritone C F♯, and find every t that reaches it.

> *Solution:* {0} has X_k = 1 for every k, with phase 0. By §1, {0, 6} has X_k = 2 for even k and 0 for odd k. Only k = 2, 4 and 6 count, all with phase 0 on both sides, so at t = 0, S = (2 + 2 + 2) / (2 + 2 + 2) = 1. At t = 6, each coefficient turns by 180k degrees, a whole number of turns for even k, so S = 1 there too. A set of one note and a set of two reach S = 1, at t = 0 and t = 6.

---

## 6. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), GA's `main` on 2026-10-06; this lesson documents that code and does not change it, and it has not run GA or its tests. The numbers below come from a line-by-line Python transcription of the GA code named.

**Magnitudes and phases come from the prime form.** [`SetClass.GetFourierCoefficients`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L157) computes the DFT of [`GetSpectralPrimeForm()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L120-L123), the prime form, not of the set the class was built from. The magnitudes are the same for every set of the class (§2), so [`GetMagnitudeSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L190) is right as a property of the class. Its test, [`GetMagnitudeSpectrum_IsInvariantUnderTransposition`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L105), builds one class from C E G and one from D F♯ A. Both reduce to the prime form (037), so both spectra come from the same 12 numbers, and the test would pass even if the DFT did not keep magnitudes under transposition. [`GetPhaseSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L213) returns the phases of the prime form too, the same for C major, D major and C minor, although [its summary](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L211) says that "Phase encodes rotational alignment on the chromatic circle". GA's newer alignment code makes the opposite choice: its coefficients come from the set's ["ACTUAL chroma (not the prime form — phases carry the transposition, which is the point)"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L75-L76). At `40d3374`, no code in GA calls `GetPhaseSpectrum`.

**The centroid and the distance.** [`GetSpectralCentroid`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L230) averages k over all 12 bins, weighted by |X_k|. Because |X_(12−k)| = |X_k|, the bins mirror each other around 6, and the centroid reduces to 6(1 − n / Σ|X_k|), a measure of how much of the total magnitude lies outside bin 0 (see the exercise below). The transcription matches that formula on the 223 non-empty classes to within 10⁻¹³. The centroid runs from 0 for the aggregate to 5.5 for a single note, the value [GA's test](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L129-L139) checks, and [`UnifiedModeService`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Unified/UnifiedModeService.cs#L133) reads it. [`GetSpectralDistance`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L257) adds the absolute differences of magnitude over the 12 bins, so k = 1 to 5 count twice and k = 0 and 6 once. [`SetClassSpectralIndex.GetNearestBySpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L16) ranks classes by the same distance, and by §3 each of the 46 Z-related classes finds its partner first, alone at distance 0 up to rounding. The method leaves out the source [by reference](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L26): a class taken from `SetClass.Items` is left out, but one built anew with `new SetClass(...)` is equal to its copy in the index without being the same object, and comes back first, at distance exactly 0, with its partner second. In the transcription, the partner's distance is a rounding residue between 9 × 10⁻¹⁵ and 3 × 10⁻¹⁴, never exactly 0. At `40d3374`, no code in GA calls `GetSpectralDistance` or `GetNearestBySpectrum`.

**The embedding's labels.** The header comment of the spectral partition of GA's embedding schema states ["Per Lewin's Lemma: ICV = |DFT|²"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L654). By §3, the squared magnitudes are a cosine transform of the size and the vector, not the vector: C major has <001110>, and |X_1|² to |X_6|² are 0.268, 1, 5, 3, 3.732 and 1. GA's own [research note](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L24) states the relation nearly correctly: it leaves out the size. Read for a set, where each pitch class counts once (not a weighted voicing chroma), the schema's labels for the six magnitudes name the wrong sets for four of them. It calls k = 2 ["Whole-tone structure"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L683), but the whole-tone scale has |X_2| = 0. It calls k = 3 ["Diminished structure"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L690), with a "minor-third cycle affinity", but the diminished seventh chord has |X_3| = 0 and the augmented triad maximises it. It calls k = 4 ["Augmented structure"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L697), the reverse. And it calls k = 6 ["Tritone structure"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L712), but the whole-tone scale maximises |X_6|; among two-note sets, the tritone shares the largest |X_6| with the major second and the major third, while it alone reaches the largest |X_2| (§4). The labels of k = 2 and 6 are swapped, and so are those of k = 3 and 4. The labels of k = 1, "Chromatic clumping", and k = 5, "Diatonic structure", are right. The research note's [§5](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L61) repeats the wrong labels and credits them to Quinn, as "Quinn's quality semantics already documented in the schema".

**Phase alignment.** [`SpectralPhaseAlignment.Similarity`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L49) and [`SimilarityTnI`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L57) compute the S and S_TnI of §5 from the set's own coefficients, with optional weights, and set S to 1 or 0 by [convention](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L111-L119) when the denominator vanishes. The transcription reproduces the research note's examples: 1 at t = 10 for C and D major; 0.5714, and 1 through the inversion, for C major and C minor; 0.3333 and 0.6667 for 4-Z15 and 4-Z29; 0.4000 for 6-Z17 and 6-Z43. It finds S_TnI below 1 on all 23 Z-related pairs, at most 0.6667, as the test [`SimilarityTnI_SeparatesAll23ZRelatedPairs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L73) asserts. The documentation promises more: [S = 1 "iff the sets are transposition-aligned"](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L27). The research note's [Theorem 3](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L26-L34) proves one direction, S(A, T_t A) = 1, and the test [`Similarity_IsOne_OnEveryTransposition_Randomized`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L108) checks that direction on 1,000 random sets. The converse fails (§5). The note's [separation corollary](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L43) argues that Z-related sets are separated because they are not TnI-equivalent. By §5 that does not follow: C D E and C E G♯ are not equivalent either, and reach S = 1. The conclusion holds for the 23 pairs because they can be checked one by one: the transcription finds S_TnI at most 0.6667, and GA's test asserts that it stays below 1 − 10⁻⁶ for each.

**What the MCP tool says.** The tool [`GaHomometricDistinguish`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L198) prints, whenever S ≥ 1 − 10⁻⁶, ["Same shape up to transposition — one is a transposition of the other."](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L231-L232) By the transcription, Csus2 against C9 and Cmaj7 against Cdim7 reach that branch. The tool reads both chords with the parser of `GaChordToSet`, which asks the `domain.chordIntervals` closure for a chord's intervals, and GA's tests pin the four readings: `GaChordToSet` turns [Cdim7 into `{C, Eb, F#, A}` and C9 into `{C, D, E, G, Bb}`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L17-L18), and the closure spells [Csus2 `P1 M2 P5`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L36) and [Cmaj7 `P1 M3 P5 M7`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L41). Both test classes first call [`GaClosureBootstrap.init()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L14).

As this lesson is written, no GA issue covers these points. Fixing any of them is for GA's owners; this lesson only describes them.

### Practice Exercise

By the transcription, GA's `GetSpectralCentroid` gives 5.044 for the major triad. Show that the centroid equals 6(1 − n / Σ|X_k|), and check it with the magnitudes of §4.

> *Solution:* Over k = 0 to 11, pair bin k with bin 12 − k for k = 1 to 5: since |X_(12−k)| = |X_k|, they add k|X_k| + (12 − k)|X_k| = 12|X_k| to the weighted sum. Bin 6 adds 6|X_6| and bin 0 adds nothing. The total magnitude is T = n + 2(|X_1| + … + |X_5|) + |X_6|, so the weighted sum is 6(T − n), and the centroid is 6(T − n)/T = 6(1 − n/T). For the major triad, T = 3 + 2(0.518 + 1 + 2.236 + 1.732 + 1.932) + 1, about 18.84, and 6(1 − 3/18.84) is about 5.04: GA's 5.044, to two decimals.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `40d3374`. Nothing in it is a measurement. The predictions come from the transcription of §6 and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Magnitudes under transposition.** For all 4,096 sets, compare `new SetClass(A).GetMagnitudeSpectrum()` with the magnitudes of the lab's own DFT of A, and call `GetPhaseSpectrum` on the classes of C E G, D F♯ A and C E♭ G. Prediction: equal magnitudes for every set, up to rounding; three identical phase arrays.
2. **Homometry.** For each of the 46 Z-related classes, call `SetClassSpectralIndex.GetNearestBySpectrum` on the class taken from `SetClass.Items`, then on the same class built with `new SetClass(...)`, and compare `GetMagnitudeSpectrum` with the partner's. Prediction: the partner comes first, alone at distance 0 up to rounding, for 46 of 46; the class built anew comes back first itself, its partner second; and the spectra are equal up to rounding.
3. **The centroid.** Compare `GetSpectralCentroid` with 6(1 − n / Σ|X_k|) on the 223 non-empty classes. Prediction: equal up to rounding; 5.5 for a single note, 3.000 for the whole-tone scale, 3.515 for the hexatonic scale and 4.091 for the diatonic collection.
4. **Separation.** Call `SimilarityTnI` on the prime forms of the 23 Z-related pairs. Prediction: every value below 1, the largest 0.6667, the smallest 0.3333. This repeats from a real run what GA's test asserts.
5. **The converse.** For every pair of distinct Tn-types, leaving aside the empty set and the aggregate, call `Similarity` on one representative of each. Prediction: S ≥ 1 − 10⁻⁶ for 270 pairs of the same size and 1,230 of different sizes, among them C D E and C E G♯ with t* = 0, 4 and 8.
6. **The MCP tool's verdict.** Call `GaClosureBootstrap.init()`, as GA's tests do, then `GaHomometricDistinguish("Csus2", "C9")` and `GaHomometricDistinguish("Cmaj7", "Cdim7")` directly. Prediction: both end with "Same shape up to transposition — one is a transposition of the other.", with the four readings that GA's tests pin (§6).

### Practice Exercise

Step 5 predicts 1,500 pairs with S = 1 that are not transpositions, yet GA's randomized test would still pass. What test would catch the "iff"?

> *Solution:* One that draws pairs that are not transpositions of each other and asserts S < 1. GA's test only draws a set and one of its transpositions, so it checks the direction that Theorem 3 proves. By the transcription of §6, the opposite assertion would fail on 270 pairs of distinct Tn-types of the same size.

---

## 8. Common Pitfalls

- **Taking the magnitudes for a fingerprint of a set.** Together with the number of notes, |X_0|, they identify a set only up to transposition, inversion and, for 23 pairs of classes, the Z-relation. |X_1| to |X_6| alone cannot even tell a set from its complement.
- **Writing "ICV = |DFT|²".** The squared magnitudes are a cosine transform of the size and the vector; they carry the same information, not the same numbers.
- **Naming a coefficient after the wrong cycle.** k = 3 measures closeness to the augmented triad, a cycle of major thirds; k = 4 to the diminished seventh, a cycle of minor thirds. Coefficient k is largest for sets whose notes lie near k points spaced evenly, 12/k semitones apart: one cluster for k = 1, two clusters a tritone apart for k = 2, the augmented triad for k = 3, the diminished seventh for k = 4, the pentatonic scale for k = 5 and the whole-tone scale for k = 6.
- **Testing an invariant on inputs that agree by construction.** Two set classes with one prime form give one spectrum whatever the DFT does.
- **Reading S = 1 as "same shape".** It says the phases agree, for one t, wherever both sets have a non-zero coefficient, and that there is at least one such coefficient (GA's convention also gives 1 when each set is the empty set or the aggregate). It does not even require the same number of notes.
- **Taking an argument for a check.** A conclusion can be true while the argument offered for it fails; for the Z-related pairs, the exhaustive test is the evidence.
- **Reading the phases of a prime form.** They are the same for every set of the class, and say nothing about where the set sits.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Pitch-class DFT** | The coefficients X_k = Σ_(x ∈ A) e^(−2πikx/12) of a pitch-class set A, for k = 0 to 11 |
| **Magnitude** | The size of a coefficient X_k, unchanged by transposition and inversion |
| **Phase** | The angle of a coefficient, turned by −30kt degrees by a transposition by t and negated by I0 |
| **Shift theorem** | X_k(T_t A) = e^(−2πikt/12) X_k(A) |
| **Lewin's lemma** | The squared magnitude of X_k equals n + 2 Σ_d ICV_d cos(πkd/6), so the magnitudes of X_0 to X_6 and the pair (size, interval-class vector) determine each other |
| **Homometric** | Having the same size and the same magnitudes of X_1 to X_6, as every pair of Z-related sets does |
| **Harmonic quality** | What one magnitude measures: closeness to the sets that maximise it, such as the whole-tone scale for k = 6 |
| **Phase-aligned similarity** | S, the best agreement of two sets' phases over the 12 transpositions, weighted by their magnitudes; S_TnI also tries the inversion |

---

## Self-Check Assessment

**1. Why do C major and C minor have the same six magnitudes?**
> C minor is I7 of C major: I0 replaces every coefficient by its conjugate and T7 multiplies it by a number of size 1, so no magnitude changes.

**2. Which of the coefficients X_1 to X_6 of the octatonic scale can be non-zero, and why?**
> Only X_4. T3 maps the scale onto itself, so X_k = 0 unless 3k is a multiple of 12, which among k = 1 to 6 leaves k = 4. Its magnitude is 4.

**3. Two sets have S = 1. What can you conclude? What if they also have the same magnitudes?**
> Alone, only that for one t their phases agree at every k where both coefficients are non-zero, and that at least one such k exists (GA's convention also gives 1 when each set is the empty set or the aggregate). With the same size and the same magnitudes, their coefficients agree after that transposition, so one set is a transposition of the other.

**4. What does GA's `GetNearestBySpectrum` return first for 4-Z15?**
> 4-Z29, at distance 0 up to rounding: the two classes are homometric, so their magnitude spectra are equal. That holds when 4-Z15 is taken from `SetClass.Items`; a class built anew comes back first itself.

**Pass criteria:** Compute and read the coefficients of a set; derive the shift theorem, the effect of inversion and of M5, and Lewin's lemma; explain homometry and the Z-related pairs; name the prototype of each magnitude and predict zeros from symmetry; and say what a phase similarity of 1 shows, with and without equal magnitudes.

---

## Research Basis

- D. Lewin, "Re: Intervallic Relations between Two Collections of Notes", *Journal of Music Theory* 3/2, 1959: the interval function of two sets and its Fourier transform
- I. Quinn, "General Equal-Tempered Harmony", *Perspectives of New Music* 44/2, 2006 (Introduction and Part I), and 45/1, 2007 (Parts II and III): the Fourier magnitudes as harmonic qualities
- E. Amiot, *Music Through Fourier Space: Discrete Fourier Transform in Music Theory*, Springer, 2016: the DFT of pitch-class sets, Lewin's lemma, homometry and phases
- Streeling MAT-021 for the DFT, and MUS-020 for set classes, interval-class vectors and the Z-relation
- GA source at commit `40d337479af36d987df3f06c8c638ffd35f13458`, including the research note `docs/research/2026-07-04-optick-spectral-phase-alignment.md`: every code fact in §6 links to its line
- Python checks over all 4,096 sets: every number in §§1–6 comes from them or from the transcription of GA's code
- Experiment: proposed in §7, not run; this lesson contains no measurement of GA itself
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
