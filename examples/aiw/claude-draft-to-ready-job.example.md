# Example AIW job — Claude draft-to-ready under DRAINING

Claude's primary lane is `builder_fixer` (net-new build), which is **blocked** while
fan-out is `DRAINING`. But its secondary `draft_to_ready_helper` role is `fix`-class
work, which stays allowed in DRAINING — so the selector should **recommend** the
fallback rather than block Claude entirely.

```json
{ "worker": "claude", "requested_role": "draft_to_ready_helper", "fan_out_mode": "DRAINING", "subject": "pull_request" }
```

Expected decision: recommend

Contrast: `builder_fixer` in `DRAINING` is **blocked** (`SYSTEM.BACKPRESSURE_HIGH`) —
net-new feature work must wait for fan-out to recover.
