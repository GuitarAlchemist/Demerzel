---
module_id: vc-006-origami-fold-state-scene-trial
department: visual-computing
course: "Test Fold-State Meaning in a Blender-to-Godot Scene"
level: intermediate
prerequisites: [vc-005-craft-details-through-blender-to-godot]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-12-006
version: "0.1.0"
---

# Test Fold-State Meaning in a Blender-to-Godot Scene

> **Department of Visual Computing** | Intermediate | 40 minutes | English draft; no folded asset, Godot import, learner trial, human review, or publication

## Objectives and project question

After this lesson, you can specify a small folded-surface scene trial, distinguish geometry from material and fold semantics, diagnose a lost fold-state cue, and write criteria that could reject an attractive but misleading asset. **Project question:** could a foldable governance panel in GA's proposed Godot observatory show two distinct policy states while preserving the state a learner can identify? This is a test design. It does not assert that an origami object, fold-state DSL, or working Godot scene exists.

The pinned GA [Godot integration plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md) sketches a constitutional-gravity scene and screenshot feedback work as unchecked items. The pinned [React Godot host](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/GodotScene.tsx) declares an iframe and message handling; it is not evidence of an exported scene. [VC-004](vc-004-godot-observatory-capture-gate.md) proposes a repeatable capture gate, and [VC-005](vc-005-craft-details-through-blender-to-godot.md) treats preservation of small craft details during GLB cleanup. Here the central problem is different: a visible ridge might survive while the *identity, direction, or policy meaning* of its fold is lost.

## 1. Define the fold-state contract before modeling

Use a deliberately small **synthetic fixture**: three labeled panels A, B, and C with two hinges. Crease `e1` joins A to B; crease `e2` joins B to C. An external trial manifest assigns each crease an ID, incident panel IDs, a state, and a semantic label. In the example, state `closed` means `e1` is a mountain fold and `e2` is a valley fold; state `open` means both panels have returned to a declared near-flat pose. The words mountain and valley name the fixture's signed orientation, not a universal reading of an arbitrary mesh. Fix face winding, crease direction, a viewing side, and a sign convention in the manifest before recording angles. Otherwise reversing the view or normals could invert the label without moving any vertices.

For the proposed observatory, give `closed` the trial meaning “a policy dependency is withheld” and `open` the trial meaning “the dependency is available.” These are invented interface meanings, not claims about an existing governance protocol or a historical origami tradition. Keep the manifest outside the exported mesh and map its stable crease IDs to scene objects after import. An asset that renders two attractive poses but has no recoverable `e1`/`e2` mapping cannot satisfy this trial's interaction requirement.

### Exercise 1: find the missing contract

A modeler hands over two screenshots labeled `open` and `closed`, plus a GLB. The GLB has a visible ridge, but no crease IDs or panel adjacency record. Can a reviewer verify that `e1` changed state and still represents the policy dependency?

> **Answer:** No. The images can support a visual difference, but they do not identify which edge is `e1`, which panels it joins, or which policy state that edge means. Add a versioned external manifest with panel and crease IDs, adjacency, signed-angle convention, state-to-meaning mapping, and the GLB and scene hashes. Then test the mapping after import with an intentional selection or state change. A ridge alone is not a semantic receipt.

## 2. Separate geometric, material, and semantic evidence

**Geometry** includes vertices, faces, panel adjacency, silhouette, thickness, normals, and the measured pose. Learn's pinned [modeling script](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/scripts/l02_modeling.py) constructs a one-quad open plane and a three-quad example sharing an edge; its [checked-in report](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/expected/l02_modeling.txt) records boundary and non-manifold edges. Those examples demonstrate how to inspect topology, not that a particular folded asset is valid. A sheet intentionally has boundary edges; requiring zero boundary edges would wrongly reject it. Conversely, a non-manifold hinge or disconnected duplicate face needs investigation even if a single render looks smooth.

**Material** includes base color, texture, UV layout, roughness, and shading. Learn's pinned [material and glTF script](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/scripts/l03_materials.py) and [reference report](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/expected/l03_materials.txt) show UV coordinates on face corners and inspect an exported glTF's mesh attributes and material values. They do not test our proposed folded panel. A dark painted line can signal a crease visually while the geometry remains flat; a geometric ridge can remain after a texture or UV is lost. Capture those as separate observations.

**Fold semantics** include `e1` and `e2`, panel ordering, mountain/valley state under the declared convention, allowed transitions, and the assigned governance meaning. A GLB render or triangle count does not establish these. Store the semantics in a sidecar for the trial, then verify the Godot scene binds the intended object IDs to the intended state transition. This sidecar is a proposed fixture, not an implemented schema or deployment format.

### Exercise 2: classify three observations

In a hypothetical import, (a) the silhouette bends at the expected location, (b) a blue line marks the crease but disappears after a material change, and (c) clicking the rendered `e1` object produces the `e2` policy label. Which layer does each observation test, and which one fails the trial?

> **Answer:** (a) is geometric evidence, although it does not by itself prove crease identity. (b) is material evidence; its disappearance shows the visual cue is vulnerable to a material change. (c) tests the scene's semantic binding and fails because `e1` selects the `e2` label. Fix the object-ID mapping and repeat the interaction trace; repairing the shader alone would not correct that error.

## 3. Make the pose measurable without making the angle the meaning

For a trial, record each panel's source transform and the two hinge poses in Blender, export one frozen state at a time, and record the intended signed fold angle in the external manifest. An angle can be calculated from consistently oriented panel normals around a directed crease; without that orientation it is only an unsigned bend magnitude. Define a synthetic target of `+60°` for `e1` and `−60°` for `e2` in `closed`, and within `±5°` of flat for each in `open`. These numbers are classroom tolerances, not measured Godot behavior or a paper-folding standard. The manifest should also record unit scale, export settings, coordinate convention, and panel/crease object names. If an export applies transforms or changes axis convention, the scene adapter must preserve the declared sign mapping explicitly.

