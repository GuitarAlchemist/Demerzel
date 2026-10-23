#!/usr/bin/env python3
"""Proof that the anti-LOLLI asset guard actually detects orphans (epic #724).

Fixture-based so the guard's logic is verified even when the repo commits no
generated assets (which would make a live scan vacuously green).
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import asset_consumer_guard as guard


def _write(dir_: Path, asset_id: str, consumer_ref, with_png=True):
    if with_png:
        (dir_ / f"{asset_id}.png").write_bytes(b"\x89PNG")
    prov = {"schema_version": "1.0", "id": asset_id, "provider": "comfyui-local",
            "consumer_ref": consumer_ref}
    (dir_ / f"{asset_id}.provenance.json").write_text(json.dumps(prov), encoding="utf-8")


class AssetGuardTests(unittest.TestCase):
    def test_missing_dir_is_clean(self):
        self.assertEqual(guard.find_orphans(Path("/no/such/dir")), [])

    def test_asset_with_consumer_ref_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            _write(Path(d), "ok", "solar-system viz: gas giant")
            self.assertEqual(guard.find_orphans(Path(d)), [])

    def test_png_without_provenance_is_orphan(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "loose.png").write_bytes(b"\x89PNG")
            orphans = guard.find_orphans(Path(d))
            self.assertTrue(any("loose.png" in o for o in orphans))

    def test_empty_consumer_ref_is_orphan(self):
        with tempfile.TemporaryDirectory() as d:
            _write(Path(d), "empty", "")
            orphans = guard.find_orphans(Path(d))
            self.assertTrue(any("consumer_ref" in o for o in orphans))

    def test_repo_generated_dir_is_clean(self):
        # The committed repo must never carry an orphaned asset.
        self.assertEqual(guard.find_orphans(guard.DEFAULT_ASSETS_DIR), [])


if __name__ == "__main__":
    unittest.main()
