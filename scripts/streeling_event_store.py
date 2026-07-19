#!/usr/bin/env python3
"""Streeling append-only engineering-event store (#545, parent #519).

The smallest useful Streeling slice: validate a normalized EngineeringEvent
against `schemas/streeling/engineering-event.schema.json`, then append it to a
line-delimited JSON (JSONL) log. The store is **append-only by construction** —
it exposes append/read only, no update or delete — matching
`docs/architecture/streeling-event-store.md`.

Idempotency keys on the event `id` (the schema's unique identifier). The
architecture doc keys webhook idempotency on `delivery_id` (X-GitHub-Delivery),
but the webhook envelope is out of scope for #545 (see #543 / #519); `id` is the
in-scope analog.

Out of scope (per #545): webhook server, GitHub App integration, org/repo/date
partitioning, and any optimization logic. Single flat JSONL file, stdlib +
`jsonschema` only.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "schemas" / "streeling" / "engineering-event.schema.json"
)


def _load_schema():
    with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_SCHEMA = _load_schema()


def validate_event(event):
    """Validate one event against the engineering-event schema.

    Returns (True, None) when valid, else (False, human-readable message).
    """
    try:
        jsonschema.validate(event, _SCHEMA)
        return True, None
    except jsonschema.exceptions.ValidationError as exc:
        return False, exc.message


class EventStore:
    """Append-only JSONL store for Streeling engineering events."""

    def __init__(self, path):
        self.path = Path(path)

    def read_all(self):
        """Yield stored events in append order. Empty if the log does not exist."""
        if not self.path.exists():
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def ids(self):
        """Return the set of event ids currently in the log."""
        return {event.get("id") for event in self.read_all()}

    def count(self):
        """Return the number of events currently in the log."""
        return sum(1 for _ in self.read_all())

    def append(self, event):
        """Validate, dedupe by ``id``, and append one JSONL line.

        Returns True when the event was written, False when it was skipped as a
        duplicate id. Raises ValueError when the event fails schema validation
        (the invalid event is never written).
        """
        ok, message = validate_event(event)
        if not ok:
            raise ValueError(f"invalid engineering event: {message}")

        if event.get("id") in self.ids():
            return False

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
        return True
