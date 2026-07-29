import json
import os
import unittest
import unittest.mock as mock
from pathlib import Path
from urllib.error import HTTPError, URLError

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from afk_backends.remote import RemoteBackend


class TestRemoteBackend(unittest.TestCase):
    def test_needs_no_local_repo(self):
        self.assertFalse(RemoteBackend().needs_local_repo())

    def test_without_endpoint_is_blocked(self):
        result = RemoteBackend().invoke({"number": 1, "title": "x", "body": "y"}, None)
        self.assertIsNone(result["branch"])
        self.assertEqual(result["commits"], [])
        self.assertIn("no endpoint", result["blocked"].lower())

    def test_prepare_without_endpoint_fails(self):
        ok, note = RemoteBackend().prepare()
        self.assertFalse(ok)
        self.assertIn("no endpoint", note.lower())

    def _make_response(self, body: bytes, code: int = 200):
        class FakeResponse:
            def __init__(self, body, code):
                self._body = body
                self.code = code
            def read(self):
                return self._body
            def __enter__(self):
                return self
            def __exit__(self, *exc):
                return False
        return FakeResponse(body, code)

    def test_invoke_posts_issue_and_repo_path(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk"})
        seen = {}
        def urlopen(req, timeout=None):
            seen["url"] = req.full_url
            seen["body"] = req.data
            seen["headers"] = dict(req.headers)
            return self._make_response(json.dumps({"branch": "agent/issue-1",
                                                   "commits": ["feat: x"],
                                                   "blocked": None}).encode())
        with mock.patch("urllib.request.urlopen", side_effect=urlopen):
            result = backend.invoke({"number": 1, "title": "x", "body": "y"}, None)
        self.assertEqual(seen["url"], "https://worker.example/afk")
        payload = json.loads(seen["body"])
        self.assertEqual(payload["issue"]["number"], 1)
        self.assertIsNone(payload["repo_path"])
        self.assertEqual(result["branch"], "agent/issue-1")
        self.assertEqual(result["commits"], ["feat: x"])
        self.assertIsNone(result["blocked"])

    def test_invoke_sends_api_key(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk",
                                 "api_key_env": "TEST_REMOTE_KEY"})
        seen = {}
        def urlopen(req, timeout=None):
            seen["auth"] = req.get_header("Authorization")
            return self._make_response(json.dumps({"branch": None,
                                                   "commits": [],
                                                   "blocked": "busy"}).encode())
        with mock.patch("urllib.request.urlopen", side_effect=urlopen), \
             mock.patch.dict(os.environ, {"TEST_REMOTE_KEY": "secret-token"}):
            backend.invoke({"number": 1}, None)
        self.assertEqual(seen["auth"], "Bearer secret-token")

    def test_http_error_returns_blocked(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk"})
        err = HTTPError("https://worker.example/afk", 503, "Service Unavailable", None, None)
        err.read = lambda: b"overloaded"
        with mock.patch("urllib.request.urlopen", side_effect=err):
            result = backend.invoke({"number": 1}, None)
        self.assertIsNone(result["branch"])
        self.assertEqual(result["commits"], [])
        self.assertIn("503", result["blocked"])

    def test_network_error_returns_blocked(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk"})
        with mock.patch("urllib.request.urlopen", side_effect=URLError("no route")):
            result = backend.invoke({"number": 1}, None)
        self.assertIsNone(result["branch"])
        self.assertEqual(result["commits"], [])
        self.assertIn("request failed", result["blocked"].lower())

    def test_invalid_json_returns_blocked(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk"})
        with mock.patch("urllib.request.urlopen",
                        return_value=self._make_response(b"not json")):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("invalid JSON", result["blocked"])

    def test_missing_result_fields_returns_blocked(self):
        backend = RemoteBackend({"endpoint": "https://worker.example/afk"})
        with mock.patch("urllib.request.urlopen",
                        return_value=self._make_response(json.dumps({"branch": "x"}).encode())):
            result = backend.invoke({"number": 1}, None)
        self.assertIn("missing required field", result["blocked"])


if __name__ == "__main__":
    unittest.main()
