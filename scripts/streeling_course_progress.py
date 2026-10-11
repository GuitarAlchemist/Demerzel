"""Report Streeling source progress without treating drafts as published courses.

Run from the repository root: python scripts/streeling_course_progress.py
The public Learn catalog and human review evidence need separate verification.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TARGET_PER_DEPARTMENT = 25
EXERCISE_HEADING = re.compile(r"^#{2,4}\s+(?:practice\s+)?exercise\b", re.IGNORECASE)
ANSWER_LINE = re.compile(r"^\s*>\s*(?:\*\*Answer:?\*\*|\*Solution:?\*|Answer:|Solution:)", re.IGNORECASE)
HEADING = re.compile(r"^#{1,4}\s+")
PINNED_REVISION_LINK = re.compile(
    r"https://github\.com/(?:GuitarAlchemist|spareilleux)/[^\s)]+/(?:blob|tree)/[0-9a-f]{40}(?:/|\b)",
    re.IGNORECASE,
)
MARKDOWN_LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")


def active_languages(policy: dict) -> list[str]:
    tiers = policy["supported_languages"]
    return [
        entry["code"]
        for entries in tiers.values()
        for entry in entries
        if entry["status"] == "active"
    ]


def content_signals(source: Path, root: Path) -> dict:
    """Conservative triage signals, never a pedagogical or publication verdict."""
    lesson = source.read_text(encoding="utf-8")
    lines = lesson.splitlines()
    paired_exercises = 0
    in_exercise = False
    has_answer = False
    for line in lines:
        if EXERCISE_HEADING.match(line):
            paired_exercises += int(in_exercise and has_answer)
            in_exercise = True
            has_answer = False
        elif HEADING.match(line):
            paired_exercises += int(in_exercise and has_answer)
            in_exercise = False
        elif in_exercise and ANSWER_LINE.match(line):
            has_answer = True
    paired_exercises += int(in_exercise and has_answer)

    fixture_link = False
    for match in MARKDOWN_LINK.finditer(lesson):
        target = match.group(1)
        if "fixtures/" not in target.replace("\\", "/"):
            continue
        candidate = (source.parent / target).resolve()
        if candidate.is_relative_to(root.resolve()) and candidate.is_file():
            fixture_link = True
            break
    return {
        "exercise_answer_pairs_signal": paired_exercises,
        "pinned_revision_link_signal": bool(PINNED_REVISION_LINK.search(lesson)),
        "existing_fixture_link_signal": fixture_link,
    }


def inventory(root: Path = ROOT) -> dict:
    courses = root / "state" / "streeling" / "courses"
    productions = root / "state" / "streeling" / "course-productions"
    policy = yaml.safe_load((root / "policies" / "multilingual-policy.yaml").read_text(encoding="utf-8"))
    languages = active_languages(policy)
    records = {}
    for path in productions.glob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        records.setdefault((record["department"], record["module_id"]), []).append(record)

    departments = []
    for department in sorted(path for path in courses.iterdir() if path.is_dir()):
        modules = []
        for source in sorted((department / "en").glob("*.md")):
            if source.name == "README.md":
                continue
            module_id = source.stem
            present = [
                lang for lang in languages
                if (source if lang == "en" else department / lang / f"{module_id}.{lang}.md").is_file()
            ]
            approvals = [
                record for record in records.get((department.name, module_id), [])
                if record.get("phases", {}).get("review", {}).get("completed") is True
                and record["phases"]["review"].get("verdict") == "approved"
            ]
            modules.append({
                "id": module_id,
                "languages_present": present,
                "missing_active_languages": [lang for lang in languages if lang not in present],
                "pipeline_review_approved": bool(approvals),
                "content_signals": content_signals(source, root),
            })
        departments.append({
            "department": department.name,
            "authored_en": len(modules),
            "remaining_to_25": max(0, TARGET_PER_DEPARTMENT - len(modules)),
            "active_language_complete": sum(not item["missing_active_languages"] for item in modules),
            "pipeline_review_approved": sum(item["pipeline_review_approved"] for item in modules),
            "modules": modules,
        })

    registered = set(json.loads((root / "state" / "streeling" / "university.json").read_text(encoding="utf-8"))["departments"])
    directory_names = {item["department"] for item in departments}
    return {
        "target_per_department": TARGET_PER_DEPARTMENT,
        "active_languages": languages,
        "departments": departments,
        "totals": {
            "department_directories": len(departments),
            "authored_en": sum(item["authored_en"] for item in departments),
            "remaining_to_25": sum(item["remaining_to_25"] for item in departments),
            "active_language_complete": sum(item["active_language_complete"] for item in departments),
            "pipeline_review_approved": sum(item["pipeline_review_approved"] for item in departments),
            "with_exercise_answer_pair_signal": sum(
                module["content_signals"]["exercise_answer_pairs_signal"] > 0
                for department in departments for module in department["modules"]
            ),
            "with_pinned_revision_link_signal": sum(
                module["content_signals"]["pinned_revision_link_signal"]
                for department in departments for module in department["modules"]
            ),
            "with_existing_fixture_link_signal": sum(
                module["content_signals"]["existing_fixture_link_signal"]
                for department in departments for module in department["modules"]
            ),
        },
        "unregistered_course_directories": sorted(directory_names - registered),
        "registered_without_course_directory": sorted(registered - directory_names),
        "caveat": "Source inventory and conservative content signals only. A signal is not proof of project usefulness, subject accuracy, native review, learner success, or public Learn publication.",
    }


if __name__ == "__main__":
    print(json.dumps(inventory(), indent=2, ensure_ascii=False))
