#!/usr/bin/env python3
"""Regression guard for the Streeling append-only event store (#545).

Runs under `python -m unittest discover -s scripts` (no pytest). Asserts the
store validates before writing, is append-only, dedupes by id, and that the
committed sample fixtures conform to the schema.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from streeling_event_store import EventStore, validate_event

REPO_ROOT = Path(__file__).resolve().parents[1]
# Sample set conforming to engineering-event.schema.json (the #545 EngineeringEvent
# model). NOTE: fixtures/streeling/sample_events.jsonl is a separate, pre-schema
# envelope (event_id/data shape) and is intentionally NOT validated here —
# reconciling the two models is #517 (engineering ontology v1) scope.
SAMPLE_FIXTURE = REPO_ROOT / "fixtures" / "streeling" / "engineering-events-sample.jsonl"


def _event(event_id="evt:1", **overrides):
    base = {
        "id": event_id,
        "observed_at": "2026-07-18T12:00:00Z",
        "source": "github",
        "repo": "GuitarAlchemist/Demerzel",
        "actor": "claude",
        "worker": "claude",
        "capability": "implementation",
        "event_type": "pr",
        "severity": "info",
        "summary": "test event",
    }
    base.update(overrides)
    return base


class ValidationTests(unittest.TestCase):
    def test_valid_event_passes(self):
        ok, message = validate_event(_event())
        self.assertTrue(ok, message)

    def test_missing_required_field_fails(self):
        bad = _event()
        del bad["summary"]
        ok, message = validate_event(bad)
        self.assertFalse(ok)
        self.assertIsNotNone(message)

    def test_bad_enum_fails(self):
        ok, _ = validate_event(_event(worker="skynet"))
        self.assertFalse(ok)

    def test_unknown_field_rejected(self):
        # schema is additionalProperties:false
        ok, _ = validate_event(_event(rogue_field="x"))
        self.assertFalse(ok)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "events.jsonl"
        self.store = EventStore(self.path)

    def tearDown(self):
        self._tmp.cleanup()

    def test_append_then_read_round_trip(self):
        self.assertTrue(self.store.append(_event("evt:1", summary="first")))
        events = list(self.store.read_all())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["summary"], "first")

    def test_invalid_event_raises_and_is_not_written(self):
        with self.assertRaises(ValueError):
            self.store.append(_event(worker="skynet"))
        self.assertEqual(self.store.count(), 0)
        self.assertFalse(self.path.exists())

    def test_idempotent_duplicate_id_skipped(self):
        self.assertTrue(self.store.append(_event("evt:dup", summary="original")))
        self.assertFalse(self.store.append(_event("evt:dup", summary="changed")))
        events = list(self.store.read_all())
        self.assertEqual(len(events), 1)
        # The original line is preserved, not overwritten.
        self.assertEqual(events[0]["summary"], "original")

    def test_append_only_preserves_prior_lines(self):
        self.store.append(_event("evt:1", summary="first"))
        self.store.append(_event("evt:2", summary="second"))
        raw_lines = self.path.read_text(encoding="utf-8").strip().split("\n")
        self.assertEqual(len(raw_lines), 2)
        self.assertEqual(json.loads(raw_lines[0])["summary"], "first")
        self.assertEqual(json.loads(raw_lines[1])["summary"], "second")

    def test_ids_reflects_store(self):
        self.store.append(_event("evt:a"))
        self.store.append(_event("evt:b"))
        self.assertEqual(self.store.ids(), {"evt:a", "evt:b"})


class SampleFixtureTests(unittest.TestCase):
    def test_committed_samples_validate(self):
        self.assertTrue(SAMPLE_FIXTURE.exists(), f"missing fixture {SAMPLE_FIXTURE}")
        count = 0
        with open(SAMPLE_FIXTURE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                count += 1
                ok, message = validate_event(json.loads(line))
                self.assertTrue(ok, f"sample event {count} invalid: {message}")
        self.assertGreater(count, 0, "sample fixture is empty")


if __name__ == "__main__":
    unittest.main()
