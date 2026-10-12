#!/usr/bin/env python3
"""Check literal source-term presence in WML-001 at one pinned Git commit.

This is a lexical inventory, not translation, cultural, or learner review.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


LANGUAGES = ("en", "fr", "es", "pt", "it", "de")
TERMS = ("rasgueado", "picado", "alzapúa", "compás", "golpe", "batidas", "la pompe")
SHA = re.compile(r"[0-9a-f]{40}\Z")
MODULE = "wml-001-guitar-around-the-world"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE).decode("utf-8").strip()


def source_path(language: str) -> str:
    suffix = "" if language == "en" else f".{language}"
    return f"state/streeling/courses/world-music-languages/{language}/{MODULE}{suffix}.md"


def check(root: Path, commit: str) -> dict:
    if not SHA.fullmatch(commit):
        raise ValueError("--ref must be a full lowercase Git commit SHA")
    resolved = git(root, "rev-parse", "--verify", f"{commit}^{{commit}}")
    languages: dict[str, dict] = {}
    for language in LANGUAGES:
        path = source_path(language)
        blob = git(root, "rev-parse", f"{resolved}:{path}")
        source = git(root, "show", f"{resolved}:{path}").casefold()
        present = {term: term.casefold() in source for term in TERMS}
        languages[language] = {"path": path, "blob": blob, "present": present}
    missing = [f"{language}:{term}" for language, row in languages.items()
               for term, present in row["present"].items() if not present]
    return {
        "module_id": MODULE,
        "source_commit": resolved,
        "terms": list(TERMS),
        "languages": languages,
        "checked_pairs": len(LANGUAGES) * len(TERMS),
        "missing": missing,
        "limit": "Case-insensitive literal presence anywhere in each source file; no semantic, cultural, or publication verdict.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument("--ref", required=True, help="full source commit SHA")
    parser.add_argument("--output", type=Path, help="write the JSON receipt to this path")
    parser.add_argument("--require-exact", action="store_true", help="exit 1 when any literal source term is absent")
    args = parser.parse_args()
    receipt = check(args.root.resolve(), args.ref)
    output = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return int(args.require_exact and bool(receipt["missing"]))


if __name__ == "__main__":
    raise SystemExit(main())
