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

    def write_event_workflow(self, name: str, events: list[str]) -> None:
        """A workflow with only event triggers — no cron at all (#844)."""
        (self.workflows / name).write_text(
            "name: stub\n"
            "on:\n"
            + "".join(f"  {event}:\n" for event in events)
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

    EVENT_SPEC = {"reviewer.yml": {"event": "pull_request", "max_stale_days": 3}}

    def _event_repo(self, events=("pull_request",)):
        self.repo.write_event_workflow("reviewer.yml", list(events))

    def _supply(self, event_age_days=None, run_age_days=None,
                conclusion="success"):
        """Stub the (newest event, latest completed run) seam."""
        event_iso = (
            None if event_age_days is None
            else _iso(NOW - timedelta(days=event_age_days))
        )
        run = None if run_age_days is None else {
            "conclusion": conclusion,
            "run_started_at": _iso(NOW - timedelta(days=run_age_days)),
            "html_url": "https://example.test/pr-run",
        }
        return lambda *args: (event_iso, run)

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
            self._supply(event_age_days=0.5, run_age_days=9)
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "stale")
        self.assertIn("9.0d old", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 1)

    def test_event_loop_quiet_with_no_event_supply_stays_silent(self):
        # THE OTHER DIRECTION: no PR in the window, so no run was owed. A repo
        # with a quiet week must not turn the board red — that is the cry-wolf
        # failure that trains people to ignore the guard.
        findings = self._event_findings(
            self._supply(event_age_days=30, run_age_days=30)
        )
        finding = self._one(findings, "reviewer.yml")
        self.assertEqual(finding["kind"], "healthy")
        self.assertIn("quiet", finding["detail"])
        self.assertEqual(ef.exit_code(findings), 0)

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

    def test_event_loop_with_live_supply_and_no_run_ever_is_red(self):
        findings = self._event_findings(
            self._supply(event_age_days=1, run_age_days=None)
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"],
                         "silent_green")
        self.assertEqual(ef.exit_code(findings), 1)

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
            self._supply(event_age_days=1, run_age_days=None),
            git_runner=lambda args, cwd: _iso(NOW - timedelta(days=0.5)) + "\n",
        )
        self.assertEqual(self._one(findings, "reviewer.yml")["kind"], "newborn")
        self.assertEqual(ef.exit_code(findings), 0)

    def test_event_loop_past_newborn_grace_still_fires(self):
        findings = self._event_findings(
            self._supply(event_age_days=1, run_age_days=None),
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
            [{"created_at": "2026-07-18T09:00:00Z"}],
            {"workflow_runs": [{"id": 7, "conclusion": "success"}]},
        ]

        def fake_urlopen(request, timeout):
            seen.append(request)
            return Response(payloads[len(seen) - 1])

        with patch.object(ef, "urlopen", fake_urlopen):
            event_iso, run = ef.default_event_supply_runner(
                "cross-model-review.yml", "pull_request",
                "GuitarAlchemist/Demerzel", "secret",
            )
        self.assertEqual(event_iso, "2026-07-18T09:00:00Z")
        self.assertEqual(run, {"id": 7, "conclusion": "success"})

        pulls_q = parse_qs(urlparse(seen[0].full_url).query)
        self.assertEqual(pulls_q, {
            "state": ["all"], "sort": ["created"],
            "direction": ["desc"], "per_page": ["1"],
        })
        runs_q = parse_qs(urlparse(seen[1].full_url).query)
        self.assertEqual(runs_q, {
            "event": ["pull_request"], "status": ["completed"], "per_page": ["1"],
        })
        # A pull_request run lives on the PR head branch, so a default-branch
        # filter would find nothing and read every healthy loop as dead.
        self.assertNotIn("branch", runs_q)
        for request in seen:
            self.assertNotIn("secret", request.full_url)
            self.assertEqual(request.get_header("Authorization"), "Bearer secret")

    def test_event_supply_adapter_requires_repository_and_token(self):
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "pull_request", "", "t")
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "pull_request", "o/r", "")
        with self.assertRaises(ef.AdapterError):
            ef.default_event_supply_runner("w.yml", "issues", "o/r", "t")

    def test_shipped_event_producers_match_live_workflow_yaml(self):
        # THE LIVE ORACLE for #844: cross-model-review.yml is on: pull_request,
        # carries no cron, and was therefore invisible to scheduled_workflows().
        workflows = Path(ef.REPO) / ef.DEFAULT_WORKFLOWS_DIR
        self.assertIn("cross-model-review.yml", ef.EVENT_PRODUCERS)
        scheduled = set(ef.scheduled_workflows(workflows))
        for wf, spec in ef.EVENT_PRODUCERS.items():
            events = ef.workflow_events(workflows, wf)
            self.assertIsNotNone(events, f"{wf} is declared but does not exist")
            self.assertIn(spec["event"], events)
            self.assertNotIn(wf, scheduled,
                             f"{wf} has a cron and belongs in the registry")
            self.assertGreater(spec["max_stale_days"], 0)

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
        findings = ef.evaluate(
            registry,
            now=NOW,
            workflows_dir=repo / ef.DEFAULT_WORKFLOWS_DIR,
            repo_root=repo,
            git_runner=lambda args, cwd: _iso(NOW) + "\n",
            actions_runner=lambda *args: {
                "conclusion": "success",
                "run_started_at": _iso(NOW),
                "html_url": "https://example.test/production-proof",
            },
            event_supply_runner=lambda *args: (_iso(NOW), {
                "conclusion": "success",
                "run_started_at": _iso(NOW),
                "html_url": "https://example.test/production-event-proof",
            }),
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
            "actions": "read", "contents": "read",
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
