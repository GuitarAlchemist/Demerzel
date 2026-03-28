# Jarvis Phase 4: Always-On Desktop Shell

> Addresses: GuitarAlchemist/Demerzel#179

## Summary

Persistent desktop presence for Demerzel — an always-on governance companion that watches, suggests, and acts proactively.

## Architecture

```
Electron/Tauri desktop shell
  ├── Prime Radiant widget (persistent governance dashboard)
  ├── Screen watcher (Windows MCP → visual context)
  ├── Proactive suggestions (driver cycle + cron triggers)
  └── Local inference (RTX 5080, zero cloud cost)
```

## Components

### Desktop Shell
- **Framework**: Tauri (Rust backend, web frontend) preferred over Electron for:
  - Lower memory footprint (~10x less than Electron)
  - Native system tray integration
  - Rust backend aligns with ix ecosystem
- **Fallback**: Electron if Tauri's webview limitations block features

### Prime Radiant Widget
- Always-visible governance health dashboard
- Belief state indicators (tetravalent: T/F/U/C)
- Conscience signals with severity coloring
- Compounding metrics trend lines
- Clickable drill-downs to full governance browser

### Screen Watching
- **Windows MCP** integration for screenshot capture
- Context-aware: detect IDE, terminal, browser, Discord
- Trigger governance checks based on visual context
- Privacy: local-only processing, no cloud upload

### Proactive Suggestions
- Driver cycle runs on configurable interval (default: 30min)
- Cron-triggered governance scans
- Toast notifications for:
  - Submodule staleness detected
  - Belief state degradation
  - Constitution violations in edited files
  - Cross-repo drift detected

### Local Inference
- All AI inference on RTX 5080
- Zero cloud API cost for routine operations
- Cloud fallback only for complex reasoning tasks
- Models: Kokoro (TTS), Whisper (STT), local LLM (suggestions)

## Checklist

- [ ] Electron or Tauri desktop shell
- [ ] Prime Radiant as persistent governance widget
- [ ] Screen watching via Windows MCP
- [ ] Proactive suggestions (driver cycle + cron)
- [ ] Local only, zero cloud cost (RTX 5080)

## Governance

- **Article 9 (Bounded Autonomy)**: Suggestions only — no autonomous action without confirmation
- **Article 3 (Reversibility)**: All proactive actions must be undoable
- **Article 2 (Transparency)**: Show reasoning for every suggestion
- **Article 8 (Observability)**: Widget IS the observability surface

## Dependencies

- Phase 2 (TTS) — voice output for spoken alerts
- Phase 3 (Perception) — visual critic for screen context
- RTX 5080 for local inference
- Windows MCP server
