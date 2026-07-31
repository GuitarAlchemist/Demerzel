#!/usr/bin/env python3
"""Which cross-model reviewers are currently unusable, and until when.

`cross-model-review.yml` selects a reviewer by asking whether that provider's
own credential is present (#846). That is necessary but not sufficient: a
credential can be present, valid, and still unable to complete a review. The
case that motivated this file, measured rather than imagined:

    llm_call: API error: You have reached your specified API usage limits.
    You will regain access on 2026-08-01 at 00:00 UTC.

ANTHROPIC_API_KEY was set and correct throughout. `has_credential` cannot see a
quota wall, so every human-authored PR kept routing to a provider guaranteed to
fail — the same "dead by construction" shape #846 fixed for absent keys, one
layer down.

The alternative to this file is editing the workflow to drop a provider from
rotation. That is a `.github/workflows/**` change, which needs human review, for
a condition that resolves itself on a date the provider already told us. So the
declaration lives in data an operator can commit, and the workflow reads it.

Bounded on purpose, mirroring `.github/loop-health.yml`'s `disabled` block: a
quarantine carries `until` and expires there. `until` is INCLUSIVE — the last
day the provider is considered unusable — matching loop-health's convention so
the two files do not drift into meaning different things by the same word.

Expiry is safe to make silent here, which it is not in loop-health. A forgotten
disable hides a dead loop, so loop-health turns red past `until`. A forgotten
quarantine merely returns the provider to rotation: if it is still broken, the
next review attempt fails loudly at the step that runs it. Expiry cannot
conceal anything, because the thing it un-hides announces itself.

Usage:

    python3 scripts/reviewer_quarantine.py --as-of 2026-07-30

Prints one quarantined provider id per line on stdout (empty output means none),
and any expired entries to stderr so stale declarations stay visible. Exits 0 on
success, 2 if the declaration is missing, unparseable, or invalid — the workflow
treats that as fatal, because a reviewer-selection step that cannot tell which
providers are usable must not guess.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from pathlib import Path
import sys

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
QUARANTINE_PATH = REPO_ROOT / ".github" / "reviewer-quarantine.yml"

# The reviewers cross-model-review.yml can select. A quarantine naming anything
# else is a typo that would otherwise silently quarantine nobody.
KNOWN_PROVIDERS = frozenset({"claude", "gemini", "codex"})

REQUIRED_FIELDS = ("provider", "reason", "since", "until")


class QuarantineInvalid(ValueError):
    """The declaration itself is malformed — distinct from "nothing is quarantined"."""


def _parse_date(value: object, field: str, provider: str) -> date:
    if not isinstance(value, str):
        raise QuarantineInvalid(
            f"{provider}: {field} must be a YYYY-MM-DD string, got {type(value).__name__}")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as error:
        raise QuarantineInvalid(f"{provider}: {field} is not a YYYY-MM-DD date: {value!r}") from error


def load(path: Path | None = None) -> list[dict]:
    """Load and validate the quarantine declaration, fail-closed."""
    target = QUARANTINE_PATH if path is None else path
    if not target.exists():
        # An absent file is a valid empty quarantine: the normal state.
        return []
    try:
        document = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise QuarantineInvalid(f"{target} could not be read: {error}") from error
    if document is None:
        return []
    if not isinstance(document, dict):
        raise QuarantineInvalid(f"{target}: expected a mapping at the top level")

    unknown = set(document) - {"schema_version", "quarantined"}
    if unknown:
        raise QuarantineInvalid(f"{target}: unknown top-level keys: {sorted(unknown)}")

    entries = document.get("quarantined") or []
    if not isinstance(entries, list):
        raise QuarantineInvalid(f"{target}: `quarantined` must be a list")

    seen: set[str] = set()
    loaded: list[dict] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise QuarantineInvalid(f"{target}: quarantined[{index}] must be a mapping")
        provider = entry.get("provider")
        if provider not in KNOWN_PROVIDERS:
            raise QuarantineInvalid(
                f"{target}: quarantined[{index}] names an unknown provider "
                f"{provider!r} (known: {sorted(KNOWN_PROVIDERS)})")
        missing = [name for name in REQUIRED_FIELDS if not entry.get(name)]
        if missing:
            raise QuarantineInvalid(f"{provider}: missing required field(s): {missing}")
        if provider in seen:
            # Two entries for one provider means two `until` dates; which one
            # wins is exactly the ambiguity this file exists to remove.
            raise QuarantineInvalid(f"{provider}: declared more than once")
        seen.add(provider)
        since = _parse_date(entry.get("since"), "since", provider)
        until = _parse_date(entry.get("until"), "until", provider)
        if until < since:
            raise QuarantineInvalid(f"{provider}: until ({until}) precedes since ({since})")
        loaded.append({**entry, "since": since, "until": until})
    return loaded


def active(entries: list[dict], as_of: date) -> tuple[list[dict], list[dict]]:
    """Split entries into (currently quarantined, expired). `until` is inclusive."""
    current = [entry for entry in entries if entry["since"] <= as_of <= entry["until"]]
    expired = [entry for entry in entries if entry["until"] < as_of]
    return current, expired


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--as-of",
        help="Date to evaluate against (YYYY-MM-DD). Defaults to today in UTC, "
             "which is the timezone GitHub Actions runners report.")
    parser.add_argument("--path", type=Path, default=None,
                        help="Override the declaration path (tests).")
    args = parser.parse_args(argv)

    if args.as_of:
        try:
            as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date()
        except ValueError:
            print(f"--as-of is not a YYYY-MM-DD date: {args.as_of!r}", file=sys.stderr)
            return 2
    else:
        as_of = datetime.now(timezone.utc).date()

    try:
        entries = load(args.path)
    except QuarantineInvalid as error:
        print(f"reviewer quarantine is invalid: {error}", file=sys.stderr)
        return 2

    current, expired = active(entries, as_of)
    for entry in expired:
        print(f"note: quarantine for {entry['provider']} expired on {entry['until']} "
              f"and is no longer in effect; remove it from "
              f"{QUARANTINE_PATH.name}", file=sys.stderr)
    for entry in current:
        print(entry["provider"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
