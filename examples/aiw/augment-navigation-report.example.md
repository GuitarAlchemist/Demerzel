# Example AIW job — Augment navigation report

Augment's primary lane is `navigator` (`navigate`-class): read-only repo
intelligence that informs grooming and fan-in decisions. Under `NORMAL` fan-out
the selector should **allow** it.

```json
{ "worker": "augment", "requested_role": "navigator", "fan_out_mode": "NORMAL", "subject": "issue" }
```

Expected decision: allow

Augment primarily *informs* decisions; `merge_decider` and `policy_override_actor`
are **forbidden** for this lane.
