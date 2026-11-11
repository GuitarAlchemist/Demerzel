#!/usr/bin/env python3
"""Tests for the confidence-rung guard over logic/*.md (scripts/build_manifest.py).

The guard exists because logic/hexavalent-logic.md claims its threshold table moves
when a rung is retuned, and nothing used to enforce that: the scan only covered
policies/*.yaml, and logic/*.md belongs to no artifact class. These tests mutate a
throwaway tree to prove the guard actually catches both directions of drift, rather
than asserting that the shipped tree happens to be clean."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_manifest  # noqa: E402

THRESHOLDS = """
thresholds:
  autonomous:
    operator: ">="
    value: 0.9
  with_note:
    operator: ">="
    value: 0.7
"""


class ConfidenceRefsInLogicDocs(unittest.TestCase):
    """check_confidence_refs() must read logic/*.md, not just the policy class."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "logic").mkdir()
        (self.root / "logic" / "confidence-thresholds.yaml").write_text(
            THRESHOLDS, encoding="utf-8"
        )
        self._saved = (build_manifest.REPO, build_manifest.CONFIDENCE)
        build_manifest.REPO = self.root
        build_manifest.CONFIDENCE = self.root / "logic" / "confidence-thresholds.yaml"
        self.addCleanup(self._restore)

    def _restore(self):
        build_manifest.REPO, build_manifest.CONFIDENCE = self._saved
        self._tmp.cleanup()

    def _write_doc(self, body: str) -> None:
        (self.root / "logic" / "example.md").write_text(body, encoding="utf-8")

    def _run(self):
        return build_manifest.check_confidence_refs({})

    def test_a_resolvable_and_shown_rung_is_clean(self):
        self._write_doc("At `autonomous` we proceed.\n<!-- ref:confidence#autonomous -->\n")
        edges, violations = self._run()
        self.assertEqual(violations, [])
        self.assertIn(
            {
                "from": "logic/example.md",
                "to": "confidence:autonomous",
                "kind": "confidence_ref",
                "resolved": True,
            },
            edges,
        )

    def test_a_renamed_rung_dangles(self):
        """The mutation the guard is for: the rung is renamed in the ladder, so the
        doc's declaration no longer names anything."""
        self._write_doc("At `proceed_alone` we proceed.\n<!-- ref:confidence#proceed_alone -->\n")
        _, violations = self._run()
        self.assertEqual(len(violations), 1)
        self.assertIn("dangling confidence ref", violations[0])
        self.assertIn("logic/example.md", violations[0])
        self.assertIn("proceed_alone", violations[0])

    def test_a_declared_rung_that_the_prose_stopped_naming_is_caught(self):
        """The other direction: the declaration survives an edit that removed the
        rung from the visible text, so the two have drifted apart."""
        self._write_doc("The table no longer names it.\n<!-- ref:confidence#with_note -->\n")
        _, violations = self._run()
        self.assertEqual(len(violations), 1)
        self.assertIn("declared but not shown", violations[0])
        self.assertIn("with_note", violations[0])

    def test_a_doc_with_no_refs_is_ignored(self):
        self._write_doc("Prose that cites no rung at all.\n")
        edges, violations = self._run()
        self.assertEqual(violations, [])
        self.assertEqual(edges, [])


class ShippedTreeIsClean(unittest.TestCase):
    """The guard must not be failing on the repository it ships in."""

    def test_repo_has_no_confidence_violations(self):
        _, violations = build_manifest.check_confidence_refs(
            build_manifest.harvest_inventory()
        )
        self.assertEqual(violations, [])

    def test_hexavalent_logic_declares_the_rungs_it_names(self):
        """Guards against the guard being vacuous here: the file that made the
        coupling claim must actually carry declarations."""
        text = (build_manifest.REPO / "logic" / "hexavalent-logic.md").read_text(
            encoding="utf-8"
        )
        found = set(build_manifest._CONFIDENCE_REF.findall(text))
        self.assertEqual(
            found, {"autonomous", "with_note", "ask_confirmation", "do_not_act"}
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
