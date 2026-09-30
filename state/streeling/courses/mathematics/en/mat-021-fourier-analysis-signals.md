---
module_id: mat-021-fourier-analysis-signals
department: mathematics
course: Fourier Analysis and Signals
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Fourier Analysis and Signals — What a Spectrum Shows, and What Sampling Hides

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Write the discrete Fourier transform as a change of basis, invert it, and check a spectrum with Parseval's theorem
- Derive the radix-2 fast Fourier transform, count its operations, and say why the way its twiddle factors are computed matters
- Predict where a sampled tone appears, and say what a decimator must do before it drops samples
- Explain leakage, choose a window, and tell the frequency grid apart from the frequency resolution
- Use the convolution theorem, and read the short-time Fourier transform and the Haar transform as two answers to the time–frequency trade-off
- Trace what IX's `fft`, `ix_fft`, `welch_psd`, filters, resampling and Haar denoising guarantee, and where the schema, contracts and invariants promise more than the code delivers

---

## 1. The DFT as a Change of Basis

Sample a signal N times and you get a vector x in ℂᴺ. The **discrete Fourier transform** writes it in the basis of sampled complex exponentials f_k, with entries e^(2πikn/N): X_k = Σ_n x_n e^(−2πikn/N), for k = 0, …, N − 1. Two of these vectors are orthogonal, since ⟨f_j, f_k⟩ = Σ_n e^(2πi(k−j)n/N) is a geometric sum that vanishes unless j = k, where it equals N. The matrix F with entries e^(−2πikn/N) therefore satisfies F F* = N I, so F/√N is unitary, a length-preserving change of basis in the sense of MAT-004. The inverse is x_n = (1/N) Σ_k X_k e^(2πikn/N), and **Parseval's theorem**, Σ|x_n|² = (1/N) Σ|X_k|², is that preservation of length written out.

The index k counts cycles per N samples: bin k is the frequency k/N cycles per sample, or k·fs/N at a sampling rate fs. For a real signal, X_(N−k) is the complex conjugate of X_k, so the bins N/2 + 1 to N − 1 repeat the bins N/2 − 1 down to 1: bin k in that range is the negative frequency (k − N)/N, not a frequency above one half, and in an 8-point DFT bin 5 is the frequency −3/8, the mirror of bin 3. A cosine of amplitude 1 on the grid, x_n = cos(2π·3n/8), has X_3 = X_5 = 4 and every other bin 0, and Parseval checks: Σ x_n² = 4 and (4² + 4²)/8 = 4.

### Practice Exercise

Compute the DFT of x = (1, 2, 3, 4) and check Parseval's theorem.

> *Solution:* With N = 4, e^(−2πik/4) = (−i)ᵏ. X_0 = 1 + 2 + 3 + 4 = 10, X_1 = 1 − 2i − 3 + 4i = −2 + 2i, X_2 = 1 − 2 + 3 − 4 = −2, and X_3 is the conjugate of X_1, −2 − 2i. Then Σ|X_k|² = 100 + 8 + 4 + 8 = 120, and 120/4 = 30 = 1 + 4 + 9 + 16.

---

## 2. The Fast Fourier Transform

Evaluating every X_k directly costs N² complex multiplications. Cooley and Tukey (1965), rediscovering an idea Gauss had used around 1805 (Heideman, Johnson and Burrus 1984), split the sum into even and odd samples. With E and O the DFTs of length N/2 of x_0, x_2, … and of x_1, x_3, …, and w = e^(−2πi/N),

X_k = E_k + wᵏ O_k,  X_(k+N/2) = E_k − wᵏ O_k,  for k < N/2,

a **butterfly** that uses each product twice. When N is a power of two, the split repeats log₂ N times, for (N/2) log₂ N multiplications: 5120 for N = 1024, against N² = 2^20. Reading the input in bit-reversed index order lets every stage overwrite the array in place.

The factors wᵏ are the **twiddle factors**, and the way they are computed decides the accuracy. With every twiddle accurate to a unit in the last place, the relative error of the whole FFT grows only like log₂ N times the unit roundoff (Higham 2002). Computing them by repeated multiplication, wᵏ = wᵏ⁻¹ · w, carries the rounding of each product into the next, so the error of a factor grows roughly in proportion to its index (Van Loan 1992); a table, or a direct call to cos and sin for each factor, avoids this.

