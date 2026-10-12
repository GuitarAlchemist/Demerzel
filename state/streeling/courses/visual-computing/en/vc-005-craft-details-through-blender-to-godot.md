---
module_id: vc-005-craft-details-through-blender-to-godot
department: visual-computing
course: "Keep Craft Details through a Blender-to-Godot Asset Trial"
level: intermediate
prerequisites: [vc-004-godot-observatory-capture-gate]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-12-005
version: "0.1.0"
---

# Keep Craft Details through a Blender-to-Godot Asset Trial

> **Department of Visual Computing** | Intermediate | 40 minutes | English draft; no Godot import, human review, learner trial, or publication

## Objectives and project question

After this lesson, you can distinguish a craft feature from disposable mesh noise, predict two cleanup losses from a pinned Blender pipeline, design a reversible asset comparison for a Godot observatory, and specify evidence that would reject an automated cleanup rule. **Project question:** if a woven knot, folded paper ridge, or chased metal mark carries meaning in a governance object, can a cleanup pipeline make the asset cheaper without erasing that meaning? This is an asset-trial design, not a claim that those crafts or the Godot scene have already been implemented.

## 1. Start with a real pipeline and a proposed scene

The pinned Learn [GLB cleanup script](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/scripts/glb_pipeline.py) imports a `.glb`, joins mesh objects, merges nearby vertices, removes connected parts below a face-fraction threshold, recalculates normals, optionally voxel-remeshes, decimates toward a triangle budget, exports a clean `.glb`, then imports it again for a report. Its docstring targets three.js. The [sample checker](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/scripts/pipeline_check.py) constructs a flawed guitar-pick mesh and runs the pipeline twice, once with voxel remesh. Its [expected report](https://github.com/spareilleux/learn/blob/93d424f872a576ba8bbcd3dd44c9733292373654/code/blender/expected/pipeline_check.txt) is a checked-in reference result, not a new execution for this lesson.

The earlier [VC-004 capture lesson](vc-004-godot-observatory-capture-gate.md) specifies a proposed image and interaction gate for the Godot observatory. This course asks whether craft-derived geometry could be introduced as a versioned asset in that future scene. The Learn script does not prove Godot compatibility. A Godot import, scene capture, and task comparison remain separate experiments.

### Exercise 1: name the evidence boundary

A colleague says, “The Learn cleanup report proves our woven node is safe in Godot.” Which part is supported, and what is still missing?

> **Answer:** The source and expected report show that a sample guitar-pick mesh can be processed under declared Blender settings. They do not contain a woven-node asset or a Godot import. To test the claim, version the candidate `.glb`, record its source and cleanup settings, import it into a versioned Godot scene, capture the intended views, and run a feature-recognition task against a baseline. The checked-in report alone cannot certify that a knot remains recognizable.

## 2. Model a feature before simplifying it

A craft detail must have a declared **role**. For a hypothetical woven governance node, a small knot might indicate an authority boundary; for an origami panel, one fold ridge might distinguish an open from a closed state; for chased metal, a shallow mark might identify a material or provenance. Treat these as candidate semantic features, not as decoration by default. Give each feature an ID, a short meaning, the mesh region or material it occupies, and one camera view where a learner should identify it. Keep this feature manifest outside the current cleanup script: the script's object-join and connected-part cleanup do not carry such an approval contract.

The pipeline's `--min-part` default is `0.01`: a connected part with **fewer** than one percent of all faces is removed. In the pinned sample's expected report, the imported model has 5,140 faces and the cleanup removes one 20-face part. That is sensible for the checker's deliberately floating blob, but it would be a semantic loss if the 20-face part were an intentional knot. The threshold is a topology rule, not a craft-meaning test. Marking an element “important” in prose does not change the current code.

### Exercise 2: apply the actual comparison

Take a **synthetic** 5,140-face asset with an isolated 20-face authority knot. At `--min-part 0.01`, is the knot removed? What is the least risky first comparison?

> **Answer:** One percent is 51.4 faces, and `20 < 51.4`, so the current rule would remove that connected part. Compare an unmodified source export with a cleanup run using `--min-part 0.001`: the threshold becomes 5.14 faces, so an isolated 20-face component is retained by this rule. Hold the other settings fixed and check both mesh reports and the rendered knot view. Keeping smaller parts may retain noise, so this is diagnostic rather than a final production policy. The pinned script's `--min-part 0` path returns an empty list where its caller expects a pair, so zero is not a valid bypass in that revision. A [draft Learn fix](https://github.com/spareilleux/learn/pull/168) corrects the return shape but has not been through a Blender run on this host. If the knot touches a larger component, this particular connected-part rule may not remove it; recognition can still fail after decimation or shading changes.

## 3. Keep geometry, material, and meaning distinct

The expected report provides a second warning. In its non-remesh path, the cleaned sample reports one UV layer and zero boundary edges before export; after export and reimport, it reports 186 boundary edges, then zero after vertices are merged by position. The script comments that glTF may split a vertex at normal or UV seams. This means a raw reimported boundary-edge count alone is not proof of a physical hole. Preserve both the raw and position-merged reports, and inspect the rendered surface where a seam matters. The sample says nothing about whether a woven pattern's thread direction or a metal finish remains legible.

In the sample's voxel-remesh path, the expected report changes UV from one layer before cleanup to `none` afterward. That may be acceptable for plain geometry, but a pattern encoded in a UV texture cannot be assumed to survive. A different material name in the report would also be only a structural signal; lighting, normal direction, color space, and viewing distance affect perception. A closed manifold mesh can still communicate the wrong craft feature.

### Exercise 3: read the report without overclaiming

After reimport, a model reports 186 boundary edges; after a position merge, it reports zero. Does this alone establish a damaged mesh? The voxel-remesh variant reports `uv: none`; what does that tell you about a UV-encoded woven pattern?

> **Answer:** No. Split vertices at export seams can produce the first count, and the second count argues against treating it as a proven hole. Inspect the source and rendered seam before deciding. `uv: none` shows that the tested remesh path did not preserve a UV layer in the reference sample. A pattern relying on that layer needs a separate preservation or rebaking step and visual check; the report does not prove how a different craft asset will look.

## 4. Compose a bounded Blender-to-Godot trial

Choose one craft feature and one target use in the observatory before generating many assets. Save the input `.glb` and a manifest containing the source SHA, object and feature IDs, intended dimensions, cleanup arguments, triangle count, UV/material report, output hash, and the expected viewing task. Produce baseline and candidate assets from that same input. A first candidate changes only `--min-part`; another candidate can vary decimation, with the first setting fixed. Do not change cleanup, camera, light, and upscaler together and then attribute a perceived improvement to craft modeling.

For a Godot trial, import each version into the same scene and capture the same camera, renderer, viewport, lights, and governance-data snapshot. Record import errors, asset scale, raw images, frame-time distribution, and whether reviewers identify the declared feature and its meaning without an answer overlay. The manifest and raw captures make a rejection reviewable. VC-004's proposed safe-zone and repeatability checks are useful capture controls, not proof of craft legibility. The user-requested forked DLSS path would require a separate supported build, render-resolution record, and performance/quality comparison; this lesson has no such run.

### Exercise 4: isolate a variable

Candidate A uses `--min-part 0.001`, 2,000 target triangles, and the baseline camera. Candidate B uses `--min-part 0.01`, 1,000 triangles, a new camera, and new lighting. B looks clearer in one screenshot. Which claim can you defend, and what comparison should follow?

> **Answer:** You can report only that this one combined B image looked clearer under changed settings. You cannot attribute the result to the face threshold or triangle budget. First compare baseline and A with the same camera, light, and render conditions to test the small-part decision. Then change one additional variable at a time. Preserve raw captures and a feature-identification result, because attractive shading can hide an absent knot.

## 5. Decide whether a reusable craft rule is warranted

A possible future craft DSL could describe `feature`, `meaning`, `source_region`, `preservation_check`, and `target_scene` as composable declarations. It would be useful only if those declarations survive export/import and lead to fewer lost features or faster review than a plain manifest plus manual checklist. The current Learn script and Godot plan do not implement this DSL. The simplest baseline is the existing GLB pipeline, one external feature manifest, and human before/after review.

Predeclare a small benchmark: several versioned assets with known retained and deliberately removable details, the same views and observers, and a bounded triangle/frame-time budget. Reject an automated preservation gate if it passes a missing semantic feature, blocks useful simplification more often than the checklist, or requires annotations that authors cannot maintain. Do not make a one-way schema or public API change from an appealing analogy alone.

### Exercise 5: reject the wrong optimization

A candidate meets the triangle budget and has no import error, but three of four reviewers cannot identify the intended authority knot; the baseline has four of four correct. Is the candidate ready for the observatory? What evidence should be stored?

> **Answer:** No under this trial's declared meaning-preservation goal. Save both asset hashes, cleanup manifests, reports, same-view raw captures, reviewer responses, and the performance results. A lower triangle count is a real geometric improvement but does not outweigh the observed semantic loss. Revisit the knot geometry or texture and rerun the controlled comparison. Four reviewers are a small trial, not a general population estimate.

## Evidence and limits

- The pinned Learn source and checked-in sample report support the pipeline operations and sample numbers above. Source inspection of the current Learn main also confirmed the zero-filter return-shape defect; draft PR #168 proposes its one-line fix, verified only by a focused source-level call here. No Blender or Godot process was run for this course; the craft examples and reviewer outcomes are explicit hypotheticals.
- The pipeline currently targets three.js and joins meshes; a Godot import, feature-ID preservation, craft DSL, and forked DLSS comparison are proposed follow-up work.
- This English draft still needs independent subject review, a learner attempt, translation and fluent review, Learn generation/build, and anonymous public readback before publication.
