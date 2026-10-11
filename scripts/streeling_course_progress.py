"""Report Streeling source progress without treating drafts as published courses.

Run from the repository root: python scripts/streeling_course_progress.py
The public Learn catalog and human review evidence need separate verification.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TARGET_PER_DEPARTMENT = 25


def active_languages(policy: dict) -> list[str]:
    tiers = policy["supported_languages"]
    return [
        entry["code"]
        for entries in tiers.values()
        for entry in entries
        if entry["status"] == "active"
    ]


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
        },
        "unregistered_course_directories": sorted(directory_names - registered),
        "registered_without_course_directory": sorted(registered - directory_names),
        "caveat": "Source inventory only. Approval records do not prove native review or public Learn publication.",
    }


if __name__ == "__main__":
    print(json.dumps(inventory(), indent=2, ensure_ascii=False))
