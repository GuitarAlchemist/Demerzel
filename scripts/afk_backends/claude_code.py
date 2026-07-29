#!/usr/bin/env python3
"""Claude Code desktop backend for the AFK implement lane.

Runs a headless `claude -p` agent in an ephemeral clone, billing the interactive
subscription by stripping ANTHROPIC_API_KEY from the child environment. This is
the default AFK backend.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402
import demerzel_kit as kit  # noqa: E402

CLAUDE_CODE_TIMEOUT = 1800  # seconds for one headless `claude -p` agent run


def _claude_code_prompt(issue: dict) -> str:
    """The instruction handed to the headless Claude Code agent. The issue body
    already carries the full implementation spec (pattern + success criteria), so
    this only frames the autonomy contract: implement, test, commit — no push/PR
    (the governor owns those)."""
    num = issue.get("number")
    return (
        "You are an autonomous AFK engineer working in a fresh clone of the "
        "Demerzel governance repo, on a dedicated branch. Implement the issue "
        "below end-to-end, then COMMIT your work on the current branch with a "
        "conventional-commit message (feat/refactor/test). Be surgical — change "
        "only what the issue requires. After editing, run "
        "`python -m unittest discover -s scripts -p \"test_*.py\"` and make sure it "
        "passes before committing. Do NOT push and do NOT open a pull request; "
        "just commit locally.\n\n"
        f"=== ISSUE #{num}: {issue.get('title', '')} ===\n\n"
        f"{issue.get('body', '')}"
    )


class ClaudeCodeBackend(AFKBackend):
    """Desktop backend: delegate one issue to a headless Claude Code agent."""

    def prepare(self) -> tuple[bool, str]:
        try:
            p = subprocess.run(["claude", "--version"], capture_output=True, text=True,
                                 timeout=30)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"claude command not available: {exc}"
        if p.returncode != 0:
            return False, f"claude --version failed: {p.stderr.strip()[:160]}"
        return True, f"claude-code ready ({p.stdout.strip()})"

    def needs_local_repo(self) -> bool:
        return True

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        """Run headless Claude Code in repo_path and return branch/commits/blocked."""
        if repo_path is None:
            return {"branch": None, "commits": [],
                    "blocked": "claude-code backend requires a local repo clone"}
        num = issue.get("number")
        branch = f"agent/issue-{num}"
        try:
            subprocess.run(["git", "-C", repo_path, "checkout", "-b", branch],
                             capture_output=True, text=True, timeout=30, check=True)
            base = subprocess.run(["git", "-C", repo_path, "rev-parse", "HEAD"],
                                  capture_output=True, text=True, timeout=30).stdout.strip()
            env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            cmd = ["claude", "-p", _claude_code_prompt(issue),
                   "--output-format", "json",
                   "--allowedTools", "Edit", "Write", "Read", "Grep", "Glob",
                   "Bash(python *)", "Bash(python3 *)", "Bash(git *)"]
            p = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True,
                               timeout=CLAUDE_CODE_TIMEOUT, env=env)
        except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
            return {"branch": None, "commits": [], "blocked": f"claude-code invoke failed: {exc}"}

        # The agent is told to commit; if it left changes uncommitted, capture them so a
        # real implementation isn't lost to a missing commit step.
        dirty = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"],
                               capture_output=True, text=True, timeout=30).stdout.strip()
        if dirty:
            subprocess.run(["git", "-C", repo_path, "add", "-A"],
                           capture_output=True, text=True, timeout=60)
            subprocess.run(["git", "-C", repo_path, "commit", "-m",
                            f"feat: implement #{num} via AFK claude-code backend"],
                           capture_output=True, text=True, timeout=60)
        commits = subprocess.run(["git", "-C", repo_path, "log", "--format=%s", f"{base}..HEAD"],
                                 capture_output=True, text=True, timeout=30).stdout.strip()
        if not commits:
            tail = (p.stderr or p.stdout or "").strip()[-200:]
            return {"branch": None, "commits": [],
                    "blocked": f"claude-code made no commits (exit {p.returncode}): {tail}"}
        return {"branch": branch, "commits": commits.splitlines(), "blocked": None}

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        """Claude Code on the subscription is treated as local-seat cost.

        The actual marginal cost is covered by the interactive subscription, so
        the budget gate sees a low default estimate unless the issue body
        overrides it.
        """
        return {"estimated_cost_usd": 0.0, "estimated_runner_minutes": 30}
