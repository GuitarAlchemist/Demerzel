#!/usr/bin/env python3
"""Anti-LOLLI guard for generated assets (epic #724).

An asset with no consumer is exactly the LOLLI failure mode this ecosystem exists
to prevent. This guard fails if anything under assets/generated/ is orphaned:
- a <id>.png with no sibling <id>.provenance.json, or
- a <id>.provenance.json whose consumer_ref is missing/empty.

Green when clean (including when the directory does not exist). Its logic is proven
by scripts/test_asset_consumer_guard.py via fixtures, so a vacuously-green CI run is
not the only evidence it works.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSETS_DIR = REPO_ROOT / "assets" / "generated"


def find_orphans(assets_dir: Path) -> list[str]:
    """Return a list of human-readable orphan reasons; empty means clean."""
    if not assets_dir.exists():
        return []
    orphans: list[str] = []

    for png in sorted(assets_dir.glob("*.png")):
        prov = png.with_suffix("").with_suffix(".provenance.json")
        # png "<id>.png" -> provenance "<id>.provenance.json"
        prov = assets_dir / f"{png.stem}.provenance.json"
        if not prov.exists():
            orphans.append(f"{png.name}: no provenance manifest")

    for prov in sorted(assets_dir.glob("*.provenance.json")):
        try:
            data = json.loads(prov.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            orphans.append(f"{prov.name}: unreadable ({error})")
            continue
        ref = data.get("consumer_ref") if isinstance(data, dict) else None
        if not isinstance(ref, str) or not ref.strip():
            orphans.append(f"{prov.name}: missing/empty consumer_ref")

    return orphans


def main(argv: list[str] | None = None) -> int:
    assets_dir = DEFAULT_ASSETS_DIR
    if argv:
        assets_dir = Path(argv[0])
    orphans = find_orphans(assets_dir)
    if orphans:
        print("anti-LOLLI guard: orphaned generated assets found:", file=sys.stderr)
        for reason in orphans:
            print(f"  - {reason}", file=sys.stderr)
        return 1
    print(f"anti-LOLLI guard: clean ({assets_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
