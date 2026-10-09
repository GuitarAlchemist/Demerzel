---
module_id: mat-022-symmetry-groups-invariants
department: mathematics
course: Symmetry, Groups and Invariants
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Symmetry, Groups and Invariants — Counting Set Classes, and What an Invariant Forgets

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Describe transposition and inversion of pitch classes as the dihedral group D12 acting on the 4096 subsets of Z/12, and check the group and action laws
- Compute orbits and stabilisers, and predict the size of a set class with the orbit–stabiliser theorem
- Count orbits with Burnside's lemma: 352 transposition classes, 224 set classes, and the counts for each cardinality
- Tell a complete invariant from an incomplete one, and read the Z-relation as the interval-class vector failing to separate orbits
- Treat the neo-Riemannian P, L and R as involutions on the 24 consonant triads, and explain why they commute with transposition and inversion
- Trace what IX's `ix-bracelet` crate computes: which representative it calls a prime form, and which sets its harmonic-path search can reach

---

## 1. Groups and Actions

Number the pitch classes C = 0, C♯ = 1, …, B = 11, so that they form Z/12, the integers modulo 12. Transposition by n is T_n: x ↦ x + n, and inversion followed by transposition is T_nI: x ↦ n − x. These 24 maps form a **group**: composing two of them gives a third, T_0 is the identity, and each has an inverse, since T_n undoes T_(−n) and each T_nI undoes itself, because n − (n − x) = x. On the clock face T_n is a rotation and T_nI a reflection, and the group is the **dihedral group** D12 of the regular 12-gon. Read compositions right to left, as for functions: T_mI T_n sends x to m − (x + n), so it is T_(m−n)I. The group is not commutative: T_1 T_0I sends x to 1 − x, while T_0I T_1 sends it to −(x + 1) = 11 − x.

A group **acts** on a set when each element g moves the points of the set, with the identity moving nothing and (gh)·x = g·(h·x). D12 acts on pitch-class sets point by point: T_n{0, 4, 7} = {n, n + 4, n + 7}. It permutes the 2^12 = 4096 subsets of Z/12 and never changes their cardinality.

### Practice Exercise

Compute T_3I of the C major triad {0, 4, 7}, and apply T_3I again.

> *Solution:* 3 − 0 = 3, 3 − 4 = 11 and 3 − 7 = 8, so T_3I{0, 4, 7} = {3, 8, 11}, the G♯ minor triad. Applying T_3I again gives 3 − 3 = 0, 3 − 8 = 7 and 3 − 11 = 4, the C major triad: T_3I is its own inverse.

---

## 2. Orbits and Stabilisers

The **orbit** of a set X is the collection of its images g·X, and its **stabiliser** is the set of elements g with g·X = X. Orbits partition the 4096 subsets. Under D12 they are the **set classes**; under the subgroup C12 of the twelve transpositions they are the transposition classes. The **orbit–stabiliser theorem** says |orbit| · |stabiliser| = |G|, here 24. The proof: g·X = h·X exactly when h⁻¹g lies in the stabiliser, so the elements that send X to a given image form one coset of the stabiliser, and all cosets have its size.

No transposition fixes the C major triad, and every inversion turns it into a minor triad, so its stabiliser is {T_0} and its orbit has 24 members, the 12 major and 12 minor triads. The augmented triad {0, 4, 8} is fixed by T_0, T_4 and T_8 and by T_0I, T_4I and T_8I, a stabiliser of 6 and an orbit of 4, the four augmented triads. The diminished seventh {0, 3, 6, 9} has a stabiliser of 8, the T_n and T_nI with n = 0, 3, 6 or 9, and an orbit of 3. Since a stabiliser is a subgroup, its order divides 24, and so does the size of every set class.

### Practice Exercise

Find the stabiliser and the orbit of the whole-tone scale {0, 2, 4, 6, 8, 10}.

> *Solution:* T_n maps the even pitch classes onto themselves for every even n, and so does T_nI, since n minus an even number is even; for odd n both send them to the odd ones. The stabiliser has 12 elements, and the orbit 24/12 = 2: the two whole-tone scales.

---

## 3. Counting Orbits with Burnside's Lemma

Dividing 4096 by 24 does not count the set classes; it is not even an integer, because symmetric sets have smaller orbits. **Burnside's lemma** counts them exactly: the number of orbits is the average number of fixed points, (1/|G|) Σ_g |Fix(g)|. Count the pairs (g, X) with g·X = X in two ways. By g they number Σ_g |Fix(g)|; by X they number Σ_X |Stab(X)| = Σ_X 24/|Orb(X)|, and the members of each orbit together contribute exactly 24.

