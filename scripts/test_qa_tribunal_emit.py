import json
import tempfile
import unittest
import unittest.mock as mock
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_tribunal_emit as q
import demerzel_kit as kit

ROOT = Path(__file__).resolve().parents[1]

class TestTribunalBuilders(unittest.TestCase):
    def test_derive_blast_radius_single_layer(self):
        paths = ["docs/plans/my-plan.md"]
        blast = q.derive_blast_radius(paths)
        self.assertEqual(blast["layers_touched"], ["docs"])
        self.assertEqual(blast["invariants_at_risk"], [])
        self.assertAlmostEqual(blast["estimated_blast_score"], 0.2)

    def test_derive_blast_radius_multiple_layers(self):
        paths = ["docs/plans/my-plan.md", "ReactComponents/button.tsx", "Common/GA.Core/Program.cs"]
        blast = q.derive_blast_radius(paths)
        self.assertCountEqual(blast["layers_touched"], ["docs", "frontend", "core"])
        self.assertEqual(blast["invariants_at_risk"], [])
        self.assertAlmostEqual(blast["estimated_blast_score"], 0.6)

    def test_derive_blast_radius_invariants(self):
        paths = ["Common/GA.Business.ML/Embeddings/some.cs", "docs/contracts/something.schema.json"]
        blast = q.derive_blast_radius(paths)
        self.assertCountEqual(blast["layers_touched"], ["ai_ml", "docs"])
        self.assertCountEqual(blast["invariants_at_risk"], ["optick.dim=240", "schema-locked-contract"])
        self.assertAlmostEqual(blast["estimated_blast_score"], 0.7)  # 2 layers (0.4) + invariant (0.3)


class TestTribunalSeam(unittest.TestCase):
    def _fake_gh_json(self, args, **kwargs):
        if args[:2] == ["api", "repos/GuitarAlchemist/Demerzel/commits/abcdef1"]:
            return {"sha": "abcdef1"}
        if args[:2] == ["api", "repos/GuitarAlchemist/Demerzel/pulls/123"]:
            return {"head": {"sha": "abcdef1", "repo": {"full_name": "GuitarAlchemist/Demerzel"}}}
        return None

    def _fake_gh_text(self, args, **kwargs):
        if args[:2] == ["pr", "diff"]:
            return "docs/contracts/my.schema.json\nReactComponents/comp.tsx"
        return ""

    def test_main_sweep_writes_valid_schema(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(q, "SWEEP_ROOT", Path(d)):
                # Mock kit.now_iso to control output if needed, but not strictly necessary
                # Run the sweep
                res = q.main(["--sweep"])
                self.assertEqual(res, 0)

                # Check output exists
                files = list(Path(d).glob("*/*.json"))
                self.assertEqual(len(files), 1)

                on_disk = json.loads(files[0].read_text(encoding="utf-8"))
                self.assertEqual(on_disk["target"]["kind"], "scheduled_sweep")

                try:
                    import jsonschema
                    schema = json.loads((ROOT / "schemas/contracts/qa-verdict.schema.json").read_text(encoding="utf-8"))
                    jsonschema.validate(on_disk, schema)
                except ImportError:
                    pass

    def test_main_dispatch_payload_writes_valid_schema(self):
        payload = {
            "action": "repository_dispatch",
            "client_payload": {
                "repo": "GuitarAlchemist/Demerzel",
                "pr": 123,
                "head_sha": "abcdef1",
                "base_sha": "1234567890abcdef",
                "idempotency_key": "some-key"
            }
        }

        with tempfile.TemporaryDirectory() as d_env, tempfile.TemporaryDirectory() as d_out:
            event_path = Path(d_env) / "event.json"
            event_path.write_text(json.dumps(payload))

            with mock.patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event_path)}), \
                 mock.patch.object(q.kit, "gh_json", self._fake_gh_json), \
                 mock.patch.object(q.kit, "gh_text", self._fake_gh_text), \
                 mock.patch.object(q, "VERDICT_ROOT", Path(d_out)):

                res = q.main([])
                self.assertEqual(res, 0)

                files = list(Path(d_out).glob("*/*/*.json"))
                self.assertEqual(len(files), 1)

                on_disk = json.loads(files[0].read_text(encoding="utf-8"))
                self.assertEqual(on_disk["target"]["kind"], "pull_request")
                self.assertEqual(on_disk["target"]["repo"], "GuitarAlchemist/Demerzel")
                self.assertEqual(on_disk["target"]["ref"], "pr/123")

                self.assertCountEqual(on_disk["blast_radius"]["layers_touched"], ["docs", "frontend"])
                self.assertCountEqual(on_disk["blast_radius"]["invariants_at_risk"], ["schema-locked-contract"])

                try:
                    import jsonschema
                    schema = json.loads((ROOT / "schemas/contracts/qa-verdict.schema.json").read_text(encoding="utf-8"))
                    jsonschema.validate(on_disk, schema)
                except ImportError:
                    pass

if __name__ == "__main__":
    unittest.main()
