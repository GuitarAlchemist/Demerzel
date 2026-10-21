# PHY-005 arithmetic fixture and pinned evidence

This directory contains six **derived arithmetic cases**, two deliberate unit mistakes, and source/test provenance. It adds no executable or runtime behavior. Physical widths, stock thicknesses, and proposed scene mappings are teaching assumptions. They are not measured sheets or active engine settings.

## Inspect the exact source

Run these read-only commands in `C:\Users\spare\source\repos\ix`, using the pinned object even if the working tree has other edits:

```powershell
git show d7c22fdd6a62becb66b9d7246ea85850e7c55854:crates/ix-origami/src/lib.rs
git show d7c22fdd6a62becb66b9d7246ea85850e7c55854:crates/ix-origami/src/thickness.rs
git show d7c22fdd6a62becb66b9d7246ea85850e7c55854:crates/ix-origami/tests/thickness.rs
```

Canonical source links: [library contract](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs), [thickness implementation](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), [thickness tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs).

`stack` uses full thickness in crease-pattern units. It multiplies `ply` and rigid `levels` by the supplied `t`. The crane assertion gives 28 plies, 36 exact rigid levels, zero undetermined pairs, and 59 face-level entries, using `t=0.4/150` for the stated 150 mm unit-square sheet. The scale test compares `t=0.25` with `0.5`, asserting doubled heights and unchanged face levels. Powers-of-two coordinate normalization in `lib.rs` serves absolute numerical tolerances; it does not supply a physical unit or convert the caller's material measurement.

The coordinator reports this focused command at unchanged IX HEAD `d7c22fdd6a62becb66b9d7246ea85850e7c55854` on 2026-10-21 (report time 20:47:52 UTC):

```powershell
cargo test -p ix-origami --test thickness
```

Result: **11 passed, 0 failed**. The course author did not run another Cargo build. This existing-target replay is not a full-suite or engine integration result; it does not execute the new arithmetic scenarios as IX inputs. A working-tree test command covers the checked-out files, so a later replay must establish the same HEAD and inspect local changes rather than treating the command alone as proof of pinned-source identity.

## Recompute by hand

For each object in [scenarios.json](scenarios.json), use `a=W/C`, `t_cp=h/a`, `H_ply_cp=28×t_cp`, and `H_rigid_cp=36×t_cp`. Recover mm by multiplying coordinate lengths by `a`. Multiply mm by `u/1000` to get scene lengths, where `u` is the case's assumed scene units per metre. The two paths `36×t_cp×a×u/1000` and `36×h×u/1000` must agree. Decimal comparisons may differ by at most `1e-9` from rounding; the fractions are authoritative.

Reference: `36×(0.4/150)×150=14.4 mm`, then `14.4/1000=0.0144 scene units` when `u=1`. The ply path yields `28×0.4=11.2 mm` and `0.0112 scene units`. Compare the six cases to isolate thicker stock, wider sheets, proportional physical enlargement, coordinate re-encoding, and scene scaling. Inspect deliberate mistakes separately; they are expected wrong values, not outputs that should match the reference.

An illustrative lower-surface convention puts level 35 at `35×h`; the top of a full 36-level stack is `36×h`. This convention adds no exported panel placement. `face_levels` is one assignment satisfying the order, not a canonical geometric witness.

## Targeted artifact check

From the Demerzel pilot root:

```powershell
python scripts/streeling_course_preflight.py cp-physics-2026-10-21-005
```

The preflight checks record schemas, metadata, declared locales, exact English whitespace word count, answered-exercise signals, and status consistency. It does not evaluate physics, translation fluency, real learning, or public availability. No runtime behavior changed, so source inspection, the existing focused test replay, arithmetic cross-checks, and this artifact check form the bounded replacement verification for the draft.

The [learner task](../../../reviews/phy-005-learner-task.md) is answer-free. The [review brief](../../../reviews/phy-005-review-brief.md) is unbound until the coordinator supplies the exact Demerzel commit and locale blobs. No subject approval, native-language approval, learner trial, physical feasibility proof, exporter, live Blender/Godot/DLSS import, or publication is claimed.