**Rotations.** T_n splits Z/12 into gcd(n, 12) cycles, and a set is fixed when it is a union of cycles, so T_n fixes 2^gcd(n, 12) sets. For n = 0, …, 11 this gives 4096 + 2 + 4 + 8 + 16 + 2 + 64 + 2 + 16 + 8 + 4 + 2 = 4224, and 4224/12 = 352 transposition classes.

**Reflections.** T_nI fixes the pitch classes x with 2x = n. For even n there are two, n/2 and n/2 + 6, and the other ten form five swapped pairs, so 2^7 = 128 sets are fixed; for odd n there are none, six pairs and 2^6 = 64 fixed sets. The six even and six odd reflections fix 6 × 128 + 6 × 64 = 1152 sets, and (4224 + 1152)/24 = 5376/24 = 224 set classes.

**One cardinality at a time.** For trichords, only T_4 and T_8 fix anything besides the identity, the four augmented triads each: (220 + 4 + 4)/12 = 228/12 = 19 transposition classes. An even reflection fixes a trichord made of one fixed pitch class and one swapped pair, 2 × 5 = 10 of them, and an odd reflection fixes none: (228 + 60)/24 = 288/24 = 12 set classes. Five of the twelve are symmetric, 3-1, 3-6, 3-9, 3-10 and 3-12, and the other seven split into two transposition classes each, which gives 12 + 7 = 19 again.

| Cardinality | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Transposition classes (C12) | 1 | 1 | 6 | 19 | 43 | 66 | 80 | 66 | 43 | 19 | 6 | 1 | 1 | 352 |
| Set classes (D12) | 1 | 1 | 6 | 12 | 29 | 38 | 50 | 38 | 29 | 12 | 6 | 1 | 1 | 224 |

### Practice Exercise

Count the tetrachord classes with Burnside's lemma, first under transposition alone, then under D12.

> *Solution:* The identity fixes all C(12, 4) = 495 tetrachords. T_3 and T_9 have three cycles of length 4 and fix 3 each; T_6 has six cycles of length 2 and fixes C(6, 2) = 15; the other rotations fix none. So (495 + 3 + 3 + 15)/12 = 516/12 = 43. An even reflection fixes the two fixed points with one pair, or two of its five pairs: 5 + 10 = 15; an odd reflection fixes two of its six pairs, again 15. So (516 + 12 × 15)/24 = 696/24 = 29.

---

## 4. Invariants and Normal Forms

An **invariant** is a function that takes the same value on every member of an orbit. Cardinality is one. The interval-class vector is another: T_n preserves every difference between two pitch classes, T_nI negates it, and the interval class min(d, 12 − d) ignores the sign. An invariant is **complete** when it also separates orbits, so that equal values imply the same orbit. The interval-class vector is not complete: {0, 1, 4, 6} and {0, 1, 3, 7} both have one interval of each class, the vector ⟨111111⟩, yet they lie in different orbits, 4-Z15 and 4-Z29. This is the **Z-relation**. An exhaustive check over the 224 classes, in the manner of MAT-002, finds 23 such pairs, 46 classes in all: 1 pair of tetrachords, 3 of pentachords, 15 of hexachords, 3 of heptachords and 1 of octachords.

A **normal form** is a complete invariant of a particular kind: a rule that picks one member of each orbit, the same whichever member it starts from. The prime form of a set class is such a rule, and the two published rules break ties differently: Forte's and Rahn's give different prime forms for 6 of the 224 classes, 5-20, 6-Z29, 6-31, 7-Z18, 7-20 and 8-26. Any rule that returns the smallest member of the orbit in a fixed total order is also a normal form, but it need not print what a published table prints. The magnitudes of the discrete Fourier transform of a pitch-class set are further invariants, and they do not separate Z-related classes either: the two members of each of the 23 pairs share them.

### Practice Exercise

Show that {0, 1, 4, 6} and {0, 1, 3, 7} have the same interval-class vector, and find an invariant that separates them.

> *Solution:* The six differences in {0, 1, 4, 6} are 1, 4, 6, 3, 5 and 2, and in {0, 1, 3, 7} they are 1, 3, 7, 2, 6 and 4, where 7 is the interval class 5: one of each class in both. Going round the circle, the steps between successive notes are 1, 3, 2, 6 for the first set and 1, 2, 4, 5 for the second. T_n keeps this cycle of steps and T_nI reverses it, so the multiset of steps is an invariant, and {1, 2, 3, 6} ≠ {1, 2, 4, 5}.

---

## 5. Neo-Riemannian Transformations

