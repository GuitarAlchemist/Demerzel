#!/usr/bin/env python3
"""Tests for the cross-model reviewer quarantine (#846).

The quarantine exists to route around a provider whose credential is valid but
whose quota is gone. Its failure modes are the interesting part: a quarantine
that silently matches nothing is worse than none at all, because it reads as
protection while every review still routes into the wall.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

import reviewer_quarantine as rq


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "cross-model-review.yml"


def write(directory: Path, text: str) -> Path:
    path = directory / "reviewer-quarantine.yml"
    path.write_text(text, encoding="utf-8")
    return path


VALID = """
schema_version: '1.0'
quarantined:
  - provider: claude
    reason: quota exhausted
    since: '2026-07-30'
    until: '2026-07-31'
"""


class TestLoadValidates(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.dir = Path(directory.name)

    def assert_invalid(self, text, needle):
        with self.assertRaises(rq.QuarantineInvalid) as caught:
            rq.load(write(self.dir, text))
        self.assertIn(needle, str(caught.exception))

    def test_a_valid_declaration_loads(self):
        entries = rq.load(write(self.dir, VALID))
        self.assertEqual(1, len(entries))
        self.assertEqual("claude", entries[0]["provider"])
        self.assertEqual(date(2026, 7, 31), entries[0]["until"])

    def test_an_absent_file_is_an_empty_quarantine(self):
        """The normal state. Nothing quarantined must not be an error."""
        self.assertEqual([], rq.load(self.dir / "does-not-exist.yml"))

    def test_an_empty_file_is_an_empty_quarantine(self):
        self.assertEqual([], rq.load(write(self.dir, "")))

    def test_an_unknown_provider_is_rejected(self):
        """A typo'd provider would quarantine nobody while looking like it had.
        That is the failure this whole file is supposed to prevent, so it must
        not be reachable through the file itself."""
        self.assert_invalid(
            VALID.replace("provider: claude", "provider: claude-3"), "unknown provider")

    def test_a_missing_until_is_rejected(self):
        """An unbounded quarantine is a provider quietly removed from rotation
        forever -- exactly the drift `until` exists to prevent."""
        self.assert_invalid(VALID.replace("    until: '2026-07-31'\n", ""), "until")

    def test_a_missing_reason_is_rejected(self):
        self.assert_invalid(VALID.replace("    reason: quota exhausted\n", ""), "reason")

    def test_a_non_date_until_is_rejected(self):
        self.assert_invalid(VALID.replace("'2026-07-31'", "'next tuesday'"), "not a YYYY-MM-DD")

    def test_an_until_before_since_is_rejected(self):
        self.assert_invalid(VALID.replace("'2026-07-31'", "'2026-07-01'"), "precedes")

    def test_a_duplicate_provider_is_rejected(self):
        """Two entries for one provider means two `until` dates and no answer to
        which one governs."""
        self.assert_invalid(VALID + """
  - provider: claude
    reason: also quota
    since: '2026-07-30'
    until: '2026-09-01'
