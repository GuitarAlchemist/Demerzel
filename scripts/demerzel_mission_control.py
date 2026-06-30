#!/usr/bin/env python3
"""
Demerzel Mission Control dry-run report.

This is the first executable wedge for the Demerzel fan-out/fan-in loop.
It is intentionally advisory-only: it reads PR metadata and prints a Markdown
review/backpressure report. It never mutates GitHub state and never merges.

Usage examples:

  python scripts/demerzel_mission_control.py --input open-prs.json
  GITHUB_TOKEN=... python scripts/demerzel_mission_control.py --repo GuitarAlchemist/Demerzel

Local JSON input may be either a GitHub `/pulls`-style list or an object with a
`pull_requests` list.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    url: str
    draft: bool
    mergeable: bool | None
    changed_files: int | None
    additions: int | None
    deletions: int | None
    updated_at: str | None
    base: str | None

    @property
    def normalized_title(self) -> str:
        return self.title.lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit an advisory Demerzel Mission Control report.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Path to a local JSON file containing PR metadata.")
    source.add_argument("--repo", help="GitHub repository in owner/name form. Requires GITHUB_TOKEN unless public access is enough.")
    parser.add_argument("--max-open-prs", type=int, default=5, help="Open PR threshold for DRAINING mode.")
    parser.add_argument("--max-draft-prs", type=int, default=2, help="Draft PR threshold for DRAINING mode.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def load_input(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("pull_requests", "prs", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Input JSON must be a list or an object with pull_requests/prs/items.")


def github_get_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "demerzel-mission-control-dry-run",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub request failed: {exc.code} {exc.reason}: {body}") from exc


def load_github_prs(repo: str) -> list[dict[str, Any]]:
    if "/" not in repo:
        raise ValueError("--repo must be in owner/name form")
    token = os.environ.get("GITHUB_TOKEN")
    pulls_url = f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=100"
    pulls = github_get_json(pulls_url, token)
    if not isinstance(pulls, list):
        raise RuntimeError("GitHub pulls response was not a list")

    enriched: list[dict[str, Any]] = []
    for item in pulls:
        number = item.get("number")
        if not isinstance(number, int):
            continue
        detail_url = f"https://api.github.com/repos/{repo}/pulls/{number}"
        details = github_get_json(detail_url, token)
        if isinstance(details, dict):
            merged = dict(item)
            merged.update({
                "mergeable": details.get("mergeable"),
                "changed_files": details.get("changed_files"),
                "additions": details.get("additions"),
                "deletions": details.get("deletions"),
            })
            enriched.append(merged)
    return enriched


def normalize_pr(raw: dict[str, Any]) -> PullRequest:
    base_value = raw.get("base")
    base_name = None
    if isinstance(base_value, dict):
        base_name = base_value.get("ref")
    elif isinstance(base_value, str):
        base_name = base_value

    html_url = raw.get("html_url") or raw.get("url") or raw.get("display_url") or ""
    return PullRequest(
        number=int(raw.get("number") or raw.get("issue_number")),
        title=str(raw.get("title") or raw.get("display_title") or "untitled"),
        url=str(html_url),
        draft=bool(raw.get("draft", False)),
        mergeable=raw.get("mergeable"),
        changed_files=as_optional_int(raw.get("changed_files")),
        additions=as_optional_int(raw.get("additions")),
        deletions=as_optional_int(raw.get("deletions")),
        updated_at=raw.get("updated_at"),
        base=base_name,
    )


def as_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def classify_mode(prs: list[PullRequest], max_open_prs: int, max_draft_prs: int) -> tuple[str, list[str]]:
    open_count = len(prs)
    draft_count = sum(1 for pr in prs if pr.draft)
    unmergeable_count = sum(1 for pr in prs if pr.mergeable is False)

    if open_count >= max_open_prs or draft_count >= max_draft_prs:
        return "DRAINING", [
            f"open_prs={open_count} threshold={max_open_prs}",
            f"draft_prs={draft_count} threshold={max_draft_prs}",
        ]
    if unmergeable_count > 0 or open_count >= max(1, max_open_prs - 2):
        return "CONSTRAINED", [
            f"open_prs={open_count}",
            f"unmergeable_prs={unmergeable_count}",
        ]
    return "NORMAL", [f"open_prs={open_count}", f"draft_prs={draft_count}"]


def priority_score(pr: PullRequest) -> tuple[int, str]:
    title = pr.normalized_title
    rules: list[tuple[int, str, tuple[str, ...]]] = [
        (100, "planner foundation", ("execution graph", "work package", "planner schema")),
        (95, "fan-out/fan-in control", ("fan-out", "fanin", "fan-in", "backpressure", "draining")),
        (90, "mission control", ("mission control", "review queue")),
        (80, "definition of ready/done", ("definition of ready", "definition of done", "dor", "dod")),
        (70, "process model", ("agile", "xp", "operating model")),
        (60, "seldon facts", ("seldon", "fact", "duckdb")),
        (50, "token economics", ("token", "economics", "cost")),
    ]
    for score, reason, needles in rules:
        if any(needle in title for needle in needles):
            return score, reason
    if pr.changed_files is not None and pr.changed_files <= 3:
        return 45, "small review surface"
    return 10, "default ordering"


def blockers_for(pr: PullRequest) -> list[str]:
    blockers: list[str] = []
    if pr.draft:
        blockers.append("draft_pr")
    if pr.mergeable is False:
        blockers.append("not_mergeable")
    if pr.base and pr.base != "master":
        blockers.append(f"base_is_{pr.base}_not_master")
    return blockers


def ranked_queue(prs: list[PullRequest]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pr in prs:
        score, reason = priority_score(pr)
        blockers = blockers_for(pr)
        if blockers:
            score -= 5
        rows.append({
            "number": pr.number,
            "title": pr.title,
            "url": pr.url,
            "score": score,
            "reason": reason,
            "draft": pr.draft,
            "mergeable": pr.mergeable,
            "changed_files": pr.changed_files,
            "blockers": blockers,
            "next_action": next_action_for(pr, blockers, reason),
        })
    return sorted(rows, key=lambda row: (-row["score"], row["number"]))


def next_action_for(pr: PullRequest, blockers: list[str], reason: str) -> str:
    if pr.number == 567 or "execution graph" in pr.normalized_title:
        return "Fix semantic blockers, then move to ready-for-review."
    if "draft_pr" in blockers:
        return "Triage draft-to-ready requirements before review."
    if "not_mergeable" in blockers:
        return "Resolve mergeability before review."
    if reason in {"fan-out/fan-in control", "mission control"}:
        return "Review next; this reduces queue pressure."
    return "Review when higher-priority control PRs are drained."


def build_report(prs: list[PullRequest], max_open_prs: int, max_draft_prs: int) -> dict[str, Any]:
    mode, reasons = classify_mode(prs, max_open_prs, max_draft_prs)
    queue = ranked_queue(prs)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "mode_reasons": reasons,
        "summary": {
            "open_prs": len(prs),
            "draft_prs": sum(1 for pr in prs if pr.draft),
            "mergeable_true": sum(1 for pr in prs if pr.mergeable is True),
            "mergeable_false": sum(1 for pr in prs if pr.mergeable is False),
            "mergeable_unknown": sum(1 for pr in prs if pr.mergeable is None),
        },
        "queue": queue,
        "policy": {
            "advisory_only": True,
            "mutates_github": False,
            "merge_allowed": False,
        },
        "next_safe_actions": next_safe_actions(mode, queue),
    }


def next_safe_actions(mode: str, queue: list[dict[str, Any]]) -> list[str]:
    actions = []
    if mode == "DRAINING":
        actions.append("Pause new feature fan-out.")
        actions.append("Convert review effort to draft-to-ready fixes and small control PR reviews.")
    if queue:
        first = queue[0]
        actions.append(f"Start with PR #{first['number']}: {first['next_action']}")
    actions.append("Keep output advisory; do not auto-merge.")
    return actions


def print_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print("# Demerzel Mission Control Dry-Run")
    print()
    print(f"Generated: `{report['generated_at']}`")
    print(f"Mode: **{report['mode']}**")
    print()
    print("## Summary")
    print()
    print(f"- Open PRs: {summary['open_prs']}")
    print(f"- Draft PRs: {summary['draft_prs']}")
    print(f"- Mergeable true: {summary['mergeable_true']}")
    print(f"- Mergeable false: {summary['mergeable_false']}")
    print(f"- Mergeable unknown: {summary['mergeable_unknown']}")
    print()
    print("## Mode reasons")
    print()
    for reason in report["mode_reasons"]:
        print(f"- `{reason}`")
    print()
    print("## Review queue")
    print()
    print("| Rank | PR | Score | Reason | Draft | Mergeable | Blockers | Next action |")
    print("| ---: | --- | ---: | --- | --- | --- | --- | --- |")
    for index, row in enumerate(report["queue"], start=1):
        blockers = ", ".join(row["blockers"]) if row["blockers"] else "-"
        print(
            f"| {index} | #{row['number']} {escape_md(row['title'])} | {row['score']} | "
            f"{escape_md(row['reason'])} | {row['draft']} | {row['mergeable']} | "
            f"{escape_md(blockers)} | {escape_md(row['next_action'])} |"
        )
    print()
    print("## Next safe actions")
    print()
    for action in report["next_safe_actions"]:
        print(f"- {action}")
    print()
    print("## Guardrails")
    print()
    print("- Advisory only.")
    print("- No GitHub mutation.")
    print("- No auto-merge.")


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    args = parse_args()
    try:
        raw_prs = load_input(args.input) if args.input else load_github_prs(args.repo)
        prs = [normalize_pr(item) for item in raw_prs]
        report = build_report(prs, args.max_open_prs, args.max_draft_prs)
    except Exception as exc:  # noqa: BLE001 - CLI should report concise failure.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_markdown(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
