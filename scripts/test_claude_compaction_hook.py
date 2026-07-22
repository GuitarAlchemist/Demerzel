#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from claude_compaction_hook import handle, project_setting_status, sha256_text
from query_compaction_telemetry import build_query


class ClaudeCompactionHookTests(unittest.TestCase):
    def test_summary_is_hashed_not_persisted_and_duckdb_can_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text(
                json.dumps({"env": {"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "40"}}),
                encoding="utf-8",
            )
            log_path = root / "events.jsonl"
            payload = {
                "hook_event_name": "PostCompact",
                "session_id": "ix-live",
                "cwd": str(root),
                "trigger": "auto",
                "transcript_path": "C:/private/transcript.jsonl",
                "compact_summary": "secret summary body",
            }
            with patch(
                "claude_compaction_hook.repository_identity",
                return_value=("ix", "feat/fleet", root),
            ):
                row = handle(payload, log_path)

            self.assertIsNotNone(row)
            assert row is not None
            self.assertEqual(row["project_setting"], "supported")
            self.assertEqual(row["summary_chars"], len("secret summary body"))
            self.assertEqual(row["summary_sha256"], sha256_text("secret summary body"))
            persisted = log_path.read_text(encoding="utf-8")
            self.assertNotIn("secret summary body", persisted)
            self.assertNotIn("C:/private/transcript.jsonl", persisted)

    def test_obsolete_project_setting_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text(
                json.dumps(
                    {"env": {"CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE": "40"}}
                ),
                encoding="utf-8",
            )
            with patch(
                "claude_compaction_hook.repository_identity",
                return_value=("ga", "main", root),
            ):
                row = handle(
                    {
                        "hook_event_name": "PreCompact",
                        "session_id": "ga-live",
                        "cwd": str(root),
                        "trigger": "auto",
                    },
                    root / "events.jsonl",
                )
            assert row is not None
            self.assertEqual(row["project_setting"], "obsolete-key")

    def test_obsolete_project_setting_wins_when_both_keys_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text(
                json.dumps(
                    {
                        "env": {
                            "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "40",
                            "CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE": "40",
                        }
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(project_setting_status(root), "obsolete-key")

    def test_duckdb_filter_query_executes(self) -> None:
        duckdb = shutil.which("duckdb")
        if not duckdb:
            self.skipTest("duckdb CLI is not installed")
        with tempfile.TemporaryDirectory() as temp:
            log_path = Path(temp) / "events.jsonl"
            rows = [
                {
                    "repo": "ix",
                    "event": "post_compact",
                    "ts": "2026-07-22T00:00:00Z",
                    "project_setting": "supported",
                },
                {
                    "repo": "ix",
                    "event": "session_rehydrated",
                    "ts": "2026-07-22T00:01:00Z",
                    "project_setting": "obsolete-key",
                },
            ]
            log_path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            query = build_query(log_path.resolve().as_posix().replace("'", "''"))
            result = subprocess.run(
                [duckdb, "-json", "-c", query],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            metrics = json.loads(result.stdout)
            self.assertEqual(metrics[0]["completed_compactions"], 1)
            self.assertEqual(metrics[0]["recoveries"], 1)
            self.assertEqual(metrics[0]["obsolete_project_setting"], "obsolete-key")

    def test_unrelated_hook_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = handle(
                {"hook_event_name": "PostToolUse", "session_id": "noop"},
                Path(temp) / "events.jsonl",
            )
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
