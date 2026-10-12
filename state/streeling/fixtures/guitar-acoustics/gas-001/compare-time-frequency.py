"""Run AUD-004's declared synthetic time-frequency comparison.

This is a Python reproduction of the pinned IX Hann-window/rFFT spectrogram
arithmetic, not an IX binary invocation. The Morlet-style kernel is imported
from the local GAS-001 method. The real recorded/rendered WAV follow-up is not
part of this synthetic benchmark.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.signal import fftconvolve


RATE = 44_100
SAMPLES = RATE
BASE_HZ = 82.4069
HARMONICS = (1, 2, 4)
BURST_CENTERS = (0.30, 0.45)
BURST_SECONDS = 0.040
HOP = 512
SEARCH_SECONDS = 0.060
NOISE_RMS = 0.01
SEED = 20261012
EPS = 1e-12
METHODS = ("stft_2048", "stft_8192", "morlet")
IX_SOURCE_REVISION = "bd1336b7c4045e427dcdbe80b102790e45da5ce1"
GAS_METHOD_REVISION = "5c4967454ddc740ed937c87719ca4d71a3522e4b"


def burst_signal(hz):
    signal = np.zeros(SAMPLES, dtype=np.float64)
    length = round(BURST_SECONDS * RATE)
    gate = np.hanning(length)
    centered_time = (np.arange(length) - (length - 1) / 2) / RATE
    burst = 0.5 * gate * np.cos(2 * np.pi * hz * centered_time)
    for center in BURST_CENTERS:
        start = round(center * RATE) - length // 2
        signal[start : start + length] += burst
    return signal


def stft_tracks(signal, size):
    starts = np.arange(0, len(signal) - size + 1, HOP)
    window = np.hanning(size)
    spectra = np.array([np.fft.rfft(signal[start : start + size] * window) for start in starts])
    times = (starts + (size - 1) / 2) / RATE
    tracks = {}
    bins = {}
    for harmonic in HARMONICS:
        target = harmonic * BASE_HZ
        index = round(target * size / RATE)
        tracks[harmonic] = np.abs(spectra[:, index])
        bins[harmonic] = {"index": index, "hz": index * RATE / size}
    return times, tracks, bins


def morlet_tracks(signal):
    times = np.arange(len(signal)) / RATE
    tracks = {}
    for harmonic in HARMONICS:
        center_hz = harmonic * BASE_HZ
        sigma = 6 / (2 * np.pi * center_hz)
        radius = int(np.ceil(4 * sigma * RATE))
        kernel_time = np.arange(-radius, radius + 1) / RATE
        kernel = np.exp(-0.5 * (kernel_time / sigma) ** 2) * np.exp(2j * np.pi * center_hz * kernel_time)
        kernel /= np.sqrt(np.sum(np.abs(kernel) ** 2))
        tracks[harmonic] = np.abs(fftconvolve(signal, np.conj(kernel[::-1]), mode="same"))
    return times, tracks, None


def tracks_for(signal, method):
    if method == "morlet":
        return morlet_tracks(signal)
    return stft_tracks(signal, int(method.split("_")[1]))


def gains_for(method):
    gains = {}
    for harmonic in HARMONICS:
        hz = harmonic * BASE_HZ
        samples = np.cos(2 * np.pi * hz * np.arange(SAMPLES) / RATE)
        times, tracks, _ = tracks_for(samples, method)
        steady = tracks[harmonic][(times >= 0.25) & (times <= 0.75)]
        if not len(steady):
            raise ValueError("calibration has no steady-state samples")
        gains[harmonic] = float(np.median(steady))
        if gains[harmonic] <= 0:
            raise ValueError("calibration gain must be positive")
    return gains


def interval_peak(times, values, center):
    mask = (times >= center - SEARCH_SECONDS) & (times <= center + SEARCH_SECONDS)
    indices = np.flatnonzero(mask)
    if not len(indices):
        return None
    local = values[indices]
    maximum = np.max(local)
    ties = np.flatnonzero(np.isclose(local, maximum, rtol=0, atol=1e-12))
    chosen = indices[int(ties[0])]
    return {"time_seconds": float(times[chosen]), "magnitude": float(maximum), "ties": len(ties)}


def score_trial(harmonic, method, arm, signal, noise_only, gains):
    times, raw, bins = tracks_for(signal, method)
    noise_times, noise_raw, _ = tracks_for(noise_only, method)
    normalized = {key: track / gains[key] for key, track in raw.items()}
    normalized_noise = noise_raw[harmonic] / gains[harmonic]
    if not np.array_equal(times, noise_times):
        raise ValueError("noise and trial time axes differ")
    scored = []
    for center in BURST_CENTERS:
        correct = interval_peak(times, normalized[harmonic], center)
        baseline = interval_peak(times, normalized_noise, center)
        wrong = [interval_peak(times, normalized[key], center) for key in HARMONICS if key != harmonic]
        if correct is None or baseline is None or any(item is None for item in wrong):
            raise ValueError("empty declared scoring interval")
        threshold = 0.0 if arm == "clean" else baseline["magnitude"] * 10 ** (6 / 20)
        detected = correct["magnitude"] > threshold
        largest_wrong = max(item["magnitude"] for item in wrong)
        scored.append(
            {
                "known_center_seconds": center,
                "detected": bool(detected),
                "absolute_error_ms": round(abs(correct["time_seconds"] - center) * 1000, 3) if detected else None,
                "peak_time_seconds": round(correct["time_seconds"], 6),
                "peak_over_noise_db": round(20 * np.log10((correct["magnitude"] + EPS) / (baseline["magnitude"] + EPS)), 3) if arm == "noise" else None,
                "wrong_center_separation_db": round(20 * np.log10((correct["magnitude"] + EPS) / (largest_wrong + EPS)), 3),
                "peak_ties": correct["ties"],
            }
        )
    return scored, bins


def run():
    rng = np.random.default_rng(SEED)
    gains = {method: gains_for(method) for method in METHODS}
    trials = []
    selected_bins = {}
    for harmonic in HARMONICS:
        clean = burst_signal(harmonic * BASE_HZ)
        raw_noise = rng.standard_normal(SAMPLES)
        noise = raw_noise * (NOISE_RMS / np.sqrt(np.mean(raw_noise * raw_noise)))
        for arm, signal, noise_only in (("clean", clean, np.zeros_like(clean)), ("noise", clean + noise, noise)):
            for method in METHODS:
                events, bins = score_trial(harmonic, method, arm, signal, noise_only, gains[method])
                if bins:
                    selected_bins[method] = bins
                trials.append({"harmonic": harmonic, "arm": arm, "method": method, "events": events})
    fourth = {}
    for method in METHODS:
        events = [event for trial in trials if trial["harmonic"] == 4 and trial["method"] == method for event in trial["events"]]
        errors = [event["absolute_error_ms"] for event in events if event["detected"]]
        fourth[method] = {
            "detections": len(errors),
            "total_bursts": len(events),
            "median_absolute_error_ms": float(np.median(errors)) if errors else None,
            "minimum_wrong_center_separation_db": min(event["wrong_center_separation_db"] for event in events),
        }
    morlet = fourth["morlet"]
    long_stft = fourth["stft_8192"]
    complete = all(item["detections"] == item["total_bursts"] for item in fourth.values())
    improvement = round(long_stft["median_absolute_error_ms"] - morlet["median_absolute_error_ms"], 3) if complete else None
    accepted = complete and improvement >= 5 and morlet["minimum_wrong_center_separation_db"] >= 6
    return {
        "scope": "Synthetic Python reproduction of pinned IX spectrogram arithmetic and GAS-001 Morlet kernel; not IX binary, recorded guitar, browser, or learner evidence",
        "source_revisions": {"ix_spectral_and_window": IX_SOURCE_REVISION, "gas_001_morlet_method": GAS_METHOD_REVISION},
        "implementation": {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "numpy": np.__version__, "scipy": scipy.__version__},
        "parameters": {"sample_rate": RATE, "samples_per_trial": SAMPLES, "harmonics": list(HARMONICS), "fundamental_hz": BASE_HZ, "burst_centers_seconds": BURST_CENTERS, "burst_duration_seconds": BURST_SECONDS, "burst_peak_amplitude": 0.5, "noise_rms": NOISE_RMS, "noise_seed": SEED, "stft_hop_samples": HOP, "search_radius_seconds": SEARCH_SECONDS, "noise_detection_margin_db": 6, "timing_improvement_threshold_ms": 5, "wrong_center_separation_threshold_db": 6},
        "selected_stft_bins": selected_bins,
        "calibration_gains": gains,
        "fourth_partial_summary": fourth,
        "fourth_partial_improvement_over_8192_ms": improvement,
        "proposed_claim_passes_this_synthetic_trial": bool(accepted),
        "trials": trials,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write deterministic JSON receipt to this path")
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
