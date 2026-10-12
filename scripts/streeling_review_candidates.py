#!/usr/bin/env python3
"""List bounded Streeling review candidates at the current clean Git HEAD.

Content signals and packet presence help triage; they never grant approval.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from streeling_course_progress import COURSE_CODE, ROOT, inventory


SOURCE_PATHS = (
    "state/streeling/courses",
    "state/streeling/course-productions",
    "state/streeling/departments",
    "state/streeling/university.json",
    "policies/multilingual-policy.yaml",
)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE).decode("utf-8").strip()


def committed_blobs(root: Path, commit: str) -> dict[str, str]:
    result = {}
    for line in git(root, "ls-tree", "-r", "--full-tree", commit,
                    "state/streeling/courses", "state/streeling/reviews").splitlines():
        metadata, path = line.split("\t", 1)
        mode, kind, blob = metadata.split()
        if mode == "100644" and kind == "blob":
            result[path] = blob
    return result


def review_candidates(root: Path = ROOT) -> dict:
    root = root.resolve()
    modified = git(root, "status", "--porcelain", "--untracked-files=all", "--", *SOURCE_PATHS)
    ignored = git(root, "ls-files", "--others", "--ignored", "--exclude-standard", "--", *SOURCE_PATHS)
    if modified or ignored:
        raise ValueError("Streeling source has local changes; commit or move them before attributing review targets to HEAD")

    commit = git(root, "rev-parse", "HEAD")
    blobs = committed_blobs(root, commit)
    report = inventory(root)
    candidates = []
    full_locale_with_answers = 0
    packet_count = 0
    for department in report["departments"]:
        for module in department["modules"]:
            match = COURSE_CODE.match(module["id"])
            code = match.group(1) if match else module["id"]
            packet = f"state/streeling/reviews/{code}-review-brief.md"
            learner_task = f"state/streeling/reviews/{code}-learner-task.md"
            has_packet = packet in blobs
            if has_packet:
                packet_count += 1
            signal = module["content_signals"]
            five_answers = signal["exercise_answer_pairs_signal"] >= 5
            full_locale = not module["missing_active_languages"]
            full_locale_with_answers += int(full_locale and five_answers)
            if not five_answers or not (full_locale or has_packet):
                continue
            locale_blobs = {}
            for locale in module["languages_present"]:
                suffix = "" if locale == "en" else f".{locale}"
                path = f"state/streeling/courses/{department['department']}/{locale}/{module['id']}{suffix}.md"
                if path not in blobs:
                    raise ValueError(f"missing committed blob for {path}")
                locale_blobs[locale] = blobs[path]
            candidates.append({
                "department": department["department"],
                "module_id": module["id"],
                "course_code": code,
                "locale_blobs": locale_blobs,
                "five_answer_pairs_signal": five_answers,
                "pinned_revision_link_signal": signal["pinned_revision_link_signal"],
                "six_active_locale_sources": full_locale,
                "review_brief": packet if has_packet else None,
                "learner_task": learner_task if learner_task in blobs else None,
                "pipeline_review_flag": module["pipeline_review_approved"],
            })
    candidates.sort(key=lambda item: (item["review_brief"] is None,
                                      not item["six_active_locale_sources"],
                                      item["department"], item["module_id"]))
    return {
        "source_commit": commit,
        "department_directories": report["totals"]["department_directories"],
        "target_core_courses": report["totals"]["department_directories"] * report["target_per_department"],
        "core_course_codes": report["totals"]["core_course_codes"],
        "authored_english": report["totals"]["authored_en"],
        "six_locale_and_five_answer_pair_candidates": full_locale_with_answers,
        "committed_review_briefs": packet_count,
        "listed_candidates": len(candidates),
        "candidates": candidates,
        "caveat": "This is source and triage evidence only. A five-answer signal, six locale files, a review brief, or a pipeline flag does not authenticate a human verdict, learner outcome, or public publication.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="write JSON to this path")
    args = parser.parse_args()
    result = review_candidates(args.root)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
