# PHY-005 bounded AI learner dry-run — raw first response

This is the first submitted response, retained without feedback or revision. This is an AI calculation dry-run, not a review approval or a human learning trial. I am an AI with general prior competence in ratios, dimensional analysis, geometry, and arithmetic; I am not a novice learner. No causal learning benefit, human experience, or score is claimed.

Actual UTC start: 2026-10-21 23:53:02 UTC (clock reading immediately before the source read).
Actual UTC end: 2026-10-21 23:54:21 UTC (clock reading after drafting the calculations and immediately before writing this response).

## Evidence and assistance boundary

Source files read, in full:

- C:\tmp\streeling-craft-dryrun-20261021-r1\phy-005\lesson.md
- C:\tmp\streeling-craft-dryrun-20261021-r1\phy-005\task.md

I read no original course, fixture, answer key, review brief, other response, memory, external source, or engine project. Source links below were already in the lesson and were not inspected. The lesson itself includes worked answers and numerical reference results; therefore this response is not evidence of performance without those supplied derivations. I used those two documents, general prior competence, and direct arithmetic, without a calculator or assistance from another agent. A clock tool supplied the actual timestamps.

The following are my unedited submitted calculations and answers. Decimal expansions marked approximately are display rounding; fractions govern the calculations.

## Lesson practice exercise 1: repair the thickness input

Reference: C = 1 CP unit, W = 150 mm, h = 0.4 mm.

a = W/C = 150 mm/CP.
Required t_CP = h/a = 0.4/150 = 1/375 CP ≈ 0.002666666667 CP.

Mistaken t_CP = 0.4 CP represents 0.4 × 150 = 60 mm of physical stock.
Error factor = 60/0.4 = 150.
Repair: supply 0.4/150 CP to a thickness parameter expressed in this coordinate representation.

## Lesson practice exercise 2: distinguish offset from extent

Ply 28 gives 28 × 0.4 = 11.2 mm under the local-ply interpretation.
The exact parallel rigid order has 36 levels, giving a complete extent of 36 × 0.4 = 14.4 mm.

With lower surfaces z_k = k × t and levels indexed 0 through 35:
highest lower surface = 35 × 0.4 = 14 mm;
complete stack extent = 36 × 0.4 = 14.4 mm.

Thus the rigid extent cannot be replaced by either the local-ply height or the highest lower-surface offset. The top slab adds its full 0.4 mm above the last lower surface. In CP units these two rigid quantities are 35/375 ≈ 0.093333333333 CP and 36/375 = 0.096 CP.

## Lesson practice exercise 3: factor-of-1000 mistake

For the proposed scale of 1 scene unit/metre:
b = 1/1000 = 0.001 scene unit/mm.

Thickness = 0.4 × 0.001 = 0.0004 scene unit.
Rigid extent = 14.4 × 0.001 = 0.0144 scene unit.
Sheet width = 150 × 0.001 = 0.15 scene unit.

A scale-independent thickness-to-width check:
physical ratio = 0.4/150 ≈ 0.002666666667;
mistaken scene ratio = 0.4/0.15 ≈ 2.666666667.
The mistaken ratio is 1000 times the physical ratio.

Likewise, the correct rigid-extent-to-width ratio is 14.4/150 = 0.096, while the mistaken scene ratio is 14.4/0.15 = 96, again a factor of 1000. Uniform length conversion preserves these ratios.

## Lesson practice exercise 4: compare three edits

Assume the exact 36-level order throughout.

A: h = 0.8 mm, W = 150 mm, C = 1 CP.
a = 150 mm/CP.
t_CP = 0.8/150 ≈ 0.005333333333 CP.
Rigid extent = 36 × 0.8 = 28.8 mm.
Coordinate extent = 36 × (0.8/150) = 0.192 CP.

B: h = 0.4 mm, W = 300 mm, C = 1 CP.
a = 300 mm/CP.
t_CP = 0.4/300 ≈ 0.001333333333 CP.
Rigid extent = 36 × 0.4 = 14.4 mm.
Coordinate extent = 36 × (0.4/300) = 0.048 CP.

