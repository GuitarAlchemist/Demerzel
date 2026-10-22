# SEM-004 bounded AI learner dry-run — raw first response

## Attempt record

- AI learner: Codex, an OpenAI agent based on GPT-6. This is an AI attempt, not a human learning trial, subject review, or approval.
- Prior competence: general existing competence with array indexing, permutations, inverse functions, composition, elementary geometry, and the distinction between a value and its identifier. No pretest was administered, so this attempt does not measure learning gains.
- Actual UTC start: 2026-10-21 23:53:10 UTC, obtained from the clock tool immediately before reading.
- Actual UTC end: 2026-10-21 23:54:22.349 UTC
- Elapsed wall time: 72.349 seconds, including reading and preparing this artifact; not a measure of human study time.
- Files read: only `C:\tmp\streeling-craft-dryrun-20261021-r1\sem-004\lesson.md` and `C:\tmp\streeling-craft-dryrun-20261021-r1\sem-004\task.md`.
- Handout identity: the supplied local `task.md`; no blob SHA or separate handout revision was supplied. The lesson declares module `sem-004-face-identity-under-reindexing`, version `0.1.0`, research cycle `semiotics-2026-10-21-004`.
- Assistance: the supplied lesson and task, general prior mathematical competence, clock and file tools. No external sources, fixtures, answer keys, other responses, original courses, or memory were consulted. No executable arithmetic checker was used.
- Preservation: this is the first submitted answer, created once. The calculation steps below are concise explanatory derivations. No subsequent correction or retest is included, and no score is assigned.

## Task handout answers

### 1. Output arrays, inverse, and domains

Let I be the input index space and O the transformed output index space. The given `p: I -> O` is `[1,3,0,2]`. Place each input item into output slot `p[i]`:

| Input i | Label | Input level | Output p[i] |
|---:|---|---:|---:|
| 0 | U | 2 | 1 |
| 1 | V | 0 | 3 |
| 2 | W | 3 | 0 |
| 3 | X | 1 | 2 |

Thus output labels are `[W,U,X,V]`, and output levels are `[3,2,1,0]`.

The inverse `r: O -> I` is `[2,0,3,1]`, because output slots 0, 1, 2, 3 came from input slots 2, 0, 3, 1 respectively.

Both inverse compositions, listing every argument:

- `r[p[0]], r[p[1]], r[p[2]], r[p[3]] = r[1], r[3], r[0], r[2] = [0,1,2,3]` in I.
- `p[r[0]], p[r[1]], p[r[2]], p[r[3]] = p[2], p[0], p[3], p[1] = [0,1,2,3]` in O.

The identical displayed integers do not erase the distinction between I and O. Each composition is the identity on its own domain.

### 2. Selection provenance

The original input selection is 3/X. Its output index is `p[3] = 2`, which contains X. The output click at slot 0 traces backward through `r[0] = 2`, identifying input W. A stale reuse of selected integer 3 in O selects V, originally input 1, rather than X.

### 3. Property comparison

Input levels `[2,0,3,1]` and output levels `[3,2,1,0]` already disagree at raw slot 0: 2 versus 3. Slot 0 names different material faces in the two arrays.

The correspondence-aware expression is `newLevels[p[i]] == oldLevels[i]`:

- U/input 0: `newLevels[1] = 2 = oldLevels[0]`.
- V/input 1: `newLevels[3] = 0 = oldLevels[1]`.
- W/input 2: `newLevels[0] = 3 = oldLevels[2]`.
- X/input 3: `newLevels[2] = 1 = oldLevels[3]`.

All four synthetic materials retain their supplied level values. This conclusion uses the supplied correspondence and constructed arrays; it is not an independent test of IX.

### 4. Relations, boundaries, and orientation

`[3,0,-1]` becomes `[p[3],p[0],-1] = [2,1,-1]`. Both face references change space; the relative sign is retained under the renumbering described by the lesson.

Shuffling the collection of relation entries changes their storage sequence without necessarily changing any relation. Cyclically rotating a boundary changes its chosen starting vertex while preserving winding, for example `[a,b,c] -> [b,c,a]`. Reversing its winding changes the traversal direction, for example `[a,b,c] -> [a,c,b]`. Those operations carry different meanings.

A relation sign interpreted relative to normals requires the orientations and a global direction convention before it can imply global above or below. The bare `-1` cannot supply that information. The lesson describes turnover as flipping orientations and up together, allowing the relative relation representation to remain unchanged; I have not inspected that implementation.

### 5. Transfer, falsification, and turnover limits

Equal aggregate stack height after arbitrary regeneration justifies an aggregate-height observation. With no correspondence map or independent provenance, the identity of the selected material face is unresolved. It does not justify asserting that the original X remains selected.

