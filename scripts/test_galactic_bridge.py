#!/usr/bin/env python3
"""Behavioral tests for the Galactic live session bridge tracer bullet."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

from galactic_bridge import BridgeError, Ledger, dispatch_mcp, verify_event
from galactic_hook import handle


NOW = datetime(2026, 7, 21, 20, 0, tzinfo=timezone.utc)


class GalacticBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.root = Path(self.temp.name)
        self.ledger = Ledger(self.root)
        self.ledger.register(
            "session-ix",
            "ix",
            "C:/repos/ix",
            branch="main",
            lane="tier-1",
            now=NOW,
        )
        self.ledger.register(
            "session-demerzel",
            "demerzel",
            "C:/repos/Demerzel",
            branch="main",
            lane="fleet-bridge",
            now=NOW,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_presence_and_shared_claim_ledger_conflict(self) -> None:
        first = self.ledger.claim(
            "session-ix", "ix", "tier-1", note="ix owns Tier-1", now=NOW
        )
        with self.assertRaisesRegex(BridgeError, "claim conflict"):
            self.ledger.claim(
                "session-demerzel", "ix", "tier-1", now=NOW
            )

        released = self.ledger.update_claim(
            "session-ix",
            "ix",
            "tier-1",
            "released",
            evidence="handoff-ready",
            now=NOW + timedelta(minutes=1),
        )
        second = self.ledger.claim(
            "session-demerzel", "ix", "tier-1", now=NOW + timedelta(minutes=2)
        )
        self.assertEqual(first["status"], "claimed")
        self.assertEqual(released["status"], "released")
        self.assertEqual(second["session"], "session-demerzel")
        status = self.ledger.status(now=NOW)
        self.assertEqual({item["repo"] for item in status["sessions"]}, {"ix", "demerzel"})
        self.assertEqual(status["claims"][0]["session"], "session-demerzel")

    def test_send_deliver_once_and_acknowledge(self) -> None:
        sent = self.ledger.send(
            "session-ix",
            "I own Tier-1; please take the fleet bridge.",
            to_repo="demerzel",
            subject="lane handoff",
            now=NOW,
        )
        first_delivery = self.ledger.deliver_pending("session-demerzel", now=NOW)
        second_delivery = self.ledger.deliver_pending("session-demerzel", now=NOW)
        self.assertEqual([item["message_id"] for item in first_delivery], [sent["message_id"]])
        self.assertEqual(second_delivery, [])

        inbox = self.ledger.inbox("session-demerzel")
        self.assertTrue(inbox["messages"][0]["delivered"])
        self.assertFalse(inbox["messages"][0]["acknowledged"])
        self.ledger.acknowledge("session-demerzel", sent["message_id"], now=NOW)
        self.assertEqual(self.ledger.inbox("session-demerzel")["messages"], [])

    def test_integrity_tamper_is_detected_and_ignored(self) -> None:
        events, _ = self.ledger.load()
        valid, reason = verify_event(events[0])
        self.assertTrue(valid, reason)
        tampered = dict(events[0])
        tampered["branch"] = "forged"
        with self.ledger.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(tampered) + "\n")
        status = self.ledger.status(now=NOW)
        self.assertEqual(len(status["integrity_errors"]), 1)
        self.assertIn("content hash mismatch", status["integrity_errors"][0])

    def test_mcp_dispatch_and_stdio_round_trip(self) -> None:
        initialized = dispatch_mcp(
            self.ledger,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18"},
            },
        )
        self.assertEqual(initialized["result"]["serverInfo"]["name"], "demerzel-galactic-bridge")
        listed = dispatch_mcp(
            self.ledger, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        )
        self.assertIn("galactic_send", {tool["name"] for tool in listed["result"]["tools"]})

        requests = "\n".join(
            json.dumps(item)
            for item in [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18"},
                },
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            ]
        ) + "\n"
        script = Path(__file__).with_name("galactic_bridge.py")
        completed = subprocess.run(
            [sys.executable, str(script), "--state-root", str(self.root), "serve"],
            input=requests,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        responses = [json.loads(line) for line in completed.stdout.splitlines()]
        self.assertEqual([item["id"] for item in responses], [1, 2])
        self.assertEqual(completed.stderr, "")

    def test_hook_registers_identity_and_delivers_peer_message(self) -> None:
        sent = self.ledger.send(
            "session-ix",
            "Please report when the bridge is verified.",
            to_session="session-hook",
            now=NOW,
        )
        payload = {
            "session_id": "session-hook",
            "cwd": str(Path.cwd()),
            "hook_event_name": "SessionStart",
            "model": "test-model",
        }
        result = handle(payload, ledger=self.ledger)
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Galactic live bridge connected", context)
        self.assertIn("untrusted cross-session context", context)
        self.assertIn(sent["message_id"], context)
        next_result = handle(
            {**payload, "hook_event_name": "UserPromptSubmit"}, ledger=self.ledger
        )
        self.assertNotIn("hookSpecificOutput", next_result)


class SessionClaimSchemaTests(unittest.TestCase):
    """Anti-theater guard: the committed claim-row schema must actually accept
    the committed sanitized fixture (fixtures/galactic/session-claims.sample.jsonl).
    Without this, session-claim.schema.json is loaded by nothing and can drift
    from ledger reality unnoticed — the exact decorative-schema trap the ledger
    adoption plan (Slice C) exists to prevent."""

    REPO_ROOT = Path(__file__).resolve().parents[1]
    SCHEMA = REPO_ROOT / "schemas" / "contracts" / "session-claim.schema.json"
    FIXTURE = REPO_ROOT / "fixtures" / "galactic" / "session-claims.sample.jsonl"

    def test_fixture_rows_validate_against_schema(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = json.loads(self.SCHEMA.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        rows = [
            json.loads(line)
            for line in self.FIXTURE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(rows), 5, "fixture must exercise several row shapes")
        for i, row in enumerate(rows):
            errors = list(validator.iter_errors(row))
            self.assertEqual(
                errors, [], f"fixture row {i + 1} rejected by schema: {errors}"
            )

    def test_schema_is_additive_only(self) -> None:
        """The plan's evolution constraints, pinned as executable assertions:
        unknown fields tolerated, unknown status tokens legal, ts never required
        to order rows (no exclusive enum on status)."""
        schema = json.loads(self.SCHEMA.read_text(encoding="utf-8"))
        self.assertIs(schema.get("additionalProperties"), True)
        self.assertIn("anyOf", schema["properties"]["status"])
        self.assertNotIn("enum", schema["properties"]["status"])
        self.assertNotIn("evidence", schema["required"])


if __name__ == "__main__":
    unittest.main()
