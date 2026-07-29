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

  3. demerzel-ideation pinned claude-sonnet-4-6-20250514 (#860) — an id that
     never existed at all. An enumerated retired-id list cannot catch that: it
     was never a model, so it was never retired. Hence the second rule below,
     which rejects *any* dated claude-* literal in live config regardless of
     whether the date has passed. Undated aliases are the only safe form.

Scope note: only *live* configuration is scanned. docs/ and state/ legitimately
record retired ids as history (incident notes, digests, superseded specs), and
rewriting history to satisfy a linter would be worse than the bug.

Comments are stripped before scanning rather than exempted line-wise. The old
exemption skipped any line containing "retired", which meant
`CLAUDE_MODEL: claude-sonnet-4-20250514  # retired id kept on purpose` passed —
mutation testing during the #833 review confirmed it. Stripping keeps prose free
to name a bad id while still failing on the value that a runtime would read.
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

# Any dated Anthropic snapshot: claude-<something>-YYYYMMDD. Matches retired ids,
# not-yet-retired ids, and ids that never existed (#860) alike.
DATED_MODEL = re.compile(r"\bclaude-[a-z0-9.-]*-\d{8}\b")

# `#` starts a comment in every live suffix that has comments; .json has none, so
# a `#` there is ordinary string content and must not truncate the scan.
COMMENT = re.compile(r"(?:^|\s)#")

# This file necessarily names every retired id.
SELF = Path(__file__).name


def _code_of(line: str, suffix: str) -> str:
    """The part of `line` a runtime would read — comment text removed."""
    if suffix == ".json":
        return line
    m = COMMENT.search(line)
    return line[: m.start()] if m else line


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


def _live_code_lines():
    """Yield (path, lineno, code) for every live-config line, comments removed."""
    for path in _live_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            yield path, lineno, _code_of(line, path.suffix)


class TestNoRetiredModels(unittest.TestCase):
    def test_scan_covers_something(self):
        # A guard that scans nothing passes forever. Pin that it has material.
        files = _live_files()
        self.assertGreater(len(files), 20, "live-config scan found suspiciously few files")

    def test_no_retired_model_ids_in_live_config(self):
        offences = []
        for path, lineno, code in _live_code_lines():
            for model, retired_on in RETIRED.items():
                if model in code:
                    rel = path.relative_to(ROOT).as_posix()
                    offences.append(f"{rel}:{lineno} uses {model} (retired {retired_on})")
        self.assertEqual(
            offences,
            [],
            "retired model id(s) in live config — these 404 at runtime:\n  "
            + "\n  ".join(offences),
        )

    def test_no_dated_model_ids_in_live_config(self):
        # The stronger rule, and the one that catches ids no list can enumerate.
        # A dated snapshot is either already dead or scheduled to die; an id that
        # was never real (#860) is dead on arrival. Undated aliases are the only
        # form that stays live, so require them everywhere.
        offences = []
        for path, lineno, code in _live_code_lines():
            for hit in DATED_MODEL.findall(code):
                rel = path.relative_to(ROOT).as_posix()
                offences.append(f"{rel}:{lineno} pins dated snapshot {hit}")
        self.assertEqual(
            offences,
            [],
            "dated claude-* model id(s) in live config — use an undated alias:\n  "
            + "\n  ".join(offences),
        )

    def test_dated_rule_catches_the_ideation_id(self):
        # #860 regression pin: this id is not retired — it never existed — so the
        # RETIRED list is structurally blind to it. Assert the dated rule is not.
        self.assertTrue(DATED_MODEL.search("claude-sonnet-4-6-20250514"))
        self.assertNotIn("claude-sonnet-4-6-20250514", RETIRED)

    def test_comment_does_not_launder_a_live_value(self):
        # The mutation that beat the old line exemption. Trailing prose must not
        # excuse the value in front of it...
        self.assertTrue(
            DATED_MODEL.search(
                _code_of("  CLAUDE_MODEL: claude-sonnet-4-20250514  # retired id kept on purpose", ".yml")
            )
        )
        # ...while a line that is only prose stays free to name the id.
        self.assertFalse(
            DATED_MODEL.search(_code_of("  # it pinned claude-sonnet-4-6-20250514, which never existed", ".yml"))
        )
        # .json has no comment syntax — nothing may be stripped there.
        self.assertTrue(DATED_MODEL.search(_code_of('{"m": "claude-sonnet-4-20250514"} # x', ".json")))

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
