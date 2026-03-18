# Rust Governance Dashboard — Design Spec

**Status:** Incubation (Experiment)
**Target:** ix repo as `ix-dashboard` crate or standalone repo
**Budget ceiling:** $20

## Problem

Demerzel's governance state lives in JSON files across `state/`. Inspecting governance health requires reading individual files. There's no at-a-glance view of:
- Which beliefs are stale, contradictory, or low-confidence
- How governance artifacts are trending (evolution)
- Cross-repo compliance status
- Active PDCA cycles and their progress

## Solution

A Rust app that reads Demerzel's `state/` directory and renders a governance dashboard.

## MVP (TUI — ratatui)

### Views

1. **Beliefs Dashboard**
   ```
   ┌─ Beliefs ─────────────────────────────────────────────────┐
   │ T  Framework integrity              0.95  2026-03-17  ✓   │
   │ F→T Behavioral test coverage        0.95  2026-03-17  ✓   │
   │ U  ix governance integration        0.40  2026-03-17  ⚠   │
   │ U  tars governance integration      0.20  2026-03-17  ⚠   │
   │ U  ga governance integration        0.20  2026-03-17  ⚠   │
   │ F  Consumer repo directives sent    0.90  2026-03-17  ✗   │
   └────────────────────────────────────────────────────────────┘
   ```
   - Color coded: T=green, F=red, U=yellow, C=magenta
   - Confidence bar visualization
   - Staleness indicator (days since update, warning at 5+, alert at 7+)

2. **Evolution Timeline**
   ```
   ┌─ Evolution ────────────────────────────────────────────────┐
   │ asimov-constitution    5 cited  0 violated  100%  maintain │
   │ default-constitution  11 cited  0 violated  100%  maintain │
   │ alignment-policy       3 cited  0 violated  100%  promote? │
   └────────────────────────────────────────────────────────────┘
   ```
   - Citation/violation counts
   - Compliance rate sparklines
   - Promotion/deprecation candidate flags

3. **PDCA Tracker**
   ```
   ┌─ Active Cycles ────────────────────────────────────────────┐
   │ ✓ behavioral-test-gap          act (complete)   2026-03-17 │
   │ ◐ rust-dashboard-experiment    plan             2026-03-17 │
   └────────────────────────────────────────────────────────────┘
   ```
   - Phase indicator (plan/do/check/act)
   - Experiment flag and budget tracking

4. **Cross-Repo Compliance**
   ```
   ┌─ Repos ────────────────────────────────────────────────────┐
   │ Demerzel  ████████████  100%  state✓  wiki✓  tests✓       │
   │ ix        ████████░░░░   66%  state✓  wiki✓  tests?       │
   │ tars      ████░░░░░░░░   33%  state?  wiki?  tests?       │
   │ ga        ████░░░░░░░░   33%  state?  wiki?  tests?       │
   └────────────────────────────────────────────────────────────┘
   ```

5. **Project Board Summary**
   ```
   ┌─ Board ────────────────────────────────────────────────────┐
   │ Done: 5  In Progress: 3  Todo: 5                          │
   │ P0: 0  P1: 3  P2: 3  P3: 2                               │
   │ Experiments: 1  Incubations: 1                            │
   └────────────────────────────────────────────────────────────┘
   ```

### Navigation

- Tab/Shift+Tab between panels
- Arrow keys within panels
- Enter to drill into detail
- `q` to quit
- `r` to refresh (re-read state files)

## Tech Stack

| Component | Crate | Why |
|-----------|-------|-----|
| TUI framework | `ratatui` 0.29+ | Standard Rust TUI, maintained |
| Terminal backend | `crossterm` | Cross-platform (Windows!) |
| JSON parsing | `serde_json` | Standard, already in ix |
| Schema validation | `jsonschema` | Validate state files against Demerzel schemas |
| File watching | `notify` | Auto-refresh on state file changes |
| Time handling | `chrono` | Staleness calculations |

## Data Sources

All read-only from Demerzel's `state/` directory:

| Directory | Schema | Dashboard View |
|-----------|--------|----------------|
| `state/beliefs/*.belief.json` | `tetravalent-state.schema.json` | Beliefs Dashboard |
| `state/evolution/*.evolution.json` | `governance-evolution.schema.json` | Evolution Timeline |
| `state/pdca/*.pdca.json` | `kaizen-pdca-state.schema.json` | PDCA Tracker |
| `state/oversight/*.json` | Various | Cross-Repo Compliance |
| `state/snapshots/*.snapshot.json` | `belief-snapshot.schema.json` | Historical view |

## Configuration

```toml
# dashboard.toml
[source]
state_dir = "../Demerzel/state"  # Path to Demerzel state directory

[display]
refresh_interval_secs = 30
staleness_warning_days = 5
staleness_alert_days = 7

[github]
project_id = "PVT_kwDOBbiyps4BR3QU"  # Optional: pull project board data
```

## Stretch Goals (Post-MVP)

- **egui GUI** — desktop app with charts and graphs (ix-demo already uses egui)
- **GitHub API integration** — pull project board data live
- **Anomaly highlighting** — flag beliefs that changed unexpectedly
- **Export** — generate governance report as Markdown
- **Multi-repo state** — read state from ix/tars/ga as well as Demerzel

## Implementation Plan

1. Create `ix-dashboard` crate in ix workspace
2. Define Rust types matching Demerzel JSON schemas (serde)
3. Implement state directory reader with file watching
4. Build TUI layout with ratatui
5. Wire data to views
6. Test on Windows (crossterm)
7. Add to ix MCP tools as `ix_dashboard` (optional)
