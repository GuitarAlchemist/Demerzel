# Hex-merge conformance fixtures (canonical)

Shared corpus for verifying that implementations of
[`logic/hex-merge.md`](../../logic/hex-merge.md) agree on output.
**This directory is the canonical home.** Consumer repos read from
here via submodule.

## Why centralize

Per the 2026-05-02 compounding cycle
([`docs/reports/2026-05-02-hex-merge-cross-repo-cycle.md`](../../docs/reports/2026-05-02-hex-merge-cross-repo-cycle.md)),
the corpus first landed in `hari/fixtures/hex-merge/` and
`ix/crates/ix-fuzzy/tests/fixtures/hex-merge/` as parallel copies.
Drift risk is real: an 8th fixture would have required syncing two
locations by hand. Centralizing in Demerzel eliminates that.

## Current consumers

| Consumer | Read path | Notes |
|---|---|---|
| `ix-fuzzy::observations` | `ix/governance/demerzel/fixtures/hex-merge/*.json` (via existing submodule) | IX's `governance/demerzel` submodule must be bumped to a Demerzel commit that includes this directory. |
| `hari_lattice::merge` | `hari/fixtures/hex-merge/*.json` (local copy) | hari does not currently have a Demerzel submodule. The local copy is treated as a snapshot of the canonical fixtures here; a CI parity check or manual review keeps them in sync. Adding a Demerzel submodule to hari is a separate decision. |

## Schema

```jsonc
{
  "name": "human_readable_name",
  "description": "what this fixture proves",
  "input": {
    "observations": [
      {
        "source": "tars",
        "diagnosis_id": "d",
        "round": 0,
        "ordinal": 0,
        "claim_key": "ix_stats::valuable",
        "variant": "T",         // T/P/U/D/F/C
        "weight": 0.9,
        "evidence": null         // optional
      }
    ],
    "current_round": null,       // u32 or null
    "staleness_k": null          // u32 or null
  },
  "expected": {
    "observations_count": 2,
    "contradictions_count": 0,
    "contradictions": [],
    "distribution": {
      "T": 0.5625, "P": 0.4375, "U": 0.0,
      "D": 0.0, "F": 0.0, "C": 0.0
    },
    "escalation_triggered": false
  }
}
```

Variants use the canonical single-letter wire format (`T`/`P`/`U`/
`D`/`F`/`C`) — same as
[`logic/hexavalent-state.schema.json`](../../logic/hexavalent-state.schema.json)
and `ix-types::Hexavalent`. Floats are compared within `1e-9`.

`expected.contradictions[].diagnosis_id` is optional. When present,
the conformance test pins it exactly — that is the strongest claim
because it pins the content-derived synthesis-id formula from
`hex-merge.md` (the associativity fix). Adding a `diagnosis_id`
expectation should be the default for any fixture exercising
synthesis.

## Current corpus

| File | Scenario |
|---|---|
| `01_agreement_no_contradiction.json` | T+P same-side agreement, no synthesis |
| `02_direct_full_contradiction.json` | T+F → C at full weight, escalation |
| `03_direct_soft_contradiction.json` | P+D → C at 0.5 multiplier, no escalation |
| `04_meta_conflict_cross_aspect.json` | Different aspects, same action → meta_conflict |
| `05_staleness_drops_old_rounds.json` | Round filter at K=5 |
| `06_dedup_collapses_duplicates.json` | Same dedup key, first-write wins |
| `07_empty_yields_uniform.json` | Empty input → uniform 1/6 fallback |

## Adding a fixture

1. Create `NN_descriptive_name.json` here.
2. Hand-compute (or read off a known-good run of) the expected
   output; commit.
3. Each consumer's conformance runner picks up new files
   automatically — no test code changes required.
4. Once Demerzel/master is updated, downstream submodules can
   fast-forward (or hari can sync manually) to gain the new fixture.

## Adding an aspect

`claim_key` aspects are defined in `logic/hex-merge.md §Claim Key
Grammar`. Adding a new aspect is a Demerzel governance change
(amend the spec); this directory will pick up fixtures exercising
it once they land.
