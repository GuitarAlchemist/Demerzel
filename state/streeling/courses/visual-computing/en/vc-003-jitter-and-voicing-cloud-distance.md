---
module_id: vc-003-jitter-and-voicing-cloud-distance
department: visual-computing
course: When Does Jitter Help a Voicing Cloud?
level: intermediate
prerequisites: [vc-002-godot-react-bridge-evidence]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-11-003
version: "0.1.0"
---

# When Does Jitter Help a Voicing Cloud?

> **Department of Visual Computing** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you can trace a 3D voicing position through GA's renderer, calculate what its spread control changes, separate overlap visibility from distance evidence, and specify checks that the current source does not perform. You will also know which observations would be needed before recommending a visual setting for real musicians.

## The project question

GA's Prime Radiant can place voicings in a Three.js point cloud. When many marks overlap, a spread control can make individual marks visible. A guitarist then sees two marks far apart and asks whether their voicings are musically far apart. What should the interface say, and which coordinates should an analyst compare?

At pinned GA revision [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), [`VoicingCloud.ts`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/VoicingCloud.ts) fetches a metadata sidecar and a binary position buffer, builds one Three.js `Points` object, colors its points by instrument, and exposes `setSpread` and `setPointSize`. The [Prime Radiant caller](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/ForceRadiant.tsx) attempts to load it when the URL has a `voicings` parameter; `voicings_url` can override the default service URL. This source says what the code would attempt, not that an IX server responded, a binary was valid, or a user saw a frame. The comment's approximate corpus count and dense-knot percentage are not independently measured in this lesson.

## 1. Identify the visual quantities

The loader expects `meta.total` 3D points and exactly `meta.total * 3` floating-point numbers in the binary buffer. Each instrument block supplies a name, an offset into that base buffer, and a count. The renderer copies each block into a sequential destination array, then chooses a color from its guitar, bass, or ukulele map. Unknown names get white. The color is a category label; it does not encode musical distance. The metadata also includes bounds, but this source only checks that `bounds` is truthy. It does not use those bounds to verify every coordinate or automatically set the camera.

`PointsMaterial` starts with size `0.3`, vertex colors, size attenuation, transparency, opacity `0.85`, and depth writing disabled. These are drawing choices. A larger mark may hide more nearby marks, and opacity can change what a dense region looks like. Neither option changes the underlying base positions. The source comments say the default spread is `1.5` and point size is `0.3`; the options in the function confirm those defaults. Thus a default rendered view is already spread unless the caller supplies `spread: 0` or later calls `setSpread(0)`.

For all exercises, use this **fixed synthetic fixture**. It is an arithmetic model of the code path, not an IX payload, browser capture, or measured voicing sample. Assume the metadata shape passes the loader's initial check, all fetches succeed, and `bounds` is `{ min: [0, 0, 0], max: [10, 0, 0] }`.

| Destination point | Instrument block | Base position from the binary |
|---|---|---|
| P0 | `guitar`, offset 0, count 2 | `(0, 0, 0)` |
| P1 | same guitar block | `(0.2, 0, 0)` |
| P2 | `bass`, offset 2, count 1 | `(10, 0, 0)` |

Here `meta.total = 3`; the first block covers source points 0 and 1, and the second covers source point 2. The decimal `0.2` is approximate after storage as a 32-bit float. Coordinates are arbitrary projected/display coordinates in this teaching fixture; they are not pitches, frets, or the full OPTIC-K vector.

### Exercise 1: check the binary length

How many floats must the binary contain for this fixture? What does the pinned loader do if it contains only eight floats while `meta.total` remains three?

> **Answer:** It needs `3 * 3 = 9` floats. Eight fails `basePositions.length !== meta.total * 3`, so `createVoicingCloud` rejects with a size-mismatch error before constructing the point group. The check concerns the total number of floats, not the validity of each instrument block.

## 2. Read the zero-spread reference view

At `spread = 0`, `rebuildGeometry()` copies the base block coordinates and skips its random-number loop. For the fixture, the display-coordinate distance between P0 and P1 is approximately `0.2`, while P1 to P2 is approximately `9.8`. The first two marks have RGB `(0.306, 0.631, 1.000)` for guitar; the third has `(0.482, 0.847, 0.561)` for bass. A later `setSpread(0)` rebuilds from the retained `basePositions`, restoring those coordinates rather than undoing a previous random offset by subtraction.