Three operations act on the 24 major and minor triads. **P** (parallel) keeps the root and the fifth and moves the third by a semitone: C major ↔ C minor. **L** (leading-tone exchange) keeps the third and the fifth of a major triad and lowers its root by a semitone: C major {0, 4, 7} ↔ E minor {4, 7, 11}. **R** (relative) keeps the root and the third of a major triad and raises its fifth by a tone: C major ↔ A minor {9, 0, 4}. Each keeps two notes of the triad and reflects the third about them, so each is an inversion chosen by the triad itself, and each is an **involution**: applied twice, it returns the triad it started from.

Because each is defined by the triad's own intervals, and T_n and T_nI carry intervals along, P, L and R commute with every transposition and inversion: transposing and then applying P gives the same triad as applying P and then transposing. The three generate a group of order 24 that acts on the same 24 triads, the dual of the T/I group in the sense of Lewin. Alternating P and L from C major visits six triads, C major, C minor, A♭ major, A♭ minor, E major and E minor, the hexatonic cycle, whose notes {0, 3, 4, 7, 8, 11} form the hexatonic collection. Alternating P and R visits eight, the octatonic cycle through C, E♭, F♯ and A. Alternating R and L visits all 24.

### Practice Exercise

Starting from C major, apply L, then P, then R. Where do you land, and what do the two triads share?

> *Solution:* L gives E minor {4, 7, 11}; P gives E major {4, 8, 11}; R keeps E and G♯ and moves B up a tone to C♯, giving C♯ minor {1, 4, 8}. C major and C♯ minor share their third, E: this is the slide S. Applying R, then P, then L also gives C♯ minor, since S is an involution.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of `dihedral.rs`, `action.rs`, `orbit.rs`, `prime_form.rs`, `forte.rs`, `neo_riemannian.rs` and `grothendieck.rs` in `crates/ix-bracelet`, and of the `ix_grothendieck_path` handler. These numbers are predictions, and §7 proposes to check them.

**The group and the action.** The crate presents [D12 by generators and relations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L1), composes elements by the [rule for r^i s^j](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L67), and [reflects before it rotates](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L41), so that an element with a reflection sends x to n − x, the T_nI of §1. The action law is, in the words of the trait, [verified in tests, not by this trait](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L10); the transcription checks it for all 576 pairs of elements, on four sets. [`orbit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L13) lists the 24 images of a set, and its tests fix the orbit of the [augmented triad](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L118) at 4 and of the [diminished seventh](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L125) at 3, as §2 derives. `all_prime_forms` finds its 224 classes by reducing [every mask](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L43) to its representative, and its comment names the [Burnside/Pólya total](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L36) that §3 computes.

**What IX calls a prime form is neither Forte's nor Rahn's.** The function behind every representative is:

```rust
/// Minimum (under [`lex_less`]) over all 24 dihedral images of `x`.
pub fn bracelet_prime_form(x: PcSet) -> PcSet {
    let mut best = x;
    for reflected in [false, true] {
        for rotation in 0u8..12 {
            let g = DihedralElement {
                rotation,
                reflected,
            };
            let cand = g.apply(x);
            if lex_less(cand.raw(), best.raw()) {
                best = cand;
            }
        }
    }
    best
}
```

- **The order is lexicographic on sorted lists.** `lex_less` implements the [lex order on sorted PC lists](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L12), so the representative is the orbit member whose sorted list is smallest, not the most compact normal form of §4. The module comment says that this matches [Forte's set-class convention](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L5). It does for the classes, not for their spellings: the representative is Forte's prime form for 189 classes and Rahn's for 183. For 4-10 it returns [0, 1, 3, 10], where both published rules give (0235).
- **The Forte numbers are right.** [`forte_number`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L360) looks up [this representative](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L363) in a table of 224 masks, and each mask carries the number that the published list gives its orbit. The table's header says that the masks [coincide exactly with the canonical Forte orbits](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L19), which is true of orbits. The invariance test checks [eight probe sets](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L427) under the 24 elements.
- **The spelling reaches users.** The DuckDB function `ix_prime_form` returns this representative as the [bracelet prime form](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/bracelet.rs#L9), so a query that compares its output with a published table disagrees on 35 classes with a table in Forte's spelling and on 41 with one in Rahn's.

**The neo-Riemannian operators.** [`p`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L36), [`l`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L48) and [`r`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L59) implement §5 on the 24 consonant triads, and a [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L134) checks that all three are involutions. The transcription adds that they generate a group of order 24 and commute with T_1 and with T_0I. The comment on the slide reads ["L ∘ P ∘ R applied left-to-right"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L67), while the code [`l(p(r(x)?)?)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L70) applies R first. Since S is an involution, both orders give the same triad.

