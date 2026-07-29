import json
import os
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_afk_cycle as g
from afk_backends.claude_code import ClaudeCodeBackend, _claude_code_prompt
from afk_backends.remote import RemoteBackend
from afk_backends.sandcastle import SandcastleBackend


class TestClassifyRisk(unittest.TestCase):
    def test_constitution_is_critical(self):
        issue = {"title": "Update Asimov constitution Article 4",
                 "body": "edit constitutions/asimov.constitution.md",
                 "labels": [{"name": "agent-implement"}]}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "critical")
        self.assertEqual(mode, "per-iteration")

    def test_policy_is_critical(self):
        issue = {"title": "Refine alignment policy", "body": "tweak policies/alignment-policy.yaml",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "critical")

    def test_schema_migration_is_high(self):
        issue = {"title": "Schema migration for personas", "body": "migrate schema",
                 "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "high")
        self.assertEqual(mode, "per-iteration")

    def test_persona_is_medium(self):
        issue = {"title": "Update skeptical-auditor persona voice", "body": "persona tweak",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "medium")

    def test_docs_is_low(self):
        issue = {"title": "Fix typo in README", "body": "documentation typo", "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "low")
        self.assertEqual(mode, "boundary-only")


class TestEligibility(unittest.TestCase):
    def test_critical_not_eligible(self):
        self.assertFalse(g.is_eligible({"title": "edit constitutions/x", "body": "", "labels": []}))

    def test_low_eligible(self):
        self.assertTrue(g.is_eligible({"title": "fix docs typo", "body": "", "labels": []}))


class TestLoopState(unittest.TestCase):
    def test_loop_id_pattern_and_required_fields(self):
        issue = {"number": 42, "title": "Fix docs typo", "body": "x", "labels": []}
        st = g.build_loop_state(issue, seq=1, risk="low", mode="boundary-only", today="2026-06-22")
        self.assertRegex(st["loop_id"], r"^loop-\d{4}-\d{2}-\d{2}-\d{3}$")
        for key in ("loop_id", "goal", "repo", "risk", "governance_mode", "status", "iterations"):
            self.assertIn(key, st)
        self.assertEqual(st["repo"], "demerzel")
        self.assertIn("#42", st["goal"])


class TestDryRunNoLiveCalls(unittest.TestCase):
    def test_dry_run_makes_no_live_calls(self):
        with mock.patch.object(g, "_gh_queue", return_value=[
                 {"number": 7, "title": "fix docs typo", "body": "x", "labels": []}]), \
             mock.patch.object(g, "_process_issue") as proc, \
             mock.patch.object(g, "get_backend") as get_backend, \
             mock.patch.object(g, "_write_audit") as audit:
            rc = g.main(["--dry-run"])
        self.assertEqual(rc, 0)
        proc.assert_not_called()         # no clone / sandbox / push / PR
        get_backend.assert_not_called()  # backend not selected in dry-run mode
        audit.assert_not_called()        # dry-run writes nothing


class TestParallelDispatch(unittest.TestCase):
    def test_live_processes_every_issue_once(self):
        issues = [{"number": n, "title": f"fix docs typo {n}", "body": "x", "labels": []}
                  for n in (1, 2, 3)]
        fake_adapter = mock.Mock()
        fake_adapter.prepare.return_value = (True, "ok")
        fake_adapter.needs_local_repo.return_value = True
        with mock.patch.object(g, "_gh_queue", return_value=issues), \
             mock.patch.object(g, "get_backend", return_value=fake_adapter), \
             mock.patch.object(g, "_process_issue",
                               side_effect=lambda issue, seq, today, backend, adapter:
                                   ({"issue": issue["number"], "action": "implement"}, {})) as proc, \
             mock.patch.object(g, "_write_audit") as audit:
            rc = g.main(["--max-parallel", "2"])
        self.assertEqual(rc, 0)
        self.assertEqual(proc.call_count, 3)            # whole queue processed, not capped at 2
        self.assertEqual(audit.call_count, 1)           # one combined audit written


class TestBackend(unittest.TestCase):
    def test_remote_backend_is_blocked_stub(self):
        hr = RemoteBackend().invoke({"number": 1, "title": "x", "body": "y"}, None)
        self.assertIsNone(hr["branch"])
        self.assertIn("remote", hr["blocked"].lower())


class TestArgValidation(unittest.TestCase):
    def test_zero_parallel_rejected(self):
        with mock.patch.object(g, "_gh_queue", return_value=[]):
            rc = g.main(["--max-parallel", "0"])
        self.assertEqual(rc, 1)


def _council(verdict="APPROVE", conf=0.75, n_reviews=2, aligned=True):
    reviews = []
    align = "pass" if aligned else "fail"
    for i in range(n_reviews):
        reviews.append({"reviewer": f"reviewer_{'ab'[i % 2]}", "correctness_score": conf,
                        "risk_assessment": "low", "constitutional_alignment": align,
                        "rationale": "x"})
    return {"verdict": verdict, "post_council_confidence": conf, "reviews": reviews}


class TestAuthorizationTrace(unittest.TestCase):
    def test_closes(self):
        self.assertEqual(g.parse_authorization_trace("Implements #381 via AFK.\nCloses #381"),
                         "github_issue:#381")

    def test_implements_lowercase(self):
        self.assertEqual(g.parse_authorization_trace("implements #42"), "github_issue:#42")

    def test_none_when_absent(self):
        self.assertIsNone(g.parse_authorization_trace("no linkage here"))
        self.assertIsNone(g.parse_authorization_trace(""))


class TestSelfMergeDecision(unittest.TestCase):
    OK = dict(risk="low", checks_green=True, authz_trace="github_issue:#1",
              conscience_max_weight=0.0)

    def _decide(self, **over):
        kw = dict(self.OK); kw.update(over)
        cv = kw.pop("council_verdict", _council())
        return g.self_merge_decision(kw["risk"], kw["checks_green"], kw["authz_trace"],
                                     kw["conscience_max_weight"], cv)

    def test_happy_path_merges(self):
        merge, reason = self._decide()
        self.assertTrue(merge, reason)

    def test_medium_also_ok(self):
        self.assertTrue(self._decide(risk="medium")[0])

    def test_high_never(self):
        merge, reason = self._decide(risk="high")
        self.assertFalse(merge)
        self.assertIn("only low/medium", reason)

    def test_critical_never(self):
        self.assertFalse(self._decide(risk="critical")[0])

    def test_ci_red_blocks(self):
        self.assertFalse(self._decide(checks_green=False)[0])

    def test_missing_authz_blocks(self):
        self.assertFalse(self._decide(authz_trace=None)[0])

    def test_conscience_block(self):
        merge, reason = self._decide(conscience_max_weight=0.85)
        self.assertFalse(merge)
        self.assertIn("conscience", reason)

    def test_conscience_below_threshold_ok(self):
        self.assertTrue(self._decide(conscience_max_weight=0.79)[0])

    def test_single_reviewer_blocks(self):
        merge, reason = self._decide(council_verdict=_council(n_reviews=1))
        self.assertFalse(merge)
        self.assertIn("need 2", reason)

    def test_request_changes_verdict_blocks(self):
        self.assertFalse(self._decide(council_verdict=_council(verdict="REQUEST_CHANGES"))[0])

    def test_low_confidence_blocks(self):
        self.assertFalse(self._decide(council_verdict=_council(conf=0.65))[0])

    def test_constitutional_fail_blocks(self):
        self.assertFalse(self._decide(council_verdict=_council(aligned=False))[0])

    def test_no_council_blocks(self):
        self.assertFalse(self._decide(council_verdict=None)[0])


class TestOpenPrLabelsForHarvest(unittest.TestCase):
    def test_open_pr_applies_agent_implement_label(self):
        """The implement lane must label the PR so the harvest lane finds it."""
        calls = []

        def fake_run(cmd, *a, **k):
            calls.append(cmd)
            return mock.Mock(returncode=0, stdout="https://github.com/x/y/pull/1", stderr="")

        with mock.patch.object(g.subprocess, "run", side_effect=fake_run):
            url = g._open_pr({"number": 42, "title": "fix typo"}, "agent/issue-42", "/tmp/clone")
        self.assertTrue(url.endswith("/pull/1"))
        create = next(c for c in calls if "pr" in c and "create" in c)
        self.assertIn("--label", create)
        self.assertEqual(create[create.index("--label") + 1], g.LABEL)


class TestHarvestDryRun(unittest.TestCase):
    def test_dry_run_no_council_no_merge(self):
        prs = [{"number": 9, "title": "fix docs typo", "body": "Closes #9", "labels": []}]
        with mock.patch.object(g, "_gh_open_afk_prs", return_value=prs), \
             mock.patch.object(g, "active_conscience_max_weight", return_value=0.0), \
             mock.patch.object(g.council_emit, "convene") as convene, \
             mock.patch.object(g, "_merge_pr") as merge:
            rc = g.main(["--harvest", "--dry-run"])
        self.assertEqual(rc, 0)
        convene.assert_not_called()   # dry-run convenes no council
        merge.assert_not_called()     # and merges nothing


class TestLoopStateWriteSeam(unittest.TestCase):
    """The loop-state write now goes through kit.write_artifact, which validates
    against schemas/loop-state.schema.json before atomic-writing — so an invalid
    state never lands on disk (it had no validation before this migration)."""

    def test_write_loop_state_validates_and_writes(self):
        issue = {"number": 42, "title": "Fix docs typo", "body": "x", "labels": []}
        st = g.build_loop_state(issue, seq=1, risk="low", mode="boundary-only",
                                today="2026-06-25")
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(g, "ROOT", Path(d)):
            g._write_loop_state(st)
            written = Path(d) / "state" / "loops" / f"{st['loop_id']}.loop.json"
            self.assertTrue(written.exists(), "loop-state must be written to disk")
            on_disk = json.loads(written.read_text(encoding="utf-8"))
            self.assertEqual(on_disk["loop_id"], st["loop_id"])
            try:
                import jsonschema
            except ImportError:
                self.skipTest("jsonschema not installed")
            schema_path = (Path(g.__file__).resolve().parents[1] / "schemas"
                           / "loop-state.schema.json")
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(on_disk, schema)  # write_artifact already did; double-check


class TestHarvestSeam(unittest.TestCase):
    """End-to-end through the demerzel_kit seam: a live --harvest pass with the gh
    reads (gh_json/gh_text) injected, proving the harvest path gates a PR and writes
    its audit to disk without touching the network. This is the test the un-seamed
    gh calls made impossible before the kit migration."""

    def _fake_gh_json(self, args, **kwargs):
        if args[:2] == ["pr", "list"]:
            return [{"number": 9, "title": "fix docs typo", "body": "Closes #9",
                     "labels": []}]
        return None

    def _fake_gh_text(self, args, **kwargs):
        if args[:2] == ["pr", "checks"]:
            return "ci\tpass\thttps://example/checks"
        return ""

    def test_harvest_self_merges_and_writes_audit(self):
        verdict = _council(verdict="APPROVE", conf=0.75, n_reviews=2)
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(g.kit, "gh_json", self._fake_gh_json), \
             mock.patch.object(g.kit, "gh_text", self._fake_gh_text), \
             mock.patch.object(g, "active_conscience_max_weight", return_value=0.0), \
             mock.patch.object(g.council_emit, "convene", return_value=verdict), \
             mock.patch.object(g, "_merge_pr", return_value="merged") as merge, \
             mock.patch.object(g, "ROOT", Path(d)):
            rc = g.main(["--harvest"])
            self.assertEqual(rc, 0)
            merge.assert_called_once_with(9)
            audit = Path(d) / "state" / "oversight"
            files = list(audit.glob("afk-harvest-*.json"))
            self.assertEqual(len(files), 1, "one harvest audit must be written")
            summary = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(summary["tally"]["self_merge"], 1)
        self.assertEqual(summary["decisions"][0]["action"], "self-merge")
        self.assertEqual(summary["decisions"][0]["merge_result"], "merged")


class TestClaudeCodeBackend(unittest.TestCase):
    """The --backend claude-code seam: delegate an issue to headless `claude -p`
    instead of a Podman sandbox, returning the same {branch,commits,blocked}."""

    def test_prompt_carries_issue_and_commit_contract(self):
        p = _claude_code_prompt({"number": 410, "title": "Migrate X onto kit", "body": "do the thing"})
        self.assertIn("#410", p)
        self.assertIn("Migrate X onto kit", p)
        self.assertIn("do the thing", p)
        self.assertIn("COMMIT", p)
        self.assertIn("unittest discover", p)
        self.assertIn("do not open a pull request", p.lower())

    def _fake_run(self, log_out):
        """A subprocess.run stand-in for the backend's git+claude calls."""
        def run(cmd, **kw):
            ns = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if "rev-parse" in cmd:
                ns.stdout = "BASE_SHA"
            elif "status" in cmd:
                ns.stdout = ""            # clean working tree after the agent
            elif cmd[:4] == ["git", "-C", cmd[2], "log"] or "log" in cmd:
                ns.stdout = log_out
            return ns
        return run

    def test_no_commits_returns_blocked(self):
        with mock.patch.object(g.subprocess, "run", side_effect=self._fake_run("")):
            out = ClaudeCodeBackend().invoke({"number": 410, "title": "t", "body": "b"}, "/tmp/x")
        self.assertIsNone(out["branch"])
        self.assertIn("no commits", out["blocked"])

    def test_commits_return_branch(self):
        with mock.patch.object(g.subprocess, "run", side_effect=self._fake_run("feat: migrate\n")):
            out = ClaudeCodeBackend().invoke({"number": 410, "title": "t", "body": "b"}, "/tmp/x")
        self.assertEqual(out["branch"], "agent/issue-410")
        self.assertEqual(out["commits"], ["feat: migrate"])
        self.assertIsNone(out["blocked"])

    def test_api_key_stripped_from_child_env(self):
        seen = {}
        def run(cmd, **kw):
            ns = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if cmd[0] == "claude":
                seen["env"] = kw.get("env", {})
            if "rev-parse" in cmd:
                ns.stdout = "BASE"
            elif "log" in cmd:
                ns.stdout = "feat: x\n"
            return ns
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-should-be-stripped"}), \
             mock.patch.object(g.subprocess, "run", side_effect=run):
            ClaudeCodeBackend().invoke({"number": 1, "title": "t", "body": "b"}, "/tmp/x")
        self.assertNotIn("ANTHROPIC_API_KEY", seen["env"],
                         "claude must run on the subscription, not the capped API key")

    def test_uses_scoped_allowlist_not_skip_permissions(self):
        seen = {}
        def run(cmd, **kw):
            ns = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if cmd and cmd[0] == "claude":
                seen["cmd"] = cmd
            if "rev-parse" in cmd:
                ns.stdout = "BASE"
            elif "log" in cmd:
                ns.stdout = "feat: x\n"
            return ns
        with mock.patch.object(g.subprocess, "run", side_effect=run):
            ClaudeCodeBackend().invoke({"number": 1, "title": "t", "body": "b"}, "/tmp/x")
        cmd = seen["cmd"]
        self.assertNotIn("--dangerously-skip-permissions", cmd,
                         "backend must not bypass all permissions")
        self.assertIn("--allowedTools", cmd)
        self.assertIn("Bash(git *)", cmd)
        self.assertIn("Bash(python *)", cmd)


class TestBudgetGate(unittest.TestCase):
    """#471: the AIW/AFK loop must run every worker invocation through the
    fail-closed budget gate (aiw_budget_gate) — no reservation, no invocation."""

    def _issue(self, **over):
        i = {"number": 77, "title": "fix docs typo", "body": "x", "labels": []}
        i.update(over)
        return i

    def test_blocked_budget_prevents_worker_invocation(self):
        adapter = mock.Mock()
        with mock.patch.object(g, "_budget_reserve",
                               return_value=(False, {"decision": "block",
                                                     "reasons": ["cycle_cost_cap_exceeded"]})), \
             mock.patch.object(g, "_prepare_clone") as clone, \
             mock.patch.object(g, "_write_loop_state"):
            decision, state = g._process_issue(self._issue(), seq=1,
                                               today="2026-07-19", backend="local",
                                               adapter=adapter)
        clone.assert_not_called()
        adapter.invoke.assert_not_called()
        self.assertIn("budget", decision["action"])
        self.assertEqual(state["status"], "halted")

    def test_allowed_budget_reserves_then_releases(self):
        adapter = mock.Mock()
        adapter.needs_local_repo.return_value = True
        adapter.invoke.return_value = {"branch": "agent/issue-77",
                                       "commits": ["x"], "blocked": None}
        with mock.patch.object(g, "_budget_reserve",
                               return_value=(True, {"decision": "allow"})) as res, \
             mock.patch.object(g, "_budget_release") as rel, \
             mock.patch.object(g, "_prepare_clone", return_value="/tmp/clone"), \
             mock.patch.object(g, "_open_pr",
                               return_value="https://github.com/x/y/pull/1"), \
             mock.patch.object(g.shutil, "rmtree"), \
             mock.patch.object(g, "_write_loop_state"):
            decision, state = g._process_issue(self._issue(), seq=1,
                                               today="2026-07-19", backend="local",
                                               adapter=adapter)
        res.assert_called_once()
        rel.assert_called_once()            # reservation reconciled after the episode
        adapter.invoke.assert_called_once()
        self.assertEqual(state["status"], "completed")

    def test_parse_budget_block_picks_known_numeric_keys(self):
        body = ("intro\nmax_cost_usd: 1.5\n- estimated_total_tokens: 50000\n"
                "ignored_key: nope\nestimated_model_calls: 3\nmax_cost_usd: abc")
        b = g._parse_budget_block(body)
        self.assertEqual(b["max_cost_usd"], 1.5)     # numeric wins; "abc" ignored
        self.assertEqual(b["estimated_total_tokens"], 50000)
        self.assertEqual(b["estimated_model_calls"], 3)
        self.assertNotIn("ignored_key", b)

    def test_budget_request_maps_backend_provider(self):
        self.assertEqual(
            g._budget_request({"number": 5, "body": ""}, "local")["provider"], "claude-code-cli")
        self.assertEqual(
            g._budget_request({"number": 5, "body": ""}, "claude-code")["provider"],
            "claude-code-cli")

    def test_unmapped_backend_fails_closed(self):
        allowed, result = g._budget_reserve({"number": 5, "body": ""}, "not-a-backend")
        self.assertFalse(allowed)
        self.assertEqual(result["decision"], "block")


if __name__ == "__main__":
    unittest.main()


class TestPolicyInvalidDistinctFromBlock(unittest.TestCase):
    """#794: on the AFK path an invalid policy was indistinguishable from an
    ordinary governed block, and a release failure vanished entirely."""

    def _issue(self):
        return {"number": 77, "title": "fix docs typo", "body": "x", "labels": []}

    def test_invalid_policy_reserves_with_its_own_reason_code(self):
        # Measured in the issue: reasons=['budget_preflight_error'] for a corrupt
        # policy — the same code an out-of-budget job gets.
        with mock.patch.object(g.budget, "load_policy",
                               side_effect=g.budget.PolicyInvalid(
                                   "-999 is less than or equal to the minimum of 0")):
            allowed, result = g._budget_reserve(self._issue(), "local")
        self.assertFalse(allowed)
        self.assertEqual(result["reasons"], ["policy_invalid"])
        self.assertNotIn("budget_preflight_error", result["reasons"])
        self.assertIn("-999", result["error"])

    def test_other_preflight_errors_keep_the_original_reason_code(self):
        # The distinction must be narrow: only policy validity moves.
        with mock.patch.object(g.budget, "load_policy",
                               side_effect=RuntimeError("ledger is busy")):
            allowed, result = g._budget_reserve(self._issue(), "local")
        self.assertFalse(allowed)
        self.assertEqual(result["reasons"], ["budget_preflight_error"])

    def test_reserve_still_fails_closed_for_both(self):
        for exc in (g.budget.PolicyInvalid("bad"), RuntimeError("other")):
            with mock.patch.object(g.budget, "load_policy", side_effect=exc):
                allowed, result = g._budget_reserve(self._issue(), "local")
            self.assertFalse(allowed, f"{type(exc).__name__} must never allow")
            self.assertEqual(result["decision"], "block")

    def test_release_failure_is_recorded_not_just_swallowed(self):
        # Measured in the issue: "_budget_release returned normally (swallowed)".
        # It must still return normally, but leave a trace.
        with mock.patch.object(g.budget, "load_policy",
                               side_effect=g.budget.PolicyInvalid("bad")), \
             mock.patch.object(g.budget, "note_release_failure",
                               return_value=True) as note:
            g._budget_release(self._issue(), actual_cost_usd=0.0)   # must not raise
        note.assert_called_once()
        self.assertEqual(note.call_args[0][1], "aiw-77")
        self.assertIn("bad", note.call_args[0][2])

    def test_release_survives_a_failure_to_record_the_failure(self):
        # The reason release swallows at all is that a reconciliation hiccup must
        # never break the loop. Adding bookkeeping must not smuggle a new way for
        # it to break: if the note itself fails, release still returns normally.
        with mock.patch.object(g.budget, "load_policy",
                               side_effect=g.budget.PolicyInvalid("bad")), \
             mock.patch.object(g.budget, "note_release_failure",
                               side_effect=OSError("ledger gone")):
            g._budget_release(self._issue(), actual_cost_usd=0.0)   # must not raise

    def test_cycle_refuses_to_start_on_an_invalid_policy(self):
        # An invalid policy is not a per-job condition: validate once, up front,
        # and refuse — rather than blocking every job for the same reason while
        # swallowing every release in flight.
        fake_adapter = mock.Mock()
        fake_adapter.prepare.return_value = (True, "ok")
        with mock.patch.object(g, "_gh_queue", return_value=[self._issue()]), \
             mock.patch.object(g.budget, "load_policy",
                               side_effect=g.budget.PolicyInvalid("bad policy")), \
             mock.patch.object(g, "get_backend", return_value=fake_adapter) as get_backend, \
             mock.patch.object(g, "_process_issue") as proc:
            rc = g.main([])
        self.assertEqual(rc, 2)          # distinct from 1 (error) and 3 (halted)
        proc.assert_not_called()         # no work started
        get_backend.assert_not_called()  # adapter not selected when policy is invalid

    def test_valid_policy_does_not_block_the_cycle(self):
        fake_adapter = mock.Mock()
        fake_adapter.prepare.return_value = (True, "")
        fake_adapter.needs_local_repo.return_value = True
        with mock.patch.object(g, "_gh_queue", return_value=[self._issue()]), \
             mock.patch.object(g.budget, "load_policy", return_value={"ok": True}), \
             mock.patch.object(g, "get_backend", return_value=fake_adapter), \
             mock.patch.object(g, "_process_issue",
                               return_value=({"issue": 77, "action": "x"}, {})), \
             mock.patch.object(g, "_write_audit"):
            rc = g.main([])
        self.assertEqual(rc, 0)
        fake_adapter.prepare.assert_called_once()

    def test_dry_run_is_unaffected_by_policy_validity(self):
        # Dry-run plans only and reserves nothing, so a broken policy must not
        # stop an operator inspecting the queue.
        with mock.patch.object(g, "_gh_queue", return_value=[self._issue()]), \
             mock.patch.object(g.budget, "load_policy",
                               side_effect=g.budget.PolicyInvalid("bad policy")):
            rc = g.main(["--dry-run"])
        self.assertEqual(rc, 0)