C: original physical sheet, h = 0.4 mm, W = 150 mm, C = 2 CP.
a = 150/2 = 75 mm/CP.
t_CP = 0.4/75 ≈ 0.005333333333 CP.
Rigid extent = 36 × 0.4 = 14.4 mm.
Coordinate extent = 36 × (0.4/75) = 0.192 CP.

## Lesson practice exercise 5: three-sentence handoff

The supplied lesson reports that the [IX thickness tests at pinned commit d7c22fdd6a62becb66b9d7246ea85850e7c55854](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) assert local ply 28 and exact rigid levels 36 for the reference crane; I have not inspected that linked source, and the reference assumptions imply 11.2 mm and 14.4 mm respectively.
Under a proposed scale of 1 scene unit/metre, map the 150 mm sheet width to 0.15 scene unit, full 0.4 mm stock to 0.0004 scene unit, and rigid extent to 0.0144 scene unit.
These conversions establish neither a physically feasible thick fold nor a verified Blender or Godot import.

## Separate handout task 1: declare the ruler and derive heights

Given W = 200 mm, C = 2 CP, h = 0.6 mm, ply = 28, levels = 36, u = 10 scene units/metre.

a = W/C = 200/2 = 100 mm/CP.
b = u/1000 = 10/1000 = 0.01 scene unit/mm.
Combined multiplier a × b = 100 × 0.01 = 1 scene unit/CP.
The sheet width maps to 200 × 0.01 = 2 scene units.

| Quantity | Coordinate length, CP | Physical length, mm | Proposed scene length |
|---|---:|---:|---:|
| Full material thickness | 0.6/100 = 0.006 | 0.6 | 0.006 |
| Local-ply height | 28 × 0.006 = 0.168 | 28 × 0.6 = 16.8 | 0.168 |
| Complete rigid extent | 36 × 0.006 = 0.216 | 36 × 0.6 = 21.6 | 0.216 |

Rigid conversion path via CP:
36 × (0.6/100) CP × (100 mm/CP) × (0.01 scene unit/mm) = 0.216 scene unit.

Independent physical path:
36 × 0.6 mm = 21.6 mm;
21.6 mm × (10 scene units/1000 mm) = 0.216 scene unit.

The matching numerical CP and scene values result from the chosen multiplier of 1 scene unit/CP; the representations still have different units.

## Separate handout task 2: mistaken coordinate thickness

Passing t_CP = 0.6 CP represents 0.6 CP × 100 mm/CP = 60 mm stock.
Error factor = 60/0.6 = 100.
Repaired value = 0.6 mm / (100 mm/CP) = 0.006 CP.

## Separate handout task 3: lower surface and complete extent

At level 35:
z_35 = 35 × 0.006 = 0.210 CP;
physical offset = 35 × 0.6 = 21 mm;
scene offset = 21 × 0.01 = 0.210 scene unit.

For all 36 levels:
extent = 36 × 0.006 = 0.216 CP;
physical extent = 36 × 0.6 = 21.6 mm;
scene extent = 21.6 × 0.01 = 0.216 scene unit.

Difference = one stock thickness = 0.6 mm = 0.006 scene unit.
This calculation uses an illustrative arrangement of slabs at lower surfaces k × t. The supplied lesson describes it as a proposed drawing convention and reports no existing IX exporter or generated mesh implementing it; I inspected no exporter.

## Separate handout task 4: resize the sheet, then resize all lengths

First change only W to 400 mm, holding C = 2 CP and h = 0.6 mm.

New a = 400/2 = 200 mm/CP.
New t_CP = 0.6/200 = 0.003 CP.
New local-ply height = 28 × 0.003 = 0.084 CP.
New rigid extent = 36 × 0.003 = 0.108 CP.

All three CP heights are half their preceding values.
Physical stock remains 0.6 mm, local-ply height remains 16.8 mm, and rigid extent remains 21.6 mm under the unchanged stated configuration.
At the unchanged proposed scene scale their scene lengths remain 0.006, 0.168, and 0.216 respectively.
Sheet width becomes 4 scene units.

