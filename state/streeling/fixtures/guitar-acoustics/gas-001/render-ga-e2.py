"""Render the GAS-001 E2 fixture with a native build of GA's pinned Rust engine.

Build GA's Rust/guitar-web-wasm-demo/rust-engine at commit
dc2e74cbd992a298f67efb928b5b3754615e1924 with `cargo build --release`,
then pass the resulting guitar_engine shared library to this script.
"""

import argparse
import ctypes
import hashlib
import struct
import wave
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", required=True, type=Path, help="native guitar_engine shared library")
    parser.add_argument("--output", required=True, type=Path, help="output PCM16 WAV path")
    args = parser.parse_args()

    engine_lib = ctypes.CDLL(str(args.library.resolve()))
    engine_lib.engine_init.argtypes = [ctypes.c_float]
    engine_lib.engine_init.restype = ctypes.c_void_p
    engine_lib.engine_note_on.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
    engine_lib.engine_render.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_size_t]

    sample_rate = 44100
    frames = 4 * sample_rate
    engine = engine_lib.engine_init(ctypes.c_float(sample_rate))
    if not engine:
        raise RuntimeError("GA engine_init returned null")
    # Default guitar profile 0; one E2 note at a velocity below the output limiter.
    engine_lib.engine_note_on(engine, ctypes.c_float(82.4069), ctypes.c_float(0.1))
    buffer = (ctypes.c_float * frames)()
    engine_lib.engine_render(engine, buffer, frames)

    pcm = [int(round(max(-1.0, min(1.0, sample)) * 32767.0)) for sample in buffer]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(struct.pack("<" + "h" * frames, *pcm))

    print(args.output)
    print("sha256", hashlib.sha256(args.output.read_bytes()).hexdigest())
    print("peak", max(abs(sample) for sample in buffer))


if __name__ == "__main__":
    main()
