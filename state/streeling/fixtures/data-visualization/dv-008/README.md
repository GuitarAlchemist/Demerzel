# DV-008 synthetic evidence cards

`scenarios.json` contains six invented course states. They are teaching examples, not observations of Streeling publication. `analyze.py` validates their fields and computes four counts plus per-card decisions; `results.json` is the saved output.

From the Demerzel root, run:

```text
python -I -B scripts/streeling_fixtures/data-visualization/dv-008/analyze.py --check
```

Expected counts are 6 authored, 2 approved, 2 exact public readbacks, and 1 card satisfying all three gates. B has approved review but HTTP 404; F has an exact public readback without review. A matching heading alone does not pass the source-provenance checks. The analyzer performs no network requests, and these counts say nothing about the real 525-course goal.
