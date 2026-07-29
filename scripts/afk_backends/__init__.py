#!/usr/bin/env python3
"""
AFK backend adapter contract.

Every AFK implementation backend — whether it runs Claude Code on the desktop, a
Podman sandcastle, a cloud worker, or any other AI tool — must satisfy the
AFKBackend protocol in this module. The governor (scripts/run_afk_cycle.py)
selects a backend by name and drives it through this contract, so new tools can be
added without changing the governor.

The contract is intentionally narrow:

- prepare()      → check prerequisites before any work is started
- needs_local_repo() → declare whether the governor must prepare an ephemeral clone
- invoke()       → run the tool and return branch/commits/blocked
- estimate_cost() → rough cost estimate for the AIW budget gate
- cancel()       → best-effort abort of an in-flight invocation

See docs/solutions/harness/2026-07-29-afk-backend-adapter-contract.md for the
full design rationale.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AFKBackend(ABC):
    """Abstract contract for an AFK implementation backend.

    Concrete implementations live in sibling modules under scripts/afk_backends/.
    The governor loads them through the registry (scripts/afk_backends/registry.py)
    and treats them as interchangeable workers.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Optional config from the registry entry.

        Backends that do not need configuration can ignore this. Cloud or
        pluggable backends should read their endpoint, credentials, etc. from
        the registry-supplied config dict.
        """
        self.config = config or {}

    @abstractmethod
    def prepare(self) -> tuple[bool, str]:
        """Check that the backend is ready to run.

        This is called once per cycle before any issue is processed. It should
        verify prerequisites such as: the tool is installed, a daemon is
        running, a cloud endpoint is reachable, credentials are present, etc.

        Returns:
            (ok, note): ok is True if the backend can proceed; note is a human-
            readable status string. A failed prepare is a hard abort for the cycle.
        """

    @abstractmethod
    def needs_local_repo(self) -> bool:
        """Return True if the backend needs an ephemeral clone on this host.

        Desktop/container backends typically return True because they run the
        tool against a local filesystem. Cloud worker backends can return False
        and receive repo_path=None in invoke().
        """

    @abstractmethod
    def invoke(self, issue: dict[str, Any], repo_path: str | None) -> dict:
        """Run the backend for a single issue.

        Args:
            issue: The GitHub issue dict with keys such as number, title, body,
                and labels. The backend must not mutate it.
            repo_path: Path to the ephemeral clone, or None if
                needs_local_repo() returns False.

        Returns:
            A dict with the exact keys:
                branch: str | None — the branch name produced by the agent, or None
                commits: list[str] — commit subject lines produced by the agent
                blocked: str | None — a human-readable reason the issue could not
                    be implemented, or None on success

            If both branch and blocked are None, the governor treats the issue as
            stalled (no progress and no explicit block reason).
        """

    @abstractmethod
    def estimate_cost(self, issue: dict[str, Any]) -> dict:
        """Return a rough cost estimate for the AIW budget gate.

        The estimate should use the recognized budget keys from
        scripts/aiw_budget_gate.py, such as:
            estimated_cost_usd
            estimated_total_tokens
            estimated_model_calls
            estimated_runner_minutes
        Missing keys are treated as zero/unbounded by the gate.
        """

    def cancel(self) -> None:
        """Best-effort cancel of an in-flight invocation.

        The default implementation is a no-op. Backends that support
        cancellation (e.g., cloud workers with a job ID) may override this.
        """
        return None
