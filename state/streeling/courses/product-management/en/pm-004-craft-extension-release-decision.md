---
module_id: pm-004-craft-extension-release-decision
department: product-management
course: "Decide When Craft Extensions Are Ready for a Release"
level: intermediate
prerequisites: [pm-002-release-evidence-gate, pm-003-review-queue-flow-metrics]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: product-management-2026-10-12-004
version: "0.1.0"
---

# Decide When Craft Extensions Are Ready for a Release

> **Department of Product and Project Management** | Intermediate | 35 minutes | English source draft; no extension release, human review, learner trial, or public course publication

## Objectives and project question

After this lesson, you can name the product task served by a craft extension, distinguish a useful source component from an installable extension, apply a non-compensating release gate across three targets, and write a release decision that a second person can reproduce. **Project question:** when can the team truthfully release ComfyUI, Blender, and Godot extensions arising from its guitar-audio and craft-to-scene experiments? For this project, a release claim requires a versioned, installable distribution with named artifacts and notes; a tag alone is insufficient. A roadmap, draft course, source script, local experiment, or passing classroom fixture is not one.

[PM-002](pm-002-release-evidence-gate.md) separates a Streeling course's review, build, and public-readback gates. [PM-003](pm-003-review-queue-flow-metrics.md) measures movement through that course review queue. This lesson makes a different decision: whether a **software extension** can be offered to users. The course itself still has its own independent review and publication gates.

## 1. Choose one user task per extension

An extension proposal must name what a user can install and do. A possible **ComfyUI** target is an offline guitar-audio workflow that takes a baseline WAV and yields a candidate plus provenance. A possible **Blender** target is a craft-feature cleanup aid that carries a declared feature identity through mesh processing. A possible **Godot** target is a scene importer or inspector that preserves the identity and over/under meaning of a woven crossing. These are *candidate product tasks*, not claims that the three installable extensions exist.

