import json
import uuid
from datetime import datetime

def generate_mock_events():
    """Generates a set of mock engineering events following the Streeling schema."""
    now = datetime.utcnow().isoformat() + "Z"

    events = [
        {
            "id": str(uuid.uuid4()),
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
            "id": str(uuid.uuid4()),
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
            "id": str(uuid.uuid4()),
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

    # Save to a mock state file
    output_path = "state/streeling/tracer_bullet_output.jsonl"
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"Tracer bullet results saved to {output_path}")

if __name__ == "__main__":
    main()
