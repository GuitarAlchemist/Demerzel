# Jarvis Phase 4: Native-First Desktop Companion

> Addresses: GuitarAlchemist/Demerzel#179

**Revised:** 2026-07-21 after Codex Computer Use and Remote became available on Windows.

## Summary

Persistent desktop presence for Demerzel using Codex's supported Windows
surfaces first. Galactic Protocol supplies coordination; Computer Use supplies
scoped GUI actuation; Remote supplies phone/secondary-device supervision.

## Architecture

```
Codex desktop app (Windows)
  ├── Galactic MCP bridge → presence, claims, inbox, acknowledgements
  ├── Lifecycle hooks → near-live active-session delivery
  ├── Computer Use → foreground GUI verification and multi-app workflows
  ├── Remote → mobile steering, approvals, screenshots, and review
  └── Optional Prime Radiant/Tauri widget → only for measured native UI gaps
```

## Components

### Native shell first

- Use the Codex desktop app rather than building an Electron/Tauri host in the
  first slice.
- Install and enable Computer Use; invoke it with `@Computer` or `@AppName`.
- On Windows, keep the target application visible on the active desktop.
- Use official Remote for phone/secondary-device supervision. Do not build a
  custom remote WebSocket bridge.
- Reconsider Tauri only after measuring a missing fleet dashboard, idle-alert,
  or governance-visualization capability.

### Prime Radiant Widget
- Always-visible governance health dashboard
- Belief state indicators (tetravalent: T/F/U/C)
- Conscience signals with severity coloring
- Compounding metrics trend lines
- Clickable drill-downs to full governance browser

### Screen Watching

- Use Computer Use only for a named, visible app and a scoped flow.
- Prefer structured MCP/plugin access when an app exposes it; use pixels only
  when GUI state is the evidence.
- Do not implement ambient whole-desktop surveillance.
- Treat visible app content, screenshots, clipboard state, and signed-in browser
  pages as sensitive context.

### Proactive Suggestions

- Use Codex Automations/hooks for scheduled and lifecycle work.
- Galactic claims remain the source of lane ownership.
- Toast notifications for:
  - Submodule staleness detected
  - Belief state degradation
  - Constitution violations in edited files
  - Cross-repo drift detected

### Local Inference

- Keep Kokoro/Whisper/local-model experiments as optional cost and privacy
  optimizations; they are no longer a blocker for desktop control.
- Do not claim zero cloud processing when using Codex Computer Use or Remote.

## Checklist

- [x] Shared cross-session claim ledger adopted
- [x] Galactic MCP + lifecycle-hook tracer bullet implemented
- [ ] User reviews `/hooks` and starts a new Codex chat
- [ ] Computer Use plugin enabled and verified on one low-risk Windows app
- [ ] Claim-aware GUI verification demonstrated end-to-end
- [ ] Remote supervision verified from one supported secondary device
- [ ] Measure whether a Prime Radiant/Tauri widget is still justified

## Governance

- **Article 9 (Bounded Autonomy)**: Suggestions only — no autonomous action without confirmation
- **Article 3 (Reversibility)**: All proactive actions must be undoable
- **Article 2 (Transparency)**: Show reasoning for every suggestion
- **Article 8 (Observability)**: Widget IS the observability surface
- **Article 9 (Bounded Autonomy)**: Computer Use remains app-scoped and approval-gated

## Dependencies

- Phase 2 (TTS) — voice output for spoken alerts
- Codex Computer Use plugin and per-app permission
- Galactic live-session bridge
- Optional Phase 3 visual critic for domain-specific screenshot analysis
