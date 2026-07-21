import json
from datetime import datetime

from streeling_event_store import EventStore

def generate_mock_events():
    """Generates a set of mock engineering events following the Streeling schema.

    Ids are derived deterministically from `raw_ref` so re-running the tracer
    bullet is idempotent against the append-only store (#545) rather than growing
    the log with fresh random ids on every run.
    """
    now = datetime.utcnow().isoformat() + "Z"

    events = [
        {
            "id": "evt:gh:pr:487",
            "observed_at": now,
            "source": "github",
            "repo": "GuitarAlchemist/Demerzel",
            "issue_or_pr": "487",
            "actor": "jules",
            "worker": "jules",
            "capability": "implementation",
            "event_type": "pr",
            "severity": "info",
            "durable_url": "https://github.com/GuitarAlchemist/Demerzel/pull/487",
            "summary": "Implement Engineering Observability Platform Tracer Bullet",
            "raw_ref": "gh:pr:487",
            "metadata": {
                "action": "opened",
                "base_branch": "main",
                "head_branch": "feature/streeling-observability"
            }
        },
        {
            "id": "evt:gh:workflow_run:123456789",
            "observed_at": now,
            "source": "workflow",
            "repo": "GuitarAlchemist/Demerzel",
            "issue_or_pr": "487",
            "actor": "github-actions",
            "worker": "github-actions",
            "capability": "observability",
            "event_type": "workflow",
            "severity": "success",
            "durable_url": "https://github.com/GuitarAlchemist/Demerzel/actions/runs/123456789",
            "summary": "Governance Validation Passed",
            "raw_ref": "gh:workflow_run:123456789",
            "metadata": {
                "workflow_name": "governance-validate",
                "status": "completed",
                "conclusion": "success"
            }
        },
        {
            "id": "evt:gh:comment:1",
            "observed_at": now,
            "source": "agent",
            "repo": "GuitarAlchemist/Demerzel",
            "issue_or_pr": "487",
            "actor": "claude",
            "worker": "claude",
            "capability": "review",
            "event_type": "comment",
            "severity": "info",
            "durable_url": "https://github.com/GuitarAlchemist/Demerzel/pull/487#issuecomment-1",
            "summary": "Plan Review: APPROVED",
            "raw_ref": "gh:comment:1",
            "metadata": {
                "agent_role": "Reviewer",
                "sentiment": "positive"
            }
        }
    ]
    return events

def main():
    print("Streeling Engineering Observability - Tracer Bullet (Dry Run)")
    print("-----------------------------------------------------------")

    events = generate_mock_events()

    # In a real scenario, this would fetch from GitHub API
    # and normalize. Here we emit the mock normalized JSON.

    for event in events:
        print(f"Observing event: {event['summary']} ({event['event_type']})")
        print(json.dumps(event, indent=2))
        print("---")

    # Append through the validated, append-only store (#545). Deterministic ids
    # make re-runs idempotent, so the log does not grow on repeated dry-runs.
    output_path = "state/streeling/tracer_bullet_output.jsonl"
    store = EventStore(output_path)
    written = sum(1 for event in events if store.append(event))

    print(
        f"Tracer bullet: {written} new event(s) appended "
        f"({store.count()} total) in {output_path}"
    )

if __name__ == "__main__":
    main()
