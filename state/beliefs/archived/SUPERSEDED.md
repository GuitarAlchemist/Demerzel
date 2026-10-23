# Archived beliefs — verdict ledger

Beliefs in this directory are retired, not deleted. The belief-currency lint
(`scripts/belief_lint.py`) skips `archived/`, so nothing here is asserted as a
live belief. Records are kept for audit.

## 2026-07-20 — placeholder beliefs (hari #29 loop audit)

Nine placeholder belief scaffolds were archived here from `state/beliefs/`:

- `slot-blue-health.belief.json`, `slot-green-health.belief.json`
  — emitter `ga-build-system` (blue/green build-slot health)
- `visual-displacement-terrain`, `visual-earth-clouds`, `visual-earth-snow`,
  `visual-earth-terminator`, `visual-milky-way-parallax`,
  `visual-planet-proportions`, `visual-sun-flare` (`.belief.json`)
  — emitter `visual-critic-loop` (visual-quality judgements)

**What they were:** empty scaffolds seeded 2026-03-28, each held
`truth_value: "U"`, `confidence: 0.0`, and empty evidence — the shape a
producer was meant to fill in.

**When they died:** last write 2026-03-28 (`943b9b3` for the slots; the
visual set the same day). Their producers (`ga-build-system`,
`visual-critic-loop`) never emitted a real value in the ~4 months since, and
no script, workflow, or policy reads them as input.

**Verdict (hari #29 — "kill or archive-with-verdict"):** dead / write-once
placeholders — no producer, no reader.

**Superseded by:** the belief lifecycle is now governed by the
belief-currency lint (`scripts/belief_lint.py`, the CI tripwire) plus the
monthly hari substrate replay
(`docs/research/2026-07-20-demerzel-belief-replay.md`). Live beliefs earn
their place by carrying real evidence and passing the lint; unfed U@0.0
placeholders do not. If blue/green slot health or visual-quality judgement is
re-owned later, it should land with its producer AND its gating consumer in
the same change (loop doctrine, hari #29).
