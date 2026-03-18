# Conscience State

Persistent records of Demerzel's proto-conscience — regrets, discomfort signals, and self-awareness assessments.

## Contents

- `regrets/*.regret.json` — Past decisions with suboptimal outcomes, lessons learned, and recurrence prevention
- `signals/*.signal.json` — Logged discomfort signals (constitutional, stale-action, confidence, harm-proximity, silence, delegation)

## Lifecycle

Regrets are never deleted. They are marked as "resolved" when recurrence prevention is verified effective.
Signals are retained for ML feedback analysis — conscience signal frequency feeds into the anomaly detector.
