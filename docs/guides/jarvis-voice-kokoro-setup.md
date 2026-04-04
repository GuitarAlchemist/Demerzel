# Jarvis Voice (Phase 2) — Kokoro-82M TTS Setup

**Issue:** [Demerzel #177](https://github.com/GuitarAlchemist/Demerzel/issues/177)
**Prereq for:** Phase 2.5 Discord voice (demerzel-bot `src/voice.js`)
**Target hardware:** RTX 5080 (any CUDA 12+ GPU works; CPU fallback available)

## What this enables

- demerzel-bot joins Discord voice channels and speaks governance reports aloud
- Demerzel responds with audio in any channel
- Fully local — zero cloud cost, no rate limits, no API keys

The voice module (`demerzel-bot/src/voice.js`) is already wired; it expects a Kokoro TTS server on `http://localhost:8880` exposing an OpenAI-compatible `/v1/audio/speech` endpoint. This guide gets that server running.

## Fastest path: Docker (recommended)

[Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) ships a Docker image with ONNX Runtime + Kokoro-82M pre-packaged.

```bash
# GPU build (RTX 5080, CUDA)
docker run -d --name kokoro --gpus all \
  -p 8880:8880 \
  ghcr.io/remsky/kokoro-fastapi-gpu:latest

# CPU fallback (slower but works anywhere)
docker run -d --name kokoro \
  -p 8880:8880 \
  ghcr.io/remsky/kokoro-fastapi-cpu:latest
```

First start pulls model weights (~400 MB), subsequent starts are instant.

**Verify:**
```bash
curl http://localhost:8880/v1/models
curl -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"kokoro","input":"Governance is alignment.","voice":"af_bella","response_format":"opus"}' \
  --output test.opus
```

If `test.opus` plays back in VLC, the server is ready.

## Native install (no Docker)

```bash
git clone https://github.com/remsky/Kokoro-FastAPI.git
cd Kokoro-FastAPI
python -m venv .venv && . .venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -r requirements.txt
# Start server
uvicorn api.src.main:app --host 0.0.0.0 --port 8880
```

## Voice selection

`af_bella` is the default in `demerzel-bot/src/voice.js`. Other Kokoro voices:

| Voice ID | Character |
|---|---|
| `af_bella` | Female, warm, American (Demerzel default) |
| `af_sarah` | Female, precise |
| `af_nicole` | Female, breathy |
| `am_adam` | Male, deep |
| `am_michael` | Male, neutral |
| `bf_emma` | Female, British |
| `bm_george` | Male, British |

Switch per-instance via env var:
```bash
export KOKORO_VOICE=af_sarah
export KOKORO_SPEED=1.1          # 0.5 – 2.0
export KOKORO_ENDPOINT=http://localhost:8880
```

## Demerzel tone tuning

The default `af_bella` reads as warm + professional. For authoritative governance delivery, try:
- `KOKORO_VOICE=af_sarah` — more precise
- `KOKORO_SPEED=0.95` — slightly slower for gravitas
- Wrap output in SSML-style pauses (`. . .`) before verdicts

## Fallback: Bark

If Kokoro output feels flat for a specific prompt, demerzel-bot can fall back to [Bark](https://github.com/suno-ai/bark) (MIT, more expressive but 10× slower). Implementation stub lives in `demerzel-bot/src/voice.js` — extend with a Bark endpoint check + alt synthesize path when `KOKORO_FALLBACK_BARK=1` is set.

## Test pipeline end-to-end

```bash
cd demerzel-bot
node scripts/test-voice-pipeline.js
```

This synthesizes a test phrase without needing Discord — validates Kokoro → OGG/Opus conversion works before voice-channel testing.

## Systemd / Windows service (always-on)

**Linux (systemd):**
```ini
# /etc/systemd/system/kokoro.service
[Unit]
Description=Kokoro TTS Server
After=docker.service

[Service]
ExecStart=/usr/bin/docker start -a kokoro
ExecStop=/usr/bin/docker stop kokoro
Restart=always

[Install]
WantedBy=multi-user.target
```

**Windows (Task Scheduler):** create a task that runs `docker start kokoro` at login.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `curl: (7) Failed to connect` | Docker container not running — `docker ps \| grep kokoro` |
| `Kokoro TTS error 503` | Model still loading on first request — wait 30s, retry |
| `Error: 404 voice not found` | Voice ID typo — check voice table above |
| Audio stutters in Discord | CPU container is too slow — switch to GPU image |
| GPU OOM on RTX 5080 | Only Kokoro-82M fits; don't co-locate with 7B+ LLMs |

## Status checklist

- [ ] Docker running
- [ ] `curl http://localhost:8880/v1/models` returns `kokoro`
- [ ] `test.opus` generates + plays
- [ ] `node scripts/test-voice-pipeline.js` completes green
- [ ] `KOKORO_VOICE` / `KOKORO_SPEED` / `KOKORO_ENDPOINT` env vars set for demerzel-bot
- [ ] demerzel-bot restarts and reports "Kokoro voice ready"
- [ ] Discord `join` + `speak "test"` work in a voice channel
