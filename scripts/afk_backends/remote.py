#!/usr/bin/env python3
"""Cloud worker backend for the AFK implement lane.

Delegates to a configurable HTTP worker endpoint (Vercel isolated sandboxes,
GitHub Codespaces, or any service that implements the AFK result contract). The
endpoint must accept a POST with the issue JSON and return
`{"branch": ..., "commits": [...], "blocked": ...}`.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from afk_backends import AFKBackend  # noqa: E402


class RemoteBackend(AFKBackend):
    """Cloud backend: delegate to a remote worker endpoint over HTTP.

    Configuration (from config/afk-backends.yaml under the remote backend entry):

        endpoint:      URL to POST to (required when enabled)
        api_key_env:   name of an env var holding an Authorization bearer token
        timeout:       request timeout in seconds (default 300)
    """

    def _endpoint(self) -> str | None:
        return self.config.get("endpoint")

    def _api_key(self) -> str | None:
        env_name = self.config.get("api_key_env")
        if env_name:
            return os.environ.get(env_name)
        return None

    def _timeout(self) -> int:
        return int(self.config.get("timeout", 300))

    def prepare(self) -> tuple[bool, str]:
        endpoint = self._endpoint()
        if not endpoint:
            return False, "remote backend is enabled but no endpoint is configured"
        try:
            req = urllib.request.Request(endpoint, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                _ = resp.read()
        except urllib.error.HTTPError as exc:
            # A 404/405 from a HEAD request is common; the endpoint may only
            # support POST. Treat HTTP-level reachability as success.
            if exc.code >= 500:
                return False, f"remote endpoint unavailable: HTTP {exc.code}"
        except (OSError, urllib.error.URLError) as exc:
            return False, f"remote endpoint unreachable: {exc}"
        return True, f"remote endpoint reachable ({endpoint})"

    def needs_local_repo(self) -> bool:
        return False

    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        endpoint = self._endpoint()
        if not endpoint:
            return {"branch": None, "commits": [],
                    "blocked": "remote backend has no endpoint configured"}

        payload = json.dumps({"issue": issue, "repo_path": repo_path}).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        api_key = self._api_key()
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")

        try:
            with urllib.request.urlopen(req, timeout=self._timeout()) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8")[:400]
            return {"branch": None, "commits": [],
                    "blocked": f"remote worker returned HTTP {exc.code}: {body}"}
        except (OSError, urllib.error.URLError) as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"remote worker request failed: {exc}"}

        try:
            result = json.loads(body)
        except json.JSONDecodeError as exc:
            return {"branch": None, "commits": [],
                    "blocked": f"remote worker returned invalid JSON: {exc}"}

        for key in ("branch", "commits", "blocked"):
            if key not in result:
                return {"branch": None, "commits": [],
                        "blocked": f"remote worker response missing required field {key!r}"}
        return result

    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        return {"estimated_cost_usd": 2.0, "estimated_runner_minutes": 30}