""", "more than once")

    def test_an_unknown_top_level_key_is_rejected(self):
        """Fail-closed on a key we do not implement: `quarantine:` instead of
        `quarantined:` would otherwise parse to an empty, silent no-op."""
        self.assert_invalid(VALID + "\nquarantine: [claude]\n", "unknown top-level")

    def test_unparseable_yaml_is_rejected(self):
        self.assert_invalid("quarantined: [unclosed", "could not be read")

    def test_a_scalar_document_is_rejected(self):
        self.assert_invalid("just a string", "expected a mapping")

    def test_a_non_list_quarantined_is_rejected(self):
        self.assert_invalid("quarantined: claude", "must be a list")


class TestActiveWindow(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.entries = rq.load(write(Path(directory.name), VALID))

    def current(self, as_of):
        return [e["provider"] for e in rq.active(self.entries, as_of)[0]]

    def test_until_is_inclusive(self):
        """`until` means the same thing here as in .github/loop-health.yml: the
        last day the entry is in effect. Drift between the two would make one
        word mean two things across the governance surface."""
        self.assertEqual(["claude"], self.current(date(2026, 7, 31)))

    def test_the_day_after_until_is_back_in_rotation(self):
        """The quota returns 2026-08-01 at 00:00 UTC, so the provider must be
        selectable that morning without anyone editing anything."""
        self.assertEqual([], self.current(date(2026, 8, 1)))

    def test_before_since_is_not_yet_quarantined(self):
        self.assertEqual([], self.current(date(2026, 7, 29)))

    def test_the_first_day_is_quarantined(self):
        self.assertEqual(["claude"], self.current(date(2026, 7, 30)))

    def test_an_expired_entry_is_reported_separately(self):
        _, expired = rq.active(self.entries, date(2026, 8, 5))
        self.assertEqual(["claude"], [e["provider"] for e in expired])


class TestCli(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.dir = Path(directory.name)

    def run_cli(self, text, as_of):
        path = write(self.dir, text)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = rq.main(["--as-of", as_of, "--path", str(path)])
        return code, out.getvalue(), err.getvalue()

    def test_prints_one_quarantined_provider_per_line(self):
        code, out, _ = self.run_cli(VALID, "2026-07-30")
        self.assertEqual(0, code)
        self.assertEqual(["claude"], out.split())

    def test_prints_nothing_when_nothing_is_quarantined(self):
        """The shell reads stdout into a word list; anything chatty on stdout
        becomes a phantom provider id. Notes belong on stderr."""
        code, out, _ = self.run_cli(VALID, "2026-08-02")
        self.assertEqual(0, code)
        self.assertEqual("", out.strip())

    def test_an_expired_entry_is_announced_on_stderr(self):
        _, out, err = self.run_cli(VALID, "2026-08-02")
        self.assertIn("expired", err)
        self.assertNotIn("claude", out)

    def test_an_invalid_declaration_exits_2(self):
        """The workflow treats a non-zero exit as fatal: a selection step that
        cannot tell which providers are usable must not fall back to guessing."""
        code, out, err = self.run_cli(VALID.replace("provider: claude", "provider: gpt5"),
                                      "2026-07-30")
        self.assertEqual(2, code)
        self.assertEqual("", out.strip())
        self.assertIn("invalid", err)

    def test_a_bad_as_of_exits_2(self):
        code, _, err = self.run_cli(VALID, "07/30/2026")
        self.assertEqual(2, code)
        self.assertIn("--as-of", err)


class TestShippedDeclaration(unittest.TestCase):
    """The committed file is the one that governs routing; validate it directly."""

    def test_the_committed_declaration_is_valid(self):
        rq.load()   # raises QuarantineInvalid if not

    def test_every_committed_entry_is_bounded(self):
        for entry in rq.load():
            self.assertIsInstance(entry["until"], date,
                                  f"{entry['provider']} quarantine is unbounded")

    def test_known_providers_match_the_workflows_credential_check(self):
        """Guard on the guard. `has_credential` in cross-model-review.yml is the
        list of providers that can actually be selected. If a provider is added
        there and not here, KNOWN_PROVIDERS rejects any attempt to quarantine
        it — the declaration would fail closed on a legitimate entry. If one is
        removed there, a quarantine naming it silently protects nothing.

        Parsed by string operations, not a regex, per repo convention."""
        text = WORKFLOW.read_text(encoding="utf-8")
        marker = "has_credential() {"
        self.assertIn(marker, text, "has_credential() disappeared from the workflow")
        # Terminate on `esac`, not on the function's closing brace: the arms
        # contain `${ANTHROPIC_API_KEY:-}`, so the first `}` is inside a
        # parameter expansion and cuts the body off mid-list.
        self.assertIn("esac", text, "has_credential() no longer uses a case block")
        body = text.split(marker, 1)[1].split("esac", 1)[0]

        found = set()
        for line in body.splitlines():
            stripped = line.strip()
            # Case arms look like:  claude) [ -n "${ANTHROPIC_API_KEY:-}" ] ;;
            if ")" not in stripped or stripped.startswith("#"):
                continue
            label = stripped.split(")", 1)[0].strip()
            if label and label != "*":
                found.add(label)

        self.assertEqual(
            rq.KNOWN_PROVIDERS, frozenset(found),
            "reviewer_quarantine.KNOWN_PROVIDERS has drifted from the providers "
            "cross-model-review.yml can select. A quarantine can only name a "
            "provider both files agree exists.")


if __name__ == "__main__":
    unittest.main()