This zero-spread view is the useful reference when the question is about the positions supplied to this renderer. Even then, a distance in its three coordinates is only a distance in this 3D representation. `VoicingCloud.ts` does not define the source projection or show that Euclidean distance here equals similarity in the full OPTIC-K embedding, perceptual closeness, playability, or voice-leading cost. Those relationships require a separate documented projection and validation. The point cloud can communicate position faithfully only relative to the supplied positions; it cannot by itself establish what the positions mean musically.

### Exercise 2: read the reference geometry

With spread zero, give the three x coordinates, the approximate P0–P1 and P1–P2 distances, and the color assignment. Is this enough to rank the pairs by high-dimensional OPTIC-K similarity?

> **Answer:** The x coordinates are `0`, about `0.2`, and `10`; y and z are zero. The displayed gaps are about `0.2` and `9.8`. P0 and P1 use the guitar RGB `(0.306, 0.631, 1.000)`; P2 uses the bass RGB `(0.482, 0.847, 0.561)`. These facts rank distances in the fixture's 3D coordinates only. They do not establish the ranking of full OPTIC-K similarities.

## 3. Calculate the effect of spread

For each coordinate in each block, the code adds `(Math.random() + Math.random() - 1) * spread` when `spread > 0`. Two independent calls to `Math.random()` make a triangular-shaped offset centered near zero, within approximately `-spread` to `+spread` per axis. The code samples separately for x, y, and z. This is a display transformation; it does not alter `basePositions`. It can reveal separate marks in a pile, but it can also create or reverse apparent gaps between particular points. The source provides no seeded random stream, so repeating a positive `setSpread` call produces a newly sampled arrangement rather than a reproducible layout.

Take **hypothetical draws**, not recorded browser values: with `spread = 1.5`, suppose P0's x draws are `0.1` and `0.1`; P1's x draws are `0.9` and `0.9`. Suppose all y and z draws for both points are `0.5` and `0.5`, yielding zero offsets on those axes. P0 receives `(0.1 + 0.1 - 1) * 1.5 = -1.2`, so its displayed x is `-1.2`. P1 receives `(0.9 + 0.9 - 1) * 1.5 = 1.2`, so its displayed x is approximately `1.4`. Their apparent gap is approximately `2.6`, thirteen times the base gap of `0.2`. No voicing changed. The draws were chosen to expose the arithmetic, not to estimate a typical outcome or claim that a live render produced these points.

An analyst who needs to compare these two projected positions should use the unspread base coordinates, or provide a visibly accessible zero-spread mode. A reader who needs to count or select overlapping marks may benefit from spread. A proposed interface label could say “Spread separates overlapping marks for inspection; visible gaps are jittered.” If a readout displays a pairwise distance, it should state whether that value comes from supplied 3D positions or another defined metric, and it should not silently compute it from jittered screen positions. This is a design recommendation, not a feature verified in the pinned UI.

### Exercise 3: compute a false-looking gap

Using the stated hypothetical draws, calculate P0's and P1's displayed x positions and their gap at spread `1.5`. Can the resulting gap be cited as measured musical dissimilarity?

> **Answer:** P0 moves from `0` to `-1.2`. P1 moves from approximately `0.2` to approximately `1.4`. Their displayed gap is approximately `2.6`, versus about `0.2` before jitter. It is an illustration from invented random draws, so it is neither a measured render nor evidence of musical dissimilarity.

## 4. Separate coordinate and glyph controls

The handle's `setSpread(amount)` updates the spread value and calls `rebuildGeometry()`. That function allocates new position and color arrays, recopies from the original base buffer, and replaces the previous geometry. `setSpread(0)` therefore gives a stable reference for a well-formed fixture. Calling `setSpread(1.5)` again, however, resamples random offsets; it does not keep the same marks in the same jittered places. Selecting a point in one spread arrangement and expecting its screen location to persist after another positive-spread call is unsafe without an identity-aware selection strategy.

