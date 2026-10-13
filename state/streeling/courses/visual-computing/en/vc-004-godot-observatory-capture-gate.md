---
module_id: vc-004-godot-observatory-capture-gate
department: visual-computing
course: A Capture Gate for the Godot Observatory
level: intermediate
prerequisites: [vc-002-godot-react-bridge-evidence]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-11-004
version: "0.1.0"
---

# A Capture Gate for the Godot Observatory

> **Department of Visual Computing** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you can state which parts of GA's Godot observatory are source-supported, specify a repeatable before-and-after capture for a camera-framing change, calculate a visual safe-zone and repeatability check, and make a bounded acceptance decision that includes both images and interaction traces.

## The project question

A designer proposes moving the observatory camera so the central governance structure and policy nodes read more clearly. A screenshot looks better on their machine. Is that enough to replace the baseline camera? What must a reviewer capture, measure, and preserve so the decision can be checked later?

The pinned GA [Godot integration plan at `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md) proposes a constitutional-gravity scene with orbiting policy nodes in `Apps/ga-godot/` (Phase 2), a web export (Phase 4), and a screenshot-to-critic loop (Phase 5). Each of those tasks is **unchecked** in the pinned plan. The [React `GodotScene.tsx` host](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/PrimeRadiant/GodotScene.tsx) declares panel and fullscreen modes, defaults its iframe URL to `/godot/index.html`, and handles `godot:ready` and `godot:node-clicked` messages. Those declarations support a future viewing and interaction path, not an observed rendered scene or an existing capture pipeline. The plan lives under `docs/plans/parked/` despite its older “active” header; neither label proves runtime availability.

The inspected GA commit has no verified Godot `.tscn` scene, web export, or capture result for this lesson. A separate local prototype without a versioned source commit would not provide a stable course citation, so it is not evidence for the numbers below. This lesson designs an evaluation **before** such a scene change can be approved. Every coordinate, count, and result in the exercise fixture is synthetic. No Godot, browser, screenshot critic, or upscaler was run here.

## 1. Name the change and freeze its controls

A fair comparison needs one declared independent variable. In this lesson it is the **camera framing** of a future Godot scene. Keep the scene contents, governance-data snapshot, node IDs, viewport, display scale, renderer, lighting, quality settings, and build revision fixed while capturing baseline and candidate camera poses. Record each pose as position, rotation, field of view or projection setting, and target. If the scene animates, freeze a named time or frame and disable any uncontrolled random seed. A comparison of two captures that changed both camera and lighting cannot isolate which change made an edge easier to see. If the intended experiment is instead a lighting, render-mode, or upscaling change, hold the camera fixed and record that variable explicitly. Upscaling comparisons must also record internal render resolution and output resolution; a large image alone does not show the scene was rendered at the same cost.

For a future run, one capture manifest should name the GA commit, Godot project commit, exported build hash, scene/data snapshot, renderer and Godot version, camera pose, viewport and device scale, frame/time, and capture-command version. Give each PNG a manifest row, a timestamp, and a content hash. Capture the React **panel** and **fullscreen** modes separately because the host declares both; select the panel's Viewer tab, since its initial Builder tab does not mount the iframe. Do not assume either mode currently loads a Godot export. The proposed capture harness should save raw PNGs and a machine-readable manifest; a curated montage is useful for discussion but cannot replace the original frames. A human reviewer can then inspect a declared change against a stable reference instead of relying on recollection.

### Exercise 1: sort the evidence

Classify these statements as **source-supported**, **planned**, or **requires a run**: (a) the host declares an iframe defaulting to `/godot/index.html`; (b) the constitutional-gravity scene has been captured three times in the same browser; (c) the pinned plan includes a screenshot-to-critic loop; (d) a new camera pose improves node readability.

> **Answer:** (a) is source-supported by `GodotScene.tsx`. (c) is planned in unchecked Phase 5. (b) requires a real export, browser, and three saved captures; none was observed here. (d) requires a defined readability task and comparison data. A plan entry or iframe source string does not satisfy those observations.

## 2. Use images to test a visual claim

Suppose the future scene has three known target nodes, named A, B, and C, visible from three named viewpoints. A camera candidate should preserve the target marks inside a **safe rectangle** that leaves five percent of the output width and height at each edge. This five-percent margin is a proposed project threshold, not a Godot default or an accessibility standard. At 1280 × 720 pixels, the safe x interval is `[64, 1216]` and the safe y interval is `[36, 684]`. A target's entire annotated bounding box must fit inside, not merely its center. The annotation should include the target ID and the rectangle coordinates in the raw output PNG. For each named viewpoint, capture three repeat frames under the same manifest values and compute the largest coordinate change of each box edge across repeats. Require at most **two pixels** of drift. That is a proposed repeatability threshold, not a measurement of this project.

The safe-zone check catches clipping and edge crowding; it does not establish that a label is legible, a color is distinguishable, or depth cues are honest. A proposed human task is to identify A, B, and C without the answer overlay, with the overlay used only to score the result. Record misses and reasons, then compare candidate and baseline under the same task and viewing conditions. A screenshot critic can flag suspicious crops or unreadable labels, but its score needs calibration against these task outcomes before it becomes a gate. A pixel-difference threshold between baseline and candidate would be inappropriate for an intentional camera move: difference proves change, not improvement. Use repeat-frame differences to test capture stability, and task outcomes to test usefulness.

### Exercise 2: control the comparison

Two captures have the same node data and output size, but the candidate changes both camera pose and lighting, while its PNG lacks a build hash. Can the pair isolate the camera's effect? Name the minimum repairs.

> **Answer:** No. Pin the scene/export build and data snapshot, record the build hash and camera settings, and hold lighting and the other rendering controls fixed for the camera comparison. Save the raw images and manifest. Evaluate lighting in a separate comparison with the camera held fixed. Without those controls, a clearer node might be due to either change or an unknown build.

### Exercise 3: calculate the safe zone

In a **synthetic** 1280 × 720 output, candidate boxes are A `(80, 50)–(180, 130)`, B `(60, 50)–(160, 130)`, and C `(90, 40)–(190, 120)`. Which satisfy the proposed five-percent safe-zone rule, and what is the smallest horizontal shift that would bring B's left edge inside it?

> **Answer:** The safe bounds are x `64–1216` and y `36–684`. A and C fit. B fails because its left edge is `60 < 64`; a rightward shift of at least four pixels would put that edge at 64. A real camera shift may move all marks, so all three boxes would need fresh captures and checks. This arithmetic is not a report from a Godot image.

## 3. Check repeatability before judging improvement

Identical capture settings should produce comparable frames. For static targets, calculate box-edge drift from each set of three repetitions; preserve all three images rather than picking the best one. If the scene has intentional motion, define a fixed simulation step or compare a stable landmark instead. If that cannot be controlled, report a distribution over repeated captures rather than claiming pixel repeatability. Also record load and frame behavior: a visual setting that improves framing but makes the web export unusable cannot pass the complete gate. Frame time should be measured on the same device and browser over a specified run, with median and tail values, rather than inferred from image size or visual smoothness in a recording. This lesson does not set an unmeasured performance budget for the future export.

The React host's ready callback can help a future harness know when the iframe reports readiness, but the pinned handler accepts repeated ready messages and does not prove a rendered frame. Its message source comparison applies when the iframe ref exists; the handler does not validate origin or `nodeId` at runtime. As [VC-002](vc-002-godot-react-bridge-evidence.md) details, a future scene check should record an actual frame and intentional node clicks, not just a vanished loading spinner. Visual and interaction evidence are separate columns in the gate.

### Exercise 4: test capture repeatability

For one target's left box edge, three **synthetic** repeat captures report x coordinates `80`, `81`, and `84`. Does this meet the proposed two-pixel maximum drift? What should the reviewer do before comparing its visual quality with the baseline?

> **Answer:** No. The maximum minus minimum is `84 − 80 = 4` pixels, exceeding two. Keep all three PNGs, check whether the camera, viewport, scene time, animation, and data were actually fixed, and recapture after the uncontrolled cause is identified. Selecting only the x = 80 image would hide instability.

## 4. Write a gate that can refuse a pretty screenshot

A proposed acceptance gate for a future, versioned Godot export has ordered stages. First, establish build provenance, a served export, a ready event **and** a captured rendered frame; otherwise the visual comparison is **not assessable**. Second, collect baseline and candidate raw PNGs for panel and fullscreen at named views, three repeats each, with complete manifests. Third, require every known target box to fit the safe rectangle and each static target's repeat drift to stay at or below two pixels. Fourth, run an identification task on the same known IDs and require the candidate to be no worse than baseline. Fifth, in a dedicated mounted-iframe test host, require **20/20 known intentional clicks** delivered to the expected React IDs in order and **zero** callbacks from injected foreign-source messages. The last threshold is a proposed check after a real export exists, not a result of this lesson; a product host that closes or switches view on a click needs a separate reentry trace. Record failures as well as passes and keep the raw event log alongside the images.

This gate is deliberately conjunctive: one failed stage blocks the decision. It does not certify artistic quality or accessibility. [VC-001](vc-001-accessible-fretboard-paths.md) supplies a distinct requirement to preserve keyboard and screen-reader access. A rendering-mode or upscaling proposal would also need its own device matrix and measured frame-time budget; the pinned GA sources do not demonstrate forked DLSS, a particular renderer, or an upscaler. A camera change approved on a synthetic table would be a category error. The table below exists only to practice the gate's logic.

| Hypothetical candidate | Build, ready, rendered frame, raw captures | Safe boxes and repeat drift | Identification vs baseline | Dedicated click trace |
|---|---|---|---|---|
| X | Complete | B left edge 60; drift 4 px | Equal | 20/20; foreign 0 |
| Y | Complete | All safe; drift 2 px | Equal | 19/20; foreign 0 |
| Z | Complete | All safe; drift 2 px | Equal | 20/20; foreign 0 |

### Exercise 5: decide without cherry-picking

Apply the stated gate to X, Y, and Z. Which hypothetical candidate passes the **fixture's** checks? What further evidence is needed before declaring a real observatory camera change accepted?

> **Answer:** X fails the safe-zone and repeatability checks despite its perfect click trace. Y fails the 20/20 click requirement despite acceptable images. Z passes every listed synthetic gate column. None is an observed Godot result. A real decision still needs a versioned scene/export, repeatable raw screenshots and manifests, actual task results and event traces, review of accessibility and visual meaning, and any agreed device-performance threshold.

## Key takeaways and evidence limits

- A pinned plan can motivate a capture protocol without proving that the planned scene, export, or critic runs.
- For a camera comparison, vary the camera and hold scene, data, renderer, lighting, viewport, and capture timing fixed. Record the inputs and preserve raw images.
- Safe-zone and drift arithmetic make a capture reviewable; task success and click traces answer different questions. A single attractive screenshot cannot substitute for them.
- The five exercises use invented boxes and outcomes. Thresholds of five percent, two pixels, and 20/20 clicks are proposed acceptance criteria, not measured GA baselines.
- No live Godot capture, IX/Gaia data feed, upscaling benchmark, human subject review, learner trial, localization, or publication is claimed here.

*Research: `visual-computing-2026-10-11-004`. English draft only; review and publication pending.*
