# Example AIW job — Gemini read-only Critic review

Gemini's primary lane is `read_only_critic` (see `docs/workflows/aiw-composite-lanes.md`).
This request asks it to review a pull request while fan-out is `NORMAL`. The advisory
lane selector (`scripts/aiw_lane_selector.py`) should **allow** it.

```json
{ "worker": "gemini", "requested_role": "read_only_critic", "fan_out_mode": "NORMAL", "subject": "pull_request" }
```

Expected decision: allow

Note: requesting `code_pusher` from Gemini is **blocked** (`CAPABILITY.FORBIDDEN_ROLE`) —
the Critic lane is read-only and may not push commits, aligning with #485.
