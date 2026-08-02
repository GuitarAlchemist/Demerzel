import tempfile
import unittest
from pathlib import Path

import backlog_facts


class BacklogFactsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / ".github" / "workflows").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_collects_mechanical_facts_without_counting_definition_or_prose(self):
        self.write("scripts/test_alpha.py", "")
        self.write("scripts/test_beta.py", "")
        self.write(
            "scripts/demerzel_kit.py",
            "from pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n",
        )
        self.write(
            "scripts/worker.py",
            '"""Path(__file__).resolve().parents[1] is prose."""\n'
            "from pathlib import Path\n"
            "HERE = Path(__file__).resolve().parents[1]\n"
            "ALSO_HERE = Path(__file__).resolve().parent.parent\n",
        )
        self.write("scripts/planner_alpha.py", "")
        self.write("scripts/planner_beta.py", "")
        self.write(
            "scripts/consumer.py",
            "# planner_alpha is part of the documented reference surface.\n"
            "import planner_alpha\nplanner_alpha.run()\n",
        )
        self.write("scripts/test_consumer.py", "import planner_beta\n")
        self.write(
            ".github/workflows/agent-blackbox.yml",
            "jobs:\n"
            "  audit:\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - name: Run audit\n"
            "        run: echo ok\n"
            "  enforce:\n"
            "    steps:\n"
            "      - name: Enforce\n"
            "        run: |\n"
            "          echo '- name: not a step'\n",
        )

        facts = backlog_facts.collect_facts(self.root)

        self.assertEqual(3, facts.test_module_count)
        self.assertEqual(2, facts.root_recompute_count)
        self.assertEqual(
            {"planner_alpha": 3, "planner_beta": 0},
            facts.planner_non_test_references,
        )
        self.assertEqual(3, facts.workflow_step_counts["agent-blackbox.yml"])

    def test_rendered_block_is_deterministic_and_names_each_fact(self):
        facts = backlog_facts.BacklogFacts(
            test_module_count=2,
            root_recompute_count=3,
            planner_non_test_references={"planner_beta": 0, "planner_alpha": 2},
            workflow_step_counts={"agent-blackbox.yml": 8},
        )

        block = backlog_facts.render_block(facts)

        self.assertIn("`python_test_modules` | 2", block)
        self.assertIn("`python_root_recomputations` | 3", block)
        self.assertLess(block.index("`planner_alpha_non_test_refs`"),
                        block.index("`planner_beta_non_test_refs`"))
        self.assertIn("`workflow_agent_blackbox_steps` | 8", block)

    def test_replace_generated_block_is_idempotent_and_requires_markers(self):
        original = (
            "before\n"
            f"{backlog_facts.BEGIN_MARKER}\n"
            "stale\n"
            f"{backlog_facts.END_MARKER}\n"
            "after\n"
        )
        replacement = "generated\n"

        updated = backlog_facts.replace_generated_block(original, replacement)

        self.assertEqual(
            "before\n"
            f"{backlog_facts.BEGIN_MARKER}\n"
            "generated\n"
            f"{backlog_facts.END_MARKER}\n"
            "after\n",
            updated,
        )
        self.assertEqual(updated, backlog_facts.replace_generated_block(updated, replacement))
        with self.assertRaisesRegex(ValueError, "exactly one generated block"):
            backlog_facts.replace_generated_block("no markers\n", replacement)


if __name__ == "__main__":
    unittest.main()
