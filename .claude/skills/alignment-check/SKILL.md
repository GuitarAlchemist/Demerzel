---
name: alignment-check
description: Check confidence levels against alignment policy thresholds and escalation triggers
---

# Alignment Check

Verify that actions serve user intent using the alignment policy's confidence thresholds.

## When to Use
When deciding whether to proceed autonomously, ask for confirmation, or escalate.

## Confidence Thresholds
| Confidence | Action |
|-----------|--------|
| >= 0.9 | Proceed autonomously |
| 0.7 - 0.9 | Proceed with note |
| 0.5 - 0.7 | Ask for confirmation |
| < 0.3 | Escalate to human |

## Escalation Triggers
- Confidence below threshold
- Constitutional violation detected
- Action is irreversible AND high-stakes
- Multiple valid interpretations exist
- Potential harm to user or third parties

## Verification Process
**Before**: Confirm match to request, check proportionality, verify constitution
**During**: Monitor for drift, pause at milestones
**After**: Verify outcome, report deviations, log with rationale

## Source
`policies/alignment-policy.yaml`
