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

    def write_workflow(self, name: str) -> None:
        (self.workflows / name).write_text(
            "name: stub\n"
            "on:\n"
            "  schedule:\n"
            "    - cron: '0 0 * * *'\n"
            "jobs: {}\n",
            encoding="utf-8",
        )


class EcosystemFreshnessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = _Repo()
        self.addCleanup(self.repo.close)

    def _evaluate(self, registry: dict, *, git_runner=None) -> list[dict]:
        kwargs = {}
        if git_runner is not None:
            kwargs["git_runner"] = git_runner
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
                "disabled": {"reason": "paused", "until": "2026-10-16"},
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
                "disabled": {"reason": "paused", "until": "2026-07-17"},
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
                "disabled": {"reason": "paused", "until": _iso(NOW)[:10]},
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

    # ── deterministic ordering ────────────────────────────────────────────

    def test_deterministic_ordering(self):
        registry = {
            "version": 1,
            "loops": [
                {"workflow": "z.yml", "status": "active",
                 "allowed_silence": True, "reason": "external"},
                {"workflow": "a.yml", "status": "active",
                 "allowed_silence": True, "reason": "external"},
                {"workflow": "m.yml", "status": "active",
                 "allowed_silence": True, "reason": "external"},
            ],
        }
        order1 = [f["workflow"] for f in self._evaluate(registry)]
        order2 = [f["workflow"] for f in self._evaluate(registry)]
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
                       "allowed_silence": True, "reason": "external"}],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "known.yml")["kind"], "allowed_silence")
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
                "allowed_silence": True,
                "reason": "external",
                "proof": {"adapter": "state_glob", "glob": "state/x/*.json",
                          "timestamp_field": "timestamp", "max_stale_days": 1},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "bad.yml")["kind"], "config_error")
        self.assertEqual(ef.exit_code(findings), 2)

    def test_allowed_silence_requires_reason(self):
        registry = {
            "version": 1,
            "loops": [{
                "workflow": "bad.yml",
                "status": "active",
                "allowed_silence": True,
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
                "disabled": {"reason": "paused", "until": "2026-10-16"},
            }],
        }
        findings = self._evaluate(registry)
        self.assertEqual(self._one(findings, "bad.yml")["kind"], "config_error")

    def test_duplicate_registry_entry_is_config_error(self):
        registry = {
            "version": 1,
            "loops": [
                {"workflow": "dup.yml", "status": "active",
                 "allowed_silence": True, "reason": "external"},
                {"workflow": "dup.yml", "status": "active",
                 "allowed_silence": True, "reason": "external"},
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
        )
        # No unregistered producers and no config/adapter errors: coverage is
        # complete and the registry is internally consistent.
        self.assertFalse([f for f in findings if f["kind"] == "unregistered"],
                         "every scheduled producer must be registered")
        self.assertFalse([f for f in findings
                          if f["kind"] in ("config_error", "adapter_error")])


if __name__ == "__main__":
    unittest.main()
