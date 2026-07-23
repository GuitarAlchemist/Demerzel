# state/constitution/evolution-history.json — ARCHIVED / SUPERSEDED (2026-07-20)

**What it was:** a hand-maintained "immutable append-only log of all
constitutional amendments, proposals, and S5 emergent value detections".

**When it died:** last write 2026-03-22 (`40e7530`). It holds only the three
2026-03-14 GENESIS amendments; `emergent_value_detections` and
`pending_proposals` have stood empty since creation. The append that
`policies/governance-process-policy.yaml` (line ~281,
"Append detection to state/constitution/evolution-history.json") calls for on
S5 detection has never fired.

**Why archived:** hari #29 loop audit ("kill or archive-with-verdict").
Verified 2026-07-20 — no executable reads or writes this file: the only
governance validator, `scripts/validate_governance.py`, checks
`state/evolution/*.evolution.json`, not this path; `scripts/build_manifest.py`
does not scan it. Its sole remaining reference is the declarative policy
directive above, which points at an append-target that is never appended to
(a starved loop: intended writer, no live producer, no reader).

**Superseded by:** `state/evolution/*.evolution.json` — the governance /
ML-governance cycle summaries, which ARE schema-validated in CI
(`scripts/validate_governance.py` against
`logic/governance-evolution.schema.json`) and are the ecosystem's live,
audit-trailed evolution log.

**Note (not modified in place):** `evolution-history.json` carries its own
`immutability_rule` ("Entries may NEVER be modified or deleted — append
only"), so this verdict is recorded here beside it rather than written into
the file. Follow-up for the owner: the dangling append-target directive in
`policies/governance-process-policy.yaml` should be repointed or retired
(left untouched here — editing policies is out of this audit's scope and
would alter the governance manifest).
