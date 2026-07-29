#!/usr/bin/env python3
"""Podman sandcastle backend for the AFK implement lane.

Delegates to the sibling `../afk-harness` project, which runs Claude Code inside a
Podman sandbox. This backend forwards ANTHROPIC_API_KEY and is therefore metered
spend — its budget provider must reflect that (see #877).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402

HARNESS_DIR = Path(__file__).resolve().parents[2] / "afk-harness"


class SandcastleBackend(AFKBackend):
    """Desktop/container backend: run the sandcastle harness in a Podman sandbox."""

    def _ensure_podman(self) -> tuple[bool, str]:
        """Restart-robustness: make sure the Podman machine is up before sandboxing.
        Idempotent — 'already running' is success. Returns (ok, note)."""
        try:
            chk = subprocess.run(["podman", "machine", "list", "--format", "{{.Running}}"],
                                 capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"podman not available: {exc}"
        if chk.returncode == 0 and "true" in chk.stdout.lower():
            return True, "podman machine already running"
        start = subprocess.run(["podman", "machine", "start"],
                               capture_output=True, text=True, timeout=180)
        if start.returncode == 0 or "already running" in (start.stderr + start.stdout).lower():
            return True, "podman machine started"
        return False, f"podman machine start failed: {start.stderr.strip()[:160]}"

    def prepare(self) -> tuple[bool, str]:
        return self._ensure_podman()

    def needs_local_repo(self) -> bool:
        return True

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        """Run the sandcastle harness for one issue against repo_path."""
        if repo_path is None:
            return {"branch": None, "commits": [],
                    "blocked": "sandcastle backend requires a local repo clone"}
        cmd = ["node", "--import", "tsx", str(HARNESS_DIR / ".sandcastle" / "main.mts"),
               "--repo", str(repo_path), "--issue", str(issue.get("number")),
               "--title", issue.get("title", ""), "--body", issue.get("body", "")]
        p = subprocess.run(cmd, cwd=str(HARNESS_DIR), capture_output=True, text=True, timeout=1800)
        if p.returncode != 0:
            return {"branch": None, "commits": [],
                    "blocked": f"harness exit {p.returncode}: {p.stderr.strip()[:200]}"}
        last = [l for l in p.stdout.strip().splitlines() if l.strip().startswith("{")]
        if not last:
            return {"branch": None, "commits": [], "blocked": "harness produced no JSON result"}
        return json.loads(last[-1])

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        """Sandcastle runs Claude Code with metered API key forwarded.

        The issue body is the authoritative source for budget estimates; the
        backend supplies a conservative default runner minute estimate.
        """
        return {"estimated_cost_usd": 2.0, "estimated_runner_minutes": 30}
