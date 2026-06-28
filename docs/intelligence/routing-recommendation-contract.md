# Routing Recommendation Contract

Seldon emits advisory routing recommendations to Demerzel. These recommendations are based on observed worker performance (capability scoring) and task requirements.

## Contract Specification

The routing recommendation is a JSON object following the [Routing Recommendation Schema](../schemas/routing-recommendation.schema.json).

### Key Fields

| Field | Description | Importance |
|---|---|---|
| **issue_or_pr** | Context identifier. | Essential for linkage. |
| **required_capability** | The primary skill needed. | Determines the worker pool. |
| **recommended_worker** | The top-ranked worker. | The primary advice. |
| **confidence** | Seldon's certainty (0.0-1.0). | Informs Demerzel's decision weight. |
| **rationale** | Human-readable justification. | Auditability and transparency. |
| **human_review_required** | Safety override. | Critical for high-risk tasks. |

## Recommendation Logic

Seldon generates recommendations by:
1. **Identifying required capability** from the issue/PR description and labels.
2. **Filtering the worker pool** for those possessing the capability.
3. **Ranking workers** using a weighted combination of:
   - `historical_success` (from Capability Score)
   - `overall_reliability_score` (from Worker Reliability)
   - `cost_per_success` (Efficiency target)
   - `median_cycle_time` (Speed target)
4. **Assessing risk:** If the task touches security-critical files or constitutional logic, `human_review_required` is set to `true`.

## Interaction Flow

1. **Trigger:** A new issue or PR is opened.
2. **Analysis:** Seldon processes the event and identifies task parameters.
3. **Emission:** Seldon writes a `RoutingRecommendation` to `state/seldon/recommendations/<id>.json`.
4. **Decision:** Demerzel's driver reads the recommendation as part of its `Step 0` triage and applies policy logic to select the final worker.

## Example

```json
{
  "issue_or_pr": "ga#482",
  "required_capability": "implementation",
  "recommended_worker": "jules",
  "backup_workers": ["claude", "gemini"],
  "confidence": 0.92,
  "rationale": "Jules has a 95% success rate on .NET implementation tasks with a median cycle time of 15 minutes.",
  "cost_notes": "Lowest cost per merged PR for this capability.",
  "risk_notes": "None identified.",
  "human_review_required": false,
  "timestamp": "2026-06-25T14:30:00Z"
}
```
