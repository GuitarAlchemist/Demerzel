#!/usr/bin/env python3
"""Fail-closed certification for repo-scoped Octopus review evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


IDENTITY_FIELDS = (
    "run_id",
    "task_id",
    "commit_range",
    "commit_fingerprint",
)
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def create_request(repo_root: Path | str,
                   runs_dir: Path | str,
                   run_id: str,
                   task_id: str,
                   commit_range: str,
                   required_providers: list[str]) -> Path:
    """Create a unique run request bound to the exact binary git diff."""
    if not SAFE_ID.fullmatch(run_id) or not SAFE_ID.fullmatch(task_id):
        raise ValueError("run_id and task_id must be filesystem-safe identifiers")
    if not required_providers or not all(
            isinstance(provider, str) and provider for provider in required_providers):
        raise ValueError("at least one required provider is required")

    repo_root = Path(repo_root).resolve()
    runs_dir = Path(runs_dir).resolve()
    expected_runs_dir = (repo_root / ".octo" / "runs").resolve()
    if runs_dir != expected_runs_dir:
        raise ValueError("runs_dir must be the repository's .octo/runs directory")
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "diff",
            "--binary",
            "--no-ext-diff",
            commit_range,
            "--",
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode(errors="replace").strip()
        raise ValueError(f"cannot fingerprint commit range: {message}")
    if not completed.stdout:
        raise ValueError("commit range produced an empty diff")

    run_dir = runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "providers").mkdir()
    request = {
        "schema_version": "1.0",
        "run_id": run_id,
        "task_id": task_id,
        "commit_range": commit_range,
        "commit_fingerprint": (
            "sha256:" + hashlib.sha256(completed.stdout).hexdigest()),
        "required_providers": sorted(set(required_providers)),
    }
    request_path = run_dir / "request.json"
    request_path.write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return request_path


def certify(request_path: Path | str,
            providers_dir: Path | str) -> dict[str, Any]:
    """Certify only evidence from the request's exact repo-scoped run directory."""
    request_path = Path(request_path).resolve()
    providers_dir = Path(providers_dir).resolve()
    request = _load_json(request_path)

    expected_dir = request_path.parent / "providers"
    if providers_dir != expected_dir.resolve():
        raise ValueError("provider evidence must come from the request run directory")
    if request_path.parent.name != request.get("run_id"):
        raise ValueError("request run_id must match its run directory name")

    required = request.get("required_providers")
    if not isinstance(required, list) or not required or not all(
            isinstance(provider, str) and provider for provider in required):
        raise ValueError("required_providers must be a non-empty string list")

    successful: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []
    stale_rejected: list[str] = []
    irrelevant_rejected: list[str] = []
    scorecard: dict[str, Any] = {}

    for result_path in sorted(providers_dir.glob("*.json")):
        result = _load_json(result_path)
        provider = result.get("provider")
        if not isinstance(provider, str) or not provider:
            irrelevant_rejected.append(result_path.stem)
            continue

        if any(result.get(field) != request.get(field)
               for field in IDENTITY_FIELDS):
            stale_rejected.append(provider)
            continue

        status = result.get("status")
        preflight = result.get("preflight")
        if status == "skipped":
            skipped.append(provider)
        elif (not isinstance(preflight, dict)
              or preflight.get("status") != "passed"):
            failed.append(provider)
        elif status == "success":
            evidence = result.get("evidence")
            if (not isinstance(evidence, dict)
                    or evidence.get("diff_received") is not True
                    or not evidence.get("files_reviewed")):
                irrelevant_rejected.append(provider)
                continue
            successful.append(provider)
            findings = evidence.get("findings", [])
            finding_ids = {
                finding.get("id")
                for finding in findings
                if isinstance(finding, dict) and finding.get("id")
            }
            provider_scorecard = result.get("scorecard", {})
            if isinstance(provider_scorecard, dict):
                for category, entry in provider_scorecard.items():
                    if not isinstance(category, str) or not isinstance(entry, dict):
                        continue
                    score = entry.get("score")
                    references = entry.get("finding_ids")
                    backed = (
                        isinstance(score, (int, float))
                        and not isinstance(score, bool)
                        and 0 <= score <= 10
                        and isinstance(references, list)
                        and bool(references)
                        and all(reference in finding_ids for reference in references)
                    )
                    if backed:
                        if scorecard.get(category) == "unknown":
                            scorecard[category] = {}
                        scorecard.setdefault(category, {})[provider] = {
                            "score": score,
                            "finding_ids": references,
                        }
                    else:
                        scorecard.setdefault(category, "unknown")
        else:
            failed.append(provider)

    missing_required = sorted(set(required) - set(successful))
    blocked = bool(missing_required or stale_rejected or irrelevant_rejected)
    return {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "task_id": request["task_id"],
        "commit_range": request["commit_range"],
        "commit_fingerprint": request["commit_fingerprint"],
        "certification": "BLOCKED" if blocked else "COMPLETE",
        "successful": sorted(successful),
        "failed": sorted(failed),
        "skipped": sorted(skipped),
        "stale_rejected": sorted(stale_rejected),
        "irrelevant_rejected": sorted(irrelevant_rejected),
        "missing_required": missing_required,
        "scorecard": dict(sorted(scorecard.items())),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create and certify repo-scoped Octopus review runs")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser(
        "init", help="create a run request bound to a git diff")
    init_parser.add_argument("--repo", required=True, type=Path)
    init_parser.add_argument("--runs-dir", required=True, type=Path)
    init_parser.add_argument("--run-id", required=True)
    init_parser.add_argument("--task-id", required=True)
    init_parser.add_argument("--commit-range", required=True)
    init_parser.add_argument(
        "--required-provider", action="append", required=True,
        dest="required_providers")

    certify_parser = commands.add_parser(
        "certify", help="certify current-run provider evidence")
    certify_parser.add_argument("--request", required=True, type=Path)
    certify_parser.add_argument("--providers-dir", required=True, type=Path)
    certify_parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            request_path = create_request(
                args.repo,
                args.runs_dir,
                args.run_id,
                args.task_id,
                args.commit_range,
                args.required_providers,
            )
            print(request_path)
            return 0
        report = certify(args.request, args.providers_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"octopus delivery gate: {error}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{report['certification']}: {args.output}")
    return 0 if report["certification"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
