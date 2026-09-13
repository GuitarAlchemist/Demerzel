#!/usr/bin/env python3
"""Unit tests for the universal ecosystem-freshness monitor.

Covers the tracer-bullet outcomes (fresh / silent-green / intentionally
disabled) plus the boundary and failure modes the brief calls out: exact
staleness boundaries, proof-adapter (git) API failure, deterministic ordering,
default-branch evidence, and monitor self-exclusion.

stdlib + PyYAML + jsonschema only; no network, no wall-clock (a fixed NOW is
threaded through every evaluation).
"""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

import yaml

try:
    from scripts import ecosystem_freshness as ef
except ModuleNotFoundError:
    import ecosystem_freshness as ef

NOW = datetime(2026, 7, 18, 12, 0, 0, tzinfo=timezone.utc)
# Activation cutoff used by the adapter-level tests: old enough that none of
# their fixtures are waived, so each test still exercises what it names.
SINCE = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class _Repo:
    """A throwaway repo root with a state/ tree and a workflows dir."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.workflows = self.root / ".github" / "workflows"
        self.workflows.mkdir(parents=True)

    def close(self) -> None:
        self._tmp.cleanup()

    def write_state(self, relpath: str, content: str) -> None:
        p = self.root / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def write_workflow(self, name: str, crons=None) -> None:
        crons = ["0 0 * * *"] if crons is None else crons
        schedule = ""
        if crons:
            schedule = "  schedule:\n" + "".join(
                f"    - cron: '{cron}'\n" for cron in crons
            )
        (self.workflows / name).write_text(
            "name: stub\n"
            "on:\n"
            f"{schedule}"
            "  workflow_dispatch:\n"
            "jobs: {}\n",
            encoding="utf-8",
        )

    def write_event_workflow(self, name: str, events: list[str],
                             activities: list[str] | None = None) -> None:
        """A workflow with only event triggers — no cron at all (#844)."""
        event_lines = ""
        for event in events:
            event_lines += f"  {event}:\n"
            if event in {"pull_request", "pull_request_target"} and activities is not None:
                event_lines += "    types: [" + ", ".join(activities) + "]\n"
        (self.workflows / name).write_text(
            "name: stub\n"
            "on:\n"
            + event_lines
            + "jobs: {}\n",
            encoding="utf-8",
        )


class EcosystemFreshnessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = _Repo()
        self.addCleanup(self.repo.close)

    def _evaluate(self, registry: dict, *, git_runner=None,
                  actions_runner=None, auto_workflows=True,
                  event_supply_runner=None, event_producers=None) -> list[dict]:
        # Most unit tests exercise an adapter, not activation declarations. Give
        # them a matching scheduled stub; activation tests opt out explicitly.
        registry = json.loads(json.dumps(registry))
        if auto_workflows:
            for loop in registry.get("loops", []):
                wf = loop.get("workflow")
                if loop.get("status") != "disabled":
                    loop.setdefault("schedule", ["0 0 * * *"])
                if not wf or (self.repo.workflows / wf).exists():
                    continue
                if loop.get("status") == "disabled":
                    self.repo.write_workflow(wf, crons=[])
                else:
                    self.repo.write_workflow(wf, crons=loop["schedule"])
        kwargs = {
            "repository": "GuitarAlchemist/Demerzel",
            "token": "test-token",
            # Event-triggered producers are opt-in per test: the shipped
            # EVENT_PRODUCERS names a real workflow that does not exist in these
            # throwaway repos.
            "event_producers": event_producers or {},
        }
        if git_runner is not None:
            kwargs["git_runner"] = git_runner
        if actions_runner is not None:
            kwargs["actions_runner"] = actions_runner
        if event_supply_runner is not None:
            kwargs["event_supply_runner"] = event_supply_runner
        return ef.evaluate(
            registry,
            now=NOW,
            workflows_dir=self.repo.workflows,
            repo_root=self.repo.root,
            **kwargs,
        )

    def _one(self, findings: list[dict], workflow: str) -> dict:
        return next(f for f in findings if f["workflow"] == workflow)

    @staticmethod
    def _json_urlopen(payloads, seen):
        """urlopen stub serving `payloads` in request order, recording requests."""
        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        return fake_urlopen

    # ── tracer-bullet outcomes ────────────────────────────────────────────

    def test_state_glob_fresh(self):
        self.repo.write_state(
            "state/quality-trend/2026-07.jsonl",
            json.dumps({"timestamp": _iso(NOW - timedelta(hours=6))}) + "\n",
        )
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "demerzel-quality-trend.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/quality-trend/*.jsonl",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 3,
                },
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "demerzel-quality-trend.yml")["kind"],
                         "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_silent_green_when_no_evidence(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "demerzel-ideation.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/ideation/*.json",
                    "timestamp_field": "created_at",
                    "max_stale_days": 7,
                },
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "demerzel-ideation.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_intentionally_disabled_is_neutral(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "seldon-plan.yml",
                "status": "disabled",
                "disabled": {"reason": "paused", "until": "2026-10-16",
                             "verification": "schedule_absent"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "seldon-plan.yml")["kind"], "disabled")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_expired_disable_turns_red(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "seldon-plan.yml",
                "status": "disabled",
                "disabled": {"reason": "paused", "until": "2026-07-17",
                             "verification": "schedule_absent"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "seldon-plan.yml")["kind"],
                         "expired_disable")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_disable_valid_through_until_inclusive(self):
        # `until` is inclusive: a disable expiring today is still valid today.
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "seldon-plan.yml",
                "status": "disabled",
                "disabled": {"reason": "paused", "until": _iso(NOW)[:10],
                             "verification": "schedule_absent"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "seldon-plan.yml")["kind"], "disabled")

    # ── exact boundaries ──────────────────────────────────────────────────

    def test_exact_staleness_boundary(self):
        base = {
            "version": 1,
            "loops": [{
                "workflow": "q.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/q/*.jsonl",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 3,
                },
            }],
        }
        # Exactly 3 days old -> fresh (threshold is strict >).
        self.repo.write_state(
            "state/q/x.jsonl",
            json.dumps({"timestamp": _iso(NOW - timedelta(days=3))}) + "\n",
        )
        self.assertEqual(self._one(self._evaluate(base), "q.yml")["kind"], "healthy")

        # One second past 3 days -> stale.
        self.repo.write_state(
            "state/q/x.jsonl",
            json.dumps(
                {"timestamp": _iso(NOW - timedelta(days=3, seconds=1))}
            ) + "\n",
        )
        self.assertEqual(self._one(self._evaluate(base), "q.yml")["kind"], "stale")

    # ── proof-adapter (git) machinery ─────────────────────────────────────

    def test_git_log_default_branch_evidence(self):
        seen = {}

        def fake_git(args, cwd):
            seen["args"] = args
            return _iso(NOW - timedelta(days=1)) + "\n"

        registry = {
            "version": 1,
            "default_branch": "main",
            "loops": [{
                "workflow": "producer.yml",
                "status": "active",
                "proof": {
                    "adapter": "git_log",
                    "path": "state/triggers/",
                    "max_stale_days": 7,
                },
            }],
        }
        findings = self._evaluate(registry, git_runner=fake_git)
        self.assertEqual(self._one(findings, "producer.yml")["kind"], "healthy")
        # Freshness is judged from the DEFAULT branch, not the working tree.
        self.assertIn("main", seen["args"])
        self.assertIn("state/triggers/", seen["args"])

    def test_git_log_api_failure_is_exit_2(self):
        def boom(args, cwd):
            raise ef.AdapterError("git exploded")

        registry = {
            "version": 1,
            "loops": [{
                "workflow": "producer.yml",
                "status": "active",
                "proof": {
                    "adapter": "git_log",
                    "path": "state/x/",
                    "max_stale_days": 7,
                },
            }],
        }
        findings = self._evaluate(registry, git_runner=boom)
        self.assertEqual(self._one(findings, "producer.yml")["kind"], "adapter_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_git_log_never_committed_is_silent_green(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "producer.yml",
                "status": "active",
                "proof": {
                    "adapter": "git_log",
                    "path": "state/x/",
                    "max_stale_days": 7,
                },
            }],
        }
        findings = self._evaluate(registry, git_runner=lambda args, cwd: "\n")
        self.assertEqual(self._one(findings, "producer.yml")["kind"], "silent_green")

    # ── live GitHub Actions proof adapter ─────────────────────────────────

    def _workflow_run_registry(self, workflow="producer.yml", max_days=3):
        return {
            "version": 1,
            "loops": [{
                "workflow": workflow,
                "status": "active",
                "proof": {
                    "adapter": "workflow_run",
                    "max_stale_days": max_days,
                },
            }],
        }

    def test_workflow_run_success_is_live_proof(self):
        seen = {}

        def runner(workflow, repository, branch, token):
            seen.update(workflow=workflow, repository=repository,
                        branch=branch, token=token)
            return {
                "conclusion": "success",
                "run_started_at": _iso(NOW - timedelta(hours=2)),
                "html_url": "https://example.test/runs/1",
            }

        findings = self._evaluate(
            self._workflow_run_registry(), actions_runner=runner
        )
        self.assertEqual(self._one(findings, "producer.yml")["kind"], "healthy")
        self.assertEqual(seen, {
            "workflow": "producer.yml",
            "repository": "GuitarAlchemist/Demerzel",
            "branch": "master",
            "token": "test-token",
        })

    def test_known_failed_loop_turns_red(self):
        findings = self._evaluate(
            self._workflow_run_registry("demerzel-capability-expansion.yml", 10),
            actions_runner=lambda *args: {
                "conclusion": "failure",
                "run_started_at": _iso(NOW - timedelta(days=5)),
                "html_url": "https://example.test/runs/failed",
            },
        )
        finding = self._one(findings, "demerzel-capability-expansion.yml")
        self.assertEqual(finding["kind"], "failed_run")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_workflow_run_missing_or_stale_turns_red(self):
        registry = self._workflow_run_registry(max_days=3)
        missing = self._evaluate(registry, actions_runner=lambda *args: None)
        self.assertEqual(self._one(missing, "producer.yml")["kind"],
                         "silent_green")
        stale = self._evaluate(registry, actions_runner=lambda *args: {
            "conclusion": "success",
            "run_started_at": _iso(NOW - timedelta(days=3, seconds=1)),
        })
        self.assertEqual(self._one(stale, "producer.yml")["kind"], "stale")

    # ── newborn vs genuinely-silent (issue #850) ──────────────────────────

    def _birth_git(self, added_at, seen=None):
        """git_runner stub answering the `--diff-filter=A` birth query."""
        def runner(args, cwd):
            if seen is not None:
                seen["args"] = args
            return "" if added_at is None else _iso(added_at) + "\n"
        return runner

    def test_newborn_low_cadence_loop_stays_quiet(self):
        # substrate-audit.yml: monthly cron, 35d threshold, added 7 days ago.
        # Its first scheduled opportunity has not arrived, so "no run" is not
        # evidence of death and must not turn the board red.
        seen = {}
        findings = self._evaluate(
            self._workflow_run_registry("substrate-audit.yml", 35),
            actions_runner=lambda *args: None,
            git_runner=self._birth_git(NOW - timedelta(days=7), seen),
        )
        finding = self._one(findings, "substrate-audit.yml")
        self.assertEqual(finding["kind"], "newborn")
        self.assertEqual(ef.exit_code(findings), 0)
        self.assertEqual(ef.stable_alert(findings), [])
        # Birth is read from the DEFAULT branch's add-commit, not the worktree.
        self.assertIn("--diff-filter=A", seen["args"])
        self.assertIn("master", seen["args"])
        self.assertIn(".github/workflows/substrate-audit.yml", seen["args"])

    def test_overdue_silent_loop_still_fires_after_grace(self):
        # Same loop, one second past its own staleness window with still no
        # run: the grace has run out and silence is now proof of death.
        findings = self._evaluate(
            self._workflow_run_registry("substrate-audit.yml", 35),
            actions_runner=lambda *args: None,
            git_runner=self._birth_git(NOW - timedelta(days=35, seconds=1)),
        )
        self.assertEqual(self._one(findings, "substrate-audit.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_newborn_grace_scales_to_the_declared_cadence(self):
        # A 1-day-threshold loop silent for 2 days is dead, not newborn — the
        # grace is the loop's own cadence-scaled window, not a fixed one.
        findings = self._evaluate(
            self._workflow_run_registry("ga-chatbot-discussions.yml", 1),
            actions_runner=lambda *args: None,
            git_runner=self._birth_git(NOW - timedelta(days=2)),
        )
        self.assertEqual(self._one(findings, "ga-chatbot-discussions.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_unprovable_birth_does_not_suppress(self):
        # Never added on the default branch -> birth unknown. An unprovable
        # birth date is not evidence of youth; the finding must survive.
        findings = self._evaluate(
            self._workflow_run_registry("producer.yml", 35),
            actions_runner=lambda *args: None,
            git_runner=self._birth_git(None),
        )
        self.assertEqual(self._one(findings, "producer.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_broken_git_does_not_suppress(self):
        def boom(args, cwd):
            raise ef.AdapterError("git exploded")

        findings = self._evaluate(
            self._workflow_run_registry("producer.yml", 35),
            actions_runner=lambda *args: None,
            git_runner=boom,
        )
        self.assertEqual(self._one(findings, "producer.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_newborn_grace_applies_to_state_glob_evidence(self):
        # Same defect for a committed-state producer: a brand-new loop has not
        # had a window in which to write its first state file.
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "newborn-producer.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/newborn/*.jsonl",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 7,
                },
            }],
        }
        findings = self._evaluate(
            registry, git_runner=self._birth_git(NOW - timedelta(days=2))
        )
        self.assertEqual(self._one(findings, "newborn-producer.yml")["kind"],
                         "newborn")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_workflow_run_adapter_failure_is_exit_2(self):
        def boom(*args):
            raise ef.AdapterError("Actions API unavailable")

        findings = self._evaluate(
            self._workflow_run_registry(), actions_runner=boom
        )
        self.assertEqual(self._one(findings, "producer.yml")["kind"],
                         "adapter_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_default_actions_adapter_queries_completed_scheduled_run(self):
        seen = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({"workflow_runs": [{"id": 42}]}).encode()

        def fake_urlopen(request, timeout):
            seen["request"] = request
            seen["timeout"] = timeout
            return Response()

        with patch.object(ef, "urlopen", fake_urlopen):
            run = ef.default_actions_runner(
                "qa-tribunal.yml", "GuitarAlchemist/Demerzel", "master", "secret"
            )
        self.assertEqual(run, {"id": 42})
        parsed = urlparse(seen["request"].full_url)
        self.assertEqual(parse_qs(parsed.query), {
            "event": ["schedule"], "branch": ["master"],
            "status": ["completed"], "per_page": ["1"],
        })
        self.assertNotIn("secret", seen["request"].full_url)
        self.assertEqual(seen["request"].get_header("Authorization"),
                         "Bearer secret")

    # ── event-triggered producers (#844) ──────────────────────────────────
    #
    # These loops have no cadence, so freshness is bound to EVENT SUPPLY: a
    # `pull_request` loop is only expected to have run when a PR happened.
    # Both directions matter — a genuinely dead loop must fire, and a quiet but
    # healthy one must stay silent.

    # The activation cutoff is deliberately far older than any event age these
    # tests use, so cutoff waiving never silently swallows a case that is meant
    # to be about liveness. Cutoff behaviour has its own tests below.
    ACTIVATION = "2024-01-01T00:00:00Z"

    EVENT_SPEC = {"reviewer.yml": {
        "events": ["pull_request", "pull_request_target"],
        "activities": ["opened", "synchronize"],
        "max_stale_days": 3,
        "activation": {
            "pull_request": ACTIVATION,
            "pull_request_target": ACTIVATION,
        },
    }}

    def _event_repo(self, events=("pull_request",)):
        self.repo.write_event_workflow(
            "reviewer.yml", list(events), ["opened", "synchronize"]
        )

    def _supply(self, event_age_days=None, run_age_days=None,
                conclusion="success", pull_number=17,
                obligation_sha="current-head", run_sha="current-head",
                run_pull_number=17, pull_state="open"):
        """Stub the (current dispatch obligation, candidate run) seam."""
        event_iso = (
            None if event_age_days is None
            else _iso(NOW - timedelta(days=event_age_days))
        )
        obligation = None if event_iso is None else {
            "activities": ["opened", "synchronize"],
            "occurred_at": event_iso,
            "pull_number": pull_number,
            "head_sha": obligation_sha,
            "pull_state": pull_state,
        }
        run = None if run_age_days is None else {
            "status": "completed",
            "conclusion": conclusion,
            "run_started_at": _iso(NOW - timedelta(days=run_age_days)),
            "html_url": "https://example.test/pr-run",
            "head_sha": run_sha,
            "pull_requests": [{"number": run_pull_number}],
        }
        return lambda *args: [] if obligation is None else [(obligation, run)]

    def _event_findings(self, supply, git_runner=None):
        self._event_repo()
        return self._evaluate(
            {"version": 1, "loops": []},
            event_producers=self.EVENT_SPEC,
            event_supply_runner=supply,
            git_runner=git_runner or (lambda args, cwd: ""),
        )

    def test_event_loop_dead_while_events_flow_turns_red(self):
        # THE #844 SHAPE: PRs kept arriving, the loop stopped answering, and
        # nothing enumerated it because it has no cron.
        findings = self._event_findings(
            self._supply(
                event_age_days=4,
                run_age_days=9,
                obligation_sha="synchronized-head",
                run_sha="opening-head",
            )
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "stale")
        self.assertIn("no correlated run after 4.0d", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_event_loop_quiet_with_no_event_supply_stays_silent(self):
        # THE OTHER DIRECTION: the last PR was 30d ago and was answered. A repo
        # with a quiet month must not turn the board red — that is the cry-wolf
        # failure that trains people to ignore the guard.
        findings = self._event_findings(
            self._supply(event_age_days=30, run_age_days=30)
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertIn("correlated successful run", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 0)

    def test_a_dead_loop_stays_red_however_long_the_repo_stays_quiet(self):
        """Regression for the vanishing detection window (adversarial review, pre-merge).

        The first version compared the event and the run each against `now`:
        `event_age <= max AND run_age > max`. That makes the window in which both hold
        exactly as wide as the gap between the dead loop's last run and the unanswered
        event — here six hours — and then it CLOSES, because the event ages past the
        window and the quiet arm returns healthy. A loop that died just before a final
        event and then went quiet read green forever, and this guard runs once a day
        (cron `15 13 * * *`), so it could miss the window entirely.

        Ordering has no window. The event is unanswered and stays unanswered, so the
        finding must hold at 4 days, 40 days and 400.
        """
        # Run at T, the event it never answered 6h later — a lag far INSIDE the
        # allowance, so only the unanswered-duration arm can catch this one.
        for quiet_days in (4, 40, 400):
            with self.subTest(quiet_days=quiet_days):
                findings = self._event_findings(
                    self._supply(
                        event_age_days=quiet_days,
                        run_age_days=quiet_days + 0.25,
                        obligation_sha="synchronized-head",
                        run_sha="opening-head",
                    )
                )
                finding = self._one(findings, "reviewer.yml")
                self.assertEqual(
                    finding["kind"], "stale",
                    f"a loop dead for {quiet_days}d read {finding['kind']!r}; evidence of "
                    "death must not decay at the same rate as the obligation")
                self.assertEqual(ef.exit_code(findings), 1)

    def test_event_loop_never_triggered_at_all_stays_silent(self):
        # No PR has ever existed: absence of supply, not absence of life.
        findings = self._event_findings(self._supply(event_age_days=None))
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_event_loop_answering_supply_is_healthy(self):
        findings = self._event_findings(
            self._supply(event_age_days=0.2, run_age_days=0.2)
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_synchronize_is_unanswered_after_a_successful_opening_run(self):
        findings = self._event_findings(self._supply(
            event_age_days=4,
            run_age_days=5,
            obligation_sha="synchronized-head",
            run_sha="opening-head",
        ))
        finding = self._one(findings, "reviewer.yml")
        self.assertIn(finding["kind"], {"silent_green", "stale"})
        self.assertEqual(ef.exit_code(findings), 1)

    def test_unrelated_delayed_run_cannot_answer_a_pull_request(self):
        findings = self._event_findings(self._supply(
            event_age_days=4,
            run_age_days=0.1,
            pull_number=17,
            obligation_sha="expected-head",
            run_pull_number=99,
            run_sha="unrelated-head",
        ))
        finding = self._one(findings, "reviewer.yml")
        self.assertIn(finding["kind"], {"silent_green", "stale"})
        self.assertEqual(ef.exit_code(findings), 1)

    def test_commit_association_correlates_a_merged_pull_request_run(self):
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=30)),
            "pull_number": 17,
            "head_sha": "merged-head",
        }
        run = {
            "status": "completed",
            "conclusion": "success",
            "run_started_at": _iso(NOW - timedelta(days=30)),
            "html_url": "https://example.test/merged-pr-run",
            "head_sha": "merged-head",
            "pull_requests": [],
            "associated_pull_requests": [{"number": 17}],
        }
        findings = self._event_findings(lambda *args: [(obligation, run)])
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_recent_absent_run_is_pending_within_response_allowance(self):
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=1)),
            "pull_number": 17,
            "head_sha": "current-head",
        }
        findings = self._event_findings(lambda *args: [(obligation, None)])
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "pending")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_recent_queued_or_in_progress_run_is_pending_within_allowance(self):
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=1)),
            "pull_number": 17,
            "head_sha": "current-head",
        }
        for status in ("queued", "in_progress"):
            with self.subTest(status=status):
                run = {
                    "status": status,
                    "conclusion": None,
                    "created_at": _iso(NOW - timedelta(days=1)),
                    "head_sha": "current-head",
                    "pull_requests": [{"number": 17}],
                }
                findings = self._event_findings(lambda *args: [(obligation, run)])
                finding = self._one(findings, "reviewer.yml")
                self.assertEqual(finding["kind"], "pending")
                self.assertEqual(ef.exit_code(findings), 0)

    def test_one_answered_pull_cannot_mask_an_overdue_pull(self):
        answered = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(hours=1)),
            "pull_number": 18,
            "head_sha": "answered-head",
        }
        answered_run = {
            "status": "completed",
            "conclusion": "success",
            "run_started_at": _iso(NOW - timedelta(hours=1)),
            "head_sha": "answered-head",
            "pull_requests": [{"number": 18}],
        }
        overdue = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=4)),
            "pull_number": 17,
            "head_sha": "unanswered-head",
        }
        findings = self._event_findings(
            lambda *args: [(answered, answered_run), (overdue, None)]
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "silent_green")
        self.assertIn("#17", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_boolean_pull_identity_is_malformed_evidence(self):
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=1)),
            "pull_number": 1,
            "head_sha": "current-head",
        }
        run = {
            "status": "completed",
            "conclusion": "success",
            "run_started_at": _iso(NOW - timedelta(days=1)),
            "head_sha": "current-head",
            "pull_requests": [{"number": True}],
        }
        findings = self._event_findings(lambda *args: [(obligation, run)])
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "malformed_proof")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_event_loop_with_live_supply_and_no_run_is_pending_within_allowance(self):
        findings = self._event_findings(
            self._supply(event_age_days=1, run_age_days=None)
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "pending")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_event_loop_failed_run_turns_red(self):
        # Post-#840 a broken reviewer exits non-zero, so the conclusion is the
        # leg that catches the original incident class.
        findings = self._event_findings(
            self._supply(event_age_days=0.5, run_age_days=0.5,
                         conclusion="failure")
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "failed_run")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_newborn_event_loop_is_not_reported_dead(self):
        # #850 grace applies unchanged: a loop added yesterday cannot have
        # answered a PR opened before it existed.
        findings = self._event_findings(
            self._supply(event_age_days=4, run_age_days=None),
            git_runner=lambda args, cwd: _iso(NOW - timedelta(days=0.5)) + "\n",
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "newborn")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_event_loop_past_newborn_grace_still_fires(self):
        findings = self._event_findings(
            self._supply(event_age_days=4, run_age_days=None),
            git_runner=lambda args, cwd: _iso(NOW - timedelta(days=40)) + "\n",
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_event_loop_losing_its_trigger_turns_red(self):
        # Silently rewriting `on:` must not make the producer vanish from the
        # guard the way a cron-less workflow does today.
        self.repo.write_event_workflow("reviewer.yml", ["workflow_dispatch"])
        findings = self._evaluate(
            {"version": 1, "loops": []},
            event_producers=self.EVENT_SPEC,
            event_supply_runner=lambda *args: self.fail("must not call API"),
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "activation_mismatch")
        self.assertIn("pull_request", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_secured_pull_request_target_trigger_is_compatible(self):
        self.repo.write_event_workflow(
            "reviewer.yml",
            ["pull_request_target"],
            ["opened", "synchronize"],
        )
        findings = self._evaluate(
            {"version": 1, "loops": []},
            event_producers=self.EVENT_SPEC,
            event_supply_runner=lambda *args: [({
                "activities": ["opened", "synchronize"],
                "occurred_at": _iso(NOW - timedelta(hours=1)),
                "pull_number": 17,
                "head_sha": "pr-head",
            }, {
                "status": "completed",
                "conclusion": "success",
                "created_at": _iso(NOW - timedelta(hours=1)),
                "run_started_at": _iso(NOW - timedelta(hours=1)),
                # pull_request_target runs execute against the trusted base SHA.
                "head_sha": "base-head",
                "pull_requests": [{
                    "number": 17,
                    "head": {"sha": "pr-head"},
                }],
            })],
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_event_loop_deleted_workflow_turns_red(self):
        findings = self._evaluate(
            {"version": 1, "loops": []},
            event_producers=self.EVENT_SPEC,
            event_supply_runner=lambda *args: self.fail("must not call API"),
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"],
                         "activation_mismatch")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_event_supply_adapter_failure_is_exit_2(self):
        def boom(*args):
            raise ef.AdapterError("GitHub API failed for pull_request supply")

        findings = self._event_findings(boom)
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"],
                         "adapter_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_event_producer_cannot_also_be_a_registered_scheduled_loop(self):
        self._event_repo()
        self.repo.write_workflow("reviewer.yml", crons=["0 0 * * *"])
        findings = self._evaluate({
            "version": 1,
            "loops": [{"workflow": "reviewer.yml", "status": "active",
                       "schedule": ["0 0 * * *"],
                       "proof": {"adapter": "workflow_run",
                                 "max_stale_days": 1}}],
        }, event_producers=self.EVENT_SPEC,
            actions_runner=lambda *args: {
                "conclusion": "success", "run_started_at": _iso(NOW)},
            event_supply_runner=lambda *args: self.fail("must not call API"))
        self.assertTrue(any(
            f["kind"] == "config_error" and "event-triggered" in f["detail"]
            for f in findings
        ))

    def test_default_event_supply_adapter_queries_pulls_and_pr_runs(self):
        seen = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        payloads = [
            [{
                "number": 939,
                "state": "open",
                "created_at": "2026-07-18T09:00:00Z",
                "updated_at": "2026-07-18T10:00:00Z",
                "head": {"sha": "current-head"},
            }],
            {"workflow_runs": [{
                "id": 7,
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-07-18T09:00:03Z",
                "run_started_at": "2026-07-18T09:00:04Z",
                "head_sha": "current-head",
                "pull_requests": [{"number": 939}],
            }]},
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        obligation, run = supplies[0]
        self.assertEqual(obligation, {
            "activities": ["opened", "synchronize"],
            "occurred_at": "2026-07-18T09:00:03+00:00",
            "pull_number": 939,
            "head_sha": "current-head",
            "pull_state": "open",
        })
        self.assertEqual(run, {
            "id": 7,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2026-07-18T09:00:03Z",
            "run_started_at": "2026-07-18T09:00:04Z",
            "head_sha": "current-head",
            "pull_requests": [{"number": 939}],
        })

        pulls_q = parse_qs(urlparse(seen[0].full_url).query)
        self.assertEqual(pulls_q, {
            # `all`, not `open`: a merge is not an answer, so a closed pull
            # request keeps its unresolved obligation visible.
            "state": ["all"], "sort": ["updated"],
            "direction": ["desc"], "per_page": ["100"], "page": ["1"],
        })
        runs_q = parse_qs(urlparse(seen[1].full_url).query)
        self.assertEqual(runs_q, {
            "event": ["pull_request"], "head_sha": ["current-head"],
            "per_page": ["1"],
        })
        # A pull_request run lives on the PR head branch, so a default-branch
        # filter would find nothing and read every healthy loop as dead.
        self.assertNotIn("branch", runs_q)
        for request in seen:
            self.assertNotIn("secret", request.full_url)
            self.assertEqual(request.get_header("Authorization"), "Bearer secret")

    def test_event_supply_adapter_treats_an_explicitly_empty_pull_list_as_quiet(self):
        seen = []

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b"[]"

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response()

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        self.assertEqual(supplies, [])
        self.assertEqual(len(seen), 1)

    def test_event_supply_adapter_resolves_empty_run_pull_association(self):
        seen = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        payloads = [
            [{
                "number": 17,
                "state": "closed",
                "created_at": "2026-07-18T09:00:00Z",
                "updated_at": "2026-07-18T10:00:00Z",
                "head": {"sha": "merged-head"},
            }],
            {"workflow_runs": [{
                "id": 7,
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-07-18T10:00:00Z",
                "head_sha": "merged-head",
                "pull_requests": [],
            }]},
            [{"number": 17}],
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        _, run = supplies[0]
        self.assertEqual(run["associated_pull_requests"], [{"number": 17}])
        self.assertIn("/commits/merged-head/pulls", seen[2].full_url)

    def test_adapter_does_not_treat_generic_pull_updated_at_as_synchronize(self):
        seen = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        payloads = [
            [{
                "number": 17,
                "state": "open",
                "created_at": "2026-07-18T09:00:00Z",
                # A comment or label may cause this update; it is not a dispatch.
                "updated_at": "2026-07-20T10:00:00Z",
                "head": {"sha": "opening-head"},
            }],
            {"workflow_runs": [{
                "id": 7,
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-07-18T09:00:03Z",
                "run_started_at": "2026-07-18T09:00:04Z",
                "head_sha": "opening-head",
                "pull_requests": [{"number": 17}],
            }]},
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        obligation, _ = supplies[0]
        self.assertEqual(obligation["activities"], ["opened", "synchronize"])
        self.assertEqual(obligation["occurred_at"], "2026-07-18T09:00:03+00:00")

    def test_adapter_dates_an_absent_run_from_the_current_head_commit(self):
        seen = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        payloads = [
            [{
                "number": 17,
                "state": "open",
                "created_at": "2026-07-18T09:00:00Z",
                "updated_at": "2026-07-20T10:00:00Z",
                "head": {"sha": "unanswered-head"},
            }],
            {"workflow_runs": []},
            {"commit": {"committer": {"date": "2026-07-19T11:00:00Z"}}},
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        obligation, run = supplies[0]
        self.assertIsNone(run)
        # Inside the GitHub-controlled [created_at, updated_at] envelope, so the
        # commit date is an accepted refinement rather than an authority.
        self.assertEqual(obligation["occurred_at"], "2026-07-19T11:00:00+00:00")
        self.assertNotIn("malformed_reason", obligation)
        self.assertIn("/commits/unanswered-head", seen[2].full_url)

    def test_pull_request_target_adapter_matches_nested_pr_head_identity(self):
        seen = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(self.payload).encode()

        payloads = [
            [{
                "number": 17,
                "state": "open",
                "created_at": "2026-07-18T09:00:00Z",
                "updated_at": "2026-07-18T09:30:00Z",
                "head": {"sha": "pr-head"},
            }],
            {"workflow_runs": [{
                "id": 7,
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-07-18T09:00:03Z",
                "run_started_at": "2026-07-18T09:00:04Z",
                "head_sha": "base-head",
                "pull_requests": [{
                    "number": 17,
                    "head": {"sha": "pr-head"},
                }],
            }]},
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request_target",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        _, run = supplies[0]
        self.assertEqual(run["id"], 7)
        runs_q = parse_qs(urlparse(seen[1].full_url).query)
        self.assertNotIn("head_sha", runs_q)

    def test_event_supply_adapter_rejects_a_malformed_first_pull(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b"[{}]"

        with patch.object(ef, "urlopen", lambda *args, **kwargs: Response()):
            with self.assertRaises(ef.AdapterError):
                ef.default_event_supply_runner(
                    "cross-model-review.yml", "pull_request",
                    "GuitarAlchemist/Demerzel", "secret",
                    ("opened", "synchronize"), SINCE,
                )

    def test_event_supply_adapter_rejects_an_unparseable_pull_timestamp(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps([{
                    "number": 17,
                    "state": "open",
                    "created_at": "not-a-timestamp",
                    "updated_at": "2026-07-18T10:00:00Z",
                    "head": {"sha": "current-head"},
                }]).encode()

        with patch.object(ef, "urlopen", lambda *args, **kwargs: Response()):
            with self.assertRaises(ef.AdapterError):
                ef.default_event_supply_runner(
                    "cross-model-review.yml", "pull_request",
                    "GuitarAlchemist/Demerzel", "secret",
                    ("opened", "synchronize"), SINCE,
                )

    def test_event_supply_adapter_requires_repository_and_token(self):
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "pull_request", "", "t")
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "pull_request", "o/r", "")
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "issues", "o/r", "t")

    def test_event_supply_adapter_requires_an_activation_cutoff(self):
        # Without a boundary the "relevant history" is unbounded and the waiver
        # has no meaning; refuse rather than walk the whole archive.
        with patch.object(ef, "urlopen",
                          lambda *a, **k: self.fail("must not call API")):
            with self.assertRaises(ef.AdapterError):
                ef.default_event_supply_runner(
                    "cross-model-review.yml", "pull_request",
                    "GuitarAlchemist/Demerzel", "secret",
                )

    # ── obligations survive PR closure (adversarial review, defect 1) ──────
    #
    # Requesting only OPEN pull requests made the merge button an eraser: a PR
    # whose head never got a correlated run vanished from the supply the moment
    # it closed, and the monitor went green. Closing is not answering.

    def _closed_obligation(self, days=4, head="unanswered-head"):
        return {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=days)),
            "pull_number": 17,
            "head_sha": head,
            "pull_state": "closed",
        }

    def test_unresolved_obligation_survives_its_pull_request_closing(self):
        findings = self._event_findings(
            lambda *args: [(self._closed_obligation(), None)]
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(
            finding["kind"], "silent_green",
            "closing a pull request must not discharge an obligation its head "
            "never had a correlated run for")
        self.assertIn("(closed)", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_closing_after_a_correlated_successful_run_is_not_an_alarm(self):
        # The other direction: a PR that WAS answered and then merged is
        # resolved, and resurrecting it would be pure cry-wolf.
        run = {
            "status": "completed",
            "conclusion": "success",
            "run_started_at": _iso(NOW - timedelta(days=4)),
            "html_url": "https://example.test/answered",
            "head_sha": "unanswered-head",
            "pull_requests": [{"number": 17}],
        }
        findings = self._event_findings(
            lambda *args: [(self._closed_obligation(), run)]
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_a_merged_pull_request_cannot_erase_its_unanswered_obligation(self):
        """End-to-end oracle for the erasure defect, adapter through evaluator.

        The stub HONOURS the `state` query the way GitHub does, so asking for
        open pull requests really does return nothing. That is the whole bug: the
        one PR in this repo is closed and its head never got a run, and querying
        `state=open` made the supply empty, which the evaluator correctly reads as
        "no event ever happened" — green. The obligation was never discharged;
        it was deleted.
        """
        merged_pull = {
            "number": 17,
            "state": "closed",
            "created_at": "2026-07-10T09:00:00Z",
            "updated_at": "2026-07-12T10:00:00Z",
            "head": {"sha": "merged-head"},
        }

        def state_honouring_urlopen(request, timeout):
            query = parse_qs(urlparse(request.full_url).query)
            if "/pulls?" in request.full_url:
                requested = query.get("state", ["open"])[0]
                pulls = [merged_pull] if requested == "all" else []
                return self._json_urlopen([pulls], [])(request, timeout)
            if "/runs?" in request.full_url:
                return self._json_urlopen(
                    [{"workflow_runs": []}], [])(request, timeout)
            return self._json_urlopen(
                [{"commit": {"committer": {"date": "2026-07-11T09:00:00Z"}}}],
                [])(request, timeout)

        with patch.object(ef, "urlopen", state_honouring_urlopen):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        self.assertEqual(
            len(supplies), 1,
            "a closed pull request whose head never ran must stay in the supply")
        obligation, run = supplies[0]
        self.assertIsNone(run)
        self.assertEqual(obligation["pull_state"], "closed")

        # …and the surviving obligation really does turn the board red.
        findings = self._event_findings(lambda *args: supplies)
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "silent_green")
        self.assertIn("(closed)", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    # ── bounded relevant history, not an unbounded archive walk ────────────

    def test_pull_retrieval_stops_at_the_activation_cutoff(self):
        seen = []
        fresh = [{
            "number": n,
            "state": "open",
            "created_at": "2026-07-17T00:00:00Z",
            "updated_at": "2026-07-17T00:00:00Z",
            "head": {"sha": f"h{n}"},
        } for n in range(100)]
        ancient = [{
            "number": 999,
            "state": "closed",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "head": {"sha": "ancient"},
        }]
        with patch.object(ef, "urlopen",
                          self._json_urlopen([fresh, ancient], seen)):
            pulls = ef._collect_relevant_pulls(
                "GuitarAlchemist/Demerzel", "GuitarAlchemist/Demerzel",
                "pull_request", "secret", SINCE,
            )
        self.assertEqual(len(pulls), 100, "pre-cutoff pulls must be dropped")
        self.assertEqual(len(seen), 2, "retrieval must stop at the boundary")

    def test_incomplete_pull_retrieval_is_adapter_error_not_absence(self):
        fresh = [{
            "number": n,
            "state": "open",
            "created_at": "2026-07-17T00:00:00Z",
            "updated_at": "2026-07-17T00:00:00Z",
            "head": {"sha": f"h{n}"},
        } for n in range(100)]
        with patch.object(ef, "urlopen",
                          self._json_urlopen([fresh] * 200, [])):
            with self.assertRaises(ef.AdapterError):
                ef._collect_relevant_pulls(
                    "GuitarAlchemist/Demerzel", "GuitarAlchemist/Demerzel",
                    "pull_request", "secret", SINCE,
                )

    # ── retrieval cost vs. sticky obligations (#963) ───────────────────────

    def _routed_urlopen(self, pulls, seen, run_for_head=None):
        """urlopen stub that answers by ENDPOINT, not by call order.

        Order-indexed stubs cannot express "N pulls, therefore N run lookups",
        which is exactly the cost shape #963 is about.
        """
        def fake_urlopen(request, timeout):
            seen.append(request)
            url = request.full_url
            query = parse_qs(urlparse(url).query)
            if "/pulls?" in url:
                page = int(query.get("page", ["1"])[0])
                payload = pulls if page == 1 else []
            elif "/runs?" in url:
                head = query.get("head_sha", [""])[0]
                run = run_for_head(head) if run_for_head else None
                payload = {"workflow_runs": [run] if run else []}
            elif url.endswith("/pulls"):  # commits/{sha}/pulls association
                payload = []
            else:  # commits/{sha}
                payload = {"commit": {"committer":
                                      {"date": "2026-05-19T00:00:00Z"}}}
            return self._json_urlopen([payload], [])(request, timeout)

        return fake_urlopen

    def test_supply_retrieval_cost_grows_with_the_number_of_pull_requests(self):
        """Baseline: one listing request plus one run lookup PER pull request.

        The activation cutoff is fixed forever, so the set of pull requests
        "updated since the cutoff" only ever grows, and with it this request
        count — the operational fuse #963 exists to bound. Recorded here as an
        executable baseline so any bounding change has a number to beat.
        """
        def measure(pull_count):
            seen = []
            pulls = [{
                "number": n,
                "state": "open",
                "created_at": "2026-07-17T00:00:00Z",
                "updated_at": "2026-07-17T00:00:00Z",
                "head": {"sha": f"h{n}"},
            } for n in range(pull_count)]
            run_for_head = lambda head: {
                "id": 1,
                "status": "completed",
                "conclusion": "success",
                "created_at": "2026-07-17T01:00:00Z",
                "run_started_at": "2026-07-17T01:00:00Z",
                "head_sha": head,
                "pull_requests": [{"number": int(head[1:]),
                                   "head": {"sha": head}}],
            }
            with patch.object(ef, "urlopen",
                              self._routed_urlopen(pulls, seen, run_for_head)):
                supplies = ef.default_event_supply_runner(
                    "cross-model-review.yml", "pull_request",
                    "GuitarAlchemist/Demerzel", "secret",
                    ("opened", "synchronize"), SINCE,
                )
            self.assertEqual(len(supplies), pull_count)
            return len(seen)

        self.assertEqual(measure(10), 11)
        self.assertEqual(measure(60), 61)
        # …and the whole growth curve stays under the budget for a long time.
        self.assertGreater(ef._MAX_SUPPLY_REQUESTS, 61)

    def test_supply_retrieval_fails_closed_at_its_request_budget(self):
        """Cost is bounded by failing loudly, never by retrieving less.

        GITHUB_TOKEN's hourly ceiling would otherwise stop retrieval mid-flight
        as an opaque 403. The budget fires first and says so — and it raises
        rather than returning the obligations it managed to collect, because a
        partial supply read as a complete one is silent green.
        """
        seen = []
        pulls = [{
            "number": n,
            "state": "open",
            "created_at": "2026-07-17T00:00:00Z",
            "updated_at": "2026-07-17T00:00:00Z",
            "head": {"sha": f"h{n}"},
        } for n in range(10)]
        with patch.object(ef, "_MAX_SUPPLY_REQUESTS", 4):
            with patch.object(ef, "urlopen", self._routed_urlopen(pulls, seen)):
                with self.assertRaises(ef.AdapterError) as caught:
                    ef.default_event_supply_runner(
                        "cross-model-review.yml", "pull_request",
                        "GuitarAlchemist/Demerzel", "secret",
                        ("opened", "synchronize"), SINCE,
                    )
        self.assertIn("budget", str(caught.exception))
        self.assertIn("cannot be read as absence", str(caught.exception))
        self.assertEqual(len(seen), 4, "the budget must stop the spending")

    def test_request_budget_does_not_leak_across_evaluations(self):
        # A module-level total would make the second daily loop inherit the
        # first one's spending and fail for a cost it never incurred.
        pulls = [{
            "number": 1,
            "state": "open",
            "created_at": "2026-07-17T00:00:00Z",
            "updated_at": "2026-07-17T00:00:00Z",
            "head": {"sha": "h1"},
        }]
        with patch.object(ef, "_MAX_SUPPLY_REQUESTS", 3):
            for _ in range(3):
                with patch.object(ef, "urlopen",
                                  self._routed_urlopen(pulls, [])):
                    supplies = ef.default_event_supply_runner(
                        "cross-model-review.yml", "pull_request",
                        "GuitarAlchemist/Demerzel", "secret",
                        ("opened", "synchronize"), SINCE,
                    )
                self.assertEqual(len(supplies), 1)

    def test_unanswered_obligation_survives_beyond_any_moving_horizon(self):
        """Sticky-red past PR closure AND past a proposed sliding window.

        The tracer bullet floated in #963 —
        `retrieval_floor = max(activation_cutoff, now - k * max_stale_days)` —
        filters the pull listing on `updated_at`. This pull request's last
        GitHub-recorded activity is far older than that horizon for any small
        `k`, its head never got a run, and it is closed. Under a sliding floor
        it would be paginated away and the board would read "no event has
        occurred" — green — while the obligation is still unanswered.
        """
        max_stale_days = self.EVENT_SPEC["reviewer.yml"]["max_stale_days"]
        horizon = NOW - timedelta(days=3 * max_stale_days)
        updated_at = NOW - timedelta(days=60)
        self.assertLess(
            updated_at, horizon,
            "fixture must sit beyond the proposed moving horizon to be a test")

        seen = []
        pulls = [{
            "number": 17,
            "state": "closed",
            "created_at": _iso(NOW - timedelta(days=62)),
            "updated_at": _iso(updated_at),
            "head": {"sha": "abandoned-head"},
        }]
        with patch.object(ef, "urlopen", self._routed_urlopen(pulls, seen)):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        self.assertEqual(
            len(supplies), 1,
            "an unanswered obligation must not age out of retrieval")
        obligation, run = supplies[0]
        self.assertIsNone(run)
        self.assertEqual(obligation["pull_state"], "closed")

        # …and it must still be RED end-to-end, not merely retrievable.
        findings = self._event_findings(lambda *args: supplies)
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

    # ── author-controlled commit dates cannot buy allowance (defect 2) ─────

    def test_future_commit_timestamp_cannot_extend_the_allowance(self):
        # A PR author controls the committer date. `2099-01-01` dated the
        # obligation decades into the future, so `event_age` went negative, the
        # obligation stayed forever "pending", and the guard never fired.
        seen = []
        payloads = [
            [{
                "number": 17,
                "state": "open",
                "created_at": "2026-06-01T09:00:00Z",
                "updated_at": "2026-06-02T09:00:00Z",
                "head": {"sha": "forged-head"},
            }],
            {"workflow_runs": []},
            {"commit": {"committer": {"date": "2099-01-01T00:00:00Z"}}},
        ]
        with patch.object(ef, "urlopen",
                          self._json_urlopen(payloads, seen)):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        obligation, _ = supplies[0]
        occurred_at = ef._parse_iso(obligation["occurred_at"])
        self.assertLessEqual(
            occurred_at, ef._parse_iso("2026-06-02T09:00:00Z"),
            "the obligation must stay inside the GitHub-controlled envelope")
        self.assertIn("malformed_reason", obligation)

        # …and the evaluator reports it as bad evidence, not as a fresh event.
        findings = self._event_findings(lambda *args: supplies)
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "malformed_proof")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_future_observation_time_fails_closed(self):
        # Whatever produced it — a forged commit, a broken clock, a GitHub
        # timestamp this monitor cannot have observed — an obligation dated in
        # the future is not proof and must never buy an unexpiring allowance.
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW + timedelta(days=26000)),
            "pull_number": 17,
            "head_sha": "future-head",
            "pull_state": "open",
        }
        findings = self._event_findings(lambda *args: [(obligation, None)])
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "malformed_proof")
        self.assertIn("future", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_clock_skew_does_not_manufacture_a_forged_timestamp(self):
        # GitHub issues the timestamp, the runner owns the clock. A few seconds
        # of NTP skew on a genuinely fresh event must not read as forgery — a
        # guard that cries wolf is one people stop reading.
        obligation = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW + timedelta(seconds=30)),
            "pull_number": 17,
            "head_sha": "just-pushed",
            "pull_state": "open",
        }
        findings = self._event_findings(lambda *args: [(obligation, None)])
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "pending")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_adapter_rejects_an_implausible_github_pull_timeline(self):
        # created_at newer than updated_at means the envelope this adapter
        # bounds author-controlled timestamps against is itself untrustworthy.
        payloads = [[{
            "number": 17,
            "state": "open",
            "created_at": "2026-07-18T09:00:00Z",
            "updated_at": "2026-07-17T09:00:00Z",
            "head": {"sha": "current-head"},
        }]]
        with patch.object(ef, "urlopen", self._json_urlopen(payloads, [])):
            with self.assertRaises(ef.AdapterError):
                ef.default_event_supply_runner(
                    "cross-model-review.yml", "pull_request",
                    "GuitarAlchemist/Demerzel", "secret",
                    ("opened", "synchronize"), SINCE,
                )

    # ── activation cutoff: no retroactive obligations (defect 3) ───────────

    def _cutoff_spec(self, cutoff, event="pull_request"):
        spec = json.loads(json.dumps(self.EVENT_SPEC))
        spec["reviewer.yml"]["activation"][event] = cutoff
        return spec

    def _cutoff_findings(self, cutoff, supply):
        self._event_repo()
        return self._evaluate(
            {"version": 1, "loops": []},
            event_producers=self._cutoff_spec(cutoff),
            event_supply_runner=supply,
            git_runner=lambda args, cwd: "",
        )

    def test_pre_cutover_head_is_explicitly_waived(self):
        # #935 flips the trigger to pull_request_target. Existing open heads
        # predate that flip and CANNOT have such a run — changing `on:` does not
        # replay opened/synchronize events. Demanding one manufactures an alarm
        # no producer could ever answer.
        stale_head = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=40)),
            "pull_number": 17,
            "head_sha": "pre-cutover-head",
            "pull_state": "open",
        }
        findings = self._cutoff_findings(
            _iso(NOW - timedelta(days=10)),
            lambda *args: [(stale_head, None)],
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertIn("waived", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 0)

    def test_post_cutover_absent_run_becomes_pending_then_stale(self):
        cutoff = _iso(NOW - timedelta(days=10))

        def head(age_days):
            return {
                "activities": ["opened", "synchronize"],
                "occurred_at": _iso(NOW - timedelta(days=age_days)),
                "pull_number": 17,
                "head_sha": "post-cutover-head",
                "pull_state": "open",
            }

        # Inside the 3d response allowance: pending, board stays green.
        pending = self._cutoff_findings(
            cutoff, lambda *args: [(head(1), None)])
        self.assertEqual(self._one(pending, "reviewer.yml")["kind"], "pending")
        self.assertEqual(ef.exit_code(pending), 0)

        # Past it: no run ever arrived for a head that really did dispatch.
        overdue = self._cutoff_findings(
            cutoff, lambda *args: [(head(4), None)])
        self.assertEqual(self._one(overdue, "reviewer.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(overdue), 1)

    def test_waiving_pre_cutover_heads_cannot_mask_a_post_cutover_one(self):
        cutoff = _iso(NOW - timedelta(days=10))
        waived = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=40)),
            "pull_number": 1,
            "head_sha": "pre-cutover-head",
            "pull_state": "closed",
        }
        overdue = {
            "activities": ["opened", "synchronize"],
            "occurred_at": _iso(NOW - timedelta(days=4)),
            "pull_number": 2,
            "head_sha": "post-cutover-head",
            "pull_state": "open",
        }
        findings = self._cutoff_findings(
            cutoff, lambda *args: [(waived, None), (overdue, None)])
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "silent_green")
        self.assertIn("#2", finding["detail"])
        self.assertIn("waived", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_active_event_without_an_activation_cutoff_is_config_error(self):
        # The shipped `pull_request_target` state until #935 merges: refuse to
        # judge rather than invent a boundary.
        findings = self._cutoff_findings(
            None, lambda *args: self.fail("must not call API"))
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "config_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_future_activation_cutoff_is_config_error(self):
        # A cutoff after `now` waives every obligation — a guard that reads
        # green because it is blind is the exact failure this repo exists for.
        findings = self._cutoff_findings(
            _iso(NOW + timedelta(days=1)),
            lambda *args: self.fail("must not call API"))
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"],
                         "config_error")
        self.assertEqual(ef.exit_code(findings), 2)

    # ── pull_request_target correlation must paginate (defect 4) ───────────

    def _target_run(self, run_id, number, head, created="2026-07-17T00:00:00Z"):
        return {
            "id": run_id,
            "status": "completed",
            "conclusion": "success",
            "created_at": created,
            "run_started_at": created,
            "head_sha": "base-head",
            "pull_requests": [{"number": number, "head": {"sha": head}}],
        }

    def test_correlated_target_run_on_page_two_is_found(self):
        # A single 100-run page is not the run history. With a busy repo the
        # valid run falls onto page 2 and the obligation reads "no run" — an
        # alarm indistinguishable from a genuinely dead loop.
        seen = []
        payloads = [
            [{
                "number": 17,
                "state": "open",
                "created_at": "2026-07-17T09:00:00Z",
                "updated_at": "2026-07-17T09:30:00Z",
                "head": {"sha": "pr-head"},
            }],
            {"workflow_runs": [
                self._target_run(i, 900 + i, f"other-head-{i}")
                for i in range(100)
            ]},
            {"workflow_runs": [self._target_run(7, 17, "pr-head")]},
        ]
        with patch.object(ef, "urlopen",
                          self._json_urlopen(payloads, seen)):
            supplies = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request_target",
                "GuitarAlchemist/Demerzel", "secret",
                ("opened", "synchronize"), SINCE,
            )
        _, run = supplies[0]
        self.assertIsNotNone(run, "a valid run on page 2 must not read as absent")
        self.assertEqual(run["id"], 7)
        self.assertEqual(
            parse_qs(urlparse(seen[2].full_url).query)["page"], ["2"])

    def test_incomplete_target_run_retrieval_is_adapter_error_not_absence(self):
        full_page = {"workflow_runs": [
            self._target_run(i, 900 + i, f"other-head-{i}") for i in range(100)
        ]}
        with patch.object(ef, "urlopen",
                          self._json_urlopen([full_page] * 200, [])):
            with self.assertRaises(ef.AdapterError):
                ef._collect_target_runs(
                    "GuitarAlchemist/Demerzel", "cross-model-review.yml",
                    "pull_request_target", "secret", SINCE,
                )

    def test_target_run_retrieval_stops_at_the_activation_cutoff(self):
        seen = []
        recent = {"workflow_runs": [
            self._target_run(i, 900 + i, f"h{i}") for i in range(100)
        ]}
        recent["workflow_runs"][-1]["created_at"] = "2023-06-01T00:00:00Z"
        with patch.object(ef, "urlopen",
                          self._json_urlopen([recent, recent], seen)):
            runs = ef._collect_target_runs(
                "GuitarAlchemist/Demerzel", "cross-model-review.yml",
                "pull_request_target", "secret", SINCE,
            )
        self.assertEqual(len(runs), 100)
        self.assertEqual(len(seen), 1, "retrieval must stop at the boundary")

    def test_malformed_target_run_page_is_adapter_error(self):
        with patch.object(ef, "urlopen",
                          self._json_urlopen([{"workflow_runs": "nope"}], [])):
            with self.assertRaises(ef.AdapterError):
                ef._collect_target_runs(
                    "GuitarAlchemist/Demerzel", "cross-model-review.yml",
                    "pull_request_target", "secret", SINCE,
                )

    def test_shipped_event_producers_match_live_workflow_yaml(self):
        # THE LIVE ORACLE for #844: cross-model-review.yml is on: pull_request,
        # carries no cron, and was therefore invisible to scheduled_workflows().
        workflows = Path(ef.REPO) / ef.DEFAULT_WORKFLOWS_DIR
        self.assertIn("cross-model-review.yml", ef.EVENT_PRODUCERS)
        scheduled = set(ef.scheduled_workflows(workflows))
        for wf, spec in ef.EVENT_PRODUCERS.items():
            events = ef.workflow_events(workflows, wf)
            self.assertIsNotNone(events, f"{wf} is declared but does not exist")
            active_events = set(spec["events"]) & events
            self.assertEqual(len(active_events), 1)
            active_event = next(iter(active_events))
            self.assertEqual(
                set(spec["activities"]),
                ef.workflow_event_activities(workflows, wf, active_event),
            )
            self.assertNotIn(wf, scheduled,
                             f"{wf} has a cron and belongs in the registry")
            self.assertGreater(spec["max_stale_days"], 0)

            # Every candidate event must have an activation decision on record —
            # an ISO instant, or an explicit None meaning "not activated yet".
            # A missing key is an undeclared cutoff, which is how retroactive
            # obligations get invented.
            activation = spec.get("activation")
            self.assertIsInstance(activation, dict, f"{wf} declares no activation")
            for candidate in spec["events"]:
                self.assertIn(candidate, activation,
                              f"{wf} has no activation decision for {candidate}")
                declared = activation[candidate]
                if declared is None:
                    continue
                self.assertIsNotNone(
                    ef._parse_iso(declared),
                    f"{wf}: activation cutoff for {candidate} is unparseable",
                )
            # The ACTIVE event must carry a usable cutoff; a None there is the
            # fail-closed state and must not reach production silently.
            self.assertIsNotNone(
                activation.get(active_event),
                f"{wf}: `{active_event}` is the live trigger but has no "
                "activation cutoff — see the #935 note on EVENT_PRODUCERS",
            )

    def test_shipped_pull_request_target_cutoff_is_explicitly_pending(self):
        """The #935 dependency, asserted rather than remembered.

        PR #935 migrates cross-model-review.yml to `pull_request_target`. Until
        it merges, the cutover instant does not exist, so the declaration holds
        None and _eval_event_producer refuses to judge that event. This test
        fails the moment someone flips the trigger without recording the instant,
        which is precisely when retroactive obligations would be invented.
        """
        spec = ef.EVENT_PRODUCERS["cross-model-review.yml"]
        live = ef.workflow_events(
            Path(ef.REPO) / ef.DEFAULT_WORKFLOWS_DIR, "cross-model-review.yml"
        )
        if "pull_request_target" in live:
            self.assertIsNotNone(
                spec["activation"]["pull_request_target"],
                "the trigger migrated but its activation instant was not recorded",
            )
        else:
            self.assertIsNone(spec["activation"]["pull_request_target"])

    def test_workflow_events_handles_every_on_shape(self):
        self.repo.write_event_workflow("mapping.yml", ["pull_request", "issues"])
        (self.repo.workflows / "seq.yml").write_text(
            "name: s\non: [push, pull_request]\njobs: {}\n", encoding="utf-8")
        (self.repo.workflows / "scalar.yml").write_text(
            "name: s\non: push\njobs: {}\n", encoding="utf-8")
        self.assertEqual(ef.workflow_events(self.repo.workflows, "mapping.yml"),
                         {"pull_request", "issues"})
        self.assertEqual(ef.workflow_events(self.repo.workflows, "seq.yml"),
                         {"push", "pull_request"})
        self.assertEqual(ef.workflow_events(self.repo.workflows, "scalar.yml"),
                         {"push"})
        self.assertIsNone(ef.workflow_events(self.repo.workflows, "gone.yml"))

    # ── registry activation must match actual workflow YAML ───────────────

    def test_active_schedule_mismatch_turns_red_before_adapter(self):
        self.repo.write_workflow("producer.yml", crons=["0 1 * * *"])
        registry = self._workflow_run_registry()
        registry["loops"][0]["schedule"] = ["0 2 * * *"]
        findings = self._evaluate(
            registry, actions_runner=lambda *args: self.fail("must not call API"),
            auto_workflows=False,
        )
        self.assertEqual(self._one(findings, "producer.yml")["kind"],
                         "activation_mismatch")

    def test_disabled_but_still_scheduled_turns_red(self):
        self.repo.write_workflow("seldon-plan.yml", crons=["0 6 * * *"])
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "seldon-plan.yml",
                "status": "disabled",
                "disabled": {
                    "reason": "paused",
                    "until": "2026-10-16",
                    "verification": "schedule_absent",
                },
            }],
        }
        findings = self._evaluate(registry, auto_workflows=False)
        self.assertEqual(self._one(findings, "seldon-plan.yml")["kind"],
                         "activation_mismatch")

    def test_monitor_exclusion_is_constrained(self):
        self.repo.write_workflow("producer.yml")
        findings = self._evaluate({
            "version": 1, "monitors": ["producer.yml"], "loops": [],
        })
        self.assertEqual(self._one(findings, "producer.yml")["kind"],
                         "config_error")

    def test_monitor_cannot_also_be_registered_as_producer(self):
        self.repo.write_workflow("ecosystem-freshness.yml")
        findings = self._evaluate({
            "version": 1,
            "monitors": ["ecosystem-freshness.yml"],
            "loops": [{
                "workflow": "ecosystem-freshness.yml",
                "status": "active",
                "schedule": ["0 0 * * *"],
                "proof": {"adapter": "workflow_run", "max_stale_days": 1},
            }],
        })
        self.assertTrue(any(
            f["kind"] == "config_error" and "both" in f["detail"]
            for f in findings
        ))

    # ── deterministic ordering ────────────────────────────────────────────

    def test_deterministic_ordering(self):
        proof = {"adapter": "workflow_run", "max_stale_days": 2}
        registry = {
            "version": 1,
            "loops": [
                {"workflow": "z.yml", "status": "active",
                 "proof": proof},
                {"workflow": "a.yml", "status": "active",
                 "proof": proof},
                {"workflow": "m.yml", "status": "active",
                 "proof": proof},
            ],
        }
        good = lambda *args: {
            "conclusion": "success", "run_started_at": _iso(NOW),
            "html_url": "https://example.test/run",
        }
        order1 = [f["workflow"] for f in self._evaluate(
            registry, actions_runner=good)]
        order2 = [f["workflow"] for f in self._evaluate(
            registry, actions_runner=good)]
        self.assertEqual(order1, ["a.yml", "m.yml", "z.yml"])
        self.assertEqual(order1, order2)

    # ── coverage: monitor self-exclusion & unregistered producers ─────────

    def test_monitor_self_exclusion(self):
        # A scheduled monitor on disk must NOT be reported as unregistered.
        self.repo.write_workflow("ecosystem-freshness.yml")
        registry = {
            "version": 1,
            "monitors": ["ecosystem-freshness.yml"],
            "loops": [],
        }
        findings = self._evaluate(registry)
        self.assertEqual(findings, [])
        self.assertEqual(ef.exit_code(findings), 0)

    def test_unregistered_scheduled_producer_turns_red(self):
        self.repo.write_workflow("brand-new-loop.yml")
        registry = {"version": 1, "monitors": [], "loops": []}
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "brand-new-loop.yml")["kind"],
                         "unregistered")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_registered_producer_not_flagged(self):
        self.repo.write_workflow("known.yml")
        registry = {
            "version": 1,
            "loops": [{"workflow": "known.yml", "status": "active",
                       "schedule": ["0 0 * * *"],
                       "proof": {"adapter": "workflow_run",
                                 "max_stale_days": 1}}],
        }
        findings = self._evaluate(registry, actions_runner=lambda *args: {
            "conclusion": "success", "run_started_at": _iso(NOW),
        })
        self.assertEqual(self._one(findings, "known.yml")["kind"], "healthy")
        self.assertEqual(ef.exit_code(findings), 0)

    # ── malformed proof (exit 1) vs config error (exit 2) ─────────────────

    def test_malformed_proof_unparseable_file(self):
        self.repo.write_state("state/q/x.jsonl", "this is not json at all\n")
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "q.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/q/*.jsonl",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 3,
                },
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "q.yml")["kind"], "malformed_proof")
        self.assertEqual(ef.exit_code(findings), 1)

    def test_malformed_proof_missing_timestamp_field(self):
        self.repo.write_state("state/q/x.jsonl",
                              json.dumps({"other": "value"}) + "\n")
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "q.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/q/*.jsonl",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 3,
                },
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "q.yml")["kind"], "malformed_proof")

    def test_state_glob_supports_json_object_and_array(self):
        # Whole-file JSON object.
        self.repo.write_state(
            "state/obj/x.json",
            json.dumps({"timestamp": _iso(NOW - timedelta(hours=1))}),
        )
        # Whole-file JSON array.
        self.repo.write_state(
            "state/obj/y.json",
            json.dumps([{"timestamp": _iso(NOW - timedelta(hours=2))}]),
        )
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "obj.yml",
                "status": "active",
                "proof": {
                    "adapter": "state_glob",
                    "glob": "state/obj/*.json",
                    "timestamp_field": "timestamp",
                    "max_stale_days": 1,
                },
            }],
        }
        self.assertEqual(self._one(self._evaluate(registry), "obj.yml")["kind"],
                         "healthy")

    # ── declaration integrity (config errors -> exit 2) ───────────────────

    def test_multiple_declarations_is_config_error(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "bad.yml",
                "status": "active",
                "proof": {"adapter": "state_glob", "glob": "state/x/*.json",
                          "timestamp_field": "timestamp", "max_stale_days": 1},
                "disabled": {"reason": "also paused", "until": "2026-10-16",
                             "verification": "schedule_absent"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "bad.yml")["kind"], "config_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_unbounded_allowed_silence_is_rejected(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "bad.yml",
                "status": "active",
                "allowed_silence": True,
                "reason": "external output is not evidence",
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "bad.yml")["kind"], "config_error")

    def test_disabled_block_with_active_status_is_config_error(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "bad.yml",
                "status": "active",
                "disabled": {"reason": "paused", "until": "2026-10-16",
                             "verification": "schedule_absent"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "bad.yml")["kind"], "config_error")

    def test_duplicate_registry_entry_is_config_error(self):
        proof = {"adapter": "state_glob", "glob": "state/x/*.json",
                 "timestamp_field": "timestamp", "max_stale_days": 1}
        registry = {
            "version": 1,
            "loops": [
                {"workflow": "dup.yml", "status": "active",
                 "proof": proof},
                {"workflow": "dup.yml", "status": "active",
                 "proof": proof},
            ],
        }
        findings = self._evaluate(registry)
        self.assertTrue(any(f["kind"] == "config_error" for f in findings))
        self.assertEqual(ef.exit_code(findings), 2)

    # ── stable alert payload (idempotent commits) ─────────────────────────

    def test_stable_alert_strips_volatile_fields(self):
        findings = [
            {"workflow": "b.yml", "kind": "stale", "detail": "17.3d old"},
            {"workflow": "a.yml", "kind": "healthy", "detail": "fresh 0.1d"},
            {"workflow": "c.yml", "kind": "silent_green", "detail": "no evidence"},
        ]
        alert = ef.stable_alert(findings)
        self.assertEqual(alert, [
            {"workflow": "b.yml", "kind": "stale"},
            {"workflow": "c.yml", "kind": "silent_green"},
        ])
        # No ages/timestamps leak into the committable payload.
        self.assertNotIn("detail", alert[0])

    def test_fail_persist_idempotence_and_recovery(self):
        alert_path = self.repo.root / "state/loop-health/.freshness-alert.json"
        failed = [{
            "workflow": "dead.yml", "kind": "failed_run", "detail": "run 1",
        }]
        ef.sync_alert(alert_path, failed)
        first = alert_path.read_text(encoding="utf-8")
        ef.sync_alert(alert_path, [{
            "workflow": "dead.yml", "kind": "failed_run", "detail": "run 2",
        }])
        self.assertEqual(alert_path.read_text(encoding="utf-8"), first)
        ef.sync_alert(alert_path, [{
            "workflow": "dead.yml", "kind": "healthy", "detail": "recovered",
        }])
        self.assertFalse(alert_path.exists())

    # ── registry schema validation (config failure -> exit 2) ─────────────

    def test_load_registry_rejects_bad_adapter(self):
        reg = self.repo.root / "loop-health.yml"
        reg.write_text(
            "version: 1\n"
            "loops:\n"
            "  - workflow: x.yml\n"
            "    status: active\n"
            "    proof:\n"
            "      adapter: not_a_real_adapter\n"
            "      max_stale_days: 3\n",
            encoding="utf-8",
        )
        schema = Path(ef.REPO) / ef.DEFAULT_SCHEMA
        with self.assertRaises(ef.ConfigError):
            ef.load_registry(reg, schema)

    def test_load_registry_missing_file(self):
        with self.assertRaises(ef.ConfigError):
            ef.load_registry(self.repo.root / "nope.yml",
                             Path(ef.REPO) / ef.DEFAULT_SCHEMA)

    # ── the shipped production registry is internally consistent ──────────

    def test_shipped_registry_validates_and_covers_producers(self):
        repo = Path(ef.REPO)
        registry = ef.load_registry(
            repo / ef.DEFAULT_REGISTRY, repo / ef.DEFAULT_SCHEMA
        )
        # The shipped activation cutoff is a real forward-moving instant, so this
        # consistency check evaluates just after it rather than at the fixed NOW
        # the behavioural tests share. Derived, not hardcoded, so it cannot rot.
        declared = [
            ef._parse_iso(value)
            for spec in ef.EVENT_PRODUCERS.values()
            for value in (spec.get("activation") or {}).values()
            if isinstance(value, str)
        ]
        now = max([NOW, *(dt + timedelta(days=1) for dt in declared if dt)])
        findings = ef.evaluate(
            registry,
            now=now,
            workflows_dir=repo / ef.DEFAULT_WORKFLOWS_DIR,
            repo_root=repo,
            git_runner=lambda args, cwd: _iso(now) + "\n",
            actions_runner=lambda *args: {
                "conclusion": "success",
                "run_started_at": _iso(now),
                "html_url": "https://example.test/production-proof",
            },
            event_supply_runner=lambda *args: [({
                "activities": ["opened", "synchronize"],
                "occurred_at": _iso(now),
                "pull_number": 939,
                "head_sha": "production-head",
                "pull_state": "open",
            }, {
                "status": "completed",
                "conclusion": "success",
                "run_started_at": _iso(now),
                "html_url": "https://example.test/production-event-proof",
                "head_sha": "production-head",
                "pull_requests": [{"number": 939}],
            })],
            repository="GuitarAlchemist/Demerzel",
            token="test-token",
        )
        # The event-triggered producers really are evaluated in production.
        self.assertEqual(
            {f["workflow"] for f in findings} & set(ef.EVENT_PRODUCERS),
            set(ef.EVENT_PRODUCERS),
            "every declared event-triggered producer must yield a finding",
        )
        # No unregistered producers and no config/adapter errors: coverage is
        # complete and the registry is internally consistent.
        self.assertFalse([f for f in findings if f["kind"] == "unregistered"],
                         "every scheduled producer must be registered")
        self.assertFalse([f for f in findings
                          if f["kind"] in ("config_error", "adapter_error")])
        self.assertNotIn("allowed_silence", json.dumps(registry))
        scheduled = set(ef.scheduled_workflows(
            repo / ef.DEFAULT_WORKFLOWS_DIR
        ))
        active_loops = {
            loop["workflow"] for loop in registry["loops"]
            if loop.get("status") == "active"
        }
        disabled_loops = {
            loop["workflow"] for loop in registry["loops"]
            if loop.get("status") == "disabled"
        }
        self.assertEqual(
            scheduled,
            set(registry["monitors"]) |
            active_loops,
        )
        self.assertTrue(disabled_loops)
        self.assertTrue(disabled_loops.isdisjoint(scheduled))

    def test_production_workflows_enforce_daily_always_and_ci_paths(self):
        repo = Path(ef.REPO)
        guard = yaml.safe_load((
            repo / ".github/workflows/ecosystem-freshness.yml"
        ).read_text(encoding="utf-8"))
        on = guard.get("on") or guard.get(True)
        self.assertEqual(on["schedule"], [{"cron": "15 13 * * *"}])
        self.assertEqual(guard["jobs"]["persist"]["if"], "always()")
        persist_steps = guard["jobs"]["persist"]["steps"]
        self.assertTrue(any(step.get("if") == "always()" for step in persist_steps))
        self.assertEqual(guard["jobs"]["evaluate"]["permissions"], {
            "actions": "read", "contents": "read", "pull-requests": "read",
        })
        self.assertEqual(guard["jobs"]["persist"]["permissions"], {
            "contents": "write",
        })

        ci_text = (repo / ".github/workflows/governance-validate.yml").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(ci_text.count(".github/loop-health.yml"), 2)
        self.assertGreaterEqual(ci_text.count(".github/workflows/*.yml"), 2)


if __name__ == "__main__":
    unittest.main()
