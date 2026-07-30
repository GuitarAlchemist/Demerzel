#!/usr/bin/env python3
"""
validate_dsp_loop.py — Automated Self-Correcting Parameter Optimization Loop.

Pairs TARS (F# code execution), IX (Signal analytics / DFT), and Hari (Swarm Consensus)
to iteratively adjust DSP parameters (e.g. gain/distortion) until they satisfy
constitutional safety limits (no clipping, acceptable noise).

Features Binary Search convergence, parameter memory/cache for warm starts,
and live streaming protocol integration with compiled hari-core Rust binary.

Three interchangeable graders, in precedence order:
  1. live hari-core `serve` over stdio JSONL, when the sibling binary is built
  2. deterministic threshold comparisons (always available)
  3. the typed BAML `EvaluateSignalSwarm` function, via --use-baml

All three read the SAME bounds from `logic/dsp-safety-bounds.yaml`, so the code
gate, the substrate gate and the model gate cannot drift apart.

Governance notes (policy `recursive-learning-eval`, Asimov Articles 4/7/9):
  * The safety bounds are goal parameters. This loop MEASURES against them and may
    PROPOSE a validated parameter; it never writes back to `logic/dsp-safety-bounds.yaml`.
  * A cached parameter is UNDERSTANDING from a previous run. Letting it silently widen
    or narrow this run's search space would be autonomous enactment (Article 9), so the
    warm start is opt-in via `--use-cached-bounds` and is recorded in the run artifact.
  * Every run emits an audited record under `state/dsp-validation/` (Article 7); the
    gitignored `.tmp/` cache is a convenience, not the audit trail.
"""
import json
import math
import subprocess
import sys
import argparse
from pathlib import Path

from demerzel_kit import now_iso, write_artifact

# Paths
ROOT = Path(__file__).resolve().parents[1]
SCRATCH_DIR = ROOT / ".tmp" / "dsp_validation"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

FSX_PATH = SCRATCH_DIR / "dsp_generator.fsx"
SIGNAL_PATH = SCRATCH_DIR / "signal.json"
CACHE_PATH = SCRATCH_DIR / "parameter_cache.json"

BOUNDS_PATH = ROOT / "logic" / "dsp-safety-bounds.yaml"
AUDIT_DIR = ROOT / "state" / "dsp-validation"

# Must match the F# template below. The fundamental's DFT bin is derived from
# these, so a change here without a change there silently mis-bins the analysis.
SAMPLE_COUNT = 512
SAMPLE_RATE = 512.0

# hari-core's wire vocabulary is the 4-value subset; BelnapState is the canonical
# 6-value enum the BAML schema and ix-types use. Translate at the boundary only.
_HARI_WIRE = {"TrueVal": "True", "FalseVal": "False", "Contradictory": "Contradictory"}

# Write F# DSP generator template if it doesn't exist
FSHARP_TEMPLATE = """
open System
open System.IO

let getArgValue name defaultValue (args: string[]) =
    match Array.tryFindIndex ((=) name) args with
    | Some idx when idx + 1 < args.Length -> float args.[idx + 1]
    | _ -> defaultValue

let args = Environment.GetCommandLineArgs()
let freq = getArgValue "--frequency" 5.0 args
let dist = getArgValue "--distortion" 0.0 args

printfn "=== DSP Generator ==="
printfn "Generating signal: Frequency = %.2f Hz, Distortion = %.2f" freq dist

let samplesCount = 512
let sampleRate = 512.0
let samples =
    [| 0 .. samplesCount - 1 |]
    |> Array.map (fun i ->
        let t = float i / sampleRate
        let raw = sin (2.0 * Math.PI * freq * t)
        if dist > 0.0 then
            Math.Tanh(raw * (1.0 + dist))
        else
            raw
    )

let json = "[" + String.Join(",", samples |> Array.map (fun x -> sprintf "%.6f" x)) + "]"
let outputPath = Path.Combine(__SOURCE_DIRECTORY__, "signal.json")
File.WriteAllText(outputPath, json)
printfn "Successfully generated %d samples and saved to: %s" samplesCount outputPath
"""


