"""Focused fixtures for the read-only Streeling course preflight."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.streeling_course_preflight import DEFAULT_ROOT, main


PIPELINE_ID = "cp-example-2026-10-11-001"
CYCLE_ID = "example-2026-10-11-001"
MODULE_ID = "ex-001-evidence"


class CoursePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        schemas = self.root / "schemas"
        schemas.mkdir()
        for name in ("course-production.schema.json", "research-cycle.schema.json"):
            shutil.copyfile(DEFAULT_ROOT / "schemas" / name, schemas / name)

        course_dir = self.root / "state/streeling/courses/example"
        self.english = course_dir / "en" / f"{MODULE_ID}.md"
        self.french = course_dir / "fr" / f"{MODULE_ID}.fr.md"
        self.english.parent.mkdir(parents=True)
        self.french.parent.mkdir(parents=True)
        self.english.write_text(
            "---\nmodule_id: ex-001-evidence\ndepartment: example\n"
            f"research_cycle: {CYCLE_ID}\n---\n\n"
            "# Source\n### Practice exercise 1\nFirst question.\n> **Answer:** First answer.\n"
            "### Practice exercise 2\nSecond question.\n> *Solution:* Second answer.\n",
            encoding="utf-8",
        )
        self.french.write_text(
            "---\nmodule_id: ex-001-evidence\ndepartment: example\n---\n\n# Leçon\n",
            encoding="utf-8",
        )

        research_dir = self.root / "state/streeling/research-cycles"
        research_dir.mkdir(parents=True)
        (research_dir / f"{CYCLE_ID}.json").write_text(json.dumps({
            "cycle_id": CYCLE_ID,
            "department": "example",
            "question": "Does this fixture validate?",
            "production_path": ["fixture"],
            "hypothesis": "The records and source agree.",
            "test_method": "thought_experiment",
            "evidence": ["Fixed fixture"],
            "conclusion": "confirm",
            "belief_value": "P",
            "belief_confidence": 0.8,
            "duration_seconds": 0,
            "timestamp": "2026-10-11T00:00:00Z",
        }), encoding="utf-8")

        production_dir = self.root / "state/streeling/course-productions"
        production_dir.mkdir()
        self.production_path = production_dir / f"{PIPELINE_ID}.json"
        self.production = {
            "pipeline_id": PIPELINE_ID,
            "department": "example",
            "research_cycle_id": CYCLE_ID,
            "module_id": MODULE_ID,
            "status": "in_progress",
            "phases": {
                "research": {"completed": True},
                "outline": {"completed": True},
                "content": {
                    "completed": True,
                    "word_count": len(self.english.read_text(encoding="utf-8").split()),
                    "exercises": 2,
                },
                "translation": {"completed": False, "languages": ["en", "fr"]},
                "review": {"completed": False},
                "publish": {"completed": False},
            },
            "timestamp": "2026-10-11T00:00:00Z",
        }
        self.save_production()

    def save_production(self):
        self.production_path.write_text(json.dumps(self.production), encoding="utf-8")

    def run_preflight(self, item=PIPELINE_ID):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["--root", str(self.root), item])
        return status, output.getvalue()

    def test_valid_id_and_relative_path_pass_without_changing_files(self):
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        status, output = self.run_preflight()
        self.assertEqual(status, 0, output)
        self.assertIn(f"PASS {PIPELINE_ID}", output)
        relative = f"state/streeling/course-productions/{PIPELINE_ID}.json"
        status, output = self.run_preflight(relative)
        self.assertEqual(status, 0, output)
        self.assertEqual(before, {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()})

    def test_missing_answer_fails_declared_exercise_count(self):
        source = self.english.read_text(encoding="utf-8").replace("> *Solution:* Second answer.\n", "")
        self.english.write_text(source, encoding="utf-8")
        self.production["phases"]["content"]["word_count"] = len(source.split())
        self.save_production()
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("answered exercise pairs 1 != declared 2", output)

    def test_extra_unanswered_exercise_fails_heading_count(self):
        source = self.english.read_text(encoding="utf-8") + "### Exercise 3\nUnanswered question.\n"
        self.english.write_text(source, encoding="utf-8")
        self.production["phases"]["content"]["word_count"] = len(source.split())
        self.save_production()
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("exercise headings 3 != declared 2", output)

    def test_group_heading_does_not_add_a_phantom_exercise(self):
        source = self.english.read_text(encoding="utf-8")
        source = source.replace("### Practice exercise 1", "## Practice Exercise\n\n### Exercise 1", 1)
        self.english.write_text(source, encoding="utf-8")
        self.production["phases"]["content"]["word_count"] = len(source.split())
        self.save_production()
        status, output = self.run_preflight()
        self.assertEqual(status, 0, output)

    def test_schema_language_and_draft_gate_failures_are_reported(self):
        self.production["phases"]["review"]["completed"] = True
        self.production["phases"]["content"]["word_count"] += 1
        self.save_production()
        self.french.unlink()
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("in_progress requires phases.review.completed=false", output)
        self.assertIn("word_count", output)
        self.assertIn("cannot read course source", output)

    def test_invalid_research_schema_is_reported(self):
        research_path = self.root / "state/streeling/research-cycles" / f"{CYCLE_ID}.json"
        research = json.loads(research_path.read_text(encoding="utf-8"))
        del research["question"]
        research_path.write_text(json.dumps(research), encoding="utf-8")
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("research-cycle", output)
        self.assertIn("'question' is a required property", output)

    def test_filename_must_match_pipeline_id(self):
        self.production["pipeline_id"] = "cp-example-2026-10-11-999"
        self.save_production()
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("filename ID differs from pipeline_id", output)

    def test_numbered_code_collision_fails_even_when_slugs_differ(self):
        other = self.english.with_name("ex-001-other-topic.md")
        other.write_text("---\nmodule_id: ex-001-other-topic\n---\n", encoding="utf-8")
        status, output = self.run_preflight()
        self.assertEqual(status, 1)
        self.assertIn("numbered course code ex-001 also belongs to ['ex-001-other-topic']", output)


if __name__ == "__main__":
    unittest.main()
