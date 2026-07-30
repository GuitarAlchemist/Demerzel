#!/usr/bin/env python3
"""Tests for the out-of-band BAML transport (`baml_claude_code`) and its one caller.

Nothing here touches the network or spawns the CLI: `render_prompt` is pure, and
`run_claude_code` is exercised through a patched `subprocess.run`. The point of the
suite is the seam where money could leak, so the load-bearing test is
`test_grader_never_uses_the_in_band_client`.
"""
import subprocess
import sys
import unittest
import unittest.mock as mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import baml_claude_code as bcc


def _request(body):
    """A stand-in for an awaited BAML HTTP request."""
    return mock.Mock(body=body, url="http://127.0.0.1:1/v1/chat/completions")


class TestRenderPrompt(unittest.TestCase):
    def test_plain_string_content(self):
        req = _request({"messages": [{"role": "user", "content": "grade this"}]})
        self.assertEqual("grade this", bcc.render_prompt(req))

    def test_multimodal_text_parts_are_joined_in_order(self):
        # This is the shape BAML actually emits for the declared client.
        req = _request({"messages": [{"role": "user", "content": [
            {"type": "text", "text": "first"},
            {"type": "text", "text": "second"},
        ]}]})
        self.assertEqual("first\nsecond", bcc.render_prompt(req))

    def test_multiple_messages_are_kept(self):
        req = _request({"messages": [
            {"role": "system", "content": "you are an auditor"},
            {"role": "user", "content": "grade this"},
        ]})
        self.assertEqual("you are an auditor\n\ngrade this", bcc.render_prompt(req))

    def test_json_body_is_decoded(self):
        req = _request(b'{"messages":[{"role":"user","content":"bytes body"}]}')
        self.assertEqual("bytes body", bcc.render_prompt(req))

    def test_non_text_part_is_refused_rather_than_silently_dropped(self):
        # Dropping an image part would send a DIFFERENT prompt than BAML rendered, and
        # the model would answer a question we did not ask.
        req = _request({"messages": [{"role": "user", "content": [
            {"type": "text", "text": "look at this"},
            {"type": "image_url", "image_url": {"url": "data:..."}},
        ]}]})
        with self.assertRaises(bcc.ClaudeCodeError) as ctx:
            bcc.render_prompt(req)
        self.assertIn("image_url", str(ctx.exception))

    def test_body_without_messages_names_the_cause(self):
        # If someone repoints the client at a non-OpenAI-shaped provider, the body shape
        # changes and this must say so instead of sending an empty prompt.
        req = _request({"contents": [{"parts": [{"text": "gemini shape"}]}]})
        with self.assertRaises(bcc.ClaudeCodeError) as ctx:
            bcc.render_prompt(req)
        self.assertIn("messages", str(ctx.exception))

    def test_empty_prompt_is_refused(self):
        req = _request({"messages": [{"role": "user", "content": "   "}]})
        with self.assertRaises(bcc.ClaudeCodeError):
            bcc.render_prompt(req)


