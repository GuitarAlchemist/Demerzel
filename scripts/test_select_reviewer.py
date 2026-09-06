#!/usr/bin/env python3
"""Deterministic tests for cross-model reviewer selection (#846)."""

from __future__ import annotations

import io
import itertools
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

import select_reviewer as sr


AUTHORS = ("claude", "gemini", "codex", "human", "unknown")
PROVIDERS = ("claude", "gemini", "codex")


def environment_for(enabled: set[str]) -> dict[str, str]:
    environment = {name: "" for name in sr.CREDENTIAL_ENV.values()}
    for provider in enabled:
        environment[sr.CREDENTIAL_ENV[provider]] = f"{provider}-credential"
    return environment


class SelectReviewerMatrixTests(unittest.TestCase):
    def test_all_authors_across_all_credential_combinations(self) -> None:
        for author in AUTHORS:
            for mask in itertools.product((False, True), repeat=len(PROVIDERS)):
                enabled = {
                    provider
                    for provider, present in zip(PROVIDERS, mask, strict=True)
                    if present
                }
                with self.subTest(author=author, enabled=sorted(enabled)):
                    candidates = sr.candidate_order(author)
                    expected = next(
                        (provider for provider in candidates if provider in enabled),
                        None,
                    )
                    if expected is None:
                        with self.assertRaises(sr.NoReviewerAvailable):
                            sr.select_reviewer(author, environment_for(enabled))
                    else:
                        selected = sr.select_reviewer(
                            author, environment_for(enabled)
                        )
                        self.assertEqual(expected, selected)
                        self.assertIn(selected, enabled)
                        if author in PROVIDERS:
                            self.assertNotEqual(author, selected)

    def test_each_provider_requires_its_own_credential(self) -> None:
        for provider in PROVIDERS:
            own = sr.CREDENTIAL_ENV[provider]
            for variable in sr.CREDENTIAL_ENV.values():
                environment = {name: "" for name in sr.CREDENTIAL_ENV.values()}
                environment[variable] = "present"
                with self.subTest(provider=provider, configured=variable):
                    self.assertEqual(
                        variable == own,
                        sr.has_credential(provider, environment),
                    )

    def test_unknown_author_uses_human_preference_order(self) -> None:
        environment = environment_for(set(PROVIDERS))
        self.assertEqual(
            sr.select_reviewer("unexpected-agent", environment),
            sr.select_reviewer("human", environment),
        )
        self.assertEqual(
            "claude",
            sr.select_reviewer("unexpected-agent", environment),
        )

    def test_whitespace_only_credentials_are_absent(self) -> None:
        environment = environment_for(set())
        environment["ANTHROPIC_API_KEY"] = "   "
        with self.assertRaises(sr.NoReviewerAvailable):
            sr.select_reviewer("gemini", environment)


class CliTests(unittest.TestCase):
    def run_cli(self, author: str, enabled: set[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        environment = environment_for(enabled)
        with patch.dict(os.environ, environment, clear=True):
            with redirect_stdout(out), redirect_stderr(err):
                code = sr.main(["--author", author])
        return code, out.getvalue(), err.getvalue()

    def test_cli_prints_only_selected_provider_on_success(self) -> None:
        code, out, err = self.run_cli("claude", {"codex"})
        self.assertEqual(0, code)
        self.assertEqual("codex\n", out)
        self.assertEqual("", err)

    def test_cli_fails_nonzero_and_explains_candidates(self) -> None:
        code, out, err = self.run_cli("codex", {"codex"})
        self.assertEqual(1, code)
        self.assertEqual("", out)
        self.assertIn("No credentialed reviewer", err)
        self.assertIn("claude, gemini", err)


if __name__ == "__main__":
    unittest.main()
