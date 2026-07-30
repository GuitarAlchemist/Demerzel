#!/usr/bin/env python3
"""
monitor_baml_and_learning.py — Progress and Blocker Telemetry Snapshot.

Checks BAML file counts, compiles schemas to verify client health, and fetches
recursive self-improvement memory caches alongside any active governance blockers
(HALT-ALL triggers and unresolved Conscience signals).
"""
import os
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BAML_SRC = ROOT / "baml_src"
BAML_CLIENT = ROOT / "baml_client"
CACHE_PATH = ROOT / ".tmp" / "dsp_validation" / "parameter_cache.json"
CONSCIENCE_DIR = ROOT / "state" / "conscience" / "signals"
HALT_PATH = Path.home() / ".demerzel" / "HALT-ALL"

def check_baml():
    print("=== BAML ADOPTION PROGRESS ===")
    if BAML_SRC.is_dir():
        baml_files = list(BAML_SRC.glob("*.baml"))
        print(f"  Source Files: {len(baml_files)} (.baml files found)")
        for f in baml_files:
            print(f"    - {f.name}")
    else:
        print("  [ERROR] baml_src/ directory is missing!")
        return False
        
    print("  Verifying compiler generation...")
    result = subprocess.run(["npx", "--yes", "@boundaryml/baml", "generate"], cwd=str(ROOT), capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        print("    [PASS] Client generated successfully under baml_client/")
        if BAML_CLIENT.is_dir():
            client_files = list(BAML_CLIENT.glob("*.py"))
            print(f"    - Generated {len(client_files)} Python client modules")
        return True
    else:
        print("    [FAIL] Client generation failed!")
        print(result.stderr.strip())
        return False

def check_learning():
    print("\n=== RECURSIVE LEARNING STATE ===")
    if CACHE_PATH.is_file():
        try:
            with open(CACHE_PATH, "r") as f:
                data = json.load(f)
            print(f"  [Memory Cache] Active: Last safe distortion resolved = {data.get('safe_distortion'):.4f}")
        except Exception as exc:
            print(f"  [ERROR] Failed to read parameter cache: {exc}")
    else:
        print("  [Memory Cache] Empty: No previous safe parameter cached yet.")

    obs_file = ROOT / "state" / "learning" / "observations.jsonl"
    if obs_file.is_file():
        try:
            with open(obs_file, "r") as f:
                count = sum(1 for _ in f)
            print(f"  [Observations Log] Active: {count} events captured")
        except Exception:
            pass
    else:
        print("  [Observations Log] Empty: No session observations captured yet.")

def check_blockers():
    print("\n=== GOVERNANCE BLOCKERS & SEVERITIES ===")
    if HALT_PATH.is_file():
        try:
            with open(HALT_PATH, "r") as f:
                data = json.load(f)
            print(f"  🚨 [BLOCKER] HALT-ALL active!")
            print(f"    Reason: {data.get('reason', 'n/a')}")
            print(f"    Expires: {data.get('expires_at', 'n/a')}")
        except Exception:
            print("  🚨 [BLOCKER] HALT-ALL file present but unreadable (fail-safe trigger)")
    else:
        print("    [PASS] No active HALT-ALL kill-switches.")

    if CONSCIENCE_DIR.is_dir():
        signals = list(CONSCIENCE_DIR.glob("*.signal.json"))
        active_signals = []
        for p in signals:
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                if not d.get("false_positive") and not d.get("resolved_at"):
                    active_signals.append(d)
            except Exception:
                pass
        
        if active_signals:
            print(f"  🚨 [BLOCKER] {len(active_signals)} active Conscience Signals detected:")
            for s in active_signals:
                print(f"    - [{s.get('signal_id', 'n/a')}] Severity: {s.get('weight', 0.0)} | Message: {s.get('message', 'n/a')}")
        else:
            print("    [PASS] No active Conscience Signals.")
    else:
        print("    [PASS] Conscience directory empty.")

if __name__ == "__main__":
    check_baml()
    check_learning()
    check_blockers()