The project already has narrower evidence. The pinned [CS-004 audio-loop lesson](https://github.com/GuitarAlchemist/Demerzel/blob/861b6b1891ef7017c22269d5ec6be4c50953040c/state/streeling/courses/computer-science/en/cs-004-composable-agentic-audio-loop.md) describes a local, unmerged GA ComfyUI bridge at `6fac5735f7ffbb4116ebee05cfc9d7911bb12ce9`; its supplied workflow loads and saves audio but demonstrates no improvement. The pinned [VC-005 craft lesson](https://github.com/GuitarAlchemist/Demerzel/blob/861b6b1891ef7017c22269d5ec6be4c50953040c/state/streeling/courses/visual-computing/en/vc-005-craft-details-through-blender-to-godot.md) cites Learn's Blender GLB cleanup script and checked-in sample report at `93d424f872a576ba8bbcd3dd44c9733292373654`, but reports no Godot import or craft-feature trial. The pinned [VC-007 weave lesson](https://github.com/GuitarAlchemist/Demerzel/blob/861b6b1891ef7017c22269d5ec6be4c50953040c/state/streeling/courses/visual-computing/en/vc-007-weave-seams-as-scene-contracts.md) has a synthetic Python evaluator: global parity yields zero adjacent-crossing violations and restarted local parity yields twelve. That is a semantic counterexample, not a Godot extension. GA's [parked Godot plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md) sketches a scene path; its unchecked items are plans.

### Exercise 1: write the user promise

A draft announcement says, “Our ComfyUI, Blender, and Godot craft suite is ready because the audio bridge, GLB script, and weave validator exist.” Repair the statement into one truthful present-tense sentence and one falsifiable proposed task.

> **Answer:** “The project has source-level audio, mesh-cleanup, and weave-validation experiments, with different provenance and no demonstrated three-target extension release.” A falsifiable proposed task is: “A user installs the versioned Godot add-on, imports the supplied woven sample, clicks `w3-f0`, and receives that crossing's declared over/under value in a saved trace.” The latter needs an installable add-on and runtime receipt before it can be stated as an achieved result.

## 2. Require evidence at every target boundary

For each target, collect four kinds of evidence. **Implementation** is a versioned, installable extension package with setup and compatibility instructions. **Runtime** is a fresh test in the named application version on a pinned input, with commands, logs, and output hashes. **Meaning** is a task-specific oracle: for audio, a matched candidate compared with the same reference and a listening task; for Blender, survival of an identified craft feature after cleanup; for Godot, stable crossing ID and over/under mapping in the scene and click trace. **Human review** asks a domain reviewer to inspect the actual artifact and an uncoached user to perform the task. A passing schema or unit test cannot replace those observations.

The bundle also needs a **contract replay** across boundaries: the output identity and hash from one tool must be the input identity and hash at the next, with no unexplained substitution. Save artifact hashes for all three packages and their trial inputs and outputs. Exact versions matter because a script examined at one commit does not prove an extension works in a later application build. Record accessibility, licensing, platform compatibility, and installation behavior in a real release checklist; the classroom fixture below does not evaluate them.

### Exercise 2: classify the pinned evidence

Which of the four target columns can be marked complete for a three-extension release using only the pinned sources above? Does Learn's checked-in Blender sample report prove that a craft feature survived in a Godot scene?

> **Answer:** None of the four columns is complete for an **installable three-extension release** from those cited sources. They support source inspection and some narrower synthetic or checked-in sample checks. The Blender report concerns a sample cleanup path, not an installed Blender extension with a craft-feature verdict; it contains no Godot scene import. Keep the bundle decision on hold and name the missing target-specific trials.

## 3. Use hard gates before ranking improvements

The [release-card fixture](../../../fixtures/product-management/pm-004/release-cards.json) is a **teaching model**, not an audit of current GitHub tags. Run `python state/streeling/fixtures/product-management/pm-004/evaluate_release.py` from the Demerzel root. It checks that each card covers exactly `comfyui`, `blender`, and `godot`, then lists false evidence fields. Its source-snapshot card deliberately gives no installable-extension gate a pass: the narrower project sources above do not establish any of those gates. The other three cards are expressly synthetic.

The evaluator makes a runtime Godot candidate with failed meaning a `reject_candidate`, even if the other eleven per-target fields, contract replay, and hashes pass. Missing receipts produce `hold_for_evidence`. When every modeled gate passes, it returns `release_candidate`, which means the *modeled* package could enter a final release decision. The evaluator never creates a tag, checks a GitHub release, or establishes that reviewer receipts really exist. Its `published` field is separate from candidacy. Avoid collapsing its boolean placeholders into actual quality scores.

### Exercise 3: challenge a weighted score

In the synthetic `pretty-but-wrong` card, every field except `godot.meaning` is true. A teammate proposes releasing because the pass rate is high. What does the evaluator say, and why should that one failure be non-compensating?

> **Answer:** It returns `reject_candidate` and names `godot.meaning` as missing. The product promise includes a correct crossing identity and over/under meaning in the Godot scene. More complete ComfyUI or Blender paperwork cannot make a wrong Godot crossing correct. The fictional score does not represent a measured team result.

### Exercise 4: distinguish review from technical completion

The synthetic `technical-only` card has implementation, runtime, meaning, contract replay, and hashes marked true for all targets, but all three human-review fields are false. State its decision, the next evidence to request, and whether a GitHub release exists.

> **Answer:** It is `hold_for_evidence`. Request reviewer identity, exact source and artifact hashes, target-specific verdict and findings, plus uncoached user task results for each extension. `published_tag` is false; neither the card nor the Python program creates a GitHub release. Its technical booleans are invented teaching data, not real test receipts.

## 4. Cut the release at a useful seam

A bundle can become a bottleneck if one immature target blocks two usable targets. Decide whether users actually need one atomic installation. The audio workflow and the 3D craft path serve different tasks, so independent extension releases may be cheaper to validate. A cross-tool integration release should come later if a user task genuinely traverses those tools and its contract replay can be demonstrated. Splitting versions is not a way to hide a failed semantic gate: each target release must still pass its own package, runtime, meaning, and human checks. Publish an explicit compatibility matrix for any combined workflow.

Set a stop rule before implementation. For a proposed Godot weave inspector, reject an import if any clicked crossing resolves to the wrong stable ID or declared over/under value. For a proposed Blender cleanup aid, reject a candidate if the identified craft feature disappears even when triangle count falls. For an audio workflow, a byte-identical candidate is a no-change control; a spectral change needs matched windows and listening, not an automatic “sounds better” claim. These rules tie the release to user value, rather than making the build itself the success metric.

### Exercise 5: make the release call

The synthetic `candidate-after-reviews` card passes every modeled gate but has `published_tag: false`. A manager asks, “Are the extensions released?” Give the correct status and two concrete next checks. Then explain what the team should say about the real pinned-source snapshot.

> **Answer:** The synthetic card is a **release candidate**, not a release. Independently inspect the named packages and receipts, including compatibility and license checks omitted from this fixture; then, if approved, create the actual tagged release and anonymously download/install the artifacts to verify the documented path. For the real pinned-source snapshot, say only that relevant experiments and plans exist and the three-extension release is on hold. The classroom card supplies no real approval or public distribution evidence.

## Key takeaways and limits

- Name the user's installation and task before deciding whether three tools need one release.
- Use target-specific hard gates for installability, runtime, semantic meaning, and human task evidence. An aggregate score cannot compensate for a wrong promised result.
- A passing fixture is evidence that the **decision model** behaves as written, not evidence that an extension, human review, tagged release, or public course page exists.

The source links above are revision-bound examples. This lesson did not run ComfyUI, Blender, or Godot, inspect an actual extension package, measure audio quality, review a craft asset with users, or publish a GitHub release. PM-004 itself awaits subject, learner, and language review plus Learn integration and anonymous public readback.
