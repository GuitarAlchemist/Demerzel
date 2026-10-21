# CS-009 panel-constraint exercises

`scenarios.json` is a hand-derived teaching trace of the IX algorithm at commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. The first two graphs mirror the pinned pierced-joint and four-strip test constructions. The final two graphs are explicitly synthetic arithmetic examples, not FOLD files or captured analyzer output. JSON `0.6` denotes the mathematical value; floating-point arithmetic may print a nearby value.

In an IX checkout at the pinned revision, replay its unchanged integration tests:

```text
cargo test -p ix-origami --test thickness
```

On 2026-10-21 the root coordinator ran this command at that HEAD: 11 tests passed, 0 failed. Source `crates/ix-origami/src/thickness.rs` has blob `43351fe867a83a10ab38113cb86db8633a0112f1`; `tests/thickness.rs` has blob `3342419488ca7039d8a76e00366f26d5416234b9`. Check these identities before comparing a later implementation.

Independently trace the examples: union faces joined by flat joints, map lower/upper face pairs to panel arcs, find a cycle or assign longest-path levels in topological order, then multiply the number of occupied levels by `t`. With undetermined overlapping pairs, compare the chain with `ply` and withhold a face-level witness.

This package adds no duplicate analyzer. The existing IX tests exercise the implementation; the JSON makes the lesson's small derivations inspectable. It does not execute the synthetic DAG through IX geometry, validate a Blender or Godot import, establish physical manufacturability, or record a learner result.
