---
module_id: mat-021-fourier-analysis-signals
department: mathematics
course: Análisis de Fourier y señales
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Análisis de Fourier y señales — Lo que muestra un espectro, y lo que oculta el muestreo

> **Departamento de Matemáticas** | Etapa: Albedo (Intermedio) | Duración estimada: 50 minutos

## Objetivos

Al terminar esta lección, podrás:
- Escribir la transformada discreta de Fourier como un cambio de base, invertirla, y comprobar un espectro con el teorema de Parseval
- Obtener la transformada rápida de Fourier en base 2, contar sus operaciones, y decir por qué importa cómo se calculan sus factores de giro
- Predecir dónde aparece un tono muestreado, y decir qué debe hacer un diezmador antes de descartar muestras
- Explicar la fuga espectral, elegir una ventana, y distinguir la rejilla de frecuencias de la resolución en frecuencia
- Usar el teorema de convolución, y leer la transformada de Fourier de tiempo corto y la transformada de Haar como dos respuestas al compromiso tiempo–frecuencia
- Rastrear lo que garantizan `fft`, `ix_fft`, `welch_psd`, los filtros, el remuestreo y la eliminación de ruido de Haar de IX, y dónde el esquema, los contratos y los invariantes prometen más de lo que el código entrega

---

## 1. La TDF como cambio de base

Muestrea una señal N veces y obtienes un vector x de ℂᴺ. La **transformada discreta de Fourier** (TDF) lo escribe en la base de las exponenciales complejas muestreadas f_k, de entradas e^(2πikn/N): X_k = Σ_n x_n e^(−2πikn/N), para k = 0, …, N − 1. Dos de estos vectores son ortogonales, ya que ⟨f_j, f_k⟩ = Σ_n e^(2πi(k−j)n/N) es una suma geométrica que se anula salvo si j = k, donde vale N. La matriz F de entradas e^(−2πikn/N) cumple por tanto F F* = N I, así que F/√N es unitaria, un cambio de base que conserva las longitudes en el sentido de MAT-004. La inversa es x_n = (1/N) Σ_k X_k e^(2πikn/N), y el **teorema de Parseval**, Σ|x_n|² = (1/N) Σ|X_k|², es esa conservación de las longitudes escrita explícitamente.

El índice k cuenta ciclos por N muestras: el bin k es la frecuencia k/N ciclos por muestra, o k·fs/N a una frecuencia de muestreo fs. Para una señal real, X_(N−k) es el conjugado de X_k, así que los bins N/2 + 1 a N − 1 repiten los bins N/2 − 1 a 1: son las frecuencias negativas −k/N, no frecuencias por encima de un medio. Un coseno de amplitud 1 en la rejilla, x_n = cos(2π·3n/8), tiene X_3 = X_5 = 4 y todos los demás bins nulos, y Parseval se cumple: Σ x_n² = 4 y (4² + 4²)/8 = 4.

### Ejercicio práctico

Calcula la TDF de x = (1, 2, 3, 4) y comprueba el teorema de Parseval.

> *Solución:* Con N = 4, e^(−2πik/4) = (−i)ᵏ. X_0 = 1 + 2 + 3 + 4 = 10, X_1 = 1 − 2i − 3 + 4i = −2 + 2i, X_2 = 1 − 2 + 3 − 4 = −2, y X_3 es el conjugado de X_1, −2 − 2i. Entonces Σ|X_k|² = 100 + 8 + 4 + 8 = 120, y 120/4 = 30 = 1 + 4 + 9 + 16.

---

## 2. La transformada rápida de Fourier

Evaluar directamente cada X_k cuesta N² multiplicaciones complejas. Cooley y Tukey (1965), redescubriendo una idea que Gauss había usado hacia 1805 (Heideman, Johnson y Burrus 1984), separan la suma en muestras pares e impares. Con E y O las TDF de longitud N/2 de x_0, x_2, … y de x_1, x_3, …, y w = e^(−2πi/N),

X_k = E_k + wᵏ O_k,  X_(k+N/2) = E_k − wᵏ O_k,  para k < N/2,

una **mariposa** que usa cada producto dos veces. Cuando N es una potencia de dos, la separación se repite log₂ N veces, para (N/2) log₂ N multiplicaciones: 5120 para N = 1024, frente a N² = 2^20. Leer la entrada en el orden de índices con bits invertidos permite que cada etapa sobrescriba el arreglo en su lugar.

