#!/usr/bin/env python3
"""Select a credentialed cross-model reviewer without allowing self-review.

This module is the executable authority for reviewer selection in
.github/workflows/cross-model-review.yml. Provider credentials are read from the
environment; secret values are never accepted as command-line arguments.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping, Sequence

CREDENTIAL_ENV = {
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_AI_KEY",
    "codex": "OPENAI_API_KEY",
}

CANDIDATES = {
    "claude": ("gemini", "codex"),
    "gemini": ("claude", "codex"),
    "codex": ("claude", "gemini"),
    "human": ("claude", "gemini", "codex"),
}


class NoReviewerAvailable(RuntimeError):
    """No non-self reviewer has its own credential configured."""


def candidate_order(author: str) -> tuple[str, ...]:
    """Return deterministic candidates; unknown authors follow the human path."""
    return CANDIDATES.get(author.strip().lower(), CANDIDATES["human"])


def has_credential(provider: str, environment: Mapping[str, str]) -> bool:
    """Return whether the provider's own credential is present and non-empty."""
    variable = CREDENTIAL_ENV.get(provider)
    return bool(variable and environment.get(variable, "").strip())


def select_reviewer(author: str, environment: Mapping[str, str]) -> str:
    """Select the first credentialed non-self reviewer or fail explicitly."""
    candidates = candidate_order(author)
    for provider in candidates:
        if has_credential(provider, environment):
            return provider
    tried = ", ".join(candidates)
    raise NoReviewerAvailable(
        f"No credentialed reviewer is available for author {author!r} "
        f"(tried: {tried})."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--author",
        default=os.environ.get("AUTHOR", "human"),
        help="Detected author model. Unknown values use the human candidate order.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reviewer = select_reviewer(args.author, os.environ)
    except NoReviewerAvailable as error:
        print(str(error), file=sys.stderr)
        return 1
    print(reviewer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
