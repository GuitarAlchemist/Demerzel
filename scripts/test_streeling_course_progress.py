"""Focused checks for the Streeling source progress report."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.streeling_course_progress import content_signals, inventory


class StreelingCourseProgressTests(unittest.TestCase):
    def test_content_signals_require_a_paired_answer_and_existing_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "state/streeling/courses/example/en/ex-001.md"
            source.parent.mkdir(parents=True)
            fixture = root / "state/streeling/fixtures/example/input.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("{}", encoding="utf-8")
            source.write_text(
                "### Practice Exercise\nSolve the project case.\n"
                "> *Solution:* Checked answer.\n"
                "### Practice exercise 2\nThis answer is missing.\n"
                "## Evidence\n"
                "[fixture](../../../fixtures/example/input.json)\n"
                "[missing](../../../fixtures/example/missing.json)\n"
                "[source](https://github.com/GuitarAlchemist/ga/blob/"
                + "a" * 40 + "/state/quality/example.json)\n",
                encoding="utf-8",
            )
            self.assertEqual(content_signals(source, root), {
                "exercise_answer_pairs_signal": 1,
                "pinned_revision_link_signal": True,
                "existing_fixture_link_signal": True,
            })
            fixture.unlink()
            self.assertFalse(content_signals(source, root)["existing_fixture_link_signal"])

    def test_draft_is_counted_but_not_approved_or_published(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            courses = root / "state/streeling/courses/example"
            (courses / "en").mkdir(parents=True)
            (courses / "en/README.md").write_text("catalog", encoding="utf-8")
            (courses / "en/ex-001-project.md").write_text("draft", encoding="utf-8")
            (root / "state/streeling").mkdir(parents=True, exist_ok=True)
            (root / "state/streeling/university.json").write_text(
                json.dumps({"departments": ["example"]}), encoding="utf-8"
            )
            policy = root / "policies/multilingual-policy.yaml"
            policy.parent.mkdir()
            policy.write_text(
                "supported_languages:\n  primary:\n    - {code: en, status: active}\n"
                "    - {code: fr, status: active}\n", encoding="utf-8"
            )
            result = inventory(root)
            item = result["departments"][0]
            self.assertEqual(item["authored_en"], 1)
            self.assertEqual(item["remaining_to_25"], 24)
            self.assertEqual(item["active_language_complete"], 0)
            self.assertEqual(item["pipeline_review_approved"], 0)
            self.assertEqual(item["modules"][0]["missing_active_languages"], ["fr"])

    def test_review_record_is_reported_only_after_explicit_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            courses = root / "state/streeling/courses/example"
            for lang in ("en", "fr"):
                (courses / lang).mkdir(parents=True)
            (courses / "en/ex-001-project.md").write_text("lesson", encoding="utf-8")
            (courses / "fr/ex-001-project.fr.md").write_text("leçon", encoding="utf-8")
            (root / "state/streeling/university.json").write_text(
                json.dumps({"departments": ["example"]}), encoding="utf-8"
            )
            policy = root / "policies/multilingual-policy.yaml"
            policy.parent.mkdir()
            policy.write_text(
                "supported_languages:\n  primary:\n    - {code: en, status: active}\n"
                "    - {code: fr, status: active}\n", encoding="utf-8"
            )
            productions = root / "state/streeling/course-productions"
            productions.mkdir()
            (productions / "one.json").write_text(json.dumps({
                "department": "example", "module_id": "ex-001-project",
                "phases": {"review": {"completed": True, "verdict": "revise"}},
            }), encoding="utf-8")
            self.assertEqual(inventory(root)["totals"]["pipeline_review_approved"], 0)
            (productions / "one.json").write_text(json.dumps({
                "department": "example", "module_id": "ex-001-project",
                "phases": {"review": {"completed": True, "verdict": "approved"}},
            }), encoding="utf-8")
            result = inventory(root)
            self.assertEqual(result["totals"]["active_language_complete"], 1)
            self.assertEqual(result["totals"]["pipeline_review_approved"], 1)


if __name__ == "__main__":
    unittest.main()