Los factores wᵏ son los **factores de giro**, y la forma de calcularlos decide la precisión. Con cada factor exacto a un ulp (una unidad en la última cifra), el error relativo de toda la FFT solo crece como log₂ N veces la unidad de redondeo (Higham 2002). Calcularlos por multiplicaciones repetidas, wᵏ = wᵏ⁻¹ · w, arrastra el redondeo de cada producto al siguiente, así que el error de un factor crece más o menos en proporción a su índice (Van Loan 1992); una tabla, o una llamada directa a cos y sin para cada factor, lo evita.

Una FFT en base 2 necesita que N sea una potencia de dos, y una comodidad habitual es añadir ceros hasta que lo sea. El resultado no es la TDF de las muestras originales: muestrea el mismo espectro subyacente Σ_n x_n e^(−2πifn) en la rejilla f = k/N′ de la longitud rellenada N′. Las seis muestras de cos(2πn/6) tienen X_1 = X_5 = 3 en su propia rejilla de sextos; rellenadas hasta 8, la rejilla de octavos no contiene 1/6, y el pico se reparte entre los bins 1/8 y 1/4 (§6).

### Ejercicio práctico

Demuestra que X_(k+N/2) = E_k − wᵏ O_k.

> *Solución:* E y O son TDF de longitud N/2, así que E_(k+N/2) = E_k y O_(k+N/2) = O_k. La suma completa es X_k = E_k + wᵏ O_k para todo k, y w^(k+N/2) = wᵏ · w^(N/2) = wᵏ · e^(−πi) = −wᵏ. Sustituir k por k + N/2 da X_(k+N/2) = E_k − wᵏ O_k.

---

## 3. Muestreo y aliasing

Muestrear una señal continua a la tasa fs conserva los valores x(n/fs). Los tonos e^(2πift) y e^(2πi(f + m·fs)t) coinciden en cada muestra para todo entero m, y un coseno real en f coincide también con uno en m·fs − f. Un tono muestreado solo se conoce, por tanto, salvo estos **alias**, y aparece en el que está entre 0 y la **frecuencia de Nyquist** fs/2: en |f − m·fs| para el entero m que lo hace mínimo. El teorema de Nyquist–Shannon da la vuelta a esto (Nyquist 1928; Shannon 1949): una señal sin contenido en fs/2 o por encima queda determinada por sus muestras, y x(t) = Σ_n x_n sinc(fs·t − n), con sinc(u) = sin(πu)/(πu).

El **diezmado** por M conserva una muestra de cada M, lo que baja la tasa a fs/M y la frecuencia de Nyquist a fs/(2M). Todo lo que esté entre fs/(2M) y fs/2 se solapa entonces, así que un diezmador lo elimina primero con un filtro paso bajo. A 8 kHz, un tono de 3 kHz diezmado por 2 sin ese filtro queda muestreado a 4 kHz y aparece en |3 − 4| = 1 kHz: 3/8 de la tasa antigua se convierte en 1/4 de la nueva.

La suma de sinc tiene infinitos términos, y truncarla tiene un coste. A medio camino entre dos muestras, los 16 términos más cercanos para una señal constante suman (4/π)(1 − 1/3 + 1/5 − … − 1/15) ≈ 0.9604, una suma parcial de la serie de Leibniz para π/4, así que un interpolador que conserva 8 coeficientes a cada lado y ninguna ventana lee ahí una constante 5 como unos 4.80. Los interpoladores prácticos atenúan el núcleo con una ventana, y algunos dividen por la suma de los pesos para que una constante siga siendo constante.

### Ejercicio práctico

Una grabadora muestrea a 8 kHz. ¿En qué frecuencia aparece un tono de 5 kHz, y uno de 13 kHz?

> *Solución:* La frecuencia de Nyquist es 4 kHz. El tono de 5 kHz aparece en |5 − 8| = 3 kHz, y el de 13 kHz en |13 − 16| = 3 kHz también: tras el muestreo, los tres tonos no se pueden distinguir. Solo un filtro paso bajo antes del muestreador puede evitarlo.

---

## 4. Fuga espectral, ventanas y resolución

Un tono cuya frecuencia cae en la rejilla, f = k/N, pone toda su energía en sus dos bins. Fuera de la rejilla, el registro finito actúa como una ventana rectangular: el espectro de L muestras de e^(2πif₀n) es el núcleo de Dirichlet Σ_(n<L) e^(2πi(f₀ − f)n), cuyo módulo |sin(πL(f − f₀))/sin(π(f − f₀))| tiene un lóbulo principal de anchura 2/L entre sus primeros ceros y lóbulos laterales que decaen despacio, y cada bin de la TDF lo muestrea. Esto es la **fuga espectral**: un tono fuerte eleva todos los bins, y puede ocultar uno débil.