class TestRunClaudeCode(unittest.TestCase):
    def _completed(self, stdout="ok", stderr="", rc=0):
        return subprocess.CompletedProcess(args=[], returncode=rc,
                                           stdout=stdout, stderr=stderr)

    def test_prompt_goes_on_stdin_not_argv(self):
        # A rendered BAML prompt is >1KB; argv limits are platform-dependent, so passing
        # it as an argument works in a test and fails on a longer schema.
        prompt = "x" * 5000
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed()) as run:
            bcc.run_claude_code(prompt)
        argv, kwargs = run.call_args[0][0], run.call_args[1]
        self.assertEqual(["claude", "-p", "--allowed-tools", ""], argv)
        self.assertEqual(prompt, kwargs["input"])
        self.assertNotIn(prompt, argv)

    def test_api_key_never_reaches_the_child_process(self):
        """The reason this transport exists. Claude Code prefers ANTHROPIC_API_KEY over
        the claude.ai subscription when both are present — verified 2026-07-30: the same
        prompt returned `API Error: 400 ... usage limits` with the key set and a normal
        completion with it unset. So a call made with the key inherited is METERED spend
        through a provider the AIW budget policy does not gate. Strip it, and assert that
        we did; a guarantee that depends on the parent environment is a coincidence."""
        with mock.patch.dict(bcc.os.environ,
                             {"ANTHROPIC_API_KEY": "sk-should-not-propagate",
                              "ANTHROPIC_AUTH_TOKEN": "also-not",
                              "PATH": "/usr/bin"}, clear=False), \
             mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed()) as run:
            bcc.run_claude_code("p")

        child_env = run.call_args[1]["env"]
        self.assertNotIn("ANTHROPIC_API_KEY", child_env)
        self.assertNotIn("ANTHROPIC_AUTH_TOKEN", child_env)
        self.assertIn("PATH", child_env)   # the rest of the environment survives

    def test_every_ambient_route_to_a_metered_backend_is_stripped(self):
        """Suppressing only ANTHROPIC_API_KEY leaves the other billing switches in place.
        CLAUDE_CODE_USE_BEDROCK / _USE_VERTEX select a cloud backend billed to the AWS
        account or GCP project, and ANTHROPIC_BASE_URL can redirect to a metering gateway —
        none of which is the subscription this transport exists to use. Raised by an
        adversarial cross-model review of the first version."""
        ambient = {
            "ANTHROPIC_API_KEY": "sk-x",
            "ANTHROPIC_AUTH_TOKEN": "tok",
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "CLAUDE_CODE_USE_VERTEX": "1",
            "ANTHROPIC_BASE_URL": "https://gateway.example/v1",
            "PATH": "/usr/bin",
        }
        with mock.patch.dict(bcc.os.environ, ambient, clear=False):
            env = bcc.subscription_env()
        for var in ambient:
            if var == "PATH":
                self.assertIn(var, env)          # unrelated environment survives
            else:
                self.assertNotIn(var, env, f"{var} still reaches the child")

    def test_no_tools_are_granted_to_the_grader(self):
        """`claude -p` is a coding agent, not a completion endpoint: by default it can
        read/write files and run commands in its cwd. A grader needs none of that, and a
        grader able to edit the repo it grades is worse than the spend problem this module
        was written to solve."""
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"),              mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed()) as run:
            bcc.run_claude_code("p")
        argv = run.call_args[0][0]
        self.assertIn("--allowed-tools", argv)
        self.assertEqual("", argv[argv.index("--allowed-tools") + 1])

    def test_subscription_env_is_a_copy_not_a_mutation(self):
        # Stripping the key from os.environ itself would change auth for the whole
        # process, including code that legitimately uses the API.
        with mock.patch.dict(bcc.os.environ, {"ANTHROPIC_API_KEY": "sk-x"}, clear=False):
            stripped = bcc.subscription_env()
            self.assertNotIn("ANTHROPIC_API_KEY", stripped)
            self.assertEqual("sk-x", bcc.os.environ["ANTHROPIC_API_KEY"])

    def test_model_is_forwarded(self):
        # Deliberately not a real dated model id: `test_no_retired_models` rejects any
        # `claude-*-YYYYMMDD` literal in live config, and it is right to — this test
        # asserts forwarding, not which model exists.
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed()) as run:
            bcc.run_claude_code("p", model="a-model-name")
        self.assertEqual(["claude", "-p", "--allowed-tools", "", "--model", "a-model-name"],
                         run.call_args[0][0])

    def test_missing_cli_is_a_clear_error(self):
        with mock.patch.object(bcc.shutil, "which", return_value=None):
            with self.assertRaises(bcc.ClaudeCodeError) as ctx:
                bcc.run_claude_code("p")
        self.assertIn("PATH", str(ctx.exception))

    def test_nonzero_exit_surfaces_stderr(self):
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed(stdout="", stderr="quota gone", rc=1)):
            with self.assertRaises(bcc.ClaudeCodeError) as ctx:
                bcc.run_claude_code("p")
        self.assertIn("quota gone", str(ctx.exception))

    def test_empty_output_is_an_error_not_an_empty_vote(self):
        # An empty completion parsed as a vote would be a grader that silently abstained.
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               return_value=self._completed(stdout="   ")):
            with self.assertRaises(bcc.ClaudeCodeError):
                bcc.run_claude_code("p")

    def test_timeout_is_reported_as_such(self):
        with mock.patch.object(bcc.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(bcc.subprocess, "run",
                               side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1)):
            with self.assertRaises(bcc.ClaudeCodeError) as ctx:
                bcc.run_claude_code("p", timeout=1)
        self.assertIn("1s", str(ctx.exception))


