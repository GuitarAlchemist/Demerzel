import json
import os
import subprocess
import unittest
import unittest.mock as mock
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from afk_backends.shell import ShellBackend


class TestShellBackend(unittest.TestCase):
    def _completed(self, stdout: bytes, stderr: bytes = b"", returncode: int = 0):
        return subprocess.CompletedProcess(args=["agent"], returncode=returncode,
                                           stdout=stdout, stderr=stderr)

    def test_needs_local_repo_defaults_true(self):
        self.assertTrue(ShellBackend().needs_local_repo())

    def test_needs_local_repo_can_be_false(self):
        self.assertFalse(ShellBackend({"needs_local_repo": False}).needs_local_repo())

    def test_prepare_without_command_fails(self):
        ok, note = ShellBackend().prepare()
        self.assertFalse(ok)
        self.assertIn("no command", note.lower())

    def test_prepare_with_missing_executable_fails(self):
        ok, note = ShellBackend({"command": ["not-a-real-binary-xyz"]}).prepare()
        self.assertFalse(ok)
        self.assertIn("not found", note.lower())

    def test_prepare_with_existing_executable_succeeds(self):
        with mock.patch("shutil.which", return_value="/usr/bin/python"):
            ok, note = ShellBackend({"command": ["python", "agent.py"]}).prepare()
        self.assertTrue(ok)
        self.assertIn("python", note.lower())

    def test_invoke_without_command_is_blocked(self):
        result = ShellBackend().invoke({"number": 1}, None)
        self.assertIn("no command", result["blocked"].lower())

    def test_invoke_runs_command_with_issue_json(self):
        backend = ShellBackend({"command": ["python", "agent.py"]})
        seen = {}
        def run(cmd, input=None, env=None, capture_output=None, timeout=None, check=None):
            seen["cmd"] = cmd
            seen["input"] = input.decode("utf-8")
            seen["timeout"] = timeout
            seen["env_keys"] = set(env.keys()) - set(os.environ.keys())
            return self._completed(json.dumps({"branch": "agent/issue-1",
                                               "commits": ["feat: x"],
                                               "blocked": None}).encode())
        with mock.patch("subprocess.run", side_effect=run):
            result = backend.invoke({"number": 1, "title": "x", "body": "y"}, None)
        self.assertEqual(seen["cmd"], ["python", "agent.py"])
        payload = json.loads(seen["input"])
        self.assertEqual(payload["number"], 1)
        self.assertEqual(seen["timeout"], 300)
        self.assertIn("AFK_ISSUE_NUMBER", seen["env_keys"])
        self.assertEqual(result["branch"], "agent/issue-1")
        self.assertEqual(result["commits"], ["feat: x"])
        self.assertIsNone(result["blocked"])

    def test_invoke_passes_repo_path_in_env(self):
        backend = ShellBackend({"command": ["agent"]})
        seen = {}
        def run(cmd, input=None, env=None, capture_output=None, timeout=None, check=None):
            seen["AFK_REPO_PATH"] = env.get("AFK_REPO_PATH")
            return self._completed(json.dumps({"branch": None, "commits": [], "blocked": "busy"}).encode())
        with mock.patch("subprocess.run", side_effect=run):
            backend.invoke({"number": 1}, "/tmp/repo")
        self.assertEqual(seen["AFK_REPO_PATH"], "/tmp/repo")

    def test_invoke_passes_extra_env(self):
        backend = ShellBackend({"command": ["agent"], "env": {"MY_MODE": "afk"}})
        seen = {}
        def run(cmd, input=None, env=None, capture_output=None, timeout=None, check=None):
            seen["MY_MODE"] = env.get("MY_MODE")
            return self._completed(json.dumps({"branch": None, "commits": [], "blocked": "busy"}).encode())
        with mock.patch("subprocess.run", side_effect=run):
            backend.invoke({"number": 1}, None)
        self.assertEqual(seen["MY_MODE"], "afk")

    def test_nonzero_exit_returns_blocked(self):
        backend = ShellBackend({"command": ["agent"]})
        with mock.patch("subprocess.run", return_value=self._completed(b"", b"bad args", 2)):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("exited 2", result["blocked"])
        self.assertIn("bad args", result["blocked"])

    def test_timeout_returns_blocked(self):
        backend = ShellBackend({"command": ["agent"], "timeout": 10})
        with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(["agent"], 10)):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("timed out", result["blocked"].lower())

    def test_invalid_json_returns_blocked(self):
        backend = ShellBackend({"command": ["agent"]})
        with mock.patch("subprocess.run", return_value=self._completed(b"not json")):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("invalid JSON", result["blocked"])

    def test_missing_result_fields_returns_blocked(self):
        backend = ShellBackend({"command": ["agent"]})
        with mock.patch("subprocess.run", return_value=self._completed(json.dumps({"branch": "x"}).encode())):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("missing required field", result["blocked"])


if __name__ == "__main__":
    unittest.main()