Multiplicar las muestras por una **ventana** que se estrecha hacia cero en los bordes baja los lóbulos laterales a costa de un lóbulo principal más ancho (Harris 1978). Calculado sobre versiones de 256 muestras, el lóbulo lateral más alto está a unos −13 dB para el rectángulo, −31 dB para Hann, −43 dB para Hamming y −58 dB para Blackman, y el lóbulo principal de Hann es el doble de ancho que el del rectángulo. Una ventana también escala el pico: Hann reduce más o menos a la mitad la amplitud de un tono en el centro de un bin, lo que un espectro calibrado compensa.

Dos magnitudes con la misma unidad se confunden fácilmente. El paso de la **rejilla** de una FFT de N puntos es fs/N, y el relleno con ceros lo hace tan fino como se quiera. La **resolución**, la menor separación a la que dos tonos dan dos picos, la fija la longitud L del registro, unos fs/L, y el relleno no puede mejorarla. Tonos en 0.20 y 0.21 ciclos por muestra, de 32 muestras y rellenados hasta 1024, muestran un solo pico, en 0.2051; 128 muestras rellenadas hasta los mismos 1024 muestran dos, en 0.1992 y 0.2100 (contando los máximos locales por encima del 30 % del mayor módulo entre 0.1 y 0.3).

### Ejercicio práctico

Una grabación de 32 muestras a 1 kHz contiene tonos de 200 Hz y 210 Hz. ¿Los separará rellenarla con ceros hasta 1024 puntos?

> *Solución:* No. La resolución es de unos fs/L = 1000/32 ≈ 31 Hz, tres veces la separación de 10 Hz, así que los dos lóbulos principales se funden en uno. El relleno muestrea ese lóbulo fundido en una rejilla más fina y sigue mostrando un solo pico. Separarlos requiere un registro de más de unas 100 muestras, una décima de segundo; 128 muestras muestran dos picos.

---

## 5. Convolución, STFT y ondículas de Haar

El **teorema de convolución** convierte el filtrado en multiplicación: la TDF de la convolución circular (x ⊛ h)_n = Σ_m x_m h_((n−m) mod N) es X_k H_k. Una convolución lineal de longitudes L y M pliega su cola sobre su cabeza a menos que ambas señales se rellenen hasta al menos L + M − 1 antes de las transformadas; la FFT la calcula entonces en O(N log N) operaciones en lugar de O(LM).

Un filtro FIR convoluciona con un h finito, así que su respuesta en frecuencia es H(f) = Σ_k h_k e^(−2πifk). El paso bajo de sinc enventanado de orden M toma h_k = 2f_c sinc(2f_c(k − M/2)) w_k para k = 0, …, M, simétrico respecto a M/2, así que H(f) = e^(−iπfM) A(f) con A real, cercano a 1 por debajo de la frecuencia de corte f_c y cercano a 0 por encima. La **inversión espectral**, δ_(k−M/2) − h_k, lo convierte en un paso alto, lo que requiere un coeficiente central: M debe ser par (ver el ejercicio del §6).

La **transformada de Fourier de tiempo corto** (STFT) desliza una ventana de L muestras a lo largo de la señal con un salto H y calcula una FFT por trama. Cada trama tiene L/2 + 1 bins útiles separados fs/L y cubre L/fs segundos, así que una ventana más larga afina la frecuencia y emborrona el tiempo, y ninguna elección de L mejora ambas: el producto de las dos resoluciones está acotado inferiormente (Gabor 1946). El método de Welch promedia los módulos al cuadrado de tramas enventanadas que se solapan para reducir la varianza de una estimación del espectro (Welch 1967). Escalada como densidad, una estimación unilateral duplica cada bin salvo 0 y L/2, porque la potencia de una señal real se reparte por igual entre f y −f; la integral de la densidad es entonces la potencia de la señal.

La **transformada de Haar** toma el otro camino hacia el análisis tiempo–frecuencia. Lleva cada par de muestras a una suma y una diferencia escaladas, a_i = (x_(2i) + x_(2i+1))/√2 y d_i = (x_(2i) − x_(2i+1))/√2, y repite sobre las sumas: tras L niveles, los detalles describen los cambios en las escalas 2, 4, …, 2ᴸ, cada uno localizado en el tiempo (Haar 1910; Mallat 1989). La transformada es ortonormal, así que conserva la energía. La umbralización suave sustituye cada detalle d por sign(d) max(|d| − t, 0), lo que elimina las fluctuaciones pequeñas y reduce las grandes (Donoho 1995), y cuando la longitud es múltiplo de 2ᴸ nunca aumenta la varianza (ver el ejercicio).