def _generated_client_importable():
    """Whether the generated client can actually be IMPORTED — not merely whether its
    file exists. `baml_client/` is committed, so a file check passes on a machine with no
    `baml-py` installed and the tests then error instead of skipping. Checking the file
    was a guard pointed at the wrong subject; this checks the thing that matters."""
    try:
        import baml_client.sync_client  # noqa: F401
        return True
    except Exception:
        return False


CLIENT_IMPORTABLE = _generated_client_importable()


class TestTheMoneySeamWithoutTheRuntime(unittest.TestCase):
    """Source-level assertions on the seam where spend could leak.

    Deliberately textual so they run EVERYWHERE, including CI, which has no `baml-py`.
    The runtime tests below are stronger but skip without it, and a gate that skips is
    not a gate — the same reasoning as the `pip install jsonschema` comment in
    `governance-validate.yml`. These cover the invariant even when the runtime is absent.
    """

    def test_grader_source_uses_request_and_parse_not_the_in_band_call(self):
        """Walk the AST rather than grepping the text.

        A substring search cannot tell a CALL from PROSE ABOUT a call — the docstring in
        `baml_votes` explains why the in-band form is wrong, and a textual guard flags
        that explanation as the violation it is warning against. Matching `ast.Call`
        nodes asks the question that actually matters. (`ast` is stdlib, so this still
        runs where `baml-py` is absent.)
        """
        import ast
        tree = ast.parse((ROOT / "scripts" / "validate_dsp_loop.py").read_text(encoding="utf-8"))

        in_band, via_request, via_parse = [], False, False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Attribute) and func.attr == "EvaluateSignalSwarm"):
                continue
            target = func.value
            if isinstance(target, ast.Name) and target.id == "b":
                in_band.append(node.lineno)                      # b.EvaluateSignalSwarm(...)
            elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                    and target.value.id == "b":
                via_request |= target.attr == "request"          # b.request.Evaluate...
                via_parse |= target.attr == "parse"              # b.parse.Evaluate...

        self.assertEqual(
            [], in_band,
            f"in-band BAML call at line(s) {in_band}: this sends to the client declared "
            "in baml_src, which is not a provider the AIW budget policy gates. Use "
            "b.request/b.parse with scripts/baml_claude_code.py.",
        )
        self.assertTrue(via_request, "grader no longer renders via b.request")
        self.assertTrue(via_parse, "grader no longer types via b.parse")

    def test_the_declared_client_cannot_bill_anyone(self):
        """Defence in depth: even if an in-band call slipped through, the declared client
        points at a port nothing can listen on, so it fails closed rather than spending.
        Asserted against baml_src, which is the contract consumers also generate from."""
        schema = (ROOT / "baml_src" / "schema.baml").read_text(encoding="utf-8")
        self.assertIn("client NeverSendInBand", schema)
        self.assertIn("127.0.0.1:1", schema)
        self.assertNotIn('client "openai/', schema)

    def test_transport_strips_the_api_key_by_construction(self):
        self.assertIn("ANTHROPIC_API_KEY", bcc._SUPPRESSED_AUTH_VARS)


@unittest.skipUnless(CLIENT_IMPORTABLE,
                     "baml-py not installed — generated client cannot be imported")
