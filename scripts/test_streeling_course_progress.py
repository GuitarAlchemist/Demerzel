"""Focused checks for the Streeling source progress report."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.streeling_course_progress import inventory


class StreelingCourseProgressTests(unittest.TestCase):
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