class SafetyBounds:
    """The constitutional limits, read from the single source of truth."""

    def __init__(self, thd_max, std_dev_max, pure_sine_std_dev):
        self.thd_max = thd_max
        self.std_dev_max = std_dev_max
        self.pure_sine_std_dev = pure_sine_std_dev


def load_bounds():
    """Read `logic/dsp-safety-bounds.yaml`.

    Deliberately fails loudly. A safety gate that falls back to a hardcoded default
    when its bounds file is missing is a gate that cannot be retuned or audited —
    the exact duplication this file was created to remove.
    """
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment problem, not logic
        raise SystemExit(f"PyYAML is required to read {BOUNDS_PATH}: {exc}")

    if not BOUNDS_PATH.is_file():
        raise SystemExit(f"Safety bounds not found at {BOUNDS_PATH} — refusing to validate without them.")

    with open(BOUNDS_PATH, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    try:
        bounds = doc["bounds"]
        return SafetyBounds(
            thd_max=float(bounds["thd_max"]["value"]),
            std_dev_max=float(bounds["std_dev_max"]["value"]),
            pure_sine_std_dev=float(doc["reference"]["pure_sine_std_dev"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"Malformed safety bounds in {BOUNDS_PATH}: {exc}")


class HariSession:
    """A live streaming session driving hari-core serve subprocess over stdio JSONL."""
    def __init__(self, proc):
        self._proc = proc
        self._closed = False

    @classmethod
    def spawn(cls, binary):
        proc = subprocess.Popen(
            [binary, "serve"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return cls(proc)

    def send(self, req):
        line = (json.dumps(req) + "\n").encode("utf-8")
        self._proc.stdin.write(line)
        self._proc.stdin.flush()
        raw = self._proc.stdout.readline()
        if not raw:
            raise RuntimeError("hari-core closed stdout before responding")
        return json.loads(raw.decode("utf-8"))

    def close(self):
        if self._closed:
            return
        try:
            self.send({"op": "close"})
        except Exception:
            pass
        self._closed = True
        if self._proc.stdin:
            try:
                self._proc.stdin.close()
            except Exception:
                pass
        try:
            self._proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait()

def ensure_templates():
    if not FSX_PATH.is_file():
        FSX_PATH.write_text(FSHARP_TEMPLATE.strip(), encoding="utf-8")

def find_hari_binary():
    suffix = ".exe" if sys.platform == "win32" else ""
    # Look for compiled hari-core in the sibling repo
    candidates = [
        ROOT.parent / "hari" / "target" / "release" / f"hari-core{suffix}",
        ROOT.parent / "hari" / "target" / "debug" / f"hari-core{suffix}",
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return None

def run_fsharp_generator(frequency, distortion):
    print(f"\n[TARS] Executing F# DSP generator script...")
    cmd = ["dotnet", "fsi", str(FSX_PATH), "--frequency", str(frequency), "--distortion", str(distortion)]
    result = subprocess.run(cmd, cwd=str(SCRATCH_DIR), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing F# script: {result.stderr}", file=sys.stderr)
        return False
    print(result.stdout.strip())
    return True

def analyze_signal(frequency):
    """Return (mean, std_dev, thd) or (None, None, None) on failure.

    The fundamental's bin index is DERIVED from the requested frequency rather than
    hardcoded. With 512 samples at 512 Hz the bin index happens to equal the frequency
    in Hz, which is why a hardcoded `4 <= k <= 6` window worked at the 5 Hz default and
    silently broke every other `--frequency`: the fundamental landed in the
    high-frequency band, THD exploded, and the loop could never pass.
    """
    print(f"\n[IX] Analyzing signal telemetry...")
    if not SIGNAL_PATH.is_file():
        print(f"Signal file not found at: {SIGNAL_PATH}", file=sys.stderr)
        return None, None, None

    with open(SIGNAL_PATH, "r") as f:
        try:
            samples = json.load(f)
        except json.JSONDecodeError as exc:
            print(f"Failed to parse signal JSON: {exc}", file=sys.stderr)
            return None, None, None

    count = len(samples)
    if count == 0:
        print("Signal file contained no samples.", file=sys.stderr)
        return None, None, None

    mean = sum(samples) / count
    variance = sum((x - mean) ** 2 for x in samples) / count
    std_dev = math.sqrt(variance)
    max_val = max(samples)
    min_val = min(samples)

    # Fundamental bin for this frequency, and the harmonic band above it.
    k0 = int(round(frequency * count / SAMPLE_RATE))
    nyquist_bin = count // 2
    if k0 < 2 or (2 * k0) >= nyquist_bin:
        print(
            f"Frequency {frequency} Hz maps to DFT bin {k0}, which leaves no usable "
            f"harmonic band below the Nyquist bin {nyquist_bin}. Choose a frequency "
            f"between {2 * SAMPLE_RATE / count:.1f} and {nyquist_bin * SAMPLE_RATE / count / 2:.1f} Hz.",
            file=sys.stderr,
        )
        return None, None, None

    # DFT for low-frequency vs high-frequency components
    high_freq_energy = 0.0
    fundamental_energy = 0.0
    for k in range(1, nyquist_bin):
        real = sum(samples[t] * math.cos(2.0 * math.pi * float(k * t) / float(count)) for t in range(count))
        imag = sum(samples[t] * math.sin(2.0 * math.pi * float(k * t) / float(count)) for t in range(count))
        mag = math.sqrt(real**2 + imag**2)

        # +/-1 bin around the fundamental; harmonics start above the second harmonic.
        if abs(k - k0) <= 1:
            fundamental_energy += mag
        elif k > 2 * k0:
            high_freq_energy += mag

    thd = high_freq_energy / (fundamental_energy + 1e-9)

    print(f"Signal Statistics:")
    print(f"  Mean: {mean:.6f}")
    print(f"  StdDev: {std_dev:.6f}")
    print(f"  Max/Min: {max_val:.6f} / {min_val:.6f}")
    print(f"  Fundamental bin: {k0} (harmonic band: k > {2 * k0})")
    print(f"  THD Proxy: {thd:.4f}")

    return mean, std_dev, thd


def fold_consensus(votes):
    """Fold SwarmVote values into a single hexavalent conclusion.

    Contradiction dominates: an explicit C, or a T and an F held simultaneously,
    both yield C. Returns (label, rationale, passed).
    """
    has_t = any(v["value"] == "TrueVal" for v in votes)
    has_f = any(v["value"] == "FalseVal" for v in votes)
    has_c = any(v["value"] == "Contradictory" for v in votes)

    if has_c:
        reasons = "; ".join(v["reason"] for v in votes if v["value"] == "Contradictory")
        return "Contradictory (C)", f"Structural boundary violation: {reasons}", False
    if has_t and has_f:
        reasons = "; ".join(v["reason"] for v in votes if v["value"] == "FalseVal")
        return "Contradictory (C)", f"Conflict between Generator (True) and Auditor (False): {reasons}", False
    if has_t:
        return "True (T)", "All agents in agreement, signal is clean.", True
    if has_f:
        return "False (F)", "Agents agree that the signal is invalid.", False
    return "Unknown (U)", "Insufficient agreement or data.", False


def deterministic_votes(std_dev, thd, bounds):
    """The code-based grader: pure threshold comparisons against the canonical bounds."""
    if thd > bounds.thd_max:
        aud_value, aud_reason = "FalseVal", f"Excessive high-frequency noise (THD {thd:.4f} > {bounds.thd_max})"
    else:
        aud_value, aud_reason = "TrueVal", f"Noise levels acceptable (THD {thd:.4f} <= {bounds.thd_max})"

    if std_dev > bounds.std_dev_max:
        arch_value, arch_reason = "Contradictory", f"Signal is clipping (StdDev {std_dev:.4f} > {bounds.std_dev_max})"
    else:
        arch_value, arch_reason = "TrueVal", f"Signal is within linear/safe bounds (StdDev {std_dev:.4f} <= {bounds.std_dev_max})"

    # self_trust is 1.0 for all three: each is a numeric threshold comparison, not a
    # judgement call. The BAML path returns the model's own calibration instead.
    return [
        {"agent_id": "tars-generator", "role": "Generator", "value": "TrueVal",
         "reason": "Code compiled and ran successfully", "self_trust": 1.0},
        {"agent_id": "sentrux-auditor", "role": "Auditor", "value": aud_value,
         "reason": aud_reason, "self_trust": 1.0},
        {"agent_id": "demerzel-architect", "role": "Architect", "value": arch_value,
         "reason": arch_reason, "self_trust": 1.0},
    ]


def baml_votes(mean, std_dev, thd, bounds, model=None):
    """The model-based grader: one typed `EvaluateSignalSwarm` call per role.

    The transport is the Claude Code CLI, not an HTTP provider. BAML renders the prompt
    (`b.request`) and types the answer (`b.parse`); neither touches the network, so the
    completion in between can come from anywhere. It comes from `claude -p`, which bills
    the subscription — `claude-code-cli` is a declared `local-seat` /
    `subscription-or-local` provider in the AIW budget policy.

    Deliberately NOT `b.EvaluateSignalSwarm(...)`. That is the in-band path: it would send
    to whatever client `baml_src` declares, which is not a provider the budget policy
    knows, so the spend would happen entirely outside the gate meant to authorise it.
    The declared client points at an unroutable port so that mistake fails closed rather
    than billing quietly; this function is why it never gets made.

    Imported lazily so the default deterministic path keeps running with neither
    `baml-py` installed nor a CLI present.
    """
    # The generated client lives at the repo root (ADR-0005 §Consequences pins the
    # `from baml_client import ...` import path), but sys.path[0] is scripts/ when this
    # runs as `python scripts/validate_dsp_loop.py`.
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    try:
        # `baml_client.b` is the ASYNC client; the sync one must be imported by module.
        from baml_client.sync_client import b
        from baml_client.types import AgentRole, SignalTelemetry, SafetyBounds as BamlBounds
        from baml_claude_code import ClaudeCodeError, render_prompt, run_claude_code
    except ImportError as exc:
        raise SystemExit(
            f"--use-baml requires the generated BAML client and its runtime: {exc}\n"
            "  pip install baml-py && npx --yes @boundaryml/baml generate"
        )

    telemetry = SignalTelemetry(mean=mean, std_dev=std_dev, thd=thd)
    baml_bounds = BamlBounds(
        thd_max=bounds.thd_max,
        std_dev_max=bounds.std_dev_max,
        pure_sine_std_dev=bounds.pure_sine_std_dev,
    )

    votes = []
    for role in (AgentRole.Generator, AgentRole.Auditor, AgentRole.Architect):
        # 1. render (local)  2. complete (subscription, out of band)  3. type (local)
        # The SYNC client returns an HTTPRequest directly; only `baml_client.b` (the async
        # one) hands back a coroutine here. Neither opens a socket.
        request = b.request.EvaluateSignalSwarm(
            telemetry=telemetry, role=role, bounds=baml_bounds)
        prompt = render_prompt(request)
        try:
            raw = run_claude_code(prompt, model=model)
        except ClaudeCodeError as exc:
            # A grader that cannot reach its model must not be mistaken for a grader that
            # voted. Abort the cycle; the caller records `aborted_reason` and exits
            # non-zero rather than proposing a parameter nothing graded.
            raise SystemExit(f"BAML grader unavailable: {exc}")
        try:
            vote = b.parse.EvaluateSignalSwarm(raw)
        except Exception as exc:  # noqa: BLE001 — baml_py.BamlError and anything under it
            # The CLI can exit 0 and still return something that is not a SwarmVote: an
            # apology, a refusal, a truncated object. BAML refuses to coerce it, which is
            # correct — but the raw exception escaped as a traceback, so the run recorded no
            # `aborted_reason` and never said which reply broke it. Same rule as above: an
            # ungradeable answer is not a vote. Abort, and quote the reply.
            raise SystemExit(
                f"BAML grader returned an ungradeable response for {role}: {exc}\n"
                f"  raw reply (first 300 chars): {raw[:300]}"
            )
        votes.append({
            "agent_id": vote.agent_id,
            "role": vote.role.value if hasattr(vote.role, "value") else str(vote.role),
            "value": vote.value.value if hasattr(vote.value, "value") else str(vote.value),
            "reason": vote.reason,
            "self_trust": vote.self_trust,
        })
    return votes


def hari_consensus(votes, binary_path):
    """Push the votes through a live hari-core substrate and read back its belief.

    Returns (label, rationale, passed, beliefs) or None if the substrate could not be
    driven — the caller then falls back to folding the votes locally.
    """
    print(f"  Spawning live {Path(binary_path).name} serve process...")
    try:
        session = HariSession.spawn(binary_path)
        session.send({"op": "open", "config": {"dimension": 4, "priority_model": "RecencyDecay"}})

        for cycle, vote in enumerate(votes, start=1):
            session.send({
                "op": "event",
                "event": {
                    "cycle": cycle,
                    "source": vote["agent_id"],
                    "payload": {
                        "type": "belief_update",
                        "proposition": "signal_quality",
                        "value": _HARI_WIRE.get(vote["value"], vote["value"]),
                    },
                },
            })

        res = session.send({"op": "metrics"})
        session.close()

        beliefs = res.get("beliefs", {})
        consensus_val = beliefs.get("signal_quality", "Unknown")

        print(f"  Swarm Beliefs in Substrate: {json.dumps(beliefs, indent=2)}")
        print(f"  Consensus Result on 'signal_quality': {consensus_val}")

        if consensus_val == "True":
            return "True (T)", "All agents in agreement, signal is clean.", True, beliefs
        if consensus_val == "Contradictory":
            return "Contradictory (C)", "Swarm resolved contradictory constraints.", False, beliefs
        return f"{consensus_val}", "Swarm rejected parameters.", False, beliefs

    except Exception as exc:
        print(f"  [WARN] Live swarm process error: {exc}")
        print("  Falling back to programmatic consensus fold...")
        return None


def run_hari_consensus(mean, std_dev, thd, bounds, use_baml, allow_hari=True,
                       baml_model=None):
    print(f"\n[Hari] Running Swarm Consensus...")

    votes = (baml_votes(mean, std_dev, thd, bounds, model=baml_model)
             if use_baml else deterministic_votes(std_dev, thd, bounds))

    # Name the model in the grader id, not just "baml": a safety gate's audit record has
    # to say what actually graded it. Two runs with different models are not the same
    # evidence, and `graders` is the only field that could tell them apart.
    grader = f"baml:claude-code:{baml_model or 'default'}" if use_baml else "deterministic"
    print(f"Grader: {'BAML EvaluateSignalSwarm (model-based)' if use_baml else 'deterministic thresholds (code-based)'}")
    print("Swarm Votes:")
    for v in votes:
        print(f"  Agent: {v['agent_id']} ({v['role']}) -> Vote: {v['value']} "
              f"| Trust: {v['self_trust']:.2f} | Rationale: {v['reason']}")

    beliefs = None
    binary_path = find_hari_binary() if allow_hari else None
    if binary_path:
        live = hari_consensus(votes, binary_path)
        if live is not None:
            consensus, rationale, passed, beliefs = live
            grader += "+hari-live"
            print(f"\nConsensus Result: {consensus}")
            print(f"Rationale: {rationale}")
            return passed, votes, consensus, rationale, grader, beliefs

    consensus, rationale, passed = fold_consensus(votes)

    print(f"\nConsensus Result: {consensus}")
    print(f"Rationale: {rationale}")

    return passed, votes, consensus, rationale, grader, beliefs

def load_cache():
    if CACHE_PATH.is_file():
        try:
            with open(CACHE_PATH, "r") as f:
                data = json.load(f)
                return data.get("safe_distortion")
        except Exception:
            pass
    return None

def write_cache(val):
    try:
        with open(CACHE_PATH, "w") as f:
            json.dump({"safe_distortion": val, "validated_at": now_iso()}, f)
    except Exception as exc:
        print(f"Failed to write parameter cache: {exc}", file=sys.stderr)


def write_audit_record(record):
    """Emit the Article 7 trace. Unlike the `.tmp/` cache this is not gitignored."""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    path = AUDIT_DIR / f"dsp-validation-{record['run_id']}.json"
    try:
        write_artifact(path, record)
        print(f"\n[Audit] Run record written to {path.relative_to(ROOT)}")
    except Exception as exc:
        print(f"Failed to write audit record: {exc}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Automated Self-Correcting Parameter Optimization Loop")
    parser.add_argument("--frequency", type=float, default=5.0, help="Target signal frequency (Hz)")
    parser.add_argument("--max-cycles", type=int, default=10, help="Maximum self-correction cycles")
    parser.add_argument("--use-baml", action="store_true",
                        help="Grade with the typed BAML EvaluateSignalSwarm function instead of "
                             "the deterministic thresholds. Needs baml-py and the Claude Code "
                             "CLI on PATH — NOT a provider API key: the prompt is rendered and "
                             "the answer typed locally, and only the completion goes out of "
                             "band, through `claude -p` on the subscription.")
    parser.add_argument("--baml-model", default=None, metavar="NAME",
                        help="Model for the BAML grader, passed to `claude -p --model`. "
                             "Defaults to the CLI's own default. Recorded in the run "
                             "artifact's `graders` field, because two runs graded by "
                             "different models are not the same evidence.")
    parser.add_argument("--no-hari", action="store_true",
                        help="Skip the live hari-core substrate even if the binary is present, "
                             "and fold the votes locally instead")
    parser.add_argument("--use-cached-bounds", action="store_true",
                        help="Authorize the previous run's validated parameter to narrow this "
                             "run's search space. Off by default: enacting a cached parameter "
                             "without authorization is an Article 9 (Bounded Autonomy) crossing, "
                             "and a stale cache silently caps the search ceiling.")
    args = parser.parse_args()

    bounds = load_bounds()
    ensure_templates()

    print("====================================================")
    print("=== SELF-CORRECTING SWARM LOOP: ORCHESTRATOR RUN ===")
    print("=== WITH PARAMETER CACHE, BINARY SEARCH & HARI    ===")
    print("====================================================")

    freq = args.frequency
    run_id = now_iso().replace(":", "").replace("-", "")

    # 1. Warm Start / Cache Load — READ as understanding, ENACT only if authorized.
    cached_safe = load_cache()
    warm_started = False
    low, high = 0.0, 10.0
    if cached_safe is None:
        print("[Memory Cache] No previous run cache found. Performing full sweep.")
    elif args.use_cached_bounds:
        print(f"[Memory Cache] Loaded last known safe distortion: {cached_safe:.4f}")
        print("[Memory Cache] --use-cached-bounds given: narrowing the search space (authorized).")
        print("[Memory Cache] Cycle 1 will RE-VALIDATE the cached value before trusting it.")
        high = max(cached_safe * 1.5, 5.0)
        warm_started = True
    else:
        print(f"[Memory Cache] Last known safe distortion: {cached_safe:.4f} (informational only).")
        print("[Memory Cache] Full sweep — pass --use-cached-bounds to authorize a warm start.")

    generation = 1
    epsilon = 0.05

    # Only a PASSING cycle in THIS run may set this. Seeding it from the cache is what
    # let a first-cycle compile error exit 0 reporting "CONSTITUTIONAL RULES SATISFIED"
    # for a value this run never validated — a safety gate that failed open.
    validated_this_run = None
    aborted_reason = None
    stale_cache = False
    cycles = []
    graders_used = set()

    print(f"Target Frequency: {freq} Hz")
    print(f"Binary Search Bounds: [{low:.4f}, {high:.4f}]")

    # A warm start must re-prove the value it carried forward, not assume it. Seeding
    # `low = cached_safe` instead would mean the known-good point is never re-tested, so
    # a run that finds nothing better reports failure for a parameter it never tried —
    # and a cache that has gone stale would never be detected.
    probe_cached = cached_safe if warm_started else None

    while generation <= args.max_cycles and (high - low) > epsilon:
        is_cached_probe = probe_cached is not None
        if is_cached_probe:
            distortion = probe_cached
            probe_cached = None
            print(f"\n--- [Cycle {generation}] Re-validating cached value: Distortion = {distortion:.4f} ---")
        else:
            # Midpoint of search space
            distortion = (low + high) / 2.0
            print(f"\n--- [Cycle {generation}] Testing Midpoint: Distortion = {distortion:.4f} ---")

        # 1. Run F# generator (TARS)
        if not run_fsharp_generator(frequency=freq, distortion=distortion):
            aborted_reason = "compilation_error"
            print("[Demerzel] Compilation error. Terminating loop.")
            break

        # 2. Run signal analysis (IX)
        mean, std_dev, thd = analyze_signal(freq)
        if std_dev is None:
            aborted_reason = "telemetry_error"
            print("[Demerzel] Telemetry extraction error. Terminating loop.")
            break

        # 3. Check consensus (Hari + Demerzel)
        passed, votes, consensus, rationale, grader, beliefs = run_hari_consensus(
            mean, std_dev, thd, bounds, args.use_baml, allow_hari=not args.no_hari,
            baml_model=args.baml_model
        )
        graders_used.add(grader)

        cycles.append({
            "cycle": generation,
            "distortion": distortion,
            "cached_probe": is_cached_probe,
            "telemetry": {"mean": mean, "std_dev": std_dev, "thd": thd},
            "votes": votes,
            "grader": grader,
            "hari_beliefs": beliefs,
            "consensus": consensus,
            "rationale": rationale,
            "passed": passed,
        })

        if passed:
            print(f"\n[Demerzel] Safe state achieved for Distortion = {distortion:.4f}.")
            validated_this_run = distortion
            low = distortion  # Try to push limits higher
            print(f"[Loop Controller] Updating Safe Lower Bound: low -> {low:.4f}")
        else:
            print(f"\n[Demerzel] Constraint boundary violated for Distortion = {distortion:.4f}.")
            if is_cached_probe:
                stale_cache = True
                print("[Memory Cache] STALE: the carried-forward value no longer validates. "
                      "Discarding it and bisecting downward.")
            high = distortion  # Pull upper bound down
            print(f"[Loop Controller] Updating Vetoed Upper Bound: high -> {high:.4f}")

        generation += 1

    record = {
        "run_id": run_id,
        "timestamp": now_iso(),
        "recursion_depth": 0,
        "article_4_check": "understanding",
        "requires_authorization": True,
        "frequency_hz": freq,
        "graders": sorted(graders_used),
        "bounds": {
            "thd_max": bounds.thd_max,
            "std_dev_max": bounds.std_dev_max,
            "source": str(BOUNDS_PATH.relative_to(ROOT)).replace("\\", "/"),
        },
        "warm_started": warm_started,
        "cached_value_seen": cached_safe,
        "cached_value_stale": stale_cache,
        "cycles": cycles,
        "validated_this_run": validated_this_run,
        "aborted_reason": aborted_reason,
        "search_converged": (high - low) <= epsilon,
    }
    write_audit_record(record)

    if aborted_reason is not None:
        print("\n====================================================")
        print(f"=== LOOP ABORTED: {aborted_reason.upper()} ===")
        print("Nothing was validated in this run. No parameter is proposed.")
        print("====================================================")
        sys.exit(1)

    if validated_this_run is not None:
        print("\n====================================================")
        print("=== LOOP COMPLETED: CONSTITUTIONAL RULES SATISFIED ===")
        print(f"Validated parameter: Distortion = {validated_this_run:.4f}")
        if not record["search_converged"]:
            print(f"NOTE: search did not converge within {args.max_cycles} cycles "
                  f"(interval still [{low:.4f}, {high:.4f}]) - this is a safe value, "
                  f"not necessarily the maximum safe value.")
        print("This is a PROPOSED parameter (understanding). Enacting it as a control")
        print("input requires human authorization - see the audit record.")
        print("====================================================")
        write_cache(validated_this_run)
        sys.exit(0)

    print("\n====================================================")
    print("=== LOOP TERMINATED: NO SAFE VALUE FOUND ===")
    print("====================================================")
    sys.exit(1)

if __name__ == "__main__":
    main()