class TestGraderUsesTheOutOfBandPath(unittest.TestCase):
    """The money tests. These need the real generated client, but no network."""

    def _bounds(self):
        import validate_dsp_loop as v
        return v.SafetyBounds(thd_max=0.05, std_dev_max=0.75, pure_sine_std_dev=0.707)

    def test_grader_never_uses_the_in_band_client(self):
        """THE tripwire. `b.EvaluateSignalSwarm(...)` sends to whatever client baml_src
        declares — a provider the AIW budget policy does not list — so the spend would
        bypass the gate meant to authorise it. That is the #863 shape: a correct gate
        pointed at a provider nobody is using. If this fails, someone reintroduced the
        in-band call; do not "fix" it by relaxing the assertion."""
        import validate_dsp_loop as v
        from baml_client.sync_client import BamlSyncClient

        raw = ('{"agent_id":"a","role":"Auditor","value":"True",'
               '"reason":"r","self_trust":0.9}')
        # `baml_votes` re-runs `from baml_claude_code import ...` on every call, so the
        # name it binds is read off the module at call time — patch it there.
        with mock.patch.object(BamlSyncClient, "EvaluateSignalSwarm") as in_band, \
             mock.patch.object(bcc, "run_claude_code", return_value=raw):
            v.baml_votes(0.0, 0.70, 0.03, self._bounds())

        in_band.assert_not_called()

    def test_votes_come_back_typed_from_a_messy_completion(self):
        """The whole reason for keeping BAML: a CLI answers conversationally. Fenced
        JSON wrapped in prose must still yield a typed, enum-coerced vote."""
        import validate_dsp_loop as v
        messy = (
            "Sure, here's my assessment:\n\n```json\n"
            '{"agent_id":"auditor-1","role":"Auditor","value":"False",'
            '"reason":"stddev near clip limit","self_trust":0.82}\n'
            "```\nHope that helps!"
        )
        with mock.patch.object(bcc, "run_claude_code", return_value=messy):
            votes = v.baml_votes(0.0, 0.70, 0.03, self._bounds())

        self.assertEqual(3, len(votes))            # one per role
        self.assertEqual("auditor-1", votes[0]["agent_id"])
        self.assertAlmostEqual(0.82, votes[0]["self_trust"])
        # The model emits the ALIAS ("False"); BAML coerces it to the enum, and the
        # internal vocabulary is the member name. Asserted explicitly because the two
        # forms are easy to confuse, and confusing them silently breaks consensus.
        self.assertEqual("FalseVal", votes[0]["value"])

    def test_both_graders_speak_the_same_vote_vocabulary(self):
        """The BAML grader and the deterministic grader feed the SAME consensus fold and
        the same `_HARI_WIRE` translation. If one said "False" while the other said
        "FalseVal", `has_c`/`_HARI_WIRE` would silently mis-read half the votes and the
        gate would grade on a vocabulary mismatch rather than on the signal."""
        import validate_dsp_loop as v
        raw = ('{"agent_id":"a","role":"Auditor","value":"False",'
               '"reason":"r","self_trust":0.9}')
        with mock.patch.object(bcc, "run_claude_code", return_value=raw):
            baml = v.baml_votes(0.0, 0.80, 0.09, self._bounds())
        det = v.deterministic_votes(0.80, 0.09, self._bounds())

        vocabulary = {vote["value"] for vote in baml} | {vote["value"] for vote in det}
        self.assertTrue(vocabulary <= set(v._HARI_WIRE),
                        f"vote values {sorted(vocabulary)} are not all translatable by "
                        f"_HARI_WIRE {sorted(v._HARI_WIRE)}")

    def test_the_model_reaches_the_cli(self):
        import validate_dsp_loop as v
        raw = ('{"agent_id":"a","role":"Auditor","value":"True",'
               '"reason":"r","self_trust":0.9}')
        with mock.patch.object(bcc, "run_claude_code", return_value=raw) as run:
            v.baml_votes(0.0, 0.70, 0.03, self._bounds(), model="some-model")
        self.assertEqual("some-model", run.call_args[1]["model"])

    def test_an_ungradeable_reply_aborts_and_quotes_itself(self):
        """The CLI can exit 0 and still return something that is not a SwarmVote — an
        apology, a refusal, a truncated object. BAML refuses to coerce it, which is right,
        but that must surface as an abort naming the reply rather than a bare traceback."""
        import validate_dsp_loop as v
        with mock.patch.object(bcc, "run_claude_code",
                               return_value="I'm sorry, I can't help with that."):
            with self.assertRaises(SystemExit) as ctx:
                v.baml_votes(0.0, 0.70, 0.03, self._bounds())
        message = str(ctx.exception)
        self.assertIn("ungradeable", message)
        self.assertIn("I'm sorry", message)      # the offending reply is quoted

    def test_an_unreachable_cli_aborts_instead_of_voting(self):
        """A grader that cannot reach its model must not be mistaken for one that voted.
        Same rule the cache fail-open taught: only a real result may report a result."""
        import validate_dsp_loop as v
        with mock.patch.object(bcc, "run_claude_code",
                               side_effect=bcc.ClaudeCodeError("no cli")):
            with self.assertRaises(SystemExit) as ctx:
                v.baml_votes(0.0, 0.70, 0.03, self._bounds())
        self.assertIn("grader unavailable", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
