#!/usr/bin/env python3
"""Query Claude compaction JSONL through DuckDB and emit fleet metrics as JSON."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def sql_literal(value: str) -> str:
    return value.replace("'", "''")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-path",
        type=Path,
        default=Path.home() / ".agents" / "compaction-events.jsonl",
    )
    args = parser.parse_args()
    if not args.log_path.exists():
        parser.error(f"telemetry log does not exist: {args.log_path}")
    duckdb = shutil.which("duckdb")
    if not duckdb:
        parser.error("duckdb CLI is required")
    source = sql_literal(args.log_path.resolve().as_posix())
    query = f"""
WITH events AS (
  SELECT * FROM read_json_auto('{source}', format='newline_delimited', union_by_name=true)
)
SELECT
  repo,
  count(*) AS lifecycle_events,
  count(*) FILTER (event = 'post_compact') AS completed_compactions,
  count(*) FILTER (event = 'session_rehydrated') AS recoveries,
  max(ts) AS latest_event,
  max(project_setting) FILTER (project_setting = 'obsolete-key') AS obsolete_project_setting
FROM events
GROUP BY repo
ORDER BY latest_event DESC, repo;
"""
    result = subprocess.run(
        [duckdb, "-json", "-c", query],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    sys.stdout.write(result.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