A radix-2 FFT needs N to be a power of two, and a common convenience is to append zeros until it is one. The result is not the DFT of the original samples: it samples the same underlying spectrum Σ_n x_n e^(−2πifn) on the grid f = k/N′ of the padded length N′. The six samples of cos(2πn/6) have X_1 = X_5 = 3 on their own grid of sixths; padded to 8, the grid of eighths misses 1/6, and the peak spreads over the bins 1/8 and 1/4 (§6).

### Practice Exercise

Show that X_(k+N/2) = E_k − wᵏ O_k.

> *Solution:* E and O are DFTs of length N/2, so E_(k+N/2) = E_k and O_(k+N/2) = O_k. The full sum is X_k = E_k + wᵏ O_k for every k, and w^(k+N/2) = wᵏ · w^(N/2) = wᵏ · e^(−πi) = −wᵏ. Substituting k + N/2 gives X_(k+N/2) = E_k − wᵏ O_k.

---

## 3. Sampling and Aliasing

Sampling a continuous signal at the rate fs keeps the values x(n/fs). The tones e^(2πift) and e^(2πi(f + m·fs)t) agree at every sample for every integer m, and a real cosine at f also agrees with one at m·fs − f. A sampled tone is therefore known only up to these **aliases**, and it appears at the one between 0 and the **Nyquist frequency** fs/2: at |f − m·fs| for the integer m that makes it smallest. The Nyquist–Shannon theorem turns this around (Nyquist 1928; Shannon 1949): a signal with no content at or above fs/2 is determined by its samples, and x(t) = Σ_n x_n sinc(fs·t − n), with sinc(u) = sin(πu)/(πu).

**Decimation** by M keeps every M-th sample, which lowers the rate to fs/M and the Nyquist frequency to fs/(2M). Anything between fs/(2M) and fs/2 then aliases, so a decimator first removes it with a low-pass filter. At 8 kHz, a 3 kHz tone decimated by 2 without that filter is sampled at 4 kHz and appears at |3 − 4| = 1 kHz: 3/8 of the old rate becomes 1/4 of the new one.

The sinc sum has infinitely many terms, and truncating it has a cost. Midway between two samples, the 16 nearest terms for a constant signal add up to (4/π)(1 − 1/3 + 1/5 − … − 1/15) ≈ 0.9604, a partial sum of Leibniz's series for π/4, so an interpolator that keeps 8 taps on each side and no window reads a constant 5 as about 4.80 there. Practical interpolators taper the kernel with a window, and some divide by the sum of the weights so that a constant stays constant.

### Practice Exercise

A recorder samples at 8 kHz. At what frequency does a 5 kHz tone appear, and a 13 kHz one?

> *Solution:* The Nyquist frequency is 4 kHz. The 5 kHz tone appears at |5 − 8| = 3 kHz, and the 13 kHz tone at |13 − 16| = 3 kHz too: after sampling, the three tones cannot be told apart. Only a low-pass filter before the sampler can prevent this.

---

## 4. Leakage, Windows and Resolution

A tone whose frequency lies on the grid, f = k/N, puts all its energy in its two bins. Off the grid, the finite record acts as a rectangular window: the spectrum of L samples of e^(2πif₀n) is the Dirichlet kernel Σ_(n<L) e^(2πi(f₀ − f)n), whose magnitude |sin(πL(f − f₀))/sin(π(f − f₀))| has a main lobe of width 2/L between its first zeros and side lobes that decay slowly, and every bin of the DFT samples it. This is **leakage**: a strong tone raises every bin, and can hide a weak one.

Multiplying the samples by a **window** that tapers to zero at the edges lowers the side lobes at the cost of a wider main lobe (Harris 1978). Computed on 256-sample versions, the highest side lobe is at about −13 dB for the rectangle, −31 dB for Hann, −43 dB for Hamming and −58 dB for Blackman, and the main lobe of Hann is twice as wide as the rectangle's. A window also scales the peak: Hann about halves the amplitude of a tone at a bin centre, which a calibrated spectrum divides out.

