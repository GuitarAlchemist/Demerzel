"""Replay the bounded CYB-003 counts from a pinned Demerzel commit."""

from __future__ import annotations

import json
import math
import subprocess
from collections import Counter


REVISION = "66083fc684b57a12ef307c19c3819d91c551295f"
RECORD_DIRECTORY = "state/streeling/course-productions"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, text=True, capture_output=True
    ).stdout


def main() -> None:
    schema = json.loads(git("show", f"{REVISION}:schemas/course-production.schema.json"))
    statuses = schema["properties"]["status"]["enum"]
    verdicts = schema["properties"]["phases"]["properties"]["review"]["properties"]["verdict"]["enum"]
    paths = [
        path for path in git("ls-tree", "-r", "--name-only", REVISION, "--", RECORD_DIRECTORY).splitlines()
        if path.endswith(".json")
    ]
    records = [json.loads(git("show", f"{REVISION}:{path}")) for path in paths]
    observed = Counter(record["status"] for record in records)
    verdict_count = sum("verdict" in record.get("phases", {}).get("review", {}) for record in records)
    entropy = -sum((count / len(records)) * math.log2(count / len(records)) for count in observed.values())

    assert len(statuses) == 5 and len(verdicts) == 3
    assert len(records) == 8
    assert observed == {"in_progress": 7, "review_pending": 1}
    assert verdict_count == 0
    assert math.isclose(entropy, 0.5435644431995964)
    print(json.dumps({
        "revision": REVISION,
        "configured_status_labels": len(statuses),
        "configured_review_verdict_labels": len(verdicts),
        "record_count": len(records),
        "observed_statuses": dict(observed),
        "records_with_review_verdict": verdict_count,
        "sample_status_entropy_bits": round(entropy, 6),
    }, indent=2))


if __name__ == "__main__":
    main()
