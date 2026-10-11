#!/usr/bin/env python3
"""Read-only consistency checks for selected Streeling course packages.

Usage: python scripts/streeling_course_preflight.py [--root REPO] CP_ID_OR_PATH [...]
This checks source and records, not subject quality, review, or publication.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import jsonschema
import yaml

if __package__:
    from .streeling_course_progress import EXERCISE_HEADING, HEADING, content_signals
else:
    from streeling_course_progress import EXERCISE_HEADING, HEADING, content_signals


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LANGUAGE = re.compile(r"[a-z]{2,3}(?:-[a-z0-9]+)*\Z")


def production_path(root: Path, item: str) -> Path:
    """Bare IDs resolve in course-productions; explicit paths are root-relative."""
    path = Path(item)
    if path.is_absolute():
        return path
    if len(path.parts) > 1:
        return root / path
    return root / "state/streeling/course-productions" / f"{path.stem}.json"


def read_json(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: cannot read JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path}: expected a JSON object")
        return None
    return value


def schema_errors(value: dict, schema: dict, label: str) -> list[str]:
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    return [
        f"{label} schema {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(value), key=lambda e: (list(map(str, e.path)), e.message))
    ]


def read_frontmatter(path: Path, errors: list[str]) -> tuple[str, dict] | None:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read course source: {exc}")
        return None
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{path}: missing opening YAML frontmatter delimiter")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path}: missing closing YAML frontmatter delimiter")
        return None
    try:
        metadata = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        errors.append(f"{path}: invalid YAML frontmatter: {exc}")
        return None
    if not isinstance(metadata, dict):
        errors.append(f"{path}: YAML frontmatter must be a mapping")
        return None
    return source, metadata


def exercise_heading_count(source: str) -> int:
    """Count exercises, excluding an unnumbered heading that groups child exercises."""
    lines = source.splitlines()
    count = 0
    for index, line in enumerate(lines):
        if not EXERCISE_HEADING.match(line):
            continue
        level = len(line) - len(line.lstrip("#"))
        title = line[level:].strip()
        if re.fullmatch(r"practice\s+exercise", title, re.IGNORECASE):
            next_heading = next((later for later in lines[index + 1:] if HEADING.match(later)), "")
            next_level = len(next_heading) - len(next_heading.lstrip("#"))
            if next_level > level and EXERCISE_HEADING.match(next_heading):
                continue
        count += 1
    return count


def check_package(root: Path, item: str, production_schema: dict, research_schema: dict) -> tuple[str, list[str]]:
    path = production_path(root, item)
    errors: list[str] = []
    production = read_json(path, errors)
    if production is None:
        return item, errors
    errors.extend(schema_errors(production, production_schema, str(path)))
    if errors:
        return item, errors

    pipeline_id = production["pipeline_id"]
    department = production["department"]
    module_id = production["module_id"]
    cycle_id = production["research_cycle_id"]
    label = pipeline_id
    if path.stem != pipeline_id:
        errors.append(f"{path}: filename ID differs from pipeline_id {pipeline_id!r}")
    for field, value in (("department", department), ("module_id", module_id), ("research_cycle_id", cycle_id)):
        if not SLUG.fullmatch(value):
            errors.append(f"{field} {value!r} is not a safe lower-case slug")
    if errors:
        return label, errors

    research_path = root / "state/streeling/research-cycles" / f"{cycle_id}.json"
    research = read_json(research_path, errors)
    if research is not None:
        errors.extend(schema_errors(research, research_schema, str(research_path)))
        if research.get("cycle_id") != cycle_id:
            errors.append(f"{research_path}: cycle_id differs from production research_cycle_id {cycle_id!r}")
        if research.get("department") != department:
            errors.append(f"{research_path}: department differs from production department {department!r}")

    phases = production["phases"]
    if production["status"] == "in_progress":
        for phase in ("review", "publish"):
            if phases.get(phase, {}).get("completed") is not False:
                errors.append(f"in_progress requires phases.{phase}.completed=false")

    languages = phases.get("translation", {}).get("languages")
    if languages is None:
        errors.append("phases.translation.languages is missing; declared source languages cannot be checked")
        languages = []
    elif len(set(languages)) != len(languages):
        errors.append("phases.translation.languages contains duplicates")
    if "en" not in languages:
        errors.append("phases.translation.languages must declare the English source 'en'")

    course_dir = root / "state/streeling/courses" / department
    english = course_dir / "en" / f"{module_id}.md"
    for language in dict.fromkeys(["en", *languages]):
        if not LANGUAGE.fullmatch(language):
            errors.append(f"invalid declared language code {language!r}")
            continue
        source_path = english if language == "en" else course_dir / language / f"{module_id}.{language}.md"
        result = read_frontmatter(source_path, errors)
        if result is None:
            continue
        source, frontmatter = result
        for field, expected in (("module_id", module_id), ("department", department)):
            if frontmatter.get(field) != expected:
                errors.append(f"{source_path}: frontmatter {field}={frontmatter.get(field)!r}, expected {expected!r}")
        if "research_cycle" in frontmatter and frontmatter["research_cycle"] != cycle_id:
            errors.append(f"{source_path}: frontmatter research_cycle differs from {cycle_id!r}")
        if language != "en":
            continue
        recorded_words = phases.get("content", {}).get("word_count")
        actual_words = len(source.split())
        if recorded_words is None:
            errors.append("phases.content.word_count is missing")
        elif actual_words != recorded_words:
            errors.append(f"{source_path}: word_count {actual_words} != declared {recorded_words}")
        recorded_exercises = phases.get("content", {}).get("exercises")
        answered = content_signals(source_path, root)["exercise_answer_pairs_signal"]
        headings = exercise_heading_count(source)
        if recorded_exercises is None:
            errors.append("phases.content.exercises is missing")
        else:
            if headings != recorded_exercises:
                errors.append(f"{source_path}: exercise headings {headings} != declared {recorded_exercises}")
            if answered != recorded_exercises:
                errors.append(f"{source_path}: answered exercise pairs {answered} != declared {recorded_exercises}")
    return label, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("production", nargs="+", help="production IDs or JSON paths relative to --root")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root (default: this script's parent repo)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    bootstrap_errors: list[str] = []
    production_schema = read_json(root / "schemas/course-production.schema.json", bootstrap_errors)
    research_schema = read_json(root / "schemas/research-cycle.schema.json", bootstrap_errors)
    if bootstrap_errors:
        for error in bootstrap_errors:
            print(f"FAIL: {error}")
        return 1

    failures = 0
    for item in args.production:
        label, errors = check_package(root, item, production_schema, research_schema)
        if errors:
            failures += 1
            print(f"FAIL {label}:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {label}: schemas, source metadata, declared languages, word count, answered exercises, status consistency")
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(main())