By comparison, `setPointSize(size)` assigns the material's size and does not rebuild coordinates. A larger glyph changes visual overlap, but its center remains where the current geometry puts it. The source does not implement a measurement overlay, a seeded spread, a before/after animation, or a distance legend. Those would be possible follow-up designs, each needing a separate behavior check. The pinned caller uses `createVoicingCloud(fg.scene(), { serveUrl })`, so this path uses the function's default spread and point size unless other code later changes them; a source read does not show what happened on any user's screen.

### Exercise 4: predict two controls

After the hypothetical jitter in Exercise 3, what happens to the fixture coordinates if `setSpread(0)` is called? What happens to the coordinates if `setPointSize(0.6)` is then called? Would another `setSpread(1.5)` preserve the previous jitter draws?

> **Answer:** `setSpread(0)` rebuilds from the base buffer, yielding x `0`, approximately `0.2`, and `10`. `setPointSize(0.6)` changes only `PointsMaterial.size`, so those centers stay put. A later positive spread rebuild draws new random values; the source has no seed or stored per-point offsets that would preserve the earlier arrangement.

## 5. Make the data contract reviewable

The current loader checks that `total` is a number, `instruments` is an array, `bounds` is truthy, and the binary has `total * 3` floats. It does not check that `total` is a nonnegative integer; that offsets and counts are nonnegative integers within the buffer; that instrument blocks cover every point exactly once; that names are expected; that coordinates are finite; or that bounds match the positions. The renderer's destination array starts at zero, then fills it as blocks are copied. Missing destination points can consequently remain at zero. A malformed block or binary may throw through typed-array operations or place wrong values; one top-level size check is not a complete payload validator.

For a production data contract, a proposed validator should check the structural and numerical rules before drawing. It should reject missing, overlapping, or out-of-range source coverage; require that the copied destination count equals `total`; check finite coordinates and coherent bounds; and define how unknown instrument names are handled. The project should then test an actual IX payload against that contract and capture a real browser render before claiming coverage or performance. For the visual decision, compare a documented set of tasks—counting dense marks, selecting a specific voicing, and comparing supplied 3D positions—with spread zero and several positive spreads. Record the payload revision, camera, point size, spread, selection accuracy, and participant method. No such user study or runtime benchmark is claimed here.

### Exercise 5: find the missing validation

Keep `meta.total = 3` and a nine-float binary, but change the blocks to `guitar` at offset 0 with count 1 and `bass` at offset 2 with count 1. Under the source's shallow checks, how many destination points are filled? What can happen to the remaining point, and what rule would catch the problem?

> **Answer:** Both the top-level metadata-shape check and nine-float length check can pass. The loop copies two points into destination slots 0 and 1; destination slot 2 remains zero-filled, including its color, because the two counts sum to 2 rather than `total = 3`. A validator requiring valid block ranges and complete, non-overlapping coverage with total copied count 3 would reject this fixture. This is source-based reasoning, not an executed renderer test.

## Key takeaways and limits

- Spread helps expose overlapping marks but changes displayed separations. Use a zero-spread reference for comparisons in the supplied 3D coordinates.
- Point size affects glyphs; spread rebuilds positions with fresh random offsets. Color identifies the instrument category in this implementation.
- A 3D point distance is not automatically a full OPTIC-K, audible, or playable distance. The projection and comparison metric need separate evidence.
- The five exercises use a tiny synthetic fixture and explicitly chosen random draws. They do not measure the actual corpus, visual density, performance, user comprehension, or a live IX service.
- This lesson identifies source checks and proposes stronger validation and task-based observation. It does not claim that those checks or observations have been implemented.

For the neighboring lessons, [VC-001](vc-001-accessible-fretboard-paths.md) addresses accessible interaction paths, and [VC-002](vc-002-godot-react-bridge-evidence.md) examines a different 3D boundary: the React host and proposed Godot bridge. Neither lesson is evidence that this voicing cloud has passed a usability trial. Source inspection was limited to the pinned GA files linked above; it did not run Three.js, IX, or a browser. Human subject review, learner attempts, localization, and publication remain pending.

*Research: `visual-computing-2026-10-11-003`. English draft only; review and publication pending.*
