# Phase 2.5: Discord Voice Channel Integration

> Addresses: GuitarAlchemist/Demerzel#182

## Summary

Bridge Phase 2 (TTS engine) and Phase 3 (perception) — Demerzel joins Discord voice channels and speaks governance reports aloud using Kokoro-82M TTS.

## Architecture

```
User command → demerzel-bot → Kokoro TTS API (localhost:8880)
                                   ↓
                              OGG/Opus audio
                                   ↓
                         @discordjs/voice → Discord voice channel
```

## Voice Commands

| Command | Description |
|---------|-------------|
| `join` | Join user's voice channel |
| `leave` | Disconnect from voice |
| `speak <text>` | Synthesize and play text |
| `announce` | Read latest governance report aloud |

## Implementation (demerzel-bot)

### New Modules
- `src/voice.js` — Voice module: synthesize (Kokoro API), join/leave channels, stream audio
- `scripts/test-voice-pipeline.js` — End-to-end pipeline test (no Discord needed)

### Dependencies
- `@discordjs/voice` — Discord voice connection management
- `libsodium-wrappers` — Encryption for voice UDP
- `opusscript` — Opus encoding (no ffmpeg required)
- `prism-media` — Audio stream handling

### Design Decisions
- **OGG/Opus format** requested directly from Kokoro → Discord-native, no ffmpeg transcoding
- **Voice: af_bella** (configurable via `KOKORO_VOICE` env var)
- **GuildVoiceStates intent** added to bot client
- Connection pooled per guild, auto-reconnect on disconnect

## Test Plan

- [ ] `npm run test:voice` — verifies TTS pipeline without Discord
- [ ] `join` in voice channel → bot joins
- [ ] `speak Hello world` → audio plays
- [ ] `announce` → governance report spoken
- [ ] `leave` → bot disconnects
- [ ] Bot auto-reconnects after brief disconnect

## Governance

- **Article 6 (Escalation)**: Voice commands require explicit user invocation
- **Article 9 (Bounded Autonomy)**: Bot only speaks when commanded, never unprompted
- **Privacy**: No voice recording or STT in this phase
