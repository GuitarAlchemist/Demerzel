import os
import subprocess
import unittest
import unittest.mock as mock
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from afk_backends.junie import JunieBackend


class TestJunieBackend(unittest.TestCase):
    def _completed(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        return subprocess.CompletedProcess(args=["junie"], returncode=returncode,
                                           stdout=stdout, stderr=stderr)

    def test_needs_local_repo(self):
        self.assertTrue(JunieBackend().needs_local_repo())

    def test_prepare_without_command_fails(self):
        ok, note = JunieBackend({"command": []}).prepare()
        self.assertFalse(ok)
        self.assertIn("no command", note.lower())

    def test_prepare_without_junie_on_path_fails(self):
        with mock.patch("shutil.which", return_value=None):
            ok, note = JunieBackend().prepare()
        self.assertFalse(ok)
        self.assertIn("not found", note.lower())

    def test_prepare_with_missing_api_key_fails(self):
        backend = JunieBackend({"api_key_env": "JUNIE_API_KEY"})
        with mock.patch("shutil.which", return_value="/usr/bin/junie"):
            ok, note = backend.prepare()
        self.assertFalse(ok)
        self.assertIn("JUNIE_API_KEY", note)

    def test_prepare_success(self):
        backend = JunieBackend({"api_key_env": "JUNIE_API_KEY"})
        with mock.patch("shutil.which", return_value="/usr/bin/junie"), \
             mock.patch.dict(os.environ, {"JUNIE_API_KEY": "secret"}):
            ok, note = backend.prepare()
        self.assertTrue(ok)
        self.assertIn("junie", note.lower())

    def test_invoke_without_repo_is_blocked(self):
        result = JunieBackend().invoke({"number": 1}, None)
        self.assertIn("requires a local repo", result["blocked"].lower())

    def test_invoke_runs_junie_and_reads_git_state(self):
        backend = JunieBackend()
        calls = []
        git_state = {
            "branch": ["main", "agent/issue-1"],
            "head": "abc123",
        }
        call_index = {"i": 0}

        def run(cmd, cwd=None, env=None, capture_output=None, text=None, check=None, timeout=None):
            if cmd[0] == "git":
                args = cmd[3:]
                if args == ["branch", "--show-current"]:
                    out = git_state["branch"][call_index["i"]]
                    call_index["i"] += 1
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=f"{out}\n")
                if args == ["rev-parse", "HEAD"]:
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=f"{git_state['head']}\n")
                if args[0] == "log":
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="feat: implement x\n")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="")
            calls.append({"cmd": cmd, "cwd": cwd, "timeout": timeout})
            return self._completed()

        with mock.patch("shutil.which", return_value="/usr/bin/junie"), \
             mock.patch("subprocess.run", side_effect=run):
            result = backend.invoke({"number": 1, "title": "x", "body": "y"}, "/tmp/repo")

        self.assertEqual(result["branch"], "agent/issue-1")
        self.assertEqual(result["commits"], ["feat: implement x"])
        self.assertIsNone(result["blocked"])
        self.assertEqual(calls[0]["cmd"], ["junie", "--headless", "Implement GitHub issue #1: x\n\ny"])
        self.assertEqual(calls[0]["cwd"], "/tmp/repo")

    def test_invoke_on_junie_error_returns_blocked(self):
        backend = JunieBackend()

        def run(cmd, cwd=None, env=None, capture_output=None, text=None, check=None, timeout=None):
            if cmd[0] == "junie":
                return self._completed(returncode=1, stderr="auth failed")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="")

        with mock.patch("shutil.which", return_value="/usr/bin/junie"), \
             mock.patch("subprocess.run", side_effect=run):
            result = backend.invoke({"number": 1}, "/tmp/repo")
        self.assertIn("auth failed", result["blocked"])


if __name__ == "__main__":
    unittest.main()