Before trying animation, compare static snapshots. Import source and candidate GLBs into the same versioned Godot scene at the same scale and camera. Save import logs, object-name mapping, raw panel and fullscreen captures, and an interaction trace for both states. Inspect front and back views: a material-only line may disappear from the back, and a fold may hide a panel from one camera. A future animation test would need intermediate states and self-intersection checks; two endpoints do not certify a physically achievable folding motion.

### Exercise 3: score a synthetic pose

Under the fixture's declared sign convention, a candidate `closed` import measures `e1 = +58°` and `e2 = +61°`. The tolerance is five degrees around each target. Which hinge passes, and why is a clear screenshot insufficient to approve the state?

> **Answer:** `e1` passes because `|58 − 60| = 2°`. `e2` fails because `|61 − (−60)| = 121°`; the magnitude resembles the target but the sign is reversed. Check the face winding and scene mapping before deciding whether the geometry or measurement convention caused it. A screenshot from one side can hide the sign error and says nothing about the `e2` policy label.

## 4. Compare one feature at a time in the observatory

Set up a baseline that uses a static flat panel and a plain text state label. It is a simpler interface, and it may prove clearer than a folded form. The folded candidate earns a place only if users can identify the two states and intended dependency at least as reliably under the same task, while staying within an agreed scene cost. Keep the governance-data snapshot, labels, viewport, renderer, lighting, camera, build, and input sequence fixed. For geometry comparison, vary the fold mesh while holding material cues fixed. For material comparison, use the same mesh and pose while changing the crease cue. For semantic binding, inject the same named state transition and inspect the selected crease ID and resulting policy label. Do not treat one combined screenshot as evidence for all three.

Use VC-004's proposed repeated raw captures and click trace as controls. Predeclare the small trial: three repeated captures of each state in panel and fullscreen; no missing object IDs; no import error; geometric angles within the stated tolerance; and intentional clicks on both `e1` and `e2` in each pose yielding each crease's declared ID, state, and policy label in every trace. For an initial comprehension task, ask four reviewers to choose `open` or `closed` and name the dependency without answer overlays. Require at least the flat-text baseline's correct count, not a universal percentage derived from four people. Keep individual answers and misses. Record triangle count and frame-time distribution on the same device, but choose a cost ceiling from an actual baseline measurement before using it as an acceptance gate. No measurements of this proposed trial were made for this lesson.

### Exercise 4: isolate the cause

Candidate X uses a new fold mesh, new blue crease texture, new camera, and a revised policy label. Four reviewers identify its `closed` state. The flat-text baseline gets three. Does this establish that folded geometry improved comprehension? Design the next comparison.

> **Answer:** No. Geometry, material, camera, and wording changed together, and four observations are too few for a broad claim. Restore the baseline camera and label, hold the crease material fixed, and compare the flat and folded geometry under the same task. Next vary the material cue with geometry fixed. Store per-reviewer responses and raw captures; report the small trial as a local result only if it is actually run.

## 5. Decide whether the fold belongs in a composable scene language

The simplest viable implementation is a Blender asset, a small external manifest, and an explicit Godot object-ID mapping reviewed against raw captures and clicks. A future composable scene description might declare `panel`, `crease`, `adjacent_to`, `signed_pose`, `state`, and `meaning`. It should not be adopted merely because the words compose on paper. The strongest counterargument is that a flat panel plus text conveys the same governance state with less modeling, import, accessibility, and maintenance work. Hidden costs include authoring and validating stable crease IDs, preserving sign across coordinate conversions, maintaining front/back cues, and translating labels independently of geometry. A proposed language would need to reduce observed mistakes or review time relative to the manifest and checklist.

**Accept the trial candidate** only after a versioned Godot import and raw evidence show correct IDs and state bindings, angles within tolerance, no missing panel, task comprehension at least as good as baseline, and a measured cost within a predeclared budget. **Reject or revise it** if a sign inversion or wrong label passes visual review, if comprehension falls below baseline, if the object-ID mapping cannot be replayed, or if performance exceeds the agreed ceiling. If no scene/export is available, mark the candidate **not assessed**, not accepted. A fold-state DSL remains an advisory hypothesis until a controlled comparison beats the simpler manifest path.

### Exercise 5: apply the decision rule

Suppose a future candidate has complete hashes and captures, angles `+60°` and `−59°`, and acceptable measured frame time. Three of four reviewers identify the dependency, versus four of four for flat text. Its `e1` click also returns the `e2` label once in ten replays. What decision follows, and what receipts are needed?

> **Answer:** Reject or revise this candidate under the declared trial rule. The angle check and cost pass, but comprehension is below the baseline and the `e1` binding is wrong in one replay. Keep the source and output GLB hashes, scene revision, sidecar manifest, import logs, raw captures, ten event traces, individual task answers, and frame-time samples. Fix the binding and visual explanation, then rerun the same comparison. The invented figures are an exercise fixture, not a project measurement.

## Evidence and limits

- The linked GA plan and host establish a proposed viewing path; they do not establish a running folded observatory. The linked Learn scripts and reports establish modeling, topology, UV, and glTF examples on other assets; they do not validate this fixture.
- All fold angles, reviewer counts, scene outcomes, and policy meanings in the exercises are synthetic. No Blender or Godot run, cultural analysis, human review, learner attempt, translation, or public readback is claimed.
- VC-005's cleanup threshold can matter later, but preserving triangles alone cannot preserve a fold's ID, sign, and meaning. This course keeps those checks separate.
