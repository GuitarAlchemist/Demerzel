#!/usr/bin/env python3
"""Tests for the AFK backend adapter contract (scripts/afk_backends/__init__.py)."""
from __future__ import annotations

import unittest
from typing import Any

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from afk_backends import AFKBackend  # noqa: E402


class TestAFKBackendContract(unittest.TestCase):
    """The AFKBackend protocol is an abstract base class. It cannot be used
    directly, and concrete implementations must return the exact shape the
    governor expects."""

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AFKBackend()

    def test_concrete_backend_implements_contract(self):
        class DummyBackend(AFKBackend):
            def prepare(self) -> tuple[bool, str]:
                return True, "ok"

            def needs_local_repo(self) -> bool:
                return True

            def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
                return {"branch": "agent/issue-1", "commits": ["feat: do it"],
                        "blocked": None}

            def estimate_cost(self, issue: dict[str, Any]) -> dict:
                return {"estimated_cost_usd": 0.5}

        backend = DummyBackend()
        self.assertTrue(backend.prepare()[0])
        self.assertTrue(backend.needs_local_repo())
        self.assertIsNone(backend.cancel())
        result = backend.invoke({"number": 1}, "/tmp/repo")
        self.assertEqual(set(result.keys()), {"branch", "commits", "blocked"})



if __name__ == "__main__":
    unittest.main()