### Ejercicio práctico

Demuestra que umbralizar suavemente los detalles de una transformada de Haar nunca aumenta la varianza de una señal cuya longitud es múltiplo de 2ᴸ.

> *Solución:* La transformada es ortonormal, así que la energía Σ x_n² es igual a la suma de los cuadrados de las aproximaciones finales y de todos los detalles; la umbralización reduce cada |d| y deja intactas las aproximaciones, así que la energía no puede crecer. En cada nivel, la síntesis convierte a_i y d_i en (a_i + d_i)/√2 y (a_i − d_i)/√2, cuya suma √2·a_i no contiene d_i, así que la suma de la señal, y con ella la media, solo depende de las aproximaciones finales y no cambia. La varianza es la energía dividida por n menos el cuadrado de la media: el primer término no puede crecer y el segundo está fijo.

---

## 6. Dónde está IX

IX es la biblioteca de aprendizaje automático en Rust del ecosistema GuitarAlchemist. Los hechos siguientes se leen en su código en el commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); esta lección documenta ese código y no lo modifica, y no ha ejecutado ni IX ni sus pruebas. Los números atribuidos al comportamiento de IX proceden de una transcripción línea a línea a Python de `fft.rs`, `spectral.rs`, `sampling.rs`, `filter.rs` y `wavelet.rs` en `crates/ix-signal`, de los manejadores de abajo, de la función DuckDB `ix_wavelet_denoise` y de `analyze_metric_spectrum`, comprobada frente a la FFT de NumPy. Estos números son predicciones, y el §7 propone comprobarlos.

**La transformada y su herramienta.** [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L86) añade ceros hasta [la siguiente potencia de dos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L87) y ejecuta una transformada en base 2 cuyas etapas calculan sus factores de giro con:

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

La herramienta MCP `ix_fft` llama a [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1299), que ejecuta:

```rust
    let spectrum = ix_signal::fft::rfft(&signal);
    let magnitudes = ix_signal::fft::magnitude_spectrum(&spectrum);
    let n = spectrum.len();
    // Frequency bins assuming sample_rate=1.0 (normalized)
    let frequencies: Vec<f64> = (0..n).map(|k| k as f64 / n as f64).collect();
```

