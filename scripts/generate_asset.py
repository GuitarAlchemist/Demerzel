#!/usr/bin/env python3
"""Deterministic driver for the governed local generative-asset pipeline (epic #724).

Takes an asset spec (JSON), drives a ComfyUI workflow through ComfyUI's HTTP API,
and writes the image plus an auditable provenance manifest that validates against
schemas/asset-provenance.schema.json.

Design notes:
- stdlib only (urllib) — no third-party runtime dependency;
- the network layer is a small ComfyClient injected into generate(), so the logic
  is fully testable offline; `--dry-run` bypasses the network entirely and emits a
  stub image + provenance so CI can prove the pipeline without a GPU;
- fails closed: any unreachable/timeout/malformed response in a real run raises,
  so a caller can never mistake a dead ComfyUI for a produced asset.

This driver is the AIW provider `comfyui-local` (see state/driver/aiw-budget-policy.json);
real asset jobs should be reserved through scripts/aiw_budget_gate.py first.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = REPO_ROOT / "assets" / "generated"
DEFAULT_COMFY_URL = "http://127.0.0.1:8188"

# Minimal valid 1x1 PNG used as the --dry-run stub (no GPU needed).
_STUB_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c6300010000050001"
    "0d0a2db40000000049454e44ae426082"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _require(spec: dict[str, Any], name: str) -> Any:
    if name not in spec or spec[name] in (None, ""):
        raise ValueError(f"spec is missing required field: {name}")
    return spec[name]


def _render_workflow(workflow_text: str, prompt: str, negative: str, seed: int) -> dict[str, Any]:
    """Substitute placeholders in the workflow text, then parse as JSON.

    Placeholders (string-based, no regex): {{PROMPT}}, {{NEGATIVE_PROMPT}}, {{SEED}}.
    JSON-encoding the substituted values keeps the workflow valid and injection-safe.
    """
    rendered = (
        workflow_text
        .replace('"{{PROMPT}}"', json.dumps(prompt))
        .replace('"{{NEGATIVE_PROMPT}}"', json.dumps(negative))
        .replace('"{{SEED}}"', json.dumps(seed))
    )
    parsed = json.loads(rendered)
    if not isinstance(parsed, dict):
        raise ValueError("workflow must be a ComfyUI API object (node-id -> node)")
    return parsed


class ComfyClient:
    """Thin ComfyUI HTTP API client. Injectable so tests never touch the network."""

    def __init__(self, base_url: str, timeout_s: float = 300.0, poll_s: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.poll_s = poll_s

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}{path}", data=data,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get_json(self, path: str) -> dict[str, Any]:
        with urllib.request.urlopen(f"{self.base_url}{path}", timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def queue_prompt(self, workflow: dict[str, Any]) -> str:
        result = self._post("/prompt", {"prompt": workflow})
        prompt_id = result.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id:
            raise ValueError("ComfyUI did not return a prompt_id")
        return prompt_id

    def wait_for_image(self, prompt_id: str) -> tuple[str, str, str]:
        """Poll /history until the prompt produces an image; return (filename, subfolder, type)."""
        deadline = time.monotonic() + self.timeout_s
        while time.monotonic() < deadline:
            history = self._get_json(f"/history/{prompt_id}")
            entry = history.get(prompt_id)
            if isinstance(entry, dict):
                for node_out in (entry.get("outputs") or {}).values():
                    images = node_out.get("images") if isinstance(node_out, dict) else None
                    if images:
                        img = images[0]
                        return img["filename"], img.get("subfolder", ""), img.get("type", "output")
            time.sleep(self.poll_s)
        raise TimeoutError(f"ComfyUI did not produce an image for {prompt_id} within {self.timeout_s}s")

    def fetch_image(self, filename: str, subfolder: str, type_: str) -> bytes:
        query = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": type_})
        with urllib.request.urlopen(f"{self.base_url}/view?{query}", timeout=60) as resp:
            return resp.read()


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_provenance(spec: dict[str, Any], workflow_sha256: str,
                     seed: int, prompt: str, negative: str, dry_run: bool,
                     now: str | None = None) -> dict[str, Any]:
    prov: dict[str, Any] = {
        "schema_version": "1.0",
        "id": spec["id"],
        "provider": "comfyui-local",
        "workflow": str(spec["workflow"]).replace("\\", "/"),
        "workflow_sha256": workflow_sha256,
        "seed": seed,
        "prompt": prompt,
        "created_at": now or _now_iso(),
        "consumer_ref": _require(spec, "consumer_ref"),
        "dry_run": dry_run,
    }
    if spec.get("model"):
        prov["model"] = spec["model"]
    if spec.get("sampler"):
        prov["sampler"] = spec["sampler"]
    if negative:
        prov["negative_prompt"] = negative
    return prov


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def generate(spec: dict[str, Any], out_dir: Path, dry_run: bool,
             client: ComfyClient | None = None, now: str | None = None) -> dict[str, Any]:
    """Produce one asset from a spec; return the provenance dict. Deterministic given the spec."""
    asset_id = _require(spec, "id")
    prompt = _require(spec, "prompt")
    _require(spec, "consumer_ref")
    negative = spec.get("negative_prompt", "")
    seed = spec.get("seed", 0)
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    if spec.get("provider", "comfyui-local") != "comfyui-local":
        raise ValueError("spec.provider must be comfyui-local")

    workflow_path = (REPO_ROOT / _require(spec, "workflow")).resolve()
    if not _is_relative_to(workflow_path, REPO_ROOT):
        raise ValueError("spec.workflow must be a repo-relative path")
    workflow_bytes = workflow_path.read_bytes()
    workflow_sha256 = hashlib.sha256(workflow_bytes).hexdigest()
    workflow = _render_workflow(workflow_bytes.decode("utf-8"), prompt, negative, seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    image_path = out_dir / f"{asset_id}.png"
    prov_path = out_dir / f"{asset_id}.provenance.json"

    if dry_run:
        image_bytes = _STUB_PNG
    else:
        active = client or ComfyClient(DEFAULT_COMFY_URL)
        try:
            prompt_id = active.queue_prompt(workflow)
            filename, subfolder, type_ = active.wait_for_image(prompt_id)
            image_bytes = active.fetch_image(filename, subfolder, type_)
        except (urllib.error.URLError, OSError, TimeoutError, ValueError, KeyError) as error:
            raise RuntimeError(f"ComfyUI generation failed (fail-closed): {error}") from error
        if not image_bytes:
            raise RuntimeError("ComfyUI returned an empty image (fail-closed)")

    image_path.write_bytes(image_bytes)
    prov = build_provenance(spec, workflow_sha256, seed, prompt, negative, dry_run, now)
    prov_path.write_text(json.dumps(prov, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return prov


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True, help="asset spec JSON")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--comfy-url", default=DEFAULT_COMFY_URL)
    parser.add_argument("--dry-run", action="store_true",
                        help="emit a stub image + provenance without contacting ComfyUI (CI/offline)")
    args = parser.parse_args(argv)
    try:
        spec = _load_json(args.spec)
        client = None if args.dry_run else ComfyClient(args.comfy_url)
        prov = generate(spec, args.out_dir, args.dry_run, client=client)
    except (OSError, ValueError, KeyError, RuntimeError, TimeoutError, json.JSONDecodeError) as error:
        print(f"generate_asset: {error}", file=sys.stderr)
        return 2
    kind = "DRY-RUN" if args.dry_run else "GENERATED"
    print(f"{kind}: {args.out_dir / (prov['id'] + '.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