For a future Godot trial with the supplied map, independently mark the input X face with an observable classroom provenance marker, select input 3, apply renumbering, and inspect the highlighted output material. The mapped selection should be output 2/X. A highlight on output 3/V while the independently marked X is at output 2 would falsify selection retention. The trial needs a functioning adapter and independent observation; no such trial was run here.

According to the lesson, the pinned turnover test checks aggregate ply, ply height, rigid level count, and rigid height. Those assertions leave unproved the claim that each corresponding material face retains its prior level after turnover, or that the same material occupies each numbered level. I did not inspect the linked test.

## Answers to the lesson's five embedded exercises

1. Missing information includes input and output model revisions, transformation, mapping direction, intended input face, compared property, actual result, and expected result. An inspectable question is: "For the lesson's synthetic input and renumbered output, does input 1/B appear at `p[1] = 0` with level 2, and does the viewer highlight that corresponding face rather than output 1/D?" Actual source revisions should accompany a real report.

2. C is input 2 and maps to output `p[2] = 3`. Output click 1 maps back through inverse `[1,3,0,2]` to input 3/D. Keeping integer 2 selects output 2/A and loses the original C selection.

3. For lesson arrays `[0,2,1,3]` and `[2,3,0,1]`, the first raw mismatch is slot 0, where 0 differs from 2. The mapped comparisons are `new[2] = old[0] = 0`, `new[0] = old[1] = 2`, `new[3] = old[2] = 1`, and `new[1] = old[3] = 3`. An inverse check is `q[p[0]] = q[2] = 0` using the lesson's inverse q.

4. A rotated boundary preserves winding but changes its starting point; shuffled relation entries change collection position; a turned-over model changes geometry and orientation context. Calling them all array reordering omits these different effects. The lesson triple maps as `[1,3,1] -> [p[1],p[3],1] = [0,1,1]`.

5. In a future Godot scene, independently mark B, select input 1/B, apply the lesson's synthetic map, and check whether the highlight follows B to output 0. Highlighting output 1/D instead falsifies correct retention. A claim such as "turnover keeps every material face at the same level" exceeds the aggregate assertions reported by the lesson. No Godot scene or turnover experiment was inspected or run in this attempt.

## Fresh two-stage transfer calculation

The initial index space is I, the first output space is A, and the final space is B. The labels in I are `[J,K,L,M,N]`.

The first old-to-new map `p: I -> A` is `[4,2,0,3,1]`:

- J: `0 -> 4`.
- K: `1 -> 2`.
- L: `2 -> 0`.
- M: `3 -> 3`.
- N: `4 -> 1`.

Reading slots of A in order gives `[L,N,K,M,J]`.

The second old-to-new map `q: A -> B` is `[1,4,3,0,2]`. It must be indexed by first-output indices. Therefore the composed old-to-final map is `c[i] = q[p[i]]`, not `p[q[i]]`:

| Original i | Label | First output p[i] | Final q[p[i]] |
|---:|---|---:|---:|
| 0 | J | 4 | 2 |
| 1 | K | 2 | 3 |
| 2 | L | 0 | 1 |
| 3 | M | 3 | 0 |
| 4 | N | 1 | 4 |

Hence `c = [2,3,1,0,4]`. Placing each original label at its c index produces final labels `[M,L,J,K,N]`. Original K reaches final index 3 by `1 -> 2 -> 3`.

Raw equality between p and q is an inappropriate identity-retention test: p accepts original indices, while q accepts first-output indices, so the same numeric position in their array representations refers to different stages. Comparing p with c numerically is possible after acknowledging their different output contexts, but equality is not required for material identity either: they describe destinations after different transformations. The relevant checks are composition with declared domains and `finalLabels[c[i]] == initialLabels[i]` for each original i. Here these give J at 2, K at 3, L at 1, M at 0, and N at 4.

## Confusion, exposure, and evidence boundary

The mathematical tasks were understandable without additional assistance. I named the task inverse r because q is reused for the fresh second transformation. That reuse could otherwise blur an inverse map with a second forward map.

There is a sequencing ambiguity: the task says to give the handout before lesson answer blocks, but this assignment supplied both files for reading, and I read the lesson before answering the task. Consequently this is a lesson-exposed AI dry-run, not an answer-block-blind attempt. My prior competence also prevents attributing successful arithmetic to the lesson alone. The handout's "no learner attempt recorded" status describes the supplied document before this response; I did not alter it.

The phrase "comparing those maps by raw equality" does not specify a pair. I addressed both p versus q and p versus the composition c above. No extra source was consulted to resolve it.

The lesson cites [IX controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [IX thickness tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), and [IX thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). All three links are reproduced from the lesson and were **not inspected** in this attempt. Claims about those sources above are qualified reports of the lesson, not independent source verification. The linked fixture was also not inspected.