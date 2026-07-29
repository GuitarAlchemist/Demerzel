#!/usr/bin/env python3
"""Cloud worker backend for the AFK implement lane.

Backend seam for Vercel isolated sandboxes or any generic HTTP worker. Not yet
implemented; this module exists to keep the governor's backend abstraction
complete while the remote worker contract is being built (see #879).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402


class RemoteBackend(AFKBackend):
    """Cloud backend: delegate to a remote worker endpoint.

    Currently returns a clean blocked result so the backend can be registered and
    selected without crashing the governor. A real implementation will be added
    in #879.
    """

    def prepare(self) -> tuple[bool, str]:
        return True, "remote backend registered but not configured (no-op)"

    def needs_local_repo(self) -> bool:
        return False

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        return {"branch": None, "commits": [],
                "blocked": "remote backend (Vercel isolated sandboxes) not implemented yet — "
                           "use --backend claude-code or local"}

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        return {"estimated_cost_usd": 2.0, "estimated_runner_minutes": 30}
