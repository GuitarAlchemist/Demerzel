#!/usr/bin/env python3
"""Junie CLI backend for the AFK implement lane.

Invokes the JetBrains Junie terminal agent and parses the resulting git state
(branch and commits) to satisfy the AFK result contract. Junie is expected to
create a branch and commit changes in the ephemeral repo path; the backend
reads those git artifacts after the command finishes.

Configuration (from config/afk-backends.yaml under the junie backend entry):

    command:        ["junie", "--headless"]   # default
    task_template:  "Implement issue #{number}: {title}\n\n{body}"
    timeout:        600                         # default 10 minutes
    api_key_env:    "JUNIE_API_KEY"            # optional
    branch_prefix:  "agent/issue-"             # hint for detecting the branch
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402


class JunieBackend(AFKBackend):
    """Desktop backend: delegate to the JetBrains CLI agent.

    This proves the AFKBackend abstraction works with a third-party commercial
    terminal agent, not just with local scripts or Claude Code.
    """

    def _command(self) -> list[str]:
        raw = self.config.get("command", ["junie", "--headless"])
        if isinstance(raw, str):
            return raw.split()
        return [str(x) for x in raw]

    def _task_template(self) -> str:
        return str(self.config.get(
            "task_template",
            "Implement GitHub issue #{number}: {title}\n\n{body}",
        ))

    def _timeout(self) -> int:
        return int(self.config.get("timeout", 600))

    def _branch_prefix(self) -> str:
        return str(self.config.get("branch_prefix", "agent/issue-"))

    def _api_key(self) -> str | None:
        env_name = self.config.get("api_key_env")
        if env_name:
            return os.environ.get(str(env_name))
        return None

    def _git(self, repo_path: str, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()

    def prepare(self) -> tuple[bool, str]:
        command = self._command()
        if not command:
            return False, "junie backend is enabled but no command is configured"
        tool = command[0]
        if not shutil.which(tool):
            return False, f"junie backend command not found on PATH: {tool}"
        api_key = self._api_key()
        if self.config.get("api_key_env") and not api_key:
            return False, f"junie backend requires env var {self.config['api_key_env']}"
        return True, f"junie backend ready ({tool})"

    def needs_local_repo(self) -> bool:
        return True

    def _build_prompt(self, issue: dict[str, Any]) -> str:
        return self._task_template().format(
            number=issue.get("number", ""),
            title=issue.get("title", ""),
            body=issue.get("body", ""),
            labels=", ".join(str(l) for l in issue.get("labels", [])),
            branch_prefix=self._branch_prefix(),
        )

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        if not repo_path:
            return {"branch": None, "commits": [],
                    "blocked": "junie backend requires a local repo path"}

        command = self._command()
        if not command:
            return {"branch": None, "commits": [],
                    "blocked": "junie backend has no command configured"}

        try:
            before_branch = self._git(repo_path, "branch", "--show-current")
            before_head = self._git(repo_path, "rev-parse", "HEAD")
        except OSError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"junie backend could not read git state: {exc}"}

        env = os.environ.copy()
        api_key = self._api_key()
        if api_key:
            env[self.config["api_key_env"]] = api_key
        env["AFK_ISSUE_NUMBER"] = str(issue.get("number", ""))
        env["AFK_ISSUE_TITLE"] = str(issue.get("title", ""))
        env["AFK_ISSUE_BODY"] = str(issue.get("body", ""))

        prompt = self._build_prompt(issue)
        try:
            result = subprocess.run(
                [*command, prompt],
                cwd=repo_path,
                env=env,
                capture_output=True,
                text=True,
                timeout=self._timeout(),
            )
        except FileNotFoundError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"junie backend command not found: {exc}"}
        except subprocess.TimeoutExpired as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"junie backend timed out after {exc.timeout} seconds"}
        except OSError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"junie backend failed to run: {exc}"}

        if result.returncode != 0:
            stderr = result.stderr[:400]
            return {"branch": None, "commits": [],
                    "blocked": f"junie exited {result.returncode}: {stderr}"}

        try:
            after_branch = self._git(repo_path, "branch", "--show-current")
            branch = after_branch if after_branch != before_branch else None
            if branch is None:
                # Junie may have created a branch but not checked it out; try to
                # find a branch matching the configured prefix + issue number.
                prefix = self._branch_prefix()
                candidate = f"{prefix}{issue.get('number')}"
                branches = self._git(repo_path, "branch", "--list", candidate)
                if candidate in branches:
                    branch = candidate
            commits = []
            if before_head:
                log = self._git(repo_path, "log", f"{before_head}..HEAD", "--format=%s")
                if log:
                    commits = [line.strip() for line in log.splitlines() if line.strip()]
        except OSError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"junie backend could not read post-run git state: {exc}"}

        return {"branch": branch, "commits": commits, "blocked": None}

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        return {"estimated_cost_usd": 2.0, "estimated_runner_minutes": 20}
