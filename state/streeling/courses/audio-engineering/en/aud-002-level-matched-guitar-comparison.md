---
module_id: aud-002-level-matched-guitar-comparison
department: audio-engineering
course: "Compare a GA Guitar Render at Matched Playback Level"
level: intermediate
prerequisites: [gas-001-open-string-audio-evidence]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-002
version: "0.1.0"
---

# Compare a GA Guitar Render at Matched Playback Level

> **Department of Audio Engineering** | Level: Intermediate | Estimated duration: 30 minutes | Status: English draft; review and publication pending

## Objectives

After this lesson, you will be able to:

- Preserve the identity and provenance of the recorded and rendered WAVs before making playback copies.
- Align the first note events and derive an approximate gain match from the same post-onset RMS window.
- Explain why a matched early level does not make two envelopes or timbres equal.
- State a falsifiable audio comparison and a bounded, blinded listening plan.

## The project question

GA's native Rust guitar engine rendered an open E2. A separate recorded open E2 is the teaching reference. If listeners hear the GA file much louder, can they fairly judge its tone against the recording? No: playback level and timing are part of the comparison setup. [GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) introduces the broad evidence path from recording to engine experiment. AUD-002 concentrates on the **audio-engineering gate before an A/B judgment**: lock the sources, align the first events, match one stated level window, and preserve what that match does not control. It does not teach the FFT, STFT, or wavelet theory behind the fixture measurements.

This case is pinned to Demerzel source revision `5c4967454ddc740ed937c87719ca4d71a3522e4b`. The [GAS-001 fixture record](../../../fixtures/guitar-acoustics/gas-001/README.md) identifies the source files, license, render settings, hashes, measurement script, and limitations. Both WAVs are four seconds, mono, 44,100 Hz. The recorded file is attributed to collegefishiesd under CC BY-SA 4.0 and labeled `low_E`, open fret, E2 by the dataset. The GA WAV is a native render of the pinned Rust source, **not** a captured browser AudioWorklet output. A listening verdict on this pair would therefore not validate browser playback.

### Practice exercise 1: lock the inputs

The fixture README gives `deb-low-e-open.wav` SHA-256 `03a1965f…7f38b248` and `ga-engine-e2-open-4s.wav` SHA-256 `a78a7024…7866c3f98`. An editor exports a louder MP3 and replaces the GA WAV in the fixture directory. Can the existing measurements and provenance still be used unchanged?

> **Answer:** No. Keep the original WAVs and their full hashes as immutable inputs. Put any gained, trimmed, or encoded playback copy at a new path with its transformation and hash. Replacing the file breaks the connection between the recorded measurement, render settings, and bytes; lossy MP3 also changes the signal. The fixture README supplies the full hashes and attribution.

## 1. Align the event, not the file header

The [measurement script](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) uses approximate first onsets of **1.1 seconds** for the recording and **0.0 seconds** for the GA render. The recorded file has a quiet lead-in and another attack near **2.75 seconds**. Choose equal-length excerpts starting at their respective first onsets. A proposed 1.5-second first-note excerpt covers recorded file time **1.1–2.6 seconds** and render file time **0.0–1.5 seconds**; it stops before the second recorded attack. Use the same boundary fade on listening copies and state it in the session log. The onset markers are estimates, so inspect the waveform and repeat key measurements after a small marker shift before treating a borderline difference as stable.

For the fixture's existing numbers, the early RMS window is **0.2–0.4 seconds after each first onset**. That means recorded file time **1.3–1.5 seconds** and render file time **0.2–0.4 seconds**. The later check is **1.0–1.2 seconds after onset**, or recorded file time **2.1–2.3 seconds** and render file time **1.0–1.2 seconds**. These windows occur before the recording's second attack. They are measurement windows, not proof that the two performances have identical pluck timing.

### Practice exercise 2: choose the actual windows

An analyst compares both files from absolute file time 0.2–0.4 seconds and calls the reference “silent.” Give the corrected early and later file-time windows for each WAV.

> **Answer:** Relative to the approximate first onsets, early is 1.3–1.5 seconds in the recording and 0.2–0.4 seconds in the render; later is 2.1–2.3 seconds in the recording and 1.0–1.2 seconds in the render. The reference's 0.2–0.4-second file segment is part of its lead-in, so it is the wrong comparison window.

## 2. Match one level window without erasing the result

The pinned [measurement JSON](../../../fixtures/guitar-acoustics/gas-001/measurements.json) reports early-window RMS of **−34.6 dBFS** for the recording and **−16.6 dBFS** for the GA render. The render is **18.0 dB higher** in this *specific aligned window*. To match that window approximately, attenuate a **playback copy** of the GA render by 18.0 dB, an amplitude multiplier of `10^(-18/20) ≈ 0.126`. Leave the source WAVs unchanged. The fixture records whole-file absolute peaks of 0.1297 for the recording and 0.4602 for the render; after this uniform attenuation, the render copy's peak would be about `0.4602 × 0.126 ≈ 0.058`, before any other processing. This is a predicted gain-only value, not a measured new file.

Do not simply raise the recording by 18 dB: its recorded whole-file peak of 0.1297 would scale to about **1.03** in normalized amplitude, risking clipping in a fixed-point export. Attenuating the louder arm is the straightforward safe choice for this pair. Record the gain, units, channel/sample-rate handling, trim/fade, and output hash. When a meter reports a different level after export, stop and investigate before listening.

