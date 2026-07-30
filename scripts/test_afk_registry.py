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
        self.assertEqual(reg["local"]["provider"], "anthropic-api")
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


class TestConfigDerivedProvider(unittest.TestCase):
    """#915: a backend whose spend attribution is a property of the endpoint an
    operator configures (``remote``) has no correct provider in the abstract.
    Naming one anyway is how a metered HTTP worker got gated as a free
    local-seat Claude Code subscription. The attribution is read from the
    backend's own config block instead, and it is mandatory to enable the lane."""

    def _write(self, body: str) -> Path:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False,
                                         encoding="utf-8") as tmp:
            tmp.write(body)
            path = Path(tmp.name)
        self.addCleanup(path.unlink)
        return path

    def test_config_declared_provider_is_what_reaches_the_gate(self):
        path = self._write(
            'schema_version: "1.0"\n'
            "backends:\n"
            "  remote:\n"
            "    adapter: afk_backends.remote.RemoteBackend\n"
            "    provider_from_config: true\n"
            "    enabled: true\n"
            "    config:\n"
            "      provider: anthropic-api\n"
            "      endpoint: https://example.com/afk-worker\n")
        reg = load_registry(path)
        self.assertEqual("anthropic-api", provider_for("remote", reg))

    def test_enabling_without_a_declared_provider_is_a_load_error(self):
        """The control the #914 comment was not: an operator who flips
        ``enabled: true`` without saying what the endpoint bills gets a refusal
        at load time, before any reservation is attempted."""
        path = self._write(
            'schema_version: "1.0"\n'
            "backends:\n"
            "  remote:\n"
            "    adapter: afk_backends.remote.RemoteBackend\n"
            "    provider_from_config: true\n"
            "    enabled: true\n"
            "    config:\n"
            "      endpoint: https://example.com/afk-worker\n")
        with self.assertRaises(RegistryError) as ctx:
            load_registry(path)
        self.assertIn("config.provider", str(ctx.exception))

    def test_disabled_without_a_provider_loads_but_never_resolves(self):
        """The shipped state: the entry is loadable while the lane is off, but
        nothing can derive a provider for it — so if anything did reach the
        budget gate, the gate fails closed instead of billing under a guess."""
        path = self._write(
            'schema_version: "1.0"\n'
            "backends:\n"
            "  remote:\n"
            "    adapter: afk_backends.remote.RemoteBackend\n"
            "    provider_from_config: true\n"
            "    enabled: false\n")
        reg = load_registry(path)
        with self.assertRaises(RegistryError):
            provider_for("remote", reg)

    def test_two_sources_of_truth_are_rejected(self):
        path = self._write(
            'schema_version: "1.0"\n'
            "backends:\n"
            "  remote:\n"
            "    adapter: afk_backends.remote.RemoteBackend\n"
            "    provider: claude-code-cli\n"
            "    provider_from_config: true\n"
            "    enabled: false\n")
        with self.assertRaises(RegistryError):
            load_registry(path)

    def test_shipped_remote_entry_declares_no_static_provider(self):
        """Bound to the real config, not a fixture: the defect was a literal
        value in config/afk-backends.yaml, so a fixture would reproduce it
        rather than catch it."""
        remote = load_registry()["remote"]
        self.assertTrue(remote.get("provider_from_config"))
        self.assertNotIn("provider", remote)


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
