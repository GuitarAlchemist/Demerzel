#!/usr/bin/env python3
"""Regression guard for the Mission Control snapshot generator (S0 #742).

Runs under `python -m unittest discover -s scripts` (no pytest). Covers status
classification, deterministic counts, schema conformance, Markdown rendering, and
that the committed docs/status/mission-control.json is the generator's output for
the committed fixture (so it cannot silently drift back to a hand-authored file).
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from mission_control_snapshot import build_snapshot, classify_issue, render_markdown, validate_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "fixtures" / "mission-control" / "sprint-0.json"
GENERATED = REPO_ROOT / "docs" / "status" / "mission-control.json"


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class ClassifyTests(unittest.TestCase):
    def test_closed_is_done(self):
        self.assertEqual(classify_issue({"state": "closed"}), "done")

    def test_blocked_label_beats_ready(self):
        self.assertEqual(
            classify_issue({"state": "open", "labels": ["ready-for-agent", "blocked"]}),
            "blocked",
        )

    def test_ready_is_executable(self):
        self.assertEqual(classify_issue({"state": "open", "labels": ["ready-for-human"]}), "executable")

    def test_open_default_is_planned(self):
        self.assertEqual(classify_issue({"state": "open", "labels": ["component:demerzel"]}), "planned")


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.data = _load(FIXTURE)
        self.snapshot = build_snapshot(self.data)

    def test_counts_are_deterministic(self):
        s = self.snapshot
        self.assertEqual(s["total_nodes"], 10)
        self.assertEqual(s["completed_nodes"], 5)
        self.assertEqual(s["blocked_nodes"], 1)
        self.assertEqual(s["executable_nodes"], 3)
        self.assertEqual(s["percent_complete"], 50.0)

    def test_counts_partition_total(self):
        by_status = self.snapshot["dashboard"]["issues_by_status"]
        self.assertEqual(sum(by_status.values()), self.snapshot["total_nodes"])

    def test_dashboard_pr_metrics(self):
        d = self.snapshot["dashboard"]
        self.assertEqual(d["open_prs"], 2)
        self.assertEqual(d["merged_prs"], 2)
        self.assertEqual(d["draft_prs"], 1)
        self.assertEqual(d["review_queue"], 1)

    def test_snapshot_validates_against_schema(self):
        self.assertTrue(validate_snapshot(self.snapshot))

    def test_later_slice_fields_empty_in_s0(self):
        self.assertEqual(self.snapshot["critical_path"], [])
        self.assertIsNone(self.snapshot["eta"])
        self.assertEqual(self.snapshot["risks"], [])
        self.assertEqual(self.snapshot["recommendations"], [])

    def test_empty_input_gives_zero_percent(self):
        snap = build_snapshot({"observed_at": "2026-07-18T00:00:00Z", "issues": [], "pull_requests": []})
        self.assertEqual(snap["total_nodes"], 0)
        self.assertEqual(snap["percent_complete"], 0.0)

    def test_markdown_renders_key_numbers(self):
        md = render_markdown(self.snapshot)
        self.assertIn("50.0% complete", md)
        self.assertIn("| Merged PRs | 2 |", md)


class GeneratedFileTests(unittest.TestCase):
    def test_committed_mission_control_matches_generator(self):
        # The committed status file must BE the generator's output for the fixture,
        # not a hand-authored artifact (the LOLLI failure mode S0 exists to kill).
        self.assertTrue(GENERATED.exists(), "docs/status/mission-control.json missing")
        expected = build_snapshot(_load(FIXTURE))
        self.assertEqual(_load(GENERATED), expected)


if __name__ == "__main__":
    unittest.main()