- **`ix_fft` ignora el `inverse` que anuncia.** Su esquema ofrece [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L74), descrito como [«If true, compute the inverse FFT»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L77), y pide una señal cuya [longitud debe ser una potencia de 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L71). El manejador nunca lee el indicador, rellena en silencio las demás longitudes e informa de la longitud rellenada como `fft_size`. Solo devuelve módulos, y etiqueta el bin k con k/n para todo k, así que para cos(2π·3n/8) informa de un módulo 4 en 0.375 y otra vez en 0.625, que es la frecuencia negativa −0.375 y no un segundo tono. Con `inverse` a verdadero, la salida es la misma.
- **El relleno cambia la rejilla sin avisar.** Los contratos de la biblioteca [dicen que rellena](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L8). Las seis muestras de cos(2πn/6) vuelven como ocho bins, con 2.5156 en 1/8 y 2.2361 en 1/4, donde la TDF de seis puntos tiene 3 en 1/6. La guía de IX da la resolución en frecuencia como la frecuencia de muestreo dividida por el tamaño N de la FFT, y dice que [«Larger N = finer frequency resolution»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/signal-processing/fft-intuition.md#L122), lo que vale cuando N cuenta muestras y no cuando el relleno agranda N (§4). En `crates/ix-code`, [`analyze_metric_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L159) toma un período dominante de la [FFT rellenada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L173): una serie de período 6 se lee como 16/3 ≈ 5.33 con 12 muestras y como 32/5 = 6.4 con 24. Solo sus propias pruebas la llaman.
- **Los factores de giro derivan.** Cada etapa calcula un factor con cos y sin y los demás por [multiplicaciones repetidas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L178). Sobre x_n = sin n + ½ cos 3n, la transcripción difiere de la FFT de NumPy en un error relativo del orden de 10^-15 en N = 2^8, 10^-14 en N = 2^12 y 10^-13 en N = 2^16, donde el mismo código con cada factor calculado directamente se queda en el orden de 10^-15. Los contratos dicen que los factores vienen de [`f64::cos/sin`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L39) y que las plataformas pueden redondearlos de forma distinta «at ULP scale»; la recurrencia extiende tal diferencia a toda la transformada, y mover en un ulp el coseno o el seno que inicia cada etapa da en N = 2^16 errores en cualquier punto entre 10^-13 y 10^-11.
- **La prueba de Parseval solo se cumple porque su señal tiene longitud 8.** [`test_parsevals_theorem`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L236) divide la energía espectral por [`signal.len()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L241), donde la identidad necesita la longitud rellenada. Para (1, −1, 2, −2, 3, −3), Σ x² = 28 y la fórmula de la prueba da 28 · 8/6 = 112/3. La inversa también rellena: [`ifft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L96) añade ceros tras el último bin, así que la TDF de seis bins de (1, 2, 3, 4, 5, 6) vuelve como ocho valores complejos que empiezan por 0.75, 2.1301 + 0.4949i, y no como las seis muestras.
- **`welch_psd` puede quedarse en un bucle infinito, e informa de la mitad de la potencia.** [`welch_psd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L57) fija [`hop = window_size - overlap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L63): un solapamiento igual a la ventana nunca hace avanzar el bucle, y uno mayor produce un desbordamiento por abajo en la resta sin signo, un pánico en una compilación de depuración. Su estimación unilateral [suma cada módulo al cuadrado una sola vez](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L80), sin la duplicación del §5, así que para la sinusoide de su propia prueba, de potencia 0.5, la integral de la estimación es 0.25. Con una ventana de 500 muestras, `rfft` rellena cada trama hasta 512 mientras que las [etiquetas de frecuencia](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L95) dividen por 500: el pico de un tono de 100 Hz muestreado a 1 kHz cae en el bin 51, en 51 × 1000/512 ≈ 99.6 Hz, y se etiqueta como 102 Hz. Su [prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L124) usa una ventana de 512 muestras, y nada más la llama; el manejador `ix_spectrogram`, en cambio, rechaza una ventana que no sea una [potencia de dos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1159).
- **El diezmado y el remuestreo no filtran.** [`decimate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L6) hace lo que [dice su comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L5), «take every M-th sample»: 64 muestras de cos(2π·3n/8) diezmadas por 2 ponen su pico en el bin 8 de 32, la frecuencia 1/4 del §3. [`resample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L42) evalúa la suma de sinc con 8 coeficientes a cada lado y ninguna ventana, aunque [su comentario](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L20) dice «windowed sinc»: una constante 5 vuelve como 4.80 en una posición semientera, y remuestrear 100 muestras de ella a 30 da valores de 4.739 a 5.152. Su [prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L83) remuestrea 100 muestras a 50, donde cada posición es entera y la interpolación reproduce las muestras salvo redondeo. Ninguna de las dos funciones tiene llamadas fuera de sus pruebas.
- **Un orden impar rompe el paso alto.** El diseño FIR documenta que el orden [«Must be even.»](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L16), pero el manejador `ix_fir_filter` solo comprueba que sea [al menos 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L809). El paso alto pone su coeficiente central en [`order / 2`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L42) redondeado hacia abajo, así que un orden impar invierte el paso bajo alrededor de la muestra equivocada: con corte 0.25, un tono de 0.1 ciclos por muestra pasa con ganancia 0.3132 en el orden 31, frente a 0.0012 en el orden 32.
- **El eliminador de ruido por ondículas de DuckDB rompe su invariante.** `ix_wavelet_denoise` promete que la [varianza de salida no supera la de la entrada](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L306), lo que el §5 demuestra para longitudes múltiplo de 2^levels. Para otras longitudes [repite el último valor](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L335) hasta tal múltiplo, elimina el ruido y trunca. Sobre (0, 0, 0, 0, 1, 2) con 2 niveles y umbral 1, el relleno (2, 2) se promedia con el final, y la salida es (0, 0, 0, 0, 1.75, 1.75): la varianza sube de 7/12 a 49/72, un factor 7/6. Su [prueba](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L739) usa 8 muestras, donde no se rellena nada, y el manejador MCP [rechaza](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L776) tales longitudes en su lugar.
- **Los contratos y los comentarios se apartan del código.** La [lista de módulos](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/lib.rs#L9) de la crate y [su módulo de ondículas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L3) anuncian ondículas de Daubechies; solo existe Haar. Los contratos dicen que [`wavelet::dwt_haar`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L14) entra en pánico con una longitud que no es potencia de dos: la función se llama `haar_dwt`, y [descarta la última muestra](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L7) de un bloque impar sin error. Dicen que [`correlation::auto_correlation`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L17) no está normalizada, mientras que `autocorrelation` [divide por el valor en el desfase cero](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/correlation.rs#L12), y que una [entrada vacía de la FFT entra en pánico](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L31), lo que contradice el paréntesis de la misma línea: `fft` devuelve un único cero. El catálogo que envía `ix_explain_algorithm` enumera los hiperparámetros de la FFT como [`["window", "n_points"]`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5841); `ix_fft` no toma ninguno de los dos.
- **Otras lagunas.** No hay FFT para longitudes que no sean potencias de dos (base mixta o Bluestein), ni transformada inversa ni fase por MCP, ni diezmador con filtro antialiasing, ni remuestreador enventanado o normalizado, ni escalado de densidad para espectros unilaterales, ni otra ondícula que Haar.

Corregir todo esto corresponde a los responsables de IX; esta lección solo lo describe.

### Ejercicio práctico

Demuestra que la inversión espectral de un paso bajo de sinc enventanado de orden impar M, con el coeficiente central colocado en (M − 1)/2, tiene una ganancia de unos 2|sin(πf/2)| donde el paso bajo deja pasar, y compárala con el filtro de orden 31 de IX en f = 0.1.

> *Solución:* El paso bajo es simétrico respecto a M/2, así que H(f) = e^(−iπfM) A(f) con A real. Con el coeficiente en m = (M − 1)/2, el filtro invertido tiene G(f) = e^(−2πifm) − H(f) = e^(−iπfM)(e^(iπf) − A(f)). Donde el paso bajo deja pasar, A(f) ≈ 1, así que |G(f)| ≈ |e^(iπf) − 1| = 2|sin(πf/2)|, que vale 0.3129 en f = 0.1; el filtro de IX tiene 0.3132, y la diferencia viene de que A(0.1) no vale exactamente 1. Con M par, m = M/2 y G(f) = e^(−iπfM)(1 − A(f)), que ahí está cerca de 0.

---

## 7. Experimento propuesto (aún no ejecutado)

**Estado: no ejecutado.** Esta sección propone un experimento para el laboratorio de Learn, que fija IX en el mismo commit. Nada en ella es una medición: las predicciones se escriben antes de cualquier ejecución, y una versión posterior de esta lección informará de los resultados. Cada paso se ejecuta en el propio proceso del laboratorio y llama directamente a las funciones, nunca a un servidor MCP en funcionamiento.

1. **Inversa.** Llama al manejador `fft` sobre las ocho muestras de cos(2π·3n/8), con `inverse` a falso, y luego a verdadero. Predicción: la misma salida dos veces, módulo 4 en 0.375 y en 0.625 y 0 en el resto, con `fft_size` igual a 8.
2. **Rejilla.** Llama a `rfft` sobre las seis muestras de cos(2πn/6), y a `analyze_metric_spectrum` sobre sin(2πi/6) con 12 y luego 24 muestras. Predicción: ocho bins, de módulo 2.5156 en el bin 1 y 2.2361 en el bin 2; períodos dominantes 16/3 y 32/5.
3. **Precisión.** Compara `rfft` de x_n = sin n + ½ cos 3n con una FFT precisa en N = 2^8, 2^12 y 2^16. Predicción: errores relativos del orden de 10^-15 y 10^-14, y luego entre 10^-13 y 10^-11; las cifras varían con el cos y el sin de la plataforma.
4. **Welch.** Llama a `welch_psd` sobre la sinusoide de su prueba con una ventana de 512 y un solapamiento de 256, luego con 500 y 250; luego con un solapamiento de 512, en un proceso hijo con límite de tiempo. Predicción: la estimación multiplicada por la anchura de bin 1000/512 suma 0.25; el pico de la segunda llamada se etiqueta como 102 Hz; la tercera llamada no termina.
5. **Muestreo.** Diezma 64 muestras de cos(2π·3n/8) por 2 y toma `rfft`; interpola 100 muestras de la constante 5 en 50.5 con 8 coeficientes; remuestréalas a 30. Predicción: un pico de 16 en el bin 8 de 32; 4.80; valores de 4.739 a 5.152.
6. **Paso alto.** Llama al manejador `fir_filter` con kind igual a highpass y cutoff 0.25 sobre 256 muestras de cos(2π·0.1n), con orden 31 y luego 32. Predicción: el mayor módulo de la salida tras la muestra 64 es 0.309, y luego 0.0012.
7. **Ondículas.** Ejecuta `ix_wavelet_denoise` en DuckDB sobre (0, 0, 0, 0, 1, 2) con 2 niveles y umbral 1, y luego sobre la serie de su prueba. Predicción: una varianza poblacional de 49/72 ≈ 0.6806 frente a 7/12 ≈ 0.5833 de la entrada; luego 0, ya que el umbral elimina todos los detalles de la serie de la prueba.

### Ejercicio práctico

En el paso 4, ¿por qué la integral de la estimación unilateral es la mitad de la potencia, y qué lo corrige?

> *Solución:* Para una señal real |X_(N−k)| = |X_k|, así que los bins k y N − k llevan la misma potencia, y el teorema de Parseval cuenta ambos. Conservar solo los bins 0 a N/2 pierde la mitad de frecuencia negativa de cada bin interior. Duplicar los bins 1 a N/2 − 1 la restituye; los bins 0 y N/2 no tienen espejo y quedan simples. Para una sinusoide, cuya potencia está en dos bins espejo, la suma sin duplicar es exactamente la mitad.

---

## 8. Errores comunes

- **Leer los bins por encima de N/2 como frecuencias altas.** Para una señal real reflejan las frecuencias negativas; conserva los bins 0 a N/2, o renumera el bin k como k − N.
- **Tomar una rejilla más fina por una resolución más fina.** El relleno con ceros interpola el espectro; solo un registro más largo separa tonos cercanos.
- **Diezmar sin paso bajo.** Filtra primero por debajo de la nueva frecuencia de Nyquist, o la banda descartada se pliega sobre la conservada.
- **Comparar alturas de pico entre ventanas o longitudes.** Una ventana escala el pico, Hann en torno a la mitad, y la fuga reparte un tono fuera de la rejilla; divide por la suma de la ventana, o compara energías.
- **Olvidar una convención de escala.** Comprueba dónde va el 1/N, y si un espectro unilateral duplica sus bins interiores, con el teorema de Parseval sobre una señal conocida.
- **Multiplicar espectros sin relleno.** Rellena hasta al menos L + M − 1, o el producto calcula una convolución circular que pliega la cola sobre la cabeza.
- **Invertir un paso bajo de orden impar.** Usa un orden par, para que exista el coeficiente central.
- **Fiarse de una rutina en base 2 con una longitud cualquiera.** Comprueba la longitud devuelta, ya que el relleno cambia la rejilla y la normalización.
- **Rellenar antes de una transformada de ondículas.** El relleno por repetición del borde cambia la estadística del último bloque; indica qué muestras se rellenaron, o recorta a un múltiplo de 2^levels.

---

## Términos clave

| Término | Definición |
|------|-----------|
| **Transformada discreta de Fourier** | Los coeficientes X_k = Σ x_n e^(−2πikn/N) de una señal en la base de las exponenciales complejas muestreadas |
| **Teorema de Parseval** | ‖x‖² = (1/N) ‖X‖²: la transformada conserva la energía salvo el factor N |
| **Transformada rápida de Fourier** | Un algoritmo que calcula la TDF en O(N log N) operaciones dividiéndola recursivamente |
| **Factor de giro** | Una potencia de e^(−2πi/N) que multiplica la mitad impar en una mariposa |
| **Frecuencia de Nyquist** | La mitad de la frecuencia de muestreo, la frecuencia más alta que el muestreo representa sin ambigüedad |
| **Aliasing** | La aparición de un tono situado por encima de la frecuencia de Nyquist en una frecuencia más baja que tiene las mismas muestras |
| **Fuga espectral** | El reparto de la energía de un tono fuera de la rejilla entre todos los bins de una TDF finita |
| **Ventana** | Una ponderación aplicada a las muestras antes de una transformada, que cambia nivel de los lóbulos laterales por anchura del lóbulo principal |
| **Resolución en frecuencia** | La menor separación a la que dos tonos dan picos distintos, más o menos la frecuencia de muestreo dividida por la longitud del registro |
| **Teorema de convolución** | La TDF de una convolución circular es el producto de las TDF |
| **Transformada de Fourier de tiempo corto** | Una sucesión de FFT enventanadas sobre tramas deslizantes, que muestra cómo cambia un espectro con el tiempo |
| **Transformada de Haar** | La transformada de ondículas ortonormal construida con sumas y diferencias escaladas de pares |

---

## Autoevaluación

**1. `ix_fft` devuelve un módulo 4 en 0.375 y en 0.625 para una señal de ocho muestras, y 0 en el resto. ¿Cuántos tonos contiene la señal?**
> Un solo tono real, en 0.375 ciclos por muestra. Para una señal real, el bin en 0.625 = 1 − 0.375 es el espejo del bin en 0.375, la frecuencia negativa −0.375; la herramienta etiqueta cada bin con k/n, incluidos los que están por encima de un medio.

**2. Alguien de tu equipo rellena con ceros 32 muestras hasta 1024 puntos, ve un solo pico en 0.2051, y concluye que la señal contiene un solo tono. ¿Qué le respondes?**
> Que los datos no permiten saberlo. La resolución de 32 muestras es de unos 1/32 de ciclo por muestra, y dos tonos a 0.01 de distancia se funden en un solo lóbulo principal; el relleno solo muestrea ese lóbulo con más finura. Un registro más largo, aquí de 128 muestras, separa tonos en 0.20 y 0.21.

**3. Necesitas bajar audio de 48 kHz a 8 kHz con IX. ¿Qué debe ocurrir antes de `decimate` con factor 6?**
> Un filtro paso bajo por debajo de la nueva frecuencia de Nyquist, 4 kHz, es decir 1/12 de la tasa antigua, ya que `decimate` solo descarta muestras y todo lo que esté entre 4 y 24 kHz se solaparía. Con `ix_fir_filter`, usa kind igual a lowpass, un corte algo por debajo de 1/12 y un orden par.

**4. Una consulta de DuckDB muestra que `ix_wavelet_denoise` aumenta la varianza de una serie de seis valores. ¿Está rota la transformada de Haar?**
> No. Con una longitud múltiplo de 2^levels, la umbralización suave de Haar no puede aumentar la varianza (§5). La función rellena la serie repitiendo el borde hasta tal longitud y trunca el resultado, y el relleno desplaza masa a las muestras conservadas. Recorta o rellena la serie por tu cuenta y comprueba qué muestras cambiaron, o usa la herramienta MCP, que rechaza tales longitudes.

**Criterio de aprobación:** Escribir la TDF como un cambio de base y comprobar un espectro con el teorema de Parseval; obtener la FFT en base 2 y explicar el papel de sus factores de giro; predecir dónde aparece un tono muestreado y qué debe hacer primero un diezmador; explicar la fuga espectral, elegir una ventana y distinguir la rejilla de la resolución; usar el teorema de convolución y comparar la STFT con la transformada de Haar; y rastrear dónde el esquema, los contratos, los invariantes y las pruebas de IX prometen más de lo que el código entrega.

---

## Base de investigación

- J. Fourier, *Théorie analytique de la chaleur*, Firmin Didot, 1822: las series trigonométricas
- A. Haar, «Zur Theorie der orthogonalen Funktionensysteme», *Mathematische Annalen* 69, 1910: el sistema de Haar
- H. Nyquist, «Certain topics in telegraph transmission theory», *Transactions of the AIEE* 47, 1928: la tasa de muestreo necesaria para una banda
- D. Gabor, «Theory of communication», *Journal of the Institution of Electrical Engineers* 93, 1946: la incertidumbre tiempo–frecuencia
- C. E. Shannon, «Communication in the presence of noise», *Proceedings of the IRE* 37, 1949: el teorema de muestreo y la reconstrucción con sinc
- J. W. Cooley y J. W. Tukey, «An algorithm for the machine calculation of complex Fourier series», *Mathematics of Computation* 19, 1965: la FFT
- P. D. Welch, «The use of fast Fourier transform for the estimation of power spectra: a method based on time averaging over short, modified periodograms», *IEEE Transactions on Audio and Electroacoustics* 15, 1967: el método de Welch
- F. J. Harris, «On the use of windows for harmonic analysis with the discrete Fourier transform», *Proceedings of the IEEE* 66, 1978: las ventanas y sus lóbulos laterales
- M. T. Heideman, D. H. Johnson y C. S. Burrus, «Gauss and the history of the fast Fourier transform», *IEEE ASSP Magazine* 1, 1984: la FFT antes de 1965
- S. G. Mallat, «A theory for multiresolution signal decomposition: the wavelet representation», *IEEE Transactions on Pattern Analysis and Machine Intelligence* 11, 1989: el análisis multirresolución
- C. Van Loan, *Computational Frameworks for the Fast Fourier Transform*, SIAM, 1992: el cálculo de los factores de giro y sus errores
- D. L. Donoho, «De-noising by soft-thresholding», *IEEE Transactions on Information Theory* 41, 1995: la umbralización suave
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2.ª ed., SIAM, 2002: el análisis de errores de la FFT
- A. V. Oppenheim y R. W. Schafer, *Discrete-Time Signal Processing*, 3.ª ed., Prentice Hall, 2010: muestreo, ventanas, la STFT y el diseño de filtros
- Código fuente de IX en el commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: cada hecho de código del §6 enlaza a su línea
- Experimento: propuesto en el §7, no ejecutado; esta lección no contiene ninguna medición
- Procedencia: redactado a mano por una sesión de Claude Code (Opus 5.5) a partir del plan de currículo de Streeling, no producido por el pipeline de cursos Seldon; en revisión
- Estado de creencia: T(0.85) F(0.02) U(0.10) C(0.03)
