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

from mission_control_snapshot import (
    agent_telemetry,
    build_snapshot,
    capability_progress,
    classify_issue,
    load_capability_map,
    load_events,
    render_markdown,
    validate_snapshot,
)

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


class CapabilityTests(unittest.TestCase):
    MAP = {
        "observability": ["area:observability", "component:streeling"],
        "planner": ["area:planner"],
        "intelligence": ["component:seldon"],
    }

    def test_issue_counts_toward_matching_capability(self):
        issues = [{"state": "closed", "labels": ["area:planner"]}]
        rows = {r["capability"]: r for r in capability_progress(issues, self.MAP)}
        self.assertEqual(rows["planner"]["completed_nodes"], 1)
        self.assertEqual(rows["planner"]["percent_complete"], 100.0)

    def test_issue_can_count_toward_several_capabilities(self):
        # a streeling+observability issue matches observability via either label
        issues = [{"state": "open", "labels": ["component:streeling", "area:observability", "ready-for-agent"]}]
        rows = {r["capability"]: r for r in capability_progress(issues, self.MAP)}
        self.assertEqual(rows["observability"]["total_nodes"], 1)
        self.assertEqual(rows["observability"]["executable_nodes"], 1)

    def test_capability_without_matches_reports_zero_not_dropped(self):
        rows = {r["capability"]: r for r in capability_progress([], self.MAP)}
        self.assertIn("intelligence", rows)
        self.assertEqual(rows["intelligence"]["total_nodes"], 0)
        self.assertEqual(rows["intelligence"]["percent_complete"], 0.0)

    def test_capability_order_is_stable(self):
        rows = capability_progress([], self.MAP)
        self.assertEqual([r["capability"] for r in rows], list(self.MAP.keys()))

    def test_canonical_map_covers_ten_capabilities(self):
        self.assertEqual(len(load_capability_map()), 10)


class SprintZeroCapabilityTests(unittest.TestCase):
    def test_fixture_capability_breakdown(self):
        snap = build_snapshot(_load(FIXTURE))
        rows = {r["capability"]: r for r in snap["capabilities"]}
        self.assertEqual(rows["planner"]["percent_complete"], 100.0)   # #531 #533 #584 done
        self.assertEqual(rows["observability"]["total_nodes"], 5)
        self.assertEqual(rows["observability"]["completed_nodes"], 1)  # #545
        self.assertEqual(rows["governance"]["completed_nodes"], 1)     # #515 done, #588 planned


class TelemetryTests(unittest.TestCase):
    EVENTS = [
        {"worker": "claude", "event_type": "pr", "metadata": {"action": "opened"}},
        {"worker": "claude", "event_type": "pr", "metadata": {"action": "merged"}},
        {"worker": "gemini", "event_type": "review"},
        {"worker": "github-actions", "event_type": "workflow", "severity": "success"},
        {"worker": "github-actions", "event_type": "workflow", "severity": "info"},
    ]

    def setUp(self):
        self.rows = {r["worker"]: r for r in agent_telemetry(self.EVENTS)}

    def test_pr_open_and_merge_counted(self):
        self.assertEqual(self.rows["claude"]["prs_opened"], 1)
        self.assertEqual(self.rows["claude"]["prs_merged"], 1)

    def test_review_counted(self):
        self.assertEqual(self.rows["gemini"]["reviews"], 1)

    def test_ci_success_rate_computed(self):
        self.assertEqual(self.rows["github-actions"]["workflow_runs"], 2)
        self.assertEqual(self.rows["github-actions"]["ci_success_rate"], 0.5)

    def test_ci_rate_null_without_runs(self):
        # gemini has no workflow events -> rate is unknown, not 0.0
        self.assertIsNone(self.rows["gemini"]["ci_success_rate"])

    def test_unmeasured_metrics_listed_not_guessed(self):
        self.assertIn("cost", self.rows["claude"]["unmeasured"])
        self.assertIn("human_rescue_rate", self.rows["claude"]["unmeasured"])

    def test_all_known_workers_reported(self):
        self.assertEqual(len(self.rows), 7)
        for worker in ("claude", "jules", "gemini", "codex", "augment", "github-actions", "human"):
            self.assertIn(worker, self.rows)

    def test_telemetry_reads_streeling_store(self):
        # the default source is the committed Streeling sample (#545) — the wiring
        events = load_events()
        self.assertTrue(events, "telemetry should read the Streeling event store")
        rows = {r["worker"]: r for r in agent_telemetry(events)}
        self.assertEqual(rows["claude"]["prs_opened"], 1)
        self.assertEqual(rows["github-actions"]["ci_success_rate"], 1.0)


class GeneratedFileTests(unittest.TestCase):
    def test_committed_mission_control_matches_generator(self):
        # The committed status file must BE the generator's output for the fixture,
        # not a hand-authored artifact (the LOLLI failure mode S0 exists to kill).
        self.assertTrue(GENERATED.exists(), "docs/status/mission-control.json missing")
        expected = build_snapshot(_load(FIXTURE))
        self.assertEqual(_load(GENERATED), expected)


if __name__ == "__main__":
    unittest.main()
