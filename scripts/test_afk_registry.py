import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from afk_backends.claude_code import ClaudeCodeBackend
from afk_backends.registry import get_backend, load_registry, provider_for, RegistryError
from afk_backends.remote import RemoteBackend
from afk_backends.sandcastle import SandcastleBackend
from afk_backends.shell import ShellBackend


class TestLoadRegistry(unittest.TestCase):
    def test_loads_default_config(self):
        reg = load_registry()
        self.assertIn("claude-code", reg)
        self.assertIn("local", reg)
        self.assertIn("remote", reg)
        self.assertIn("shell", reg)
        self.assertEqual(reg["claude-code"]["provider"], "claude-code-cli")
        self.assertEqual(reg["local"]["provider"], "claude-code-cli")
        self.assertEqual(reg["shell"]["provider"], "generic-shell")
        self.assertFalse(reg["shell"]["enabled"])

    def test_missing_schema_version_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write("backends:\n  x:\n    adapter: a.b.C\n    provider: p\n")
            path = tmp.name
        self.addCleanup(Path(path).unlink)
        with self.assertRaises(RegistryError):
            load_registry(Path(path))

    def test_missing_backend_section_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write('schema_version: "1.0"\n')
            path = tmp.name
        self.addCleanup(Path(path).unlink)
        with self.assertRaises(RegistryError):
            load_registry(Path(path))

    def test_missing_adapter_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write('schema_version: "1.0"\nbackends:\n  x:\n    provider: p\n')
            path = tmp.name
        self.addCleanup(Path(path).unlink)
        with self.assertRaises(RegistryError):
            load_registry(Path(path))


class TestGetBackend(unittest.TestCase):
    def test_returns_configured_adapters(self):
        reg = {
            "claude-code": {"adapter": "afk_backends.claude_code.ClaudeCodeBackend",
                            "provider": "claude-code-cli", "enabled": True},
            "local": {"adapter": "afk_backends.sandcastle.SandcastleBackend",
                      "provider": "codex-cli", "enabled": True},
            "remote": {"adapter": "afk_backends.remote.RemoteBackend",
                       "provider": "claude-code-cli", "enabled": False},
            "shell": {"adapter": "afk_backends.shell.ShellBackend",
                      "provider": "generic-shell", "enabled": True,
                      "config": {"command": ["echo"]}},
        }
        self.assertIsInstance(get_backend("claude-code", reg), ClaudeCodeBackend)
        self.assertIsInstance(get_backend("local", reg), SandcastleBackend)
        self.assertIsInstance(get_backend("shell", reg), ShellBackend)

    def test_disabled_backend_raises(self):
        reg = {
            "remote": {"adapter": "afk_backends.remote.RemoteBackend",
                       "provider": "claude-code-cli", "enabled": False},
        }
        with self.assertRaisesRegex(RegistryError, "disabled"):
            get_backend("remote", reg)

    def test_unknown_backend_raises(self):
        reg = {"claude-code": {"adapter": "afk_backends.claude_code.ClaudeCodeBackend",
                               "provider": "claude-code-cli", "enabled": True}}
        with self.assertRaisesRegex(RegistryError, "unknown backend"):
            get_backend("not-real", reg)

    def test_bad_adapter_path_raises(self):
        reg = {"x": {"adapter": "not.a.module.Class", "provider": "p", "enabled": True}}
        with self.assertRaises(RegistryError):
            get_backend("x", reg)

    def test_non_afk_backend_raises(self):
        reg = {"x": {"adapter": "builtins.str", "provider": "p", "enabled": True}}
        with self.assertRaisesRegex(RegistryError, "does not implement AFKBackend"):
            get_backend("x", reg)


class TestProviderFor(unittest.TestCase):
    def test_returns_provider_for_backend(self):
        reg = {
            "claude-code": {"adapter": "afk_backends.claude_code.ClaudeCodeBackend",
                            "provider": "claude-code-cli", "enabled": True},
        }
        self.assertEqual(provider_for("claude-code", reg), "claude-code-cli")

    def test_unknown_backend_raises(self):
        with self.assertRaisesRegex(RegistryError, "unknown backend"):
            provider_for("missing", {})


if __name__ == "__main__":
    unittest.main()
