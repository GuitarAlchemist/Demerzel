# SEM-004 synthetic face correspondence fixture

`scenarios.json` is a hand-authored arithmetic example. The four faces, labels, levels, and permutation are explicitly synthetic. They are not crane face values, a saved IX random seed, a FOLD model, or measurements. The labels are classroom provenance marks supplied by the author; the inspected IX code does not thereby acquire persistent identity infrastructure.

Read `old_to_new` by input index. Place each old item at its mapped output index: input 0/A goes to output 2; 1/B to 0; 2/C to 3; 3/D to 1. Read `new_to_old` by output index. It is `[1,3,0,2]`, so output 0 came from input 1. Both compositions produce `[0,1,2,3]`.

Input levels `[0,2,1,3]` become output levels `[2,3,0,1]`. Comparing `new[p[f]]` with `old[f]` yields four matches; comparing raw arrays yields inequality; using the inverse in that forward comparison yields four mismatches. The selected input 1/B must become output 0/B. Reusing slot 1 selects D. The deliberately non-self-inverse map distinguishes the two directions.

The synthetic triple `[1,3,1]` becomes `[0,1,1]`. The sign remains unchanged by renumbering and is interpreted relative to face normals. The boundary examples distinguish cyclic rotation from reversal; they do not supply actual IX vertices or introduce geometry.

## Pinned source and replay

Authoritative IX source revision: `d7c22fdd6a62becb66b9d7246ea85850e7c55854`.

| Source | Blob | Evidence |
|---|---|---|
| [src/controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs) | `29e73655fdbcb14e08c06520c9773950ce0b6407` | Old-to-new direction, remapped references, cyclic boundary rotations, endpoint swaps, relation-list shuffle, rigid motion, turnover |
| [tests/thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) | `3342419488ca7039d8a76e00366f26d5416234b9` | Crane controls and exact scope of the assertions |
| [src/thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) | `43351fe867a83a10ab38113cb86db8633a0112f1` | Optional face levels, one stack witness, aggregate level/height semantics |

The controls are in `src/controls.rs` at this revision; no `tests/common` implementation is assumed. In an IX checkout already at the pinned revision, these commands inspect the version and replay the named source test:

```powershell
git rev-parse HEAD
cargo test -p ix-origami --test thickness controls_leave_the_stack_unchanged -- --exact
cargo test -p ix-origami --test thickness
```

Do not treat the output as pinned evidence if HEAD differs. The coordinating author independently reported the thickness target at this exact HEAD: 11 tests passed, zero failed, on 2026-10-21. This package's worker did not rerun Cargo; its work changes course and data artifacts only. The lesson itself relies on inspected assertions, not an invented saved test transcript.

## Read-only package preflight

From Demerzel, run:

```powershell
python -B scripts/streeling_course_preflight.py cp-semiotics-2026-10-21-004
```

This checks record schemas, source metadata, declared languages, exact English whitespace word count, answered English exercises, and status consistency. Separately derive both inverse compositions, labels, levels, selection and triple mapping from the JSON, without treating the stored expected values as their own proof. No executable fixture analyzer is added.

## Proposed integration trial

In a future Godot scene with an actual adapter, select input 1/B, record the exact model and map, apply this permutation, then require the highlight and event report to identify output 0/B at level 2. Capture raw selection events and before/after screenshots. Output 1/D is a falsifier even if totals remain equal. This is a prepared trial; no scene, adapter, renderer, export, import or observation has been delivered or tested here. A turnover trial needs its own property-specific expectations because the pinned source does not assert per-face level equality for turnover.