**The harmonic path cannot reach the augmented triad.** `find_shortest_path` runs IX's A* over the sets of one cardinality, and a step goes to any other set whose [interval-class vector](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L129) lies within L1 distance [2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L259):

```rust
    fn successors(&self) -> Vec<(PcSet, Self, f64)> {
        let card = self.current.cardinality();
        find_nearby(self.current, FIND_NEARBY_RADIUS_PER_STEP)
            .into_iter()
            .filter(|(s, _, _)| s.cardinality() == card && *s != self.current)
            .map(|(s, _, _)| {
                (
                    s,
                    PathNode {
                        current: s,
                        target: self.target,
                    },
                    1.0,
                )
            })
            .collect()
    }
```

- **Some classes form islands.** Two major thirds among three notes force the third interval to be a major third too, so no trichord has exactly two intervals of class 4. The augmented triad's vector ⟨000300⟩ therefore lies at L1 distance 4 or more from every other trichord's, and the four augmented triads form a component of their own. The 12 diminished triads form another, and among tetrachords the three diminished sevenths do. The trichords split into components of 4, 12, 36 and 168 sets, the tetrachords into components of 3, 30 and 462.
- **"Not found" has two meanings.** [`find_shortest_path`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L275) returns an empty path when [A* finds none](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L169), and also when the shortest one is longer than `max_steps`. `ix_grothendieck_path` defaults `max_steps` to [5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7066) and reports both cases as [`"found": false`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7075). From {0, 4, 8} to {0, 4, 7} it reports no path, although moving one voice by a semitone joins them; the distance is built on an invariant, and cannot see what that invariant forgets.
- **The heuristic is sound; its comment hesitates.** The heuristic is [half the L1 distance to the target](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L289). It is consistent, which IX's A* needs because [closed states are never reopened](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L75), so the paths it returns are shortest; every trichord in the component of C major is at most 3 steps from it. The doc comment reaches that conclusion after a correction left in place, ["wait, actually"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L267).
- **Other gaps.** Nothing returns a stabiliser or counts orbits by Burnside's lemma; there is no prime form in Forte's or Rahn's spelling; P, L and R are defined on consonant triads only; and the path search measures distance between interval-class vectors, not voice leading.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Show that the heuristic h = L1/2 is consistent for steps of cost 1 whose interval-class vectors differ by at most 2 in L1 distance.

> *Solution:* For a step from u to v and a target t, the triangle inequality gives L1(u, t) ≤ L1(u, v) + L1(v, t) ≤ 2 + L1(v, t). Dividing by 2, h(u) ≤ 1 + h(v): the estimate never falls by more than the cost of the step, which is consistency, and h(t) = 0 at the target.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Burnside against enumeration.** Apply `necklace_prime_form` and `bracelet_prime_form` to all 4096 masks and count the distinct results for each cardinality. Prediction: 352 and 224 in all, split as in the table of §3.
2. **Stabilisers.** For every mask, count the elements that fix it and the members of `orbit_unique`. Prediction: the product is 24 for every mask; the rotations fix 4224 sets in all and the reflections 1152.
3. **Spellings.** Compare `bracelet_prime_form` of each class with Forte's and Rahn's prime forms. Prediction: 35 and 41 differences, with [0, 1, 3, 10] for 4-10.
4. **Neo-Riemannian cycles.** Apply `p`, `l`, `r`, `s`, `n` and `h` twice to each of the 24 triads, then alternate P and L, P and R, and R and L from C major. Prediction: six involutions, and cycles of 6, 8 and 24 triads.
5. **Paths.** Call `find_shortest_path` from {0, 4, 8} to {0, 4, 7} with `max_steps` 10, and from {0, 4, 7} to {0, 1, 2} with 3, then 2. Prediction: an empty path; a path of four sets; an empty path.

### Practice Exercise

In step 5, how can a caller tell whether an empty path means that no path exists or that the limit was too small?

> *Solution:* A shortest path never visits a set twice, so it has fewer steps than there are sets of that cardinality. With `max_steps` at C(12, k) − 1, 219 for trichords, an empty path means that no path exists. Cheaper still, compare the components of the interval-class graph, which depend only on the vectors.

---

## 8. Common Pitfalls