Two quantities with the same unit are easy to confuse. The **grid** spacing of an N-point FFT is fs/N, and zero-padding makes it as fine as one likes. The **resolution**, the smallest separation at which two tones give two peaks, is set by the record length L, about fs/L, and padding cannot improve it. Tones at 0.20 and 0.21 cycles per sample, 32 samples long and padded to 1024, show a single peak, at 0.2051; 128 samples padded to the same 1024 show two, at 0.1992 and 0.2100 (counting the local maxima above 30% of the largest magnitude between 0.1 and 0.3).

### Practice Exercise

A recording of 32 samples at 1 kHz contains tones at 200 Hz and 210 Hz. Will zero-padding it to 1024 points separate them?

> *Solution:* No. The resolution is about fs/L = 1000/32 ≈ 31 Hz, three times the 10 Hz separation, so the two main lobes merge into one. Padding samples that merged lobe on a finer grid and still shows one peak. Separating them needs a record of more than about 100 samples, a tenth of a second; 128 samples show two peaks.

---

## 5. Convolution, the STFT and Haar Wavelets

The **convolution theorem** turns filtering into multiplication: the DFT of the circular convolution (x ⊛ h)_n = Σ_m x_m h_((n−m) mod N) is X_k H_k. A linear convolution of lengths L and M wraps its tail onto its head unless both signals are padded to at least L + M − 1 before the transforms; the FFT then computes it in O(N log N) operations instead of O(LM).

An FIR filter convolves with a finite h, so its frequency response is H(f) = Σ_k h_k e^(−2πifk). The windowed-sinc low-pass of order M takes h_k = 2f_c sinc(2f_c(k − M/2)) w_k for k = 0, …, M, symmetric about M/2, so H(f) = e^(−iπfM) A(f) with A real, close to 1 below the cutoff f_c and close to 0 above it. **Spectral inversion**, δ_(k−M/2) − h_k, turns it into a high-pass, which needs a centre tap: M must be even (see the exercise of §6).

The **short-time Fourier transform** slides a window of L samples along the signal by a hop H and takes one FFT per frame. Each frame has L/2 + 1 useful bins spaced fs/L apart and covers L/fs seconds, so a longer window sharpens frequency and blurs time, and no choice of L improves both: the product of the two resolutions is bounded below (Gabor 1946). Welch's method averages the squared magnitudes of overlapping windowed frames to lower the variance of a spectrum estimate (Welch 1967). Scaled as a density, a one-sided estimate doubles every bin except 0 and L/2, because a real signal's power is split evenly between f and −f; the density then integrates to the signal's power.

The **Haar transform** takes the other road to time–frequency analysis. It maps each pair of samples to a scaled sum and difference, a_i = (x_(2i) + x_(2i+1))/√2 and d_i = (x_(2i) − x_(2i+1))/√2, then repeats on the sums: after L levels, the details describe changes at the scales 2, 4, …, 2ᴸ, each localised in time (Haar 1910; Mallat 1989). The transform is orthonormal, so it preserves energy. Soft thresholding replaces each detail d by sign(d) max(|d| − t, 0), which removes small fluctuations and shrinks the large ones (Donoho 1995), and when the length is a multiple of 2ᴸ it never raises the variance (see the exercise).

### Practice Exercise

Show that soft-thresholding the details of a Haar transform never raises the variance of a signal whose length is a multiple of 2ᴸ.

> *Solution:* The transform is orthonormal, so the energy Σ x_n² equals the sum of the squares of the final approximations and of all the details; thresholding shrinks every |d| and leaves the approximations alone, so the energy cannot grow. At each level, the synthesis turns a_i and d_i into (a_i + d_i)/√2 and (a_i − d_i)/√2, whose sum √2·a_i does not involve d_i, so the sum of the signal, and with it the mean, depends only on the final approximations and does not change. The variance is the energy divided by n minus the squared mean: the first term cannot grow and the second is fixed.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of `fft.rs`, `spectral.rs`, `sampling.rs`, `filter.rs` and `wavelet.rs` in `crates/ix-signal`, of the handlers below, of the DuckDB function `ix_wavelet_denoise` and of `analyze_metric_spectrum`, checked against NumPy's FFT. These numbers are predictions, and §7 proposes to check them.

**The transform and its tool.** [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L86) appends zeros up to [the next power of two](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L87) and runs a radix-2 transform whose stages compute their twiddle factors with:

```rust
        let w_base = Complex::new(angle.cos(), angle.sin());

        for start in (0..n).step_by(len) {
            let mut w = Complex::new(1.0, 0.0);
            for k in 0..half {
                let even = data[start + k];
                let odd = data[start + k + half] * w;
                data[start + k] = even + odd;
                data[start + k + half] = even - odd;
                w = w * w_base;
            }
        }
```

The MCP tool `ix_fft` calls [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1299), which runs:

```rust
    let spectrum = ix_signal::fft::rfft(&signal);
    let magnitudes = ix_signal::fft::magnitude_spectrum(&spectrum);
    let n = spectrum.len();
    // Frequency bins assuming sample_rate=1.0 (normalized)
    let frequencies: Vec<f64> = (0..n).map(|k| k as f64 / n as f64).collect();
```

- **`ix_fft` ignores the `inverse` it advertises.** Its schema offers [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L74), described as ["If true, compute the inverse FFT"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L77), and asks for a signal whose [length must be a power of 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L71). The handler never reads the flag, pads other lengths silently and reports the padded length as `fft_size`. It returns magnitudes only, and labels bin k with k/n for every k, so for cos(2π·3n/8) it reports magnitude 4 at 0.375 and again at 0.625, which is the negative frequency −0.375 and not a second tone. With `inverse` true the output is the same.
- **Padding changes the grid without a warning.** The library's contracts [state that it pads](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L8). The six samples of cos(2πn/6) come back as eight bins, with 2.5156 at 1/8 and 2.2361 at 1/4, where the six-point DFT has 3 at 1/6. IX's guide gives the frequency resolution as the sampling rate divided by the FFT size N, and says that ["Larger N = finer frequency resolution"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/signal-processing/fft-intuition.md#L122), which holds when N counts samples and not when padding makes N larger (§4). In `crates/ix-code`, [`analyze_metric_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L159) takes a dominant period from the [padded FFT](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L173): a series of period 6 reads as 16/3 ≈ 5.33 with 12 samples and as 32/5 = 6.4 with 24. Only its own tests call it.
- **The twiddle factors drift.** Each stage computes one factor with cos and sin and the others by [repeated multiplication](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L178). On x_n = sin n + ½ cos 3n, the transcription differs from NumPy's FFT by a relative error of order 10^-15 at N = 2^8, 10^-14 at N = 2^12 and 10^-13 at N = 2^16, where the same code with every twiddle computed directly stays of order 10^-15. The contracts say that the twiddles come from [`f64::cos/sin`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L39) and that platforms may round them differently "at ULP scale"; the recurrence spreads such a difference over the whole transform, and moving the cosine or the sine that seeds every stage by one unit in the last place gives errors at N = 2^16 anywhere between 10^-13 and 10^-11.
- **The Parseval test holds only because its signal has length 8.** [`test_parsevals_theorem`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L236) divides the spectral energy by [`signal.len()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L241), where the identity needs the padded length. For (1, −1, 2, −2, 3, −3), Σ x² = 28 and the test's formula gives 28 · 8/6 = 112/3. The inverse pads too: [`ifft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L96) appends zeros after the last bin, so the six-bin DFT of (1, 2, 3, 4, 5, 6) comes back as eight complex values that start 0.75, 2.1301 + 0.4949i, not as the six samples.
- **`welch_psd` can loop forever, and reports half the power.** [`welch_psd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L57) sets [`hop = window_size - overlap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L63): an overlap equal to the window never advances the loop, and a larger one underflows the unsigned subtraction, a panic in a debug build. Its one-sided estimate [adds each squared magnitude once](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L80), without the doubling of §5, so for the sine of its own test, of power 0.5, the estimate integrates to 0.25. With a window of 500 samples, `rfft` pads each frame to 512 while the [frequency labels](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L95) divide by 500: the peak of a 100 Hz tone sampled at 1 kHz falls in bin 51, at 51 × 1000/512 ≈ 99.6 Hz, and is labelled 102 Hz. Its [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L124) uses a window of 512 samples, and nothing else calls it; the `ix_spectrogram` handler does reject a window that is not a [power of two](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1159).
- **Decimation and resampling do not low-pass.** [`decimate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L6) does what [its comment says](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L5), "take every M-th sample": 64 samples of cos(2π·3n/8) decimated by 2 put their peak at bin 8 of 32, the frequency 1/4 of §3. [`resample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L42) evaluates the sinc sum with 8 taps on each side and no window, although [its comment](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L20) says "windowed sinc": a constant 5 comes back as 4.80 at a half-integer position, and resampling 100 samples of it to 30 gives values from 4.739 to 5.152. Its [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L83) resamples 100 samples to 50, where every position is an integer and the interpolation reproduces the samples up to rounding. Neither function has a caller outside its tests.
- **An odd order breaks the high-pass.** The FIR design documents that the order ["Must be even."](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L16), but the `ix_fir_filter` handler only checks that it is [at least 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L809). The high-pass puts its centre tap at [`order / 2`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L42) rounded down, so an odd order inverts the low-pass about the wrong sample: at cutoff 0.25, a tone at 0.1 cycles per sample passes with gain 0.3132 at order 31, against 0.0012 at order 32.
- **The DuckDB wavelet denoiser breaks its invariant.** `ix_wavelet_denoise` promises that the [output variance does not exceed the input's](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L306), which §5 proves for lengths that are multiples of 2^levels. For other lengths it [repeats the last value](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L335) up to such a multiple, denoises, and truncates. On (0, 0, 0, 0, 1, 2) with 2 levels and threshold 1, the padding (2, 2) is averaged with the tail, and the output is (0, 0, 0, 0, 1.75, 1.75): the variance rises from 7/12 to 49/72, by a factor 7/6. Its [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L739) uses 8 samples, where nothing is padded, and the MCP handler [rejects](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L776) such lengths instead.
- **The contracts and comments drift from the code.** The crate's [module list](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/lib.rs#L9) and [its wavelet module](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L3) announce Daubechies wavelets; only Haar exists. The contracts say that [`wavelet::dwt_haar`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L14) panics on a length that is not a power of two: the function is `haar_dwt`, and it [drops the last sample](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L7) of an odd block without an error. They say that [`correlation::auto_correlation`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L17) is unnormalised, while `autocorrelation` [divides by the zero-lag value](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/correlation.rs#L12), and that an [empty FFT input panics](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L31), which the parenthesis of the same line contradicts: `fft` returns one zero. The catalogue that `ix_explain_algorithm` sends lists the FFT's hyperparameters as [`["window", "n_points"]`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5841); `ix_fft` takes neither.
- **Other gaps.** There is no FFT for lengths that are not powers of two (mixed radix or Bluestein), no inverse transform or phase over MCP, no decimator with an anti-aliasing filter, no windowed or normalised resampler, no density scaling for one-sided spectra, and no wavelet other than Haar.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Show that spectral inversion of a windowed-sinc low-pass of odd order M, with the centre tap placed at (M − 1)/2, has a gain of about 2|sin(πf/2)| where the low-pass passes, and compare with IX's order-31 filter at f = 0.1.

> *Solution:* The low-pass is symmetric about M/2, so H(f) = e^(−iπfM) A(f) with A real. With the tap at m = (M − 1)/2, the inverted filter has G(f) = e^(−2πifm) − H(f) = e^(−iπfM)(e^(iπf) − A(f)). Where the low-pass passes, A(f) ≈ 1, so |G(f)| ≈ |e^(iπf) − 1| = 2|sin(πf/2)|, which is 0.3129 at f = 0.1; IX's filter has 0.3132, the difference coming from A(0.1) not being exactly 1. With M even, m = M/2 and G(f) = e^(−iπfM)(1 − A(f)), which is close to 0 there.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **Inverse.** Call the `fft` handler on the eight samples of cos(2π·3n/8), with `inverse` false, then true. Prediction: the same output twice, magnitude 4 at 0.375 and at 0.625 and 0 elsewhere, with `fft_size` 8.
2. **Grid.** Call `rfft` on the six samples of cos(2πn/6), and `analyze_metric_spectrum` on sin(2πi/6) for 12, then 24 samples. Prediction: eight bins, of magnitude 2.5156 at bin 1 and 2.2361 at bin 2; dominant periods 16/3 and 32/5.
3. **Accuracy.** Compare `rfft` of x_n = sin n + ½ cos 3n with an accurate FFT at N = 2^8, 2^12 and 2^16. Prediction: relative errors of order 10^-15 and 10^-14, then between 10^-13 and 10^-11; the digits vary with the platform's cos and sin.
4. **Welch.** Call `welch_psd` on the sine of its test with a window of 512 and an overlap of 256, then with 500 and 250; then with an overlap of 512, in a child process with a time limit. Prediction: the estimate times the bin width 1000/512 sums to 0.25; the peak of the second call is labelled 102 Hz; the third call does not return.
5. **Sampling.** Decimate 64 samples of cos(2π·3n/8) by 2 and take `rfft`; interpolate 100 samples of the constant 5 at 50.5 with 8 taps; resample them to 30. Prediction: a peak of 16 at bin 8 of 32; 4.80; values from 4.739 to 5.152.
6. **High-pass.** Call the `fir_filter` handler with kind highpass and cutoff 0.25 on 256 samples of cos(2π·0.1n), with order 31, then 32. Prediction: the largest magnitude of the output after sample 64 is 0.309, then 0.0012.
7. **Wavelets.** Run `ix_wavelet_denoise` in DuckDB on (0, 0, 0, 0, 1, 2) with 2 levels and threshold 1, then on the series of its test. Prediction: a population variance of 49/72 ≈ 0.6806 against the input's 7/12 ≈ 0.5833; then 0, since the threshold removes every detail of the test's series.

### Practice Exercise

In step 4, why does the one-sided estimate integrate to half the power, and what fixes it?

> *Solution:* For a real signal |X_(N−k)| = |X_k|, so the bins k and N − k carry equal power, and Parseval's theorem counts both. Keeping only the bins 0 to N/2 drops the negative-frequency half of every interior bin. Doubling the bins 1 to N/2 − 1 restores it; the bins 0 and N/2 have no mirror and stay single. For a sine, whose power sits in two mirrored bins, the undoubled sum is exactly half.

---

## 8. Common Pitfalls

- **Reading the bins above N/2 as high frequencies.** For a real signal they mirror the negative frequencies; keep the bins 0 to N/2, or relabel bin k as k − N.
- **Taking a finer grid for a finer resolution.** Zero-padding interpolates the spectrum; only a longer record separates close tones.
- **Decimating without a low-pass.** Filter below the new Nyquist frequency first, or the discarded band folds onto the kept one.
- **Comparing peak heights across windows or lengths.** A window scales the peak, Hann by about one half, and leakage spreads an off-grid tone; divide by the window's sum, or compare energies.
- **Forgetting a scaling convention.** Check where the 1/N goes, and whether a one-sided spectrum doubles its interior bins, with Parseval's theorem on a known signal.
- **Multiplying spectra without padding.** Pad to at least L + M − 1, or the product computes a circular convolution that wraps the tail onto the head.
- **Inverting a low-pass of odd order.** Use an even order, so that the centre tap exists.
- **Trusting a radix-2 routine with an arbitrary length.** Check the returned length, since padding changes the grid and the normalisation.
- **Padding before a wavelet transform.** Edge padding changes the statistics of the last block; report which samples were padded, or trim to a multiple of 2^levels.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Discrete Fourier transform** | The coefficients X_k = Σ x_n e^(−2πikn/N) of a signal in the basis of sampled complex exponentials |
| **Parseval's theorem** | ‖x‖² = (1/N) ‖X‖²: the transform preserves energy up to the factor N |
| **Fast Fourier transform** | An algorithm that computes the DFT in O(N log N) operations by splitting it recursively |
| **Twiddle factor** | A power of e^(−2πi/N) that multiplies the odd half in a butterfly |
| **Nyquist frequency** | Half the sampling rate, the highest frequency that sampling represents without ambiguity |
| **Aliasing** | The appearance of a tone above the Nyquist frequency at a lower frequency with the same samples |
| **Spectral leakage** | The spread of an off-grid tone's energy over every bin of a finite DFT |
| **Window** | A taper applied to the samples before a transform, trading side-lobe level for main-lobe width |
| **Frequency resolution** | The smallest separation at which two tones give distinct peaks, about the sampling rate divided by the record length |
| **Convolution theorem** | The DFT of a circular convolution is the product of the DFTs |
| **Short-time Fourier transform** | A sequence of windowed FFTs over sliding frames, showing how a spectrum changes over time |
| **Haar transform** | The orthonormal wavelet transform built from scaled pairwise sums and differences |

---

## Self-Check Assessment

**1. `ix_fft` returns magnitude 4 at 0.375 and at 0.625 for an eight-sample signal, and 0 elsewhere. How many tones does the signal contain?**
> One real tone, at 0.375 cycles per sample. For a real signal the bin at 0.625 = 1 − 0.375 is the mirror of the bin at 0.375, the negative frequency −0.375; the tool labels every bin k/n, including those above one half.

**2. A colleague zero-pads 32 samples to 1024 points, sees one peak at 0.2051, and concludes that the signal holds a single tone. What do you answer?**
> That the data cannot tell. The resolution of 32 samples is about 1/32 of a cycle per sample, and two tones 0.01 apart merge into one main lobe; padding only samples that lobe more finely. A longer record, 128 samples here, separates tones at 0.20 and 0.21.

**3. You need to bring 48 kHz audio down to 8 kHz with IX. What must happen before `decimate` with factor 6?**
> A low-pass filter below the new Nyquist frequency, 4 kHz, that is 1/12 of the old rate, since `decimate` only drops samples and anything between 4 and 24 kHz would alias. With `ix_fir_filter`, use kind lowpass, a cutoff somewhat below 1/12 and an even order.

**4. A DuckDB query shows `ix_wavelet_denoise` raising the variance of a series of six values. Is the Haar transform broken?**
> No. On a length that is a multiple of 2^levels, Haar soft thresholding cannot raise the variance (§5). The function edge-pads the series up to such a length and truncates the result, and the padding moves mass into the kept samples. Trim or pad the series yourself and check which samples changed, or use the MCP tool, which rejects such lengths.

**Pass criteria:** Write the DFT as a change of basis and check a spectrum with Parseval's theorem; derive the radix-2 FFT and explain the role of its twiddle factors; predict where a sampled tone appears and what a decimator must do first; explain leakage, choose a window and separate the grid from the resolution; use the convolution theorem and compare the STFT with the Haar transform; and trace where IX's schema, contracts, invariants and tests promise more than the code delivers.

---

## Research Basis

- J. Fourier, *Théorie analytique de la chaleur*, Firmin Didot, 1822: trigonometric series
- A. Haar, "Zur Theorie der orthogonalen Funktionensysteme", *Mathematische Annalen* 69, 1910: the Haar system
- H. Nyquist, "Certain topics in telegraph transmission theory", *Transactions of the AIEE* 47, 1928: the sampling rate needed for a band
- D. Gabor, "Theory of communication", *Journal of the Institution of Electrical Engineers* 93, 1946: the time–frequency uncertainty
- C. E. Shannon, "Communication in the presence of noise", *Proceedings of the IRE* 37, 1949: the sampling theorem and sinc reconstruction
- J. W. Cooley and J. W. Tukey, "An algorithm for the machine calculation of complex Fourier series", *Mathematics of Computation* 19, 1965: the FFT
- P. D. Welch, "The use of fast Fourier transform for the estimation of power spectra: a method based on time averaging over short, modified periodograms", *IEEE Transactions on Audio and Electroacoustics* 15, 1967: Welch's method
- F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform", *Proceedings of the IEEE* 66, 1978: windows and their side lobes
- M. T. Heideman, D. H. Johnson and C. S. Burrus, "Gauss and the history of the fast Fourier transform", *IEEE ASSP Magazine* 1, 1984: the FFT before 1965
- S. G. Mallat, "A theory for multiresolution signal decomposition: the wavelet representation", *IEEE Transactions on Pattern Analysis and Machine Intelligence* 11, 1989: multiresolution analysis
- C. Van Loan, *Computational Frameworks for the Fast Fourier Transform*, SIAM, 1992: the computation of twiddle factors and its errors
- D. L. Donoho, "De-noising by soft-thresholding", *IEEE Transactions on Information Theory* 41, 1995: soft thresholding
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002: the error analysis of the FFT
- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Prentice Hall, 2010: sampling, windows, the STFT and filter design
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
