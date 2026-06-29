#!/usr/bin/env python3
"""
Governance manifest generator — harvest, don't declare.

Walks the artifact tree and EMITS governance-manifest.json: a derived,
deterministic view of the governance graph. Nothing here is authored or
recomputed — every fact is harvested from where it already lives:

  - inventory : the artifact files on disk
  - edges     : the artifacts' own reference fields (references:, estimator_pairing,
                persona<->test coverage), harvested and resolved
  - counts    : derived from inventory (never stored by hand)
  - health    : pulled from emitter outputs with provenance (Phase 4)

Validation runs INSIDE generation (ADR-0003): dangling edges, orphaned tests,
README count drift, and persona schema violations are all detected as the
manifest is built. The script:

  1. always writes governance-manifest.json (so the committed-file + CI diff
     gate in ADR-0001 reflects reality), then
  2. exits non-zero if any violation was found.

Output is sorted and free of wall-clock timestamps so that, given unchanged
inputs, the manifest is byte-stable and `git diff --exit-code` is meaningful.

See docs/adr/0001-derived-governance-manifest.md, 0002, 0003.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "governance-manifest.json"
HEALTH = REPO / "governance-health.json"
CONFIDENCE = REPO / "logic" / "confidence-thresholds.yaml"
SCHEMA_VERSION = 1

_CONFIDENCE_REF = re.compile(r"ref:confidence#([\w-]+)")

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252.
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Artifact classes — (type, glob, how to read metadata)
# ---------------------------------------------------------------------------

def _first_yaml_doc(path: Path) -> dict[str, Any]:
    """Policy/persona files are YAML front-matter possibly followed by a `---`
    markdown body. Return the first mapping document, or {} if unparseable."""
    try:
        for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
            if isinstance(doc, dict):
                return doc
            break
    except yaml.YAMLError:
        return {}
    return {}


def _name_version(path: Path) -> dict[str, Any]:
    doc = _first_yaml_doc(path)
    return {"name": doc.get("name"), "version": doc.get("version")}


# Each entry: type -> (glob pattern relative to REPO, metadata reader)
ARTIFACT_CLASSES: dict[str, tuple[str, Any]] = {
    "constitution": ("constitutions/*.md", None),
    "persona": ("personas/*.persona.yaml", _name_version),
    "policy": ("policies/*.yaml", _name_version),
    "schema": (("schemas/*.json", "schemas/seldon/*.json"), None),
    "contract_schema": ("schemas/contracts/*.json", None),
    "grammar": ("grammars/*.ebnf", None),
    "behavioral_test": ("tests/behavioral/*.md", None),
    "pipeline": ("pipelines/*.ixql", None),
    "workflow": (".github/workflows/*", None),
}


def harvest_inventory() -> dict[str, list[dict[str, Any]]]:
    inv: dict[str, list[dict[str, Any]]] = {}
    for art_type, (patterns, reader) in ARTIFACT_CLASSES.items():
        if isinstance(patterns, str):
            patterns = (patterns,)
        items: list[dict[str, Any]] = []
        for pattern in patterns:
            for path in sorted(REPO.glob(pattern)):
                if art_type == "workflow" and path.suffix not in (".yml", ".yaml"):
                    continue
                rel = path.relative_to(REPO).as_posix()
                entry: dict[str, Any] = {"name": path.stem, "path": rel}
                if reader:
                    entry.update(reader(path))
                items.append(entry)
        inv[art_type] = items
    # Skills are directories, not files.
    skills = sorted(p for p in (REPO / ".claude" / "skills").glob("*/") if p.is_dir())
    inv["skill"] = [{"name": p.name, "path": p.relative_to(REPO).as_posix()} for p in skills]
    return inv


def derive_counts(inv: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    return {k: len(v) for k, v in sorted(inv.items())}


# ---------------------------------------------------------------------------
# Edge harvest — read references out of the artifacts themselves
# ---------------------------------------------------------------------------

# Reference strings today are prose: a target, optionally a "Article N" cite,
# optionally a "— gloss". The canonical syntax (ADR-0003) is the target token
# followed by " — gloss"; until every file is swept, the harvester normalises
# what it can and resolves bare names against a basename index.
_GLOSS_SEPARATORS = ("—", "–", "→", " - ")  # em-dash, en-dash, arrow


def _basename_index() -> dict[str, list[str]]:
    """filename -> [repo-relative paths] across the dirs references point into."""
    index: dict[str, list[str]] = {}
    patterns = [
        "policies/*.yaml", "constitutions/*", "schemas/*.json", "schemas/contracts/*.json",
        "logic/*.json", "personas/*.yaml", "grammars/*.ebnf", "pipelines/*.ixql",
        "tests/behavioral/*.md", "docs/*.md", ".claude/skills/*/SKILL.md",
    ]
    for pat in patterns:
        for p in REPO.glob(pat):
            if p.is_file():
                index.setdefault(p.name, []).append(p.relative_to(REPO).as_posix())
    return index


def normalize_ref(raw: str) -> tuple[str, str | None]:
    """Strip the prose gloss and any 'Article N' cite. Return (target, article)."""
    s = raw.strip()
    for sep in _GLOSS_SEPARATORS:
        idx = s.find(sep)
        if idx != -1:
            s = s[:idx].strip()
    article = None
    m = re.search(r"\s+Articles?\s+(.+)$", s)
    if m:
        article = m.group(1).strip()
        s = s[: m.start()].strip()
    return s, article


def resolve_ref(target: str, basenames: dict[str, list[str]]) -> str | None:
    """Return the canonical repo-relative path a reference resolves to, or None."""
    if not target:
        return None
    candidates = [target]
    if target.startswith("skills/"):  # shorthand for .claude/skills/
        candidates.append(".claude/" + target)
    for cand in candidates:
        p = REPO / cand
        if p.exists():
            return cand.rstrip("/") + ("/" if cand.endswith("/") else "")
    if "/" not in target:  # bare filename -> basename lookup
        hits = basenames.get(target)
        if hits and len(hits) == 1:
            return hits[0]
    return None


def harvest_edges(
    inv: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """Return (edges, hard_violations, soft_warnings)."""
    edges: list[dict[str, Any]] = []
    hard: list[str] = []
    soft: list[str] = []
    basenames = _basename_index()

    persona_names = {p["name"].removesuffix(".persona") for p in inv["persona"]}
    test_stems = {t["name"] for t in inv["behavioral_test"]}

    # policy/persona `references:` — harvest, normalise, resolve. Unresolved refs
    # are SOFT (legacy prose predates the canonical sweep); they are recorded and
    # printed but do not fail the build yet.
    for art_type in ("policy", "persona"):
        for art in inv[art_type]:
            doc = _first_yaml_doc(REPO / art["path"])
            for raw in doc.get("references", []) or []:
                if not isinstance(raw, str):
                    continue
                target, article = normalize_ref(raw)
                resolved = resolve_ref(target, basenames)
                edge: dict[str, Any] = {
                    "from": art["path"], "to": resolved or target,
                    "kind": "reference", "resolved": resolved is not None,
                }
                if article:
                    edge["article"] = article
                edges.append(edge)
                if resolved is None:
                    soft.append(f"unresolved reference: {art['path']} -> {target!r}")

    # persona.estimator_pairing -> must name a real persona. HARD.
    for p in inv["persona"]:
        doc = _first_yaml_doc(REPO / p["path"])
        pairing = doc.get("estimator_pairing")
        if pairing:
            ok = pairing in persona_names
            edges.append({"from": p["path"], "to": f"persona:{pairing}", "kind": "estimator_pairing", "resolved": ok})
            if not ok:
                hard.append(f"dangling estimator_pairing: {p['path']} -> persona:{pairing}")

    # persona -> behavioral test coverage. HARD (ADR-0001 folds in the check
    # formerly in validate_governance.py).
    for p in inv["persona"]:
        base = p["name"].removesuffix(".persona")
        expected = f"{base}-cases"
        ok = expected in test_stems
        edges.append({"from": p["path"], "to": f"tests/behavioral/{expected}.md", "kind": "has_test", "resolved": ok})
        if not ok:
            hard.append(f"persona missing behavioral test: {p['path']} -> tests/behavioral/{expected}.md")

    # behavioral test -> policy it validates (the `validates:` frontmatter, #351).
    # Harvested as an explicit edge so policy<->test coverage is queryable; a test
    # naming a policy that does not exist is HARD.
    policy_names = {p.get("name") for p in inv["policy"] if p.get("name")}
    for t in inv["behavioral_test"]:
        doc = _first_yaml_doc(REPO / t["path"])
        validates = doc.get("validates") if isinstance(doc, dict) else None
        if isinstance(validates, dict) and validates.get("policy"):
            pol = validates["policy"]
            ok = pol in policy_names
            edges.append({"from": t["path"], "to": f"policy:{pol}", "kind": "validates", "resolved": ok})
            if not ok:
                hard.append(f"test validates unknown policy: {t['path']} -> policy:{pol}")

    edges.sort(key=lambda e: (e["from"], e["kind"], e["to"]))
    return edges, hard, soft


# ---------------------------------------------------------------------------
# README count-drift check (counts are populated here in Phase 4; for now,
# detect drift between derived counts and the README-SYNC table)
# ---------------------------------------------------------------------------

# README table label -> manifest count key
README_LABELS: dict[str, str] = {
    "Constitutions": "constitution",
    "Personas": "persona",
    "Policies": "policy",
    "Grammars": "grammar",
    "Schemas": "schema",
    "Behavioral tests": "behavioral_test",
    "Skills": "skill",
    "IxQL pipelines": "pipeline",
    "GitHub workflows": "workflow",
}


def check_readme_counts(counts: dict[str, int]) -> list[str]:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    violations: list[str] = []
    for line in readme.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = cells[0]
        key = README_LABELS.get(label)
        if not key:
            continue
        m = re.search(r"\d+", cells[1])
        if not m:
            continue
        stated = int(m.group())
        actual = counts[key]
        if stated != actual:
            violations.append(f"README count drift: '{label}' says {stated}, actual {actual}")
    return violations


# ---------------------------------------------------------------------------
# Persona schema validation (ADR-0003 — persona.schema.json finally used)
# ---------------------------------------------------------------------------

def _schema_check(inv_items: list[dict[str, Any]], schema_name: str, label: str) -> list[str]:
    import jsonschema

    schema = json.loads((REPO / "schemas" / schema_name).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    violations: list[str] = []
    for art in inv_items:
        doc = _first_yaml_doc(REPO / art["path"])
        for err in sorted(validator.iter_errors(doc), key=str):
            loc = "/".join(str(x) for x in err.path) or "(root)"
            violations.append(f"{label} schema: {art['path']} [{loc}] {err.message}")
    return violations


def check_persona_schema(inv: dict[str, list[dict[str, Any]]]) -> list[str]:
    return _schema_check(inv["persona"], "persona.schema.json", "persona")


def check_policy_schema(inv: dict[str, list[dict[str, Any]]]) -> list[str]:
    return _schema_check(inv["policy"], "policy.schema.json", "policy")


def check_yaml_wellformed(inv: dict[str, list[dict[str, Any]]]) -> list[str]:
    """A persona/policy whose YAML HEADER doesn't parse used to be silently
    swallowed (_first_yaml_doc returns {}). Surface it instead. Only the first
    document is checked — policy files are a YAML header followed by `---` and a
    markdown body that is intentionally not YAML."""
    violations: list[str] = []
    for art_type in ("persona", "policy"):
        for art in inv[art_type]:
            try:
                next(yaml.safe_load_all((REPO / art["path"]).read_text(encoding="utf-8")), None)
            except yaml.YAMLError as exc:
                first = str(exc).splitlines()[0]
                violations.append(f"malformed YAML header: {art['path']} ({first})")
    return violations


# ---------------------------------------------------------------------------
# Health harvest (ADR-0002) — pull the LATEST emitter output with provenance.
# Never recompute the formula; just record value + source + computed_at. Health
# changes on a different cadence than structure, so it is written to a separate
# governance-health.json that is NOT diff-gated (the structural manifest is).
# ---------------------------------------------------------------------------

def harvest_health() -> dict[str, Any]:
    health: dict[str, Any] = {}

    rp = REPO / "state" / "resilience" / "history.json"
    if rp.exists():
        try:
            data = json.loads(rp.read_text(encoding="utf-8"))
            records = data.get("records") if isinstance(data, dict) else data
            if records:
                last = records[-1]
                health["resilience"] = {
                    "value": last.get("overall_score"),
                    "injections_caught": last.get("injections_caught"),
                    "injections_total": last.get("injections_total"),
                    "source": "state/resilience/history.json",
                    "computed_at": last.get("timestamp"),
                }
        except (json.JSONDecodeError, AttributeError, IndexError):
            pass

    qt_dir = REPO / "state" / "quality-trend"
    if qt_dir.exists():
        latest: tuple[Path, str] | None = None
        for f in sorted(qt_dir.glob("*.jsonl")):
            lines = [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if lines:
                latest = (f, lines[-1])
        if latest:
            f, line = latest
            try:
                rec = json.loads(line)
                health["quality_trend"] = {
                    "latest_artifact": rec.get("artifact"),
                    "source": f.relative_to(REPO).as_posix(),
                    "computed_at": rec.get("timestamp"),
                }
            except json.JSONDecodeError:
                pass

    return health


# ---------------------------------------------------------------------------
# Constitutional precedence (ADR-0003 / #353) — assert each constitution's
# header AGREES with the single authored precedence.yaml. Never generate headers.
# ---------------------------------------------------------------------------

def check_precedence(inv: dict[str, list[dict[str, Any]]]) -> tuple[dict[str, Any], list[str]]:
    prec_path = REPO / "constitutions" / "precedence.yaml"
    prec = _first_yaml_doc(prec_path)
    violations: list[str] = []

    declared = {e["file"]: e for e in prec.get("order", []) if isinstance(e, dict)}
    on_disk = {Path(c["path"]).name for c in inv["constitution"]}

    for missing in sorted(on_disk - set(declared)):
        violations.append(f"precedence: constitution {missing} on disk but not declared in precedence.yaml")
    for ghost in sorted(set(declared) - on_disk):
        violations.append(f"precedence: precedence.yaml declares {ghost} but no such constitution on disk")

    for fname, entry in sorted(declared.items()):
        path = REPO / "constitutions" / fname
        if not path.exists():
            continue
        header = "\n".join(path.read_text(encoding="utf-8").splitlines()[:14])
        if entry.get("rank") == "ROOT":
            if "Precedence: ROOT" not in header:
                violations.append(f"precedence: {fname} is ROOT but header lacks 'Precedence: ROOT'")
        sub = entry.get("subordinate_to")
        if sub and f"Subordinate to: `{sub}`" not in header and f"Subordinate to: {sub}" not in header:
            violations.append(f"precedence: {fname} should declare 'Subordinate to: {sub}' in its header")

    return prec, violations


def check_confidence_refs(inv: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[str]]:
    """Resolve every `ref:confidence#<key>` token against the canonical thresholds
    (logic/confidence-thresholds.yaml). Returns (edges, violations); a token that
    names no such rung is a hard violation. ADR-0002 / Candidate 6 — the values
    are single-sourced; policies reference a rung instead of restating the number."""
    edges: list[dict[str, Any]] = []
    violations: list[str] = []
    if not CONFIDENCE.exists():
        return edges, ["confidence: logic/confidence-thresholds.yaml is missing"]
    thresholds = (yaml.safe_load(CONFIDENCE.read_text(encoding="utf-8")) or {}).get("thresholds", {})
    valid = set(thresholds)
    for art in inv.get("policy", []):
        text = (REPO / art["path"]).read_text(encoding="utf-8")
        for key in sorted(set(_CONFIDENCE_REF.findall(text))):
            ok = key in valid
            edges.append({"from": art["path"], "to": f"confidence:{key}", "kind": "confidence_ref", "resolved": ok})
            if not ok:
                violations.append(
                    f"dangling confidence ref: {art['path']} -> ref:confidence#{key} (valid: {sorted(valid)})"
                )
    return edges, violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build() -> tuple[dict[str, Any], list[str], list[str]]:
    inv = harvest_inventory()
    counts = derive_counts(inv)
    edges, hard, soft = harvest_edges(inv)

    hard += check_yaml_wellformed(inv)
    hard += check_persona_schema(inv)
    hard += check_policy_schema(inv)
    hard += check_readme_counts(counts)
    precedence, prec_violations = check_precedence(inv)
    hard += prec_violations

    conf_edges, conf_violations = check_confidence_refs(inv)
    edges += conf_edges
    hard += conf_violations

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "scripts/build_manifest.py",
        "discipline": "harvest, don't declare (docs/adr/0002)",
        "counts": counts,
        "inventory": inv,
        "edges": edges,
        "precedence": precedence.get("order", []),
        "unresolved_references": sorted(set(soft)),
    }
    return manifest, sorted(set(hard)), sorted(set(soft))


def populate_readme(counts: dict[str, int]) -> bool:
    """Update the leading integer of each README-SYNC count cell from derived
    counts, preserving the rest of the cell (ADR-0001: README reads from the
    manifest). Returns True if the file changed."""
    readme_path = REPO / "README.md"
    original = readme_path.read_text(encoding="utf-8")
    out_lines: list[str] = []
    for line in original.splitlines():
        new = line
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] in README_LABELS:
                key = README_LABELS[cells[0]]
                new = re.sub(r"\d+", str(counts[key]), line, count=1)
        out_lines.append(new)
    updated = "\n".join(out_lines) + ("\n" if original.endswith("\n") else "")
    if updated != original:
        readme_path.write_text(updated, encoding="utf-8")
        return True
    return False


def populate_health_row(counts: dict[str, int], health: dict[str, Any]) -> bool:
    """Populate the README 'Governance health' table row from harvested health
    (ADR-0002 consumer). Ungated — health changes on its own cadence, so this is
    a populate convenience, never a gated check. Returns True if changed."""
    res = health.get("resilience") or {}
    caught, total = res.get("injections_caught"), res.get("injections_total")
    if res.get("value") is None or caught is None or total is None:
        return False
    pct = round(res["value"] * 100)
    gaps = total - caught
    new_row = (f"| {pct}% ({gaps} gaps) | L0–L4 + Policy + Schema "
               f"| {counts['policy']} | {counts['persona']} | {counts['behavioral_test']} |")

    readme_path = REPO / "README.md"
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    header = "| Resilience score | LOLLI detection | Policies | Personas | Tests |"
    changed = False
    for i, line in enumerate(lines):
        if line.strip() == header and i + 2 < len(lines) and lines[i + 1].lstrip().startswith("|:"):
            if lines[i + 2] != new_row:
                lines[i + 2] = new_row
                changed = True
            break
    if changed:
        readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    write_readme = "--write-readme" in sys.argv

    manifest, hard, soft = build()
    health = harvest_health()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HEALTH.write_text(json.dumps(health, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST.relative_to(REPO)} "
          f"({sum(manifest['counts'].values())} artifacts, {len(manifest['edges'])} edges) "
          f"and {HEALTH.relative_to(REPO)}")

    if write_readme:
        if populate_readme(manifest["counts"]):
            print("Updated README.md count cells from the manifest.")
            # Re-check after populating so the run reflects the corrected counts.
            hard = [v for v in hard if not v.startswith("README count drift")]
        if populate_health_row(manifest["counts"], health):
            print("Updated README.md governance-health row from governance-health.json.")
    if soft:
        print(f"\n{len(soft)} unresolved reference(s) [soft — to canonicalise]:")
        for w in soft:
            print(f"  warn {w}")
    if hard:
        print(f"\n{len(hard)} violation(s):")
        for v in hard:
            print(f"  FAIL {v}")
        return 1
    print("\nPASSED: manifest green (no dangling edges, no count drift, schemas valid).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