- **Composing in the wrong order.** T_mI T_n is T_(m−n)I, not T_(m+n)I; the group is not commutative, so say which map acts first.
- **Dividing by the group order to count classes.** Symmetric sets have smaller orbits; use Burnside's lemma, or count orbits directly.
- **Taking an invariant for a complete one.** Equal interval-class vectors do not make two sets equivalent under transposition and inversion: the Z-relation.
- **Mixing prime-form conventions.** Forte's and Rahn's rules differ on six classes, and a lexicographic representative differs from both on dozens; name the rule before comparing tables.
- **Confusing a class with its representative.** Two tools can agree on every class and still print different prime forms.
- **Reading "no path" as "unrelated".** A distance built on an invariant cannot see what the invariant forgets, such as voice leading.
- **Leaving the order of a neo-Riemannian product unstated.** Left to right and right to left agree only when the product is an involution, as for S.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Group** | A set with an associative composition, an identity and an inverse for every element |
| **Dihedral group D12** | The 24 symmetries of the regular 12-gon: the transpositions T_n and the inversions T_nI |
| **Group action** | A rule g·x under which the identity moves nothing and (gh)·x = g·(h·x) |
| **Orbit** | The images g·X of X; for D12 on pitch-class sets, a set class |
| **Stabiliser** | The elements g with g·X = X |
| **Orbit–stabiliser theorem** | The size of an orbit times the size of the stabiliser equals the order of the group |
| **Burnside's lemma** | The number of orbits equals the average number of fixed points |
| **Invariant** | A function constant on orbits; complete when it also separates them |
| **Z-relation** | Two set classes that share an interval-class vector |
| **Prime form** | A canonical member of a set class, chosen by a stated tie-breaking rule |
| **Neo-Riemannian P, L, R** | The inversions of a consonant triad that keep two of its notes |
| **Involution** | A map that is its own inverse |

---

## Self-Check Assessment

**1. A published table lists 4-10 as (0235), and IX prints [0, 1, 3, 10]. Is one of them wrong?**
> Neither. T_10 sends {0, 2, 3, 5} to {10, 0, 1, 3}, so both lie in the same orbit, and `forte_number` gives both 4-10. They differ only in the rule that picks the representative: the published rules take the most compact form, IX the lexicographically smallest sorted list.

**2. Without enumerating anything, why can a set class not have 5 or 7 members?**
> By the orbit–stabiliser theorem, the size of an orbit is 24 divided by the order of its stabiliser, which is a subgroup of D12. The possible sizes are the divisors of 24: 1, 2, 3, 4, 6, 8, 12 and 24.

**3. `ix_grothendieck_path` returns `"found": false` from the augmented triad to C major. What does that tell you?**
> That in IX's graph, where sets are joined when their interval-class vectors lie within L1 distance 2, the four augmented triads form a component of their own, since no trichord has exactly two intervals of class 4. It says nothing about voice leading, where one semitone joins them. In general the flag can also mean that the path exceeds `max_steps`; here it cannot, since the component has four sets.

**4. Why do P, L and R commute with every T_n and T_nI?**
> Each keeps two notes of the triad and reflects the third about them, a rule stated in the triad's own intervals. T_n and T_nI carry those intervals along, so applying P after a transposition or an inversion gives the image of P's result.

**Pass criteria:** Describe transposition and inversion as the group D12 acting on pitch-class sets; compute orbits and stabilisers; count classes with Burnside's lemma, in total and by cardinality; tell a complete invariant from an incomplete one and explain the Z-relation; work with P, L and R and their cycles; and trace which representative IX calls a prime form and which sets its path search can reach.

---

## Research Basis

- W. Burnside, *Theory of Groups of Finite Order*, Cambridge University Press, 1897: the orbit-counting lemma, also credited to Cauchy and Frobenius
- G. Pólya, "Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen", *Acta Mathematica* 68, 1937: counting under symmetry
- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973: set classes and their numbering
- J. Rahn, *Basic Atonal Theory*, Longman, 1980: the prime-form rule most current tables use
- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987: transformation groups and contextual inversion
- R. Cohn, "Maximally smooth cycles, hexatonic systems, and the analysis of late-Romantic triadic progressions", *Music Analysis* 15, 1996: hexatonic cycles
- R. Cohn, "Neo-Riemannian operations, parsimonious trichords, and their Tonnetz representations", *Journal of Music Theory* 41, 1997: P, L, R and their cycles
- A. S. Crans, T. M. Fiore and R. Satyendra, "Musical actions of dihedral groups", *American Mathematical Monthly* 116, 2009: the PLR group as the dual of the T/I group
- D. Tymoczko, *A Geometry of Music*, Oxford University Press, 2011: voice-leading distance
- E. Amiot, *Music Through Fourier Space*, Springer, 2016: Fourier magnitudes as invariants
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
