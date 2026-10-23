#!/usr/bin/env python3
"""Run a typed BAML function over the Claude Code CLI instead of a metered HTTP API.

BAML has no "shell out to a CLI" provider — its clients are HTTP. But the two halves
of a BAML call are separable in the generated client, and only the middle one needs a
provider:

    req    = asyncio.run(b.request.Fn(...))   # render the prompt   — local, free
    raw    = run_claude_code(prompt)          # get a completion    — subscription
    result = b.parse.Fn(raw)                  # type + validate     — local, free

So the prompt templating and the schema enforcement that ADR-0005 was adopted for both
still apply; only the transport changes. `b.request` builds the HTTP request WITHOUT
sending it, so no key is read and no socket is opened.

Why this rather than a provider key: `claude-code-cli` is a declared provider in
`state/driver/aiw-budget-policy.json` (tier `local-seat`, cost model
`subscription-or-local`, no manual approval). The client declared in `baml_src` is not
in that policy at all, so an in-band call would bill a provider the budget gate has
never heard of — the same shape as #863, where a gate was correct about a provider that
was not the one being used.

This module deliberately exposes the three steps rather than one clever wrapper: each is
independently testable, and the seam where spend could leak is visible in the caller.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess

# `claude -p` is Claude Code's headless/print mode. Verified against 2.1.220.
CLAUDE_BIN = "claude"
DEFAULT_TIMEOUT_S = 300

# Claude Code prefers an API key over the claude.ai subscription login when both are
# available, and says so: "claude.ai connectors are disabled because ANTHROPIC_API_KEY
# or another auth source is set and takes precedence over your claude.ai login".
#
# That preference is the whole bug this transport exists to avoid. With the key present,
# a call bills metered API spend through a provider the AIW budget policy does not gate;
# with it absent, the same call runs on the subscription — `claude-code-cli`, a declared
# `local-seat` / `subscription-or-local` provider. Verified 2026-07-30: identical prompt,
# key set -> `API Error: 400 ... usage limits`, key unset -> a normal completion.
#
# So strip it from the CHILD environment rather than trusting the parent's. A transport
# whose billing depends on an ambient variable is not a guarantee, it is a coincidence.
# The key is not the only ambient route to a metered backend, which is why this is a list
# and not one name. An adversarial cross-model review of the first version pointed out that
# suppressing only the key leaves every other billing switch in place:
#
#   ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN  — direct metered API credentials
#   CLAUDE_CODE_USE_BEDROCK                   — routes to AWS Bedrock, billed to the AWS account
#   CLAUDE_CODE_USE_VERTEX                    — routes to GCP Vertex, billed to the GCP project
#   ANTHROPIC_BASE_URL                        — redirects to a gateway/proxy that may meter
#
# Deliberately NOT stripping AWS_*/GOOGLE_* credentials: without the routing switch above
# they select no backend, and removing them could break unrelated tooling in the same
# process tree. Suppress the switch, not the whole cloud.
_SUPPRESSED_AUTH_VARS = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "ANTHROPIC_BASE_URL",
)


class ClaudeCodeError(RuntimeError):
    """The CLI could not be run, or exited non-zero."""


def render_prompt(request) -> str:
    """Flatten an awaited BAML HTTP request into the prompt text the CLI should receive.

    `request.body` is provider-shaped (OpenAI chat-completions, for the currently
    declared client), so `content` may be a plain string or a list of typed parts.
    Both are handled; anything else raises rather than silently sending a stringified
    dict to the model.
    """
    body = request.body
    if hasattr(body, "json"):
        body = body.json()
    if isinstance(body, (bytes, bytearray)):
        body = json.loads(body.decode("utf-8"))
    if isinstance(body, str):
        body = json.loads(body)
    if not isinstance(body, dict):
        raise ClaudeCodeError(f"unexpected BAML request body type: {type(body).__name__}")

    messages = body.get("messages")
    if not messages:
        raise ClaudeCodeError(
            "BAML request body has no `messages` — the declared client is probably not "
            "an OpenAI-shaped provider; render_prompt needs updating for it."
        )

    chunks: list[str] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            # Multimodal part list: keep the text parts, in order. A non-text part
            # (image, audio) cannot survive this transport, so say so instead of
            # dropping it and sending a subtly different prompt than BAML rendered.
            kinds = {part.get("type") for part in content if isinstance(part, dict)}
            unsupported = kinds - {"text"}
            if unsupported:
                raise ClaudeCodeError(
                    f"prompt contains non-text parts {sorted(unsupported)}; the CLI "
                    "transport carries text only"
                )
            text = "\n".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        else:
            raise ClaudeCodeError(
                f"unexpected message content type: {type(content).__name__}"
            )
        chunks.append(text)

    prompt = "\n\n".join(chunk for chunk in chunks if chunk.strip())
    if not prompt.strip():
        raise ClaudeCodeError("rendered prompt is empty")
    return prompt


def subscription_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """The child environment for a CLI call: the caller's, minus any API-key auth.

    Separate from `run_claude_code` so the guarantee is directly testable — the property
    that matters is "no API key reaches the child", and that should be assertable without
    spawning anything.
    """
    env = dict(os.environ if base is None else base)
    for var in _SUPPRESSED_AUTH_VARS:
        env.pop(var, None)
    return env


def run_claude_code(prompt: str, *, model: str | None = None,
                    timeout: int = DEFAULT_TIMEOUT_S) -> str:
    """Send `prompt` through `claude -p` on the SUBSCRIPTION and return the raw text.

    The prompt goes on **stdin**, not argv: a rendered BAML prompt is easily over a
    kilobyte and argv limits are platform-dependent, so passing it as an argument would
    work in testing and fail on a longer schema.

    `ANTHROPIC_API_KEY` is removed from the child environment — see `_SUPPRESSED_AUTH_VARS`.
    """
    if shutil.which(CLAUDE_BIN) is None:
        raise ClaudeCodeError(
            f"`{CLAUDE_BIN}` is not on PATH. The Claude Code CLI provides this "
            "transport; install it or pass a different grader."
        )

    # `claude -p` is a CODING AGENT in headless mode, not a text-completion endpoint: by
    # default it can read and write files and run commands in its working directory. This
    # transport wants exactly one thing from it — a completion — and a grader that can edit
    # the repository it is grading is a worse problem than the metered spend this module was
    # written to avoid. An empty allowlist grants no tools. (Verified: `claude -p
    # --allowed-tools ""` still answers normally.)
    #
    # Cheap now, load-bearing later: today's prompt is assembled from telemetry floats, but
    # `render_prompt` forwards whatever BAML renders, so a future prompt carrying model- or
    # file-derived text would otherwise be an injection path straight into tool use.
    argv = [CLAUDE_BIN, "-p", "--allowed-tools", ""]
    if model:
        argv += ["--model", model]

    try:
        completed = subprocess.run(
            argv,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            env=subscription_env(),
        )
    except subprocess.TimeoutExpired as exc:
        raise ClaudeCodeError(
            f"`{CLAUDE_BIN} -p` did not return within {timeout}s"
        ) from exc
    except OSError as exc:
        raise ClaudeCodeError(f"could not run `{CLAUDE_BIN} -p`: {exc}") from exc

    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[:400]
        raise ClaudeCodeError(
            f"`{CLAUDE_BIN} -p` exited {completed.returncode}: {stderr or '(no stderr)'}"
        )

    raw = (completed.stdout or "").strip()
    if not raw:
        raise ClaudeCodeError(f"`{CLAUDE_BIN} -p` returned no output")
    return raw