This early-window RMS match is an **operational control**, not perceptual loudness equality. A listener can still hear different attacks, spectral balance, room/microphone coloration, and decay. A single scalar gain cannot repair those differences. For a longer clip or different task, select and justify a more suitable loudness method; do not silently switch method midway through a candidate comparison.

### Practice exercise 3: calculate the playback gain

Using the pinned −34.6 and −16.6 dBFS early RMS values, calculate the GA playback-copy gain in dB and its approximate linear amplitude multiplier. Does that gain establish that the GA engine is now as realistic as the recording?

> **Answer:** `−34.6 − (−16.6) = −18.0 dB` applied to the GA copy, or `10^(−18/20) ≈ 0.126` times its sample amplitudes. This matches one measured RMS window approximately. It does not equalize timbre, attack, decay, the recording chain, or perceived realism.

## 3. Check the remaining mismatch and listen blind

The same measurement JSON reports later RMS of **−38.5 dBFS** for the recording and **−17.7 dBFS** for the raw render. Applying the same −18.0 dB gain predicts **−35.7 dBFS** for the render's later window, still **2.8 dB above** the recording's later RMS. Equivalently, the recorded file falls **3.9 dB** between the early and later windows while the render falls **1.1 dB**. Uniform gain leaves each file's within-file change intact. This does not prove which note sounds more natural; it identifies an envelope difference under the fixture's approximate onset and chosen windows.

For a listening check, prepare lossless first-note copies from the pinned WAVs. Apply documented gain and matching trim/fade; verify the resulting early levels and absence of clipping. Randomize A/B identity and order, hide file names and waveforms, keep playback chain and volume fixed, and record each listener's response before revealing identities. Ask a specific question such as which version sounds more like a single played open E2, plus a free-text reason. Record the number of listeners and trials, their experience, conditions, and disagreements. No such blind listening result is in the fixture. Even a preference for the recording would mix performance, instrument, microphone, room, processing, and synthesis differences; it would not isolate one GA engine parameter.

### Practice exercise 4: test what matching did not fix

After applying −18.0 dB to the GA copy, what later-window RMS is predicted? How far is it from the recording's later window, and which comparison claim fails?

> **Answer:** The render's later value becomes approximately `−17.7 − 18.0 = −35.7 dBFS`, which is `−35.7 − (−38.5) = 2.8 dB` higher than the recorded later window. The claim “matching early RMS also matches the later envelope” fails for these rounded fixture measurements. This is not a listening verdict.

## 4. Make the next change falsifiable

The baseline's 2.8 dB early-to-late mismatch offers a measurable starting point, not an automatic optimization target. A proposed engine change should declare its parameter diff, GA source revision, render settings, new WAV hash, and a predeclared window and onset policy. One **illustrative, unapproved** rule could require a new candidate to reduce the absolute early-to-late difference below **1.8 dB** (at least 1.0 dB less than this baseline), retain an E2 peak under the same method, avoid clipping, and survive a separately recorded blinded preference check. The 1.8 dB threshold is a teaching choice, not a GA acceptance standard or a perceptual threshold. A candidate that misses any predeclared condition fails that proposed gate; a pass on this one E2 would still not establish general guitar realism.

### Practice exercise 5: state a falsifier

An agent claims that a new GA brightness setting improves the rendered guitar because one spectral value moved closer to the reference. Give a falsifiable next comparison using this fixture, and state what result would reject the claim.

> **Answer:** Freeze the reference and baseline hashes, render one documented candidate from a pinned GA revision, apply the same onset/excerpt and early-level matching method to baseline and candidate, then compare the declared later-window gap, peak/pitch checks, and blinded listener responses. Under the **illustrative** gate above, a candidate with a gap of 1.8 dB or more, clipping, a failed E2 check, or no supported listener preference does not pass. No candidate run or listener result is claimed here; one moved spectral feature alone does not establish an improvement.

## Key takeaways

- Hash and retain the original recorded and rendered WAVs; transform new copies for listening.
- Align to the first onset before choosing the same relative windows.
- A fixed gain can match one RMS window while leaving a measured 2.8 dB later-window difference.
- Blind labels reduce expectation bias but cannot remove source, performance, microphone, or room differences.
- Decide the measurement and listening gates before testing a candidate, then report both passes and failures.

## Project evidence and limits

- Pinned Demerzel revision `5c4967454ddc740ed937c87719ca4d71a3522e4b`: [fixture provenance and license](../../../fixtures/guitar-acoustics/gas-001/README.md), [recorded WAV](../../../fixtures/guitar-acoustics/gas-001/deb-low-e-open.wav), [GA native-rendered WAV](../../../fixtures/guitar-acoustics/gas-001/ga-engine-e2-open-4s.wav), [measurement code](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py), and [measurement output](../../../fixtures/guitar-acoustics/gas-001/measurements.json). The two WAV hashes were checked against the README and JSON. These are fixed lesson inputs, not browser-WASM captures.
- All gain, peak, and later-window calculations in this lesson are derived from the fixture's rounded numbers. No gained WAV or blind listening session was produced for AUD-002. The onset positions are approximate, and early-window RMS is only one possible level-matching rule.
- These source-relative WAV links resolve in Demerzel; a Learn publication must package the audio or provide stable public asset links.
- This English draft has no completed subject, fluent-language, learner, Learn sync/build, or anonymous public readback gate.
