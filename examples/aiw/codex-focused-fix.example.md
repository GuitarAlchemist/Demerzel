# Example AIW job — Codex focused fix under CONSTRAINED

Codex's primary lane is `focused_patch_helper` (`fix`-class). Under `CONSTRAINED`
fan-out only net-new feature and broad-architecture work are reduced, so a focused
fix is still allowed. The selector should **allow** it.

```json
{ "worker": "codex", "requested_role": "focused_patch_helper", "fan_out_mode": "CONSTRAINED", "subject": "worker_task" }
```

Expected decision: allow

Codex runs inside explicit issue/job constraints; `broad_architecture_owner` is a
**forbidden** role for this lane.
