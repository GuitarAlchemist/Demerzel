#!/usr/bin/env python3
"""Fail closed when the deterministic quality-trend feeder stops producing proof."""
from __future__ import annotations

import argparse
import glob
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def newest_evidence(out_dir: str) -> tuple[datetime | None, str | None]:
    newest: datetime | None = None
    source: str | None = None
    for path in sorted(glob.glob(os.path.join(out_dir, "*.jsonl"))):
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = _parse_timestamp(row.get("timestamp"))
                if timestamp is not None and (newest is None or timestamp > newest):
                    newest, source = timestamp, path
    return newest, source


def evaluate(out_dir: str, now: datetime, max_stale_days: int) -> dict:
    newest, source = newest_evidence(out_dir)
    if newest is None:
        return {
            "stale": True,
            "age_days": None,
            "reason": "no quality-trend data found at all",
        }

    elapsed = now - newest
    age_days = elapsed.days
    return {
        "stale": elapsed > timedelta(days=max_stale_days),
        "age_days": age_days,
        "reason": (f"newest quality-trend row is {age_days}d old "
                   f"(threshold {max_stale_days}d) from {source}"),
    }


def sync_alert(result: dict, alert_path: Path, now: datetime,
               max_stale_days: int) -> None:
    if not result["stale"]:
        alert_path.unlink(missing_ok=True)
        return

    alert_path.parent.mkdir(parents=True, exist_ok=True)
    diagnostic = {
        "alert": "quality-trend-stale",
        "detected_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "newest_row_age_days": result["age_days"],
        "max_stale_days": max_stale_days,
        "reason": result["reason"],
        "likely_cause": "the demerzel-quality-trend feeder stopped running",
    }
    alert_path.write_text(
        json.dumps(diagnostic, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="state/quality-trend")
    parser.add_argument("--max-stale-days", type=int, default=3)
    parser.add_argument("--now", help="ISO8601 override for deterministic tests")
    args = parser.parse_args()

    now = _parse_timestamp(args.now) or datetime.now(timezone.utc)
    result = evaluate(args.out_dir, now, args.max_stale_days)
    alert_path = Path(args.out_dir) / ".freshness-alert.json"
    sync_alert(result, alert_path, now, args.max_stale_days)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        heading = "### 🔴 quality-trend STALE" if result["stale"] else "quality-trend fresh"
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(f"{heading}\n\n{result['reason']}\n")

    status = "STALE" if result["stale"] else "OK"
    print(f"{status}: {result['reason']}")
    return 1 if result["stale"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
