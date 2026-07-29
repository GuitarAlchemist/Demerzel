"""Guard: no retired LLM model id may appear in live configuration.

A dated model snapshot is a time bomb. It works until its retirement date, then
every caller starts getting 404s — and if the caller swallows failures, the loop
dies green. This repo has now been bitten twice by the same id:

  1. council_emit's reviewer_b 404'd on claude-sonnet-4-20250514 and was fixed
     to a current model — but the identical id was left in four other places.
  2. Those four then took down demerzel-capability-expansion (#703), which had
     been failing weekly since 2026-06-22.

The fix for (1) was correct and local; what was missing was a sweep. This test
is that sweep, run continuously.

Scope note: only *live* configuration is scanned. docs/ and state/ legitimately
record retired ids as history (incident notes, digests, superseded specs), and
rewriting history to satisfy a linter would be worse than the bug.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Anthropic model ids past their retirement date, with the date for the record.
# Extend this as models retire; see the Claude API model catalogue.
RETIRED = {
    "claude-sonnet-4-20250514": "2026-06-15",
    "claude-opus-4-20250514": "2026-06-15",
    "claude-3-haiku-20240307": "2026-04-19",
    "claude-3-7-sonnet-20250219": "2026-02-19",
    "claude-3-5-haiku-20241022": "2026-02-19",
    "claude-3-opus-20240229": "2026-01-05",
    "claude-3-5-sonnet-20241022": "2025-10-28",
    "claude-3-5-sonnet-20240620": "2025-10-28",
    "claude-3-sonnet-20240229": "2025-07-21",
    "claude-2.1": "2025-07-21",
    "claude-2.0": "2025-07-21",
}

# Directories that actually drive behaviour. Anything here is executed or
# rendered into something executed.
LIVE_DIRS = (".github", "scripts", "templates", "pipelines", "tools")
LIVE_SUFFIXES = {".sh", ".yml", ".yaml", ".py", ".json", ".ps1", ".psm1"}

# This file necessarily names every retired id.
SELF = Path(__file__).name


def _live_files() -> list[Path]:
    out = []
    for d in LIVE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix not in LIVE_SUFFIXES:
                continue
            if p.name == SELF:
                continue
            out.append(p)
    return out


class TestNoRetiredModels(unittest.TestCase):
    def test_scan_covers_something(self):
        # A guard that scans nothing passes forever. Pin that it has material.
        files = _live_files()
        self.assertGreater(len(files), 20, "live-config scan found suspiciously few files")

    def test_no_retired_model_ids_in_live_config(self):
        offences = []
        for path in _live_files():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                # A line explaining *why* an id is retired is not a use of it.
                if "retired" in line.lower() or "#703" in line:
                    continue
                for model, retired_on in RETIRED.items():
                    if model in line:
                        rel = path.relative_to(ROOT).as_posix()
                        offences.append(f"{rel}:{lineno} uses {model} (retired {retired_on})")
        self.assertEqual(
            offences,
            [],
            "retired model id(s) in live config — these 404 at runtime:\n  "
            + "\n  ".join(offences),
        )

    def test_llm_call_seam_default_is_current(self):
        # The seam's default is the single highest-blast-radius model id in the
        # repo: every workflow that does not override it inherits this value.
        seam = ROOT / ".github" / "scripts" / "llm_call.sh"
        m = re.search(r'^CLAUDE_MODEL="\$\{LLM_CLAUDE_MODEL:-([^}]+)\}"', seam.read_text(encoding="utf-8"), re.M)
        self.assertIsNotNone(m, "could not parse CLAUDE_MODEL default out of llm_call.sh")
        default = m.group(1)
        self.assertNotIn(default, RETIRED, f"llm_call.sh defaults to retired model {default}")


if __name__ == "__main__":
    unittest.main()