Alternatively double both physical width and stock from the handout baseline:
W = 400 mm, h = 1.2 mm, C = 2 CP, a = 200 mm/CP.
t_CP = 1.2/200 = 0.006 CP.
Local-ply height = 0.168 CP and rigid extent = 0.216 CP, unchanged from the baseline in coordinates.
Physical heights double: stock 1.2 mm, local ply 33.6 mm, rigid extent 43.2 mm.
At 10 scene units/metre these become 0.012, 0.336, and 0.432 scene unit respectively.
These are conditional conversions of the same assumed order, not predictions from a new physical folding experiment.

## Separate handout task 5: evidence-bounded handoff and limitations

Inspect the [IX thickness tests at pinned commit d7c22fdd6a62becb66b9d7246ea85850e7c55854](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) to check the lesson's reported crane assertions; that link was not inspected here, and the reused 28-ply/36-level order is a teaching assumption for the 200 mm sheet.
For the proposed 10 scene units/metre mapping, use 100 mm/CP, map 2 CP to 2 scene units, and map 0.6 mm stock and 21.6 mm rigid extent to 0.006 and 0.216 scene unit respectively.
Neither these calculations nor the supplied lesson establishes a physically feasible folding motion or an actual Blender or Godot configuration/import.

Powers-of-two normalization does not declare a physical unit. According to the supplied lesson it conditions coordinates for numerical tolerance checks; an external physical ruler is still required.

An absent cyclic rigid height does not mean zero. Under the supplied account, a cycle rejects the positive-thickness parallel-panel interpretation, leaving that height unavailable; a zero-thickness case may report a cycle without that refusal. A missing result and a measured zero are different claims.

## Additional transfer calculation requested for this dry-run

Given W = 300 mm, C = 3 CP, h = 0.45 mm, rigid levels = 12, u = 100 scene units/metre:

a = 300/3 = 100 mm/CP.
b = 100/1000 = 0.1 scene unit/mm.
a × b = 10 scene units/CP.
Sheet width = 300 × 0.1 = 30 scene units.

Full stock thickness:
t_CP = 0.45/100 = 0.0045 CP;
t_scene = 0.45 × 0.1 = 0.045 scene unit.

Complete 12-level extent:
H_CP = 12 × 0.0045 = 0.054 CP;
H_mm = 12 × 0.45 = 5.4 mm;
H_scene = 5.4 × 0.1 = 0.54 scene unit.

Independent coordinate check:
0.054 CP × 10 scene units/CP = 0.54 scene unit.

Level 11 lower-surface offset, with levels 0 through 11:
z_11_CP = 11 × 0.0045 = 0.0495 CP;
z_11_mm = 11 × 0.45 = 4.95 mm;
z_11_scene = 4.95 × 0.1 = 0.495 scene unit.

Top of final slab:
4.95 + 0.45 = 5.4 mm;
0.495 + 0.045 = 0.54 scene unit.

No local-ply count was supplied for this additional case, so I make no separate ply-height calculation.

## Confusion, assistance, confidence, and specific ambiguities

I encountered no point requiring help to complete the arithmetic. I used the supplied lesson's explanations of rigid levels, normalization, and cyclic results; I cannot demonstrate prior independent knowledge of those IX-specific behaviors from this attempt. I requested no feedback and made no correction pass before submission. The short actual elapsed interval, recorded by the timestamps, describes this AI run and does not estimate a human's completion time or validate the advertised 40-minute duration.

Confidence: high in the dimensional arithmetic conditional on the given assumptions; source behavior remains unverified beyond the supplied lesson.

Specific ambiguities and limits:

- CP coordinates may undergo internal normalization; an eventual integration must identify exactly which coordinate representation is being mapped and apply its matching physical ruler consistently. I have not traced that representation through IX.
- “Level 11” is interpreted as zero-based because the requested convention is z_k = k × t; a one-based naming convention would require explicit translation.
- The height extent assumes full slabs beginning at z = 0. A centered-slab convention would change individual surface coordinates and the chosen origin; the complete extent is still the number of occupied levels times full thickness.
- The handout imports a fixed crane order as an assumption for resized and thicker sheets. This dry-run does not establish that the same configuration is physically attainable with those materials.
- Existing-source assertions and the lesson's reported 11-test result were supplied claims, not independently inspected or rerun evidence.
- The proposed scene scales are declarations for these calculations. No engine configuration, import round trip, exporter, or physical thickness was observed.

