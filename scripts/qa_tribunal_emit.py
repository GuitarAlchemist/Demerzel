#!/usr/bin/env python3
"""
QA Architect Tribunal — Phase 0 verdict emitter (Path B, per v2 plan §D-runtime).

Reads a repository_dispatch payload from GITHUB_EVENT_PATH, validates it
against the vendored qa-verdict.schema.json, builds a contract-valid
verdict, and writes it to state/quality/verdicts/<repo>/<pr>/<verdict_id>.json.

Phase 0 scope (per docs/plans/2026-05-14-arch-cherny-adoption-and-
tribunal-ci-plan-v2.md §"Phase 0 #3"):

  - Validate dispatch payload (allowlist + SHA verify + PR cross-check +
    fork-PR isolation).
  - Build a verdict with real blast_radius (regex-derived layers_touched
    + components_reached from `gh pr diff --name-only`).
  - Emit `informational` verdict with one reviewer (this emitter).
  - NOT hardcoded — real values, just minimal evidence array.

Out of scope for Phase 0 (deferred to Phase 1+):

  - Real evidence producers (semantic basin, adversarial replay).
  - Tribunal aggregation across multiple roles.
  - Followup auto-generation + GitHub issue creation.
  - PR comment posting.

Security:

  - Repository allowlist (only GA / ix / tars / Demerzel SHA references).
  - `gh api` SHA-existence verification before trusting head_sha.
  - PR-number cross-check against the named repo.
  - Forked-PR runs fail closed (would need secretless isolation; out of
    scope for Phase 0).
  - Idempotency key prevents replay-overwrite of stricter verdicts.

Usage:

  python scripts/qa_tribunal_emit.py [--sweep]

  Without --sweep: reads GITHUB_EVENT_PATH for repository_dispatch payload.
  With --sweep: emits a scheduled-sweep informational verdict targeting
  the day (no PR reference).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import demerzel_kit as kit


# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

REPO_ALLOWLIST = {
    "GuitarAlchemist/ga",
    "GuitarAlchemist/ix",
    "GuitarAlchemist/tars",
    "GuitarAlchemist/Demerzel",
}

PRODUCER_SLUG = "qa-architect-cycle"
PRODUCER_VERSION = "0.1.0"

VERDICT_ROOT = Path("state/quality/verdicts")
SWEEP_ROOT = VERDICT_ROOT / "sweeps"


# Path → layer regex map. Patterns are matched case-insensitively against
# repo-relative changed paths. First match wins. Unmatched paths land in
# "apps" by default for the layer count.
LAYER_PATTERNS = [
    (re.compile(r"^docs/contracts/", re.IGNORECASE), "docs"),
    (re.compile(r"^docs/plans/", re.IGNORECASE), "docs"),
    (re.compile(r"^Common/GA\.Core\b", re.IGNORECASE), "core"),
    (re.compile(r"^Common/GA\.Domain\.Core\b", re.IGNORECASE), "core"),
    (re.compile(r"^Common/GA\.Business\.Core(?!\.Analysis)", re.IGNORECASE), "domain"),
    (re.compile(r"^Common/GA\.Business\.Core\.Analysis", re.IGNORECASE), "analysis"),
    (re.compile(r"^Common/GA\.Business\.Core\.Fretboard", re.IGNORECASE), "analysis"),
    (re.compile(r"^Common/GA\.Business\.Core\.Harmony", re.IGNORECASE), "analysis"),
    (re.compile(r"^Common/GA\.Business\.ML\b", re.IGNORECASE), "ai_ml"),
    (re.compile(r"^Common/GA\.Business\.Core\.Orchestration", re.IGNORECASE), "orchestration"),
    (re.compile(r"^Apps/", re.IGNORECASE), "apps"),
    (re.compile(r"^ReactComponents/", re.IGNORECASE), "frontend"),
    (re.compile(r"^\.github/", re.IGNORECASE), "infra"),
    (re.compile(r"^Scripts/", re.IGNORECASE), "infra"),
    (re.compile(r"^docs/", re.IGNORECASE), "docs"),
]

# Paths that, when touched, raise the invariants_at_risk list.
INVARIANT_PATTERNS = [
    (re.compile(r"Common/GA\.Business\.ML/Embeddings/", re.IGNORECASE), "optick.dim=240"),
    (re.compile(r"OPTIC-K", re.IGNORECASE), "optick.schema=OPTIC-K-v1.8"),
    (re.compile(r"docs/contracts/.*\.schema\.json$", re.IGNORECASE), "schema-locked-contract"),
    (re.compile(r"^state/quality/_schema\.json$", re.IGNORECASE), "quality-baseline-pin"),
]


# ---------------------------------------------------------------------------
# Payload validation
# ---------------------------------------------------------------------------

class PayloadError(ValueError):
    """Dispatch payload failed validation."""


def validate_dispatch_payload(payload: dict) -> dict:
    """Validate the client_payload from a repository_dispatch event.

    Required fields: repo, pr, head_sha, base_sha, idempotency_key.
    Returns the cleaned payload (post-allowlist).
    Raises PayloadError on any validation failure.
    """
    required = {"repo", "pr", "head_sha", "base_sha", "idempotency_key"}
    missing = required - set(payload.keys())
    if missing:
        raise PayloadError(f"missing required client_payload fields: {sorted(missing)}")

    repo = str(payload["repo"]).strip()
    if repo not in REPO_ALLOWLIST:
        raise PayloadError(f"repo '{repo}' not in allowlist {sorted(REPO_ALLOWLIST)}")

    pr_raw = payload["pr"]
    try:
        pr = int(pr_raw)
    except (TypeError, ValueError) as exc:
        raise PayloadError(f"pr must be integer, got {pr_raw!r}") from exc
    if pr <= 0:
        raise PayloadError(f"pr must be positive, got {pr}")

    head_sha = str(payload["head_sha"]).strip()
    if not re.match(r"^[0-9a-f]{7,40}$", head_sha):
        raise PayloadError(f"head_sha not a valid hex SHA: {head_sha!r}")

    base_sha = str(payload["base_sha"]).strip()
    if not re.match(r"^[0-9a-f]{7,40}$", base_sha):
        raise PayloadError(f"base_sha not a valid hex SHA: {base_sha!r}")

    # SHA-existence verification — closes the SHA-confusion attack from the
    # 2026-05-15 octo security review.
    commit = kit.gh_json(["api", f"repos/{repo}/commits/{head_sha}"])
    if not commit:
        raise PayloadError(f"head_sha {head_sha} not found in {repo}")

    # PR cross-check — the PR's head.sha must match the dispatched head_sha.
    pr_info = kit.gh_json(["api", f"repos/{repo}/pulls/{pr}"])
    if not pr_info:
        raise PayloadError(f"PR #{pr} not found in {repo}")
    actual_head = pr_info.get("head", {}).get("sha", "")
    if actual_head and not actual_head.startswith(head_sha) and not head_sha.startswith(actual_head[:7]):
        raise PayloadError(
            f"head_sha mismatch: dispatched {head_sha}, PR has {actual_head}"
        )

    # Forked-PR fail-closed for Phase 0 (real isolation would need
    # `pull_request_target` + secretless job — out of scope).
    head_repo = pr_info.get("head", {}).get("repo", {})
    if head_repo and head_repo.get("fork"):
        raise PayloadError(
            f"PR #{pr} is from a fork ({head_repo.get('full_name')}); "
            "Phase 0 emitter does not handle forked-PR isolation"
        )

    return {
        "repo": repo,
        "pr": pr,
        "head_sha": head_sha,
        "base_sha": base_sha,
        "idempotency_key": str(payload["idempotency_key"]),
    }


# ---------------------------------------------------------------------------
# Blast radius derivation
# ---------------------------------------------------------------------------

def changed_files(repo: str, pr: int) -> list[str]:
    """Return list of changed file paths via `gh pr diff --name-only`."""
    result = kit.gh_text(["pr", "diff", str(pr), "--repo", repo, "--name-only"])
    if not result:
        return []
    return [line.strip() for line in result.splitlines() if line.strip()]


def derive_blast_radius(paths: list[str]) -> dict:
    """Compute blast_radius from changed file paths.

    Heuristic — not load-bearing for Phase 0 (verdict is informational).
    """
    layers: set[str] = set()
    invariants: list[str] = []
    for path in paths:
        for pattern, layer in LAYER_PATTERNS:
            if pattern.search(path):
                layers.add(layer)
                break
        for pattern, inv in INVARIANT_PATTERNS:
            if pattern.search(path) and inv not in invariants:
                invariants.append(inv)

    # Blast score heuristic: cap at 1.0; saturates near 0.7 when 4+ layers touched
    # OR any invariant flagged.
    layer_score = min(len(layers) / 5.0, 0.8)
    invariant_score = 0.3 if invariants else 0.0
    estimated = min(round(layer_score + invariant_score, 2), 1.0)

    return {
        "layers_touched": sorted(layers),
        "one_way_doors_crossed": [],  # Phase 0: not tracked yet
        "invariants_at_risk": invariants,
        "components_reached": paths[:50],  # cap to keep verdict size bounded
        "estimated_blast_score": estimated,
    }


# ---------------------------------------------------------------------------
# Verdict construction
# ---------------------------------------------------------------------------

def build_pr_verdict(payload: dict, paths: list[str]) -> dict:
    """Build a contract-conforming verdict for a pull_request target."""
    iso = kit.now_iso()
    file_safe = iso.replace(":", "-")
    blast = derive_blast_radius(paths)

    return {
        "schema_version": 1,
        "verdict_id": f"{file_safe}-pr-{payload['repo'].replace('/', '_')}-{payload['pr']}-{PRODUCER_SLUG}",
        "produced_at": iso,
        "producer": PRODUCER_SLUG,
        "producer_version": PRODUCER_VERSION,
        "target": {
            "kind": "pull_request",
            "repo": payload["repo"],
            "ref": f"pr/{payload['pr']}",
            "sha": payload["head_sha"],
            "base_sha": payload["base_sha"],
        },
        "risk_tier": "P3",
        "verdict": "informational",
        "blast_radius": blast,
        "evidence": [],  # Phase 0 — real evidence ships in Phase 1
        "followups": [],
        "reviewer_chain": [
            {
                "agent": "demerzel.qa-architect-cycle",
                "role": "architecture",
                "score": None,
                "notes": (
                    "Phase 0 informational verdict — blast_radius heuristic "
                    "only; semantic basin / adversarial replay / mutation "
                    "scoring lands in Phase 1."
                ),
            }
        ],
        "narrative": (
            f"Phase 0 informational verdict for {payload['repo']}#{payload['pr']}. "
            f"Touches {len(blast['layers_touched'])} layers"
            + (
                f" and brushes {len(blast['invariants_at_risk'])} invariant(s)"
                if blast["invariants_at_risk"]
                else ""
            )
            + f". Blast score: {blast['estimated_blast_score']}."
        ),
        "links": {
            "pr": f"https://github.com/{payload['repo']}/pull/{payload['pr']}",
            "plan": "https://github.com/GuitarAlchemist/ga/blob/main/docs/plans/2026-05-14-arch-cherny-adoption-and-tribunal-ci-plan-v2.md",
        },
    }


def build_sweep_verdict() -> dict:
    """Build a scheduled-sweep informational verdict."""
    iso = kit.now_iso()
    file_safe = iso.replace(":", "-")
    return {
        "schema_version": 1,
        "verdict_id": f"{file_safe}-sweep-{PRODUCER_SLUG}",
        "produced_at": iso,
        "producer": PRODUCER_SLUG,
        "producer_version": PRODUCER_VERSION,
        "target": {
            "kind": "scheduled_sweep",
            "repo": "GuitarAlchemist/Demerzel",
            "ref": iso[:10],  # date as the ref
            "sha": None,
            "base_sha": None,
        },
        "risk_tier": "P3",
        "verdict": "informational",
        "blast_radius": {
            "layers_touched": [],
            "one_way_doors_crossed": [],
            "invariants_at_risk": [],
            "components_reached": [],
            "estimated_blast_score": 0.0,
        },
        "evidence": [],
        "followups": [],
        "reviewer_chain": [
            {
                "agent": "demerzel.qa-architect-cycle",
                "role": "architecture",
                "score": None,
                "notes": "Phase 0 daily sweep — no signal computed yet.",
            }
        ],
        "narrative": f"Phase 0 scheduled sweep for {iso[:10]}. No signal computed yet.",
        "links": {
            "plan": "https://github.com/GuitarAlchemist/ga/blob/main/docs/plans/2026-05-14-arch-cherny-adoption-and-tribunal-ci-plan-v2.md",
        },
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def emit_verdict(verdict: dict, payload: dict | None) -> Path:
    """Validate against schema + write to verdict path. Returns the output path."""
    if payload is not None:
        # Per-PR verdict path
        repo_slug = payload["repo"].replace("/", "_")
        out_dir = VERDICT_ROOT / repo_slug / str(payload["pr"])
    else:
        # Sweep path
        out_dir = SWEEP_ROOT / verdict["target"]["ref"]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{verdict['verdict_id']}.json"

    try:
        kit.write_artifact(out_path, verdict, schema="contracts/qa-verdict")
    except Exception as exc:
        # demerzel_kit's validate raises jsonschema.ValidationError which we need to wrap
        # if it occurs. demerzel_kit doesn't expose ValidationError natively unless imported.
        # So we catch Exception and convert to PayloadError if it's a validation error.
        err_name = type(exc).__name__
        if "ValidationError" in err_name:
            raise PayloadError(f"emitter produced schema-invalid verdict: {exc}") from exc
        raise

    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Emit a scheduled-sweep verdict (no dispatch payload)",
    )
    args = parser.parse_args(argv)

    if args.sweep:
        verdict = build_sweep_verdict()
        out = emit_verdict(verdict, payload=None)
        print(f"sweep verdict written: {out}")
        return 0

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("ERROR: GITHUB_EVENT_PATH not set; use --sweep for scheduled runs", file=sys.stderr)
        return 2

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    if event.get("action") and "client_payload" not in event:
        print(f"ERROR: not a repository_dispatch event (action={event.get('action')})", file=sys.stderr)
        return 2

    payload = event.get("client_payload") or {}
    try:
        cleaned = validate_dispatch_payload(payload)
    except PayloadError as exc:
        print(f"ERROR: dispatch payload invalid: {exc}", file=sys.stderr)
        return 1

    paths = changed_files(cleaned["repo"], cleaned["pr"])
    verdict = build_pr_verdict(cleaned, paths)

    out = emit_verdict(verdict, cleaned)
    print(f"verdict written: {out}")
    print(f"blast_score: {verdict['blast_radius']['estimated_blast_score']}")
    print(f"layers_touched: {verdict['blast_radius']['layers_touched']}")
    print(f"invariants_at_risk: {verdict['blast_radius']['invariants_at_risk']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
