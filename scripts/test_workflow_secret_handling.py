"""No workflow may interpolate a secret into a shell script body.

Why (#846). `${{ secrets.X }}` inside a `run:` block is expanded by the Actions runner
into the shell SOURCE before bash ever parses it. A secret containing a quote, backtick,
newline or `$(` therefore breaks the script or executes as code. GitHub masks secrets in
the log, which hides the value but does nothing about the shell parsing it — masking is a
log feature, not a quoting mechanism.

The safe form passes the secret through `env:` and tests the variable, so the value is
data the shell receives rather than text the shell compiles:

    env:
      GOOGLE_AI_KEY: ${{ secrets.GOOGLE_AI_KEY }}
    run: |
      if [ -n "$GOOGLE_AI_KEY" ]; then

`cross-model-review.yml` had four occurrences, one per `case` branch. At the time this
test was written that was the only offender in the repository, so this pins a clean state
rather than grandfathering an allowlist — the moment an allowlist exists, the next
violation joins it instead of being fixed.

Scope note: this checks `run:` bodies only. `${{ secrets.X }}` in an `env:` block or a
`with:` input is the CORRECT usage and is deliberately not flagged.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - pyyaml is installed in CI
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
ACTIONS_EXPRESSION_RE = re.compile(r"\$\{\{.*?\}\}")
SECRET_LOOKUP_RE = re.compile(r"\bsecrets\s*(?:\.|\[)")


def _contains_secret_lookup(line):
    """Return whether an Actions expression reads from the secrets context."""
    return any(
        SECRET_LOOKUP_RE.search(expression)
        for expression in ACTIONS_EXPRESSION_RE.findall(line)
    )


def _run_blocks():
    """Yield (workflow_name, step_name, run_body) for every step that runs a script."""
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:  # a malformed workflow is its own failure
            raise AssertionError(f"{path.name} is not parseable YAML: {error}") from error
        if not isinstance(data, dict):
            continue
        for job in (data.get("jobs") or {}).values():
            if not isinstance(job, dict):
                continue
            for step in (job.get("steps") or []):
                if not isinstance(step, dict) or "run" not in step:
                    continue
                yield path.name, step.get("name", "<unnamed>"), str(step["run"])


@unittest.skipIf(yaml is None, "pyyaml not installed")
class TestWorkflowSecretHandling(unittest.TestCase):
    def test_workflows_are_discoverable(self):
        """Guard the guard: an empty scan would make the check below vacuously green."""
        blocks = list(_run_blocks())
        self.assertGreater(
            len(blocks), 20,
            "found almost no `run:` steps across .github/workflows — the scan is probably "
            "broken, and a broken scan passes silently. Fix the walk, do not relax this.")

    def test_no_secret_is_interpolated_into_a_script_body(self):
        offenders = []
        for workflow, step, body in _run_blocks():
            for number, line in enumerate(body.splitlines(), start=1):
                if _contains_secret_lookup(line):
                    offenders.append(f"{workflow} :: {step} :: line {number}: {line.strip()[:100]}")

        self.assertEqual(
            [], offenders,
            "secret interpolated into a shell script body:\n  "
            + "\n  ".join(offenders)
            + "\n\nThe runner expands `${{ secrets.X }}` into the script SOURCE before bash "
              "parses it, so a value containing a quote or backtick breaks the script or "
              "executes. Log masking does not prevent that. Pass the secret through `env:` "
              "and test the variable instead (#846).")

    def test_secret_lookup_detection_covers_dot_and_bracket_forms(self):
        for lookup in (
            "${{ secrets.TOKEN }}",
            "${{ secrets['TOKEN'] }}",
            '${{ secrets [ "TOKEN" ] }}',
        ):
            with self.subTest(lookup=lookup):
                self.assertTrue(_contains_secret_lookup(lookup))

        for safe in ("$TOKEN", "${{ vars.TOKEN }}", "${{ github.token }}"):
            with self.subTest(safe=safe):
                self.assertFalse(_contains_secret_lookup(safe))


if __name__ == "__main__":
    unittest.main()
