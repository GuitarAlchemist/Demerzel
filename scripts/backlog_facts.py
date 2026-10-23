#!/usr/bin/env python3
"""Generate mechanically checkable repository facts used by BACKLOG.md.

The backlog explains architectural judgment, but counts that Git can answer are
derived here instead of being maintained by hand. Running this script updates the
single marked block in BACKLOG.md deterministically. CI may later run the same
command and fail on ``git diff``; the generator itself owns no CI policy.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import re
import sys

import demerzel_kit as kit


ROOT = kit.ROOT
BACKLOG = ROOT / "BACKLOG.md"
BEGIN_MARKER = "<!-- BEGIN GENERATED BACKLOG FACTS -->"
END_MARKER = "<!-- END GENERATED BACKLOG FACTS -->"
WORKFLOW_TARGETS = ("agent-blackbox.yml",)
_ROOT_EXPRESSIONS = {
    "Path(__file__).resolve().parents[1]",
    "Path(__file__).resolve().parent.parent",
}


@dataclass(frozen=True)
class BacklogFacts:
    test_module_count: int
    root_recompute_count: int
    planner_non_test_references: dict[str, int]
    workflow_step_counts: dict[str, int]


def _python_files(root: Path) -> list[Path]:
    return sorted((root / "scripts").glob("*.py"))


def _is_root_definition(path: Path, node: ast.AST,
                        parents: dict[ast.AST, ast.AST]) -> bool:
    """The shared kit's ``ROOT = ...`` is the definition, not a duplicate."""
    parent = parents.get(node)
    if path.name != "demerzel_kit.py" or not isinstance(parent, ast.Assign):
        return False
    return any(isinstance(target, ast.Name) and target.id == "ROOT"
               for target in parent.targets)


def count_root_recomputations(root: Path) -> int:
    count = 0
    for path in _python_files(root):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        parents = {child: parent for parent in ast.walk(tree)
                   for child in ast.iter_child_nodes(parent)}
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Attribute, ast.Subscript)):
                continue
            if ast.unparse(node) not in _ROOT_EXPRESSIONS:
                continue
            if not _is_root_definition(path, node, parents):
                count += 1
    return count


def _reference_line_count(path: Path, identifier: str) -> int:
    """Match the repo's established `rg -n` meaning of a reference count."""
    pattern = re.compile(rf"\b{re.escape(identifier)}\b")
    return sum(pattern.search(line) is not None
               for line in path.read_text(encoding="utf-8").splitlines())


def planner_reference_counts(root: Path) -> dict[str, int]:
    scripts = root / "scripts"
    planners = sorted(path for path in scripts.glob("planner_*.py")
                      if not path.name.startswith("test_"))
    non_tests = [path for path in _python_files(root)
                 if not path.name.startswith("test_")]
    return {
        planner.stem: sum(_reference_line_count(path, planner.stem)
                          for path in non_tests if path != planner)
        for planner in planners
    }


def count_workflow_steps(path: Path) -> int:
    """Count direct list entries under every YAML ``steps:`` key, stdlib-only."""
    count = 0
    steps_indent: int | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(stripped)
        if steps_indent is not None:
            if indent <= steps_indent:
                steps_indent = None
            elif indent == steps_indent + 2 and re.match(r"-\s+\w", stripped):
                count += 1
        if stripped == "steps:":
            steps_indent = indent
    return count


def collect_facts(root: Path = ROOT) -> BacklogFacts:
    scripts = root / "scripts"
    workflow_dir = root / ".github" / "workflows"
    return BacklogFacts(
        test_module_count=len(list(scripts.glob("test_*.py"))),
        root_recompute_count=count_root_recomputations(root),
        planner_non_test_references=planner_reference_counts(root),
        workflow_step_counts={
            name: count_workflow_steps(workflow_dir / name)
            for name in WORKFLOW_TARGETS
        },
    )


def _fact_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def render_block(facts: BacklogFacts) -> str:
    rows = [
        ("python_test_modules", facts.test_module_count,
         "`scripts/test_*.py` modules"),
        ("python_root_recomputations", facts.root_recompute_count,
         "Executable repo-root recomputations outside `demerzel_kit.ROOT`"),
    ]
    rows.extend(
        (f"{name}_non_test_refs", count,
         f"Matching lines for `{name}` outside tests and its definition")
        for name, count in sorted(facts.planner_non_test_references.items())
    )
    rows.extend(
        (f"workflow_{_fact_id(Path(name).stem)}_steps", count,
         f"Steps in `.github/workflows/{name}`")
        for name, count in sorted(facts.workflow_step_counts.items())
    )
    lines = [
        "_Generated by `python scripts/backlog_facts.py`; do not edit these values._",
        "",
        "| Fact ID | Value | Ground truth |",
        "|---|---:|---|",
    ]
    lines.extend(f"| `{name}` | {value} | {meaning} |"
                 for name, value, meaning in rows)
    return "\n".join(lines) + "\n"


def replace_generated_block(text: str, replacement: str) -> str:
    if text.count(BEGIN_MARKER) != 1 or text.count(END_MARKER) != 1:
        raise ValueError("BACKLOG.md must contain exactly one generated block")
    before, remainder = text.split(BEGIN_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return (before + BEGIN_MARKER + "\n" + replacement.rstrip("\n") + "\n"
            + END_MARKER + after)


def main() -> int:
    try:
        original = BACKLOG.read_text(encoding="utf-8")
        updated = replace_generated_block(original, render_block(collect_facts()))
        BACKLOG.write_text(updated, encoding="utf-8")
    except (OSError, SyntaxError, ValueError) as error:
        print(f"backlog_facts: {error}", file=sys.stderr)
        return 1
    print(f"Updated {BACKLOG.relative_to(ROOT)} from repository state.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
