# Jarvis Phase 2: Local TTS — Kokoro-82M

> Addresses: GuitarAlchemist/Demerzel#177

## Summary

Give Demerzel an audible voice using Kokoro-82M, a lightweight open-source TTS model running locally on RTX 5080.

## Architecture

```
Text input (governance report, response, alert)
  → Kokoro-82M ONNX Runtime (localhost:8880)
  → OGG/Opus audio stream
  → Output target (Discord voice, local speaker, file)
```

## Components

### TTS Engine
- **Model**: Kokoro-82M (Apache 2.0, 82M parameters)
- **Runtime**: ONNX Runtime with CUDA EP on RTX 5080
- **API**: HTTP REST on localhost:8880
- **Format**: OGG/Opus (Discord-native, no transcoding needed)

### Voice Personality
- **Primary voice**: `af_bella` — warm, clear
- **Blend**: `af_bella(2) + af_sky(1)` for Demerzel persona
- **Configurable**: `KOKORO_VOICE` environment variable
- **Fallback**: Bark (MIT) for expressive speech if Kokoro unavailable

### Integration Points
- **demerzel-bot**: Discord voice channel playback (Phase 2.5)
- **Jarvis desktop**: Local speaker output (Phase 4)
- **Governance reports**: Spoken audit summaries
- **Algedonic alerts**: Audible warnings for governance violations

## Checklist

- [ ] Install Kokoro-82M (Apache 2.0, 82M params)
- [ ] ONNX Runtime inference on RTX 5080
- [ ] Wire into demerzel-bot (respond with audio in Discord)
- [ ] Voice personality tuning (warm, precise, Demerzel tone)
- [ ] Fallback: Bark (MIT) for expressive speech

## Governance

- **Constitutional**: Article 8 (Observability) — voice output is an observability channel
- **Policy**: No PII in synthesized speech without explicit consent
- **Reversibility**: Audio is ephemeral in voice channels, logged as text source only

## Dependencies

- RTX 5080 GPU (local inference)
- ONNX Runtime with CUDA
- Kokoro-82M model weights
