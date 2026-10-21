"""Layout tests for the Streeling course fixtures.

The programs live under scripts/streeling_fixtures/<department>/<module>/ and their data under
state/streeling/fixtures/<department>/<module>/ (CONTRIBUTING.md: no executable code outside scripts/).
These tests keep the two halves together. They do not rerun the analyses unless STREELING_FIXTURE_CHECK=1,
because some take half a minute.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

import demerzel_kit as kit

REPO_ROOT = kit.ROOT
PROGRAMS = REPO_ROOT / "scripts" / "streeling_fixtures"
DATA = REPO_ROOT / "state" / "streeling" / "fixtures"


def modules() -> list[Path]:
    return sorted(p for p in PROGRAMS.glob("*/*") if p.is_dir() and p.name != "__pycache__")


class StreelingFixtureLayoutTest(unittest.TestCase):
    def test_some_module_exists(self) -> None:
        self.assertTrue(modules(), f"no module folder under {PROGRAMS}")

    def test_programs_compile(self) -> None:
        for program in sorted(PROGRAMS.glob("*/*/*.py")):
            with self.subTest(program=program.relative_to(REPO_ROOT).as_posix()):
                compile(program.read_text(encoding="utf-8"), str(program), "exec")

    def test_each_module_has_its_program_and_its_data(self) -> None:
        for module in modules():
            data = DATA / module.parent.name / module.name
            with self.subTest(module=module.relative_to(PROGRAMS).as_posix()):
                self.assertTrue((module / "analyze.py").is_file(), "analyze.py missing")
                expected = ["scenarios.json", "results.json", "README.md"]
                if (module / "extract.py").is_file():
                    expected.append("observed-input.json")
                missing = [name for name in expected if not (data / name).is_file()]
                self.assertEqual(missing, [], f"missing in {data.relative_to(REPO_ROOT).as_posix()}")

    def test_no_program_is_left_next_to_the_data(self) -> None:
        stray = sorted(p.relative_to(REPO_ROOT).as_posix() for p in DATA.glob("*/*/*.py")
                       if (PROGRAMS / p.parent.parent.name / p.parent.name).is_dir())
        self.assertEqual(stray, [])

    @unittest.skipUnless(os.environ.get("STREELING_FIXTURE_CHECK") == "1",
                         "set STREELING_FIXTURE_CHECK=1 to rerun every analysis")
    def test_saved_results_match_a_fresh_run(self) -> None:
        for module in modules():
            with self.subTest(module=module.relative_to(PROGRAMS).as_posix()):
                done = subprocess.run(
                    [sys.executable, "-I", "-B", str(module / "analyze.py"), "--check"],
                    cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=300)
                self.assertEqual(done.returncode, 0, (done.stdout + done.stderr)[-600:])


if __name__ == "__main__":
    unittest.main()
