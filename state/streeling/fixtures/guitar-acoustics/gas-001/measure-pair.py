"""Measure fixed GAS-001 windows; this is a teaching fixture, not a realism score."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve


TARGET_HZ = 82.4069


def load(path: Path):
    rate, samples = wavfile.read(path)
    if samples.ndim != 1:
        raise ValueError(f"expected mono audio: {path}")
    if np.issubdtype(samples.dtype, np.integer):
        samples = samples.astype(np.float64) / np.iinfo(samples.dtype).max
    else:
        samples = samples.astype(np.float64)
    return rate, samples


def rms_db(samples, rate, start, end):
    section = samples[round(start * rate) : round(end * rate)]
    return 20 * np.log10(np.sqrt(np.mean(section * section)) + 1e-12)


def partials(samples, rate, start):
    section = samples[round(start * rate) : round((start + 1.0) * rate)]
    magnitudes = np.abs(np.fft.rfft(section * np.hanning(len(section))))
    frequencies = np.fft.rfftfreq(len(section), 1 / rate)
    peaks = []
    for harmonic in range(1, 7):
        center = harmonic * TARGET_HZ
        candidates = np.flatnonzero((frequencies >= center - 8) & (frequencies <= center + 8))
        peak = candidates[np.argmax(magnitudes[candidates])]
        peaks.append((float(frequencies[peak]), float(magnitudes[peak])))
    first = peaks[0][1]
    return [
        {
            "harmonic": index + 1,
            "peak_hz": round(freq, 2),
            "db_relative_to_first": round(20 * np.log10((mag + 1e-12) / (first + 1e-12)), 1),
        }
        for index, (freq, mag) in enumerate(peaks)
    ]


def morlet_partial_tracks(samples, rate, onset):
    """Track selected partials with six-cycle complex Morlet-style wavelets."""
    segment = samples[round(onset * rate) : round((onset + 1.5) * rate)]
    tracks = []
    for harmonic in (1, 2, 4):
        center_hz = harmonic * TARGET_HZ
        sigma = 6 / (2 * np.pi * center_hz)
        radius = int(np.ceil(4 * sigma * rate))
        time = np.arange(-radius, radius + 1) / rate
        kernel = np.exp(-0.5 * (time / sigma) ** 2) * np.exp(2j * np.pi * center_hz * time)
        kernel /= np.sqrt(np.sum(np.abs(kernel) ** 2))
        envelope = np.abs(fftconvolve(segment, np.conj(kernel[::-1]), mode="same"))
        early = np.mean(envelope[round(0.2 * rate) : round(0.4 * rate)])
        late = np.mean(envelope[round(1.0 * rate) : round(1.2 * rate)])
        attack_region = envelope[: round(0.6 * rate)]
        tracks.append(
            {
                "harmonic": harmonic,
                "center_hz": round(center_hz, 2),
                "peak_time_first_0p6s": round(float(np.argmax(attack_region) / rate), 3),
                "late_minus_early_db": round(float(20 * np.log10((late + 1e-12) / (early + 1e-12))), 1),
            }
        )
    return tracks


def measure(path: Path, onset):
    rate, samples = load(path)
    early = rms_db(samples, rate, onset + 0.2, onset + 0.4)
    late = rms_db(samples, rate, onset + 1.0, onset + 1.2)
    return {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "sample_rate": int(rate),
        "duration_seconds": round(len(samples) / rate, 3),
        "peak_abs": round(float(np.max(np.abs(samples))), 4),
        "onset_seconds_approx": onset,
        "rms_dbfs_0p2_0p4_after_onset": round(float(early), 1),
        "rms_dbfs_1p0_1p2_after_onset": round(float(late), 1),
        "late_minus_early_db": round(float(late - early), 1),
        "partials_0p2_1p2_after_onset": partials(samples, rate, onset + 0.2),
        "morlet_partial_tracks": morlet_partial_tracks(samples, rate, onset),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recorded", type=Path, default=Path(__file__).with_name("deb-low-e-open.wav"))
    parser.add_argument("--synth", type=Path, default=Path(__file__).with_name("ga-engine-e2-open-4s.wav"))
    parser.add_argument("--output", type=Path, help="write the measurement JSON to this path")
    args = parser.parse_args()
    # The recorded file has a quiet lead-in and a second pluck near 2.75 s.
    # 1.1 s is an approximate first onset chosen by inspecting 0.25 s RMS bins.
    result = {"recorded": measure(args.recorded, 1.1), "ga_synth": measure(args.synth, 0.0)}
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
