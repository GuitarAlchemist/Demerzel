#!/usr/bin/env python3
"""Generic shell backend for the AFK implement lane.

Runs a configurable external command as the implementation agent. The command
receives the issue as JSON on stdin and a set of AFK_* environment variables.
It must print a JSON object with branch, commits, and blocked keys on stdout.

Configuration (from config/afk-backends.yaml under the shell backend entry):

    command: ["python", "my_agent.py"]          # required
    timeout: 300                                 # default 300
    needs_local_repo: true                         # default true
    env:                                            # extra env vars
      MY_AGENT_MODE: "afk"
"""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402


class ShellBackend(AFKBackend):
    """Desktop backend: delegate to a configurable shell command.

    This proves the AFKBackend abstraction works with any non-Claude tool that
    can read a JSON issue from stdin and emit a JSON result on stdout.
    """

    def _command(self) -> list[str] | None:
        raw = self.config.get("command")
        if raw is None:
            return None
        if isinstance(raw, list):
            return [str(x) for x in raw]
        if isinstance(raw, str):
            return shlex.split(raw)
        return None

    def _timeout(self) -> int:
        return int(self.config.get("timeout", 300))

    def _needs_local_repo(self) -> bool:
        return bool(self.config.get("needs_local_repo", True))

    def _env(self, issue: dict[str, Any], repo_path: str | None) -> dict[str, str]:
        base = os.environ.copy()
        extra = self.config.get("env") or {}
        base.update({str(k): str(v) for k, v in extra.items()})
        base["AFK_ISSUE_NUMBER"] = str(issue.get("number", ""))
        base["AFK_ISSUE_TITLE"] = str(issue.get("title", ""))
        base["AFK_ISSUE_BODY"] = str(issue.get("body", ""))
        base["AFK_ISSUE_LABELS"] = ",".join(str(l) for l in issue.get("labels", []))
        if repo_path is not None:
            base["AFK_REPO_PATH"] = repo_path
        return base

    def prepare(self) -> tuple[bool, str]:
        command = self._command()
        if not command:
            return False, "shell backend is enabled but no command is configured"
        tool = command[0]
        if not shutil.which(tool):
            return False, f"shell backend command not found on PATH: {tool}"
        return True, f"shell backend command ready ({tool})"

    def needs_local_repo(self) -> bool:
        return self._needs_local_repo()

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        command = self._command()
        if not command:
            return {"branch": None, "commits": [],
                    "blocked": "shell backend has no command configured"}

        try:
            result = subprocess.run(
                command,
                input=json.dumps(issue).encode("utf-8"),
                env=self._env(issue, repo_path),
                capture_output=True,
                timeout=self._timeout(),
                check=False,
            )
        except FileNotFoundError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"shell backend command not found: {exc}"}
        except subprocess.TimeoutExpired as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"shell backend timed out after {exc.timeout} seconds"}
        except OSError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"shell backend failed to run: {exc}"}

        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace")[:400]
            return {"branch": None, "commits": [],
                    "blocked": f"shell backend exited {result.returncode}: {stderr}"}

        stdout = result.stdout.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"shell backend returned invalid JSON: {exc}"}

        for key in ("branch", "commits", "blocked"):
            if key not in parsed:
                return {"branch": None, "commits": [],
                        "blocked": f"shell backend response missing required field {key!r}"}
        return parsed

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        return {"estimated_cost_usd": 1.0, "estimated_runner_minutes": 15}
