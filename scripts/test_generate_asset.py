#!/usr/bin/env python3
"""Offline proof of the generative-asset driver (epic #724, Slice 0 #726).

Exercises every LLM-testable layer without a GPU: placeholder injection, dry-run
stub, a real run through an injected fake ComfyUI client, fail-closed behavior, the
anti-LOLLI consumer requirement, and provenance shape against the schema. The
physical generation + render proof is out of scope here — it runs on local ComfyUI.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import generate_asset as ga


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = "assets/comfyui/workflows/tileable-gasgiant.json"


def _spec(**over):
    spec = {
        "id": "test-asset-1",
        "provider": "comfyui-local",
        "workflow": WORKFLOW,
        "model": "sd_xl_base_1.0.safetensors",
        "sampler": "euler",
        "seed": 424242,
        "prompt": "seamless tileable gas giant bands",
        "negative_prompt": "seams, text",
        "consumer_ref": "solar-system viz: gas giant material",
    }
    spec.update(over)
    return spec


class FakeClient:
    """Stands in for ComfyClient; records the workflow it was queued with."""

    def __init__(self, image=b"\x89PNGFAKE", fail=False):
        self.image = image
        self.fail = fail
        self.queued = None

    def queue_prompt(self, workflow):
        if self.fail:
            raise TimeoutError("comfy down")
        self.queued = workflow
        return "pid-1"

    def wait_for_image(self, prompt_id):
        return ("demerzel-asset_00001_.png", "", "output")

    def fetch_image(self, filename, subfolder, type_):
        return self.image


class RenderWorkflowTests(unittest.TestCase):
    def test_placeholders_are_injected_and_valid_json(self):
        text = (REPO_ROOT / WORKFLOW).read_text(encoding="utf-8")
        wf = ga._render_workflow(text, "a prompt", "a negative", 777)
        self.assertEqual(wf["6"]["inputs"]["text"], "a prompt")
        self.assertEqual(wf["7"]["inputs"]["text"], "a negative")
        self.assertEqual(wf["3"]["inputs"]["seed"], 777)  # int, not string

    def test_prompt_with_quotes_stays_injection_safe(self):
        text = (REPO_ROOT / WORKFLOW).read_text(encoding="utf-8")
        wf = ga._render_workflow(text, 'quote " and \\ backslash', "", 1)
        self.assertEqual(wf["6"]["inputs"]["text"], 'quote " and \\ backslash')


class GenerateTests(unittest.TestCase):
    def test_dry_run_writes_stub_and_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            prov = ga.generate(_spec(), Path(d), dry_run=True, now="2026-07-18T00:00:00Z")
            png = Path(d) / "test-asset-1.png"
            pj = Path(d) / "test-asset-1.provenance.json"
            self.assertTrue(png.exists() and pj.exists())
            self.assertEqual(png.read_bytes(), ga._STUB_PNG)
            self.assertTrue(prov["dry_run"])
            self.assertEqual(prov["provider"], "comfyui-local")
            self.assertEqual(len(prov["workflow_sha256"]), 64)

    def test_real_run_uses_injected_client(self):
        client = FakeClient(image=b"IMGBYTES")
        with tempfile.TemporaryDirectory() as d:
            prov = ga.generate(_spec(), Path(d), dry_run=False, client=client,
                               now="2026-07-18T00:00:00Z")
            self.assertEqual((Path(d) / "test-asset-1.png").read_bytes(), b"IMGBYTES")
            self.assertFalse(prov["dry_run"])
            # the fake client received the injected workflow with our prompt/seed
            self.assertEqual(client.queued["3"]["inputs"]["seed"], 424242)

    def test_fail_closed_when_comfy_unreachable(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(RuntimeError):
                ga.generate(_spec(), Path(d), dry_run=False, client=FakeClient(fail=True))

    def test_missing_consumer_ref_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                ga.generate(_spec(consumer_ref=""), Path(d), dry_run=True)

    def test_provider_must_be_comfyui_local(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                ga.generate(_spec(provider="jules"), Path(d), dry_run=True)

    def test_negative_seed_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                ga.generate(_spec(seed=-1), Path(d), dry_run=True)


class ProvenanceSchemaTests(unittest.TestCase):
    def test_dry_run_provenance_matches_schema_shape(self):
        schema = json.loads((REPO_ROOT / "schemas" / "asset-provenance.schema.json")
                            .read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            prov = ga.generate(_spec(), Path(d), dry_run=True, now="2026-07-18T00:00:00Z")
        for field in schema["required"]:
            self.assertIn(field, prov, f"provenance missing required field {field}")
        # optional jsonschema validation when the lib is present
        try:
            import jsonschema  # type: ignore
        except ImportError:
            return
        jsonschema.validate(instance=prov, schema=schema)

    def test_example_spec_is_valid_and_drives_a_dry_run(self):
        spec = json.loads((REPO_ROOT / "assets" / "specs" / "gasgiant-example.json")
                          .read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            prov = ga.generate(spec, Path(d), dry_run=True, now="2026-07-18T00:00:00Z")
            self.assertEqual(prov["id"], "gasgiant-jovian-01")
            self.assertTrue(prov["consumer_ref"])


if __name__ == "__main__":
    unittest.main()
